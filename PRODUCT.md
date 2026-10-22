# Anamnese Bovina

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Stack definida pela equipe: React 19, TypeScript 5.x, Vite 8, React Router 7 e CSS Modules com variáveis CSS. Fontes locais por `@fontsource`. Tipos gerados do OpenAPI com `openapi-typescript`. Vitest, Testing Library e Playwright verificam a interface. A SPA compilada é servida pela API FastAPI em `http://localhost:8000/`.

## Users

Produtor de bovinos leiteiros e médico-veterinário. O modo produtor apresenta observações acessíveis ao produtor; o modo especialista corresponde a `veterinario` na API e inclui perguntas técnicas. Os dois modos compartilham fatos, base de conhecimento e motor.

## Product Purpose

Coletar sinais e histórico de uma vaca em lactação por perguntas estruturadas e apresentar hipóteses, urgência e explicações. A consulta admite incerteza, desconhecimento e hipóteses simultâneas. O resultado apoia a triagem e não constitui diagnóstico ou recomendação terapêutica.

## Positioning

Diálogo adaptativo inspirado no Akinator, com regras explícitas e fatores de certeza MYCIN. O motor e a API determinam a próxima pergunta e o parecer. O navegador apresenta os dados e envia respostas, sem raciocínio clínico nem cálculo de CF.

## Operating Context

Prova de conceito para o Hackathon UFJF 2026, com animais e casos fictícios. Execução em localhost, sem serviços externos durante a consulta. A base ativa é versionada e cada sessão permanece vinculada à sua versão. A entrega requer demonstração pela interface, documentação e casos conhecidos reproduzíveis.

## Capabilities and Constraints

- Fluxo requerido: início, escolha do modo, triagem, perguntas dinâmicas, alerta de segurança, parecer e explicações.
- Respostas booleanas ou categóricas usam opções. Múltipla seleção envia todos os campos apresentados. “Não sei” é explícito e distinto de “Não” e de uma pergunta sem resposta.
- Números seguem como a string digitada, sem coerção, arredondamento ou envio de CF. O backend decide faixa e precisão e o frontend mostra o erro 422 no campo.
- Uma pausa de bandeira exige apresentar o alerta, mesmo quando `proxima` for nulo. As ações disponíveis vêm da API.
- A interface trata erros de rede, base ausente, carregamento, duplo envio e conflito entre requisições. Um 409 de mutação exige reler a sessão.
- A porcentagem representa confiança do sistema, sem equivaler a probabilidade clínica. Toda regra permanece como suposição a validar.
- Todos os textos de interface são em português do Brasil. Os termos são “verificação”, “modo produtor”, “modo especialista” e “parecer”.
- Acessibilidade: contraste, foco visível, controles nativos, teclado, foco protegido nos alertas, alvos de 44 px e redução de movimento.
- A identidade visual e os assets pertencem ao protótipo Figma fornecido. As decisões visuais ficam em `DESIGN.md`.
- O editor visual de regras fica fora deste frontend de anamnese. Revisão clínica, aprovação dos pesos e eventual uso real permanecem pendentes.

## Voice

Próximo e lúdico no diálogo, claro e sério ao comunicar gravidade. Perguntas simples e ações diretas. Sem prometer certeza diagnóstica nem inventar orientações clínicas ausentes na API.

## Evidence

Plano: `docs/superpowers/plans/2026-10-22-frontend-web.md`. Contrato: `contratos/openapi.json` e seção “Para o frontend” em `api/README.md`. Referência visual: arquivo Figma HackAtom, página “Protótipo”, informado pela equipe. Contexto registrado a partir dessas fontes por instrução expressa da equipe, sem introduzir decisões de produto adicionais.
