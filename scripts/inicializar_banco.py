"""Cria o banco SQLite, aplica migrações e cadastra Sapiranga - RS.

Uso (na raiz do projeto, com o ambiente virtual ativo):
    python scripts/inicializar_banco.py
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 11 e 12 · Documento 09 (Implantação e operação).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

import _bootstrap  # noqa: F401

from src.config import get_settings
from src.database import repositories as repo
from src.database.connection import init_db, run_migrations, session_scope
from src.services.municipality_service import ensure_default_municipality
from src.utils.logging_config import setup_logging


def main() -> None:
    raise NotImplementedError("TODO: implementar main")


if __name__ == "__main__":
    main()
