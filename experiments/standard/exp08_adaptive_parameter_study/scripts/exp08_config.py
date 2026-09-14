from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

INPUT_IMAGE = (
    ROOT
    / "data"
    / "images"
    / "exp07"
    / "03_texture_nature.png"
)

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
    / "exp08_adaptive_parameter_study"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
DIFF_DIR = RESULTS_DIR / "difference_maps"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

WINDOW_SIZES = [3, 5, 7, 9]

TEXTURE_METRICS = [
    "variance",
    "gradient",
    "laplacian",
]


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