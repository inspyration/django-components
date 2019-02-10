from django.db.models import Manager


class ScreenManager(Manager):
    def get_by_natural_key(self, parent, label):
        if parent is None:
            return self.get(parent__isnull=True, label=label)
        return self.get(parent__label=parent, label=label)

    def get_natural_fields(self):
        return ("parent", "label")


class LayoutManager(Manager):
    def get_by_natural_key(self, screen, component, block, order):
        return self.get(screen=screen, component=component, block=block, order=order)

    def get_natural_fields(self):
        return ("screen", "component", "block", "order")
