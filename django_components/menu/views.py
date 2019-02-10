from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from menu.models import MenuItem
from screen.models import Screen


class MenuView(ListView):
    template_name = "menu/menu.html"
    queryset = MenuItem.objects.filter(parent__isnull=True).order_by("order")


class BreadcrumbView(TemplateView):
    template_name = "menu/breadcrumb.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen = context.get("screen")
        # Last Screen
        context["breadcrumb"] = [("#", screen.label, ())]
        while screen.parent:
            sibling = ()
            # sibling = tuple((child.get_absolute_url(context), child.label) for child in screen.parent.child_set.exclude(screen))
            screen = screen.parent
            context["breadcrumb"].insert(0, (screen.get_absolute_url(context), screen.label, sibling))
        menu_item = screen.menu_item
        while True:
            parent = menu_item.parent
            if parent:
                sibling = tuple((child.screen.get_absolute_url(context), child.label)
                                for child in parent.child_set.exclude(pk=menu_item.pk)
                                if child.screen)
            else:
                sibling = ()
            context["breadcrumb"].insert(0, ("#", menu_item.label, sibling))
            menu_item = parent
            if menu_item is None:
                break
        print(context)
        return context


class BreadcrumbMenuView(TemplateView):
    template_name = "breadcrumb_menu.html"
