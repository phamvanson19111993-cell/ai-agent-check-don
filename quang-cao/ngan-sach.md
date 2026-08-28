# NGÂN SÁCH ĐẶT BAO NHIÊU CHO ĐÚNG
Phòng 7 · 28/08/2026 · tính ngược từ số thật, không đoán

---

## Trước hết: em nhận sai

Câu **"một nhóm vượt quá 150.000đ/ngày là ngân sách bị đặt sai"** là **em viết sai.**

Con số 150.000đ đó em đặt trong `tao-chien-dich.py` từ hồi **chưa có một dữ liệu nào** — nó chỉ là số tròn cho dễ nhìn. Nay có số thật thì phải tính lại, và tính ra thì **188.912đ hôm qua mới là đúng**, còn 150.000đ là chậm.

Đã sửa lại trong `tao-chien-dich.py`, kèm ghi chú vì sao.

---

## Số thật làm gốc

| | |
|---|---|
| Chi ngày 27/08 | 224.227đ |
| Lượt xem trang đích | 235 |
| **Giá mỗi lượt xem** | **954đ** |
| Đơn | 0 |

*(tài khoản 2260044828113956)*

---

## Ngân sách phải trả lời được hai câu hỏi khác nhau

### Câu 1 — Đủ để Meta học chưa?

Meta cần **~50 sự kiện tối ưu mỗi tuần** mới thoát giai đoạn học.

| Sự kiện tối ưu | Cần mỗi ngày |
|---|---|
| Lượt xem trang đích *(đang chạy)* | 6.815đ |
| CompleteRegistration | 20.446đ |
| InitiateCheckout | 68.154đ |

Ngưỡng này **thấp**. Không phải chỗ cần lo.

### Câu 2 — Đủ để biết trang có chốt được không?

Đây mới là câu tốn tiền. Hiện **235 lượt, 0 đơn** — chưa kết luận được gì.

| Chạy tới | Tốn | Nếu tỷ lệ chốt thật 0,5% thì xác suất vẫn 0 đơn |
|---|---|---|
| 500 lượt | 477.079đ | 8,2% |
| **1.000 lượt** | **954.157đ** | **0,7%** |
| 2.000 lượt | 1.908.315đ | 0,0% |

**Chọn mốc 1.000 lượt.** Tới đó mà vẫn 0 đơn thì chỉ còn 0,7% khả năng là do may rủi — nghĩa là **trang hoặc lời chào hàng có vấn đề, không phải quảng cáo**.

---

## Con số đúng

| Muốn có kết luận trong | Ngân sách/ngày |
|---|---|
| 3 ngày | 318.052đ |
| **5 ngày** | **190.831đ ← chọn cái này** |
| 7 ngày | 136.308đ |
| 10 ngày | 95.416đ |

> # 190.000đ mỗi ngày

**Vì sao 5 ngày:**
- Chậm hơn → thị trường và mùa vụ đổi, số đo mất nghĩa
- Nhanh hơn 3 ngày → Meta chưa kịp thoát giai đoạn học, giá đội lên

**Đối chiếu:** 188.912đ hôm qua → 5,1 ngày là xong. **Anh đặt đúng.** 150.000đ của em → 6,4 ngày, chậm hơn mà chẳng được gì.

---

## Cách chia 190.000đ

| Quảng cáo | Tỷ lệ | đ/lượt | Xử lý |
|---|---|---|---|
| Doanh số mới **1** | 1,26% | 1.541đ | **TẮT** — z=4,14, kém thật |
| Doanh số mới **2** | 3,19% | 706đ | giữ |
| Doanh số mới | 3,05% | 954đ | giữ |

Mẫu 2 và mẫu 3 **không khác nhau về mặt thống kê** (3,19% với 814 hiển thị, so 3,05% với 6.489). Mẫu 2 rẻ hơn có thể chỉ là may — mới 26 sự kiện. **Giữ cả hai, để Meta tự chia.**

Đặt ngân sách **ở cấp nhóm quảng cáo (ABO)**, đừng đặt ở cấp chiến dịch (CBO) trong lúc thử. CBO sẽ dồn tiền vào một mẫu trước khi mẫu kia kịp có đủ dữ liệu.

---

## Mốc dừng — quyết định trước, không quyết định lúc đang xót tiền

Khi cộng đủ **1.000 lượt xem trang đích** *(tính từ hôm nay 28/08, vì trước đó đo sai)*:

| Kết quả | Làm gì |
|---|---|
| **≥ 3 đơn** | Tỷ lệ chốt ≥0,3%. Tăng ngân sách, leo lên tối ưu CompleteRegistration |
| **1–2 đơn** | Sát biên. Chạy thêm 1.000 lượt nữa rồi mới quyết |
| **0 đơn** | **Dừng tiền.** Vấn đề nằm ở trang hoặc ở lời chào hàng, đổ thêm tiền không cứu được |

> **Lưu ý quan trọng:** đếm lại từ 0 kể từ **28/08**. Toàn bộ 235 lượt và 224.227đ trước đó chạy trong lúc pixel báo sai giá trị và đơn không chảy vào bảng nào — số đó không dùng để kết luận về tỷ lệ chốt được.

---

## Trần tuyệt đối — không bao giờ vượt

Theo giả định giá vốn 50%, trần hoà vốn cho **một đơn**:

| Mốc | Trần hoà vốn/đơn | Mục tiêu 5% của anh |
|---|---|---|
| 1 hộp | 1.445.000đ | 144.500đ |
| 2 hộp | 2.890.000đ | 289.000đ |
| 6 hộp | 7.225.000đ | 867.000đ |

Chi phí mỗi đơn vượt cột **trần hoà vốn** là đang lỗ thật, tắt ngay.
Vượt cột **mục tiêu 5%** mà chưa vượt trần thì vẫn lãi — chỉ là chưa đạt mục tiêu, đừng vội tắt.
