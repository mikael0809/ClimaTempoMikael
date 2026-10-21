"""Geração de dados meteorológicos SIMULADOS para a dashboard de exemplo.

Os números são produzidos por fórmulas e por um gerador aleatório com
semente fixa: executar duas vezes gera exatamente os mesmos valores. Eles
NÃO representam medições reais. A coluna ``tipo_dado`` registra isso em
cada linha.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 3 · exemplos/dashboard_python/README.md.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import math
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

TIPO_SIMULADO = "SIMULADO"
PASTA_DADOS = Path(__file__).parent / "dados"
ARQUIVO_CSV = PASTA_DADOS / "dados_simulados.csv"

# Nomes reais são usados apenas para dar contexto; os valores são inventados.
MUNICIPIOS = {
    "Sapiranga - RS": {"base_temp": 21.0, "base_umid": 72.0},
    "Porto Alegre - RS": {"base_temp": 22.5, "base_umid": 70.0},
    "Caxias do Sul - RS": {"base_temp": 17.0, "base_umid": 78.0},
}


def gerar_dados_simulados(
    inicio: datetime = datetime(2026, 10, 1, 0, 0),
    dias: int = 14,
    semente: int = 42,
) -> pd.DataFrame:
    """Gera uma linha por hora e por município."""
    raise NotImplementedError("TODO: implementar gerar_dados_simulados")


def salvar_csv(df: pd.DataFrame, caminho: Path = ARQUIVO_CSV) -> Path:
    raise NotImplementedError("TODO: implementar salvar_csv")


def carregar_dados_simulados(caminho: Path = ARQUIVO_CSV) -> pd.DataFrame:
    """Lê o CSV; se ele não existir, gera e salva os dados primeiro."""
    raise NotImplementedError("TODO: implementar carregar_dados_simulados")


if __name__ == "__main__":
    print(f"Arquivo gerado: {salvar_csv(gerar_dados_simulados())}")
