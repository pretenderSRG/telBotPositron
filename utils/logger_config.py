import logging
import sys


def setup_logging():
    sys.stdout.reconfigure(encoding="utf-8")
    logging.basicConfig(level=logging.INFO,
                        # filename=settings.LOG_PATH,
                        stream=sys.stdout,
                        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
                        filemode="w", encoding="utf-8"
                        )
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)