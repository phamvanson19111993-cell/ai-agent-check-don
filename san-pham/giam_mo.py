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
        # Anh Sơn chốt 35–55 (đi qua 30–45 rồi 30–55).
        "ten":  "Nhom 1 · nu 35-55",
        "tuoi": (35, 55),
        "gioi": 2,          # 2 = nữ. Lời quảng cáo xưng "chị" nên phải khoá lại.
        # Viết theo Ogilvy và Kotler. Bốn thứ mượn của hai ông:
        #
        # 1. Ogilvy: "Nếu tiêu đề có giá, nhiều người đọc hơn." Giá lọc khách
        #    chứ không đuổi khách. Người bỏ đi khi thấy giá thì không có giá
        #    họ cũng bỏ đi — chỉ khác là mình đã trả tiền cho cú bấm đó rồi.
        # 2. Ogilvy: con số cụ thể thắng tính từ. Không "hiệu quả vượt trội",
        #    mà "159mg chiết xuất, 1,5mg axit ellagic, một túi 60 viên đủ 30 ngày".
        # 3. Kotler — khung tham chiếu: khách không định giá tuyệt đối, khách
        #    so với thứ gần nhất trong đầu. 675.000đ đứng cạnh "một lần đi chợ";
        #    22.500đ đứng cạnh "cốc cà phê". Cùng số tiền, khác cỡ quyết định.
        # 4. Kotler — đảo ngược rủi ro: nói trước phần bất lợi cho mình, và
        #    hạ mức phải làm xuống còn "đọc trang", không phải "để lại số".
        #
        # Ràng buộc không được vượt: giấy 1581/2024/XNQC-ATTP chỉ cho một câu
        # công dụng. Nên lực kéo phải đến từ con số thật và sự thành thật,
        # không đến từ lời hứa kết quả.
        "chu": (
            "Cái quần năm ngoái vẫn kéo lên được. Chỉ là lúc cài cúc phải hóp "
            "bụng vào một cái.\n\n"
            "Nhiều chị 35–55 kể lại đúng chuyện đó: cân nặng nhích lên chậm tới mức "
            "không ai để ý, tới lúc để ý thì là cái quần nhắc chứ không phải cái cân.\n\n"
            "Đây là thứ bên em bán. Nói bằng con số, không nói bằng lời hứa:\n\n"
            "• ELLAGIC ACID của AFC Nhật Bản, sản xuất tại nhà máy AFC-HD AMS "
            "Life Science ở Shizuoka\n"
            "• Mỗi viên 159mg chiết xuất xoài châu Phi (Irvingia gabonensis), "
            "trong đó 1,5mg axit ellagic\n"
            "• Ngày 2 viên với nước. Một túi nhôm 60 viên dùng đúng 30 ngày\n"
            "• 675.000đ một túi — tính ra 22.500đ mỗi ngày, chưa bằng một cốc "
            "cà phê ngoài quán\n"
            "• Công dụng ghi trên nhãn: hỗ trợ giảm béo. Đúng một câu đó, "
            "bên em không nói thêm câu nào\n"
            "• Số tiếp nhận công bố 3993/2024/ĐKSP — gõ số này lên cổng Cục An "
            "toàn thực phẩm là ra hồ sơ, không cần tin lời bên em\n\n"
            "Bên em không nói chị sẽ xuống mấy cân trong mấy ngày. Ai nói được "
            "câu đó là họ đang nói liều.\n\n"
            "Và nói luôn phần bất lợi cho bên em: sản phẩm không dùng cho phụ nữ "
            "có thai, phụ nữ đang cho con bú, và người đang có bệnh.\n\n"
            "Bấm xem trang trước đã — trong đó có ảnh chụp hai giấy tờ gốc, bản "
            "chép nguyên văn nhãn phụ, và bảng giá đủ bốn mốc. Đọc xong thấy hợp "
            "thì hẵng để lại số. Không phải để lại số mới được xem."
            + _CUOI_BAI
        ),
        # Ogilvy: tiêu đề ăn 80% số tiền, và tiêu đề có giá thì nhiều người đọc hơn.
        "tieu_de": "22.500đ mỗi ngày · Hỗ trợ giảm béo",
        "mo_ta":   "AFC Nhật Bản · túi nhôm 60 viên dùng 30 ngày · công bố 3993/2024/ĐKSP",
    },
    {
        # Đẩy lên 56–65 để KHÔNG chồng lấn với Nhóm 1 vừa mở rộng tới 55.
        # Hai nhóm cùng nhắm một người là mình tự đấu giá với chính mình,
        # đội giá lên mà vẫn ngần ấy người.
        "ten":  "Nhom 2 · nu 56-65",
        "tuoi": (56, 65),
        "gioi": 2,
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
        "gioi": 1,          # 1 = nam
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
