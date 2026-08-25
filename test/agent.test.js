import test from 'node:test';
import assert from 'node:assert/strict';
import { OrderAgent, HANDOFF_MESSAGE } from '../src/agent/agent.js';
import { SessionStore } from '../src/store/sessions.js';
import { MockOrderProvider } from '../src/orders/mockProvider.js';

/** Client Anthropic gia: tra lan luot cac response da dinh san. */
function fakeClient(responses) {
  const requests = [];
  return {
    requests,
    beta: {
      messages: {
        create: async (params) => {
          // Chup lai mang messages: agent tiep tuc push vao chinh mang nay.
          requests.push({ ...params, messages: [...params.messages] });
          const next = responses[requests.length - 1];
          if (!next) throw new Error('Khong con response gia nao');
          return next;
        },
      },
    },
  };
}

const orders = new MockOrderProvider('./data/orders.json');

function makeAgent(client, extra = {}) {
  return new OrderAgent({
    client,
    orders,
    sessions: new SessionStore({ maxTurns: 4 }),
    ...extra,
  });
}

test('tra loi thang khi model khong goi cong cu', async () => {
  const client = fakeClient([
    {
      stop_reason: 'end_turn',
      content: [{ type: 'text', text: 'Anh/chị cho shop xin mã đơn ạ.' }],
      usage: { input_tokens: 10, output_tokens: 5 },
    },
  ]);
  const agent = makeAgent(client);

  const answer = await agent.reply({ userId: 'u1', text: 'shop oi' });
  assert.equal(answer.text, 'Anh/chị cho shop xin mã đơn ạ.');
  assert.equal(answer.escalated, false);
  assert.equal(client.requests[0].model, 'claude-opus-5');
  assert.deepEqual(client.requests[0].thinking, { type: 'adaptive' });
  assert.deepEqual(client.requests[0].output_config, { effort: 'low' });
  assert.deepEqual(client.requests[0].tools.map((t) => t.name), [
    'lookup_order',
    'find_orders_by_phone',
    'escalate_to_human',
  ]);
});

test('chay lookup_order va gui ket qua ve model', async () => {
  const client = fakeClient([
    {
      stop_reason: 'tool_use',
      content: [
        { type: 'tool_use', id: 'tu_1', name: 'lookup_order', input: { order_code: 'DH123456' } },
      ],
    },
    {
      stop_reason: 'end_turn',
      content: [{ type: 'text', text: 'Đơn DH123456 đang giao ạ.' }],
      usage: {},
    },
  ]);
  const agent = makeAgent(client);

  const answer = await agent.reply({ userId: 'u1', text: 'don DH123456 sao roi' });
  assert.equal(answer.text, 'Đơn DH123456 đang giao ạ.');

  const followUp = client.requests[1].messages.at(-1);
  assert.equal(followUp.role, 'user');
  const result = followUp.content[0];
  assert.equal(result.type, 'tool_result');
  assert.equal(result.tool_use_id, 'tu_1');
  const payload = JSON.parse(result.content);
  assert.equal(payload.found, true);
  assert.equal(payload.order.status, 'shipping');
  assert.equal(payload.order.trackingCode, 'GHN889231');
});

test('bao found=false khi khong tim thay don, khong nem loi', async () => {
  const client = fakeClient([
    {
      stop_reason: 'tool_use',
      content: [
        { type: 'tool_use', id: 'tu_1', name: 'lookup_order', input: { order_code: 'DH000000' } },
      ],
    },
    { stop_reason: 'end_turn', content: [{ type: 'text', text: 'Shop không tìm thấy đơn ạ.' }] },
  ]);
  const agent = makeAgent(client);

  await agent.reply({ userId: 'u1', text: 'DH000000' });
  const payload = JSON.parse(client.requests[1].messages.at(-1).content[0].content);
  assert.deepEqual(payload, { found: false, order_code: 'DH000000' });
});

test('escalate_to_human danh dau escalated va goi callback', async () => {
  const escalations = [];
  const client = fakeClient([
    {
      stop_reason: 'tool_use',
      content: [
        {
          type: 'tool_use',
          id: 'tu_1',
          name: 'escalate_to_human',
          input: { reason: 'khach doi hoan tien', order_code: 'DH123456' },
        },
      ],
    },
    { stop_reason: 'end_turn', content: [{ type: 'text', text: 'Shop chuyển nhân viên hỗ trợ ạ.' }] },
  ]);
  const agent = makeAgent(client, { onEscalate: async (info) => escalations.push(info) });

  const answer = await agent.reply({ userId: 'u9', text: 'toi muon hoan tien' });
  assert.equal(answer.escalated, true);
  assert.deepEqual(escalations, [
    { userId: 'u9', reason: 'khach doi hoan tien', orderCode: 'DH123456' },
  ]);
});

test('loi cong cu tra ve tool_result is_error thay vi lam sap luot chat', async () => {
  const brokenOrders = {
    getOrder: async () => {
      throw new Error('API don hang timeout');
    },
    findOrdersByPhone: async () => [],
  };
  const client = fakeClient([
    {
      stop_reason: 'tool_use',
      content: [
        { type: 'tool_use', id: 'tu_1', name: 'lookup_order', input: { order_code: 'DH1' } },
      ],
    },
    { stop_reason: 'end_turn', content: [{ type: 'text', text: 'Shop đang kiểm tra lại ạ.' }] },
  ]);
  const agent = new OrderAgent({
    client,
    orders: brokenOrders,
    sessions: new SessionStore({ maxTurns: 4 }),
  });

  const answer = await agent.reply({ userId: 'u1', text: 'DH1' });
  const result = client.requests[1].messages.at(-1).content[0];
  assert.equal(result.is_error, true);
  assert.match(result.content, /API don hang timeout/);
  assert.equal(answer.text, 'Shop đang kiểm tra lại ạ.');
});

test('stop_reason refusal tra ve tin nhan chuyen nhan vien', async () => {
  const client = fakeClient([
    { stop_reason: 'refusal', stop_details: { category: 'cyber' }, content: [] },
  ]);
  const agent = makeAgent(client);

  const answer = await agent.reply({ userId: 'u1', text: 'noi dung bi tu choi' });
  assert.equal(answer.text, HANDOFF_MESSAGE);
  assert.equal(answer.refused, true);
});

test('dung lai khi vuot so luot goi cong cu toi da', async () => {
  const toolTurn = {
    stop_reason: 'tool_use',
    content: [{ type: 'tool_use', id: 'tu', name: 'lookup_order', input: { order_code: 'DH1' } }],
  };
  const client = fakeClient([toolTurn, toolTurn]);
  const agent = makeAgent(client, { maxToolTurns: 2 });

  const answer = await agent.reply({ userId: 'u1', text: 'DH1' });
  assert.equal(answer.text, HANDOFF_MESSAGE);
  assert.equal(client.requests.length, 2);
});

test('luu lich su de luot sau van co ngu canh', async () => {
  const client = fakeClient([
    { stop_reason: 'end_turn', content: [{ type: 'text', text: 'Dạ anh/chị cho xin mã đơn ạ.' }] },
    { stop_reason: 'end_turn', content: [{ type: 'text', text: 'Shop kiểm tra ngay ạ.' }] },
  ]);
  const agent = makeAgent(client);

  await agent.reply({ userId: 'u1', text: 'shop oi' });
  await agent.reply({ userId: 'u1', text: 'DH123456' });

  assert.deepEqual(
    client.requests[1].messages.map((m) => m.role),
    ['user', 'assistant', 'user'],
  );
});
