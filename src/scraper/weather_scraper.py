"""Extração de dados meteorológicos de uma página web com Selenium.

Fluxo didático:
1. abrir a página (``driver.get``);
2. esperar o conteúdo dinâmico (``WebDriverWait`` + condição esperada);
3. localizar elementos por seletor CSS;
4. ler textos, atributos e links;
5. tratar elementos ausentes sem interromper a extração;
6. normalizar os textos em números.

O alvo padrão é a página local ``exemplos/selenium/pagina_meteorologica_demo.html``,
que contém APENAS DADOS FICTÍCIOS. Os resultados do scraper nunca são
gravados nas tabelas de dados reais.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 4 e 5 · Documento 06 (Fluxograma 4).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config import PROJECT_ROOT
from src.scraper import normalizer
from src.scraper import selectors as sel

logger = logging.getLogger(__name__)

DEMO_PAGE = PROJECT_ROOT / "exemplos" / "selenium" / "pagina_meteorologica_demo.html"
SOURCE_LABEL = "Página de demonstração (DADOS FICTÍCIOS)"


class ScraperError(RuntimeError):
    """Falha na extração (página não carregou ou estrutura inesperada)."""


@dataclass
class ScrapedCity:
    city_id: str | None
    name: str | None
    state_code: str | None
    temperature: float | None
    humidity: float | None
    wind_speed: float | None
    wind_direction: str | None
    condition: str | None
    details_url: str | None
    updated_at: str | None
    missing_fields: list[str] = field(default_factory=list)
    source: str = SOURCE_LABEL


@dataclass
class ScrapedForecastRow:
    date: str | None
    temperature_min: float | None
    temperature_max: float | None
    precipitation_mm: float | None
    source: str = SOURCE_LABEL


@dataclass
class ScrapeResult:
    url: str
    is_demo_data: bool
    page_updated_at: str | None
    cities: list[ScrapedCity]
    forecast: list[ScrapedForecastRow]

    def cities_as_dicts(self) -> list[dict]:
        raise NotImplementedError("TODO: implementar ScrapeResult.cities_as_dicts")


def page_url(path: Path = DEMO_PAGE) -> str:
    raise NotImplementedError("TODO: implementar page_url")


def _optional_text(parent: WebElement, selector: sel.Selector) -> str | None:
    """Lê o texto de um elemento filho; devolve None se ele não existir."""
    raise NotImplementedError("TODO: implementar _optional_text")


def _optional_attribute(parent: WebElement, selector: sel.Selector, attribute: str) -> str | None:
    raise NotImplementedError("TODO: implementar _optional_attribute")


def parse_city_card(card: WebElement) -> ScrapedCity:
    """Converte um cartão de cidade em ``ScrapedCity``, registrando campos ausentes."""
    raise NotImplementedError("TODO: implementar parse_city_card")


def parse_forecast_row(row: WebElement) -> ScrapedForecastRow | None:
    raise NotImplementedError("TODO: implementar parse_forecast_row")


class WeatherPageScraper:
    def __init__(self, driver: WebDriver, timeout: float = 10.0) -> None:
        raise NotImplementedError("TODO: implementar WeatherPageScraper.__init__")

    def wait_until_loaded(self) -> None:
        """Espera explícita: aguarda o marcador de carregamento ficar presente."""
        raise NotImplementedError("TODO: implementar WeatherPageScraper.wait_until_loaded")

    def scrape(self, url: str | None = None) -> ScrapeResult:
        raise NotImplementedError("TODO: implementar WeatherPageScraper.scrape")
