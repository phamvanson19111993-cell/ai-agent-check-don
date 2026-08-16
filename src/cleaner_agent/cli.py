"""Giao diện dòng lệnh."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, config as config_mod, report as report_mod, scheduler
from .cleaner import run_once
from .daemon import Watcher, setup_logging
from .quarantine import Quarantine
from .rules import active_rules, platform_rules


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cleaner-agent",
        description="AI Agent dọn rác máy tính — an toàn, khôi phục được, chạy liên tục.",
    )
    p.add_argument("--version", action="version", version=f"cleaner-agent {__version__}")
    p.add_argument("-c", "--config", type=Path, help="đường dẫn file cấu hình TOML")
    p.add_argument("-v", "--verbose", action="store_true", help="in thêm chi tiết")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="tạo file cấu hình mẫu")

    s = sub.add_parser("scan", help="quét và báo cáo, không đụng vào file nào")
    s.add_argument("--json", action="store_true", help="xuất JSON thay vì bảng")

    c = sub.add_parser("clean", help="dọn rác (mặc định vẫn là chạy thử)")
    c.add_argument("--apply", action="store_true", help="thực sự dọn, không chỉ báo cáo")
    c.add_argument("--json", action="store_true", help="xuất JSON thay vì bảng")

    w = sub.add_parser("watch", help="chạy liên tục theo chu kỳ")
    w.add_argument("--apply", action="store_true", help="thực sự dọn ở mỗi lượt")
    w.add_argument("--once", action="store_true", help="chỉ chạy một lượt rồi thoát")

    sub.add_parser("rules", help="liệt kê quy tắc đang áp dụng")
    sub.add_parser("status", help="tình trạng khu cách ly và lượt chạy gần nhất")

    r = sub.add_parser("restore", help="khôi phục một mục từ khu cách ly")
    r.add_argument("entry_id", help="id của mục (xem bằng lệnh `status`)")

    sub.add_parser("purge", help="xoá hẳn các mục đã quá hạn cách ly")

    i = sub.add_parser("install-service", help="cài chạy nền cùng hệ điều hành")
    i.add_argument("--apply", action="store_true", help="dịch vụ sẽ dọn thật, không chạy thử")
    i.add_argument("--write", action="store_true", help="ghi luôn file cấu hình dịch vụ")

    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    cfg = config_mod.load(args.config)

    if args.command == "init":
        path = config_mod.write_template(args.config)
        print(f"Cấu hình tại: {path}")
        print("Mở file này để bật/tắt quy tắc trước khi chạy `clean --apply`.")
        return 0

    if args.command == "rules":
        active = {r.id for r in active_rules(cfg)}
        print(f"{'TRẠNG THÁI':<12} {'ID':<24} MÔ TẢ")
        for rule in platform_rules():
            state = "đang bật" if rule.id in active else "tắt"
            print(f"{state:<12} {rule.id:<24} {rule.description}")
        return 0

    if args.command == "status":
        q = Quarantine(cfg.quarantine.dir, cfg.quarantine.retention_days)
        entries = q.entries()
        print(f"Khu cách ly : {cfg.quarantine.dir}")
        print(f"Đang giữ    : {len(entries)} mục · {report_mod.human_size(q.usage_bytes())}")
        print(f"Hạn giữ     : {cfg.quarantine.retention_days} ngày")
        for e in entries[-15:]:
            print(f"  {e.id}  {report_mod.human_size(e.size):>9}  {e.original_path}")
        last = cfg.state_dir / "last-report.json"
        if last.exists():
            data = json.loads(last.read_text(encoding="utf-8"))
            print(
                f"\nLượt gần nhất: dọn {data['cleaned']} mục "
                f"({report_mod.human_size(data['cleaned_bytes'])}), "
                f"{'chạy thử' if data['dry_run'] else 'đã thực thi'}"
            )
        return 0

    if args.command == "restore":
        q = Quarantine(cfg.quarantine.dir, cfg.quarantine.retention_days)
        try:
            restored = q.restore(args.entry_id)
        except (KeyError, FileNotFoundError) as exc:
            print(f"Lỗi: {exc}", file=sys.stderr)
            return 1
        print(f"Đã khôi phục về: {restored}")
        return 0

    if args.command == "purge":
        q = Quarantine(cfg.quarantine.dir, cfg.quarantine.retention_days)
        removed, freed = q.purge()
        print(f"Đã xoá hẳn {removed} mục · {report_mod.human_size(freed)}")
        return 0

    if args.command == "install-service":
        print(scheduler.install(args.apply, cfg.general.interval_minutes, args.write))
        return 0

    if args.command == "watch":
        setup_logging(cfg.state_dir, args.verbose)
        watcher = Watcher(cfg, apply=args.apply or None)
        watcher.install_signal_handlers()
        watcher.run(max_cycles=1 if args.once else None)
        return 0

    # scan / clean
    apply = getattr(args, "apply", False)
    rep = run_once(cfg, apply=apply if args.command == "clean" else False)
    report_mod.save(rep, cfg.state_dir)

    if getattr(args, "json", False):
        print(json.dumps(rep.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(report_mod.render(rep, verbose=args.verbose))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
