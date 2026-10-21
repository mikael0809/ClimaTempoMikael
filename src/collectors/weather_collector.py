"""Coletor de previsões e condições atuais (Open-Meteo -> SQLite).

Cada município é coletado em sua própria transação. Se a fonte falhar, a
transação de dados não é aberta e os registros válidos já existentes
permanecem intactos (RN010). Toda tentativa gera um ``CollectionLog``.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 11 e 12 · Documento 05 (BPMN 1 e 4) · Documento 06 (Fluxogramas 3 e 10).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from dataclasses import dataclass

from src.database import repositories as repo
from src.database.connection import session_scope
from src.database.models import CollectionLog
from src.integrations.http_client import InvalidResponseError, SourceUnavailableError
from src.integrations.open_meteo import SOURCE_NAME, OpenMeteoClient

logger = logging.getLogger(__name__)


@dataclass
class CollectionResult:
    source: str
    municipality: str | None
    status: str
    records: int
    error: str | None = None


def finish_log(database_url: str, log_id: int, status: str, records: int, error: str | None) -> None:
    raise NotImplementedError("TODO: implementar finish_log")


def collect_weather(
    database_url: str,
    client: OpenMeteoClient,
    municipality_ids: list[int] | None = None,
    forecast_days: int = 7,
) -> list[CollectionResult]:
    raise NotImplementedError("TODO: implementar collect_weather")
