"""Funções de criação de gráficos Plotly para o dashboard F1."""

import plotly.graph_objects as go

from projeto_f1.models import Lap
from projeto_f1.models.stint import Stint
from projeto_f1.transformation.laps import volta_mais_rapida, voltas_por_piloto
from projeto_f1.utils.formatters import formatar_duracao

_CORES_COMPOSTOS: dict[str, str] = {
    "SOFT": "#FF3333",
    "MEDIUM": "#FFF200",
    "HARD": "#CCCCCC",
    "INTERMEDIATE": "#39B54A",
    "WET": "#0067FF",
    "UNKNOWN": "#888888",
}

_LAYOUT_BASE = {
    "plot_bgcolor": "#1a1a2e",
    "paper_bgcolor": "#16213e",
    "font": {"color": "#e0e0e0"},
    "xaxis": {"gridcolor": "#2d2d4e", "zerolinecolor": "#2d2d4e"},
    "yaxis": {"gridcolor": "#2d2d4e", "zerolinecolor": "#2d2d4e"},
    "legend": {"bgcolor": "rgba(0,0,0,0.3)", "bordercolor": "#444"},
}


def chart_tempos_volta(
    voltas: list[Lap],
    mapa_pilotos: dict[int, str],
) -> go.Figure:
    """Gráfico de linhas com a evolução dos tempos de volta por piloto.

    Args:
        voltas: Lista de voltas já filtradas (sem pit-out, sem None).
        mapa_pilotos: Mapa driver_number -> sigla do piloto.

    Returns:
        Figura Plotly pronta para renderizar.
    """
    fig = go.Figure()
    agrupado = voltas_por_piloto(voltas)

    for num, vlist in sorted(agrupado.items(), key=lambda kv: kv[0]):
        nome = mapa_pilotos.get(num, str(num))
        vlist_ord = sorted(vlist, key=lambda v: v.lap_number)
        x = [v.lap_number for v in vlist_ord if v.lap_duration is not None]
        y = [v.lap_duration for v in vlist_ord if v.lap_duration is not None]
        hover = [formatar_duracao(d) for d in y]

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers",
                name=nome,
                hovertemplate=f"<b>{nome}</b><br>Volta %{{x}}<br>Tempo: %{{customdata}}<extra></extra>",
                customdata=hover,
                marker={"size": 5},
                line={"width": 2},
            )
        )

    fig.update_layout(
        title="Evolução dos Tempos de Volta",
        xaxis_title="Número da Volta",
        yaxis_title="Tempo (s)",
        hovermode="x unified",
        **_LAYOUT_BASE,
    )
    return fig


def chart_voltas_rapidas(
    voltas: list[Lap],
    mapa_pilotos: dict[int, str],
) -> go.Figure:
    """Gráfico de barras horizontais com a volta mais rápida por piloto.

    Args:
        voltas: Lista de voltas já filtradas.
        mapa_pilotos: Mapa driver_number -> sigla do piloto.

    Returns:
        Figura Plotly pronta para renderizar.
    """
    agrupado = voltas_por_piloto(voltas)
    dados: list[tuple[str, float]] = []

    for num, vlist in agrupado.items():
        rapida = volta_mais_rapida(vlist)
        if rapida and rapida.lap_duration is not None:
            nome = mapa_pilotos.get(num, str(num))
            dados.append((nome, rapida.lap_duration))

    if not dados:
        fig = go.Figure()
        fig.update_layout(title="Sem dados disponíveis", **_LAYOUT_BASE)
        return fig

    dados_ord = sorted(dados, key=lambda d: d[1])
    nomes = [d[0] for d in dados_ord]
    tempos = [d[1] for d in dados_ord]
    hover = [formatar_duracao(t) for t in tempos]

    tempo_min = min(tempos)
    cores = [
        f"rgba(255, {int(200 * (1 - (t - tempo_min) / max(tempos[-1] - tempo_min, 0.001)))}, 0, 0.85)"
        for t in tempos
    ]

    fig = go.Figure(
        go.Bar(
            x=tempos,
            y=nomes,
            orientation="h",
            marker_color=cores,
            marker_line_color="#444",
            marker_line_width=0.8,
            text=hover,
            textposition="outside",
            textfont={"color": "#e0e0e0"},
            hovertemplate="<b>%{y}</b><br>Melhor volta: %{text}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Ranking — Volta Mais Rápida por Piloto",
        xaxis_title="Tempo (s)",
        yaxis_title="Piloto",
        **_LAYOUT_BASE,
    )
    return fig


def chart_estrategia_pneus(
    stints: list[Stint],
    mapa_pilotos: dict[int, str],
) -> go.Figure:
    """Gráfico de Gantt horizontal com a estratégia de pneus por piloto.

    Args:
        stints: Lista de stints da sessão.
        mapa_pilotos: Mapa driver_number -> sigla do piloto.

    Returns:
        Figura Plotly pronta para renderizar.
    """
    fig = go.Figure()
    compostos_vistos: set[str] = set()

    for stint in sorted(stints, key=lambda s: (s.driver_number, s.stint_number or 0)):
        if stint.lap_start is None:
            continue
        nome = mapa_pilotos.get(stint.driver_number, str(stint.driver_number))
        composto = (stint.compound or "UNKNOWN").upper()
        cor = _CORES_COMPOSTOS.get(composto, _CORES_COMPOSTOS["UNKNOWN"])
        lap_end = stint.lap_end or (stint.lap_start + 1)
        duracao = lap_end - stint.lap_start + 1
        idade = stint.tyre_age_at_start or 0
        show_legend = composto not in compostos_vistos
        compostos_vistos.add(composto)

        fig.add_trace(
            go.Bar(
                name=composto,
                y=[nome],
                x=[duracao],
                base=[stint.lap_start - 1],
                orientation="h",
                marker_color=cor,
                marker_line_color="#222",
                marker_line_width=1,
                legendgroup=composto,
                showlegend=show_legend,
                hovertemplate=(
                    f"<b>{nome}</b><br>"
                    f"Composto: {composto}<br>"
                    f"Voltas: {stint.lap_start}–{lap_end}<br>"
                    f"Duração: {duracao} voltas<br>"
                    f"Idade do pneu: {idade} voltas<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="Estratégia de Pneus",
        barmode="stack",
        xaxis_title="Volta",
        yaxis_title="Piloto",
        legend_title="Composto",
        **_LAYOUT_BASE,
    )
    return fig
