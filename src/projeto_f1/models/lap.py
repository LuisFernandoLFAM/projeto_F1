"""Modelo Pydantic para voltas da OpenF1 API."""

from pydantic import BaseModel


class Lap(BaseModel):
    """Representa os dados de uma volta de um piloto em uma sessão.

    Args:
        driver_number: Número de corrida do piloto.
        lap_number: Número sequencial da volta.
        lap_duration: Tempo total da volta em segundos.
        duration_sector_1: Tempo do setor 1 em segundos.
        duration_sector_2: Tempo do setor 2 em segundos.
        duration_sector_3: Tempo do setor 3 em segundos.
        i1_speed: Velocidade (km/h) no ponto de medição 1.
        i2_speed: Velocidade (km/h) no ponto de medição 2.
        st_speed: Velocidade (km/h) na reta principal.
        is_pit_out_lap: Indica se é a volta de saída dos pits.
        date_start: Data e hora de início da volta (ISO 8601).
        session_key: Sessão à qual a volta pertence.
    """

    driver_number: int
    lap_number: int
    lap_duration: float | None = None
    duration_sector_1: float | None = None
    duration_sector_2: float | None = None
    duration_sector_3: float | None = None
    i1_speed: int | None = None
    i2_speed: int | None = None
    st_speed: int | None = None
    is_pit_out_lap: bool = False
    date_start: str | None = None
    session_key: int
