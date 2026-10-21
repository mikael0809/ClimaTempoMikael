"""Funções de análise da dashboard de exemplo (filtros, resumos e indicador).

Ficam separadas do ``app.py`` para poderem ser testadas sem abrir a
interface.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 3 · exemplos/dashboard_python/README.md.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from datetime import date

import pandas as pd


def filtrar(df: pd.DataFrame, municipios: list[str], inicio: date, fim: date) -> pd.DataFrame:
    """Mantém apenas os municípios escolhidos e o período [inicio, fim]."""
    raise NotImplementedError("TODO: implementar filtrar")


def resumo_por_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por município com as estatísticas do período."""
    raise NotImplementedError("TODO: implementar resumo_por_municipio")


def chuva_diaria(df: pd.DataFrame) -> pd.DataFrame:
    """Soma a precipitação por dia e por município."""
    raise NotImplementedError("TODO: implementar chuva_diaria")


def indicador_atencao_chuva(df: pd.DataFrame, limite_mm: float) -> pd.DataFrame:
    """INDICADOR CALCULADO (não oficial): dias com chuva acumulada >= limite.

    É apenas um exemplo de regra de negócio. Não é um alerta oficial.
    """
    raise NotImplementedError("TODO: implementar indicador_atencao_chuva")


def garantir_fonte_unica(df: pd.DataFrame) -> str:
    """Impede a mistura silenciosa de dados simulados e reais."""
    raise NotImplementedError("TODO: implementar garantir_fonte_unica")
