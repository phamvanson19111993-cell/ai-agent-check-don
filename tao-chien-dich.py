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

CÁCH CHẠY — không cần sửa gì trong file này
  1. pip install requests
  2. python3 tao-chien-dich.py
  3. Chương trình hỏi bốn số, dán vào từng cái rồi Enter

Ai muốn khỏi gõ lại mỗi lần thì điền sẵn vào khối CẦN ĐIỀN bên dưới,
hoặc đặt biến môi trường FB_TOKEN, FB_ACT, FB_PAGE, FB_PIXEL.

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

TOKEN      = os.environ.get("FB_TOKEN", "")                   # Mã truy cập, chuỗi rất dài
TAI_KHOAN  = os.environ.get("FB_ACT",   "2260044828113956")   # Pham Son BM1.1 — BM cua anh
TRANG      = os.environ.get("FB_PAGE",  "61592861334561")     # Trang DiLiM Supplement
PIXEL      = os.environ.get("FB_PIXEL", "1277743445418211")   # Pixel đang gắn trên sonsongkhoe.com

# ── HỒ SƠ SẢN PHẨM ──────────────────────────────────────────────
# Cấu hình từng sản phẩm nằm trong thư mục san-pham/, không nằm ở đây nữa.
# Thêm sản phẩm mới thì thêm một file vào đó, KHÔNG sửa file này.
#
#     python3 tao-chien-dich.py                    -> Q10 (mặc định)
#     python3 tao-chien-dich.py --san-pham giam-mo -> giảm mỡ
#     python3 tao-chien-dich.py --san-pham q10
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import importlib.util as _iu

def _nap_ho_so(ten):
    thu_muc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'san-pham')
    duong = os.path.join(thu_muc, ten.replace('-', '_') + '.py')
    if not os.path.exists(duong):
        co = sorted(f[:-3].replace('_', '-') for f in os.listdir(thu_muc)
                    if f.endswith('.py') and not f.startswith('__'))
        sys.exit("Khong co ho so san pham '%s'. Dang co: %s" % (ten, ', '.join(co)))
    spec = _iu.spec_from_file_location('sp_' + ten.replace('-', '_'), duong)
    m = _iu.module_from_spec(spec); spec.loader.exec_module(m)
    for k in ('TEN_CD', 'LINK', 'NGAN_SACH', 'ANH_QC', 'NHOM'):
        if not hasattr(m, k):
            sys.exit("Ho so %s thieu bien bat buoc: %s" % (duong, k))
    # O nao con de CAN_DIEN thi DUNG HAN — khong dang quang cao voi cau bia.
    thieu = []
    def di(gt, ten_o):
        if isinstance(gt, str):
            if gt.strip().startswith('CAN_DIEN'):
                thieu.append('%s\n       %s' % (ten_o, gt.strip().split(chr(10))[0]))
        elif isinstance(gt, dict):
            for k2, v in gt.items(): di(v, '%s[%r]' % (ten_o, k2))
        elif isinstance(gt, (list, tuple)):
            for i2, v in enumerate(gt): di(v, '%s[%d]' % (ten_o, i2))
    for k in dir(m):
        if not k.startswith('_'): di(getattr(m, k), k)
    if thieu:
        print("\nKHONG CHAY DUOC — ho so '%s' con %d o chua dien:\n" % (ten, len(thieu)))
        for d in thieu: print("   -", d)
        print("\nDien vao: %s" % duong)
        print("\nTUYET DOI khong tu bia so cong bo, gia, hay cong dung.")
        print("Khach tra ra khong khop la Facebook go bai va mat uy tin ca ten mien.")
        sys.exit(1)
    return m

_TEN_SP = 'q10'
if '--san-pham' in sys.argv:
    _TEN_SP = sys.argv[sys.argv.index('--san-pham') + 1]
_HS = _nap_ho_so(_TEN_SP)

ANH_QC     = _HS.ANH_QC
LINK       = _HS.LINK
NGAN_SACH  = _HS.NGAN_SACH
TEN_CD     = _HS.TEN_CD
NHOM       = _HS.NHOM

# --nhom 1      -> chi dung Nhom 1
# --nhom 1,3    -> dung Nhom 1 va Nhom 3
# khong ghi     -> dung het, y nhu truoc
#
# De chay thu mot nhom cho re thi dung co tao ca ba roi chi bat mot. Tao ba
# nhom la ba cai cong tac nam san do; gat nham mot cai la ngan sach nhan ba.
# Chay lai lenh nay voi --nhom 2 thi no TIM LAI chien dich cu theo ten va
# them nhom moi vao do, khong dung them mot chien dich trung ten.
def _chon_nhom(tat_ca):
    if '--nhom' not in sys.argv:
        return tat_ca
    tho = sys.argv[sys.argv.index('--nhom') + 1]
    try:
        so = [int(x) for x in tho.replace(' ', '').split(',') if x]
    except ValueError:
        sys.exit("--nhom phai la so, vi du: --nhom 1  hoac  --nhom 1,3")
    xau = [n for n in so if not 1 <= n <= len(tat_ca)]
    if xau:
        sys.exit("Ho so '%s' chi co %d nhom, khong co nhom %s"
                 % (_TEN_SP, len(tat_ca), ', '.join(str(n) for n in xau)))
    return [tat_ca[n - 1] for n in so]

NHOM = _chon_nhom(NHOM)
# ────────────────────────────────────────────────────────────────

def goi(duong_dan, du_lieu=None, tep=None, lay=False):
    """Gọi một lệnh tới Facebook. Dừng hẳn nếu Facebook báo lỗi."""
    url = "%s/%s" % (API, duong_dan)
    try:
        return _goi(url, du_lieu, tep, lay)
    except requests.exceptions.SSLError:
        sys.exit("Lỗi chứng chỉ bảo mật khi nối tới Facebook. Mạng công ty hoặc phần mềm "
                 "diệt virus có thể đang chặn. Thử mạng khác, hoặc tắt tạm phần mềm chặn.")
    except requests.exceptions.ConnectionError:
        sys.exit("Không nối được tới Facebook. Kiểm tra mạng, rồi thử mở "
                 "graph.facebook.com trên trình duyệt xem có vào được không.")
    except requests.exceptions.Timeout:
        sys.exit("Facebook trả lời quá chậm, quá thời gian chờ. Chạy lại lệnh một lần nữa.")


def _goi(url, du_lieu, tep, lay):
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


def hoi(nhac, goi_y="", kin=False):
    """Hỏi một giá trị ngay trên màn hình, khỏi phải mở file ra sửa."""
    while True:
        if kin:
            import getpass
            v = getpass.getpass(nhac).strip()
        else:
            v = input(nhac).strip()
        if not v and goi_y:
            return goi_y
        if v:
            return v
        print("  Chưa nhập gì. Thử lại, hoặc Ctrl+C để thoát.")


ANH_TREN_MANG = "https://sonsongkhoe.com/images/qc-vuong.jpg"


def lay_anh_ve():
    """Không có ảnh trong máy thì tự tải từ trang web về, khỏi phải tạo thư mục."""
    print("Không thấy %s — đang tải ảnh quảng cáo từ sonsongkhoe.com…" % ANH_QC)
    try:
        r = requests.get(ANH_TREN_MANG, timeout=60)
        r.raise_for_status()
    except Exception as e:
        sys.exit("Tải ảnh không được (%s).\nAnh tải tay ảnh qc-vuong.jpg rồi để cạnh file này, "
                 "và sửa dòng ANH_QC thành \"qc-vuong.jpg\"." % e)
    thu_muc = os.path.dirname(ANH_QC)
    if thu_muc:
        os.makedirs(thu_muc, exist_ok=True)
    with open(ANH_QC, "wb") as f:
        f.write(r.content)
    print("Đã tải xong ảnh, %d KB" % (len(r.content) // 1024))


def kiem_tra_dau_vao():
    """Thiếu số nào thì hỏi ngay, không bắt người dùng mở file."""
    global TOKEN, TAI_KHOAN, TRANG, PIXEL

    if not (TOKEN and TAI_KHOAN and TRANG and PIXEL):
        print("""
╭────────────────────────────────────────────────────────────╮
│  Ba số đã điền sẵn. Thiếu số nào chương trình hỏi bên dưới.│
│  Cách lấy từng số nằm ở cuối file này.                     │
╰────────────────────────────────────────────────────────────╯""")

    if not TOKEN:
        print("\nMã token — dán vào rồi Enter. Chữ sẽ KHÔNG hiện lên màn hình,")
        print("đó là bình thường, cứ dán rồi Enter.")
        TOKEN = hoi("  Token: ", kin=True)
    if not TAI_KHOAN:
        print("\nMã tài khoản quảng cáo — dãy số sau chữ act= trên thanh địa chỉ.")
        TAI_KHOAN = hoi("  Mã tài khoản: ")
    if not TRANG:
        print("\nMã Trang — Enter luôn để dùng 61592861334561 (lấy từ link Messenger).")
        TRANG = hoi("  Mã Trang [61592861334561]: ", goi_y="61592861334561")
    if not PIXEL:
        print("\nMã Pixel — dãy số sau /dataset/ trong Trình quản lý sự kiện.")
        print("KHÔNG phải mã tài khoản quảng cáo.")
        PIXEL = hoi("  Mã Pixel: ")

    for ten, v in (("Mã tài khoản", TAI_KHOAN), ("Mã Trang", TRANG), ("Mã Pixel", PIXEL)):
        if not v.isdigit():
            sys.exit("%s phải là dãy số, anh vừa nhập: %r" % (ten, v))

    if TAI_KHOAN == PIXEL:
        sys.exit("Mã tài khoản và mã Pixel đang giống hệt nhau. Một trong hai đang sai.\n"
                 "Mã Pixel lấy ở Trình quản lý sự kiện, trong URL đoạn /dataset/<mã>/")

    if not os.path.exists(ANH_QC):
        lay_anh_ve()


def lo_pixel(act):
    """Kiem tra Pixel co dung duoc khong. Khong dung duoc thi tu tao cai moi."""
    global PIXEL
    if PIXEL:
        r = requests.get("%s/%s" % (API, PIXEL),
                         params={"fields": "name", "access_token": TOKEN}, timeout=60)
        if "error" not in r.json():
            print("Pixel     : %s · %s" % (PIXEL, r.json().get("name", "")))
            return
        print("Pixel %s khong dung duoc voi tai khoan nay." % PIXEL)

    print("Dang tao Pixel moi ten \"DiLiM Q10\"…")
    kq = goi("%s/adspixels" % act, {"name": "DiLiM Q10"})
    PIXEL = kq["id"]
    print("""
╭────────────────────────────────────────────────────────────╮
│  ĐÃ TẠO PIXEL MỚI                                          │
│                                                            │
│     %-54s│
│                                                            │
│  GỬI DÃY SỐ NÀY CHO CLAUDE để gắn lên sonsongkhoe.com.     │
│  Chưa gắn thì quảng cáo chạy mà không đếm được đơn nào.    │
╰────────────────────────────────────────────────────────────╯
""" % PIXEL)


def main():
    kiem_tra_dau_vao()
    act = "act_%s" % TAI_KHOAN.replace("act_", "")

    # Xem tài khoản có sống không, và tiêu bằng tiền gì
    tk = goi(act, {"fields": "name,currency,account_status,disable_reason,"
                             "spend_cap,amount_spent"}, lay=True)
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

    # Giới hạn chi tiêu tài khoản — chỗ này đã chặn đứng chiến dịch Q10 ngày
    # 29/08 ("Đã đạt giới hạn chi tiêu"). Dựng chiến dịch mới trên một tài khoản
    # đang đụng trần thì bật lên nó vẫn nằm im, mà nhìn thì tưởng ads kém.
    tran = tk.get("spend_cap")
    da_tieu = tk.get("amount_spent")
    if tran and str(tran) != "0":
        tran, da_tieu = int(tran), int(da_tieu or 0)
        con = tran - da_tieu
        print("Giới hạn  : %s đ · đã tiêu %s đ · còn %s đ"
              % (format(tran, ","), format(da_tieu, ","), format(con, ",")))
        if con <= 0:
            print("""
╭────────────────────────────────────────────────────────────╮
│  TÀI KHOẢN ĐÃ ĐỤNG TRẦN CHI TIÊU — dựng xong cũng không   │
│  chạy được đồng nào.                                       │
│                                                            │
│  Sửa trước: Ads Manager → Cài đặt thanh toán →            │
│  Giới hạn chi tiêu tài khoản → tăng hạn mức, hoặc          │
│  Đặt lại số tiền đã chi.                                   │
╰────────────────────────────────────────────────────────────╯""")
            if input("Vẫn dựng chiến dịch để sẵn đó? (co/khong): ").strip().lower() \
                    not in ("co", "có", "c", "y", "yes"):
                sys.exit("Dung lai. Nang tran chi tieu roi chay lai lenh nay.")
        elif con < NGAN_SACH * len(NHOM):
            print("!! Chỗ còn lại (%s đ) không đủ một ngày ngân sách (%s đ)."
                  % (format(con, ","), format(NGAN_SACH * len(NHOM), ",")))

    lo_pixel(act)

    # Ảnh dùng chung cho ba mẫu
    with open(ANH_QC, "rb") as f:
        anh = goi("%s/adimages" % act, tep={"file": (os.path.basename(ANH_QC), f)})
    ma_anh = list(anh["images"].values())[0]["hash"]
    print("Ảnh       : đã tải lên")

    # Tầng 1 — chiến dịch.
    # Tìm lại theo tên trước đã. Chạy lệnh này lần hai với --nhom 2 thì nhóm
    # mới phải rơi vào ĐÚNG chiến dịch cũ, không dựng thêm một cái trùng tên —
    # hai chiến dịch cùng tên là ba ngày sau không ai đọc nổi số liệu.
    cu = goi("%s/campaigns" % act,
             {"fields": "id,name,status", "limit": 200}, lay=True).get("data", [])
    trung = [c for c in cu if c.get("name") == TEN_CD]
    if trung:
        cd = trung[0]
        print("\nChiến dịch: %s  (%s) — DÙNG LẠI cái đã có, không tạo trùng"
              % (TEN_CD, cd["id"]))
        if len(trung) > 1:
            print("!! Đang có %d chiến dịch trùng tên này. Vào Ads Manager xoá bớt."
                  % len(trung))
    else:
        cd = goi("%s/campaigns" % act, {
            "name": TEN_CD,
            "objective": "OUTCOME_SALES",
            "status": "PAUSED",
            "special_ad_categories": json.dumps([]),
        })
        print("\nChiến dịch: %s  (%s) — tạo mới" % (TEN_CD, cd["id"]))

    # Nhóm nào đã dựng rồi thì bỏ qua, khỏi tiêu tiền hai lần cho một đối tượng.
    da_co = {a.get("name") for a in
             goi("%s/adsets" % act, {"fields": "name", "limit": 200},
                 lay=True).get("data", [])}

    dung = 0
    for n in NHOM:
        tuoi_min, tuoi_max = n["tuoi"]

        if n["ten"] in da_co:
            print("  %-24s đã có sẵn, bỏ qua" % n["ten"])
            continue

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

        dung += 1
        print("  %-24s tuổi %2d–%2d  %s đ/ngày   nhóm %s"
              % (n["ten"], tuoi_min, tuoi_max, format(NGAN_SACH, ","), nhom["id"]))

    print("""
╭────────────────────────────────────────────────────────────╮
│  XONG. Mọi thứ đang TẠM DỪNG, chưa tiêu đồng nào.          │
│                                                            │
│  Việc còn lại của anh:                                     │
│   1. Mở Ads Manager, xem lại mẫu quảng cáo                 │
│   2. Thay ảnh bằng video nếu đã quay xong                  │
│   3. Gạt nút bật ĐỦ BA TẦNG: chiến dịch, nhóm, quảng cáo. │
│      Thiếu một tầng là không đồng nào chạy, mà nhìn trên   │
│      Ads Manager lại tưởng đã bật rồi.                     │
╰────────────────────────────────────────────────────────────╯""")
    print("Vừa dựng %d nhóm. Bật hết số nhóm đó là tiêu %s đ mỗi ngày.\n"
          % (dung, format(NGAN_SACH * dung, ",")))
    print("Pixel dang dung: %s" % PIXEL)
    print("Neu so nay khac voi so tren web thi bao Claude doi lai.\n")


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
