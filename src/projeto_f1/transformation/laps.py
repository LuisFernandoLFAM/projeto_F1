"""Transformações e análises sobre dados de voltas."""

import logging

from projeto_f1.models import Lap

logger = logging.getLogger(__name__)


def filtrar_voltas_validas(voltas: list[Lap]) -> list[Lap]:
    """Remove voltas sem tempo registrado e voltas de saída dos pits.

    Args:
        voltas: Lista de voltas brutas da API.

    Returns:
        Lista filtrada contendo apenas voltas com tempo válido.
    """
    validas = [v for v in voltas if v.lap_duration is not None and not v.is_pit_out_lap]
    logger.debug("Voltas válidas: %d de %d", len(validas), len(voltas))
    return validas


def volta_mais_rapida(voltas: list[Lap]) -> Lap | None:
    """Retorna a volta mais rápida de uma lista.

    Args:
        voltas: Lista de voltas (preferencialmente já filtradas).

    Returns:
        O objeto Lap com o menor lap_duration, ou None se a lista for vazia.
    """
    validas = [v for v in voltas if v.lap_duration is not None]
    if not validas:
        logger.warning("Nenhuma volta válida para calcular a mais rápida.")
        return None
    return min(validas, key=lambda v: v.lap_duration)  # type: ignore[arg-type, return-value]


def voltas_por_piloto(voltas: list[Lap]) -> dict[int, list[Lap]]:
    """Agrupa voltas por número de piloto.

    Args:
        voltas: Lista de voltas de qualquer piloto.

    Returns:
        Dicionário mapeando driver_number -> lista de voltas.
    """
    resultado: dict[int, list[Lap]] = {}
    for volta in voltas:
        resultado.setdefault(volta.driver_number, []).append(volta)
    return resultado
