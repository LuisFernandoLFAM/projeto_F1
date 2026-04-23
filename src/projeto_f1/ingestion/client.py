"""Cliente HTTP para a OpenF1 API."""

import logging

import requests

from projeto_f1.config import settings

logger = logging.getLogger(__name__)


class OpenF1Client:
    """Cliente para consumir a OpenF1 API.

    Args:
        base_url: URL base da API. Usa o valor de settings se não informado.
        timeout: Timeout em segundos para as requisições.
    """

    def __init__(self, base_url: str | None = None, timeout: int | None = None) -> None:
        self.base_url = base_url or settings.openf1_base_url
        self.timeout = timeout or settings.request_timeout

    def get(self, endpoint: str, params: dict | None = None) -> list[dict]:
        """Executa uma requisição GET e retorna a lista de resultados.

        Args:
            endpoint: Caminho do endpoint (ex: '/sessions').
            params: Parâmetros de query opcionais.

        Returns:
            Lista de dicionários com os dados retornados pela API.

        Raises:
            requests.HTTPError: Se a resposta tiver status de erro.
            requests.ConnectionError: Se não for possível conectar à API.
        """
        url = f"{self.base_url}{endpoint}"
        logger.info("Requisição GET: %s params=%s", url, params)

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error("Erro HTTP ao chamar %s: %s", url, e)
            raise
        except requests.ConnectionError as e:
            logger.error("Erro de conexão ao chamar %s: %s", url, e)
            raise

        data = response.json()
        logger.debug("Recebidos %d registros de %s", len(data), endpoint)
        return data
