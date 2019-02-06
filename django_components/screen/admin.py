"""Admin IHM"""


from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.admin.decorators import register

from screen.models import Screen, Layout


class LayoutInline(StackedInline):
    """Layout inline class"""

    model = Layout
    fields = ("component", "block", "order")
    readonly_fields = ()
    min_num = 1
    extra = 0


@register(Screen)
class ScreenAdmin(ModelAdmin):
    """
    ## Screen admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = Screen
    fields = ("comprehensive", "label", "icon", "hide_in_sitemap")
    list_display = ("comprehensive", "label", "icon")
    search_fields = ("parent__label", "comprehensive__label", "label")
    list_filter = ("comprehensive", "specific_set")
    list_display_links = ("label",)
    inlines = [LayoutInline]

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
