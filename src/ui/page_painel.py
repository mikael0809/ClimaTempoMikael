"""Página: Painel principal (dashboard)."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import repositories as repo
from src.services.alert_service import official_alerts_for, validity_status
from src.services.diagnostics_service import source_statuses
from src.services.indicators import DISCLAIMER
from src.services.weather_service import assess_freshness, get_dashboard_data
from src.ui import common
from src.ui.common import fmt
from src.utils.timeutils import format_datetime
from src.utils.weather_codes import describe_weather_code, weather_icon, wind_direction_label


def render() -> None:
    raise NotImplementedError("TODO: implementar render")
