# Casos de teste — documentação gerada

> GERADO por `scripts/gerar_doc_regras.py`; resultados obtidos com `engine.casos.executar_caso`.

Base `v0006`. Casos sintéticos executados: **60**. Aprovados: **60**.

Os casos demonstram integração e comportamento determinístico. Não medem acurácia, sensibilidade ou especificidade clínicas. Os testes unitários são contabilizados separadamente.

| Caso | Resultado | Urgência | Primeira hipótese | Pausa ocorreu |
| --- | --- | --- | --- | --- |
| C-MAS-01 | passou | observar | mastite | não |
| C-MAS-02 | passou | chamar_agora | mastite | não |
| C-MAS-03 | passou | observar | mastite | não |
| C-MET-01 | passou | chamar_agora | metrite | não |
| C-MET-02 | passou | chamar_agora | metrite | não |
| C-MET-03 | passou | sem_problema | brucelose | não |
| C-TPB-01 | passou | chamar_agora | tpb | sim |
| C-TPB-02 | passou | chamar_agora | tpb | não |
| C-TPB-03 | passou | sem_problema | pneumonia | não |
| C-CET-01 | passou | observar | cetose | não |
| C-CET-02 | passou | observar | cetose | não |
| C-CET-03 | passou | observar | cetose | não |
| C-HIP-01 | passou | chamar_agora | hipocalcemia | sim |
| C-HIP-02 | passou | chamar_agora | hipocalcemia | não |
| C-HIP-03 | passou | sem_problema | acidose | não |
| C-DAB-01 | passou | chamar_agora | deslocamento_abomaso_esquerda | não |
| C-DAB-02 | passou | chamar_agora | deslocamento_abomaso_esquerda | não |
| C-DAB-03 | passou | sem_problema | acidose | não |
| C-ACI-01 | passou | observar | acidose | não |
| C-ACI-02 | passou | observar | acidose | não |
| C-ACI-03 | passou | sem_problema | acidose | não |
| C-DD-01 | passou | observar | dermatite_digital | não |
| C-DD-02 | passou | observar | dermatite_digital | não |
| C-DD-03 | passou | sem_problema | dermatite_digital | não |
| C-BV-01 | passou | chamar_agora | hipocalcemia | sim |
| C-BV-02 | passou | chamar_agora | acidose | sim |
| C-BV-03 | passou | chamar_agora | acidose | não |
| C-COM-01 | passou | chamar_agora | mastite | não |
| C-MODO-01 | passou | chamar_agora | deslocamento_abomaso_esquerda | não |
| C-LIM-01 | passou | observar | cetose | não |
| C-SAD-01 | passou | sem_problema | acidose | não |
| DEV-BV-01 | passou | chamar_agora | hipocalcemia | sim |
| DEV-MAS-01 | passou | observar | mastite | não |
| C-DAB-DIALOGO | passou | observar | cetose | não |
| C-N-DAD-01 | passou | chamar_agora | deslocamento_abomaso_direita | não |
| C-N-DAD-02 | passou | chamar_agora | deslocamento_abomaso_direita | não |
| C-N-TES-01 | passou | chamar_agora | timpanismo_espumoso | não |
| C-N-TES-02 | passou | chamar_agora | timpanismo_espumoso | não |
| C-N-TGA-01 | passou | chamar_agora | timpanismo_gasoso | não |
| C-N-TGA-02 | passou | chamar_agora | timpanismo_gasoso | não |
| C-N-RPL-01 | passou | observar | retencao_placenta | não |
| C-N-RPL-02 | passou | observar | retencao_placenta | não |
| C-N-PNE-01 | passou | observar | pneumonia | não |
| C-N-PNE-02 | passou | observar | pneumonia | não |
| C-N-RPT-01 | passou | chamar_agora | reticulopericardite_traumatica | não |
| C-N-RPT-02 | passou | chamar_agora | reticulopericardite_traumatica | não |
| C-N-HMG-01 | passou | chamar_agora | hipomagnesemia | não |
| C-N-HMG-02 | passou | chamar_agora | hipomagnesemia | não |
| C-N-BRU-01 | passou | chamar_agora | brucelose | não |
| C-N-BRU-02 | passou | chamar_agora | brucelose | não |
| C-N-LEP-01 | passou | chamar_agora | leptospirose | não |
| C-N-LEP-02 | passou | chamar_agora | leptospirose | não |
| C-N-IBR-01 | passou | observar | ibr | não |
| C-N-IBR-02 | passou | observar | ibr | não |
| C-N-BVD-01 | passou | chamar_agora | bvd | não |
| C-N-BVD-02 | passou | chamar_agora | bvd | não |
| C-N-TUB-01 | passou | chamar_agora | tuberculose | não |
| C-N-TUB-02 | passou | chamar_agora | tuberculose | não |
| C-EXC-DAB | passou | chamar_agora | deslocamento_abomaso_direita | não |
| C-EXC-TIM | passou | chamar_agora | timpanismo_espumoso | não |

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
    "historico_retencao_placenta": false
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
      "tuberculose",
      "acidose"
    ],
    "percentuais": {
      "mastite": 80,
      "tuberculose": 5,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "retencao_placenta": 0
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
    "emagrecimento_progressivo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "focinho_avermelhado",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "leite_com_sangue",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
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
    "historico_retencao_placenta": false
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
      "pneumonia",
      "acidose"
    ],
    "percentuais": {
      "mastite": 88,
      "pneumonia": 10,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_direita": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
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
    "aborto_recente",
    "agitacao",
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "claudicacao",
    "cmt_reagente",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "edema_barbela",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "gas_livre_sonda",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "magnesio_serico",
    "mucosas_palidas_ou_ictericas",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
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
    "historico_retencao_placenta": false
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
      "brucelose"
    ],
    "percentuais": {
      "mastite": 50,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
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
    "historico_retencao_placenta": true
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
      "retencao_placenta",
      "acidose"
    ],
    "percentuais": {
      "metrite": 85,
      "retencao_placenta": 41,
      "acidose": 5,
      "brucelose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
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
    "aborto_recente",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "historico_retencao_placenta",
    "leite_alterado",
    "membranas_expostas_vulva",
    "placenta_nao_expulsa_24h",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
      "brucelose"
    ],
    "percentuais": {
      "metrite": 85,
      "acidose": 5,
      "brucelose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "aborto_recente",
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "claudicacao",
    "corrimento_fetido",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "magnesio_serico",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
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
    "historico_retencao_placenta": false
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
    "top1": "brucelose",
    "top3_contem": [
      "brucelose",
      "acidose",
      "bvd"
    ],
    "percentuais": {
      "brucelose": 5,
      "acidose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
      "leptospirose",
      "pneumonia"
    ],
    "percentuais": {
      "tpb": 77,
      "leptospirose": 5,
      "pneumonia": 5,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
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
    "aborto_recente",
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
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "olhos_lacrimejando",
    "queda_producao",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
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
    "historico_retencao_placenta": false
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
      "pneumonia",
      "acidose"
    ],
    "percentuais": {
      "tpb": 97,
      "pneumonia": 10,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "leptospirose": 0,
      "retencao_placenta": 0
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
    "espuma_sonda",
    "extremidades",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
    "top1": "pneumonia",
    "top3_contem": [
      "pneumonia",
      "acidose",
      "brucelose"
    ],
    "percentuais": {
      "pneumonia": 5,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "aborto_recente",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda",
      "acidose"
    ],
    "percentuais": {
      "cetose": 84,
      "deslocamento_abomaso_esquerda": 33,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fezes_escassas",
    "halito_adocicado_acetona",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda",
      "acidose"
    ],
    "percentuais": {
      "cetose": 91,
      "deslocamento_abomaso_esquerda": 33,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "secrecao_nasal",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "tosse",
    "tuberculina_reagente",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda"
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
      "deslocamento_abomaso_esquerda",
      "acidose"
    ],
    "percentuais": {
      "cetose": 43,
      "deslocamento_abomaso_esquerda": 33,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fezes_escassas",
    "halito_adocicado_acetona",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
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
    "historico_retencao_placenta": false
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
      "brucelose"
    ],
    "percentuais": {
      "hipocalcemia": 64,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0
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
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fezes_escassas",
    "flanco_esquerdo_afundado",
    "halito_adocicado_acetona",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "membranas_expostas_vulva",
    "mucosas_palidas_ou_ictericas",
    "pescoco_em_s",
    "placenta_nao_expulsa_24h",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
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
    "historico_retencao_placenta": false
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
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_direita": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0
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
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
      "brucelose",
      "bvd"
    ],
    "percentuais": {
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0
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
    "historico_retencao_placenta",
    "leite_alterado",
    "membranas_expostas_vulva",
    "mucosas_palidas_ou_ictericas",
    "pescoco_em_s",
    "placenta_nao_expulsa_24h",
    "queda_producao",
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
    "historico_retencao_placenta": false,
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
    "top1": "deslocamento_abomaso_esquerda",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso_esquerda": [
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
    "top1": "deslocamento_abomaso_esquerda",
    "top3_contem": [
      "deslocamento_abomaso_esquerda",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso_esquerda": 60,
      "cetose": 43,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0,
      "deslocamento_abomaso_direita": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "deslocamento_abomaso_esquerda",
      "cetose"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "flanco_esquerdo_afundado",
    "halito_adocicado_acetona",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "outros_animais_estufados",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "respiracao_ofegante",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
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
    "historico_retencao_placenta": false
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
    "top1": "deslocamento_abomaso_esquerda",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso_esquerda": [
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
    "top1": "deslocamento_abomaso_esquerda",
    "top3_contem": [
      "deslocamento_abomaso_esquerda",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso_esquerda": 93,
      "cetose": 43,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "reticulopericardite_traumatica": 0,
      "retencao_placenta": 0,
      "deslocamento_abomaso_direita": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "gas_livre_sonda",
    "halito_adocicado_acetona",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "magnesio_serico",
    "mucosas_palidas_ou_ictericas",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "secrecao_nasal",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "teste_caneca_grumos",
    "tosse",
    "tuberculina_reagente",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda": [
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
      "deslocamento_abomaso_esquerda"
    ],
    "percentuais": {
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fezes_escassas",
    "halito_adocicado_acetona",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "teste_caneca_grumos",
    "tosse",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda"
    ],
    "percentuais": {
      "acidose": 86,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "bvd": 0,
      "retencao_placenta": 0
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
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "historico_retencao_placenta",
    "leite_alterado",
    "mudanca_abrupta_concentrado",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_direita"
    ],
    "percentuais": {
      "acidose": 93,
      "cetose": 5,
      "deslocamento_abomaso_direita": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "mudanca_abrupta_concentrado",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "temperatura_retal",
    "tuberculina_reagente",
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
    "historico_retencao_placenta": false
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
      "brucelose",
      "bvd"
    ],
    "percentuais": {
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "feridas_boca",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "mudanca_abrupta_concentrado",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
      "brucelose"
    ],
    "percentuais": {
      "dermatite_digital": 65,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
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
    "historico_retencao_placenta": false
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
      "brucelose"
    ],
    "percentuais": {
      "dermatite_digital": 90,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "magnesio_serico",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "tuberculina_reagente",
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
    "historico_retencao_placenta": false
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
      "brucelose"
    ],
    "percentuais": {
      "dermatite_digital": 30,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "dor_flexao_talao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
    "top1": "hipocalcemia",
    "top3_contem": [
      "hipocalcemia",
      "hipomagnesemia",
      "acidose"
    ],
    "percentuais": {
      "hipocalcemia": 20,
      "hipomagnesemia": 5,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "fezes_aquosas_espuma_graos",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_direita"
    ],
    "percentuais": {
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_direita": 5,
      "deslocamento_abomaso_esquerda": 5,
      "timpanismo_gasoso": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "teste_caneca_grumos",
    "tosse",
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
    "historico_retencao_placenta": false
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
      "brucelose",
      "bvd"
    ],
    "percentuais": {
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
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
    "aborto_recente",
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "edema_barbela",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "magnesio_serico",
    "mucosas_palidas_ou_ictericas",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
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
    "historico_retencao_placenta": false
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
      "retencao_placenta"
    ],
    "percentuais": {
      "mastite": 80,
      "metrite": 74,
      "retencao_placenta": 10,
      "brucelose": 5,
      "acidose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0
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
    "fezes_escassas",
    "flanco_esquerdo_afundado",
    "halito_adocicado_acetona",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "membranas_expostas_vulva",
    "mucosas_palidas_ou_ictericas",
    "placenta_nao_expulsa_24h",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
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
    "historico_retencao_placenta": false
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
    "top1": "deslocamento_abomaso_esquerda",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso_esquerda": [
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
    "top1": "deslocamento_abomaso_esquerda",
    "top3_contem": [
      "deslocamento_abomaso_esquerda",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso_esquerda": 93,
      "cetose": 43,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "reticulopericardite_traumatica": 0,
      "retencao_placenta": 0,
      "deslocamento_abomaso_direita": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fezes_escassas",
    "fita_urina_corpos_cetonicos",
    "gas_livre_sonda",
    "halito_adocicado_acetona",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "magnesio_serico",
    "mucosas_palidas_ou_ictericas",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "secrecao_nasal",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "teste_caneca_grumos",
    "tosse",
    "tuberculina_reagente",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda"
    ],
    "percentuais": {
      "cetose": 43,
      "acidose": 38,
      "deslocamento_abomaso_esquerda": 33,
      "dermatite_digital": 30,
      "brucelose": 0,
      "bvd": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "cetose",
      "acidose"
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
    "distensao_flanco_esquerdo",
    "extremidades",
    "historico_retencao_placenta",
    "leite_alterado",
    "mudanca_abrupta_concentrado",
    "queda_producao",
    "tosse",
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda": [
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
      "brucelose",
      "bvd"
    ],
    "percentuais": {
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
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
      "hipomagnesemia",
      "acidose"
    ],
    "percentuais": {
      "hipocalcemia": 64,
      "hipomagnesemia": 5,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0
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
      "brucelose"
    ],
    "percentuais": {
      "mastite": 80,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "historico_retencao_placenta": false
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
      "deslocamento_abomaso_esquerda": [
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
      "deslocamento_abomaso_esquerda",
      "acidose"
    ],
    "percentuais": {
      "cetose": 43,
      "deslocamento_abomaso_esquerda": 33,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "sem_potencial",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fezes_escassas",
    "halito_adocicado_acetona",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-DAD-01

Deslocamento à direita: barriga estufada à direita, pouco esterco e desidratação Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-DAD-01",
  "descricao": "Deslocamento à direita: barriga estufada à direita, pouco esterco e desidratação Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 20,
    "historico_retencao_placenta": false
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
    "distensao_flanco_direito": true,
    "fezes_escassas": true,
    "desidratacao": true
  },
  "esperado": {
    "top1": "deslocamento_abomaso_direita",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso_direita": [
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
  "caso_id": "C-N-DAD-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "deslocamento_abomaso_direita",
    "top3_contem": [
      "deslocamento_abomaso_direita",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso_direita": 75,
      "cetose": 43,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0,
      "deslocamento_abomaso_esquerda": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "deslocamento_abomaso_direita",
      "cetose"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "respiracao_ofegante",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-DAD-02

Deslocamento à direita: ping no flanco direito Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-DAD-02",
  "descricao": "Deslocamento à direita: ping no flanco direito Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 15,
    "historico_retencao_placenta": false
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
    "ping_flanco_direito": true,
    "ping_metalico_flanco_esquerdo": false
  },
  "esperado": {
    "top1": "deslocamento_abomaso_direita",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso_direita": [
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
  "caso_id": "C-N-DAD-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "deslocamento_abomaso_direita",
    "top3_contem": [
      "deslocamento_abomaso_direita",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso_direita": 90,
      "cetose": 43,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0,
      "deslocamento_abomaso_esquerda": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "gas_livre_sonda",
    "halito_adocicado_acetona",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "magnesio_serico",
    "mucosas_palidas_ou_ictericas",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "secrecao_nasal",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "teste_caneca_grumos",
    "tosse",
    "tuberculina_reagente",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-TES-01

Timpanismo espumoso: barriga estufada após leguminosa, outras vacas estufadas Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-TES-01",
  "descricao": "Timpanismo espumoso: barriga estufada após leguminosa, outras vacas estufadas Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 120,
    "historico_retencao_placenta": false
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
    "distensao_flanco_esquerdo": true,
    "pasto_leguminosa_recente": true,
    "outros_animais_estufados": true
  },
  "esperado": {
    "top1": "timpanismo_espumoso",
    "urgencia": "chamar_agora",
    "faixas": {
      "timpanismo_espumoso": [
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
  "caso_id": "C-N-TES-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "timpanismo_espumoso",
    "top3_contem": [
      "timpanismo_espumoso",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "timpanismo_espumoso": 79,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "tpb": 0,
      "tuberculose": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "timpanismo_gasoso": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "timpanismo_espumoso"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "desidratacao",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "emagrecimento_progressivo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "focinho_avermelhado",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "outros_animais_estufados",
    "pasto_leguminosa_recente",
    "queda_producao",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-TES-02

Timpanismo espumoso: espuma pela sonda Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-TES-02",
  "descricao": "Timpanismo espumoso: espuma pela sonda Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 110,
    "historico_retencao_placenta": false
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
    "espuma_sonda": true,
    "distensao_flanco_esquerdo": true
  },
  "esperado": {
    "top1": "timpanismo_espumoso",
    "urgencia": "chamar_agora",
    "faixas": {
      "timpanismo_espumoso": [
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
  "caso_id": "C-N-TES-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "timpanismo_espumoso",
    "top3_contem": [
      "timpanismo_espumoso",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "timpanismo_espumoso": 90,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "tpb": 0,
      "tuberculose": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "timpanismo_gasoso": 0
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
    "distensao_flanco_esquerdo",
    "espuma_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-TGA-01

Timpanismo gasoso: barriga estufada com engasgo, sem leguminosa Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-TGA-01",
  "descricao": "Timpanismo gasoso: barriga estufada com engasgo, sem leguminosa Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 130,
    "historico_retencao_placenta": false
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
    "distensao_flanco_esquerdo": true,
    "engasgo": true,
    "pasto_leguminosa_recente": false
  },
  "esperado": {
    "top1": "timpanismo_gasoso",
    "urgencia": "chamar_agora",
    "faixas": {
      "timpanismo_gasoso": [
        55,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-TGA-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "timpanismo_gasoso",
    "top3_contem": [
      "timpanismo_gasoso",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "timpanismo_gasoso": 60,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "tpb": 0,
      "tuberculose": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "timpanismo_espumoso": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "timpanismo_gasoso"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "desidratacao",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "emagrecimento_progressivo",
    "engasgo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "focinho_avermelhado",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "pasto_leguminosa_recente",
    "queda_producao",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-TGA-02

Timpanismo gasoso: gás livre pela sonda Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-TGA-02",
  "descricao": "Timpanismo gasoso: gás livre pela sonda Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 140,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.7,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "gas_livre_sonda": true,
    "espuma_sonda": false,
    "distensao_flanco_esquerdo": true
  },
  "esperado": {
    "top1": "timpanismo_gasoso",
    "urgencia": "chamar_agora",
    "faixas": {
      "timpanismo_gasoso": [
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
  "caso_id": "C-N-TGA-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "timpanismo_gasoso",
    "top3_contem": [
      "timpanismo_gasoso",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "timpanismo_gasoso": 90,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "tpb": 0,
      "tuberculose": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "timpanismo_espumoso": 0
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
    "distensao_flanco_esquerdo",
    "espuma_sonda",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-RPL-01

Retenção de placenta: restos de placenta na vulva no segundo dia Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-RPL-01",
  "descricao": "Retenção de placenta: restos de placenta na vulva no segundo dia Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 2,
    "historico_retencao_placenta": false
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
  "respostas": {
    "membranas_expostas_vulva": true,
    "placenta_nao_expulsa_24h": true
  },
  "esperado": {
    "top1": "retencao_placenta",
    "urgencia": "observar",
    "faixas": {
      "retencao_placenta": [
        80,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-RPL-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "retencao_placenta",
    "top3_contem": [
      "retencao_placenta",
      "brucelose",
      "acidose"
    ],
    "percentuais": {
      "retencao_placenta": 81,
      "brucelose": 5,
      "acidose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0
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
    "historico_retencao_placenta",
    "leite_alterado",
    "membranas_expostas_vulva",
    "queda_producao",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-RPL-02

Retenção de placenta: membranas retidas ao exame Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-RPL-02",
  "descricao": "Retenção de placenta: membranas retidas ao exame Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 3,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.8,
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "palpacao_membranas_retidas": true
  },
  "esperado": {
    "top1": "retencao_placenta",
    "urgencia": "observar",
    "faixas": {
      "retencao_placenta": [
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
  "caso_id": "C-N-RPL-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "retencao_placenta",
    "top3_contem": [
      "retencao_placenta",
      "acidose",
      "brucelose"
    ],
    "percentuais": {
      "retencao_placenta": 90,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "palpacao_membranas_retidas",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "temperatura_retal",
    "tuberculina_reagente",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-PNE-01

Pneumonia: tosse, respiração com esforço e catarro Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-PNE-01",
  "descricao": "Pneumonia: tosse, respiração com esforço e catarro Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 150,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "quente",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "tosse": true,
    "respiracao_ofegante": true,
    "secrecao_nasal": true,
    "distensao_flanco_esquerdo": false
  },
  "esperado": {
    "top1": "pneumonia",
    "urgencia": "observar",
    "faixas": {
      "pneumonia": [
        55,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-PNE-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "pneumonia",
    "top3_contem": [
      "pneumonia",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "pneumonia": 62,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "reticulopericardite_traumatica": 5,
      "ibr": 2,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "pneumonia"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "aborto_recente",
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "emagrecimento_progressivo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "focinho_avermelhado",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-PNE-02

Pneumonia: febre e crepitações à auscultação Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-PNE-02",
  "descricao": "Pneumonia: febre e crepitações à auscultação Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 160,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 40.0,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "ausculta_crepitacoes": true,
    "tosse": true
  },
  "esperado": {
    "top1": "pneumonia",
    "urgencia": "observar",
    "faixas": {
      "pneumonia": [
        80,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-PNE-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "pneumonia",
    "top3_contem": [
      "pneumonia",
      "reticulopericardite_traumatica",
      "acidose"
    ],
    "percentuais": {
      "pneumonia": 80,
      "reticulopericardite_traumatica": 10,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "ibr": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
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
    "ausculta_crepitacoes",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-RPT-01

Reticulopericardite: costas arqueadas e gemido Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-RPT-01",
  "descricao": "Reticulopericardite: costas arqueadas e gemido Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 100,
    "historico_retencao_placenta": false
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
    "costas_arqueadas": true,
    "gemido": true
  },
  "esperado": {
    "top1": "reticulopericardite_traumatica",
    "urgencia": "chamar_agora",
    "faixas": {
      "reticulopericardite_traumatica": [
        65,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-RPT-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "reticulopericardite_traumatica",
    "top3_contem": [
      "reticulopericardite_traumatica",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "reticulopericardite_traumatica": 70,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "reticulopericardite_traumatica"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "desidratacao",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "gemido",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "respiracao_ofegante",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-RPT-02

Reticulopericardite: prova de dor reticular positiva Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-RPT-02",
  "descricao": "Reticulopericardite: prova de dor reticular positiva Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 100,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 39.6,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "prova_dor_reticular": true,
    "ping_metalico_flanco_esquerdo": false
  },
  "esperado": {
    "top1": "reticulopericardite_traumatica",
    "urgencia": "chamar_agora",
    "faixas": {
      "reticulopericardite_traumatica": [
        80,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-RPT-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "reticulopericardite_traumatica",
    "top3_contem": [
      "reticulopericardite_traumatica",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "reticulopericardite_traumatica": 86,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "ibr": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "secrecao_nasal",
    "sorologia_brucelose_reagente",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-HMG-01

Hipomagnesemia: tremores e agitação após pasto novo Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-HMG-01",
  "descricao": "Hipomagnesemia: tremores e agitação após pasto novo Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 60,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "tremores": true,
    "agitacao": true,
    "pasto_novo_adubado": true
  },
  "esperado": {
    "top1": "hipomagnesemia",
    "urgencia": "chamar_agora",
    "faixas": {
      "hipomagnesemia": [
        65,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-HMG-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "hipomagnesemia",
    "top3_contem": [
      "hipomagnesemia",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "hipomagnesemia": 72,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "hipomagnesemia"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "desidratacao",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "outros_animais_estufados",
    "pasto_novo_adubado",
    "queda_producao",
    "respiracao_ofegante",
    "teste_caneca_grumos",
    "tosse",
    "tremores",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-HMG-02

Hipomagnesemia: magnésio sérico baixo Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-HMG-02",
  "descricao": "Hipomagnesemia: magnésio sérico baixo Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 60,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.5,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "magnesio_serico": 0.8,
    "tremores": true
  },
  "esperado": {
    "top1": "hipomagnesemia",
    "urgencia": "chamar_agora",
    "faixas": {
      "hipomagnesemia": [
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
  "caso_id": "C-N-HMG-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "hipomagnesemia",
    "top3_contem": [
      "hipomagnesemia",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "hipomagnesemia": 90,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipocalcemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
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
    "distensao_flanco_esquerdo",
    "espuma_sonda",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-BRU-01

Brucelose: aborto, retenção de placenta e higroma Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-BRU-01",
  "descricao": "Brucelose: aborto, retenção de placenta e higroma Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 40,
    "historico_retencao_placenta": true
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
  "respostas": {
    "aborto_recente": true,
    "higroma": true,
    "vacinada_brucelose": false
  },
  "esperado": {
    "top1": "brucelose",
    "urgencia": "chamar_agora",
    "faixas": {
      "brucelose": [
        60,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-BRU-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "brucelose",
    "top3_contem": [
      "brucelose",
      "acidose",
      "bvd"
    ],
    "percentuais": {
      "brucelose": 66,
      "acidose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "sem_perguntas",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "aborto_recente",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "fezes_escassas",
    "flanco_esquerdo_afundado",
    "halito_adocicado_acetona",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-BRU-02

Brucelose: sorologia reagente Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-BRU-02",
  "descricao": "Brucelose: sorologia reagente Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 80,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.6,
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "sorologia_brucelose_reagente": true
  },
  "esperado": {
    "top1": "brucelose",
    "urgencia": "chamar_agora",
    "faixas": {
      "brucelose": [
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
  "caso_id": "C-N-BRU-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "brucelose",
    "top3_contem": [
      "brucelose",
      "acidose",
      "bvd"
    ],
    "percentuais": {
      "brucelose": 90,
      "acidose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-LEP-01

Leptospirose: leite com sangue e aborto Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-LEP-01",
  "descricao": "Leptospirose: leite com sangue e aborto Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 90,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "quente",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao",
      "leite_alterado"
    ],
    "excrecoes": []
  },
  "respostas": {
    "leite_com_sangue": true,
    "aborto_recente": true
  },
  "esperado": {
    "top1": "leptospirose",
    "urgencia": "chamar_agora",
    "faixas": {
      "leptospirose": [
        60,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-LEP-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "leptospirose",
    "top3_contem": [
      "leptospirose",
      "mastite",
      "acidose"
    ],
    "percentuais": {
      "leptospirose": 67,
      "mastite": 59,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "reticulopericardite_traumatica": 5,
      "ibr": 2,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "metrite": 0,
      "pneumonia": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "leptospirose",
      "mastite"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "aborto_recente",
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "falhas_reprodutivas_lote",
    "fezes_aquosas_espuma_graos",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "leite_com_sangue",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-LEP-02

Leptospirose: sorologia reagente Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-LEP-02",
  "descricao": "Leptospirose: sorologia reagente Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 90,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 39.8,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "sorologia_leptospirose_reagente": true,
    "esfregaco_hemoparasitas": false
  },
  "esperado": {
    "top1": "leptospirose",
    "urgencia": "chamar_agora",
    "faixas": {
      "leptospirose": [
        80,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-LEP-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "leptospirose",
    "top3_contem": [
      "leptospirose",
      "reticulopericardite_traumatica",
      "acidose"
    ],
    "percentuais": {
      "leptospirose": 85,
      "reticulopericardite_traumatica": 10,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "ibr": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "secrecao_nasal",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-IBR-01

IBR: focinho vermelho, catarro e olhos lacrimejando Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-IBR-01",
  "descricao": "IBR: focinho vermelho, catarro e olhos lacrimejando Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 100,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "quente",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "focinho_avermelhado": true,
    "secrecao_nasal": true,
    "olhos_lacrimejando": true
  },
  "esperado": {
    "top1": "ibr",
    "urgencia": "observar",
    "faixas": {
      "ibr": [
        60,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-IBR-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "ibr",
    "top3_contem": [
      "ibr",
      "acidose",
      "brucelose"
    ],
    "percentuais": {
      "ibr": 68,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipomagnesemia": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "sem_perguntas",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "aborto_recente",
    "apatia",
    "apetite",
    "carrapatos_historico_recente",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "emagrecimento_progressivo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "focinho_avermelhado",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "olhos_lacrimejando",
    "queda_producao",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-IBR-02

IBR: BoHV-1 detectado Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-IBR-02",
  "descricao": "IBR: BoHV-1 detectado Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 100,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 40.0,
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "pcr_bohv1": true,
    "ausculta_crepitacoes": false
  },
  "esperado": {
    "top1": "ibr",
    "urgencia": "observar",
    "faixas": {
      "ibr": [
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
  "caso_id": "C-N-IBR-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "observar",
    "top1": "ibr",
    "top3_contem": [
      "ibr",
      "acidose",
      "brucelose"
    ],
    "percentuais": {
      "ibr": 90,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipomagnesemia": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "pcr_bohv1",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-BVD-01

BVD: diarreia e feridas na boca Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-BVD-01",
  "descricao": "BVD: diarreia e feridas na boca Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 100,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "quente",
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": [
      "diarreia"
    ]
  },
  "respostas": {
    "feridas_boca": true
  },
  "esperado": {
    "top1": "bvd",
    "urgencia": "chamar_agora",
    "faixas": {
      "bvd": [
        55,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-BVD-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "bvd",
    "top3_contem": [
      "bvd",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "bvd": 62,
      "acidose": 38,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "bvd",
      "acidose"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "aborto_recente",
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "feridas_boca",
    "fezes_aquosas_espuma_graos",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "mucosas_palidas_ou_ictericas",
    "mudanca_abrupta_concentrado",
    "olhos_lacrimejando",
    "queda_producao",
    "respiracao_ofegante",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-BVD-02

BVD: antígeno detectado Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-BVD-02",
  "descricao": "BVD: antígeno detectado Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 100,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 39.7,
    "atitude_locomocao": [],
    "apetite_ruminacao": "reduzido",
    "producao_leite": [],
    "excrecoes": [
      "diarreia"
    ]
  },
  "respostas": {
    "antigeno_bvdv": true
  },
  "esperado": {
    "top1": "bvd",
    "urgencia": "chamar_agora",
    "faixas": {
      "bvd": [
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
  "caso_id": "C-N-BVD-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "bvd",
    "top3_contem": [
      "bvd",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "bvd": 91,
      "acidose": 38,
      "cetose": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "hipocalcemia": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "extremidades",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "mudanca_abrupta_concentrado",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "temperatura_retal",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-N-TUB-01

Tuberculose: emagrecimento, tosse e ínguas Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-TUB-01",
  "descricao": "Tuberculose: emagrecimento, tosse e ínguas Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 200,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": "normal",
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "emagrecimento_progressivo": true,
    "tosse": true,
    "linfonodos_aumentados": true
  },
  "esperado": {
    "top1": "tuberculose",
    "urgencia": "chamar_agora",
    "faixas": {
      "tuberculose": [
        65,
        100
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-N-TUB-01",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "tuberculose",
    "top3_contem": [
      "tuberculose",
      "acidose",
      "brucelose"
    ],
    "percentuais": {
      "tuberculose": 72,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "retencao_placenta": 0
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
    "emagrecimento_progressivo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "focinho_avermelhado",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-N-TUB-02

Tuberculose: tuberculinização reagente Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-N-TUB-02",
  "descricao": "Tuberculose: tuberculinização reagente Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 200,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.6,
    "atitude_locomocao": [],
    "apetite_ruminacao": "normal",
    "producao_leite": [],
    "excrecoes": []
  },
  "respostas": {
    "tuberculina_reagente": true
  },
  "esperado": {
    "top1": "tuberculose",
    "urgencia": "chamar_agora",
    "faixas": {
      "tuberculose": [
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
  "caso_id": "C-N-TUB-02",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "tuberculose",
    "top3_contem": [
      "tuberculose",
      "acidose",
      "brucelose"
    ],
    "percentuais": {
      "tuberculose": 90,
      "acidose": 0,
      "brucelose": 0,
      "bvd": 0,
      "cetose": 0,
      "dermatite_digital": 0,
      "deslocamento_abomaso_direita": 0,
      "deslocamento_abomaso_esquerda": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "retencao_placenta": 0
    },
    "motivo_parada": "confirmacao",
    "bandeiras": [],
    "inconclusivas": [],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "ausculta_crepitacoes",
    "calcio_serico",
    "claudicacao",
    "corrimento_vaginal",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "gas_livre_sonda",
    "historico_retencao_placenta",
    "leite_alterado",
    "magnesio_serico",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "temperatura_retal",
    "tuberculina_reagente",
    "ubere_inflamado",
    "urina_escura"
  ]
}
```

## C-EXC-DAB

Par excludente: deslocamento à direita vence e rebaixa o lado esquerdo Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-EXC-DAB",
  "descricao": "Par excludente: deslocamento à direita vence e rebaixa o lado esquerdo Caso fictício de regressão; suposição a validar.",
  "modo": "produtor",
  "ficha": {
    "dias_em_lactacao": 20,
    "historico_retencao_placenta": false
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
    "distensao_flanco_direito": true,
    "fezes_escassas": true,
    "desidratacao": true,
    "flanco_esquerdo_afundado": false
  },
  "esperado": {
    "top1": "deslocamento_abomaso_direita",
    "urgencia": "chamar_agora",
    "faixas": {
      "deslocamento_abomaso_direita": [
        70,
        100
      ],
      "deslocamento_abomaso_esquerda": [
        0,
        0
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-EXC-DAB",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "deslocamento_abomaso_direita",
    "top3_contem": [
      "deslocamento_abomaso_direita",
      "cetose",
      "acidose"
    ],
    "percentuais": {
      "deslocamento_abomaso_direita": 75,
      "cetose": 43,
      "acidose": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "pneumonia": 0,
      "reticulopericardite_traumatica": 0,
      "timpanismo_espumoso": 0,
      "timpanismo_gasoso": 0,
      "tpb": 0,
      "tuberculose": 0,
      "retencao_placenta": 0,
      "deslocamento_abomaso_esquerda": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [],
    "inconclusivas": [
      "deslocamento_abomaso_direita",
      "cetose"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "apatia",
    "apetite",
    "claudicacao",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "extremidades",
    "fezes_aquosas_espuma_graos",
    "halito_adocicado_acetona",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "linfonodos_aumentados",
    "mucosas_palidas_ou_ictericas",
    "queda_producao",
    "recusa_concentrado_come_volumoso",
    "respiracao_ofegante",
    "secrecao_nasal",
    "teste_caneca_grumos",
    "tosse",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

## C-EXC-TIM

Par excludente: timpanismo espumoso por leguminosa vence o gasoso, que tinha evidência positiva fraca (apetite ausente com abatimento). Caso fictício de regressão; suposição a validar.

### Entrada e resultado esperado

```json
{
  "id": "C-EXC-TIM",
  "descricao": "Par excludente: timpanismo espumoso por leguminosa vence o gasoso, que tinha evidência positiva fraca (apetite ausente com abatimento). Caso fictício de regressão; suposição a validar.",
  "modo": "veterinario",
  "ficha": {
    "dias_em_lactacao": 110,
    "historico_retencao_placenta": false
  },
  "triagem": {
    "estado_termico": 38.6,
    "atitude_locomocao": [
      "apatia"
    ],
    "apetite_ruminacao": "ausente",
    "producao_leite": [
      "queda_producao"
    ],
    "excrecoes": []
  },
  "respostas": {
    "distensao_flanco_esquerdo": true,
    "pasto_leguminosa_recente": true,
    "outros_animais_estufados": true,
    "engasgo": true,
    "gas_livre_sonda": false
  },
  "esperado": {
    "top1": "timpanismo_espumoso",
    "urgencia": "chamar_agora",
    "faixas": {
      "timpanismo_espumoso": [
        65,
        100
      ],
      "timpanismo_gasoso": [
        0,
        0
      ]
    }
  }
}
```

### Resultado observado

```json
{
  "caso_id": "C-EXC-TIM",
  "status": "passou",
  "falhas": [],
  "obtido": {
    "urgencia": "chamar_agora",
    "top1": "timpanismo_espumoso",
    "top3_contem": [
      "timpanismo_espumoso",
      "acidose",
      "cetose"
    ],
    "percentuais": {
      "timpanismo_espumoso": 72,
      "acidose": 5,
      "cetose": 5,
      "deslocamento_abomaso_direita": 5,
      "deslocamento_abomaso_esquerda": 5,
      "brucelose": 0,
      "bvd": 0,
      "dermatite_digital": 0,
      "hipocalcemia": 0,
      "hipomagnesemia": 0,
      "ibr": 0,
      "leptospirose": 0,
      "mastite": 0,
      "metrite": 0,
      "reticulopericardite_traumatica": 0,
      "tpb": 0,
      "tuberculose": 0,
      "pneumonia": 0,
      "retencao_placenta": 0,
      "timpanismo_gasoso": 0
    },
    "motivo_parada": "limite",
    "bandeiras": [
      "R-BV-03"
    ],
    "inconclusivas": [
      "timpanismo_espumoso"
    ],
    "alerta": {
      "pausa": false
    }
  },
  "respondidas": [
    "agitacao",
    "antigeno_bvdv",
    "apatia",
    "apetite",
    "bhb_sanguineo",
    "calcio_serico",
    "claudicacao",
    "cmt_reagente",
    "corrimento_vaginal",
    "costas_arqueadas",
    "decubito",
    "diarreia",
    "dias_em_lactacao",
    "distensao_flanco_direito",
    "distensao_flanco_esquerdo",
    "esfregaco_hemoparasitas",
    "espuma_sonda",
    "fezes_aquosas_espuma_graos",
    "fita_urina_corpos_cetonicos",
    "focinho_avermelhado",
    "gas_livre_sonda",
    "higroma",
    "historico_retencao_placenta",
    "leite_alterado",
    "lesao_erosiva_talao_morango",
    "linfonodos_aumentados",
    "magnesio_serico",
    "mucosas_palidas_ou_ictericas",
    "pasto_leguminosa_recente",
    "pcr_bohv1",
    "ph_ruminal",
    "ping_flanco_direito",
    "ping_metalico_flanco_esquerdo",
    "prova_dor_reticular",
    "queda_producao",
    "sorologia_brucelose_reagente",
    "sorologia_leptospirose_reagente",
    "temperatura_retal",
    "teste_caneca_grumos",
    "tuberculina_reagente",
    "ubere_inflamado",
    "urina_escura",
    "vacinada_brucelose"
  ]
}
```

Este documento executa 60 cenário(s) sintético(s); não substitui validação especializada. Os desvios em relação à especificação e os limites da coleta estão no registro de riscos. `limite_dinamico: 0`, quando presente no caso, encerra após a triagem; os limites normais da base são 15/30.
