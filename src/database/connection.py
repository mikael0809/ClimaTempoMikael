"""Conexão com o SQLite, inicialização e migrações de esquema.

Migrações: a versão do esquema é guardada em ``PRAGMA user_version``.
Para alterar o banco no futuro, acrescente uma função à lista
``MIGRATIONS``; ela será aplicada uma única vez em bancos antigos.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 8 · Documento 04 (Dicionário de dados e modelo ER) · Documento 12.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, sessionmaker

from src.database.models import Base

logger = logging.getLogger(__name__)


def _migration_001_initial(conn: Connection) -> None:
    """Versão 1: esquema inicial (criado por ``create_all``)."""


MIGRATIONS: list[Callable[[Connection], None]] = [_migration_001_initial]
SCHEMA_VERSION = len(MIGRATIONS)

_engines: dict[str, Engine] = {}


def _enable_sqlite_foreign_keys(dbapi_connection, _record) -> None:
    # O SQLite só respeita chaves estrangeiras com este PRAGMA ativo.
    raise NotImplementedError("TODO: implementar _enable_sqlite_foreign_keys")


def get_engine(database_url: str) -> Engine:
    """Cria (uma vez) e devolve o engine para a URL informada."""
    raise NotImplementedError("TODO: implementar get_engine")


def run_migrations(engine: Engine) -> int:
    """Aplica migrações pendentes e devolve a versão final do esquema."""
    raise NotImplementedError("TODO: implementar run_migrations")


def init_db(database_url: str) -> Engine:
    """Cria as tabelas que não existem e aplica as migrações (idempotente)."""
    raise NotImplementedError("TODO: implementar init_db")


_factories: dict[str, sessionmaker[Session]] = {}


def get_session_factory(database_url: str) -> sessionmaker[Session]:
    """Inicializa o banco na primeira chamada e reaproveita a fábrica de sessões."""
    raise NotImplementedError("TODO: implementar get_session_factory")


@contextmanager
def session_scope(database_url: str) -> Iterator[Session]:
    """Abre uma sessão, faz commit ao final ou rollback em caso de erro."""
    raise NotImplementedError("TODO: implementar session_scope")


def dispose_engines() -> None:
    """Fecha todas as conexões (usado nos testes)."""
    raise NotImplementedError("TODO: implementar dispose_engines")
