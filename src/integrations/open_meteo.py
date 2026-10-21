"""Integração com a API de previsão da Open-Meteo.

Documentação: https://open-meteo.com/en/docs
Endpoint: https://api.open-meteo.com/v1/forecast
Licença dos dados: CC BY 4.0 — a atribuição "Dados: Open-Meteo.com" é
exibida na interface.

O módulo apenas busca e converte os dados (``parse_forecast``). Ele não
grava nada no banco: isso é responsabilidade dos coletores.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 6 · Documento 03 (Arquitetura) · Documento 12 (Interfaces).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from src.integrations.http_client import HttpClient, InvalidResponseError
from src.utils.timeutils import local_to_utc
from src.utils.validators import validate_measurement

logger = logging.getLogger(__name__)

SOURCE_NAME = "Open-Meteo"
ATTRIBUTION = "Dados meteorológicos: Open-Meteo.com (CC BY 4.0)"

CURRENT_VARIABLES = [
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
]
HOURLY_VARIABLES = [
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "precipitation_probability",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
    "uv_index",
]
DAILY_VARIABLES = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "precipitation_probability_max",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "uv_index_max",
]

# Nome na API -> (nome no banco, variável usada na validação)
CURRENT_MAP = {
    "temperature_2m": ("temperature", "temperature"),
    "apparent_temperature": ("apparent_temperature", "apparent_temperature"),
    "relative_humidity_2m": ("humidity", "humidity"),
    "precipitation": ("precipitation", "precipitation"),
    "weather_code": ("weather_code", "weather_code"),
    "surface_pressure": ("pressure", "pressure"),
    "wind_speed_10m": ("wind_speed", "wind_speed"),
    "wind_direction_10m": ("wind_direction", "wind_direction"),
    "wind_gusts_10m": ("wind_gusts", "wind_gusts"),
}
HOURLY_MAP = {
    **CURRENT_MAP,
    "precipitation_probability": ("precipitation_probability", "precipitation_probability"),
    "uv_index": ("uv_index", "uv_index"),
}
DAILY_MAP = {
    "weather_code": ("weather_code", "weather_code"),
    "temperature_2m_max": ("temperature_max", "temperature_max"),
    "temperature_2m_min": ("temperature_min", "temperature_min"),
    "precipitation_sum": ("precipitation_sum", "precipitation_sum"),
    "precipitation_probability_max": ("precipitation_probability", "precipitation_probability"),
    "wind_speed_10m_max": ("wind_speed", "wind_speed"),
    "wind_gusts_10m_max": ("wind_gusts", "wind_gusts"),
    "wind_direction_10m_dominant": ("wind_direction", "wind_direction"),
    "uv_index_max": ("uv_index_max", "uv_index"),
}


@dataclass
class ForecastBundle:
    """Resultado convertido de uma consulta à Open-Meteo."""

    timezone: str
    current: dict[str, Any] | None
    hourly: list[dict[str, Any]] = field(default_factory=list)
    daily: list[dict[str, Any]] = field(default_factory=list)
    source: str = SOURCE_NAME


def build_params(
    latitude: float, longitude: float, forecast_days: int = 7, timezone: str = "America/Sao_Paulo"
) -> dict:
    raise NotImplementedError("TODO: implementar build_params")


def _convert(raw: dict[str, Any], mapping: dict[str, tuple[str, str]]) -> dict[str, Any]:
    raise NotImplementedError("TODO: implementar _convert")


def _series_rows(block: dict[str, Any], variables: list[str]) -> list[dict[str, Any]]:
    """Transforma {"time": [...], "x": [...]} em uma lista de dicionários."""
    raise NotImplementedError("TODO: implementar _series_rows")


def parse_forecast(payload: Any) -> ForecastBundle:
    """Valida e converte o JSON da Open-Meteo para o formato do projeto."""
    raise NotImplementedError("TODO: implementar parse_forecast")


def current_hour_probability(bundle: ForecastBundle) -> float | None:
    """A probabilidade de chuva não existe no bloco 'current'; usamos a da hora corrente."""
    raise NotImplementedError("TODO: implementar current_hour_probability")


class OpenMeteoClient:
    def __init__(self, http: HttpClient, base_url: str = "https://api.open-meteo.com/v1/forecast") -> None:
        raise NotImplementedError("TODO: implementar OpenMeteoClient.__init__")

    def fetch_forecast(
        self, latitude: float, longitude: float, forecast_days: int = 7, timezone: str = "America/Sao_Paulo"
    ) -> ForecastBundle:
        raise NotImplementedError("TODO: implementar OpenMeteoClient.fetch_forecast")
