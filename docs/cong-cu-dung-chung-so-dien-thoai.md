# Công cụ dùng chung — chuẩn hoá số điện thoại Việt Nam

Dành cho Phòng 10, Phòng 11, Phòng Ads và bất cứ phòng nào cần **khớp khách giữa
các nguồn**. Cùng một khách ghi `0913.351.394`, `+84 913 351 394`, `913351394`
là ba chuỗi khác nhau — chuẩn hoá xong mới so được.

- **Nguồn gốc:** `claude/fanpage-pancake-auto-update-iy8fuu` → `pancake_export/phones.py`
- **Phụ thuộc:** không có. Chỉ dùng thư viện chuẩn Python (`re`).
- **Không dính Pancake** — có 3 test khoá điều này (`tests/test_pancake_export.py`,
  lớp `TestPhonesDungChung`). Ai sửa làm nó dính lại là test đỏ ngay.

## Lấy về

```bash
git fetch origin claude/fanpage-pancake-auto-update-iy8fuu
git show origin/claude/fanpage-pancake-auto-update-iy8fuu:pancake_export/phones.py > phones.py
```

## Dùng trong code

```python
from phones import normalize, extract, extract_many

normalize("0913.351.394")        # '0913351394'
normalize("+84 913 351 394")     # '0913351394'
normalize("01682345678")         # '0382345678'  (đầu số 11 số cũ -> 10 số mới)
normalize("913351394")           # '0913351394'  (số mất số 0 đầu do Google Sheet)
normalize("đơn PKE1503852")      # None          (không phải SĐT)

extract("Bên Thịnh gọi mình số 0913.351.394")   # ['0913351394']
extract_many(record)             # dò trong dict/list lồng nhau, tự bỏ trùng
```

## Dùng ngoài dòng lệnh

```bash
python3 phones.py "0913.351.394" "+84 913 351 394"
# 0913.351.394        0913351394
# +84 913 351 394     0913351394
```

## Nó xử lý được gì

| Trường hợp | Vào | Ra |
|---|---|---|
| Dấu chấm / gạch / khoảng trắng | `0913.351.394`, `09666.111.04` | `0913351394`, `0966611104` |
| Mã quốc gia | `+84 913 351 394`, `84913351394` | `0913351394` |
| Đầu số 11 số cũ (đổi 2018) | `01682345678`, `01234567890` | `0382345678`, `0834567890` |
| Mất số 0 đầu (lỗi Google Sheet) | `913592043` | `0913592043` |
| Số cố định | `02439998888` | giữ nguyên |
| Không phải SĐT | mã đơn `PKE1503852`, ngày `12.08.2026` | `None` |

**Liên quan mâu thuẫn MT-14:** các sheet cũ trên Drive lưu SĐT mất số 0 đầu.
Chạy `normalize()` trước khi so khớp thì hai bên khớp lại được — đừng so chuỗi thô.
