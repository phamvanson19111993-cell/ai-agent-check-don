"""Giao diện dòng lệnh cho ai-agent-check-don.

Ví dụ:
  python -m src.cli check                 # đếm & liệt kê cơ hội đang hoạt động
  python -m src.cli list --limit 20
  python -m src.cli import data/don.xlsx  # import/cập nhật cơ hội từ file
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .config import load_config
from .crm import CrmService
from .odoo_client import OdooClient, OdooError
from .orders import REF_COLUMN, REF_FIELD, load_orders, order_to_opportunity


def _build_service() -> CrmService:
    config = load_config()
    client = OdooClient(config)
    client.authenticate()
    return CrmService(client)


def cmd_check(_args: argparse.Namespace) -> int:
    svc = _build_service()
    total = svc.count_active_opportunities()
    print(f"Tổng số cơ hội đang hoạt động: {total}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    svc = _build_service()
    opps = svc.list_active_opportunities(limit=args.limit)
    if not opps:
        print("Không có cơ hội nào.")
        return 0
    for o in opps:
        stage = o.get("stage_id") or ["", ""]
        stage_name = stage[1] if isinstance(stage, list) and len(stage) > 1 else ""
        print(
            f"[{o.get('id')}] {o.get('name')} | giai đoạn: {stage_name} "
            f"| doanh thu: {o.get('expected_revenue')}"
        )
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    svc = _build_service()
    orders = load_orders(args.file)
    print(f"Đọc được {len(orders)} dòng từ {args.file}")
    created = updated = skipped = 0
    for order in orders:
        ref = order.get(REF_COLUMN)
        if not ref:
            skipped += 1
            continue
        values = order_to_opportunity(order)
        values.pop(REF_FIELD, None)  # ref đã truyền riêng
        if args.dry_run:
            print(f"[DRY-RUN] upsert {REF_FIELD}={ref} <- {values}")
            continue
        result = svc.upsert_by_ref(str(ref), values, ref_field=REF_FIELD)
        if result["action"] == "created":
            created += 1
        else:
            updated += 1
        print(f"{result['action']} id={result['id']} ({REF_FIELD}={ref})")
    if not args.dry_run:
        print(f"Xong: tạo mới {created}, cập nhật {updated}, bỏ qua {skipped}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-agent-check-don",
        description="Kiểm tra đơn & cập nhật Cơ hội vào Odoo CRM (ef.foxia.vn)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="Đếm số cơ hội đang hoạt động")

    p_list = sub.add_parser("list", help="Liệt kê cơ hội đang hoạt động")
    p_list.add_argument("--limit", type=int, default=20)

    p_import = sub.add_parser("import", help="Import/cập nhật cơ hội từ file CSV/Excel")
    p_import.add_argument("file", help="Đường dẫn file .csv/.xlsx")
    p_import.add_argument(
        "--dry-run", action="store_true", help="Chỉ in ra, không ghi lên Odoo"
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = {
        "check": cmd_check,
        "list": cmd_list,
        "import": cmd_import,
    }[args.command]
    try:
        return handler(args)
    except OdooError as exc:
        print(f"Lỗi Odoo: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Lỗi cấu hình/dữ liệu: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
