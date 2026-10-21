"""Pesquisa de municípios (geocodificação Open-Meteo + código IBGE)."""

from __future__ import annotations

import pytest

from src.integrations.geocoding import GeocodingClient, find_ibge_code, parse_geocoding
from src.integrations.http_client import InvalidResponseError
from src.utils.validators import ValidationError
from tests.conftest import FakeHttp


def test_parse_real_geocoding(geocoding_payload):
    candidates = parse_geocoding(geocoding_payload)
    assert [c.state_code for c in candidates] == ["RS", "SC"]
    sapiranga = candidates[0]
    assert sapiranga.name == "Sapiranga"
    assert (sapiranga.latitude, sapiranga.longitude) == (-29.63806, -51.00694)
    assert sapiranga.geonames_id == 3448063
    assert "Sapiranga - RS" in sapiranga.label


def test_no_results_key_means_empty_list():
    # Comportamento real verificado: sem resultados, a API omite "results".
    assert parse_geocoding({"generationtime_ms": 0.1}) == []


def test_foreign_and_non_populated_places_are_ignored():
    payload = {
        "results": [
            {"name": "Lisboa", "country_code": "PT", "admin1": "Lisboa", "latitude": 38.7, "longitude": -9.1},
            {
                "name": "Aeroporto",
                "country_code": "BR",
                "feature_code": "AIRP",
                "admin1": "Rio Grande do Sul",
                "latitude": -29.9,
                "longitude": -51.1,
            },
            {"name": "Sem UF", "country_code": "BR", "admin1": "Desconhecido", "latitude": -10, "longitude": -50},
        ]
    }
    assert parse_geocoding(payload) == []


def test_invalid_geocoding_payload():
    with pytest.raises(InvalidResponseError):
        parse_geocoding(["x"])


def test_find_ibge_code_ignores_accents():
    payload = [{"id": 4318705, "nome": "São Leopoldo"}, {"id": 4319901, "nome": "Sapiranga"}]
    assert find_ibge_code(payload, "Sao Leopoldo") == 4318705
    assert find_ibge_code(payload, "Inexistente") is None


def test_client_search_validates_term(fake_http_ok):
    client = GeocodingClient(fake_http_ok)
    with pytest.raises(ValidationError):
        client.search("x")
    assert client.search("Sapiranga")[0].name == "Sapiranga"
    assert fake_http_ok.calls[-1][1]["countryCode"] == "BR"


def test_ibge_lookup_returns_none_when_offline(fake_http_down):
    assert GeocodingClient(fake_http_down).lookup_ibge_code("Sapiranga", "RS") is None


def test_ibge_lookup_success(fake_http_ok):
    assert GeocodingClient(fake_http_ok).lookup_ibge_code("Sapiranga", "rs") == 4319901


def test_ibge_lookup_invalid_payload():
    http = FakeHttp({"ibge": {"erro": "x"}})
    assert GeocodingClient(http).lookup_ibge_code("Sapiranga", "RS") is None
