# HƯỚNG DẪN TẠO ZALO OA — TỪNG BƯỚC MỘT

> Dành cho anh Sơn — DILI Supplement.
> **Chỉ anh làm được**, vì cần giấy phép kinh doanh, CCCD và mã OTP về số của anh.
> Làm xong bước 3 là bot Zalo của Phòng 9 chạy được.

---

## ⚠️ ĐỌC TRƯỚC — CÓ HAI THỨ KHÁC NHAU, ĐỪNG NHẦM

Nhiều người làm xong OA rồi tưởng xong, hoá ra bot vẫn không chạy. Vì cần **cả hai**:

| | Là gì | Ở đâu | Cho cái gì |
|---|---|---|---|
| **① Zalo OA** | Tài khoản chính thức của DILI | `oa.zalo.me` | Để có tài khoản, nhắn tin, xác thực |
| **② Zalo App** | Ứng dụng lập trình, nối vào OA | `developers.zalo.me` | Để lấy `APP_ID`, `APP_SECRET`, token cho **bot** |

**Làm ① trước, xong mới làm được ②.** Bot của Phòng 9 cần cả `ZALO_APP_ID`,
`ZALO_APP_SECRET` và `ZALO_REFRESH_TOKEN` — ba thứ này đều đến từ ②.

---

# PHẦN 0 — CHUẨN BỊ TRƯỚC KHI NGỒI VÀO MÁY

Gom đủ 6 thứ này rồi hãy bắt đầu, không thì làm giữa chừng phải dừng:

- [ ] **Giấy phép kinh doanh** — scan/chụp rõ, đủ các trang
- [ ] **CCCD người đại diện pháp luật** — chụp 2 mặt, phải **khớp tên trên GPKD**
- [ ] **Mã số thuế / mã số doanh nghiệp**
- [ ] **Số điện thoại Việt Nam chính chủ** — để nhận OTP. Chỉ số **+84** mới tạo được OA
- [ ] **Logo DILI** — ảnh vuông, tối thiểu 500×500px, nền sáng
- [ ] **Ảnh bìa** — ảnh ngang, ảnh cửa hàng hoặc banner sản phẩm

> 💡 Chụp bằng điện thoại cũng được, miễn **rõ chữ, không loá, không cắt góc**.
> Ảnh mờ là lý do bị trả hồ sơ nhiều nhất.

---

# 🔴 BƯỚC 1 — KIỂM TRA TÊN (làm trước, đừng bỏ qua)

**Đây là bước hỏng nhiều nhất.** Làm sai là mất cả tuần chờ duyệt lại.

Anh mở giấy phép kinh doanh, đọc **tên chính xác từng chữ** ghi trên đó.

Zalo bắt tên OA phải khớp **tên trên GPKD** hoặc **tên thương hiệu đã đăng ký**.

| Nếu GPKD ghi | Đặt tên OA |
|---|---|
| "Công ty Cổ phần DILI Supplement" | **DILI Supplement** ✅ |
| "Công ty CP 5SPRO" mà muốn đặt "DILI Supplement" | ⚠️ Phải có giấy tờ chứng minh thương hiệu DILI, **hoặc** đặt theo tên 5SPRO |
| "Hộ kinh doanh Phạm Văn Sơn" | ⚠️ Đặt "DILI Supplement" sẽ bị từ chối |

> 📌 Trong hồ sơ sản phẩm của bên mình, **đơn vị công bố và nhập khẩu là Công ty Cổ phần
> 5SPRO**. Anh kiểm xem GPKD anh dùng để đăng ký là 5SPRO hay pháp nhân khác — **tên OA
> phải theo đúng cái giấy anh nộp.**

**Anh đọc xong nhắn em tên trên GPKD, em nói anh nên đặt tên OA thế nào cho qua ngay lần đầu.**

---

# PHẦN ① — TẠO ZALO OA

## Bước 2 — Vào trang và đăng nhập

1. Mở trình duyệt trên máy tính (**đừng làm trên điện thoại**, khó thao tác hơn nhiều)
2. Vào **`oa.zalo.me`**
3. Bấm **Đăng nhập**, dùng **tài khoản Zalo cá nhân của anh** (Phạm Sơn – Sống Khoẻ Mỗi Ngày)
4. Xác nhận OTP về điện thoại anh

> 🔑 Tài khoản Zalo cá nhân đăng nhập lần đầu này sẽ thành **chủ sở hữu OA**. Nhớ dùng đúng
> tài khoản anh giữ lâu dài, đừng dùng tài khoản của nhân viên.

## Bước 3 — Tạo Official Account

1. Bấm **"Tạo Official Account mới"**

2. **Chọn loại tài khoản: DOANH NGHIỆP**

   > 🔴 **Chỗ này sai là phải làm lại từ đầu.** Zalo có mấy loại: Doanh nghiệp, Cơ quan
   > nhà nước, Nội dung (người nổi tiếng)…
   > **Phải chọn Doanh nghiệp.** Loại khác không dùng được ZNS và API cho bot.
   > Hộ kinh doanh, cửa hàng bán lẻ cũng chọn Doanh nghiệp.

3. **Chọn danh mục con:** nhóm **Sức khoẻ** → **Thực phẩm chức năng** (hoặc mục gần nhất
   có trong danh sách)

4. **Điền thông tin:**

| Ô | Điền gì |
|---|---|
| **Tên OA** | Theo kết quả Bước 1 — khớp GPKD |
| **Mô tả** | Ngắn gọn: bên mình bán gì, ở đâu. Ví dụ: *"DILI Supplement — phân phối thực phẩm bảo vệ sức khoẻ nhập khẩu chính hãng từ Nhật Bản."* |
| **Ảnh đại diện** | Logo vuông ≥ 500×500px |
| **Ảnh bìa** | Ảnh ngang |

> ⚠️ **Mô tả không được viết công dụng chữa bệnh.** Không ghi "hỗ trợ điều trị", "chữa
> mất ngủ"… Viết về **công ty**, đừng viết về **công dụng sản phẩm**.

5. Bấm **Tạo**

→ Xong bước này OA đã tồn tại, nhưng đang ở trạng thái **"Chưa xác thực"**, chưa dùng
được đầy đủ tính năng.

## Bước 4 — Xác thực OA

1. Trong trang quản lý OA, vào **Quản lý** → **Quản lý tài khoản** → **Xác thực OA**

2. **Nộp bộ hồ sơ 1A** — tải ảnh lên:
   - Giấy phép kinh doanh (scan rõ)
   - CCCD người đại diện pháp luật, **cả 2 mặt**

3. **Nộp bộ hồ sơ 1B** — công văn xác thực:
   - **Tải mẫu công văn** ngay trên trang Zalo về
   - Điền đúng **mã số thuế / mã số doanh nghiệp**
   - **Ký tên + đóng dấu** công ty
   - Scan rồi tải lên

4. Bấm **Gửi hồ sơ** → chờ Zalo duyệt

### Bị trả hồ sơ thì thường vì mấy lý do này

| Lý do | Cách sửa |
|---|---|
| Tên OA không khớp GPKD | Sửa tên OA theo đúng giấy — quay lại Bước 1 |
| Ảnh giấy tờ mờ, cắt góc, loá | Chụp lại nơi đủ sáng, đặt giấy phẳng, chụp thẳng từ trên xuống |
| Công văn thiếu dấu hoặc thiếu chữ ký | Ký và đóng dấu đầy đủ rồi scan lại |
| Mã số thuế điền sai | Đối chiếu lại với GPKD từng số |
| CCCD hết hạn, hoặc tên khác tên trên GPKD | Phải đúng người đại diện pháp luật ghi trên giấy |

---

# PHẦN ② — TẠO ZALO APP CHO BOT

> Chỉ làm được **sau khi OA đã xác thực xong**.
> Đây là phần lấy 3 chìa khoá cho bot của Phòng 9.

## Bước 5 — Tạo ứng dụng

1. Vào **`developers.zalo.me`**, đăng nhập **cùng tài khoản Zalo** đã tạo OA
2. Bấm **Tạo ứng dụng mới**
3. Điền tên ứng dụng — ví dụ *"DILI CSKH Bot"*, chọn loại phù hợp
4. Vào phần **Official Account API** → **liên kết ứng dụng với OA** vừa tạo
5. Xin quyền gửi/nhận tin nhắn cho OA

## Bước 6 — Lấy 3 chìa khoá

Trong trang ứng dụng, anh sẽ thấy:

| Lấy ở đâu | Điền vào đâu (file `.env` của bot) |
|---|---|
| **App ID** | `ZALO_APP_ID=` |
| **App Secret / Secret Key** | `ZALO_APP_SECRET=` và `ZALO_OA_SECRET_KEY=` |
| **Refresh Token** (qua bước cấp quyền OAuth) | `ZALO_REFRESH_TOKEN=` |

> 🔴 **Ba chuỗi này là chìa khoá vào tài khoản Zalo doanh nghiệp của anh.**
> - **Không gửi cho em, không gửi vào chat này, không chụp màn hình đưa lên đâu cả**
> - **Không commit lên GitHub** — repo đang công khai
> - Chỉ điền thẳng vào file `.env` trên máy chủ chạy bot
> - Ai xin ba chuỗi này qua Zalo hay điện thoại đều là **lừa đảo**

## Bước 7 — Khai báo webhook

Bot cần một địa chỉ để Zalo đẩy tin nhắn khách vào:

1. Trong trang ứng dụng, tìm mục **Webhook**
2. Điền địa chỉ máy chủ chạy bot, dạng: `https://<tên-miền-của-anh>/webhook`
3. Chọn nhận sự kiện **tin nhắn từ người dùng**

> Phần này **Phòng 9 làm cùng anh**, vì cần máy chủ có tên miền HTTPS.
> Hướng dẫn kỹ thuật đầy đủ ở nhánh Phòng 9: `docs/SETUP-ZALO.md`.

---

# CHECKLIST TỔNG — in ra tích dần

```
CHUẨN BỊ
[ ] Giấy phép kinh doanh (scan rõ)
[ ] CCCD người đại diện, 2 mặt
[ ] Mã số thuế
[ ] SĐT Việt Nam chính chủ
[ ] Logo vuông ≥ 500x500
[ ] Ảnh bìa

PHẦN ① — OA
[ ] Bước 1: đọc tên trên GPKD, chốt tên OA
[ ] Bước 2: đăng nhập oa.zalo.me
[ ] Bước 3: tạo OA, chọn DOANH NGHIỆP, danh mục Sức khoẻ
[ ] Bước 4: nộp hồ sơ 1A + 1B, chờ duyệt
[ ] OA hiện trạng thái ĐÃ XÁC THỰC

PHẦN ② — APP CHO BOT
[ ] Bước 5: tạo app trên developers.zalo.me, liên kết OA
[ ] Bước 6: lấy App ID, App Secret, Refresh Token
[ ] Bước 7: khai báo webhook (làm cùng Phòng 9)

SAU KHI XONG
[ ] Phòng 9 điền .env và chạy bot
[ ] Nhắn thử từ một tài khoản Zalo khác vào OA để kiểm tra
```

---

# LÀM XONG OA RỒI THÌ ĐƯỢC GÌ

| Có OA xác thực | Chưa có OA |
|---|---|
| Bot Zalo Phòng 9 nhận và trả lời tin khách 24/7 | Bot nằm im, không nhận được tin nào |
| Đăng ký được ZBS/ZNS gửi tin xác nhận đơn, nhắc lịch | Không gửi được |
| Khách thấy dấu tích xác thực, tin tưởng hơn | Nhắn tay từ Zalo cá nhân |
| Nhiều nhân viên cùng trực một tài khoản | Chỉ một người một máy |

> ⚠️ Nhưng nhắc lại điều em đã nói: **OA không thay được việc nhắn tay.**
> Tin hỏi thăm tâm tình với các cô chú vẫn nên nhắn tay từ Zalo cá nhân — ZNS
> không duyệt loại nội dung đó. Chi tiết ở [`dang-ky-zalo-oa-zns.md`](./dang-ky-zalo-oa-zns.md).

---

## Anh làm Bước 1 trước nhé

Mở giấy phép kinh doanh, đọc tên trên đó rồi nhắn em. Em nói anh biết nên đặt tên OA thế nào
cho qua duyệt ngay lần đầu, khỏi mất tuần chờ làm lại.
