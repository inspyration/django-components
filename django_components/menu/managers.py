from django.db.models import Manager


class MenuItemManager(Manager):
    def get_by_natural_key(self, parent, title):
        return self.get(parent=parent, title=title)
