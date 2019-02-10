from django.db.models import Manager


class HtmlTagManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)

    def get_natural_fields(self):
        return ("label",)


class BrowserManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)

    def get_natural_fields(self):
        return ("label",)


class HttpResourceManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)

    def get_natural_fields(self):
        return ("label",)


class KeywordManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)

    def get_natural_fields(self):
        return ("label",)


class TemplateManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)

    def get_natural_fields(self):
        return ("label",)
