from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from project.models import Project

@register(Project)
class ProjectAdmin(ModelAdmin):

    model = Project
    fields = ("description","texte")

    