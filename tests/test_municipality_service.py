"""Cadastro e consulta de municípios (RN001, RN002, RN005)."""

from __future__ import annotations

import pytest

from src.database import repositories as repo
from src.integrations.geocoding import GeocodingClient, parse_geocoding
from src.services.municipality_service import (
    SAPIRANGA,
    ensure_default_municipality,
    register_candidate,
    register_manual,
)
from src.utils.validators import ValidationError


def test_default_municipality_is_idempotent(session):
    first = ensure_default_municipality(session)
    second = ensure_default_municipality(session)
    assert first.id == second.id
    assert len(repo.list_municipalities(session)) == 1
    assert first.ibge_code == 4319901
    assert (first.latitude, first.longitude) == (SAPIRANGA["latitude"], SAPIRANGA["longitude"])


def test_register_candidate_from_search(session, fake_http_ok, geocoding_payload):
    candidate = parse_geocoding(geocoding_payload)[0]
    m = register_candidate(session, candidate, GeocodingClient(fake_http_ok))
    assert m.label == "Sapiranga - RS"
    assert m.ibge_code == 4319901
    assert "GeoNames 3448063" in m.coordinates_source
    with pytest.raises(repo.DuplicateMunicipalityError):
        register_candidate(session, candidate, None)


def test_register_candidate_without_ibge_when_offline(session, fake_http_down, geocoding_payload):
    candidate = parse_geocoding(geocoding_payload)[1]  # Sapiranga - SC
    m = register_candidate(session, candidate, GeocodingClient(fake_http_down))
    assert m.state_code == "SC" and m.ibge_code is None


def test_register_manual_valid(session):
    m = register_manual(session, "  Novo   Hamburgo ", "rs", -29.6783, -51.1306, 4313409)
    assert m.name == "Novo Hamburgo" and m.state == "Rio Grande do Sul"
    assert m.coordinates_source == "Informadas manualmente pelo usuário"


@pytest.mark.parametrize(
    ("name", "uf", "lat", "lon", "ibge"),
    [
        ("", "RS", -29.6, -51.0, None),
        ("Cidade", "XX", -29.6, -51.0, None),
        ("Cidade", "RS", 48.85, 2.35, None),  # Paris: fora do Brasil
        ("Cidade", "RS", -29.6, -51.0, 123),  # código IBGE com dígitos insuficientes
    ],
)
def test_register_manual_invalid(session, name, uf, lat, lon, ibge):
    with pytest.raises(ValidationError):
        register_manual(session, name, uf, lat, lon, ibge)


def test_list_active_only(session):
    a = register_manual(session, "Cidade A", "RS", -29.6, -51.0)
    register_manual(session, "Cidade B", "RS", -29.7, -51.1)
    repo.set_municipality_active(session, a.id, False)
    session.expire_all()
    assert [m.name for m in repo.list_municipalities(session, active_only=True)] == ["Cidade B"]
