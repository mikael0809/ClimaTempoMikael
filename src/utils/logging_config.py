"""Configuração centralizada de logging.

Os registros são enviados para o console e para ``logs/climaalerta.log``
(arquivo rotativo, para não crescer indefinidamente).
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 2 · Documento 10 (Validação de entradas) · Documento 12.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_CONFIGURED = False
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def create_file_handler(log_dir: Path) -> RotatingFileHandler:
    """Arquivo de log rotativo: até 1 MB por arquivo, 5 arquivos de histórico."""
    raise NotImplementedError("TODO: implementar create_file_handler")


def setup_logging(log_dir: Path | None = None, level: str = "INFO") -> None:
    """Configura o logging uma única vez por processo."""
    raise NotImplementedError("TODO: implementar setup_logging")
