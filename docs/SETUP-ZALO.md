# Nối Zalo OA vào bot — hướng dẫn từng bước

Toàn bộ việc dưới đây **anh tự làm trên máy/máy chủ của anh**. Em (Claude) không đăng nhập
được vào tài khoản Zalo của anh, và anh cũng **không nên gửi mật khẩu, `app_secret` hay
`refresh_token` cho bất kỳ ai**, kể cả trong khung chat này.

Thời gian: khoảng 10 phút.

---

## Bước 0 — Chuẩn bị

- Một **Official Account** (tạo tại <https://oa.zalo.me>), anh là quản trị viên.
- Node.js 20 trở lên trên máy.
- Mã nguồn này: `git clone` rồi `npm install`.

> **Vì sao phải là OA, không phải Zalo cá nhân?** Zalo chỉ mở API chính thức cho Official
> Account. Việc tự động hoá tài khoản Zalo cá nhân (đăng nhập hộ, gửi tin thay người dùng)
> vi phạm điều khoản của Zalo và tài khoản có thể bị khoá — nên bot này đi đường OA.

## Bước 1 — Tạo ứng dụng trên Zalo for Developers

1. Vào <https://developers.zalo.me> → **Tạo ứng dụng mới**.
2. Trong ứng dụng, thêm sản phẩm **Official Account API** và **liên kết OA** của anh.
3. Ghi lại **App ID** và **App Secret Key** (mục *Thông tin ứng dụng*).
4. Mục *Đăng nhập* / *Callback URL*, thêm địa chỉ nhận callback OAuth:

   ```
   http://localhost:3000/oauth/callback
   ```

   Nếu Zalo không chấp nhận `localhost`, dùng tunnel: chạy `ngrok http 3000` rồi khai
   `https://<id>.ngrok-free.app/oauth/callback`, và khi lấy token thì thêm
   `--redirect=https://<id>.ngrok-free.app/oauth/callback`.

## Bước 2 — Điền thông tin vào `.env`

```bash
cp .env.example .env
```

Mở `.env`, điền:

```ini
ZALO_APP_ID=<App ID>
ZALO_APP_SECRET=<App Secret Key>
ANTHROPIC_API_KEY=<key từ console.anthropic.com>
```

Để trống `ANTHROPIC_API_KEY` thì bot vẫn chạy, nhưng ở chế độ regex (không hiểu câu chữ tự do).

## Bước 3 — Lấy refresh token

```bash
npm run token
```

Script in ra một đường link. Mở link bằng trình duyệt **đang đăng nhập tài khoản quản trị OA**,
bấm **Cho phép**. Zalo gọi ngược về máy anh, script tự đổi lấy token và in ra:

```
ZALO_REFRESH_TOKEN=xxxxxxxx
```

Dán dòng đó vào `.env`. Xong bước khó nhất.

Nếu callback phải về máy chủ thật (không phải máy anh):

```bash
npm run token -- --url-only        # in link + lưu code_verifier
npm run token -- --code=<code>     # dán code lấy được từ URL callback
```

> ⚠️ Refresh token của Zalo **chỉ dùng được một lần**. Mỗi lần bot làm mới access token,
> Zalo trả token mới và app tự ghi đè vào `data/zalo-token.json`. Đừng xoá file này, và
> nếu chạy nhiều máy chủ cùng lúc thì phải dùng chung một nơi lưu token (xem README).

## Bước 4 — Khai báo Webhook

Bot cần một địa chỉ **HTTPS công khai**. Lúc thử nghiệm:

```bash
npm start          # cổng 3000
ngrok http 3000    # cửa sổ terminal khác
```

Vào ứng dụng trên developers.zalo.me → **Official Account API → Webhook**:

- Webhook URL: `https://<domain-của-anh>/webhook`
- Bật sự kiện: `user_send_text`, `follow`, `user_send_image`

## Bước 5 — Thử

Nhắn tin cho OA của anh từ Zalo cá nhân: `cho hỏi đơn DH123456`.

Bot dùng dữ liệu mẫu trong `data/orders.json` nên trả lời được ngay. Muốn nối vào hệ thống
đơn hàng thật thì đặt `ORDER_PROVIDER=http` và `ORDER_API_BASE_URL` (xem README).

---

## Lỗi thường gặp

| Hiện tượng | Nguyên nhân / cách xử lý |
|---|---|
| `redirect_uri mismatch` khi bấm link uỷ quyền | Callback URL trong app Zalo phải **trùng từng ký tự** với `--redirect` / `ZALO_REDIRECT_URI` |
| `Doi code lay token that bai` | Code chỉ sống vài phút — chạy lại `npm run token`. Kiểm tra lại `ZALO_APP_SECRET` |
| Log `webhook.rejected reason=invalid_signature` | `ZALO_OA_SECRET_KEY` sai. Nếu OA dùng khoá ký riêng, điền khoá đó thay vì app secret |
| Không thấy log webhook nào | Zalo không gọi tới được — kiểm tra URL đã là HTTPS công khai và đã bật đúng sự kiện |
| Zalo trả lỗi `-216` liên tục | Refresh token đã bị dùng ở nơi khác. Chạy lại `npm run token` và chỉ chạy **một** instance |
| Bot trả lời chung chung, không tra được đơn | Chưa có `ANTHROPIC_API_KEY`, hoặc mã đơn không có trong nguồn dữ liệu |

## Bảo mật

> 🔴 **Repo này đang CÔNG KHAI** — ai trên Internet cũng đọc được mọi file ở mọi nhánh.
> Một dòng `.env` lỡ commit là app secret của OA nằm ngoài đó vĩnh viễn (xoá commit sau
> cũng không lấy lại được, phải tạo lại secret key).

- `.env` và `data/zalo-token.json` đã nằm trong `.gitignore` — đừng commit lên GitHub.
- Dữ liệu trong `data/orders.json` là **đơn giả để demo**. Đừng thay bằng đơn khách thật:
  không tên, không số điện thoại, không địa chỉ thật vào repo. Nối hệ thống thật thì đặt
  `ORDER_PROVIDER=http` — đơn ở lại máy chủ của anh, repo chỉ gọi API.
- Ai có `app_secret` + `refresh_token` là gửi được tin nhắn dưới danh nghĩa OA của anh.
- Nếu lỡ lộ: vào developers.zalo.me tạo lại secret key, rồi chạy lại `npm run token`.
