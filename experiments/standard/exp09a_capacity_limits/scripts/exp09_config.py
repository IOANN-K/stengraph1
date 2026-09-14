from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

INPUT_IMAGE = (
    ROOT
    / "data"
    / "images"
    / "input2.png"
)

EXP01_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp01_sequential_random_adaptive_1lsb"
    / "scripts"
)

EXP06_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp06_lsb_depth_study"
    / "scripts"
)

EXPERIMENT_DIR = Path(__file__).resolve().parents[1]

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
DIFF_DIR = RESULTS_DIR / "difference_maps"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

CAPACITY_FRACTIONS = [
    0.10,
    0.25,
    0.50,
    0.75,
    0.90,
    1.00,
]

RANDOM_KEY = "stengraph-exp09"


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
