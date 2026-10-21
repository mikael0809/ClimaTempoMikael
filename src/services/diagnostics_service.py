"""Diagnóstico: situação das fontes e do banco (sem expor segredos)."""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 7 e 9 · Documento 02 (Regras de negócio) · Documento 06 (Fluxogramas 7 a 9).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from src.config import Settings
from src.database import repositories as repo
from src.integrations import inmet, open_meteo
from src.services.weather_service import Freshness, assess_freshness

SOURCES = {
    open_meteo.SOURCE_NAME: "Previsões e condições atuais (API REST/JSON)",
    inmet.SOURCE_NAME: "Avisos meteorológicos oficiais (JSON público do portal de avisos)",
}


@dataclass
class SourceStatus:
    source: str
    purpose: str
    last_success: datetime | None
    last_attempt: datetime | None
    last_attempt_status: str | None
    last_error: str | None
    last_error_at: datetime | None
    freshness: Freshness

    @property
    def availability(self) -> str:
        raise NotImplementedError("TODO: implementar SourceStatus.availability")


def source_statuses(session: Session, settings: Settings) -> list[SourceStatus]:
    raise NotImplementedError("TODO: implementar source_statuses")
