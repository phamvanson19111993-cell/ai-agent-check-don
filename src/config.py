"""Nạp cấu hình kết nối Odoo từ biến môi trường / file .env."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:  # python-dotenv là tùy chọn khi chạy; không có thì bỏ qua
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - môi trường không có dotenv
    pass


@dataclass
class OdooConfig:
    """Thông tin cấu hình để kết nối một instance Odoo."""

    url: str
    db: str
    username: str = ""
    password: str = ""
    session_id: str = ""
    max_retries: int = 4
    timeout: int = 30

    @property
    def uses_session(self) -> bool:
        """True nếu ưu tiên dùng cookie session_id thay vì đăng nhập user/pass."""
        return bool(self.session_id)

    def validate(self) -> None:
        """Kiểm tra cấu hình tối thiểu, ném ValueError nếu thiếu."""
        if not self.url:
            raise ValueError("Thiếu ODOO_URL")
        if not self.db:
            raise ValueError("Thiếu ODOO_DB")
        if not self.uses_session and not (self.username and self.password):
            raise ValueError(
                "Cần ODOO_USERNAME + ODOO_PASSWORD (hoặc API key), "
                "hoặc ODOO_SESSION_ID."
            )


def load_config() -> OdooConfig:
    """Đọc cấu hình từ môi trường và trả về OdooConfig."""

    def _int(name: str, default: int) -> int:
        raw = os.getenv(name, "").strip()
        try:
            return int(raw) if raw else default
        except ValueError:
            return default

    return OdooConfig(
        url=os.getenv("ODOO_URL", "").strip().rstrip("/"),
        db=os.getenv("ODOO_DB", "").strip(),
        username=os.getenv("ODOO_USERNAME", "").strip(),
        password=os.getenv("ODOO_PASSWORD", "").strip(),
        session_id=os.getenv("ODOO_SESSION_ID", "").strip(),
        max_retries=_int("ODOO_MAX_RETRIES", 4),
        timeout=_int("ODOO_TIMEOUT", 30),
    )
