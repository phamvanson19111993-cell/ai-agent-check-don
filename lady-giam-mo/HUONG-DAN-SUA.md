# Sửa trang giảm mỡ ở đâu

Cả trang nằm trong một file `index.html`. Mọi thứ hay phải sửa đều gom vào
hai khối ở gần cuối file, không phải đi tìm khắp nơi.

## 1 · Điền bảng giá

Tìm dòng `var BANG_GIA = [];` rồi điền vào. Ví dụ:

```js
var BANG_GIA = [
  { hop:1, gia:590000,  ngay:30,  nhan:'Đủ 1 tháng' },
  { hop:3, gia:1650000, ngay:90,  qua:'Tên quà tặng', qua_tien:675000 },
  { hop:6, gia:3100000, ngay:180, loi_nhat:true }
];
```

Điền xong thì **ba chỗ tự đổi theo**: bảng báo giá, thẻ chọn số lượng trong
phiếu đặt hàng, và dòng đơn giá ở đầu ô đặt hàng. Không phải sửa ba lần.

`qua_tien` là trị giá quà tính bằng tiền. Chữ "kèm quà tặng" là chữ rỗng —
khách không quy ra được thành tiền thì không thấy lợi ở đâu.

## 2 · Sinh lại mã QR sau khi đổi giá

Mã QR nhúng sẵn số tiền trong nó. Đổi giá mà không sinh lại thì khách quét
ra số tiền cũ.

```bash
pip install segno
python3 lady-giam-mo/tao-ma-qr.py 590000 1650000 3100000
```

Chép nguyên khối `var QR_TIEN = {...}` in ra màn hình, dán đè lên dòng
`var QR_TIEN = {};` trong `index.html`.

Mã đặt cọc 200.000đ đã có sẵn, không phải sinh lại — trừ khi đổi số tiền cọc
hoặc đổi tài khoản ngân hàng.

## 3 · Nối nơi nhận đơn

Trong bảng điều khiển:

- `NOI_NHAN_DON` — dán đường dẫn kết thúc bằng `/exec` của Apps Script.
- `FORM_GOOGLE.ma` và `FORM_GOOGLE.gop` — nếu dùng Biểu mẫu Google.

Để trống cả hai thì đơn vẫn không mất: nó đi qua Messenger, Zalo, SMS, và
được chép sẵn vào bộ nhớ tạm của máy khách. Nhưng **đường chắc nhất là bảng
tính**, nên nối trước khi chạy quảng cáo.

⚠️ Đừng dùng lại mã biểu mẫu của trang Q10 — đơn sẽ chảy nhầm vào bảng tính Q10.

## 4 · Điền nhãn phụ

Các khối viền vàng trên trang là chỗ chờ nhãn. Chép **đúng từng chữ** từ ảnh
nhãn phụ, không diễn giải, không làm đẹp. Trang Q10 từng có khối tự nhận là
chép nguyên nhãn nhưng sai 8 chỗ.

Cần điền: Phần 06 (cơ chế) · Phần 07 (hồ sơ, khối chép nhãn) · Phần 08 (khác biệt) ·
Phần 09 (nhà máy) · khối `spec-list` trong phần sản phẩm · dòng số công bố ở
khối pháp lý cuối trang.

## 5 · Tự kiểm trước khi đẩy

```bash
pip install playwright opencv-python-headless numpy segno
python3 lady-giam-mo/kiem-trang.py
```

42 mục, gồm cả việc **quét lại mã QR bằng máy** đúng như app ngân hàng của
khách, xem có ra đúng số tiền không. Xanh hết rồi hãy đẩy.

## 6 · Trước khi đăng lên tên miền

⚠️ Một kho GitHub chỉ đăng được **một** trang. Kho này đang đăng sonsongkhoe.com
từ nhánh Q10. Thêm workflow đăng trang giảm mỡ vào đây là **đè mất trang Q10**.
Trang này phải nằm ở kho riêng, tên miền riêng.

## Bảng điều khiển có những gì

| Biến | Là gì |
|---|---|
| `BANG_GIA` | Các mốc giá và quà tặng |
| `QR_TIEN` | Mã QR cho từng số tiền |
| `QR_COC` | Mã QR đặt cọc — đã có sẵn |
| `TIEN_COC` | Tiền cọc giữ hàng, đang là 200.000đ |
| `NGAN_HANG` | Tài khoản nhận tiền |
| `PIXEL_ID` | Pixel Facebook — đang dùng chung `1277743445418211` |
| `NOI_NHAN_DON` · `FORM_GOOGLE` | Nơi đơn chảy về |
| `TU_MO_MESSENGER` | Có tự mở Messenger sau khi khách gửi đơn không |
| `LIEN_HE` | Hotline, Messenger, Zalo |
