# Lady Page — Viên Uống Giảm Mỡ AFC Ellagic Acid (Nhật Bản, 60 viên)

Phòng làm trang bán sản phẩm giảm mỡ, dựng theo đúng bộ khung đã chạy thật của
trang Q10 (sonsongkhoe.com).

Bản gốc học theo: nhánh `claude/dilim-one-website-es08sj` — trang Q10 đang sống,
kèm `prompt/lam-lady-san-pham-moi.md` là bản chỉ dẫn dựng Lady cho sản phẩm mới.

## Trạng thái

🟡 **Trang đã dựng xong, chạy được, nhưng chưa được phép chạy quảng cáo.**

Chạy được ngay: bài kiểm tra 30 giây · phiếu đặt hàng · bản tin Messenger/Zalo/SMS ·
mã QR đặt cọc 200.000đ (đã quét thử, ra đúng số tiền và số tài khoản) · thang sự kiện pixel.

Còn trống, và cố ý để trống: công dụng · thành phần · số công bố · bảng giá.
Xem `HO-SO-CAN-ANH-GUI.md`. Bốn ô bắt buộc còn thiếu, nặng nhất là **ảnh nhãn phụ tiếng Việt**.

## File trong thư mục này

| File | Là gì |
|---|---|
| `index.html` | Cả trang trong một file — 157KB, không phụ thuộc gì bên ngoài trừ phông chữ Google |
| `HUONG-DAN-SUA.md` | Sửa giá, sửa nhãn, sửa nơi nhận đơn ở đâu |
| `HO-SO-CAN-ANH-GUI.md` | Bốn ô bắt buộc anh cần gửi |
| `tao-ma-qr.py` | Sinh mã VietQR cho từng mốc giá |
| `kiem-trang.py` | Tự kiểm trên trình duyệt trước khi đẩy — 42 mục |

## ⚠️ Một kho GitHub chỉ đăng được MỘT trang

Đây là việc phải quyết trước khi em viết một dòng nào của trang.

Kho `ai-agent-check-don` này đã có `.github/workflows/pages.yml` trên nhánh Q10,
đăng `sonsongkhoe.com` lên GitHub Pages. GitHub Pages cho **một trang duy nhất mỗi kho**.
Nếu em thêm một workflow đăng trang giảm mỡ vào cùng kho này, hai bên sẽ đè lên nhau:
lần đẩy sau thắng, và **sonsongkhoe.com đang có khách sẽ bị thay bằng trang giảm mỡ**.

Nên trang giảm mỡ phải nằm ở **kho riêng, tên miền riêng**. Em không tự tạo kho —
cần anh quyết tên kho và tên miền.

Trong lúc chờ, thư mục này chỉ giữ hồ sơ và ghi chú. Không có workflow đăng trang,
cố ý để không đụng vào trang Q10.

## Bộ khung sẽ dựng (12 phần, hai giai đoạn: cho trước — bán sau)

```
Mở đầu   chạm nỗi khổ, chưa nói tên sản phẩm · 2 nút · 3 con số · số điện thoại
  01  Bài tự kiểm tra 6 câu  ← thứ giá trị nhất trên trang
  02  Nguyên nhân gốc rễ          07  Hồ sơ & kiểm nghiệm
  03  Câu chuyện đi vòng          08  Điểm khác biệt
  04  Vì sao cách cũ chỉ đỡ       09  Nhà máy
  05  Muốn tới gốc cần gì         10  Kiểm chứng
  ──  Ba việc làm ngay, miễn phí  11  Minh bạch công ty mẹ
  06  Cơ chế sản phẩm             12  Báo giá & đặt hàng
  ──  Hỏi đáp  ·  Khối nội bộ (ẩn)
```

Một file `index.html` duy nhất, ảnh nhúng base64, không phụ thuộc gì bên ngoài.

## Ranh giới cứng của nhóm giảm cân

Chỉ nói đúng công dụng ghi trên nhãn, không thêm một chữ. Không hứa số cân,
không hứa số ngày, không ảnh trước–sau, không "không cần ăn kiêng",
không hình ảnh hay danh xưng y tế. Bắt buộc in:

> Thực phẩm này không phải là thuốc, không có tác dụng thay thế thuốc chữa bệnh.

## Mười lỗi trang Q10 đã mắc — đi vòng hết

1. Gắn nhầm mã tài khoản quảng cáo vào chỗ mã Pixel
2. Purchase báo tiền cọc thay vì giá trị đơn (lệch ROAS gần 90 lần)
3. Bản tin Messenger/SMS luôn đòi cọc kể cả khi khách trả đủ
4. Khối chuyển khoản hiện sai vì hàm đổi hiển thị chỉ chạy khi có sự kiện `change`
5. `form.reset()` không bắn `change`, viền sáng thẻ bấm kẹt ở ô cũ
6. Mã QR để SVG — điện thoại không lưu được, mất đường chuyển khoản nhanh nhất
7. Khối "chép nguyên nhãn phụ" sai 8 chỗ
8. Thiếu hẳn khối Lưu ý bắt buộc
9. Chèn JS neo vào thẻ `</script>` cuối — thẻ đó nằm trong chú thích HTML, code không chạy
10. Đặt `font-size` cho chữ SVG bằng thuộc tính, bị CSS đè, chữ tràn khung
