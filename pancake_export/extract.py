"""Chuyển hội thoại Pancake thành dòng dữ liệu 'khách chưa chốt đơn'."""

import datetime

from . import phones, tagging

_NAME_KEYS = ("customer_name", "name", "from_name", "title", "page_customer_name")
_TIME_KEYS = ("updated_at", "last_sent_at", "inserted_at", "last_message_at", "created_at", "time")
_PHONE_KEYS = ("recent_phone_numbers", "phone_numbers", "phone", "phones", "customer_phone")
_SNIPPET_KEYS = ("snippet", "last_message", "last_sent_message", "message", "preview")


def _first(conversation, keys):
    for key in keys:
        value = conversation.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def customer_name(conversation):
    value = _first(conversation, _NAME_KEYS)
    if isinstance(value, dict):
        value = value.get("name") or value.get("text")
    return str(value).strip() if value else ""


def snippet(conversation):
    value = _first(conversation, _SNIPPET_KEYS)
    if isinstance(value, dict):
        value = value.get("message") or value.get("text") or value.get("content")
    return " ".join(str(value).split()) if value else ""


def parse_time(value):
    """Chuyển nhiều kiểu thời gian Pancake về datetime (None nếu không đọc được)."""
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        number = float(value)
        if number > 1e11:  # mili giây
            number /= 1000.0
        try:
            return datetime.datetime.fromtimestamp(number)
        except (OverflowError, OSError, ValueError):
            return None
    text = str(value).strip().replace("Z", "+00:00")
    for parser in (
        lambda t: datetime.datetime.fromisoformat(t),
        lambda t: datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S"),
        lambda t: datetime.datetime.strptime(t, "%d/%m/%Y %H:%M"),
        lambda t: datetime.datetime.strptime(t, "%d/%m/%Y"),
    ):
        try:
            parsed = parser(text)
            return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
        except (ValueError, TypeError):
            continue
    return None


def conversation_time(conversation):
    for key in _TIME_KEYS:
        parsed = parse_time(conversation.get(key))
        if parsed:
            return parsed
    return None


def conversation_phones(conversation, messages=None):
    """Gom số điện thoại: ưu tiên field sẵn có, sau đó dò trong nội dung chat."""
    found = phones.extract_many(*(conversation.get(key) for key in _PHONE_KEYS))
    if not found:
        found = phones.extract_many(
            snippet(conversation),
            conversation.get("customer"),
            conversation.get("note"),
        )
    if not found and messages:
        found = phones.extract_many(messages)
    return found


def conversation_link(page_id, conversation):
    conversation_id = (
        conversation.get("id")
        or conversation.get("conversation_id")
        or conversation.get("thread_id")
    )
    if not conversation_id:
        return "https://pancake.vn/%s" % page_id
    return "https://pancake.vn/%s?c_id=%s" % (page_id, conversation_id)


def build_row(conversation, page_id, tag_lookup=None, messages=None):
    """Tạo dòng dữ liệu theo layout Google Sheet đang dùng.

    Cột: Tên | SĐT | Tình trạng | Ngày | Ghi chú
    """
    numbers = conversation_phones(conversation, messages)
    if not numbers:
        return None

    when = conversation_time(conversation)
    tags = tagging.tag_names_of(conversation, tag_lookup)
    note_parts = []
    if tags:
        note_parts.append("Nhãn: " + ", ".join(tags))
    text = snippet(conversation)
    if text:
        note_parts.append(text[:180])
    if len(numbers) > 1:
        note_parts.append("SĐT khác: " + ", ".join(numbers[1:]))

    return {
        "ten": customer_name(conversation),
        "sdt": numbers[0],
        "tinh_trang": "Chưa chốt",
        "ngay": when.strftime("%d/%m") if when else "",
        "ghi_chu": " | ".join(note_parts),
        "thoi_gian": when.strftime("%Y-%m-%d %H:%M") if when else "",
        "link": conversation_link(page_id, conversation),
    }


def collect(conversations, page_id, closed_tags, tag_lookup=None, match_yellow=False,
            fetch_messages=None):
    """Lọc hội thoại CHƯA có nhãn chốt đơn và trả về danh sách dòng + thống kê."""
    rows = []
    stats = {"tong": 0, "da_chot": 0, "khong_co_sdt": 0, "chua_chot": 0}
    seen_phones = set()

    for conversation in conversations:
        stats["tong"] += 1
        if tagging.has_closed_tag(conversation, closed_tags, match_yellow, tag_lookup):
            stats["da_chot"] += 1
            continue

        messages = None
        if fetch_messages and not conversation_phones(conversation):
            messages = fetch_messages(conversation)

        row = build_row(conversation, page_id, tag_lookup, messages)
        if row is None:
            stats["khong_co_sdt"] += 1
            continue
        if row["sdt"] in seen_phones:
            continue
        seen_phones.add(row["sdt"])
        stats["chua_chot"] += 1
        rows.append(row)

    rows.sort(key=lambda item: item["thoi_gian"], reverse=True)
    return rows, stats
