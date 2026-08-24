"""Giao diện dòng lệnh cho AI Agent viết kịch bản video sức khoẻ.

Ví dụ:
    python -m agent.cli list
    python -m agent.cli generate --trieu-chung mat-ngu --doi-tuong phu-nu-45-55
    python -m agent.cli check output/mat-ngu.md
    python -m agent.cli plan --so-ngay 30 --luu ke-hoach.md
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

from . import kb, planner
from .config import MODEL, OUTPUT_DIR


def _slug(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "D").lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:60]


# --------------------------------------------------------------------------- list
def cmd_list(args: argparse.Namespace) -> int:
    print("TRIỆU CHỨNG (--trieu-chung)")
    for s in kb.symptoms():
        print(f"  {s['id']:<20} {s['ten']}")
    print("\nĐỐI TƯỢNG (--doi-tuong)")
    for p in kb.personas():
        print(f"  {p['id']:<20} {p['ten']}")
    print("\nĐỊNH DẠNG (--dinh-dang)")
    for f in kb.formats():
        print(f"  {f['id']:<24} {f['ten']:<32} ~{f['thoi_luong_goi_y']}s")
    print("\nSẢN PHẨM (--san-pham)")
    for p in kb.products():
        print(f"  {p['id']:<20} {p['ten']} - {p['vai_tro']}")
    print("\nNỀN TẢNG (--nen-tang): tiktok, facebook, youtube, shopee_tiktokshop")

    thieu = [
        (p["ten"], k)
        for p in kb.products()
        for k, v in p.get("CAN_DIEN_THEM", {}).items()
        if not v
    ]
    if thieu:
        print(f"\nCẢNH BÁO: còn {len(thieu)} trường thông tin sản phẩm chưa điền "
              f"trong knowledge/products.json (hàm lượng, số công bố, giá...).")
        print("Agent sẽ viết [CẦN ĐIỀN] thay vì bịa số liệu.")
    return 0


# ------------------------------------------------------------------------ generate
def cmd_generate(args: argparse.Namespace) -> int:
    from . import generator  # nhập trễ để lệnh khác chạy được khi chưa cài anthropic

    print(f"Đang viết kịch bản bằng {MODEL} ...", file=sys.stderr)
    kq = generator.generate(
        symptom_key=args.trieu_chung,
        persona_key=args.doi_tuong,
        format_key=args.dinh_dang,
        platform=args.nen_tang,
        duration=args.thoi_luong,
        product_keys=args.san_pham or None,
        extra=args.them,
        max_fix=args.so_lan_sua,
    )

    if kq.tu_choi:
        print(f"Model từ chối tạo nội dung này: {kq.tu_choi}", file=sys.stderr)
        return 2

    dat = "ĐẠT" if kq.report.dat else "CHƯA ĐẠT"
    header = (
        f"<!-- Tạo lúc {datetime.now():%Y-%m-%d %H:%M} | model {kq.model} | "
        f"tự sửa {kq.so_lan_sua} lần | kiểm tra tuân thủ: {dat} -->\n\n"
    )
    noi_dung = header + kq.text

    out = Path(args.luu) if args.luu else OUTPUT_DIR / (
        f"{date.today():%Y%m%d}-{args.trieu_chung}-{args.doi_tuong}-{args.dinh_dang}.md"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(noi_dung, encoding="utf-8")

    print(kq.text)
    print(f"\n---\nĐã lưu: {out}", file=sys.stderr)
    print(f"Kiểm tra tuân thủ: {dat} (tự sửa {kq.so_lan_sua} lần)", file=sys.stderr)
    if not kq.report.dat:
        print(kq.report.to_text(), file=sys.stderr)
        print("Hãy sửa tay những chỗ trên trước khi quay.", file=sys.stderr)
        return 1
    if kq.usage:
        print(f"Token: {kq.usage}", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- check
def cmd_check(args: argparse.Namespace) -> int:
    from . import compliance

    loi = 0
    for path_str in args.duong_dan:
        path = Path(path_str)
        if not path.exists():
            print(f"Không tìm thấy: {path}", file=sys.stderr)
            loi += 1
            continue
        report = compliance.check(
            path.read_text(encoding="utf-8"), yeu_cau_khuyen_cao=not args.bo_qua_khuyen_cao
        )
        print(f"=== {path} ===")
        print(report.to_text())
        print()
        if not report.dat:
            loi += 1
    return 1 if loi else 0


# ---------------------------------------------------------------------------- plan
def cmd_plan(args: argparse.Namespace) -> int:
    bat_dau = date.fromisoformat(args.tu_ngay) if args.tu_ngay else None
    ke_hoach = planner.build(args.so_ngay, bat_dau)
    md = planner.to_markdown(ke_hoach)
    if args.luu:
        out = Path(args.luu)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"Đã lưu lịch nội dung: {out}", file=sys.stderr)
    print(md)
    return 0


# --------------------------------------------------------------------------- batch
def cmd_batch(args: argparse.Namespace) -> int:
    from . import generator

    ke_hoach = planner.build(args.so_ngay)
    thu_muc = Path(args.thu_muc)
    thu_muc.mkdir(parents=True, exist_ok=True)
    that_bai = 0

    for i, n in enumerate(ke_hoach, start=1):
        print(f"[{i}/{len(ke_hoach)}] {n.ngay} - {n.trieu_chung} / {n.dinh_dang}", file=sys.stderr)
        try:
            kq = generator.generate(
                symptom_key=n.trieu_chung,
                persona_key=n.doi_tuong,
                format_key=n.dinh_dang,
                platform=n.nen_tang,
                duration=n.thoi_luong,
            )
        except SystemExit as exc:
            print(f"  Dừng: {exc}", file=sys.stderr)
            return 1
        if kq.tu_choi or not kq.text:
            print("  Bỏ qua (model từ chối).", file=sys.stderr)
            that_bai += 1
            continue
        ten = f"{n.ngay}-{_slug(n.trieu_chung)}-{_slug(n.dinh_dang)}.md"
        (thu_muc / ten).write_text(kq.text, encoding="utf-8")
        print(f"  -> {ten} ({'ĐẠT' if kq.report.dat else 'CẦN SỬA TAY'})", file=sys.stderr)
        if not kq.report.dat:
            that_bai += 1
    print(f"Xong. {len(ke_hoach) - that_bai}/{len(ke_hoach)} kịch bản đạt tuân thủ.", file=sys.stderr)
    return 1 if that_bai else 0


# --------------------------------------------------------------------------- hooks
def cmd_hooks(args: argparse.Namespace) -> int:
    """Tra ngân hàng hook, lọc theo triệu chứng hoặc kiểu hook."""
    kho = kb.hooks()
    items = kho["mau_hook"]
    if args.trieu_chung:
        items = [h for h in items if h["trieu_chung"] in (args.trieu_chung, "chung")]
    if args.kieu:
        items = [h for h in items if h["kieu"] == args.kieu]
    if args.doi_tuong:
        items = [h for h in items if h.get("doi_tuong") in (args.doi_tuong, "chung")]
    items = items[: args.so_luong] if args.so_luong else items

    if not items:
        print("Không có hook nào khớp bộ lọc.", file=sys.stderr)
        print("Các kiểu hook có sẵn: " + ", ".join(sorted({h["kieu"] for h in kho["mau_hook"]})))
        return 1

    print("NGUYÊN TẮC VIẾT HOOK")
    for n in kho["nguyen_tac"]:
        print(f"  - {n}")
    print(f"\n{len(items)} HOOK")
    for i, h in enumerate(items, start=1):
        print(f"\n{i:>3}. {h['cau']}")
        meta = f"     [{h['kieu']}] {h['trieu_chung']}"
        if h.get("doi_tuong") and h["doi_tuong"] != "chung":
            meta += f" / {h['doi_tuong']}"
        print(meta)
        if h.get("ghi_chu"):
            print(f"     {h['ghi_chu']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agent.cli",
        description="AI Agent viết kịch bản video về đau đầu, chóng mặt, mất ngủ, tê bì chân tay.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="lenh", required=True)

    sub.add_parser("list", help="Xem các lựa chọn có sẵn").set_defaults(func=cmd_list)

    g = sub.add_parser("generate", help="Viết một kịch bản mới")
    g.add_argument("--trieu-chung", required=True, help="dau-dau | chong-mat | mat-ngu | te-bi-chan-tay")
    g.add_argument("--doi-tuong", default="phu-nu-45-55")
    g.add_argument("--dinh-dang", default="hook-noi-dau-giai-phap")
    g.add_argument("--nen-tang", default="tiktok")
    g.add_argument("--thoi-luong", type=int, default=None, help="Số giây, để trống thì lấy mặc định của định dạng")
    g.add_argument("--san-pham", nargs="*", default=None, help="Chỉ định sản phẩm, mặc định theo triệu chứng")
    g.add_argument("--them", default=None, help="Yêu cầu thêm, ví dụ: quay ngoài trời, có phụ đề tiếng Anh")
    g.add_argument("--so-lan-sua", type=int, default=2, help="Số lần cho model tự sửa lỗi tuân thủ")
    g.add_argument("--luu", default=None, help="Đường dẫn file lưu kết quả")
    g.set_defaults(func=cmd_generate)

    c = sub.add_parser("check", help="Soát tuân thủ một hoặc nhiều file (không cần API)")
    c.add_argument("duong_dan", nargs="+")
    c.add_argument("--bo-qua-khuyen-cao", action="store_true", help="Không bắt buộc có câu khuyến cáo")
    c.set_defaults(func=cmd_check)

    pl = sub.add_parser("plan", help="Lên lịch nội dung (không cần API)")
    pl.add_argument("--so-ngay", type=int, default=30)
    pl.add_argument("--tu-ngay", default=None, help="YYYY-MM-DD")
    pl.add_argument("--luu", default=None)
    pl.set_defaults(func=cmd_plan)

    h = sub.add_parser("hooks", help="Tra ngân hàng hook (không cần API)")
    h.add_argument("--trieu-chung", default=None, help="Lọc theo triệu chứng")
    h.add_argument("--kieu", default=None, help="cau-hoi | phan-de | con-so | ke-chuyen | dong-cam ...")
    h.add_argument("--doi-tuong", default=None, help="Lọc theo chân dung khách hàng")
    h.add_argument("--so-luong", type=int, default=None, help="Chỉ lấy N hook đầu")
    h.set_defaults(func=cmd_hooks)

    b = sub.add_parser("batch", help="Viết hàng loạt kịch bản theo lịch nội dung")
    b.add_argument("--so-ngay", type=int, default=7)
    b.add_argument("--thu-muc", default=str(OUTPUT_DIR / "batch"))
    b.set_defaults(func=cmd_batch)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
