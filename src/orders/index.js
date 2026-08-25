import { MockOrderProvider } from './mockProvider.js';
import { HttpOrderProvider } from './httpProvider.js';

export function createOrderProvider(ordersConfig) {
  switch (ordersConfig.provider) {
    case 'http':
      return new HttpOrderProvider({
        baseUrl: ordersConfig.httpBaseUrl,
        apiKey: ordersConfig.httpApiKey,
        timeoutMs: ordersConfig.httpTimeoutMs,
      });
    case 'mock':
      return new MockOrderProvider(ordersConfig.mockFile);
    default:
      throw new Error(`ORDER_PROVIDER khong hop le: ${ordersConfig.provider}`);
  }
}

export { MockOrderProvider, HttpOrderProvider };
