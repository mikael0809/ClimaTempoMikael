"""Cliente HTTP compartilhado pelas integrações.

Recursos de confiabilidade:
* ``timeout`` em todas as requisições (nunca esperar para sempre);
* retentativas limitadas, com espera crescente (*backoff*), apenas para
  falhas transitórias (erros 429, 500, 502, 503, 504 e falhas de conexão);
* ``User-Agent`` que identifica o projeto, por cortesia com as fontes;
* conversão dos erros em exceções do próprio projeto.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 6 · Documento 03 (Arquitetura) · Documento 12 (Interfaces).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class SourceUnavailableError(RuntimeError):
    """A fonte externa não respondeu (rede, timeout ou erro HTTP)."""


class InvalidResponseError(ValueError):
    """A fonte respondeu, mas o conteúdo não tem o formato esperado."""


def build_session(user_agent: str, max_retries: int = 3, backoff_factor: float = 1.0) -> requests.Session:
    raise NotImplementedError("TODO: implementar build_session")


class HttpClient:
    def __init__(
        self,
        user_agent: str = "ClimaAlerta/1.0 (projeto educacional)",
        timeout: float = 15.0,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        session: requests.Session | None = None,
    ) -> None:
        raise NotImplementedError("TODO: implementar HttpClient.__init__")

    def get(self, url: str, params: dict[str, Any] | None = None) -> requests.Response:
        raise NotImplementedError("TODO: implementar HttpClient.get")

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        raise NotImplementedError("TODO: implementar HttpClient.get_json")
