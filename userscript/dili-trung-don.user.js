// ==UserScript==
// @name         DiLi - Bắt SĐT nhóm "Xử lý trùng đơn" (Messenger → Bot)
// @namespace    dili-supplement
// @version      1.0
// @description  Theo dõi khung chat "Xử lý trùng đơn DiLi Supplement" trên Facebook/Messenger, bắt số điện thoại mới và gửi tới bot Telegram qua cổng HTTP nội bộ. Có nút bật/tắt.
// @match        https://www.facebook.com/*
// @match        https://www.messenger.com/*
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-idle
// ==/UserScript==

(function () {
  "use strict";

  // ================== CẤU HÌNH ==================
  const INTAKE_URL = "http://127.0.0.1:8787/intake";
  const INTAKE_SECRET = "doi-mat-khau-nay-ngay"; // PHẢI GIỐNG HỆT INTAKE_SECRET trong file .env của bot
  const CHAT_TITLE_KEYWORD = "Xử lý trùng đơn";   // chỉ hoạt động khi tiêu đề trang/chat chứa chuỗi này
  const SCAN_INTERVAL_MS = 3000;                  // quét lại mỗi 3 giây
  const MAX_REMEMBERED = 500;                     // nhớ tối đa N số đã gửi (chống gửi lặp)

  // ================== TIỆN ÍCH SĐT (giống bot Python) ==================
  const PHONE_RE = /(?<!\d)(?:\+?84|0)(?:[\s.\-]?\d){9}(?![\s.\-]?\d)/g;
  const VALID_FIRST = new Set(["3", "5", "7", "8", "9"]);

  function normalize(raw) {
    let d = (raw || "").replace(/\D/g, "");
    if (d.startsWith("84")) d = d.slice(2);
    if (d.startsWith("0")) d = d.slice(1);
    if (d.length !== 9 || !VALID_FIRST.has(d[0])) return null;
    return d;
  }

  function extractPhones(text) {
    const out = [];
    for (const m of (text || "").matchAll(PHONE_RE)) {
      const k = normalize(m[0]);
      if (k && !out.includes(k)) out.push(k);
    }
    return out;
  }

  // ================== BỘ NHỚ SỐ ĐÃ GỬI ==================
  let sent = GM_getValue("dili_sent_phones", []);
  function remember(key) {
    sent.push(key);
    if (sent.length > MAX_REMEMBERED) sent = sent.slice(-MAX_REMEMBERED);
    GM_setValue("dili_sent_phones", sent);
  }

  // ================== NÚT BẬT/TẮT ==================
  let enabled = GM_getValue("dili_enabled", true);
  const btn = document.createElement("button");
  Object.assign(btn.style, {
    position: "fixed", bottom: "16px", right: "16px", zIndex: 999999,
    padding: "8px 14px", borderRadius: "20px", border: "none",
    fontSize: "13px", fontWeight: "bold", cursor: "pointer",
    boxShadow: "0 2px 8px rgba(0,0,0,.3)",
  });
  function renderBtn() {
    btn.textContent = enabled ? "🟢 DiLi: ĐANG BẮT SỐ" : "🔴 DiLi: TẠM DỪNG";
    btn.style.background = enabled ? "#d1f7d6" : "#f7d1d1";
  }
  btn.addEventListener("click", () => {
    enabled = !enabled;
    GM_setValue("dili_enabled", enabled);
    renderBtn();
  });
  renderBtn();
  document.body.appendChild(btn);

  // ================== GỬI SỐ SANG BOT ==================
  function sendToBot(key) {
    GM_xmlhttpRequest({
      method: "POST",
      url: INTAKE_URL,
      headers: {
        "Content-Type": "application/json",
        "X-Intake-Secret": INTAKE_SECRET,
      },
      data: JSON.stringify({ phone: "0" + key }),
      onload: (res) => {
        if (res.status === 200) {
          console.log("[DiLi] Đã gửi số 0" + key + " sang bot");
        } else {
          console.warn("[DiLi] Bot trả lỗi", res.status, res.responseText);
        }
      },
      onerror: () => console.warn("[DiLi] Không kết nối được bot (bot đã chạy chưa?)"),
    });
  }

  // ================== QUÉT KHUNG CHAT ==================
  function inTargetChat() {
    // Tiêu đề tab trình duyệt của Messenger/Facebook chứa tên đoạn chat đang mở
    return (document.title || "").includes(CHAT_TITLE_KEYWORD);
  }

  function scan() {
    if (!enabled || !inTargetChat()) return;
    // Lấy toàn bộ chữ trong vùng hội thoại đang hiển thị
    const main = document.querySelector('[role="main"]') || document.body;
    const phones = extractPhones(main.innerText || "");
    for (const key of phones) {
      if (sent.includes(key)) continue;
      remember(key);
      sendToBot(key);
    }
  }

  setInterval(scan, SCAN_INTERVAL_MS);
  console.log("[DiLi] Userscript bắt SĐT đã nạp. Trạng thái:", enabled ? "BẬT" : "TẮT");
})();
