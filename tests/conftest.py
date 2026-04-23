"""Fixtures compartilhadas entre os testes do projeto F1."""

import pytest

from projeto_f1.models import Driver, Lap, Session
from projeto_f1.models.stint import Stint


@pytest.fixture
def sessao_corrida() -> Session:
    return Session(
        session_key=9159,
        session_name="Race",
        session_type="Race",
        meeting_key=1219,
        date_start="2024-03-24T15:00:00",
        date_end="2024-03-24T17:00:00",
        circuit_short_name="Bahrain",
        country_name="Bahrain",
        is_cancelled=False,
    )


@pytest.fixture
def sessao_cancelada() -> Session:
    return Session(
        session_key=9999,
        session_name="Practice 1",
        session_type="Practice",
        meeting_key=1219,
        date_start="2024-03-22T11:30:00",
        is_cancelled=True,
    )


@pytest.fixture
def piloto_verstappen() -> Driver:
    return Driver(
        driver_number=1,
        full_name="Max Verstappen",
        name_acronym="VER",
        broadcast_name="M. VERSTAPPEN",
        team_name="Red Bull Racing",
        team_colour="3671C6",
        session_key=9159,
    )


@pytest.fixture
def lista_voltas() -> list[Lap]:
    return [
        Lap(driver_number=1, lap_number=1, lap_duration=95.123, session_key=9159, is_pit_out_lap=True),
        Lap(driver_number=1, lap_number=2, lap_duration=91.500, session_key=9159),
        Lap(driver_number=1, lap_number=3, lap_duration=90.800, session_key=9159),
        Lap(driver_number=11, lap_number=1, lap_duration=92.000, session_key=9159),
        Lap(driver_number=11, lap_number=2, lap_duration=None, session_key=9159),
        Lap(driver_number=11, lap_number=3, lap_duration=91.200, session_key=9159),
    ]


@pytest.fixture
def lista_stints() -> list[Stint]:
    return [
        Stint(driver_number=1, stint_number=1, lap_start=1, lap_end=20, compound="SOFT", tyre_age_at_start=0, session_key=9159),
        Stint(driver_number=1, stint_number=2, lap_start=21, lap_end=40, compound="MEDIUM", tyre_age_at_start=0, session_key=9159),
        Stint(driver_number=1, stint_number=3, lap_start=41, lap_end=57, compound="HARD", tyre_age_at_start=0, session_key=9159),
        Stint(driver_number=11, stint_number=1, lap_start=1, lap_end=18, compound="MEDIUM", tyre_age_at_start=3, session_key=9159),
        Stint(driver_number=11, stint_number=2, lap_start=19, lap_end=57, compound="HARD", tyre_age_at_start=0, session_key=9159),
    ]


@pytest.fixture
def mapa_pilotos() -> dict[int, str]:
    return {1: "VER", 11: "PER"}
