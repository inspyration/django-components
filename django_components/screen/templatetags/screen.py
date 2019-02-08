from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.simple_tag(name='component')
def render_component(screen, block, **context):
    if screen is None:
        return _("This screen does not exist")
    return mark_safe(screen.render_component(block, **context))


@register.simple_tag(name='page')
def render_page(screen, **context):
    if screen is None:
        return _("This screen does not exist")
    return mark_safe(screen.render_page(**context))
