// Danh sách AI Agent — sắp xếp theo độ quan trọng TĂNG DẦN:
// ít quan trọng ở trên, quan trọng nhất ở dưới cùng.
window.AGENT_GROUPS = [
  {
    name: 'ai-agent-check-don',
    agents: [
      { icon: '📚', name: 'AI agent học tập và đào tạo',     role: 'Nội bộ: tự học, đào tạo nhân viên mới' },
      { icon: '🎥', name: 'Video hướng dẫn curl Foxia API',  role: 'Hướng dẫn kỹ thuật: gọi API Foxia bằng curl' },
      { icon: '🩺', name: 'AI Agent video content sức khỏe', role: 'Sản xuất nội dung video chủ đề sức khỏe' },
      { icon: '👩', name: 'Lady Page',                        role: 'Vận hành & trả lời fanpage thương hiệu' },
      { icon: '📊', name: 'Cập nhật dữ liệu Fanpage Pancake', role: 'Đồng bộ dữ liệu fanpage từ Pancake về hệ thống' }
    ]
  },
  {
    name: 'mac',
    agents: [
      { icon: '🎬', name: 'Edivideo',                         role: 'Dựng & cắt video tự động' },
      { icon: '✍️', name: 'AI viết kịch bản sale',            role: 'Viết kịch bản bán hàng, content chốt đơn' },
      { icon: '💬', name: 'Agen Zalo',                         role: 'Tư vấn & chăm khách trên Zalo' },
      { icon: '🎧', name: 'AI chăm sóc khách hàng',           role: 'CSKH sau bán, xử lý khiếu nại' },
      { icon: '📞', name: 'Tổng hợp SĐT chưa chốt Pancake',   role: 'Gom lead chưa chốt để gọi lại, remarketing' },
      { icon: '🔁', name: 'Telegram bot kiểm tra trùng đơn',  role: 'Chặn trùng đơn, cảnh báo tức thì qua Telegram' }
    ]
  }
];
