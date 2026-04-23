"""Modelo Pydantic para sessões da OpenF1 API."""

from pydantic import BaseModel


class Session(BaseModel):
    """Representa uma sessão de Fórmula 1 (treino, classificação, corrida).

    Args:
        session_key: Identificador único da sessão.
        session_name: Nome da sessão (ex: 'Race', 'Qualifying').
        session_type: Tipo da sessão (ex: 'Race', 'Practice').
        meeting_key: Identificador do GP/fim de semana.
        date_start: Data e hora de início (ISO 8601).
        date_end: Data e hora de término (ISO 8601).
        circuit_short_name: Abreviação do nome do circuito.
        country_name: Nome do país.
        is_cancelled: Indica se a sessão foi cancelada.
    """

    session_key: int
    session_name: str
    session_type: str
    meeting_key: int
    date_start: str
    date_end: str | None = None
    circuit_short_name: str | None = None
    country_name: str | None = None
    is_cancelled: bool = False
