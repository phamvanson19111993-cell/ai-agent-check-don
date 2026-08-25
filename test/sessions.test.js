import test from 'node:test';
import assert from 'node:assert/strict';
import { SessionStore } from '../src/store/sessions.js';

test('luu va doc lai lich su theo user', () => {
  const store = new SessionStore({ maxTurns: 5 });
  store.set('u1', [{ role: 'user', content: 'hi' }]);
  assert.deepEqual(store.get('u1'), [{ role: 'user', content: 'hi' }]);
  assert.deepEqual(store.get('u2'), []);
});

test('het TTL thi lich su bi bo', () => {
  let now = 0;
  const store = new SessionStore({ maxTurns: 5, ttlMs: 1000, now: () => now });
  store.set('u1', [{ role: 'user', content: 'hi' }]);
  now = 1500;
  assert.deepEqual(store.get('u1'), []);
});

test('cat lich su nhung khong bao gio bat dau bang tool_result mo coi', () => {
  const store = new SessionStore({ maxTurns: 1 }); // giu toi da 2 tin
  store.set('u1', [
    { role: 'user', content: 'don DH1' },
    {
      role: 'assistant',
      content: [{ type: 'tool_use', id: 't1', name: 'lookup_order', input: {} }],
    },
    { role: 'user', content: [{ type: 'tool_result', tool_use_id: 't1', content: '{}' }] },
    { role: 'assistant', content: [{ type: 'text', text: 'Đơn đang giao ạ.' }] },
    { role: 'user', content: 'cam on shop' },
  ]);

  const kept = store.get('u1');
  assert.equal(kept[0].role, 'user');
  assert.equal(kept[0].content, 'cam on shop');
});

test('prune xoa cac phien qua han', () => {
  let now = 0;
  const store = new SessionStore({ maxTurns: 5, ttlMs: 1000, now: () => now });
  store.set('u1', [{ role: 'user', content: 'hi' }]);
  now = 5000;
  store.set('u2', [{ role: 'user', content: 'hi' }]);
  store.prune();
  assert.equal(store.sessions.has('u1'), false);
  assert.equal(store.sessions.has('u2'), true);
});
