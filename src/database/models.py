"""Modelos de dados (ORM SQLAlchemy 2.x).

Cada classe corresponde a uma tabela do banco SQLite. Convenções:
* instantes (``*_at``, ``*_time``) em UTC sem fuso;
* campos meteorológicos opcionais aceitam ``NULL`` quando a fonte não
  fornece o valor — nunca inventamos dados ausentes;
* restrições de unicidade evitam registros duplicados (ver RN005).
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 8 · Documento 04 (Dicionário de dados e modelo ER) · Documento 12.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.utils.timeutils import utc_now

# Valores permitidos (também usados na documentação gerada).
COLLECTION_STATUSES = ("SUCESSO", "FALHA", "PARCIAL")
COLLECTION_TYPES = ("PREVISAO", "ALERTAS", "SCRAPER_DEMO")
ALERT_TYPES = ("OFICIAL",)
ALERT_STATUSES = ("ATIVO", "ALTERADO", "ENCERRADO")


class Base(DeclarativeBase):
    pass


class Municipality(Base):
    """Município monitorado (cadastro local)."""

    __tablename__ = "municipality"
    __abstract__ = True  # TODO: remova esta linha depois de declarar as colunas
    # TODO: declare as colunas, chaves, restrições e relacionamentos desta tabela
    # (veja o Documento 04 — Dicionário de dados — e o modelo entidade-relacionamento).


class WeatherObservation(Base):
    """Condição atual coletada (o "agora" da Open-Meteo, estimado por modelo)."""

    __tablename__ = "weather_observation"
    __abstract__ = True  # TODO: remova esta linha depois de declarar as colunas
    # TODO: declare as colunas, chaves, restrições e relacionamentos desta tabela
    # (veja o Documento 04 — Dicionário de dados — e o modelo entidade-relacionamento).


class WeatherForecast(Base):
    """Previsão diária (um registro por município, dia e fonte)."""

    __tablename__ = "weather_forecast"
    __abstract__ = True  # TODO: remova esta linha depois de declarar as colunas
    # TODO: declare as colunas, chaves, restrições e relacionamentos desta tabela
    # (veja o Documento 04 — Dicionário de dados — e o modelo entidade-relacionamento).


class HourlyForecast(Base):
    """Previsão horária (próximas horas)."""

    __tablename__ = "hourly_forecast"
    __abstract__ = True  # TODO: remova esta linha depois de declarar as colunas
    # TODO: declare as colunas, chaves, restrições e relacionamentos desta tabela
    # (veja o Documento 04 — Dicionário de dados — e o modelo entidade-relacionamento).


class WeatherAlert(Base):
    """Alerta OFICIAL publicado por uma autoridade (ex.: INMET).

    Indicadores calculados pelo sistema NUNCA são gravados nesta tabela
    (a restrição ``ck_alert_type`` aceita apenas 'OFICIAL').
    """

    __tablename__ = "weather_alert"
    __abstract__ = True  # TODO: remova esta linha depois de declarar as colunas
    # TODO: declare as colunas, chaves, restrições e relacionamentos desta tabela
    # (veja o Documento 04 — Dicionário de dados — e o modelo entidade-relacionamento).


class CollectionLog(Base):
    """Registro de cada execução de coleta (sucesso ou falha)."""

    __tablename__ = "collection_log"
    __abstract__ = True  # TODO: remova esta linha depois de declarar as colunas
    # TODO: declare as colunas, chaves, restrições e relacionamentos desta tabela
    # (veja o Documento 04 — Dicionário de dados — e o modelo entidade-relacionamento).
