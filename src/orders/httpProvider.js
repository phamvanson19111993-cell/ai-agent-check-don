import { normalizeOrder } from './normalize.js';

/**
 * Adapter goi API don hang cua ban.
 * Mac dinh dung:
 *   GET {baseUrl}/orders/{code}
 *   GET {baseUrl}/orders?phone={phone}
 * Neu backend co duong dan khac, chi can sua hai ham duoi day.
 */
export class HttpOrderProvider {
  constructor({ baseUrl, apiKey = '', timeoutMs = 8000, fetchImpl = globalThis.fetch }) {
    if (!baseUrl) throw new Error('ORDER_API_BASE_URL chua duoc cau hinh');
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.timeoutMs = timeoutMs;
    this.fetch = fetchImpl;
  }

  async #get(pathname) {
    const headers = { accept: 'application/json' };
    if (this.apiKey) headers.authorization = `Bearer ${this.apiKey}`;
    const res = await this.fetch(`${this.baseUrl}${pathname}`, {
      headers,
      signal: AbortSignal.timeout(this.timeoutMs),
    });
    if (res.status === 404) return null;
    if (!res.ok) {
      throw new Error(`API don hang tra ve ${res.status} cho ${pathname}`);
    }
    return res.json();
  }

  async getOrder(code) {
    const body = await this.#get(`/orders/${encodeURIComponent(code)}`);
    if (!body) return null;
    return normalizeOrder(body.data ?? body.order ?? body);
  }

  async findOrdersByPhone(phone) {
    const body = await this.#get(`/orders?phone=${encodeURIComponent(phone)}`);
    if (!body) return [];
    const list = Array.isArray(body) ? body : (body.data ?? body.orders ?? []);
    return list.map(normalizeOrder).filter(Boolean);
  }
}
