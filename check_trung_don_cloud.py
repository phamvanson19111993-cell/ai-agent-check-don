#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUET TRUNG DON TREN MAY CHU GITHUB — khong can may Mac, khong can Tampermonkey

Chuong trinh CHI DOC. Tai Sheet don hang ve, do tim so dien thoai bi
trung, roi gui bao cao len Telegram.

Vi sao can cai nay:
  Duong cu phai co may Mac bat, bot chay, Tampermonkey song, nut xanh
  bat — dut mot mat xich la im. Duong nay chay tren may chu GitHub, may
  anh tat hay mat dien deu khong anh huong.

CAN HAI MA BI MAT (dat trong Settings > Secrets and variables > Actions):
  TG_TOKEN   ma bot Telegram, lay tu @BotFather
  TG_CHAT    ma cuoc tro chuyen/nhom, lay tu @userinfobot hoac go /id

Sheet phai chia se: Bat ky ai co link -> Nguoi xem.

Chay lan dau: 12/09/2026 — sau khi da dat TG_TOKEN va TG_CHAT.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    sys.exit("Thieu thu vien. Chay: pip install requests openpyxl")

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit("Thieu thu vien. Chay: pip install requests openpyxl")

from phone_utils import extract_phones, normalize

SHEET_ID = os.environ.get(
    "SHEET_ID", "1CaCQZvLhAafJ42vuinOlwGhlGmPZCCSzPyzxmlIFNyE")
TG_TOKEN = os.environ.get("TG_TOKEN", "")
TG_CHAT = os.environ.get("TG_CHAT", "")

VN = timezone(timedelta(hours=7))
TAI_VE = "https://docs.google.com/spreadsheets/d/%s/export?format=xlsx" % SHEET_ID
FILE_TAM = "/tmp/don_hang.xlsx"

# Nho cac so DA BAO roi, de moi gio chay lai khong bao lap
FILE_TRANG_THAI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "da_bao.json")

# Toi da moi tin Telegram (that ra 4096, tru hao cho an toan)
GIOI_HAN = 3800


def tai_sheet():
    """Tai ca workbook (moi tab) ve file tam."""
    r = requests.get(TAI_VE, timeout=90)
    if r.status_code != 200:
        raise SystemExit(
            "Khong tai duoc Sheet (HTTP %d).\n"
            "Kiem tra: Sheet da chia se 'Bat ky ai co link -> Nguoi xem' chua?"
            % r.status_code)
    with open(FILE_TAM, "wb") as f:
        f.write(r.content)
    return FILE_TAM


def quet(duong_dan):
    """Tra ve {so: [ {tab, dong, ngu_canh}, ... ]} va tong so khac nhau."""
    wb = load_workbook(duong_dan, read_only=True, data_only=True)
    danh_ba = {}

    for ten_tab in wb.sheetnames:
        ws = wb[ten_tab]
        for chi_so, hang in enumerate(ws.iter_rows(values_only=True), start=1):
            o_list = [str(o).strip() for o in hang if o is not None and str(o).strip()]
            if not o_list:
                continue

            so_trong_dong, o_thuan_so = [], set()
            for o in o_list:
                k = normalize(o)
                if k:
                    o_thuan_so.add(o)
                    if k not in so_trong_dong:
                        so_trong_dong.append(k)
            for o in o_list:
                if o in o_thuan_so:
                    continue
                for k in extract_phones(o):
                    if k not in so_trong_dong:
                        so_trong_dong.append(k)
            if not so_trong_dong:
                continue

            ngu_canh = " · ".join(o for o in o_list if o not in o_thuan_so)[:70]
            for k in so_trong_dong:
                danh_ba.setdefault(k, []).append(
                    {"tab": ten_tab, "dong": chi_so, "nc": ngu_canh})

    wb.close()
    return danh_ba


def doc_da_bao():
    """Danh sach so da bao lan truoc. Mat file thi coi nhu chua bao gi.

    Dat BAO_TAT_CA=1 de bo qua tri nho va bao lai toan bo — dung khi
    muon xem lai day du danh sach, khong phai cho ca moi.
    """
    if os.environ.get("BAO_TAT_CA") == "1":
        return set()
    try:
        with open(FILE_TRANG_THAI, encoding="utf-8") as f:
            return set(json.load(f).get("da_bao", []))
    except Exception:
        return set()


def ghi_da_bao(tat_ca):
    with open(FILE_TRANG_THAI, "w", encoding="utf-8") as f:
        json.dump({"da_bao": sorted(tat_ca),
                   "cap_nhat": datetime.now(VN).isoformat()},
                  f, ensure_ascii=False, indent=1)


def de_doc(khoa):
    s = "0" + khoa
    return "%s %s %s" % (s[:4], s[4:7], s[7:])


def dung_bao_cao(danh_ba, da_bao):
    """Chi bao cac so TRUNG MOI (chua bao lan nao). Tra ve list manh tin."""
    trung = {k: v for k, v in danh_ba.items() if len(v) > 1}
    moi = {k: v for k, v in trung.items() if k not in da_bao}
    gio = datetime.now(VN).strftime("%H:%M %d/%m/%Y")

    if not moi:
        return []  # khong co gi moi -> im lang, khong lam phien

    ba_lan = sum(1 for v in moi.values() if len(v) > 2)
    dau = ["🔔 <b>TRÙNG ĐƠN MỚI — DiLi Supplement</b>",
           "🕐 %s" % gio,
           "",
           "Đã quét <b>%d</b> số trong Sheet" % len(danh_ba),
           "<b>%d SỐ TRÙNG MỚI</b> (chưa báo lần nào)" % len(moi)]
    if ba_lan:
        dau.append("Trong đó <b>%d số trùng từ 3 lần</b>" % ba_lan)
    dau.append("")

    sap = sorted(moi.items(), key=lambda kv: len(kv[1]), reverse=True)

    manh, hien_tai = [], "\n".join(dau)
    for thu_tu, (khoa, cho) in enumerate(sap, 1):
        khoi = ["<b>%d. %s</b> — trùng %d lần" % (thu_tu, de_doc(khoa), len(cho))]
        for x in cho:
            khoi.append("   • %s · dòng %d · %s" % (x["tab"], x["dong"], x["nc"]))
        khoi_chu = "\n".join(khoi)

        if len(hien_tai) + len(khoi_chu) + 2 > GIOI_HAN:
            manh.append(hien_tai)
            hien_tai = khoi_chu
        else:
            hien_tai = hien_tai + "\n" + khoi_chu

    manh.append(hien_tai)
    return manh


def gui_telegram(chu):
    r = requests.post(
        "https://api.telegram.org/bot%s/sendMessage" % TG_TOKEN,
        data={"chat_id": TG_CHAT, "text": chu,
              "parse_mode": "HTML", "disable_web_page_preview": "true"},
        timeout=30)
    kq = r.json()
    if not kq.get("ok"):
        raise SystemExit("Telegram tu choi: %s" % kq.get("description", "khong ro"))


def main():
    thieu = [t for t, g in (("TG_TOKEN", TG_TOKEN), ("TG_CHAT", TG_CHAT)) if not g]
    if thieu:
        print("Chua dien ma bi mat: %s" % " ".join(thieu))
        print("Vao: Settings > Secrets and variables > Actions > New repository secret")
        sys.exit(1)

    print("Dang tai Sheet...")
    duong_dan = tai_sheet()

    print("Dang quet...")
    danh_ba = quet(duong_dan)
    trung = {k for k, v in danh_ba.items() if len(v) > 1}
    da_bao = doc_da_bao()
    moi = trung - da_bao
    print("Tong so: %d | Trung: %d | Da bao truoc: %d | MOI: %d"
          % (len(danh_ba), len(trung), len(da_bao), len(moi)))

    manh = dung_bao_cao(danh_ba, da_bao)
    if not manh:
        print("Khong co ca trung moi — khong gui gi. XONG.")
        return

    for i, m in enumerate(manh, 1):
        gui_telegram(m)
        print("Da gui manh %d/%d (%d ky tu)" % (i, len(manh), len(m)))

    ghi_da_bao(trung | da_bao)
    print("Da ghi trang thai: %d so." % len(trung | da_bao))
    print("XONG.")


if __name__ == "__main__":
    main()
