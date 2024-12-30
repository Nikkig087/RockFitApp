from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def csp_nonce(context):
    return context.get('csrf_token')
