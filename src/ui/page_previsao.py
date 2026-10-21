"""Página: Previsão horária (24 h) e diária (7 dias)."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import streamlit as st

from src.integrations.open_meteo import ATTRIBUTION
from src.services.export_service import prepare_weather_export, to_csv_bytes
from src.services.weather_service import (
    daily_frame,
    get_daily_next_days,
    get_hourly_next_24h,
    hourly_frame,
)
from src.ui import charts, common
from src.utils.timeutils import weekday_label
from src.utils.weather_codes import describe_weather_code, wind_direction_label


def render() -> None:
    raise NotImplementedError("TODO: implementar render")
