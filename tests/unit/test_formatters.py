"""Testes unitários para utilitários de formatação."""

import pytest

from projeto_f1.utils.formatters import formatar_duracao, formatar_velocidade


class TestFormatarDuracao:
    @pytest.mark.parametrize(
        "entrada,esperado",
        [
            (83.456, "1:23.456"),
            (60.0, "1:00.000"),
            (0.0, "0:00.000"),
            (90.800, "1:30.800"),
        ],
    )
    def test_formata_segundos_corretamente(self, entrada, esperado):
        assert formatar_duracao(entrada) == esperado

    def test_none_retorna_traco(self):
        assert formatar_duracao(None) == "–"

    def test_menos_de_um_minuto(self):
        resultado = formatar_duracao(59.999)
        assert resultado.startswith("0:")


class TestFormatarVelocidade:
    def test_formata_com_unidade(self):
        assert formatar_velocidade(315) == "315 km/h"

    def test_zero_kmh(self):
        assert formatar_velocidade(0) == "0 km/h"

    def test_none_retorna_traco(self):
        assert formatar_velocidade(None) == "–"

    @pytest.mark.parametrize("kmh", [100, 200, 350])
    def test_varios_valores(self, kmh):
        assert formatar_velocidade(kmh) == f"{kmh} km/h"
