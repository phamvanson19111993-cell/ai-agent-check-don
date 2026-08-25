/** Cac trang thai chuan hoa + nhan tieng Viet dung khi tra loi khach. */
export const STATUS_LABELS = {
  pending: 'Chờ xác nhận',
  confirmed: 'Đã xác nhận',
  packing: 'Đang đóng gói',
  shipping: 'Đang giao',
  delivered: 'Giao thành công',
  cancelled: 'Đã hủy',
  returned: 'Hoàn hàng',
  unknown: 'Không xác định',
};

const STATUS_ALIASES = {
  cho_xac_nhan: 'pending',
  choxacnhan: 'pending',
  new: 'pending',
  da_xac_nhan: 'confirmed',
  dang_dong_goi: 'packing',
  processing: 'packing',
  dang_giao: 'shipping',
  shipped: 'shipping',
  in_transit: 'shipping',
  da_giao: 'delivered',
  completed: 'delivered',
  success: 'delivered',
  da_huy: 'cancelled',
  canceled: 'cancelled',
  hoan_hang: 'returned',
  refunded: 'returned',
};

export function normalizeStatus(status) {
  const key = String(status ?? '')
    .trim()
    .toLowerCase()
    .replace(/[\s-]+/g, '_');
  if (!key) return 'unknown';
  if (STATUS_LABELS[key]) return key;
  return STATUS_ALIASES[key] ?? 'unknown';
}

/** Ma don: 6-24 ky tu chu/so, cho phep gach ngang. VD: DH123456, SPX-77A9B2 */
const ORDER_CODE_RE = /\b([A-Za-z]{0,4}[-_]?\d[A-Za-z0-9-]{4,23})\b/g;

export function extractOrderCodes(text) {
  const found = new Set();
  for (const match of String(text ?? '').matchAll(ORDER_CODE_RE)) {
    const code = match[1].replace(/[-_]+$/, '');
    // Loai so dien thoai (10-11 chu so thuan) khoi danh sach ma don.
    if (/^0\d{9,10}$/.test(code)) continue;
    if (code.length >= 6) found.add(code.toUpperCase());
  }
  return [...found];
}

/** So dien thoai VN: 0xxxxxxxxx, +84xxxxxxxxx, 84xxxxxxxxx */
export function extractPhone(text) {
  const match = String(text ?? '').match(/(?:\+?84|0)(\d{9,10})\b/);
  if (!match) return null;
  return `0${match[1]}`;
}

export function normalizeOrder(raw) {
  if (!raw) return null;
  const status = normalizeStatus(raw.status);
  return {
    code: String(raw.code ?? raw.order_code ?? raw.id ?? '').toUpperCase(),
    status,
    statusLabel: raw.status_label || STATUS_LABELS[status],
    customerName: raw.customer_name ?? raw.customerName ?? null,
    phone: raw.phone ?? raw.customer_phone ?? null,
    address: raw.address ?? raw.shipping_address ?? null,
    items: (raw.items ?? []).map((item) => ({
      name: item.name ?? item.product_name ?? 'San pham',
      quantity: Number(item.quantity ?? item.qty ?? 1),
      price: Number(item.price ?? 0),
    })),
    total: Number(raw.total ?? raw.total_amount ?? 0),
    paymentStatus: raw.payment_status ?? raw.paymentStatus ?? null,
    carrier: raw.carrier ?? raw.shipping_partner ?? null,
    trackingCode: raw.tracking_code ?? raw.trackingCode ?? null,
    createdAt: raw.created_at ?? raw.createdAt ?? null,
    estimatedDelivery: raw.estimated_delivery ?? raw.estimatedDelivery ?? null,
    history: (raw.history ?? []).map((entry) => ({
      at: entry.at ?? entry.time ?? null,
      status: normalizeStatus(entry.status),
      note: entry.note ?? null,
    })),
  };
}

export function formatCurrency(amount) {
  if (!Number.isFinite(amount)) return null;
  return `${amount.toLocaleString('vi-VN')}đ`;
}
