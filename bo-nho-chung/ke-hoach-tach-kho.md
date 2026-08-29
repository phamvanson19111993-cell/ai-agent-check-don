# KẾ HOẠCH TÁCH KHO — mỗi phòng một kho riêng

> Anh Sơn chốt 28/08/2026: tách các phòng ban ra kho riêng biệt.

## ⛔ Em không tự tạo kho được

Quyền GitHub của Tổng Chỉ Huy bị chặn ở bước tạo kho:
`403 Resource not accessible by integration`.

**Anh phải bấm tạo kho.** Mỗi kho khoảng 20 giây. Sau đó em đẩy mã sang, việc đó em làm được.

## ⚠️ HAI ĐIỀU PHẢI BIẾT TRƯỚC KHI TÁCH

### 1. Tách kho KHÔNG tự chuyển phiên AI

Sidebar Claude nhóm phiên **theo kho lúc phiên được lập**. Tạo kho mới **không** kéo các phiên
hiện có sang. Muốn mỗi phòng nằm dưới kho riêng trong sidebar thì phải **lập phiên mới**.

Lập phiên mới nghĩa là:
- Phòng đó **mất toàn bộ bối cảnh** đã tích luỹ (Phòng 7 riêng đã tiêu hơn 386 đô công)
- **Toàn bộ lịch báo cáo phải dựng lại** — lịch gắn với mã phiên, không gắn với kho

→ **Đây là cái giá thật.** Tách kho để dọn mã thì đáng; tách kho để dọn sidebar thì trả giá đắt.

### 2. Bộ nhớ chung phải đổi cách đọc

Bot Phòng 9 đang đọc thẳng `origin/claude/dilim-ai-command-center-yy5uvo:bo-nho-chung/...`.
Sang kho khác thì đường dẫn đó chết, bot câm về sản phẩm.

**Cách giữ:** bộ nhớ chung ở lại **một kho duy nhất** (kho Tổng Chỉ Huy), các phòng đọc chéo kho.
Đọc chéo kho riêng tư cần khoá truy cập — thêm một thứ phải cấp và phải giữ.

## Danh sách kho cần tạo

Tất cả để **Private**. Kho hiện tại đang **công khai** và lịch sử git còn số điện thoại khách thật.

| # | Tên kho đề nghị | Nội dung | Dung lượng |
|---|---|---|---|
| 1 | `dilim-phong-06-video-suc-khoe` | Kịch bản, 60 hook, bộ soát tuân thủ | 0,2 MB · 47 file |
| 2 | `dilim-phong-07-lady-page` | Trang bán, ảnh nhãn, video phản hồi | **70,8 MB** · 71 file |
| 3 | `dilim-phong-08-fanpage-pancake` | Đường ống kéo đơn, chuẩn hoá SĐT | 0,1 MB · 26 file |
| 4 | `dilim-phong-09-agen-zalo` | Bot Zalo OA, trình đọc bộ nhớ chung | 0,1 MB · 45 file |
| 5 | `dilim-phong-10-cskh` | Thư viện tin nhắn, kịch bản chốt đơn | 0,2 MB · 20 file |
| 6 | `dilim-phong-11-check-trung-don` | Bot Telegram chặn trùng đơn | 0,0 MB · 20 file |
| 7 | `dilim-phong-12-ads` | 10 playbook, máy tính đơn hàng | 0,1 MB · 24 file |
| 8 | `dilim-tong-chi-huy` | **Bộ nhớ chung** — kho gốc, các phòng đọc về đây | 0,1 MB · 27 file |

Kho `dilim-phong-07-lady-page` nặng 70,8 MB vì chứa video phản hồi — bình thường, nhưng biết trước để khỏi bất ngờ.

## Anh làm gì

1. GitHub → **New repository** → dán tên ở cột 2 → chọn **Private** → **Create**.
   Không tích "Add a README" — để trống, em đẩy mã vào.
2. Làm xong bao nhiêu kho thì báo em bấy nhiêu, em đẩy mã sang ngay.
3. Kho cũ `ai-agent-check-don`: **chuyển sang Private** — lịch sử git vẫn còn số điện thoại khách thật.

## Em đề nghị làm theo thứ tự này

**Bước 1 — làm trước, không rủi ro:** tạo 8 kho, em đẩy mã sang. Mã có nhà riêng, nhìn là rõ.
**Bước 2 — cân nhắc riêng:** có chuyển phiên AI sang kho mới không. Cái này mất bối cảnh và
phải dựng lại toàn bộ lịch báo cáo, nên đừng làm cùng lúc với bước 1.
