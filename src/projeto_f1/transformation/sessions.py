"""Transformações e filtros sobre dados de sessões."""

import logging

from projeto_f1.models import Session

logger = logging.getLogger(__name__)


def filtrar_sessoes_por_tipo(sessoes: list[Session], tipo: str) -> list[Session]:
    """Filtra sessões pelo tipo informado.

    Args:
        sessoes: Lista de sessões brutas.
        tipo: Tipo desejado, ex: 'Race', 'Qualifying', 'Practice'.

    Returns:
        Lista de sessões cujo session_type corresponde ao tipo informado.
    """
    filtradas = [s for s in sessoes if s.session_type == tipo and not s.is_cancelled]
    logger.debug("Sessões do tipo '%s': %d de %d", tipo, len(filtradas), len(sessoes))
    return filtradas
