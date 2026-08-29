// ═══════════════════════════════════════════════════════════════
//  CHUÔNG BÁO ĐƠN — kêu ngay khi khách bấm gửi
//  Phòng 7 · 29/08/2026
//
//  Khách bấm gửi trên sonsongkhoe.com  →  đơn vào Biểu mẫu
//  →  script này chạy  →  anh Sơn nhận thư (và tin Telegram nếu bật)
//
//  DÁN VÀO ĐÂU
//  Mở BẢNG TRẢ LỜI của Biểu mẫu (không phải bảng "Lady Page")
//  → Tiện ích mở rộng → Apps Script → dán toàn bộ file này
//  → Lưu → chạy hàm  catChuong  MỘT LẦN → cho phép quyền
//
//  Chạy catChuong xong là xong. Từ đó mỗi đơn mới là chuông kêu.
//  Muốn thử ngay thì chạy hàm  chayThu.
// ═══════════════════════════════════════════════════════════════

// ─── CẦN ĐIỀN ──────────────────────────────────────────────────
var THU = 'phamvanson19111993@gmail.com';   // nhận thư báo đơn

// Telegram — để trống thì bỏ qua, chỉ gửi thư.
// LƯU Ý: mã bot cũ đã lộ trên mạng, PHẢI thu hồi rồi lấy mã mới:
// BotFather → /mybots → chọn bot → API Token → Revoke current token
var TG_TOKEN = '';   // dán mã bot MỚI vào đây
var TG_CHAT  = '';   // số chat của anh, hỏi @userinfobot

// ═══════════════════════════════════════════════════════════════

function catChuong() {
  var bang = SpreadsheetApp.getActiveSpreadsheet();
  var da = ScriptApp.getProjectTriggers();
  for (var i = 0; i < da.length; i++) {
    if (da[i].getHandlerFunction() === 'khiCoDon') ScriptApp.deleteTrigger(da[i]);
  }
  ScriptApp.newTrigger('khiCoDon').forSpreadsheet(bang).onFormSubmit().create();
  Logger.log('Xong. Chuông đã cắt. Từ giờ mỗi đơn mới là báo ngay.');
}


function khiCoDon(e) {
  var don = docDon(e);
  var tieu_de = '🔔 ĐƠN MỚI — Rich Coenzyme Q10';

  try {
    MailApp.sendEmail({
      to: THU,
      subject: tieu_de,
      body: don.chu,
      htmlBody: don.html
    });
  } catch (loi) {
    Logger.log('Gửi thư hỏng: ' + loi);
  }

  if (TG_TOKEN && TG_CHAT) {
    try {
      UrlFetchApp.fetch('https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage', {
        method: 'post',
        payload: { chat_id: TG_CHAT, text: tieu_de + '\n\n' + don.chu },
        muteHttpExceptions: true
      });
    } catch (loi) {
      Logger.log('Gửi Telegram hỏng: ' + loi);
    }
  }
}


// Đọc đơn ra khỏi sự kiện. Biểu mẫu hiện gộp cả đơn vào MỘT ô,
// nên cứ ghép hết mọi câu trả lời lại — không đoán tên cột.
function docDon(e) {
  var dong = [];
  if (e && e.namedValues) {
    for (var ten in e.namedValues) {
      var gt = String(e.namedValues[ten] || '').trim();
      if (gt) dong.push([ten, gt]);
    }
  } else if (e && e.values) {
    for (var i = 0; i < e.values.length; i++) {
      var v = String(e.values[i] || '').trim();
      if (v) dong.push(['Ô ' + (i + 1), v]);
    }
  }
  if (!dong.length) dong.push(['(trống)', 'Không đọc được nội dung đơn']);

  var luc = Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'HH:mm dd/MM/yyyy');
  var chu = 'Lúc ' + luc + '\n\n';
  var html = '<div style="font:15px/1.6 system-ui,sans-serif">'
           + '<p style="margin:0 0 12px;color:#666">Lúc ' + luc + '</p>';

  for (var j = 0; j < dong.length; j++) {
    chu  += dong[j][0] + ': ' + dong[j][1] + '\n';
    html += '<p style="margin:0 0 8px"><b>' + dong[j][0] + ':</b> '
          + dong[j][1].replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</p>';
  }

  chu  += '\nGọi khách xác nhận đơn rồi mới gửi hàng.';
  html += '<p style="margin:16px 0 0;padding:10px 12px;background:#FCE4EC;'
        + 'border-radius:8px"><b>Gọi khách xác nhận đơn rồi mới gửi hàng.</b></p></div>';

  return { chu: chu, html: html };
}


// Bấm chạy hàm này để thử — nó gửi một đơn giả cho anh xem chuông có kêu không.
function chayThu() {
  khiCoDon({
    namedValues: {
      'Đơn hàng': ['Họ tên: Nguyen Van Thu\nĐiện thoại: 0912345678\n'
                 + 'Địa chỉ: Số 12 Trần Hưng Đạo, Hải Hậu, Nam Định\n'
                 + 'Số lượng: 6 hộp — 17.340.000đ\nCách trả: Nhận hàng rồi trả tiền']
    }
  });
  Logger.log('Đã gửi đơn thử. Mở hộp thư xem chuông có kêu không.');
}
