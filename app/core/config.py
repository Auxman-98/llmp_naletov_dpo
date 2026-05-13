from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    model_config: dict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_name: str

    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int

    sqlite_path: str

    openrouter_api_key: str
    openrouter_base_url: AnyHttpUrl
    openrouter_model: str
    openrouter_site_url: AnyHttpUrl
    openrouter_app_name: str


settings = Settings()
