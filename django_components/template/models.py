from django.db.models import Model, ForeignKey, CharField, OneToOneField, CASCADE, ManyToManyField, PROTECT
from django.utils.translation import ugettext_lazy as _

from component.models import Component
from template.managers import HtmlTagManager, BrowserManager, HttpResourceManager, KeywordManager, TemplateManager


class HtmlTag(Model):
    """HTML Tag"""

    objects = HtmlTagManager()

    label = CharField(
        verbose_name=_("label"),
        help_text=_("The way the data will be see from foreign objects"),
        max_length=255,
        blank=False,
        unique=True
    )

    def __str__(self):
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """HtmlTag Meta class"""

        verbose_name = _("Html tag")
        verbose_name_plural = _("Html tags")


class Browser(Model):
    """Web Browser"""

    objects = BrowserManager()

    label = CharField(
        verbose_name=_("label"),
        help_text=_("The way the data will be see from foreign objects"),
        max_length=255,
        blank=False,
        unique=True
    )

    def __str__(self):
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Browser Meta class"""

        verbose_name = _("Browser")
        verbose_name_plural = _("Browsers")


class HttpResource(Model):
    """HTTP Resource"""

    objects = HttpResourceManager()

    label = CharField(
        verbose_name=_("label"),
        help_text=_("The way the data will be see from foreign objects"),
        max_length=255,
        blank=False,
        unique=True
    )

    tag = ForeignKey(
        verbose_name=_("tag"),
        related_name="tag_%(class)s_set",
        help_text=_("HTML Tag used to call this resource"),
        to=HtmlTag,
        blank=False,
        on_delete=PROTECT,
    )

    browser = ForeignKey(
        verbose_name=_("browser"),
        related_name="browser_%(class)s_set",
        help_text=_("Specific Browser (potentially with version number)"),
        to=Browser,
        blank=False,
        on_delete=PROTECT,
    )

    path = CharField(
        verbose_name=_("path"),
        help_text=_("Path to the (hosted) resource"),
        max_length=127,
        blank=True,
    )

    def __str__(self):
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """HttpResource Meta class"""

        verbose_name = _("Http resource")
        verbose_name_plural = _("Http resources")


class Keyword(Model):
    """Keyword of a page (html>head>meta[keyword])"""

    objects = KeywordManager()

    label = CharField(
        verbose_name=_("label"),
        help_text=_("The way the data will be see from foreign objects"),
        max_length=255,
        blank=False,
        unique=True
    )

    def __str__(self):
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Keyword Meta class"""

        verbose_name = _("keyword")
        verbose_name_plural = _("keywords")


class Template(Model):
    """
    Template model

    A template is a specific component that is the main container.

    This model is linked to every objects described above.

    every screen must use one and only one template.
    """

    objects = TemplateManager()

    component = OneToOneField(
        verbose_name=_("component used by this template"),
        related_name="template",
        help_text=_("If this is null, this menu item is a not a leaf"),
        to=Component,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    label = CharField(
        verbose_name=_("label"),
        help_text=_("The way the data will be see from foreign objects"),
        max_length=255,
        blank=False,
        unique=True
    )

    resource_set = ManyToManyField(
        HttpResource,
        related_name="template_set",
        blank=True,
    )

    keyword_set = ManyToManyField(
        Keyword,
        related_name="template_set",
        blank=True,
    )

    def __str__(self):
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Keyword Meta class"""

        verbose_name = _("template")
        verbose_name_plural = _("templates")
