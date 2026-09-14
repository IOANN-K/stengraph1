import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp02_config import (
    METRICS_DIR,
    PLOTS_DIR,
)


def load_results():
    path = METRICS_DIR / "results.csv"
    return load_csv_rows(path)


def group_by_method(rows):
    result = {}

    for row in rows:
        result.setdefault(
            row["method"],
            [],
        ).append(row)

    return result


def plot_metric(
    grouped,
    metric,
    ylabel,
    filename,
):
    plt.figure()

    for method, rows in grouped.items():
        rows = sorted(
            rows,
            key=lambda row: float(
                row["payload_percent"]
            ),
        )

        x = [
            float(row["payload_percent"])
            for row in rows
        ]

        y = [
            float(row[metric])
            for row in rows
        ]

        plt.plot(
            x,
            y,
            marker="o",
            label=method,
        )

    plt.xlabel("Payload size (%)")
    plt.ylabel(ylabel)
    plt.title(
        f"Payload Size vs {ylabel}"
    )
    plt.legend()
    plt.grid(True)

    output = PLOTS_DIR / filename

    plt.savefig(
        output,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()

def plot_ssim_loss(
    grouped,
    filename,
):
    plt.figure()

    for method, rows in grouped.items():
        rows = sorted(
            rows,
            key=lambda row: float(
                row["payload_percent"]
            ),
        )

        x = [
            float(row["payload_percent"])
            for row in rows
        ]

        y = [
            1.0 - float(row["ssim"])
            for row in rows
        ]

        plt.plot(
            x,
            y,
            marker="o",
            label=method,
        )

    plt.xlabel("Payload size (%)")
    plt.ylabel("SSIM loss (1 - SSIM)")
    plt.title("Payload Size vs SSIM Loss")
    plt.legend()
    plt.grid(True)

    output = PLOTS_DIR / filename

    plt.savefig(
        output,
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
    grouped = group_by_method(rows)

    plot_metric(
        grouped,
        "psnr",
        "PSNR (dB)",
        "payload_vs_psnr.png",
    )

    plot_metric(
        grouped,
        "ssim",
        "SSIM",
        "payload_vs_ssim.png",
    )
    
    plot_ssim_loss(
        grouped,
        "payload_vs_ssim_loss.png",
    )

    plot_metric(
        grouped,
        "changed_pixels_percent",
        "Changed pixels (%)",
        "payload_vs_changed_pixels.png",
    )

    plot_metric(
        grouped,
        "changed_channels_percent",
        "Changed channels (%)",
        "payload_vs_changed_channels.png",
    )

    plot_metric(
        grouped,
        "mse",
        "MSE",
        "payload_vs_mse.png",
    )

    print("Plots created.")


if __name__ == "__main__":
    main()
