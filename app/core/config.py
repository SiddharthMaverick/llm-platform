from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    ollama_host: str
    model_name: str

    class Config:
        env_file = ".env"


settings = Settings()