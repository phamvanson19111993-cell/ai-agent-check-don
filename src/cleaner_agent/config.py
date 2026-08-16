"""Đọc/ghi cấu hình (TOML) cho agent."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "cleaner-agent" / "config.toml"
DEFAULT_STATE_DIR = Path.home() / ".local" / "share" / "cleaner-agent"


def expand(p: str | Path) -> Path:
    """Mở rộng ~ và biến môi trường (%TEMP%, $HOME...) thành đường dẫn tuyệt đối."""
    text = os.path.expandvars(str(p))
    # Windows dùng %VAR%; os.path.expandvars đã xử lý cả hai dạng.
    return Path(text).expanduser()


@dataclass
class GeneralConfig:
    dry_run: bool = True
    interval_minutes: int = 60
    max_delete_per_run: int = 5000
    max_bytes_per_run: int = 20 * 1024**3  # 20 GB
    min_free_gb: float = 0.0  # 0 = luôn dọn; >0 = chỉ dọn khi đĩa còn ít hơn mức này


@dataclass
class QuarantineConfig:
    enabled: bool = True
    dir: Path = field(default_factory=lambda: DEFAULT_STATE_DIR / "quarantine")
    retention_days: int = 7


@dataclass
class SafetyConfig:
    extra_protected: list[Path] = field(default_factory=list)
    follow_symlinks: bool = False
    # Gỡ bảo vệ cho một thư mục cá nhân cụ thể. Đây là hành động có chủ đích:
    # phải ghi rõ từng đường dẫn, không nhận wildcard, không nhận thư mục gốc.
    unprotect: list[Path] = field(default_factory=list)


@dataclass
class AIConfig:
    enabled: bool = False
    model: str = "claude-opus-5"
    review_roots: list[Path] = field(default_factory=list)
    min_age_days: int = 30
    max_files_per_call: int = 200


@dataclass
class RulesConfig:
    disabled: list[str] = field(default_factory=list)
    enabled_extra: list[str] = field(default_factory=list)
    overrides: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass
class Config:
    general: GeneralConfig = field(default_factory=GeneralConfig)
    quarantine: QuarantineConfig = field(default_factory=QuarantineConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    rules: RulesConfig = field(default_factory=RulesConfig)
    state_dir: Path = field(default_factory=lambda: DEFAULT_STATE_DIR)
    source_path: Path | None = None


def load(path: Path | None = None) -> Config:
    """Đọc config từ file TOML; thiếu file thì dùng mặc định an toàn."""
    cfg = Config()
    path = path or DEFAULT_CONFIG_PATH
    if not path.exists():
        return cfg

    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    cfg.source_path = path

    g = raw.get("general", {})
    cfg.general = GeneralConfig(
        dry_run=bool(g.get("dry_run", True)),
        interval_minutes=int(g.get("interval_minutes", 60)),
        max_delete_per_run=int(g.get("max_delete_per_run", 5000)),
        max_bytes_per_run=int(g.get("max_bytes_per_run", 20 * 1024**3)),
        min_free_gb=float(g.get("min_free_gb", 0.0)),
    )

    q = raw.get("quarantine", {})
    cfg.quarantine = QuarantineConfig(
        enabled=bool(q.get("enabled", True)),
        dir=expand(q.get("dir", DEFAULT_STATE_DIR / "quarantine")),
        retention_days=int(q.get("retention_days", 7)),
    )

    s = raw.get("safety", {})
    cfg.safety = SafetyConfig(
        extra_protected=[expand(p) for p in s.get("extra_protected", [])],
        follow_symlinks=bool(s.get("follow_symlinks", False)),
        unprotect=[expand(p) for p in s.get("unprotect", []) if "*" not in str(p)],
    )

    a = raw.get("ai", {})
    cfg.ai = AIConfig(
        enabled=bool(a.get("enabled", False)),
        model=str(a.get("model", "claude-opus-5")),
        review_roots=[expand(p) for p in a.get("review_roots", [])],
        min_age_days=int(a.get("min_age_days", 30)),
        max_files_per_call=int(a.get("max_files_per_call", 200)),
    )

    r = raw.get("rules", {})
    cfg.rules = RulesConfig(
        disabled=list(r.get("disabled", [])),
        enabled_extra=list(r.get("enabled_extra", [])),
        overrides={k: v for k, v in r.items() if isinstance(v, dict)},
    )

    if "state_dir" in raw:
        cfg.state_dir = expand(raw["state_dir"])

    return cfg


TEMPLATE = """\
# Cấu hình AI Agent dọn rác.
# Mọi giá trị dưới đây là mặc định — sửa theo nhu cầu của bạn.

[general]
# true = chỉ báo cáo, KHÔNG đụng vào file. Đổi thành false (hoặc chạy với --apply)
# khi bạn đã xem báo cáo và thấy an toàn.
dry_run = true
interval_minutes = 60          # chu kỳ quét khi chạy chế độ `watch`
max_delete_per_run = 5000      # trần số file mỗi lượt
max_bytes_per_run = 21474836480  # trần dung lượng mỗi lượt (20 GB)
min_free_gb = 0                # >0: chỉ dọn khi ổ đĩa còn trống ít hơn mức này

[quarantine]
# File bị "xoá" thực chất được chuyển vào đây, có thể khôi phục lại.
enabled = true
retention_days = 7             # sau ngần này ngày mới xoá hẳn khỏi khu cách ly

[safety]
# Thêm thư mục bạn muốn agent TUYỆT ĐỐI không đụng tới.
extra_protected = []
follow_symlinks = false
# Mặc định Documents/Desktop/Pictures/... được bảo vệ tuyệt đối.
# Muốn agent đụng tới một thư mục cá nhân (ví dụ kho ảnh Zalo đã tải về),
# bạn phải ghi rõ từng đường dẫn ở đây — đây là hành động có chủ đích.
#   unprotect = ["~/Documents/Zalo Received Files"]
unprotect = []

[ai]
# Bật để Claude đánh giá các file "khó xử" (ví dụ trong Downloads).
# Chỉ gửi metadata (tên, kích thước, tuổi file) — KHÔNG gửi nội dung file.
enabled = false
model = "claude-opus-5"
review_roots = ["~/Downloads"]
min_age_days = 30
max_files_per_call = 200

[rules]
# Tắt bớt quy tắc theo id, ví dụ: disabled = ["browser-cache", "trash"]
disabled = []
# Bật thêm quy tắc mặc định tắt, ví dụ: enabled_extra = ["empty-dirs", "old-downloads"]
enabled_extra = []
"""


def write_template(path: Path | None = None) -> Path:
    """Ghi file config mẫu; không ghi đè nếu đã tồn tại."""
    path = path or DEFAULT_CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(TEMPLATE, encoding="utf-8")
    return path
