from django.db.models import Manager


class HtmlTagManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)


class BrowserManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)


class HttpResourceManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)


class KeywordManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)


class TemplateManager(Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)
