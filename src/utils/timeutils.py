"""Funções de data e hora.

Convenção do projeto:
* No banco de dados, todos os instantes são gravados em UTC, sem fuso
  (``datetime`` "ingênuo"), porque o SQLite não armazena fuso horário.
* Na interface, os instantes são convertidos para ``America/Sao_Paulo``.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 2 · Documento 10 (Validação de entradas) · Documento 12.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

DISPLAY_TZ = ZoneInfo("America/Sao_Paulo")


def utc_now() -> datetime:
    """Instante atual em UTC, sem tzinfo (formato usado no banco)."""
    raise NotImplementedError("TODO: implementar utc_now")


def local_to_utc(value: str | datetime, tz_name: str) -> datetime:
    """Converte um horário local (ex.: '2026-10-21T14:00') para UTC ingênuo."""
    raise NotImplementedError("TODO: implementar local_to_utc")


def to_display(dt: datetime | None, tz: ZoneInfo = DISPLAY_TZ) -> datetime | None:
    """Converte um UTC ingênuo do banco para o fuso de exibição."""
    raise NotImplementedError("TODO: implementar to_display")


def format_datetime(dt: datetime | None, with_seconds: bool = False) -> str:
    """Formata um UTC ingênuo como 'dd/mm/aaaa hh:mm' no horário de Brasília."""
    raise NotImplementedError("TODO: implementar format_datetime")


def format_date(d: date | None) -> str:
    raise NotImplementedError("TODO: implementar format_date")


WEEKDAYS_PT = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def weekday_label(d: date) -> str:
    raise NotImplementedError("TODO: implementar weekday_label")


def minutes_since(dt: datetime | None, now: datetime | None = None) -> float | None:
    """Minutos decorridos desde ``dt`` (UTC ingênuo)."""
    raise NotImplementedError("TODO: implementar minutes_since")
