# -*- coding: utf-8 -*-
"""Tự kiểm tra logic bot KHÔNG cần token Telegram.

Chạy:  python selftest.py
- Kiểm tra regex tách SĐT (không nhận nhầm số tiền).
- Nạp Sheet từ CSV_URL/CSV_URLS trong .env (nếu có), nếu không thì dùng dữ liệu mẫu.
- In thử báo cáo cho /check 0976486366 và một số không tồn tại.
"""
import os
import sys

from phone_utils import extract_phones, normalize
from report import build_report
from sheet_store import store
import config

FAILED = False


def check(name: str, cond: bool, extra: str = "") -> None:
    global FAILED
    mark = "✅" if cond else "❌"
    print(f"{mark} {name}" + (f" — {extra}" if extra else ""))
    if not cond:
        FAILED = True


print("=== 1. Kiểm tra tách & chuẩn hoá SĐT ===")
check("0378415411 → 378415411", normalize("0378415411") == "378415411")
check("+84976486366 → 976486366", normalize("+84976486366") == "976486366")
check("976486366 (mất số 0 đầu như trong Sheet) → hợp lệ", normalize("976486366") == "976486366")
check("Số tiền 3.290.000 KHÔNG bị nhận nhầm", extract_phones("giá 3.290.000 đ") == [])
check("Số tiền 1.234.567.890 KHÔNG bị nhận nhầm", extract_phones("tổng 1.234.567.890 đ") == [])
check(
    "Bắt số trong câu chat có dấu chấm ngăn cách",
    extract_phones("chị Loan 0976.486.366 chốt đơn 3.290.000đ nhé") == ["976486366"],
)
check(
    "Bắt nhiều số, bỏ trùng",
    extract_phones("0378415411 và +84 378 415 411 và 0976486366")
    == ["378415411", "976486366"],
)
check("Tin nhắn không có số → danh sách rỗng", extract_phones("chốt đơn cho chị nhé") == [])

print("\n=== 2. Nạp Sheet ===")
if not config.CSV_SOURCES:
    # Không có .env → dùng dữ liệu mẫu để minh hoạ
    sample = os.path.join(os.path.dirname(__file__), "sample_data", "don_hang_mau.csv")
    config.CSV_SOURCES = [("Đơn hàng mẫu", sample)]
    print("(Chưa cấu hình CSV_URL — dùng dữ liệu mẫu sample_data/don_hang_mau.csv)")

try:
    rows, tabs = store.load()
    print(f"✅ Nạp thành công: {rows} dòng có SĐT / {tabs} tab")
    if store.last_error:
        print(f"⚠️ Một phần tab lỗi: {store.last_error}")
except Exception as e:  # noqa: BLE001
    check("Nạp Sheet", False, str(e))
    print("→ Kiểm tra Sheet đã chia sẻ 'Bất kỳ ai có link → Người xem' chưa.")
    sys.exit(1)

print("\n=== 3. Thử /check 0976486366 (kỳ vọng TRÙNG - Tran Loan) ===")
key = normalize("0976486366")
matches = store.lookup(key)
print(build_report(key, matches))
check("\nKết quả là TRÙNG", len(matches) > 0, f"{len(matches)} dòng")
if matches:
    check("Có khách Tran Loan", any("tran loan" in m["customer"].lower() for m in matches),
          f"khách: {[m['customer'] for m in matches]}")

print("\n=== 4. Thử một số KHÔNG có trong Sheet ===")
key2 = normalize("0378415411")
matches2 = store.lookup(key2)
print(build_report(key2, matches2))
check("\nKết quả là KHÔNG TRÙNG", len(matches2) == 0)

print("\n" + ("🛑 CÓ LỖI — xem các mục ❌ ở trên" if FAILED else "🎉 TẤT CẢ ĐỀU ĐẠT"))
sys.exit(1 if FAILED else 0)
