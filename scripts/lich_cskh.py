#!/usr/bin/env python3
"""Lịch chăm sóc khách hàng Zalo theo chu kỳ 10 ngày.

Cách dùng:
    python3 scripts/lich_cskh.py data/danh_sach_khach_mau.csv
    python3 scripts/lich_cskh.py data/danh_sach_khach_mau.csv --ngay 2026-09-01
    python3 scripts/lich_cskh.py data/danh_sach_khach_mau.csv --tat-ca

In ra danh sách khách đến hạn nhắn tin hôm nay, kèm gợi ý mẫu tin đã điền sẵn thông tin.
"""
import argparse
import csv
import json
import sys
from datetime import date, datetime
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
FILE_MAU = GOC / "data" / "mau_tin_nhan.json"

# Chu kỳ mặc định theo phân khúc (ngày)
CHU_KY_PHAN_KHUC = {
    "moi": 10,
    "than_thiet": 10,
    "vip": 7,
    "ngu_dong": 20,
    "im_lang": 30,
}

# Nhóm chủ đề xoay vòng cho khách thường
VONG_CHU_DE = ["HOI_THAM", "SAU_MUA", "MEO_HUU_ICH", "HOI_THAM", "HANG_MOI", "TRI_AN"]


def doc_ngay(chuoi):
    chuoi = (chuoi or "").strip()
    if not chuoi:
        return None
    try:
        return datetime.strptime(chuoi, "%Y-%m-%d").date()
    except ValueError:
        return None


def chu_ky_cua_khach(khach, quy_tac):
    """Chu kỳ cơ bản theo phân khúc; chỉ nới rộng khi khách im lặng nhiều lượt."""
    co_ban = CHU_KY_PHAN_KHUC.get(khach.get("phan_khuc", ""), 10)
    try:
        khong_rep = int(khach.get("so_lan_khong_rep") or 0)
    except ValueError:
        khong_rep = 0
    if khong_rep < 3:
        return co_ban
    gian = quy_tac.get(str(khong_rep))
    if gian is None:
        gian = max(int(v) for v in quy_tac.values())
    return max(co_ban, int(gian))


def ten_goi(ho_ten):
    """Người Việt gọi nhau bằng tên: 'Nguyễn Thị Lan' -> 'Lan'."""
    phan = (ho_ten or "").split()
    return phan[-1] if phan else ho_ten


def dien_bien(mau, khach):
    thay = {
        "{ten}": ten_goi(khach.get("ten", "")),
        "{xung_ho}": khach.get("xung_ho", "anh/chị"),
        "{san_pham}": khach.get("san_pham", "sản phẩm"),
        "{san_pham_moi}": khach.get("san_pham", "sản phẩm mới"),
        "{ngay_mua}": khach.get("ngay_mua_cuoi", ""),
        "{ten_nv}": khach.get("ten_nv") or "em",
        "{shop}": khach.get("shop") or "shop",
    }
    for k, v in thay.items():
        mau = mau.replace(k, v)
    return mau[:1].upper() + mau[1:] if mau else mau


def chon_tin(khach, du_lieu, hom_nay, luot):
    """Ưu tiên: sinh nhật > dịp lễ > chủ đề xoay vòng."""
    sn = doc_ngay(khach.get("sinh_nhat"))
    if sn and (sn.month, sn.day) == (hom_nay.month, hom_nay.day):
        return "SINH NHẬT 🎂", du_lieu["sinh_nhat"]

    khoa_ngay = hom_nay.strftime("%d-%m")
    for dip in du_lieu["dip_le"]:
        if dip["ngay"] != khoa_ngay or dip.get("thu_cong"):
            continue
        chi_cho = dip.get("chi_xung_ho")
        if chi_cho and khach.get("xung_ho") not in chi_cho:
            continue  # ví dụ 8/3, 20/10 chỉ gửi cho khách nữ
        return f"DỊP LỄ – {dip['ten']}", dip["mau"]

    if khach.get("phan_khuc") == "ngu_dong":
        ma = "NGU_DONG"
    elif khach.get("phan_khuc") == "im_lang":
        ma = "HOI_THAM"
    else:
        ma = VONG_CHU_DE[luot % len(VONG_CHU_DE)]

    nhom = next(n for n in du_lieu["nhom_chu_de"] if n["ma"] == ma)
    mau = nhom["mau"][luot % len(nhom["mau"])]
    return nhom["ten"].upper(), mau


def main():
    p = argparse.ArgumentParser(description="Lịch CSKH Zalo chu kỳ 10 ngày")
    p.add_argument("csv_khach", help="File CSV danh sách khách")
    p.add_argument("--ngay", help="Ngày cần tính (YYYY-MM-DD), mặc định hôm nay")
    p.add_argument("--tat-ca", action="store_true", help="In cả khách chưa đến hạn")
    args = p.parse_args()

    hom_nay = doc_ngay(args.ngay) or date.today()
    du_lieu = json.loads(FILE_MAU.read_text(encoding="utf-8"))
    quy_tac = du_lieu["quy_tac_gian_tan_suat"]

    with open(args.csv_khach, encoding="utf-8") as f:
        khach_hang = list(csv.DictReader(f))

    print(f"\n📅 LỊCH CHĂM SÓC KHÁCH HÀNG ZALO — ngày {hom_nay:%d/%m/%Y}")
    print(f"⏰ Giờ gửi khuyến nghị: {' · '.join(du_lieu['gio_gui_khuyen_nghi'])}")
    print("=" * 72)

    den_han = 0
    for i, khach in enumerate(khach_hang):
        lien_he_cuoi = doc_ngay(khach.get("ngay_lien_he_cuoi"))
        chu_ky = chu_ky_cua_khach(khach, quy_tac)
        if lien_he_cuoi is None:
            so_ngay, phai_nhan = chu_ky, True
        else:
            so_ngay = (hom_nay - lien_he_cuoi).days
            phai_nhan = so_ngay >= chu_ky

        sn = doc_ngay(khach.get("sinh_nhat"))
        la_sinh_nhat = bool(sn and (sn.month, sn.day) == (hom_nay.month, hom_nay.day))
        phai_nhan = phai_nhan or la_sinh_nhat

        if not phai_nhan and not args.tat_ca:
            continue
        den_han += 1 if phai_nhan else 0

        chu_de, mau = chon_tin(khach, du_lieu, hom_nay, so_ngay // max(chu_ky, 1) + i)
        trang_thai = "🔔 ĐẾN HẠN" if phai_nhan else "⏳ chưa tới hạn"

        print(f"\n{trang_thai} — {khach['ten']} ({khach.get('so_dien_thoai','')})")
        print(f"  Phân khúc: {khach.get('phan_khuc','')} | chu kỳ {chu_ky} ngày | "
              f"lần cuối cách đây {so_ngay} ngày | chưa rep {khach.get('so_lan_khong_rep','0')} lượt")
        if khach.get("ghi_chu"):
            print(f"  Ghi chú: {khach['ghi_chu']}")
        print(f"  Chủ đề: {chu_de}")
        print(f"  ✉️  {dien_bien(mau, khach)}")

    print("\n" + "=" * 72)
    print(f"Tổng: {den_han} khách cần nhắn hôm nay / {len(khach_hang)} khách.")
    print("Nhớ: sửa ít nhất 1 chi tiết riêng cho mỗi khách trước khi gửi.\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
