from pathlib import Path


def repository_root() -> Path:
    """Повернути корінь репозиторію для редагованої/початкової копії."""
    return Path(__file__).resolve().parents[2]


ROOT = repository_root()
DATA_DIR = ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"
PAYLOAD_DIR = DATA_DIR / "payload"
CANONICAL_PAYLOAD = PAYLOAD_DIR / "text.txt"
EXPERIMENTS_DIR = ROOT / "experiments" / "standard"


def experiment_dir(name: str) -> Path:
    return EXPERIMENTS_DIR / name


def ensure_directories(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
