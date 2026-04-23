"""Testes unitários para o módulo de transformação."""

import pytest

from projeto_f1.models import Lap, Session
from projeto_f1.transformation.laps import (
    filtrar_voltas_validas,
    volta_mais_rapida,
    voltas_por_piloto,
)
from projeto_f1.transformation.sessions import filtrar_sessoes_por_tipo


class TestFiltrarVoltasValidas:
    def test_remove_voltas_sem_tempo(self, lista_voltas):
        resultado = filtrar_voltas_validas(lista_voltas)
        assert all(v.lap_duration is not None for v in resultado)

    def test_remove_voltas_saida_pit(self, lista_voltas):
        resultado = filtrar_voltas_validas(lista_voltas)
        assert all(not v.is_pit_out_lap for v in resultado)

    def test_lista_vazia_retorna_vazia(self):
        assert filtrar_voltas_validas([]) == []

    def test_todas_validas_nao_remove_nenhuma(self):
        voltas = [
            Lap(driver_number=1, lap_number=1, lap_duration=90.0, session_key=9159),
            Lap(driver_number=1, lap_number=2, lap_duration=91.0, session_key=9159),
        ]
        assert len(filtrar_voltas_validas(voltas)) == 2


class TestVoltaMaisRapida:
    def test_retorna_volta_com_menor_tempo(self, lista_voltas):
        validas = filtrar_voltas_validas(lista_voltas)
        mais_rapida = volta_mais_rapida(validas)
        assert mais_rapida is not None
        assert mais_rapida.lap_duration == 90.800

    def test_lista_vazia_retorna_none(self):
        assert volta_mais_rapida([]) is None

    def test_lista_somente_sem_tempo_retorna_none(self):
        voltas = [Lap(driver_number=1, lap_number=1, lap_duration=None, session_key=9159)]
        assert volta_mais_rapida(voltas) is None

    def test_unica_volta_e_a_mais_rapida(self):
        volta = Lap(driver_number=1, lap_number=1, lap_duration=88.5, session_key=9159)
        assert volta_mais_rapida([volta]) == volta


class TestVoltasPorPiloto:
    def test_agrupa_por_numero_piloto(self, lista_voltas):
        agrupado = voltas_por_piloto(lista_voltas)
        assert set(agrupado.keys()) == {1, 11}

    def test_quantidade_correta_por_piloto(self, lista_voltas):
        agrupado = voltas_por_piloto(lista_voltas)
        assert len(agrupado[1]) == 3
        assert len(agrupado[11]) == 3

    def test_lista_vazia_retorna_dict_vazio(self):
        assert voltas_por_piloto([]) == {}

    @pytest.mark.parametrize(
        "driver,lap_duration,esperado",
        [
            (1, 90.0, 1),
            (44, 92.5, 1),
        ],
    )
    def test_um_piloto_um_resultado(self, driver, lap_duration, esperado):
        volta = Lap(driver_number=driver, lap_number=1, lap_duration=lap_duration, session_key=9159)
        agrupado = voltas_por_piloto([volta])
        assert len(agrupado[driver]) == esperado


class TestFiltrarSessoesPorTipo:
    def test_retorna_apenas_tipo_correto(self, sessao_corrida, sessao_cancelada):
        sessoes = [sessao_corrida, sessao_cancelada]
        resultado = filtrar_sessoes_por_tipo(sessoes, "Race")
        assert len(resultado) == 1
        assert resultado[0].session_type == "Race"

    def test_exclui_sessoes_canceladas(self, sessao_cancelada):
        resultado = filtrar_sessoes_por_tipo([sessao_cancelada], "Practice")
        assert resultado == []

    def test_tipo_inexistente_retorna_vazio(self, sessao_corrida):
        resultado = filtrar_sessoes_por_tipo([sessao_corrida], "Sprint")
        assert resultado == []

    def test_lista_vazia_retorna_vazia(self):
        assert filtrar_sessoes_por_tipo([], "Race") == []
