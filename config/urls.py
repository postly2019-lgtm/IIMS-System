from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from intelligence_agent import views as agent_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('intelligence/', include('intelligence.urls')),
    path('agent/', include('intelligence_agent.urls')), # AI Agent URLs
    path('health/llm/', agent_views.llm_health_check),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
