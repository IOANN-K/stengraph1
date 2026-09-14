from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

EXP10_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp10_basic_steganalysis"
    / "scripts"
)

EXP11_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp11_rs_analysis"
    / "scripts"
)

EXP13_IMAGES = (
    ROOT
    / "experiments"
    / "standard"
    / "exp13_rs_generalization"
    / "results"
    / "images"
)

EXPERIMENT_DIR = (
    ROOT
    / "experiments"
    / "standard"
    / "exp15_hybrid_steganalysis"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

DATASET_CSV = METRICS_DIR / "dataset.csv"
RESULTS_CSV = METRICS_DIR / "results.csv"
SUMMARY_CSV = METRICS_DIR / "summary.csv"

CONTAINERS = [
    "smooth_light",
    "smooth_dark",
    "texture_nature",
    "photo_mixed",
    "graphics",
]

METHODS = [
    "sequential",
    "random",
    "adaptive",
]

RATES = [
    15,
    35,
    60,
    85,
]

MASK = [1, 0, 1, 0]


def ensure_directories():
    METRICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )