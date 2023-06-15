"""Plugin declaration for ansible_filters."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

__version__ = metadata.version(__name__)

from django_jinja import library
from nautobot_ansible_filters.utilities import gather_filter_plugins


@library.filter
def testing_filter():
    """Testing testing."""
    return "TESTING"


def init_filters():
    """Generic function to load filters into Nautobot and allow plugin metadata to pick up that this plugin is offering Jinja filters."""
    for filter_name, filter_func in gather_filter_plugins().items():
        library.filter(name=filter_name, fn=filter_func)
