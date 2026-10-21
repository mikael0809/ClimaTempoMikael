"""Validação e conversão de dados (RN002, RN004)."""

from __future__ import annotations

import pytest

from src.utils.brazil import state_code_from_name
from src.utils.timeutils import format_datetime, local_to_utc
from src.utils.validators import (
    ValidationError,
    normalize_text,
    to_float,
    validate_coordinates,
    validate_measurement,
    validate_search_term,
)
from src.utils.weather_codes import describe_weather_code, wind_direction_label


@pytest.mark.parametrize(
    ("variable", "raw", "expected"),
    [
        ("temperature", 24.7, 24.7),
        ("temperature", "18", 18.0),
        ("humidity", 150, None),  # fisicamente impossível
        ("humidity", -1, None),
        ("precipitation_probability", 100, 100.0),
        ("wind_direction", 361, None),
        ("pressure", 1013.3, 1013.3),
        ("pressure", 50, None),
        ("temperature", None, None),
        ("temperature", "abc", None),
        ("temperature", float("nan"), None),
    ],
)
def test_validate_measurement(variable, raw, expected):
    assert validate_measurement(variable, raw) == expected


def test_to_float_rejects_bool():
    assert to_float(True) is None


def test_coordinates_valid_for_sapiranga():
    assert validate_coordinates(-29.638061, -51.006944) == (-29.63806, -51.00694)


@pytest.mark.parametrize(("lat", "lon"), [(91, 0), (0, 181), (40.7, -74.0), ("x", 1), (None, None)])
def test_coordinates_invalid(lat, lon):
    with pytest.raises(ValidationError):
        validate_coordinates(lat, lon)


def test_coordinates_outside_brazil_allowed_when_flag_disabled():
    assert validate_coordinates(40.7, -74.0, brazil_only=False) == (40.7, -74.0)


@pytest.mark.parametrize("term", ["", "a", "x" * 81, "Sapiranga; DROP TABLE", "<script>"])
def test_search_term_invalid(term):
    with pytest.raises(ValidationError):
        validate_search_term(term)


def test_search_term_normalizes_spaces():
    assert validate_search_term("  São   Leopoldo ") == "São Leopoldo"


def test_normalize_text_removes_accents():
    assert normalize_text("São José dos Pinhais") == "sao jose dos pinhais"


def test_state_code_from_name():
    assert state_code_from_name("Rio Grande do Sul") == "RS"
    assert state_code_from_name("sao paulo") == "SP"
    assert state_code_from_name("rs") == "RS"
    assert state_code_from_name("Atlantida") is None


def test_local_to_utc_brasilia():
    assert local_to_utc("2026-10-21T14:45", "America/Sao_Paulo").isoformat() == "2026-10-21T17:45:00"


def test_format_datetime_displays_brasilia():
    from datetime import datetime

    assert format_datetime(datetime(2026, 10, 21, 17, 45)) == "21/10/2026 14:45"
    assert format_datetime(None) == "—"


def test_weather_code_and_wind_labels():
    assert describe_weather_code(3) == "Nublado"
    assert describe_weather_code(None) == "Indisponível"
    assert describe_weather_code(42).startswith("Código")
    assert wind_direction_label(134) == "SE"
    assert wind_direction_label(0) == "N"
    assert wind_direction_label(None) == "—"
