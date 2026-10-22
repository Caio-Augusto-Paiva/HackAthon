import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import estilos from './Privacidade.module.css';

/** Texto fixo: descreve o que o sistema realmente faz hoje (banco SQLite local, sem conta, sem cookies, sem serviços externos). */
export function Privacidade() {
  useEffect(() => { document.title = 'Política de privacidade · Anamnese Bovina'; return () => { document.title = 'Anamnese Bovina'; }; }, []);
  return <div className={`fundoComBrilho ${estilos.pagina}`}>
    <header className={estilos.cabecalho}><Link to="/">Anamnese Bovina</Link></header>
    <main className={estilos.folha}>
      <h1>Política de privacidade</h1>
      <p className={estilos.resumo}>Em uma frase: tudo o que você responde fica <strong>neste computador</strong>. Não pedimos dados pessoais, não usamos cookies e não enviamos nada para a internet.</p>

      <section aria-labelledby="dados"><h2 id="dados">Quais dados guardamos</h2>
        <ul>
          <li><strong>Do animal:</strong> brinco, nome e, se você importar, a ficha com o histórico do animal. Na verificação pela tela inicial, o animal é anônimo.</li>
          <li><strong>Da verificação:</strong> o modo escolhido, cada resposta dada, as perguntas feitas e o parecer calculado, junto com a versão da base de conhecimento usada.</li>
        </ul>
      </section>

      <section aria-labelledby="onde"><h2 id="onde">Onde os dados ficam</h2>
        <p>Em um único arquivo de banco de dados (SQLite) no computador onde o sistema está rodando. O sistema responde só para este computador (endereço local) e não depende de nenhum serviço na nuvem. Nenhuma inteligência artificial externa recebe suas respostas: o parecer é calculado aqui, por regras.</p>
      </section>

      <section aria-labelledby="nao"><h2 id="nao">O que não coletamos</h2>
        <ul>
          <li>Nome, e-mail, CPF, telefone ou localização de quem usa o sistema.</li>
          <li>Cookies, rastreadores ou estatísticas de uso.</li>
          <li>Fontes, scripts ou imagens de outros sites: tudo é carregado do próprio sistema.</li>
        </ul>
      </section>

      <section aria-labelledby="tempo"><h2 id="tempo">Por quanto tempo</h2>
        <p>Os dados ficam guardados até que o responsável pela instalação apague o arquivo do banco de dados. Não há cópia em outro lugar.</p>
      </section>

      <section aria-labelledby="direitos"><h2 id="direitos">Seus direitos</h2>
        <p>Pela Lei Geral de Proteção de Dados (LGPD), você pode pedir para ver, corrigir ou apagar dados que digam respeito a você. Como o sistema não guarda dados pessoais de quem o usa, esses pedidos se resolvem com o responsável pela instalação, que tem acesso ao arquivo do banco.</p>
      </section>

      <p className={estilos.nota}>Esta é uma prova de conceito do Hackathon UFJF 2026 e usa apenas animais e casos fictícios. Uma versão em produção precisaria indicar um responsável pelo tratamento dos dados e um canal de contato.</p>
      <Link className={estilos.voltar} to="/">Voltar ao início</Link>
    </main>
  </div>;
}
