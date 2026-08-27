# BỘ NHỚ CHUNG — DILIM AI

Đây là **nơi duy nhất** các phòng AI lấy dữ liệu của nhau.
Trước khi hỏi anh bất cứ điều gì, agent phải đọc ở đây trước.

## Vì sao có thư mục này

Trước đây 11 phòng nằm trên 11 nhánh git riêng, không phòng nào thấy phòng nào.
Kết quả: cùng một sản phẩm được mô tả 3 kiểu khác nhau, và **cùng một câu hỏi
bị hỏi đi hỏi lại** ở từng phòng — tốn tiền, tốn thời gian của anh.

Bộ nhớ chung chỉ có vài file nhỏ. Agent đọc 1 file thay vì quét 13 nhánh.

## Luật dùng — 4 điều

1. **ĐỌC TRƯỚC KHI HỎI.** Mở `index.json` → tra loại dữ liệu cần → mở đúng file.
   Chỉ khi bộ nhớ chung không có mới được hỏi anh.
2. **KHÔNG COPY SỐ RA CHỖ KHÁC.** Cần giá thì trỏ về file gốc, đừng chép lại —
   chép là ngày mai lệch.
3. **TẠO DỮ LIỆU MỚI PHẢI GHI LẠI** theo mẫu `DATA UPDATE` bên dưới, rồi push lên `main`.
4. **KHÔNG TỰ ĐỔI TRẠNG THÁI THÀNH "Đã xác minh".** Chỉ anh hoặc nguồn hệ thống mới xác minh được.

## Mẫu DATA UPDATE

```
DATA UPDATE
- Loại dữ liệu:
- Giá trị:
- Kỳ:
- Nguồn:
- Thời gian cập nhật:
- Agent tạo:
- Trạng thái xác minh:   [Đã xác minh | Anh cung cấp, chưa đối chiếu | Suy ra, cần kiểm]
```

## Có gì trong đây

| File | Nội dung | Ai cần |
|---|---|---|
| `index.json` | Mục lục máy đọc — tra "cần X → mở file nào" | Mọi agent, đọc đầu tiên |
| `00-ban-do-he-thong.md` | 13 nhánh có gì, dùng lại được gì | Agent muốn tìm code/tài liệu có sẵn |
| `san-pham/rich-coenzyme-q10.md` | Hồ sơ sản phẩm chuẩn — giá, quy cách, liều | Sale, CSKH, Ads, Video |
| `luat-tuan-thu.md` | Được nói / không được nói + cảnh báo tương tác | Mọi phòng viết nội dung |
| `mau-thuan-dang-mo.md` | Chỗ dữ liệu đang lệch nhau, chưa chốt | Tổng Chỉ Huy, trước khi kết luận |

## 🔒 CAM KẾT ĐƯỜNG DẪN — Tổng Chỉ Huy không được đổi tuỳ tiện

Phòng 9 đã viết bot **đọc thẳng** hai file dưới đây lúc chạy, theo đúng đường dẫn:

```
bo-nho-chung/san-pham/rich-coenzyme-q10.md
bo-nho-chung/luat-tuan-thu.md
```

**Đổi tên hoặc di chuyển hai file này = bot mất hồ sơ và tự câm về sản phẩm.**
Tổng Chỉ Huy cam kết giữ nguyên đường dẫn; nếu buộc phải đổi thì **báo trước cho các phòng**.

## ♻️ Công cụ dùng chung — đừng viết lại

| Công cụ | Của phòng | Lấy về |
|---|---|---|
| **Đọc bộ nhớ chung lúc chạy** — `git show`, cache 15 phút, đọc hỏng thì giữ bản cũ | Phòng 9 | `git show origin/claude/agen-zalo-3780k7:src/knowledge/sharedMemory.js` — copy nguyên file, không dính phần Zalo |
| **Bộ soát tuân thủ tự động** — 5 luật chặn câu sai giá / sai liệu trình / sai thành phần | Phòng 6 | `python -m agent.cli check <file>` — chạy trên file markdown bất kỳ, không cần khoá API |
| **Chuẩn hoá số điện thoại Việt Nam** — khôi phục số 0 đầu, đầu số 11 số cũ | Phòng 8 | `git show origin/claude/fanpage-pancake-auto-update-iy8fuu:pancake_export/phones.py` |

## Câu dán vào đầu mỗi phòng

Xem `prompts/moi-phong-doc-dau-phien.md` — dán 1 lần vào mỗi agent,
từ đó nó tự đọc bộ nhớ chung thay vì hỏi lại anh.
