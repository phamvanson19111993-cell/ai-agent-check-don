import crypto from 'node:crypto';

/**
 * Zalo OA ky webhook bang header `X-ZEvent-Signature` co dang:
 *   mac=sha256(appId + rawBody + timestamp + OASecretKey)
 * `rawBody` phai la chuoi body goc, khong duoc JSON.parse roi stringify lai.
 */
export function computeMac({ appId, rawBody, timestamp, oaSecretKey }) {
  return crypto
    .createHash('sha256')
    .update(`${appId}${rawBody}${timestamp}${oaSecretKey}`, 'utf8')
    .digest('hex');
}

export function parseSignatureHeader(header) {
  if (!header) return '';
  const value = String(header).trim();
  return value.startsWith('mac=') ? value.slice(4) : value;
}

export function verifySignature({ header, appId, rawBody, timestamp, oaSecretKey }) {
  const provided = parseSignatureHeader(header);
  if (!provided || !appId || !oaSecretKey || !timestamp) return false;
  const expected = computeMac({ appId, rawBody, timestamp, oaSecretKey });
  const a = Buffer.from(provided, 'utf8');
  const b = Buffer.from(expected, 'utf8');
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}
