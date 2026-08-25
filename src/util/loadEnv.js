import fs from 'node:fs';

/**
 * Nap file .env vao process.env. Import module NAY TRUOC config.js
 * (ESM chay import theo thu tu khai bao) de config doc duoc gia tri moi.
 */
const envPath = process.env.ENV_FILE || '.env';

if (fs.existsSync(envPath) && typeof process.loadEnvFile === 'function') {
  process.loadEnvFile(envPath);
}

export default envPath;
