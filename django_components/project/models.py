from django.db.models import Model, CharField, TextField

class Project(Model):
    
    description = CharField(max_length=120)
    texte = TextField()
    
    def __str__(self):
        return self.description