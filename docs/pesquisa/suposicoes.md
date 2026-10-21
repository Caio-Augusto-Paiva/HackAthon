# Suposições, lacunas e itens a validar

Extraído de `docs/prompts/secao-1.md` a `secao-5.md`, `docs/fontes/fontes.md` e `docs/agentes-e-skills.md`. Trechos copiados dos arquivos. Termos buscados: "(suposição)", "suposição a validar", "a calibrar", "a confirmar", "não confirmado", "sem fonte", status "R" (leitura pendente) em fontes, "Decisão minha, a confirmar", itens de risco.

| # | Seção | Trecho curto | Tipo | Como validar |
|---|---|---|---|---|
| 1 | S1 (§ Triagem, tela 2) | "Orelhas frias sugere hipocalcemia (suposição a validar)." | clínica (veterinária) | especialista/RERUM |
| 2 | S2 (Dimensão estimada) | "Dimensão estimada (suposição, para caber em dois dias e meio)" | processo/prazo | decisão da equipe |
| 3 | S2 (Casos de teste) | "Os casos são inventados por nós, então são suposição a validar." | clínica (veterinária) | especialista/RERUM |
| 4 | S3 (linha inicial) | "Todo conteúdo veterinário aqui é suposição a validar." | clínica (veterinária) | especialista/RERUM |
| 5 | S3 §3.2 | "numero_lactacoes, numérico, registrado; sem regra no PoC (sem fonte)" | clínica (veterinária) | especialista/RERUM |
| 6 | S3 §3.2 | "retencao_placenta, parto_distocico, historico_mastite_12m: metrite (suposição), mastite (suposição)" | clínica (veterinária) | especialista/RERUM |
| 7 | S3 §3.3 | "R-DER-05 SE temperatura_retal < 38,0 ENTÃO hipotermia +0,90 suposição [vet]" | número/limiar | especialista/RERUM |
| 8 | S3 §3.3 | "R-DER-06 SE 38,0 ≤ temperatura_retal < 39,5 ENTÃO febre −0,90 suposição [vet]" | número/limiar | especialista/RERUM |
| 9 | S3 §3.3 | "R-DER-07 SE extremidades = quente ENTÃO febre +0,50 suposição [produtor]" | clínica (veterinária) | especialista/RERUM |
| 10 | S3 §3.3 | "R-DER-09 SE extremidades = normal ENTÃO febre −0,40 suposição [produtor]" | clínica (veterinária) | especialista/RERUM |
| 11 | S3 §3.3 | "R-DER-10 SE retencao_placenta ENTÃO parto_complicado +0,90 suposição (combinacao: max)" | clínica (veterinária) | especialista/RERUM |
| 12 | S3 §3.3 | "R-DER-11 SE parto_distocico ENTÃO parto_complicado +0,90 suposição" | clínica (veterinária) | especialista/RERUM |
| 13 | S3 §3.4 | "um_quarto_afetado, sim, sim, mastite (suposição)" | clínica (veterinária) | especialista/RERUM |
| 14 | S3 §3.4 | "fraqueza_tremores, sim, sim, hipocalcemia (suposição)" | clínica (veterinária) | especialista/RERUM |
| 15 | S3 §3.5 | "CF são estimativas minhas" | número/limiar | caso de teste |
| 16 | S3 §3.5 (todas as regras da base) | "Todas com status: suposicao_a_validar" | clínica (veterinária) | especialista/RERUM |
| 17 | S3 §3.5 mastite | "R-MAS-04 SE um_quarto_afetado ENTÃO mastite +0,30 suposição" | clínica (veterinária) | especialista/RERUM |
| 18 | S3 §3.5 mastite | "R-MAS-06 SE historico_mastite_12m ENTÃO mastite +0,15 suposição" | clínica (veterinária) | especialista/RERUM |
| 19 | S3 §3.5 mastite | "R-MAS-07 SE leite_alterado = não E ubere_inflamado = não ENTÃO mastite −0,60 suposição" | clínica (veterinária) | especialista/RERUM |
| 20 | S3 §3.5 metrite | "R-MET-04 SE parto_complicado ENTÃO metrite +0,30 suposição" | clínica (veterinária) | especialista/RERUM |
| 21 | S3 §3.5 TPB | "R-TPB-07 SE febre = não E urina_escura = não ENTÃO tpb −0,50 suposição" | clínica (veterinária) | especialista/RERUM |
| 22 | S3 §3.5 cetose | "R-CET-07 SE febre ENTÃO cetose −0,30 suposição (cetose primária é afebril)" | clínica (veterinária) | especialista/RERUM |
| 23 | S3 §3.5 hipocalcemia | "R-HIP-03 SE fraqueza_tremores E periparto_imediato ENTÃO hipocalcemia +0,50 suposição" | clínica (veterinária) | especialista/RERUM |
| 24 | S3 §3.5 hipocalcemia | "R-HIP-06 SE dias_em_lactacao > 7 ENTÃO hipocalcemia −0,70 F7 (até 48 h; margem suposição)" | número/limiar | especialista/RERUM |
| 25 | S3 §3.5 acidose | "R-ACI-04 SE diarreia E apatia ENTÃO acidose +0,20 suposição" | clínica (veterinária) | especialista/RERUM |
| 26 | S3 §3.5 dermatite | "R-DD-02 SE claudicacao E febre = não E apetite = normal ENTÃO dermatite_digital +0,25 suposição (quadro local)" | clínica (veterinária) | especialista/RERUM |
| 27 | S3 §3.6 | "R-BV-03 SE apetite = ausente E apatia quadro sistêmico grave (suposição)" | clínica (veterinária) | especialista/RERUM |
| 28 | S3 §3.6 | "R-BV-06 SE temperatura_retal ≥ 41,0 febre muito alta (vet; limiar suposição)" | número/limiar | especialista/RERUM |
| 29 | S3 §3.7 | "Gravidade é atributo do símbolo doenca (suposição)" | clínica (veterinária) | especialista/RERUM |
| 30 | S3 §3.8 item 6 | "sem_problema sai das regras e vira resultado padrão ... Decisão minha, a confirmar." | técnica (versão, comando, ferramenta) | decisão da equipe |
| 31 | S3 §3.9 | "CF são estimativas sem calibração com dados reais" | número/limiar | caso de teste |
| 32 | S3 §3.9 | "espere três ou quatro hipóteses entre 20% e 50% em casos vagos" | clínica (veterinária) | caso de teste |
| 33 | S3 §3.9 | "Hemoglobinúria também ocorre em hipofosfatemia pós-parto e hemoglobinúria bacilar" | clínica (veterinária) | especialista/RERUM |
| 34 | S3 §3.9 | "Foot rot fica fora do escopo e pode ser confundido com dermatite digital" | clínica (veterinária) | especialista/RERUM |
| 35 | S4 §4.1 (TypeScript) | "(suposição a confirmar)"; "confirmar na instalação" | técnica (versão, comando, ferramenta) | instalação/execução |
| 36 | S4 §4.3 (árvore) | "db/ ... repositorios.py (sqlite3 da biblioteca padrão, sem ORM) (suposição)" | técnica (versão, comando, ferramenta) | decisão da equipe |
| 37 | S4 §4.5.1 | "Ids das telas (dias_em_lactacao, estado_termico, ...) são (suposição)" | técnica (versão, comando, ferramenta) | decisão da equipe |
| 38 | S4 §4.5.2 | "dias_em_lactacao é calculado na criação da sessão (suposição; ver decisão 4)" | técnica (versão, comando, ferramenta) | decisão da equipe |
| 39 | S5 (§5 cabeçalho) | "Tudo que não vem das Seções 1 a 4 ou de [A]/[D] está marcado (suposição)." | organização (regra do hackathon) | decisão da equipe |
| 40 | S5 §5.1 | "cd e2e && npx playwright test (suposição: e2e/ com package.json próprio)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 41 | S5 §5.1 | "Tempo-alvo: abaixo de 30 s (suposição)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 42 | S5 §5.1 camada 1 | "cobertura das linhas de engine/ acima de 90% (suposição)" | número/limiar | instalação/execução |
| 43 | S5 §5.1 camada 1 | "nenhum import de api, web ou sqlite3 em engine/ (teste de arquitetura, suposição)" | técnica (versão, comando, ferramenta) | decisão da equipe |
| 44 | S5 §5.1 camada 3 | "Convenções do executor (engine/casos.py), todas (suposição) a registrar na Seção 2" | técnica (versão, comando, ferramenta) | decisão da equipe |
| 45 | S5 §5.1 camada 3 | "versões antigas só reportam (suposição, pois um caso pode ter sido criado depois delas)" | técnica (versão, comando, ferramenta) | decisão da equipe |
| 46 | S5 §5.1 camada 3 | "valores abaixo foram estimados à mão com os CF da Seção 3 v2" | número/limiar | caso de teste |
| 47 | S5 §5.1 camada 3 | "Todos os casos são inventados (suposição a validar)." | clínica (veterinária) | especialista/RERUM |
| 48 | S5 §5.1 tabela (C-SAD-01) | "motivo_parada em {sem_potencial, sem_perguntas} (suposição)" | técnica (versão, comando, ferramenta) | caso de teste |
| 49 | S5 §5.1 pronto camada 3 | "rodar a suíte inteira em menos de 10 s (suposição)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 50 | S5 §5.1 pronto camada 4b | "--offline do Chromium não é necessário; basta Wi-Fi desligado (suposição)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 51 | S5 §5.1 pronto camada 4b | "cada falha gera trace do Playwright em e2e/test-results/ (suposição)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 52 | S5 §5.2 pré-requisitos | "Windows 11, suposição de que a demonstração roda em Windows" | técnica (versão, comando, ferramenta) | decisão da equipe |
| 53 | S5 §5.2 pré-requisitos | "winget install --id astral-sh.uv -e, suposição de id" | técnica (versão, comando, ferramenta) | instalação/execução |
| 54 | S5 §5.2 pré-requisitos | "winget install OpenJS.NodeJS.LTS (suposição de id; confirmar a linha 24)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 55 | S5 §5.2 preparo | "-SoPreparar (suposição de nome)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 56 | S5 §5.2 rodar.ps1, passo 2 | "uv sync --frozen --offline, suposição de flag" | técnica (versão, comando, ferramenta) | instalação/execução |
| 57 | S5 §5.2 rodar.ps1, passo 5 | "Se a versão instalada do FastAPI tiver função própria ... (a confirmar na instalação ...)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 58 | S5 §5.2 rodar.ps1, passo 6 | "Espera GET /api/saude responder (até 30 s (suposição))" | técnica (versão, comando, ferramenta) | instalação/execução |
| 59 | S5 §5.2 modo dev | "VITE_USAR_MOCKS=1 (suposição: ...)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 60 | S5 §5.2 sem internet, item 2 | "grep -rn http web/src web/index.html revisado a mão (suposição)" | técnica (versão, comando, ferramenta) | instalação/execução |
| 61 | S5 §5.2 sem internet, item 4 | "Feito na quinta à noite e na sexta às 08:00 (suposição de horário)" | processo/prazo | decisão da equipe |
| 62 | S5 §5.3 cronograma | "Ter 20/10 noite (≤ 2 h, suposição)" | processo/prazo | decisão da equipe |
| 63 | S5 §5.3 cronograma | "Cada pessoa registra prompts e decisões em docs/processo/<pessoa>.md (suposição)" | processo/prazo | decisão da equipe |
| 64 | S5 §5.4 plano de corte | "Ganho (suposição)" (coluna com 2 h, 1,5 h, 3 a 4 h etc.) | processo/prazo | decisão da equipe |
| 65 | S5 §5.2/4b (ambiente) | "variáveis de ambiente lidas por api/config.py, suposição" | técnica (versão, comando, ferramenta) | instalação/execução |
| 66 | agentes-e-skills, princípio 5 | "não conflitam com a exigência de open source (suposição)" | organização (regra do hackathon) | decisão da equipe |
| 67 | agentes-e-skills, final | "Skills não confirmadas para este projeto: FastAPI, pytest, React Flow e Vite" | técnica (versão, comando, ferramenta) | leitura da fonte |
| 68 | fontes.md (status R) | "F1 a F5 e F7 a F11 com status R: conferida só por resumo de busca (leitura integral pendente)" | clínica (veterinária) | leitura da fonte |

Nota: a linha 16 agrupa todas as regras da base com status `suposicao_a_validar`. As regras da camada 2 e da camada 3 que não aparecem acima têm o mesmo status e entram nessa linha.

## Contagem por Tipo

- clínica (veterinária): 28
- número/limiar: 8
- técnica (versão, comando, ferramenta): 25
- processo/prazo: 5
- organização (regra do hackathon): 2

Total: 68 linhas.
