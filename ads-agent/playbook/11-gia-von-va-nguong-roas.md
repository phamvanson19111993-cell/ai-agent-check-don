# 11 — GIÁ VỐN & NGƯỠNG ROAS (Rich Coenzyme Q10)

> ## ⚠️ SỐ GIẢ ĐỊNH — CHƯA XÁC MINH
>
> | | |
> |---|---|
> | Giá bán 1 hộp | **2.890.000đ** — đã xác minh (nguồn: trang bán đang chạy) |
> | Giá vốn 1 hộp | **1.445.000đ** — **GIẢ ĐỊNH 50%**, anh Sơn đặt, **chưa đối chiếu hoá đơn nhập** |
> | Kỳ | 08/2026 · cập nhật 27/08/2026 |
> | Nguồn gốc | Phòng Tổng Chỉ Huy — `bo-nho-chung/tai-chinh/gia-von-va-nguong-roas.md` |
>
> Bản gốc: `git show origin/claude/dilim-ai-command-center-yy5uvo:bo-nho-chung/tai-chinh/gia-von-va-nguong-roas.md`

## Ba luật bắt buộc khi Phòng Ads dùng số này

1. **Ghi kèm giả định.** Mọi kết luận, báo cáo, khuyến nghị ngân sách có dùng số này phải kèm câu
   *"theo giả định giá vốn 50%"*. Không trình bày như số đã xác minh.
2. **ROAS 2,0 là SÀN TUYỆT ĐỐI, không phải mốc an toàn.** Bảng dưới mới trừ giá vốn hàng.
   Không được khuyến nghị chạy ở ROAS 2,2–2,5 như thể đang lãi.
3. **Máy tính phải hiện cảnh báo trên màn hình** — người mở `tools/unit-economics.html`
   phải thấy ngay, không cần đọc code mới biết. (Đã làm.)

## Bảng lãi gộp

| Mốc | Doanh thu | Hộp phải giao | Giá vốn | Lãi gộp | Biên | Trần chi phí ads mỗi đơn |
|---|---|---|---|---|---|---|
| 1 hộp | 2.890.000đ | 1 | 1.445.000đ | **1.445.000đ** | 50,0% | 1.445.000đ |
| 3 hộp | 8.670.000đ | 3 | 4.335.000đ | **4.335.000đ** | 50,0% | 4.335.000đ |
| 5 hộp | 14.450.000đ | 5 | 7.225.000đ | **7.225.000đ** | 50,0% | 7.225.000đ |
| 6 hộp | 17.340.000đ | **7** *(tặng 1)* | 10.115.000đ | **7.225.000đ** | **41,7%** | 7.225.000đ |

**ROAS hoà vốn** = 1 ÷ biên lãi gộp → **2,00** ở mốc 1·3·5 · **2,40** ở mốc 6.

## 🔍 Mốc 5 và mốc 6 lãi gộp Y HỆT NHAU

Cả hai đều **7.225.000đ**. Hộp thứ 6 mang về đúng 1.445.000đ lãi, hộp thứ 7 tặng đi tốn đúng
1.445.000đ vốn — triệt tiêu nhau.

Mốc 6 chỉ hơn về **doanh thu** và **thời gian giữ khách** (420 ngày so với 300 ngày),
**không hơn về lãi**, mà tốn thêm 2 hộp tồn kho và tiền ship.

**Hệ quả khi lập kế hoạch ads:** đừng mặc định đẩy khách lên mốc 6 vì tưởng lãi hơn.
Nếu chọn đẩy mốc 6, phải nói rõ lý do là *giữ khách dùng dài*, không phải *lãi cao hơn*.
Trang bán đang quảng cáo mốc 6 là "lợi nhất" — đúng với khách, không đúng với lãi công ty.

## Bốn khoản CHƯA trừ — ngưỡng thật cao hơn

1. **Quà tặng mốc 3 và mốc 5** — chưa biết quà là gì. Nếu quà là 1 hộp cùng loại:
   mốc 3 tụt từ 50% xuống **33,3%** (ROAS hoà vốn 3,00), mốc 5 tụt xuống **41,7%** (ROAS hoà vốn 2,40).
2. **Mức "giảm tiền mặt"** thay quà ở mốc 3–5 — chưa biết bao nhiêu.
3. **Hoa hồng đại lý / sale** — chưa có chính sách.
4. **Vận chuyển, đổi trả, vận hành** — chưa có số.

→ Trong máy tính, bốn ô này đang để **0**. Ngưỡng hiện ra là **mức tối đa lý thuyết**.
Có số nào thì điền số đó, ngưỡng siết lại ngay.

## Cần gì để bỏ chữ "giả định"

| Dữ liệu | Ai có thể cho |
|---|---|
| Giá nhập thật mỗi hộp (hoá đơn) | Anh Sơn |
| Quà tặng mốc 3–5 là gì, vốn bao nhiêu | Anh Sơn / Phòng 7 |
| Mức giảm tiền mặt thay quà | Anh Sơn / Phòng 7 |
| Chính sách hoa hồng | Anh Sơn |
| Phí ship trung bình mỗi đơn | Phòng 8 (dữ liệu đơn thật) |

Khi có hoá đơn nhập thật: sửa **một dòng giá vốn** ở file gốc bên Phòng Tổng Chỉ Huy,
cập nhật bảng này và ô "Giá vốn 1 hộp" trong máy tính, rồi bỏ dòng cảnh báo giả định.
