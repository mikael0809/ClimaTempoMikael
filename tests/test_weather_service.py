"""Consultas para a interface e identificação de dados desatualizados (RN010)."""

from __future__ import annotations

from datetime import datetime, timedelta

from src.config import IndicatorThresholds
from src.database import repositories as repo
from src.integrations.open_meteo import parse_forecast
from src.services.indicators import build_rules
from src.services.weather_service import (
    FRESH,
    STALE,
    UNAVAILABLE,
    assess_freshness,
    daily_frame,
    get_dashboard_data,
    hourly_frame,
    next_hours_window,
    observations_frame,
)
from tests.conftest import NOW


def test_freshness_levels():
    assert assess_freshness(None, 180, NOW).status == UNAVAILABLE
    assert assess_freshness(NOW - timedelta(minutes=30), 180, NOW).status == FRESH
    stale = assess_freshness(NOW - timedelta(hours=5), 180, NOW)
    assert stale.status == STALE
    assert "desatualizados" in stale.message


def test_next_hours_window():
    start, end = next_hours_window(24, datetime(2026, 10, 21, 18, 37))
    assert start == datetime(2026, 10, 21, 18, 0)
    assert end - start == timedelta(hours=23)


def _store(session, payload):
    m = repo.find_municipality(session, "Sapiranga", "RS")
    bundle = parse_forecast(payload)
    repo.upsert_observation(session, m.id, bundle.current)
    repo.upsert_hourly_forecasts(session, m.id, bundle.hourly)
    repo.upsert_daily_forecasts(session, m.id, bundle.daily)
    session.flush()
    return m, bundle


def test_dashboard_data(session, sapiranga_id, forecast_payload):
    m, bundle = _store(session, forecast_payload)
    data = get_dashboard_data(session, m, build_rules(IndicatorThresholds()), 180, NOW + timedelta(minutes=5))
    assert data.observation.temperature == bundle.current["temperature"]
    assert len(data.hourly) == 24
    assert data.hourly[0].forecast_time == datetime(2026, 10, 21, 18, 0)
    assert len(data.daily) == 7
    assert data.today.forecast_date.isoformat() == "2026-10-21"


def test_dashboard_marks_old_data_as_stale(session, sapiranga_id, forecast_payload):
    m, _ = _store(session, forecast_payload)
    much_later = datetime.now() + timedelta(days=2)
    data = get_dashboard_data(session, m, [], 180, much_later)
    assert data.freshness.status == STALE  # a última informação continua disponível, mas sinalizada
    assert data.observation is not None


def test_frames_are_converted_to_brasilia(session, sapiranga_id, forecast_payload):
    m, _ = _store(session, forecast_payload)
    hourly = hourly_frame(
        repo.list_hourly_forecasts(session, m.id, datetime(2026, 10, 21, 3), datetime(2026, 10, 21, 5))
    )
    assert str(hourly["forecast_time"].dt.tz) == "America/Sao_Paulo"
    assert hourly["forecast_time"].iloc[0].hour == 0
    daily = daily_frame(repo.list_daily_forecasts(session, m.id, datetime(2026, 10, 21).date()))
    assert len(daily) == 7
    obs = observations_frame(repo.list_observations(session), {m.id: m.label})
    assert obs["municipality"].iloc[0] == "Sapiranga - RS"
    assert observations_frame([]).empty
