import fs from 'node:fs/promises';
import { normalizeOrder } from './normalize.js';

/**
 * Provider doc don tu file JSON — dung de dev/demo khi chua noi he thong that.
 * File duoc doc lai khi mtime thay doi nen sua don la thay ngay, khong can restart.
 */
export class MockOrderProvider {
  constructor(filePath) {
    this.filePath = filePath;
    this.cache = null;
    this.mtimeMs = 0;
  }

  async #load() {
    const stat = await fs.stat(this.filePath);
    if (this.cache && stat.mtimeMs === this.mtimeMs) return this.cache;
    const raw = JSON.parse(await fs.readFile(this.filePath, 'utf8'));
    const orders = Array.isArray(raw) ? raw : (raw.orders ?? []);
    this.cache = orders.map(normalizeOrder).filter(Boolean);
    this.mtimeMs = stat.mtimeMs;
    return this.cache;
  }

  async getOrder(code) {
    const wanted = String(code ?? '').trim().toUpperCase();
    if (!wanted) return null;
    const orders = await this.#load();
    return orders.find((order) => order.code === wanted) ?? null;
  }

  async findOrdersByPhone(phone) {
    const wanted = String(phone ?? '').replace(/\D/g, '');
    if (!wanted) return [];
    const orders = await this.#load();
    return orders.filter((order) => String(order.phone ?? '').replace(/\D/g, '') === wanted);
  }
}
