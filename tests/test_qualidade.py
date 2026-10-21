"""Qualidade de código e registros de log (RNF009, RNF011)."""

from __future__ import annotations

import logging
import subprocess
import sys

from src.config import PROJECT_ROOT
from src.utils.logging_config import create_file_handler


def test_ruff_reports_no_problems():
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "."], cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_log_file_is_rotating_and_utf8(tmp_path):
    handler = create_file_handler(tmp_path / "logs")
    logger = logging.getLogger("teste.climaalerta")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    try:
        logger.info("Coleta concluída para São Leopoldo")
    finally:
        logger.removeHandler(handler)
        handler.close()
    content = (tmp_path / "logs" / "climaalerta.log").read_text(encoding="utf-8")
    assert "São Leopoldo" in content and "| INFO" in content
    assert handler.maxBytes == 1_000_000 and handler.backupCount == 5
