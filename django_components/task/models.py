from django.db.models import Model, CharField, TextField


class Task(Model):

    description = CharField(max_length=120)
    text = TextField()

    def __str__(self):
        return self.description