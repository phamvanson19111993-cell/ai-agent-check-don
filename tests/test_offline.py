"""Unit test chạy offline (mock Odoo) — không cần mạng."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import OdooConfig  # noqa: E402
from src.crm import ACTIVE_OPP_DOMAIN, CrmService  # noqa: E402
from src.odoo_client import OdooClient  # noqa: E402
from src.orders import load_orders, order_to_opportunity  # noqa: E402


class TestConfig(unittest.TestCase):
    def test_validate_requires_auth(self):
        cfg = OdooConfig(url="https://x", db="db")
        with self.assertRaises(ValueError):
            cfg.validate()

    def test_session_mode(self):
        cfg = OdooConfig(url="https://x", db="db", session_id="abc")
        cfg.validate()  # không ném lỗi
        self.assertTrue(cfg.uses_session)

    def test_userpass_mode(self):
        cfg = OdooConfig(url="https://x", db="db", username="u", password="p")
        cfg.validate()
        self.assertFalse(cfg.uses_session)


class TestOdooClientTransport(unittest.TestCase):
    def _client(self, **kw):
        cfg = OdooConfig(url="https://x", db="db", username="u", password="p", **kw)
        return OdooClient(cfg)

    def test_execute_kw_userpass_payload(self):
        client = self._client()
        client.uid = 7
        captured = {}

        def fake_post(path, payload):
            captured["path"] = path
            captured["payload"] = payload
            return [{"id": 1}]

        client._post = fake_post
        result = client.search_read("crm.lead", domain=[("a", "=", 1)], fields=["id"])
        self.assertEqual(result, [{"id": 1}])
        self.assertEqual(captured["path"], "/jsonrpc")
        args = captured["payload"]["params"]["args"]
        # args = [db, uid, password, model, method, [domain], kwargs]
        self.assertEqual(args[0], "db")
        self.assertEqual(args[1], 7)
        self.assertEqual(args[3], "crm.lead")
        self.assertEqual(args[4], "search_read")

    def test_execute_kw_session_payload(self):
        cfg = OdooConfig(url="https://x", db="db", session_id="sess")
        client = OdooClient(cfg)
        captured = {}

        def fake_post(path, payload):
            captured["path"] = path
            captured["payload"] = payload
            return True

        client._post = fake_post
        client.create("crm.lead", {"name": "X"})
        self.assertEqual(captured["path"], "/web/dataset/call_kw")
        self.assertEqual(captured["payload"]["params"]["model"], "crm.lead")
        self.assertEqual(captured["payload"]["params"]["method"], "create")


class TestCrmService(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock(spec=OdooClient)
        self.svc = CrmService(self.client)

    def test_list_active_uses_domain(self):
        self.client.search_read.return_value = []
        self.svc.list_active_opportunities()
        called_domain = self.client.search_read.call_args.kwargs["domain"]
        for cond in ACTIVE_OPP_DOMAIN:
            self.assertIn(cond, called_domain)

    def test_upsert_updates_when_found(self):
        self.client.search_read.return_value = [{"id": 42}]
        res = self.svc.upsert_by_ref("DON001", {"phone": "1"})
        self.assertEqual(res, {"action": "updated", "id": 42})
        self.client.write.assert_called_once()

    def test_upsert_creates_when_missing(self):
        self.client.search_read.return_value = []
        self.client.create.return_value = 99
        res = self.svc.upsert_by_ref("DON002", {"phone": "2"})
        self.assertEqual(res, {"action": "created", "id": 99})
        self.client.create.assert_called_once()


class TestOrders(unittest.TestCase):
    def test_load_csv_and_map(self):
        path = Path(__file__).resolve().parents[1] / "data" / "mau_don_hang.csv"
        orders = load_orders(path)
        self.assertEqual(len(orders), 2)
        values = order_to_opportunity(orders[0])
        self.assertEqual(values["name"], "DON001")
        self.assertEqual(values["phone"], "0901234567")
        self.assertEqual(values["expected_revenue"], 1500000.0)


if __name__ == "__main__":
    unittest.main()
