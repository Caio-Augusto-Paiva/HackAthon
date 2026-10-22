import { act, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { Contador } from './Contador';

function movimento(reduzido: boolean) {
  vi.stubGlobal('matchMedia', (consulta: string) => ({ matches: reduzido && consulta.includes('reduce'), media: consulta,
    addEventListener() {}, removeEventListener() {} }));
}

describe('contador de porcentagem', () => {
  afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers(); });

  it('mostra o valor final na hora quando o movimento está reduzido', () => {
    movimento(true);
    render(<Contador valor={64} />);
    expect(screen.getByText('64%')).toBeInTheDocument();
  });

  it('conta de 0 até o valor e termina exatamente nele', () => {
    movimento(false);
    vi.useFakeTimers();
    let agora = 0;
    vi.stubGlobal('requestAnimationFrame', (f: FrameRequestCallback) => setTimeout(() => { agora += 16; f(agora); }, 16));
    vi.stubGlobal('cancelAnimationFrame', (id: number) => clearTimeout(id));
    render(<Contador valor={87} />);
    expect(screen.getByText('0%')).toBeInTheDocument();
    act(() => { vi.advanceTimersByTime(300); });
    const meio = Number(screen.getByText(/%$/).textContent!.replace('%', ''));
    expect(meio).toBeGreaterThan(0); expect(meio).toBeLessThan(87);
    act(() => { vi.advanceTimersByTime(2000); });
    expect(screen.getByText('87%')).toBeInTheDocument();
  });
});
