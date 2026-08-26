# 06 — ĐỌC SỐ LIỆU & CHẨN ĐOÁN FUNNEL

## A. Đọc theo tầng — tìm tầng rơi mạnh nhất

```
Impression
   ↓ CTR (link)              ← creative / hook / angle
Click
   ↓ Click → LP View         ← tốc độ trang, link hỏng, tracking
Landing Page View
   ↓ LP View → Lead (CVR)    ← offer, headline, form, trust, mobile UX
Lead
   ↓ Tỷ lệ nghe máy          ← chất lượng số, tốc độ gọi, giờ gọi
Nghe máy
   ↓ Tỷ lệ đủ điều kiện      ← đúng tệp target chưa
Đủ điều kiện
   ↓ Tỷ lệ chốt              ← kịch bản sale, giá, offer
Đơn
   ↓ Tỷ lệ giao thành công   ← COD bom hàng, xác nhận đơn
Doanh thu thật
```

Điểm nghẽn = tầng có tỷ lệ rơi bất thường nhất so với chính lịch sử tài khoản.
**Không so với benchmark trên mạng.**

## B. Bảng triệu chứng → nghi phạm → hành động

| Triệu chứng | Nghi phạm | Hành động |
|---|---|---|
| **CPM cao** | Tệp quá hẹp · creative bị chấm điểm thấp · mùa cạnh tranh · placement xấu | Mở rộng tệp về broad · làm creative mới · bật Advantage+ placements |
| **CTR thấp** | Hook yếu · angle sai người · visual nhạt | Thay 3 giây đầu · đổi angle · thử format khác (ảnh ↔ video) |
| **CTR tốt nhưng CPC cao** | CPM cao kéo theo | Xem lại CPM, không phải lỗi creative |
| **CPC tốt nhưng ít LP View** | Trang tải chậm · link sai · pixel không bắn PageView · click nhầm (clickbait) | Test tốc độ trang trên 4G · bấm thử link · kiểm tra Test Events |
| **LP View nhiều, ít Lead** | Offer yếu · headline không khớp quảng cáo · form dài · thiếu bằng chứng · mobile UX xấu | Đồng bộ thông điệp ads ↔ LP · rút form còn Tên + SĐT · thêm proof · xem `08-landing-page.md` |
| **CPL rẻ nhưng không có đơn** | Sai tệp · số rác · form quá dễ điền · sale gọi chậm · kịch bản sale sai | **Không scale.** Đối chiếu bảng lead theo `utm_content` · siết lại angle để lọc người · rút thời gian gọi |
| **Có đơn nhưng lãi mỏng** | CAC cao · AOV thấp · COGS/ship cao · bom hàng COD · hoa hồng | Tăng AOV bằng combo/upsell · giảm bom hàng bằng xác nhận đơn · tính lại Profit ROAS |
| **Đang tốt rồi tụt dần** | Creative mỏi (frequency tăng, CTR giảm) · cạnh tranh tăng | Nạp creative mới cùng angle thắng · làm mới hook |
| **Số nhảy loạn sau khi chỉnh** | Bị đẩy về learning | Ngừng chỉnh, chờ ổn định rồi mới đọc |

## C. Khi nhận screenshot Ads Manager

Agent tự đọc số trong ảnh, không bắt gõ lại. Trả về:

```
WINNER : [tên ad] — vì sao
LOSER  : [tên ad] — vì sao
Từng dòng: GIỮ / TẮT / TEST / SCALE / SỬA + lý do một dòng
Chỉ số ảnh không có mà cần hỏi thêm: [...]
```

Chỉ số ảnh Ads Manager **không bao giờ có**, phải hỏi người dùng:
tỷ lệ nghe máy · lead đủ điều kiện · số đơn thật · doanh thu thật · tỷ lệ giao thành công.

## D. Không kết luận khi

- Ad chưa tiêu đủ ≈ 1× CAC hoà vốn.
- Vừa chỉnh ngân sách/target trong 48–72h qua (đang learning).
- Đang trong đợt biến động bên ngoài (lễ, sale sàn, sự kiện) mà chưa loại trừ.
- Chưa đối chiếu bảng lead — số trên Ads Manager mới là **một nửa sự thật**.

Khi rơi vào các trường hợp trên, câu trả lời đúng là:
*"Chưa đủ dữ liệu để kết luận — cần thêm [X]."*
