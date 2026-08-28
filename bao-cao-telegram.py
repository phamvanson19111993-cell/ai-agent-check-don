#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GỬI BÁO CÁO QUẢNG CÁO VỀ TELEGRAM — chạy tự động mỗi giờ

Chương trình CHỈ ĐỌC. Không tạo, không sửa, không tắt bật gì trong
tài khoản quảng cáo.

VÌ SAO TELEGRAM CHỨ KHÔNG PHẢI ZALO
  Zalo chỉ cho gửi tin tự động qua Official Account đã được duyệt —
  phải đăng ký doanh nghiệp, chờ xét, và token cũng hết hạn định kỳ.
  Telegram thì tạo bot mất 30 giây và token dùng vĩnh viễn.
  Anh vẫn nhận trên điện thoại như mọi tin nhắn khác.

CẦN BA THỨ, điền vào khối CẦN ĐIỀN bên dưới hoặc đặt biến môi trường:
  TG_TOKEN   mã bot Telegram        — lấy từ @BotFather
  TG_CHAT    mã cuộc trò chuyện     — lấy từ @userinfobot
  FB_TOKEN   mã truy cập Facebook   — NÊN dùng token Người dùng hệ thống

⚠️ TOKEN FACEBOOK LẤY TỪ GRAPH API EXPLORER CHỈ SỐNG 1-2 TIẾNG.
   Chạy tự động mỗi giờ thì phải dùng token Người dùng hệ thống
   (System User) trong Trình quản lý doanh nghiệp — loại đó không
   hết hạn. Xem hướng dẫn cuối file.

CÁCH CHẠY THỬ MỘT LẦN
    python3 bao-cao-telegram.py

CÁCH CHẠY TỰ ĐỘNG MỖI GIỜ
    Windows : Task Scheduler → Create Task → Trigger: mỗi 1 giờ
              → Action: python3  C:\\...\\bao-cao-telegram.py
    Mac/Linux: crontab -e  rồi thêm dòng
              0 * * * * cd /duong/dan && python3 bao-cao-telegram.py
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    sys.exit("Thiếu thư viện. Chạy trước:  pip install requests")

API = "https://graph.facebook.com/v21.0"

# ─────────────────────────── CẦN ĐIỀN ───────────────────────────
TG_TOKEN  = os.environ.get("TG_TOKEN", "")
TG_CHAT   = os.environ.get("TG_CHAT",  "")
FB_TOKEN  = os.environ.get("FB_TOKEN", "")
TAI_KHOAN = os.environ.get("FB_ACT",   "2260044828113956")
PIXEL     = os.environ.get("FB_PIXEL", "1277743445418211")
# ────────────────────────────────────────────────────────────────

GIA_HOP  = 2890000
MUC_TIEU = 0.05
VN = timezone(timedelta(hours=7))

PHEU = [
    ("PageView",         "Vào trang"),
    ("DenCoChe",         "Tới cơ chế"),
    ("DenHoSo",          "Tới giấy tờ"),
    ("DenBangGia",       "Tới bảng giá"),
    ("DenForm",          "Thấy biểu mẫu"),
    ("InitiateCheckout", "Bắt đầu điền"),
    ("Lead",             "Gửi đơn"),
    ("Purchase",         "Đã chuyển khoản"),
]


def tien(x):
    try:
        return "{:,}".format(int(round(float(x)))).replace(",", ".") + "đ"
    except (TypeError, ValueError):
        return "—"


def doc(duong, tham=None):
    t = dict(tham or {}); t["access_token"] = FB_TOKEN
    try:
        r = requests.get("%s/%s" % (API, duong), params=t, timeout=45)
        kq = r.json()
    except Exception as e:
        return {"_loi": str(e)[:120]}
    if "error" in kq:
        e = kq["error"]
        return {"_loi": e.get("error_user_msg") or e.get("message") or "lỗi không rõ"}
    return kq


def gui_telegram(chu):
    """Gửi tin. Trả về None nếu xong, hoặc câu lỗi."""
    if not TG_TOKEN or not TG_CHAT:
        return "Chưa điền TG_TOKEN hoặc TG_CHAT"
    try:
        r = requests.post(
            "https://api.telegram.org/bot%s/sendMessage" % TG_TOKEN,
            data={"chat_id": TG_CHAT, "text": chu,
                  "parse_mode": "HTML", "disable_web_page_preview": "true"},
            timeout=30)
        kq = r.json()
        if not kq.get("ok"):
            return "Telegram từ chối: %s" % kq.get("description", "không rõ")
    except Exception as e:
        return "Không gửi được: %s" % str(e)[:120]
    return None


def so_tu_actions(ds, ten):
    for a in ds or []:
        if a.get("action_type") == ten:
            try:
                return float(a.get("value", 0))
            except (TypeError, ValueError):
                return 0.0
    return 0.0


# ══════════════════════════════════════════════════════════════════
def dung_bao_cao():
    gio = datetime.now(VN).strftime("%H:%M %d/%m")
    d = ["<b>BÁO CÁO Q10 · %s</b>" % gio]
    act = "act_" + str(TAI_KHOAN).replace("act_", "")

    # ── Tình trạng tài khoản ──
    tt = doc(act, {"fields": "name,account_status,amount_spent,spend_cap"})
    if "_loi" in tt:
        d.append("\n⚠️ Không đọc được tài khoản.")
        d.append("Lý do: %s" % tt["_loi"])
        d.append("\nThường là mã truy cập đã hết hạn. Token lấy từ Graph API")
        d.append("Explorer chỉ sống 1-2 tiếng — chạy tự động phải dùng token")
        d.append("Người dùng hệ thống.")
        return "\n".join(d)

    if tt.get("account_status") != 1:
        d.append("\n⛔ <b>TÀI KHOẢN KHÔNG HOẠT ĐỘNG BÌNH THƯỜNG</b> (mã %s)"
                 % tt.get("account_status"))

    # ── Chi tiêu hôm nay ──
    ins = doc("%s/insights" % act,
              {"fields": "spend,impressions,reach,clicks,actions", "date_preset": "today"})
    r = (ins.get("data") or [{}])[0] if "_loi" not in ins else {}
    chi = float(r.get("spend", 0) or 0)
    acts = r.get("actions") or []
    lpv  = so_tu_actions(acts, "landing_page_view")
    lead = max(so_tu_actions(acts, "lead"),
               so_tu_actions(acts, "onsite_conversion.lead_grouped"))

    d.append("\n<b>HÔM NAY</b>")
    d.append("Chi          %s" % tien(chi))
    d.append("Tiếp cận     %s người" % (r.get("reach") or "0"))
    d.append("Xem trang    %d" % lpv)
    if lpv:
        d.append("Mỗi lượt xem %s" % tien(chi / lpv))
    d.append("Đơn          <b>%d</b>" % lead)

    if lead:
        moi_don = chi / lead
        d.append("\nChi phí mỗi đơn <b>%s</b>" % tien(moi_don))
        for n in (1, 2, 6):
            ng = GIA_HOP * n * MUC_TIEU
            d.append("  đơn %d hộp · ngưỡng 5%% %s → %s"
                     % (n, tien(ng), "ĐẠT ✅" if moi_don <= ng else "chưa đạt"))
    elif chi > 0:
        d.append("\nChưa có đơn nào hôm nay.")

    # ── Phễu ──
    st = doc("%s/stats" % PIXEL, {"aggregation": "event"})
    dem = {}
    if "_loi" not in st:
        for muc in (st.get("data") or []):
            v = muc.get("value")
            if isinstance(v, dict):
                for k, n in v.items():
                    dem[k] = dem.get(k, 0) + int(n)

    if dem:
        goc = dem.get("PageView", 0)
        d.append("\n<b>KHÁCH ĐỌC TỚI ĐÂU</b>")
        truoc, mat_nhat, cho = None, 0, ""
        for ten, mo in PHEU:
            n = dem.get(ten, 0)
            pt = (100.0 * n / goc) if goc else 0
            d.append("%-16s %5d  %3.0f%%" % (mo, n, pt))
            if truoc is not None and truoc >= 10 and (truoc - n) > mat_nhat:
                mat_nhat, cho = truoc - n, mo
            truoc = n
        if cho:
            d.append("\n⛔ Mất nhiều nhất ở: <b>%s</b> (%d người)" % (cho, mat_nhat))
    else:
        d.append("\n<i>Chưa đọc được phễu từ Pixel.</i>")

    d.append("\n<i>Chương trình chỉ đọc, không sửa gì.</i>")
    return "\n".join(d)


def main():
    if not FB_TOKEN:
        print("Chưa có FB_TOKEN. Điền vào khối CẦN ĐIỀN hoặc đặt biến môi trường.")
        sys.exit(1)

    chu = dung_bao_cao()
    print(chu.replace("<b>", "").replace("</b>", "")
             .replace("<i>", "").replace("</i>", ""))

    loi = gui_telegram(chu)
    print("\n" + ("─" * 50))
    if loi:
        print("⚠️ CHƯA GỬI ĐƯỢC TELEGRAM: %s" % loi)
        print("Báo cáo vẫn in ra màn hình ở trên.")
    else:
        print("✅ Đã gửi về Telegram lúc %s" % datetime.now(VN).strftime("%H:%M %d/%m"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng.")


# ══════════════════════════════════════════════════════════════════
# LẤY BA MÃ Ở ĐÂU
#
# 1. TG_TOKEN — mã bot Telegram
#    Mở Telegram, tìm  @BotFather  → gõ  /newbot
#    Đặt tên bot, đặt tên đăng nhập kết thúc bằng "bot"
#    BotFather trả về một chuỗi dạng  8123456789:AAH...xyz
#
# 2. TG_CHAT — mã cuộc trò chuyện của anh
#    Tìm  @userinfobot  → bấm Start → nó trả về Id của anh
#    NHỚ: phải nhắn cho bot của anh một câu bất kỳ trước, nếu không
#    Telegram không cho bot nhắn tới anh.
#
# 3. FB_TOKEN — mã truy cập Facebook, loại KHÔNG HẾT HẠN
#    business.facebook.com → Cài đặt doanh nghiệp → Người dùng
#    → Người dùng hệ thống → Thêm → đặt tên, vai trò Quản trị viên
#    → Chỉ định tài sản: chọn tài khoản quảng cáo và Pixel
#    → Tạo mã truy cập mới → tick quyền  ads_read  và  business_management
#    Token này KHÔNG hết hạn, hợp cho chạy tự động mỗi giờ.
#
#    ĐỪNG GỬI TOKEN NÀY CHO AI, KỂ CẢ TRONG KHUNG CHAT.
# ══════════════════════════════════════════════════════════════════
