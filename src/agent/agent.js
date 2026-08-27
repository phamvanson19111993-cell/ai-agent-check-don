import { buildSystemPrompt, TOOLS } from './prompt.js';
import { createToolRunner } from './tools.js';
import { log } from '../util/log.js';

const HANDOFF_MESSAGE =
  'Shop chưa xử lý được yêu cầu này ngay. Anh/chị để lại mã đơn hoặc số điện thoại, nhân viên sẽ liên hệ hỗ trợ trong thời gian sớm nhất ạ.';

/**
 * Agent tra cuu don hang: Claude quyet dinh khi nao goi cong cu, code o day
 * chay cong cu va lap lai cho den khi model tra loi bang van ban.
 */
export class OrderAgent {
  constructor({
    client,
    orders,
    sessions,
    model = 'claude-opus-5',
    effort = 'low',
    maxTokens = 16000,
    maxToolTurns = 6,
    onEscalate,
    knowledge = null,
  }) {
    this.client = client;
    this.knowledge = knowledge;
    this.sessions = sessions;
    this.model = model;
    this.effort = effort;
    this.maxTokens = maxTokens;
    this.maxToolTurns = maxToolTurns;
    this.toolRunner = createToolRunner({ orders, onEscalate });
  }

  async reply({ userId, text }) {
    const messages = [...this.sessions.get(userId), { role: 'user', content: text }];
    let escalated = false;
    // Doc that bai thi buildSystemPrompt tu lui ve che do chi tra don hang.
    const system = buildSystemPrompt(await this.#loadKnowledge());

    for (let turn = 0; turn < this.maxToolTurns; turn += 1) {
      const response = await this.client.beta.messages.create({
        model: this.model,
        max_tokens: this.maxTokens,
        system,
        tools: TOOLS,
        thinking: { type: 'adaptive' },
        output_config: { effort: this.effort },
        // Bo phan loai an toan co the tu choi tra loi; fallback phia server se
        // dinh tuyen sang model khac thay vi tra ve tin nhan rong cho khach.
        betas: ['server-side-fallback-2026-07-01'],
        fallbacks: 'default',
        cache_control: { type: 'ephemeral' },
        messages,
      });

      if (response.stop_reason === 'refusal') {
        log.warn('agent.refusal', { userId, category: response.stop_details?.category });
        this.sessions.reset(userId);
        return { text: HANDOFF_MESSAGE, escalated: true, refused: true };
      }

      messages.push({ role: 'assistant', content: response.content });

      if (response.stop_reason !== 'tool_use') {
        const reply = textOf(response.content) || HANDOFF_MESSAGE;
        this.sessions.set(userId, messages);
        return { text: reply, escalated, usage: response.usage };
      }

      const toolUses = response.content.filter((block) => block.type === 'tool_use');
      // Chay song song roi tra TAT CA tool_result trong MOT tin nhan user duy nhat.
      const results = await Promise.all(
        toolUses.map((block) => this.#runTool(block, { userId })),
      );
      if (toolUses.some((block) => block.name === 'escalate_to_human')) escalated = true;
      messages.push({ role: 'user', content: results });
    }

    log.warn('agent.tool_turns_exhausted', { userId });
    this.sessions.set(userId, messages);
    return { text: HANDOFF_MESSAGE, escalated: true };
  }

  async #loadKnowledge() {
    if (!this.knowledge) return null;
    try {
      return await this.knowledge.get();
    } catch (err) {
      log.error('knowledge.load_failed', { error: err.message });
      return null;
    }
  }

  async #runTool(block, context) {
    const handler = this.toolRunner[block.name];
    if (!handler) {
      return {
        type: 'tool_result',
        tool_use_id: block.id,
        is_error: true,
        content: `Cong cu khong ton tai: ${block.name}`,
      };
    }
    try {
      const result = await handler(block.input, context);
      return {
        type: 'tool_result',
        tool_use_id: block.id,
        content: JSON.stringify(result),
      };
    } catch (err) {
      log.error('agent.tool_failed', { tool: block.name, error: err.message });
      return {
        type: 'tool_result',
        tool_use_id: block.id,
        is_error: true,
        content: `Loi khi goi ${block.name}: ${err.message}`,
      };
    }
  }
}

function textOf(content) {
  return content
    .filter((block) => block.type === 'text')
    .map((block) => block.text)
    .join('\n')
    .trim();
}

export { HANDOFF_MESSAGE };
