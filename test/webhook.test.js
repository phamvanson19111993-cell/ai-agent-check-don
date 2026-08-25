import test from 'node:test';
import assert from 'node:assert/strict';
import { createWebhookHandler, Deduper, GREETING, ERROR_REPLY } from '../src/zalo/webhook.js';
import { computeMac } from '../src/zalo/signature.js';

const config = {
  zalo: { appId: 'app1', oaSecretKey: 'secret1', verifySignature: true },
};

function fakeZalo() {
  const sent = [];
  return {
    sent,
    sendText: async (userId, text) => sent.push({ userId, text }),
    sendTypingOn: async () => {},
  };
}

function build({ agent = null, fallbackAgent, zalo = fakeZalo(), deduper } = {}) {
  const handler = createWebhookHandler({
    config,
    agent,
    fallbackAgent: fallbackAgent ?? { reply: async () => ({ text: 'fallback reply' }) },
    zalo,
    deduper,
  });
  return { handler, zalo };
}

test('verifyAndParse tu choi chu ky sai', () => {
  const { handler } = build();
  const rawBody = JSON.stringify({ timestamp: '1756100000000' });
  const result = handler.verifyAndParse({ rawBody, signature: 'mac=sai' });
  assert.deepEqual(result, { ok: false, status: 401, reason: 'invalid_signature' });
});

test('verifyAndParse chap nhan chu ky dung', () => {
  const { handler } = build();
  const rawBody = JSON.stringify({ timestamp: '1756100000000', event_name: 'follow' });
  const mac = computeMac({
    appId: 'app1',
    rawBody,
    timestamp: '1756100000000',
    oaSecretKey: 'secret1',
  });
  const result = handler.verifyAndParse({ rawBody, signature: `mac=${mac}` });
  assert.equal(result.ok, true);
  assert.equal(result.event.event_name, 'follow');
});

test('verifyAndParse bao loi khi body khong phai JSON', () => {
  const { handler } = build();
  const result = handler.verifyAndParse({ rawBody: 'khong-phai-json', signature: 'mac=x' });
  assert.deepEqual(result, { ok: false, status: 400, reason: 'invalid_json' });
});

test('su kien follow gui loi chao', async () => {
  const { handler, zalo } = build();
  await handler.processEvent({ event_name: 'follow', sender: { id: 'u1' } });
  assert.deepEqual(zalo.sent, [{ userId: 'u1', text: GREETING }]);
});

test('user_send_text goi agent va gui cau tra loi', async () => {
  const agent = { reply: async ({ text }) => ({ text: `da nhan: ${text}` }) };
  const { handler, zalo } = build({ agent });

  await handler.processEvent({
    event_name: 'user_send_text',
    sender: { id: 'u1' },
    message: { msg_id: 'm1', text: 'DH123456' },
  });
  assert.deepEqual(zalo.sent, [{ userId: 'u1', text: 'da nhan: DH123456' }]);
});

test('bo qua event trung msg_id', async () => {
  const agent = { reply: async () => ({ text: 'reply' }) };
  const { handler, zalo } = build({ agent });
  const event = {
    event_name: 'user_send_text',
    sender: { id: 'u1' },
    message: { msg_id: 'm1', text: 'hi' },
  };

  await handler.processEvent(event);
  const second = await handler.processEvent(event);
  assert.equal(second.skipped, 'duplicate');
  assert.equal(zalo.sent.length, 1);
});

test('agent loi thi rot xuong fallback, khach van co tra loi', async () => {
  const agent = {
    reply: async () => {
      throw new Error('Anthropic 529');
    },
  };
  const { handler, zalo } = build({ agent });

  await handler.processEvent({
    event_name: 'user_send_text',
    sender: { id: 'u1' },
    message: { msg_id: 'm1', text: 'DH123456' },
  });
  assert.deepEqual(zalo.sent, [{ userId: 'u1', text: 'fallback reply' }]);
});

test('ca agent lan fallback loi thi gui tin xin loi', async () => {
  const boom = async () => {
    throw new Error('down');
  };
  const { handler, zalo } = build({
    agent: { reply: boom },
    fallbackAgent: { reply: boom },
  });

  await handler.processEvent({
    event_name: 'user_send_text',
    sender: { id: 'u1' },
    message: { msg_id: 'm1', text: 'hi' },
  });
  assert.deepEqual(zalo.sent, [{ userId: 'u1', text: ERROR_REPLY }]);
});

test('anh/file duoc tra loi huong dan gui text', async () => {
  const { handler, zalo } = build();
  const result = await handler.processEvent({
    event_name: 'user_send_image',
    sender: { id: 'u1' },
    message: { msg_id: 'm2' },
  });
  assert.equal(result.handled, 'attachment');
  assert.match(zalo.sent[0].text, /mã đơn hàng/);
});

test('event khong ho tro thi bo qua, khong gui gi', async () => {
  const { handler, zalo } = build();
  const result = await handler.processEvent({ event_name: 'oa_send_text', sender: { id: 'u1' } });
  assert.equal(result.skipped, 'unsupported_event');
  assert.equal(zalo.sent.length, 0);
});

test('Deduper quen cac id da qua TTL', () => {
  let now = 0;
  const deduper = new Deduper({ ttlMs: 1000, now: () => now });
  assert.equal(deduper.seenBefore('m1'), false);
  assert.equal(deduper.seenBefore('m1'), true);
  now = 2000;
  assert.equal(deduper.seenBefore('m1'), false);
});
