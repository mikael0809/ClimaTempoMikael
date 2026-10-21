"""Integração OPCIONAL com dados reais (API Open-Meteo, gratuita e sem chave).

Devolve um DataFrame com as MESMAS colunas dos dados simulados, mas com
``tipo_dado = "REAL"``. A dashboard usa uma fonte OU outra, nunca as duas.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 3 · exemplos/dashboard_python/README.md.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import pandas as pd
import requests

TIPO_REAL = "REAL"
URL = "https://api.open-meteo.com/v1/forecast"

# Coordenadas obtidas na geocodificação da Open-Meteo (GeoNames).
COORDENADAS = {
    "Sapiranga - RS": (-29.63806, -51.00694),
    "Porto Alegre - RS": (-30.03283, -51.23019),
    "Caxias do Sul - RS": (-29.16806, -51.17944),
}


def buscar_dados_reais(municipio: str, dias_passados: int = 7, dias_futuros: int = 2) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar buscar_dados_reais")


def buscar_varios(municipios: list[str]) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar buscar_varios")
