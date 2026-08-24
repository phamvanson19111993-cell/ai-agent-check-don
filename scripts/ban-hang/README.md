# 10 nội dung bán hàng

Mười kịch bản có CTA mạnh, đã qua bộ soát tuân thủ. Trải đều 4 triệu chứng và cả 3 sản phẩm.

| Mã | Chủ đề | Đối tượng | Sản phẩm | Giây | CTA |
|---|---|---|---|---|---|
| [BH01](01-mat-ngu-3-kieu.md) | Ba kiểu mất ngủ, kiểu thứ ba bị bỏ sót | Phụ nữ 45-55 | DHA EPA SQ + Nattokinase | 50 | Giỏ hàng |
| [BH02](02-te-tay-con-cai-mua-cho-bo-me.md) | Bố mẹ kêu tê tay, đừng nghĩ do tuổi già | Con cái 28-40 | Nattokinase | 45 | Giỏ hàng |
| [BH03](03-dau-dau-4h-chieu-coq10.md) | Cứ 4 giờ chiều là đầu nặng | Dân văn phòng | Rich CoQ10 | 45 | Giỏ hàng |
| [BH04](04-chong-mat-dung-len-xay-xam.md) | Ba nhịp đứng dậy an toàn | Người cao tuổi 60+ | Nattokinase | 50 | Nhắn tin |
| [BH05](05-met-hut-hoi-coq10.md) | Leo hai tầng cầu thang đã thở | Người 40-55 | Rich CoQ10 | 45 | Giỏ hàng |
| [BH06](06-mo-mau-cao-dha-epa.md) | Bốn dòng cần nhìn trên tờ xét nghiệm mỡ máu | Người có chỉ số bất thường | DHA EPA SQ | 55 | Nhắn tin |
| [BH07](07-hay-quen-dha.md) | Đi vào bếp quên mất mình định làm gì | Phụ nữ 45-55 | DHA EPA SQ | 45 | Giỏ hàng |
| [BH08](08-quiz-nen-bat-dau-tu-dau.md) | Ba câu hỏi chọn đúng sản phẩm | Người đang cân nhắc | Cả bộ 3 | 60 | Bình luận rồi nhắn tin |
| [BH09](09-dang-uong-thuoc-co-dung-duoc-khong.md) | Ba trường hợp khuyên đừng mua | Người đang dùng thuốc | Cả bộ 3 | 55 | Nhắn tin |
| [BH10](10-qua-bieu-bo-me.md) | Biếu bố mẹ gì cho có ích | Con cái 28-40 | Cả bộ 3 | 50 | Nhắn tin |

## Thứ tự đăng gợi ý cho 2 tuần

Đừng đăng liên tiếp 10 video bán hàng. Xen kịch bản giáo dục trong `scripts/` để tài khoản
không bị đánh giá là kênh quảng cáo thuần.

| Ngày | Đăng gì |
|---|---|
| 1 | BH08 - quiz, thu bình luận để có tệp khách |
| 2 | Video giáo dục (`scripts/03`) |
| 3 | BH02 - tê tay, nhắm người con |
| 4 | Video giáo dục (`scripts/01`) |
| 5 | BH09 - xử lý phản đối về thuốc, video xây niềm tin |
| 6 | BH04 - ba nhịp đứng dậy, dễ được lưu và chia sẻ |
| 7 | Nghỉ hoặc livestream (`scripts/05`) |
| 8 | BH01 - ba kiểu mất ngủ |
| 9 | Video giáo dục |
| 10 | BH03 - đau đầu 4 giờ chiều |
| 11 | BH06 - đọc tờ xét nghiệm mỡ máu |
| 12 | BH07 - hay quên |
| 13 | BH05 - mệt, hụt hơi |
| 14 | BH10 - quà biếu, hoặc dời sang đúng dịp lễ |

## Trước khi đăng

```bash
python -m agent.cli check scripts/ban-hang/*.md
```

Ba video mạnh nhất về khả năng ra đơn: **BH08** (khách tự phân loại), **BH09** (bán bằng sự
thành thật), **BH02** (người mua là con cái, khả năng chi trả cao hơn).

Nhớ điền thông tin thật vào `knowledge/products.json` - hàm lượng, số công bố, giá - trước khi
trả lời bình luận về sản phẩm.

---

Nhắc lại câu bắt buộc phải có trong mọi video và mọi caption:

> Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh.
