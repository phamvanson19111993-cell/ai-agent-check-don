# ai-agent-check-don — Agent Zalo tra cứu đơn hàng

Bot Zalo Official Account (OA) trả lời khách hỏi tình trạng đơn hàng. Khách nhắn mã đơn
hoặc số điện thoại, Claude đọc ý định, gọi công cụ tra cứu và trả lời bằng tiếng Việt.

```
Khách ── Zalo OA ──► POST /webhook ──► kiểm tra chữ ký ──► Agent (Claude + công cụ)
                                                              │
                                                              ├─ lookup_order
                                                              ├─ find_orders_by_phone   ──► nguồn đơn (mock JSON | API của bạn)
                                                              └─ escalate_to_human
                                                              │
                          Zalo Send API ◄── câu trả lời tiếng Việt
```

Điểm chính:

- **Không mất tin nhắn**: webhook trả `200` ngay rồi mới xử lý; sự kiện trùng `msg_id` bị chặn.
- **Không im lặng khi Claude lỗi**: rơi xuống chế độ regex (`FallbackOrderAgent`) vẫn tra được đơn.
- **Không bịa dữ liệu**: model chỉ được nói những gì công cụ trả về; tra không ra thì báo không ra.
- **Chạy được ngay không cần API key**: mặc định dùng dữ liệu mẫu trong `data/orders.json`.

## Chạy thử trong 1 phút

```bash
npm install
npm run chat                 # chat với agent ngay trên terminal, không cần Zalo
```

Thử: `cho hỏi đơn DH123456`, `sđt của mình là 0901234567`, `mình muốn hủy đơn`.

Chưa có `ANTHROPIC_API_KEY` thì CLI chạy chế độ regex. Có key thì Claude vào cuộc:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
npm run chat
```

## Kết nối Zalo OA

Hướng dẫn đầy đủ từng bước (kèm bảng lỗi thường gặp): **[docs/SETUP-ZALO.md](docs/SETUP-ZALO.md)**.

Tóm tắt:

```bash
cp .env.example .env      # điền ZALO_APP_ID + ZALO_APP_SECRET
npm run token             # mở link Zalo hiện ra, bấm Cho phép → nhận ZALO_REFRESH_TOKEN
npm start                 # rồi trỏ Webhook URL của OA về https://<domain>/webhook
```

`npm run token` chạy luồng OAuth v4 + PKCE của Zalo (`oa/permission` → `oa/access_token`),
tự mở server nhận callback ở `http://localhost:3000/oauth/callback` và lưu token vào
`data/zalo-token.json`. Callback về máy chủ khác thì dùng
`npm run token -- --url-only` rồi `npm run token -- --code=<code>`.

Test cục bộ thì mở tunnel (`ngrok http 3000`) rồi dán URL https vào phần Webhook của OA.

> Zalo ký webhook bằng header `X-ZEvent-Signature` = `mac=sha256(app_id + raw_body + timestamp + OA_secret_key)`.
> App tự kiểm tra chữ ký này. Chỉ đặt `ZALO_VERIFY_SIGNATURE=false` khi test cục bộ bằng curl.

## Biến môi trường

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `ZALO_APP_ID` | – | App ID trên developers.zalo.me (bắt buộc) |
| `ZALO_APP_SECRET` | – | Secret key của app, dùng cho header `secret_key` khi refresh token (bắt buộc) |
| `ZALO_OA_SECRET_KEY` | `ZALO_APP_SECRET` | Khóa ký webhook, nếu OA dùng khóa riêng |
| `ZALO_REFRESH_TOKEN` | – | Refresh token khởi tạo, lấy bằng `npm run token` (bắt buộc) |
| `ZALO_REDIRECT_URI` | `http://localhost:3000/oauth/callback` | Callback OAuth, phải trùng khai báo trong app Zalo |
| `ZALO_TOKEN_FILE` | `./data/zalo-token.json` | Nơi lưu access/refresh token mới |
| `ZALO_VERIFY_SIGNATURE` | `true` | Bật/tắt kiểm tra chữ ký webhook |
| `ANTHROPIC_API_KEY` | – | Không có thì bot chạy chế độ regex |
| `CLAUDE_MODEL` | `claude-opus-5` | Model dùng cho agent |
| `CLAUDE_EFFORT` | `low` | `low`…`max`. Chat CSKH ưu tiên `low` cho nhanh; nâng lên nếu cần suy luận sâu |
| `CLAUDE_MAX_TOOL_TURNS` | `6` | Số vòng gọi công cụ tối đa mỗi tin nhắn |
| `ORDER_PROVIDER` | `mock` | `mock` (file JSON) hoặc `http` (API của bạn) |
| `ORDER_MOCK_FILE` | `./data/orders.json` | Dữ liệu đơn mẫu |
| `ORDER_API_BASE_URL` / `ORDER_API_KEY` | – | Dùng khi `ORDER_PROVIDER=http` |
| `SESSION_MAX_TURNS` / `SESSION_TTL_MS` | `12` / `1800000` | Độ dài và thời gian sống của ngữ cảnh hội thoại |
| `PORT` / `LOG_LEVEL` | `3000` / `info` | – |

## Nối vào hệ thống đơn hàng thật

Đặt `ORDER_PROVIDER=http` và `ORDER_API_BASE_URL`. Mặc định adapter gọi:

- `GET {base}/orders/{code}` → trả về một đơn (404 = không tìm thấy)
- `GET {base}/orders?phone={phone}` → trả về danh sách đơn

API của bạn có đường dẫn khác thì chỉ cần sửa hai hàm trong `src/orders/httpProvider.js`.
Trường dữ liệu được chuẩn hóa trong `src/orders/normalize.js` — nhận cả `snake_case` lẫn
`camelCase`, và map trạng thái (`dang_giao`, `in_transit`, `shipped`… → `shipping`).
Provider chỉ cần hai method:

```js
{ getOrder(code) -> order|null, findOrdersByPhone(phone) -> order[] }
```

## Agent hoạt động thế nào

`src/agent/agent.js` chạy vòng lặp tool use: gửi tin khách + lịch sử cho Claude, model
quyết định gọi công cụ nào, code chạy công cụ rồi trả **tất cả** `tool_result` trong một
tin nhắn, lặp đến khi model trả lời bằng văn bản.

- Công cụ và system prompt: `src/agent/prompt.js`. Sửa giọng văn, chính sách trả lời ở đây.
- `escalate_to_human` gọi callback `onEscalate` trong `src/index.js` — nối vào ticket/nhóm
  CSKH của bạn tại đó.
- Bật `thinking: adaptive` và `fallbacks: "default"` (bộ phân loại an toàn từ chối thì
  request được định tuyến sang model khác thay vì trả tin rỗng cho khách).
- Nếu Claude lỗi/hết hạn mức, `src/zalo/webhook.js` tự chuyển sang `FallbackOrderAgent`.

## Kiểm thử

```bash
npm test
```

53 test chạy bằng `node --test`, không cần mạng: chữ ký webhook, refresh + retry token Zalo,
vòng lặp công cụ của agent, chế độ fallback, cắt lịch sử hội thoại, và tầng HTTP.

## Triển khai

- Chạy **một instance** là an toàn nhất: refresh token Zalo dùng một lần và lịch sử hội thoại
  đang giữ trong RAM. Muốn scale nhiều instance thì thay `FileTokenStore` (`src/zalo/tokenStore.js`)
  và `SessionStore` (`src/store/sessions.js`) bằng Redis — giữ nguyên các method hiện có.
- Mount `data/` như volume để không mất `zalo-token.json` khi restart container.
- Có sẵn `GET /health` cho load balancer.

## Cần biết trước khi lên production

- Endpoint và tham số Zalo trong `src/zalo/client.js` theo OA API v3.0 và OAuth v4; Zalo có
  đổi API theo thời gian, nên đối chiếu lại với tài liệu chính thức khi triển khai.
- Bot chỉ trả lời tin **text**. Ảnh/file/sticker được trả lời hướng dẫn gõ mã đơn.
- Cửa sổ nhắn tin của Zalo OA có giới hạn (tin tư vấn chỉ gửi được trong khoảng thời gian
  sau khi khách nhắn); bot chỉ trả lời khi khách chủ động nhắn nên phù hợp với giới hạn này.
- Chưa có chống spam theo user. Nếu OA đông khách, thêm rate limit trước khi gọi Claude.
