"""Tự động 'nhận' cơ hội về tài khoản của bạn nhanh nhất có thể.

Ý tưởng: liên tục quét các cơ hội đủ điều kiện (mặc định: cơ hội đang hoạt
động CHƯA có người phụ trách) rồi lập tức gán user_id = tài khoản của bạn.
"""

from __future__ import annotations

import time
from typing import Any, Callable, List, Optional

from .crm import MODEL
from .odoo_client import OdooClient, OdooError

# Cơ hội "có thể nhận": là opportunity, đang active, chưa ai phụ trách.
DEFAULT_CLAIM_DOMAIN: List[Any] = [
    ("type", "=", "opportunity"),
    ("active", "=", True),
    ("user_id", "=", False),
]


class Grabber:
    def __init__(
        self,
        client: OdooClient,
        target_uid: Optional[int] = None,
        domain: Optional[List[Any]] = None,
        batch_limit: int = 80,
        on_claim: Optional[Callable[[List[int]], None]] = None,
    ):
        self.client = client
        self.target_uid = target_uid or client.get_uid()
        self.domain = list(domain) if domain else list(DEFAULT_CLAIM_DOMAIN)
        self.batch_limit = batch_limit
        self.on_claim = on_claim
        self.claimed_total = 0

    def find_claimable(self) -> List[int]:
        """Chỉ lấy id (nhẹ, nhanh), ưu tiên cơ hội mới nhất."""
        return self.client.search(
            MODEL, self.domain, limit=self.batch_limit, order="id desc"
        )

    def claim(self, ids: List[int]) -> bool:
        """Gán ngay user_id cho các cơ hội -> nhảy về tài khoản của bạn."""
        if not ids:
            return False
        ok = self.client.write(MODEL, ids, {"user_id": self.target_uid})
        if ok:
            self.claimed_total += len(ids)
            if self.on_claim:
                self.on_claim(ids)
        return bool(ok)

    def run_once(self) -> List[int]:
        ids = self.find_claimable()
        if ids:
            self.claim(ids)
        return ids

    def run(
        self,
        interval: float = 0.2,
        max_iterations: Optional[int] = None,
        stop: Optional[Callable[[], bool]] = None,
        logger: Callable[[str], None] = print,
    ) -> int:
        """Vòng lặp nhận cơ hội. interval=giây giữa 2 lần quét (nhỏ = nhanh).

        Trả về tổng số cơ hội đã nhận. Dừng bằng Ctrl+C, `stop()` hoặc
        đạt `max_iterations`.
        """
        logger(
            f"Bắt đầu auto-grab: target uid={self.target_uid}, "
            f"interval={interval}s, domain={self.domain}"
        )
        i = 0
        try:
            while True:
                if stop and stop():
                    break
                if max_iterations is not None and i >= max_iterations:
                    break
                i += 1
                try:
                    ids = self.run_once()
                    if ids:
                        logger(f"[{i}] Đã nhận {len(ids)} cơ hội: {ids}")
                except OdooError as exc:
                    logger(f"[{i}] Lỗi (bỏ qua, tiếp tục): {exc}")
                if interval > 0:
                    time.sleep(interval)
        except KeyboardInterrupt:
            logger("Dừng theo yêu cầu (Ctrl+C).")
        logger(f"Tổng cộng đã nhận: {self.claimed_total} cơ hội.")
        return self.claimed_total
