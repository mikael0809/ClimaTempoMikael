"""Integração com os avisos oficiais do INMET (amostra real de 21/10/2026)."""

from __future__ import annotations

import copy
import xml.etree.ElementTree as ET
from datetime import datetime

import pytest

from src.integrations.http_client import InvalidResponseError
from src.integrations.inmet import InmetAlertsClient, alert_applies_to, parse_active_alerts, parse_alert
from src.utils.timeutils import local_to_utc
from tests.conftest import FIXTURES, FakeHttp


def test_parse_real_sample(inmet_payload):
    alerts = parse_active_alerts(inmet_payload)
    assert len(alerts) == 4
    first = next(a for a in alerts if a["external_id"] == "56124")
    assert first["source"] == "INMET"
    assert first["alert_type"] == "OFICIAL"
    assert first["event"] == "Chuvas Intensas"
    assert first["severity"] == "Perigo Potencial"  # preservada como publicada
    assert first["headline"] == "Aviso de Chuvas Intensas. Severidade Grau: Perigo Potencial"
    assert first["official_url"] == "https://avisos.inmet.gov.br/56124"
    assert first["status"] == "ATIVO"
    # 'inicio' 2026-10-21 00:01 (Brasília) = 03:01 UTC
    assert first["effective_at"] == datetime(2026, 10, 21, 3, 1)
    assert first["expires_at"] == datetime(2026, 10, 22, 2, 59)
    assert "Acre" in first["affected_area"]
    assert "1200013" in first["affected_geocodes"]
    assert first["description"].startswith("Chuva entre 20 e 30 mm/h")


def test_parsed_validity_matches_official_cap_document(inmet_payload):
    """Confere a conversão de horário com o documento CAP 1.2 oficial do mesmo aviso."""
    ns = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}
    root = ET.parse(FIXTURES / "inmet_cap_56124.xml").getroot()
    info = root.find("cap:info", ns)
    onset = info.find("cap:onset", ns).text
    expires = info.find("cap:expires", ns).text
    web = info.find("cap:web", ns).text
    alert = parse_alert(next(a for a in inmet_payload["hoje"] if a["id"] == 56124))
    assert alert["effective_at"] == local_to_utc(datetime.fromisoformat(onset), "UTC")
    assert alert["expires_at"] == local_to_utc(datetime.fromisoformat(expires), "UTC")
    assert alert["official_url"] == web
    assert alert["cap_identifier"] == root.find("cap:identifier", ns).text


def test_status_mapping(inmet_payload):
    item = copy.deepcopy(inmet_payload["hoje"][0])
    item["alterado"] = True
    assert parse_alert(item)["status"] == "ALTERADO"
    item["encerrado"] = True
    assert parse_alert(item)["status"] == "ENCERRADO"


def test_alert_without_required_fields_is_ignored(inmet_payload):
    payload = copy.deepcopy(inmet_payload)
    del payload["hoje"][0]["severidade"]
    alerts = parse_active_alerts(payload)
    assert len(alerts) == 3
    with pytest.raises(InvalidResponseError):
        parse_alert(payload["hoje"][0])


def test_duplicate_ids_are_merged(inmet_payload):
    payload = copy.deepcopy(inmet_payload)
    payload["futuro"].append(copy.deepcopy(payload["hoje"][0]))
    assert len(parse_active_alerts(payload)) == 4


@pytest.mark.parametrize("payload", [None, [], {"outra": []}, {"hoje": "texto"}])
def test_invalid_payload(payload):
    with pytest.raises(InvalidResponseError):
        parse_active_alerts(payload)


def test_alert_applies_by_ibge_code_or_state(inmet_payload):
    alert = parse_alert(inmet_payload["hoje"][0])
    assert alert_applies_to(alert, 1200013, None)  # Acrelândia - AC
    assert not alert_applies_to(alert, 4319901, "Rio Grande do Sul")  # Sapiranga não está no aviso
    assert alert_applies_to(alert, None, "Acre")  # sem código IBGE, usa a UF
    assert not alert_applies_to(alert, None, None)


def test_client_fetch(inmet_payload):
    http = FakeHttp({"apiprevmet3": inmet_payload})
    alerts = InmetAlertsClient(http).fetch_active_alerts()
    assert {a["external_id"] for a in alerts} == {"56124", "56127", "56134", "56138"}
