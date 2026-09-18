import os
from tkinter.font import names

from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPEN_API_KEY: str = os.getenv("OPEN_API_KEY")
    BOT_API_KEY: str = os.getenv("BOT_API_KEY")
    LOG_PATH: str = os.getenv("LOG_PATH")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    OPENAI_REASONING: str = os.getenv("OPENAI_REASONING", "none")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "600"))
    OPENAI_TIMEOUT: float = float(os.getenv("OPENAI_TIMEOUT", "30"))

    def validate(self):
        missing = [name for name in Settings.__annotations__.keys() if not getattr(self, name)]
        if missing:
            raise RuntimeError(f"У .env не заповнені: {','.join(missing)}."
                               f"Скопіюйте .env.example у .env і додайте токени")


settings = Settings()
