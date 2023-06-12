"""Unit tests for ansible_filters."""
from django.apps import apps
from django.test import TestCase

from django_jinja import library
from ansible.plugins.loader import filter_loader


class AppConfigReadyTest(TestCase):
    """Test the AnsibleFilters API."""

    def setUp(self):
        """Initiate the app config for all tests."""
        self.app_config = apps.get_app_config("ansible_filters")
        self.ansible_filters = {f.ansible_name for f in filter_loader.all()}

    def test_app_config_ready_templates_exist(self):
        """Verify ALL ansible-core filters are loaded properly within app_config.ready()."""
        self.app_config.ready()
        self.assertEqual(
            self.ansible_filters, {filter for filter in library._local_env["filters"] if "ansible" in filter}
        )  # noqa
