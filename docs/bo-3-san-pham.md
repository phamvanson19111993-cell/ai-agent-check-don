# Bộ 3 sản phẩm - tài liệu cho người làm nội dung

Đây là bản tóm tắt để biên kịch và người livestream nắm nhanh. Mọi công dụng nêu ở đây phải
được đối chiếu lại với nhãn và hồ sơ công bố của lô hàng bạn đang bán.

## Ví von xuyên suốt: Đường thông - Xe tốt - Xăng đủ

Cơ thể như một thành phố. Máu là xe chở oxy và dưỡng chất. Mạch máu là đường. Tế bào là nhà máy.

| Sản phẩm | Vai trò trong ví von | Lo phần nào |
|---|---|---|
| Nattokinase | ĐƯỜNG THÔNG | Hỗ trợ tuần hoàn máu, để dưỡng chất tới được não và tứ chi |
| DHA EPA SQ | XE TỐT | Nguyên liệu cho màng tế bào thần kinh, hỗ trợ chuyển hoá mỡ máu |
| Rich Coenzyme Q10 | XĂNG ĐỦ | Ví von nội bộ về vai trò của CoQ10 trong ty thể. Công dụng nói ra ngoài phải theo nguyên văn nhãn ở dưới |

Câu chốt khi bị hỏi "sao phải mua ba loại":
> Máu lưu thông tốt mà tế bào không có năng lượng thì vẫn mệt. Tế bào đủ năng lượng mà đường đi
> của máu kém thì dưỡng chất không tới nơi. Ba thứ hỗ trợ nhau chứ không thay thế nhau. Nhưng
> không bắt buộc dùng cả ba - cứ xem mình vướng ở đâu thì bắt đầu từ đó.

## 1. Nattokinase

- **Là gì**: enzyme chiết từ đậu nành lên men natto, món ăn truyền thống Nhật Bản.
- **Công dụng được phép nói**: hỗ trợ tuần hoàn máu; hỗ trợ tăng cường lưu thông máu não; hỗ trợ giảm nguy cơ hình thành huyết khối.
- **Hợp với ai**: hay tê bì chân tay, hay đau đầu chóng mặt do tuần hoàn kém, người cao tuổi ít vận động.
- **Bắt buộc nhắc**: đang dùng thuốc chống đông máu, rối loạn đông máu, sắp phẫu thuật hoặc nhổ răng, có thai, cho con bú, dị ứng đậu nành → hỏi bác sĩ hoặc không dùng.
- **Không được nói**: làm tan cục máu đông, phòng chống đột quỵ, thay thế thuốc chống đông.

## 2. DHA EPA SQ

- **Là gì**: omega-3 gồm DHA và EPA, kết hợp với squalene.
- **Công dụng được phép nói**: hỗ trợ sức khoẻ não bộ và trí nhớ; hỗ trợ sức khoẻ tim mạch; hỗ trợ giảm mỡ máu; hỗ trợ sức khoẻ thị lực.
- **Hợp với ai**: hay quên, khó tập trung, ít ăn cá biển, mỡ máu cao, làm việc trí óc nhiều.
- **Bắt buộc nhắc**: dị ứng hải sản cần đọc kỹ thành phần; đang dùng thuốc chống đông cần hỏi bác sĩ; ngưng trước phẫu thuật theo hướng dẫn.
- **Mẹo bán hàng đúng luật**: hướng dẫn khách nhìn hàm lượng DHA và EPA trên nhãn thay vì chỉ nhìn tổng lượng dầu cá.

## 3. Rich Coenzyme Q10

- **Là gì**: CoQ10 là chất có sẵn trong cơ thể, nằm trong ty thể - nơi tế bào tạo ra năng lượng.
- **Công dụng được phép nói**: bổ sung Coenzyme Q10 cho cơ thể; chống oxy hoá; giảm mệt mỏi; giúp giảm nguy cơ xơ vữa động mạch; tốt cho tim mạch (nguyên văn nhãn phụ).
- **Hợp với ai**: trên 40 tuổi, hay mệt và hụt hơi kéo dài, quan tâm sức khoẻ tim mạch, đang dùng statin (hỏi bác sĩ trước).
- **Bắt buộc nhắc**: đang dùng thuốc chống đông, có thai, cho con bú → hỏi bác sĩ. Nên uống cùng bữa ăn có chất béo để hấp thu tốt hơn.

## Gợi ý điểm vào theo triệu chứng

| Khách kêu | Bắt đầu từ | Vì sao |
|---|---|---|
| Tê bì chân tay, chóng mặt | Nattokinase | Mắt xích tuần hoàn |
| Hay quên, khó tập trung, mỡ máu cao | DHA EPA SQ | Mắt xích nuôi dưỡng thần kinh và mỡ máu |
| Mệt mỏi, hụt hơi, trên 40 tuổi | Rich Coenzyme Q10 | Nhãn cho nói "giảm mệt mỏi" |
| Mất ngủ | Hỏi thêm trước khi gợi ý | Mất ngủ nhiều nguyên nhân, cần hỏi rõ nội tiết, stress hay tuần hoàn |

## Việc còn phải làm

File `knowledge/products.json` có mục `CAN_DIEN_THEM` cho mỗi sản phẩm, hiện đang để trống:
hàm lượng, số công bố sản phẩm, nhà sản xuất, xuất xứ, liều dùng theo nhãn, giá bán lẻ.

Cho tới khi những trường này được điền, agent sẽ viết `[CẦN ĐIỀN]` trong kịch bản thay vì
bịa số liệu. Hãy điền từ nhãn sản phẩm thật, đừng lấy từ trang bán hàng của bên khác.
