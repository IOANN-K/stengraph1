from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

INPUT_IMAGE = ROOT / "data" / "images" / "input2.png"
PAYLOAD_FILE = ROOT / "data" / "payload" / "text.txt"

EXP01_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp01_sequential_random_adaptive_1lsb"
    / "scripts"
)

EXPERIMENT_DIR = (
    ROOT
    / "experiments"
    / "standard"
    / "exp03_compression_before_embedding"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
DIFF_DIR = RESULTS_DIR / "difference_maps"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"


def ensure_directories():
    for directory in (
        IMAGES_DIR,
        DIFF_DIR,
        METRICS_DIR,
        PLOTS_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


def read_payload():
    return PAYLOAD_FILE.read_bytes()