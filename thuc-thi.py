#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THI HÀNH LỆNH ĐIỀU CHỈNH QUẢNG CÁO

Phòng 7 không nối được ra Facebook, nên không tự bấm được. Cách làm thay
thế: Phòng 7 viết lệnh vào file lenh.json, anh chạy chương trình này trên
máy anh, chương trình đọc lệnh rồi thi hành.

AN TOÀN — ba lớp, không bỏ lớp nào:
  1. Chạy thường là CHẠY THỬ. Chỉ in ra sẽ làm gì, KHÔNG đụng tài khoản.
  2. Muốn làm thật phải thêm chữ  --lam  vào câu lệnh.
  3. Kể cả khi làm thật, mỗi việc vẫn hỏi lại, anh gõ CO mới chạy.

CÁCH CHẠY
  python3 thuc-thi.py            ← xem trước, không đụng gì
  python3 thuc-thi.py --lam      ← làm thật, vẫn hỏi từng việc

Cần mã truy cập có quyền  ads_management  (mạnh hơn ads_read của
bao-cao-ads.py, vì lần này là sửa chứ không chỉ đọc).
"""

import io
import json
import os
import sys
from getpass import getpass

try:
    import requests
except ImportError:
    sys.exit("Thiếu thư viện. Chạy trước:  pip install requests")

API   = "https://graph.facebook.com/v21.0"
TOKEN = os.environ.get("FB_TOKEN", "")
LAM_THAT = "--lam" in sys.argv
KHONG_HOI = "--khong-hoi" in sys.argv and LAM_THAT


def tien(x):
    try:
        return "{:,}".format(int(round(float(x)))).replace(",", ".") + "đ"
    except (TypeError, ValueError):
        return "—"


def _mang(ham, duong, tham):
    t = dict(tham or {})
    t["access_token"] = TOKEN
    try:
        r = ham("%s/%s" % (API, duong), params=t if ham is requests.get else None,
                data=None if ham is requests.get else t, timeout=60)
    except requests.exceptions.SSLError:
        sys.exit("Không thiết lập được kết nối an toàn tới Facebook. "
                 "Thử đổi sang mạng 4G điện thoại.")
    except requests.exceptions.ConnectionError:
        sys.exit("Không nối được mạng ra Facebook.")
    except requests.exceptions.Timeout:
        sys.exit("Facebook trả lời quá chậm. Chạy lại sau vài phút.")
    try:
        return r.json()
    except ValueError:
        return {"error": {"message": "Facebook trả về nội dung lạ (mã %d)" % r.status_code}}


def doc(duong, tham=None):
    kq = _mang(requests.get, duong, tham)
    if "error" in kq:
        print("  ⚠ Facebook báo: %s" % (kq["error"].get("error_user_msg")
                                        or kq["error"].get("message")))
        return None
    return kq


def sua(duong, tham):
    kq = _mang(requests.post, duong, tham)
    if "error" in kq:
        print("  ✗ KHÔNG THÀNH CÔNG: %s" % (kq["error"].get("error_user_msg")
                                            or kq["error"].get("message")))
        return False
    print("  ✓ Xong")
    return True


def hoi_lam(mo_ta):
    """Hỏi lại trước mỗi việc. Chạy thử thì chỉ in ra."""
    if not LAM_THAT:
        print("  → CHẠY THỬ, không đụng gì. Muốn làm thật thì thêm --lam")
        return False
    # Tren may chu GitHub khong co ai go phim. --khong-hoi bo buoc go CO,
    # nhung VAN phai co --lam, va quy trinh con bat go dung chu xac nhan
    # truoc khi truyen co nay vao.
    if KHONG_HOI:
        print("  → --khong-hoi: LÀM LUÔN, không hỏi lại.")
        return True
    tra = input("  Làm việc này? gõ CO rồi Enter (bỏ qua thì Enter luôn): ").strip()
    if tra.upper() in ("CO", "CÓ", "Y", "YES"):
        return True
    print("  — bỏ qua")
    return False


def lay_het(duong, tham=None):
    ra = []
    kq = doc(duong, dict(tham or {}, limit=100))
    while kq:
        ra.extend(kq.get("data", []))
        tiep = kq.get("paging", {}).get("next")
        if not tiep or len(ra) > 500:
            break
        try:
            kq = requests.get(tiep, timeout=60).json()
        except Exception:
            break
        if "error" in kq:
            break
    return ra


def khop(ten, chuoi):
    return chuoi.lower() in (ten or "").lower()


# ══════════════════════════════════════════════════════════════════
def viec_tam_dung_het(act, v):
    """Tạm dừng MỌI chiến dịch đang bật trên tài khoản."""
    cds = lay_het("%s/campaigns" % act,
                  {"fields": "name,status,effective_status,daily_budget"})
    dang_bat = [c for c in (cds or []) if c.get("status") == "ACTIVE"]
    if not dang_bat:
        print("  Không có chiến dịch nào đang bật. Không phải làm gì.")
        return
    tong = sum(float(c.get("daily_budget") or 0) for c in dang_bat)
    print("  Sẽ tạm dừng %d chiến dịch, tổng ngân sách %s mỗi ngày:"
          % (len(dang_bat), tien(tong)))
    for c in dang_bat:
        print("     · %s  (%s/ngày)" % (c.get("name"), tien(c.get("daily_budget") or 0)))
    if hoi_lam(""):
        for c in dang_bat:
            print("  Đang tạm dừng: %s" % c.get("name"))
            sua(c["id"], {"status": "PAUSED"})


def viec_tam_dung(act, v):
    ten = v.get("ten", "")
    cds = lay_het("%s/campaigns" % act, {"fields": "name,status,daily_budget"})
    hop = [c for c in (cds or []) if khop(c.get("name"), ten) and c.get("status") == "ACTIVE"]
    if not hop:
        print("  Không thấy chiến dịch nào đang bật có tên chứa %r." % ten)
        return
    for c in hop:
        print("  Sẽ tạm dừng: %s  (%s/ngày)" % (c.get("name"), tien(c.get("daily_budget") or 0)))
    if hoi_lam(""):
        for c in hop:
            sua(c["id"], {"status": "PAUSED"})


def viec_ngan_sach(act, v):
    ten = v.get("ten", "")
    moi = int(v.get("ngan_sach", 0))
    if moi <= 0:
        print("  Lệnh thiếu số ngân sách. Bỏ qua.")
        return
    cds = lay_het("%s/campaigns" % act, {"fields": "name,daily_budget"})
    hop = [c for c in (cds or []) if khop(c.get("name"), ten)]
    for c in hop:
        print("  %s: %s/ngày  →  %s/ngày"
              % (c.get("name"), tien(c.get("daily_budget") or 0), tien(moi)))
    if not hop:
        print("  Không thấy chiến dịch nào tên chứa %r." % ten)
        return
    if hoi_lam(""):
        for c in hop:
            sua(c["id"], {"daily_budget": str(moi)})


def viec_su_kien(act, v):
    """Đổi sự kiện tối ưu của nhóm quảng cáo."""
    ten    = v.get("ten", "")
    muc    = v.get("muc_tieu", "LANDING_PAGE_VIEWS")
    pixel  = v.get("pixel")
    su_kien = v.get("su_kien")
    cds = lay_het("%s/campaigns" % act, {"fields": "name"})
    for c in cds or []:
        nhs = lay_het("%s/adsets" % c["id"], {"fields": "name,optimization_goal"})
        for nh in nhs or []:
            if not (khop(nh.get("name"), ten) or khop(c.get("name"), ten)):
                continue
            print("  Nhóm %s: tối ưu %s  →  %s"
                  % (nh.get("name"), nh.get("optimization_goal"), muc))
            if hoi_lam(""):
                t = {"optimization_goal": muc}
                if pixel and su_kien:
                    t["promoted_object"] = json.dumps(
                        {"pixel_id": str(pixel), "custom_event_type": su_kien})
                sua(nh["id"], t)



def viec_bat(act, v):
    """Bat chien dich dang tam dung — BAT CA BA TANG.

    Bat moi chien dich la KHONG DU. tao-chien-dich.py dung moi thu o trang
    thai tam dung, nen phai bat lan luot: chien dich -> nhom quang cao ->
    tung mau quang cao. Thieu mot tang la khong mot dong nao chay, ma nhin
    tren Ads Manager lai tuong da bat roi.
    """
    ten = v.get("ten", "")
    cds = lay_het("%s/campaigns" % act,
                  {"fields": "name,status,effective_status,daily_budget"})
    hop = [c for c in (cds or [])
           if khop(c.get("name"), ten) and c.get("status") != "ACTIVE"]
    if not hop:
        print("  Khong thay chien dich nao dang tam dung co ten chua %r." % ten)
        print("  (Neu no da bat san roi thi khong phai lam gi.)")
        return

    for c in hop:
        nhs = lay_het("%s/adsets" % c["id"], {"fields": "name,status,daily_budget"}) or []
        tong = sum(float(n.get("daily_budget") or 0) for n in nhs) \
               or float(c.get("daily_budget") or 0)
        print("  Se BAT: %s" % c.get("name"))
        print("     %d nhom quang cao · tong %s moi ngay" % (len(nhs), tien(tong)))
        for n in nhs:
            print("       · %s  (%s/ngay)" % (n.get("name"), tien(n.get("daily_budget") or 0)))
        print("     TIEN BAT DAU CHAY NGAY SAU KHI BAT.")

    if not hoi_lam(""):
        return

    for c in hop:
        print("  Dang bat chien dich: %s" % c.get("name"))
        sua(c["id"], {"status": "ACTIVE"})
        for n in lay_het("%s/adsets" % c["id"], {"fields": "name,status"}) or []:
            sua(n["id"], {"status": "ACTIVE"})
            for q in lay_het("%s/ads" % n["id"], {"fields": "name,status"}) or []:
                sua(q["id"], {"status": "ACTIVE"})
        print("     Da bat ca ba tang: chien dich, nhom, mau quang cao.")



def viec_gia_han(act, v):
    """Doi ngay het han cua NHOM quang cao — chi keo DAI ra, khong bao gio rut ngan.

    Vi sao can: nhom quang cao dat han la den ngay do tu dung. Quen gia han la
    sang hom sau dung may, va Facebook mat luon phan da hoc duoc ve nhom khach.
    Dung bai moi la hoc lai tu dau, dat hon nhieu lan.

    Doi han KHONG bat lai quang cao dang tat. Mau nao dang tat van nam im.
    """
    import datetime

    ten    = v.get("ten", "")
    so_ngay = int(v.get("so_ngay", 3))
    if so_ngay < 1 or so_ngay > 30:
        print("  so_ngay phai tu 1 den 30. Dang de %r nen bo qua." % v.get("so_ngay"))
        return

    cds = lay_het("%s/campaigns" % act, {"fields": "name,status"})
    hop = [c for c in (cds or []) if khop(c.get("name"), ten)]
    if not hop:
        print("  Khong thay chien dich nao co ten chua %r." % ten)
        for c in (cds or [])[:10]:
            print("     dang co: %s" % c.get("name"))
        return

    bay_gio = datetime.datetime.now(datetime.timezone.utc)
    viec = []
    for c in hop:
        nhs = lay_het("%s/adsets" % c["id"],
                      {"fields": "name,status,end_time,daily_budget"}) or []
        for n in nhs:
            cu = n.get("end_time")
            if not cu:
                print("  · %s — khong dat han, chay lien tuc. Khong phai gia han."
                      % n.get("name"))
                continue
            try:
                moc = datetime.datetime.fromisoformat(cu.replace("Z", "+00:00"))
            except ValueError:
                print("  · %s — khong doc duoc ngay het han %r, bo qua."
                      % (n.get("name"), cu))
                continue
            # Het han roi thi tinh tu bay gio. Con han thi noi them vao duoi.
            goc = moc if moc > bay_gio else bay_gio
            moi = goc + datetime.timedelta(days=so_ngay)
            viec.append((c, n, moc, moi))

    if not viec:
        print("  Khong co nhom quang cao nao can gia han.")
        return

    tong = 0.0
    print("  SE GIA HAN THEM %d NGAY:" % so_ngay)
    for c, n, moc, moi in viec:
        ns = float(n.get("daily_budget") or 0)
        tong += ns * so_ngay
        qcs = lay_het("%s/ads" % n["id"], {"fields": "name,status"}) or []
        bat = [q for q in qcs if q.get("status") == "ACTIVE"]
        print("   · %s / %s" % (c.get("name"), n.get("name")))
        print("       han cu : %s" % moc.strftime("%d/%m/%Y %H:%M"))
        print("       han moi: %s" % moi.strftime("%d/%m/%Y %H:%M"))
        print("       ngan sach %s/ngay · %d mau dang BAT tren %d mau"
              % (tien(ns), len(bat), len(qcs)))
        for q in qcs:
            print("         %s %s" % ("BAT " if q.get("status") == "ACTIVE" else "tat ",
                                      q.get("name")))
    print("  TOI DA TIEU THEM: %s (%d ngay x ngan sach ngay)" % (tien(tong), so_ngay))
    print("  Mau dang tat van nam im — doi han khong bat lai gi ca.")

    if not hoi_lam(""):
        return

    for c, n, moc, moi in viec:
        print("  Dang doi han: %s" % n.get("name"))
        sua(n["id"], {"end_time": moi.strftime("%Y-%m-%dT%H:%M:%S+0000")})


VIEC = {
    "bat":          viec_bat,
    "gia_han":      viec_gia_han,
    "tam_dung_het": viec_tam_dung_het,
    "tam_dung":     viec_tam_dung,
    "ngan_sach":    viec_ngan_sach,
    "su_kien":      viec_su_kien,
}


# ══════════════════════════════════════════════════════════════════
def main():
    global TOKEN

    print("\n" + "═" * 62)
    print("  THI HÀNH LỆNH QUẢNG CÁO — %s"
          % ("LÀM THẬT (vẫn hỏi từng việc)" if LAM_THAT else "CHẠY THỬ, không đụng gì"))
    print("═" * 62)

    # --lenh <file>: chay mot file lenh khac. Can cho may chu GitHub — o do
    # chi duoc lam DUNG MOT viec, khong duoc quet ca lenh.json (trong do co
    # tam_dung_het va bat, chay nham la hong to).
    duong_lenh = "lenh.json"
    if "--lenh" in sys.argv:
        i = sys.argv.index("--lenh")
        if i + 1 >= len(sys.argv):
            sys.exit("Thiếu tên file sau --lenh")
        duong_lenh = sys.argv[i + 1]
        if os.path.sep in duong_lenh or duong_lenh.startswith("."):
            sys.exit("Tên file lệnh phải nằm ngay cạnh chương trình, không có đường dẫn.")
    if not os.path.exists(duong_lenh):
        sys.exit("Không thấy file %s cạnh chương trình này." % duong_lenh)
    lenh = json.load(io.open(duong_lenh, encoding="utf-8"))

    print("\n  Ghi chú của Phòng 7:")
    for d in (lenh.get("ghi_chu") or "").split("\n"):
        print("    %s" % d)

    if not TOKEN:
        # Tren may chu khong co ban phim. Bao ro chu khong de getpass no ra
        # mot dong loi Python kho hieu.
        if not sys.stdin.isatty():
            sys.exit("Không có FB_TOKEN, mà ở đây cũng không gõ tay được. "
                     "Đặt biến môi trường FB_TOKEN rồi chạy lại.")
        print("\nDán mã truy cập rồi Enter (cần quyền ads_management).")
        print("Gõ vào sẽ KHÔNG hiện lên màn hình — đó là cố ý.")
        TOKEN = getpass("  Mã truy cập: ").strip()
    if not TOKEN:
        sys.exit("Chưa có mã truy cập, dừng lại.")

    for khoi in lenh.get("khoi", []):
        tk = str(khoi.get("tai_khoan", "")).replace("act_", "").strip()
        if not tk.isdigit():
            print("\n⚠ Bỏ qua một khối: mã tài khoản không hợp lệ (%r)" % tk)
            continue
        act = "act_" + tk

        tt = doc(act, {"fields": "name,account_status,currency"})
        print("\n" + "─" * 62)
        print("  TÀI KHOẢN %s — %s" % (act, (tt or {}).get("name", "không đọc được")))
        print("─" * 62)
        if not tt:
            print("  Không đọc được tài khoản này, bỏ qua cả khối.")
            continue

        for v in khoi.get("viec", []):
            lam = v.get("lam")
            print("\n  ▸ %s" % (v.get("ly_do") or lam))
            ham = VIEC.get(lam)
            if not ham:
                print("    Lệnh %r chưa được hỗ trợ. Bỏ qua." % lam)
                continue
            ham(act, v)

    print("\n" + "═" * 62)
    if not LAM_THAT:
        print("  Vừa rồi chỉ là CHẠY THỬ. Không có gì bị thay đổi.")
        print("  Ưng thì chạy lại:   python3 thuc-thi.py --lam")
    else:
        print("  Đã thi hành xong. Chạy bao-cao-ads.py để xem lại kết quả.")
    print("═" * 62 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã dừng. Những việc chưa xác nhận thì chưa chạy.\n")
