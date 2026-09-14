import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp08_config import (
    METRICS_DIR,
    PLOTS_DIR,
    TEXTURE_METRICS,
)


def load_results():
    return load_csv_rows(METRICS_DIR / "results.csv")


def plot_metric(
    rows,
    metric,
    ylabel,
    filename,
):
    plt.figure()

    for texture_metric in TEXTURE_METRICS:
        subset = [
            row
            for row in rows
            if (
                row["texture_metric"]
                == texture_metric
            )
        ]

        subset.sort(
            key=lambda row: int(
                row["window_size"]
            )
        )

        x = [
            int(
                row["window_size"]
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
            label=texture_metric,
        )

    plt.xlabel(
        "Window size"
    )

    plt.ylabel(
        ylabel
    )

    plt.xticks(
        [3, 5, 7, 9]
    )

    plt.title(
        f"Adaptive Parameters vs {ylabel}"
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
        "ssim_loss",
        "SSIM loss",
        "window_vs_ssim_loss.png",
    )

    plot_metric(
        rows,
        "psnr",
        "PSNR (dB)",
        "window_vs_psnr.png",
    )

    plot_metric(
        rows,
        "mse",
        "MSE",
        "window_vs_mse.png",
    )

    print("Plots created.")


if __name__ == "__main__":
    main()
