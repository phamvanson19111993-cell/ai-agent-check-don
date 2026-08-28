# LUẬT CẢI TIẾN LIÊN TỤC — Phòng 7 Lady Page

> **Anh Sơn ra lệnh 28/08/2026:** *"Nếu Lady Phòng 7 chưa có đơn hoặc ít đơn thì tự bắt phòng
> sửa lỗi liên tục."*
>
> Nghĩa là: **không chờ anh nhắc, không chờ có đơn mới làm.** Mỗi kỳ báo cáo phải giao được
> ít nhất **một cải tiến cụ thể đã lên trang**, hoặc nói rõ vì sao không.

## ⚠️ ĐỌC TRƯỚC: hôm nay CHƯA ĐO ĐƯỢC ĐƠN, và traffic quá ít để kết luận

**Hai sự thật phải nắm trước khi sửa bất cứ thứ gì:**

1. **Đơn không chảy vào bảng nào** (MT-11). Apps Script chưa triển khai. Nghĩa là "chưa có đơn"
   hiện nay **không phải kết luận, mà là không biết**. Sửa trang khi chưa đo được là sửa mù.

2. **235 lượt xem là quá ít để phán trang hỏng.** Ngày 27/08 chạy 235 lượt (224.190đ).
   Hoà vốn 1 đơn mốc 1 hộp cần **1.515 lượt** → mới đi được **16% quãng đường** tới mốc
   đánh giá được. **0 đơn trên 235 lượt KHÔNG phải bằng chứng trang kém.**

→ Vì vậy thứ tự dưới đây bắt đầu từ **đo được**, không bắt đầu từ viết lại nội dung.

## Thang ưu tiên — làm từ trên xuống, không nhảy cóc

### P0 · ĐO ĐƯỢC ĐÃ *(chặn tất cả)*
Không có số thì mọi cải tiến chỉ là đoán.
- Apps Script nhận đơn → đơn chảy vào bảng. **Cần anh Sơn bấm triển khai.**
- Trong lúc chờ: dựng đường dự phòng để không mất đơn nào (Messenger / Zalo / SMS soạn sẵn).
- Mỗi kỳ, xin anh **ảnh Ads Manager**: lượt xem · chi phí · và các sự kiện pixel
  `PageView → CompleteRegistration → InitiateCheckout → Lead → Purchase`.

### P1 · SỬA CHỖ CHẮC CHẮN HỎNG — không cần dữ liệu vẫn biết là sai
Làm ngay, không phải chờ ai:
- Lỗi hiển thị, tràn ngang, ảnh vỡ ở 390px / 768px / 1280px
- Trang tải chậm, ảnh nặng, video tự phát ăn băng thông
- Bước thừa trong luồng đặt hàng, ô nhập thừa, bắt điền thứ không cần
- **Câu khách hay hỏi mà trang chưa trả lời** — lấy từ Phòng 10 CSKH
  (`claude/zalo-customer-care-messaging-uj9q4i` → `docs/thu-vien-tin-nhan.md`)
- Chỗ nói suông chưa có bằng chứng — thay bằng ảnh, giấy tờ, con số

### P2 · ĐỌC PHỄU, SỬA ĐÚNG CHỖ RƠI
Khi có số pixel, tính tỷ lệ giữa từng bậc thang:
```
PageView → CompleteRegistration → InitiateCheckout → Lead → Purchase
```
**Bậc nào rơi nhiều nhất là bậc phải sửa.** Không sửa bậc khác cho vui.

### P3 · THỬ TỪNG THỨ MỘT
Chỉ khi P0–P2 đã sạch. **Mỗi kỳ đúng MỘT thay đổi lớn.** Đổi nhiều thứ cùng lúc thì
không biết cái nào ăn.

## Bốn điều CẤM khi tự cải tiến

1. **Cấm đập đi làm lại vì "chưa có đơn".** Traffic chưa đủ để kết luận. Đập trang đang chạy
   là mất luôn nền so sánh.
2. **Cấm tự sửa giá, mốc combo, quà tặng, số giấy tờ, câu tuân thủ.** Đó là dữ liệu có nguồn,
   không phải chỗ để tối ưu. Muốn đổi phải qua anh Sơn.
3. **Cấm đổi nhiều thứ cùng một kỳ** rồi báo "đã tối ưu". Không đo được thì không tính là cải tiến.
4. **Cấm báo cáo suông.** Mỗi cải tiến phải ghi đủ: **sửa gì · vì sao · đo bằng chỉ số nào ·
   commit nào.**

## Mẫu ghi vào đơn báo cáo mỗi kỳ

```
## CẢI TIẾN KỲ NÀY
- Sửa gì:        <thay đổi cụ thể>
- Ưu tiên:       P0 | P1 | P2 | P3
- Vì sao:        <lỗi thấy được, hoặc bậc phễu đang rơi>
- Đo bằng:       <chỉ số sẽ nhìn để biết ăn hay không>
- Commit:        <mã commit>
- Trạng thái nền: <số lượt xem cộng dồn, đã đủ 1.515 lượt chưa>
```

Không có cải tiến nào thì ghi thẳng **"KHÔNG CẢI TIẾN — lý do: ..."**. Im lặng không được tính.
