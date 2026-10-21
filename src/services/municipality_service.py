"""Regras de cadastro de municípios (RN001, RN002, RN005)."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 7 e 9 · Documento 02 (Regras de negócio) · Documento 06 (Fluxogramas 7 a 9).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from src.database import repositories as repo
from src.database.models import Municipality
from src.integrations.geocoding import GeocodingClient, MunicipalityCandidate
from src.utils.brazil import STATES
from src.utils.validators import ValidationError, validate_coordinates

logger = logging.getLogger(__name__)

# Município inicial de demonstração. Coordenadas obtidas em 21/10/2026 na
# geocodificação da Open-Meteo (GeoNames id 3448063); código IBGE obtido na
# API de Localidades do IBGE. Ficam gravados para o sistema funcionar mesmo
# sem acesso à internet no primeiro uso.
SAPIRANGA = {
    "name": "Sapiranga",
    "state": "Rio Grande do Sul",
    "state_code": "RS",
    "country": "Brasil",
    "latitude": -29.63806,
    "longitude": -51.00694,
    "elevation": 36.0,
    "timezone": "America/Sao_Paulo",
    "ibge_code": 4319901,
    "geonames_id": 3448063,
    "coordinates_source": "Open-Meteo Geocoding (GeoNames 3448063), consultado em 21/10/2026",
}


def ensure_default_municipality(session: Session) -> Municipality:
    """Garante que Sapiranga - RS esteja cadastrado (idempotente)."""
    raise NotImplementedError("TODO: implementar ensure_default_municipality")


def register_candidate(
    session: Session, candidate: MunicipalityCandidate, geocoding: GeocodingClient | None = None
) -> Municipality:
    """Cadastra um município escolhido na pesquisa (com validação e anti-duplicação)."""
    raise NotImplementedError("TODO: implementar register_candidate")


def register_manual(
    session: Session, name: str, state_code: str, latitude: object, longitude: object, ibge_code: int | None = None
) -> Municipality:
    """Cadastro manual (quando a geocodificação estiver indisponível)."""
    raise NotImplementedError("TODO: implementar register_manual")
