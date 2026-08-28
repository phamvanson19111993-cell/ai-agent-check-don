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

## Nhắc từ cấm ĐỂ CẤM thì không bị báo lỗi

Từ 28/08 bộ soát phân biệt được "dùng từ cấm" với "nhắc từ cấm để cấm". Bốn dấu hiệu:

1. Dòng mở đầu bằng ❌ ⛔ ⚠️ 🚨 🚫
2. Gạch đầu dòng và ô bảng nằm ngay dưới một dòng gợi ý ("Không được nói:", "Bảng thay từ", "❌ Cấm | ✅ Thay bằng")
3. Phủ định đứng ngay trước: "không hứa chữa khỏi", "tránh nói X", "thay vì X"
4. Phủ định đứng ngay sau: "Làm tan cục máu đông | công dụng như thuốc", "Nói X là vi phạm"

Câu khuyến cáo bắt buộc và các câu khuyên đi khám cũng được bỏ qua sẵn.

**Vì sao phải có phần này:** bộ soát càng nghiêm càng đẩy các phòng đi xoá chính danh sách
cấm của mình cho báo cáo xanh — ngược đúng mục đích. Đây là lỗi thiết kế Phòng 10 phát hiện,
không phải chuyện chỉnh ngưỡng.

**Việc bỏ qua không âm thầm.** Cuối báo cáo luôn ghi đã bỏ qua bao nhiêu dòng. Ai lạm dụng
thì con số đó nhảy lên và nhìn là thấy.

### Chỗ vẫn có thể lách — biết trước để không bị lừa

Gạch đầu dòng nằm dưới tiêu đề "Không được nói" thì được tha. Về lý thuyết có thể nhét câu
quảng cáo vào đó để qua mặt. Văn xuôi thì **không** tha được — mà kịch bản và tin nhắn khách
đều viết bằng văn xuôi, nên lỗ hổng này không dùng để đăng bài thật được.

Muốn soát không tha gì cả:

```bash
python -m agent.cli check kich-ban-sap-quay.md --nghiem-ngat
```

Nên chạy `--nghiem-ngat` cho kịch bản sắp quay, chạy chế độ thường cho tài liệu tra cứu.

## File tra cứu bị báo lỗi oan

Tài liệu nội bộ liệt kê từ cấm làm ví dụ sẽ bị chính bộ soát chặn. Thêm dòng này ở đầu file:

```
<!-- soat-tuan-thu: bo-qua -->
```

Chỉ dùng cho tài liệu tra cứu. **Không bao giờ đặt dòng này vào kịch bản hay caption đem đăng.**

## Báo lỗi

Thấy bộ soát báo nhầm (chặn câu đúng) hoặc bỏ sót (cho qua câu sai), báo Phòng 6.
Cả hai loại đều đã xảy ra và đều sửa được trong ngày.
