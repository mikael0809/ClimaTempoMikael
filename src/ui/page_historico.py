"""Página: Histórico de observações efetivamente coletadas."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from datetime import datetime, time, timedelta

import streamlit as st

from src.database import repositories as repo
from src.services.export_service import prepare_weather_export, to_csv_bytes
from src.services.weather_service import observations_frame
from src.ui import charts, common
from src.utils.timeutils import DISPLAY_TZ, local_to_utc

VARIABLES = {
    "temperature": ("Temperatura", "°C"),
    "apparent_temperature": ("Sensação térmica", "°C"),
    "humidity": ("Umidade relativa", "%"),
    "pressure": ("Pressão", "hPa"),
    "precipitation": ("Precipitação", "mm"),
    "wind_speed": ("Velocidade do vento", "km/h"),
    "wind_gusts": ("Rajadas", "km/h"),
}


def render() -> None:
    raise NotImplementedError("TODO: implementar render")
