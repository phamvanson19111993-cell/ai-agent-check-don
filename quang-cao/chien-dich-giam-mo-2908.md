# CHIẾN DỊCH ELLAGIC ACID — vòng 1 · 29/08/2026

> Trang đích: **https://sonsongkhoe.com/giam-mo/**
> Tài khoản: **2260044828113956** (Phạm Sơn BM1.1) — đúng BM đang chạy Q10
> Trang: **61592861334561** (DiLiM Supplement) · Pixel: **1277743445418211**
> Cùng tài khoản, cùng Pixel, cùng tên miền với Q10 — nên số liệu hai sản phẩm
> so sánh được với nhau, không phải đoán.

---

## 0. Ai làm gì

| Việc | Xong chưa | Ai làm |
|---|---|---|
| Trang bán đứng trên tên miền, thư mục con `/giam-mo/` | ✅ | Claude |
| Đơn có chỗ về (biểu mẫu Google) | ✅ tạm | Claude |
| Ảnh quảng cáo 4:5 | ✅ | Claude |
| Chữ quảng cáo 3 nhóm tuổi, soát luật xong | ✅ | Claude |
| **Bấm tạo chiến dịch trên Facebook** | ❌ | **Anh Sơn** |
| **Thử Pixel bắn `Lead` thật** | ❌ | **Anh Sơn** |

**Vì sao Claude không tự bấm được:** máy chạy Claude bị chặn toàn bộ đường ra
facebook.com và graph.facebook.com (cổng trả 403 cho mọi kết nối). Không phải
thiếu quyền trong BM — là chặn ở tầng mạng. Nên phần bấm nút phải chạy ở máy anh.

---

## 1. Anh chạy hai lệnh này

Anh chốt **chạy một nhóm trước** — đúng theo SOP. Nên thêm `--nhom 1`:

```bash
python3 kiem-quang-cao.py giam-mo                     # soát luật, ra "ĐẠT" mới đi tiếp
python3 tao-chien-dich.py --san-pham giam-mo --nhom 1
```

Chỉ dựng Nhóm 1 (nữ 30-45), 300.000đ/ngày. Hai nhóm kia **không được tạo ra** —
không có cái công tắc nào nằm đó để gạt nhầm thành 900.000đ.

Sau này muốn mở thêm thì chạy lại `--nhom 2`. Chương trình tìm lại chiến dịch cũ
theo tên và thêm nhóm mới vào đó, không dựng thêm chiến dịch trùng tên.

Lệnh thứ hai hỏi **mã token**, dán vào rồi Enter (chữ không hiện lên màn hình,
đó là bình thường). Ba số còn lại đã điền sẵn trong file.

Cách lấy token nằm ở cuối `tao-chien-dich.py`. Nhanh nhất:
developers.facebook.com/tools/explorer → quyền `ads_management` + `business_management`
→ Generate Access Token.

**Chương trình dựng mọi thứ ở trạng thái TẠM DỪNG.** Không một đồng nào bị tiêu
cho tới khi anh vào Ads Manager tự gạt nút. Cố ý như vậy để anh soi lại một lượt.

---

## 2. Nó dựng ra cái gì

```
CHIẾN DỊCH  Giam mo · Ellagic Acid · Vong 1 · 2908      mục tiêu Doanh số
└── NHÓM 1 · nữ 30-45   ·  300.000đ/ngày  ·  tối ưu cho Lead
    └── QC · Nhom 1 · nu 30-45
```

Bật phải gạt **đủ ba tầng**: chiến dịch → nhóm → quảng cáo. Thiếu một tầng là
không đồng nào chạy, mà nhìn trên Ads Manager lại tưởng đã bật rồi. Lỗi này rất
hay gặp vì chương trình dựng mọi thứ ở trạng thái tạm dừng.

Toàn quốc · sở thích để trống (broad) · vị trí tự động · tắt Advantage+ creative
(nó tự đổi chữ, dễ phá câu khuyến cáo bắt buộc).

### Ngân sách

**300.000đ/ngày, một nhóm, ba ngày không đụng vào.**

Đối chiếu để biết ba ngày đó mua được gì: Q10 trên cùng tài khoản, cùng Pixel,
cùng tên miền đo được 849đ mỗi lượt xem trang đích (28/08).
300.000đ ≈ 353 lượt/ngày → ba ngày ≈ 1.060 lượt, vừa đủ mốc quyết định 1.000 lượt.

Tới 1.000 lượt mà vẫn 0 đơn thì chỉ còn khoảng 0,7% khả năng là do may rủi —
nghĩa là trang hoặc lời chào hàng có vấn đề, đổ thêm tiền không cứu được.

Đây đúng theo SOP Phòng 7 mục 2A: ngân sách test dưới ~1 triệu/ngày thì chạy
**một nhóm**, vì chia nhỏ ra thì không nhóm nào đủ số để kết luận gì.

---

## 2b. CHẶN TRƯỚC MẮT — tài khoản đang đụng trần chi tiêu

Ảnh Ads Manager 29/08 của anh Sơn ghi rõ:

> *"Quảng cáo của bạn dừng chạy vì bạn đã đạt giới hạn chi tiêu của tài khoản
> quảng cáo cho Phạm Sơn BM1.1"* — chiến dịch `Q10 · T9 · Tiếp cận mới` vẫn bật,
> nhưng cột Phân phối là **"Đã đạt giới hạn chi tiêu"**.

Nghĩa là **tài khoản đang không tiêu được đồng nào**, không riêng Q10. Dựng
chiến dịch giảm mỡ lên rồi bật, nó cũng nằm im y như vậy — mà nhìn thì tưởng
quảng cáo kém, tưởng trang không ra đơn.

**Sửa trước khi làm gì khác:**
Ads Manager → **Cài đặt thanh toán** → **Giới hạn chi tiêu tài khoản** →
tăng hạn mức, hoặc bấm **Đặt lại số tiền đã chi**.

`tao-chien-dich.py` nay tự đọc `spend_cap` và `amount_spent` của tài khoản.
Đụng trần thì nó in cảnh báo và hỏi lại trước khi dựng, không lặng lẽ dựng xong
để anh tưởng đã chạy.

---

## 3. TRƯỚC KHI GẠT NÚT BẬT — ba việc, thiếu một là chạy mù

**3.1 · Thử Pixel bắn `Lead` thật.**
Trình quản lý sự kiện → Pixel 1277743445418211 → **Test Events** → mở
https://sonsongkhoe.com/giam-mo/ trên điện thoại → điền phiếu thật → bấm đặt hàng.
Phải thấy `PageView` rồi `Lead`. **Không thấy `Lead` thì dừng.** Nhóm quảng cáo
đang tối ưu vào `Lead` — Pixel không bắn thì Meta không có gì để học, tiền chỉ đi ra.
Đây đúng là lỗi đã làm hỏng ba chiến dịch trên tài khoản thuê (xem `lenh.json`).

**3.2 · Thử đơn có về bảng không.**
Đơn thử ở bước 3.1 phải hiện ra trong bảng đơn của trang Q10, dòng đầu ghi
`Sản phẩm: ELLAGIC ACID (hỗ trợ giảm béo) — túi 60 viên`.
Không thấy dòng đó thì **báo Claude ngay** — nhân viên sẽ giao nhầm hàng Q10.

**3.3 · Dặn nhân viên trực.**
Đơn giảm mỡ và đơn Q10 đang rơi chung một bảng. Nhân viên phải đọc dòng
"Sản phẩm" ở đầu mỗi đơn trước khi gọi. Đây là đường tạm; đường đúng là bảng
riêng, cần anh triển khai Apps Script rồi đưa Claude link `/exec`.

---

## 4. Ba ngày đầu — không đụng vào

Sửa bất cứ thứ gì trong 24–48 giờ đầu là Meta học lại từ đầu, tiền test coi như bỏ.

Ngày 4 gửi Claude đúng những số này, không cần đẹp:

```
Chi tiêu · Lượt hiển thị · Tần suất · CPM · CTR liên kết · CPC
Lượt xem trang đích · Lead · Chi phí mỗi Lead
```

Cộng thêm từ bảng đơn: bao nhiêu số đã gọi, bao nhiêu nghe máy, bao nhiêu chốt.
Thiếu phần này thì chỉ đánh giá được nửa phễu — biết quảng cáo ra form,
không biết quảng cáo ra **đơn**.

---

## 5. Luật tắt / giữ / tăng (theo SOP Phòng 7 mục 8)

| Trạng thái | Điều kiện | Làm gì |
|---|---|---|
| 🟢 TĂNG | CPL ≤ 0,8 × mục tiêu, đủ số, có đơn thật | Tăng 20–30% mỗi lần, cách nhau 2 ngày |
| 🟡 GIỮ | CPL trong khoảng 0,8–1,2 × mục tiêu | Không đụng vào |
| 🟠 THEO DÕI | CPL 1,2–1,5 × mục tiêu | Thêm 1 ngày, chuẩn bị chữ mới |
| 🔴 TẮT | CPL > 2 × mục tiêu khi đã đủ số, hoặc chi 2× CPL mà 0 Lead | Tắt riêng nhóm đó |

Chưa đủ số thì **chờ**, không tắt vì "thấy nó chậm".
CTR thấp là lỗi **câu mở đầu và góc tiếp cận**, không phải lỗi nhắm đối tượng.

---

## 6. Ranh giới đã tự đặt cho chữ quảng cáo

Giấy xác nhận nội dung quảng cáo **1581/2024/XNQC-ATTP** chỉ cho phép nói một câu:
**"Hỗ trợ giảm béo."**

Nên cả ba mẫu đều **không** nói: mỡ nội tạng · vòng eo · số cân · số ngày ·
cam kết · ảnh trước–sau. Cả ba đều có số công bố 3993/2024/ĐKSP, có đối tượng
không dùng được, và có đủ dòng khuyến cáo.

`kiem-quang-cao.py` soát tự động những cái này. Sửa chữ xong nhớ chạy lại nó.

> Ghi thêm, ngoài phạm vi việc này: chạy `python3 kiem-quang-cao.py q10` thì hồ sơ
> Q10 đang trượt vài mục — dùng chữ "duy nhất", và cả ba mẫu đều không nêu
> đối tượng không dùng được. Chưa sửa vì Q10 đang chạy; anh quyết có sửa không.
