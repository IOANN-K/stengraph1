import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp09_config import (
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


def plot_metric(
    rows,
    metric,
    ylabel,
    filename,
):
    plt.figure()

    for method in METHODS:
        subset = [
            row
            for row in rows
            if row["method"] == method
        ]

        subset.sort(
            key=lambda row: float(
                row[
                    "capacity_actual_percent"
                ]
            )
        )

        x = [
            float(
                row[
                    "capacity_actual_percent"
                ]
            )
            for row in subset
        ]

        y = [
            float(
                row[metric]
            )
            for row in subset
        ]

        plt.plot(
            x,
            y,
            marker="o",
            label=method,
        )

    plt.xlabel(
        "Capacity used (%)"
    )

    plt.ylabel(
        ylabel
    )

    plt.title(
        f"Capacity Usage vs {ylabel}"
    )

    plt.legend()
    plt.grid(True)

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

    plot_metric(
        rows,
        "psnr",
        "PSNR (dB)",
        "capacity_vs_psnr.png",
    )

    plot_metric(
        rows,
        "ssim",
        "SSIM",
        "capacity_vs_ssim.png",
    )

    plot_metric(
        rows,
        "ssim_loss",
        "SSIM loss",
        "capacity_vs_ssim_loss.png",
    )

    plot_metric(
        rows,
        "mse",
        "MSE",
        "capacity_vs_mse.png",
    )

    plot_metric(
        rows,
        "changed_pixels_percent",
        "Changed pixels (%)",
        "capacity_vs_changed_pixels.png",
    )

    plot_metric(
        rows,
        "changed_channels_percent",
        "Changed channels (%)",
        "capacity_vs_changed_channels.png",
    )

    print(
        "Plots created."
    )


if __name__ == "__main__":
    main()
