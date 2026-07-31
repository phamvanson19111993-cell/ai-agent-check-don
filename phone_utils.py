# -*- coding: utf-8 -*-
"""Tách và chuẩn hoá số điện thoại Việt Nam từ văn bản tự do.

Nguyên tắc:
- Bắt các dạng: 0378415411, 0378.415.411, 0378 415 411, +84378415411, 84 378 415 411
- KHÔNG nhận nhầm số tiền kiểu 3.290.000 (không bắt đầu bằng 0/84, không đủ cấu trúc)
- Chuẩn hoá về "khoá" = 9 chữ số cuối để so sánh (0378415411 ~ +84378415411 ~ 378415411)
"""
import re

# Bắt đầu bằng +84 / 84 / 0, theo sau đúng 9 chữ số (cho phép ngăn cách . - hoặc khoảng trắng)
_PHONE_RE = re.compile(r"(?<![\d])(?:\+?84|0)(?:[\s.\-]?\d){9}(?![\s.\-]?\d)")

# Đầu số di động VN hợp lệ (chữ số đầu của 9 số cuối): 03x,05x,07x,08x,09x
_VALID_FIRST = set("35789")


def normalize(raw: str) -> str | None:
    """Chuẩn hoá một chuỗi số về khoá 9 chữ số cuối. Trả None nếu không hợp lệ."""
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("84"):
        digits = digits[2:]
    if digits.startswith("0"):
        digits = digits[1:]
    if len(digits) != 9 or digits[0] not in _VALID_FIRST:
        return None
    return digits


def display(key: str) -> str:
    """Hiển thị khoá 9 số dưới dạng số VN 10 chữ số (thêm 0 đầu)."""
    return "0" + key


def extract_phones(text: str) -> list[str]:
    """Trả về danh sách khoá 9 số (không trùng lặp, giữ thứ tự xuất hiện)."""
    seen: dict[str, None] = {}
    for m in _PHONE_RE.finditer(text or ""):
        key = normalize(m.group())
        if key and key not in seen:
            seen[key] = None
    return list(seen.keys())
