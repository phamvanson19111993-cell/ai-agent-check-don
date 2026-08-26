/**
 * NHẬN ĐƠN TỪ sonsongkhoe.com GHI VÀO GOOGLE SHEET "Lady Page"
 *
 * Bản này viết khớp với trang đang chạy: trang gửi đơn dạng JSON, gồm các mục
 * ten, sdt, dia_chi, so_tien, so_hop, soluong, tinhtrang, tuKiem, thoi_gian, nguon.
 *
 * Script dò cột theo TÊN ở hàng 1, không theo thứ tự — anh kéo cột đi đâu cũng chạy đúng.
 *   Cột anh đã đặt : Tên Khách | Số điện thoại | Địa chỉ | Số Tiền | Số Hộp
 *   Script tự thêm : Thời gian | Gói đã chọn | Tình trạng | Kết quả kiểm tra | Nguồn | Trạng thái
 *
 * ── CÁCH LẮP, làm một lần, khoảng 10 phút ────────────────────────────────
 *  1. Mở Google Sheet "Lady Page"
 *  2. Menu  Tiện ích mở rộng  >  Apps Script
 *  3. Xoá sạch chữ có sẵn, dán toàn bộ file này vào, bấm lưu
 *  4. Muốn nhận email báo mỗi khi có đơn thì điền email vào EMAIL_BAO bên dưới
 *  5. Bấm  Triển khai  >  Tuỳ chọn triển khai mới  >  chọn loại "Ứng dụng web"
 *        Thực thi với tư cách : Tôi
 *        Ai có quyền truy cập : Bất kỳ ai      ← KHÔNG phải "Bất kỳ ai có Tài khoản Google"
 *  6. Bấm Triển khai, cấp quyền (Nâng cao > Đi tới ... > Cho phép)
 *  7. Copy đường link kết thúc bằng /exec
 *  8. Mở index.html, tìm dòng   var NOI_NHAN_DON = "";   dán link vào giữa hai dấu nháy
 *
 * Sau này sửa mã thì phải  Triển khai > Quản lý triển khai > sửa > Phiên bản mới,
 * nếu không link cũ vẫn chạy bản cũ.
 */

var EMAIL_BAO = '';   // ví dụ 'phamvanson19111993@gmail.com'. Để trống là tắt.

/* ── ĐẨY ĐƠN SANG PANCAKE POS ────────────────────────────────────────────
   Lấy trong Pancake: Cài đặt > API. Điền vào đây, KHÔNG điền vào trang web —
   trang web ai cũng xem được mã nguồn, để khoá ở đó là người lạ tạo đơn giả
   và đọc hết đơn thật của anh. Trong file này thì khách không nhìn thấy.
   Để trống cả hai là tắt, mọi thứ khác vẫn chạy bình thường.            */
var PANCAKE = {
  shop_id : '',      // mã shop, chỉ gồm số
  api_key : '',      // khoá API
  ma_hang : ''       // mã sản phẩm trong Pancake (variation id). Chưa có cũng
                     // được — đơn vẫn tạo, số hộp ghi trong phần ghi chú.
};

// Trái: tên cột trong Sheet. Phải: tên mục dữ liệu trang gửi lên.
var ANH_XA_COT = {
  'Tên Khách'         : 'ten',
  'Họ và tên'         : 'ten',
  'Số điện thoại'     : 'sdt',
  'Địa chỉ'           : 'dia_chi',
  'Số Tiền'           : 'so_tien',
  'Số Hộp'            : 'so_hop',
  'Thời gian'         : 'thoi_gian',
  'Gói đã chọn'       : 'soluong',
  'Tình trạng'        : 'tinhtrang',
  'Kết quả kiểm tra'  : 'tuKiem',
  'Nguồn'             : 'nguon',
  'Trạng thái'        : 'trang_thai'
};

// Những cột này script tự thêm vào bên phải nếu Sheet chưa có.
var COT_THEM = ['Thời gian', 'Gói đã chọn', 'Tình trạng', 'Kết quả kiểm tra', 'Nguồn', 'Trạng thái'];

function doPost(e) {
  var khoa = LockService.getScriptLock();
  try {
    khoa.waitLock(20000);          // hai khách bấm cùng lúc thì không đè lên nhau

    var d = docDuLieu(e);
    if (!d) return traLoi({ ok: false, error: 'khong doc duoc du lieu' });

    var ten = chuoi(d.ten);
    var sdt = chuoi(d.sdt).replace(/[^0-9+]/g, '');
    if (!ten && !sdt) return traLoi({ ok: false, error: 'thieu ten va so dien thoai' });

    var sheet  = laySheet();
    var tieuDe = layTieuDe(sheet);

    var giaTri = {
      ten       : ten,
      sdt       : "'" + sdt,                       // dấu ' giữ số 0 đứng đầu, không hiện ra
      dia_chi   : chuoi(d.dia_chi) || ghepDiaChi(d),
      so_tien   : Number(d.so_tien) || '',
      so_hop    : Number(d.so_hop) || '',
      soluong   : chuoi(d.soluong),
      tinhtrang : chuoi(d.tinhtrang),
      tuKiem    : chuoi(d.tuKiem),
      nguon     : chuoi(d.nguon),
      thoi_gian : new Date(),
      trang_thai: 'Chưa gọi'
    };

    var hang = tieuDe.map(function (tenCot) {
      var khoaDuLieu = ANH_XA_COT[tenCot];
      return (khoaDuLieu && giaTri[khoaDuLieu] !== undefined) ? giaTri[khoaDuLieu] : '';
    });

    sheet.appendRow(hang);
    dinhDangHangMoi(sheet, tieuDe);
    daySangPancake(giaTri, d);
    baoEmail(giaTri, d);

    return traLoi({ ok: true });

  } catch (err) {
    return traLoi({ ok: false, error: String(err) });
  } finally {
    try { khoa.releaseLock(); } catch (boQua) {}
  }
}

// Mở link /exec bằng trình duyệt sẽ thấy dòng này — dùng để kiểm tra đã triển khai đúng chưa.
function doGet() {
  return traLoi({ ok: true, message: 'Endpoint dang chay. Trang gui don bang POST.' });
}

/** Trang gửi JSON trong thân yêu cầu. Vẫn đọc được cả kiểu form thường cho chắc. */
function docDuLieu(e) {
  if (!e) return null;
  if (e.postData && e.postData.contents) {
    try { return JSON.parse(e.postData.contents); } catch (boQua) {}
  }
  if (e.parameter && (e.parameter.ten || e.parameter.sdt)) return e.parameter;
  return null;
}

function ghepDiaChi(d) {
  var phan = [d.sonha, d.thon, d.xa, d.huyen, d.tinh]
               .map(chuoi)
               .filter(function (x) { return x; });
  var s = phan.join(', ');
  if (chuoi(d.moc)) s += ' (' + chuoi(d.moc) + ')';
  return s;
}

function laySheet() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
}

/** Đọc hàng tiêu đề, bổ sung cột còn thiếu vào bên phải, trả về danh sách tên cột. */
function layTieuDe(sheet) {
  var soCot  = Math.max(sheet.getLastColumn(), 1);
  var tieuDe = sheet.getRange(1, 1, 1, soCot).getValues()[0]
                    .map(function (v) { return String(v).trim(); });

  while (tieuDe.length && !tieuDe[tieuDe.length - 1]) tieuDe.pop();

  if (!tieuDe.length) {
    tieuDe = ['Tên Khách', 'Số điện thoại', 'Địa chỉ', 'Số Tiền', 'Số Hộp'];
    sheet.getRange(1, 1, 1, tieuDe.length).setValues([tieuDe]);
  }

  var thieu = COT_THEM.filter(function (t) { return tieuDe.indexOf(t) === -1; });
  if (thieu.length) {
    sheet.getRange(1, tieuDe.length + 1, 1, thieu.length).setValues([thieu]);
    tieuDe = tieuDe.concat(thieu);
    sheet.getRange(1, 1, 1, tieuDe.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return tieuDe;
}

function dinhDangHangMoi(sheet, tieuDe) {
  var hang = sheet.getLastRow();
  var cot  = function (t) { return tieuDe.indexOf(t) + 1; };

  if (cot('Thời gian')     > 0) sheet.getRange(hang, cot('Thời gian')).setNumberFormat('dd/MM/yyyy HH:mm:ss');
  if (cot('Số Tiền')       > 0) sheet.getRange(hang, cot('Số Tiền')).setNumberFormat('#,##0"đ"');
  if (cot('Số điện thoại') > 0) sheet.getRange(hang, cot('Số điện thoại')).setNumberFormat('@');
}

function baoEmail(g, d) {
  if (!EMAIL_BAO) return;
  try {
    var sdt = String(g.sdt).replace("'", '');
    MailApp.sendEmail({
      to: EMAIL_BAO,
      subject: 'Đơn mới: ' + (g.ten || '(không tên)') + ' — ' + sdt,
      body: [
        'Họ và tên     : ' + g.ten,
        'Số điện thoại : ' + sdt,
        'Địa chỉ       : ' + g.dia_chi,
        'Gói đã chọn   : ' + (g.soluong || 'chưa chọn'),
        'Số hộp        : ' + (g.so_hop  || '—'),
        'Số tiền       : ' + (g.so_tien ? Number(g.so_tien).toLocaleString('vi-VN') + 'đ' : '—'),
        'Tình trạng    : ' + g.tinhtrang,
        'Bài kiểm tra  : ' + g.tuKiem,
        'Cách trả       : ' + chuoi(d['cach-tra']),
        'Nguồn         : ' + g.nguon,
        '',
        'Gọi lại trong 15 phút đầu là lúc khách còn đang mở trang.'
      ].join('\n')
    });
  } catch (err) {
    // Hết hạn mức gửi mail thì bỏ qua — dòng dữ liệu đã ghi vào Sheet rồi, không được để mất.
  }
}

/**
 * Tạo đơn bên Pancake POS. Ghi lại nguyên văn phản hồi vào trang "Nhật ký"
 * để lần chạy thử đầu tiên biết ngay đúng hay sai, sai ở chỗ nào.
 *
 * LƯU Ý THẬT: tên các trường dưới đây viết theo cách Pancake thường dùng,
 * nhưng mỗi shop cấu hình một kiểu. Chạy thử một đơn rồi mở trang Nhật ký,
 * thấy mã 200 là xong; thấy mã khác thì gửi nguyên dòng đó cho Claude sửa lại.
 */
function daySangPancake(g, d) {
  if (!PANCAKE.shop_id || !PANCAKE.api_key) return;

  var sdt = String(g.sdt).replace("'", '');
  var ghiChu = [
    'Đơn từ sonsongkhoe.com',
    g.soluong   ? 'Gói: '          + g.soluong   : '',
    g.tinhtrang ? 'Tình trạng: '   + g.tinhtrang : '',
    g.tuKiem    ? 'Bài kiểm tra: ' + g.tuKiem    : ''
  ].filter(function (x) { return x; }).join(' | ');

  var don = {
    bill_full_name    : g.ten,
    bill_phone_number : sdt,
    shipping_address  : { full_address: g.dia_chi },
    note              : ghiChu,
    status            : 0                     // 0 = đơn mới, chờ xác nhận
  };
  if (PANCAKE.ma_hang) {
    don.items = [{ variation_id: PANCAKE.ma_hang, quantity: Number(g.so_hop) || 1 }];
  }

  var url = 'https://pos.pages.fm/api/v1/shops/' + PANCAKE.shop_id +
            '/orders?api_key=' + encodeURIComponent(PANCAKE.api_key);
  try {
    var res = UrlFetchApp.fetch(url, {
      method            : 'post',
      contentType       : 'application/json',
      payload           : JSON.stringify(don),
      muteHttpExceptions: true
    });
    ghiNhatKy('Pancake', res.getResponseCode(), res.getContentText());
  } catch (err) {
    ghiNhatKy('Pancake', 'lỗi', String(err));
  }
}

/** Ghi một dòng vào trang "Nhật ký". Không có trang đó thì tự tạo. */
function ghiNhatKy(dau, ma, noiDung) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var nk = ss.getSheetByName('Nhật ký');
    if (!nk) {
      nk = ss.insertSheet('Nhật ký');
      nk.getRange(1, 1, 1, 4)
        .setValues([['Thời gian', 'Nơi', 'Mã trả về', 'Nội dung']])
        .setFontWeight('bold');
      nk.setFrozenRows(1);
    }
    nk.appendRow([new Date(), dau, ma, String(noiDung).slice(0, 4000)]);
  } catch (boQua) {}
}

function chuoi(v) {
  return (v === undefined || v === null) ? '' : String(v).trim();
}

function traLoi(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
