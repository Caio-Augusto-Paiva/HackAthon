// @vitest-environment node
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { expect, it } from 'vitest';

it.skipIf(process.platform !== 'win32')('prepara o frontend ausente uma vez e preserva um build existente', () => {
  const raiz = mkdtempSync(join(tmpdir(), 'anamnese-inicializacao-'));
  for (const pasta of ['scripts', '.venv/Scripts', 'web', 'comandos']) mkdirSync(join(raiz, pasta), { recursive: true });
  copyFileSync(resolve(import.meta.dirname, '../../../scripts/rodar.ps1'), join(raiz, 'scripts/rodar.ps1'));
  writeFileSync(join(raiz, '.venv/Scripts/python.exe'), '');
  writeFileSync(join(raiz, 'banco.db'), 'banco mantido');
  writeFileSync(join(raiz, 'web/package.json'), '{}');
  writeFileSync(join(raiz, 'comandos/npm.cmd'), '@echo off\r\necho %*>> "%~dp0chamadas.txt"\r\nexit /b 0\r\n');
  const rodar = () => spawnSync('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', join(raiz, 'scripts/rodar.ps1'), '-SoPreparar'], {
    encoding: 'utf8', env: { ...process.env, ANAMNESE_DB: join(raiz, 'banco.db'), PATH: `${join(raiz, 'comandos')};${process.env.PATH}` },
  });
  const primeira = rodar();
  expect(primeira.status, primeira.stdout + primeira.stderr).toBe(0);
  const chamadas = join(raiz, 'comandos/chamadas.txt');
  expect(readFileSync(chamadas, 'utf8').trim().split(/\r?\n/)).toEqual(['ci', 'run build']);
  mkdirSync(join(raiz, 'web/dist'));
  writeFileSync(join(raiz, 'web/dist/index.html'), '<html lang="pt-BR"></html>');
  expect(rodar().status).toBe(0);
  expect(readFileSync(chamadas, 'utf8').trim().split(/\r?\n/)).toHaveLength(2);
  expect(readFileSync(join(raiz, 'banco.db'), 'utf8')).toBe('banco mantido');
});
