# Hướng dẫn sử dụng chi tiết

## Cài đặt

```bash
git clone <repo> && cd ai-agent-check-don
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

Ba lệnh `list`, `check`, `plan` chạy được ngay mà không cần khoá API.

## Lệnh 1: xem các lựa chọn

```bash
python -m agent.cli list
```

In ra mã của triệu chứng, đối tượng, định dạng, sản phẩm để dùng cho lệnh `generate`.
Cuối danh sách có cảnh báo về những trường thông tin sản phẩm chưa điền.

## Lệnh 2: viết một kịch bản

```bash
python -m agent.cli generate \
  --trieu-chung te-bi-chan-tay \
  --doi-tuong nguoi-cao-tuoi-60 \
  --dinh-dang hook-noi-dau-giai-phap \
  --nen-tang facebook \
  --thoi-luong 45
```

Tuỳ chọn khác:

| Tham số | Ý nghĩa |
|---|---|
| `--san-pham nattokinase dha-epa-sq` | Chỉ định sản phẩm được nhắc, mặc định lấy theo triệu chứng |
| `--them "quay ngoài trời, có phụ đề"` | Yêu cầu riêng cho video này |
| `--so-lan-sua 3` | Số lần cho model tự sửa lỗi tuân thủ, mặc định 2 |
| `--luu duong/dan.md` | Nơi lưu, mặc định là `output/` |

Kịch bản in ra màn hình và lưu vào file. Mã thoát khác 0 nghĩa là còn lỗi tuân thủ phải sửa tay.

## Lệnh 3: soát tuân thủ

```bash
python -m agent.cli check scripts/*.md
python -m agent.cli check ban-nhap.md --bo-qua-khuyen-cao
```

Dùng được cho cả kịch bản do người viết tay, không riêng gì kịch bản do agent tạo.
Đây là lệnh nên chạy trước mỗi lần đăng bài.

## Lệnh 4: lên lịch nội dung

```bash
python -m agent.cli plan --so-ngay 30 --tu-ngay 2026-09-01 --luu ke-hoach-thang-9.md
```

Xoay vòng triệu chứng, đối tượng, định dạng theo tỉ lệ 3 giáo dục - 2 câu chuyện - 1 sản phẩm -
1 tương tác mỗi tuần. Cuối file có sẵn lệnh `generate` cho từng ngày để chép và chạy.

## Lệnh 5: viết hàng loạt

```bash
python -m agent.cli batch --so-ngay 7 --thu-muc output/tuan-1
```

Chạy theo lịch nội dung và sinh kịch bản cho từng ngày. Lệnh này gọi API nhiều lần nên
tốn chi phí, hãy thử với `--so-ngay 2` trước.

## Sửa agent theo ý mình

| Muốn đổi gì | Sửa file nào |
|---|---|
| Thông tin sản phẩm, công dụng được phép nói | `knowledge/products.json` |
| Thêm triệu chứng mới | `knowledge/symptoms.json` |
| Thêm chân dung khách hàng | `knowledge/personas.json` |
| Thêm kiểu video mới | `knowledge/formats.json` |
| Thêm từ cấm, sửa luật tuân thủ | `knowledge/compliance.json` |
| Thêm hook, thêm câu kêu gọi hành động | `knowledge/hooks.json`, `knowledge/ctas.json` |
| Đổi giọng thương hiệu | biến môi trường `KICHBAN_BRAND_VOICE` hoặc `agent/config.py` |
| Đổi khung kết quả trả về | `agent/prompts.py`, hàm `build_system` |

Thêm một triệu chứng mới chỉ cần thêm một khối JSON, không phải sửa code.

## Chi phí và model

Mặc định dùng `claude-opus-5`. Muốn rẻ hơn cho những video đơn giản:

```bash
KICHBAN_MODEL=claude-sonnet-5 KICHBAN_EFFORT=medium python -m agent.cli generate --trieu-chung mat-ngu
```

Phần system prompt được đánh dấu cache nên khi viết nhiều kịch bản liên tiếp, phần luật tuân thủ
và thông tin sản phẩm được tái sử dụng, giảm đáng kể token đầu vào.

## Chạy kiểm thử

```bash
python -m unittest discover -s tests -v
```

Bộ kiểm thử soát cả các kịch bản mẫu trong `scripts/`, nên nếu bạn sửa luật tuân thủ mà kịch bản
mẫu vi phạm, kiểm thử sẽ báo ngay.
