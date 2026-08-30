# BÁO CÁO KHỞI ĐỘNG — AI SALES & CSKH 24/7

> Chạy ngày 30/08/2026 theo LỆNH KHỞI ĐỘNG trong Master Prompt.
> **Kết luận: CHƯA ACTIVE ĐƯỢC.** Thiếu 4 công cụ. Chi tiết bên dưới.

---

## ⚠️ Điều phải nói trước

**Phòng 10 (CSKH) không phải nơi cài Master Prompt này.**

Phòng 10 là phòng tài liệu, chạy trong kho git. Phòng 10 **không có công cụ đọc tin nhắn
khách, không có công cụ gửi tin nhắn**. Master Prompt yêu cầu một agent trực tiếp hội thoại
với khách — việc đó phải chạy trên **bot Zalo của Phòng 9** (`claude/agen-zalo-3780k7`).

→ Master Prompt cần cài vào `src/agent/prompt.js` của Phòng 9, dùng tài liệu Phòng 10 làm
Knowledge Base.

---

## Bảng kiểm 11 mục của LỆNH KHỞI ĐỘNG

| # | Mục | Trạng thái | Ghi chú |
|---|---|---|---|
| 1 | Knowledge Base | ✅ | 10 file docs Phòng 10 + bộ nhớ chung Tổng Chỉ Huy |
| 2 | Bảng sản phẩm | ⚠️ **1/6** | Chỉ Rich Coenzyme Q10 có hồ sơ đủ. 5 sản phẩm còn lại chưa có nhãn |
| 3 | Bảng giá | ⚠️ **1/6** | 5 mốc của CoQ10 đã xác minh. 5 sản phẩm kia chưa có giá |
| 4 | Chính sách bán hàng | ❌ **THIẾU** | Không có thông tin thanh toán, không có chính sách đổi trả |
| 5 | Quy trình CSKH | ✅ | Chu kỳ 10 ngày · chốt đơn 6 bước · upsell/cross-sell · thư viện tin |
| 6 | Kiểm tra tool/API | ⚠️ | Xem bảng dưới |
| 7 | Tool đọc tin nhắn | ⚠️ **CÓ CODE, CHƯA NỐI** | `src/zalo/webhook.js` — nhưng `ZALO_APP_ID` trống |
| 8 | Tool gửi tin nhắn | ⚠️ **CÓ CODE, CHƯA NỐI** | `src/zalo/client.js` — cùng lý do |
| 9 | CRM / database | ❌ **THIẾU** | Chỉ có `SessionStore` trong RAM, TTL 30 phút |
| 10 | Công cụ tạo đơn | ⚠️ **ĐANG CHẠY GIẢ** | `ORDER_PROVIDER=mock`, đọc file JSON. `ORDER_API_BASE_URL` trống |
| 11 | Scheduler follow-up | ❌ **THIẾU** | Không có cron/scheduler nào trong bot |

---

## BỐN CÔNG CỤ CÒN THIẾU — báo chính xác

### ❌ 1. Zalo OA chưa có → bot không nhận được tin nhắn nào

`.env.example` của Phòng 9 cần `ZALO_APP_ID`, `ZALO_APP_SECRET`, `ZALO_REFRESH_TOKEN`.
Muốn có ba thứ đó phải **đăng ký Zalo Official Account đã xác thực** — hiện chưa đăng ký.

**Không có OA thì toàn bộ Master Prompt nằm im**, vì không có đường nào để tin nhắn khách
đi vào và câu trả lời đi ra.

→ Hồ sơ đăng ký: [`dang-ky-zalo-oa-zns.md`](./dang-ky-zalo-oa-zns.md). Cần anh Sơn nộp.

### ❌ 2. Không có CRM → mục 5, 12, 13, 14 của Master Prompt không chạy được

Bot chỉ có `SessionStore` **trong bộ nhớ RAM**, tự xoá sau **30 phút** và **mất sạch khi
khởi động lại**.

Master Prompt yêu cầu lưu `CUSTOMER_ID · NEED · CURRENT_STAGE · NEXT_ACTION ·
FOLLOW_UP_TIME · LEAD_SCORE`. Không có kho bền vững thì:

- Khách quay lại sau 31 phút → **AI tư vấn lại từ đầu** (vi phạm mục 4 và 14)
- Không nhớ được HOT LEAD → **không chống mất khách được** (mục 13)
- Không có khách cũ → **không chăm sóc sau bán, không mua lại** (mục 14)

→ Cần một kho bền vững (Redis, SQLite, Google Sheet hay bảng nào cũng được). **Chưa ai làm.**

### ❌ 3. Không có scheduler → mục 12 (FOLLOW-UP TỰ ĐỘNG) không chạy được

Không có cron nào trong bot. Không có gì đánh thức bot để nhắn lại khách đã hẹn.

→ Chu kỳ chăm sóc 10 ngày Phòng 10 đã dựng **hiện chỉ chạy tay** bằng
`scripts/lich_cskh.py` — người mở máy, chạy lệnh, rồi tự dán vào Zalo.

### ❌ 4. Công cụ tạo đơn đang chạy giả

`ORDER_PROVIDER=mock` — đọc file `data/orders.json`. `ORDER_API_BASE_URL` để trống.

Master Prompt mục 10 cấm tuyên bố *"đơn đã tạo thành công"* khi hệ thống chưa xác nhận.
Với cấu hình hiện tại, bot **không tạo được đơn thật**.

→ Liên quan MT-11 trong sổ mâu thuẫn: *"đơn khách không chảy vào bảng nào"*.

---

## ➕ Còn thiếu dữ liệu, không phải công cụ

| Thiếu | Chặn mục nào của Master Prompt |
|---|---|
| **Thông tin thanh toán** (số TK, chủ TK, COD, ship, QR) | Mục 10 — ORDER MODE không hoàn tất được |
| **Chính sách đổi trả** | Mục 6 — không xử lý được TRUST_OBJECTION |
| **Giá + nhãn 5 sản phẩm còn lại** | Mục 9 — phải trả `PRICE_DATA_REQUIRED` cho 5/6 sản phẩm |
| **Mức giảm tiền mặt mốc 3 và 5** (MT-18) | Mục 9 — khách hỏi thật, không trả lời được |
| **Ảnh 4 giấy tờ** | Mục 6 — không xử lý được TRUST_OBJECTION khi khách đối chiếu |

---

## ✅ Cái gì đã sẵn sàng

- **Knowledge Base bán hàng đầy đủ cho Rich Coenzyme Q10**: giá 5 mốc đã xác minh, quy cách,
  thành phần, số công bố, nhà sản xuất
- **Luật tuân thủ TPCN** — khớp mục 15 và 16 của Master Prompt:
  cấm "chữa khỏi / điều trị / thay thế thuốc", bắt buộc câu khuyến cáo, bắt buộc ghi
  "hiệu quả tuỳ cơ địa" khi dẫn lời người dùng
- **Cảnh báo tương tác thuốc** — khớp mục 16: thuốc chống đông, đang hoá trị, thuốc huyết áp
- **4 câu hỏi sàng lọc bắt buộc** theo nhãn: dị ứng · đang dùng thuốc · đang điều trị tại
  bệnh viện · đang mang thai
- **Hàng rào MT-10**: nhắc "dạng khử" phải dẫn nguồn chữ 還元型 trên hộp gốc Nhật
- **Kịch bản 6 bước, xử lý 6 lời từ chối, upsell/cross-sell, chu kỳ chăm sóc 10 ngày**
- **Bot đã đọc thẳng bộ nhớ chung** (`SHARED_MEMORY_ENABLED=true`) — không chép số, không lệch

---

## Thứ tự nên làm

```
1. Đăng ký Zalo OA          → không có thì mọi thứ khác vô nghĩa
2. Gửi thông tin thanh toán → để ORDER MODE hoàn tất được
3. Dựng CRM bền vững        → để AI nhớ khách, chống mất khách
4. Nối API tạo đơn thật     → thay mock (liên quan MT-11)
5. Dựng scheduler follow-up → để chu kỳ 10 ngày tự chạy
6. Nạp giá + nhãn 5 SP còn lại
```

Bước 1 và 2 cần **anh Sơn**. Bước 3, 4, 5 cần **Phòng 9**. Bước 6 cần **Phòng 7**.

---

## TRẠNG THÁI

```
AI SALES & CSKH 24/7 = CHƯA ACTIVE
Thiếu: ZALO_OA · CRM_DATABASE · SCHEDULER · ORDER_API
Thiếu dữ liệu: PAYMENT_INFO · RETURN_POLICY · PRICE_DATA (5/6 sản phẩm)
```
