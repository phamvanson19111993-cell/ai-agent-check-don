# -*- coding: utf-8 -*-
"""Dựng nội dung báo cáo gửi Telegram — bám sát mẫu định dạng của DiLi Supplement."""
from datetime import datetime
from zoneinfo import ZoneInfo

import config
from phone_utils import display

_SEP = "────────────"


def _now_str() -> str:
    now = datetime.now(ZoneInfo(config.TZ_NAME))
    return now.strftime("%H:%M %d/%m/%Y")


def build_report(key: str, matches: list[dict]) -> str:
    """key: khoá 9 số cuối; matches: các dòng trùng trong Sheet."""
    phone = display(key)
    if not matches:
        return (
            "❌ Không trùng\n"
            f"📞 {phone}\n"
            "(Đã đối chiếu toàn bộ các tab trong Sheet, không thấy số này)\n"
            f"🕒 {_now_str()}"
        )

    lines = [
        f"⚠️ TRÙNG ĐƠN — số đã có trong Sheet ({len(matches)} dòng)",
        f"📞 {phone}",
        _SEP,
    ]
    for i, m in enumerate(matches, 1):
        lines.append(
            f"#{i} Khách: {m['customer']} | Ngày: {m['date']} | "
            f"SẢN PHẨM: {m['product']} | Trạng thái: {m['status']} | 📄 Tab: {m['tab']}"
        )
        lines.append(_SEP)
    lines.append(f"📌 Xử lý trùng đơn DiLi Supplement · 🕒 {_now_str()}")
    return "\n".join(lines)
