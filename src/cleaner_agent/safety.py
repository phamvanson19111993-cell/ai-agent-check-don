"""Hàng rào an toàn: những nơi agent không bao giờ được đụng tới.

Đây là tầng phòng thủ cuối cùng — mọi ứng viên xoá đều phải đi qua `guard.check()`
trước khi được chuyển vào khu cách ly.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

# Thư mục dữ liệu cá nhân: không bao giờ quét, không bao giờ xoá.
_PERSONAL_DIR_NAMES = (
    "Documents", "Desktop", "Pictures", "Videos", "Music", "Movies",
    "Public", "Templates", "Tài liệu", "Máy tính",
)

# Thư mục nhạy cảm (khoá, cấu hình xác thực) — kể cả khi nằm trong ~/.cache.
_SENSITIVE_DIR_NAMES = (
    ".ssh", ".gnupg", ".aws", ".kube", ".docker", ".password-store",
    ".mozilla/firefox/profiles.ini", "Keychains", ".config/gh",
)

# Đuôi file không bao giờ xoá tự động, dù nằm trong thư mục cache.
_NEVER_DELETE_SUFFIXES = (
    ".key", ".pem", ".p12", ".pfx", ".keystore", ".jks",
    ".kdbx", ".sqlite", ".db-wal", ".gpg", ".asc",
)

# Tên thư mục báo hiệu "đây là mã nguồn / dữ liệu đang dùng".
_PROJECT_MARKERS = (".git", ".hg", ".svn")


def _system_roots() -> list[Path]:
    if sys.platform == "win32":
        drive = Path(os.environ.get("SystemDrive", "C:") + "\\")
        return [
            drive / "Windows",
            drive / "Program Files",
            drive / "Program Files (x86)",
            drive / "ProgramData" / "Microsoft" / "Windows Defender",
            drive,
        ]
    if sys.platform == "darwin":
        return [
            Path("/"), Path("/System"), Path("/Library"), Path("/Applications"),
            Path("/usr"), Path("/bin"), Path("/sbin"), Path("/etc"), Path("/var"),
            Path("/private/etc"), Path("/opt"),
        ]
    return [
        Path("/"), Path("/usr"), Path("/bin"), Path("/sbin"), Path("/lib"),
        Path("/lib64"), Path("/etc"), Path("/boot"), Path("/dev"), Path("/proc"),
        Path("/sys"), Path("/opt"), Path("/srv"), Path("/var/lib"),
    ]


@dataclass(frozen=True)
class Verdict:
    """Kết quả kiểm tra an toàn."""

    allowed: bool
    reason: str = ""

    def __bool__(self) -> bool:  # cho phép `if verdict:`
        return self.allowed


ALLOWED = Verdict(True)


def is_within(path: Path, root: Path) -> bool:
    """True nếu `path` nằm trong (hoặc chính là) `root`, so sánh sau khi resolve."""
    try:
        p = path.resolve(strict=False)
        r = root.resolve(strict=False)
    except (OSError, RuntimeError):
        return False
    return p == r or r in p.parents


class Guard:
    """Kiểm tra một đường dẫn có được phép dọn hay không."""

    def __init__(
        self,
        extra_protected: list[Path] | None = None,
        follow_symlinks: bool = False,
        quarantine_dir: Path | None = None,
        unprotect: list[Path] | None = None,
    ) -> None:
        home = Path.home()
        self.home = home.resolve(strict=False)
        self.follow_symlinks = follow_symlinks
        self.unprotected = [p.resolve(strict=False) for p in (unprotect or [])]

        # `unprotect` chỉ có hiệu lực với thư mục cá nhân nằm trong home, và không
        # bao giờ gỡ được bảo vệ cho thư mục hệ thống, thư mục nhạy cảm, hay chính home.
        sensitive = {(home / n).resolve(strict=False) for n in _SENSITIVE_DIR_NAMES}
        self.unprotected = [
            p
            for p in self.unprotected
            if is_within(p, self.home)
            and p != self.home
            and not any(is_within(p, s) or p == s for s in sensitive)
        ]

        protected: list[Path] = list(_system_roots())
        protected.append(home)  # bản thân thư mục home, không phải nội dung bên trong
        protected.extend(home / name for name in _PERSONAL_DIR_NAMES)
        protected.extend(home / name for name in _SENSITIVE_DIR_NAMES)
        if quarantine_dir is not None:
            protected.append(quarantine_dir)
        protected.extend(extra_protected or [])

        self.protected = [p.resolve(strict=False) for p in protected]
        # `home` và các ổ đĩa gốc là "chặn xoá chính nó" chứ không chặn cả cây con.
        self._self_only = {self.home, *(r.resolve(strict=False) for r in _system_roots() if r == Path("/") or str(r).endswith(":\\"))}

    def check(self, path: Path) -> Verdict:
        """Trả về Verdict cho biết `path` có được phép dọn không, kèm lý do."""
        try:
            resolved = path.resolve(strict=False)
        except (OSError, RuntimeError) as exc:
            return Verdict(False, f"không resolve được đường dẫn: {exc}")

        if not self.follow_symlinks and path.is_symlink():
            return Verdict(False, "là symlink (đang tắt follow_symlinks)")

        if resolved == resolved.parent:
            return Verdict(False, "là thư mục gốc của ổ đĩa")

        # Người dùng đã chủ động gỡ bảo vệ cho nhánh này.
        exempt = any(is_within(resolved, u) for u in self.unprotected)

        for prot in self.protected:
            if resolved == prot:
                return Verdict(False, f"trùng thư mục được bảo vệ: {prot}")
            if prot in self._self_only:
                continue
            if is_within(resolved, prot):
                if exempt:
                    continue
                return Verdict(False, f"nằm trong thư mục được bảo vệ: {prot}")

        if resolved.suffix.lower() in _NEVER_DELETE_SUFFIXES:
            return Verdict(False, f"đuôi file nhạy cảm: {resolved.suffix}")

        for marker in _PROJECT_MARKERS:
            if marker in resolved.parts:
                return Verdict(False, f"nằm trong thư mục quản lý phiên bản ({marker})")

        # Không đụng vào file đang được tiến trình khác ghi (heuristic: file .lock/.pid)
        if resolved.name.endswith((".lock", ".pid")) or resolved.name == "lockfile":
            return Verdict(False, "là file khoá của tiến trình đang chạy")

        return ALLOWED

    def is_protected_root(self, path: Path) -> bool:
        """True nếu không nên *quét* vào bên trong đường dẫn này."""
        return not self.check(path).allowed and not is_within(path, self.home)
