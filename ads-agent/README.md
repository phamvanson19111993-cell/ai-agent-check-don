# 📈 Phòng 12 — AI Ads Manager

Agent chạy quảng cáo Meta, viết creative và **kiểm soát quảng cáo cùng anh** cho mô hình:

```
Facebook / Instagram Ads → LadiPage → Form → Lead → Sale gọi → Đơn hàng → Doanh thu
```

Khác với một AI "viết content quảng cáo": agent này ra **quyết định** — GIỮ / TẮT / TEST / SCALE / SỬA —
và mọi quyết định đều quy về một câu hỏi: **đơn này có lãi không.**

---

## Dùng trong 3 bước

**Bước 1 — Nạp não.**
Copy toàn bộ [`AGENT.md`](AGENT.md) dán vào Custom Instructions của Claude / ChatGPT
(hoặc tạo một Project riêng và đặt file này làm chỉ dẫn).

**Bước 2 — Nạp bối cảnh.**
Điền [`playbook/01-brief.md`](playbook/01-brief.md) rồi gửi cho agent. Ô nào chưa biết ghi `?`.

**Bước 3 — Làm việc hằng ngày.**
Sáng gửi số liệu theo mẫu trong [`playbook/10-nhip-lam-viec.md`](playbook/10-nhip-lam-viec.md),
hoặc chụp thẳng màn hình Ads Manager gửi vào — agent tự đọc số trong ảnh.

---

## Hỏi được những gì

| Muốn gì | Nhắn thế nào |
|---|---|
| Dựng chiến dịch mới | "Dựng campaign cho [sản phẩm], ngân sách [x]/ngày" |
| Viết content | "Viết 3 primary text theo angle Sai lầm phổ biến" |
| Kịch bản video | "Viết kịch bản 45 giây angle Chuyên gia giải thích" |
| Đọc báo cáo | Gửi ảnh Ads Manager → "Ad nào giữ, ad nào tắt?" |
| Chẩn đoán | "CPL 30k mà 2 ngày không có đơn, lỗi ở đâu?" |
| Thao tác | Gửi ảnh màn hình → "Bấm đâu để gắn UTM?" |
| Kiểm claim | "Câu này có bị Meta chặn không?" |
| Trước khi tăng tiền | "Đủ điều kiện scale chưa?" |

---

## Máy tính kinh tế đơn hàng

[`tools/unit-economics.html`](tools/unit-economics.html) — mở bằng trình duyệt.

Nhập giá bán, giá vốn, ship, hoa hồng, tỷ lệ bom hàng, chi phí ads, số lead, số đơn →
ra ngay **CAC hoà vốn**, **CPL hoà vốn**, **Profit ROAS** và một quyết định kèm lý do.

> Đây là thứ phải có trước mọi câu "CPL này rẻ hay đắt". Không có ngưỡng hoà vốn thì
> mọi nhận xét về giá lead đều là cảm tính.

---

## Sổ tay

| File | Nội dung |
|---|---|
| [`AGENT.md`](AGENT.md) | System prompt đầy đủ — bộ não của agent |
| [`01-brief.md`](playbook/01-brief.md) | Bảng thông tin phải điền trước khi chạy |
| [`02-tracking-utm.md`](playbook/02-tracking-utm.md) | Pixel, event `Lead`, Conversion API, UTM, cột bảng lead |
| [`03-angle-hook-content.md`](playbook/03-angle-hook-content.md) | 10 angle, 12 khung hook, primary text, headline, CTA |
| [`04-kich-ban-video.md`](playbook/04-kich-ban-video.md) | Khung video + 3 kịch bản mẫu |
| [`05-cau-truc-campaign.md`](playbook/05-cau-truc-campaign.md) | Cấu trúc campaign, đặt tên, ngân sách, lịch test 7 ngày |
| [`06-doc-so-lieu-chan-doan.md`](playbook/06-doc-so-lieu-chan-doan.md) | Bảng triệu chứng → nghi phạm → hành động |
| [`07-scale-retargeting.md`](playbook/07-scale-retargeting.md) | Checklist scale, 6 nhóm retargeting |
| [`08-landing-page.md`](playbook/08-landing-page.md) | Chấm điểm LadiPage 16 mục |
| [`09-claim-tpcn.md`](playbook/09-claim-tpcn.md) | Câu cấm, bảng viết lại an toàn cho TPCN |
| [`10-nhip-lam-viec.md`](playbook/10-nhip-lam-viec.md) | Nhịp sáng / tuần / tháng |

---

## Ba luật agent không được phá

1. **Không bịa số.** Thiếu dữ liệu thì nói "chưa đủ dữ liệu" và hỏi đúng chỉ số còn thiếu.
2. **CPL rẻ không phải thắng.** Chỉ CAC dưới ngưỡng hoà vốn mới là thắng.
3. **TPCN: hỗ trợ ≠ điều trị.** Câu nào rủi ro thì cảnh báo và viết lại bản an toàn ngay.
