import { extractOrderCodes, extractPhone } from '../orders/normalize.js';
import { formatOrder, formatOrderList } from './format.js';

const ASK_INFO =
  'Chào anh/chị! Anh/chị cho shop xin mã đơn hàng (ví dụ DH123456) hoặc số điện thoại đặt hàng để shop kiểm tra giúp ạ.';

/**
 * Agent du phong khong dung AI: bat mã don / so dien thoai bang regex.
 * Dung khi chua cau hinh ANTHROPIC_API_KEY, hoac khi goi Claude that bai —
 * khach van nhan duoc tra loi huu ich thay vi im lang.
 */
export class FallbackOrderAgent {
  constructor({ orders }) {
    this.orders = orders;
  }

  async reply({ text }) {
    const codes = extractOrderCodes(text);
    for (const code of codes) {
      const order = await this.orders.getOrder(code);
      if (order) return { text: formatOrder(order), escalated: false, fallback: true };
    }

    const phone = extractPhone(text);
    if (phone) {
      const orders = await this.orders.findOrdersByPhone(phone);
      if (orders.length === 1) {
        return { text: formatOrder(orders[0]), escalated: false, fallback: true };
      }
      if (orders.length > 1) {
        return {
          text: `Shop tìm thấy ${orders.length} đơn của số ${phone}:\n${formatOrderList(orders)}\nAnh/chị cho shop xin mã đơn cần kiểm tra ạ.`,
          escalated: false,
          fallback: true,
        };
      }
    }

    if (codes.length) {
      return {
        text: `Shop chưa tìm thấy đơn ${codes[0]}. Anh/chị kiểm tra lại mã đơn hoặc gửi số điện thoại đặt hàng giúp shop ạ.`,
        escalated: false,
        fallback: true,
      };
    }

    return { text: ASK_INFO, escalated: false, fallback: true };
  }
}

export { ASK_INFO };
