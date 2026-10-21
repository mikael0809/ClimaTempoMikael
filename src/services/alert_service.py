"""Central de alertas: filtros, validade e expiração (RN006, RN009).

Os alertas oficiais (tabela ``weather_alert``) e os indicadores locais
(calculados) são mantidos em listas separadas e exibidos em seções
visualmente distintas.
"""

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

from src.database import repositories as repo
from src.database.models import Municipality, WeatherAlert
from src.integrations.inmet import SEVERITY_ORDER, alert_applies_to
from src.utils.timeutils import utc_now

VALIDITY_CURRENT = "Vigente"
VALIDITY_FUTURE = "Previsto"
VALIDITY_EXPIRED = "Expirado"
VALIDITY_CLOSED = "Encerrado pela fonte"
VALIDITY_UNKNOWN = "Validade não informada"


def is_expired(alert: WeatherAlert, now: datetime | None = None) -> bool:
    """Um alerta está expirado quando o fim da validade já passou."""
    raise NotImplementedError("TODO: implementar is_expired")


def validity_status(alert: WeatherAlert, now: datetime | None = None) -> str:
    raise NotImplementedError("TODO: implementar validity_status")


def severity_rank(severity: str) -> int:
    raise NotImplementedError("TODO: implementar severity_rank")


@dataclass
class AlertFilters:
    municipalities: list[Municipality] | None = None
    sources: list[str] | None = None
    events: list[str] | None = None
    severities: list[str] | None = None
    validities: list[str] | None = None  # Vigente, Previsto, Expirado...
    start: datetime | None = None  # período de validade (UTC)
    end: datetime | None = None


def filter_alerts(alerts: list[WeatherAlert], filters: AlertFilters, now: datetime | None = None) -> list[WeatherAlert]:
    raise NotImplementedError("TODO: implementar filter_alerts")


def official_alerts_for(
    session: Session, municipality: Municipality, include_expired: bool = False
) -> list[WeatherAlert]:
    raise NotImplementedError("TODO: implementar official_alerts_for")


def alert_options(alerts: list[WeatherAlert]) -> dict[str, list[str]]:
    """Valores existentes para preencher os filtros da interface."""
    raise NotImplementedError("TODO: implementar alert_options")
