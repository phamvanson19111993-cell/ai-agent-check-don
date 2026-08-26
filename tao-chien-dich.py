#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DỰNG CHIẾN DỊCH QUẢNG CÁO RICH COENZYME Q10 — TỰ ĐỘNG

Chương trình này tự tạo trong tài khoản quảng cáo của anh:
  · 1 chiến dịch          mục tiêu Doanh số
  · 3 nhóm quảng cáo      40-50 · 50-65 · 28-40, mỗi nhóm 150.000đ/ngày
  · 3 mẫu quảng cáo       chữ riêng cho từng nhóm tuổi

TẤT CẢ ĐỀU Ở TRẠNG THÁI TẠM DỪNG. Không một đồng nào bị tiêu cho tới khi
anh vào Ads Manager tự gạt nút bật. Đây là cố ý — để anh soi lại một lượt
trước khi tiền bắt đầu chạy.

CÁCH CHẠY
  1. Điền bốn dòng trong khối CẦN ĐIỀN bên dưới
  2. pip install requests
  3. python3 tao-chien-dich.py

LẤY BỐN SỐ Ở ĐÂU — xem cuối file.
"""

import json
import os
import sys

try:
    import requests
except ImportError:
    sys.exit("Thiếu thư viện. Chạy trước:  pip install requests")

API = "https://graph.facebook.com/v21.0"

# ─────────────────────────── CẦN ĐIỀN ───────────────────────────
# Có thể điền thẳng vào đây, hoặc đặt biến môi trường cùng tên.

TOKEN      = os.environ.get("FB_TOKEN",   "")   # Mã truy cập, chuỗi rất dài
TAI_KHOAN  = os.environ.get("FB_ACT",     "")   # Mã tài khoản quảng cáo, chỉ số
TRANG      = os.environ.get("FB_PAGE",    "")   # Mã Trang DiLiM Supplement
PIXEL      = os.environ.get("FB_PIXEL",   "")   # Mã Pixel THẬT (không phải mã tài khoản)

ANH_QC     = "images/qc-vuong.jpg"              # Ảnh quảng cáo 1080x1080
LINK       = "https://sonsongkhoe.com"
NGAN_SACH  = 150000                             # đồng mỗi ngày, mỗi nhóm
TEN_CD     = "Q10 · T9 · Tiếp cận mới"
# ────────────────────────────────────────────────────────────────

KHUYEN_CAO = "Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."

NHOM = [
    {
        "ten": "Nhom 1 · 40-50",
        "tuoi": (40, 50),
        "chu": (
            "Sau tuổi 40, lượng Coenzyme Q10 cơ thể tự tạo ra giảm dần. Nhiều người thấy "
            "chiều nào cũng đuối dù sáng vẫn khoẻ, ngủ đủ mà sáng dậy vẫn nặng người.\n\n"
            "Rich Coenzyme Q10 — hàng nội địa Nhật của AFC, 2 viên mỗi ngày. Giúp chống "
            "oxy hoá, giảm mệt mỏi.\n\n"
            "Trên trang có bài tự kiểm 30 giây: sáu câu hỏi, không hỏi tên, không hỏi số "
            "điện thoại, trả lời xong có kết quả ngay.\n\n" + KHUYEN_CAO
        ),
        "tieu_de": "Sáu câu hỏi, 30 giây, có kết quả ngay",
        "mo_ta": "Hàng nội địa Nhật · Số công bố 4107/2024/ĐKSP",
    },
    {
        "ten": "Nhom 2 · 50-65",
        "tuoi": (50, 65),
        "chu": (
            "Tim là cơ bắp duy nhất trong người không được phép nghỉ. Sau tuổi 50, nhiều "
            "người leo hai tầng cầu thang đã phải dừng lại thở.\n\n"
            "Coenzyme Q10 là chất tế bào dùng để tạo ra năng lượng, và cơ thể tự tạo ra "
            "ngày một ít đi theo tuổi.\n\n"
            "Rich Coenzyme Q10 của AFC Nhật Bản — hãng niêm yết trên sàn Tokyo, nhà máy "
            "đạt chuẩn GMP Nhật. Một lọ 120 viên dùng đúng hai tháng. Giúp chống oxy hoá, "
            "giảm mệt mỏi; giúp giảm nguy cơ xơ vữa động mạch, tốt cho tim mạch.\n\n" + KHUYEN_CAO
        ),
        "tieu_de": "Một lọ 120 viên, dùng đúng hai tháng",
        "mo_ta": "Giấy tờ tra được ngay trên trang",
    },
    {
        "ten": "Nhom 3 · 28-40 con mua",
        "tuoi": (28, 40),
        "chu": (
            "Bố mẹ ngoài 55 thường ngại nói mình mệt. Đến lúc nói ra thì đã mệt lâu rồi.\n\n"
            "Rich Coenzyme Q10 — hàng nội địa Nhật của AFC, hãng ra đời năm 1969 và niêm "
            "yết trên sàn Tokyo. Một lọ 120 viên dùng đúng hai tháng, ngày 2 viên sau bữa sáng.\n\n"
            "Giấy tiếp nhận công bố số 4107/2024/ĐKSP, ảnh chụp giấy gốc và nhãn phụ đăng "
            "ngay trên trang để nhà mình tự đối chiếu.\n\n" + KHUYEN_CAO
        ),
        "tieu_de": "Quà cho bố mẹ, hàng nội địa Nhật",
        "mo_ta": "Giao toàn quốc · Đặt cọc 200.000đ giữ hàng",
    },
]


def goi(duong_dan, du_lieu=None, tep=None, lay=False):
    """Gọi một lệnh tới Facebook. Dừng hẳn nếu Facebook báo lỗi."""
    url = "%s/%s" % (API, duong_dan)
    if lay:
        r = requests.get(url, params=dict(du_lieu or {}, access_token=TOKEN), timeout=60)
    elif tep:
        r = requests.post(url, data={"access_token": TOKEN}, files=tep, timeout=180)
    else:
        r = requests.post(url, data=dict(du_lieu, access_token=TOKEN), timeout=60)

    try:
        kq = r.json()
    except ValueError:
        sys.exit("Facebook trả về thứ không đọc được (mã %s):\n%s" % (r.status_code, r.text[:600]))

    if "error" in kq:
        e = kq["error"]
        print("\n╭─ FACEBOOK TỪ CHỐI ─────────────────────────────")
        print("│ " + e.get("error_user_title") or e.get("type", ""))
        print("│ " + (e.get("error_user_msg") or e.get("message", "")))
        if e.get("error_subcode"):
            print("│ mã phụ: %s" % e["error_subcode"])
        print("╰────────────────────────────────────────────────")
        sys.exit(1)
    return kq


def kiem_tra_dau_vao():
    thieu = [t for t, v in (("FB_TOKEN", TOKEN), ("FB_ACT", TAI_KHOAN),
                            ("FB_PAGE", TRANG), ("FB_PIXEL", PIXEL)) if not v]
    if thieu:
        sys.exit("Chưa điền: %s — mở file, điền vào khối CẦN ĐIỀN." % ", ".join(thieu))

    if TAI_KHOAN == PIXEL:
        sys.exit("Mã tài khoản và mã Pixel đang giống hệt nhau. Một trong hai đang sai.\n"
                 "Mã Pixel lấy ở Trình quản lý sự kiện, trong URL đoạn /dataset/<mã>/")

    if not os.path.exists(ANH_QC):
        sys.exit("Không thấy ảnh %s — sửa dòng ANH_QC cho đúng đường dẫn." % ANH_QC)


def main():
    kiem_tra_dau_vao()
    act = "act_%s" % TAI_KHOAN.replace("act_", "")

    # Xem tài khoản có sống không, và tiêu bằng tiền gì
    tk = goi(act, {"fields": "name,currency,account_status,disable_reason"}, lay=True)
    print("Tài khoản : %s" % tk.get("name"))
    print("Đơn vị    : %s" % tk.get("currency"))
    if tk.get("account_status") != 1:
        sys.exit("Tài khoản đang không ở trạng thái hoạt động (account_status=%s). "
                 "Kiểm tra thẻ thanh toán trước." % tk.get("account_status"))
    if tk.get("currency") != "VND":
        print("!! Tài khoản tiêu bằng %s chứ không phải VND — con số ngân sách bên dưới "
              "sẽ KHÔNG phải 150.000đ. Dừng lại và tính lại trước khi chạy tiếp."
              % tk.get("currency"))
        sys.exit(1)

    # Ảnh dùng chung cho ba mẫu
    with open(ANH_QC, "rb") as f:
        anh = goi("%s/adimages" % act, tep={"file": (os.path.basename(ANH_QC), f)})
    ma_anh = list(anh["images"].values())[0]["hash"]
    print("Ảnh       : đã tải lên")

    # Tầng 1 — chiến dịch
    cd = goi("%s/campaigns" % act, {
        "name": TEN_CD,
        "objective": "OUTCOME_SALES",
        "status": "PAUSED",
        "special_ad_categories": json.dumps([]),
    })
    print("\nChiến dịch: %s  (%s)" % (TEN_CD, cd["id"]))

    for n in NHOM:
        tuoi_min, tuoi_max = n["tuoi"]

        # Tầng 2 — nhóm quảng cáo
        nhom = goi("%s/adsets" % act, {
            "name": n["ten"],
            "campaign_id": cd["id"],
            "status": "PAUSED",
            "daily_budget": NGAN_SACH,
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "OFFSITE_CONVERSIONS",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "promoted_object": json.dumps({
                "pixel_id": PIXEL,
                "custom_event_type": "LEAD",
            }),
            "targeting": json.dumps({
                "geo_locations": {"countries": ["VN"]},
                "age_min": tuoi_min,
                "age_max": tuoi_max,
                "targeting_automation": {"advantage_audience": 0},
            }),
        })

        # Tầng 3 — mẫu quảng cáo
        mau = goi("%s/adcreatives" % act, {
            "name": "Mau · %s" % n["ten"],
            "object_story_spec": json.dumps({
                "page_id": TRANG,
                "link_data": {
                    "link": LINK,
                    "message": n["chu"],
                    "name": n["tieu_de"],
                    "description": n["mo_ta"],
                    "image_hash": ma_anh,
                    "call_to_action": {"type": "LEARN_MORE", "value": {"link": LINK}},
                },
            }),
            "degrees_of_freedom_spec": json.dumps({
                "creative_features_spec": {
                    "standard_enhancements": {"enroll_status": "OPT_OUT"}
                }
            }),
        })

        qc = goi("%s/ads" % act, {
            "name": "QC · %s" % n["ten"],
            "adset_id": nhom["id"],
            "creative": json.dumps({"creative_id": mau["id"]}),
            "status": "PAUSED",
        })

        print("  %-24s tuổi %2d–%2d  %s đ/ngày   nhóm %s"
              % (n["ten"], tuoi_min, tuoi_max, format(NGAN_SACH, ","), nhom["id"]))

    print("""
╭────────────────────────────────────────────────────────────╮
│  XONG. Mọi thứ đang TẠM DỪNG, chưa tiêu đồng nào.          │
│                                                            │
│  Việc còn lại của anh:                                     │
│   1. Mở Ads Manager, xem lại ba mẫu quảng cáo              │
│   2. Thay ảnh bằng video nếu đã quay xong                  │
│   3. Gạt nút bật ở cả chiến dịch lẫn ba nhóm              │
│                                                            │
│  Bật đủ ba nhóm là tiêu 450.000đ mỗi ngày.                │
╰────────────────────────────────────────────────────────────╯
""")


if __name__ == "__main__":
    main()

# ─────────────────── LẤY BỐN SỐ Ở ĐÂU ───────────────────
#
# FB_TOKEN — Mã truy cập
#   Cách nhanh, dùng được 1–2 giờ, đủ để chạy chương trình này:
#     developers.facebook.com/tools/explorer
#     → chọn app của anh (chưa có thì bấm Tạo ứng dụng, loại Doanh nghiệp)
#     → Permissions, thêm: ads_management, business_management, pages_show_list
#     → bấm Generate Access Token, đăng nhập, copy chuỗi dài
#
#   Cách bền, dùng mãi:
#     business.facebook.com → Cài đặt doanh nghiệp → Người dùng → Người dùng hệ thống
#     → Thêm → cấp quyền Quản lý cho tài khoản quảng cáo và Trang
#     → Tạo mã truy cập mới, tick ads_management + business_management
#
# FB_ACT — Mã tài khoản quảng cáo
#   Nằm ngay trên thanh địa chỉ Ads Manager, đoạn act=XXXXXXXXXXX
#
# FB_PAGE — Mã Trang
#   Vào Trang DiLiM Supplement → Giới thiệu → kéo xuống cuối, mục ID Trang
#
# FB_PIXEL — Mã Pixel
#   business.facebook.com → Trình quản lý sự kiện → chọn pixel
#   → thanh địa chỉ, đoạn /dataset/XXXXXXXXXXX/
#   KHÔNG phải mã tài khoản quảng cáo. Hai số này luôn khác nhau.
