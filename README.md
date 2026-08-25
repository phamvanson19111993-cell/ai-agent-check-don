# ai-agent-check-don

Công cụ **kiểm tra đơn ("check đơn") và cập nhật Cơ hội** vào Odoo CRM tại
`ef.foxia.vn` — màn hình *Cơ hội đang hoạt động*
(`/odoo/cohoidanghoatdongs`, model `crm.lead`).

Kết nối Odoo qua **JSON-RPC**, hỗ trợ 2 cách xác thực:
1. **User + password/API key** (khuyến nghị, ổn định) — endpoint `/jsonrpc`.
2. **Cookie `session_id`** lấy từ trình duyệt — endpoint `/web/dataset/call_kw`.

## Cài đặt

```bash
pip install -r requirements.txt
cp .env.example .env      # rồi điền thông tin kết nối
```

Điền `.env`:
- `ODOO_URL=https://ef.foxia.vn`
- `ODOO_DB=<tên database>` (xem tại `/web/database/selector` hoặc hỏi quản trị)
- Cách 1: `ODOO_USERNAME`, `ODOO_PASSWORD` (mật khẩu hoặc API key)
- Cách 2: `ODOO_SESSION_ID` (dán từ cookie trình duyệt)

## Sử dụng

```bash
# Đếm số cơ hội đang hoạt động
python -m src.cli check

# Liệt kê 20 cơ hội gần nhất
python -m src.cli list --limit 20

# Import/cập nhật cơ hội từ file (khớp theo mã đơn -> upsert)
python -m src.cli import data/mau_don_hang.csv --dry-run   # xem trước
python -m src.cli import data/mau_don_hang.csv             # ghi thật
```

## Cấu trúc

| File | Vai trò |
|------|---------|
| `src/config.py` | Nạp cấu hình từ `.env` |
| `src/odoo_client.py` | Client JSON-RPC (login, search_read, create, write) + retry |
| `src/crm.py` | Nghiệp vụ Cơ hội: liệt kê / tạo / cập nhật / upsert |
| `src/orders.py` | Đọc đơn từ CSV/Excel & ánh xạ sang field `crm.lead` |
| `src/cli.py` | Giao diện dòng lệnh |
| `tests/` | Unit test offline (mock Odoo, không cần mạng) |

## Ánh xạ cột file → field Odoo

Sửa trong `src/orders.py` (`COLUMN_MAP`) cho khớp file thực tế của bạn.
Mặc định: `ma_don→name`, `khach_hang→contact_name`, `so_dien_thoai→phone`,
`email→email_from`, `doanh_thu→expected_revenue`, `ghi_chu→description`.
Khóa upsert: cột `ma_don` khớp với field `name`.

## Kiểm thử

```bash
python -m unittest discover -s tests -v
```

## Ghi chú
- Trong môi trường sandbox của Claude, domain `ef.foxia.vn` bị chặn bởi chính
  sách mạng nên không test online được — hãy chạy trên máy/môi trường của bạn.
- `crm.lead` có thể được đặt tên field khác trên bản Odoo tùy biến; nếu gặp lỗi
  field, kiểm tra lại tên field qua `ir.model.fields` hoặc giao diện Studio.
