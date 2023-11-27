from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Quokka"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "poi"
    device: str = "cpu"


settings = Settings()
