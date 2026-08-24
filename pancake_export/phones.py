"""Nhận diện và chuẩn hoá số điện thoại Việt Nam."""

import re

# Bắt các cụm chữ số có thể chèn dấu chấm/gạch/khoảng trắng ở giữa,
# ví dụ: 0913.351.394 | 09666.111.04 | +84 913 351 394 | 0913-351-394
_RAW_PHONE = re.compile(r"(?:(?<![\d.,])|(?<=^))(\+?84|0)[\d.\-\s]{7,16}\d")

# Đầu số 11 chữ số cũ -> đầu số 10 chữ số hiện hành (chuyển đổi từ 2018).
_OLD_TO_NEW = {
    "0120": "070", "0121": "079", "0122": "077", "0126": "076", "0128": "078",
    "0123": "083", "0124": "084", "0125": "085", "0127": "081", "0129": "082",
    "0162": "032", "0163": "033", "0164": "034", "0165": "035", "0166": "036",
    "0167": "037", "0168": "038", "0169": "039",
    "0186": "056", "0188": "058", "0199": "059",
}

_MOBILE_PREFIXES = (
    "032", "033", "034", "035", "036", "037", "038", "039",   # Viettel
    "070", "076", "077", "078", "079",                         # Mobifone
    "081", "082", "083", "084", "085",                         # Vinaphone
    "086", "088", "089",                                       # Viettel/Vina/Mobi
    "090", "091", "092", "093", "094", "095", "096", "097", "098", "099",
    "056", "058", "059",                                       # Vietnamobile/Gmobile
    "052",
)


def normalize(raw):
    """Chuẩn hoá một chuỗi thành số điện thoại VN dạng 0xxxxxxxxx.

    Trả về None nếu không phải số điện thoại hợp lệ.
    """
    if raw is None:
        return None
    digits = re.sub(r"\D", "", str(raw))
    if not digits:
        return None

    # +84 / 84 -> 0
    if digits.startswith("840"):
        digits = "0" + digits[3:]
    elif digits.startswith("84") and len(digits) >= 11:
        digits = "0" + digits[2:]
    elif not digits.startswith("0"):
        digits = "0" + digits

    # Đầu số 11 số cũ -> 10 số mới
    if len(digits) == 11 and digits[:4] in _OLD_TO_NEW:
        digits = _OLD_TO_NEW[digits[:4]] + digits[4:]

    # Di động: 10 chữ số
    if len(digits) == 10 and digits[:3] in _MOBILE_PREFIXES:
        return digits

    # Cố định: 02x + 8 chữ số (tổng 10-11)
    if digits.startswith("02") and len(digits) in (10, 11):
        return digits

    return None


def extract(text):
    """Lấy toàn bộ số điện thoại hợp lệ xuất hiện trong một đoạn văn bản."""
    if not text:
        return []
    found = []
    for match in _RAW_PHONE.finditer(str(text)):
        phone = normalize(match.group(0))
        if phone and phone not in found:
            found.append(phone)
    return found


def extract_many(*values):
    """Gộp số điện thoại từ nhiều nguồn (chuỗi, list, dict lồng nhau)."""
    phones = []

    def walk(value):
        if value is None:
            return
        if isinstance(value, str):
            for phone in extract(value):
                if phone not in phones:
                    phones.append(phone)
        elif isinstance(value, (int, float)):
            phone = normalize(value)
            if phone and phone not in phones:
                phones.append(phone)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, (list, tuple, set)):
            for item in value:
                walk(item)

    for value in values:
        walk(value)
    return phones
