from collections import defaultdict
from re import findall

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, CharField, BooleanField, CASCADE, ManyToManyField, IntegerField
from django.urls import path, reverse
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from component.models import Component
from screen.managers import ScreenManager, LayoutManager
from screen.views import (
    TemplateScreen,
    ArchiveIndexScreen,
    YearArchiveScreen,
    MonthArchiveScreen,
    WeekArchiveScreen,
    DayArchiveScreen,
    TodayArchiveScreen,
    DateDetailScreen,
    DetailScreen,
    FormScreen,
    CreateScreen,
    UpdateScreen,
    DeleteScreen,
    ListScreen,
)

from template.models import Template


PATH_ARGUMENT_REGEX = "<(.+?)>+?"


class Screen(Model):
    """
    Screen model

    A screen is an assembly of components
    Screens are organized in a tree
    """

    VIEW_CLASSES = (
        ("TemplateScreen", TemplateScreen),
        ("ArchiveIndexScreen", ArchiveIndexScreen),
        ("YearArchiveScreen", YearArchiveScreen),
        ("MonthArchiveScreen", MonthArchiveScreen),
        ("WeekArchiveScreen", WeekArchiveScreen),
        ("DayArchiveScreen", DayArchiveScreen),
        ("TodayArchiveScreen", TodayArchiveScreen),
        ("DateDetailScreen", DateDetailScreen),
        ("DetailScreen", DetailScreen),
        ("FormScreen", FormScreen),
        ("CreateScreen", CreateScreen),
        ("UpdateScreen", UpdateScreen),
        ("DeleteScreen", DeleteScreen),
        ("ListScreen", ListScreen),
    )

    objects = ScreenManager()

    parent = ForeignKey(
        verbose_name=_("parent"),
        related_name="child_set",
        help_text=_("parent menu item"),
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

    # This is the label used by reverse to get to this screen view.
    label = CharField(
        verbose_name=_("label"),
        max_length=16,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
    )

    # The type is the label a subclass of django View
    view_class = CharField(
        verbose_name=_("Class-based view"),
        max_length=64,
        choices=VIEW_CLASSES,
        blank=False,
        null=False,
        db_index=True,
    )

    # The content type is identifying the model behind this view
    content_type = ForeignKey(
        verbose_name=_("content type"),
        related_name="screen_set",
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

    def __str__(self):
        return self.label

    def extract_argument(self, argument, **context):
        if ":" not in argument:
            type_check = None
        else:
            type_check, argument = argument.split(":")

        value = context.get(argument)
        if value is None:
            raise ValidationError("Missing value for {} in {}.".format(argument, self.path))

        if type_check == "int":
            try:
                return argument, int(value)
            except ValueError:
                raise ValidationError("Invalid int value {} for {} in {}.".format(value, argument, self.path))
        return argument, value

    def get_absolute_url(self, context):
        kwargs = dict(self.extract_argument(argument, **context)
                      for argument in findall(PATH_ARGUMENT_REGEX, self.path))

        return reverse(self.label, kwargs=kwargs)

    def get_view_kwargs(self, **kwargs):
        kwargs["screen_pk"] = self.pk
        if self.content_type:
            kwargs["model"] = self.content_type.model_class()
        if self.kwargs:
            kwargs.update(self.kwargs)
        return kwargs

    @property
    def view(self):
        return dict(self.VIEW_CLASSES)[self.view_class].as_view(**self.get_view_kwargs())

    @property
    def url_pattern(self):
        return path(self.path, self.view, name=self.label)

    template = ForeignKey(
        verbose_name=_("template"),
        related_name="screen_set",
        help_text=_("set the comprehensive screen of which this current screen is a specific version of"),
        to=Template,
        null=False,
        blank=False,
        db_index=True,
        on_delete=CASCADE,
    )

    icon = CharField(  # Debatable
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

    hide_in_sitemap = BooleanField(
        verbose_name=_("Should this screen be hidden in sitemap ?"),
        default=False,
    )

    # def __str__(self):
    #     return self.label

    def render_components(self):
        result = defaultdict(list)
        # Render main template
        result["page"].append(self.template.component.render(screen=self))
        # Render every other components
        for layout in self.layout_set.order_by("block", "order").all():
            result[layout.block].append(layout.component.render(screen=self))
        return dict(result)

    def render_page(self, **context):
        screen = context.pop("screen")
        assert screen == self
        return self.template.component.render(screen=self, **context)

    def render_component(self, block, **context):
        screen = context.pop("screen")
        assert screen == self
        # TODO: manage order  # TODO: Is this the right spot for this piece of code ?
        return "".join(
            [layout.component.render(screen=self, **context) for layout in self.layout_set.filter(block=block)]
        )
        # TODO what if layout does not exists

    class Meta:  # pylint: disable=too-few-public-methods
        """Screen Meta class"""

        verbose_name = _("screen")
        verbose_name_plural = _("screens")
        index_together = (
            ("parent", "label"),
            ("comprehensive", "label"),
            ("parent", "comprehensive", "label"),
        )
        unique_together = (
            ("parent", "label"),
        )


class Layout(Model):

    objects = LayoutManager()

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

    order = IntegerField(
        verbose_name=_("block order"),
        help_text=_("If many components are set to get into the same spot, the first one to get there is the lower."),
        blank=False,
        db_index=True,
    )

    def __str__(self):
        return "{} <<< {}".format(self.screen.label, self.component.label)

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
