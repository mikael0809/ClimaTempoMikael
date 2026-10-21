"""Regras de atenção (indicadores locais calculados) — RN007, RN008."""

from __future__ import annotations

import inspect
from datetime import date, datetime

import pytest

from src.config import IndicatorThresholds, get_settings
from src.services import indicators as ind
from src.services.indicators import CLASSIFICATION, build_rules, evaluate_daily, evaluate_hourly, evaluate_indicators


def rules() -> dict:
    """Regras com os limites padrão (calculadas sob demanda, não na importação)."""
    return {r.rule_id: r for r in build_rules(IndicatorThresholds())}


def hour(h: int, **values):
    return {"forecast_time": datetime(2026, 10, 21, h), "source": "Open-Meteo", **values}


def day(d: int, **values):
    return {"forecast_date": date(2026, 10, d), "source": "Open-Meteo", **values}


def test_rules_are_built_from_thresholds():
    rules = build_rules(IndicatorThresholds(wind_gusts_kmh=50))
    assert {r.rule_id for r in rules} == {f"IND0{i}" for i in range(1, 8)}
    assert next(r for r in rules if r.rule_id == "IND04").threshold == 50


@pytest.mark.parametrize(
    ("rule_id", "rows", "expected_value"),
    [
        ("IND01", [hour(1, precipitation_probability=40), hour(2, precipitation_probability=85)], 85),
        ("IND02", [hour(1, precipitation=12.5)], 12.5),
        ("IND04", [hour(1, wind_gusts=61), hour(2, wind_gusts=75), hour(3, wind_gusts=20)], 75),
        ("IND07", [hour(1, humidity=28), hour(2, humidity=22)], 22),  # '<=' escolhe o menor
    ],
)
def test_hourly_rules_pick_extreme_value(rule_id, rows, expected_value):
    hit = evaluate_hourly(rules()[rule_id], rows)
    assert hit is not None
    assert hit.value == expected_value
    assert hit.classification == CLASSIFICATION
    assert hit.threshold == rules()[rule_id].threshold


def test_hourly_rule_counts_occurrences_and_reference_time():
    hit = evaluate_hourly(rules()["IND04"], [hour(1, wind_gusts=61), hour(2, wind_gusts=75)])
    assert hit.occurrences == 2
    assert hit.reference_time == datetime(2026, 10, 21, 2)
    assert hit.source == "Open-Meteo"


def test_values_below_threshold_do_not_trigger():
    assert evaluate_hourly(rules()["IND01"], [hour(1, precipitation_probability=69.9)]) is None
    assert evaluate_hourly(rules()["IND07"], [hour(1, humidity=30.1)]) is None


def test_threshold_is_inclusive():
    assert evaluate_hourly(rules()["IND01"], [hour(1, precipitation_probability=70)]) is not None


def test_missing_values_never_trigger():
    assert evaluate_hourly(rules()["IND04"], [hour(1, wind_gusts=None), hour(2)]) is None
    assert evaluate_daily(rules()["IND05"], [day(21, temperature_max=None)]) == []


def test_daily_rules_one_indicator_per_day():
    rows = [day(21, temperature_max=36), day(22, temperature_max=34), day(23, temperature_max=38)]
    hits = evaluate_daily(rules()["IND05"], rows)
    assert [h.reference_time for h in hits] == [date(2026, 10, 21), date(2026, 10, 23)]
    cold = evaluate_daily(rules()["IND06"], [day(24, temperature_min=2.5)])
    assert cold[0].value == 2.5 and cold[0].operator == "<="
    rain = evaluate_daily(rules()["IND03"], [day(25, precipitation_sum=30)])
    assert len(rain) == 1


def test_evaluate_indicators_with_real_forecast(forecast_payload):
    from src.integrations.open_meteo import parse_forecast

    bundle = parse_forecast(forecast_payload)
    found = evaluate_indicators(
        build_rules(IndicatorThresholds()), bundle.hourly[:24], bundle.daily, 1, "Sapiranga - RS"
    )
    # Na resposta real de 21/10/2026 nenhum dia teve máxima >= 35 °C.
    assert not any(i.rule_id == "IND05" for i in found)
    assert all(i.municipality_label == "Sapiranga - RS" for i in found)
    strict = evaluate_indicators(build_rules(IndicatorThresholds(temperature_max_c=25)), [], bundle.daily)
    expected_days = [d["forecast_date"] for d in bundle.daily if d["temperature_max"] >= 25]
    assert [i.reference_time for i in strict if i.rule_id == "IND05"] == expected_days


def test_thresholds_come_from_environment(monkeypatch):
    monkeypatch.setenv("LIMITE_RAJADA_KMH", "45,5")
    monkeypatch.setenv("LIMITE_UMIDADE_MINIMA", "valor-invalido")
    get_settings.cache_clear()
    try:
        t = get_settings().thresholds
        assert t.wind_gusts_kmh == 45.5
        assert t.humidity_min_percent == 30.0  # valor inválido volta ao padrão
    finally:
        get_settings.cache_clear()


def test_rule_engine_does_not_use_eval():
    import ast

    tree = ast.parse(inspect.getsource(ind))
    names = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "eval" not in names
    assert set(ind.OPERATORS) == {">=", "<="}
