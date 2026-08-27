# ai-agent-check-don — Sơ đồ 11 phòng AI

Mỗi AI Agent là một **phòng ban**, đánh số **Phòng 1 → Phòng 11** từ trên xuống.
5 phòng chạy trên máy Mac xếp trước (Phòng 1–5), 6 phòng chạy trên Claude cloud xếp sau (Phòng 6–11);
trong mỗi nhóm vẫn giữ thứ tự "sát tiền" tăng dần — phòng giữ tiền ở cuối.

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

## Quy trình

- [`sop/phong-7-set-quang-cao.md`](sop/phong-7-set-quang-cao.md) — SOP set quảng cáo Meta:
  nhận video từ Phòng 3 (Edivideo) → check compliance → set campaign trên page
  "Phạm Sơn sống khoẻ mỗi ngày" → đọc số → luật Keep/Kill/Scale.
- [`sop/content-ads-dilim.md`](sop/content-ads-dilim.md) — content quảng cáo DiLiM/AFC theo
  Kotler (STP, định vị, value proposition) và Ogilvy (10 tiêu đề, 6 bài copy, kịch bản video 60s),
  kèm bảng nhắm mục tiêu theo độ tuổi & hành vi.

## Cấu trúc

- `index.html` — trang sổ phòng
- `agents.js` — dữ liệu 11 phòng (icon, tên, vai trò, nơi chạy, trạng thái, link session)
- `app.js` — render, đánh số Phòng 1 → N
- `styles.css` — giao diện, có sẵn nền sáng/tối
