from django import template
from django.template.defaultfilters import stringfilter
import markdown as md
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='render_markdown')
@stringfilter
def render_markdown(value):
    try:
        return mark_safe(md.markdown(value, extensions=['fenced_code', 'tables']))
    except Exception as e:
        return value
