#!/usr/bin/env node
/**
 * Chat thu voi agent ngay tren terminal, khong can Zalo:
 *   node scripts/chat.js
 * Huu ich de chinh prompt va kiem tra logic tra cuu truoc khi deploy.
 */
import readline from 'node:readline/promises';
import { stdin, stdout } from 'node:process';
import Anthropic from '@anthropic-ai/sdk';
import { config } from '../src/config.js';
import { createOrderProvider } from '../src/orders/index.js';
import { SessionStore } from '../src/store/sessions.js';
import { OrderAgent } from '../src/agent/agent.js';
import { FallbackOrderAgent } from '../src/agent/fallbackAgent.js';

const orders = createOrderProvider(config.orders);
const sessions = new SessionStore(config.session);
const agent = config.claude.enabled
  ? new OrderAgent({
      client: new Anthropic(),
      orders,
      sessions,
      model: config.claude.model,
      effort: config.claude.effort,
      maxTokens: config.claude.maxTokens,
      maxToolTurns: config.claude.maxToolTurns,
    })
  : new FallbackOrderAgent({ orders });

if (!config.claude.enabled) {
  console.log('[!] Chua co ANTHROPIC_API_KEY — dang chay che do regex.\n');
}

const rl = readline.createInterface({ input: stdin, output: stdout });
const userId = 'cli-user';

console.log('Go tin nhan cua khach (Ctrl+C de thoat).\n');
for (;;) {
  const text = (await rl.question('Khach: ')).trim();
  if (!text) continue;
  try {
    const answer = await agent.reply({ userId, text });
    console.log(`\nBot: ${answer.text}\n`);
  } catch (err) {
    console.error(`\n[loi] ${err.message}\n`);
  }
}
