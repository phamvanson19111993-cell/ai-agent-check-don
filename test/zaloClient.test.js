import test from 'node:test';
import assert from 'node:assert/strict';
import { ZaloClient, splitText } from '../src/zalo/client.js';
import { MemoryTokenStore } from '../src/zalo/tokenStore.js';

function jsonResponse(body, { ok = true, status = 200 } = {}) {
  return { ok, status, json: async () => body };
}

function makeClient(handler, { store = new MemoryTokenStore(), now = () => 1_000_000 } = {}) {
  const calls = [];
  const client = new ZaloClient({
    appId: 'app1',
    appSecret: 'secret1',
    refreshToken: 'seed-refresh',
    tokenStore: store,
    fetchImpl: async (url, options) => {
      calls.push({ url, options });
      return handler(url, options, calls.length);
    },
    now,
  });
  return { client, calls, store };
}

test('splitText giu nguyen tin ngan va cat tin dai theo ranh gioi tu', () => {
  assert.deepEqual(splitText('xin chao'), ['xin chao']);
  assert.deepEqual(splitText('   '), []);
  const chunks = splitText('a'.repeat(30) + ' ' + 'b'.repeat(30), 40);
  assert.equal(chunks.length, 2);
  assert.ok(chunks.every((chunk) => chunk.length <= 40));
});

test('getAccessToken lam moi va luu refresh token moi', async () => {
  const { client, store, calls } = makeClient(() =>
    jsonResponse({ access_token: 'at-1', refresh_token: 'rt-2', expires_in: '90000' }),
  );

  assert.equal(await client.getAccessToken(), 'at-1');
  const saved = await store.read();
  assert.equal(saved.refresh_token, 'rt-2');
  assert.equal(saved.expires_at, 1_000_000 + 90_000_000);
  assert.equal(calls[0].options.headers.secret_key, 'secret1');
  assert.match(calls[0].options.body, /grant_type=refresh_token/);
});

test('getAccessToken dung lai token con han, khong goi lai OAuth', async () => {
  const store = new MemoryTokenStore({
    access_token: 'at-cached',
    refresh_token: 'rt-1',
    expires_at: 2_000_000,
  });
  const { client, calls } = makeClient(() => {
    throw new Error('khong duoc goi OAuth');
  }, { store });

  assert.equal(await client.getAccessToken(), 'at-cached');
  assert.equal(calls.length, 0);
});

test('cac lan getAccessToken song song chi refresh mot lan', async () => {
  let refreshes = 0;
  const { client } = makeClient(() => {
    refreshes += 1;
    return jsonResponse({ access_token: 'at-1', refresh_token: 'rt-2', expires_in: 90000 });
  });

  const tokens = await Promise.all([client.getAccessToken(), client.getAccessToken()]);
  assert.deepEqual(tokens, ['at-1', 'at-1']);
  assert.equal(refreshes, 1);
});

test('sendText goi endpoint CS message voi access token', async () => {
  const { client, calls } = makeClient((url) => {
    if (url.includes('access_token')) {
      return jsonResponse({ access_token: 'at-1', refresh_token: 'rt-2', expires_in: 90000 });
    }
    return jsonResponse({ error: 0, message: 'Success', data: { message_id: 'm1' } });
  });

  await client.sendText('user-1', 'xin chao');
  const send = calls.at(-1);
  assert.match(send.url, /\/oa\/message\/cs$/);
  assert.equal(send.options.headers.access_token, 'at-1');
  assert.deepEqual(JSON.parse(send.options.body), {
    recipient: { user_id: 'user-1' },
    message: { text: 'xin chao' },
  });
});

test('sendText lam moi token va thu lai khi Zalo bao -216', async () => {
  let sendAttempts = 0;
  const { client } = makeClient((url) => {
    if (url.includes('access_token')) {
      return jsonResponse({ access_token: 'at-new', refresh_token: 'rt-2', expires_in: 90000 });
    }
    sendAttempts += 1;
    if (sendAttempts === 1) return jsonResponse({ error: -216, message: 'Access token expired' });
    return jsonResponse({ error: 0, message: 'Success', data: {} });
  });

  await client.sendText('user-1', 'hi');
  assert.equal(sendAttempts, 2);
});

test('sendText nem loi khi Zalo tra ma loi khong phai loi token', async () => {
  const { client } = makeClient((url) => {
    if (url.includes('access_token')) {
      return jsonResponse({ access_token: 'at-1', refresh_token: 'rt-2', expires_in: 90000 });
    }
    return jsonResponse({ error: -32, message: 'User khong ton tai' });
  });

  await assert.rejects(() => client.sendText('user-x', 'hi'), /User khong ton tai/);
});
