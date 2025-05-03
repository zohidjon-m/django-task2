
from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.conf import settings
from unittest.mock import patch, MagicMock
import os
import json

from tenants.views import config_view, custom_page_view

class TenantViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.config_dir = os.path.join(settings.BASE_DIR, 'configs')
        os.makedirs(self.config_dir, exist_ok=True)

        # Valid configs
        self.valid_config_a = {
            "tenant_id": "a",
            "enable_custom_page": True,
            "page_title": "Welcome to Tenant A"
        }
        self.valid_config_b = {
            "tenant_id": "b",
            "enable_custom_page": False,
            "page_title": "Access Denied"
        }

        with open(os.path.join(self.config_dir, "tenant_a_config.json"), "w") as f:
            json.dump(self.valid_config_a, f)
        with open(os.path.join(self.config_dir, "tenant_b_config.json"), "w") as f:
            json.dump(self.valid_config_b, f)

    def mock_tenant_request(self, tenant_id):
        req = self.factory.get(f"/api/config/{tenant_id}/")
        req.tenant = MagicMock()
        req.tenant.schema_name = f"tenant_{tenant_id}"
        return req

    def test_config_view_success(self):
        req = self.mock_tenant_request("a")
        res = config_view(req, "a")
        self.assertEqual(res.status_code, 200)
        self.assertIn("tenant_id", json.loads(res.content))

    def test_config_view_wrong_tenant(self):
        req = self.mock_tenant_request("a")
        res = config_view(req, "b")
        self.assertEqual(res.status_code, 403)

    def test_config_view_missing_file(self):
        req = self.mock_tenant_request("c")
        res = config_view(req, "c")
        self.assertEqual(res.status_code, 404)

    def test_config_view_malformed_json(self):
        bad_path = os.path.join(self.config_dir, "tenant_bad_config.json")
        with open(bad_path, "w") as f:
            f.write("{ bad json")
        req = self.mock_tenant_request("bad")
        res = config_view(req, "bad")
        self.assertEqual(res.status_code, 500)

    def test_custom_page_success(self):
        req = self.mock_tenant_request("a")
        res = custom_page_view(req, "a")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Welcome to Tenant A", res.content.decode())

    def test_custom_page_disabled(self):
        req = self.mock_tenant_request("b")
        res = custom_page_view(req, "b")
        self.assertEqual(res.status_code, 403)

    def test_custom_page_wrong_tenant(self):
        req = self.mock_tenant_request("a")
        res = custom_page_view(req, "b")
        self.assertEqual(res.status_code, 403)

    def test_custom_page_missing_file(self):
        req = self.mock_tenant_request("c")
        res = custom_page_view(req, "c")
        self.assertEqual(res.status_code, 404)
