import { useEffect, useRef, useState } from 'react';

const duracao = 900;
const suavizar = (t: number) => 1 - (1 - t) ** 3;

function semMovimento() {
  return typeof window.matchMedia !== 'function' || typeof window.requestAnimationFrame !== 'function'
    || window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** Porcentagem que conta do valor anterior (0 na montagem) até o atual; com movimento reduzido mostra o valor direto. */
export function Contador({ valor, atraso = 0 }: { valor: number; atraso?: number }) {
  const [mostrado, definirMostrado] = useState(() => semMovimento() ? valor : 0);
  const atual = useRef(mostrado);
  useEffect(() => {
    if (semMovimento()) { atual.current = valor; definirMostrado(valor); return; }
    const inicio = atual.current;
    let quadro = 0;
    let comeco: number | undefined;
    const passo = (agora: number) => {
      comeco ??= agora + atraso;
      const t = Math.min(1, Math.max(0, (agora - comeco) / duracao));
      atual.current = Math.round(inicio + (valor - inicio) * suavizar(t));
      definirMostrado(atual.current);
      if (t < 1) quadro = requestAnimationFrame(passo);
    };
    quadro = requestAnimationFrame(passo);
    return () => cancelAnimationFrame(quadro);
  }, [valor, atraso]);
  return <>{mostrado}%</>;
}
