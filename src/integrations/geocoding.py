"""Pesquisa de municípios (geocodificação).

* Coordenadas: API de geocodificação da Open-Meteo, baseada no GeoNames
  (https://open-meteo.com/en/docs/geocoding-api).
* Código IBGE: API de Localidades do IBGE
  (https://servicodados.ibge.gov.br/api/docs/localidades), usado para
  relacionar o município aos avisos do INMET, que listam códigos IBGE.

As coordenadas ficam gravadas no cadastro, evitando consultas repetidas.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 6 · Documento 03 (Arquitetura) · Documento 12 (Interfaces).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from src.integrations.http_client import HttpClient, InvalidResponseError, SourceUnavailableError
from src.utils.brazil import STATES, state_code_from_name
from src.utils.validators import ValidationError, normalize_text, validate_coordinates, validate_search_term

logger = logging.getLogger(__name__)

# Códigos de feição do GeoNames que representam localidades povoadas.
POPULATED_PLACE_CODES = {"PPL", "PPLA", "PPLA2", "PPLA3", "PPLA4", "PPLC", "PPLL", "PPLF", "PPLS", "PPLX"}


@dataclass(frozen=True)
class MunicipalityCandidate:
    name: str
    state: str
    state_code: str
    country: str
    latitude: float
    longitude: float
    elevation: float | None
    timezone: str
    geonames_id: int | None
    population: int | None
    admin2: str | None

    @property
    def label(self) -> str:
        raise NotImplementedError("TODO: implementar MunicipalityCandidate.label")


def parse_geocoding(payload: Any) -> list[MunicipalityCandidate]:
    """Converte a resposta da geocodificação em candidatos brasileiros válidos."""
    raise NotImplementedError("TODO: implementar parse_geocoding")


def find_ibge_code(payload: Any, name: str) -> int | None:
    """Procura o código IBGE do município na lista de municípios da UF."""
    raise NotImplementedError("TODO: implementar find_ibge_code")


class GeocodingClient:
    def __init__(
        self,
        http: HttpClient,
        geocoding_url: str = "https://geocoding-api.open-meteo.com/v1/search",
        ibge_url: str = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios",
    ) -> None:
        raise NotImplementedError("TODO: implementar GeocodingClient.__init__")

    def search(self, term: str, limit: int = 10) -> list[MunicipalityCandidate]:
        raise NotImplementedError("TODO: implementar GeocodingClient.search")

    def lookup_ibge_code(self, name: str, state_code: str) -> int | None:
        """Busca o código IBGE; devolve None se a API do IBGE estiver indisponível."""
        raise NotImplementedError("TODO: implementar GeocodingClient.lookup_ibge_code")
