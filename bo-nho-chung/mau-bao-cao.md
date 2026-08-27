# MẪU ĐƠN BÁO CÁO — nộp 3 lần mỗi ngày

Mọi phòng nộp báo cáo tiến độ vào **12h00 · 18h00 · 22h00** (giờ Việt Nam).
Tổng Chỉ Huy gom lúc 12h15 · 18h15 · 22h15 rồi tổng hợp một bản duy nhất cho anh Sơn.

## Nộp ở đâu

Ghi file vào **nhánh của chính phòng mình** (không đụng nhánh phòng khác):

```
bao-cao/<YYYY-MM-DD>-<12h|18h|22h>.md
```

Ví dụ: `bao-cao/2026-08-27-12h.md`

Rồi `git add` + `git commit` + `git push`. Tổng Chỉ Huy đọc bằng:
`git show origin/<nhánh>:bao-cao/<tên file>.md`

## Mẫu đơn — chép nguyên khung này

```markdown
# BÁO CÁO — Phòng <số> · <tên phòng>
Kỳ: <YYYY-MM-DD> <12h|18h|22h>   ·   Nhánh: <tên nhánh>

## 1. LÀM ĐƯỢC TỪ LẦN BÁO TRƯỚC
- <việc đã xong, kèm file/commit nếu có>

## 2. ĐANG LÀM
- <việc dở dang, còn bao nhiêu>

## 3. DỮ LIỆU MỚI TẠO RA  (để phòng khác dùng lại)
DATA UPDATE
- Loại dữ liệu:
- Giá trị:
- Kỳ:
- Nguồn:
- Thời gian cập nhật:
- Agent tạo: Phòng <số>
- Trạng thái xác minh: [Đã xác minh | Anh cung cấp, chưa đối chiếu | Suy ra, cần kiểm]

(Không có thì ghi: KHÔNG CÓ DỮ LIỆU MỚI)

## 4. ĐANG BỊ CHẶN — cần ai gỡ
- <việc đang kẹt> → cần: <anh Sơn | Phòng nào | dữ liệu gì>

## 5. CẦN DỮ LIỆU CỦA PHÒNG KHÁC
- Cần <dữ liệu gì> từ <phòng nào> — để làm <việc gì>

## 6. PHÁT HIỆN MÂU THUẪN
- <số/thông tin của em lệch với phòng nào, lệch chỗ nào>
(Không có thì ghi: KHÔNG PHÁT HIỆN)
```

## 4 luật khi viết báo cáo

1. **Không có việc thì ghi "không có"** — đừng chế việc cho đầy đơn.
2. **Số phải kèm nguồn.** Số không có nguồn thì ghi rõ "chưa xác minh".
3. **Không tự đoán số liệu.** Thiếu thì ghi `CHƯA ĐỦ DỮ LIỆU`.
4. **Ngắn.** Mục 1–2 mỗi mục tối đa 5 gạch đầu dòng. Đơn dài không giúp anh quyết nhanh hơn.
