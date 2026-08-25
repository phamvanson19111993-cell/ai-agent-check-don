import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { computeMac, parseSignatureHeader, verifySignature } from '../src/zalo/signature.js';

const appId = '1234567890';
const oaSecretKey = 'super-secret';
const rawBody = '{"event_name":"user_send_text","timestamp":"1756100000000"}';
const timestamp = '1756100000000';

test('computeMac khop cong thuc sha256(appId + body + timestamp + secret)', () => {
  const expected = crypto
    .createHash('sha256')
    .update(appId + rawBody + timestamp + oaSecretKey)
    .digest('hex');
  assert.equal(computeMac({ appId, rawBody, timestamp, oaSecretKey }), expected);
});

test('parseSignatureHeader bo tien to mac=', () => {
  assert.equal(parseSignatureHeader('mac=abc123'), 'abc123');
  assert.equal(parseSignatureHeader('abc123'), 'abc123');
  assert.equal(parseSignatureHeader(undefined), '');
});

test('verifySignature chap nhan chu ky dung va tu choi chu ky sai', () => {
  const mac = computeMac({ appId, rawBody, timestamp, oaSecretKey });
  assert.equal(
    verifySignature({ header: `mac=${mac}`, appId, rawBody, timestamp, oaSecretKey }),
    true,
  );
  assert.equal(
    verifySignature({ header: 'mac=deadbeef', appId, rawBody, timestamp, oaSecretKey }),
    false,
  );
  assert.equal(
    verifySignature({ header: `mac=${mac}`, appId, rawBody: `${rawBody} `, timestamp, oaSecretKey }),
    false,
  );
});

test('verifySignature tu choi khi thieu tham so', () => {
  assert.equal(verifySignature({ header: '', appId, rawBody, timestamp, oaSecretKey }), false);
  assert.equal(
    verifySignature({ header: 'mac=x', appId, rawBody, timestamp: undefined, oaSecretKey }),
    false,
  );
});
