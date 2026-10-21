"""Criação e encerramento do WebDriver (Chrome/Chromium).

O Selenium 4 inclui o *Selenium Manager*, que localiza ou baixa
automaticamente o ``chromedriver`` compatível com o Chrome instalado.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 4 e 5 · Documento 06 (Fluxograma 4).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)


class BrowserUnavailableError(RuntimeError):
    """Não foi possível iniciar o navegador."""


def build_chrome_options(headless: bool = True) -> Options:
    raise NotImplementedError("TODO: implementar build_chrome_options")


def create_chrome_driver(headless: bool = True, page_load_timeout: float = 30.0) -> webdriver.Chrome:
    raise NotImplementedError("TODO: implementar create_chrome_driver")


@contextmanager
def chrome_driver(headless: bool = True) -> Iterator[webdriver.Chrome]:
    """Uso: ``with chrome_driver() as driver: ...`` — o navegador sempre é fechado."""
    raise NotImplementedError("TODO: implementar chrome_driver")
