import http from 'node:http';
import { log } from './util/log.js';

const MAX_BODY_BYTES = 1024 * 1024;

function readRawBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new Error('body_too_large'));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function json(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(body),
  });
  res.end(body);
}

export function createServer({ handler, webhookPath = '/webhook' }) {
  return http.createServer(async (req, res) => {
    const url = new URL(req.url, 'http://localhost');

    if (req.method === 'GET' && url.pathname === '/health') {
      return json(res, 200, { status: 'ok', uptime: process.uptime() });
    }

    // Zalo goi GET khi ban bam "Kiem tra" URL webhook trong OA Console.
    if (req.method === 'GET' && url.pathname === webhookPath) {
      return json(res, 200, { status: 'ok' });
    }

    if (req.method === 'POST' && url.pathname === webhookPath) {
      let rawBody;
      try {
        rawBody = await readRawBody(req);
      } catch (err) {
        return json(res, 413, { error: err.message });
      }

      const parsed = handler.verifyAndParse({
        rawBody,
        signature: req.headers['x-zevent-signature'],
      });
      if (!parsed.ok) {
        log.warn('webhook.rejected', { reason: parsed.reason });
        return json(res, parsed.status, { error: parsed.reason });
      }

      // Tra 200 ngay: Zalo timeout nhanh va se gui lai event neu cho lau.
      json(res, 200, { status: 'ok' });
      handler.processEvent(parsed.event).catch((err) => {
        log.error('webhook.process_failed', { error: err.message, stack: err.stack });
      });
      return undefined;
    }

    return json(res, 404, { error: 'not_found' });
  });
}
