"""Exportação para CSV (RN011).

Padrão adotado para abrir corretamente no Excel/LibreOffice em português:
separador ``;``, vírgula decimal, codificação UTF-8 com BOM, datas no
horário de Brasília. Toda exportação inclui as colunas de fonte e de tipo
de registro, para que dados oficiais, calculados e de demonstração nunca se
confundam.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 7 e 9 · Documento 02 (Regras de negócio) · Documento 06 (Fluxogramas 7 a 9).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.database.models import WeatherAlert
from src.services.alert_service import validity_status
from src.services.indicators import LocalIndicator
from src.utils.timeutils import format_datetime

CSV_OPTIONS = {"sep": ";", "decimal": ",", "index": False, "encoding": "utf-8-sig", "date_format": "%d/%m/%Y %H:%M"}

COLUMN_LABELS = {
    "municipality": "municipio",
    "municipality_id": "municipio_id",
    "observed_at": "horario_referencia",
    "forecast_time": "horario_previsto",
    "forecast_date": "data_prevista",
    "temperature": "temperatura_c",
    "apparent_temperature": "sensacao_termica_c",
    "temperature_min": "temperatura_minima_c",
    "temperature_max": "temperatura_maxima_c",
    "humidity": "umidade_pct",
    "pressure": "pressao_hpa",
    "precipitation": "precipitacao_mm",
    "precipitation_sum": "precipitacao_acumulada_mm",
    "precipitation_probability": "probabilidade_chuva_pct",
    "wind_speed": "vento_kmh",
    "wind_direction": "direcao_vento_graus",
    "wind_gusts": "rajada_kmh",
    "uv_index": "indice_uv",
    "uv_index_max": "indice_uv_max",
    "weather_code": "codigo_wmo",
    "source": "fonte",
    "collected_at": "coletado_em",
}


def prepare_weather_export(df: pd.DataFrame, record_type: str) -> pd.DataFrame:
    """Renomeia colunas para português e acrescenta o tipo de registro."""
    raise NotImplementedError("TODO: implementar prepare_weather_export")


def alerts_export_frame(alerts: list[WeatherAlert]) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar alerts_export_frame")


def indicators_export_frame(indicators: list[LocalIndicator]) -> pd.DataFrame:
    raise NotImplementedError("TODO: implementar indicators_export_frame")


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Conteúdo CSV em bytes (usado no botão de download da interface)."""
    raise NotImplementedError("TODO: implementar to_csv_bytes")


def write_csv(df: pd.DataFrame, path: Path) -> Path:
    raise NotImplementedError("TODO: implementar write_csv")
