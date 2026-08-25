import fs from 'node:fs/promises';
import path from 'node:path';

/**
 * Refresh token cua Zalo OA chi dung duoc MOT lan: moi lan lam moi access token
 * se tra ve refresh token moi va vo hieu cai cu. Vi vay bat buoc phai luu lai,
 * neu khong sau 25 gio bot se mat quyen gui tin.
 */
export class FileTokenStore {
  constructor(filePath) {
    this.filePath = filePath;
  }

  async read() {
    try {
      const raw = await fs.readFile(this.filePath, 'utf8');
      return JSON.parse(raw);
    } catch (err) {
      if (err.code === 'ENOENT') return null;
      throw err;
    }
  }

  async write(data) {
    await fs.mkdir(path.dirname(this.filePath), { recursive: true });
    const tmp = `${this.filePath}.tmp`;
    await fs.writeFile(tmp, JSON.stringify(data, null, 2), { mode: 0o600 });
    await fs.rename(tmp, this.filePath);
  }
}

/** Dung cho test hoac khi chay nhieu instance va da co store rieng. */
export class MemoryTokenStore {
  constructor(initial = null) {
    this.data = initial;
  }

  async read() {
    return this.data;
  }

  async write(data) {
    this.data = data;
  }
}
