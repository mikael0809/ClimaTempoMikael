"""Garante que o código do manual pedagógico (exemplos/tutorial) funciona como descrito."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from src.config import PROJECT_ROOT

TUTORIAL = PROJECT_ROOT / "exemplos" / "tutorial"
sys.path.insert(0, str(TUTORIAL))


def run_script(name: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TUTORIAL / name), *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )


def test_m01_verifica_ambiente():
    result = run_script("m01_verificar_ambiente.py")
    assert result.returncode == 0
    assert "streamlit" in result.stdout and "Python" in result.stdout


def test_m02_fundamentos():
    import m02_fundamentos as m

    assert m.celsius_para_fahrenheit(100) == 212
    assert m.classificar(30) == "quente" and m.classificar(20) == "agradável" and m.classificar(5) == "frio"
    result = run_script("m02_fundamentos.py")
    assert result.returncode == 0 and "Média" in result.stdout


def test_m03_dashboard():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(TUTORIAL / "m03_primeira_dashboard.py"), default_timeout=60).run()
    assert not at.exception
    assert len(at.metric) == 3


@pytest.mark.selenium
def test_m05_selenium():
    import m05_selenium_basico as m
    from selenium.common.exceptions import WebDriverException

    try:
        dados = m.raspar()
    except WebDriverException as exc:
        pytest.skip(f"Chrome indisponível: {exc}")
    assert [d["cidade"] for d in dados] == ["Sapiranga", "Porto Alegre", "Florianópolis"]
    assert dados[0]["temperatura"] == 24.5 and dados[0]["link"].startswith("https://")
    assert dados[1]["link"] is None and dados[2]["uf"] == "SC"


class _FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class _FakeHttp:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params, timeout))
        return _FakeResponse(self.payload)


def test_m06_api_com_resposta_real_gravada(forecast_payload):
    import m06_api_open_meteo as m

    http = _FakeHttp(forecast_payload)
    dados = m.buscar_condicoes(-29.63806, -51.00694, http=http)
    assert dados["temperatura"] == forecast_payload["current"]["temperature_2m"]
    assert http.calls[0][2] == 15  # timeout informado


def test_m07_pandas(tmp_path):
    import m07_pandas as m

    df = m.carregar_horario()
    assert len(df) == 168
    resumo = m.resumo_por_dia(df)
    assert len(resumo) == 7
    assert (resumo["maxima"] >= resumo["minima"]).all()


def test_m08_banco(tmp_path):
    import m08_banco as m

    engine = m.preparar(tmp_path / "t.db")
    m.popular(engine)
    m.popular(engine)  # idempotente
    linhas = m.consultar(engine)
    assert len(linhas) == 3  # 24.4, 24.5 e 20.2 °C
    assert m.tentar_duplicar(engine) == "recusado pela restrição UNIQUE"
    engine.dispose()


def test_m10_interface_le_o_banco(tmp_path, monkeypatch):
    import m08_banco as m
    from streamlit.testing.v1 import AppTest

    banco = tmp_path / "t.db"
    monkeypatch.setattr(m, "BANCO", banco)
    engine = m.preparar(banco)
    m.popular(engine)
    engine.dispose()
    script = (
        f"import sys; sys.path.insert(0, r'{TUTORIAL}')\nimport m08_banco\nfrom pathlib import Path\n"
        f"m08_banco.BANCO = Path(r'{banco}')\n"
        f"m08_banco.preparar.__defaults__ = (m08_banco.BANCO,)\n"
        f"exec(open(r'{TUTORIAL / 'm10_interface.py'}', encoding='utf-8').read())\n"
    )
    at = AppTest.from_string(script, default_timeout=60).run()
    assert not at.exception
    assert at.metric[0].value == "4"


def test_m12_agendador_continua_apos_falha():
    import m12_agendador as m

    chamadas = {"n": 0}

    def coletar(lat, lon):
        chamadas["n"] += 1
        if chamadas["n"] == 2:
            raise RuntimeError("sem internet (simulado)")
        return {"temperatura": 20.0}

    esperas: list[float] = []
    resultados = m.executar(3, 5, coletar=coletar, esperar=esperas.append)
    assert len(resultados) == 2 and esperas == [5, 5]


def test_arquivos_do_tutorial_existem():
    for nome in [
        "m01_verificar_ambiente.py",
        "m02_fundamentos.py",
        "m03_primeira_dashboard.py",
        "m04_pagina.html",
        "m05_selenium_basico.py",
        "m06_api_open_meteo.py",
        "m07_pandas.py",
        "m08_banco.py",
        "m09_regras.py",
        "test_m09_regras.py",
        "m10_interface.py",
        "m12_agendador.py",
    ]:
        assert (TUTORIAL / nome).exists(), nome
    assert Path(TUTORIAL / "m04_pagina.html").read_text(encoding="utf-8").count('class="cidade') == 3
