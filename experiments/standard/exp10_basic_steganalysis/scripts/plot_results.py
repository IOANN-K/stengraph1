import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp10_config import (
    METRICS_DIR,
    METHODS,
    PLOTS_DIR,
)


def load_rows():
    return load_csv_rows(METRICS_DIR / "results.csv")


def cover_value(
    rows,
    metric,
):
    for row in rows:
        if row["image_type"] == "cover":
            return float(
                row[metric]
            )

    raise ValueError(
        "Cover row missing"
    )


def plot_metric(
    rows,
    metric,
    ylabel,
    filename,
):
    plt.figure(
        figsize=(9, 6)
    )

    for method in METHODS:
        subset = [
            row
            for row in rows
            if (
                row["image_type"] == "stego"
                and row["method"] == method
            )
        ]

        subset.sort(
            key=lambda row: int(
                row["capacity_percent"]
            )
        )

        x = [
            int(
                row["capacity_percent"]
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

    cover = cover_value(
        rows,
        metric,
    )

    plt.axhline(
        cover,
        linestyle="--",
        label="cover",
    )

    plt.xlabel(
        "Capacity used (%)"
    )

    plt.ylabel(
        ylabel
    )

    plt.title(
        f"Capacity vs {ylabel}"
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

    rows = load_rows()

    plot_metric(
        rows,
        "pooled_lsb_one_ratio",
        "LSB one ratio",
        "capacity_vs_lsb_one_ratio.png",
    )

    plot_metric(
        rows,
        "pooled_lsb_entropy",
        "LSB entropy",
        "capacity_vs_lsb_entropy.png",
    )

    plot_metric(
        rows,
        "pooled_chi_square_normalized",
        "Chi-square / DOF",
        "capacity_vs_chi_square.png",
    )

    plot_metric(
        rows,
        "pooled_chi_square_p_value",
        "Chi-square p-value",
        "capacity_vs_chi_p_value.png",
    )

    plot_metric(
        rows,
        "mean_spatial_agreement",
        "Mean spatial LSB agreement",
        "capacity_vs_spatial_agreement.png",
    )

    print(
        "Plots created."
    )


if __name__ == "__main__":
    main()
