# ai-agent-check-don — Sơ đồ 12 phòng AI

Mỗi AI Agent là một **phòng ban**, đánh số **Phòng 1 → Phòng 12** từ trên xuống.
5 phòng chạy trên máy Mac xếp trước (Phòng 1–5), 6 phòng chạy trên Claude cloud xếp sau (Phòng 6–11),
Phòng 12 là bộ prompt + sổ tay dán vào Claude/ChatGPT là chạy;
trong mỗi nhóm vẫn giữ thứ tự "sát tiền" tăng dần — phòng sát tiền nhất ở cuối.

Mở `index.html` bằng trình duyệt để xem. Sửa danh sách trong `agents.js` — số phòng tự chạy lại.

## Sổ phòng

| Phòng | Agent | Vai trò | Ở đâu |
|---|---|---|---|
| 1 | 📚 Học tập & đào tạo | Nội bộ: tự học, đào tạo nhân viên mới | 💻 máy Mac |
| 2 | 🎥 Curl Foxia API | Hướng dẫn kỹ thuật: gọi API Foxia | 💻 máy Mac |
| 3 | 🎬 Edivideo | Dựng & cắt video tự động | 💻 máy Mac |
| 4 | ✍️ Kịch bản sale | Content bán hàng, kịch bản chốt đơn | 💻 máy Mac |
| 5 | 📞 SĐT chưa chốt Pancake | Gom lead chưa chốt để gọi lại | 💻 máy Mac |
| 6 | 🩺 Video content sức khỏe | Kịch bản & hook cho video sức khỏe | ☁️ cloud |
| 7 | 👩 Lady Page | Video & ads sản phẩm trên fanpage | ☁️ cloud |
| 8 | 📊 Fanpage Pancake | Đồng bộ dữ liệu fanpage về hệ thống | ☁️ cloud |
| 9 | 💬 Agen Zalo | Tư vấn & chăm khách trên Zalo | ☁️ cloud |
| 10 | 🎧 CSKH | Chăm sóc sau bán, xử lý khiếu nại | ☁️ cloud |
| 11 | 🔁 Check trùng đơn | Bot Telegram chặn trùng đơn, cảnh báo ngay | ☁️ cloud |
| 12 | 📈 [AI Ads Manager](ads-agent/README.md) | Chạy & kiểm soát Meta Ads: creative, số liệu, quyết định scale | 📄 prompt |

## Tên session trên Claude

7 session cloud đã đổi tên tự động:

```
Phòng 6 · 🩺 Video content sức khỏe
Phòng 7 · 👩 Lady Page
Phòng 8 · 📊 Fanpage Pancake
Phòng 9 · 💬 Agen Zalo
Phòng 10 · 🎧 CSKH
Phòng 11 · 🔁 Check trùng đơn
🗺️ Sơ đồ phòng AI
```

5 session nhóm `mac` chạy trên máy cá nhân nên phải đổi tay — copy đúng các chuỗi sau:

```
Phòng 1 · 📚 Học tập & đào tạo
Phòng 2 · 🎥 Curl Foxia API
Phòng 3 · 🎬 Edivideo
Phòng 4 · ✍️ Kịch bản sale
Phòng 5 · 📞 SĐT chưa chốt Pancake
```

Lưu ý: số 1–9 hiện trong sidebar Claude là **phím tắt theo vị trí**, app tự gán, không đặt tay được;
sidebar cũng sắp theo lần dùng gần nhất. Số phòng trong file này mới là thứ tự ưu tiên.

## Phòng 12 — AI Ads Manager

Phòng duy nhất không phải một session, mà là **một bộ não dán được vào bất cứ đâu**:
prompt đầy đủ + 10 sổ tay vận hành + máy tính kinh tế đơn hàng.

- [`ads-agent/AGENT.md`](ads-agent/AGENT.md) — dán vào Custom Instructions là xong
- [`ads-agent/README.md`](ads-agent/README.md) — cách dùng trong 3 bước
- [`ads-agent/tools/unit-economics.html`](ads-agent/tools/unit-economics.html) — nhập giá vốn & số liệu → ra **CAC hoà vốn**, **CPL hoà vốn** và quyết định GIỮ / TẮT / SCALE

Nguyên tắc gốc của phòng này: *CPL rẻ không phải thắng — CAC dưới ngưỡng hoà vốn mới là thắng.*

## Cấu trúc

- `index.html` — trang sổ phòng
- `agents.js` — dữ liệu 12 phòng (icon, tên, vai trò, nơi chạy, trạng thái, link session hoặc sổ tay)
- `app.js` — render, đánh số Phòng 1 → N
- `ads-agent/` — Phòng 12: prompt, playbook, máy tính kinh tế đơn hàng
- `styles.css` — giao diện, có sẵn nền sáng/tối
