from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    ZIP_CODE: int
    IFTTT_EVENT_NAME: str
    IFTTT_WEBHOOK_KEY: str

settings = Settings()