import os

from dotenv import load_dotenv


load_dotenv()

class Settings:
    OPEN_API_KEY = os.getenv("OPEN_API_KEY")
    BOT_API_KEY = os.getenv("BOT_API_KEY")
    LOG_PATH = os.getenv("LOG_PATH")


settings = Settings()