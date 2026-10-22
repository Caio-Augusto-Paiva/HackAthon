import { useEffect, useId, useRef, useState, type PointerEvent, type ReactNode, type RefObject } from 'react';
import { createPortal } from 'react-dom';
import { Botao } from './Botao';
import estilos from './Modal.module.css';

type Propriedades = {
  titulo: string; children: ReactNode; aoFechar?: () => void; seguranca?: boolean;
  /** `folha`: painel que sobe do rodapé, arrastável pelo puxador; o conteúdo rola por dentro. */
  variante?: 'centro' | 'folha'; resumo?: ReactNode;
};

const margemTopo = 12;
const alturaMinima = 220;

export function Modal({ titulo, children, aoFechar, seguranca = false, variante = 'centro', resumo }: Propriedades) {
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
  if (variante === 'folha') return createPortal(<div className={`${estilos.fundo} ${estilos.fundoFolha}`} onClick={e => {
    if (e.target === e.currentTarget) aoFechar?.();
  }}>
    <div ref={dialogo} role="dialog" aria-modal="true" aria-labelledby={id} tabIndex={-1} className={estilos.folha}>
      <Puxador alvo={dialogo} aoFechar={aoFechar} />
      <header className={estilos.folhaCabecalho}><h2 id={id}>{titulo}</h2>{resumo}</header>
      <div className={estilos.folhaCorpo} tabIndex={0} aria-label={`Conteúdo de ${titulo}`}>{children}</div>
      {aoFechar && <footer className={estilos.folhaRodape}><Botao variante="secundario" onClick={aoFechar}>Fechar</Botao></footer>}
    </div>
  </div>, document.body);
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

/** Arrastar muda a altura; soltar abaixo de 30% da tela fecha; clique ou Enter alterna entre normal e tela cheia. */
function Puxador({ alvo, aoFechar }: { alvo: RefObject<HTMLDivElement | null>; aoFechar?: () => void }) {
  const [expandido, definirExpandido] = useState(false);
  const arraste = useRef<{ y: number; altura: number; moveu: boolean } | null>(null);
  const ignorarClique = useRef(false);
  const aplicar = (altura: number | null) => { if (alvo.current) alvo.current.style.height = altura === null ? '' : `${altura}px`; };
  const cheia = () => window.innerHeight - margemTopo;
  const limitar = (altura: number) => Math.min(cheia(), Math.max(alturaMinima, altura));
  function iniciar(e: PointerEvent<HTMLButtonElement>) {
    e.currentTarget.setPointerCapture?.(e.pointerId);
    arraste.current = { y: e.clientY, altura: alvo.current?.getBoundingClientRect().height ?? 0, moveu: false };
    alvo.current?.setAttribute('data-arrastando', '');
  }
  function mover(e: PointerEvent<HTMLButtonElement>) {
    const atual = arraste.current;
    if (!atual) return;
    const delta = e.clientY - atual.y;
    if (Math.abs(delta) > 4) atual.moveu = true;
    if (atual.moveu) aplicar(limitar(atual.altura - delta));
  }
  function soltar(e: PointerEvent<HTMLButtonElement>) {
    const atual = arraste.current;
    arraste.current = null;
    alvo.current?.removeAttribute('data-arrastando');
    if (!atual?.moveu) return;
    ignorarClique.current = true;
    const final = atual.altura - (e.clientY - atual.y);
    if (final < window.innerHeight * 0.3) { aplicar(null); aoFechar?.(); return; }
    const tela = final > window.innerHeight * 0.85;
    definirExpandido(tela); aplicar(tela ? cheia() : limitar(final));
  }
  function alternar() {
    if (ignorarClique.current) { ignorarClique.current = false; return; }
    const proximo = !expandido;
    definirExpandido(proximo); aplicar(proximo ? cheia() : null);
  }
  return <button type="button" className={estilos.puxador} aria-expanded={expandido}
    aria-label={expandido ? 'Recolher painel' : 'Expandir painel'} title="Arraste para cima ou para baixo"
    onPointerDown={iniciar} onPointerMove={mover} onPointerUp={soltar} onPointerCancel={soltar} onClick={alternar}>
    <span aria-hidden="true" />
  </button>;
}
