import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createServer } from '../src/server.js';

async function withServer(handler, fn) {
  const server = createServer({ handler });
  server.listen(0);
  await once(server, 'listening');
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    await fn(base);
  } finally {
    server.close();
    await once(server, 'close');
  }
}

const okHandler = (processed) => ({
  verifyAndParse: ({ rawBody }) => ({ ok: true, status: 200, event: JSON.parse(rawBody) }),
  processEvent: async (event) => {
    processed.push(event);
  },
});

test('GET /health tra ve trang thai', async () => {
  await withServer(okHandler([]), async (base) => {
    const res = await fetch(`${base}/health`);
    assert.equal(res.status, 200);
    assert.equal((await res.json()).status, 'ok');
  });
});

test('POST /webhook ack 200 ngay va xu ly event sau do', async () => {
  const processed = [];
  await withServer(okHandler(processed), async (base) => {
    const res = await fetch(`${base}/webhook`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ event_name: 'follow', sender: { id: 'u1' } }),
    });
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { status: 'ok' });
    // processEvent chay sau khi da tra loi HTTP
    await new Promise((resolve) => setImmediate(resolve));
    assert.equal(processed.length, 1);
    assert.equal(processed[0].event_name, 'follow');
  });
});

test('POST /webhook tra ve ma loi khi verify that bai', async () => {
  const handler = {
    verifyAndParse: () => ({ ok: false, status: 401, reason: 'invalid_signature' }),
    processEvent: async () => assert.fail('khong duoc xu ly event chua xac thuc'),
  };
  await withServer(handler, async (base) => {
    const res = await fetch(`${base}/webhook`, { method: 'POST', body: '{}' });
    assert.equal(res.status, 401);
    assert.equal((await res.json()).error, 'invalid_signature');
  });
});

test('loi trong processEvent khong lam sap server', async () => {
  const handler = {
    verifyAndParse: ({ rawBody }) => ({ ok: true, status: 200, event: JSON.parse(rawBody) }),
    processEvent: async () => {
      throw new Error('loi xu ly');
    },
  };
  await withServer(handler, async (base) => {
    const res = await fetch(`${base}/webhook`, { method: 'POST', body: '{}' });
    assert.equal(res.status, 200);
    await new Promise((resolve) => setImmediate(resolve));
    const health = await fetch(`${base}/health`);
    assert.equal(health.status, 200);
  });
});

test('duong dan la tra ve 404', async () => {
  await withServer(okHandler([]), async (base) => {
    const res = await fetch(`${base}/khong-ton-tai`);
    assert.equal(res.status, 404);
  });
});
