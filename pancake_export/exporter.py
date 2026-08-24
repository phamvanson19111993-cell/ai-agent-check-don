"""Ghi kết quả ra CSV/JSON, tự gộp với dữ liệu cũ (không ghi đè, không trùng số)."""

import csv
import json
import os

FIELDS = ["ten", "sdt", "tinh_trang", "ngay", "ghi_chu", "thoi_gian", "link"]
HEADERS = ["Tên", "SĐT", "Tình trạng", "Ngày", "Ghi chú", "Thời gian", "Link hội thoại"]


def read_existing(path):
    """Đọc file CSV cũ -> dict {sdt: dòng}. File chưa có thì trả về rỗng."""
    if not os.path.exists(path):
        return {}
    existing = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            row = {}
            for field, header in zip(FIELDS, HEADERS):
                row[field] = (record.get(header) or record.get(field) or "").strip()
            if row.get("sdt"):
                existing[row["sdt"]] = row
    return existing


def merge(existing, rows):
    """Gộp dòng mới vào dữ liệu cũ. Trả về (danh sách đầy đủ, danh sách dòng mới)."""
    merged = dict(existing)
    new_rows = []
    for row in rows:
        phone = row["sdt"]
        if phone in merged:
            old = merged[phone]
            # Giữ ghi chú cũ do người dùng tự sửa, chỉ bổ sung nếu đang trống.
            for field in ("ten", "ngay", "ghi_chu"):
                if not old.get(field) and row.get(field):
                    old[field] = row[field]
            continue
        merged[phone] = row
        new_rows.append(row)

    ordered = sorted(merged.values(), key=lambda item: item.get("thoi_gian", ""), reverse=True)
    return ordered, new_rows


def write_csv(path, rows):
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    # utf-8-sig để Excel tiếng Việt mở không lỗi font.
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        for row in rows:
            writer.writerow([row.get(field, "") for field in FIELDS])
    return path


def write_json(path, rows):
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=2)
    return path
