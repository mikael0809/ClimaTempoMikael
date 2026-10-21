"""ClimaAlerta — ponto de entrada da interface.

Execução (na raiz do projeto, com o ambiente virtual ativo):
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from src.ui import (
    page_alertas,
    page_aprenda,
    page_diagnostico,
    page_historico,
    page_municipios,
    page_painel,
    page_previsao,
)
from src.ui.common import get_services

st.set_page_config(page_title="ClimaAlerta", page_icon="🌦️", layout="wide")
get_services()  # inicializa banco, logging e município de demonstração

pages = [
    st.Page(page_painel.render, title="Painel", icon="🏠", url_path="painel", default=True),
    st.Page(page_previsao.render, title="Previsão", icon="📈", url_path="previsao"),
    st.Page(page_alertas.render, title="Central de alertas", icon="🚨", url_path="alertas"),
    st.Page(page_municipios.render, title="Municípios", icon="📍", url_path="municipios"),
    st.Page(page_historico.render, title="Histórico", icon="🗂️", url_path="historico"),
    st.Page(page_diagnostico.render, title="Diagnóstico", icon="🩺", url_path="diagnostico"),
    st.Page(page_aprenda.render, title="Aprenda", icon="📚", url_path="aprenda"),
]
st.sidebar.markdown("## 🌦️ ClimaAlerta")
st.sidebar.caption("Monitoramento meteorológico educacional")
st.navigation(pages).run()
