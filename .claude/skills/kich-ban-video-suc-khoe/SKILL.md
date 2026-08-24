---
name: kich-ban-video-suc-khoe
description: Viết kịch bản video về đau đầu, chóng mặt, mất ngủ, tê bì chân tay gắn với bộ 3 sản phẩm Rich Coenzyme Q10, DHA EPA SQ, Nattokinase. Dùng khi người dùng xin kịch bản video, nội dung TikTok/Facebook/YouTube, caption bán hàng, khung livestream hoặc lịch nội dung cho các sản phẩm này. Cũng dùng khi cần soát một nội dung có vi phạm quy định quảng cáo thực phẩm bảo vệ sức khoẻ hay không.
---

# Viết kịch bản video sức khoẻ

Dùng kho kiến thức và bộ luật tuân thủ trong repo này để viết kịch bản. Không viết theo trí nhớ.

## Bước 1: đọc kho kiến thức

Luôn đọc trước khi viết:

- `knowledge/compliance.json` - luật bắt buộc, từ cấm, câu khuyến cáo
- `knowledge/products.json` - công dụng ĐƯỢC PHÉP nói của từng sản phẩm và lưu ý an toàn
- `knowledge/symptoms.json` - triệu chứng, nguyên nhân, nỗi đau cảm xúc, dấu hiệu phải đi khám
- `knowledge/personas.json` - giọng điệu theo từng nhóm người xem
- `knowledge/formats.json` - khung thời lượng theo từng kiểu video
- `knowledge/hooks.json`, `knowledge/ctas.json` - ngân hàng hook và câu kêu gọi hành động

Đọc thêm một file trong `scripts/` để nắm đúng khung trình bày.

## Bước 2: hỏi cho đủ đề bài

Nếu người dùng chưa nói rõ, hỏi ngắn gọn: triệu chứng nào, người xem là ai, nền tảng nào,
bao nhiêu giây, có nhắc sản phẩm hay không. Nếu họ không muốn trả lời thì tự chọn mặc định
hợp lý và nói rõ mình đã chọn gì.

## Bước 3: viết theo đúng khung

Bám khung 7 phần như các file trong `scripts/`: ý tưởng chính, ba phương án hook, bảng kịch bản
theo từng giây (lời thoại + hình ảnh + chữ trên màn hình), ghi chú quay dựng, caption kèm hashtag,
ba bình luận hay gặp và cách trả lời, phần tự kiểm tra tuân thủ.

Nguyên tắc bắt buộc:

- Chỉ nói công dụng có trong `loi_ich_duoc_phep_noi` của sản phẩm, không thêm.
- Nhắc Nattokinase thì bắt buộc nhắc lưu ý về thuốc chống đông máu và phẫu thuật.
- Luôn có nguyên văn: "Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."
- Cho người xem ít nhất một việc tự làm được miễn phí trước khi nhắc tới sản phẩm.
- Không bịa số liệu, không bịa nghiên cứu. Thiếu dữ liệu thì viết [CẦN ĐIỀN].
- Nếu chủ đề có liên quan, đưa phần dấu hiệu phải đi khám ngay lên TRƯỚC phần bán hàng.

## Bước 4: soát lại bằng máy

Sau khi ghi kịch bản ra file, luôn chạy:

```bash
python -m agent.cli check <file>
```

Còn lỗi thì sửa rồi chạy lại cho tới khi sạch. Đừng báo là xong khi lệnh này còn báo lỗi chặn đăng.

## Các lệnh khác của repo

```bash
python -m agent.cli list                    # xem mã triệu chứng, đối tượng, định dạng
python -m agent.cli plan --so-ngay 30       # lịch nội dung 30 ngày
python -m agent.cli generate --trieu-chung mat-ngu --doi-tuong phu-nu-45-55   # cần ANTHROPIC_API_KEY
```

Khi đang chạy trong Claude Code thì tự viết kịch bản là đủ, không cần gọi `generate`.
Lệnh `check` và `plan` thì luôn dùng được vì không cần khoá API.
