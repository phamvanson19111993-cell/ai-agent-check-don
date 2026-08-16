"""Hiển thị và lưu báo cáo."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .cleaner import RunReport


def human_size(n: int) -> str:
    step = 1024.0
    value = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(value) < step:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= step
    return f"{value:.1f} PB"


def render(report: RunReport, verbose: bool = False, top: int = 15) -> str:
    when = datetime.fromtimestamp(report.started_at).strftime("%Y-%m-%d %H:%M:%S")
    mode = "CHẠY THỬ (không đụng file nào)" if report.dry_run else "ĐÃ THỰC THI"

    lines = [
        f"╭─ Dọn rác — {when}",
        f"│  Chế độ      : {mode}",
        f"│  Đã quét     : {report.scanned_roots} thư mục gốc trong {report.duration_s:.1f}s",
        f"│  Tìm thấy    : {report.found} mục · {human_size(report.found_bytes)}",
    ]

    if report.dry_run:
        lines.append(f"│  Sẽ dọn      : {report.found} mục · {human_size(report.found_bytes)}")
    else:
        lines.append(f"│  Đã dọn      : {report.cleaned} mục · {human_size(report.cleaned_bytes)}")
        if report.purged:
            lines.append(
                f"│  Xoá hẳn     : {report.purged} mục quá hạn cách ly "
                f"· {human_size(report.purged_bytes)}"
            )

    if report.held:
        lines.append(f"│  Giữ lại     : {report.held} mục cần bạn tự xem")
    if report.note:
        lines.append(f"│  Lưu ý       : {report.note}")
    if report.errors:
        lines.append(f"│  Lỗi         : {len(report.errors)}")

    if report.items:
        lines.append("│")
        lines.append(f"│  {min(top, len(report.items))} mục lớn nhất:")
        for item in report.items[:top]:
            lines.append(
                f"│    {human_size(item['size']):>9}  "
                f"{item['age_days']:>6.0f}d  [{item['rule_id']}]  {item['path']}"
            )
        if len(report.items) > top:
            lines.append(f"│    … và {len(report.items) - top} mục khác")

    if verbose and report.skipped:
        lines.append("│")
        lines.append("│  Lý do bỏ qua:")
        for reason, count in sorted(report.skipped.items(), key=lambda kv: -kv[1])[:10]:
            lines.append(f"│    {count:>6}×  {reason}")

    if verbose and report.errors:
        lines.append("│")
        lines.append("│  Lỗi chi tiết:")
        for err in report.errors[:10]:
            lines.append(f"│    {err}")

    lines.append("╰─")
    if report.dry_run and report.found:
        lines.append("")
        lines.append("Xem ổn rồi thì chạy lại với --apply để thực sự dọn.")
        lines.append("File bị dọn sẽ vào khu cách ly, khôi phục được bằng lệnh `restore`.")

    return "\n".join(lines)


def save(report: RunReport, state_dir: Path) -> Path:
    """Ghi báo cáo JSON vào lịch sử."""
    hist = state_dir / "reports"
    hist.mkdir(parents=True, exist_ok=True)
    stamp = datetime.fromtimestamp(report.started_at).strftime("%Y%m%d-%H%M%S")
    path = hist / f"{stamp}.json"
    path.write_text(
        json.dumps(report.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    latest = state_dir / "last-report.json"
    latest.write_text(
        json.dumps(report.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path
