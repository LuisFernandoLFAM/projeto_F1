"""Exportação de dados de modelos Pydantic para arquivos CSV."""

import csv
import logging
import os
from pathlib import Path

from pydantic import BaseModel

from projeto_f1.config import settings

logger = logging.getLogger(__name__)


def salvar_csv(registros: list[BaseModel], nome_arquivo: str, diretorio: str | None = None) -> Path:
    """Salva uma lista de modelos Pydantic em um arquivo CSV.

    Args:
        registros: Lista de objetos Pydantic a exportar.
        nome_arquivo: Nome do arquivo de saída (sem extensão ou com .csv).
        diretorio: Diretório de destino. Usa settings.output_dir se não informado.

    Returns:
        Caminho absoluto do arquivo gerado.

    Raises:
        ValueError: Se a lista de registros estiver vazia.
    """
    if not registros:
        raise ValueError("A lista de registros não pode ser vazia.")

    if not nome_arquivo.endswith(".csv"):
        nome_arquivo = f"{nome_arquivo}.csv"

    destino = Path(diretorio or settings.output_dir)
    os.makedirs(destino, exist_ok=True)
    caminho = destino / nome_arquivo

    campos = list(type(registros[0]).model_fields.keys())
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for registro in registros:
            writer.writerow(registro.model_dump())

    logger.info("CSV salvo: %s (%d registros)", caminho, len(registros))
    return caminho
