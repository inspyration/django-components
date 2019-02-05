from collections import defaultdict

from django.db.models import Model, ForeignKey, CharField, BooleanField, CASCADE, ManyToManyField, IntegerField
from django.utils.translation import ugettext_lazy as _

from component.models import Component
from screen.managers import ScreenManager


class Screen(Model):
    """
    Screen model

    A screen is an assembly of components
    Screens are organized in a tree
    """

    objects = ScreenManager()

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
        unique=True,
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

    def __str__(self):
        return self.title

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
            ("comprehensive", "title"),
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

    order = IntegerField(
        verbose_name=_("block order"),
        help_text=_("If many components are set to get into the same spot, the first one to get there is the lower."),
        blank=False,
        db_index=True,
    )

    def __str__(self):
        return "{} <<< {}".format(self.screen.title, self.component.name)

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
