from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    exec_hour: str = Field(..., env='EXECUTION_HOUR')
    refresh_rate: int = Field(..., env='REFRESH_RATE')


settings = Settings()
