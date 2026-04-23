"""Ingestão de dados de voltas da OpenF1 API."""

import logging

from projeto_f1.ingestion.client import OpenF1Client
from projeto_f1.models import Lap

logger = logging.getLogger(__name__)


def buscar_voltas(
    session_key: int,
    driver_number: int | None = None,
    client: OpenF1Client | None = None,
) -> list[Lap]:
    """Busca dados de voltas de uma sessão na OpenF1 API.

    Args:
        session_key: Identificador da sessão.
        driver_number: Número do piloto para filtrar. Se None, retorna todos.
        client: Instância do cliente HTTP. Cria um novo se não informado.

    Returns:
        Lista de objetos Lap com os dados retornados.
    """
    api = client or OpenF1Client()
    params: dict = {"session_key": session_key}
    if driver_number is not None:
        params["driver_number"] = driver_number

    dados = api.get("/laps", params=params)
    voltas = [Lap(**item) for item in dados]
    logger.info("Voltas recuperadas: %d (session=%d)", len(voltas), session_key)
    return voltas
