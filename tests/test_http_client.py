"""Cliente HTTP: timeouts, falhas de rede, HTTP de erro e JSON inválido."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import requests

from src.integrations.http_client import HttpClient, InvalidResponseError, SourceUnavailableError, build_session


def _client_with(side_effect=None, response=None) -> HttpClient:
    session = MagicMock(spec=requests.Session)
    if side_effect is not None:
        session.get.side_effect = side_effect
    else:
        session.get.return_value = response
    return HttpClient(session=session, timeout=3)


def _response(status: int, body: bytes = b"{}") -> requests.Response:
    r = requests.Response()
    r.status_code = status
    r._content = body
    return r


def test_timeout_becomes_source_unavailable():
    client = _client_with(side_effect=requests.Timeout("lento"))
    with pytest.raises(SourceUnavailableError, match="Tempo de resposta"):
        client.get_json("https://exemplo.test/api")


def test_connection_error_becomes_source_unavailable():
    client = _client_with(side_effect=requests.ConnectionError("sem rede"))
    with pytest.raises(SourceUnavailableError, match="ConnectionError"):
        client.get_json("https://exemplo.test/api")


def test_http_500_becomes_source_unavailable():
    client = _client_with(response=_response(503))
    with pytest.raises(SourceUnavailableError, match="HTTP 503"):
        client.get_json("https://exemplo.test/api")


def test_invalid_json_becomes_invalid_response():
    client = _client_with(response=_response(200, b"<html>manutencao</html>"))
    with pytest.raises(InvalidResponseError):
        client.get_json("https://exemplo.test/api")


def test_valid_json_and_timeout_is_passed():
    client = _client_with(response=_response(200, b'{"ok": 1}'))
    assert client.get_json("https://exemplo.test/api", {"a": 1}) == {"ok": 1}
    client.session.get.assert_called_once_with("https://exemplo.test/api", params={"a": 1}, timeout=3)


def test_session_has_limited_retries_and_user_agent():
    session = build_session("ClimaAlerta-teste", max_retries=2, backoff_factor=0.5)
    retry = session.get_adapter("https://api.open-meteo.com").max_retries
    assert retry.total == 2
    assert 503 in retry.status_forcelist and 429 in retry.status_forcelist
    assert session.headers["User-Agent"] == "ClimaAlerta-teste"
