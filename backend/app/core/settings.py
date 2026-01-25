from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "SGI Chatbot"
    ENV: str = "dev"

    AWS_DEFAULT_REGION: str = "ca-central-1"
    BEDROCK_KNOWLEDGE_BASE_ID: str
    
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4.1"

    DEFAULT_TOP_K: int = Field(default=4, ge=1, le=20)

settings = Settings()
