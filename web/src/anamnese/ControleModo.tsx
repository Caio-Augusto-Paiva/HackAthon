import { Botao } from '../componentes/Botao';
import { Modal } from '../componentes/Modal';
import type { Modo } from '../api/sessao';
import estilos from './ControleModo.module.css';

export const avisoEspecialista = 'No modo especialista as perguntas têm complexidade maior: exames e sinais clínicos (temperatura retal, CMT, cálcio, BHB...).';

export function ControleModo({ modo, enviando, aoMudar, mostrarModo = true }: {
  modo: Modo; enviando: boolean; aoMudar: () => void; mostrarModo?: boolean;
}) {
  return <div className={estilos.controle}>
    {mostrarModo && <span className={estilos.modo}>Modo {modo === 'produtor' ? 'produtor' : 'especialista'}</span>}
    <Botao variante="secundario" disabled={enviando} onClick={aoMudar}>
      Mudar para modo {modo === 'produtor' ? 'especialista' : 'produtor'}
    </Botao>
  </div>;
}

export function ConfirmacaoEspecialista({ enviando, aoConfirmar, aoFechar }: {
  enviando: boolean; aoConfirmar: () => void; aoFechar: () => void;
}) {
  return <Modal titulo="Mudar para modo especialista?" aoFechar={enviando ? undefined : aoFechar}>
    <p className={estilos.aviso} id="aviso-troca-especialista">{avisoEspecialista}</p>
    <p>As respostas anteriores continuam nesta mesma verificação.</p>
    <Botao carregando={enviando} aria-describedby="aviso-troca-especialista" onClick={aoConfirmar}>Confirmar troca</Botao>
  </Modal>;
}
