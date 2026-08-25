import crypto from 'node:crypto';

/**
 * Luong uy quyen OA cua Zalo (OAuth v4 + PKCE):
 *   1. Tao code_verifier ngau nhien, code_challenge = base64url(sha256(verifier))
 *   2. Mo .../v4/oa/permission?app_id=&redirect_uri=&code_challenge=&state=
 *   3. Zalo goi ve redirect_uri kem ?code=...&oa_id=...&state=...
 *   4. POST .../v4/oa/access_token voi code + code_verifier => access_token + refresh_token
 * Refresh token thu duoc chinh la ZALO_REFRESH_TOKEN can dien vao .env.
 */
export function base64UrlEncode(buffer) {
  return buffer.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function createPkcePair(verifier = base64UrlEncode(crypto.randomBytes(48))) {
  const challenge = base64UrlEncode(crypto.createHash('sha256').update(verifier).digest());
  return { codeVerifier: verifier, codeChallenge: challenge };
}

export function buildPermissionUrl({
  appId,
  redirectUri,
  codeChallenge,
  state,
  oauthBase = 'https://oauth.zaloapp.com/v4',
}) {
  const url = new URL(`${oauthBase.replace(/\/$/, '')}/oa/permission`);
  url.searchParams.set('app_id', appId);
  url.searchParams.set('redirect_uri', redirectUri);
  url.searchParams.set('code_challenge', codeChallenge);
  if (state) url.searchParams.set('state', state);
  return url.toString();
}

export async function exchangeCodeForToken({
  appId,
  appSecret,
  code,
  codeVerifier,
  oauthBase = 'https://oauth.zaloapp.com/v4',
  fetchImpl = globalThis.fetch,
  now = () => Date.now(),
}) {
  const res = await fetchImpl(`${oauthBase.replace(/\/$/, '')}/oa/access_token`, {
    method: 'POST',
    headers: {
      'content-type': 'application/x-www-form-urlencoded',
      secret_key: appSecret,
    },
    body: new URLSearchParams({
      code,
      app_id: appId,
      grant_type: 'authorization_code',
      code_verifier: codeVerifier,
    }).toString(),
  });

  const body = await res.json().catch(() => ({}));
  if (!res.ok || !body.access_token) {
    const reason = body.error_description || body.message || body.error || `HTTP ${res.status}`;
    throw new Error(`Doi code lay token that bai: ${reason}`);
  }

  const expiresInSec = Number(body.expires_in) || 90_000;
  return {
    access_token: body.access_token,
    refresh_token: body.refresh_token,
    expires_at: now() + expiresInSec * 1000,
    updated_at: new Date(now()).toISOString(),
  };
}
