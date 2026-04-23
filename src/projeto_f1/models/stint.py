"""Modelo Pydantic para stints (períodos de corrida por pneu) da OpenF1 API."""

from pydantic import BaseModel


class Stint(BaseModel):
    """Representa um período de corrida com o mesmo conjunto de pneus.

    Args:
        driver_number: Número de corrida do piloto.
        stint_number: Número sequencial do stint na corrida.
        lap_start: Volta de início do stint.
        lap_end: Volta de término do stint.
        compound: Composto do pneu (SOFT, MEDIUM, HARD, INTERMEDIATE, WET).
        tyre_age_at_start: Idade do pneu em voltas no início do stint.
        session_key: Sessão à qual o stint pertence.
    """

    driver_number: int
    stint_number: int | None = None
    lap_start: int | None = None
    lap_end: int | None = None
    compound: str | None = None
    tyre_age_at_start: int | None = None
    session_key: int
