"""Admin IHM"""


from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.admin.decorators import register

from component.models import Component


@register(Component)
class ComponentAdmin(ModelAdmin):
    """
    ## Component admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = Component
    fields = ("view_class", "content_type", "label", "path", "kwargs")
    list_display = ("view_class", "content_type", "label", "path")
    search_fields = ("view_class", "content_type", "label", "path")
    list_filter = ("view_class", "content_type")
    list_display_links = ("label",)

    def has_module_permission(self, request):
        """Can be accessed from home page"""
        return True

    def has_add_permission(self, request):
        """Can add an object"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Cannot delete an object"""
        return True

    def has_change_permission(self, request, obj=None):
        """Cannot change an object"""
        return True

    def has_view_permission(self, request, obj=None):
        """Can view an object"""
        return True
