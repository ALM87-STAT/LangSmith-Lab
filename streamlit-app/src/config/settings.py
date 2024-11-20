# src/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_URL = os.getenv("API_URL")
    OPIK_LOCAL_URL = os.getenv("OPIK_LOCAL_URL")

    DEFAULT_CONTEXT = """
    Contexto...
    """

    DEFAULT_REQUIREMENTS = "Crea..."
