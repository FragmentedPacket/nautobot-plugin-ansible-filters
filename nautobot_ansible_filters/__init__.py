"""Plugin declaration for ansible_filters."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig
from django_jinja import library
from ansible.plugins.loader import filter_loader


class AnsibleFiltersConfig(PluginConfig):
    """Plugin configuration for the ansible_filters plugin."""

    name = "nautobot_ansible_filters"
    verbose_name = "Nautobot Ansible Filters"
    version = __version__
    author = "Mikhail Yohman"
    description = "Nautobot plugin to include Ansible built-in Jinja filters."
    base_url = "ansible-filters"
    required_settings = []
    min_version = "1.2.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}

    def ready(self):
        for filter_plugin in filter_loader.all():
            # Handle <2.14 that passes the FilterModule back that requires us to iterate over filters to add them.
            if not hasattr(filter_plugin, "j2_function") and hasattr(filter_plugin, "filters"):
                for filter_name, filter_func in filter_plugin.filters().items():
                    library.filter(name=filter_name, fn=filter_func)
                continue

            # If it's ansible-core >2.14 then we can add using this method.
            library.filter(name=filter_plugin.ansible_name, fn=filter_plugin.j2_function)


config = AnsibleFiltersConfig  # pylint:disable=invalid-name
