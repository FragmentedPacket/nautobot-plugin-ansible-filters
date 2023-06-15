"""Store any utilities for plugin."""
from ansible.plugins.loader import filter_loader


def gather_filter_plugins():
    """Gather all filter plugins from ansible-core using their filter_loader of filter plugins they have loaded."""
    found_filters = {}
    for filter_plugin in filter_loader.all():
        # Handle <2.14 that passes the FilterModule back that requires us to iterate over filters to add them.
        if not hasattr(filter_plugin, "j2_function") and hasattr(filter_plugin, "filters"):
            for filter_name, filter_func in filter_plugin.filters().items():
                if "ansible" not in filter_name:
                    filter_name = f"ansible.builtin.{filter_name}"
                found_filters[filter_name] = filter_func
            # Continuing  the outer loop since we processed the filters passed in for this filter plugin.
            continue

        # This handles ansible-core >=2.14
        found_filters[filter_plugin.ansible_name] = filter_plugin.j2_function

    return found_filters
