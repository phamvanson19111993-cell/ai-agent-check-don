# -*- coding: utf-8 -*-
"""Nạp dữ liệu đơn hàng từ Google Sheet (link CSV export) và tra cứu số điện thoại.

- Hỗ trợ nhiều link CSV (mỗi tab một link, theo &gid=...).
- SĐT trong Sheet có thể mất số 0 đầu (Google lưu thành số) → chuẩn hoá về 9 số cuối.
- Nếu không tìm thấy cột SĐT theo tên, tự dò cột nào chứa nhiều số điện thoại nhất.
"""
import csv
import io
import logging
import threading
import time

import requests

import config
from phone_utils import normalize

log = logging.getLogger(__name__)


def _find_col(header: list[str], candidates: list[str]) -> int | None:
    lowered = [h.strip().lower() for h in header]
    for cand in candidates:
        if cand in lowered:
            return lowered.index(cand)
    return None


def _fetch_csv(url: str, retries: int = 3) -> str:
    """Tải CSV, tự thử lại với backoff. Hỗ trợ cả đường dẫn file cục bộ (để test)."""
    import os
    if os.path.exists(url):
        with open(url, encoding="utf-8-sig") as f:
            return f.read()
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            if "text/html" in resp.headers.get("Content-Type", ""):
                raise RuntimeError(
                    "Link trả về trang HTML thay vì CSV — kiểm tra Sheet đã chia sẻ "
                    "'Bất kỳ ai có link → Người xem' và link có ?format=csv chưa."
                )
            resp.encoding = "utf-8"
            return resp.text
        except Exception as e:  # noqa: BLE001
            last_err = e
            wait = 2 ** attempt
            log.warning("Tải CSV lỗi (lần %d/%d): %s — thử lại sau %ds", attempt + 1, retries, e, wait)
            time.sleep(wait)
    raise RuntimeError(f"Không tải được CSV sau {retries} lần: {last_err}")


class SheetStore:
    """Giữ chỉ mục SĐT → danh sách dòng đơn hàng, an toàn khi truy cập từ nhiều luồng."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._index: dict[str, list[dict]] = {}
        self._row_count = 0
        self._tab_count = 0
        self._loaded_at: float | None = None
        self._last_error: str | None = None
        # chống báo lặp: khoá SĐT -> thời điểm báo gần nhất
        self._reported: dict[str, float] = {}

    # ---------- nạp dữ liệu ----------

    def load(self) -> tuple[int, int]:
        """Nạp toàn bộ các nguồn CSV. Trả về (số dòng có SĐT, số tab). Ném lỗi nếu MỌI tab đều lỗi."""
        if not config.CSV_SOURCES:
            raise RuntimeError("Chưa cấu hình CSV_URL / CSV_URLS trong .env")

        index: dict[str, list[dict]] = {}
        rows = 0
        tabs_ok = 0
        errors: list[str] = []

        for tab_name, url in config.CSV_SOURCES:
            try:
                text = _fetch_csv(url)
                n = self._parse_tab(tab_name, text, index)
                rows += n
                tabs_ok += 1
                log.info("Tab '%s': %d dòng có SĐT", tab_name, n)
            except Exception as e:  # noqa: BLE001
                errors.append(f"{tab_name}: {e}")
                log.error("Lỗi nạp tab '%s': %s", tab_name, e)

        if tabs_ok == 0:
            raise RuntimeError("Đọc Sheet thất bại — " + " | ".join(errors))

        with self._lock:
            self._index = index
            self._row_count = rows
            self._tab_count = tabs_ok
            self._loaded_at = time.time()
            self._last_error = " | ".join(errors) if errors else None

        return rows, tabs_ok

    def _parse_tab(self, tab_name: str, text: str, index: dict[str, list[dict]]) -> int:
        reader = csv.reader(io.StringIO(text))
        table = [row for row in reader if any(cell.strip() for cell in row)]
        if not table:
            return 0

        header = table[0]
        i_phone = _find_col(header, config.COL_PHONE)
        i_cust = _find_col(header, config.COL_CUSTOMER)
        i_date = _find_col(header, config.COL_DATE)
        i_prod = _find_col(header, config.COL_PRODUCT)
        i_stat = _find_col(header, config.COL_STATUS)

        body = table[1:]
        if i_phone is None:
            # Tự dò: chọn cột có nhiều giá trị là SĐT hợp lệ nhất
            best, best_hits = None, 0
            for col in range(max(len(r) for r in table)):
                hits = sum(1 for r in body[:200] if col < len(r) and normalize(r[col]))
                if hits > best_hits:
                    best, best_hits = col, hits
            if best is None or best_hits == 0:
                raise RuntimeError(f"Không tìm thấy cột SĐT (header: {header})")
            i_phone = best
            log.warning("Tab '%s': không thấy cột tên SĐT, tự dò ra cột #%d", tab_name, i_phone + 1)

        def cell(row: list[str], idx: int | None) -> str:
            if idx is None or idx >= len(row):
                return ""
            return row[idx].strip()

        count = 0
        for row in body:
            key = normalize(cell(row, i_phone))
            if not key:
                continue
            index.setdefault(key, []).append({
                "customer": cell(row, i_cust) or "(trống)",
                "date": cell(row, i_date) or "(trống)",
                "product": cell(row, i_prod) or "(trống)",
                "status": cell(row, i_stat) or "(trống)",
                "tab": tab_name,
            })
            count += 1
        return count

    # ---------- tra cứu ----------

    def lookup(self, key: str) -> list[dict]:
        with self._lock:
            return list(self._index.get(key, []))

    @property
    def row_count(self) -> int:
        with self._lock:
            return self._row_count

    @property
    def tab_count(self) -> int:
        with self._lock:
            return self._tab_count

    @property
    def last_error(self) -> str | None:
        with self._lock:
            return self._last_error

    @property
    def loaded(self) -> bool:
        with self._lock:
            return self._loaded_at is not None

    # ---------- chống báo trùng lặp ----------

    def recently_reported(self, key: str) -> bool:
        """True nếu số này vừa được báo trong DEDUP_TTL_MIN phút (và đánh dấu lại)."""
        ttl = config.DEDUP_TTL_MIN * 60
        now = time.time()
        with self._lock:
            # dọn các mục quá hạn
            for k in [k for k, t in self._reported.items() if now - t > ttl]:
                del self._reported[k]
            if key in self._reported:
                return True
            self._reported[key] = now
            return False


store = SheetStore()
