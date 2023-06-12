"""Plugin declaration for ansible_filters."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig
from django_jinja import library
from ansible.plugins.loader import filter_loader


class AnsibleFiltersConfig(PluginConfig):
    """Plugin configuration for the ansible_filters plugin."""

    name = "ansible_filters"
    verbose_name = "Ansible Filters"
    version = __version__
    author = "Mikhail Yohman"
    description = "Ansible Filters."
    base_url = "ansible-filters"
    required_settings = []
    min_version = "1.2.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}

    def ready(self):
        for filter_plugin in filter_loader.all():
            library.filter(fn=filter_plugin.j2_function, name=filter_plugin.ansible_name)


config = AnsibleFiltersConfig  # pylint:disable=invalid-name
