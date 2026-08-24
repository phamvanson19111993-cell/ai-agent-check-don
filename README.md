# AI Agent viết kịch bản video sức khoẻ

Agent tạo kịch bản video quay được ngay về **đau đầu, chóng mặt, mất ngủ, tê bì chân tay**,
gắn với bộ 3 sản phẩm **Rich Coenzyme Q10 - DHA EPA SQ - Nattokinase**.

Điểm khác biệt so với việc hỏi thẳng một chatbot: agent này có kho kiến thức riêng về sản phẩm,
có chân dung khách hàng, có khung định dạng video, và quan trọng nhất là **bộ kiểm tra tuân thủ
quảng cáo thực phẩm bảo vệ sức khoẻ tự động chặn những câu vi phạm** trước khi bạn kịp đăng.

```
   Đề bài                 Kho kiến thức              Claude              Bộ soát tuân thủ
triệu chứng   ─┐      products / symptoms       ┌─────────┐       ┌──────────────────┐
đối tượng     ─┼──►   personas / formats   ──►  │ viết    │  ──►  │ dính từ cấm?     │
định dạng     ─┤      hooks / ctas              │ kịch bản│       │ thiếu khuyến cáo?│
nền tảng      ─┘      compliance                └─────────┘       └────────┬─────────┘
                                                     ▲                     │ còn lỗi
                                                     └─────────────────────┘ tự sửa lại
```

## Bắt đầu nhanh

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

python -m agent.cli list                      # xem các lựa chọn có sẵn
python -m agent.cli generate --trieu-chung mat-ngu --doi-tuong phu-nu-45-55
python -m agent.cli plan --so-ngay 30         # lịch nội dung 30 ngày
python -m agent.cli check scripts/*.md        # soát tuân thủ, không cần API
```

## Có sẵn 5 kịch bản quay được ngay

Không cần khoá API, mở ra là quay. Đây cũng là mẫu chuẩn cho agent học theo.

| File | Chủ đề | Định dạng |
|---|---|---|
| [scripts/01](scripts/01-mat-ngu-phu-nu-45-ke-chuyen.md) | Mất ngủ tuổi tiền mãn kinh | Kể chuyện, 75s |
| [scripts/02](scripts/02-te-bi-chan-tay-nguoi-cao-tuoi.md) | Tê bì chân tay ở người cao tuổi | Bán hàng, 45s |
| [scripts/03](scripts/03-dau-dau-chong-mat-dan-van-phong.md) | Đau đầu, hoa mắt cuối ngày | Giải thích cơ chế, 70s |
| [scripts/04](scripts/04-bo-3-san-pham.md) | Bộ 3 sản phẩm khác nhau chỗ nào | Video trụ cột, 90s |
| [scripts/05](scripts/05-livestream-15-phut.md) | Khung livestream bán hàng | Live, 15 phút |

Mỗi kịch bản gồm: 3 phương án hook, bảng lời thoại theo từng giây kèm B-roll và chữ trên màn hình,
ghi chú quay dựng, caption và hashtag, ba bình luận hay gặp kèm câu trả lời.

## Tuân thủ - phần quan trọng nhất

Nội dung thực phẩm bảo vệ sức khoẻ ở Việt Nam bị quản lý chặt. Agent được cài sẵn:

- Câu khuyến cáo bắt buộc phải xuất hiện trong mọi kịch bản và caption.
- Hơn 25 cụm từ cấm kèm cách nói thay thế (`chữa khỏi` → `hỗ trợ cải thiện`...).
- Chặn cam kết theo thời gian kiểu "hết tê sau 7 ngày".
- Chặn việc mượn danh nghĩa bác sĩ, dược sĩ, bệnh viện.
- Chặn tự xưng số 1, tốt nhất, duy nhất.
- Bắt buộc nhắc cảnh báo an toàn của Nattokinase với người dùng thuốc chống đông.
- Bắt buộc có phần dấu hiệu phải đi khám ngay, đặt trước phần bán hàng.

Nếu model viết ra câu vi phạm, agent **tự gửi lại lỗi cho model sửa** tối đa 2 lần trước khi
trả kết quả. Chi tiết: [docs/quy-tac-tuan-thu.md](docs/quy-tac-tuan-thu.md).

> Bộ soát tự động không thay được mắt người và không phải tư vấn pháp lý. Trước khi chạy quảng
> cáo trả phí, hãy đối chiếu với hồ sơ công bố sản phẩm và bộ phận pháp chế của nhà phân phối.

## Việc bạn cần làm trước khi dùng thật

Mở `knowledge/products.json`, tìm mục `CAN_DIEN_THEM` của từng sản phẩm và điền từ **nhãn sản
phẩm thật**: hàm lượng, số công bố sản phẩm, nhà sản xuất, xuất xứ, liều dùng, giá bán lẻ.

Những trường này đang để trống có chủ đích. Chừng nào chưa điền, agent sẽ viết `[CẦN ĐIỀN]`
trong kịch bản thay vì bịa số liệu.

## Cấu trúc dự án

```
agent/
  cli.py           5 lệnh: list, generate, check, plan, batch
  kb.py            đọc kho kiến thức
  prompts.py       dựng system prompt và đề bài cho model
  generator.py     gọi Claude API, streaming, vòng tự sửa lỗi tuân thủ
  compliance.py    bộ soát tuân thủ, chạy độc lập không cần API
  planner.py       lịch nội dung theo tháng
  config.py        model, effort, giọng thương hiệu
knowledge/         7 file JSON - sửa ở đây là đổi hành vi agent, không phải sửa code
scripts/           5 kịch bản mẫu quay được ngay
docs/              hướng dẫn sử dụng, quy tắc tuân thủ, tài liệu bộ 3 sản phẩm
tests/             18 kiểm thử, gồm cả việc soát lại các kịch bản mẫu
```

## Tài liệu

- [Hướng dẫn sử dụng chi tiết](docs/huong-dan-su-dung.md)
- [Quy tắc tuân thủ](docs/quy-tac-tuan-thu.md)
- [Tài liệu bộ 3 sản phẩm](docs/bo-3-san-pham.md)

## Kiểm thử

```bash
python -m unittest discover -s tests -v
```
