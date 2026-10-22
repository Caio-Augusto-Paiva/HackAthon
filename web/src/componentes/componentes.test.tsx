import { useState } from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { Botao } from './Botao';
import { OpcaoResposta } from './OpcaoResposta';
import { CampoNumerico } from './CampoNumerico';
import { BarraConfianca } from './BarraConfianca';
import { Modal } from './Modal';

describe('controles de resposta', () => {
  it('impede enviar de novo enquanto o botão está carregando', async () => {
    const enviar = vi.fn();
    render(<Botao carregando onClick={enviar}>Responder</Botao>);
    const botao = screen.getByRole('button', { name: /Responder/ });
    expect(botao).toBeDisabled();
    expect(botao).toHaveAttribute('aria-busy', 'true');
    await userEvent.click(botao);
    expect(enviar).not.toHaveBeenCalled();
  });

  it('permite marcar uma opção múltipla pelo rótulo acessível', async () => {
    function Exemplo() {
      const [marcado, marcar] = useState(false);
      return <OpcaoResposta tipo="multipla" name="sinais" value="apatia" checked={marcado}
        onChange={marcar}>Abatida</OpcaoResposta>;
    }
    render(<Exemplo />);
    await userEvent.click(screen.getByRole('checkbox', { name: 'Abatida' }));
    expect(screen.getByRole('checkbox', { name: 'Abatida' })).toBeChecked();
  });

  it('ignora letras e sinais digitados sem transformar o valor em um número', async () => {
    function Exemplo() {
      const [valor, mudar] = useState('');
      return <CampoNumerico rotulo="Dias" valor={valor} onChange={mudar} casas={0} />;
    }
    render(<Exemplo />);
    await userEvent.type(screen.getByRole('textbox', { name: 'Dias' }), '1a-2');
    expect(screen.getByRole('textbox', { name: 'Dias' })).toHaveValue('12');
    expect(screen.getByRole('textbox', { name: 'Dias' })).toHaveAttribute('inputmode', 'numeric');
  });

  it('associa o erro retornado pelo backend ao campo numérico', () => {
    render(<CampoNumerico rotulo="Dias" valor="12,5" onChange={() => {}}
      erro="Use só números inteiros." />);
    const campo = screen.getByRole('textbox', { name: 'Dias' });
    expect(campo).toHaveAttribute('aria-invalid', 'true');
    expect(campo).toHaveAccessibleDescription('Use só números inteiros.');
    expect(campo).toHaveValue('12,5');
  });

  it('expõe o percentual recebido como medidor acessível', () => {
    render(<BarraConfianca percentual={64} rotulo="Hipocalcemia" />);
    expect(screen.getByRole('meter', { name: 'Hipocalcemia' })).toHaveAttribute('aria-valuenow', '64');
  });

  it('fecha uma explicação por Esc e devolve foco ao controle de origem', async () => {
    function Exemplo() {
      const [aberto, abrir] = useState(false);
      return <><button onClick={() => abrir(true)}>Explicar</button>{aberto && <Modal
        titulo="Explicação" aoFechar={() => abrir(false)}><p>Motivo da pergunta</p></Modal>}</>;
    }
    render(<Exemplo />);
    await userEvent.click(screen.getByRole('button', { name: 'Explicar' }));
    expect(screen.getByRole('dialog', { name: 'Explicação' })).toBeInTheDocument();
    await userEvent.keyboard('{Escape}');
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Explicar' })).toHaveFocus();
  });
});
