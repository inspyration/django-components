"""Admin IHM"""


from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.admin.decorators import register

from template.models import HtmlTag, Browser, HttpResource, Keyword, Template


@register(HtmlTag)
class HtmlTagAdmin(ModelAdmin):
    """
    ## Component admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = HtmlTag
    fields = ("label",)
    list_display = ("label",)
    search_fields = ("label",)
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


@register(Browser)
class BrowserAdmin(ModelAdmin):
    """
    ## Component admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = Browser
    fields = ("label",)
    list_display = ("label",)
    search_fields = ("label",)
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


@register(HttpResource)
class HttpResourceAdmin(ModelAdmin):
    """
    ## Component admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = HttpResource
    fields = ("label", "tag", "browser", "path")
    list_display = ("label", "tag", "browser", "path")
    search_fields = ("label", "tag__label", "browser__label")
    list_filter = ("tag", "browser")
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


@register(Keyword)
class KeywordAdmin(ModelAdmin):
    """
    ## Component admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = Keyword
    fields = ("label",)
    list_display = ("label",)
    search_fields = ("label",)
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


class HttpResourceInline(StackedInline):
    """HttpResource inline class"""

    model = Template.resource_set.through
    fields = ("label",)
    readonly_fields = ()
    min_num = 0
    extra = 0


class KeywordInline(StackedInline):
    """Layout inline class"""

    model = Template.keyword_set.through
    fields = ("label",)
    readonly_fields = ()
    min_num = 1
    extra = 0


@register(Template)
class TemplateAdmin(ModelAdmin):
    """
    ## Component admin IHM

    This object should'nt be created or modified here (as long as the proof of concept has been validated).
    """

    model = Template
    fields = ("label", "component")
    list_display = ("label", "component")
    search_fields = ("label", "component__name")
    list_display_links = ("label",)
    inlines = [HttpResourceInline, KeywordInline]

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
