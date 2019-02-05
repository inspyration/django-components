from django.db.models import Model, ForeignKey, CharField, CASCADE, OneToOneField
from django.utils.translation import ugettext_lazy as _

from menu.managers import MenuItemManager
from screen.models import Screen


class MenuItem(Model):
    """
    Menu item model

    A menu item is an way to get to a screen
    Menu are organized in a tree:

    - a menu with children can be called "node"
    - a menu with a screen can be called a "leaf"
    - being both is not forbidden
    """

    objects = MenuItemManager()

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

    screen = OneToOneField(
        verbose_name=_("screen pointed by this menu item"),
        related_name="menu_item",
        help_text=_("If this is null, this menu item is a not a leaf"),
        to=Screen,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    title = CharField(
        verbose_name=_("screen title"),
        help_text=_("used in the menu when fully deployed"),
        max_length=127,
        blank=False,
        db_index=True,
    )

    icon = CharField(
        verbose_name=_("CSS icon name"),
        help_text=_("""according to your CSS framework
                       used as visual identification everywhere it should
                       used in the menu when reduced"""),
        max_length=16,
        blank=False,
    )

    def __str__(self):
        return self.title

    class Meta:  # pylint: disable=too-few-public-methods
        """MenuItem Meta class"""

        verbose_name = _("menu item")
        verbose_name_plural = _("menu items")
        index_together = (
            ("parent", "screen"),
            ("parent", "screen", "title"),
            ("screen", "title"),
            ("screen", "icon"),
        )
        unique_together = (
            ("parent", "title"),
            ("parent", "icon"),
        )
