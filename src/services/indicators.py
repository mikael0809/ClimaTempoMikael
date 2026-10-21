"""Indicadores locais de atenção (regras configuráveis).

ATENÇÃO — conceito central do projeto:
* Um INDICADOR LOCAL é um cálculo feito pelo ClimaAlerta comparando a
  previsão numérica com limites configurados no arquivo ``.env``.
* Ele NÃO é um alerta oficial, não prevê desastres e não garante segurança.
  Alertas oficiais vêm de autoridades (ex.: INMET, Defesa Civil).

Os indicadores são calculados sob demanda a partir das previsões
armazenadas e nunca são gravados na tabela ``weather_alert``.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 7 e 9 · Documento 02 (Regras de negócio) · Documento 06 (Fluxogramas 7 a 9).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import operator
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from src.config import IndicatorThresholds

CLASSIFICATION = "INDICADOR CALCULADO (não oficial)"
DISCLAIMER = (
    "Indicadores calculados pelo ClimaAlerta a partir da previsão numérica e de limites "
    "demonstrativos configuráveis. Não são alertas oficiais nem recomendações de segurança. "
    "Consulte sempre o INMET e a Defesa Civil."
)

# Operadores permitidos — usamos o módulo operator em vez de eval() por segurança.
OPERATORS: dict[str, Callable[[float, float], bool]] = {">=": operator.ge, "<=": operator.le}


@dataclass(frozen=True)
class IndicatorRule:
    rule_id: str
    name: str
    variable: str  # nome da coluna na previsão
    operator: str  # '>=' ou '<='
    threshold: float
    unit: str
    scope: str  # 'HORARIA' (próximas 24 h) ou 'DIARIA' (próximos dias)

    @property
    def description(self) -> str:
        raise NotImplementedError("TODO: implementar IndicatorRule.description")


@dataclass(frozen=True)
class LocalIndicator:
    rule_id: str
    condition: str
    value: float
    threshold: float
    operator: str
    unit: str
    reference_time: datetime | date
    scope: str
    occurrences: int
    rule_description: str
    source: str
    municipality_id: int | None = None
    municipality_label: str | None = None
    classification: str = CLASSIFICATION


def build_rules(t: IndicatorThresholds) -> list[IndicatorRule]:
    """Cria as regras a partir dos limites configurados."""
    raise NotImplementedError("TODO: implementar build_rules")


def _matches(rule: IndicatorRule, value: Any) -> bool:
    raise NotImplementedError("TODO: implementar _matches")


def _get(row: Any, name: str) -> Any:
    raise NotImplementedError("TODO: implementar _get")


def evaluate_hourly(rule: IndicatorRule, rows: Iterable[Any]) -> LocalIndicator | None:
    """Regras horárias: um indicador por regra, com o valor mais extremo encontrado."""
    raise NotImplementedError("TODO: implementar evaluate_hourly")


def evaluate_daily(rule: IndicatorRule, rows: Iterable[Any]) -> list[LocalIndicator]:
    """Regras diárias: um indicador para cada dia em que a condição ocorre."""
    raise NotImplementedError("TODO: implementar evaluate_daily")


def evaluate_indicators(
    rules: Iterable[IndicatorRule],
    hourly_rows: Iterable[Any],
    daily_rows: Iterable[Any],
    municipality_id: int | None = None,
    municipality_label: str | None = None,
) -> list[LocalIndicator]:
    raise NotImplementedError("TODO: implementar evaluate_indicators")
