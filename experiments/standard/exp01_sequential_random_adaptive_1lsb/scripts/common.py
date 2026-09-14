from pathlib import Path
import hashlib


ROOT = Path(__file__).resolve().parents[4]

INPUT_IMAGE = ROOT / "data" / "images" / "input2.png"
PAYLOAD_FILE = ROOT / "data" / "payload" / "text.txt"

EXPERIMENT_DIR = (
    ROOT
    / "experiments"
    / "standard"
    / "exp01_sequential_random_adaptive_1lsb"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
DIFF_DIR = RESULTS_DIR / "difference_maps"
METRICS_DIR = RESULTS_DIR / "metrics"


def ensure_directories():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)


def read_payload_bytes():
    return PAYLOAD_FILE.read_bytes()


def bytes_to_bits(data):
    return "".join(f"{byte:08b}" for byte in data)


def calculate_sha256(data):
    return hashlib.sha256(data).hexdigest()