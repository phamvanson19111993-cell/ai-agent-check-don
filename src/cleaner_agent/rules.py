"""Bộ quy tắc nhận diện rác theo từng hệ điều hành."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config, expand


@dataclass
class Rule:
    """Một quy tắc quét rác.

    `roots` là các thư mục để quét. `patterns` là glob tương đối bên trong root
    ("**/*" nghĩa là mọi thứ). Chỉ file/thư mục cũ hơn `min_age_days` mới bị tính.
    """

    id: str
    description: str
    roots: list[str]
    patterns: list[str] = field(default_factory=lambda: ["**/*"])
    min_age_days: float = 7.0
    enabled: bool = True
    match_dirs: bool = False
    exclude: list[str] = field(default_factory=list)

    def resolved_roots(self) -> list[Path]:
        out = []
        for r in self.roots:
            p = expand(r)
            if "*" in str(p):
                # root có wildcard, ví dụ ~/.mozilla/firefox/*/cache2
                base = Path(str(p).split("*", 1)[0])
                pattern = str(p)[len(str(base)):].lstrip(os.sep).replace(os.sep, "/")
                if base.is_dir():
                    out.extend(m for m in base.glob(pattern) if m.is_dir())
            elif p.is_dir():
                out.append(p)
        return out


def _common_rules() -> list[Rule]:
    return [
        Rule(
            id="empty-dirs",
            description="Thư mục rỗng còn sót lại sau khi dọn",
            roots=["~/.cache"],
            patterns=["**/"],
            min_age_days=30,
            match_dirs=True,
            enabled=False,  # bật qua rules.enabled_extra
        ),
        Rule(
            id="old-downloads",
            description="File trong Downloads quá cũ (chỉ để AI xem xét, mặc định TẮT)",
            roots=["~/Downloads"],
            patterns=["*"],
            min_age_days=90,
            enabled=False,
        ),
        Rule(
            id="pip-cache",
            description="Cache của pip",
            roots=["~/.cache/pip", "~/Library/Caches/pip", "%LOCALAPPDATA%/pip/Cache"],
            min_age_days=30,
        ),
        Rule(
            id="npm-cache",
            description="Cache của npm",
            roots=["~/.npm/_cacache", "%LOCALAPPDATA%/npm-cache/_cacache"],
            min_age_days=30,
        ),
        Rule(
            id="yarn-cache",
            description="Cache của yarn",
            roots=["~/.cache/yarn", "~/Library/Caches/Yarn", "%LOCALAPPDATA%/Yarn/Cache"],
            min_age_days=30,
        ),
    ]


def _linux_rules() -> list[Rule]:
    return [
        Rule(
            id="user-cache",
            description="Cache ứng dụng trong ~/.cache",
            roots=["~/.cache"],
            min_age_days=7,
            exclude=["**/.ssh/**", "**/gnupg/**", "**/keyrings/**"],
        ),
        Rule(
            id="thumbnails",
            description="Ảnh thumbnail đã tạo lại được",
            roots=["~/.cache/thumbnails", "~/.thumbnails"],
            min_age_days=14,
        ),
        Rule(
            id="trash",
            description="Thùng rác đã quá hạn",
            roots=["~/.local/share/Trash/files", "~/.local/share/Trash/info"],
            min_age_days=7,
        ),
        Rule(
            id="tmp",
            description="File tạm trong /tmp thuộc sở hữu của bạn",
            roots=["/tmp", "/var/tmp"],
            min_age_days=3,
        ),
        Rule(
            id="browser-cache",
            description="Cache trình duyệt (tự sinh lại được)",
            roots=[
                "~/.cache/google-chrome/*/Cache",
                "~/.cache/chromium/*/Cache",
                "~/.cache/mozilla/firefox/*/cache2",
                "~/.cache/BraveSoftware/*/Cache",
            ],
            min_age_days=7,
        ),
        Rule(
            id="crash-reports",
            description="Báo cáo lỗi/core dump cũ",
            roots=["/var/crash", "~/.local/share/apport"],
            min_age_days=14,
        ),
    ]


def _macos_rules() -> list[Rule]:
    return [
        Rule(
            id="user-cache",
            description="Cache ứng dụng trong ~/Library/Caches",
            roots=["~/Library/Caches"],
            min_age_days=7,
            exclude=["**/CloudKit/**", "**/com.apple.keychain*/**"],
        ),
        Rule(
            id="logs",
            description="Log ứng dụng cũ",
            roots=["~/Library/Logs"],
            min_age_days=14,
        ),
        Rule(
            id="trash",
            description="Thùng rác đã quá hạn",
            roots=["~/.Trash"],
            min_age_days=7,
        ),
        Rule(
            id="crash-reports",
            description="Báo cáo lỗi cũ",
            roots=["~/Library/Application Support/CrashReporter", "~/Library/Logs/DiagnosticReports"],
            min_age_days=14,
        ),
        Rule(
            id="ios-backups-cache",
            description="Cache cập nhật phần mềm iOS",
            roots=["~/Library/Caches/com.apple.dt.Xcode", "~/Library/Developer/Xcode/DerivedData"],
            min_age_days=30,
        ),
    ]


def _windows_rules() -> list[Rule]:
    return [
        Rule(
            id="user-temp",
            description="Thư mục Temp của người dùng",
            roots=["%LOCALAPPDATA%/Temp", "%TEMP%"],
            min_age_days=3,
        ),
        Rule(
            id="inet-cache",
            description="Cache Internet của Windows",
            roots=["%LOCALAPPDATA%/Microsoft/Windows/INetCache"],
            min_age_days=7,
        ),
        Rule(
            id="crash-reports",
            description="Crash dump cũ",
            roots=["%LOCALAPPDATA%/CrashDumps"],
            min_age_days=14,
        ),
        Rule(
            id="browser-cache",
            description="Cache trình duyệt (tự sinh lại được)",
            roots=[
                "%LOCALAPPDATA%/Google/Chrome/User Data/*/Cache",
                "%LOCALAPPDATA%/Microsoft/Edge/User Data/*/Cache",
                "%LOCALAPPDATA%/Mozilla/Firefox/Profiles/*/cache2",
            ],
            min_age_days=7,
        ),
        Rule(
            id="windows-update-cache",
            description="Bộ nhớ tạm giao hàng cập nhật",
            roots=["%LOCALAPPDATA%/Microsoft/Windows/Explorer/ThumbCacheToDelete"],
            min_age_days=14,
        ),
    ]


def _zalo_rules() -> list[Rule]:
    """Zalo: tách bạch cache (an toàn) và kho ảnh đã nhận (dữ liệu cá nhân)."""
    return [
        Rule(
            id="zalo-cache",
            description="Cache Zalo — ảnh xem trước, thumbnail, media tự tải (tải lại được)",
            roots=[
                "%APPDATA%/ZaloPC/*/cache",
                "%APPDATA%/ZaloPC/*/Cache",
                "%LOCALAPPDATA%/ZaloPC/*/cache",
                "~/Library/Caches/com.vng.zalo",
                "~/Library/Application Support/Zalo/*/Cache",
                "~/.cache/zalo",
            ],
            min_age_days=14,
        ),
        Rule(
            id="zalo-media",
            description=(
                "Ảnh/file Zalo đã nhận — ĐÂY LÀ DỮ LIỆU CÁ NHÂN, không phải rác. "
                "Chỉ chạy sau khi bạn tự sao lưu và gỡ bảo vệ thư mục trong config."
            ),
            roots=[
                "~/Documents/Zalo Received Files",
                "~/Downloads/Zalo Received Files",
            ],
            patterns=["*"],
            min_age_days=365,
            enabled=False,  # phải bật thủ công qua rules.enabled_extra
        ),
    ]


def platform_rules() -> list[Rule]:
    """Trả về bộ quy tắc mặc định cho hệ điều hành hiện tại."""
    if sys.platform == "win32":
        base = _windows_rules()
    elif sys.platform == "darwin":
        base = _macos_rules()
    else:
        base = _linux_rules()
    return base + _common_rules() + _zalo_rules()


def active_rules(cfg: Config) -> list[Rule]:
    """Áp dụng cấu hình người dùng lên bộ quy tắc mặc định."""
    rules = platform_rules()
    disabled = set(cfg.rules.disabled)
    extra = set(cfg.rules.enabled_extra)

    out: list[Rule] = []
    for rule in rules:
        if rule.id in disabled:
            continue
        if rule.id in extra:
            rule.enabled = True
        if not rule.enabled:
            continue
        override = cfg.rules.overrides.get(rule.id, {})
        if "min_age_days" in override:
            rule.min_age_days = float(override["min_age_days"])
        out.append(rule)
    return out
