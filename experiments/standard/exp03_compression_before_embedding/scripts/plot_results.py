import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp03_config import (
    METRICS_DIR,
    PLOTS_DIR,
)


def load_results():
    path = METRICS_DIR / "results.csv"
    return load_csv_rows(path)


def get_value(rows, method, compression, metric):
    for row in rows:
        if (
            row["method"] == method
            and row["compression"] == compression
        ):
            return float(row[metric])

    raise ValueError(
        f"Missing result: "
        f"{method}/{compression}/{metric}"
    )


def plot_raw_vs_zlib(
    rows,
    metric,
    ylabel,
    filename,
):
    methods = [
        "sequential",
        "random",
        "adaptive",
    ]

    raw_values = [
        get_value(
            rows,
            method,
            "raw",
            metric,
        )
        for method in methods
    ]

    zlib_values = [
        get_value(
            rows,
            method,
            "zlib",
            metric,
        )
        for method in methods
    ]

    x = list(range(len(methods)))

    width = 0.35

    plt.figure()

    plt.bar(
        [value - width / 2 for value in x],
        raw_values,
        width,
        label="raw",
    )

    plt.bar(
        [value + width / 2 for value in x],
        zlib_values,
        width,
        label="zlib",
    )

    plt.xticks(
        x,
        methods,
    )

    plt.ylabel(ylabel)
    plt.title(
        f"Raw vs Zlib — {ylabel}"
    )
    plt.legend()
    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.savefig(
        PLOTS_DIR / filename,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()


def plot_payload_size(rows):
    raw = float(
        rows[0][
            "original_payload_bytes"
        ]
    )

    compressed = float(
        rows[0][
            "embedded_payload_bytes"
        ]
    )

    for row in rows:
        if row["compression"] == "zlib":
            compressed = float(
                row[
                    "embedded_payload_bytes"
                ]
            )
            break

    plt.figure()

    plt.bar(
        ["raw", "zlib"],
        [raw, compressed],
    )

    plt.ylabel("Payload size (bytes)")
    plt.title(
        "Payload Size Before and After Compression"
    )

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.savefig(
        PLOTS_DIR / "payload_size.png",
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

    plot_payload_size(rows)

    plot_raw_vs_zlib(
        rows,
        "psnr",
        "PSNR (dB)",
        "raw_vs_zlib_psnr.png",
    )

    plot_raw_vs_zlib(
        rows,
        "ssim",
        "SSIM",
        "raw_vs_zlib_ssim.png",
    )

    plot_raw_vs_zlib(
        rows,
        "ssim_loss",
        "SSIM loss",
        "raw_vs_zlib_ssim_loss.png",
    )

    plot_raw_vs_zlib(
        rows,
        "mse",
        "MSE",
        "raw_vs_zlib_mse.png",
    )

    plot_raw_vs_zlib(
        rows,
        "changed_pixels_percent",
        "Changed pixels (%)",
        "raw_vs_zlib_changed_pixels.png",
    )

    plot_raw_vs_zlib(
        rows,
        "changed_channels_percent",
        "Changed channels (%)",
        "raw_vs_zlib_changed_channels.png",
    )

    print("Plots created.")


if __name__ == "__main__":
    main()
