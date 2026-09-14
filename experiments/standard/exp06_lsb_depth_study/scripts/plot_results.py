import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp06_config import (
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
        method_rows = [
            row
            for row in rows
            if row["method"] == method
        ]

        method_rows.sort(
            key=lambda row: int(
                row["lsb_depth"]
            )
        )

        x = [
            int(row["lsb_depth"])
            for row in method_rows
        ]

        y = [
            float(row[metric])
            for row in method_rows
        ]

        plt.plot(
            x,
            y,
            marker="o",
            label=method,
        )

    plt.xlabel("LSB depth")
    plt.ylabel(ylabel)
    plt.title(
        f"LSB Depth vs {ylabel}"
    )

    plt.xticks(
        [1, 2, 3, 4]
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
        "lsb_vs_psnr.png",
    )

    plot_metric(
        rows,
        "ssim",
        "SSIM",
        "lsb_vs_ssim.png",
    )

    plot_metric(
        rows,
        "ssim_loss",
        "SSIM loss",
        "lsb_vs_ssim_loss.png",
    )

    plot_metric(
        rows,
        "mse",
        "MSE",
        "lsb_vs_mse.png",
    )

    plot_metric(
        rows,
        "changed_pixels_percent",
        "Changed pixels (%)",
        "lsb_vs_changed_pixels.png",
    )

    plot_metric(
        rows,
        "changed_channels_percent",
        "Changed channels (%)",
        "lsb_vs_changed_channels.png",
    )

    print("Plots created.")


if __name__ == "__main__":
    main()
