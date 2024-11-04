from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    project_title: str
    backend_port: int
    is_reload: bool
    database_url: str

    class Config:
        env_path = ".env"


@lru_cache()
def get_config():
    return Config()
