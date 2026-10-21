"""Persistência: esquema, restrições, upserts e prevenção de duplicações."""

from __future__ import annotations

from datetime import date, datetime

import pytest
from sqlalchemy import func, inspect, select, text
from sqlalchemy.exc import IntegrityError

from src.database import repositories as repo
from src.database.connection import SCHEMA_VERSION, get_engine, init_db, run_migrations, session_scope
from src.database.models import HourlyForecast, WeatherAlert, WeatherForecast, WeatherObservation
from src.integrations.inmet import parse_active_alerts
from src.integrations.open_meteo import parse_forecast
from tests.conftest import SAPIRANGA


def test_init_db_is_idempotent_and_versioned(db_url):
    engine = init_db(db_url)
    init_db(db_url)
    assert run_migrations(engine) == SCHEMA_VERSION
    tables = set(inspect(engine).get_table_names())
    assert {
        "municipality",
        "weather_observation",
        "weather_forecast",
        "hourly_forecast",
        "weather_alert",
        "collection_log",
    } <= tables


def test_foreign_keys_are_enforced(db_url, session):
    assert session.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
    session.add(WeatherObservation(municipality_id=999, observed_at=datetime(2026, 1, 1), source="x"))
    with pytest.raises(IntegrityError):
        session.flush()


def test_first_municipality_becomes_primary_and_duplicates_are_blocked(session):
    m = repo.add_municipality(session, **SAPIRANGA)
    assert m.is_primary
    with pytest.raises(repo.DuplicateMunicipalityError):
        repo.add_municipality(session, **{**SAPIRANGA, "name": "SAPIRANGA"})  # sem diferenciar maiúsculas
    other = repo.add_municipality(
        session, **{**SAPIRANGA, "name": "Sapiranga", "state_code": "SC", "state": "Santa Catarina"}
    )
    assert not other.is_primary
    repo.set_primary_municipality(session, other.id)
    session.flush()
    assert repo.get_primary_municipality(session).id == other.id


def test_check_constraint_on_coordinates(session):
    with pytest.raises(IntegrityError):
        repo.add_municipality(session, **{**SAPIRANGA, "latitude": 120})


def test_observation_upsert_does_not_duplicate(session, forecast_payload):
    m = repo.add_municipality(session, **SAPIRANGA)
    bundle = parse_forecast(forecast_payload)
    repo.upsert_observation(session, m.id, bundle.current)
    repo.upsert_observation(session, m.id, {**bundle.current, "temperature": 30.0})
    rows = session.scalars(select(WeatherObservation)).all()
    assert len(rows) == 1
    session.expire_all()
    assert repo.latest_observation(session, m.id).temperature == 30.0


def test_forecast_upsert_updates_existing_rows(session, forecast_payload):
    m = repo.add_municipality(session, **SAPIRANGA)
    bundle = parse_forecast(forecast_payload)
    assert repo.upsert_daily_forecasts(session, m.id, bundle.daily) == 7
    assert repo.upsert_hourly_forecasts(session, m.id, bundle.hourly) == 168
    changed = [{**d, "temperature_max": 40.0} for d in bundle.daily]
    repo.upsert_daily_forecasts(session, m.id, changed)
    repo.upsert_hourly_forecasts(session, m.id, bundle.hourly)
    assert session.scalar(select(func.count(WeatherForecast.id))) == 7
    assert session.scalar(select(func.count(HourlyForecast.id))) == 168
    session.expire_all()
    days = repo.list_daily_forecasts(session, m.id, date(2026, 10, 21))
    assert {d.temperature_max for d in days} == {40.0}


def test_delete_municipality_cascades(session, forecast_payload):
    m = repo.add_municipality(session, **SAPIRANGA)
    bundle = parse_forecast(forecast_payload)
    repo.upsert_observation(session, m.id, bundle.current)
    repo.upsert_daily_forecasts(session, m.id, bundle.daily)
    session.flush()
    session.expire_all()
    assert repo.delete_municipality(session, m.id)
    session.flush()
    assert session.scalar(select(func.count(WeatherObservation.id))) == 0
    assert session.scalar(select(func.count(WeatherForecast.id))) == 0
    assert not repo.delete_municipality(session, 12345)


def test_alerts_upsert_and_close_missing(session, inmet_payload):
    alerts = parse_active_alerts(inmet_payload)
    assert repo.upsert_alerts(session, alerts) == 4
    repo.upsert_alerts(session, alerts)
    assert session.scalar(select(func.count(WeatherAlert.id))) == 4
    closed = repo.close_missing_alerts(session, "INMET", {"56124"})
    assert closed == 3
    session.expire_all()
    statuses = {a.external_id: a.status for a in repo.list_alerts(session)}
    assert statuses["56124"] == "ATIVO" and statuses["56127"] == "ENCERRADO"


def test_calculated_indicator_cannot_be_saved_as_alert(session, inmet_payload):
    """RN009: a tabela de alertas aceita apenas alertas oficiais."""
    alert = parse_active_alerts(inmet_payload)[0]
    with pytest.raises(ValueError, match="oficiais"):
        repo.upsert_alerts(session, [{**alert, "alert_type": "INDICADOR"}])
    session.add(WeatherAlert(**{**alert, "external_id": "x1", "alert_type": "INDICADOR"}))
    with pytest.raises(IntegrityError):
        session.flush()


def test_collection_log_lifecycle(db_url):
    with session_scope(db_url) as s:
        log = repo.start_collection_log(s, "Open-Meteo", "PREVISAO")
        assert log.status == "FALHA"  # pessimista até terminar
        repo.finish_collection_log(log, "SUCESSO", 10)
    with session_scope(db_url) as s:
        last = repo.last_log(s, "Open-Meteo", "SUCESSO")
        assert last.records_collected == 10 and last.finished_at is not None
        assert repo.count_rows(s)["collection_log"] == 1


def test_engine_is_reused(db_url):
    assert get_engine(db_url) is get_engine(db_url)
