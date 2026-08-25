"""Test Grabber bằng một Odoo giả lập (không cần mạng)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.crm import MODEL  # noqa: E402
from src.grabber import DEFAULT_CLAIM_DOMAIN, Grabber  # noqa: E402


class FakeOdoo:
    """Giả lập tối thiểu: giữ danh sách cơ hội, hỗ trợ search + write."""

    def __init__(self, records):
        # records: list dict có 'id', 'user_id' (False nếu chưa nhận)
        self.records = {r["id"]: dict(r) for r in records}
        self.write_calls = []

    def get_uid(self):
        return 99

    def search(self, model, domain, limit=None, order=None):
        assert model == MODEL
        cond = {(d[0], d[2]) for d in domain}
        ids = [
            r["id"]
            for r in self.records.values()
            if ("user_id", False) not in cond or r.get("user_id") in (False, None)
        ]
        ids.sort(reverse=(order or "").endswith("desc"))
        return ids[:limit] if limit else ids

    def write(self, model, ids, values):
        self.write_calls.append((list(ids), dict(values)))
        for i in ids:
            self.records[i].update(values)
        return True


class TestGrabber(unittest.TestCase):
    def test_default_domain_targets_unassigned(self):
        self.assertIn(("user_id", "=", False), DEFAULT_CLAIM_DOMAIN)

    def test_uses_logged_in_uid_by_default(self):
        fake = FakeOdoo([])
        g = Grabber(fake)
        self.assertEqual(g.target_uid, 99)

    def test_claims_unassigned_and_reassigns(self):
        fake = FakeOdoo(
            [
                {"id": 1, "user_id": False},
                {"id": 2, "user_id": 5},  # đã có người -> bỏ qua
                {"id": 3, "user_id": False},
            ]
        )
        g = Grabber(fake, target_uid=42)
        claimed = g.run_once()
        self.assertCountEqual(claimed, [1, 3])
        # đã gán user_id = 42 cho các cơ hội trống
        self.assertEqual(fake.records[1]["user_id"], 42)
        self.assertEqual(fake.records[3]["user_id"], 42)
        self.assertEqual(fake.records[2]["user_id"], 5)
        self.assertEqual(g.claimed_total, 2)

    def test_run_stops_after_max_iterations(self):
        fake = FakeOdoo([{"id": 1, "user_id": False}])
        g = Grabber(fake, target_uid=7)
        total = g.run(interval=0, max_iterations=3, logger=lambda *_: None)
        # sau vòng 1 đã nhận id=1, các vòng sau không còn gì để nhận
        self.assertEqual(total, 1)


if __name__ == "__main__":
    unittest.main()
