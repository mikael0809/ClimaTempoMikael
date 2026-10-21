"""Configurações: valores padrão, limites e proteção de informações sensíveis."""

from __future__ import annotations

from pathlib import Path

from src.config import PROJECT_ROOT, get_settings


def test_defaults(monkeypatch):
    for var in ("CLIMAALERTA_DB_PATH", "INTERVALO_ATUALIZACAO_MINUTOS", "HTTP_MAX_RETENTATIVAS"):
        monkeypatch.delenv(var, raising=False)
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.database_path == PROJECT_ROOT / "data" / "climaalerta.db"
        assert s.timezone == "America/Sao_Paulo"
        assert s.http_timeout_seconds > 0
        assert s.database_url.startswith("sqlite:///")
    finally:
        get_settings.cache_clear()


def test_limits_are_enforced(monkeypatch):
    monkeypatch.setenv("INTERVALO_ATUALIZACAO_MINUTOS", "1")  # abaixo do mínimo de cortesia
    monkeypatch.setenv("HTTP_MAX_RETENTATIVAS", "50")
    monkeypatch.setenv("DIAS_PREVISAO", "99")
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.update_interval_minutes == 15
        assert s.http_max_retries == 5
        assert s.forecast_days == 16
    finally:
        get_settings.cache_clear()


def test_public_dict_has_no_secret_like_keys():
    keys = " ".join(get_settings().as_public_dict()).lower()
    for forbidden in ("senha", "password", "token", "secret", "chave", "key"):
        assert forbidden not in keys


def test_env_example_documents_every_variable():
    example = (PROJECT_ROOT / ".env.example").read_text(encoding="utf-8")
    source = (PROJECT_ROOT / "src" / "config.py").read_text(encoding="utf-8")
    import re

    used = set(re.findall(r'_env_\w+\(\s*"([A-Z_]+)"', source))
    documented = set(re.findall(r"^([A-Z_]+)=", example, re.MULTILINE))
    assert used == documented


def test_no_eval_or_exec_in_source():
    """Analisa o código (AST) e garante que nenhuma chamada a eval/exec existe."""
    import ast

    for path in Path(PROJECT_ROOT / "src").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        assert not calls & {"eval", "exec"}, path
