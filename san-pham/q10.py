# -*- coding: utf-8 -*-
"""Hồ sơ sản phẩm: Rich Coenzyme Q10 — bản đang chạy thật.

Số liệu trong đây đã chạy quảng cáo có tiền thật, đừng sửa nếu không có lý do.
"""

ANH_QC     = "qc-vuong.jpg"                     # Tự tải về nếu chưa có
LINK       = "https://sonsongkhoe.com"
# NGÂN SÁCH — sửa 28/08/2026, số cũ 150.000đ là em đặt bừa khi chưa có dữ liệu.
# Số mới tính ngược từ giá thật đo được ngày 27/08: 954đ mỗi lượt xem trang đích
# (224.227đ chia cho 235 lượt, tài khoản 2260044828113956).
#   Mốc quyết định  : 1.000 lượt xem → đủ để biết trang có chốt được không
#   Tiền cần        : 1.000 x 954đ = 954.157đ
#   Chia 5 ngày     : 190.831đ mỗi ngày → làm tròn 190.000đ
# Chạy chậm hơn 5 ngày thì thị trường và mùa vụ đổi, số đo mất nghĩa.
# Chạy nhanh hơn 3 ngày thì Meta chưa kịp thoát giai đoạn học.
NGAN_SACH  = 190000                             # đồng mỗi ngày, cho cả đợt thử
TEN_CD     = "Q10 · T9 · Tiếp cận mới"

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
