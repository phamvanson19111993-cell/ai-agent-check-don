# ai-agent-check-don

Danh sách AI Agent hiển thị dạng **đánh số từ 1**, mỗi dòng kèm **icon theo đúng vai trò**
và mô tả chức năng ngắn gọn. Thứ tự: **ít quan trọng ở trên → quan trọng nhất ở dưới**.

Mở `index.html` bằng trình duyệt để xem. Sửa danh sách trong `agents.js`.

## Danh sách (copy để đặt lại tên từng agent)

| # | Agent | Vai trò / chức năng |
|---|-------|---------------------|
| 1 | 🔢 AI Agent icons với dòng đánh số | Giao diện danh sách agent, đánh số + icon |
| 2 | 📚 AI agent học tập và đào tạo | Nội bộ: tự học, đào tạo nhân viên mới |
| 3 | 🎥 Video hướng dẫn curl Foxia API | Hướng dẫn kỹ thuật: gọi API Foxia bằng curl |
| 4 | 🩺 AI Agent video content sức khỏe | Sản xuất nội dung video chủ đề sức khỏe |
| 5 | 👩 Lady Page | Vận hành & trả lời fanpage thương hiệu |
| 6 | 📊 Cập nhật dữ liệu Fanpage Pancake | Đồng bộ dữ liệu fanpage từ Pancake về hệ thống |
| 7 | 🎬 Edivideo | Dựng & cắt video tự động |
| 8 | ✍️ AI viết kịch bản sale | Viết kịch bản bán hàng, content chốt đơn |
| 9 | 💬 Agen Zalo | Tư vấn & chăm khách trên Zalo |
| 10 | 🎧 AI chăm sóc khách hàng | CSKH sau bán, xử lý khiếu nại |
| 11 | 📞 Tổng hợp SĐT chưa chốt Pancake | Gom lead chưa chốt để gọi lại, remarketing |
| 12 | 🔁 Telegram bot kiểm tra trùng đơn | Chặn trùng đơn, cảnh báo tức thì qua Telegram |

Nhóm `mac` gồm các agent số 7–12; số thứ tự chạy liên tục qua các nhóm.

## Cấu trúc

- `index.html` — khung sidebar
- `agents.js` — dữ liệu agent (icon, tên, vai trò, thứ tự)
- `app.js` — render danh sách, đánh số liên tục, chọn dòng
- `styles.css` — giao diện
