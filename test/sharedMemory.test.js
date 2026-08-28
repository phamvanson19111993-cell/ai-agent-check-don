import test from 'node:test';
import assert from 'node:assert/strict';
import { SharedMemory } from '../src/knowledge/sharedMemory.js';
import { buildSystemPrompt } from '../src/agent/prompt.js';

function fakeExec(map) {
  const calls = [];
  return {
    calls,
    exec: async (cmd, args) => {
      calls.push({ cmd, args });
      const ref = args[1];
      if (!(ref in map)) throw new Error(`fatal: path not found: ${ref}`);
      return { stdout: map[ref] };
    },
  };
}

test('doc file tu nhanh Tong Chi Huy bang git show, khong chep sang nhanh minh', async () => {
  const { exec, calls } = fakeExec({
    'origin/cmd:san-pham.md': '# Giá\n1 hộp 2.890.000đ',
    'origin/cmd:luat.md': '# Luật\nKhông nói chữa bệnh',
  });
  const memory = new SharedMemory({
    branch: 'origin/cmd',
    files: ['san-pham.md', 'luat.md'],
    exec,
  });

  const loaded = await memory.load();
  assert.deepEqual(calls.map((c) => c.args), [
    ['show', 'origin/cmd:san-pham.md'],
    ['show', 'origin/cmd:luat.md'],
  ]);
  assert.match(loaded.text, /2\.890\.000đ/);
  assert.match(loaded.text, /Không nói chữa bệnh/);
  assert.deepEqual(loaded.sources, ['san-pham.md', 'luat.md']);
});

test('thieu mot file thi van dung duoc phan doc duoc', async () => {
  const { exec } = fakeExec({ 'origin/cmd:san-pham.md': 'noi dung' });
  const memory = new SharedMemory({
    branch: 'origin/cmd',
    files: ['san-pham.md', 'khong-ton-tai.md'],
    exec,
  });

  const loaded = await memory.load();
  assert.deepEqual(loaded.sources, ['san-pham.md']);
});

test('khong doc duoc file nao thi tra null', async () => {
  const { exec } = fakeExec({});
  const memory = new SharedMemory({ branch: 'origin/cmd', files: ['a.md'], exec });
  assert.equal(await memory.load(), null);
});

test('get() dung cache trong refreshMs roi doc lai khi het han', async () => {
  let now = 0;
  const { exec, calls } = fakeExec({ 'origin/cmd:a.md': 'v1' });
  const memory = new SharedMemory({
    branch: 'origin/cmd',
    files: ['a.md'],
    refreshMs: 1000,
    now: () => now,
    exec,
  });

  await memory.get();
  await memory.get();
  assert.equal(calls.length, 1, 'lan thu hai phai lay tu cache');
  now = 1500;
  await memory.get();
  assert.equal(calls.length, 2, 'het han thi doc lai');
});

test('doc lai that bai thi giu ban cu, khong mat kien thuc giua chung', async () => {
  let now = 0;
  let failing = false;
  const memory = new SharedMemory({
    branch: 'origin/cmd',
    files: ['a.md'],
    refreshMs: 1000,
    now: () => now,
    exec: async () => {
      if (failing) throw new Error('git khong chay duoc');
      return { stdout: 'noi dung goc' };
    },
  });

  await memory.get();
  now = 5000;
  failing = true;
  const after = await memory.get();
  assert.match(after.text, /noi dung goc/);
});

test('co ho so thi prompt cho phep tu van san pham va tach block de cache', () => {
  const blocks = buildSystemPrompt({ text: 'HO SO: gia 2.890.000d' });
  assert.equal(blocks.length, 2);
  assert.match(blocks[0].text, /chỉ được dùng HỒ SƠ CHUẨN/);
  assert.match(blocks[0].text, /không phải là thuốc/);
  assert.match(blocks[1].text, /HO SO: gia 2\.890\.000d/);
  assert.deepEqual(blocks[1].cache_control, { type: 'ephemeral' });
});

test('khong co ho so thi prompt cam tra loi cau hoi san pham', () => {
  const blocks = buildSystemPrompt(null);
  assert.equal(blocks.length, 1);
  assert.match(blocks[0].text, /KHÔNG tự trả lời/);
  assert.match(blocks[0].text, /escalate_to_human/);
  assert.doesNotMatch(blocks[0].text, /HỒ SƠ CHUẨN/);
});

test('la cong cu dung chung: chi import node core, chay duoc khi khong truyen logger', async () => {
  const source = await import('node:fs/promises').then((fs) =>
    fs.readFile('src/knowledge/sharedMemory.js', 'utf8'),
  );
  const imports = [...source.matchAll(/^import .* from '([^']+)';$/gm)].map((m) => m[1]);
  assert.deepEqual(
    imports.filter((mod) => !mod.startsWith('node:')),
    [],
    'khong duoc phu thuoc file nao cua du an — phong khac phai copy nguyen file la chay',
  );

  // Khong truyen logger van chay binh thuong, khong nem loi.
  const memory = new SharedMemory({
    branch: 'origin/cmd',
    files: ['a.md'],
    exec: async () => {
      throw new Error('khong co nhanh');
    },
  });
  assert.equal(await memory.load(), null);
});

test('doc duoc file o nhanh khac khi muc ghi dang "nhanh:duong-dan"', async () => {
  const { exec, calls } = fakeExec({
    'origin/cmd:bo-nho-chung/luat.md': 'luat chung',
    'origin/phong-cskh:docs/thu-vien.md': 'thu vien tin nhan',
  });
  const memory = new SharedMemory({
    branch: 'origin/cmd',
    files: ['bo-nho-chung/luat.md', 'origin/phong-cskh:docs/thu-vien.md'],
    exec,
  });

  const loaded = await memory.load();
  assert.deepEqual(calls.map((c) => c.args[1]), [
    'origin/cmd:bo-nho-chung/luat.md',
    'origin/phong-cskh:docs/thu-vien.md',
  ]);
  assert.match(loaded.text, /luat chung/);
  assert.match(loaded.text, /thu vien tin nhan/);
});
