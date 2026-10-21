"""Execução do scraper Selenium sobre a página local de demonstração.

Os dados extraídos são FICTÍCIOS: vão apenas para um CSV próprio
(``data/scraper_demo_resultado.csv``) e para o log de coletas, nunca para as
tabelas de dados meteorológicos reais.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 11 e 12 · Documento 05 (BPMN 1 e 4) · Documento 06 (Fluxogramas 3 e 10).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.collectors.weather_collector import CollectionResult, finish_log
from src.config import PROJECT_ROOT
from src.database import repositories as repo
from src.database.connection import session_scope
from src.scraper.driver import BrowserUnavailableError, chrome_driver
from src.scraper.weather_scraper import ScraperError, ScrapeResult, WeatherPageScraper, page_url

logger = logging.getLogger(__name__)

SOURCE_NAME = "DEMO_SELENIUM"
OUTPUT_CSV = PROJECT_ROOT / "data" / "scraper_demo_resultado.csv"


def run_demo_scraper(
    database_url: str | None = None, headless: bool = True, timeout: float = 10.0, output: Path = OUTPUT_CSV
) -> tuple[CollectionResult, ScrapeResult | None]:
    raise NotImplementedError("TODO: implementar run_demo_scraper")
