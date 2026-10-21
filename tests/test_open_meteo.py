"""Integração Open-Meteo: conversão, validação e respostas inválidas."""

from __future__ import annotations

import copy
from datetime import date, datetime

import pytest

from src.integrations.http_client import InvalidResponseError, SourceUnavailableError
from src.integrations.open_meteo import (
    DAILY_VARIABLES,
    HOURLY_VARIABLES,
    OpenMeteoClient,
    build_params,
    current_hour_probability,
    parse_forecast,
)
from tests.conftest import FakeHttp


def test_parse_real_response(forecast_payload):
    bundle = parse_forecast(forecast_payload)
    assert bundle.timezone == "America/Sao_Paulo"
    assert len(bundle.hourly) == 168  # 7 dias x 24 h
    assert len(bundle.daily) == 7
    assert bundle.current["source"] == "Open-Meteo"
    # 14:45 em Brasília = 17:45 UTC
    assert bundle.current["observed_at"] == datetime(2026, 10, 21, 17, 45)
    assert bundle.current["temperature"] == forecast_payload["current"]["temperature_2m"]
    assert bundle.current["pressure"] == forecast_payload["current"]["surface_pressure"]
    first_day = bundle.daily[0]
    assert first_day["forecast_date"] == date(2026, 10, 21)
    assert first_day["temperature_max"] == forecast_payload["daily"]["temperature_2m_max"][0]
    assert first_day["uv_index_max"] == forecast_payload["daily"]["uv_index_max"][0]
    assert bundle.hourly[0]["forecast_time"] == datetime(2026, 10, 21, 3, 0)  # 00:00 local


def test_weather_code_is_integer(forecast_payload):
    bundle = parse_forecast(forecast_payload)
    assert isinstance(bundle.current["weather_code"], int)
    assert all(isinstance(r["weather_code"], int) for r in bundle.daily)


def test_out_of_range_values_become_none(forecast_payload):
    payload = copy.deepcopy(forecast_payload)
    payload["current"]["relative_humidity_2m"] = 180
    payload["hourly"]["temperature_2m"][0] = 999
    bundle = parse_forecast(payload)
    assert bundle.current["humidity"] is None
    assert bundle.hourly[0]["temperature"] is None


def test_missing_values_become_none(forecast_payload):
    payload = copy.deepcopy(forecast_payload)
    payload["hourly"]["uv_index"] = [None] * len(payload["hourly"]["time"])
    del payload["daily"]["uv_index_max"]
    bundle = parse_forecast(payload)
    assert all(r["uv_index"] is None for r in bundle.hourly)
    assert all(r["uv_index_max"] is None for r in bundle.daily)


@pytest.mark.parametrize("payload", [None, [], "texto", {}, {"error": True, "reason": "Latitude inválida"}])
def test_invalid_payloads(payload):
    with pytest.raises(InvalidResponseError):
        parse_forecast(payload)


def test_series_with_different_lengths_is_rejected(forecast_payload):
    payload = copy.deepcopy(forecast_payload)
    payload["hourly"]["temperature_2m"] = payload["hourly"]["temperature_2m"][:10]
    with pytest.raises(InvalidResponseError, match="tamanho"):
        parse_forecast(payload)


def test_current_hour_probability(forecast_payload):
    bundle = parse_forecast(forecast_payload)
    # hora corrente: 14:00 local = índice 14 da série horária
    assert current_hour_probability(bundle) == forecast_payload["hourly"]["precipitation_probability"][14]


def test_build_params_requests_metric_units_and_timezone():
    params = build_params(-29.6, -51.0)
    assert params["timezone"] == "America/Sao_Paulo"
    assert params["wind_speed_unit"] == "kmh"
    assert params["forecast_days"] == 7
    assert set(params["hourly"].split(",")) == set(HOURLY_VARIABLES)
    assert set(params["daily"].split(",")) == set(DAILY_VARIABLES)


def test_client_uses_http_and_fills_probability(forecast_payload):
    http = FakeHttp({"api.open-meteo.com": forecast_payload})
    bundle = OpenMeteoClient(http).fetch_forecast(-29.63806, -51.00694)
    assert http.calls[0][1]["latitude"] == -29.63806
    assert bundle.current["precipitation_probability"] is not None


def test_client_propagates_network_failure(fake_http_down):
    with pytest.raises(SourceUnavailableError):
        OpenMeteoClient(fake_http_down).fetch_forecast(-29.6, -51.0)
