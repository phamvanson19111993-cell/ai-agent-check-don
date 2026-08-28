# Hướng dẫn thao tác thật trên Zalo PC

> Dành cho tài khoản **Phạm Sơn – Sống Khoẻ Mỗi Ngày** (DILI Supplement).
> Ngành thực phẩm chức năng, khách phần lớn lớn tuổi → xưng hô **"em – cô/chú"**.

---

## 1. Chuẩn hoá cách đặt tên hội thoại

Anh đang đặt tên kiểu: `<Tên khách> <SĐT> <ngày> hẹn <ngày>` — cách này đúng hướng rồi,
chỉ cần thống nhất lại thành **1 công thức cố định** để tìm kiếm nhanh:

```
[Tên] [SĐT] [Ngày liên hệ cuối] [Trạng thái]
```

**Bộ trạng thái nên dùng (chỉ 6 cái, không thêm):**

| Trạng thái | Nghĩa | Chu kỳ nhắn |
|---|---|---|
| `Mới` | Vừa để lại thông tin, chưa tư vấn | 3–5 ngày |
| `Tiềm năng` | Đã tư vấn, chưa chốt | 7 ngày |
| `Đã mua` | Đang dùng sản phẩm | 10 ngày |
| `Liệu trình` | Đang theo liệu trình dài | 10 ngày |
| `Ngủ đông` | Trên 60 ngày không mua lại | 20–30 ngày |
| `Dừng` | Khách yêu cầu không nhắn nữa | ❌ không nhắn |

Ví dụ: `Nguyễn Văn A 09xxxxxxxx 23/08 Tiềm năng` · `Trần Thị B 09xxxxxxxx 23/08 Liệu trình`

> ⚠️ **Repo này công khai** — ví dụ trong tài liệu phải là tên và số giả.
> Tên khách thật, số thật chỉ nằm trong Zalo và bảng tính riêng của anh, không đưa lên đây.

**Lợi ích:** gõ `Tiềm năng` vào ô Tìm kiếm là ra hết khách cần chăm hôm đó.

> 💡 Đổi tên: chuột phải hội thoại → **Đổi tên gợi nhớ** (không ảnh hưởng tên thật của khách).

---

## 2. Dùng "Phân loại" (thẻ màu) — anh đã có sẵn ở góc phải

Nút **Phân loại** trên thanh danh sách hội thoại cho phép gắn thẻ màu. Nên tạo đúng 5 thẻ:

| Màu | Thẻ | Dùng cho |
|---|---|---|
| 🔴 Đỏ | Cần chăm hôm nay | Khách tới hạn 10 ngày |
| 🟡 Vàng | Tiềm năng | Chưa chốt đơn |
| 🟢 Xanh lá | Đang dùng liệu trình | Khách đã mua |
| 🔵 Xanh dương | VIP / khách sỉ | Ưu tiên báo hàng mới |
| ⚪ Xám | Ngủ đông | Giãn lịch |

Mỗi sáng chỉ cần lọc thẻ 🔴 là biết phải nhắn ai.

---

## 3. Tin nhắn nhanh (đỡ gõ lại 100 lần)

Zalo PC có **Tin nhắn nhanh**: gõ `/` trong khung chat → hiện danh sách mẫu đã lưu.

Nên lưu sẵn các mẫu hay dùng nhất (lấy từ [`thu-vien-tin-nhan.md`](./thu-vien-tin-nhan.md)):

| Phím tắt | Nội dung |
|---|---|
| `/chao` | Mẫu hỏi thăm đầu tuần |
| `/hoithamsk` | Hỏi tình trạng sức khoẻ sau khi dùng sản phẩm |
| `/nhaclieutrinh` | Nhắc sắp hết liệu trình |
| `/lehoi` | Chúc dịp lễ |
| `/camon` | Cảm ơn – xin đánh giá |

⚠️ **Dán mẫu xong PHẢI sửa ít nhất 1 chi tiết** (tên cô/chú, triệu chứng đang gặp, tuần dùng thứ mấy).
Zalo phát hiện tin trùng lặp gửi hàng loạt → dễ bị hạn chế tài khoản.

---

## 4. Quy trình 15 phút mỗi sáng

```
1. Chạy script    → python3 scripts/lich_cskh.py data/khach_hang.csv
                    (ra danh sách ai tới hạn hôm nay + gợi ý nội dung)
2. Mở Zalo PC     → lọc thẻ 🔴 Cần chăm hôm nay
3. Nhắn từng khách → gõ / lấy mẫu, SỬA cho riêng khách đó, gửi
4. Gửi rải        → mỗi tin cách nhau 20–40 giây, KHÔNG gửi liên tiếp
5. Cập nhật lại   → đổi ngày trong tên hội thoại + sửa CSV
```

**Khung giờ tốt cho khách lớn tuổi:** 8h30–10h30 sáng và 19h30–21h tối.
Tránh giờ trưa (11h30–14h) vì các cô chú hay nghỉ.

---

## 5. ⚠️ Lưu ý riêng cho ngành thực phẩm chức năng

Đây là phần quan trọng nhất, ảnh hưởng pháp lý:

**KHÔNG được nhắn:**
- ❌ "Sản phẩm chữa khỏi bệnh …" / "điều trị dứt điểm"
- ❌ "Thay thế thuốc" / "không cần uống thuốc nữa"
- ❌ Cam kết khỏi trong bao nhiêu ngày
- ❌ Khoe ảnh/lời chứng thực của bệnh nhân như bằng chứng chữa bệnh

**NÊN nhắn:**
- ✅ "Cô dùng được 2 tuần rồi, cô thấy người mình thế nào ạ?"
- ✅ "Cô nhớ uống đều và đủ nước giúp em nha ạ"
- ✅ "Cô vẫn uống thuốc bác sĩ kê bình thường nha cô, cái này chỉ hỗ trợ thêm thôi ạ"

Khi giới thiệu sản phẩm, giữ đúng câu bắt buộc:
> *"Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."*

---

## 6. Chống bị khoá / hạn chế tài khoản

| Việc nên tránh | Vì sao |
|---|---|
| Gửi cùng 1 nội dung cho 20+ người trong ít phút | Dấu hiệu spam rõ nhất |
| Kết bạn hàng loạt người lạ | Dễ bị báo cáo |
| Nhắn cho người chưa từng liên hệ | Khách bấm "Báo xấu" |
| Nhắn sau 22h | Khách khó chịu → chặn |
| Tiếp tục nhắn khi khách đã từ chối | Lý do bị khoá phổ biến nhất |

**Nguyên tắc an toàn:** khách không phản hồi 3 lượt liên tiếp → giãn xuống 30 ngày.
Khách nói "đừng nhắn nữa" → đổi trạng thái thành `Dừng`, ngừng hẳn.

---

## 7. Nếu muốn gửi tự động thật sự

Zalo cá nhân **không có API chính thức** — mọi công cụ "gửi tin hàng loạt Zalo cá nhân"
đều là tool lách, rủi ro **mất tài khoản**. Con đường hợp lệ duy nhất:

| Kênh | Dùng để | Ghi chú |
|---|---|---|
| **Zalo OA** (Official Account) | Nhắn tin chăm sóc chính thức | Cần đăng ký, xác thực doanh nghiệp |
| **ZNS** (Zalo Notification Service) | Gửi tin theo mẫu đã duyệt | Trả phí/tin, mẫu phải được Zalo duyệt trước |

Tin hỏi thăm – chúc mừng kiểu tâm tình như trong playbook này thì **nhắn tay qua Zalo cá nhân
vẫn hiệu quả hơn nhiều**, vì khách cảm nhận được là người thật quan tâm.
Script trong repo này đóng vai trò **nhắc việc**, không thay anh bấm gửi.
