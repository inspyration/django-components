from django.core.exceptions import ImproperlyConfigured

from django.views.generic import (
    TemplateView,
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
    WeekArchiveView,
    DayArchiveView,
    TodayArchiveView,
    DateDetailView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)


class ScreenMixin:
    screen_pk = None
    template_name = "screen.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        from screen.models import Screen
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(self.kwargs)
        context["screen"] = Screen.objects.get(pk=self.get_screen_pk())
        return context

    def get_screen_pk(self):
        if not hasattr(self, "screen_pk"):
            raise ImproperlyConfigured("You must set the screen pk")
        return self.screen_pk


class TemplateScreen(ScreenMixin, TemplateView):
    pass


class ArchiveIndexScreen(ScreenMixin, ArchiveIndexView):
    pass


class YearArchiveScreen(ScreenMixin, YearArchiveView):
    pass


class MonthArchiveScreen(ScreenMixin, MonthArchiveView):
    pass


class WeekArchiveScreen(ScreenMixin, WeekArchiveView):
    pass


class DayArchiveScreen(ScreenMixin, DayArchiveView):
    pass


class TodayArchiveScreen(ScreenMixin, TodayArchiveView):
    pass


class DateDetailScreen(ScreenMixin, DateDetailView):
    pass


class DetailScreen(ScreenMixin, DetailView):
    pass


class FormScreen(ScreenMixin, FormView):
    pass


class CreateScreen(ScreenMixin, CreateView):
    pass


class UpdateScreen(ScreenMixin, UpdateView):
    pass


class DeleteScreen(ScreenMixin, DeleteView):
    pass


class ListScreen(ScreenMixin, ListView):
    pass
