from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

PAYLOAD_FILE = ROOT / "data" / "payload" / "text.txt"

IMAGE_DIR = (
    ROOT
    / "data"
    / "images"
    / "exp07"
)

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
    / "exp07_container_content_sensitivity"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
DIFF_DIR = RESULTS_DIR / "difference_maps"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"


CONTAINERS = {
    "smooth_light": IMAGE_DIR / "01_smooth_light.png",
    "smooth_dark": IMAGE_DIR / "02_smooth_dark.png",
    "texture_nature": IMAGE_DIR / "03_texture_nature.png",
    "photo_mixed": IMAGE_DIR / "04_photo_mixed.png",
    "graphics": IMAGE_DIR / "05_graphics.png",
}


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