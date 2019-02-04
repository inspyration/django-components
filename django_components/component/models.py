import importlib
from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ViewDoesNotExist
from django.db.models import Model, ForeignKey, CharField, BooleanField, CASCADE, ManyToManyField
from django.http import HttpRequest
from django.urls import path, reverse
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField


class Component(Model):
    """
    Component model

    A component is a django view that is used to render a dedicated part of a bigger one.
    Components should be created by fixtures only and math specific existing views with a path starting with /components
    """

    # This is the name used by reverse to get to this component view.
    name = CharField(
        verbose_name=_("name"),
        max_length=16,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
    )

    # The type is the name a subclass of django View
    view_class = CharField(
        verbose_name=_("Class-based view"),
        max_length=64,
        blank=False,
        null=False,
        db_index=True,
    )

    # The content type is identifying the model behind this view
    content_type = ForeignKey(
        verbose_name=_("content type"),
        related_name="view_set",
        help_text=_("Blank if type is TemplateView"),
        to=ContentType,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    # This path is the one used to get to this component
    path = CharField(
        verbose_name=_("path"),
        max_length=64,
        blank=False,
        null=False,
        db_index=True,
    )

    kwargs = JSONField(
        verbose_name=_("keyword arguments"),
        blank=True,
        null=True,
    )

    def get_view_kwargs(self, **kwargs):
        if self.content_type:
            kwargs["model"] = self.content_type.model_class()
        if self.kwargs:
            kwargs.update(self.kwargs)
        return kwargs

    @property
    def view(self):
        cls_path = self.view_class.split(".")
        # Check that this is a valid class path
        if len(cls_path) < 2:
            raise ViewDoesNotExist(_("The python path {} is not valid".format(cls_path)))
        cls_name, module_name = cls_path[-1], ".".join(cls_path[:-1])
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise ViewDoesNotExist(_("The module name {} is not valid".format(module_name)))
        try:
            cls = getattr(module, cls_name)
        except ModuleNotFoundError:
            raise ViewDoesNotExist(_("The class {} is not part of module {}.".format(cls_name, module_name)))

        return cls.as_view(**self.get_view_kwargs())

    @property
    def url_pattern(self):
        return path(self.path, self.view, name=self.name)

    def render(self, screen, **context):
        # Create a dummy request:
        request = HttpRequest()
        request.method = "GET"
        # Render the view:
        if context:
            request.path = reverse(self.name, kwargs=context)
            # import pdb; pdb.set_trace()
        context["screen"] = screen
        response = self.view(request, **context)
        # return the content
        return response.rendered_content

    class Meta:  # pylint: disable=too-few-public-methods
        """View Meta class"""

        verbose_name = _("component")
        verbose_name_plural = _("components")
        index_together=(
            ("view_class", "content_type"),
        )


class Screen(Model):
    """
    Screen model

    A screen is an assembly of components
    Screens are organized in a tree
    """

    parent = ForeignKey(
        verbose_name=_("parent"),
        related_name="child_set",
        help_text=_("parent view"),
        to="self",
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    comprehensive = ForeignKey(
        verbose_name=_("overloaded screen"),
        related_name="specific_set",
        help_text=_("set the comprehensive screen of which this current screen is a specific version of"),
        to="self",
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    title = CharField(
        verbose_name=_("screen title"),
        help_text=_("used in html head and H1 (you can use templating language)"),
        max_length=127,
        blank=False,
        db_index=True,
    )

    icon = CharField(
        verbose_name=_("CSS icon name"),
        help_text=_("icon name, according to your CSS framework - used as visual identification everywhere it should"),
        max_length=16,
        blank=False,
    )

    component_set = ManyToManyField(
        Component,
        through='Layout',
        blank=False,
    )

    visible_in_sitemap = BooleanField(
        verbose_name=_("Should this screen appear in sitemap ?"),
        default=True,
    )

    visible_in_breadcrumb = BooleanField(
        verbose_name=_("Should this screen appear in children breadcrumb ?"),
        default=True,
    )

    use_comprehensive_in_breadcrumb = BooleanField(
        verbose_name=_("Should children breadcrumb use the comprehensive version of this screen instead ?"),
        default=False,
    )

    visible_in_menu = BooleanField(
        verbose_name=_("Should this screen must appear in menu ?"),
        default=True,
    )

    def render_components(self):
        result = defaultdict(list)
        for layout in self.layout_set.order_by("block", "order").all():
            result[layout.block].append(layout.component.render(screen=self))
        return dict(result)

    def render_component(self, block, **context):  # TODO: manage order  # TODO: Is this the right spot for this piece of code ?
        return "".join([layout.component.render(screen=self, **context) for layout in self.layout_set.filter(block=block)])  # TODO what if layout does not exists

    class Meta:  # pylint: disable=too-few-public-methods
        """Screen Meta class"""

        verbose_name = _("screen")
        verbose_name_plural = _("screens")
        index_together = (
            ("parent", "title"),
            ("parent", "comprehensive", "title"),
        )


class Layout(Model):

    screen = ForeignKey(
        verbose_name=_("screen"),
        related_name="layout_set",
        to=Screen,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    component = ForeignKey(
        verbose_name=_("component"),
        related_name="layout_set",
        to=Component,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    block = CharField(
        verbose_name=_("block name"),
        help_text=_("Name of the spot the component should be inserted into."),
        max_length=127,
        blank=False,
        db_index=True,
    )

    order = CharField(
        verbose_name=_("block order"),
        help_text=_("If many components are set to get into the same spot, the first one to get there is the lower."),
        max_length=127,
        blank=False,
        db_index=True,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Layout Meta class"""

        verbose_name = _("layout")
        verbose_name_plural = _("layouts")
        index_together = (
            ("screen", "component"),
            ("screen", "component", "block"),
            ("screen", "component", "block", "order"),
        )
        unique_together = (
            ("screen", "component", "block"),
        )
