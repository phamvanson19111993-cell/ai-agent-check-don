"""Đọc cấu hình từ biến môi trường / file .env."""

import os

DEFAULT_API_BASE = "https://pages.fm/api"
DEFAULT_CLOSED_TAGS = "CHỐT ĐƠN"
# File Drive "SĐT chưa chốt Pancake - 3 tháng gần nhất"
DEFAULT_SHEET_ID = "1_SjwNvfzPMUzAjeDJ46MmCsSXYcmZ_cggj6NKz5kJjk"


def load_dotenv(path=".env"):
    """Nạp biến môi trường từ file .env (không ghi đè biến đã có sẵn)."""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


class Config:
    def __init__(self, args=None):
        load_dotenv()
        get = os.environ.get
        self.access_token = getattr(args, "token", None) or get("PANCAKE_ACCESS_TOKEN", "")
        self.page_id = getattr(args, "page_id", None) or get("PANCAKE_PAGE_ID", "")
        self.api_base = (
            getattr(args, "api_base", None) or get("PANCAKE_API_BASE") or DEFAULT_API_BASE
        ).rstrip("/")

        raw_tags = getattr(args, "closed_tag", None) or get("PANCAKE_CLOSED_TAGS", DEFAULT_CLOSED_TAGS)
        if isinstance(raw_tags, str):
            raw_tags = raw_tags.split(",")
        self.closed_tags = [t.strip() for t in raw_tags if t and t.strip()]

        self.service_account_file = get("GOOGLE_SERVICE_ACCOUNT_FILE", "")
        self.sheet_id = getattr(args, "sheet_id", None) or get("GSHEET_ID", DEFAULT_SHEET_ID)
        self.sheet_tab = get("GSHEET_TAB", "")

    def require_pancake(self):
        missing = []
        if not self.access_token:
            missing.append("PANCAKE_ACCESS_TOKEN")
        if not self.page_id:
            missing.append("PANCAKE_PAGE_ID")
        if missing:
            raise SystemExit(
                "Thiếu cấu hình: %s.\n"
                "Hãy copy .env.example thành .env rồi điền thông tin "
                "(Pancake -> Cấu hình -> Cấu hình ứng dụng -> Webhook & API Key)."
                % ", ".join(missing)
            )
