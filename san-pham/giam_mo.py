# -*- coding: utf-8 -*-
"""Hồ sơ sản phẩm: Viên Uống Giảm Mỡ AFC Ellagic Acid — Nhật Bản — 60 viên.

CHƯA CHẠY ĐƯỢC. Mọi ô ghi CAN_DIEN bên dưới phải điền từ NGUỒN THẬT trước:
ảnh nhãn phụ, giấy tiếp nhận công bố, bảng giá anh Sơn chốt.

Chương trình sẽ TỰ DỪNG và liệt kê ô còn thiếu — cố ý như vậy.
Bịa một số công bố hay một công dụng lên quảng cáo là khách tra ra không khớp,
Facebook gỡ bài, và mất uy tín cả tên miền chứ không riêng sản phẩm này.
"""

TEN_CD    = "Giam mo · T9 · Tiep can moi"
LINK      = "https://sonsongkhoe.com/giam-mo/"
ANH_QC    = "quang-cao/anh/giam-mo-vuong.jpg"

# Ngân sách: KHÔNG đặt bừa. Tính ngược từ giá thật đo được của Q10 trên cùng
# tài khoản, cùng Pixel, cùng tên miền — 849đ mỗi lượt xem trang đích (28/08).
# Giảm mỡ là ngách khác nên giá sẽ lệch, nhưng đây là điểm khởi đầu có cơ sở
# thay vì bốc một con số.
#     mốc quyết định : 1.000 lượt xem
#     tiền cần       : 1.000 x 849đ = 849.000đ
#     chia 4 ngày    : 212.250đ  ->  làm tròn 210.000đ
NGAN_SACH = 210000

KHUYEN_CAO = "Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."

# Số công bố: chép NGUYÊN VĂN từ giấy tiếp nhận, không nhớ lại, không suy ra.
SO_CONG_BO = "CAN_DIEN: số giấy tiếp nhận đăng ký bản công bố sản phẩm, chép từ ảnh giấy gốc"

# Công dụng: chỉ được dùng ĐÚNG câu ghi trên nhãn phụ. Không diễn giải,
# không thêm tính từ, không hứa giảm bao nhiêu cân trong bao nhiêu ngày.
CONG_DUNG = "CAN_DIEN: công dụng chép nguyên văn từ nhãn phụ tiếng Việt"

QUY_CACH  = "CAN_DIEN: quy cách đóng gói ghi trên nhãn, ví dụ 'Hộp 60 viên'"
CACH_DUNG = "CAN_DIEN: cách dùng ghi trên nhãn, ví dụ 'Ngày 2 viên sau bữa ăn'"
TIEN_COC  = "CAN_DIEN: tiền cọc giữ hàng, đồng"

NHOM = [
    {
        "ten":  "Nhom 1 · nu 30-45",
        "tuoi": (30, 45),
        "chu": (
            "CAN_DIEN: lời quảng cáo cho nhóm nữ 30-45.\n"
            "Viết theo đúng khuôn đã chạy được của Q10: mở bằng MỘT tình huống"
            " khách tự nhận ra mình, không mở bằng lời khen sản phẩm.\n"
            "Nêu tên đầy đủ và xuất xứ. Nêu công dụng ĐÚNG CÂU TRÊN NHÃN.\n"
            "Kết bằng một việc nhẹ để bấm vào, không phải 'mua ngay'.\n"
            "KHÔNG hứa số cân, KHÔNG hứa số ngày, KHÔNG ảnh trước-sau.\n"
            "Kết thúc bằng câu khuyến cáo."
        ),
        "tieu_de": "CAN_DIEN: tiêu đề dưới ảnh, tối đa 40 ký tự",
        "mo_ta":   "CAN_DIEN: mô tả một dòng, nêu xuất xứ và số công bố",
    },
    {
        "ten":  "Nhom 2 · nu 45-60",
        "tuoi": (45, 60),
        "chu":     "CAN_DIEN: lời quảng cáo cho nhóm nữ 45-60",
        "tieu_de": "CAN_DIEN: tiêu đề dưới ảnh",
        "mo_ta":   "CAN_DIEN: mô tả một dòng",
    },
    {
        "ten":  "Nhom 3 · nam 30-50",
        "tuoi": (30, 50),
        "chu":     "CAN_DIEN: lời quảng cáo cho nhóm nam 30-50",
        "tieu_de": "CAN_DIEN: tiêu đề dưới ảnh",
        "mo_ta":   "CAN_DIEN: mô tả một dòng",
    },
]
