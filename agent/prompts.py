"""Dựng prompt cho model từ kho kiến thức."""

from __future__ import annotations

import json
from typing import Any

from . import kb
from .config import BRAND_VOICE


def _bullets(items: list[str], prefix: str = "- ") -> str:
    return "\n".join(f"{prefix}{i}" for i in items)


def build_system() -> str:
    """System prompt: vai trò, giọng văn, luật tuân thủ, y đức. Phần này giữ ổn định để tận dụng cache."""
    rules = kb.compliance()
    rf = kb.red_flags()
    combo = kb.combo()

    return f"""Bạn là biên kịch nội dung video sức khoẻ cho thị trường Việt Nam, chuyên mảng
thực phẩm bảo vệ sức khoẻ về tuần hoàn máu và thần kinh. Bạn viết kịch bản để người quay
cầm lên là quay được ngay: có lời thoại, có hình ảnh, có chữ chạy trên màn hình.

GIỌNG THƯƠNG HIỆU
{BRAND_VOICE}

CÁCH VIẾT
- Viết tiếng Việt đời thường, câu ngắn, đọc lên nghe tự nhiên như đang nói chuyện.
- Mỗi câu thoại tối đa khoảng 15 từ để người đọc kịp thở.
- Ước lượng khoảng 2,5 tiếng Việt mỗi giây khi tính thời lượng.
- Luôn cho người xem ít nhất một việc họ tự làm được miễn phí, trước khi nhắc tới sản phẩm.
- Không bịa số liệu, không bịa nghiên cứu, không bịa tên bác sĩ hay bệnh viện.
- Nếu cần một con số mà bạn không chắc, hãy viết [CẦN KIỂM CHỨNG] thay vì đoán.

CÂU CHUYỆN BỘ 3 SẢN PHẨM
{combo["cach_noi_trong_video"]}
Ví von dễ nhớ: {combo["vi_von_de_nho"]["ten"]}
- Nattokinase = {combo["vi_von_de_nho"]["nattokinase"]}
- DHA EPA SQ = {combo["vi_von_de_nho"]["dha_epa_sq"]}
- Rich Coenzyme Q10 = {combo["vi_von_de_nho"]["coenzyme_q10"]}
Lưu ý khi bán: {combo["canh_bao_cach_ban"]}

LUẬT TUÂN THỦ - BẮT BUỘC, KHÔNG ĐƯỢC VI PHẠM
{_bullets(rules["quy_tac_bat_buoc"])}

Câu khuyến cáo bắt buộc phải xuất hiện nguyên văn trong kịch bản và trong caption:
"{rules["cau_bat_buoc"]["khuyen_cao"]}"

TUYỆT ĐỐI KHÔNG DÙNG các cụm sau (bên phải là cách nói thay thế):
{_bullets([f'"{p["cam"]}" -> "{p["thay_bang"]}"' for p in rules["tu_cam_va_tu_thay_the"]])}

Các câu an toàn nên dùng:
{_bullets(rules["cau_an_toan_nen_dung"])}

Y ĐỨC - {rf["tieu_de"]}
Nếu chủ đề có liên quan, hãy nhắc người xem những dấu hiệu cần đi khám ngay:
{_bullets(rf["danh_sach"])}
Cách nói: "{rf["cau_phai_noi_trong_video"]}"

ĐỊNH DẠNG KẾT QUẢ - luôn trả về Markdown đúng khung sau, không thêm lời dẫn nào khác:

# <Tiêu đề kịch bản>

> Triệu chứng: ... | Đối tượng: ... | Định dạng: ... | Nền tảng: ... | Thời lượng: ...s

## 1. Ý tưởng chính
Hai đến ba câu nói rõ video này muốn người xem hiểu điều gì và làm gì.

## 2. Hook - chọn 1 trong 3
1. ...
2. ...
3. ...

## 3. Kịch bản chi tiết

| Thời gian | Lời thoại | Hình ảnh / B-roll | Chữ trên màn hình |
|---|---|---|---|
| 0-3s | ... | ... | ... |

## 4. Ghi chú quay dựng
- Bối cảnh, ánh sáng, nhịp cắt, nhạc nền, tốc độ đọc.

## 5. Caption đăng bài
Phần caption hoàn chỉnh để dán thẳng lên nền tảng, kết thúc bằng câu khuyến cáo bắt buộc,
sau đó là 5 tới 8 hashtag.

## 6. Ba bình luận hay gặp và cách trả lời
- Hỏi: ... / Đáp: ...

## 7. Tự kiểm tra tuân thủ
- [x] Có câu khuyến cáo bắt buộc
- [x] Không có từ cấm
- [x] Không cam kết kết quả
- [x] Không dùng danh nghĩa nhân viên y tế
"""


def build_brief(
    *,
    symptom_key: str,
    persona_key: str,
    format_key: str,
    platform: str,
    duration: int | None = None,
    product_keys: list[str] | None = None,
    extra: str | None = None,
) -> str:
    """User prompt: đề bài cụ thể cho một video."""
    sym = kb.get_symptom(symptom_key)
    per = kb.get_persona(persona_key)
    fmt = kb.get_format(format_key)
    rules = kb.compliance()
    cta = kb.ctas()

    prods: list[dict[str, Any]] = (
        [kb.get_product(k) for k in product_keys]
        if product_keys
        else kb.products_for_symptom(symptom_key)
    )
    seconds = duration or fmt["thoi_luong_goi_y"]

    khung = "\n".join(
        f'- {b["giay"]}s | {b["muc_tieu"]} | {b["yeu_cau"]}' for b in fmt["cau_truc"]
    )
    hook_pool = "\n".join(f'- ({h["kieu"]}) {h["cau"]}' for h in kb.hooks_for(symptom_key))
    prod_block = "\n\n".join(_product_block(p) for p in prods)
    platform_note = rules["luu_y_nen_tang"].get(
        platform, "Viết chuẩn mực, không dùng từ ngữ gây tranh cãi."
    )

    cta_group = (
        cta["cta_manh"]
        if format_key in {"hook-noi-dau-giai-phap", "bo-ba-san-pham", "livestream"}
        else cta["cta_mem"] + cta["cta_trung_binh"]
    )
    hashtags = cta["hashtag_goi_y"]["chung"] + cta["hashtag_goi_y"].get(symptom_key, [])

    return f"""Viết một kịch bản video theo đề bài sau.

TRIỆU CHỨNG: {sym["ten"]}
Người xem cảm nhận thế nào: {sym["mo_ta_dan_da"]}
Nguyên nhân thường gặp:
{_bullets(sym["nguyen_nhan_thuong_gap"])}
Nỗi đau cảm xúc cần chạm tới:
{_bullets(sym["noi_dau_cam_xuc"])}

NGƯỜI XEM: {per["ten"]}
Hoàn cảnh: {per["hoan_canh"]}
Cách xưng hô và giọng điệu: {per["ngon_ngu_nen_dung"]}
Nỗi sợ lớn nhất: {per["noi_so_lon_nhat"]}
Điều họ muốn nghe: {per["dieu_ho_muon_nghe"]}

ĐỊNH DẠNG: {fmt["ten"]} - {fmt["khi_nao_dung"]}
Tổng thời lượng: {seconds} giây. Bám sát khung sau, được co giãn mốc thời gian cho khớp tổng thời lượng:
{khung}
{("Cảnh báo riêng của định dạng này: " + fmt["canh_bao"]) if fmt.get("canh_bao") else ""}

NỀN TẢNG: {platform}
Lưu ý nền tảng: {platform_note}

SẢN PHẨM ĐƯỢC NHẮC TỚI (chỉ nói đúng công dụng đã liệt kê, không thêm):
{prod_block}

NGÂN HÀNG HOOK ĐỂ THAM KHẢO - được sửa cho hợp video, không bắt buộc dùng nguyên văn:
{hook_pool}

GỢI Ý CÂU KÊU GỌI HÀNH ĐỘNG (chọn đúng một):
{_bullets(cta_group)}

HASHTAG GỢI Ý: {" ".join(hashtags)}
{("YÊU CẦU THÊM CỦA NGƯỜI ĐẶT: " + extra) if extra else ""}

Viết kịch bản ngay theo đúng khung định dạng đã quy định."""


def _product_block(p: dict[str, Any]) -> str:
    missing = [k for k, v in p.get("CAN_DIEN_THEM", {}).items() if not v]
    filled = {k: v for k, v in p.get("CAN_DIEN_THEM", {}).items() if v}
    lines = [
        f'### {p["ten"]} ({p["vai_tro"]})',
        f'Thành phần chính: {", ".join(p["thanh_phan_chinh"])}',
        "Cơ chế nói cho người thường hiểu:",
        _bullets(p["co_che_noi_don_gian"]),
        "Công dụng ĐƯỢC PHÉP nói (không được nói gì ngoài danh sách này):",
        _bullets(p["loi_ich_duoc_phep_noi"]),
        f'Phù hợp với: {"; ".join(p["phu_hop_voi"])}',
        "Lưu ý an toàn BẮT BUỘC nhắc nếu có nói tới sản phẩm này:",
        _bullets(p["luu_y_an_toan"]),
    ]
    if filled:
        lines.append(f"Thông tin sản phẩm: {json.dumps(filled, ensure_ascii=False)}")
    if missing:
        lines.append(
            "Chưa có dữ liệu về: "
            + ", ".join(missing)
            + ". Không được bịa. Nếu kịch bản cần tới, hãy viết [CẦN ĐIỀN] để người dùng tự điền."
        )
    return "\n".join(lines)
