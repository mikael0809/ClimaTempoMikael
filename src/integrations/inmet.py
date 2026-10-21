"""Integração com os avisos meteorológicos oficiais do INMET.

Fonte verificada em 21/10/2026:
* ``https://apiprevmet3.inmet.gov.br/avisos/ativos`` — JSON público consumido
  pelo portal https://avisos.inmet.gov.br, com as listas ``hoje`` e
  ``futuro``. Não há documentação formal publicada desse endpoint; os campos
  abaixo foram validados na resposta real (amostra em
  ``tests/fixtures/inmet_avisos_ativos_amostra.json``).
* ``https://apiprevmet3.inmet.gov.br/avisos/rss/{id}`` — o mesmo aviso em
  formato CAP 1.2 (XML), cujo campo ``<web>`` aponta para
  ``https://avisos.inmet.gov.br/{id}``, usado como link oficial.

Os textos e a severidade são preservados exatamente como publicados.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 6 · Documento 03 (Arquitetura) · Documento 12 (Interfaces).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from src.integrations.http_client import HttpClient, InvalidResponseError
from src.utils.timeutils import local_to_utc

logger = logging.getLogger(__name__)

SOURCE_NAME = "INMET"
INMET_TZ = "America/Sao_Paulo"  # os campos 'inicio'/'fim' estão no horário de Brasília
REQUIRED_FIELDS = ("id", "descricao", "severidade", "inicio", "fim")
# Escala de severidade publicada pelo INMET, da menor para a maior.
SEVERITY_ORDER = ["Perigo Potencial", "Perigo", "Grande Perigo"]


def _join(value: Any) -> str | None:
    raise NotImplementedError("TODO: implementar _join")


def _parse_local(value: Any) -> datetime | None:
    raise NotImplementedError("TODO: implementar _parse_local")


def _parse_utc(value: Any) -> datetime | None:
    """Converte '2026-10-20T00:00:00.000Z' para UTC ingênuo."""
    raise NotImplementedError("TODO: implementar _parse_utc")


def parse_alert(item: dict[str, Any], page_url_template: str = "https://avisos.inmet.gov.br/{id}") -> dict[str, Any]:
    """Converte um aviso do JSON do INMET em uma linha da tabela weather_alert."""
    raise NotImplementedError("TODO: implementar parse_alert")


def parse_active_alerts(
    payload: Any, page_url_template: str = "https://avisos.inmet.gov.br/{id}"
) -> list[dict[str, Any]]:
    """Lê as listas 'hoje' e 'futuro'; avisos malformados são ignorados e registrados."""
    raise NotImplementedError("TODO: implementar parse_active_alerts")


def alert_applies_to(alert: dict[str, Any] | Any, ibge_code: int | None, state_name: str | None) -> bool:
    """Indica se o aviso abrange o município (pelo código IBGE) ou, sem código, pela UF."""
    raise NotImplementedError("TODO: implementar alert_applies_to")


class InmetAlertsClient:
    def __init__(
        self,
        http: HttpClient,
        url: str = "https://apiprevmet3.inmet.gov.br/avisos/ativos",
        page_url_template: str = "https://avisos.inmet.gov.br/{id}",
    ) -> None:
        raise NotImplementedError("TODO: implementar InmetAlertsClient.__init__")

    def fetch_active_alerts(self) -> list[dict[str, Any]]:
        raise NotImplementedError("TODO: implementar InmetAlertsClient.fetch_active_alerts")
