"""Permite executar os scripts com ``python scripts/<nome>.py`` a partir da raiz.

Acrescenta a raiz do projeto ao ``sys.path`` para que ``import src...``
funcione sem instalar o pacote.
"""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Saída em UTF-8 também no console do Windows (acentos e símbolos).
for stream in (sys.stdout, sys.stderr):
    with contextlib.suppress(AttributeError, ValueError):
        stream.reconfigure(encoding="utf-8")
