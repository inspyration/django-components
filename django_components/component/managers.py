from django.db.models import Manager


class ComponentManager(Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)
