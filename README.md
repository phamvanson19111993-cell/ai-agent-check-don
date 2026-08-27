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

## DILIM AI Command Center

Sổ 11 phòng ở trên là **ai đang chạy**. Command Center là **cách 8 phòng chuyên môn phối hợp**:
AI Tổng Chỉ Huy nhận yêu cầu → chọn phòng → thu thập dữ liệu → kiểm tra nguồn →
phát hiện mâu thuẫn → giao phân tích → kiểm toán chéo → mới kết luận.

Mở `command-center.html` để xem sơ đồ. Prompt gốc: `prompts/dilim-tong-chi-huy.md`.

| Phòng | Chuyên môn | Agent đang bơm dữ liệu |
|---|---|---|
| 1 | 🗄️ Data Center — dữ liệu gốc, ưu tiên số thực tế | 📊 Fanpage Pancake · 📞 SĐT chưa chốt · 🔁 Check trùng đơn |
| 2 | 📜 Chính sách & Hoa hồng | ⚠️ chưa có |
| 3 | 📞 Sale — lead, tỷ lệ chốt, AOV | ✍️ Kịch bản sale · 📞 SĐT chưa chốt · 💬 Agen Zalo |
| 4 | 📣 Marketing & Ads — CPL, ROAS | 🩺 Video sức khỏe · 👩 Lady Page · 🎬 Edivideo |
| 5 | 🌐 Đại lý & Hệ thống — F1, F2 | ⚠️ chưa có |
| 6 | 🎧 CSKH — tái mua, khiếu nại | 🎧 CSKH · 💬 Agen Zalo |
| 7 | 💰 Tài chính — dòng tiền, lợi nhuận | ⚠️ chưa có |
| 8 | 🔍 AI Kiểm toán — chốt chặn độc lập | 🔁 Check trùng đơn (một phần) |

**3 phòng chưa có agent phụ trách: Chính sách & Hoa hồng, Đại lý & Hệ thống, Tài chính.**
Chừng nào chưa có, mọi câu hỏi về hoa hồng / F1–F2 / lợi nhuận đều phải lấy số từ anh và ghi rõ
trạng thái *"Chưa đối chiếu hệ thống"* — không được coi là đã xác minh.

### Bộ nhớ chung — nơi các AI lấy dữ liệu của nhau

Trước đây 11 phòng nằm trên 11 nhánh git riêng, không phòng nào thấy phòng nào, nên cùng
một câu hỏi bị hỏi lại ở từng phòng. `bo-nho-chung/` sửa đúng chỗ đó:

| File | Nội dung |
|---|---|
| `bo-nho-chung/index.json` | Mục lục máy đọc — agent đọc đầu tiên, tra "cần X → mở file nào" |
| `bo-nho-chung/00-ban-do-he-thong.md` | 13 nhánh có gì, phòng nào đang giữ code/tài liệu nào |
| `bo-nho-chung/san-pham/rich-coenzyme-q10.md` | Hồ sơ chuẩn — giá, quy cách, liều (lấy từ trang bán đang chạy) |
| `bo-nho-chung/luat-tuan-thu.md` | Được nói / không được nói + cảnh báo tương tác thuốc |
| `bo-nho-chung/mau-thuan-dang-mo.md` | Chỗ dữ liệu đang lệch nhau, chưa chốt |
| `prompts/moi-phong-doc-dau-phien.md` | Câu dán 1 lần vào mỗi phòng để nó tự đọc bộ nhớ chung |

### 3 luật cứng

1. **Một dữ liệu — một nguồn chính thức.** Trí nhớ AI không phải nguồn.
2. **Thiếu dữ liệu thì ghi `CHƯA ĐỦ DỮ LIỆU ĐỂ KẾT LUẬN`** và chỉ rõ đang thiếu gì — không suy đoán.
3. **Hai phòng lệch số thì không tự chọn** — báo `PHÁT HIỆN MÂU THUẪN DỮ LIỆU` và trình bày cả hai nguồn.

## Cấu trúc

- `index.html` — trang sổ phòng
- `agents.js` — dữ liệu 11 phòng (icon, tên, vai trò, nơi chạy, trạng thái, link session)
- `app.js` — render, đánh số Phòng 1 → N
- `command-center.html` — sơ đồ 8 phòng chuyên môn & quy trình 8 bước
- `departments.js` — dữ liệu 8 phòng, 8 bước, thứ tự ưu tiên dữ liệu
- `command-center.js` — render trang Command Center
- `prompts/dilim-tong-chi-huy.md` — **bản gốc prompt AI Tổng Chỉ Huy** (sửa ở đây trước)
- `prompts/moi-phong-doc-dau-phien.md` — câu dán vào từng phòng
- `bo-nho-chung/` — **bộ nhớ chung**: mục lục, bản đồ hệ thống, hồ sơ sản phẩm, luật tuân thủ, sổ mâu thuẫn
- `styles.css` — giao diện chung, có sẵn nền sáng/tối
