"""Dashboard meteorológica de EXEMPLO — independente do sistema ClimaAlerta.

Objetivo didático: mostrar, em um único arquivo curto, os elementos de uma
dashboard (cartões, gráficos, tabela, filtros e um indicador calculado)
antes de estudar APIs, Selenium e banco de dados.

Execução (na raiz do projeto, com o ambiente virtual ativo):
    streamlit run exemplos/dashboard_python/app.py
"""

import plotly.express as px  # gráficos interativos
import streamlit as st  # interface web

# Como o Streamlit executa este arquivo diretamente, os módulos vizinhos
# (na mesma pasta) podem ser importados pelo nome.
from analise import chuva_diaria, filtrar, garantir_fonte_unica, indicador_atencao_chuva, resumo_por_municipio
from dados_simulados import MUNICIPIOS, carregar_dados_simulados

st.set_page_config(page_title="Dashboard de exemplo", page_icon="📊", layout="wide")
st.title("📊 Dashboard meteorológica de exemplo")

# ------------------------------------------------------------------ 1. Fonte
st.sidebar.header("Fonte dos dados")
modo = st.sidebar.radio(
    "Escolha a origem",
    ["Simulados (padrão, funciona sem internet)", "Reais — Open-Meteo (opcional, requer internet)"],
)
usar_reais = modo.startswith("Reais")


@st.cache_data(show_spinner="Carregando dados...")
def carregar(reais: bool):
    """Carrega UMA fonte. O cache evita recarregar a cada clique."""
    if reais:
        from fonte_real import buscar_varios  # import só quando o usuário pede dados reais

        return buscar_varios(list(MUNICIPIOS))
    return carregar_dados_simulados()


try:
    dados = carregar(usar_reais)
except Exception as erro:  # sem internet, por exemplo
    st.error(f"Não foi possível obter dados reais ({erro}). Selecione 'Simulados' para continuar.")
    st.stop()

tipo = garantir_fonte_unica(dados)  # nunca mistura simulados com reais
if tipo == "SIMULADO":
    st.warning("⚠️ **DADOS SIMULADOS** — valores gerados por fórmula, apenas para estudo. Não são medições reais.")
else:
    st.success("✅ **DADOS REAIS** — fonte: Open-Meteo.com (licença CC BY 4.0). Inclui previsão para os próximos dias.")

# ---------------------------------------------------------------- 2. Filtros
st.sidebar.header("Filtros")
municipios = st.sidebar.multiselect(
    "Municípios",
    sorted(dados["municipio"].unique()),
    default=["Sapiranga - RS"] if "Sapiranga - RS" in set(dados["municipio"]) else [],
)
data_min, data_max = dados["data_hora"].min().date(), dados["data_hora"].max().date()
periodo = st.sidebar.slider(
    "Período", min_value=data_min, max_value=data_max, value=(data_min, data_max), format="DD/MM/YYYY"
)
limite = st.sidebar.number_input("Limite do indicador de chuva diária (mm)", 1.0, 200.0, 10.0, step=1.0)

if not municipios:
    st.info("Selecione pelo menos um município na barra lateral.")
    st.stop()
filtrado = filtrar(dados, municipios, periodo[0], periodo[1])
if filtrado.empty:
    st.info("Não há dados para o período escolhido.")
    st.stop()

# ---------------------------------------------------------------- 3. Cartões
ultima = filtrado.sort_values("data_hora").groupby("municipio").tail(1)
st.subheader("Últimos valores do período")
for _, linha in ultima.iterrows():
    st.markdown(f"**{linha['municipio']}** — {linha['data_hora']:%d/%m/%Y %H:%M}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡️ Temperatura", f"{linha['temperatura_c']:.1f} °C")
    c2.metric("💧 Umidade", f"{linha['umidade_pct']:.0f} %")
    c3.metric("🌧️ Chuva (hora)", f"{linha['precipitacao_mm']:.1f} mm")
    c4.metric("💨 Vento", f"{linha['vento_kmh']:.1f} km/h")

# ---------------------------------------------------------------- 4. Gráficos
st.subheader("Gráficos")
fig_temp = px.line(
    filtrado,
    x="data_hora",
    y="temperatura_c",
    color="municipio",
    labels={"data_hora": "Data e hora", "temperatura_c": "Temperatura (°C)", "municipio": "Município"},
    title="Temperatura horária",
)
fig_temp.update_xaxes(tickformat="%d/%m")  # datas no formato brasileiro
st.plotly_chart(fig_temp)

diaria = chuva_diaria(filtrado)
fig_chuva = px.bar(
    diaria,
    x="dia",
    y="precipitacao_mm",
    color="municipio",
    barmode="group",
    labels={"dia": "Dia", "precipitacao_mm": "Chuva (mm)", "municipio": "Município"},
    title="Precipitação acumulada por dia",
)
fig_chuva.update_xaxes(tickformat="%d/%m")
fig_chuva.add_hline(y=limite, line_dash="dash", annotation_text=f"limite do indicador: {limite:g} mm")
st.plotly_chart(fig_chuva)

# ------------------------------------------------------- 5. Indicador calculado
st.subheader("🧮 Indicador de atenção (calculado)")
st.caption(
    "Regra: dia com chuva acumulada maior ou igual ao limite escolhido. "
    "É um cálculo didático — NÃO é um alerta oficial."
)
atencao = indicador_atencao_chuva(filtrado, limite)
if atencao.empty:
    st.success("Nenhum dia atingiu o limite no período filtrado.")
else:
    st.error(f"{len(atencao)} dia(s) atingiram o limite de {limite:g} mm.")
    st.dataframe(atencao, hide_index=True)

# ------------------------------------------------------------------ 6. Tabela
st.subheader("Resumo por município")
st.dataframe(resumo_por_municipio(filtrado), hide_index=True)
with st.expander("Ver todos os registros filtrados"):
    st.dataframe(filtrado, hide_index=True)
st.caption(f"Tipo de dado exibido: {tipo} · Registros: {len(filtrado)}")
