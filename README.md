# ai-agent-check-don — Sơ đồ 11 phòng AI

Mỗi AI Agent là một **phòng ban**, đánh số **Phòng 1 → Phòng 11** từ trên xuống,
xếp theo mức "sát tiền" tăng dần: việc nội bộ ở trên, phòng giữ tiền ở dưới cùng.

Mở `index.html` bằng trình duyệt để xem. Sửa danh sách trong `agents.js` — số phòng tự chạy lại.

## Sổ phòng

| Phòng | Agent | Vai trò | Ở đâu |
|---|---|---|---|
| 1 | 📚 Học tập & đào tạo | Nội bộ: tự học, đào tạo nhân viên mới | 💻 máy Mac |
| 2 | 🎥 Curl Foxia API | Hướng dẫn kỹ thuật: gọi API Foxia | 💻 máy Mac |
| 3 | 🩺 Video content sức khỏe | Kịch bản & hook cho video sức khỏe | ☁️ cloud |
| 4 | 👩 Lady Page | Video & ads sản phẩm trên fanpage | ☁️ cloud |
| 5 | 📊 Fanpage Pancake | Đồng bộ dữ liệu fanpage về hệ thống | ☁️ cloud |
| 6 | 🎬 Edivideo | Dựng & cắt video tự động | 💻 máy Mac |
| 7 | ✍️ Kịch bản sale | Content bán hàng, kịch bản chốt đơn | 💻 máy Mac |
| 8 | 💬 Agen Zalo | Tư vấn & chăm khách trên Zalo | ☁️ cloud |
| 9 | 🎧 CSKH | Chăm sóc sau bán, xử lý khiếu nại | ☁️ cloud |
| 10 | 📞 SĐT chưa chốt Pancake | Gom lead chưa chốt để gọi lại | 💻 máy Mac |
| 11 | 🔁 Check trùng đơn | Bot Telegram chặn trùng đơn, cảnh báo ngay | ☁️ cloud |

## Tên session trên Claude

7 session cloud đã đổi tên tự động:

```
Phòng 3 · 🩺 Video content sức khỏe
Phòng 4 · 👩 Lady Page
Phòng 5 · 📊 Fanpage Pancake
Phòng 8 · 💬 Agen Zalo
Phòng 9 · 🎧 CSKH
Phòng 11 · 🔁 Check trùng đơn
🗺️ Sơ đồ phòng AI
```

5 session nhóm `mac` chạy trên máy cá nhân nên phải đổi tay — copy đúng các chuỗi sau:

```
Phòng 1 · 📚 Học tập & đào tạo
Phòng 2 · 🎥 Curl Foxia API
Phòng 6 · 🎬 Edivideo
Phòng 7 · ✍️ Kịch bản sale
Phòng 10 · 📞 SĐT chưa chốt Pancake
```

Lưu ý: số 1–9 hiện trong sidebar Claude là **phím tắt theo vị trí**, app tự gán, không đặt tay được;
sidebar cũng sắp theo lần dùng gần nhất. Số phòng trong file này mới là thứ tự ưu tiên.

## Cấu trúc

- `index.html` — trang sổ phòng
- `agents.js` — dữ liệu 11 phòng (icon, tên, vai trò, nơi chạy, trạng thái, link session)
- `app.js` — render, đánh số Phòng 1 → N
- `styles.css` — giao diện, có sẵn nền sáng/tối
