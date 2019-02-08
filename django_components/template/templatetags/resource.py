from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.inclusion_tag('template/resource.html')
def display_resource(resource):
    return {
        "label": resource.label,
        "tag": resource.tag.label,
        "enter": resource.browser.enter,
        "exit": resource.browser.exit,
        "path": resource.path,
    }
