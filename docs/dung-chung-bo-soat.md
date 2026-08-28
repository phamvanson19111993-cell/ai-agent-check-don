<!-- soat-tuan-thu: bo-qua -->

# Bộ soát tuân thủ — hướng dẫn cho các phòng khác

Phòng nào cũng chạy được trên file markdown của mình. **Không cần khoá API, không cần cài gì.**

## Lấy về

```bash
git clone -b claude/ai-agent-health-video-content-rmedj9 <repo> soat-tuan-thu
cd soat-tuan-thu
```

Hoặc nếu đã có repo, chỉ cần `git fetch` rồi checkout nhánh trên.

## Chạy

```bash
python -m agent.cli check duong-dan/file.md              # một file
python -m agent.cli check thu-muc/*.md                   # nhiều file
python -m agent.cli check ban-nhap.md --bo-qua-khuyen-cao   # file nội bộ, không cần câu khuyến cáo
```

Mã thoát `0` là sạch, khác `0` là còn lỗi chặn đăng. Dùng được trong CI.

## Nó bắt những gì

| Nhóm | Ví dụ bị chặn |
|---|---|
| Từ cấm theo Nghị định 15/2018 | chữa khỏi · điều trị · đặc trị · dứt điểm · thay thế thuốc |
| Thiếu câu khuyến cáo bắt buộc | file không có câu "Thực phẩm này không phải là thuốc..." |
| Cam kết kết quả theo thời gian | "hết tê sau 7 ngày" |
| Mượn danh nghĩa y tế | "bác sĩ khuyên dùng sản phẩm này" |
| So sánh tuyệt đối | "sản phẩm số 1 Việt Nam" · "tốt nhất thị trường" |
| Cam kết phòng ngừa bệnh cụ thể | "phòng ngừa đột quỵ" · "chống ung thư" |
| Sai sự thật về giá | "mua nhiều rẻ hơn" — giá mỗi hộp phẳng ở mọi mốc |
| Sai sự thật về liệu trình | "một hộp chưa kịp thấy gì" — 1 hộp dùng 60 ngày |
| Sai thành phần | "thìa là đen" — thực tế là chiết xuất hạt tiêu đen |
| Gán ubiquinol cho giấy tờ Việt Nam | nhãn phụ chỉ ghi "Coenzyme Q10 50mg" |
| Số giấy tờ chưa có ảnh chứng minh | XNQC 1582/2024 · GMP JHNFA 11105 · mã sàn 2927... |

Nó **không** bắt được: công dụng nằm ngoài nhãn nhưng diễn đạt lạ, câu chuyện bịa,
và mọi thứ cần đọc bằng mắt. Đây là lưới lọc thô, không thay được người duyệt.

## Sửa luật

Mọi luật nằm trong `knowledge/compliance.json`, không nằm trong code:

- `tu_cam_va_tu_thay_the` — cụm cấm, so khớp nguyên văn
- `mau_cam_regex` — luật có ngữ cảnh (tự xưng số 1, cam kết phòng ngừa bệnh...)
- `ngoai_le_khong_tinh_la_vi_pham` — cụm hợp lệ, che trước khi soát (ví dụ chính câu khuyến cáo bắt buộc cũng chứa từ nằm trong danh sách cấm)

Thêm luật thì thêm một dòng JSON, không phải sửa code. Sửa xong chạy
`python -m unittest discover -s tests` để chắc không phá luật cũ.

## File tra cứu bị báo lỗi oan

Tài liệu nội bộ liệt kê từ cấm làm ví dụ sẽ bị chính bộ soát chặn. Thêm dòng này ở đầu file:

```
<!-- soat-tuan-thu: bo-qua -->
```

Chỉ dùng cho tài liệu tra cứu. **Không bao giờ đặt dòng này vào kịch bản hay caption đem đăng.**

## Báo lỗi

Thấy bộ soát báo nhầm (chặn câu đúng) hoặc bỏ sót (cho qua câu sai), báo Phòng 6.
Cả hai loại đều đã xảy ra và đều sửa được trong ngày.
