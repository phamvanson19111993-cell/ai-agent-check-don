"""So khớp nhãn (tag) Pancake, bỏ qua dấu tiếng Việt và hoa/thường."""

import unicodedata

# Các mã màu vàng Pancake hay dùng cho nhãn (dùng cho chế độ lọc theo màu).
YELLOW_HEXES = {
    "#ffc107", "#ffca28", "#ffd54f", "#f5c343", "#f1c40f", "#ffeb3b",
    "#fdd835", "#e6c84f", "#d9c56b", "#e0d16a", "#ffdd57",
}


def fold(text):
    """Bỏ dấu tiếng Việt, chuyển thường, gom khoảng trắng."""
    if text is None:
        return ""
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "d")
    return " ".join(text.lower().split())


def tag_name(tag):
    """Lấy tên nhãn từ nhiều kiểu dữ liệu Pancake trả về (dict hoặc chuỗi)."""
    if isinstance(tag, dict):
        for key in ("text", "name", "title", "label", "tag_name"):
            value = tag.get(key)
            if value:
                return str(value)
        return ""
    return str(tag or "")


def tag_color(tag):
    if isinstance(tag, dict):
        for key in ("color", "colour", "background", "bg_color"):
            value = tag.get(key)
            if value:
                return str(value).strip().lower()
    return ""


def is_yellow(tag):
    color = tag_color(tag)
    if not color:
        return False
    if not color.startswith("#"):
        color = "#" + color
    if len(color) == 4:  # #fc0 -> #ffcc00
        color = "#" + "".join(ch * 2 for ch in color[1:])
    return color in YELLOW_HEXES


def matches(tag, wanted_names, match_yellow=False):
    """Nhãn này có phải nhãn 'đã chốt đơn' không?

    So khớp linh hoạt: 'CHỐT ĐƠN' khớp cả 'Đã chốt đơn', 'chot don Hạnh'...
    """
    if match_yellow and is_yellow(tag):
        return True
    name = fold(tag_name(tag))
    if not name:
        return False
    for wanted in wanted_names:
        wanted = fold(wanted)
        if wanted and (wanted in name or name in wanted):
            return True
    return False


def conversation_tags(conversation):
    """Trích danh sách nhãn của một hội thoại, chịu được nhiều kiểu payload."""
    for key in ("tags", "tag_ids", "labels", "conversation_tags"):
        value = conversation.get(key)
        if isinstance(value, list) and value:
            return value
        if isinstance(value, dict) and value:
            return list(value.values())
    return []


def has_closed_tag(conversation, wanted_names, match_yellow=False, tag_lookup=None):
    """True nếu hội thoại đã được gắn nhãn chốt đơn."""
    for tag in conversation_tags(conversation):
        # Trường hợp API chỉ trả về id nhãn -> tra ngược qua bảng nhãn của page.
        if tag_lookup is not None and not isinstance(tag, dict):
            resolved = tag_lookup.get(str(tag))
            if resolved is not None:
                tag = resolved
        if matches(tag, wanted_names, match_yellow=match_yellow):
            return True
    return False


def tag_names_of(conversation, tag_lookup=None):
    names = []
    for tag in conversation_tags(conversation):
        if tag_lookup is not None and not isinstance(tag, dict):
            tag = tag_lookup.get(str(tag), tag)
        name = tag_name(tag)
        if name:
            names.append(name)
    return names
