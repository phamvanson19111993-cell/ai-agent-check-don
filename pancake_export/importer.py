"""Đọc file Pancake xuất ra (CSV/TSV/XLSX) khi không dùng API.

Dùng khi chưa có API key: trong Pancake bấm xuất danh sách hội thoại/khách hàng
ra file, rồi chạy: python3 -m pancake_export --from-file duong_dan.csv
"""

import csv
import os

from . import extract, tagging

# Từ khoá nhận diện cột, đã bỏ dấu tiếng Việt.
_NAME_HINTS = ("ten", "khach", "customer", "name", "ho ten")
_PHONE_HINTS = ("sdt", "so dien thoai", "dien thoai", "phone", "mobile")
_TAG_HINTS = ("nhan", "tag", "label")
_DATE_HINTS = ("ngay", "thoi gian", "date", "time", "cap nhat", "updated")
_NOTE_HINTS = ("ghi chu", "note", "noi dung", "tin nhan", "message", "snippet")


def _pick(headers, hints):
    for index, header in enumerate(headers):
        folded = tagging.fold(header)
        for hint in hints:
            if hint in folded:
                return index
    return None


def _read_rows(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        try:
            import openpyxl
        except ImportError:
            raise SystemExit(
                "Đọc file Excel cần thư viện openpyxl. Chạy: pip install openpyxl\n"
                "Hoặc lưu file dưới dạng CSV rồi chạy lại."
            )
        workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
        sheet = workbook.active
        return [[("" if cell is None else str(cell)) for cell in row]
                for row in sheet.iter_rows(values_only=True)]

    delimiter = "\t" if ext in (".tsv", ".tab") else ","
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.reader(handle, delimiter=delimiter)]


def load(path, page_id, closed_tags, match_yellow=False):
    """Đọc file xuất, lọc dòng CHƯA có nhãn chốt đơn, trả về (rows, stats)."""
    table = [row for row in _read_rows(path) if any(str(cell).strip() for cell in row)]
    if not table:
        return [], {"tong": 0, "da_chot": 0, "khong_co_sdt": 0, "chua_chot": 0}

    headers = [str(cell) for cell in table[0]]
    columns = {
        "ten": _pick(headers, _NAME_HINTS),
        "sdt": _pick(headers, _PHONE_HINTS),
        "tags": _pick(headers, _TAG_HINTS),
        "ngay": _pick(headers, _DATE_HINTS),
        "note": _pick(headers, _NOTE_HINTS),
    }
    if columns["sdt"] is None:
        raise SystemExit(
            "Không tìm thấy cột số điện thoại trong file %s.\n"
            "Các cột đang có: %s" % (path, ", ".join(headers))
        )

    def cell(row, key):
        index = columns[key]
        if index is None or index >= len(row):
            return ""
        return str(row[index]).strip()

    conversations = []
    for row in table[1:]:
        tags_text = cell(row, "tags")
        conversations.append({
            "id": "",
            "customer_name": cell(row, "ten"),
            "recent_phone_numbers": [cell(row, "sdt")],
            "updated_at": cell(row, "ngay"),
            "snippet": cell(row, "note"),
            "tags": [{"text": part.strip()} for part in tags_text.replace(";", ",").split(",")
                     if part.strip()],
        })

    return extract.collect(conversations, page_id, closed_tags, match_yellow=match_yellow)
