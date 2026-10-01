import logging
import sys

from config import settings


def setup_logging():
    sys.stdout.reconfigure(encoding="utf-8")

    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(filename=settings.LOG_PATH, mode="w", encoding="utf-8")

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
                        handlers=[stream_handler, file_handler],
                        )

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)