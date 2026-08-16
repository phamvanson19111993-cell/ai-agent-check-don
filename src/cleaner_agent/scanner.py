"""Quét hệ thống, tìm ứng viên rác theo bộ quy tắc."""

from __future__ import annotations

import fnmatch
import os
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path

from .rules import Rule
from .safety import Guard

_DAY = 86400.0


@dataclass
class Candidate:
    """Một file/thư mục được đề xuất dọn."""

    path: Path
    size: int
    mtime: float
    age_days: float
    rule_id: str
    reason: str
    is_dir: bool = False
    decision: str = "junk"  # junk | keep | review
    confidence: float = 1.0

    def as_dict(self) -> dict:
        return {
            "path": str(self.path),
            "size": self.size,
            "age_days": round(self.age_days, 1),
            "rule_id": self.rule_id,
            "reason": self.reason,
            "is_dir": self.is_dir,
            "decision": self.decision,
            "confidence": self.confidence,
        }


@dataclass
class ScanResult:
    candidates: list[Candidate] = field(default_factory=list)
    skipped: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    roots_scanned: list[Path] = field(default_factory=list)

    @property
    def total_bytes(self) -> int:
        return sum(c.size for c in self.candidates)

    def note_skip(self, reason: str) -> None:
        self.skipped[reason] = self.skipped.get(reason, 0) + 1


def _matches(rel: str, patterns: list[str]) -> bool:
    if not patterns:
        return True
    for pat in patterns:
        if pat in ("**/*", "**", "*"):
            return True
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(rel, pat.lstrip("*/")):
            return True
    return False


def _excluded(rel: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel, pat) for pat in patterns)


def free_bytes(path: Path) -> int:
    """Dung lượng trống của ổ đĩa chứa `path`."""
    try:
        return shutil.disk_usage(path).free
    except OSError:
        return 0


def scan(rules: list[Rule], guard: Guard, now: float | None = None) -> ScanResult:
    """Duyệt các quy tắc và trả về danh sách ứng viên đã qua kiểm tra an toàn."""
    now = now if now is not None else time.time()
    result = ScanResult()
    seen: set[Path] = set()

    for rule in rules:
        cutoff = now - rule.min_age_days * _DAY
        for root in rule.resolved_roots():
            if guard.is_protected_root(root):
                result.note_skip(f"root được bảo vệ: {root}")
                continue
            result.roots_scanned.append(root)
            _scan_root(rule, root, cutoff, now, guard, result, seen)

    return result


def _scan_root(
    rule: Rule,
    root: Path,
    cutoff: float,
    now: float,
    guard: Guard,
    result: ScanResult,
    seen: set[Path],
) -> None:
    empty_dir_candidates: list[Path] = []

    for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        here = Path(dirpath)

        # Không đi vào thư mục được bảo vệ (ví dụ .ssh nằm lẫn trong cache).
        dirnames[:] = [d for d in dirnames if guard.check(here / d).allowed]

        if rule.match_dirs and not dirnames and not filenames and here != root:
            empty_dir_candidates.append(here)

        for name in filenames:
            fpath = here / name
            if fpath in seen:
                continue

            try:
                rel = str(fpath.relative_to(root)).replace(os.sep, "/")
            except ValueError:
                continue

            if not _matches(rel, rule.patterns):
                continue
            if _excluded(rel, rule.exclude):
                result.note_skip("khớp danh sách loại trừ của quy tắc")
                continue

            try:
                st = fpath.lstat()
            except OSError as exc:
                result.errors.append(f"{fpath}: {exc}")
                continue

            if st.st_mtime > cutoff:
                result.note_skip("chưa đủ tuổi")
                continue

            verdict = guard.check(fpath)
            if not verdict.allowed:
                result.note_skip(verdict.reason)
                continue

            seen.add(fpath)
            result.candidates.append(
                Candidate(
                    path=fpath,
                    size=st.st_size,
                    mtime=st.st_mtime,
                    age_days=(now - st.st_mtime) / _DAY,
                    rule_id=rule.id,
                    reason=rule.description,
                )
            )

    for d in empty_dir_candidates:
        if d in seen:
            continue
        verdict = guard.check(d)
        if not verdict.allowed:
            result.note_skip(verdict.reason)
            continue
        try:
            st = d.lstat()
        except OSError:
            continue
        if st.st_mtime > cutoff:
            continue
        seen.add(d)
        result.candidates.append(
            Candidate(
                path=d,
                size=0,
                mtime=st.st_mtime,
                age_days=(now - st.st_mtime) / _DAY,
                rule_id=rule.id,
                reason=rule.description,
                is_dir=True,
            )
        )
