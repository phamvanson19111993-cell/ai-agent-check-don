# -*- coding: utf-8 -*-
"""Đọc cấu hình từ file .env"""
import os

from dotenv import load_dotenv

load_dotenv()


def _split_names(value: str) -> list[str]:
    return [v.strip().lower() for v in (value or "").split(",") if v.strip()]


def _parse_csv_sources(raw: str) -> list[tuple[str, str]]:
    """CSV_URLS: mỗi nguồn cách nhau bởi dấu ; hoặc xuống dòng.
    Mỗi nguồn có dạng "Tên tab|URL" hoặc chỉ "URL" (tab sẽ tự đặt Tab 1, Tab 2...).
    """
    sources: list[tuple[str, str]] = []
    for i, part in enumerate(re.split(r"[;\n]+", raw or "")):
        part = part.strip()
        if not part:
            continue
        if "|" in part:
            name, url = part.split("|", 1)
            sources.append((name.strip() or f"Tab {i + 1}", url.strip()))
        else:
            sources.append((f"Tab {i + 1}", part))
    return sources


import re  # noqa: E402  (dùng trong _parse_csv_sources)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
REPORT_CHAT_ID = os.getenv("REPORT_CHAT_ID", "").strip()

SOURCE_TYPE = os.getenv("SOURCE_TYPE", "csv").strip().lower()

# Cho phép cả CSV_URL (1 link) lẫn CSV_URLS (nhiều link, mỗi tab một link)
_raw_urls = os.getenv("CSV_URLS", "").strip() or os.getenv("CSV_URL", "").strip()
CSV_SOURCES = _parse_csv_sources(_raw_urls)

# Tên cột trong Sheet — có thể liệt kê nhiều tên (phân cách bằng dấu phẩy) để tự dò.
# Mặc định khớp Sheet "2026 Giàu sang phú quý !": Ngày | KHÁCH HÀNG | SĐT | TRIỆU CHỨNG | SẢN PHẨM | trạng thái | Ghi Chú
COL_PHONE = _split_names(os.getenv("COL_PHONE", "SĐT,SDT,SỐ ĐIỆN THOẠI,PHONE,ĐIỆN THOẠI"))
COL_CUSTOMER = _split_names(os.getenv("COL_CUSTOMER", "KHÁCH HÀNG,KHACH HANG,TÊN KHÁCH,CUSTOMER"))
COL_DATE = _split_names(os.getenv("COL_DATE", "NGÀY,NGAY,DATE,NGÀY LÊN ĐƠN"))
COL_PRODUCT = _split_names(os.getenv("COL_PRODUCT", "SẢN PHẨM,SAN PHAM,PRODUCT"))
COL_STATUS = _split_names(os.getenv("COL_STATUS", "TRẠNG THÁI,TRANG THAI,STATUS"))

INTAKE_HOST = os.getenv("INTAKE_HOST", "127.0.0.1").strip()
INTAKE_PORT = int(os.getenv("INTAKE_PORT", "8787"))
INTAKE_SECRET = os.getenv("INTAKE_SECRET", "").strip()

HEARTBEAT_HOURS = float(os.getenv("HEARTBEAT_HOURS", "0") or 0)   # 0 = tắt
RELOAD_MINUTES = float(os.getenv("RELOAD_MINUTES", "15") or 15)   # tự nạp lại Sheet
DEDUP_TTL_MIN = float(os.getenv("DEDUP_TTL_MIN", "10") or 10)     # không báo lại cùng 1 số trong N phút

TZ_NAME = os.getenv("TZ_NAME", "Asia/Ho_Chi_Minh").strip()
