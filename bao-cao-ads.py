#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BÁO CÁO QUẢNG CÁO RICH COENZYME Q10 — CHỈ ĐỌC, KHÔNG SỬA GÌ

Chương trình này KHÔNG tạo, KHÔNG sửa, KHÔNG tắt bật bất cứ thứ gì trong
tài khoản quảng cáo. Nó chỉ đọc rồi in ra màn hình. Chạy bao nhiêu lần
cũng không ảnh hưởng chiến dịch.

NÓ TRẢ LỜI HAI CÂU:
  1. Vì sao chưa cắn tiền?   — đọc mục issues_info của Meta, tức đúng
                                dòng lý do Meta ghi cho từng quảng cáo
  2. Đang lãi hay lỗ?        — chi phí mỗi đơn, đối chiếu mục tiêu 5%

CÁCH CHẠY
  1. pip install requests
  2. python3 bao-cao-ads.py
  3. Dán mã truy cập vào (gõ không hiện lên màn hình, đó là bình thường)

Cuối cùng nó in ra một khối BÁO CÁO. Anh copy khối đó gửi cho Phòng 7
để đối chiếu với số đơn thật.

LẤY MÃ TRUY CẬP Ở ĐÂU — xem cuối file.
"""

import json
import os
import sys
from getpass import getpass

try:
    import requests
except ImportError:
    sys.exit("Thiếu thư viện. Chạy trước:  pip install requests")

API = "https://graph.facebook.com/v21.0"

TOKEN     = os.environ.get("FB_TOKEN", "")
TAI_KHOAN = os.environ.get("FB_ACT", "2260044828113956")   # Phạm Sơn BM1.1

# Giá mỗi hộp, dùng để quy doanh thu ra mục tiêu 5%
GIA_HOP   = 2890000
MUC_TIEU  = 0.05          # chi phí quảng cáo tối đa = 5% doanh thu


def tien(x):
    """1234567 -> '1.234.567đ'"""
    try:
        n = int(round(float(x)))
    except (TypeError, ValueError):
        return "—"
    return "{:,}".format(n).replace(",", ".") + "đ"


def goi(duong, tham=None):
    t = dict(tham or {})
    t["access_token"] = TOKEN
    try:
        r = requests.get("%s/%s" % (API, duong), params=t, timeout=60)
    except requests.exceptions.SSLError:
        sys.exit("Không thiết lập được kết nối an toàn tới Facebook.\n"
                 "Thường là do phần mềm diệt virus hoặc mạng công ty chặn. "
                 "Thử đổi sang mạng 4G điện thoại.")
    except requests.exceptions.ConnectionError:
        sys.exit("Không nối được mạng ra Facebook. Kiểm tra lại đường truyền.")
    except requests.exceptions.Timeout:
        sys.exit("Facebook trả lời quá chậm. Chạy lại sau vài phút.")

    try:
        kq = r.json()
    except ValueError:
        sys.exit("Facebook trả về nội dung lạ (mã %d). Chạy lại sau." % r.status_code)

    if "error" in kq:
        e = kq["error"]
        thong_bao = e.get("error_user_msg") or e.get("message") or "lỗi không rõ"
        print("\n  ⚠ Facebook báo: %s" % thong_bao)
        return None
    return kq


def lay_het(duong, tham=None):
    """Đọc hết các trang kết quả."""
    ra = []
    kq = goi(duong, dict(tham or {}, limit=100))
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


def so_tu_actions(danh_sach, ten):
    for a in danh_sach or []:
        if a.get("action_type") == ten:
            try:
                return float(a.get("value", 0))
            except (TypeError, ValueError):
                return 0.0
    return 0.0


# ══════════════════════════════════════════════════════════════════
def main():
    global TOKEN, TAI_KHOAN

    print("\n" + "═" * 62)
    print("  BÁO CÁO QUẢNG CÁO Q10 — chương trình chỉ đọc, không sửa gì")
    print("═" * 62)

    if not TOKEN:
        print("\nDán mã truy cập rồi Enter.")
        print("Gõ vào sẽ KHÔNG hiện lên màn hình — đó là cố ý, để người ngồi cạnh")
        print("hoặc ảnh chụp màn hình không đọc trộm được mã của anh.")
        TOKEN = getpass("  Mã truy cập: ").strip()
    if not TOKEN:
        sys.exit("Chưa có mã truy cập, dừng lại.")

    tk = input("\n  Mã tài khoản quảng cáo [%s]: " % TAI_KHOAN).strip() or TAI_KHOAN
    tk = tk.replace("act_", "").strip()
    if not tk.isdigit():
        sys.exit("Mã tài khoản phải là dãy số. Nhận được: %r" % tk)
    TAI_KHOAN = tk
    act = "act_" + TAI_KHOAN

    # ── 1. Sức khoẻ tài khoản ────────────────────────────────────
    print("\n" + "─" * 62)
    print("  1. TÀI KHOẢN")
    print("─" * 62)

    tt = goi(act, {"fields": "name,account_status,disable_reason,currency,"
                             "amount_spent,spend_cap,balance,funding_source_details"})
    if not tt:
        sys.exit("\nKhông đọc được tài khoản. Thường do mã truy cập sai, hết hạn, "
                 "hoặc mã này không có quyền trên tài khoản vừa nhập.")

    TRANG_THAI = {1: "Đang hoạt động bình thường",
                  2: "ĐÃ BỊ VÔ HIỆU HOÁ",
                  3: "Chưa thanh toán",
                  7: "Đang chờ xét duyệt rủi ro",
                  8: "Chờ kết thúc",
                  9: "Đang trong thời gian ân hạn",
                  100: "Đóng vĩnh viễn",
                  101: "ĐÃ BỊ ĐÓNG"}
    ma_tt = tt.get("account_status")
    print("  Tên tài khoản   : %s" % tt.get("name", "—"))
    print("  Tình trạng      : %s (mã %s)" % (TRANG_THAI.get(ma_tt, "không rõ"), ma_tt))
    if tt.get("disable_reason"):
        print("  Lý do bị khoá   : mã %s" % tt["disable_reason"])
    print("  Tiền tệ         : %s" % tt.get("currency", "—"))
    print("  Đã tiêu từ đầu  : %s" % tien(tt.get("amount_spent", 0)))
    if tt.get("spend_cap") and float(tt["spend_cap"]) > 0:
        cap = float(tt["spend_cap"]); da = float(tt.get("amount_spent", 0))
        print("  Hạn mức chi tiêu: %s (còn lại %s)" % (tien(cap), tien(cap - da)))
        if da >= cap - 1:
            print("  ⛔ ĐÃ CHẠM HẠN MỨC — đây chính là lý do không tiêu thêm được đồng nào.")
    kv = (tt.get("funding_source_details") or {}).get("display_string")
    print("  Hình thức trả   : %s" % (kv or "CHƯA GẮN PHƯƠNG THỨC THANH TOÁN"))

    if ma_tt != 1:
        print("\n  ⛔ Tài khoản không ở trạng thái bình thường. Chiến dịch vẫn có thể")
        print("     hiện 'Đang hoạt động' nhưng sẽ KHÔNG tiêu một đồng nào.")

    # ── 2. Vì sao chưa chạy ──────────────────────────────────────
    print("\n" + "─" * 62)
    print("  2. VÌ SAO CHƯA CẮN TIỀN — lý do do chính Meta ghi")
    print("─" * 62)

    cds = lay_het("%s/campaigns" % act,
                  {"fields": "name,status,effective_status,daily_budget,lifetime_budget,issues_info"})
    if cds is None or not cds:
        print("  Tài khoản chưa có chiến dịch nào.")

    tat_ca_van_de = []

    for cd in cds:
        ns = cd.get("daily_budget") or cd.get("lifetime_budget")
        print("\n  ▸ CHIẾN DỊCH: %s" % cd.get("name"))
        print("      công tắc %s · phân phối %s%s" % (
            cd.get("status"), cd.get("effective_status"),
            " · ngân sách %s/ngày" % tien(ns) if cd.get("daily_budget") else ""))
        for v in cd.get("issues_info") or []:
            tat_ca_van_de.append(("Chiến dịch " + str(cd.get("name")), v))
            print("      ⚠ %s" % (v.get("error_summary") or v.get("error_message")))

        nhs = lay_het("%s/adsets" % cd["id"],
                      {"fields": "name,status,effective_status,daily_budget,"
                                 "optimization_goal,start_time,issues_info"})
        for nh in nhs or []:
            print("      • Nhóm: %s" % nh.get("name"))
            print("          công tắc %s · phân phối %s · tối ưu %s%s" % (
                nh.get("status"), nh.get("effective_status"),
                nh.get("optimization_goal", "—"),
                " · %s/ngày" % tien(nh["daily_budget"]) if nh.get("daily_budget") else ""))
            if nh.get("start_time"):
                print("          bắt đầu chạy từ %s" % nh["start_time"])
            for v in nh.get("issues_info") or []:
                tat_ca_van_de.append(("Nhóm " + str(nh.get("name")), v))
                print("          ⚠ %s" % (v.get("error_summary") or v.get("error_message")))

            qcs = lay_het("%s/ads" % nh["id"],
                          {"fields": "name,status,effective_status,issues_info"})
            for q in qcs or []:
                print("          - Quảng cáo: %s  [%s / %s]" % (
                    q.get("name"), q.get("status"), q.get("effective_status")))
                for v in q.get("issues_info") or []:
                    tat_ca_van_de.append(("Quảng cáo " + str(q.get("name")), v))
                    print("              ⚠ %s" % (v.get("error_summary") or v.get("error_message")))

    if not tat_ca_van_de:
        print("\n  Meta không ghi nhận vấn đề nào ở cả ba cấp.")
        print("  Nếu vẫn không tiêu tiền, xem lại mục 1 (hạn mức, thanh toán, tình trạng")
        print("  tài khoản) và giờ bắt đầu của nhóm quảng cáo ở trên.")
    else:
        print("\n  ⛔ TỔNG CỘNG %d VẤN ĐỀ ĐANG CHẶN PHÂN PHỐI:" % len(tat_ca_van_de))
        for o, v in tat_ca_van_de:
            print("     · [%s] %s" % (o, v.get("error_summary") or v.get("error_message")))

    # ── 3. Số liệu ───────────────────────────────────────────────
    print("\n" + "─" * 62)
    print("  3. SỐ LIỆU")
    print("─" * 62)

    truong = ("spend,impressions,reach,clicks,ctr,cpc,cpm,"
              "actions,cost_per_action_type")

    for nhan, moc in [("HÔM NAY", "today"),
                      ("HÔM QUA", "yesterday"),
                      ("7 NGÀY QUA", "last_7d")]:
        kq = goi("%s/insights" % act, {"fields": truong, "date_preset": moc})
        d = (kq or {}).get("data") or []
        if not d:
            print("\n  %-12s chưa có dữ liệu (chưa phân phối lần nào trong kỳ này)" % nhan)
            continue
        r = d[0]
        chi = float(r.get("spend", 0) or 0)
        acts = r.get("actions") or []
        lead     = so_tu_actions(acts, "lead")
        onsite   = so_tu_actions(acts, "onsite_conversion.lead_grouped")
        tin_nhan = so_tu_actions(acts, "onsite_conversion.messaging_first_reply")
        lpv      = so_tu_actions(acts, "landing_page_view")
        don      = max(lead, onsite)

        print("\n  %-12s chi %s · hiện %s lần · %s người · %s click · CTR %s%%" % (
            nhan, tien(chi),
            r.get("impressions", "0"), r.get("reach", "0"),
            r.get("clicks", "0"), r.get("ctr", "0")[:4] if r.get("ctr") else "0"))
        print("               CPM %s · CPC %s" % (tien(r.get("cpm", 0)), tien(r.get("cpc", 0))))
        print("               xem trang đích %d · tin nhắn %d · khách để lại số %d" % (
            lpv, tin_nhan, don))

        if don > 0:
            moi_don = chi / don
            print("               ➜ chi phí mỗi khách để lại số: %s" % tien(moi_don))
            for so_hop in (1, 3, 5, 6):
                dt = GIA_HOP * so_hop
                nguong = dt * MUC_TIEU
                dat = "ĐẠT" if moi_don <= nguong else "chưa đạt"
                print("                  đơn %d hộp (%s): ngưỡng 5%% = %s → %s"
                      % (so_hop, tien(dt), tien(nguong), dat))
        elif chi > 0:
            print("               ➜ đã tiêu %s mà chưa có khách nào để lại số." % tien(chi))
            for so_hop in (1, 6):
                print("                  (ngưỡng 5%% của đơn %d hộp là %s)"
                      % (so_hop, tien(GIA_HOP * so_hop * MUC_TIEU)))

    # ── 4. Khối copy gửi Phòng 7 ─────────────────────────────────
    kq = goi("%s/insights" % act, {"fields": "spend,actions", "date_preset": "today"})
    d = (kq or {}).get("data") or [{}]
    r = d[0] if d else {}
    chi_hom_nay = float(r.get("spend", 0) or 0)
    acts = r.get("actions") or []
    don_hom_nay = max(so_tu_actions(acts, "lead"),
                      so_tu_actions(acts, "onsite_conversion.lead_grouped"))

    print("\n" + "═" * 62)
    print("  4. KHỐI BÁO CÁO — copy nguyên khối dưới đây gửi Phòng 7")
    print("═" * 62)
    print("""
BÁO CÁO ADS %s
Tình trạng tài khoản : %s
Chi hôm nay          : %s
Khách để lại số      : %d
Vấn đề chặn phân phối: %d
%s
""" % (act,
       TRANG_THAI.get(ma_tt, "không rõ"),
       tien(chi_hom_nay),
       int(don_hom_nay),
       len(tat_ca_van_de),
       "\n".join("  - [%s] %s" % (o, v.get("error_summary") or v.get("error_message"))
                 for o, v in tat_ca_van_de) or "  (không có)"))

    print("═" * 62)
    print("  Chương trình không sửa gì trong tài khoản. Chạy lại lúc nào cũng được.")
    print("═" * 62 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã dừng.\n")


# ══════════════════════════════════════════════════════════════════
# LẤY MÃ TRUY CẬP Ở ĐÂU
#
#   1. Mở  https://developers.facebook.com/tools/explorer/
#   2. Ô "Meta App" chọn ứng dụng bất kỳ của anh
#   3. Bấm "Add permissions" thêm hai quyền:
#         ads_read
#         business_management
#   4. Bấm "Generate Access Token", đăng nhập, đồng ý
#   5. Copy chuỗi rất dài đó, dán vào chương trình khi nó hỏi
#
#   Mã này sống khoảng 1-2 giờ rồi hết hạn. Hết hạn thì lấy lại mã mới,
#   mất chừng 30 giây.
#
#   ĐỪNG GỬI MÃ NÀY CHO AI, KỂ CẢ CHO EM TRONG KHUNG CHAT.
#   Ai cầm mã này là đọc và tiêu được tiền trong tài khoản quảng cáo của anh.
#   Chương trình hỏi bằng getpass nên mã không hiện lên màn hình, không lọt
#   vào ảnh chụp màn hình, và không nằm lại trong lịch sử câu lệnh.
# ══════════════════════════════════════════════════════════════════
