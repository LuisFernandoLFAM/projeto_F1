"""Testes unitários para o módulo de ingestão de stints."""

from unittest.mock import MagicMock

from projeto_f1.ingestion.stints import buscar_stints


STINT_FIXTURE = {
    "driver_number": 1,
    "stint_number": 1,
    "lap_start": 1,
    "lap_end": 20,
    "compound": "SOFT",
    "tyre_age_at_start": 0,
    "session_key": 9159,
}


class TestBuscarStints:
    def test_retorna_lista_de_stints(self):
        mock_client = MagicMock()
        mock_client.get.return_value = [STINT_FIXTURE]
        resultado = buscar_stints(session_key=9159, client=mock_client)
        assert len(resultado) == 1
        assert resultado[0].compound == "SOFT"

    def test_passa_session_key_nos_params(self):
        mock_client = MagicMock()
        mock_client.get.return_value = []
        buscar_stints(session_key=9159, client=mock_client)
        args = mock_client.get.call_args
        assert args[1]["params"]["session_key"] == 9159

    def test_filtra_por_driver_number(self):
        mock_client = MagicMock()
        mock_client.get.return_value = []
        buscar_stints(session_key=9159, driver_number=1, client=mock_client)
        args = mock_client.get.call_args
        assert args[1]["params"]["driver_number"] == 1

    def test_nao_passa_driver_number_quando_ausente(self):
        mock_client = MagicMock()
        mock_client.get.return_value = []
        buscar_stints(session_key=9159, client=mock_client)
        args = mock_client.get.call_args
        assert "driver_number" not in args[1]["params"]

    def test_stint_sem_lap_end_e_valido(self):
        mock_client = MagicMock()
        fixture_sem_lap_end = {**STINT_FIXTURE, "lap_end": None}
        mock_client.get.return_value = [fixture_sem_lap_end]
        resultado = buscar_stints(session_key=9159, client=mock_client)
        assert resultado[0].lap_end is None

    def test_stint_com_lap_start_nulo_nao_lanca_excecao(self):
        mock_client = MagicMock()
        fixture_lap_start_nulo = {**STINT_FIXTURE, "lap_start": None, "stint_number": None}
        mock_client.get.return_value = [fixture_lap_start_nulo]
        resultado = buscar_stints(session_key=9159, client=mock_client)
        assert resultado[0].lap_start is None
        assert resultado[0].stint_number is None
