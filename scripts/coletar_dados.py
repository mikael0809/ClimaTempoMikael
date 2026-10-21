"""Coleta manual ou periódica de previsões (Open-Meteo) e avisos (INMET).

Uso (na raiz do projeto, com o ambiente virtual ativo):
    python scripts/coletar_dados.py                 # uma rodada
    python scripts/coletar_dados.py --loop          # repete no intervalo do .env
    python scripts/coletar_dados.py --loop --intervalo 30
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

from src.collectors.scheduler import run_forever, run_once
from src.services.context import build_services
from src.utils.logging_config import setup_logging


def main() -> int:
    raise NotImplementedError("TODO: implementar main")


if __name__ == "__main__":
    raise SystemExit(main())
