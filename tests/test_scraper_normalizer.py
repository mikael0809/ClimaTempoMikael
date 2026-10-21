"""Normalização dos textos extraídos pelo Selenium."""

from __future__ import annotations

import pytest

from src.scraper import normalizer as n
from src.scraper import selectors


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("24,5 °C", 24.5),
        ("-3,2 °C", -3.2),
        ("1.013,2 hPa", 1013.2),
        ("  18 °C ", 18.0),
        ("12.5", 12.5),
        ("—", None),
        ("N/D", None),
        ("", None),
        (None, None),
        ("sem número", None),
    ],
)
def test_parse_decimal_br(text, expected):
    assert n.parse_decimal_br(text) == expected


def test_specific_parsers_validate_ranges():
    assert n.parse_temperature("24,5 °C") == 24.5
    assert n.parse_temperature("120 °C") is None  # fora da faixa física
    assert n.parse_humidity("Umidade: 57 %") == 57.0
    assert n.parse_humidity("Umidade: 140 %") is None
    assert n.parse_precipitation("25,2 mm") == 25.2


def test_parse_wind():
    assert n.parse_wind("Vento: 13,5 km/h (SE)") == (13.5, "SE")
    assert n.parse_wind("Vento: 4 km/h") == (4.0, None)
    assert n.parse_wind(None) == (None, None)


def test_parse_date_and_clean_text():
    assert n.parse_date_br("Data: 22/10/2026") == "2026-10-22"
    assert n.parse_date_br("amanhã") is None
    assert n.clean_text("  Parcialmente \n  nublado ") == "Parcialmente nublado"
    assert n.is_missing(" — ")


def test_selectors_are_centralized_and_documented():
    assert len(selectors.ALL_SELECTORS) >= 10
    for name, selector in selectors.ALL_SELECTORS.items():
        assert selector.css and selector.purpose, name
