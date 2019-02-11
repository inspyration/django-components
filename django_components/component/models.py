import importlib
from re import findall

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ViewDoesNotExist, ValidationError
from django.db.models import Model, ForeignKey, CharField, CASCADE
from django.http import HttpRequest
from django.urls import path, reverse
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from component.managers import ComponentManager


PATH_ARGUMENT_REGEX = "<(.+?)>+?"


class Component(Model):
    """
    Component model

    A component is a django view that is used to render a dedicated part of a bigger one.
    Components should be created by fixtures only and math specific existing views with a path starting with /components
    """

    objects = ComponentManager()

    # This is the label used by reverse to get to this component view.
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
        blank=False,
        null=False,
        db_index=True,
    )

    # The content type is identifying the model behind this view
    content_type = ForeignKey(
        verbose_name=_("content type"),
        related_name="component_set",
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
        return path(self.path, self.view, name=self.label)

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

    def render(self, screen, **context):
        # Get all arguments
        kwargs = dict(self.extract_argument(argument, **context)
                      for argument in findall(PATH_ARGUMENT_REGEX, self.path))

        # Create a dummy request:
        request = HttpRequest()
        request.method = "GET"
        request.path = reverse(self.label, kwargs=kwargs)

        context["kwargs"] = kwargs
        context["screen"] = screen
        # import pdb; pdb.set_trace()
        if "request" in context:
            context.pop("request")
        response = self.view(request, **context)
        # return the content
        return response.rendered_content

    class Meta:  # pylint: disable=too-few-public-methods
        """View Meta class"""

        verbose_name = _("component")
        verbose_name_plural = _("components")
        index_together = (
            ("view_class", "content_type"),
        )
