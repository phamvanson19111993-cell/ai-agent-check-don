# Nơi để đồ — tra trước khi báo "chưa có"

Viết ngày 30/08/2026 sau khi Phòng 7 báo sai suốt hai ngày rằng "chưa có bảng đơn".
Bảng vẫn luôn tồn tại; lỗi là tra Drive theo cái tên tự đoán.

**Quy tắc:** chưa tìm thấy thì ghi **"chưa tìm thấy"**, không ghi "chưa có".
Hai câu đó khác nhau, và cái sau làm anh Sơn đi bấm lại thứ đã có.

## Đơn hàng từ trang sonsongkhoe.com

| Thứ | Nơi để | Cách tìm |
|---|---|---|
| Bảng trả lời Biểu mẫu | Google Drive, tên **"Mẫu không có tiêu đề (Câu trả lời)"** | `search_files` với `mimeType = 'application/vnd.google-apps.spreadsheet' and owner = 'me'` rồi tìm tên có chữ **"Câu trả lời"** |
| Bảng "Lady Page" | Drive, rỗng | Là đích của Apps Script, mà Apps Script **chưa** triển khai. Rỗng ở đây **không** chứng minh không có đơn |
| Bản lưu trên máy khách | localStorage khoá `dilim-don-da-gui` | Mở `sonsongkhoe.com/#don-da-luu` trên chính máy đó |

Đừng tìm theo tên đoán sẵn. **Tìm theo loại tệp rồi đọc tên**, vì Biểu mẫu Google
đặt tên bảng theo tên Biểu mẫu, mà Biểu mẫu này chưa được đặt tên.

## Đọc bảng đơn thế nào cho đúng

- Biểu mẫu chỉ có **một câu hỏi**, nên cả đơn nằm gọn trong một ô. Đọc cả ô.
- **Lọc đơn bấm thử trước khi đếm.** Phần lớn các dòng hiện có trùng một số điện
  thoại, lặp lại cách nhau vài phút, có dòng ghi thẳng tên anh Sơn.
- Số đơn trong bảng **không** bằng số Lead của Pixel. Pixel đếm lúc khách bấm gửi;
  bảng đếm lúc đơn về tới Google. Lệch nhau là dấu hiệu mất đơn — đã từng xảy ra
  ngày 28/08 (2 Lead, 1 dòng), nguyên nhân và bản vá ghi ở `bao-cao/2026-08-30-02h.md`.

## Số quảng cáo

Máy chạy Phòng 7 **không ra được Facebook** (graph.facebook.com trả 000).
Số quảng cáo chỉ đến từ **ảnh anh Sơn gửi trong khung chat**.
Không thấy ảnh thì ghi **"chưa có số"** — không bao giờ ghi "0".
