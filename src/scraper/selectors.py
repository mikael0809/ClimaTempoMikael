"""Seletores CSS centralizados do scraper de demonstração.

Manter todos os seletores em um só lugar facilita a manutenção: quando o
HTML da página muda, apenas este arquivo precisa ser ajustado.

Cada seletor é acompanhado de sua finalidade.
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulos 4 e 5 · Documento 06 (Fluxograma 4).
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Selector:
    css: str
    purpose: str


# Elemento que só aparece depois que o JavaScript termina de carregar os dados.
PAGE_READY = Selector("#painel-cidades[data-status='carregado']", "Indica que o conteúdo dinâmico foi carregado")
DEMO_NOTICE = Selector("#aviso-dados-ficticios", "Faixa que identifica os dados como fictícios")
UPDATED_AT = Selector("#atualizado-em", "Data/hora da última atualização (atributo datetime)")

CITY_CARD = Selector("article.cartao-cidade", "Cartão de cada cidade (um por cidade)")
CITY_NAME = Selector(".cidade-nome", "Nome da cidade dentro do cartão")
CITY_STATE = Selector(".cidade-uf", "Sigla da UF dentro do cartão")
TEMPERATURE = Selector(".temperatura", "Texto da temperatura, ex.: '24,5 °C'")
HUMIDITY = Selector(".umidade", "Texto da umidade, ex.: 'Umidade: 57 %'")
WIND = Selector(".vento", "Texto do vento, ex.: 'Vento: 13,5 km/h (SE)'")
CONDITION = Selector(".condicao", "Descrição da condição do tempo")
DETAILS_LINK = Selector("a.link-detalhes", "Link para a página de detalhes (atributo href)")

FORECAST_ROWS = Selector("#tabela-previsao tbody tr", "Linhas da tabela de previsão")
FORECAST_CELLS = Selector("td", "Células de uma linha da tabela")

ALL_SELECTORS = {name: value for name, value in globals().items() if isinstance(value, Selector)}
