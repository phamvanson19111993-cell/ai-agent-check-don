import { log } from '../util/log.js';

/** Zalo cat tin nhan text o 2000 ky tu. */
const MAX_TEXT_LENGTH = 2000;
/** Ma loi Zalo cho access token het han / khong hop le. */
const TOKEN_ERRORS = new Set([-216, -217, -124]);

export function splitText(text, limit = MAX_TEXT_LENGTH) {
  const clean = String(text ?? '').trim();
  if (!clean) return [];
  if (clean.length <= limit) return [clean];

  const chunks = [];
  let rest = clean;
  while (rest.length > limit) {
    // Cat o xuong dong hoac khoang trang gan cuoi nhat de khong vo tu.
    let cut = rest.lastIndexOf('\n', limit);
    if (cut < limit * 0.5) cut = rest.lastIndexOf(' ', limit);
    if (cut < limit * 0.5) cut = limit;
    chunks.push(rest.slice(0, cut).trim());
    rest = rest.slice(cut).trim();
  }
  if (rest) chunks.push(rest);
  return chunks;
}

export class ZaloError extends Error {
  constructor(message, { code, details } = {}) {
    super(message);
    this.name = 'ZaloError';
    this.code = code;
    this.details = details;
  }
}

export class ZaloClient {
  /**
   * @param {object} opts
   * @param {string} opts.appId
   * @param {string} opts.appSecret     secret key cua ung dung (header `secret_key`)
   * @param {string} [opts.refreshToken] refresh token khoi tao, dung khi store con rong
   * @param {{read:Function, write:Function}} opts.tokenStore
   * @param {typeof fetch} [opts.fetchImpl]
   */
  constructor({
    appId,
    appSecret,
    refreshToken = '',
    tokenStore,
    oauthBase = 'https://oauth.zaloapp.com/v4',
    apiBase = 'https://openapi.zalo.me/v3.0',
    fetchImpl = globalThis.fetch,
    now = () => Date.now(),
  }) {
    this.appId = appId;
    this.appSecret = appSecret;
    this.seedRefreshToken = refreshToken;
    this.tokenStore = tokenStore;
    this.oauthBase = oauthBase.replace(/\/$/, '');
    this.apiBase = apiBase.replace(/\/$/, '');
    this.fetch = fetchImpl;
    this.now = now;
    this.refreshing = null;
  }

  async getAccessToken({ force = false } = {}) {
    const saved = await this.tokenStore.read();
    if (!force && saved?.access_token && saved.expires_at > this.now() + 60_000) {
      return saved.access_token;
    }
    // Gop cac lan refresh song song lai lam mot: refresh token chi dung duoc mot lan.
    if (!this.refreshing) {
      this.refreshing = this.#refresh(saved).finally(() => {
        this.refreshing = null;
      });
    }
    return this.refreshing;
  }

  async #refresh(saved) {
    const refreshToken = saved?.refresh_token || this.seedRefreshToken;
    if (!refreshToken) {
      throw new ZaloError('Thieu refresh token — hay dat ZALO_REFRESH_TOKEN.');
    }

    const res = await this.fetch(`${this.oauthBase}/oa/access_token`, {
      method: 'POST',
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        secret_key: this.appSecret,
      },
      body: new URLSearchParams({
        refresh_token: refreshToken,
        app_id: this.appId,
        grant_type: 'refresh_token',
      }).toString(),
    });

    const body = await res.json().catch(() => ({}));
    if (!res.ok || !body.access_token) {
      throw new ZaloError('Lam moi access token that bai', {
        code: body.error,
        details: body,
      });
    }

    const expiresInSec = Number(body.expires_in) || 90_000; // Zalo tra ~25 gio
    await this.tokenStore.write({
      access_token: body.access_token,
      // Zalo tra refresh token moi moi lan; giu lai cai cu neu response khong co.
      refresh_token: body.refresh_token || refreshToken,
      expires_at: this.now() + expiresInSec * 1000,
      updated_at: new Date(this.now()).toISOString(),
    });
    log.info('zalo.token.refreshed', { expires_in: expiresInSec });
    return body.access_token;
  }

  async #post(pathname, payload, { retryOnTokenError = true } = {}) {
    const accessToken = await this.getAccessToken();
    const res = await this.fetch(`${this.apiBase}${pathname}`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        access_token: accessToken,
      },
      body: JSON.stringify(payload),
    });
    const body = await res.json().catch(() => ({}));
    const code = Number(body.error ?? 0);

    if (code !== 0 && TOKEN_ERRORS.has(code) && retryOnTokenError) {
      log.warn('zalo.token.invalid_retry', { code });
      await this.getAccessToken({ force: true });
      return this.#post(pathname, payload, { retryOnTokenError: false });
    }
    if (!res.ok || code !== 0) {
      throw new ZaloError(body.message || `Zalo API loi (${pathname})`, {
        code,
        details: body,
      });
    }
    return body.data ?? body;
  }

  /** Gui tin nhan tu van (CS message) toi nguoi dung. */
  async sendText(userId, text) {
    const parts = splitText(text);
    const results = [];
    for (const part of parts) {
      results.push(
        await this.#post('/oa/message/cs', {
          recipient: { user_id: String(userId) },
          message: { text: part },
        }),
      );
    }
    return results;
  }

  /** Hien "dang soan tin" de nguoi dung biet bot da nhan tin. */
  async sendTypingOn(userId) {
    try {
      await this.#post('/oa/conversation/typing', {
        recipient: { user_id: String(userId) },
      });
    } catch (err) {
      // Chi la tin hieu UX, khong duoc lam hong luong tra loi.
      log.debug('zalo.typing.failed', { error: err.message });
    }
  }
}
