"""Web Scraping com Selenium em páginas HTML locais (Chrome headless real).

Os testes são ignorados (skip) se o Chrome não puder ser iniciado.
"""

from __future__ import annotations

import pandas as pd
import pytest
from sqlalchemy import func, select

from src.collectors.scraper_demo import run_demo_scraper
from src.database import repositories as repo
from src.database.connection import session_scope
from src.database.models import WeatherObservation
from src.scraper.driver import BrowserUnavailableError, create_chrome_driver
from src.scraper.weather_scraper import DEMO_PAGE, ScraperError, WeatherPageScraper, page_url
from tests.conftest import FIXTURES

pytestmark = pytest.mark.selenium


@pytest.fixture(scope="module")
def driver():
    try:
        drv = create_chrome_driver(headless=True)
    except BrowserUnavailableError as exc:
        pytest.skip(f"Chrome indisponível: {exc}")
    yield drv
    drv.quit()


def test_demo_page_extraction(driver):
    result = WeatherPageScraper(driver, timeout=10).scrape(page_url(DEMO_PAGE))
    assert result.is_demo_data
    assert result.page_updated_at == "2026-10-21T14:00:00-03:00"
    by_id = {c.city_id: c for c in result.cities}
    assert set(by_id) == {"sapiranga-rs", "porto-alegre-rs", "cidade-exemplo-sc", "vila-modelo-pr"}
    sap = by_id["sapiranga-rs"]
    assert (sap.name, sap.state_code, sap.temperature, sap.humidity) == ("Sapiranga", "RS", 24.5, 57.0)
    assert (sap.wind_speed, sap.wind_direction) == (13.5, "SE")
    assert sap.details_url.startswith("file:///") and sap.details_url.endswith("detalhes.html#sapiranga-rs")
    assert sap.missing_fields == []
    assert "DADOS FICTÍCIOS" in sap.source


def test_demo_page_missing_and_unavailable_values(driver):
    result = WeatherPageScraper(driver, timeout=10).scrape(page_url(DEMO_PAGE))
    by_id = {c.city_id: c for c in result.cities}
    assert by_id["cidade-exemplo-sc"].humidity is None  # elemento ausente no HTML
    assert by_id["cidade-exemplo-sc"].missing_fields == ["humidity"]
    assert by_id["vila-modelo-pr"].temperature is None  # valor "—"
    assert [r.date for r in result.forecast] == ["2026-10-22", "2026-10-23", "2026-10-24", "2026-10-25"]
    assert result.forecast[3].precipitation_mm == 25.2


def test_explicit_wait_times_out_when_content_never_loads(driver):
    with pytest.raises(ScraperError, match="não terminou de carregar"):
        WeatherPageScraper(driver, timeout=1.5).scrape(page_url(FIXTURES / "scraper_sem_carregamento.html"))


def test_changed_structure_raises_clear_error(driver):
    with pytest.raises(ScraperError, match="Nenhum cartão"):
        WeatherPageScraper(driver, timeout=3).scrape(page_url(FIXTURES / "scraper_sem_cartoes.html"))


def test_missing_elements_do_not_stop_extraction(driver):
    result = WeatherPageScraper(driver, timeout=3).scrape(page_url(FIXTURES / "scraper_elementos_ausentes.html"))
    assert not result.is_demo_data  # a faixa de dados fictícios não existe nesta página
    assert result.page_updated_at is None
    complete, incomplete, empty = result.cities
    assert complete.details_url == "https://exemplo.test/detalhes/completa"
    assert complete.wind_direction == "NO"
    assert incomplete.temperature is None  # 999 °C descartado pela validação
    assert incomplete.condition is None and incomplete.details_url is None
    assert set(incomplete.missing_fields) == {"temperature", "humidity", "wind_speed", "condition"}
    assert empty.city_id is None and empty.name is None
    assert len(result.forecast) == 1 and result.forecast[0].precipitation_mm is None


def test_demo_collector_writes_csv_and_log_but_not_real_tables(db_url, tmp_path):
    output = tmp_path / "scraper.csv"
    status, result = run_demo_scraper(db_url, headless=True, timeout=10, output=output)
    assert status.status == "SUCESSO" and status.records == 4
    df = pd.read_csv(output, sep=";", decimal=",")
    assert set(df["source"]) == {"Página de demonstração (DADOS FICTÍCIOS)"}
    with session_scope(db_url) as s:
        assert repo.last_log(s, "DEMO_SELENIUM", "SUCESSO") is not None
        assert s.scalar(select(func.count(WeatherObservation.id))) == 0  # nunca mistura com dados reais
