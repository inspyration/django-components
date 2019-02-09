from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


register = template.Library()


def context_to_dict(context):
    result = {}
    for d in context.dicts:
        result.update(d)
    return result


@register.simple_tag(takes_context=True, name='component')
def render_component(context, block):
    screen = context.get("screen")
    if screen is None:
        return _("This screen does not exist")
    return mark_safe(screen.render_component(block, **context_to_dict(context)))


@register.simple_tag(takes_context=True, name='page')
def render_page(context):
    screen = context.get("screen")
    if screen is None:
        return _("This screen does not exist")
    return mark_safe(screen.render_page(**context_to_dict(context)))
