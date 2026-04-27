from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações centrais da aplicação.

    Mantém o projeto limpo, seguro e preparado para deploy.
    Em ambiente real, segredos devem ficar em vault, secrets manager
    ou solução corporativa equivalente.
    """

    app_name: str = "Data Naming AI"
    app_env: str = "local"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
