from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

INPUT_IMAGE = ROOT / "data" / "images" / "input2.png"
PAYLOAD_DIR = ROOT / "data" / "payload" / "literature"

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

EXPERIMENT_DIR = (
    ROOT
    / "experiments"
    / "standard"
    / "exp09b_literary_payloads"
)

RESULTS_DIR = EXPERIMENT_DIR / "results"
IMAGES_DIR = RESULTS_DIR / "images"
DIFF_DIR = RESULTS_DIR / "difference_maps"
METRICS_DIR = RESULTS_DIR / "metrics"
PLOTS_DIR = RESULTS_DIR / "plots"

PAYLOADS = {
    "alice": PAYLOAD_DIR / "alice.txt",
    "jekyll_hyde": PAYLOAD_DIR / "jekyll_hyde.txt",
    "frankenstein": PAYLOAD_DIR / "frankenstein.txt",
    "sherlock_holmes": PAYLOAD_DIR / "sherlock_holmes.txt",
    "moby_dick": PAYLOAD_DIR / "moby_dick.txt",
    "war_and_peace": PAYLOAD_DIR / "war_and_peace.txt",
}

RANDOM_KEY = "stengraph-exp09b"


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