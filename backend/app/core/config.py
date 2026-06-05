from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_password: str
    secret_key: str
    database_url: str
    algorithm: str = "HS256"
    access_token_expire_hours: int = 24

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
