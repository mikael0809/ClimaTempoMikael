"""Executa o scraper Selenium na página local de demonstração (dados fictícios).

Uso (na raiz do projeto, com o ambiente virtual ativo):
    python scripts/executar_scraper_demo.py
    python scripts/executar_scraper_demo.py --visivel   # abre a janela do Chrome
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 11 e 12 · Documento 09 (Implantação e operação).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401

from src.collectors.scraper_demo import OUTPUT_CSV, run_demo_scraper
from src.config import get_settings
from src.utils.logging_config import setup_logging


def main() -> int:
    raise NotImplementedError("TODO: implementar main")


if __name__ == "__main__":
    raise SystemExit(main())
