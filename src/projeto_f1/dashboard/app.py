"""Dashboard interativo de Fórmula 1 — OpenF1 API."""

import logging

import streamlit as st

from projeto_f1.dashboard.charts import (
    chart_estrategia_pneus,
    chart_tempos_volta,
    chart_voltas_rapidas,
)
from projeto_f1.ingestion import buscar_pilotos, buscar_sessoes, buscar_voltas
from projeto_f1.ingestion.stints import buscar_stints
from projeto_f1.transformation.laps import filtrar_voltas_validas, volta_mais_rapida
from projeto_f1.transformation.sessions import filtrar_sessoes_por_tipo
from projeto_f1.utils.formatters import formatar_duracao

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Dashboard F1",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

_CSS = """
<style>
    .stMetric { background: #1a1a2e; border-radius: 8px; padding: 12px; }
    .block-container { padding-top: 1.5rem; }
</style>
"""
st.markdown(_CSS, unsafe_allow_html=True)


@st.cache_data(ttl=300, show_spinner=False)
def _buscar_sessoes_cache(ano: int):
    return buscar_sessoes(ano=ano)


@st.cache_data(ttl=300, show_spinner=False)
def _buscar_dados_sessao(session_key: int):
    voltas = buscar_voltas(session_key=session_key)
    pilotos = buscar_pilotos(session_key=session_key)
    stints = buscar_stints(session_key=session_key)
    return voltas, pilotos, stints


def _mapa_pilotos(pilotos) -> dict[int, str]:
    return {p.driver_number: p.name_acronym for p in pilotos}


def _cabecalho_sessao(sessao, n_pilotos: int, n_voltas: int, mais_rapida) -> None:
    st.title("🏎️ Dashboard F1 — OpenF1")
    st.subheader(
        f"{sessao.country_name or ''} · {sessao.circuit_short_name or ''} "
        f"· {sessao.session_name} · {sessao.date_start[:10]}"
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Pilotos na sessão", n_pilotos)
    col2.metric("Voltas válidas", n_voltas)
    if mais_rapida:
        col3.metric("Volta mais rápida", formatar_duracao(mais_rapida.lap_duration))
    else:
        col3.metric("Volta mais rápida", "–")


def main() -> None:
    """Ponto de entrada do dashboard Streamlit."""
    with st.sidebar:
        st.header("⚙️ Filtros")
        ano = st.selectbox("Temporada", [2025, 2024, 2023], index=0)
        tipo = st.selectbox(
            "Tipo de sessão",
            ["Race", "Qualifying", "Sprint", "Practice"],
            index=0,
        )

    with st.spinner("Carregando calendário..."):
        try:
            sessoes = _buscar_sessoes_cache(ano)
        except Exception as exc:
            st.error(f"Erro ao buscar sessões: {exc}")
            logger.error("Falha ao buscar sessões para %d: %s", ano, exc)
            return

    sessoes_filtradas = filtrar_sessoes_por_tipo(sessoes, tipo)

    if not sessoes_filtradas:
        st.title("🏎️ Dashboard F1 — OpenF1")
        st.warning(f"Nenhuma sessão do tipo **{tipo}** encontrada para **{ano}**.")
        return

    opcoes = {
        f"{s.country_name} — {s.circuit_short_name or s.session_name} ({s.date_start[:10]})": s
        for s in sessoes_filtradas
    }

    with st.sidebar:
        nome_sessao = st.selectbox("Sessão", list(opcoes.keys()))
        st.divider()
        st.caption("Dados fornecidos por [OpenF1](https://openf1.org)")

    sessao = opcoes[nome_sessao]

    with st.spinner("Carregando dados da sessão..."):
        try:
            voltas, pilotos, stints = _buscar_dados_sessao(sessao.session_key)
        except Exception as exc:
            st.error(f"Erro ao buscar dados da sessão: {exc}")
            logger.error("Falha ao buscar sessão %d: %s", sessao.session_key, exc)
            return

    mapa = _mapa_pilotos(pilotos)
    voltas_validas = filtrar_voltas_validas(voltas)
    mais_rapida = volta_mais_rapida(voltas_validas)

    _cabecalho_sessao(sessao, len(pilotos), len(voltas_validas), mais_rapida)

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["📈 Tempos de Volta", "🏆 Ranking de Voltas Rápidas", "🔴 Estratégia de Pneus"]
    )

    with tab1:
        if voltas_validas:
            st.plotly_chart(
                chart_tempos_volta(voltas_validas, mapa),
                use_container_width=True,
            )
        else:
            st.info("Dados de tempos de volta não disponíveis para esta sessão.")

    with tab2:
        if voltas_validas:
            st.plotly_chart(
                chart_voltas_rapidas(voltas_validas, mapa),
                use_container_width=True,
            )
        else:
            st.info("Sem dados de voltas válidas.")

    with tab3:
        if stints:
            st.plotly_chart(
                chart_estrategia_pneus(stints, mapa),
                use_container_width=True,
            )
        else:
            st.info("Dados de estratégia de pneus não disponíveis para esta sessão.")


main()
