# SOP — Set quảng cáo Meta cho page "Phạm Sơn sống khoẻ mỗi ngày"

> Luồng 3 phòng: **Phòng 3 · 🎬 Edivideo** (ra video) → **Phòng 7 · 👩 Lady Page** (set & chạy ads)
> → **Phòng 8 · 📊 Fanpage Pancake** + **Phòng 11 · 🔁 Check trùng đơn** (đọc đơn về).
>
> File này là bản hướng dẫn bấm tay từng bước, kèm luật đọc số và luật Keep/Kill/Scale.
> Chỗ nào ghi `[ANH ĐIỀN]` là số liệu thật, em **không** tự bịa.

---

## 0. Checklist đầu vào — thiếu 1 dòng là chưa được set ads

| # | Cần có | Trạng thái |
|---|---|---|
| 1 | Video từ Phòng 3 (Edivideo), đã qua QC ở mục 2 | ⬜ |
| 2 | Page **Phạm Sơn sống khoẻ mỗi ngày** — em/anh có quyền quảng cáo trên page | ⬜ |
| 3 | Tài khoản quảng cáo + thẻ thanh toán còn hoạt động, không bị hạn chế | ⬜ |
| 4 | Sản phẩm: tên, thành phần chính, công dụng **được phép nói**, giá lẻ, giá combo, quà tặng | `[ANH ĐIỀN]` |
| 5 | Bán qua đâu: Inbox Messenger / Form tin nhắn / Landing page + COD | `[ANH ĐIỀN]` |
| 6 | Kịch bản chào inbox + kịch bản sale (lấy từ Phòng 4 · ✍️ Kịch bản sale) | ⬜ |
| 7 | Ngân sách/ngày, ngân sách test tối đa, giá vốn, AOV, tỷ lệ chốt hiện tại | `[ANH ĐIỀN]` |
| 8 | Pancake đã nối page để đếm hội thoại & đơn (Phòng 8) | ⬜ |

**Thiếu mục 4, 5, 7 thì chưa set được**, vì không có căn cứ tính KPI — chạy sẽ tiêu tiền mù.

---

## 1. Nhận video từ Phòng 3 (Edivideo)

Yêu cầu file bàn giao:

- **Tỷ lệ:** 9:16 (Reels/Story) là chính; thêm bản 1:1 hoặc 4:5 cho Feed nếu có.
- **Độ dài:** 30–60 giây cho video bán hàng; bản cắt 15 giây để test hook.
- **Định dạng:** MP4 (H.264) + AAC, dưới 4GB, tối thiểu 1080×1920.
- **Phụ đề cháy sẵn (burn-in):** bắt buộc — phần lớn người xem tắt tiếng.
- **Chừa vùng an toàn:** chừa ~14% trên và ~20% dưới, tránh chữ bị UI Reels che.
- **Không** chèn logo/nút CTA giả dạng nút bấm của Facebook.

Quy ước tên file, để sau này đọc số biết ngay video nào:

```
DILI_A01-ProblemAware_H02-CauHoi_9x16_v1.mp4
     └ angle       └ hook          └ tỷ lệ └ phiên bản
```

**QC video trước khi upload** (video trượt 1 ô là trả về Phòng 3):

- [ ] 3 giây đầu có hook rõ, người xem hiểu ngay vì sao phải xem tiếp
- [ ] Có phụ đề, chữ đọc được trên điện thoại
- [ ] Không nêu tên bệnh, không "chữa khỏi", không before/after (xem mục 3)
- [ ] Có câu CTA ở cuối, khớp với nút CTA sẽ chọn trong Ads Manager
- [ ] Cuối video hoặc trong caption có dòng: *"Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."*

Nơi lưu: 1 thư mục Drive theo tuần, ví dụ `Video ads/2026-W35/`, để em lấy đúng bản và không upload nhầm bản nháp.

---

## 2. Cấu trúc chiến dịch — chọn theo cách bán

### 2A. Bán qua INBOX (mặc định cho page sức khoẻ, ngân sách nhỏ)

```
CAMPAIGN  — Mục tiêu: Tương tác (Engagement) → Vị trí chuyển đổi: Messenger
   └ AD SET  — Ngân sách ở ad set (ABO), tối ưu: Cuộc trò chuyện qua tin nhắn
        ├ AD 1  Angle 01 × Hook A
        ├ AD 2  Angle 01 × Hook B
        ├ AD 3  Angle 03 × Hook A
        └ AD 4  Angle 05 × Hook A
```

Chỉ **1 ad set** khi ngân sách test dưới ~1 triệu/ngày. Nhiều ad set = chia nhỏ dữ liệu = không ad nào đủ số để kết luận.

### 2B. Bán qua LANDING PAGE / FORM

```
CAMPAIGN  — Mục tiêu: Khách hàng tiềm năng (Leads)
   └ AD SET  — Vị trí chuyển đổi: Website (có Pixel + sự kiện Lead) hoặc Biểu mẫu tức thì
        └ 4 ads như trên
```

Bắt buộc trước khi chạy 2B: Pixel đã bắn `Lead` thật (test bằng Trình trợ giúp Pixel), không thì mù hoàn toàn.

**Chưa chốt cách bán thì chưa set campaign** — hai nhánh này khác nhau từ mục tiêu tới cách đọc số.

---

## 3. COMPLIANCE CHECK — làm TRƯỚC khi upload, không phải sau khi bị khoá

Quét cả video, caption và tiêu đề. Dính 1 ô là **STOP — COMPLIANCE RISK**, viết lại rồi mới chạy.

| Cấm | Vì sao | Viết lại an toàn |
|---|---|---|
| "Chữa khỏi", "đặc trị", "hết hẳn" | Biến TPBS thành thuốc — sai luật quảng cáo TPBS | "hỗ trợ", "giúp bổ sung", "chăm sóc" |
| Nêu tên bệnh (tiểu đường, ung thư, thoái hoá...) | Claim điều trị bệnh | Nói về biểu hiện sinh hoạt: "hay mỏi lưng khi ngồi lâu" |
| "Bạn đang bị đau khớp phải không?" | Meta cấm ám chỉ **thuộc tính sức khoẻ cá nhân** của người xem | "Nhiều cô chú tuổi 50+ hay gặp tình trạng này" |
| Ảnh/video before–after, ảnh cơ thể cận cảnh | Vi phạm chính sách quảng cáo Meta | Cảnh sinh hoạt thường ngày, cảnh sản phẩm |
| "Cam kết 100%", "khỏi sau 7 ngày" | Cam kết kết quả không có căn cứ | "Nhiều khách dùng đủ liệu trình phản hồi tích cực" (chỉ khi có phản hồi thật) |
| Doạ nạt quá mức ("không uống là tàn phế") | Nội dung gây sợ hãi | Nói lợi ích của việc chăm sóc sớm |
| Mượn hình bác sĩ / logo bệnh viện không có quyền | Rủi ro pháp lý + Meta | Chuyên gia thật, có giấy tờ, có xác nhận cho dùng hình |

Caption phải có dòng miễn trừ: *"Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."*

---

## 4. Các bước bấm trong Trình quản lý quảng cáo

**Bước 1 — Tạo chiến dịch**
1. Ads Manager → **Tạo** → mục tiêu **Tương tác** (bán inbox) hoặc **Khách hàng tiềm năng** (bán form/web).
2. Đặt tên theo quy ước ở mục 5.
3. Ngân sách: chọn **Ngân sách ở cấp nhóm quảng cáo (ABO)** khi test. Không bật Advantage+ campaign budget lúc test.
4. Tắt A/B test tự động của Meta — mình tự test bằng nhiều ad trong 1 ad set.

**Bước 2 — Nhóm quảng cáo (Ad set)**
1. **Vị trí chuyển đổi:** Messenger (chỉ tick Messenger; bỏ Instagram Direct/WhatsApp nếu không có người trực).
2. **Sự kiện tối ưu:** Cuộc trò chuyện qua tin nhắn.
3. **Ngân sách hằng ngày:** `[ANH ĐIỀN]` — xem mục 6.
4. **Lịch chạy:** bắt đầu 00:00 ngày mai, chạy liên tục. Không dùng lịch theo giờ khi mới test.
5. **Đối tượng:**
   - Vị trí: `[ANH ĐIỀN]` — nên loại trừ vùng giao hàng khó nếu bán COD.
   - Tuổi/giới: theo avatar sản phẩm, ví dụ 35–65+ `[ANH ĐIỀN]`.
   - Sở thích chi tiết: **để trống (broad)** ở vòng test đầu. Meta bây giờ tìm người theo creative tốt hơn mình đoán sở thích.
6. **Vị trí quảng cáo:** Tự động (Advantage+ placements). Test đủ số rồi mới cắt vị trí xấu.
7. Bật **Advantage+ audience** nếu tài khoản có — nhưng chỉ đổi 1 biến mỗi lần để còn biết cái gì tạo ra kết quả.

**Bước 3 — Quảng cáo (Ad)**
1. **Trang:** chọn **Phạm Sơn sống khoẻ mỗi ngày**. Kiểm tra lại tên page trước khi xuất bản — chọn nhầm page là mất sạch dữ liệu học của page đúng.
2. **Định dạng:** Video đơn → tải video từ mục 1. Thêm bản 1:1/4:5 ở phần "Tuỳ chỉnh theo vị trí".
3. **Ảnh thu nhỏ:** chọn khung có mặt người hoặc chữ hook, đừng để khung đen.
4. **Văn bản chính:** 3–6 dòng, theo khung HOOK → PROBLEM → MECHANISM → OFFER → CTA. Xuống dòng thoáng, không viết 1 khối chữ.
5. **Tiêu đề:** 1 câu, nhắc lại lợi ích chính hoặc offer.
6. **Nút kêu gọi:** **Gửi tin nhắn**.
7. **Lời chào tin nhắn:** soạn sẵn 3 câu — chào, hỏi 1 câu để phân loại, xin số điện thoại. Lấy từ Phòng 4.
8. **Theo dõi:** bật tham số URL/ref cho Pancake nếu Phòng 8 yêu cầu; kiểm tra Pixel nếu chạy nhánh web.
9. **Xuất bản** → chờ duyệt.

**Bước 4 — Sau khi xuất bản**
- Tự inbox thử vào page bằng nick khác: xem lời chào có chạy, có ai trả lời trong 5 phút không.
- Không sửa gì trong 24–48 giờ đầu (giai đoạn learning). Sửa là reset học lại, tiền test coi như bỏ.

---

## 5. Quy ước đặt tên — đọc số sống nhờ cái này

```
Campaign : DILI | MSG | TEST | 2026-08-27
Ad set   : BROAD | 35-65 | VN | Auto-PL | 200k
Ad       : A01-ProblemAware | H02-CauHoi | 9x16 | v1
```

Nguyên tắc: nhìn tên ad là biết **angle nào, hook nào, định dạng nào**. Không đặt tên kiểu "video 1", "test mới" — 3 ngày sau không ai đọc được dữ liệu nữa.

---

## 6. Ngân sách & KPI — tính ra từ số thật, không lấy số trên mạng

Anh cấp 5 số này, em tính ngược ra toàn bộ ngưỡng:

```
GIÁ BÁN (AOV)              = [ANH ĐIỀN]
GIÁ VỐN + ship + đóng gói  = [ANH ĐIỀN]
LƯƠNG/hoa hồng sale mỗi đơn= [ANH ĐIỀN]
TỶ LỆ CHỐT (số đơn / số hội thoại có SĐT) = [ANH ĐIỀN]
NGÂN SÁCH/NGÀY + NGÂN SÁCH TEST TỐI ĐA    = [ANH ĐIỀN]
```

Công thức:

```
Lợi nhuận gộp mỗi đơn = AOV − giá vốn − ship − hoa hồng
CPA tối đa            = Lợi nhuận gộp × 0,6   (chừa 40% làm lãi)
CPL mục tiêu          = CPA tối đa × Tỷ lệ chốt
ROAS hoà vốn          = AOV ÷ Lợi nhuận gộp
```

Ngân sách test vòng 1 (quy tắc chung, không phải con số ngành):
**ngân sách/ngày của ad set ≈ 3–5 × CPL mục tiêu**, chạy 3 ngày, tổng không vượt MAX TEST BUDGET.
Lý do: mỗi ngày cần vài lead thì Meta mới đủ tín hiệu để tối ưu.

Em **không** vượt ngân sách anh đặt, và **không** tự tăng ngân sách trước khi báo cáo.

---

## 7. Đọc số — bật đúng cột, đủ số mới kết luận

Cột cần bật trong Ads Manager (lưu thành preset "DILI MSG"):

`Số tiền đã chi · Lượt hiển thị · Tần suất · CPM · CTR (tất cả) · CTR liên kết · CPC · Cuộc trò chuyện qua tin nhắn · Chi phí/cuộc trò chuyện · Lượt xem video 3s · ThruPlay · Kết quả`

Cộng thêm số lấy từ Pancake (Phòng 8): số hội thoại **có SĐT**, số đơn, doanh thu, tỷ lệ chốt.

**Ngưỡng dữ liệu tối thiểu trước khi ra quyết định:**

| Cấp | Đủ số khi |
|---|---|
| Ad | chi ≥ 1× CPL mục tiêu **và** ≥ 1.000 lượt hiển thị |
| Kill sớm | chi ≥ 2× CPL mục tiêu mà **0** hội thoại |
| Kết luận angle | chi ≥ 3× CPL mục tiêu |

Chưa đủ số → **WAIT FOR DATA**. Không tắt ads vì "thấy nó chậm".

---

## 8. Luật Keep / Kill / Scale

| Trạng thái | Điều kiện | Hành động |
|---|---|---|
| 🟢 SCALE | CPL ≤ 0,8 × mục tiêu, đủ số, có đơn thật về | Tăng ngân sách 20–30%/lần, cách nhau 2 ngày. Hoặc nhân bản sang ad set mới. |
| 🟡 KEEP | CPL trong khoảng 0,8–1,2 × mục tiêu | Giữ nguyên, không đụng vào. |
| 🟠 WATCH | CPL 1,2–1,5 × mục tiêu, xu hướng chưa xấu hẳn | Theo dõi thêm 1 ngày, chuẩn bị hook mới. |
| 🔴 KILL | CPL > 2 × mục tiêu khi đã đủ số, hoặc chi 2× CPL mà 0 hội thoại | Tắt ad (không tắt cả ad set nếu ad khác đang tốt). |
| 🔵 NEW TEST | Mỗi tuần | Ít nhất 3 creative mới: 1 angle mới + 2 hook mới cho angle đang thắng. |

Thứ tự tìm winner: **Angle → Hook → Creative → Offer**.
Một video chết **không** kết luận được sản phẩm không bán được.

Khi scale: mỗi lần chỉ đổi **một** biến. Và luôn giữ bản gốc của creative đang thắng, không sửa đè lên nó.

---

## 9. Chẩn đoán nhanh — số xấu ở đâu thì soi chỗ đó

| Triệu chứng | Nghi phạm | Việc làm ngay |
|---|---|---|
| CPM cao | Đối tượng hẹp, cạnh tranh, creative kém tương tác | Mở broad, đổi creative, để vị trí tự động |
| CTR thấp (< ~1%) | **Hook và angle** | Đổi 3 giây đầu, đổi angle — không phải đổi target |
| CTR ổn nhưng ít inbox | Nút CTA, lời chào, tốc độ mở Messenger | Sửa lời chào, rút gọn câu hỏi đầu tiên |
| Nhiều inbox, ít số điện thoại | Kịch bản sale, tốc độ trả lời | Trả lời dưới 5 phút, hỏi SĐT ở lượt thứ 2 |
| Nhiều số, ít đơn | Chất lượng lead, giá, lời hứa trong ads | Đối chiếu lời hứa quảng cáo với thứ sale nói; xem lại offer |
| Tần suất tăng + CTR giảm + CPL tăng | **Creative fatigue** | Không tăng tiền — làm hook/angle/format mới (đặt Phòng 3) |

Không đổ lỗi cho quảng cáo khi nghẽn nằm ở khâu sale hoặc funnel — và ngược lại.

---

## 10. Báo cáo hằng ngày

```
DILI ADS DAILY REPORT — [ngày]
Chi tiêu:        Doanh thu:
Hội thoại:       Số SĐT:        Đơn:
CPM:  CTR:  CPC:  CPL:  CPA:  ROAS:

WINNERS   — ad nào, số nào chứng minh
LOSERS    — ad nào, đã tắt chưa
PROBLEMS  — nghẽn ở đâu trong funnel
ACTIONS   — làm gì, vì sao
NEW TEST  — creative gì, test giả thuyết gì
NGÂN SÁCH NGÀY MAI
KẾT QUẢ DỰ KIẾN
```

**Chế độ CEO** — báo cáo cho anh chỉ cần 5 câu:
1. Hôm nay quảng cáo tốt / trung bình / xấu?
2. Tiền đang mất ở đâu?
3. Cái gì đang hiệu quả?
4. Ngày mai làm gì?
5. Tại sao — dẫn số ra.

---

## 11. Nhịp làm việc mỗi ngày

| Giờ | Việc |
|---|---|
| 09:00 | Đọc số 24h qua, đối chiếu KPI, đánh dấu 🟢🟡🟠🔴 từng ad |
| 09:30 | Tắt loser, không đụng winner, ghi lại giả thuyết |
| 14:00 | Kiểm tra tốc độ trả lời inbox, tần suất, ngân sách còn |
| 21:00 | Xuất báo cáo ngày + chốt ngân sách ngày mai |
| Thứ 2 | Đặt Phòng 3 dựng 3 creative mới cho vòng test tuần |

---

## 12. Em cần anh cấp để tự chạy được

1. **Quyền:** thêm em vào tài khoản quảng cáo + page ở Business Manager (hoặc anh bấm, em soạn sẵn từng bước).
2. **Số liệu:** 5 dòng ở mục 6.
3. **Ranh giới phê duyệt:** mức nào em tự làm, mức nào phải hỏi. Đề xuất mặc định:
   - Tự làm: tắt ad lỗ, đổi creative, tăng/giảm ngân sách ≤ 30% trong hạn mức ngày.
   - Phải hỏi anh trước: tạo campaign mới, tăng ngân sách > 30%, đổi offer, đổi sự kiện tối ưu, tắt campaign chủ lực.
