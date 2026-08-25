import { log } from '../util/log.js';

const MAX_ORDERS_BY_PHONE = 5;

/**
 * Bo thuc thi cong cu cho agent. Tach rieng khoi vong lap goi model de test
 * duoc doc lap va de tai su dung cho fallback khong dung AI.
 */
export function createToolRunner({ orders, onEscalate }) {
  return {
    async lookup_order({ order_code: orderCode }) {
      const order = await orders.getOrder(orderCode);
      if (!order) {
        return { found: false, order_code: String(orderCode ?? '').toUpperCase() };
      }
      return { found: true, order };
    },

    async find_orders_by_phone({ phone }) {
      const list = await orders.findOrdersByPhone(phone);
      return {
        found: list.length > 0,
        count: list.length,
        orders: list.slice(0, MAX_ORDERS_BY_PHONE).map((order) => ({
          code: order.code,
          status: order.status,
          status_label: order.statusLabel,
          created_at: order.createdAt,
          total: order.total,
        })),
      };
    },

    async escalate_to_human({ reason, order_code: orderCode }, context) {
      log.info('agent.escalate', { userId: context?.userId, reason, orderCode });
      await onEscalate?.({ userId: context?.userId, reason, orderCode });
      return { ok: true, note: 'Da ghi nhan yeu cau chuyen nhan vien CSKH.' };
    },
  };
}
