"""Textos que a API escreve para o usuário (urgência, alerta, aviso do parecer).

Todas as frases são **suposição**: precisam ser validadas com a RERUM e com o veterinário. Ficam num só lugar para a
equipe revisar a redação sem mexer na lógica.
"""
from __future__ import annotations

# (nível de urgência, modo) -> texto da urgência no parecer
TEXTO_URGENCIA: dict[tuple[str, str], str] = {
    ("chamar_agora", "produtor"): "Chame um veterinário o mais rápido possível.",
    ("chamar_agora", "veterinario"): "Urgência máxima: indicação de atendimento veterinário imediato.",
    ("observar", "produtor"): "Observe o animal de perto e chame um veterinário se ele piorar.",
    ("observar", "veterinario"): "Observação: acompanhar a evolução e reavaliar o quadro.",
    ("sem_problema", "produtor"): "Nenhum problema aparente com o que foi informado. Continue acompanhando o animal.",
    ("sem_problema", "veterinario"): "Sem indício de urgência nos dados informados.",
}

# modo -> texto do alerta de bandeira vermelha
TEXTO_ALERTA: dict[str, str] = {
    "produtor": "Sintoma grave: chame um veterinário o mais rápido possível.",
    "veterinario": "Bandeira vermelha: sinal de gravidade presente nos dados informados.",
}

AVISO_PARECER = "A porcentagem é o grau de confiança do sistema, não uma probabilidade."
