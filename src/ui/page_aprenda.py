"""Página educacional: APIs, Web Scraping e funcionamento do sistema."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.collectors.scraper_demo import OUTPUT_CSV, run_demo_scraper
from src.integrations.open_meteo import build_params
from src.scraper import selectors
from src.ui import common


def render() -> None:
    raise NotImplementedError("TODO: implementar render")
