# Casos de teste — documentação gerada

> GERADO por `scripts/gerar_doc_regras.py`; resultados obtidos com `engine.casos.executar_caso`.

Base `v0001`. Casos sintéticos executados: **34**. Aprovados: **34**.

Os casos demonstram integração e comportamento determinístico. Não medem acurácia, sensibilidade ou especificidade clínicas. Os testes unitários são contabilizados separadamente.

| Caso | Resultado | Urgência | Primeira hipótese | Pausa ocorreu |
| --- | --- | --- | --- | --- |
| C-MAS-01 | passou | observar | mastite | não |
| C-MAS-02 | passou | chamar_agora | mastite | não |
| C-MAS-03 | passou | observar | mastite | não |
| C-MET-01 | passou | chamar_agora | metrite | não |
| C-MET-02 | passou | chamar_agora | metrite | não |
| C-MET-03 | passou | sem_problema | acidose | não |
| C-TPB-01 | passou | chamar_agora | tpb | sim |
| C-TPB-02 | passou | chamar_agora | tpb | não |
| C-TPB-03 | passou | sem_problema | acidose | não |
| C-CET-01 | passou | observar | cetose | não |
| C-CET-02 | passou | observar | cetose | não |
| C-CET-03 | passou | observar | cetose | não |
| C-HIP-01 | passou | chamar_agora | hipocalcemia | sim |
| C-HIP-02 | passou | chamar_agora | hipocalcemia | não |
| C-HIP-03 | passou | sem_problema | acidose | não |
| C-DAB-01 | passou | chamar_agora | deslocamento_abomaso | não |
| C-DAB-02 | passou | chamar_agora | deslocamento_abomaso | não |
| C-DAB-03 | passou | sem_problema | acidose | não |
| C-ACI-01 | passou | observar | acidose | não |
| C-ACI-02 | passou | observar | acidose | não |
| C-ACI-03 | passou | sem_problema | acidose | não |
| C-DD-01 | passou | observar | dermatite_digital | não |
| C-DD-02 | passou | observar | dermatite_digital | não |
| C-DD-03 | passou | sem_problema | dermatite_digital | não |
| C-BV-01 | passou | chamar_agora | acidose | sim |
| C-BV-02 | passou | chamar_agora | acidose | sim |
| C-BV-03 | passou | chamar_agora | acidose | não |
| C-COM-01 | passou | chamar_agora | mastite | não |
| C-MODO-01 | passou | chamar_agora | deslocamento_abomaso | não |
| C-LIM-01 | passou | observar | cetose | não |
| C-SAD-01 | passou | sem_problema | acidose | não |
| DEV-BV-01 | passou | chamar_agora | hipocalcemia | sim |
| DEV-MAS-01 | passou | observar | mastite | não |
| C-DAB-DIALOGO | passou | observar | cetose | não |

## C-MAS-01

Mastite: leite alterado e úbere inflamado Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-MAS-01",
  "descricao": "Mastite: leite alterado e úbere inflamado Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 90,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [
      "leite_alterado",
      "ubere_inflamado",
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "top1": "mastite",
    "urgencia": "observar",
    "faixas": {
      "mastite": [
        75,
        100
      ]
    },
    "motivo_parada": "sem_perguntas"
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-MAS-01",
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
    "motivo_parada": "sem_perguntas",
    "bandeiras": [],
    "inconclusivas": [],
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
    "fezes_aquosas_espuma_graos",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-MAS-02

Mastite com sinais sistêmicos Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-MAS-02",
  "descricao": "Mastite com sinais sistêmicos Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 150,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 40.2,
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "leite_alterado",
      "ubere_inflamado"
    ],
    "excrecoes": []
  },
  "respostas": {
    "cmt_reagente": true
  },
  "esperado": {
    "top1": "mastite",
    "urgencia": "chamar_agora",
    "faixas": {
      "mastite": [
        75,
        100
      ]
    },
    "bandeira": "R-BV-05"
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-MAS-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "mastite",
    "top3_contem": [
      "mastite",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "mastite": 88,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "metrite": 0,
      "tpb": 0,
      "hipocalcemia": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [
      "R-BV-05"
    ],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "claudicacao",
    "cmt_reagente",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "mucosas_palidas_ou_ictericas",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-MAS-03

Mastite ambígua: só úbere inflamado Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-MAS-03",
  "descricao": "Mastite ambígua: só úbere inflamado Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 90,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [
      "ubere_inflamado"
    ],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "top1": "mastite",
    "urgencia": "observar",
    "faixas": {
      "mastite": [
        45,
        75
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-MAS-03",
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
      "mastite": 50,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
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
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-MET-01

Metrite no puerpério com corrimento fétido Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-MET-01",
  "descricao": "Metrite no puerpério com corrimento fétido Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 6,
    "retencao_placenta": true
  },
  "triagem": {
    "estado_termico": "quente",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": [
      "corrimento_vaginal"
    ]
  },
  "respostas": {
    "corrimento_fetido": true
  },
  "esperado": {
    "top1": "metrite",
    "urgencia": "chamar_agora",
    "faixas": {
      "metrite": [
        75,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-MET-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "metrite",
    "top3_contem": [
      "metrite",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "metrite": 85,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "tpb": 0,
      "hipocalcemia": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "leite_alterado",
    "queda_producao",
    "retencao_placenta",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-MET-02

Metrite: febre e achados uterinos Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-MET-02",
  "descricao": "Metrite: febre e achados uterinos Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 8,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 39.9,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": [
      "corrimento_vaginal"
    ]
  },
  "respostas": {
    "utero_aumentado_palpacao": true,
    "corrimento_fetido": true
  },
  "esperado": {
    "top1": "metrite",
    "urgencia": "chamar_agora",
    "faixas": {
      "metrite": [
        75,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-MET-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "metrite",
    "top3_contem": [
      "metrite",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "metrite": 85,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "tpb": 0,
      "hipocalcemia": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-MET-03

Metrite ambígua: corrimento sem confirmação de odor Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.

### Entrada e resultado esperado

```json
{
  "id": "C-MET-03",
  "descricao": "Metrite ambígua: corrimento sem confirmação de odor Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 12,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": [
      "corrimento_vaginal"
    ]
  },
  "respostas": {},
  "esperado": {
    "urgencia": "sem_problema",
    "faixas": {
      "metrite": [
        0,
        5
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-MET-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "sem_problema",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-TPB-01

TPB: urina escura, mucosas e carrapatos Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-TPB-01",
  "descricao": "TPB: urina escura, mucosas e carrapatos Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 100,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "quente",
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": [
      "urina_escura"
    ]
  },
  "respostas": {
    "mucosas_palidas_ou_ictericas": true,
    "carrapatos_historico_recente": true
  },
  "esperado": {
    "top1": "tpb",
    "urgencia": "chamar_agora",
    "faixas": {
      "tpb": [
        70,
        100
      ]
    },
    "bandeira": "R-BV-02"
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-TPB-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "tpb",
    "top3_contem": [
      "tpb",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "tpb": 77,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "metrite": 0,
      "hipocalcemia": 0
    },
    "motivo_parada": "sem_perguntas",
    "bandeiras": [
      "R-BV-02"
    ],
    "inconclusivas": [],
    "alerta": {
      "pausa": true
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "carrapatos_historico_recente",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-TPB-02

TPB: febre, urina escura e esfregaço Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-TPB-02",
  "descricao": "TPB: febre, urina escura e esfregaço Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 200,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 40.1,
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": [
      "urina_escura"
    ]
  },
  "respostas": {
    "esfregaco_hemoparasitas": true,
    "mucosas_palidas_ou_ictericas": true
  },
  "esperado": {
    "top1": "tpb",
    "urgencia": "chamar_agora",
    "faixas": {
      "tpb": [
        85,
        100
      ]
    },
    "bandeira": "R-BV-02"
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-TPB-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "tpb",
    "top3_contem": [
      "tpb",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "tpb": 97,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "metrite": 0,
      "hipocalcemia": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [
      "R-BV-02"
    ],
    "inconclusivas": [],
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
    "esfregaco_hemoparasitas",
    "leite_alterado",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-TPB-03

TPB ambígua: calor e carrapatos sem mucosas informadas Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.

### Entrada e resultado esperado

```json
{
  "id": "C-TPB-03",
  "descricao": "TPB ambígua: calor e carrapatos sem mucosas informadas Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 100,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "quente",
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "carrapatos_historico_recente": true
  },
  "esperado": {
    "urgencia": "sem_problema",
    "faixas": {
      "tpb": [
        0,
        5
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-TPB-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "sem_problema",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0,
      "hipocalcemia": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
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
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-CET-01

Cetose: redução do apetite, acetona e recusa de concentrado Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-CET-01",
  "descricao": "Cetose: redução do apetite, acetona e recusa de concentrado Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 25,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "halito_adocicado_acetona": true,
    "recusa_concentrado_come_volumoso": true
  },
  "esperado": {
    "top1": "cetose",
    "urgencia": "observar",
    "faixas": {
      "cetose": [
        75,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-CET-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "cetose",
    "top3_contem": [
      "cetose",
      "deslocamento_abomaso",
      "acidose"
    ],
    "percentuais": {
      "cetose": 83,
      "deslocamento_abomaso": 30,
      "acidose": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
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
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-CET-02

Cetose: BHB acima do limiar Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-CET-02",
  "descricao": "Cetose: BHB acima do limiar Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 30,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.6,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "bhb_sanguineo": 1.8,
    "ping_metalico_flanco_esquerdo": false,
    "flanco_esquerdo_afundado": false
  },
  "esperado": {
    "top1": "cetose",
    "urgencia": "observar",
    "faixas": {
      "cetose": [
        85,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-CET-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "cetose",
    "top3_contem": [
      "cetose",
      "deslocamento_abomaso",
      "acidose"
    ],
    "percentuais": {
      "cetose": 91,
      "deslocamento_abomaso": 30,
      "acidose": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "leite_alterado",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-CET-03

Cetose ambígua: só apetite e produção Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-CET-03",
  "descricao": "Cetose ambígua: só apetite e produção Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 20,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "urgencia": "observar",
    "top3_contem": [
      "cetose",
      "deslocamento_abomaso"
    ],
    "faixas": {
      "cetose": [
        35,
        60
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-CET-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "cetose",
    "top3_contem": [
      "cetose",
      "deslocamento_abomaso",
      "acidose"
    ],
    "percentuais": {
      "cetose": 40,
      "deslocamento_abomaso": 30,
      "acidose": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-HIP-01

Hipocalcemia: decúbito no periparto Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-HIP-01",
  "descricao": "Hipocalcemia: decúbito no periparto Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 1,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "fria",
    "atitude_locomocao": [
      "decubito"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "top1": "hipocalcemia",
    "urgencia": "chamar_agora",
    "faixas": {
      "hipocalcemia": [
        60,
        70
      ]
    },
    "bandeira": "R-BV-01"
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-HIP-01",
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
    "motivo_parada": "sem_perguntas",
    "bandeiras": [
      "R-BV-01"
    ],
    "inconclusivas": [],
    "alerta": {
      "pausa": true
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "flanco_esquerdo_afundado",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "pescoco_em_s",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-HIP-02

Hipocalcemia: hipotermia, apatia e cálcio baixo Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-HIP-02",
  "descricao": "Hipocalcemia: hipotermia, apatia e cálcio baixo Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 2,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 37.2,
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "calcio_serico": 1.1
  },
  "esperado": {
    "top1": "hipocalcemia",
    "urgencia": "chamar_agora",
    "faixas": {
      "hipocalcemia": [
        85,
        100
      ]
    },
    "bandeira": "R-BV-04"
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-HIP-02",
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
      "hipocalcemia": 90,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [
      "R-BV-04"
    ],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "leite_alterado",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-HIP-03

Hipocalcemia ambígua: frio sem decúbito Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.

### Entrada e resultado esperado

```json
{
  "id": "C-HIP-03",
  "descricao": "Hipocalcemia ambígua: frio sem decúbito Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 2,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "fria",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "urgencia": "sem_problema",
    "faixas": {
      "hipocalcemia": [
        0,
        5
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-HIP-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "sem_problema",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "pescoco_em_s",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-DAB-01

Deslocamento de abomaso: redução de ingestão e flanco afundado Caso fictício de regressão; suposição a validar. Observação prévia fictícia de flanco afundado fornecida na ficha do executor; não comprova coleta pelo diálogo/API. Ver R15.

### Entrada e resultado esperado

```json
{
  "id": "C-DAB-01",
  "descricao": "Deslocamento de abomaso: redução de ingestão e flanco afundado Caso fictício de regressão; suposição a validar. Observação prévia fictícia de flanco afundado fornecida na ficha do executor; não comprova coleta pelo diálogo/API. Ver R15.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 35,
    "retencao_placenta": false,
    "flanco_esquerdo_afundado": true
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "top1": "deslocamento_abomaso",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso": [
        50,
        75
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-DAB-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "deslocamento_abomaso",
    "top3_contem": [
      "deslocamento_abomaso",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso": 58,
      "cetose": 40,
      "acidose": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_perguntas",
    "bandeiras": [],
    "inconclusivas": [],
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
    "fezes_aquosas_espuma_graos",
    "flanco_esquerdo_afundado",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-DAB-02

Deslocamento de abomaso: ping metálico Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-DAB-02",
  "descricao": "Deslocamento de abomaso: ping metálico Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 20,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.5,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "ping_metalico_flanco_esquerdo": true
  },
  "esperado": {
    "top1": "deslocamento_abomaso",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso": [
        85,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-DAB-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "deslocamento_abomaso",
    "top3_contem": [
      "deslocamento_abomaso",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso": 93,
      "cetose": 40,
      "acidose": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "mucosas_palidas_ou_ictericas",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-DAB-03

Deslocamento de abomaso ambíguo: apetite e flanco Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.

### Entrada e resultado esperado

```json
{
  "id": "C-DAB-03",
  "descricao": "Deslocamento de abomaso ambíguo: apetite e flanco Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 35,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "flanco_esquerdo_afundado": true
  },
  "esperado": {
    "urgencia": "sem_problema",
    "faixas": {
      "deslocamento_abomaso": [
        0,
        5
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-DAB-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "sem_problema",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
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
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-ACI-01

Acidose: diarreia após mudança de concentrado Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-ACI-01",
  "descricao": "Acidose: diarreia após mudança de concentrado Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 80,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": [
      "diarreia"
    ]
  },
  "respostas": {
    "mudanca_abrupta_concentrado": true,
    "fezes_aquosas_espuma_graos": true
  },
  "esperado": {
    "top1": "acidose",
    "urgencia": "observar",
    "faixas": {
      "acidose": [
        75,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-ACI-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 85,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
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
    "fezes_aquosas_espuma_graos",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "mudanca_abrupta_concentrado",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-ACI-02

Acidose: pH ruminal baixo Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-ACI-02",
  "descricao": "Acidose: pH ruminal baixo Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 60,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.7,
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": [
      "diarreia"
    ]
  },
  "respostas": {
    "ph_ruminal": 5.2
  },
  "esperado": {
    "top1": "acidose",
    "urgencia": "observar",
    "faixas": {
      "acidose": [
        85,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-ACI-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 92,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "leite_alterado",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-ACI-03

Acidose ambígua: diarreia e fezes com grãos Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.

### Entrada e resultado esperado

```json
{
  "id": "C-ACI-03",
  "descricao": "Acidose ambígua: diarreia e fezes com grãos Caso fictício de regressão; suposição a validar. Limitação documentada em R15: o sinal adicional não é solicitado no diálogo da v0001.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 80,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": [
      "diarreia"
    ]
  },
  "respostas": {
    "fezes_aquosas_espuma_graos": true
  },
  "esperado": {
    "urgencia": "sem_problema",
    "faixas": {
      "acidose": [
        0,
        5
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-ACI-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "sem_problema",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
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
    "mucosas_palidas_ou_ictericas",
    "mudanca_abrupta_concentrado",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-DD-01

Dermatite digital: claudicação e dor ao flexionar o talão Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-DD-01",
  "descricao": "Dermatite digital: claudicação e dor ao flexionar o talão Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 150,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [
      "claudicacao"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "dor_flexao_talao": true
  },
  "esperado": {
    "top1": "dermatite_digital",
    "urgencia": "observar",
    "faixas": {
      "dermatite_digital": [
        60,
        75
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-DD-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "dermatite_digital",
    "top3_contem": [
      "dermatite_digital",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "dermatite_digital": 65,
      "acidose": 0,
      "cetose": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_perguntas",
    "bandeiras": [],
    "inconclusivas": [],
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
    "dor_flexao_talao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-DD-02

Dermatite digital: lesão erosiva no talão Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-DD-02",
  "descricao": "Dermatite digital: lesão erosiva no talão Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 150,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.5,
    "atitude_locomocao": [
      "claudicacao"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "lesao_erosiva_talao_morango": true
  },
  "esperado": {
    "top1": "dermatite_digital",
    "urgencia": "observar",
    "faixas": {
      "dermatite_digital": [
        85,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-DD-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "dermatite_digital",
    "top3_contem": [
      "dermatite_digital",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "dermatite_digital": 90,
      "acidose": 0,
      "cetose": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-DD-03

Dermatite digital ambígua: claudicação sem inspeção de lesão Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-DD-03",
  "descricao": "Dermatite digital ambígua: claudicação sem inspeção de lesão Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 150,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [
      "claudicacao"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "urgencia": "sem_problema",
    "faixas": {
      "dermatite_digital": [
        25,
        35
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-DD-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "sem_problema",
    "top1": "dermatite_digital",
    "top3_contem": [
      "dermatite_digital",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "dermatite_digital": 30,
      "acidose": 0,
      "cetose": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_perguntas",
    "bandeiras": [],
    "inconclusivas": [],
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
    "dor_flexao_talao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-BV-01

Bandeira de decúbito isolado, fora do periparto Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-BV-01",
  "descricao": "Bandeira de decúbito isolado, fora do periparto Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 200,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [
      "decubito",
      "apatia"
    ],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "urgencia": "chamar_agora",
    "bandeira": "R-BV-01",
    "alerta": {
      "pausa": true
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-BV-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [
      "R-BV-01"
    ],
    "inconclusivas": [],
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
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-BV-02

Bandeira de apetite ausente com apatia Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-BV-02",
  "descricao": "Bandeira de apetite ausente com apatia Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 100,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "ausente",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "urgencia": "chamar_agora",
    "bandeira": "R-BV-03",
    "alerta": {
      "pausa": true
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-BV-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [
      "R-BV-03"
    ],
    "inconclusivas": [],
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
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-BV-03

Bandeira de febre alta isolada Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-BV-03",
  "descricao": "Bandeira de febre alta isolada Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 100,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 41.3,
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "urgencia": "chamar_agora",
    "bandeira": "R-BV-06",
    "alerta": {
      "pausa": false
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-BV-03",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0,
      "hipocalcemia": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [
      "R-BV-06"
    ],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "fita_urina_corpos_cetonicos",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "mucosas_palidas_ou_ictericas",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "retencao_placenta",
    "temperatura_retal",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-COM-01

Comorbidade: mastite e metrite no puerpério Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-COM-01",
  "descricao": "Comorbidade: mastite e metrite no puerpério Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 5,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [
      "leite_alterado",
      "ubere_inflamado"
    ],
    "excrecoes": [
      "corrimento_vaginal"
    ]
  },
  "respostas": {
    "corrimento_fetido": true
  },
  "esperado": {
    "urgencia": "chamar_agora",
    "top3_contem": [
      "mastite",
      "metrite"
    ],
    "faixas": {
      "mastite": [
        75,
        100
      ],
      "metrite": [
        70,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-COM-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "mastite",
    "top3_contem": [
      "mastite",
      "metrite",
      "acidose"
    ],
    "percentuais": {
      "mastite": 80,
      "metrite": 74,
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_perguntas",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "flanco_esquerdo_afundado",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-MODO-01

Troca produtor para veterinário preserva evidência e acrescenta ping Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-MODO-01",
  "descricao": "Troca produtor para veterinário preserva evidência e acrescenta ping Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 40,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "flanco_esquerdo_afundado": true
  },
  "esperado": {
    "top1": "deslocamento_abomaso",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso": [
        85,
        100
      ]
    }
  },
  "continuacao": {
    "modo": "veterinario",
    "triagem": {
      "estado_termico": 38.4
    },
    "respostas": {
      "ping_metalico_flanco_esquerdo": true
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-MODO-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "deslocamento_abomaso",
    "top3_contem": [
      "deslocamento_abomaso",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso": 93,
      "cetose": 40,
      "acidose": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "mucosas_palidas_ou_ictericas",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "retencao_placenta",
    "temperatura_retal",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-LIM-01

Limite de três perguntas dinâmicas em quadro inespecífico Caso fictício de regressão; suposição a validar. Só cetose supera o limiar estrito de 0,35; acidose=0,35 e dermatite=0,30 não são inconclusivas.

### Entrada e resultado esperado

```json
{
  "id": "C-LIM-01",
  "descricao": "Limite de três perguntas dinâmicas em quadro inespecífico Caso fictício de regressão; suposição a validar. Só cetose supera o limiar estrito de 0,35; acidose=0,35 e dermatite=0,30 não são inconclusivas.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 10,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [
      "claudicacao"
    ],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": [
      "diarreia"
    ]
  },
  "respostas": {},
  "esperado": {
    "urgencia": "observar",
    "motivo_parada": "limite",
    "inconclusivas": [
      "cetose"
    ],
    "faixas": {
      "cetose": [
        35,
        70
      ]
    }
  },
  "limite_dinamico": 3
}
```

### Resultado observado

```json
{
  "caso_id": "C-LIM-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "cetose",
    "top3_contem": [
      "cetose",
      "acidose",
      "dermatite_digital"
    ],
    "percentuais": {
      "cetose": 40,
      "acidose": 35,
      "dermatite_digital": 30,
      "deslocamento_abomaso": 30,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "cetose"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-SAD-01

Triagem sem alterações Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-SAD-01",
  "descricao": "Triagem sem alterações Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 120,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {},
  "esperado": {
    "urgencia": "sem_problema",
    "faixas": {
      "mastite": [
        0,
        20
      ],
      "metrite": [
        0,
        20
      ],
      "tpb": [
        0,
        20
      ],
      "cetose": [
        0,
        20
      ],
      "hipocalcemia": [
        0,
        20
      ],
      "deslocamento_abomaso": [
        0,
        20
      ],
      "acidose": [
        0,
        20
      ],
      "dermatite_digital": [
        0,
        20
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-SAD-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "sem_problema",
    "top1": "acidose",
    "top3_contem": [
      "acidose",
      "cetose",
      "dermatite_digital"
    ],
    "percentuais": {
      "acidose": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
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
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

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

## C-DAB-DIALOGO

Regressão da limitação R15: sem observação prévia do flanco, o diálogo não a solicita. Caso fictício; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-DAB-DIALOGO",
  "descricao": "Regressão da limitação R15: sem observação prévia do flanco, o diálogo não a solicita. Caso fictício; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 35,
    "retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "flanco_esquerdo_afundado": true
  },
  "esperado": {
    "urgencia": "observar",
    "top1": "cetose",
    "faixas": {
      "deslocamento_abomaso": [
        25,
        35
      ],
      "cetose": [
        35,
        45
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-DAB-DIALOGO",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "cetose",
    "top3_contem": [
      "cetose",
      "deslocamento_abomaso",
      "acidose"
    ],
    "percentuais": {
      "cetose": 40,
      "deslocamento_abomaso": 30,
      "acidose": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "mastite": 0,
      "metrite": 0,
      "tpb": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
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
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "retencao_placenta",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

Este documento executa 34 cenário(s) sintético(s); não substitui validação especializada. Os desvios em relação à especificação e os limites da coleta estão no registro de riscos. `limite_dinamico: 0`, quando presente no caso, encerra após a triagem; os limites normais da base são 12/25.
