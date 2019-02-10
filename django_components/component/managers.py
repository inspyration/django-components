from django.db.models import Manager


class ComponentManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)

    def get_natural_fields(self):
        return ("label", )
