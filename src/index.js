import './util/loadEnv.js';
import Anthropic from '@anthropic-ai/sdk';
import { config } from './config.js';
import { log } from './util/log.js';
import { createOrderProvider } from './orders/index.js';
import { SessionStore } from './store/sessions.js';
import { OrderAgent } from './agent/agent.js';
import { SharedMemory } from './knowledge/sharedMemory.js';
import { FallbackOrderAgent } from './agent/fallbackAgent.js';
import { ZaloClient } from './zalo/client.js';
import { FileTokenStore } from './zalo/tokenStore.js';
import { createWebhookHandler } from './zalo/webhook.js';
import { createServer } from './server.js';

function assertConfigured() {
  const missing = [];
  if (!config.zalo.appId) missing.push('ZALO_APP_ID');
  if (!config.zalo.appSecret) missing.push('ZALO_APP_SECRET');
  if (!config.zalo.refreshToken) missing.push('ZALO_REFRESH_TOKEN');
  if (missing.length) {
    log.error('config.missing', { missing });
    log.error('config.hint', {
      detail: 'Sao chep .env.example thanh .env va dien thong tin OA truoc khi chay.',
    });
    process.exit(1);
  }
}

function main() {
  assertConfigured();

  const orders = createOrderProvider(config.orders);
  const sessions = new SessionStore(config.session);
  const fallbackAgent = new FallbackOrderAgent({ orders });

  const knowledge = config.knowledge.enabled ? new SharedMemory(config.knowledge) : null;

  let agent = null;
  if (config.claude.enabled) {
    agent = new OrderAgent({
      client: new Anthropic(),
      orders,
      sessions,
      model: config.claude.model,
      effort: config.claude.effort,
      maxTokens: config.claude.maxTokens,
      maxToolTurns: config.claude.maxToolTurns,
      knowledge,
      onEscalate: async ({ userId, reason, orderCode }) => {
        // TODO: noi vao he thong ticket / thong bao nhom CSKH cua ban.
        log.warn('cskh.handoff', { userId, reason, orderCode });
      },
    });
  } else {
    log.warn('claude.disabled', {
      detail: 'Chua co ANTHROPIC_API_KEY — bot chay che do tra cuu bang regex.',
    });
  }

  const zalo = new ZaloClient({
    appId: config.zalo.appId,
    appSecret: config.zalo.appSecret,
    refreshToken: config.zalo.refreshToken,
    tokenStore: new FileTokenStore(config.zalo.tokenFile),
    oauthBase: config.zalo.oauthBase,
    apiBase: config.zalo.apiBase,
  });

  const handler = createWebhookHandler({ config, agent, fallbackAgent, zalo });
  const server = createServer({ handler });

  const pruneTimer = setInterval(() => sessions.prune(), 5 * 60 * 1000);
  pruneTimer.unref();

  // Nap truoc de biet ngay luc khoi dong la co doc duoc ho so hay khong.
  knowledge?.get().then((loaded) => {
    if (!loaded) {
      log.warn('knowledge.unavailable', {
        detail: 'Khong doc duoc bo nho chung — bot se khong tra loi cau hoi san pham.',
        branch: config.knowledge.branch,
      });
    }
  });

  server.listen(config.port, () => {
    log.info('server.listening', {
      port: config.port,
      orderProvider: config.orders.provider,
      claude: config.claude.enabled ? config.claude.model : 'disabled',
    });
  });

  for (const signal of ['SIGINT', 'SIGTERM']) {
    process.on(signal, () => {
      log.info('server.shutdown', { signal });
      server.close(() => process.exit(0));
    });
  }
}

main();
