// ═══════════════════════════════════════════════════════════════
//  NHẬN ĐƠN TỪ TRANG GIẢM MỠ  →  ghi thẳng vào Google Sheet
//  Phòng Lady giảm mỡ · Ellagic Acid
//
//  Bảng đã tạo sẵn trong Drive của anh Sơn, mã bảng đã điền bên dưới:
//  "Đơn Ellagic Acid — Lady giảm mỡ"
//
//  ANH SƠN CÒN PHẢI LÀM BỐN BƯỚC, khoảng 3 phút:
//   1. Mở bảng đó → Tiện ích mở rộng → Apps Script
//   2. Xoá hết code cũ → dán toàn bộ file này vào → bấm Lưu
//   3. Bấm Triển khai → Tuỳ chọn triển khai mới → chọn "Ứng dụng web"
//        Thực thi với  : Tôi
//        Ai có quyền   : Bất kỳ ai
//      → Triển khai → cho phép quyền truy cập
//   4. Copy đường dẫn kết thúc bằng /exec, gửi cho em.
//      Em dán vào biến NOI_NHAN_DON trong index.html là đơn chảy về bảng.
//
//  Muốn thử trước khi triển khai: chọn hàm thuMotDon rồi bấm Chạy.
//  Phải thấy một đơn mẫu hiện ra trong bảng.
//
//  ⚠️ ĐỪNG dùng lại mã bảng của trang Q10 — đơn sẽ chảy nhầm bảng.
// ═══════════════════════════════════════════════════════════════

var MA_BANG = '1fcUxwgmu2XGHG1QJ5fx1ZFw6X5UOFjmfVf885aJWsVE';

// Hai đơn cùng số điện thoại cách nhau dưới ngần này phút thì coi là
// trùng — thường do khách bấm Gửi hai lần, hoặc tải lại trang rồi gửi lại.
var PHUT_COI_LA_TRUNG = 30;

var TIEU_DE = ['Thời gian', 'Trạng thái', 'Họ tên', 'Số điện thoại', 'Địa chỉ',
               'Số lượng', 'Số gói', 'Giá trị đơn', 'Nhắc đặt lại',
               'Bài kiểm tra', 'Nguồn'];

// Nhân viên gõ vào cột Trạng thái. Để sẵn danh sách cho khỏi gõ sai chính tả.
var CAC_TRANG_THAI = ['Mới', 'Đã gọi', 'Chốt đơn', 'Hẹn gọi lại', 'Không nghe máy', 'Huỷ'];


function doPost(e) {
  var lock = LockService.getScriptLock();
  // Hai đơn về cùng lúc mà cùng ghi thì đè nhau. Xếp hàng chờ nhau.
  lock.waitLock(20000);
  try {
    var sheet = SpreadsheetApp.openById(MA_BANG).getSheets()[0];
    var d = JSON.parse(e.postData.contents);

    datTieuDe(sheet);

    var sdt = String(d.sdt || '').replace(/\D/g, '');
    if (laDonTrung(sheet, sdt)) {
      return ContentService.createTextOutput('trung');
    }

    sheet.appendRow([
      d.thoi_gian || new Date().toLocaleString('vi-VN'),
      'Mới',
      d.ten || '',
      "'" + (d.sdt || ''),                  // dấu ' giữ số 0 đứng đầu
      d.dia_chi || '',
      d.soluong || '',
      d.so_hop ? Number(d.so_hop) : '',
      d.so_tien ? Number(d.so_tien) : '',
      d.nhac ? 'Có' : 'Không',
      d.tuKiem || '',
      d.nguon || ''
    ]);

    var r = sheet.getLastRow();
    sheet.getRange(r, 1, 1, TIEU_DE.length)
         .setBackground(r % 2 === 0 ? '#FDF3F0' : null);
    // Đơn mới tô đậm cột Trạng thái cho dễ thấy
    sheet.getRange(r, 2).setFontWeight('bold').setFontColor('#BE1B10');
    sheet.getRange(r, 8).setNumberFormat('#,##0"đ"');

    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}


function datTieuDe(sheet) {
  sheet.getRange(1, 1, 1, TIEU_DE.length)
       .setValues([TIEU_DE])
       .setFontWeight('bold')
       .setBackground('#FDE7E2');
  sheet.setFrozenRows(1);

  // Cột Trạng thái: cho chọn thay vì gõ tay
  var quy = SpreadsheetApp.newDataValidation()
              .requireValueInList(CAC_TRANG_THAI, true)
              .setAllowInvalid(true)
              .build();
  sheet.getRange(2, 2, Math.max(sheet.getMaxRows() - 1, 1), 1).setDataValidation(quy);
}


function laDonTrung(sheet, sdt) {
  if (!sdt) return false;
  var n = sheet.getLastRow();
  if (n < 2) return false;

  // Chỉ dò 40 đơn gần nhất — đủ xa để bắt trùng, đủ gần để chạy nhanh
  var dau = Math.max(2, n - 39);
  var o = sheet.getRange(dau, 1, n - dau + 1, 4).getValues();
  var gioi_han = Date.now() - PHUT_COI_LA_TRUNG * 60 * 1000;

  for (var i = o.length - 1; i >= 0; i--) {
    var cu = String(o[i][3] || '').replace(/\D/g, '');
    if (cu !== sdt) continue;
    var luc = docGio(o[i][0]);
    if (luc === null || luc >= gioi_han) return true;
  }
  return false;
}


// Trang gửi thời gian dạng chữ theo giờ Việt Nam, ví dụ "17:08:55 28/8/2026".
// Đọc không ra thì trả về null và coi như đơn trùng, cho chắc.
function docGio(x) {
  if (x instanceof Date) return x.getTime();
  var m = String(x).match(/(\d{1,2}):(\d{2}):(\d{2})\s+(\d{1,2})\/(\d{1,2})\/(\d{4})/);
  if (!m) return null;
  return new Date(+m[6], +m[5] - 1, +m[4], +m[1], +m[2], +m[3]).getTime();
}


// Chạy hàm này một lần để thử. Phải thấy một đơn mẫu hiện ra trong bảng,
// và chạy lần hai phải báo "trung" chứ không ghi thêm dòng nữa.
function thuMotDon() {
  var mau = {
    ten: 'Nguyễn Thị Thử',
    sdt: '0900000000',
    dia_chi: 'Xóm 1, xã Thử Nghiệm, Hải Hậu, Nam Định',
    soluong: '1 gói — 675.000đ',
    so_hop: '1',
    so_tien: '675000',
    nhac: 'Có',
    tuKiem: 'Bài tự kiểm: 8/12 điểm',
    thoi_gian: new Date().toLocaleString('vi-VN'),
    nguon: 'chạy thử từ Apps Script'
  };
  var kq = doPost({ postData: { contents: JSON.stringify(mau) } });
  Logger.log('lần 1: ' + kq.getContent());
  Logger.log('lần 2: ' + doPost({ postData: { contents: JSON.stringify(mau) } }).getContent());
}
