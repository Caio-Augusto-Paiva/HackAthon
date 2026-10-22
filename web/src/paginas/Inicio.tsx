import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { iniciarVerificacao, type Modo } from '../api/sessao';
import { ErroApi } from '../api/cliente';
import { Boi } from '../componentes/Boi';
import { Botao } from '../componentes/Botao';
import alerta from '../assets/alerta.svg';
import estilos from './Inicio.module.css';

export function Inicio() {
  const navegar = useNavigate();
  const enviando = useRef(false);
  const [carregando, carregar] = useState<Modo | null>(null);
  const [erro, definirErro] = useState('');
  const [ultimoModo, definirUltimoModo] = useState<Modo>('produtor');
  async function iniciar(modo: Modo) {
    if (enviando.current) return;
    enviando.current = true;
    carregar(modo);
    definirErro('');
    definirUltimoModo(modo);
    try {
      const sessao = await iniciarVerificacao(modo);
      navegar(`/anamnese/${encodeURIComponent(sessao.sessao_id)}`);
    } catch (falha) {
      if (falha instanceof ErroApi && falha.status === 409 && /base.*ativ/i.test(falha.message)) {
        definirErro('Nenhuma base ativa. Peça para ativar uma versão.');
      } else {
        definirErro(falha instanceof ErroApi ? falha.message : 'Não foi possível iniciar. Tente de novo.');
      }
    } finally {
      enviando.current = false;
      carregar(null);
    }
  }
  return <main className={`fundoComBrilho ${estilos.inicio}`}>
    <div className={estilos.palco}><Boi tamanho={360} /></div>
    <section className={estilos.chamada} aria-labelledby="titulo-inicio">
      <h1 id="titulo-inicio">Anamnese Bovina</h1>
      <p className={estilos.apresentacao}>Responda algumas perguntas sobre a vaca e eu descubro o que ela pode ter, quão grave é e por quê.</p>
      <div className={estilos.cartao}>
        <Botao onClick={() => iniciar('produtor')} disabled={carregando !== null} carregando={carregando === 'produtor'}>
          Iniciar verificação
        </Botao>
        <Botao variante="secundario" aria-describedby="aviso-especialista" onClick={() => iniciar('veterinario')}
          disabled={carregando !== null} carregando={carregando === 'veterinario'}>
          Iniciar verificação como especialista
        </Botao>
        <div className={estilos.aviso}>
          <img src={alerta} alt="" width={22} height={22} />
          <p id="aviso-especialista">No modo especialista as perguntas têm complexidade maior: exames e sinais clínicos (temperatura retal, CMT, cálcio, BHB...).</p>
        </div>
        {erro && <div className={estilos.falha}>
          <p role="alert">{erro}</p>
          <Botao variante="secundario" onClick={() => iniciar(ultimoModo)} carregando={carregando !== null}>Tentar de novo</Botao>
        </div>}
      </div>
      <p className={estilos.nota}>Triagem explicável por um sistema especialista. Não substitui o médico-veterinário. Dados fictícios.</p>
    </section>
  </main>;
}
