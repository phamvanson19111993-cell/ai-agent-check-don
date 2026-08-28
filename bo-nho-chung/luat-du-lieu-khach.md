# LUẬT DỮ LIỆU KHÁCH — repo này CÔNG KHAI

> Kiểm ngày 28/08/2026: `phamvanson19111993-cell/ai-agent-check-don` có `private: false`.
> **Ai trên Internet cũng đọc được mọi file trong mọi nhánh.**

## Cấm tuyệt đối đưa vào repo

- Tên khách hàng thật
- Số điện thoại thật
- Địa chỉ thật
- **Ảnh bill chuyển khoản** (có tên chủ tài khoản, số tài khoản, số dư)
- Ảnh chụp màn hình có thông tin khách
- Token, khoá API, mã bot Telegram, chuỗi kết nối

Kể cả trong file báo cáo, file mẫu, file test, hay ví dụ trong README.

## Đơn hàng thật đi đường nào

```
Khách bấm gửi trên trang
        ↓
   Apps Script (/exec) — giữ khoá bí mật ở phía máy chủ
        ↓
   Telegram riêng của anh Sơn   ←  đơn đầy đủ + ảnh bill nằm ở ĐÂY
        ↓
   Bảng tính Google riêng       ←  lưu trữ, đối chiếu
```

**Repo chỉ nhận CON SỐ, không nhận NGƯỜI.**

| Được ghi trong báo cáo | Không được ghi |
|---|---|
| “3 đơn trong giờ qua” | tên, số điện thoại, địa chỉ của 3 người đó |
| “1 đơn mốc 6 hộp, 17.340.000đ” | ảnh bill, số tài khoản người gửi |
| “đơn lúc 14h05 chưa khớp bill” | nội dung chuyển khoản có tên khách |
| “khách hỏi về giảm tiền mặt” | đoạn chat có tên và số của khách |

Cần trỏ tới một đơn cụ thể thì dùng **mã đơn hoặc giờ**, không dùng tên người.

## Ví dụ trong tài liệu phải là số giả

Dùng dạng `09xxxxxxxx` hoặc số rõ ràng là giả (`0901234567`).
**Không lấy số của khách thật làm ví dụ test**, kể cả trong README hay file cài đặt.

## Hai chỗ đang rò, phát hiện 28/08

| Nơi | Rò gì | Trạng thái |
|---|---|---|
| `bo-nho-chung/mau-thuan-dang-mo.md` (nhánh Tổng Chỉ Huy) | 1 số điện thoại thật | ✅ đã che 28/08 |
| Nhánh `claude/telegram-duplicate-order-bot-ayyubm` — `README.md`, `bot.py`, `cai_dat.bat`, `chan_doan.command` | **tên khách + số điện thoại thật** dùng làm ví dụ `/check` | ❌ chưa sửa — phòng đó đang chết vì hết hạn mức model |

> ⚠️ **Xoá khỏi file KHÔNG xoá khỏi lịch sử git.** Số đã đẩy lên vẫn nằm trong các commit cũ và
> vẫn đọc được từ Internet. Cách dứt điểm duy nhất là **chuyển repo sang riêng tư**
> (GitHub → Settings → General → Danger Zone → Change visibility → Private).
> Việc này không ảnh hưởng gì tới các phòng AI — chúng vẫn đọc ghi bình thường.
