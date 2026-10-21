"""Montagem dos objetos usados pela aplicação (injeção de dependências simples).

Centralizar a criação dos clientes permite substituí-los por *mocks* nos
testes, sem acessar a internet.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 7 e 9 · Documento 02 (Regras de negócio) · Documento 06 (Fluxogramas 7 a 9).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass

from src.config import Settings, get_settings
from src.integrations.geocoding import GeocodingClient
from src.integrations.http_client import HttpClient
from src.integrations.inmet import InmetAlertsClient
from src.integrations.open_meteo import OpenMeteoClient


@dataclass
class AppServices:
    settings: Settings
    http: HttpClient
    open_meteo: OpenMeteoClient
    geocoding: GeocodingClient
    inmet: InmetAlertsClient

    @property
    def database_url(self) -> str:
        raise NotImplementedError("TODO: implementar AppServices.database_url")


def build_services(settings: Settings | None = None, http: HttpClient | None = None) -> AppServices:
    raise NotImplementedError("TODO: implementar build_services")
