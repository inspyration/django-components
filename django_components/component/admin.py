"""Admin IHM"""


from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.admin.decorators import register

from component.models import Component, Screen, Layout


@register(Component)
class ComponentAdmin(ModelAdmin):
    """
    ## Component admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = Component
    fields = ("view_class", "content_type", "name", "path", "kwargs")
    list_display = ("view_class", "content_type", "name", "path")
    search_fields = ("view_class", "content_type", "name", "path")
    list_filter = ("view_class", "content_type")
    list_display_links = ("name",)

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
    fields = ("parent", "comprehensive", "title", "icon",
              "visible_in_sitemap", "visible_in_breadcrumb", "use_comprehensive_in_breadcrumb", "visible_in_menu")
    list_display = ("parent", "comprehensive", "title", "icon")
    search_fields = ("parent__title", "comprehensive__title", "title")
    list_filter = ("parent", "comprehensive", "child_set", "specific_set")
    list_display_links = ("title",)
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
