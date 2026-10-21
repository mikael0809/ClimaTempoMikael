"""Operações de acesso ao banco (camada de persistência).

As funções recebem uma ``Session`` aberta e não fazem ``commit`` — quem
chama decide a transação (normalmente ``session_scope``). As gravações de
dados meteorológicos usam *upsert* (INSERT ... ON CONFLICT DO UPDATE) do
SQLite: executar a mesma coleta duas vezes atualiza o registro existente em
vez de duplicá-lo.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 8 · Documento 04 (Dicionário de dados e modelo ER) · Documento 12.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import date, datetime
from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from src.database.models import (
    CollectionLog,
    HourlyForecast,
    Municipality,
    WeatherAlert,
    WeatherForecast,
    WeatherObservation,
)
from src.utils.timeutils import utc_now


class DuplicateMunicipalityError(ValueError):
    """O município já está cadastrado."""


# --------------------------------------------------------------------- municípios
def find_municipality(session: Session, name: str, state_code: str) -> Municipality | None:
    raise NotImplementedError("TODO: implementar find_municipality")


def add_municipality(session: Session, **fields: Any) -> Municipality:
    """Insere um município; lança ``DuplicateMunicipalityError`` se já existir."""
    raise NotImplementedError("TODO: implementar add_municipality")


def get_municipality(session: Session, municipality_id: int) -> Municipality | None:
    raise NotImplementedError("TODO: implementar get_municipality")


def list_municipalities(session: Session, active_only: bool = False) -> list[Municipality]:
    raise NotImplementedError("TODO: implementar list_municipalities")


def get_primary_municipality(session: Session) -> Municipality | None:
    raise NotImplementedError("TODO: implementar get_primary_municipality")


def set_primary_municipality(session: Session, municipality_id: int) -> None:
    raise NotImplementedError("TODO: implementar set_primary_municipality")


def set_municipality_active(session: Session, municipality_id: int, active: bool) -> None:
    raise NotImplementedError("TODO: implementar set_municipality_active")


def delete_municipality(session: Session, municipality_id: int) -> bool:
    """Remove o município e, em cascata, seus dados meteorológicos."""
    raise NotImplementedError("TODO: implementar delete_municipality")


# ------------------------------------------------------------------- upserts
def _upsert(session: Session, model: type, rows: Sequence[dict[str, Any]], keys: list[str]) -> int:
    raise NotImplementedError("TODO: implementar _upsert")


def upsert_observation(session: Session, municipality_id: int, row: dict[str, Any]) -> int:
    raise NotImplementedError("TODO: implementar upsert_observation")


def upsert_daily_forecasts(session: Session, municipality_id: int, rows: Iterable[dict[str, Any]]) -> int:
    raise NotImplementedError("TODO: implementar upsert_daily_forecasts")


def upsert_hourly_forecasts(session: Session, municipality_id: int, rows: Iterable[dict[str, Any]]) -> int:
    raise NotImplementedError("TODO: implementar upsert_hourly_forecasts")


def upsert_alerts(session: Session, rows: Iterable[dict[str, Any]]) -> int:
    raise NotImplementedError("TODO: implementar upsert_alerts")


def close_missing_alerts(session: Session, source: str, active_external_ids: set[str]) -> int:
    """Marca como ENCERRADO o aviso que deixou de constar na lista de ativos da fonte."""
    raise NotImplementedError("TODO: implementar close_missing_alerts")


# ------------------------------------------------------------------ consultas
def latest_observation(session: Session, municipality_id: int) -> WeatherObservation | None:
    raise NotImplementedError("TODO: implementar latest_observation")


def list_observations(
    session: Session,
    municipality_ids: Sequence[int] | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[WeatherObservation]:
    raise NotImplementedError("TODO: implementar list_observations")


def list_hourly_forecasts(
    session: Session, municipality_id: int, start: datetime, end: datetime
) -> list[HourlyForecast]:
    raise NotImplementedError("TODO: implementar list_hourly_forecasts")


def list_daily_forecasts(
    session: Session, municipality_id: int, start_date: date, days: int = 7
) -> list[WeatherForecast]:
    raise NotImplementedError("TODO: implementar list_daily_forecasts")


def list_alerts(session: Session, source: str | None = None) -> list[WeatherAlert]:
    raise NotImplementedError("TODO: implementar list_alerts")


# ------------------------------------------------------------ logs de coleta
def start_collection_log(
    session: Session, source: str, collection_type: str, municipality_id: int | None = None
) -> CollectionLog:
    raise NotImplementedError("TODO: implementar start_collection_log")


def finish_collection_log(log: CollectionLog, status: str, records: int = 0, error_message: str | None = None) -> None:
    raise NotImplementedError("TODO: implementar finish_collection_log")


def list_collection_logs(session: Session, limit: int = 100) -> list[CollectionLog]:
    raise NotImplementedError("TODO: implementar list_collection_logs")


def last_log(session: Session, source: str, status: str | None = None) -> CollectionLog | None:
    raise NotImplementedError("TODO: implementar last_log")


def count_rows(session: Session) -> dict[str, int]:
    """Quantidade de registros em cada tabela (tela de diagnóstico)."""
    raise NotImplementedError("TODO: implementar count_rows")
