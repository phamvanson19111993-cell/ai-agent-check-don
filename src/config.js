import process from 'node:process';

/**
 * Doc cau hinh tu bien moi truong. Khong throw o day de test/CLI van chay duoc
 * khi thieu credential — cac module tu kiem tra phan minh can.
 */
function bool(value, fallback = false) {
  if (value === undefined || value === '') return fallback;
  return ['1', 'true', 'yes', 'on'].includes(String(value).toLowerCase());
}

function int(value, fallback) {
  const n = Number.parseInt(value ?? '', 10);
  return Number.isFinite(n) ? n : fallback;
}

export function loadConfig(env = process.env) {
  return {
    port: int(env.PORT, 3000),
    logLevel: env.LOG_LEVEL || 'info',
    zalo: {
      appId: env.ZALO_APP_ID || '',
      appSecret: env.ZALO_APP_SECRET || '',
      oaSecretKey: env.ZALO_OA_SECRET_KEY || env.ZALO_APP_SECRET || '',
      refreshToken: env.ZALO_REFRESH_TOKEN || '',
      tokenFile: env.ZALO_TOKEN_FILE || './data/zalo-token.json',
      oauthBase: env.ZALO_OAUTH_BASE || 'https://oauth.zaloapp.com/v4',
      apiBase: env.ZALO_API_BASE || 'https://openapi.zalo.me/v3.0',
      verifySignature: bool(env.ZALO_VERIFY_SIGNATURE, true),
    },
    claude: {
      // SDK tu doc ANTHROPIC_API_KEY; chi dung co o day de biet nen bat agent hay khong.
      enabled: bool(env.CLAUDE_ENABLED, Boolean(env.ANTHROPIC_API_KEY)),
      model: env.CLAUDE_MODEL || 'claude-opus-5',
      // low = tra loi nhanh cho chat CSKH; nang len medium/high neu can suy luan sau hon.
      effort: env.CLAUDE_EFFORT || 'low',
      maxTokens: int(env.CLAUDE_MAX_TOKENS, 16000),
      maxToolTurns: int(env.CLAUDE_MAX_TOOL_TURNS, 6),
    },
    orders: {
      provider: env.ORDER_PROVIDER || 'mock',
      mockFile: env.ORDER_MOCK_FILE || './data/orders.json',
      httpBaseUrl: env.ORDER_API_BASE_URL || '',
      httpApiKey: env.ORDER_API_KEY || '',
      httpTimeoutMs: int(env.ORDER_API_TIMEOUT_MS, 8000),
    },
    session: {
      maxTurns: int(env.SESSION_MAX_TURNS, 12),
      ttlMs: int(env.SESSION_TTL_MS, 30 * 60 * 1000),
    },
  };
}

export const config = loadConfig();
