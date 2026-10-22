---
name: Anamnese Bovina
description: Interface de triagem explicável conforme o protótipo HackAthon
colors:
  fundo-escuro: "#1f4d2c"
  fundo-medio: "#2e6b3f"
  creme: "#f6f1e4"
  superficie: "#ffffff"
  primaria: "#2e6b3f"
  primaria-escura: "#173d22"
  acento: "#f4a6a6"
  acento-escuro: "#b5545c"
  texto: "#1e2a20"
  texto-suave: "#55604f"
  texto-claro: "#f6f1e4"
  perigo: "#c62828"
  perigo-fundo: "#fde8e6"
  alerta: "#e8a317"
  ok: "#3e8e4e"
  trilho: "#e3dcc8"
typography:
  display:
    fontFamily: Varela Round
    fontWeight: 400
    fontSize: 64px
    lineHeight: 1.3
  title:
    fontFamily: Varela Round
    fontWeight: 400
    fontSize: 40px
    lineHeight: 1.3
  body:
    fontFamily: Nunito Sans
    fontWeight: 400
    fontSize: 20px
    lineHeight: 1.3
rounded:
  opcao: 18px
  botao: 22px
  balao: 28px
  cartao: 32px
spacing:
  pequeno: 12px
  medio: 20px
  grande: 36px
---

## Overview

Referência fixa: [HackAthon, página Protótipo](https://www.figma.com/design/MUiGJ81WjX97iyjX0yE6jz/HackAtom?node-id=9-2), conferida por `get_design_context`, `get_variable_defs` e leitura da coleção “Tokens” em 22/10/2026. O desenho usa fundo verde, superfícies creme, boi ilustrado e ação principal rosa (o rosa do focinho do boi). A adaptação implementa o fluxo real da API em layouts responsivos, sem substituir conteúdo clínico por exemplos estáticos do Figma.

## Colors

As 16 entradas de `colors` reproduzem os tokens `cor/*` da coleção Figma “Tokens”, modo “Claro”. No CSS, cada nome recebe `--cor-`, mantendo o sufixo original. Fundo escuro para a página, primária escura para a barra de hipóteses, creme para balões e cartões, superfície branca para campos e opções. Perigo, alerta e confirmação também precisam de rótulo textual. Ajustes de contraste usam derivados sem alterar os 16 valores de origem.

## Typography

Varela Round nos títulos e no nome do produto; Nunito Sans nos textos, perguntas e controles. A pergunta usa 30 px e peso 800 no desktop. Botões usam 22 px e peso 800; opções usam 20 px. Pesos locais 400, 600, 700 e 800, com números tabulares no parecer. Escala fluida para telas pequenas, sem recortar textos ou impedir zoom.

## Layout

Frames de referência: início `9:2`, pergunta inicial `9:42`, erro `24:192`, pergunta com lateral `9:99`, múltipla `10:43`, alerta `10:144` e parecer `10:217`. O desktop de referência tem 1440 px. Início: palco do boi com 460 px, ilustração de 360 px, intervalo de 96 px e chamada de 520 px. Perguntas: cabeçalho com margens de 56 px, formulário de até 560 px e balão ao lado do boi de 132 px. A lateral de 380 px aparece da segunda pergunta em diante. Parecer: corpo de até 1040 px e boi de 96 px.

Em 375/768 px, reorganizar em uma coluna e preservar a ordem de leitura. A lateral passa para baixo da pergunta. Em 1024 px, reduzir margens e permitir quebra do cabeçalho sem sobreposição. Tabelas mantêm semântica e adaptação legível. As medidas do Figma são referências de composição, não larguras mínimas que provoquem rolagem horizontal.

## Elevation & Depth

Profundidade claymórfica macia. Cartão/balão: sombra externa `0 10px 20px rgba(14,38,20,.45)`, interna inferior `inset 0 -4px 6px rgba(14,38,20,.22)` e superior `inset 0 3px 4px rgba(255,255,255,.55)`. Botão rosa: externa `0 6px 6px rgba(181,84,92,.40)` e interiores com o mesmo tratamento. Opções: externa `0 4px 4px rgba(143,134,112,.45)`. Nenhuma sombra dura sem desfoque. O brilho de fundo é o SVG fornecido pelo Figma.

## Shapes

Bordas de 3 px e raios de 18–32 px conforme os tokens. Balão com canto inferior esquerdo de 6 px. Seleção única tem marcador circular; múltipla, quadrado arredondado. Ilustrações e ícones são os SVGs originais, armazenados localmente e sem alterar seus atributos de raiz. Estados de gravidade têm texto e cor.

## Components

- Botão primário rosa e secundário branco com contorno verde. Carregando impede novo envio e informa `aria-busy`.
- Opções usam `radio`/`checkbox` nativos dentro de `fieldset` e `legend`. Selecionada recebe fundo creme, contorno rosa e check original do Figma.
- Campo numérico é texto com teclado numérico/decimal, rótulo, unidade e ajuda. O erro preserva a entrada e aparece abaixo, com borda vermelha e texto acessível. Sem valor inicial inventado.
- Barras usam `role="meter"` e preenchimento sólido proporcional ao percentual recebido. Não reproduzir o gradiente usado no protótipo.
- Alerta de segurança protege foco, mostra texto e ações da API e não fecha por Esc ou clique externo. Outros diálogos permitem fechamento explícito e devolvem foco.
- Parecer usa tabela semântica com caption, blocos e percentuais da API. O frontend ordena a apresentação, sem criar cortes clínicos.
- Uma única transição autoral entre perguntas: leve subida e fade do balão, desativada por `prefers-reduced-motion`.
- Todo controle recebe foco visível, alvos de pelo menos 44 px e estados carregando, erro, vazio e desabilitado.

## Do's and Don'ts

Preservar a identidade do Figma e a autoridade da API. Sem CDN, fontes remotas, assets temporários em runtime, biblioteca de componentes, Tailwind ou CSS-in-JS. Não redesenhar o boi. Não usar o screenshot como fundo ou implementação. Não calcular CF, converter porcentagem em probabilidade ou publicar orientações clínicas escritas no cliente.
