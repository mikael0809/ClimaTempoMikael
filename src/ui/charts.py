"""Gráficos interativos (Plotly) usados nas páginas."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

COLORS = {
    "temp": "#d9480f",
    "feels": "#f08c00",
    "min": "#1971c2",
    "max": "#e03131",
    "rain": "#1c7ed6",
    "prob": "#5f3dc4",
    "wind": "#2b8a3e",
    "gust": "#e67700",
}


def _layout(fig: go.Figure, title: str, y_title: str, hourly: bool = True) -> go.Figure:
    raise NotImplementedError("TODO: implementar _layout")


def hourly_temperature(df: pd.DataFrame) -> go.Figure:
    raise NotImplementedError("TODO: implementar hourly_temperature")


def hourly_precipitation(df: pd.DataFrame) -> go.Figure:
    raise NotImplementedError("TODO: implementar hourly_precipitation")


def hourly_wind(df: pd.DataFrame) -> go.Figure:
    raise NotImplementedError("TODO: implementar hourly_wind")


def daily_temperature(df: pd.DataFrame) -> go.Figure:
    raise NotImplementedError("TODO: implementar daily_temperature")


def daily_precipitation(df: pd.DataFrame) -> go.Figure:
    raise NotImplementedError("TODO: implementar daily_precipitation")


def history_line(df: pd.DataFrame, variable: str, label: str, unit: str) -> go.Figure:
    raise NotImplementedError("TODO: implementar history_line")
