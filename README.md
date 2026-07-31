# 🤖 Bot check trùng đơn — DiLi Supplement

Bot Telegram nhận số điện thoại (từ Telegram hoặc từ Messenger qua userscript), dò trong
Google Sheet đơn hàng (mọi tab), rồi báo **TRÙNG / KHÔNG TRÙNG** lên nhóm Telegram.

## Cấu trúc

| File | Công dụng |
|---|---|
| `bot.py` | Bot chính (chạy file này) |
| `config.py` | Đọc cấu hình từ `.env` |
| `phone_utils.py` | Regex tách SĐT Việt Nam, chuẩn hoá 9 số cuối |
| `sheet_store.py` | Tải CSV từ Google Sheet, đánh chỉ mục SĐT |
| `report.py` | Dựng tin báo cáo đúng mẫu |
| `intake_server.py` | Cổng HTTP 127.0.0.1:8787 nhận số từ userscript |
| `userscript/dili-trung-don.user.js` | Userscript Tampermonkey cho Facebook/Messenger |
| `run_bot.bat` | Chạy 24/7 trên Windows (bỏ vào Startup) |
| `dili-bot.service` | Chạy 24/7 trên VPS Linux (systemd) |
| `selftest.py` | Tự kiểm tra logic, không cần token |

## Cài đặt trên Windows — CÁCH NHANH NHẤT

1. Bấm đúp **`cai_dat.bat`** — tự kiểm tra Python, cài thư viện, mở Notepad cho bạn dán `BOT_TOKEN`.
2. Bấm đúp **`run_bot.bat`** — chạy bot (tự khởi động lại nếu lỗi).
3. Thêm bot vào nhóm Telegram → gõ `/id` → điền số vào `REPORT_CHAT_ID=` trong `.env` → chạy lại `run_bot.bat`.

Chi tiết từng bước thủ công ở dưới (nếu cần).

## Cài đặt trên Windows (5 bước)

### 1. Cài thư viện
Mở CMD trong thư mục này:
```bat
pip install -r requirements.txt
```

### 2. Tạo file cấu hình
```bat
copy .env.example .env
notepad .env
```
Điền vào `.env`:
- `BOT_TOKEN=` → dán token của **@dili_supplement_tr_bot** (lấy từ @BotFather). **Không gửi token cho ai.**
- `INTAKE_SECRET=` → đặt một chuỗi bí mật dài tuỳ ý (dùng chung với userscript).
- `REPORT_CHAT_ID=` → tạm để trống, lấy ở bước 4.

⚠️ Google Sheet phải chia sẻ: **Bất kỳ ai có link → Người xem** thì link CSV mới đọc được.
Muốn quét **mọi tab**: dùng `CSV_URLS` — mỗi tab một link với `&gid=...` (mở tab trên trình
duyệt, số sau `#gid=` ở cuối URL chính là gid). Xem ví dụ trong `.env.example`.

### 3. Chạy bot
```bat
python bot.py
```

### 4. Lấy REPORT_CHAT_ID
1. Mở nhóm Telegram muốn nhận báo cáo → **Add member** → thêm `@dili_supplement_tr_bot`.
2. Trong nhóm, gõ `/id` → bot trả về Chat ID (thường dạng `-100xxxxxxxxxx`).
3. Dán số đó vào `REPORT_CHAT_ID=` trong `.env`, tắt bot (Ctrl+C) và chạy lại.
4. Khi khởi động, nhóm sẽ nhận tin **"✅ Bot đã BẬT"** → thành công.

> Nếu gõ `/id` mà bot không trả lời: vào @BotFather → `/mybots` → chọn bot →
> **Bot Settings → Group Privacy → Turn OFF** rồi xoá bot khỏi nhóm và thêm lại.
> (Cũng cần tắt Privacy để bot đọc được SĐT nhắn trong nhóm.)

### 5. Test
Trong nhóm (hoặc chat riêng với bot):
- `/check 0976486366` → phải ra **⚠️ TRÙNG ĐƠN** (khách Tran Loan)
- `/check 0378415411` → **❌ Không trùng**
- Nhắn một câu có SĐT → bot báo cáo lên nhóm; câu không có số → bot **im lặng**.

## Lệnh hỗ trợ

| Lệnh | Công dụng |
|---|---|
| `/id` | Lấy Chat ID của nhóm/chat hiện tại |
| `/check <số>` | Kiểm tra tay một số, trả lời ngay tại chỗ |
| `/reload` | Nạp lại Google Sheet ngay lập tức |

Bot cũng **tự nạp lại** Sheet mỗi `RELOAD_MINUTES` phút (mặc định 15), tự thử lại khi lỗi
mạng, và báo lỗi lên nhóm nếu đọc Sheet thất bại (tối đa 1 tin/30 phút).

## Bắt số từ Messenger (Tampermonkey)

1. Cài extension **Tampermonkey** cho Chrome/Edge.
2. Mở Tampermonkey → **Create a new script** → dán toàn bộ nội dung
   `userscript/dili-trung-don.user.js` → Save.
3. Sửa dòng `INTAKE_SECRET = "..."` trong userscript cho **giống hệt** `.env`.
4. Mở facebook.com / messenger.com, vào đúng đoạn chat **"Xử lý trùng đơn DiLi Supplement"**.
   Góc phải dưới có nút 🟢/🔴 để bật/tắt.
5. Khi có số mới trong khung chat → userscript gửi sang bot (cổng 127.0.0.1:8787) →
   bot báo cáo lên nhóm Telegram. Số đã gửi rồi sẽ không gửi lại.

> Yêu cầu: bot Python phải đang chạy **trên cùng máy** với trình duyệt.

## Chạy 24/7

**Windows:** nhấn `Win + R` → gõ `shell:startup` → Enter → kéo **shortcut** của
`run_bot.bat` vào thư mục đó. Máy bật lên là bot tự chạy, bot lỗi thì tự khởi động lại sau 5 giây.

**VPS Linux:** xem hướng dẫn trong file `dili-bot.service` (systemd, `Restart=always`).

## Kiểm tra nhanh không cần token
```bat
python selftest.py
```
