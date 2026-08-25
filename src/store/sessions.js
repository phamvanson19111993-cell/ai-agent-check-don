/**
 * Luu lich su hoi thoai theo tung user Zalo. Bo nho trong tien cho 1 instance;
 * neu chay nhieu instance hoac can ben vung sau restart thi thay bang Redis
 * (chi can giu nguyen 4 method duoi day).
 */
export class SessionStore {
  constructor({ maxTurns = 12, ttlMs = 30 * 60 * 1000, now = () => Date.now() } = {}) {
    this.maxMessages = maxTurns * 2;
    this.ttlMs = ttlMs;
    this.now = now;
    this.sessions = new Map();
  }

  get(userId) {
    const entry = this.sessions.get(userId);
    if (!entry) return [];
    if (this.now() - entry.updatedAt > this.ttlMs) {
      this.sessions.delete(userId);
      return [];
    }
    return entry.messages;
  }

  set(userId, messages) {
    this.sessions.set(userId, {
      messages: trim(messages, this.maxMessages),
      updatedAt: this.now(),
    });
  }

  reset(userId) {
    this.sessions.delete(userId);
  }

  prune() {
    const cutoff = this.now() - this.ttlMs;
    for (const [userId, entry] of this.sessions) {
      if (entry.updatedAt < cutoff) this.sessions.delete(userId);
    }
  }
}

/**
 * Cat bot luot cu. Phai cat sao cho tin dau tien la mot luot `user` that su —
 * neu cat trung vao khoi tool_result thi API se bao loi thieu tool_use tuong ung.
 */
function trim(messages, maxMessages) {
  if (messages.length <= maxMessages) return messages;
  let start = messages.length - maxMessages;
  while (start < messages.length && !isPlainUserTurn(messages[start])) start += 1;
  return messages.slice(start);
}

function isPlainUserTurn(message) {
  if (message.role !== 'user') return false;
  if (typeof message.content === 'string') return true;
  return !message.content.some((block) => block.type === 'tool_result');
}
