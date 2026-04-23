"""Ingestão de dados de pilotos da OpenF1 API."""

import logging

from projeto_f1.ingestion.client import OpenF1Client
from projeto_f1.models import Driver

logger = logging.getLogger(__name__)


def buscar_pilotos(
    session_key: int,
    driver_number: int | None = None,
    client: OpenF1Client | None = None,
) -> list[Driver]:
    """Busca dados de pilotos de uma sessão na OpenF1 API.

    Args:
        session_key: Identificador da sessão.
        driver_number: Número do piloto para filtrar. Se None, retorna todos.
        client: Instância do cliente HTTP. Cria um novo se não informado.

    Returns:
        Lista de objetos Driver com os dados retornados.
    """
    api = client or OpenF1Client()
    params: dict = {"session_key": session_key}
    if driver_number is not None:
        params["driver_number"] = driver_number

    dados = api.get("/drivers", params=params)
    pilotos = [Driver(**item) for item in dados]
    logger.info("Pilotos recuperados: %d (session=%d)", len(pilotos), session_key)
    return pilotos
