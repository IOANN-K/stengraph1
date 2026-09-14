import csv

import matplotlib.pyplot as plt
import numpy as np
from stengraph.io.csv_utils import load_csv_rows

from exp07_config import (
    METRICS_DIR,
    PLOTS_DIR,
)


METHODS = [
    "sequential",
    "random",
    "adaptive",
]


def load_results():
    return load_csv_rows(METRICS_DIR / "results.csv")


def containers_from_rows(rows):
    result = []

    for row in rows:
        name = row["container"]

        if name not in result:
            result.append(name)

    return result


def get_value(
    rows,
    container,
    method,
    metric,
):
    for row in rows:
        if (
            row["container"] == container
            and row["method"] == method
        ):
            return float(
                row[metric]
            )

    raise ValueError(
        f"Missing {container}/{method}/{metric}"
    )


def plot_grouped(
    rows,
    metric,
    ylabel,
    filename,
):
    containers = containers_from_rows(
        rows
    )

    x = np.arange(
        len(containers)
    )

    width = 0.25

    plt.figure(
        figsize=(10, 6)
    )

    offsets = [
        -width,
        0,
        width,
    ]

    for offset, method in zip(
        offsets,
        METHODS,
    ):
        values = [
            get_value(
                rows,
                container,
                method,
                metric,
            )
            for container in containers
        ]

        plt.bar(
            x + offset,
            values,
            width,
            label=method,
        )

    plt.xticks(
        x,
        containers,
        rotation=20,
        ha="right",
    )

    plt.ylabel(ylabel)
    plt.title(
        f"Container Type vs {ylabel}"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        PLOTS_DIR / filename,
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

    plot_grouped(
        rows,
        "psnr",
        "PSNR (dB)",
        "container_vs_psnr.png",
    )

    plot_grouped(
        rows,
        "ssim_loss",
        "SSIM loss",
        "container_vs_ssim_loss.png",
    )

    plot_grouped(
        rows,
        "changed_pixels_percent",
        "Changed pixels (%)",
        "container_vs_changed_pixels.png",
    )

    print("Plots created.")


if __name__ == "__main__":
    main()
