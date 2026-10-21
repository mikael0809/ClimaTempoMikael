"""Página: Central de alertas (oficiais x indicadores calculados)."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from datetime import datetime, time, timedelta

import pandas as pd
import streamlit as st

from src.database import repositories as repo
from src.services.alert_service import (
    VALIDITY_CLOSED,
    VALIDITY_CURRENT,
    VALIDITY_EXPIRED,
    VALIDITY_FUTURE,
    AlertFilters,
    alert_options,
    filter_alerts,
    validity_status,
)
from src.services.export_service import alerts_export_frame, indicators_export_frame, to_csv_bytes
from src.services.indicators import CLASSIFICATION, DISCLAIMER, evaluate_indicators
from src.services.weather_service import get_daily_next_days, get_hourly_next_24h
from src.ui import common
from src.ui.common import fmt
from src.utils.timeutils import DISPLAY_TZ, format_datetime, local_to_utc


def _to_utc_bounds(start, end) -> tuple[datetime, datetime]:
    raise NotImplementedError("TODO: implementar _to_utc_bounds")


def render() -> None:
    raise NotImplementedError("TODO: implementar render")
