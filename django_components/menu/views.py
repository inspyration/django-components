from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView

from menu.models import MenuItem


class MenuView(ListView):
    template_name = "menu/menu.html"
    queryset = MenuItem.objects.filter(parent__isnull=True).order_by("order")


class BreadcrumbView(TemplateView):
    template_name = "breadcrumb.html"


class BreadcrumbMenuView(TemplateView):
    template_name = "breadcrumb_menu.html"
