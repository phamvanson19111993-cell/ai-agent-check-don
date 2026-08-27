# GIÁ VỐN & NGƯỠNG ROAS — Rich Coenzyme Q10

> ## ⚠️ ĐÂY LÀ GIẢ ĐỊNH, KHÔNG PHẢI SỐ ĐÃ XÁC MINH
>
> ```
> DATA UPDATE
> - Loại dữ liệu:        Giá vốn mỗi hộp
> - Giá trị:             1.445.000đ  (= 50% giá bán lẻ 2.890.000đ)
> - Kỳ:                  08/2026
> - Nguồn:               Anh Sơn đặt mức 50% để tính
> - Thời gian cập nhật:  27/08/2026
> - Agent tạo:           Phòng Tổng Chỉ Huy
> - Trạng thái xác minh: ANH CUNG CẤP, CHƯA ĐỐI CHIẾU HOÁ ĐƠN NHẬP
> ```
>
> **Mọi con số dưới đây kế thừa trạng thái này.** Phòng nào trích ra ngoài
> (báo cáo, kịch bản, quyết định ngân sách) **bắt buộc ghi kèm "theo giả định giá vốn 50%"**.
> Khi có hoá đơn nhập thật, sửa đúng một dòng `von = 50%` ở đây rồi tính lại.

## Bảng lãi gộp theo từng mốc

Giá bán 1 hộp: **2.890.000đ** (đã xác minh, nguồn: trang bán đang chạy)
Giá vốn 1 hộp: **1.445.000đ** (giả định 50%)

| Mốc | Doanh thu | Hộp phải giao | Giá vốn | Lãi gộp | Biên | Trần chi phí ads mỗi đơn |
|---|---|---|---|---|---|---|
| 1 hộp | 2.890.000đ | 1 | 1.445.000đ | **1.445.000đ** | 50,0% | 1.445.000đ |
| 3 hộp | 8.670.000đ | 3 | 4.335.000đ | **4.335.000đ** | 50,0% | 4.335.000đ |
| 5 hộp | 14.450.000đ | 5 | 7.225.000đ | **7.225.000đ** | 50,0% | 7.225.000đ |
| 6 hộp | 17.340.000đ | **7** *(tặng 1)* | 10.115.000đ | **7.225.000đ** | **41,7%** | 7.225.000đ |

## 🔍 PHÁT HIỆN — mốc 5 và mốc 6 cho lãi gộp Y HỆT NHAU

Cả hai mốc đều lãi **7.225.000đ**, nhưng mốc 6 phải **giao thêm 2 hộp hàng**.

Lý do: hộp thứ 6 mang về đúng 1.445.000đ lãi, còn hộp thứ 7 tặng đi tốn đúng
1.445.000đ vốn — hai khoản triệt tiêu nhau.

**Nghĩa là:** mốc 6 chỉ hơn mốc 5 về *doanh thu* và *giữ chân khách lâu hơn* (420 ngày
so với 300 ngày), **không hơn về lãi**, mà lại tốn thêm 2 hộp tồn kho và tiền ship.
Trang bán đang quảng cáo mốc 6 là "lợi nhất" — đúng với **khách**, không đúng với **lãi của công ty**.

→ Cần anh quyết: giữ nguyên (chấp nhận đổi lãi lấy khách dùng dài), hay đổi cơ cấu quà mốc 6.

## Ngưỡng ROAS hoà vốn

```
ROAS hoà vốn = 1 ÷ biên lãi gộp
```

| Mốc | Biên lãi gộp | ROAS hoà vốn |
|---|---|---|
| 1 · 3 · 5 hộp | 50,0% | **2,00** |
| 6 hộp | 41,7% | **2,40** |

**Cách dùng cho Phòng Ads:** ROAS dưới ngưỡng trên là **đang lỗ**, không phải "lãi mỏng".
Và đây mới là ngưỡng *gộp* — ngưỡng thật còn cao hơn (xem dưới).

## ⚠️ Bốn khoản CHƯA trừ — ngưỡng thật cao hơn con số trên

Bảng trên mới trừ mỗi giá vốn hàng. Chưa trừ:

1. **Quà tặng mốc 3 và mốc 5** — trang ghi "sản phẩm chính hãng trong danh mục, tính theo
   giá niêm yết". Quà cũng có giá vốn. **Chưa biết quà là gì** → chưa trừ được.
   Nếu quà là 1 hộp cùng loại thì mốc 3 tụt từ 50% xuống 33,3%, mốc 5 tụt xuống 41,7%.
2. **Phương án "giảm tiền mặt"** thay quà ở mốc 3–5 — **chưa biết giảm bao nhiêu**.
3. **Hoa hồng đại lý / sale** — chưa có chính sách, chưa trừ được đồng nào.
4. **Vận chuyển, đổi trả, chi phí vận hành** — chưa có số.

**Kết luận thẳng:** ROAS 2,0 là **sàn tuyệt đối**, không phải mốc an toàn.
Chạy ads ở ROAS 2,2–2,5 mà chưa trừ 4 khoản trên thì rất có thể **đang lỗ mà tưởng lãi**.

## Cần gì để bỏ chữ "giả định"

| Dữ liệu | Ai có thể cho |
|---|---|
| Hoá đơn nhập / giá nhập thật mỗi hộp | Anh Sơn |
| Quà tặng mốc 3–5 là sản phẩm gì, vốn bao nhiêu | Anh Sơn / Phòng 7 |
| Mức "giảm tiền mặt" thay quà | Anh Sơn / Phòng 7 |
| Chính sách hoa hồng | Anh Sơn |
| Phí ship trung bình mỗi đơn | Phòng 8 (dữ liệu đơn thật) |
