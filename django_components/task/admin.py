from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from task.models import Task

@register(Task)
class TaskAdmin(ModelAdmin):

    model = Task
    fields = ("description","texte")
