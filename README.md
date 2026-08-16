# AI Agent dọn rác máy tính

Agent quét và dọn file rác trên máy bạn, chạy liên tục theo chu kỳ. Thiết kế theo
nguyên tắc **không bao giờ làm mất dữ liệu**: mặc định chỉ báo cáo, khi dọn thật thì
chuyển vào khu cách ly có thể khôi phục, và có hàng rào chặn cứng những thư mục quan trọng.

Chạy được trên Linux, macOS và Windows. Không cần thư viện ngoài (Python 3.11+).

## Cài đặt

```bash
git clone https://github.com/phamvanson19111993-cell/ai-agent-check-don.git
cd ai-agent-check-don
pip install -e .

# Nếu muốn dùng thêm tầng đánh giá bằng Claude:
pip install -e ".[ai]"
```

## Dùng nhanh

```bash
cleaner-agent init      # tạo file cấu hình mẫu
cleaner-agent scan      # xem có gì để dọn — KHÔNG đụng vào file nào
cleaner-agent rules     # xem các quy tắc đang bật

cleaner-agent clean --apply   # dọn thật (file vào khu cách ly)
cleaner-agent status          # xem khu cách ly đang giữ gì
cleaner-agent restore <id>    # lấy lại một mục đã dọn nhầm
```

## Chạy liên tục

```bash
cleaner-agent watch --apply           # chạy nền trong terminal, mặc định 60 phút/lượt
cleaner-agent install-service --apply --write   # cài chạy cùng hệ điều hành
```

`install-service` sinh cấu hình phù hợp với máy bạn:

| Hệ điều hành | Cơ chế | Bật |
|---|---|---|
| Linux | systemd user unit | `systemctl --user enable --now cleaner-agent` |
| macOS | launchd agent | `launchctl load -w ~/Library/LaunchAgents/com.local.cleaner-agent.plist` |
| Windows | Task Scheduler | lệnh `schtasks` được in ra màn hình |

## Ba lớp an toàn

**1. Chặn cứng (`safety.py`).** Mọi ứng viên đều phải qua `Guard.check()` trước khi bị đụng tới.
Bị chặn tuyệt đối: thư mục hệ thống (`/etc`, `C:\Windows`, `/usr`…), `Documents`, `Desktop`,
`Pictures`, `Videos`, `Music`, `.ssh`, `.gnupg`, `.aws`, mọi thứ trong cây `.git`, file có
đuôi nhạy cảm (`.pem`, `.key`, `.kdbx`, `.sqlite`…), symlink, và file khoá của tiến trình đang chạy.

**2. Cách ly thay vì xoá (`quarantine.py`).** "Xoá" nghĩa là chuyển vào
`~/.local/share/cleaner-agent/quarantine` kèm sổ ghi đường dẫn gốc. Sau `retention_days`
(mặc định 7 ngày) mới xoá hẳn. Trong thời gian đó `cleaner-agent restore <id>` đưa file về chỗ cũ.

**3. Chạy thử là mặc định.** `dry_run = true` trong config. Phải chủ động thêm `--apply`
hoặc sửa config thì agent mới động vào file. Kèm trần số lượng (5000 mục) và dung lượng
(20 GB) mỗi lượt để một lỗi cấu hình không thể quét sạch máy.

## Quy tắc nhận diện rác

Chỉ nhắm vào những thứ **máy tự tạo lại được**: cache ứng dụng, thumbnail, thùng rác quá hạn,
file tạm, cache trình duyệt, crash dump, cache của pip/npm/yarn, cache Zalo. Mỗi quy tắc có
ngưỡng tuổi riêng — file mới sửa gần đây không bao giờ bị đụng.

Xem danh sách đầy đủ bằng `cleaner-agent rules`. Tắt bớt trong config:

```toml
[rules]
disabled = ["browser-cache", "trash"]
enabled_extra = ["empty-dirs"]
```

## Tầng đánh giá bằng Claude (tuỳ chọn)

Với những thư mục "khó xử" như `~/Downloads` — nơi lẫn lộn giữa file cài đặt đã dùng xong và
tài liệu quan trọng — quy tắc cứng không đủ. Bật `[ai]` để Claude phân loại:

```toml
[ai]
enabled = true
model = "claude-opus-5"
review_roots = ["~/Downloads"]
min_age_days = 30
```

Cần biến môi trường `ANTHROPIC_API_KEY`.

**Về riêng tư:** agent chỉ gửi *metadata* — đường dẫn, tên file, phần mở rộng, kích thước,
số ngày kể từ lần sửa cuối. Nội dung file không bao giờ được đọc hay gửi đi.

Claude trả về `junk` / `keep` / `review` kèm độ tin cậy. Chỉ những mục `junk` với độ tin cậy
≥ 0.8 mới được dọn; mọi trường hợp còn lại được giữ nguyên. Nếu gọi API thất bại, toàn bộ
được giữ lại — lỗi không bao giờ dẫn tới xoá nhầm.

Khi `[ai]` tắt, agent bỏ qua hoàn toàn các thư mục trong `review_roots`.

## Về ảnh Zalo

Agent tách bạch hai thứ hay bị gộp làm một:

- **`zalo-cache`** (bật sẵn) — ảnh xem trước, thumbnail, media Zalo tự tải về để hiển thị.
  Đây là rác thật: xoá đi Zalo tự tải lại khi cần. Thường chiếm vài trăm MB đến vài GB.
- **`zalo-media`** (tắt sẵn) — thư mục *Zalo Received Files*, tức ảnh và file người khác gửi
  cho bạn. **Đây là dữ liệu cá nhân, không phải rác.** Xoá đi là mất, Zalo không giữ bản sao
  vĩnh viễn trên máy chủ.

Muốn dọn nhóm thứ hai, bạn phải làm ba việc có chủ đích — **sau khi đã tự sao lưu**:

```toml
[safety]
unprotect = ["~/Documents/Zalo Received Files"]

[rules]
enabled_extra = ["zalo-media"]

[ai]
enabled = true
review_roots = ["~/Documents/Zalo Received Files"]
```

Rồi chạy `cleaner-agent scan` để **xem danh sách trước**, đối chiếu xem có ảnh nào bạn còn cần
không, rồi mới `clean --apply`. Kể cả lúc đó file vẫn vào khu cách ly 7 ngày.

Dọn cache Zalo trước đã — thường chỉ riêng nó đã nhẹ máy đáng kể mà không mất gì:

```bash
cleaner-agent scan
```

## Cấu hình

File tại `~/.config/cleaner-agent/config.toml`, sinh ra bằng `cleaner-agent init`.

```toml
[general]
dry_run = true                 # false = dọn thật
interval_minutes = 60          # chu kỳ ở chế độ watch
max_delete_per_run = 5000
max_bytes_per_run = 21474836480
min_free_gb = 0                # >0: chỉ dọn khi đĩa còn trống ít hơn mức này

[quarantine]
enabled = true
retention_days = 7

[safety]
extra_protected = []           # thêm thư mục cấm đụng
unprotect = []                 # gỡ bảo vệ một thư mục cá nhân cụ thể
```

## Cấu trúc mã nguồn

```
src/cleaner_agent/
├── safety.py      # hàng rào chặn cứng — tầng phòng thủ cuối
├── rules.py       # quy tắc nhận diện rác theo hệ điều hành
├── scanner.py     # duyệt cây thư mục, lọc theo tuổi và quy tắc
├── ai.py          # phân loại bằng Claude cho vùng khó xử
├── quarantine.py  # cách ly, khôi phục, xoá hẳn khi quá hạn
├── cleaner.py     # điều phối một lượt dọn
├── daemon.py      # vòng lặp chạy liên tục
├── scheduler.py   # cài dịch vụ hệ điều hành
├── report.py      # hiển thị và lưu báo cáo
└── cli.py         # dòng lệnh
```

## Kiểm thử

```bash
pip install -e ".[dev]"
pytest
```

Bộ test tập trung vào phần quan trọng nhất: hàng rào an toàn (không cho đụng `Documents`,
khoá SSH, cây `.git`, thư mục hệ thống), vòng đời cách ly/khôi phục, và việc `dry_run`
thật sự không đụng vào file nào.
