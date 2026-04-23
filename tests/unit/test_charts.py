"""Testes unitários para as funções de geração de gráficos Plotly."""

import plotly.graph_objects as go
import pytest

from projeto_f1.dashboard.charts import (
    chart_estrategia_pneus,
    chart_tempos_volta,
    chart_voltas_rapidas,
)
from projeto_f1.models import Lap
from projeto_f1.transformation.laps import filtrar_voltas_validas


class TestChartTemposVolta:
    def test_retorna_figure(self, lista_voltas, mapa_pilotos):
        validas = filtrar_voltas_validas(lista_voltas)
        fig = chart_tempos_volta(validas, mapa_pilotos)
        assert isinstance(fig, go.Figure)

    def test_tem_trace_por_piloto(self, lista_voltas, mapa_pilotos):
        validas = filtrar_voltas_validas(lista_voltas)
        fig = chart_tempos_volta(validas, mapa_pilotos)
        nomes = [trace.name for trace in fig.data]
        assert "VER" in nomes
        assert "PER" in nomes

    def test_lista_vazia_retorna_figure_sem_traces(self, mapa_pilotos):
        fig = chart_tempos_volta([], mapa_pilotos)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 0

    def test_titulo_correto(self, lista_voltas, mapa_pilotos):
        validas = filtrar_voltas_validas(lista_voltas)
        fig = chart_tempos_volta(validas, mapa_pilotos)
        assert "Tempos de Volta" in fig.layout.title.text


class TestChartVoltasRapidas:
    def test_retorna_figure(self, lista_voltas, mapa_pilotos):
        validas = filtrar_voltas_validas(lista_voltas)
        fig = chart_voltas_rapidas(validas, mapa_pilotos)
        assert isinstance(fig, go.Figure)

    def test_tem_um_trace(self, lista_voltas, mapa_pilotos):
        validas = filtrar_voltas_validas(lista_voltas)
        fig = chart_voltas_rapidas(validas, mapa_pilotos)
        assert len(fig.data) >= 1

    def test_lista_vazia_retorna_figure(self, mapa_pilotos):
        fig = chart_voltas_rapidas([], mapa_pilotos)
        assert isinstance(fig, go.Figure)

    def test_orientacao_horizontal(self, lista_voltas, mapa_pilotos):
        validas = filtrar_voltas_validas(lista_voltas)
        fig = chart_voltas_rapidas(validas, mapa_pilotos)
        assert fig.data[0].orientation == "h"

    def test_numero_de_barras_igual_numero_de_pilotos(self, lista_voltas, mapa_pilotos):
        validas = filtrar_voltas_validas(lista_voltas)
        fig = chart_voltas_rapidas(validas, mapa_pilotos)
        # O gráfico tem 1 trace Bar com y = lista de pilotos
        assert len(fig.data[0].y) == 2


class TestChartEstrategiaPneus:
    def test_retorna_figure(self, lista_stints, mapa_pilotos):
        fig = chart_estrategia_pneus(lista_stints, mapa_pilotos)
        assert isinstance(fig, go.Figure)

    def test_tem_traces(self, lista_stints, mapa_pilotos):
        fig = chart_estrategia_pneus(lista_stints, mapa_pilotos)
        assert len(fig.data) > 0

    def test_lista_vazia_retorna_figure(self, mapa_pilotos):
        fig = chart_estrategia_pneus([], mapa_pilotos)
        assert isinstance(fig, go.Figure)

    def test_cada_composto_com_cor_propria(self, lista_stints, mapa_pilotos):
        fig = chart_estrategia_pneus(lista_stints, mapa_pilotos)
        cores = {trace.marker.color for trace in fig.data}
        assert len(cores) > 1

    @pytest.mark.parametrize("composto,cor_esperada", [
        ("SOFT", "#FF3333"),
        ("MEDIUM", "#FFF200"),
        ("HARD", "#CCCCCC"),
    ])
    def test_cores_dos_compostos(self, mapa_pilotos, composto, cor_esperada):
        from projeto_f1.models.stint import Stint

        stints = [Stint(driver_number=1, stint_number=1, lap_start=1, lap_end=10, compound=composto, session_key=9159)]
        fig = chart_estrategia_pneus(stints, mapa_pilotos)
        assert fig.data[0].marker.color == cor_esperada
