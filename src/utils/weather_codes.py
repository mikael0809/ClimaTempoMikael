"""Tradução dos códigos meteorológicos WMO usados pela Open-Meteo.

Referência: tabela "WMO Weather interpretation codes (WW)" na documentação
da Open-Meteo (https://open-meteo.com/en/docs).
"""

# ---------------------------------------------------------------------------
# ESQUELETO PARA OS ALUNOS: as funções e métodos deste arquivo estão sem
# implementação (NotImplementedError). Implemente-os mantendo as assinaturas.
# Referências: Manual, módulo 2 · Documento 10 (Validação de entradas) · Documento 12.
# Os testes em tests/ descrevem o comportamento esperado.
# ---------------------------------------------------------------------------

from __future__ import annotations

WMO_CODES: dict[int, tuple[str, str]] = {
    0: ("Céu limpo", "☀️"),
    1: ("Predominantemente limpo", "🌤️"),
    2: ("Parcialmente nublado", "⛅"),
    3: ("Nublado", "☁️"),
    45: ("Nevoeiro", "🌫️"),
    48: ("Nevoeiro com geada", "🌫️"),
    51: ("Garoa fraca", "🌦️"),
    53: ("Garoa moderada", "🌦️"),
    55: ("Garoa densa", "🌧️"),
    56: ("Garoa congelante fraca", "🌧️"),
    57: ("Garoa congelante densa", "🌧️"),
    61: ("Chuva fraca", "🌧️"),
    63: ("Chuva moderada", "🌧️"),
    65: ("Chuva forte", "🌧️"),
    66: ("Chuva congelante fraca", "🌧️"),
    67: ("Chuva congelante forte", "🌧️"),
    71: ("Neve fraca", "🌨️"),
    73: ("Neve moderada", "🌨️"),
    75: ("Neve forte", "❄️"),
    77: ("Grãos de neve", "🌨️"),
    80: ("Pancadas de chuva fracas", "🌦️"),
    81: ("Pancadas de chuva moderadas", "🌧️"),
    82: ("Pancadas de chuva violentas", "⛈️"),
    85: ("Pancadas de neve fracas", "🌨️"),
    86: ("Pancadas de neve fortes", "❄️"),
    95: ("Trovoada", "⛈️"),
    96: ("Trovoada com granizo fraco", "⛈️"),
    99: ("Trovoada com granizo forte", "⛈️"),
}


def describe_weather_code(code: int | None) -> str:
    raise NotImplementedError("TODO: implementar describe_weather_code")


def weather_icon(code: int | None) -> str:
    raise NotImplementedError("TODO: implementar weather_icon")


COMPASS_PT = ["N", "NE", "L", "SE", "S", "SO", "O", "NO"]


def wind_direction_label(degrees: float | None) -> str:
    """Converte graus (0–360) em ponto cardeal em português (L = leste, O = oeste)."""
    raise NotImplementedError("TODO: implementar wind_direction_label")
