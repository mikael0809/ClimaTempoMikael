"""Página: Pesquisa e cadastro de municípios monitorados."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 3 e 10 · Documento 07 (Casos de uso) · capturas no Documento 07.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import repositories as repo
from src.integrations.http_client import InvalidResponseError, SourceUnavailableError
from src.services.municipality_service import register_candidate, register_manual
from src.ui import common
from src.utils.brazil import STATES
from src.utils.validators import ValidationError


def render() -> None:
    raise NotImplementedError("TODO: implementar render")
