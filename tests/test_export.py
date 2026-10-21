"""Exportação CSV (RN011)."""

from __future__ import annotations

import io

import pandas as pd

from src.database import repositories as repo
from src.integrations.inmet import parse_active_alerts
from src.integrations.open_meteo import parse_forecast
from src.services.export_service import (
    alerts_export_frame,
    indicators_export_frame,
    prepare_weather_export,
    to_csv_bytes,
    write_csv,
)
from src.services.indicators import LocalIndicator
from src.services.weather_service import daily_frame, hourly_frame


def _read(data: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(data), sep=";", decimal=",", encoding="utf-8-sig")


def test_csv_format_is_excel_friendly(session, sapiranga_id, forecast_payload):
    bundle = parse_forecast(forecast_payload)
    repo.upsert_daily_forecasts(session, sapiranga_id, bundle.daily)
    session.flush()
    df = prepare_weather_export(
        daily_frame(repo.list_daily_forecasts(session, sapiranga_id, bundle.daily[0]["forecast_date"])),
        "PREVISAO DIARIA",
    )
    data = to_csv_bytes(df)
    assert data.startswith(b"\xef\xbb\xbf")  # BOM UTF-8
    header = data.decode("utf-8-sig").splitlines()[0]
    assert "temperatura_maxima_c" in header and ";" in header and "tipo_registro" in header
    back = _read(data)
    assert len(back) == 7
    assert back["temperatura_maxima_c"].iloc[0] == bundle.daily[0]["temperature_max"]
    assert set(back["fonte"]) == {"Open-Meteo"}


def test_hourly_export_keeps_brasilia_time(session, sapiranga_id, forecast_payload):
    bundle = parse_forecast(forecast_payload)
    repo.upsert_hourly_forecasts(session, sapiranga_id, bundle.hourly[:3])
    session.flush()
    rows = repo.list_hourly_forecasts(
        session, sapiranga_id, bundle.hourly[0]["forecast_time"], bundle.hourly[2]["forecast_time"]
    )
    text = to_csv_bytes(prepare_weather_export(hourly_frame(rows), "PREVISAO HORARIA")).decode("utf-8-sig")
    assert "21/10/2026 00:00" in text  # 03:00 UTC exibido como 00:00 em Brasília


def test_alerts_export_identifies_official_records(inmet_payload, session):
    repo.upsert_alerts(session, parse_active_alerts(inmet_payload))
    session.flush()
    back = _read(to_csv_bytes(alerts_export_frame(repo.list_alerts(session))))
    assert set(back["tipo_registro"]) == {"ALERTA OFICIAL"}
    assert back["link_oficial"].str.startswith("https://avisos.inmet.gov.br/").all()


def test_indicators_export_identifies_calculated_records():
    from datetime import date

    indicator = LocalIndicator(
        "IND05",
        "Temperatura máxima elevada",
        36.2,
        35,
        ">=",
        "°C",
        date(2026, 10, 23),
        "DIARIA",
        1,
        "regra",
        "Open-Meteo",
        1,
        "Sapiranga - RS",
    )
    back = _read(to_csv_bytes(indicators_export_frame([indicator])))
    assert back["tipo_registro"].iloc[0] == "INDICADOR CALCULADO (não oficial)"
    assert back["valor_encontrado"].iloc[0] == 36.2
    assert back["referencia"].iloc[0] == "23/10/2026"


def test_write_csv(tmp_path):
    path = write_csv(pd.DataFrame({"a": [1.5]}), tmp_path / "sub" / "x.csv")
    assert path.read_bytes().startswith(b"\xef\xbb\xbf")
    assert "1,5" in path.read_text(encoding="utf-8-sig")
