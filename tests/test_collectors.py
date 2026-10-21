"""Coletores, registro de coletas, falhas de rede e atualização periódica."""

from __future__ import annotations

from sqlalchemy import func, select

from src.collectors.alerts_collector import collect_alerts
from src.collectors.scheduler import run_forever, run_once
from src.collectors.weather_collector import collect_weather
from src.config import get_settings
from src.database import repositories as repo
from src.database.connection import session_scope
from src.database.models import HourlyForecast, WeatherAlert, WeatherForecast, WeatherObservation
from src.integrations.inmet import InmetAlertsClient
from src.integrations.open_meteo import OpenMeteoClient
from src.services.context import build_services


def _counts(db_url):
    with session_scope(db_url) as s:
        return {
            "obs": s.scalar(select(func.count(WeatherObservation.id))),
            "hourly": s.scalar(select(func.count(HourlyForecast.id))),
            "daily": s.scalar(select(func.count(WeatherForecast.id))),
            "alerts": s.scalar(select(func.count(WeatherAlert.id))),
        }


def test_weather_collection_success_and_no_duplicates(db_url, sapiranga_id, fake_http_ok):
    client = OpenMeteoClient(fake_http_ok)
    first = collect_weather(db_url, client)
    assert first[0].status == "SUCESSO" and first[0].records == 1 + 168 + 7
    collect_weather(db_url, client)  # segunda execução: atualiza, não duplica
    assert _counts(db_url) == {"obs": 1, "hourly": 168, "daily": 7, "alerts": 0}
    with session_scope(db_url) as s:
        logs = repo.list_collection_logs(s)
        assert [log.status for log in logs] == ["SUCESSO", "SUCESSO"]
        assert logs[0].municipality_id == sapiranga_id


def test_weather_failure_preserves_existing_data(db_url, sapiranga_id, fake_http_ok, fake_http_down):
    collect_weather(db_url, OpenMeteoClient(fake_http_ok))
    before = _counts(db_url)
    result = collect_weather(db_url, OpenMeteoClient(fake_http_down))
    assert result[0].status == "FALHA" and "esgotado" in result[0].error
    assert _counts(db_url) == before
    with session_scope(db_url) as s:
        failure = repo.last_log(s, "Open-Meteo", "FALHA")
        assert failure.error_message and failure.finished_at


def test_weather_invalid_response_is_logged(db_url, sapiranga_id, fake_http_invalid):
    result = collect_weather(db_url, OpenMeteoClient(fake_http_invalid))
    assert result[0].status == "FALHA"
    assert _counts(db_url)["obs"] == 0


def test_inactive_municipality_is_skipped(db_url, sapiranga_id, fake_http_ok):
    with session_scope(db_url) as s:
        repo.set_municipality_active(s, sapiranga_id, False)
    assert collect_weather(db_url, OpenMeteoClient(fake_http_ok)) == []
    assert len(collect_weather(db_url, OpenMeteoClient(fake_http_ok), [sapiranga_id])) == 1


def test_alert_collection_and_failure(db_url, fake_http_ok, fake_http_down, fake_http_invalid):
    ok = collect_alerts(db_url, InmetAlertsClient(fake_http_ok))
    assert ok.status == "SUCESSO" and ok.records == 4
    assert collect_alerts(db_url, InmetAlertsClient(fake_http_down)).status == "FALHA"
    assert collect_alerts(db_url, InmetAlertsClient(fake_http_invalid)).status == "FALHA"
    assert _counts(db_url)["alerts"] == 4  # avisos anteriores preservados


def _services(db_url, http, monkeypatch, tmp_path):
    monkeypatch.setenv("CLIMAALERTA_DB_PATH", db_url.removeprefix("sqlite:///"))
    monkeypatch.setenv("CLIMAALERTA_LOG_DIR", str(tmp_path / "logs"))
    get_settings.cache_clear()
    return build_services(get_settings(), http=http)


def test_run_once_collects_everything(db_url, fake_http_ok, monkeypatch, tmp_path):
    services = _services(db_url, fake_http_ok, monkeypatch, tmp_path)
    try:
        results = run_once(services)
        assert [r.status for r in results] == ["SUCESSO", "SUCESSO"]
        assert _counts(db_url)["alerts"] == 4
    finally:
        get_settings.cache_clear()


def test_run_forever_respects_interval_and_survives_errors(db_url, fake_http_ok, monkeypatch, tmp_path):
    services = _services(db_url, fake_http_ok, monkeypatch, tmp_path)
    sleeps: list[float] = []
    calls = {"n": 0}

    def flaky(*_args, **_kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("erro inesperado simulado")
        return []

    monkeypatch.setattr("src.collectors.scheduler.run_once", flaky)
    try:
        cycles = run_forever(services, interval_minutes=30, max_cycles=3, sleep=sleeps.append)
        assert cycles == 3 and calls["n"] == 3
        assert sleeps == [1800, 1800]
    finally:
        get_settings.cache_clear()
