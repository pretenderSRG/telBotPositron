import os

from dotenv import load_dotenv


load_dotenv()

class Config:
    OPEN_API_KEY = os.getenv("OPEN_API_KEY")
    BOT_API_KEY = os.getenv("BOT_API_KEY")


settings = Config()