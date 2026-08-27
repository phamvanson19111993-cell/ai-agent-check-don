# BẢN ĐỒ HỆ THỐNG — 13 nhánh, phòng nào đang giữ gì

Đọc file này trước khi định làm mới bất cứ thứ gì. **Phần lớn đã có người làm rồi.**
Muốn lấy: `git fetch origin && git show <nhánh>:<đường dẫn file>`

| Phòng / Nhánh | Đã có sẵn | Dùng lại được gì |
|---|---|---|
| **Sơ đồ phòng** `main` | `index.html`, `agents.js`, `app.js` | Sổ 11 phòng, trang chủ |
| **Tổng Chỉ Huy** `claude/dilim-ai-command-center-yy5uvo` | `prompts/dilim-tong-chi-huy.md`, `command-center.html`, `departments.js`, **`bo-nho-chung/`** | Prompt điều phối + bộ nhớ chung này |
| **🩺 Video sức khoẻ** `claude/ai-agent-health-video-content-rmedj9` | `knowledge/` (hooks, personas, formats, CTA, products, compliance), `docs/10-hook-manh-nhat.md`, agent Python | **Ngân hàng hook** — Ads đừng viết lại từ đầu |
| **👩 Lady Page** `claude/dilim-one-website-es08sj` | Trang bán hoàn chỉnh, ảnh, video phản hồi, `APPS-SCRIPT.gs`, `tao-chien-dich.py` | **Giá & hồ sơ sản phẩm gốc** · script tạo chiến dịch Meta |
| **🌐 Web đang chạy** `web` | Bản deploy + `CNAME` + GitHub Pages workflow + Pixel `1440077257813466` | Trang thật khách đang thấy |
| **📊 Fanpage Pancake** `claude/fanpage-pancake-auto-update-iy8fuu` | `pancake_export/` (client, exporter, sheets, tagging, phones), cài đặt 1 lệnh | **Đường ống kéo đơn về Sheets** — Data Center dùng cái này |
| **🔁 Check trùng đơn** `claude/telegram-duplicate-order-bot-ayyubm` | `bot.py`, `phone_utils.py`, `sheet_store.py`, userscript, bản cài Mac/Win | **Chuẩn hoá số điện thoại** — dùng chung để khớp khách giữa các phòng |
| **💬 Agen Zalo** `claude/agen-zalo-3780k7` | Agent Node.js đầy đủ, `get-token.js`, `docs/SETUP-ZALO.md` | Khung agent + lấy refresh token Zalo OA |
| **🎧 CSKH** `claude/zalo-customer-care-messaging-uj9q4i` | `playbook-cskh-zalo-10-ngay.md`, `thu-vien-tin-nhan.md`, `kich-ban-upsell-crosssell.md`, `lich_cskh.py` | **Thư viện tin nhắn + kịch bản upsell** |
| **📣 Ads (Phòng 12)** `claude/meta-ads-performance-agent-on9nn7` | `ads-agent/AGENT.md` + **10 playbook** + `unit-economics.html` | Sổ tay chạy ads + máy tính kinh tế đơn hàng |
| **🧹 Dọn rác máy** `claude/alo-03rc3e` | `cleaner_agent` Python + test | Agent dọn máy, chạy nền |
| **🤖 Auto-grab đơn** `claude/new-session-cz7pol` | `grabber.py`, `odoo_client.py`, `crm.py` + test | Nối CRM/Odoo |

## ⚠️ Ba điều anh cần biết ngay

**1. Không nhánh nào được gộp về `main`.**
`main` chỉ có 5 file (trang sổ phòng). Toàn bộ ~250 file công việc thật nằm rải trên 12 nhánh
chưa merge. Đây là lý do gốc khiến các AI không thấy nhau — không phải vì AI kém.

**2. Có Phòng 12 nhưng sổ chỉ ghi 11.**
Nhánh `meta-ads-performance-agent-on9nn7` tự đánh số "Phòng 12 · AI Ads Manager" và sửa
`agents.js` riêng. Sổ trên `main` vẫn 11 phòng. **Hai bản sổ đang lệch nhau.**

**3. Phòng 11 (Check trùng đơn) đang HỎNG.**
Phiên chạy bằng model Fable 5 và đã chạm giới hạn: *"You've reached your Fable 5 limit"*.
Muốn chạy tiếp phải đổi model cho phòng đó.

## Hai nhánh chưa có trong sổ 11 phòng

`claude/alo-03rc3e` (dọn rác máy) và `claude/new-session-cz7pol` (auto-grab đơn / Odoo)
— có code, có test, nhưng không phòng nào trong sổ trỏ tới. Anh quyết định: đưa vào sổ hay bỏ.
