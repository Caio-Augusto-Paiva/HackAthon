import { render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { exemploComo, resposta } from '../teste/cenarios';
import { ComoChegou } from './ComoChegou';

function montar(como: unknown) {
  vi.stubGlobal('fetch', vi.fn(async () => resposta(como)));
  render(<ComoChegou sessaoId="ses_0001" simbolo="mastite" aoFechar={() => {}} />);
}
const exclusao = { tipo: 'exclusao', frase: 'Retenção de placenta ficou mais forte e a metrite perdeu força', por: 'retencao_placenta', por_nome: 'Retenção de placenta', antes: 0.7, depois: -0.1 };

describe('explicação Como cheguei aqui?', () => {
  it('mostra cada exclusão como passo no fim, com frase e variação', async () => {
    montar({ ...exemploComo, exclusoes: [exclusao] });
    const dialogo = await screen.findByRole('dialog');
    const itens = await within(dialogo).findAllByRole('listitem');
    const passo = (await within(dialogo).findByText(/Retenção de placenta ficou mais forte/)).closest('li') as HTMLElement;
    expect(passo).toHaveTextContent('70% → 0%');
    expect(itens.filter(i => i.querySelector(':scope > p'))[ itens.filter(i => i.querySelector(':scope > p')).length - 1 ]).toBe(passo);
  });
  it('sem exclusões, nada muda', async () => {
    montar({ ...exemploComo, exclusoes: [] });
    await screen.findByRole('dialog');
    await screen.findAllByText(/Porque foi observado/);
    expect(screen.queryByText(/perdeu força/)).toBeNull();
  });
});
