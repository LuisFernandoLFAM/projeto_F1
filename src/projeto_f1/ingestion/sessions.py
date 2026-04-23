"""Ingestão de sessões da OpenF1 API."""

import logging

from projeto_f1.ingestion.client import OpenF1Client
from projeto_f1.models import Session

logger = logging.getLogger(__name__)


def buscar_sessoes(
    ano: int | None = None,
    session_key: int | str | None = None,
    client: OpenF1Client | None = None,
) -> list[Session]:
    """Busca sessões de Fórmula 1 na OpenF1 API.

    Args:
        ano: Ano do campeonato para filtrar. Se None, retorna todas.
        session_key: Chave específica da sessão ou 'latest'.
        client: Instância do cliente HTTP. Cria um novo se não informado.

    Returns:
        Lista de objetos Session com os dados retornados.
    """
    api = client or OpenF1Client()
    params: dict = {}
    if ano is not None:
        params["year"] = ano
    if session_key is not None:
        params["session_key"] = session_key

    dados = api.get("/sessions", params=params)
    sessoes = [Session(**item) for item in dados]
    logger.info("Sessões recuperadas: %d", len(sessoes))
    return sessoes
