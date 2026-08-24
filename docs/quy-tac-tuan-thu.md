# Quy tắc tuân thủ khi làm nội dung thực phẩm bảo vệ sức khoẻ

Tài liệu này là bản diễn giải cho người làm nội dung. Nguồn luật tham chiếu: Luật Quảng cáo,
Nghị định 15/2018/NĐ-CP, Thông tư 09/2015/TT-BYT. Đây không phải tư vấn pháp lý - trước khi
chạy quảng cáo trả phí, hãy đối chiếu với nội dung đã được xác nhận trong hồ sơ công bố sản phẩm
và hỏi bộ phận pháp chế của đơn vị phân phối.

## 1. Câu bắt buộc

Mọi video và mọi caption phải có nguyên văn:

> Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh.

Trong video: đọc thành lời hoặc hiện chữ rõ ràng, đủ lâu để đọc hết.

## 2. Bảy điều không bao giờ được làm

1. Nói sản phẩm chữa, điều trị, đặc trị hay khỏi bệnh.
2. Dùng hình ảnh, danh nghĩa, lời cảm ơn của bác sĩ, dược sĩ, nhân viên y tế, bệnh viện, phòng khám.
3. Dùng thư cảm ơn hoặc lời chứng thực của người bệnh để quảng cáo sản phẩm.
4. Cam kết kết quả hoặc mốc thời gian: "hết tê sau 7 ngày", "hiệu quả 100%", "không khỏi hoàn tiền".
5. So sánh sản phẩm mình tốt hơn sản phẩm của đơn vị khác, hoặc tự xưng số 1, tốt nhất, duy nhất.
6. Doạ nạt quá mức về bệnh tật, dựng cảnh giả về đột quỵ, cấp cứu, kết quả xét nghiệm.
7. Nói công dụng nằm ngoài phần công dụng đã công bố trên nhãn sản phẩm.

## 3. Cách nói thay thế

| Không dùng | Dùng thay |
|---|---|
| chữa khỏi, điều trị, đặc trị | hỗ trợ, hỗ trợ cải thiện |
| dứt điểm, khỏi hẳn, tiêu tan | cải thiện dần, dễ chịu hơn, giảm bớt |
| thay thế thuốc | dùng kèm theo chỉ định của bác sĩ |
| cam kết khỏi, hiệu quả 100% | hiệu quả tuỳ cơ địa mỗi người |
| thần dược, công dụng thần kỳ | sản phẩm hỗ trợ sức khoẻ |
| tan cục máu đông, phòng chống đột quỵ | hỗ trợ tuần hoàn máu, hỗ trợ sức khoẻ tim mạch |
| sản phẩm số 1, tốt nhất thị trường | được nhiều người lựa chọn, phù hợp với |

Danh sách đầy đủ nằm trong `knowledge/compliance.json` và được bộ kiểm tra tự động soát.

## 4. Bốn câu an toàn nên có sẵn trong đầu

- Sản phẩm hỗ trợ, không thay thế việc thăm khám và điều trị.
- Hiệu quả tuỳ thuộc cơ địa từng người.
- Nếu đang dùng thuốc điều trị, hãy hỏi ý kiến bác sĩ trước khi bổ sung.
- Đọc kỹ hướng dẫn sử dụng trước khi dùng.

## 5. Dấu hiệu phải dừng bán hàng và khuyên đi viện

Nếu chủ đề video có liên quan, luôn nhắc những dấu hiệu này:

- Đau đầu dữ dội đột ngột, chưa từng đau như vậy bao giờ
- Méo miệng, nói khó, đột ngột yếu hoặc liệt nửa người
- Đột ngột mất thị lực hoặc nhìn đôi
- Tê bì kèm mất cảm giác lan nhanh trong vài giờ
- Đau đầu kèm sốt cao, cứng gáy, nôn vọt
- Đau ngực, khó thở, tim đập nhanh bất thường
- Chóng mặt kèm ngất xỉu

Đưa phần này lên TRƯỚC phần bán hàng. Vừa đúng về y tế, vừa xây được uy tín thật.

## 6. Lưu ý an toàn riêng của Nattokinase

Đây là sản phẩm cần cẩn thận nhất trong bộ ba. Bắt buộc nhắc mỗi khi nói tới:

- Người đang dùng thuốc chống đông máu phải hỏi bác sĩ trước.
- Người rối loạn đông máu, đang chảy máu, chuẩn bị phẫu thuật hoặc nhổ răng: không tự dùng.
- Phụ nữ có thai và cho con bú: hỏi ý kiến bác sĩ.
- Người dị ứng đậu nành: không dùng.

## 7. Lưu ý theo nền tảng

- **TikTok**: hạn chế nói tên bệnh và từ ngữ về thuốc trong 3 giây đầu, ưu tiên mô tả cảm giác.
- **Facebook**: viết theo hướng "nhiều người ở tuổi này" thay vì "bạn đang bị", tránh bị hạn chế tài khoản quảng cáo.
- **YouTube**: được nói dài hơn nhưng phải trích nguồn rõ, tránh khẳng định y khoa tuyệt đối.
- **TikTok Shop / Shopee**: nội dung video phải khớp với thông tin công bố trên trang sản phẩm.

## 8. Quy trình trước khi đăng

```bash
python -m agent.cli check duong-dan-kich-ban.md
```

Bộ kiểm tra bắt được từ cấm, thiếu khuyến cáo, cam kết thời gian, danh nghĩa y tế và so sánh
tuyệt đối. Nó không thay được mắt người: vẫn phải đọc lại một lượt, nhất là phần công dụng
có khớp với nhãn sản phẩm hay không.
