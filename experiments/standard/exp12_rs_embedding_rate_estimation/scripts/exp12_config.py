from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

INPUT_IMAGE = ROOT / "data" / "images" / "input2.png"

EXP06_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp06_lsb_depth_study"
    / "scripts"
)

EXP09A_METRICS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp09a_capacity_limits"
    / "results"
    / "metrics"
    / "results.csv"
)

EXP11_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp11_rs_analysis"
    / "scripts"
)

EXP11_METRICS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp11_rs_analysis"
    / "results"
    / "metrics"
    / "results.csv"
)

EXPERIMENT_DIR = (
    ROOT
    / "experiments"
    / "standard"
    / "exp12_rs_embedding_rate_estimation"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

TRAIN_RATES = [
    0,
    10,
    25,
    50,
    75,
    90,
    100,
]

TEST_RATES = [
    15,
    35,
    60,
    85,
]

METHODS = [
    "sequential",
    "random",
    "adaptive",
]

MASK = [1, 0, 1, 0]

RANDOM_KEY = "stengraph-exp12"


def ensure_directories():
    for directory in (
        IMAGES_DIR,
        METRICS_DIR,
        PLOTS_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )