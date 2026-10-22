import os
from pathlib import Path
from dotenv import load_dotenv

# Encontra o .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    DB_USER = os.getenv("POSTGRES_USER", "marcos_gis")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "senha_agro_2026")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "monitoramento_territorial")

    @classmethod
    def get_db_url(cls) -> str:
        # Adicionado o +psycopg para mapear o driver explicitamente
            return f"postgresql+psycopg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

