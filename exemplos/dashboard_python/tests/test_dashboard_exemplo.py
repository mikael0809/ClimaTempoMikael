"""Testes da dashboard de exemplo (sem internet)."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))

from analise import (  # noqa: E402
    chuva_diaria,
    filtrar,
    garantir_fonte_unica,
    indicador_atencao_chuva,
    resumo_por_municipio,
)
from dados_simulados import MUNICIPIOS, TIPO_SIMULADO, carregar_dados_simulados, gerar_dados_simulados  # noqa: E402


@pytest.fixture(scope="module")
def dados() -> pd.DataFrame:
    return gerar_dados_simulados(dias=3)


def test_dados_simulados_sao_reprodutiveis():
    a = gerar_dados_simulados(dias=2, semente=7)
    b = gerar_dados_simulados(dias=2, semente=7)
    pd.testing.assert_frame_equal(a, b)


def test_dados_simulados_identificados(dados):
    assert set(dados["tipo_dado"]) == {TIPO_SIMULADO}
    assert len(dados) == 3 * 24 * len(MUNICIPIOS)
    assert dados["umidade_pct"].between(0, 100).all()
    assert (dados["precipitacao_mm"] >= 0).all()


def test_csv_versionado_carrega_somente_simulados():
    df = carregar_dados_simulados()
    assert garantir_fonte_unica(df) == TIPO_SIMULADO
    assert pd.api.types.is_datetime64_any_dtype(df["data_hora"])


def test_filtro_por_municipio_e_periodo(dados):
    resultado = filtrar(dados, ["Sapiranga - RS"], date(2026, 10, 2), date(2026, 10, 2))
    assert set(resultado["municipio"]) == {"Sapiranga - RS"}
    assert len(resultado) == 24
    assert set(resultado["data_hora"].dt.date) == {date(2026, 10, 2)}


def test_resumo_por_municipio(dados):
    resumo = resumo_por_municipio(dados)
    assert len(resumo) == len(MUNICIPIOS)
    assert (resumo["temperatura_max"] >= resumo["temperatura_min"]).all()


def test_indicador_atencao_respeita_limite(dados):
    diaria = chuva_diaria(dados)
    limite = float(diaria["precipitacao_mm"].max())
    atencao = indicador_atencao_chuva(dados, limite)
    assert len(atencao) >= 1
    assert (atencao["precipitacao_mm"] >= limite).all()
    assert set(atencao["classificacao"]) == {"INDICADOR CALCULADO (não oficial)"}
    assert indicador_atencao_chuva(dados, limite + 1000).empty


def test_mistura_de_fontes_e_bloqueada(dados):
    real = dados.head(2).assign(tipo_dado="REAL")
    with pytest.raises(ValueError, match="Mistura"):
        garantir_fonte_unica(pd.concat([dados, real]))


def test_app_exemplo_executa_com_dados_simulados():
    """Executa o app.py de verdade com o mecanismo de testes do Streamlit."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(PASTA / "app.py"), default_timeout=60).run()
    assert not at.exception
    assert any("DADOS SIMULADOS" in w.value for w in at.warning)
    assert len(at.metric) >= 4
    assert at.title[0].value.startswith("📊")
