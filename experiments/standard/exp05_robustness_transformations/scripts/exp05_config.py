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
    / "exp05_robustness_transformations"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"

BASELINE_DIR = RESULTS_DIR / "baseline"
TRANSFORMED_DIR = RESULTS_DIR / "transformed"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

KEY_FILE = METRICS_DIR / "experiment.key"


TRANSFORMATIONS = [
    "none",
    "resave",
    "optimize",
    "resize",
    "crop",
    "jpeg_roundtrip",
]


def ensure_directories():
    BASELINE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    METRICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for transformation in TRANSFORMATIONS:
        if transformation == "none":
            continue

        (
            TRANSFORMED_DIR
            / transformation
        ).mkdir(
            parents=True,
            exist_ok=True,
        )


def read_payload():
    return PAYLOAD_FILE.read_bytes()