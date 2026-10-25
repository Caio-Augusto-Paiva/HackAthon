import { useRef, useState, type ReactNode } from 'react';
import type { components } from '../api/tipos.gerado';
import { agirBandeira, obterSessao, type EstadoSessao } from '../api/sessao';
import { ErroApi } from '../api/cliente';
import { Modal } from '../componentes/Modal';
import { Botao } from '../componentes/Botao';
import icone from '../assets/alerta-modal.svg';
import estilos from './AlertaBandeira.module.css';

const listaPt = new Intl.ListFormat('pt-BR', { type: 'conjunction' });

export function AlertaBandeira({ alerta, sessaoId, aoAtualizar, complemento, erroExterno }: {
  alerta: components['schemas']['Alerta']; sessaoId: string; aoAtualizar: (estado: EstadoSessao) => void;
  complemento?: ReactNode; erroExterno?: string;
}) {
  const [enviando, definirEnviando] = useState<string>();
  const [erro, definirErro] = useState<string>();
  const trava = useRef(false);
  async function agir(acao: components['schemas']['AcaoBandeira']['acao']) {
    if (trava.current) return;
    trava.current = true; definirEnviando(acao); definirErro(undefined);
    try { aoAtualizar(await agirBandeira(sessaoId, acao)); }
    catch (e) {
      if (e instanceof ErroApi && e.status === 409) {
        try { aoAtualizar(await obterSessao(sessaoId)); }
        catch (falha) { definirErro(falha instanceof Error ? falha.message : 'Não consegui atualizar a verificação.'); }
      } else definirErro(e instanceof Error ? e.message : 'Não consegui registrar sua escolha. Tente novamente.');
    } finally { trava.current = false; definirEnviando(undefined); }
  }
  return <Modal titulo="Atenção: sintoma grave" seguranca>
    <img src={icone} width={32} height={32} alt="" className={estilos.icone} />
    <p className={estilos.texto}>{alerta.texto}</p>
    {alerta.sinais?.length ? <p className={estilos.regras}>Sinais que acenderam o alerta: {listaPt.format(alerta.sinais)}.</p> : null}
    {erro && <p role="alert" className={estilos.erro}>{erro}</p>}
    {erroExterno && <p role="alert" className={estilos.erro}>{erroExterno}</p>}
    <div className={estilos.acoes}>
      {alerta.acoes.includes('ver_parecer') && <Botao carregando={enviando === 'ver_parecer'} disabled={Boolean(enviando)} onClick={() => agir('ver_parecer')}>Ver parecer</Botao>}
      {alerta.acoes.includes('continuar') && <Botao variante="secundario" carregando={enviando === 'continuar'} disabled={Boolean(enviando)} onClick={() => agir('continuar')}>Continuar respondendo</Botao>}
    </div>
    {complemento && <fieldset className={estilos.complemento} disabled={Boolean(enviando)}>
      <legend className="somenteLeitor">Modo da verificação</legend>{complemento}
    </fieldset>}
  </Modal>;
}
