# Casos de teste — documentação gerada

> GERADO por `scripts/gerar_doc_regras.py`; resultados obtidos com `engine.casos.executar_caso`.

Base `3.1.0-revisao1`. Casos sintéticos executados: **2**. Aprovados: **2**.

Os casos demonstram integração e comportamento determinístico. Não medem acurácia, sensibilidade ou especificidade clínicas. Os testes unitários são contabilizados separadamente.

| Caso | Resultado | Urgência | Primeira hipótese | Pausa ocorreu |
| --- | --- | --- | --- | --- |
| DEV-BV-01 | passou | chamar_agora | hipocalcemia | sim |
| DEV-MAS-01 | passou | observar | mastite | não |

## DEV-BV-01

Demonstração sintética de alerta por incapacidade de se levantar. Suposição a validar; não constitui caso clínico validado.

### Entrada e resultado esperado

```json
{
  "id": "DEV-BV-01",
  "descricao": "Demonstração sintética de alerta por incapacidade de se levantar. Suposição a validar; não constitui caso clínico validado.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 2
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [
      "decubito"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "limite_dinamico": 0,
  "esperado": {
    "urgencia": "chamar_agora",
    "bandeira": "R-BV-01",
    "top1": "hipocalcemia",
    "faixas": {
      "hipocalcemia": [
        64,
        65
      ]
    },
    "alerta": {
      "pausa": true
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "DEV-BV-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "hipocalcemia",
    "top3_contem": [
      "hipocalcemia",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "hipocalcemia": 64,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [
      "R-BV-01"
    ],
    "inconclusivas": [
      "hipocalcemia"
    ],
    "alerta": {
      "pausa": true
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "leite_alterado",
    "queda_producao",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## DEV-MAS-01

Demonstração sintética de leite alterado e úbere inflamado durante a triagem. Suposição a validar; não constitui caso clínico validado.

### Entrada e resultado esperado

```json
{
  "id": "DEV-MAS-01",
  "descricao": "Demonstração sintética de leite alterado e úbere inflamado durante a triagem. Suposição a validar; não constitui caso clínico validado.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 10
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [
      "leite_alterado",
      "ubere_inflamado"
    ],
    "excrecoes": []
  },
  "respostas": {},
  "limite_dinamico": 0,
  "esperado": {
    "urgencia": "observar",
    "top1": "mastite",
    "faixas": {
      "mastite": [
        79,
        81
      ]
    },
    "alerta": {
      "pausa": false
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "DEV-MAS-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "mastite",
    "top3_contem": [
      "mastite",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "mastite": 80,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "mastite"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "leite_alterado",
    "queda_producao",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

A base canônica planejada prevê uma cobertura clínica maior. Os dois exemplos atuais não substituem esse conjunto nem validação especializada. `limite_dinamico: 0` nos exemplos encerra após a triagem; os limites normais da base continuam 12/25.
