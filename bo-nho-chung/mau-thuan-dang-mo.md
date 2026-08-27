# MÂU THUẪN ĐANG MỞ — chưa chốt, không phòng nào được tự chọn

Theo Bước 5 quy trình Tổng Chỉ Huy: hai nguồn lệch nhau thì **dừng kết luận, đối chiếu**.
Phát hiện ngày 27/08/2026 khi quét toàn bộ 13 nhánh.

---

## MT-01 · Dạng hoạt chất CoQ10 — ⚠️ ảnh hưởng trực tiếp tới câu chốt đơn

| Nguồn | Nói gì |
|---|---|
| Trang bán đang chạy (`web`) | **Dạng khử (ubiquinol)** — khẳng định chắc, dùng làm lý do giải thích chênh giá |
| Phòng CSKH — `ho-so-san-pham-Rich-Coenzyme-Q10.md` | **Dạng khử (ubiquinol)** ✅ khớp |
| Phòng Video — `knowledge/products.json` | `"Coenzyme Q10 (ubiquinone/ubiquinol)"` — **không chốt dạng nào** |

**Rủi ro:** video nói một đằng, trang bán nói một nẻo, khách so ra là mất tin.
**Đề xuất:** lấy theo trang bán (dạng khử), sửa `products.json`. **Cần anh xác nhận đúng nhãn.**

---

## MT-02 · Thành phần bổ sung — chỉ 1 nguồn nhắc tới

Phòng CSKH ghi có **tinh chất thìa là đen + vi tảo**. Trang bán và Phòng Video **không nhắc**.
→ Hoặc trang bán thiếu điểm bán tốt, hoặc CSKH đang nói thừa. **Cần anh xác nhận theo nhãn.**

---

## MT-03 · Sổ 11 phòng hay 12 phòng

`main` ghi 11 phòng. Nhánh Ads tự thêm "Phòng 12 · AI Ads Manager" và sửa `agents.js` riêng.
Hai file `agents.js` sẽ đụng nhau khi merge. **Cần anh chốt: Ads là Phòng 12 hay thay chỗ phòng khác.**

---

## MT-04 · CSKH đang tư vấn khách mà không có giá

Hồ sơ CSKH để trống 🟡 ở: giá lẻ, giá liệu trình, quy cách, liều dùng —
trong khi trang bán **đã có đủ** từ lâu. Phòng CSKH cũng đang đứng chờ anh gửi
"payment info + biểu mẫu" từ 25/08.

**Đã xử lý một phần:** `san-pham/rich-coenzyme-q10.md` giờ có đủ giá và quy cách.
**Còn thiếu thật:** thông tin thanh toán (số tài khoản), biểu mẫu đặt hàng.

---

## Chưa có nguồn nào — không phòng nào giữ

| Dữ liệu | Hậu quả khi thiếu |
|---|---|
| **Chính sách hoa hồng + ngày hiệu lực** | Không trả lời được câu "anh có được hoa hồng không" |
| **Doanh số cá nhân / F1 / F2 / hệ thống** | Không tính được hoa hồng, không đánh giá được đại lý |
| **Giá vốn mỗi hộp** | Không ra lợi nhuận, Ads không biết ngưỡng ROAS hoà vốn |
| **Chi phí Ads thực tế** | ROAS chỉ là ước lượng |
| **Số công bố sản phẩm** | Khách hỏi giấy tờ là bí |
