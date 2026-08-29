# -*- coding: utf-8 -*-
"""Hồ sơ sản phẩm: Thực phẩm bảo vệ sức khỏe ELLAGIC ACID — AFC Nhật Bản — túi nhôm 60 viên.

ĐÃ ĐIỀN XONG 29/08/2026. Nguồn của từng ô:
  · Giấy tiếp nhận đăng ký bản công bố sản phẩm số 3993/2024/ĐKSP  (ảnh gốc anh Sơn gửi)
  · Giấy xác nhận nội dung quảng cáo số 1581/2024/XNQC-ATTP        (ảnh gốc anh Sơn gửi)
  · Nhãn phụ tiếng Việt / bản công bố, mã hồ sơ 23.11.10.278248.DKCB
  · Bảng giá niêm yết 2026 anh Sơn chốt

LUẬT TỰ ĐẶT CHO FILE NÀY — đừng nới ra:
  Giấy 1581/2024/XNQC-ATTP chỉ cho phép nói MỘT câu công dụng: "Hỗ trợ giảm béo."
  Không "giảm mỡ nội tạng", không "giảm vòng eo", không số cân, không số ngày,
  không ảnh trước–sau, không "cam kết". Quảng cáo vượt nội dung đã xác nhận là
  vi phạm Nghị định 15/2018 — và giảm cân là nhóm bị soi gắt nhất.
  Meta cũng cấm câu ám chỉ thẳng vào thân thể người xem ("bạn đang béo phải không").
"""

TEN_CD    = "Giam mo · Ellagic Acid · Vong 1 · 2908"
LINK      = "https://sonsongkhoe.com/giam-mo/"
ANH_QC    = "quang-cao/anh/giam-mo-vuong.jpg"

# Ngân sách MỖI NHÓM, mỗi ngày. Anh Sơn chốt 300.000đ cho một bài.
#
# CẢNH BÁO ĐỌC KỸ: chương trình dựng 3 nhóm. Bật cả 3 là 900.000đ/ngày.
# SOP Phòng 7 mục 2A nói rõ: ngân sách test dưới ~1 triệu/ngày thì chỉ nên
# chạy MỘT nhóm, vì chia nhỏ ra thì không nhóm nào đủ số để kết luận.
# Đề xuất: bật Nhóm 1 trước, 300.000đ/ngày, chạy 3 ngày không đụng vào.
#
# Đối chiếu để biết 300.000đ mua được gì: Q10 trên cùng tài khoản, cùng Pixel,
# cùng tên miền đo được 849đ mỗi lượt xem trang đích (28/08).
#     300.000đ / 849đ  ≈  353 lượt xem mỗi ngày
#     3 ngày           ≈  1.060 lượt  — vừa đủ mốc quyết định 1.000 lượt
# Giảm béo là ngách khác nên giá sẽ lệch; đây là điểm khởi đầu có cơ sở,
# không phải con số bốc ra.
NGAN_SACH = 300000

KHUYEN_CAO = "Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."

# Chép nguyên văn từ giấy tiếp nhận công bố.
SO_CONG_BO = "3993/2024/ĐKSP — Cục An toàn thực phẩm cấp ngày 05/05/2024 cho Công ty Cổ phần 5SPRO"

# Chép nguyên văn từ nhãn phụ. MỘT câu, không thêm chữ nào.
CONG_DUNG = "Hỗ trợ giảm béo."

QUY_CACH  = "Túi nhôm 60 viên"
CACH_DUNG = "Uống 2 viên mỗi ngày với nước."
TIEN_COC  = 0   # Trang đã bỏ chuyển khoản, khách trả khi nhận hàng (COD). Không thu cọc.

# Ba dòng bắt buộc dán cuối mọi mẫu quảng cáo. Bỏ một dòng là bài sai luật.
_CUOI_BAI = (
    "\n\nĐối tượng sử dụng: người lớn từ 18 tuổi trở lên béo phì, người muốn giảm béo.\n"
    "Không dùng cho phụ nữ có thai, phụ nữ cho con bú và người đang có bệnh.\n"
    "Hiệu quả tuỳ thuộc cơ địa từng người.\n"
    + KHUYEN_CAO
)

# Khối giấy tờ, dán vào giữa bài — đây là thứ tách bài này khỏi hàng xách tay.
_GIAY_TO = (
    "Thực phẩm bảo vệ sức khỏe ELLAGIC ACID — AFC Nhật Bản, sản xuất tại "
    "AFC-HD AMS Life Science, Shizuoka. Mỗi viên chứa 159mg chiết xuất xoài "
    "châu Phi (Irvingia gabonensis). Công dụng ghi trên nhãn: hỗ trợ giảm béo.\n"
    "Số tiếp nhận công bố 3993/2024/ĐKSP — gõ số này lên cổng Cục An toàn "
    "thực phẩm là ra hồ sơ, không cần tin lời bên em."
)

NHOM = [
    {
        "ten":  "Nhom 1 · nu 30-45",
        "tuoi": (30, 45),
        "chu": (
            "Cái quần năm ngoái vẫn kéo lên được. Chỉ là lúc cài cúc phải hóp "
            "bụng vào một cái.\n\n"
            "Nhiều chị 30–45 kể lại đúng chuyện đó: cân nặng nhích lên chậm tới mức "
            "không ai để ý, tới lúc để ý thì là cái quần nhắc chứ không phải cái cân.\n\n"
            + _GIAY_TO + "\n\n"
            "Uống 2 viên mỗi ngày với nước. Túi nhôm 60 viên, chia ra dùng được 30 ngày.\n\n"
            "Bên em không hứa chị xuống bao nhiêu cân trong bao nhiêu ngày — "
            "cái đó không ai hứa thật được. Bấm xem trang để đọc nhãn, thành phần "
            "và bảng giá trước đã, thấy hợp thì hẵng để lại số."
            + _CUOI_BAI
        ),
        "tieu_de": "Hỗ trợ giảm béo — AFC Nhật Bản",
        "mo_ta":   "Túi nhôm 60 viên · công bố 3993/2024/ĐKSP · xem nhãn và giá trước khi mua",
    },
    {
        "ten":  "Nhom 2 · nu 45-60",
        "tuoi": (45, 60),
        "chu": (
            "Ăn vẫn bằng ngần ấy, đi bộ vẫn ngần ấy vòng, mà cái cân thì không "
            "chịu đi xuống như hồi bốn mươi.\n\n"
            "Nhiều cô ở tuổi này nói cùng một câu. Không phải tại cô lười.\n\n"
            + _GIAY_TO + "\n\n"
            "Uống 2 viên mỗi ngày với nước. Túi nhôm 60 viên, dùng 30 ngày.\n\n"
            "Bên em nói trước phần bất lợi cho mình: nhãn ghi rõ sản phẩm không "
            "dùng cho phụ nữ có thai, đang cho con bú và người đang có bệnh. "
            "Cô chú đang uống thuốc theo đơn thì hỏi bác sĩ trước, đừng vội mua.\n\n"
            "Bấm xem trang để đọc nhãn và bảng giá."
            + _CUOI_BAI
        ),
        "tieu_de": "Nói thật: ai không nên dùng",
        "mo_ta":   "ELLAGIC ACID · AFC Nhật Bản · công bố 3993/2024/ĐKSP · đọc nhãn trước",
    },
    {
        "ten":  "Nhom 3 · nam 30-50",
        "tuoi": (30, 50),
        "chu": (
            "Thắt lưng vẫn cái cũ, chỉ là dịch sang lỗ tiếp theo lúc nào không nhớ.\n\n"
            "Ngồi tám tiếng, bữa trưa ăn vội, tối mới rảnh để ăn cho ra bữa — "
            "nhiều anh 30–50 sống đúng lịch đó suốt mấy năm.\n\n"
            "Ba việc không mất đồng nào, làm trước đã: cứ 45 phút đứng dậy đi 3 phút, "
            "ăn trưa tử tế thay vì để dồn vào bữa tối, ngủ đủ.\n\n"
            + _GIAY_TO + "\n\n"
            "Uống 2 viên mỗi ngày với nước. Túi nhôm 60 viên, dùng 30 ngày.\n\n"
            "Muốn xem nhãn, thành phần và giá thì bấm vào trang. Không phải để lại "
            "số mới xem được."
            + _CUOI_BAI
        ),
        "tieu_de": "Hỗ trợ giảm béo — xem nhãn và giá",
        "mo_ta":   "ELLAGIC ACID · AFC Nhật Bản · túi 60 viên · công bố 3993/2024/ĐKSP",
    },
]
