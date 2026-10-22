import { useEffect, useId, useRef, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { Botao } from './Botao';
import estilos from './Modal.module.css';

type Propriedades = { titulo: string; children: ReactNode; aoFechar?: () => void; seguranca?: boolean };

export function Modal({ titulo, children, aoFechar, seguranca = false }: Propriedades) {
  const id = useId();
  const dialogo = useRef<HTMLDivElement>(null);
  const fecharAtual = useRef(aoFechar);
  fecharAtual.current = aoFechar;
  useEffect(() => {
    const origem = document.activeElement;
    const raiz = document.getElementById('root');
    const eraInerte = raiz?.hasAttribute('inert');
    const rolagem = document.body.style.overflow;
    raiz?.setAttribute('inert', '');
    document.body.style.overflow = 'hidden';
    const alvos = () => Array.from(dialogo.current?.querySelectorAll<HTMLElement>(
      'button:not(:disabled), a[href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex="0"]',
    ) ?? []);
    const primeiro = () => alvos()[0] ?? dialogo.current;
    primeiro()?.focus();
    const tecla = (evento: KeyboardEvent) => {
      if (evento.key === 'Escape') {
        evento.preventDefault();
        if (!seguranca) fecharAtual.current?.();
      }
      if (evento.key === 'Tab') {
        const itens = alvos();
        const inicio = itens[0];
        const fim = itens.at(-1);
        if (!inicio) { evento.preventDefault(); dialogo.current?.focus(); }
        else if (evento.shiftKey && (document.activeElement === inicio || document.activeElement === dialogo.current)) {
          evento.preventDefault(); fim?.focus();
        } else if (!evento.shiftKey && document.activeElement === fim) {
          evento.preventDefault(); inicio.focus();
        }
      }
    };
    const proteger = (evento: FocusEvent) => {
      if (evento.target instanceof Node && !dialogo.current?.contains(evento.target)) primeiro()?.focus();
    };
    document.addEventListener('keydown', tecla);
    document.addEventListener('focusin', proteger);
    return () => {
      document.removeEventListener('keydown', tecla);
      document.removeEventListener('focusin', proteger);
      if (!eraInerte) raiz?.removeAttribute('inert');
      document.body.style.overflow = rolagem;
      if (origem instanceof HTMLElement && origem.isConnected) origem.focus();
    };
  }, [seguranca]);
  return createPortal(<div className={estilos.fundo} onClick={e => {
    if (e.target === e.currentTarget && !seguranca) aoFechar?.();
  }}>
    <div ref={dialogo} role={seguranca ? 'alertdialog' : 'dialog'} aria-modal="true" aria-labelledby={id}
      tabIndex={-1} className={`${estilos.dialogo} ${seguranca ? estilos.perigo : ''}`}>
      <h2 id={id}>{titulo}</h2>
      {children}
      {aoFechar && !seguranca && <Botao variante="secundario" onClick={aoFechar}>Fechar</Botao>}
    </div>
  </div>, document.body);
}
