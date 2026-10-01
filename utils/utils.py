from pathlib import Path

RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"


def image_path(filename: str) -> str:
    path = RESOURCES_DIR / "images" / f"{filename}.jpg"

    if not path.exists():
        raise FileNotFoundError(f"Такого зображення немає {path}")
    return path


def load_message(filename):
    path = RESOURCES_DIR / "messages" / f"{filename}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Такого файлу не існує {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_prompt(filename):
    path = RESOURCES_DIR / "prompts" / f"{filename}.txt"
    if not path.exists():
        raise RuntimeError(f"Такого файлу не існує {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
