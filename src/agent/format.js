import { formatCurrency } from '../orders/normalize.js';

function formatDate(value) {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleDateString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

/** Ban tom tat don hang dung cho tin nhan tra loi (fallback khong dung AI). */
export function formatOrder(order) {
  const lines = [`Đơn ${order.code}: ${order.statusLabel}`];

  if (order.items.length) {
    const items = order.items
      .map((item) => `• ${item.name} x${item.quantity}`)
      .slice(0, 5)
      .join('\n');
    lines.push(items);
    if (order.items.length > 5) lines.push(`… và ${order.items.length - 5} sản phẩm khác`);
  }

  const total = formatCurrency(order.total);
  if (total && order.total > 0) lines.push(`Tổng tiền: ${total}`);
  if (order.carrier) {
    lines.push(
      order.trackingCode
        ? `Vận chuyển: ${order.carrier} (mã ${order.trackingCode})`
        : `Vận chuyển: ${order.carrier}`,
    );
  }
  const eta = formatDate(order.estimatedDelivery);
  if (eta && order.status !== 'delivered' && order.status !== 'cancelled') {
    lines.push(`Dự kiến giao: ${eta}`);
  }
  const last = order.history.at(-1);
  if (last?.note) lines.push(`Cập nhật mới nhất: ${last.note}`);

  return lines.join('\n');
}

export function formatOrderList(orders) {
  if (!orders.length) return 'Không tìm thấy đơn hàng nào.';
  return orders
    .map((order) => `• ${order.code} — ${order.statusLabel}`)
    .join('\n');
}
