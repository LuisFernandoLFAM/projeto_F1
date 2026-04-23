"""Testes unitários para o módulo de ingestão."""

from unittest.mock import MagicMock, patch

import pytest

from projeto_f1.ingestion.client import OpenF1Client
from projeto_f1.ingestion.drivers import buscar_pilotos
from projeto_f1.ingestion.laps import buscar_voltas
from projeto_f1.ingestion.sessions import buscar_sessoes


SESSAO_FIXTURE = {
    "session_key": 9159,
    "session_name": "Race",
    "session_type": "Race",
    "meeting_key": 1219,
    "date_start": "2024-03-24T15:00:00",
    "country_name": "Bahrain",
    "circuit_short_name": "Bahrain",
    "is_cancelled": False,
}

VOLTA_FIXTURE = {
    "driver_number": 1,
    "lap_number": 2,
    "lap_duration": 91.5,
    "duration_sector_1": 28.1,
    "duration_sector_2": 33.4,
    "duration_sector_3": 30.0,
    "is_pit_out_lap": False,
    "session_key": 9159,
}

PILOTO_FIXTURE = {
    "driver_number": 1,
    "full_name": "Max Verstappen",
    "name_acronym": "VER",
    "broadcast_name": "M. VERSTAPPEN",
    "team_name": "Red Bull Racing",
    "team_colour": "3671C6",
    "session_key": 9159,
}


class TestOpenF1Client:
    def test_get_retorna_lista(self):
        client = OpenF1Client()
        with patch("projeto_f1.ingestion.client.requests.get") as mock_get:
            mock_get.return_value = MagicMock(status_code=200, json=lambda: [SESSAO_FIXTURE])
            mock_get.return_value.raise_for_status = MagicMock()
            resultado = client.get("/sessions")
        assert isinstance(resultado, list)
        assert len(resultado) == 1

    def test_get_chama_url_correta(self):
        client = OpenF1Client(base_url="https://api.openf1.org/v1")
        with patch("projeto_f1.ingestion.client.requests.get") as mock_get:
            mock_get.return_value = MagicMock(status_code=200, json=lambda: [])
            mock_get.return_value.raise_for_status = MagicMock()
            client.get("/sessions", params={"year": 2024})
            mock_get.assert_called_once_with(
                "https://api.openf1.org/v1/sessions",
                params={"year": 2024},
                timeout=client.timeout,
            )


class TestBuscarSessoes:
    def test_retorna_lista_de_sessions(self):
        mock_client = MagicMock()
        mock_client.get.return_value = [SESSAO_FIXTURE]
        resultado = buscar_sessoes(client=mock_client)
        assert len(resultado) == 1
        assert resultado[0].session_name == "Race"

    def test_passa_filtro_de_ano(self):
        mock_client = MagicMock()
        mock_client.get.return_value = []
        buscar_sessoes(ano=2024, client=mock_client)
        mock_client.get.assert_called_once_with("/sessions", params={"year": 2024})

    def test_passa_session_key(self):
        mock_client = MagicMock()
        mock_client.get.return_value = [SESSAO_FIXTURE]
        buscar_sessoes(session_key="latest", client=mock_client)
        args = mock_client.get.call_args
        assert args[1]["params"]["session_key"] == "latest"


class TestBuscarVoltas:
    def test_retorna_lista_de_laps(self):
        mock_client = MagicMock()
        mock_client.get.return_value = [VOLTA_FIXTURE]
        resultado = buscar_voltas(session_key=9159, client=mock_client)
        assert len(resultado) == 1
        assert resultado[0].lap_duration == 91.5

    def test_passa_driver_number_quando_informado(self):
        mock_client = MagicMock()
        mock_client.get.return_value = []
        buscar_voltas(session_key=9159, driver_number=1, client=mock_client)
        args = mock_client.get.call_args
        assert args[1]["params"]["driver_number"] == 1

    def test_nao_passa_driver_number_quando_ausente(self):
        mock_client = MagicMock()
        mock_client.get.return_value = []
        buscar_voltas(session_key=9159, client=mock_client)
        args = mock_client.get.call_args
        assert "driver_number" not in args[1]["params"]


class TestBuscarPilotos:
    def test_retorna_lista_de_drivers(self):
        mock_client = MagicMock()
        mock_client.get.return_value = [PILOTO_FIXTURE]
        resultado = buscar_pilotos(session_key=9159, client=mock_client)
        assert len(resultado) == 1
        assert resultado[0].name_acronym == "VER"

    def test_filtra_por_driver_number(self):
        mock_client = MagicMock()
        mock_client.get.return_value = []
        buscar_pilotos(session_key=9159, driver_number=1, client=mock_client)
        args = mock_client.get.call_args
        assert args[1]["params"]["driver_number"] == 1
