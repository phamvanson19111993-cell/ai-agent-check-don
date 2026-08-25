import test from 'node:test';
import assert from 'node:assert/strict';
import {
  extractOrderCodes,
  extractPhone,
  normalizeOrder,
  normalizeStatus,
} from '../src/orders/normalize.js';

test('normalizeStatus map cac alias tieng Viet va tieng Anh', () => {
  assert.equal(normalizeStatus('dang_giao'), 'shipping');
  assert.equal(normalizeStatus('IN TRANSIT'), 'shipping');
  assert.equal(normalizeStatus('completed'), 'delivered');
  assert.equal(normalizeStatus('lung tung'), 'unknown');
  assert.equal(normalizeStatus(undefined), 'unknown');
});

test('extractOrderCodes bat ma don va bo qua so dien thoai', () => {
  assert.deepEqual(extractOrderCodes('cho minh hoi don DH123456 voi'), ['DH123456']);
  assert.deepEqual(extractOrderCodes('ma spx-77a9b2 sao roi'), ['SPX-77A9B2']);
  assert.deepEqual(extractOrderCodes('sdt cua minh la 0901234567'), []);
});

test('extractPhone chuan hoa cac dinh dang so VN', () => {
  assert.equal(extractPhone('sdt 0901234567'), '0901234567');
  assert.equal(extractPhone('+84901234567 nhe'), '0901234567');
  assert.equal(extractPhone('khong co so'), null);
});

test('normalizeOrder chap nhan ca snake_case lan camelCase', () => {
  const order = normalizeOrder({
    order_code: 'dh999',
    status: 'DANG GIAO',
    customer_name: 'Test',
    items: [{ product_name: 'Ao thun', qty: '2', price: '100000' }],
    total_amount: '200000',
    trackingCode: 'GHN1',
  });
  assert.equal(order.code, 'DH999');
  assert.equal(order.status, 'shipping');
  assert.equal(order.statusLabel, 'Đang giao');
  assert.deepEqual(order.items, [{ name: 'Ao thun', quantity: 2, price: 100000 }]);
  assert.equal(order.total, 200000);
  assert.equal(order.trackingCode, 'GHN1');
});
