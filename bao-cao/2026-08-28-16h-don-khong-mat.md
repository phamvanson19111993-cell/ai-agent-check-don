# Phòng 7 · Lady Page — 28/08/2026 16h05

Ảnh báo cáo: `bao-cao/anh/2026-08-28-16h-don-khong-mat.png`

## 1. Đơn khách có mất không

**Từ commit `96d6a9c` trở đi: không mất nữa.** Đơn ghi vào máy khách trước khi
chạm vào mạng. Mở `sonsongkhoe.com/#don-da-luu` trên chính máy đó in ra hết.

**Hai lần bấm gửi 25–27/08 thì không truy lại được.** Dữ liệu nằm trên máy khách,
không phải máy mình, và lúc đó chưa có kho lưu. Nếu Biểu mẫu không nhận thì hai
đơn đó mất thật — nói thẳng, không nói tránh.

Gọi đúng tên theo lệnh Tổng Chỉ Huy: đó là **"2 lần bấm gửi"**, không phải "2 đơn".

## 2. Đã sửa — commit `96d6a9c`, đã lên trang thật

Ba việc, cùng một nguyên nhân gốc: trang gửi bằng `mode:'no-cors'` nên trình
duyệt không đọc được Google trả về gì.

| Sửa gì | Ưu tiên | Vì sao | Đo bằng |
|---|---|---|---|
| `luuDon()` ghi đơn vào localStorage trước khi gửi | P0 | Mạng rớt là mất đơn | Số đơn lấy lại được ở `#don-da-luu` |
| `guiNoiNhan() \|\| guiBieuMau()` → `Promise.all` cả hai | P0 | `\|\|` nghĩa là có Apps Script thì thôi Biểu mẫu — một đường hỏng là mất đơn | Đơn vào Biểu mẫu |
| Bỏ câu "Bên em đã nhận được đơn" | P0 | Trang không chứng minh được câu đó | Tỷ lệ khách bấm Gửi qua Messenger |

### Đơn thử — chạy thật, hai chế độ mạng

| Kiểm | Kết quả |
|---|---|
| Đặt đơn "TEST TỔNG CHỈ HUY" | đã đặt |
| Mạng tốt → lưu máy + gửi đi | đạt (`trang_thai: da-gui-di`) |
| Mạng hỏng → vẫn lưu, báo lỗi rõ | đạt (`trang_thai: gui-hong`) |
| Đủ 5 cấp địa chỉ | đạt |
| Số tiền 5.780.000đ · trả đủ | đạt |
| Trang `#don-da-luu` lấy lại đơn | đạt |

Không kiểm được từ máy này: **Biểu mẫu Google có thật sự nhận hay không.**
Phiên này bị chặn ra `docs.google.com` (trả về 000). Chỉ anh Sơn mở tab
"Câu trả lời" mới biết.

## 3. Đính chính gửi Tổng Chỉ Huy

Bảng tính "Lady Page" (`1OrfV...`) rỗng **không** chứng minh Biểu mẫu rỗng.
Bảng đó là đích của Apps Script; Apps Script chưa triển khai nên nó rỗng là
đương nhiên. Câu trả lời của Biểu mẫu nằm trong chính Biểu mẫu
(`1Un2cq-BMmq19pPLmF5jUkhf7AZKJQbQGKYFszrr8iqk`), và bảng tính liên kết
**chưa từng được tạo**.

Có thể hai đơn đó vẫn đang nằm trong Biểu mẫu.

## 4. Việc không làm — nhét mã bot Telegram vào trang

Lệnh yêu cầu dùng bot Telegram sẵn có để đẩy đơn thẳng từ trang.

`index.html` là trang công khai — ai mở cũng đọc được mã nguồn. Nhét mã bot vào
đó là công bố mã bot cho toàn bộ internet: bất kỳ ai cũng đọc được đơn khách và
nhắn giả danh vào khung chat. Đó chính là rủi ro đang phải xử lý, không phải
cách xử lý nó.

Cách đúng cho cùng kết quả: Apps Script giữ mã bot ở phía máy chủ, trang chỉ
biết địa chỉ nhận. Mã đã viết sẵn ở `apps-script/nhan-don-lady-page.gs`.

Mã bot lộ trong ảnh chụp màn hình hôm nay **vẫn chưa thu hồi**.

## 5. Việc cần anh Sơn quyết / làm

1. Mở Biểu mẫu → tab **Câu trả lời**: có 2 đơn không? Có thì gọi khách ngay.
2. Bấm **Liên kết tới Trang tính** ngay trong tab đó — hai cú bấm.
3. Thu hồi mã bot Telegram bị lộ.

## Lượt xem cộng dồn

235 (27/08) + 109 (28/08 tới 15h) = **344 / 1.515** — 23% quãng đường tới mốc
hoà vốn một đơn. Chưa đủ để kết luận trang kém.
