"""Atualização manual e periódica.

* ``run_once``: executa uma rodada completa (avisos + previsões).
* ``run_forever``: repete a rodada a cada N minutos até ser interrompido
  (Ctrl+C). ``max_cycles`` existe para os testes.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 11 e 12 · Documento 05 (BPMN 1 e 4) · Documento 06 (Fluxogramas 3 e 10).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
import time
from collections.abc import Callable

from src.collectors.alerts_collector import collect_alerts
from src.collectors.weather_collector import CollectionResult, collect_weather
from src.database.connection import session_scope
from src.services.context import AppServices
from src.services.municipality_service import ensure_default_municipality

logger = logging.getLogger(__name__)


def run_once(services: AppServices, municipality_ids: list[int] | None = None) -> list[CollectionResult]:
    raise NotImplementedError("TODO: implementar run_once")


def run_forever(
    services: AppServices,
    interval_minutes: int | None = None,
    max_cycles: int | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    raise NotImplementedError("TODO: implementar run_forever")
