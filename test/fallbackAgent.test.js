import test from 'node:test';
import assert from 'node:assert/strict';
import { FallbackOrderAgent, ASK_INFO } from '../src/agent/fallbackAgent.js';
import { MockOrderProvider } from '../src/orders/mockProvider.js';

const agent = new FallbackOrderAgent({ orders: new MockOrderProvider('./data/orders.json') });

test('tra cuu duoc khi khach gui ma don', async () => {
  const answer = await agent.reply({ text: 'cho hoi don DH123456' });
  assert.match(answer.text, /DH123456/);
  assert.match(answer.text, /Đang giao/);
  assert.match(answer.text, /GHN889231/);
});

test('liet ke nhieu don khi so dien thoai co nhieu don', async () => {
  const answer = await agent.reply({ text: 'sdt 0901234567' });
  assert.match(answer.text, /2 đơn/);
  assert.match(answer.text, /DH123456/);
  assert.match(answer.text, /DH123458/);
});

test('tra chi tiet khi so dien thoai chi co mot don', async () => {
  const answer = await agent.reply({ text: 'so cua toi la 0912345678' });
  assert.match(answer.text, /DH123457/);
  assert.match(answer.text, /Giao thành công/);
});

test('bao khong tim thay khi ma don khong ton tai', async () => {
  const answer = await agent.reply({ text: 'don DH000111 dau roi' });
  assert.match(answer.text, /chưa tìm thấy đơn DH000111/i);
});

test('hoi xin thong tin khi tin nhan khong co ma don lan sdt', async () => {
  const answer = await agent.reply({ text: 'shop oi' });
  assert.equal(answer.text, ASK_INFO);
});
