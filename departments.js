// 8 phòng của DILIM AI Command Center — bản gốc: prompts/dilim-tong-chi-huy.md
// owns   : dữ liệu phòng này là NGUỒN CHÍNH THỨC (source of truth)
// rule   : ràng buộc riêng, tuyệt đối không được vi phạm
// feeds  : agent trong sổ 11 phòng (agents.js) đang bơm dữ liệu cho phòng này
//          mảng rỗng = CHƯA CÓ AGENT PHỤ TRÁCH → dữ liệu phòng này phải hỏi anh
window.DEPARTMENTS = [
  {
    icon: '🗄️', name: 'Data Center',
    role: 'Nơi ưu tiên lấy dữ liệu thực tế',
    owns: ['Doanh số cá nhân', 'Doanh số F1', 'Doanh số F2', 'Doanh số toàn hệ thống', 'Khách hàng', 'Đơn hàng', 'Đại lý', 'Sale', 'Chi phí', 'Doanh thu', 'Lợi nhuận', 'Dữ liệu quảng cáo', 'KPI', 'Dữ liệu lịch sử'],
    feeds: ['📊 Fanpage Pancake', '📞 SĐT chưa chốt Pancake', '🔁 Check trùng đơn']
  },
  {
    icon: '📜', name: 'Chính sách & Hoa hồng',
    role: 'Chính sách, cấp bậc, điều kiện hoa hồng, ngày hiệu lực',
    owns: ['Chính sách công ty', 'Chính sách hoa hồng', 'Điều kiện nhận hoa hồng', 'Điều kiện doanh số cá nhân', 'Điều kiện F1/F2', 'Hoa hồng lãnh đạo', 'Cấp bậc', 'Điều kiện duy trì cấp bậc', 'Ngày hiệu lực', 'Phiên bản chính sách cũ/mới'],
    rule: 'Không tự tạo điều kiện nếu tài liệu không quy định',
    feeds: []
  },
  {
    icon: '📞', name: 'Sale',
    role: 'Lead, tỷ lệ chốt, hiệu quả từng sale',
    owns: ['Lead', 'Khách hàng', 'Sale phụ trách', 'Doanh số từng sale', 'Tỷ lệ chốt', 'Giá trị đơn trung bình (AOV)', 'Tình trạng khách', 'Lịch follow-up', 'Kịch bản sale', 'Lý do khách chưa mua', 'Hiệu quả từng sale'],
    feeds: ['✍️ Kịch bản sale', '📞 SĐT chưa chốt Pancake', '💬 Agen Zalo']
  },
  {
    icon: '📣', name: 'Marketing & Ads',
    role: 'Meta Ads, content, chỉ số chuyển đổi, ROAS',
    owns: ['Meta Ads', 'Campaign', 'Ad Set', 'Ads', 'Content', 'Creative', 'CPM', 'CTR', 'CPC', 'CPL', 'Chi phí data', 'Số lead', 'Tỷ lệ chuyển đổi', 'Doanh thu từ Ads', 'ROAS', 'Hiệu quả từng nội dung'],
    feeds: ['🩺 Video content sức khỏe', '👩 Lady Page', '🎬 Edivideo']
  },
  {
    icon: '🌐', name: 'Đại lý & Hệ thống',
    role: 'F1, F2, tuyến dưới, tăng trưởng hệ thống',
    owns: ['F1', 'F2', 'Tuyến dưới', 'Doanh số từng đại lý', 'Tổng doanh số hệ thống', 'Đại lý hoạt động / không hoạt động', 'Tuyển mới', 'Điều kiện nhận hoa hồng', 'Tăng trưởng hệ thống'],
    feeds: []
  },
  {
    icon: '🎧', name: 'CSKH',
    role: 'Khách đã mua, chăm sóc, tái mua, khiếu nại',
    owns: ['Khách đã mua', 'Sản phẩm khách đang dùng', 'Ngày bắt đầu', 'Lịch chăm sóc', 'Phản hồi', 'Tái mua', 'Khiếu nại', 'Khách tiềm năng mua thêm'],
    rule: 'Không chẩn đoán y khoa, không biến thông tin chưa xác nhận thành sự thật',
    feeds: ['🎧 CSKH', '💬 Agen Zalo']
  },
  {
    icon: '💰', name: 'Tài chính',
    role: 'Doanh thu, chi phí, dòng tiền, lợi nhuận',
    owns: ['Doanh thu', 'Giá vốn', 'Chi phí Ads', 'Chi phí sale', 'Hoa hồng', 'Chi phí vận hành', 'Công nợ', 'Dòng tiền', 'Lợi nhuận gộp', 'Lợi nhuận ròng'],
    feeds: []
  },
  {
    icon: '🔍', name: 'AI Kiểm toán',
    role: 'Phòng kiểm tra độc lập — chốt chặn trước khi kết luận',
    owns: ['Kiểm tra dữ liệu', 'Kiểm tra phép tính', 'Kiểm tra nguồn', 'Kiểm tra ngày hiệu lực', 'Phát hiện dữ liệu trùng', 'Phát hiện dữ liệu cũ', 'Phát hiện mâu thuẫn giữa các phòng', 'Phân biệt dữ liệu thật với giả định', 'Phát hiện AI suy diễn'],
    rule: 'Có quyền yêu cầu tính toán lại trước khi Tổng Chỉ Huy kết luận',
    feeds: ['🔁 Check trùng đơn']
  }
];

// 8 bước xử lý mọi câu hỏi
window.STEPS = [
  { n: 1, name: 'Hiểu yêu cầu',        note: 'Anh thực sự muốn biết điều gì' },
  { n: 2, name: 'Xác định phòng',      note: 'Không gọi tất cả các phòng nếu không cần' },
  { n: 3, name: 'Thu thập dữ liệu',    note: 'Lấy từ nguồn chính thức của phòng' },
  { n: 4, name: 'Kiểm tra nguồn',      note: 'Từ đâu · kỳ nào · cập nhật khi nào · xác minh chưa' },
  { n: 5, name: 'Kiểm tra mâu thuẫn',  note: 'Hai phòng lệch số → KHÔNG tự chọn, phải báo và đối chiếu' },
  { n: 6, name: 'Phân tích',           note: 'Giao Agent chuyên môn xử lý' },
  { n: 7, name: 'Kiểm toán',           note: 'Bắt buộc với tiền · doanh số · hoa hồng · chính sách · KPI · lợi nhuận' },
  { n: 8, name: 'Trả kết quả',         note: 'Chỉ kết luận, số liệu, cách tính, cảnh báo, hành động' }
];

// Thứ tự ưu tiên khi hai dữ liệu mâu thuẫn (cao → thấp)
window.PRIORITY = [
  'Dữ liệu hệ thống gốc / tài liệu chính thức',
  'Dữ liệu API / database / CRM',
  'File anh cung cấp',
  'Thông tin anh trực tiếp xác nhận',
  'Kết quả phân tích của AI'
];
