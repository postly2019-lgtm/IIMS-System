from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import IntelligenceReport, Entity

@login_required
def graph_data_api(request):
    """
    Returns nodes and edges for the intelligence graph.
    """
    nodes = []
    edges = []
    
    # Track added nodes to avoid duplicates
    added_nodes = set()
    
    # 1. Add Reports
    try:
        limit = int(request.GET.get('limit', '150'))
    except ValueError:
        limit = 150
    reports = IntelligenceReport.objects.all().order_by('-published_at')[:limit]
    reports = reports.prefetch_related('entities', 'related_reports', 'source')
    
    for report in reports:
        # Report Node
        if f"rep_{report.id}" not in added_nodes:
            nodes.append({
                'id': f"rep_{report.id}",
                'label': report.title[:20] + "...",
                'fullLabel': report.title,
                'group': 'report',
                'classification': report.classification,
                'value': 20 # Size
            })
            added_nodes.add(f"rep_{report.id}")
        
        # 2. Link Report to Source (Optional: Source Node)
        # For now, let's stick to Report-Entity and Report-Report
        
        # 3. Entities
        for entity in report.entities.all():
            if f"ent_{entity.id}" not in added_nodes:
                nodes.append({
                    'id': f"ent_{entity.id}",
                    'label': entity.name,
                    'group': 'entity',
                    'type': entity.entity_type,
                    'value': 10
                })
                added_nodes.add(f"ent_{entity.id}")
            
            # Edge: Report -> Entity
            edges.append({
                'from': f"rep_{report.id}",
                'to': f"ent_{entity.id}",
                'arrows': 'to',
                'color': {'color': '#64748b'} # Slate 500
            })
            
        # 4. Related Reports
        for related in report.related_reports.all():
            # Only add if the other node exists (or will exist) - simpler to just add edge
            # We assume bidirectional, so we might duplicate edges, but vis.js handles this or we can filter
            if report.id < related.id: # Avoid double edges
                edges.append({
                    'from': f"rep_{report.id}",
                    'to': f"rep_{related.id}",
                    'arrows': {'to': {'enabled': False}}, # Undirected for similarity
                    'color': {'color': '#ef4444', 'opacity': 0.6}, # Red for relation
                    'dashes': True
                })

    return JsonResponse({'nodes': nodes, 'edges': edges})
