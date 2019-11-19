from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EjClustersConfig(AppConfig):
    """Configurations of EJ Cluters
    Attributes: 
        name: name of cluster
        verbose_name:
        rules: rules to cluster
        api: api key to cluster
    """

    name = "ej_clusters"
    verbose_name = _("Clusters")
    rules = None
    api = None

    def ready(self):
        from . import rules
        from . import api

        self.rules = rules
        self.api = api
