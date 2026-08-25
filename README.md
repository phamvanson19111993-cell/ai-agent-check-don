# ai-agent-check-don

Danh sách AI Agent hiển thị dạng **đánh số từ 1**, mỗi dòng kèm **icon theo đúng vai trò**
và mô tả chức năng ngắn gọn. Thứ tự: **ít quan trọng ở trên → quan trọng nhất ở dưới**.

Mở `index.html` bằng trình duyệt để xem. Sửa danh sách trong `agents.js`.

## Danh sách (copy để đặt lại tên từng agent)

| # | Agent | Vai trò / chức năng |
|---|-------|---------------------|
| 1 | 📚 AI agent học tập và đào tạo | Nội bộ: tự học, đào tạo nhân viên mới |
| 2 | 🎥 Video hướng dẫn curl Foxia API | Hướng dẫn kỹ thuật: gọi API Foxia bằng curl |
| 3 | 🩺 AI Agent video content sức khỏe | Sản xuất nội dung video chủ đề sức khỏe |
| 4 | 👩 Lady Page | Vận hành & trả lời fanpage thương hiệu |
| 5 | 📊 Cập nhật dữ liệu Fanpage Pancake | Đồng bộ dữ liệu fanpage từ Pancake về hệ thống |
| 6 | 🎬 Edivideo | Dựng & cắt video tự động |
| 7 | ✍️ AI viết kịch bản sale | Viết kịch bản bán hàng, content chốt đơn |
| 8 | 💬 Agen Zalo | Tư vấn & chăm khách trên Zalo |
| 9 | 🎧 AI chăm sóc khách hàng | CSKH sau bán, xử lý khiếu nại |
| 10 | 📞 Tổng hợp SĐT chưa chốt Pancake | Gom lead chưa chốt để gọi lại, remarketing |
| 11 | 🔁 Telegram bot kiểm tra trùng đơn | Chặn trùng đơn, cảnh báo tức thì qua Telegram |

Nhóm `mac` gồm các agent số 6–11; số thứ tự chạy liên tục qua các nhóm.

## Tên session trên Claude

Đã đổi tự động (7 session cloud):

| Vai trò | Tên session |
|---|---|
| Video content sức khỏe | `🩺 Video content sức khỏe — kịch bản & hook` |
| Fanpage thương hiệu | `👩 Lady Page — video & ads sản phẩm` |
| Đồng bộ dữ liệu | `📊 Fanpage Pancake — đồng bộ dữ liệu` |
| Bán hàng Zalo | `💬 Agen Zalo — tư vấn & chăm khách` |
| Chăm sóc sau bán | `🎧 CSKH — chăm sóc khách sau bán` |
| Chống trùng đơn | `🔁 Check trùng đơn — bot Telegram` |
| Giao diện danh sách | `🔢 Danh sách agent — icon & đánh số` |

Nhóm `mac` chạy trên máy cá nhân nên phải đổi tay — copy đúng các chuỗi sau:

```
🎬 Edivideo — dựng & cắt video tự động
✍️ Kịch bản sale — content chốt đơn
🎥 Curl Foxia API — hướng dẫn kỹ thuật
📚 Học tập & đào tạo — nội bộ
📞 SĐT chưa chốt Pancake — gom lead gọi lại
```

Lưu ý: số 1–9 hiện trong sidebar là **phím tắt theo vị trí**, không phải số đặt được;
sidebar cũng sắp theo lần dùng gần nhất, nên thứ tự ưu tiên xem ở bảng trên cùng file này.

## Cấu trúc

- `index.html` — khung sidebar
- `agents.js` — dữ liệu agent (icon, tên, vai trò, thứ tự)
- `app.js` — render danh sách, đánh số liên tục, chọn dòng
- `styles.css` — giao diện
