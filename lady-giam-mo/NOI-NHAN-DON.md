# Nơi nhận đơn — anh Sơn quản lý số ở đâu

## 📋 Bảng đơn hàng

**https://docs.google.com/spreadsheets/d/1fcUxwgmu2XGHG1QJ5fx1ZFw6X5UOFjmfVf885aJWsVE/edit**

Em đã tạo sẵn trong Drive của anh, tên **"Đơn Ellagic Acid — Lady giảm mỡ"**.
Mở được trên điện thoại. Có sẵn một **đơn mẫu** để anh thấy hình dạng — xoá đi khi chạy thật.

Mười một cột:

| Cột | Là gì |
|---|---|
| Thời gian | Lúc khách bấm Gửi |
| **Trạng thái** | Nhân viên chọn: Mới · Đã gọi · Chốt đơn · Hẹn gọi lại · Không nghe máy · Huỷ |
| Họ tên · Số điện thoại · Địa chỉ | Ba ô khách điền |
| Số lượng · Số gói · Giá trị đơn | Mốc khách chọn |
| Nhắc đặt lại | Khách có tích ô "gọi nhắc trước khi hết gói" không |
| Bài kiểm tra | Kết quả bài 30 giây, nếu khách có làm |
| Nguồn | Trang nào gửi đơn về |

## ⚠️ Hiện tại đơn CHƯA chảy về bảng này

Còn thiếu một bước, và **chỉ anh làm được** — em không có quyền triển khai Apps Script
trong tài khoản của anh.

### Bốn bước, khoảng 3 phút

1. Mở bảng ở trên → **Tiện ích mở rộng** → **Apps Script**
2. Xoá hết code cũ → dán toàn bộ `apps-script/nhan-don.gs` vào → bấm **Lưu**
3. Bấm **Triển khai** → **Tuỳ chọn triển khai mới** → chọn **Ứng dụng web**
   - Thực thi với: **Tôi**
   - Ai có quyền: **Bất kỳ ai**
   - → **Triển khai** → cho phép quyền truy cập
4. Copy đường dẫn kết thúc bằng `/exec`, **gửi cho em**

Em dán vào biến `NOI_NHAN_DON` trong `index.html` là đơn chảy thẳng về bảng.

**Muốn thử trước:** trong Apps Script chọn hàm `thuMotDon` rồi bấm Chạy.
Phải thấy một đơn mẫu hiện ra. Chạy lần hai phải báo `trung` chứ không ghi thêm dòng.

## Bộ máy nhận đơn có gì

**Chặn đơn trùng.** Hai đơn cùng số điện thoại cách nhau dưới **30 phút** thì bỏ qua đơn sau.
Khách hay bấm Gửi hai lần, hoặc tải lại trang rồi gửi lại. Đổi mốc ở biến `PHUT_COI_LA_TRUNG`.

**Xếp hàng khi đơn về cùng lúc.** Hai đơn về một lúc mà cùng ghi thì đè nhau —
`LockService` bắt chúng chờ nhau.

**Giữ số 0 đầu số điện thoại.** Ghi thẳng thì Sheet nuốt mất số 0, thành `912345678`.

## Đơn đang đi đường nào khi chưa cắm

| | Đường | Chắc không |
|---|---|---|
| 1 | Messenger tự mở với đơn soạn sẵn | ⚠️ khách phải bấm Gửi |
| 2 | Chép đơn vào bộ nhớ tạm máy khách | lưới an toàn |
| 3 | Bốn nút: Messenger · Zalo · SMS · Gọi | khách tự chọn |

**Chưa cắm xong thì đừng bật tiền quảng cáo.** Khách điền form xong mà không bấm Gửi
trong Messenger là đơn mất luôn, bên em không có bản ghi nào.
