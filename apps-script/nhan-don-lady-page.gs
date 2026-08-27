// ═══════════════════════════════════════════════════════════════
//  NHẬN ĐƠN TỪ sonsongkhoe.com  →  ghi vào bảng "Lady Page"
//  Bản cập nhật 28/08/2026 — Phòng 7
//
//  KHÁC BẢN CŨ Ở ĐÂU:
//  Bản cũ ghi cột "Tình trạng sức khoẻ". Ô đó đã bị gỡ khỏi trang
//  ngày 27/08 nên cột đó nay luôn trống.
//  Bản này thay bằng cột "CÁCH TRẢ" — đặt cọc 200.000đ hay chuyển
//  khoản đủ. Đây chính là con số anh Sơn cần trong báo cáo.
//
//  CÁCH DÙNG: mở bảng "Lady Page" → Tiện ích mở rộng → Apps Script
//  → xoá hết code cũ → dán toàn bộ file này vào.
// ═══════════════════════════════════════════════════════════════

var MA_BANG = '1OrfVCvhvUV0T0PqaSdK5u0_rEG_5U2G_KY913tDNNWs';

var TIEU_DE = ['Tên Khách', 'Số điện thoại', 'Địa chỉ', 'Số Tiền', 'Số Hộp',
               'Thời gian', 'Cách trả', 'Tiền cọc', 'Bài kiểm tra', 'Nguồn'];

function doPost(e) {
  var sheet = SpreadsheetApp.openById(MA_BANG).getSheets()[0];
  var d = JSON.parse(e.postData.contents);

  // Luôn đặt lại hàng tiêu đề cho khớp bản mới
  sheet.getRange(1, 1, 1, TIEU_DE.length).setValues([TIEU_DE]).setFontWeight('bold');

  var traDu   = (d.cach_tra === 'du');
  var soTien  = d.so_tien ? Number(d.so_tien) : '';
  var tienCoc = traDu ? soTien : 200000;

  sheet.appendRow([
    d.ten     || '',
    "'" + (d.sdt || ''),        // dấu ' giữ số 0 đứng đầu
    d.dia_chi || '',
    soTien,
    d.so_hop  ? Number(d.so_hop) : '',
    d.thoi_gian || '',
    traDu ? 'Chuyển khoản đủ' : 'Đặt cọc 200.000đ',
    tienCoc,
    d.tuKiem  || '',
    d.nguon   || ''
  ]);

  var r = sheet.getLastRow();
  sheet.getRange(r, 1, 1, TIEU_DE.length).setBackground(r % 2 === 0 ? '#FDF0F5' : null);

  return ContentService.createTextOutput('ok');
}

// Chạy hàm này một lần để thử. Phải thấy 2 dòng test hiện ra trong bảng.
function chayThu() {
  doPost({ postData: { contents: JSON.stringify({
    ten: 'Nguyen Van Test', sdt: '0912345678',
    dia_chi: 'So 12 Tran Hung Dao, Huyen Hai Hau, Nam Dinh',
    so_tien: '17340000', so_hop: '6', cach_tra: 'coc',
    thoi_gian: new Date().toLocaleString('vi-VN'),
    tuKiem: 'Bai tu kiem: 9/12 diem', nguon: 'chay thu'
  })}});

  doPost({ postData: { contents: JSON.stringify({
    ten: 'Tran Thi Test', sdt: '0987654321',
    dia_chi: 'So 5 Ngo 12, Huyen Nam Sach, Hai Duong',
    so_tien: '5780000', so_hop: '2', cach_tra: 'du',
    thoi_gian: new Date().toLocaleString('vi-VN'),
    tuKiem: '', nguon: 'chay thu'
  })}});
}
