# BÁO CÁO GẤP — OCR ảnh trên Drive KHÔNG đọc được
Phòng 7 · 28/08/2026 · gửi Tổng Chỉ Huy và Phòng check trùng đơn

---

## Việc đã làm

Phòng 7 định dựng đường lấy số quảng cáo giống bot check trùng đơn: anh Sơn chụp
màn hình Ads Manager, thả vào một thư mục Drive, Phòng 7 quét mỗi giờ và đọc chữ
trong ảnh bằng OCR của Drive.

Đã tạo thư mục `📊 ẢNH ADS Q10` (id `1DoUc_PgDo58ZSkpCWYoaTVTHtUFoTsCm`).

## Đã thử hai cách, CẢ HAI ĐỀU RỖNG

Ảnh thử: PNG 760×250, nền trắng, chữ đen nét sắc, 8 màu phẳng — dạng dễ đọc nhất
có thể. Nội dung mô phỏng đúng bảng Ads Manager: `109` · `1.018 đ` · `300.000 đ` ·
`111.014 đ` · `5.000` · `3.557`.

| Cách | File tạo ra | `read_file_content` trả về |
|---|---|---|
| Tải lên giữ nguyên PNG (`disableConversionToGoogleType: true`) | `1XUdzbHjuvorNx3uDOaSz_19gTNnQ1EIO` · 3.501 byte | **rỗng** |
| Tải lên cho Drive tự chuyển thành Google Docs | `1xDx3K3Qom-3uZA5OITaRk3-w58CmDYKu_t6WYcKpNnc` · **1 byte** | **rỗng** |

Cách thứ hai đáng chú ý: Drive **có** chuyển sang Google Docs, nhưng tài liệu sinh
ra chỉ **1 byte** — tức là không rút được chữ nào từ ảnh.

## Kết luận

**Bộ công cụ Drive của Phòng 7 không lấy được chữ trong ảnh.** Ảnh càng rõ cũng
không đọc được — không phải do ảnh mờ.

Nhiều khả năng vì tham số bật OCR (`ocrLanguage`, `useContentAsIndexableText`)
không có trong công cụ này.

## ⚠️ CẦN PHÒNG CHECK TRÙNG ĐƠN KIỂM LẠI

Lệnh của bot check trùng đơn ghi: *"đọc nội dung bằng read_file_content (Drive tự
OCR chữ trong ảnh), tách số điện thoại Việt Nam"*.

Phòng 7 **không kết luận bot đó hỏng** — phiên khác có thể có công cụ khác. Nhưng
nếu nó cũng dùng đúng công cụ này thì rất nên kiểm: thả một ảnh mới vào thư mục
`1ctoaGLopCU0UIlSZQlpNjX6sZppkR5Td` rồi xem có tách được số điện thoại không.

Nếu cũng rỗng thì bot đó đang báo "không có số mới" mỗi giờ **không phải vì không
có ảnh mới, mà vì không đọc được ảnh nào cả.** Sai lặng lẽ, khó phát hiện.

## Phòng 7 chuyển sang cách nào

Ảnh **gửi thẳng trong khung chat thì đọc được bình thường** — Phòng 7 đã đọc chính
xác ảnh Ads Manager anh Sơn gửi nhiều lần hôm nay (109 lượt xem, 1.018đ, 111.014đ,
5.000 hiển thị, 3.557 tiếp cận).

Nên đổi: **anh Sơn chụp màn hình rồi gửi thẳng vào khung chat**, không thả Drive nữa.
Lịch mỗi giờ sẽ đọc ảnh từ lịch sử trò chuyện.

Thư mục Drive vẫn giữ lại, phòng khi sau này có công cụ OCR thật.

---

## Đã xử lý xong — 15h55

**1. Lịch mỗi giờ đã đổi.**
Routine `trig_01FD8wK6c2YRr71HHkoQJwc1`, đổi tên thành
*"Báo cáo Q10 mỗi giờ · đọc ảnh Ads gửi trong chat"*.
Bỏ hẳn bước quét thư mục Drive + `read_file_content` trên ảnh.
Thay bằng: đọc ảnh Ads Manager trong lịch sử trò chuyện của phiên.
Vẫn chạy phút 18 mỗi giờ, vẫn bám phiên `session_01NKVuC993sRBvHy3My1qzVp`.

Trong lệnh mới có ghi rõ lý do bỏ Drive, để lần sau không ai bật lại nhầm.

**2. Dọn thư mục Drive.**
- Bỏ vào thùng rác 2 file thử OCR (`2026-08-28-MAU-THU-OCR.png`, `THU-OCR-CHUYEN-DOI`)
- Bỏ file hướng dẫn cũ — nó bảo anh Sơn thả ảnh vào, mà đường đó không chạy
- Thêm file `ĐỌC TRƯỚC — đừng thả ảnh vào đây nữa.txt`
- Đổi tên thư mục thành `📊 ẢNH ADS Q10 (KHÔNG DÙNG — gửi ảnh thẳng trong chat)`

Thư mục vẫn còn, không xoá. Nhưng ai mở ra cũng thấy ngay là đừng thả vào.

**3. Việc còn lại của anh Sơn:** không có gì thêm.
Từ giờ chụp màn hình Ads Manager rồi gửi thẳng vào khung chat — hết.
