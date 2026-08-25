import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {
  base64UrlEncode,
  buildPermissionUrl,
  createPkcePair,
  exchangeCodeForToken,
} from '../src/zalo/oauth.js';

test('createPkcePair tao challenge = base64url(sha256(verifier))', () => {
  const { codeVerifier, codeChallenge } = createPkcePair('verifier-co-dinh');
  const expected = base64UrlEncode(
    crypto.createHash('sha256').update('verifier-co-dinh').digest(),
  );
  assert.equal(codeVerifier, 'verifier-co-dinh');
  assert.equal(codeChallenge, expected);
  assert.doesNotMatch(codeChallenge, /[+/=]/); // phai la base64url, an toan tren URL
});

test('createPkcePair sinh verifier ngau nhien du dai', () => {
  const a = createPkcePair();
  const b = createPkcePair();
  assert.notEqual(a.codeVerifier, b.codeVerifier);
  assert.ok(a.codeVerifier.length >= 43 && a.codeVerifier.length <= 128);
});

test('buildPermissionUrl dung endpoint OA va day du tham so', () => {
  const url = new URL(
    buildPermissionUrl({
      appId: 'app1',
      redirectUri: 'http://localhost:3000/oauth/callback',
      codeChallenge: 'chal',
      state: 'st1',
    }),
  );
  assert.equal(url.origin + url.pathname, 'https://oauth.zaloapp.com/v4/oa/permission');
  assert.equal(url.searchParams.get('app_id'), 'app1');
  assert.equal(url.searchParams.get('redirect_uri'), 'http://localhost:3000/oauth/callback');
  assert.equal(url.searchParams.get('code_challenge'), 'chal');
  assert.equal(url.searchParams.get('state'), 'st1');
});

test('exchangeCodeForToken gui dung header secret_key va body authorization_code', async () => {
  let seen;
  const token = await exchangeCodeForToken({
    appId: 'app1',
    appSecret: 'secret1',
    code: 'code-abc',
    codeVerifier: 'ver-1',
    fetchImpl: async (url, options) => {
      seen = { url, options };
      return {
        ok: true,
        status: 200,
        json: async () => ({ access_token: 'at', refresh_token: 'rt', expires_in: '90000' }),
      };
    },
    now: () => 1000,
  });

  assert.equal(seen.url, 'https://oauth.zaloapp.com/v4/oa/access_token');
  assert.equal(seen.options.headers.secret_key, 'secret1');
  const body = new URLSearchParams(seen.options.body);
  assert.equal(body.get('grant_type'), 'authorization_code');
  assert.equal(body.get('code'), 'code-abc');
  assert.equal(body.get('code_verifier'), 'ver-1');
  assert.equal(body.get('app_id'), 'app1');
  assert.deepEqual(token, {
    access_token: 'at',
    refresh_token: 'rt',
    expires_at: 1000 + 90_000_000,
    updated_at: new Date(1000).toISOString(),
  });
});

test('exchangeCodeForToken bao loi ro rang khi Zalo tu choi', async () => {
  await assert.rejects(
    () =>
      exchangeCodeForToken({
        appId: 'app1',
        appSecret: 'secret1',
        code: 'sai',
        codeVerifier: 'ver',
        fetchImpl: async () => ({
          ok: true,
          status: 200,
          json: async () => ({ error: -201, error_description: 'Code khong hop le' }),
        }),
      }),
    /Code khong hop le/,
  );
});
