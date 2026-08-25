import { verifySignature } from './signature.js';
import { log } from '../util/log.js';

const GREETING =
  'Cảm ơn anh/chị đã quan tâm shop! Anh/chị gửi mã đơn hàng hoặc số điện thoại đặt hàng, shop kiểm tra tình trạng đơn ngay ạ.';
const UNSUPPORTED_ATTACHMENT =
  'Shop mới nhận được file/ảnh của anh/chị. Anh/chị gõ giúp shop mã đơn hàng hoặc số điện thoại đặt hàng để shop tra cứu ạ.';
const ERROR_REPLY =
  'Hệ thống shop đang bận, anh/chị vui lòng gửi lại tin sau ít phút giúp shop ạ.';

/** Zalo gui lai webhook khi khong nhan duoc 200 — chan trung theo msg_id. */
export class Deduper {
  constructor({ ttlMs = 10 * 60 * 1000, now = () => Date.now() } = {}) {
    this.ttlMs = ttlMs;
    this.now = now;
    this.seen = new Map();
  }

  seenBefore(id) {
    if (!id) return false;
    const cutoff = this.now() - this.ttlMs;
    for (const [key, ts] of this.seen) {
      if (ts < cutoff) this.seen.delete(key);
    }
    if (this.seen.has(id)) return true;
    this.seen.set(id, this.now());
    return false;
  }
}

export function createWebhookHandler({ config, agent, fallbackAgent, zalo, deduper = new Deduper() }) {
  /**
   * Xu ly mot event webhook. Ham nay chay SAU khi da tra 200 cho Zalo,
   * nen moi loi deu phai duoc bat tai day.
   */
  async function processEvent(event) {
    const userId = event.sender?.id;
    if (!userId) return { skipped: 'no_sender' };

    switch (event.event_name) {
      case 'follow':
        await zalo.sendText(userId, GREETING);
        return { handled: 'follow' };

      case 'user_send_text': {
        const text = event.message?.text?.trim();
        if (!text) return { skipped: 'empty_text' };
        if (deduper.seenBefore(event.message?.msg_id)) return { skipped: 'duplicate' };

        await zalo.sendTypingOn(userId);
        const answer = await replyWithFallback({ userId, text });
        await zalo.sendText(userId, answer.text);
        log.info('zalo.replied', {
          userId,
          escalated: Boolean(answer.escalated),
          fallback: Boolean(answer.fallback),
        });
        return { handled: 'user_send_text', answer };
      }

      case 'user_send_image':
      case 'user_send_file':
      case 'user_send_sticker':
        if (deduper.seenBefore(event.message?.msg_id)) return { skipped: 'duplicate' };
        await zalo.sendText(userId, UNSUPPORTED_ATTACHMENT);
        return { handled: 'attachment' };

      default:
        log.debug('zalo.event.ignored', { event: event.event_name });
        return { skipped: 'unsupported_event' };
    }
  }

  async function replyWithFallback({ userId, text }) {
    if (agent) {
      try {
        return await agent.reply({ userId, text });
      } catch (err) {
        log.error('agent.failed', { userId, error: err.message });
      }
    }
    try {
      return await fallbackAgent.reply({ userId, text });
    } catch (err) {
      log.error('fallback.failed', { userId, error: err.message });
      return { text: ERROR_REPLY, escalated: true };
    }
  }

  /**
   * Kiem tra chu ky + parse body. Tra ve { ok, status, event } de lop HTTP
   * quyet dinh ma tra ve; luon nen tra 200 that nhanh roi xu ly bat dong bo.
   */
  function verifyAndParse({ rawBody, signature }) {
    let event;
    try {
      event = JSON.parse(rawBody);
    } catch {
      return { ok: false, status: 400, reason: 'invalid_json' };
    }

    if (config.zalo.verifySignature) {
      const valid = verifySignature({
        header: signature,
        appId: config.zalo.appId,
        rawBody,
        timestamp: event.timestamp,
        oaSecretKey: config.zalo.oaSecretKey,
      });
      if (!valid) return { ok: false, status: 401, reason: 'invalid_signature' };
    }

    return { ok: true, status: 200, event };
  }

  return { processEvent, verifyAndParse, replyWithFallback };
}

export { GREETING, UNSUPPORTED_ATTACHMENT, ERROR_REPLY };
