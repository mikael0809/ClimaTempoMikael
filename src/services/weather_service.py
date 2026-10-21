"""Consultas meteorológicas para a interface (somente dados armazenados).

A interface sempre lê do banco local. Assim, se a fonte externa estiver
fora do ar, o usuário continua vendo a última informação conhecida — com o
aviso de que ela pode estar desatualizada (RN010).
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 7 e 9 · Documento 02 (Regras de negócio) · Documento 06 (Fluxogramas 7 a 9).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

import pandas as pd
from sqlalchemy.orm import Session

from src.database import repositories as repo
from src.database.models import HourlyForecast, Municipality, WeatherForecast, WeatherObservation
from src.services.indicators import IndicatorRule, LocalIndicator, evaluate_indicators
from src.utils.timeutils import DISPLAY_TZ, minutes_since, to_display, utc_now

FRESH = "ATUALIZADO"
STALE = "DESATUALIZADO"
UNAVAILABLE = "INDISPONÍVEL"


@dataclass
class Freshness:
    status: str
    minutes: float | None
    collected_at: datetime | None

    @property
    def message(self) -> str:
        raise NotImplementedError("TODO: implementar Freshness.message")


def assess_freshness(collected_at: datetime | None, stale_after_minutes: int, now: datetime | None = None) -> Freshness:
    raise NotImplementedError("TODO: implementar assess_freshness")


def local_today(now: datetime | None = None) -> date:
    raise NotImplementedError("TODO: implementar local_today")


def next_hours_window(hours: int = 24, now: datetime | None = None) -> tuple[datetime, datetime]:
    """Janela [hora atual, hora atual + N h] em UTC."""
    raise NotImplementedError("TODO: implementar next_hours_window")


def get_hourly_next_24h(session: Session, municipality_id: int, now: datetime | None = None) -> list[HourlyForecast]:
    raise NotImplementedError("TODO: implementar get_hourly_next_24h")


def get_daily_next_days(
    session: Session, municipality_id: int, days: int = 7, now: datetime | None = None
) -> list[WeatherForecast]:
    raise NotImplementedError("TODO: implementar get_daily_next_days")


@dataclass
class DashboardData:
    municipality: Municipality
    observation: WeatherObservation | None
    today: WeatherForecast | None
    hourly: list[HourlyForecast]
    daily: list[WeatherForecast]
    freshness: Freshness
    indicators: list[LocalIndicator]


def get_dashboard_data(
    session: Session,
    municipality: Municipality,
    rules: list[IndicatorRule],
    stale_after_minutes: int,
    now: datetime | None = None,
) -> DashboardData:
    raise NotImplementedError("TODO: implementar get_dashboard_data")


# ------------------------------------------------------------- DataFrames
HOURLY_COLUMNS = [
    "forecast_time",
    "temperature",
    "apparent_temperature",
    "humidity",
    "pressure",
    "precipitation",
    "precipitation_probability",
    "wind_speed",
    "wind_direction",
    "wind_gusts",
    "uv_index",
    "weather_code",
    "source",
]
DAILY_COLUMNS = [
    "forecast_date",
    "temperature_min",
    "temperature_max",
    "precipitation_probability",
    "precipitation_sum",
    "wind_speed",
    "wind_gusts",
    "wind_direction",
    "uv_index_max",
    "weather_code",
    "source",
    "collected_at",
]
OBSERVATION_COLUMNS = [
    "municipality_id",
    "observed_at",
    "temperature",
    "apparent_temperature",
    "humidity",
    "pressure",
    "precipitation",
    "precipitation_probability",
    "wind_speed",
    "wind_direction",
    "wind_gusts",
    "weather_code",
    "source",
    "collected_at",
]


def _to_frame(rows: list, columns: list[str]) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar _to_frame")


def _localize(series: pd.Series) -> pd.Series:
    """Converte uma coluna UTC ingênua para America/Sao_Paulo."""
    raise NotImplementedError("TODO: implementar _localize")


def hourly_frame(rows: list[HourlyForecast]) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar hourly_frame")


def daily_frame(rows: list[WeatherForecast]) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar daily_frame")


def observations_frame(rows: list[WeatherObservation], labels: dict[int, str] | None = None) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar observations_frame")
