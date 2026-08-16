"""Điều phối một lượt dọn: quét → đánh giá → cách ly → báo cáo."""

from __future__ import annotations

import logging
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path

from .ai import Classifier, is_review_root, split_by_decision
from .config import Config
from .quarantine import Quarantine
from .rules import active_rules
from .safety import Guard
from .scanner import Candidate, ScanResult, free_bytes, scan

log = logging.getLogger(__name__)


@dataclass
class RunReport:
    started_at: float
    dry_run: bool
    scanned_roots: int = 0
    found: int = 0
    found_bytes: int = 0
    cleaned: int = 0
    cleaned_bytes: int = 0
    held: int = 0
    purged: int = 0
    purged_bytes: int = 0
    errors: list[str] = field(default_factory=list)
    skipped: dict[str, int] = field(default_factory=dict)
    items: list[dict] = field(default_factory=list)
    duration_s: float = 0.0
    note: str = ""

    def as_dict(self) -> dict:
        return {
            "started_at": self.started_at,
            "dry_run": self.dry_run,
            "scanned_roots": self.scanned_roots,
            "found": self.found,
            "found_bytes": self.found_bytes,
            "cleaned": self.cleaned,
            "cleaned_bytes": self.cleaned_bytes,
            "held": self.held,
            "purged": self.purged,
            "purged_bytes": self.purged_bytes,
            "errors": self.errors,
            "skipped": self.skipped,
            "duration_s": round(self.duration_s, 2),
            "note": self.note,
            "items": self.items,
        }


def build_guard(cfg: Config) -> Guard:
    return Guard(
        extra_protected=cfg.safety.extra_protected,
        follow_symlinks=cfg.safety.follow_symlinks,
        quarantine_dir=cfg.quarantine.dir,
        unprotect=cfg.safety.unprotect,
    )


def _should_run(cfg: Config) -> tuple[bool, str]:
    """Kiểm tra ngưỡng dung lượng trống trước khi dọn."""
    if cfg.general.min_free_gb <= 0:
        return True, ""
    free_gb = free_bytes(Path.home()) / 1024**3
    if free_gb >= cfg.general.min_free_gb:
        return False, (
            f"bỏ qua: đĩa còn trống {free_gb:.1f} GB, "
            f"trên ngưỡng {cfg.general.min_free_gb:.1f} GB"
        )
    return True, ""


def _apply_limits(cands: list[Candidate], cfg: Config) -> tuple[list[Candidate], str]:
    """Cắt danh sách theo trần số lượng và dung lượng mỗi lượt."""
    selected: list[Candidate] = []
    total = 0
    note = ""
    for c in cands:
        if len(selected) >= cfg.general.max_delete_per_run:
            note = f"đã chạm trần {cfg.general.max_delete_per_run} mục/lượt"
            break
        if total + c.size > cfg.general.max_bytes_per_run:
            note = f"đã chạm trần {cfg.general.max_bytes_per_run / 1024**3:.1f} GB/lượt"
            break
        selected.append(c)
        total += c.size
    return selected, note


def _remove(path: Path, is_dir: bool) -> None:
    if is_dir and not path.is_symlink():
        shutil.rmtree(path, ignore_errors=False)
    else:
        path.unlink(missing_ok=True)


def run_once(cfg: Config, apply: bool | None = None) -> RunReport:
    """Chạy một lượt dọn đầy đủ và trả về báo cáo."""
    started = time.time()
    dry_run = cfg.general.dry_run if apply is None else not apply
    report = RunReport(started_at=started, dry_run=dry_run)

    ok, why = _should_run(cfg)
    if not ok:
        report.note = why
        report.duration_s = time.time() - started
        return report

    guard = build_guard(cfg)
    result: ScanResult = scan(active_rules(cfg), guard)

    report.scanned_roots = len(result.roots_scanned)
    report.skipped = result.skipped
    report.errors.extend(result.errors)

    candidates = result.candidates

    # Những file nằm trong vùng "cần xem xét" đi qua Claude trước khi được đụng tới.
    if cfg.ai.enabled and cfg.ai.review_roots:
        review = [c for c in candidates if is_review_root(c.path, cfg.ai.review_roots)]
        certain = [c for c in candidates if c not in review]
        if review:
            classified = Classifier(cfg.ai).classify(review)
            approved, held = split_by_decision(classified)
            report.held = len(held)
            candidates = certain + approved
        else:
            candidates = certain
    else:
        # Không bật AI: mọi thứ trong review_roots đều được giữ lại cho an toàn.
        held = [c for c in candidates if is_review_root(c.path, cfg.ai.review_roots)]
        if held:
            report.held = len(held)
            candidates = [c for c in candidates if c not in held]

    report.found = len(candidates)
    report.found_bytes = sum(c.size for c in candidates)

    # Ưu tiên dọn file to trước để giải phóng dung lượng nhanh nhất.
    candidates.sort(key=lambda c: c.size, reverse=True)
    selected, limit_note = _apply_limits(candidates, cfg)
    if limit_note:
        report.note = limit_note

    report.items = [c.as_dict() for c in selected]

    if dry_run:
        report.duration_s = time.time() - started
        return report

    quarantine = Quarantine(cfg.quarantine.dir, cfg.quarantine.retention_days)
    for cand in selected:
        # Kiểm tra lại ngay trước khi động vào: file có thể đã đổi trạng thái.
        verdict = guard.check(cand.path)
        if not verdict.allowed:
            report.errors.append(f"{cand.path}: chặn ở lần kiểm tra cuối ({verdict.reason})")
            continue
        if not cand.path.exists() and not cand.path.is_symlink():
            continue
        try:
            if cfg.quarantine.enabled:
                quarantine.store(cand.path, cand.rule_id, cand.size)
            else:
                _remove(cand.path, cand.is_dir)
            report.cleaned += 1
            report.cleaned_bytes += cand.size
        except OSError as exc:
            report.errors.append(f"{cand.path}: {exc}")

    if cfg.quarantine.enabled:
        purged, freed = quarantine.purge()
        report.purged = purged
        report.purged_bytes = freed

    report.duration_s = time.time() - started
    return report
