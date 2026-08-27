# 03 — ANGLE · HOOK · PRIMARY TEXT · HEADLINE · CTA

## A. 10 ANGLE GỐC

| # | Angle | Mở bài bằng | Hợp với |
|---|---|---|---|
| 1 | Vấn đề | Mô tả đúng nỗi khổ hằng ngày | Cold traffic, thị trường đã biết vấn đề |
| 2 | Sai lầm phổ biến | "Nhiều người làm sai chỗ này" | Khách đã thử nhiều cách, chưa được |
| 3 | Cơ chế | "Vì sao nó xảy ra" | Sản phẩm có cơ chế khác biệt |
| 4 | Câu chuyện khách hàng | Một người cụ thể, mốc thời gian cụ thể | Sản phẩm cần niềm tin |
| 5 | Chuyên gia giải thích | Người có thẩm quyền nói | Ngành sức khoẻ, tài chính |
| 6 | Giáo dục thị trường | Dạy khách một điều họ chưa biết | Sản phẩm mới, khách chưa nhận ra vấn đề |
| 7 | Giải pháp | Đi thẳng vào sản phẩm + ưu đãi | Retargeting, khách đã biết |
| 8 | So sánh | Cách cũ vs cách mới | Thị trường đông đối thủ |
| 9 | FAQ | Trả lời câu khách hay hỏi | Retargeting, khách đang lưỡng lự |
| 10 | Objection Handling | Đập thẳng lý do khách chưa mua | Retargeting, lead chưa chốt |

**Quy tắc test:** mỗi lần test là test **angle**, không phải đổi vài chữ.
Mỗi angle phải có tối thiểu 2–3 hook và 2 format khác nhau trước khi kết luận nó thua.

## B. HOOK — LẤY TỪ NGÂN HÀNG CỦA PHÒNG 6, KHÔNG VIẾT LẠI

Phòng 6 (Video content sức khoẻ) đã có sẵn **60 hook** đã qua kiểm tuân thủ, kèm câu nối,
đối tượng và triệu chứng. Phòng Ads **dùng lại**, không tự chế hook mới cho cùng bộ sản phẩm.

```bash
# 10 hook mạnh nhất, có câu nối liền sau — cầm lên quay được ngay
git show origin/claude/ai-agent-health-video-content-rmedj9:docs/10-hook-manh-nhat.md

# ngân hàng đầy đủ 60 hook
git show origin/claude/ai-agent-health-video-content-rmedj9:knowledge/hooks.json

# personas, format, CTA, quy tắc tuân thủ
git show origin/claude/ai-agent-health-video-content-rmedj9:knowledge/personas.json
git show origin/claude/ai-agent-health-video-content-rmedj9:knowledge/formats.json
```

### Bản đồ Angle (Phòng 12) ↔ kiểu hook (Phòng 6)

| Angle | Lọc `kieu` trong `hooks.json` | Số hook có sẵn |
|---|---|---|
| 1 · Vấn đề | `dong-cam`, `cau-hoi` | 15 |
| 2 · Sai lầm phổ biến | `sai-lam-thuong-gap`, `phan-de` | 12 |
| 3 · Cơ chế | `vi-von`, `tiet-lo` | 4 |
| 4 · Câu chuyện khách hàng | `ke-chuyen` | 4 |
| 5 · Chuyên gia giải thích | `tiet-lo`, `con-so` | 11 |
| 6 · Giáo dục thị trường | `con-so`, `thoi-su-doi-song` | 11 |
| 7 · Giải pháp | `thu-thach`, `danh-cho-con-cai` | 4 |
| 8 · So sánh | `so-sanh` | 4 |
| 9 · FAQ | `doc-binh-luan`, `cau-hoi` | 10 |
| 10 · Objection Handling | `phan-de`, `canh-bao-nhe` | 11 |

### 5 personas dùng chung với Phòng 6

`phu-nu-45-55` · `dan-van-phong-30-45` · `nguoi-cao-tuoi-60` ·
`con-cai-mua-cho-bo-me` · `nguoi-mo-mau-huyet-ap`

Đặt tên ad theo persona để đối chiếu được với bảng lead:
`AngleB_Hook02_concai_video20s`.

### Ba hook Phòng 6 đánh giá mạnh nhất về khả năng ra đơn

- **"Có ba trường hợp tôi khuyên anh chị đừng mua của tôi."** — bán bằng sự thành thật.
- **"Ba câu hỏi, trả lời xong là biết mình nên bắt đầu từ đâu."** — khách tự phân loại ở bình luận.
- **"Bố mẹ kêu tê tay, đừng vội nghĩ là do tuổi già."** — người mua là con cái, chi trả cao hơn.

### Nguyên tắc hook (kế thừa từ Phòng 6, không sửa)

- 3 giây đầu quyết định phần lớn lượt xem hết video.
- Hook mô tả **cảm giác của người xem**, không giới thiệu bản thân, không nhắc sản phẩm.
- Một hook chỉ nói một ý.
- Tránh tên bệnh và từ y tế mạnh ngay câu đầu.
- Hook phải hứa điều mà thân video trả được.
- Đọc lên thành tiếng: nghe như quảng cáo thì viết lại.

**Kỵ:** mở bằng logo, tên thương hiệu, "Kính chào quý khách", nhạc intro.

### Khi nào Phòng Ads mới tự viết hook

Chỉ khi chạy sản phẩm **ngoài bộ 3** của Phòng 6, hoặc khi cần biến thể cho một angle
mà bank chưa phủ. Viết xong phải gửi ngược cho Phòng 6 để họ kiểm tuân thủ trước khi chạy.

## C. PRIMARY TEXT — 3 khung dùng được ngay

**Khung 1 — PAS (Problem · Agitate · Solution)**
```
[Câu hook chạm nỗi đau]
[2–3 dòng mô tả nó ảnh hưởng gì tới cuộc sống hằng ngày]
[Lý do các cách cũ chưa giải quyết được]
[Sản phẩm hỗ trợ ở điểm nào — nói cơ chế, không nói phép màu]
[Bằng chứng: con số, phản hồi, chuyên gia]
[CTA + điều khách nhận được khi để lại số]
```

**Khung 2 — Story**
```
[Tên/đặc điểm một người cụ thể + tình huống]
[Điều họ đã thử và vì sao chưa hiệu quả]
[Bước ngoặt: họ biết tới cách này]
[Kết quả — mô tả trung thực, có mốc thời gian]
[Lời mời: nếu bạn cũng đang như vậy thì...]
[CTA]
```

**Khung 3 — Objection Handling (dùng cho retargeting)**
```
"[Câu khách hay nói khi từ chối]" — nghe quen chứ?
[Thừa nhận là hợp lý]
[Đưa dữ kiện/bằng chứng khiến lo ngại đó nhẹ đi]
[Giảm rủi ro: tư vấn miễn phí / đổi trả / trả sau khi nhận]
[CTA]
```

Độ dài: mobile chỉ hiện ~125 ký tự đầu trước nút "Xem thêm" — **câu đầu phải đứng một mình được**.

## D. HEADLINE (dòng dưới ảnh/video, ~40 ký tự)

- Nói **kết quả**, không nói tên sản phẩm: "Đỡ [vấn đề] sau [thời gian] — tư vấn miễn phí"
- Hoặc nói **rào cản được gỡ**: "Không cần [việc khách ngại làm]"
- Hoặc nói **ưu đãi cụ thể**: "Tặng [quà] cho 50 người đăng ký hôm nay"

## E. CTA

Chọn theo mức độ sẵn sàng của khách:

| Traffic | CTA nên dùng |
|---|---|
| Cold | "Để lại số, được tư vấn miễn phí" · "Nhận bảng [thông tin hữu ích]" |
| Đã xem video / vào LP | "Xem còn suất ưu đãi không" · "Nhận báo giá hôm nay" |
| Lead chưa chốt | "Nhận lại ưu đãi đã đăng ký" · "Gọi lại cho tôi trong hôm nay" |

CTA phải nói **chuyện gì xảy ra tiếp theo** ("nhân viên gọi trong 15 phút"), không chỉ "Đăng ký ngay".

## F. Ma trận sản xuất — 1 tuần test

| | Hook 1 | Hook 2 | Hook 3 |
|---|---|---|---|
| **Angle A** | AD 01 | AD 02 | — |
| **Angle B** | AD 03 | AD 04 | — |
| **Angle C** | AD 05 | — | — |

Đặt tên ad theo đúng ô: `AngleA_Hook01_video15s`. Nhìn báo cáo là biết ngay hook nào kéo CTR,
angle nào ra lead thật.
