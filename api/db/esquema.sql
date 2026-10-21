-- Esquema SQLite da API (Seção 4.6 da especificação). Dados fictícios apenas.
-- Idempotente: pode ser executado a cada subida do servidor.
--
-- Os arquivos de base/ continuam sendo a fonte da verdade da base; o banco guarda índice, sessões e resultados.
-- Desvio da 4.6 (decisão D1 do plano): sessoes.snapshot_json é a fonte da verdade para restaurar a sessão
-- (respostas, perguntas_feitas e bandeiras_reconhecidas_json são projeção para consulta e auditoria) e
-- resultados_casos.extra_json guarda descricao, mudou_vs_pai e erro.
-- Colunas *_json guardam JSON em texto (UTF-8, sem escapar acentos); datas e horas são ISO-8601.

CREATE TABLE IF NOT EXISTS animais (
    id            TEXT NOT NULL PRIMARY KEY,
    brinco        TEXT NOT NULL UNIQUE,
    nome          TEXT,
    ficha_json    TEXT NOT NULL,
    origens_json  TEXT NOT NULL,
    criado_em     TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessoes (
    id                          TEXT NOT NULL PRIMARY KEY,
    animal_id                   TEXT NOT NULL REFERENCES animais (id),
    modo                        TEXT NOT NULL,
    versao_base                 TEXT NOT NULL,
    revisao                     INTEGER NOT NULL,
    fase                        TEXT NOT NULL,
    motivo_parada               TEXT,
    bandeiras_reconhecidas_json TEXT NOT NULL DEFAULT '[]',
    snapshot_json               TEXT NOT NULL,
    criada_em                   TEXT NOT NULL,
    atualizada_em               TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_sessoes_animal ON sessoes (animal_id);

CREATE TABLE IF NOT EXISTS respostas (
    sessao_id        TEXT NOT NULL REFERENCES sessoes (id),
    simbolo          TEXT NOT NULL,
    valor_json       TEXT NOT NULL,
    nao_sei          INTEGER NOT NULL DEFAULT 0 CHECK (nao_sei IN (0, 1)),
    origem           TEXT NOT NULL,
    tela_id          TEXT,
    ordem            INTEGER NOT NULL,
    modo_na_resposta TEXT NOT NULL,
    respondida_em    TEXT NOT NULL,
    PRIMARY KEY (sessao_id, simbolo)
);

CREATE TABLE IF NOT EXISTS perguntas_feitas (
    sessao_id   TEXT NOT NULL REFERENCES sessoes (id),
    simbolo     TEXT NOT NULL,
    ordem       INTEGER NOT NULL,
    motivo_json TEXT NOT NULL,
    feita_em    TEXT NOT NULL,
    PRIMARY KEY (sessao_id, simbolo)
);

CREATE TABLE IF NOT EXISTS versoes_base (
    versao    TEXT NOT NULL PRIMARY KEY,
    pai       TEXT,
    autor     TEXT,
    data      TEXT,
    nota      TEXT,
    hash      TEXT NOT NULL,
    criada_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS execucoes_casos (
    id            TEXT NOT NULL PRIMARY KEY,
    versao        TEXT NOT NULL REFERENCES versoes_base (versao),
    executada_em  TEXT NOT NULL,
    total         INTEGER NOT NULL,
    passou        INTEGER NOT NULL,
    falhou        INTEGER NOT NULL,
    comparada_com TEXT
);

CREATE INDEX IF NOT EXISTS ix_execucoes_versao ON execucoes_casos (versao);

CREATE TABLE IF NOT EXISTS resultados_casos (
    execucao_id TEXT NOT NULL REFERENCES execucoes_casos (id),
    caso_id     TEXT NOT NULL,
    status      TEXT NOT NULL,
    obtido_json TEXT NOT NULL,
    falhas_json TEXT NOT NULL,
    extra_json  TEXT NOT NULL,
    PRIMARY KEY (execucao_id, caso_id)
);
