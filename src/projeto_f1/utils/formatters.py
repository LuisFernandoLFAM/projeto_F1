"""Funções utilitárias de formatação de dados de F1."""


def formatar_duracao(segundos: float | None) -> str:
    """Converte segundos em formato de tempo legível (M:SS.mmm).

    Args:
        segundos: Duração em segundos. Aceita None para voltas sem tempo.

    Returns:
        String formatada como '1:23.456' ou '–' se segundos for None.

    Examples:
        >>> formatar_duracao(83.456)
        '1:23.456'
        >>> formatar_duracao(None)
        '–'
    """
    if segundos is None:
        return "–"
    minutos = int(segundos) // 60
    resto = segundos - minutos * 60
    return f"{minutos}:{resto:06.3f}"


def formatar_velocidade(kmh: int | None) -> str:
    """Formata velocidade em km/h com unidade.

    Args:
        kmh: Velocidade em km/h. Aceita None para leituras ausentes.

    Returns:
        String formatada como '315 km/h' ou '–' se kmh for None.

    Examples:
        >>> formatar_velocidade(315)
        '315 km/h'
        >>> formatar_velocidade(None)
        '–'
    """
    if kmh is None:
        return "–"
    return f"{kmh} km/h"
