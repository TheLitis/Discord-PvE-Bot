from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN: str = getenv("DISCORD_TOKEN")
    DATABASE_URL: str = getenv("DATABASE_URL")
    LOG_LEVEL: str = getenv("LOG_LEVEL", "INFO")