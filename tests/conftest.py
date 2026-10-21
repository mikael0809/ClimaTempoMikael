"""Fixtures compartilhadas pelos testes.

Nenhum teste acessa a internet: as integrações recebem um ``FakeHttp`` que
devolve respostas REAIS gravadas em ``tests/fixtures`` (coletadas em
21/10/2026) ou simula falhas de rede.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from src.database import connection
from src.database.connection import get_session_factory, session_scope
from src.integrations.http_client import InvalidResponseError, SourceUnavailableError
from src.services.municipality_service import SAPIRANGA, ensure_default_municipality

FIXTURES = Path(__file__).parent / "fixtures"
# "Agora" fixo, coerente com as respostas gravadas: 21/10/2026 15:00 em Brasília.
NOW = datetime(2026, 10, 21, 18, 0, 0)


def load_json(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class FakeHttp:
    """Substitui o HttpClient: devolve respostas pré-definidas por trecho de URL."""

    def __init__(self, routes: dict[str, Any] | None = None) -> None:
        self.routes = routes or {}
        self.calls: list[tuple[str, dict | None]] = []

    def get_json(self, url: str, params: dict | None = None) -> Any:
        self.calls.append((url, params))
        for fragment, answer in self.routes.items():
            if fragment in url:
                if isinstance(answer, Exception):
                    raise answer
                return answer
        raise SourceUnavailableError(f"Rota não configurada no teste: {url}")


@pytest.fixture
def forecast_payload() -> dict:
    return load_json("open_meteo_forecast_sapiranga.json")


@pytest.fixture
def geocoding_payload() -> dict:
    return load_json("open_meteo_geocoding_sapiranga.json")


@pytest.fixture
def inmet_payload() -> dict:
    return load_json("inmet_avisos_ativos_amostra.json")


@pytest.fixture
def db_url(tmp_path: Path) -> str:
    url = f"sqlite:///{(tmp_path / 'teste.db').as_posix()}"
    yield url
    connection.dispose_engines()


@pytest.fixture
def session(db_url: str):
    """Sessão de teste: desfeita ao final (permite testar erros de integridade)."""
    s = get_session_factory(db_url)()
    yield s
    s.rollback()
    s.close()


@pytest.fixture
def sapiranga_id(db_url: str) -> int:
    with session_scope(db_url) as s:
        return ensure_default_municipality(s).id


@pytest.fixture
def fake_http_ok(forecast_payload, inmet_payload, geocoding_payload) -> FakeHttp:
    return FakeHttp(
        {
            "//api.open-meteo.com": forecast_payload,
            "apiprevmet3.inmet.gov.br": inmet_payload,
            "geocoding-api": geocoding_payload,
            "servicodados.ibge.gov.br": [{"id": 4319901, "nome": "Sapiranga"}, {"id": 4314902, "nome": "Porto Alegre"}],
        }
    )


@pytest.fixture
def fake_http_down() -> FakeHttp:
    error = SourceUnavailableError("Tempo de resposta esgotado (simulado)")
    return FakeHttp({"//api.open-meteo.com": error, "apiprevmet3": error, "geocoding": error, "ibge": error})


@pytest.fixture
def fake_http_invalid() -> FakeHttp:
    return FakeHttp({"//api.open-meteo.com": {"inesperado": True}, "apiprevmet3": ["lista", "inválida"]})


__all__ = ["FakeHttp", "NOW", "SAPIRANGA", "InvalidResponseError", "load_json", "FIXTURES"]
