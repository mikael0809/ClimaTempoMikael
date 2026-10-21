# Pasta do tutorial (módulos 1 a 13 do manual)

Esta pasta começa **vazia**. Em cada módulo do manual pedagógico você cria aqui o
arquivo indicado — no PyCharm: botão direito nesta pasta › **New › Python File**
(ou **New › HTML File** no módulo 4) — e verifica com o teste correspondente.

Antes de começar, marque esta pasta como raiz de código: botão direito ›
**Mark Directory as › Sources Root**. No módulo 1 do manual, ignore a instrução de
renomear a pasta: neste repositório ela já vem vazia.

| Módulo | Arquivo que você cria | Verificação no PyCharm (`tests/test_tutorial.py`) | Terminal |
|---|---|---|---|
| 1 | `m01_verificar_ambiente.py` | ▶ em `test_m01_verifica_ambiente` | `pytest tests/test_tutorial.py -k m01 -v` |
| 2 | `m02_fundamentos.py` | ▶ em `test_m02_fundamentos` | `pytest tests/test_tutorial.py -k m02 -v` |
| 3 | `m03_primeira_dashboard.py` | ▶ em `test_m03_dashboard` | `pytest tests/test_tutorial.py -k m03 -v` |
| 4 | `m04_pagina.html` | abrir no Chrome pelo PyCharm e testar seletores (F12) | — |
| 5 | `m05_selenium_basico.py` | ▶ em `test_m05_selenium` | `pytest tests/test_tutorial.py -k m05 -v` |
| 6 | `m06_api_open_meteo.py` | ▶ em `test_m06_api_com_resposta_real_gravada` | `pytest tests/test_tutorial.py -k m06 -v` |
| 7 | `m07_pandas.py` | ▶ em `test_m07_pandas` | `pytest tests/test_tutorial.py -k m07 -v` |
| 8 | `m08_banco.py` | ▶ em `test_m08_banco` | `pytest tests/test_tutorial.py -k m08 -v` |
| 9 | `m09_regras.py` | execução manual (os testes vêm no módulo 13) | — |
| 10 | `m10_interface.py` | ▶ em `test_m10_interface_le_o_banco` | `pytest tests/test_tutorial.py -k m10 -v` |
| 12 | `m12_agendador.py` | ▶ em `test_m12_agendador_continua_apos_falha` | `pytest tests/test_tutorial.py -k m12 -v` |
| 13 | `test_m09_regras.py` | botão direito no arquivo › Run | `pytest exemplos/tutorial/test_m09_regras.py -v` |

Todo o código desses arquivos está completo e comentado no manual pedagógico.
