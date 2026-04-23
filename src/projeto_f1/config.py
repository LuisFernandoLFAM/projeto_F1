"""Configurações centralizadas do projeto via variáveis de ambiente."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do arquivo .env."""

    openf1_base_url: str = "https://api.openf1.org/v1"
    output_dir: str = "data"
    request_timeout: int = 30
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
