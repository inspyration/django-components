"""Admin IHM"""


from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register

from menu.models import MenuItem


@register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    """
    ## MenuItem admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = MenuItem
    fields = ("parent", "screen", "label", "icon", "order")
    list_display = ("parent", "screen", "label", "icon")
    search_fields = ("parent__label", "screen__label", "label")
    list_filter = ("parent", "screen", "child_set")
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
