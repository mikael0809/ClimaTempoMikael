"""Configurações do ClimaAlerta.

Todas as configurações operacionais ficam em variáveis de ambiente (arquivo
``.env``), separadas do código. Este módulo lê esses valores uma única vez e
os disponibiliza em um objeto imutável ``Settings``.

Nenhuma credencial é necessária: as fontes utilizadas (Open-Meteo e INMET)
são públicas e gratuitas. Mesmo assim, o padrão de leitura via ``.env`` é
mantido para ensinar a separação entre configuração e código.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 11 · Documento 12 (Configurações) · .env.example.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Raiz do projeto: a pasta que contém app.py, src/, tests/ etc.
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _env_str(name: str, default: str) -> str:
    raise NotImplementedError("TODO: implementar _env_str")


def _env_float(name: str, default: float) -> float:
    raise NotImplementedError("TODO: implementar _env_float")


def _env_int(name: str, default: int) -> int:
    raise NotImplementedError("TODO: implementar _env_int")


def _env_bool(name: str, default: bool) -> bool:
    raise NotImplementedError("TODO: implementar _env_bool")


@dataclass(frozen=True)
class IndicatorThresholds:
    """Limites dos indicadores locais.

    IMPORTANTE: são parâmetros DEMONSTRATIVOS para fins didáticos, e não
    recomendações oficiais de segurança.
    """

    precipitation_probability: float = 70.0  # %
    precipitation_hourly_mm: float = 10.0  # mm em 1 hora
    precipitation_daily_mm: float = 30.0  # mm no dia
    wind_gusts_kmh: float = 60.0  # km/h
    temperature_max_c: float = 35.0  # °C
    temperature_min_c: float = 3.0  # °C
    humidity_min_percent: float = 30.0  # %


@dataclass(frozen=True)
class Settings:
    database_path: Path
    log_dir: Path
    log_level: str
    timezone: str
    http_timeout_seconds: float
    http_max_retries: int
    http_backoff_factor: float
    user_agent: str
    update_interval_minutes: int
    stale_after_minutes: int
    forecast_days: int
    open_meteo_forecast_url: str
    open_meteo_geocoding_url: str
    inmet_alerts_url: str
    inmet_alert_page_url: str
    ibge_municipalities_url: str
    selenium_headless: bool
    selenium_timeout_seconds: float
    thresholds: IndicatorThresholds = field(default_factory=IndicatorThresholds)

    @property
    def database_url(self) -> str:
        raise NotImplementedError("TODO: implementar Settings.database_url")

    def as_public_dict(self) -> dict[str, object]:
        """Configurações não sensíveis exibidas na tela de diagnóstico."""
        raise NotImplementedError("TODO: implementar Settings.as_public_dict")


def _resolve_path(raw: str) -> Path:
    raise NotImplementedError("TODO: implementar _resolve_path")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Lê o arquivo .env (se existir) e devolve as configurações."""
    raise NotImplementedError("TODO: implementar get_settings")
