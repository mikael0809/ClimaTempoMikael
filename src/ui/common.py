"""Funções compartilhadas pelas páginas da interface Streamlit."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import streamlit as st

from src.collectors.scheduler import run_once
from src.database import repositories as repo
from src.database.connection import session_scope
from src.database.models import Municipality
from src.integrations.open_meteo import ATTRIBUTION
from src.services.context import AppServices, build_services
from src.services.indicators import IndicatorRule, build_rules
from src.services.municipality_service import ensure_default_municipality
from src.services.weather_service import FRESH, STALE, Freshness
from src.utils.logging_config import setup_logging
from src.utils.timeutils import format_datetime


@st.cache_resource(show_spinner=False)
def get_services() -> AppServices:
    raise NotImplementedError("TODO: implementar get_services")


def get_rules() -> list[IndicatorRule]:
    raise NotImplementedError("TODO: implementar get_rules")


def db():
    """Atalho: ``with db() as session: ...``"""
    raise NotImplementedError("TODO: implementar db")


def list_municipalities(active_only: bool = False) -> list[Municipality]:
    raise NotImplementedError("TODO: implementar list_municipalities")


def select_municipality(key: str = "municipio_global") -> Municipality | None:
    """Seletor de município na barra lateral; o padrão é o município principal."""
    raise NotImplementedError("TODO: implementar select_municipality")


def sidebar_update_button() -> None:
    """Atualização manual: consulta INMET e Open-Meteo e grava no banco."""
    raise NotImplementedError("TODO: implementar sidebar_update_button")


def freshness_banner(freshness: Freshness, source: str = "Open-Meteo") -> None:
    raise NotImplementedError("TODO: implementar freshness_banner")


def attribution_footer() -> None:
    raise NotImplementedError("TODO: implementar attribution_footer")


def fmt(value: float | None, unit: str = "", digits: int = 1) -> str:
    raise NotImplementedError("TODO: implementar fmt")
