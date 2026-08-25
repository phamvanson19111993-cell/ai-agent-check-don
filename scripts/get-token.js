#!/usr/bin/env node
/**
 * Lay refresh token cua Zalo OA (chay TREN MAY CUA BAN, khong gui secret di dau).
 *
 *   node scripts/get-token.js                 # tu mo server callback o localhost
 *   node scripts/get-token.js --url-only      # chi in link uy quyen (khi callback ve server that)
 *   node scripts/get-token.js --code=XXX      # doi code da nhan thanh token
 *
 * Ket qua: ghi data/zalo-token.json va in ZALO_REFRESH_TOKEN de dan vao .env
 */
import '../src/util/loadEnv.js';
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { once } from 'node:events';
import { config } from '../src/config.js';
import { buildPermissionUrl, createPkcePair, exchangeCodeForToken } from '../src/zalo/oauth.js';
import { FileTokenStore } from '../src/zalo/tokenStore.js';

const args = Object.fromEntries(
  process.argv.slice(2).map((arg) => {
    const [key, value = 'true'] = arg.replace(/^--/, '').split('=');
    return [key, value];
  }),
);

const VERIFIER_FILE = path.join(path.dirname(config.zalo.tokenFile), '.oauth-verifier.json');
const PORT = Number(args.port || process.env.OAUTH_PORT || 3000);
const REDIRECT_URI =
  args.redirect || process.env.ZALO_REDIRECT_URI || `http://localhost:${PORT}/oauth/callback`;

function fail(message) {
  console.error(`\n✖ ${message}\n`);
  process.exit(1);
}

if (!config.zalo.appId || !config.zalo.appSecret) {
  fail('Thieu ZALO_APP_ID / ZALO_APP_SECRET. Dien vao .env truoc (xem .env.example).');
}

async function saveToken(token) {
  await new FileTokenStore(config.zalo.tokenFile).write(token);
  await fs.rm(VERIFIER_FILE, { force: true });
  console.log(`\n✔ Da luu token vao ${config.zalo.tokenFile}`);
  console.log('\nDan dong nay vao .env:\n');
  console.log(`ZALO_REFRESH_TOKEN=${token.refresh_token}\n`);
  console.log('Sau do chay: npm start');
}

async function exchange(code, codeVerifier) {
  const token = await exchangeCodeForToken({
    appId: config.zalo.appId,
    appSecret: config.zalo.appSecret,
    code,
    codeVerifier,
    oauthBase: config.zalo.oauthBase,
  });
  await saveToken(token);
  return token;
}

// --- Che do 3: doi code thu cong -------------------------------------------
if (args.code && args.code !== 'true') {
  let verifier = args.verifier;
  if (!verifier) {
    try {
      verifier = JSON.parse(await fs.readFile(VERIFIER_FILE, 'utf8')).code_verifier;
    } catch {
      fail('Khong tim thay code_verifier. Chay lai voi --verifier=<chuoi da luu>.');
    }
  }
  await exchange(args.code, verifier);
  process.exit(0);
}

const { codeVerifier, codeChallenge } = createPkcePair();
const state = crypto.randomBytes(8).toString('hex');
const permissionUrl = buildPermissionUrl({
  appId: config.zalo.appId,
  redirectUri: REDIRECT_URI,
  codeChallenge,
  state,
  oauthBase: config.zalo.oauthBase,
});

// --- Che do 2: chi in link --------------------------------------------------
if (args['url-only'] === 'true') {
  await fs.mkdir(path.dirname(VERIFIER_FILE), { recursive: true });
  await fs.writeFile(VERIFIER_FILE, JSON.stringify({ code_verifier: codeVerifier, state }, null, 2), {
    mode: 0o600,
  });
  console.log('\n1) Mo link nay bang tai khoan quan tri OA:\n');
  console.log(permissionUrl);
  console.log(`\n2) Zalo se goi ve ${REDIRECT_URI}?code=...`);
  console.log('3) Lay gia tri code roi chay:\n');
  console.log('   node scripts/get-token.js --code=<code>\n');
  process.exit(0);
}

// --- Che do 1: tu bat server callback --------------------------------------
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  if (!url.pathname.startsWith('/oauth/callback')) {
    res.writeHead(404).end('not found');
    return;
  }

  const code = url.searchParams.get('code');
  const returnedState = url.searchParams.get('state');
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });

  if (!code) {
    res.end('<h2>Thieu code trong callback. Xem log terminal.</h2>');
    console.error('\n✖ Callback khong co code:', url.search);
    server.close();
    return;
  }
  if (returnedState && returnedState !== state) {
    res.end('<h2>State khong khop — huy de an toan.</h2>');
    console.error('\n✖ State khong khop, co the bi gia mao callback.');
    server.close();
    process.exitCode = 1;
    return;
  }

  try {
    await exchange(code, codeVerifier);
    res.end('<h2>Xong! Quay lai terminal de lay refresh token.</h2>');
  } catch (err) {
    res.end(`<h2>Loi: ${err.message}</h2>`);
    console.error(`\n✖ ${err.message}`);
    process.exitCode = 1;
  }
  server.close();
});

server.listen(PORT);
await once(server, 'listening');

console.log('\n────────────────────────────────────────────────────────');
console.log('Mo link duoi day bang trinh duyet dang dang nhap tai khoan quan tri OA:\n');
console.log(permissionUrl);
console.log(`\nDang cho Zalo goi ve ${REDIRECT_URI} … (Ctrl+C de huy)`);
console.log('────────────────────────────────────────────────────────\n');
console.log(`Luu y: redirect_uri phai TRUNG KHOP voi Callback URL khai bao trong app Zalo.`);
