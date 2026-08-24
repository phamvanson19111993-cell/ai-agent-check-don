"""CLI: lấy SĐT các hội thoại Pancake chưa gắn nhãn CHỐT ĐƠN."""

import argparse
import datetime
import sys
import time

from . import exporter, extract, importer, sheets, tagging
from .client import PancakeClient, PancakeError
from .config import Config

# Page mặc định: Bùi Phúc Thịnh - Tim Mạch Não Bộ
DEFAULT_PAGE_ID = "1121021804424838"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pancake-export",
        description="Lấy số điện thoại của hội thoại Pancake CHƯA có nhãn chốt đơn "
                    "và lưu ra CSV / Google Sheet trên Drive.",
    )
    parser.add_argument("--days", type=int, default=3,
                        help="Quét N ngày gần nhất (mặc định 3).")
    parser.add_argument("--since", help="Mốc bắt đầu dd/mm/yyyy (ưu tiên hơn --days).")
    parser.add_argument("--until", help="Mốc kết thúc dd/mm/yyyy.")
    parser.add_argument("--page-id", default=None,
                        help="ID page Pancake (mặc định page Phúc Thịnh: %s)." % DEFAULT_PAGE_ID)
    parser.add_argument("--token", default=None, help="API key Pancake (ưu tiên hơn .env).")
    parser.add_argument("--api-base", default=None, help="Đổi base URL API nếu Pancake thay đổi.")
    parser.add_argument("--closed-tag", action="append", default=None,
                        help="Tên nhãn coi là ĐÃ chốt đơn (lặp lại được). Mặc định: CHỐT ĐƠN.")
    parser.add_argument("--yellow", action="store_true",
                        help="Coi mọi nhãn màu vàng là nhãn chốt đơn.")
    parser.add_argument("--out", default="data/sdt_chua_chot.csv", help="File CSV kết quả.")
    parser.add_argument("--json", dest="json_out", default=None, help="Xuất thêm file JSON.")
    parser.add_argument("--sheet-id", default=None, help="ID Google Sheet để ghi lên Drive.")
    parser.add_argument("--drive", action="store_true",
                        help="Đẩy kết quả lên Google Sheet sau khi chạy.")
    parser.add_argument("--deep", action="store_true",
                        help="Mở thêm tin nhắn để dò SĐT khi hội thoại chưa có số (chậm hơn).")
    parser.add_argument("--list-tags", action="store_true",
                        help="Chỉ in ra danh sách nhãn của page rồi thoát.")
    parser.add_argument("--watch", type=int, metavar="PHUT", default=0,
                        help="Chạy lặp mỗi N phút để tự cập nhật liên tục.")
    parser.add_argument("--max-pages", type=int, default=200, help="Giới hạn số trang API.")
    parser.add_argument("--from-file", dest="from_file", default=None,
                        help="Bỏ qua API, đọc file Pancake xuất ra (CSV/TSV/XLSX).")
    parser.add_argument("--debug", action="store_true", help="In thông tin gỡ lỗi.")
    return parser


def parse_date(text):
    for pattern in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%y"):
        try:
            return datetime.datetime.strptime(text, pattern)
        except ValueError:
            continue
    raise SystemExit("Không đọc được ngày '%s'. Dùng dạng dd/mm/yyyy." % text)


def time_window(args):
    until = parse_date(args.until) if args.until else None
    if args.since:
        since = parse_date(args.since)
    else:
        base = until or datetime.datetime.now()
        since = base - datetime.timedelta(days=max(args.days, 0))
    return int(since.timestamp()), int(until.timestamp()) if until else None


def save(config, args, rows, stats):
    """Ghi CSV (gộp dữ liệu cũ) và đẩy lên Google Sheet nếu được yêu cầu."""
    existing = exporter.read_existing(args.out)
    merged, new_rows = exporter.merge(existing, rows)
    exporter.write_csv(args.out, merged)
    if args.json_out:
        exporter.write_json(args.json_out, merged)

    print("→ Quét: %(tong)s | đã chốt: %(da_chot)s | không có SĐT: %(khong_co_sdt)s "
          "| chưa chốt có SĐT: %(chua_chot)s" % stats)
    print("→ File: %s (tổng %s số, mới thêm %s)" % (args.out, len(merged), len(new_rows)))

    if args.drive:
        try:
            added = sheets.append_rows(
                config.sheet_id, rows, config.service_account_file, config.sheet_tab
            )
            print("→ Google Sheet: đã thêm %s dòng mới\n  https://docs.google.com/spreadsheets/d/%s/edit"
                  % (added, config.sheet_id))
        except sheets.SheetsUnavailable as error:
            print("! Chưa đẩy lên Drive được: %s" % error)

    return len(new_rows)


def run_from_file(config, args):
    print("→ Đọc file %s (không cần API)" % args.from_file)
    rows, stats = importer.load(
        args.from_file, config.page_id, config.closed_tags, match_yellow=args.yellow
    )
    return save(config, args, rows, stats)


def run_once(config, args):
    client = PancakeClient(
        config.access_token, config.page_id, config.api_base, debug=args.debug
    )

    tag_lookup = {}
    try:
        tags, tag_lookup = client.get_tags()
    except PancakeError as error:
        tags = []
        print("! Không lấy được danh sách nhãn (%s). Vẫn tiếp tục theo tên nhãn trong hội thoại."
              % error)

    if args.list_tags:
        if not tags:
            print("Không có nhãn nào đọc được.")
            return 0
        print("Nhãn của page %s:" % config.page_id)
        for tag in tags:
            print("  - %-28s %s" % (tagging.tag_name(tag), tagging.tag_color(tag)))
        return 0

    since, until = time_window(args)
    print("→ Quét page %s từ %s%s"
          % (config.page_id,
             datetime.datetime.fromtimestamp(since).strftime("%d/%m/%Y %H:%M"),
             "" if not until else " đến " + datetime.datetime.fromtimestamp(until).strftime("%d/%m/%Y %H:%M")))
    print("→ Nhãn coi là đã chốt: %s%s"
          % (", ".join(config.closed_tags), " (+ mọi nhãn vàng)" if args.yellow else ""))

    fetch_messages = None
    if args.deep:
        def fetch_messages(conversation):
            return client.get_messages(
                conversation.get("id") or conversation.get("conversation_id"),
                conversation.get("customer_id"),
            )

    conversations = client.iter_conversations(since=since, until=until, max_pages=args.max_pages)
    rows, stats = extract.collect(
        conversations,
        config.page_id,
        config.closed_tags,
        tag_lookup=tag_lookup,
        match_yellow=args.yellow,
        fetch_messages=fetch_messages,
    )

    return save(config, args, rows, stats)


def main(argv=None):
    args = build_parser().parse_args(argv)
    config = Config(args)
    if not config.page_id:
        config.page_id = DEFAULT_PAGE_ID

    if args.from_file:
        return 0 if run_from_file(config, args) >= 0 else 1

    config.require_pancake()

    if not args.watch:
        try:
            run_once(config, args)
        except PancakeError as error:
            print("Lỗi: %s" % error, file=sys.stderr)
            return 1
        return 0

    print("Chạy tự động mỗi %s phút. Nhấn Ctrl+C để dừng." % args.watch)
    while True:
        stamp = datetime.datetime.now().strftime("%d/%m %H:%M")
        print("\n===== %s =====" % stamp)
        try:
            run_once(config, args)
        except PancakeError as error:
            print("! Lỗi lần chạy này: %s" % error, file=sys.stderr)
        except KeyboardInterrupt:
            print("\nĐã dừng.")
            return 0
        try:
            time.sleep(args.watch * 60)
        except KeyboardInterrupt:
            print("\nĐã dừng.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
