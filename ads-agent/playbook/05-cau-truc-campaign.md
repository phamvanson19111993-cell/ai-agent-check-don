# 05 — CẤU TRÚC CHIẾN DỊCH & NGÂN SÁCH

## A. Cấu trúc khởi động (ngân sách nhỏ)

```
CAMPAIGN: LEADGEN – [SẢN PHẨM] – [DDMM]      | Mục tiêu: Sales/Leads · Ngân sách ở cấp campaign (CBO)
└── AD SET 01 — BROAD
    │   Vị trí: [tỉnh/thành hoặc toàn quốc]
    │   Tuổi/Giới: chỉ giới hạn khi thật sự cần
    │   Sở thích: để trống (broad)
    │   Placements: Advantage+ (tự động)
    │   Tối ưu cho: Lead (conversion event trên website)
    ├── AD 01 — AngleA_Hook01
    ├── AD 02 — AngleA_Hook02
    └── AD 03 — AngleB_Hook01
```

**Vì sao 1 ad set:** ngân sách nhỏ chia nhiều ad set → mỗi ad set không đủ conversion để thoát
learning → Meta học chậm, giá đắt, số liệu nhiễu. Gom lại cho Meta đủ dữ liệu học.

**Vì sao broad:** với mô hình leadgen, tệp broad + creative đúng thường rẻ hơn tệp interest hẹp,
vì chính creative làm nhiệm vụ lọc người.

## B. Khi nào mới tách ad set

- Tách **retargeting** ra khỏi cold — bắt buộc, vì thông điệp khác nhau.
- Tách khi test **audience thật sự** (ví dụ 2 vùng địa lý có giá khác nhau rõ rệt).
- Tách khi **scale**: nhân bản ad set thắng sang campaign scale riêng.
- **Không** tách chỉ vì muốn "thử cho biết".

## C. Quy tắc đặt tên

```
Campaign : LEADGEN – TPCN_XUONGKHOP – 0612
Ad set   : BROAD_18-65_TOANQUOC          |  RTG_LPVIEW_14D  |  RTG_VIDEO75_30D
Ad       : AngleA_Hook01_video15s        |  AngleC_Hook02_anh
```

Tên ad **phải chứa Angle + Hook + Format**. Đây là điều kiện để đọc báo cáo ra kết luận,
và để cột `utm_content` trong bảng lead có nghĩa.

## D. Ngân sách

- Ngân sách ngày của ad set nên đủ để mua được **vài conversion mỗi ngày** —
  ước lượng thô: `ngân sách ngày ≈ 3–5 × CPL mục tiêu`. Thấp hơn thì Meta học rất chậm.
- Để CBO ở cấp campaign khi có nhiều ad set; ABO khi muốn ép ngân sách cho một ad set đang test.
- **Không đổi ngân sách mỗi ngày.** Mỗi lần đổi lớn là một lần đẩy ad set về learning.

## E. Lịch test 7 ngày

| Ngày | Việc |
|---|---|
| 1–2 | Chạy 3–5 ad, không đụng vào. Chỉ kiểm tra tracking có nhận `Lead` không |
| 3 | Đọc CTR + CPL. Tắt ad tiêu đủ ngưỡng mà chưa có lead nào |
| 4–5 | Nạp thêm 2 ad mới từ angle có tín hiệu tốt nhất |
| 6 | Đối chiếu bảng lead: ad nào ra lead **nghe máy được**, ad nào ra số rác |
| 7 | Chốt winner → cân nhắc scale. Loser → tắt hoặc làm lại creative |

## F. Ngưỡng dữ liệu tối thiểu trước khi phán

- Một **ad** chỉ đáng kết luận khi đã tiêu ≈ **1× CAC hoà vốn** trở lên.
- Một **angle** chỉ đáng kết luận khi đã thử ≥ 2 hook × 2 format.
- **Chất lượng lead** chỉ đáng kết luận khi đã có ≥ 20–30 lead của cùng nguồn đó được gọi hết.

Chưa đủ ngưỡng → giữ nguyên và chờ, đừng tắt sớm rồi kết luận "angle này không ăn".
