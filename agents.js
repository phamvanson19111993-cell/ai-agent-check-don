// 11 phòng AI — nhóm chạy trên máy Mac xếp trước (Phòng 1–5),
// nhóm chạy trên Claude cloud xếp sau (Phòng 6–11), trong mỗi nhóm giữ thứ tự ưu tiên tăng dần.
// Đổi thứ tự = đổi vị trí trong mảng này, số phòng tự chạy lại.
// where: 'mac' (chạy trên máy) | 'cloud' (mở được từ Claude)
// status: 'wait' (chờ anh) | 'ready' (xong, chờ duyệt) | 'run' (đang chạy) | ''
window.AGENTS = [
  { icon: '📚', name: 'Học tập & đào tạo',      role: 'Nội bộ: tự học, đào tạo nhân viên mới',        where: 'mac' },
  { icon: '🎥', name: 'Curl Foxia API',          role: 'Hướng dẫn kỹ thuật: gọi API Foxia',            where: 'mac' },
  { icon: '🎬', name: 'Edivideo',                role: 'Dựng & cắt video tự động',                     where: 'mac' },
  { icon: '✍️', name: 'Kịch bản sale',           role: 'Content bán hàng, kịch bản chốt đơn',          where: 'mac' },
  { icon: '📞', name: 'SĐT chưa chốt Pancake',   role: 'Gom lead chưa chốt để gọi lại',                where: 'mac' },
  { icon: '🩺', name: 'Video content sức khỏe',  role: 'Kịch bản & hook cho video sức khỏe',           where: 'cloud', status: 'wait',  session: 'session_01NdQBctgvkQShj1xcjPDnET' },
  { icon: '👩', name: 'Lady Page',               role: 'Video & ads sản phẩm trên fanpage',            where: 'cloud', status: 'run',   session: 'session_01NKVuC993sRBvHy3My1qzVp' },
  { icon: '📊', name: 'Fanpage Pancake',         role: 'Đồng bộ dữ liệu fanpage về hệ thống',          where: 'cloud', status: 'ready', session: 'session_01S4GidnKgEJhxx4eWvT9Kx3' },
  { icon: '💬', name: 'Agen Zalo',               role: 'Tư vấn & chăm khách trên Zalo',                where: 'cloud', status: 'ready', session: 'session_019kdZ7RZ4TytuPHKkn5uBFk' },
  { icon: '🎧', name: 'CSKH',                    role: 'Chăm sóc sau bán, xử lý khiếu nại',            where: 'cloud', status: 'wait',  session: 'session_0181dYS4ZhTFf6rMjhxWg23c' },
  { icon: '🔁', name: 'Check trùng đơn',         role: 'Bot Telegram chặn trùng đơn, cảnh báo ngay',   where: 'cloud', status: 'ready', session: 'session_01Kf9BfAZLiJ2CychW21bTn2' }
];
