from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

IMAGE_DIR = (
    ROOT
    / "data"
    / "images"
    / "exp07"
)

CONTAINERS = {
    "smooth_light": IMAGE_DIR / "01_smooth_light.png",
    "smooth_dark": IMAGE_DIR / "02_smooth_dark.png",
    "texture_nature": IMAGE_DIR / "03_texture_nature.png",
    "photo_mixed": IMAGE_DIR / "04_photo_mixed.png",
    "graphics": IMAGE_DIR / "05_graphics.png",
}

EXP06_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp06_lsb_depth_study"
    / "scripts"
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

EXP12_SCRIPTS = (
    ROOT
    / "experiments"
    / "standard"
    / "exp12_rs_embedding_rate_estimation"
    / "scripts"
)

EXPERIMENT_DIR = (
    ROOT
    / "experiments"
    / "standard"
    / "exp13_rs_generalization"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

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

RANDOM_KEY = "stengraph-exp13"


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