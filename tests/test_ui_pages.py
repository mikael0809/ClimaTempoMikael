"""Testes da interface Streamlit (todas as páginas) com banco temporário."""

from __future__ import annotations

import time

import pytest
from streamlit.testing.v1 import AppTest

from src.collectors.alerts_collector import collect_alerts
from src.collectors.weather_collector import collect_weather
from src.config import PROJECT_ROOT, get_settings
from src.integrations.inmet import InmetAlertsClient
from src.integrations.open_meteo import OpenMeteoClient

PAGES = ["painel", "previsao", "alertas", "municipios", "historico", "diagnostico", "aprenda"]


@pytest.fixture
def populated_env(db_url, sapiranga_id, fake_http_ok, monkeypatch, tmp_path):
    collect_alerts(db_url, InmetAlertsClient(fake_http_ok))
    collect_weather(db_url, OpenMeteoClient(fake_http_ok))
    monkeypatch.setenv("CLIMAALERTA_DB_PATH", db_url.removeprefix("sqlite:///"))
    monkeypatch.setenv("CLIMAALERTA_LOG_DIR", str(tmp_path / "logs"))
    get_settings.cache_clear()
    from src.ui import common

    common.get_services.clear()
    yield
    common.get_services.clear()
    get_settings.cache_clear()


def _run_page(page: str) -> AppTest:
    script = (
        f"import sys; sys.path.insert(0, r'{PROJECT_ROOT}')\nfrom src.ui import page_{page}\npage_{page}.render()\n"
    )
    return AppTest.from_string(script, default_timeout=90).run()


@pytest.mark.parametrize("page", PAGES)
def test_page_renders_without_errors(populated_env, page):
    at = _run_page(page)
    assert not at.exception, [e.value for e in at.exception]
    assert at.title


@pytest.mark.parametrize("page", PAGES)
def test_page_render_time(populated_env, page):
    """RNF007: cada página renderiza em até 10 s com o banco local."""
    _run_page(page)  # primeira execução aquece importações e caches
    start = time.perf_counter()
    _run_page(page)
    assert time.perf_counter() - start < 10


def test_dashboard_shows_current_conditions(populated_env):
    at = _run_page("painel")
    labels = [m.label for m in at.metric]
    for expected in ("Temperatura", "Sensação térmica", "Umidade relativa", "Pressão (superfície)", "Rajadas"):
        assert expected in labels
    subheaders = [s.value for s in at.subheader]
    assert any("Alertas oficiais" in s for s in subheaders)
    assert any("Indicadores locais" in s for s in subheaders)


def test_alert_center_separates_official_and_calculated(populated_env):
    at = _run_page("alertas")
    headers = [h.value for h in at.header]
    assert headers.index("🏛️ Alertas oficiais") < headers.index("🧮 Indicadores locais calculados")
    assert any("não são alertas oficiais" in w.value.lower() for w in at.warning)


def test_history_explains_origin_of_records(populated_env):
    at = _run_page("historico")
    assert any("Nenhum registro é inventado" in i.value for i in at.info)
