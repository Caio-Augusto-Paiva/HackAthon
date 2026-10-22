import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { Inicio } from './Inicio';
import { Privacidade } from './Privacidade';

function montar(inicial: string) {
  render(<MemoryRouter initialEntries={[inicial]}><Routes>
    <Route path="/" element={<Inicio />} />
    <Route path="/privacidade" element={<Privacidade />} />
  </Routes></MemoryRouter>);
}

describe('política de privacidade', () => {
  it('abre pela tela de início', async () => {
    montar('/');
    await userEvent.click(screen.getByRole('link', { name: 'Política de privacidade' }));
    expect(await screen.findByRole('heading', { level: 1, name: 'Política de privacidade' })).toBeInTheDocument();
  });

  it('diz o que é guardado, onde fica e o que não é coletado', () => {
    montar('/privacidade');
    for (const secao of ['Quais dados guardamos', 'Onde os dados ficam', 'O que não coletamos', 'Por quanto tempo', 'Seus direitos'])
      expect(screen.getByRole('heading', { level: 2, name: secao })).toBeInTheDocument();
    expect(screen.getByText(/neste computador/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Voltar ao início' })).toHaveAttribute('href', '/');
  });
});
