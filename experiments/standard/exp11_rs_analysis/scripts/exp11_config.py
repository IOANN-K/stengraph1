from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

COVER_IMAGE = (
    ROOT
    / "data"
    / "images"
    / "input2.png"
)

EXP09A_IMAGES = (
    ROOT
    / "experiments"
    / "standard"
    / "exp09a_capacity_limits"
    / "results"
    / "images"
)

EXPERIMENT_DIR = (
    ROOT
    / "experiments"
    / "standard"
    / "exp11_rs_analysis"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

CAPACITIES = [
    10,
    25,
    50,
    75,
    90,
    100,
]

METHODS = [
    "sequential",
    "random",
    "adaptive",
]

MASK = [1, 0, 1, 0]


def ensure_directories():
    for directory in (
        METRICS_DIR,
        PLOTS_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )