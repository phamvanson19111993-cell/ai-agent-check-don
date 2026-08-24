# ai-agent-check-don

Lấy **số điện thoại của khách trên Pancake chưa gắn nhãn `CHỐT ĐƠN`**, lưu ra CSV
và tự đẩy lên Google Sheet trên Drive.

Page mặc định: `1121021804424838` — *Bùi Phúc Thịnh - Tim Mạch Não Bộ*.
Sheet mặc định: [SĐT chưa chốt Pancake - 3 tháng gần nhất](https://docs.google.com/spreadsheets/d/1_SjwNvfzPMUzAjeDJ46MmCsSXYcmZ_cggj6NKz5kJjk/edit).

## Cài đặt

Chỉ cần Python 3.8 trở lên, không bắt buộc cài thư viện nào:

```bash
git clone <repo> && cd ai-agent-check-don
cp .env.example .env      # điền API key Pancake vào đây
```

Lấy API key: **Pancake → Cấu hình → Cấu hình ứng dụng → Webhook & API Key**.

## Dùng hằng ngày

```bash
# Quét 3 ngày gần nhất, ghi ra data/sdt_chua_chot.csv
python3 -m pancake_export

# Lấy đúng khoảng ngày (ví dụ từ 16/8 đến 23/8)
python3 -m pancake_export --since 16/08/2026 --until 23/08/2026

# Quét xong đẩy luôn lên Google Sheet trên Drive
python3 -m pancake_export --days 7 --drive

# Chạy nền, cứ 30 phút tự cập nhật một lần
python3 -m pancake_export --watch 30 --drive
```

Xem trước danh sách nhãn của page để chắc chắn tên nhãn đúng:

```bash
python3 -m pancake_export --list-tags
```

## Chạy tự động mỗi ngày

Cài 1 lệnh, sau đó máy tự chạy và tự ghi lên Google Sheet, không phải bấm tay.

**Windows** — nháy đúp `caidat.bat` (hoặc `caidat.bat 07:00` để đổi giờ).

**macOS / Linux:**

```bash
chmod +x caidat.sh
./caidat.sh          # 8h sáng mỗi ngày
./caidat.sh 7        # đổi sang 7h sáng
./caidat.sh 8 --go   # cài xong chạy thử luôn
```

Lần đầu chạy, nó tạo file `.env` và dừng lại nhắc anh dán API key Pancake vào —
dán xong chạy lại là chạy được. Cài lại nhiều lần cũng không bị trùng lịch.

| Việc | macOS / Linux | Windows |
|---|---|---|
| Xem lịch | `crontab -l` | `schtasks /query /tn "PancakeChuaChot"` |
| Chạy thử ngay | `./chay_hang_ngay.sh` | `schtasks /run /tn "PancakeChuaChot"` |
| Xem nhật ký | `tail -f data/nhat_ky.log` | mở `data\nhat_ky.log` |
| Gỡ lịch | `crontab -e` rồi xoá dòng | `schtasks /delete /tn "PancakeChuaChot" /f` |

Mỗi lần chạy quét 2 ngày gần nhất (phòng hội thoại cập nhật muộn) và chỉ thêm số
mới — chạy lại bao nhiêu lần cũng không sinh dòng trùng.

## Không có API key thì làm sao?

Xuất danh sách hội thoại/khách hàng từ Pancake ra file rồi đưa cho công cụ đọc —
không cần API:

```bash
python3 -m pancake_export --from-file pancake_export.csv --drive
```

Công cụ tự dò các cột *Tên / Số điện thoại / Nhãn / Ngày*, kể cả file `.xlsx`
(cần `pip install openpyxl`).

## Cách nó lọc

| Bước | Xử lý |
|---|---|
| 1 | Duyệt hội thoại của page theo khoảng thời gian |
| 2 | Bỏ hội thoại đã gắn nhãn `CHỐT ĐƠN` (không phân biệt hoa thường/dấu, khớp cả “Đã chốt đơn”) |
| 3 | Lấy SĐT: ưu tiên số Pancake lưu sẵn, không có thì dò trong nội dung chat |
| 4 | Chuẩn hoá số VN: `0913.351.394`, `+84 913 351 394`, đầu số 11 số cũ → `0913351394` |
| 5 | Bỏ số trùng, ghi ra CSV theo layout `Tên / SĐT / Tình trạng / Ngày / Ghi chú` |

Chạy lại nhiều lần **không ghi đè**: file CSV và Google Sheet chỉ được **thêm số
mới**, ghi chú anh tự sửa trong file vẫn giữ nguyên.

## Tuỳ chọn hay dùng

| Cờ | Ý nghĩa |
|---|---|
| `--days N` / `--since` / `--until` | Khoảng thời gian quét |
| `--closed-tag "TÊN NHÃN"` | Đổi nhãn coi là đã chốt (lặp lại được cho nhiều nhãn) |
| `--yellow` | Coi mọi nhãn màu vàng là nhãn chốt đơn |
| `--deep` | Mở thêm tin nhắn để dò SĐT khi hội thoại chưa có số (chậm hơn) |
| `--drive` | Đẩy kết quả lên Google Sheet |
| `--watch N` | Tự chạy lại mỗi N phút |
| `--out FILE` | Đổi nơi lưu CSV |

## Ghi lên Google Sheet

1. Tạo **service account** trên Google Cloud, tải file JSON credentials về máy.
2. Điền đường dẫn file đó vào `GOOGLE_SERVICE_ACCOUNT_FILE` trong `.env`.
3. Mở Google Sheet → **Chia sẻ** cho email service account, quyền **Editor**.
4. Chạy kèm cờ `--drive`.

Số điện thoại được ghi dạng chữ nên **không bị mất số 0 đầu** như file cũ.

## Kiểm thử

```bash
python3 -m unittest discover -s tests -v
```
