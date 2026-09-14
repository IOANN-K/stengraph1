import csv

import matplotlib.pyplot as plt
import numpy as np
from stengraph.io.csv_utils import load_csv_rows

from exp05_config import (
    METRICS_DIR,
    PLOTS_DIR,
)


METHODS = [
    "sequential",
    "random",
    "adaptive",
]

TRANSFORMATIONS = [
    "none",
    "resave",
    "optimize",
    "resize",
    "crop",
    "jpeg_roundtrip",
]


def load_results():
    return load_csv_rows(METRICS_DIR / "results.csv")


def get_success(
    rows,
    method,
    transformation,
):
    for row in rows:
        if (
            row["method"] == method
            and row["transformation"]
            == transformation
        ):
            return (
                row["decode_success"]
                == "True"
            )

    raise ValueError(
        f"Missing result: "
        f"{method}/{transformation}"
    )


def plot_success_matrix(rows):
    matrix = np.zeros(
        (
            len(METHODS),
            len(TRANSFORMATIONS),
        )
    )

    for y, method in enumerate(
        METHODS
    ):
        for x, transformation in enumerate(
            TRANSFORMATIONS
        ):
            matrix[y, x] = (
                1
                if get_success(
                    rows,
                    method,
                    transformation,
                )
                else 0
            )

    fig, ax = plt.subplots()

    image = ax.imshow(
        matrix,
        vmin=0,
        vmax=1,
    )

    ax.set_xticks(
        range(len(TRANSFORMATIONS))
    )

    ax.set_xticklabels(
        TRANSFORMATIONS,
        rotation=25,
        ha="right",
    )

    ax.set_yticks(
        range(len(METHODS))
    )

    ax.set_yticklabels(
        METHODS
    )

    for y in range(len(METHODS)):
        for x in range(
            len(TRANSFORMATIONS)
        ):
            text = (
                "PASS"
                if matrix[y, x] == 1
                else "FAIL"
            )

            ax.text(
                x,
                y,
                text,
                ha="center",
                va="center",
            )

    ax.set_title(
        "Payload Recovery After Image Transformations"
    )

    plt.tight_layout()

    plt.savefig(
        PLOTS_DIR
        / "robustness_matrix.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()


def main():
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = load_results()

    plot_success_matrix(rows)

    print("Plots created.")


if __name__ == "__main__":
    main()
