import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp04_config import (
    METRICS_DIR,
    PLOTS_DIR,
)


METHODS = [
    "sequential",
    "random",
    "adaptive",
]

VARIANTS = [
    "raw",
    "encrypted",
    "compressed",
    "compressed_encrypted",
]


def load_results():
    return load_csv_rows(METRICS_DIR / "results.csv")


def get_value(
    rows,
    method,
    variant,
    metric,
):
    for row in rows:
        if (
            row["method"] == method
            and row["variant"] == variant
        ):
            return float(row[metric])

    raise ValueError(
        f"Missing {method}/{variant}/{metric}"
    )


def plot_metric(
    rows,
    metric,
    ylabel,
    filename,
):
    x = list(range(len(METHODS)))

    width = 0.18

    plt.figure()

    offsets = [
        -1.5,
        -0.5,
        0.5,
        1.5,
    ]

    for offset, variant in zip(
        offsets,
        VARIANTS,
    ):
        values = [
            get_value(
                rows,
                method,
                variant,
                metric,
            )
            for method in METHODS
        ]

        positions = [
            value + offset * width
            for value in x
        ]

        plt.bar(
            positions,
            values,
            width,
            label=variant,
        )

    plt.xticks(
        x,
        METHODS,
    )

    plt.ylabel(ylabel)
    plt.title(ylabel)
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


def plot_payload_sizes(rows):
    row_method = "adaptive"

    values = [
        get_value(
            rows,
            row_method,
            variant,
            "embedded_payload_bytes",
        )
        for variant in VARIANTS
    ]

    plt.figure()

    plt.bar(
        VARIANTS,
        values,
    )

    plt.ylabel("Bytes")
    plt.title("Embedded Payload Size")
    plt.xticks(
        rotation=15,
    )

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.savefig(
        PLOTS_DIR / "payload_sizes.png",
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

    plot_payload_sizes(rows)

    plot_metric(
        rows,
        "psnr",
        "PSNR (dB)",
        "psnr.png",
    )

    plot_metric(
        rows,
        "ssim_loss",
        "SSIM loss",
        "ssim_loss.png",
    )

    plot_metric(
        rows,
        "changed_pixels_percent",
        "Changed pixels (%)",
        "changed_pixels.png",
    )

    plot_metric(
        rows,
        "changed_channels_percent",
        "Changed channels (%)",
        "changed_channels.png",
    )

    print("Plots created.")


if __name__ == "__main__":
    main()
