from django.db.models import Manager


class ScreenManager(Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)
