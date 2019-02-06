from django.db.models import Manager


class ScreenManager(Manager):
    def get_by_natural_key(self, parent, label):
        if parent is None:
            return self.get(parent__isnull=True, label=label)
        return self.get(parent__label=parent, label=label)
