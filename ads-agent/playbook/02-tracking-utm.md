# 02 — TRACKING & UTM

## Chuỗi phải thông

```
Meta Ads → LadiPage → Pixel → Lead Event → CRM/Sheet → Sale gọi → Đơn hàng → CAPI Purchase về Meta
```

Đứt ở đâu thì mù ở đó. Chưa thông **không được scale**.

## A. Gắn Pixel vào LadiPage

1. Vào **Events Manager** trên Meta → **Data sources** → chọn Pixel → copy **Pixel ID**.
2. Trong LadiPage: mở trang → **Cài đặt trang** → tab **Chuyển đổi / Tracking**.
3. Dán **Pixel ID** vào ô Facebook Pixel. Lưu → **Xuất bản** lại trang.
4. Nếu LadiPage không có ô riêng: dán đoạn mã Pixel vào phần **Javascript `<head>`** của trang.

## B. Bắn event `Lead` khi submit form

1. Trong LadiPage, chọn **nút submit** của form → **Hành động sau khi gửi**.
2. Chọn thêm hành động **Chạy Javascript** (hoặc gắn vào trang cảm ơn).
3. Đoạn cần chạy:

```html
<script>
  if (typeof fbq === 'function') {
    fbq('track', 'Lead', { content_name: 'ĐĂNG KÝ TƯ VẤN', value: 0, currency: 'VND' });
  }
</script>
```

4. Nếu có trang cảm ơn riêng: cách chắc chắn hơn là bắn `Lead` ngay khi trang cảm ơn load —
   khách chỉ tới được trang đó khi đã gửi form thật.

## C. Kiểm tra (bắt buộc, đừng tin là xong)

1. Events Manager → chọn Pixel → tab **Test Events**.
2. Copy link LadiPage, mở trên **điện thoại**, điền form thật, bấm gửi.
3. Trong Test Events phải thấy lần lượt: `PageView` → `Lead`.
4. Không thấy `Lead` → kiểm tra theo thứ tự: trang đã xuất bản lại chưa → Pixel ID đúng chưa →
   script gắn đúng nút submit chưa → có chặn bởi trình duyệt/adblock không (thử trình duyệt khác).

## D. Conversion API — nâng cấp đáng làm nhất

Pixel bị mất tín hiệu do iOS/adblock. CAPI gửi dữ liệu từ **server**, không bị chặn.

Mức tối thiểu nên làm: khi sale **chốt đơn**, đẩy event `Purchase` (kèm `value`) hoặc
`Lead` chất lượng (Qualified Lead) từ CRM/Google Sheet về Meta qua CAPI.

Hiệu quả: Meta ngừng tối ưu tìm "người thích điền form" và bắt đầu tìm **người giống người đã mua**.
Đây thường là đòn bẩy giảm CAC mạnh hơn mọi việc chỉnh target.

Cách làm thực tế nhất khi chưa có dev: Google Sheet chứa đơn → tự động hoá (Zapier/Make/Apps Script)
→ gọi Conversion API endpoint của Meta. Cần: Pixel ID + Access Token (tạo trong Events Manager →
Settings → Conversions API → Generate access token).

## E. UTM

Gắn vào ô **Website URL** của từng ad (hoặc ô URL parameters):

```
utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}
```

Trong LadiPage, thêm **trường ẩn** trong form để hứng các tham số này (LadiPage hỗ trợ điền tự động
trường ẩn theo query string). Kết quả: mỗi dòng lead trong Sheet/CRM có sẵn cột
`utm_campaign`, `utm_content`, `utm_term`.

**Đây là thứ trả lời câu hỏi quan trọng nhất:** creative nào ra ĐƠN, không phải creative nào ra FORM.

## F. Cột tối thiểu của bảng lead

| Thời gian | SĐT | Tên | utm_campaign | utm_content | utm_term | Nghe máy | Đủ ĐK | Chốt | Giá trị đơn | Ghi chú sale |
|---|---|---|---|---|---|---|---|---|---|---|

Không có 4 cột `utm_*` + `Nghe máy` + `Chốt` thì agent không phân tích chất lượng lead được,
chỉ phân tích được số bề mặt trên Ads Manager.
