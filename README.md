<div align="center">

# 🌦️ ClimaAlerta — repositório da turma

**Implemente um sistema real de monitoramento meteorológico em Python,
guiado pelos testes, pela documentação técnica e pelo manual pedagógico.**

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![IDE](https://img.shields.io/badge/IDE-PyCharm-000000?logo=pycharm&logoColor=white)
![pytest](https://img.shields.io/badge/testes-pytest-0A9EDC?logo=pytest&logoColor=white)

</div>

> [!IMPORTANT]
> Projeto educacional. Os *indicadores locais* que você vai programar **não são
> alertas oficiais**. Em situações de risco, siga o INMET e a Defesa Civil (199).

## Sumário

1. [O desafio](#1-o-desafio)
2. [Como saber o que fazer](#2-como-saber-o-que-fazer)
3. [Preparação no PyCharm](#3-preparação-no-pycharm)
4. [Preparação pelo terminal (alternativa)](#4-preparação-pelo-terminal-alternativa)
5. [Acompanhando o progresso](#5-acompanhando-o-progresso)
6. [Ordem sugerida de implementação](#6-ordem-sugerida-de-implementação)
7. [Executando o sistema](#7-executando-o-sistema)
8. [Git e GitHub no PyCharm](#8-git-e-github-no-pycharm)
9. [Integração contínua](#9-integração-contínua-github-actions)
10. [Regras da turma](#10-regras-da-turma)
11. [Problemas comuns](#11-problemas-comuns)

## 1. O desafio

Todos os arquivos do sistema já existem, com as **assinaturas** das funções e
classes e suas **docstrings**, mas **sem o código**. Cada função termina em:

```python
raise NotImplementedError("TODO: implementar nome_da_funcao")
```

Sua tarefa é substituir essa linha pela implementação, **sem mudar o nome, os
parâmetros nem o tipo de retorno** — outras partes do sistema e os testes dependem deles.

Já vêm prontos: `app.py`, os seletores CSS (`src/scraper/selectors.py`), as tabelas
de constantes (códigos WMO, UFs, mapeamentos da Open-Meteo), a página HTML do
Selenium, os dados de teste e toda a documentação em PDF.

## 2. Como saber o que fazer

| Fonte | Onde | Para quê |
|---|---|---|
| **Manual pedagógico** (PyCharm) | `documentacao/pedagogica/manual_pedagogico_climaalerta.pdf` | Passo a passo em 15 módulos; os módulos 1–13 são feitos em `exemplos/tutorial/` |
| **Documentação técnica** | `documentacao/tecnica/` (12 PDFs) | Requisitos, regras de negócio, arquitetura, dicionário de dados, BPMN, fluxogramas, casos de uso, testes, implantação, segurança, rastreabilidade, manual técnico |
| **Testes automatizados** | `tests/` | Descrevem exatamente o comportamento esperado. **Não altere os testes.** |
| **Comentário no topo de cada arquivo** | `src/**/*.py` | Indica o módulo do manual e o documento técnico correspondentes |
| **Janela TODO do PyCharm** | Alt+6 | Lista todas as funções ainda não implementadas |

## 3. Preparação no PyCharm

1. **Abrir:** *Get from VCS / Clone Repository* com o endereço deste repositório
   (ou **Open** na pasta, se você baixou o ZIP). Confirme **Trust Project**.
2. **Interpretador:** Settings (Ctrl+Alt+S) › Project › **Python Interpreter** ›
   *Add Interpreter* › *Add Local Interpreter* › **Generate new · Virtualenv** ·
   *Location* `<pasta do projeto>/.venv` · Python 3.12+ › OK.
   (Se o PyCharm oferecer criar o ambiente automaticamente, aceite.)
3. **Dependências** — um dos caminhos:
   - abra `requirements.txt` e clique em **Install requirements** na faixa do topo do editor; ou
   - **View › Tool Windows › Python Packages**, pesquise e instale cada pacote; ou
   - Terminal do PyCharm (Alt+F12): `python -m pip install -r requirements.txt`.
4. **Ajustes:**
   - Settings › Editor › **File Encodings** › UTF-8;
   - Settings › Tools › Python Integrated Tools › *Default test runner*: **pytest**;
   - Run › Edit Configurations › *Edit configuration templates* › **Python** e
     **Python tests › pytest** › *Working directory*: `$ProjectFileDir$`;
   - botão direito em `exemplos/tutorial` › Mark Directory as › **Sources Root**;
   - copie `.env.example` para `.env` (Ctrl+C / Ctrl+V na janela Project).
5. **Teste rápido:** botão direito na pasta `tests` › **Run 'pytest in tests'**.
   No início, quase tudo fica vermelho — é o esperado.

## 4. Preparação pelo terminal (alternativa)

Windows (PowerShell), na pasta raiz:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Linux (Bash), na pasta raiz:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## 5. Acompanhando o progresso

| No PyCharm | No terminal |
|---|---|
| Botão direito em `tests` › Run 'pytest in tests' | `pytest` |
| ▶ ao lado de um `def test_...` | `pytest -k nome_do_teste -v` |
| Botão direito em um arquivo de teste › Run | `pytest tests/test_validators.py -v` |
| Botão *Rerun Failed Tests* na janela Run | `pytest --lf` |
| Janela TODO (Alt+6) | — |
| Code › Inspect Code | `ruff check .` |

Um teste que falha com `NotImplementedError: TODO: implementar X` aponta a próxima
função a escrever. Use o depurador (🐞 Debug) para investigar falhas: marque um
ponto de parada na margem e avance com F8.

## 6. Ordem sugerida de implementação

Cada etapa usa as anteriores. Execute os testes indicados ao final de cada uma.

| Etapa | Arquivos | Testes | Manual / documento |
|---|---|---|---|
| 0 | Tutorial `exemplos/tutorial/m01` a `m12` | `tests/test_tutorial.py` | Módulos 1–13 |
| 1 | `src/utils/validators.py`, `timeutils.py`, `weather_codes.py`, `brazil.py`, `logging_config.py` | `test_validators.py` | Módulo 2 · Doc 10 |
| 2 | `src/config.py` | `test_config.py` | Módulo 11 · Doc 12 |
| 3 | `src/database/models.py`, `connection.py`, `repositories.py` | `test_database.py` | Módulo 8 · Doc 04 |
| 4 | `src/integrations/http_client.py`, `open_meteo.py`, `geocoding.py`, `inmet.py` | `test_http_client.py`, `test_open_meteo.py`, `test_geocoding.py`, `test_inmet.py` | Módulo 6 · Doc 03 |
| 5 | `src/scraper/normalizer.py`, `driver.py`, `weather_scraper.py` | `test_scraper_normalizer.py`, `test_scraper_selenium.py` | Módulos 4–5 · Doc 06 |
| 6 | `src/services/*.py` | `test_indicators.py`, `test_municipality_service.py`, `test_weather_service.py`, `test_alert_service.py`, `test_export.py` | Módulos 7 e 9 · Doc 02 |
| 7 | `src/collectors/*.py`, `scripts/*.py` | `test_collectors.py` | Módulos 11–12 · Docs 05 e 09 |
| 8 | `src/ui/*.py` (o `app.py` já está pronto) | `test_ui_pages.py` | Módulos 3 e 10 · Doc 07 |
| 9 | `exemplos/dashboard_python/*.py` | `exemplos/dashboard_python/tests` | Módulo 3 |

Nos modelos do banco (`src/database/models.py`) cada classe tem a linha
`__abstract__ = True`. **Remova-a** quando declarar as colunas da tabela (o
Documento 04 lista todas elas).

## 7. Executando o sistema

Depois das etapas 1 a 8, crie as configurações de execução
(Run › Edit Configurations › **+** › Python):

| Nome | Tipo | Valor | Parâmetros |
|---|---|---|---|
| `Inicializar banco` | script | `scripts/inicializar_banco.py` | — |
| `Coletar dados` | script | `scripts/coletar_dados.py` | — |
| `ClimaAlerta` | **module** | `streamlit` | `run app.py` |

Execute nessa ordem. Pelo terminal:

```bash
python scripts/inicializar_banco.py
python scripts/coletar_dados.py
streamlit run app.py
```

## 8. Git e GitHub no PyCharm

| Ação | Como |
|---|---|
| Commit | Ctrl+K — marque os arquivos, escreva a mensagem, **Commit** |
| Enviar (push) | Ctrl+Shift+K |
| Receber alterações | Ctrl+T (Update Project) |
| Histórico | Alt+9 › Log |
| Novo ramo | Clique no nome do ramo na barra superior › New Branch |
| Ver diferenças | Botão direito no arquivo › Git › Show Diff |

Faça *commits* pequenos e frequentes, com mensagens que expliquem o que mudou e por quê.

## 9. Integração contínua (GitHub Actions)

A cada `push`, o GitHub executa `ruff check .` e `pytest` em Linux
(`.github/workflows/testes.yml`). No início o resultado será vermelho — é esperado.
Acompanhe a aba **Actions** do repositório para ver os testes ficando verdes.

## 10. Regras da turma

- Não altere os arquivos de `tests/` nem as assinaturas das funções.
- Dados fictícios (página do Selenium) e simulados (dashboard de exemplo) nunca
  devem ser misturados com dados reais.
- Indicadores calculados nunca são apresentados como alertas oficiais.
- Nunca grave senhas ou chaves no código; o `.env` não vai para o Git.
- Cite as fontes de dados: Open-Meteo (CC BY 4.0), INMET e IBGE.

## 11. Problemas comuns

| Sintoma | Solução |
|---|---|
| Barra de status sem `.venv` | Refaça o passo 2 da seção 3 |
| `ModuleNotFoundError` de uma biblioteca | Instale as dependências (passo 3) |
| `ModuleNotFoundError: No module named 'src'` | *Working directory* = pasta raiz (passo 4) |
| Não aparece ▶ ao lado dos testes | *Default test runner* = pytest (passo 4) |
| Testes de Selenium "skipped" | Instale o Google Chrome |
| "missing ScriptRunContext" | Execute o Streamlit como **module** `streamlit` com `run app.py` |
