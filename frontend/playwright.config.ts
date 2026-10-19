import { defineConfig } from '@playwright/test';
import path from 'node:path';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  workers: 1,
  webServer: {
    command: '".venv/Scripts/python.exe" -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001',
    cwd: path.resolve('..'), url: 'http://127.0.0.1:8001/api/health',
    reuseExistingServer: false,
    env: { DATA_DIR: path.resolve('..', '.runtime', `browser-data-${Date.now()}`),
      OPENAI_API_KEY: '', VECTOR_BACKEND: 'local', EMBEDDING_MODE: 'hash', RERANKER: 'lexical' },
  },
  use: {
    baseURL: 'http://127.0.0.1:8001',
    viewport: { width: 1440, height: 1000 },
    channel: 'msedge',
    headless: true,
    screenshot: 'only-on-failure',
  },
});
