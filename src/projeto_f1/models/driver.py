"""Modelo Pydantic para pilotos da OpenF1 API."""

from pydantic import BaseModel


class Driver(BaseModel):
    """Representa um piloto em uma sessão específica.

    Args:
        driver_number: Número de corrida do piloto (1–99).
        full_name: Nome completo do piloto.
        name_acronym: Sigla de três letras usada em transmissões.
        broadcast_name: Nome usado nas transmissões oficiais.
        team_name: Nome da equipe.
        team_colour: Cor hexadecimal da equipe (sem '#').
        headshot_url: URL da foto de perfil oficial.
        session_key: Sessão à qual o registro pertence.
    """

    driver_number: int
    full_name: str
    name_acronym: str
    broadcast_name: str | None = None
    team_name: str | None = None
    team_colour: str | None = None
    headshot_url: str | None = None
    session_key: int
