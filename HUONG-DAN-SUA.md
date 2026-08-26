# Tự sửa trang sonsongkhoe.com

Mọi cài đặt hay phải đổi đều nằm trong **BẢNG ĐIỀU KHIỂN** ở đầu phần script
của `index.html`. Mở file trên GitHub, bấm biểu tượng bút chì, sửa, rồi
**Commit changes**. Trang tự đăng lại sau khoảng hai phút.

## Sửa được ngay, không cần hỏi ai

| Muốn đổi | Tìm chữ này trong index.html |
|---|---|
| Nơi nhận đơn (link /exec) | `var NOI_NHAN_DON` |
| Mã Pixel Facebook | `var PIXEL_ID` |
| Số tiền cọc | `var TIEN_COC` |
| Hotline, Messenger, Zalo | `var LIEN_HE` |
| Tiêu đề hiện trên tab trình duyệt | `<title>` |
| Câu hỏi bài kiểm tra | `var QUESTIONS` |
| Giá và số hộp | `2.890.000đ` |
| Ảnh sản phẩm | thay file trong thư mục `images/` |

Hotline còn nằm rải rác trong phần chữ của trang. Đổi số thì tìm cả
`0913.351.394` và `0913351394`, thay hết.

## Đổi được nhưng phải báo trước

**Số tài khoản** (`var NGAN_HANG`) và **số tiền cọc**: chữ trên trang đổi ngay,
nhưng mã QR đã nhúng sẵn số cũ ở dạng ảnh, không tự đổi theo. Đổi mà không sinh
lại mã thì khách quét ra số tài khoản cũ hoặc số tiền cũ.

## Đừng sửa một mình

- **Ba công dụng** — chép nguyên từ giấy công bố. Viết thêm là vượt giấy xác
  nhận nội dung quảng cáo 1582/2024/XNQC-ATTP.
- **Khối khuyến cáo** cuối trang — luật bắt buộc phải có.
- **Khối nhãn phụ và ảnh giấy tờ** — phải khớp với hồ sơ thật.

## Xem lại và quay về bản cũ

Vào tab **Commits** của kho là thấy toàn bộ lịch sử, mỗi lần sửa ghi rõ đã đổi
gì và vì sao. Bản nào hỏng thì mở commit đó, bấm **Revert** là quay lại.
