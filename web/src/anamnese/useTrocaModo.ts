import { useState, type RefObject } from 'react';
import { ErroApi } from '../api/cliente';
import { obterSessao, trocarModo, type EstadoSessao, type Modo } from '../api/sessao';

/** Compartilha a troca de modo com a trava de mutações da página. */
export function useTrocaModo({ sessaoId, modo, trava, definirEnviando, aoAtualizar }: {
  sessaoId: string; modo?: Modo; trava: RefObject<boolean>; definirEnviando: (valor: boolean) => void;
  aoAtualizar: (estado: EstadoSessao) => void;
}) {
  const [confirmando, definirConfirmando] = useState(false);
  const [erro, definirErro] = useState<string>();
  const [anuncio, definirAnuncio] = useState('');
  async function efetivar(destino: Modo) {
    if (trava.current) return;
    trava.current = true; definirEnviando(true); definirErro(undefined);
    try {
      const atualizado = await trocarModo(sessaoId, destino).catch(e => {
        if (e instanceof ErroApi && e.status === 409) return obterSessao(sessaoId);
        throw e;
      });
      aoAtualizar(atualizado);
      definirAnuncio(`Modo ${atualizado.modo === 'produtor' ? 'produtor' : 'especialista'} ativado.`);
    } catch { definirErro('Não consegui trocar o modo. Tente novamente.'); }
    finally { trava.current = false; definirEnviando(false); definirConfirmando(false); }
  }
  return {
    confirmando, erro, anuncio,
    solicitar: () => {
      if (trava.current || !modo) return;
      definirErro(undefined);
      if (modo === 'produtor') definirConfirmando(true);
      else void efetivar('produtor');
    },
    confirmar: () => { void efetivar('veterinario'); },
    fechar: () => { if (!trava.current) definirConfirmando(false); },
    anunciarModo: (atual: Modo) => definirAnuncio(`Modo ${atual === 'produtor' ? 'produtor' : 'especialista'} ativado.`),
  };
}
