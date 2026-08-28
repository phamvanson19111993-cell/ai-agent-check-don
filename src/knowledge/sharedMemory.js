import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import fs from 'node:fs/promises';
import path from 'node:path';

const run = promisify(execFile);

/** Logger rong: file nay chi phu thuoc node core de phong khac copy ve dung ngay. */
const NO_LOG = { info() {}, warn() {}, error() {} };

/**
 * Doc bo nho chung (ho so san pham + luat tuan thu) TRUC TIEP tu nhanh cua
 * Tong Chi Huy, khong chep so lieu sang nhanh minh.
 *
 * Ly do: luat ghi "Moi phong lay so o day. Khong phong nao duoc tu ghi khac".
 * Chep ra ban sao la tao nguon thu hai, se lech ngay khi Phong 7 sua ho so.
 * Doc thang nen bot luon dung phien ban moi nhat da fetch ve.
 *
 * Doc that bai (chua fetch nhanh, khong co git, sai duong dan) thi tra ve null
 * — agent tu dong quay ve che do khong tra loi cau hoi san pham.
 *
 * CONG CU DUNG CHUNG (danh ba bo nho chung, muc "Trinh doc bo nho chung").
 * Chi phu thuoc node core — copy nguyen file sang phong khac la chay duoc,
 * khong keo theo bat cu thu gi cua phan Zalo. Muon co log thi truyen `logger`.
 */
export class SharedMemory {
  constructor({
    branch = 'origin/claude/dilim-ai-command-center-yy5uvo',
    files = [],
    dir = '',
    refreshMs = 15 * 60 * 1000,
    cwd = process.cwd(),
    now = () => Date.now(),
    exec = run,
    logger = NO_LOG,
  } = {}) {
    this.branch = branch;
    this.files = files;
    this.dir = dir;
    this.refreshMs = refreshMs;
    this.cwd = cwd;
    this.now = now;
    this.exec = exec;
    this.log = logger;
    this.cache = null;
  }

  /**
   * Mot muc trong `files` co hai dang:
   *   'bo-nho-chung/luat.md'            -> lay o nhanh mac dinh
   *   'origin/nhanh-khac:docs/abc.md'   -> lay o nhanh khac
   * Danh ba bo nho chung tro sang nhieu nhanh phong khac nhau nen can dang thu hai.
   */
  #resolve(entry) {
    const cut = entry.lastIndexOf(':');
    if (cut === -1) return { branch: this.branch, file: entry };
    return { branch: entry.slice(0, cut), file: entry.slice(cut + 1) };
  }

  /** Doc mot file: uu tien thu muc cuc bo neu duoc chi dinh, con lai lay tu nhanh git. */
  async #readFile(entry) {
    const { branch, file } = this.#resolve(entry);
    if (this.dir) {
      return fs.readFile(path.join(this.dir, file), 'utf8');
    }
    const { stdout } = await this.exec('git', ['show', `${branch}:${file}`], {
      cwd: this.cwd,
      maxBuffer: 4 * 1024 * 1024,
    });
    return stdout;
  }

  async load() {
    const sections = [];
    for (const file of this.files) {
      try {
        const content = await this.#readFile(file);
        if (content.trim()) sections.push({ file, content: content.trim() });
      } catch (err) {
        this.log.warn('knowledge.file_unavailable', { file, error: err.message });
      }
    }

    if (!sections.length) {
      this.log.warn('knowledge.empty', { branch: this.branch, files: this.files.length });
      return null;
    }

    const text = sections
      .map(({ file, content }) => `### Nguồn: ${file}\n\n${content}`)
      .join('\n\n---\n\n');

    this.log.info('knowledge.loaded', { files: sections.map((s) => s.file), chars: text.length });
    return { text, sources: sections.map((s) => s.file), loadedAt: this.now() };
  }

  /** Ban ghi nho, tu doc lai sau refreshMs de bat kip khi Tong Chi Huy sua ho so. */
  async get() {
    if (this.cache && this.now() - this.cache.loadedAt < this.refreshMs) {
      return this.cache;
    }
    const loaded = await this.load();
    // Doc that bai thi giu ban cu con dung duoc, hon la mat kien thuc giua chung.
    if (loaded) this.cache = loaded;
    return this.cache;
  }
}
