import logging
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_KEY: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file='.env',
        encoding='utf-8'
    )


settings = Settings()

log_format = (
    '%(levelname)s - %(asctime)s - %(name)s: '
    '%(lineno)d - %(funcName)s: %(message)s'
)

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    stream=sys.stdout
)
