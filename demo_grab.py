"""Demo chạy tại chỗ (KHÔNG cần mạng): mô phỏng cơ hội mới liên tục xuất
hiện trong Odoo, và tool auto-grab nhận chúng về tài khoản uid=42.

Chạy: python demo_grab.py
"""

from src.crm import MODEL
from src.grabber import Grabber


class SimOdoo:
    """Odoo giả lập: mỗi lần search lại 'sinh' thêm 1-2 cơ hội mới chưa ai nhận."""

    def __init__(self):
        self.records = {}
        self._next_id = 100
        self._ticks = 0

    def get_uid(self):
        return 42

    def _spawn_new_leads(self):
        # Mô phỏng: cứ mỗi lần quét lại có cơ hội mới rơi vào hệ thống
        n = 2 if self._ticks % 2 == 0 else 1
        for _ in range(n):
            self.records[self._next_id] = {"id": self._next_id, "user_id": False}
            self._next_id += 1
        self._ticks += 1

    def search(self, model, domain, limit=None, order=None):
        assert model == MODEL
        self._spawn_new_leads()
        ids = [r["id"] for r in self.records.values() if not r.get("user_id")]
        ids.sort(reverse=True)
        return ids[:limit] if limit else ids

    def write(self, model, ids, values):
        for i in ids:
            self.records[i].update(values)
        return True


def main():
    sim = SimOdoo()
    grabber = Grabber(sim, target_uid=42)
    total = grabber.run(interval=0, max_iterations=5)
    mine = [r["id"] for r in sim.records.values() if r.get("user_id") == 42]
    print(f"\nKết quả demo: {len(mine)} cơ hội đã về tài khoản uid=42 -> {sorted(mine)}")


if __name__ == "__main__":
    main()
