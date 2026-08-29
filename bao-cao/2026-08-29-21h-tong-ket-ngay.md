# Phòng 7 · Lady Page — TỔNG KẾT NGÀY 29/08/2026

Ảnh báo cáo: `bao-cao/anh/2026-08-29-tong-ket.png` (`d4bc8fc`)

## SỐ CỦA NGÀY
| | |
|---|---|
| Chi quảng cáo | **0đ** |
| Lượt xem | **0** |
| Đơn | **0** |
| Số giờ liên tiếp không một lượt xem | **24 giờ tròn** |

Không phải trang hỏng — **chưa ai bật quảng cáo**. Số thật gần nhất vẫn là ngày 28/08:
366 lượt xem · 2 đơn gửi · 1 chuyển khoản · 0,55%.
10 thay đổi hôm nay CHƯA có một khách thật nào nhìn thấy, nên không được phép
kết luận chúng hiệu quả hay không.

## TRANG — 10 thay đổi đã lên, đo được từng cái
| | Trước | Sau |
|---|---|---|
| Ô khách phải gõ | 7 | **2 bắt buộc** (3 ô tổng) |
| Biểu mẫu nằm ở màn | 34 | **14** |
| Thao tác để xong đơn | — | **4** |
| Phải trả tiền trước | có | **KHÔNG** (COD mặc định) |
| Cửa thoát ra ngoài | 6 | **1** (giữ Messenger) |

Kèm: ảnh sản phẩm cạnh bảng giá · giá quy ra mỗi ngày ở màn đầu · hai cam kết của
anh Sơn ngay trên nút gửi · bỏ dòng "Nhân vật minh hoạ" theo yêu cầu anh Sơn ·
bản tin đơn bỏ dòng "Địa chỉ:" trống.
Commit: `df4d971` · `2227ebf` · `5272480`

## QUẢNG CÁO CÓ BỊ ẢNH HƯỞNG KHÔNG — KHÔNG
Đối chiếu index.html đầu ngày (`9c1efce`) với bây giờ:
- Toàn bộ lời gọi Pixel: **giống hệt** (diff sạch)
- Mã Pixel 1277743445418211: **không đổi**
- Tên 12 sự kiện tuỳ chỉnh: **không đổi**
- Đường dẫn đích: **không đổi**
Sửa index.html 3 lần, không lần nào chạm ba thứ khiến Meta học lại.

## CÔNG CỤ DỰNG THÊM
- `apps-script/chuong-don.gs` — chuông báo đơn qua email + Telegram (`17070ed`)
- `thuc-thi.py` việc **"bật"** — bật chiến dịch CẢ BA TẦNG (`767a976`)
- `san-pham/q10.py` — qua được bộ soát luật quảng cáo, 6 chỗ hỏng về 0 (`2c26c17`),
  trong đó 3 chỗ là vi phạm luật quảng cáo thực phẩm chức năng (thiếu câu chống
  chỉ định), 1 chỗ dùng chữ cấm "duy nhất", 1 chỗ ảnh quảng cáo trỏ vào file không tồn tại.
- `dung-ban-nhap.py` — mỗi thay đổi chờ duyệt là một hàm, chạy lại được nhiều lần

## HAI VIỆC CHẶN, CHỈ ANH SƠN LÀM ĐƯỢC — mỗi việc dưới 1 phút
1. **Bí mật kho `FB_TOKEN`** → Settings → Secrets and variables → Actions →
   New repository secret → Name: FB_TOKEN.
   Có nó là Phòng 7 bấm chạy quảng cáo từ máy chủ GitHub được ngay.
   Hồ sơ đã qua soát luật, bộ tự kiểm 27/27 đạt, quy trình chạy tới bước cuối rồi
   dừng đúng ở dòng "Thieu Bi mat kho FB_TOKEN".
2. **Chuông báo đơn** → Biểu mẫu → tab Câu trả lời → dấu ⋮ →
   "Nhận thông báo qua email cho câu trả lời mới". Không cần bảng trả lời, không cần code.

## PHẦN VIỆC CỦA PHÒNG 7
Đã cạn. Không còn việc nào làm được mà chưa làm.
