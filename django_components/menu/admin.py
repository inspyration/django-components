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
    fields = ("parent", "screen", "title", "icon")
    list_display = ("parent", "screen", "title", "icon")
    search_fields = ("parent__title", "screen__title", "title")
    list_filter = ("parent", "screen", "child_set")
    list_display_links = ("title",)

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
