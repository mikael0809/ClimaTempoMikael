"""Coletor de avisos oficiais do INMET.

Uma única consulta traz os avisos ativos de todo o país. Os avisos são
gravados por *upsert* (sem duplicar) e os que deixaram de constar na lista
de ativos são marcados como ENCERRADO. Em caso de falha, nada é alterado:
a central continua exibindo a última atualização conhecida.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 11 e 12 · Documento 05 (BPMN 1 e 4) · Documento 06 (Fluxogramas 3 e 10).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging

from src.collectors.weather_collector import CollectionResult, finish_log
from src.database import repositories as repo
from src.database.connection import session_scope
from src.database.models import CollectionLog
from src.integrations.http_client import InvalidResponseError, SourceUnavailableError
from src.integrations.inmet import SOURCE_NAME, InmetAlertsClient

logger = logging.getLogger(__name__)


def collect_alerts(database_url: str, client: InmetAlertsClient) -> CollectionResult:
    raise NotImplementedError("TODO: implementar collect_alerts")
