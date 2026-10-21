"""Central de alertas: validade, expiração, filtros e separação oficial x calculado."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select

from src.config import IndicatorThresholds
from src.database import repositories as repo
from src.database.models import WeatherAlert
from src.integrations.inmet import parse_active_alerts
from src.integrations.open_meteo import parse_forecast
from src.services.alert_service import (
    VALIDITY_CLOSED,
    VALIDITY_CURRENT,
    VALIDITY_EXPIRED,
    VALIDITY_FUTURE,
    AlertFilters,
    alert_options,
    filter_alerts,
    is_expired,
    validity_status,
)
from src.services.indicators import LocalIndicator, build_rules, evaluate_indicators
from src.services.municipality_service import register_manual
from tests.conftest import NOW


def _alerts(session, payload):
    repo.upsert_alerts(session, parse_active_alerts(payload))
    session.flush()
    return {a.external_id: a for a in repo.list_alerts(session)}


def test_validity_and_expiration(session, inmet_payload):
    alerts = _alerts(session, inmet_payload)
    today = alerts["56124"]  # 21/10 00:01 a 23:59 (Brasília)
    future = alerts["56134"]  # 24/10
    assert validity_status(today, NOW) == VALIDITY_CURRENT
    assert validity_status(future, NOW) == VALIDITY_FUTURE
    after = datetime(2026, 10, 22, 3, 0)  # 22/10 00:00 Brasília
    assert is_expired(today, after)
    assert validity_status(today, after) == VALIDITY_EXPIRED
    assert not is_expired(future, after)


def test_closed_by_source(session, inmet_payload):
    alerts = _alerts(session, inmet_payload)
    alert = alerts["56134"]
    alert.status = "ENCERRADO"
    assert validity_status(alert, NOW) == VALIDITY_CLOSED


def test_filters(session, inmet_payload):
    alerts = list(_alerts(session, inmet_payload).values())
    by_event = filter_alerts(alerts, AlertFilters(events=["Tempestade"]), NOW)
    assert {a.event for a in by_event} == {"Tempestade"}
    assert filter_alerts(alerts, AlertFilters(sources=["OUTRA"]), NOW) == []
    current = filter_alerts(alerts, AlertFilters(validities=[VALIDITY_CURRENT]), NOW)
    assert {a.external_id for a in current} == {"56124", "56127"}
    period = filter_alerts(alerts, AlertFilters(start=datetime(2026, 10, 24, 3), end=datetime(2026, 10, 25, 2)), NOW)
    assert {a.external_id for a in period} == {"56134"}
    options = alert_options(alerts)
    assert options["sources"] == ["INMET"]
    assert "Chuvas Intensas" in options["events"]


def test_filter_by_municipality_uses_ibge_code(session, inmet_payload):
    alerts = list(_alerts(session, inmet_payload).values())
    acrelandia = register_manual(session, "Acrelândia", "AC", -9.82, -66.89, 1200013)
    sapiranga = register_manual(session, "Sapiranga", "RS", -29.63806, -51.00694, 4319901)
    assert {a.external_id for a in filter_alerts(alerts, AlertFilters(municipalities=[acrelandia]), NOW)} == {"56124"}
    # Na amostra real, o aviso 56127 abrange o RS mas não lista Sapiranga; o 56134 lista.
    by_code = filter_alerts(alerts, AlertFilters(municipalities=[sapiranga]), NOW)
    assert {a.external_id for a in by_code} == {"56134"}
    sapiranga.ibge_code = None  # sem código IBGE, o filtro recorre à UF
    by_state = filter_alerts(alerts, AlertFilters(municipalities=[sapiranga]), NOW)
    assert {a.external_id for a in by_state} == {"56127", "56134"}


def test_official_alerts_and_indicators_are_separate(session, inmet_payload, forecast_payload):
    """RN009: indicadores calculados nunca viram registros da tabela de alertas oficiais."""
    _alerts(session, inmet_payload)
    before = session.scalar(select(func.count(WeatherAlert.id)))
    bundle = parse_forecast(forecast_payload)
    rules = build_rules(IndicatorThresholds(precipitation_probability=1, temperature_max_c=1))
    indicators = evaluate_indicators(rules, bundle.hourly[:24], bundle.daily)
    assert indicators, "limites baixos devem gerar indicadores"
    assert all(isinstance(i, LocalIndicator) and i.classification.startswith("INDICADOR CALCULADO") for i in indicators)
    assert session.scalar(select(func.count(WeatherAlert.id))) == before
    assert {a.alert_type for a in repo.list_alerts(session)} == {"OFICIAL"}
