# LUẬT TỰ LẤY THÔNG TIN

> **Anh Sơn ra lệnh 27/08/2026:** khi anh hỏi, **các phòng TỰ đi lấy thông tin của nhau.**
> Không hỏi lại anh thứ phòng khác đã có. Không ngồi chờ Tổng Chỉ Huy chuyển tin.

## Bốn bước bắt buộc — làm đúng thứ tự

**Bước 1 — Mở mục lục bộ nhớ chung.**
```bash
git fetch origin claude/dilim-ai-command-center-yy5uvo
git show origin/claude/dilim-ai-command-center-yy5uvo:bo-nho-chung/index.json
```
Tra loại dữ liệu cần trong mục `tra_cuu` → mở đúng file. **Phần lớn câu hỏi dừng ở đây.**

**Bước 2 — Không có trong bộ nhớ chung thì tra bản đồ, sang thẳng nhánh phòng giữ nó.**
```bash
git show origin/claude/dilim-ai-command-center-yy5uvo:bo-nho-chung/00-ban-do-he-thong.md
git show origin/<nhánh phòng đó>:<đường dẫn file>
```
Không phải xin phép ai. Không phải nhờ Tổng Chỉ Huy chuyển. **Tự lấy.**

**Bước 3 — Vẫn không có thì kiểm tra `chua_co_nguon` trong `index.json`.**
Nếu dữ liệu nằm trong danh sách đó → trả lời anh đúng câu này:
```
CHƯA ĐỦ DỮ LIỆU ĐỂ KẾT LUẬN
Đang thiếu: <tên dữ liệu>
Ai cấp được: <anh Sơn / phòng nào>
```
Và ghi vào mục 5 đơn báo cáo kỳ tới.

**Bước 4 — Chỉ hỏi anh Sơn khi dữ liệu thật sự không tồn tại ở đâu trong hệ thống.**

## Ba điều CẤM

1. **Cấm hỏi anh thứ mà phòng khác đã có.** Anh phải trả lời hai lần cùng một câu là hệ thống hỏng.
2. **Cấm bịa để lấp chỗ trống.** Thiếu thì nói thiếu.
   **Và cấm ghi "0" khi chưa đo** — không có số thì ghi "chưa có số". *"Không thấy"* khác
   *"bằng không"*. Ghi 0 là khẳng định một phép đo mình chưa làm. (Thêm 29/08 sau MT-20.)
3. **Cấm ngồi chờ.** Tổng Chỉ Huy không phải người đưa thư — phòng tự đi lấy.

## DANH BẠ — cần gì, lấy ở đâu

Tiền tố chung: `git show origin/<nhánh>:<file>`

| Cần gì | Lấy ở đâu |
|---|---|
| **Giá, mốc combo, quà tặng, quy cách, thành phần, số công bố, nhà sản xuất, công dụng được nói** | `claude/dilim-ai-command-center-yy5uvo` → `bo-nho-chung/san-pham/rich-coenzyme-q10.md` |
| **Luật tuân thủ, câu cấm, cảnh báo tương tác thuốc** | cùng nhánh → `bo-nho-chung/luat-tuan-thu.md` |
| **Giá vốn, biên lãi từng mốc, ngưỡng ROAS hoà vốn** | cùng nhánh → `bo-nho-chung/tai-chinh/gia-von-va-nguong-roas.md` |
| **Dữ liệu đang lệch nhau, việc đang treo** | cùng nhánh → `bo-nho-chung/mau-thuan-dang-mo.md` |
| **Hook, kịch bản video, personas, format** | `claude/ai-agent-health-video-content-rmedj9` → `knowledge/hooks.json`, `docs/10-hook-manh-nhat.md`, `scripts/` |
| **Bộ soát tuân thủ tự động** (chạy được trên file markdown bất kỳ) | cùng nhánh → `python -m agent.cli check <file>` |
| **Trang bán, ảnh nhãn phụ, giấy công bố, ảnh hộp Nhật, script tạo chiến dịch Meta** | `claude/dilim-one-website-es08sj` → `index.html`, `images/`, `tao-chien-dich.py` |
| **794 số khách chưa chốt · chuẩn hoá số điện thoại Việt Nam** | `claude/fanpage-pancake-auto-update-iy8fuu` → `pancake_export/phones.py`, `tools/gom_data.py` |
| **Trình đọc bộ nhớ chung lúc bot đang chạy** (copy nguyên file, không dính Zalo) | `claude/agen-zalo-3780k7` → `src/knowledge/sharedMemory.js` |
| **Thư viện tin nhắn, kịch bản chốt đơn, upsell, chu kỳ chăm sóc 10 ngày** | `claude/zalo-customer-care-messaging-uj9q4i` → `docs/thu-vien-tin-nhan.md`, `docs/kich-ban-upsell-crosssell.md` |
| **10 playbook chạy ads, máy tính kinh tế đơn hàng, bộ chiến dịch sẵn bấm** | `claude/meta-ads-performance-agent-on9nn7` → `ads-agent/AGENT.md`, `ads-agent/playbook/`, `ads-agent/chien-dich/` |
| **Bot chặn trùng đơn Telegram, userscript bắt số trên Facebook** | `claude/telegram-duplicate-order-bot-ayyubm` → `bot.py`, `userscript/` |

## Khi lấy được của phòng khác

- **Không chép số sang nhánh mình.** Trỏ về nguồn gốc. Chép là ngày mai lệch.
- Cần dùng lúc chạy chương trình thì **đọc thẳng** như Phòng 9 đã làm (`sharedMemory.js`).
- Thấy số của phòng khác **lệch** số của mình → **không tự chọn bên nào**, ghi vào mục 6 đơn báo cáo.
- Lấy về dùng thì **ghi rõ nguồn** khi trả lời anh: *"số này lấy từ hồ sơ chuẩn / từ Phòng 7"*.
