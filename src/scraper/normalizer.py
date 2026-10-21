"""Normalização dos textos extraídos das páginas.

Páginas web exibem números como texto formatado para pessoas
("24,5 °C", "Umidade: 57 %"). Estas funções convertem esses textos em
números, sempre devolvendo ``None`` quando o valor está ausente ou é
inválido — nunca um valor inventado.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 4 e 5 · Documento 06 (Fluxograma 4).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import re

from src.utils.validators import validate_measurement

MISSING_MARKERS = {"", "-", "—", "–", "n/d", "nd", "indisponível", "indisponivel", "sem dados"}
_NUMBER_RE = re.compile(r"-?\d+(?:[.,]\d+)?")
_DIRECTION_RE = re.compile(r"\(([NSLOEW]{1,3})\)", re.IGNORECASE)


def clean_text(text: str | None) -> str:
    """Remove espaços repetidos e quebras de linha."""
    raise NotImplementedError("TODO: implementar clean_text")


def is_missing(text: str | None) -> bool:
    raise NotImplementedError("TODO: implementar is_missing")


def parse_decimal_br(text: str | None) -> float | None:
    """'24,5 °C' -> 24.5 ; '1.013,2 hPa' -> 1013.2 ; '—' -> None."""
    raise NotImplementedError("TODO: implementar parse_decimal_br")


def parse_temperature(text: str | None) -> float | None:
    raise NotImplementedError("TODO: implementar parse_temperature")


def parse_humidity(text: str | None) -> float | None:
    raise NotImplementedError("TODO: implementar parse_humidity")


def parse_precipitation(text: str | None) -> float | None:
    raise NotImplementedError("TODO: implementar parse_precipitation")


def parse_wind(text: str | None) -> tuple[float | None, str | None]:
    """'Vento: 13,5 km/h (SE)' -> (13.5, 'SE')."""
    raise NotImplementedError("TODO: implementar parse_wind")


def parse_date_br(text: str | None) -> str | None:
    """'21/10/2026' -> '2026-10-21' (ISO); devolve None se inválido."""
    raise NotImplementedError("TODO: implementar parse_date_br")
