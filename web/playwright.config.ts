import { defineConfig, devices } from '@playwright/test';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const raiz = resolve(import.meta.dirname, '..');
const temporario = mkdtempSync(join(tmpdir(), 'anamnese-e2e-'));
export default defineConfig({
  testDir: './e2e', fullyParallel: false, workers: 1, timeout: 90_000,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: { baseURL: 'http://127.0.0.1:8000', trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } } }],
  webServer: {
    command: `"${join(raiz, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python')}" -m uvicorn api.main:app --host 127.0.0.1 --port 8000`,
    cwd: raiz, url: 'http://127.0.0.1:8000/api/saude', reuseExistingServer: false,
    env: { ANAMNESE_DB: join(temporario, 'anamnese.db'), ANAMNESE_BASE_DIR: join(raiz, 'base') },
    timeout: 30_000,
  },
});
