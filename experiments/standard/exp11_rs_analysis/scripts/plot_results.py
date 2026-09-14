import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp11_config import (
    METRICS_DIR,
    METHODS,
    PLOTS_DIR,
)


def load_rows():
    return load_csv_rows(METRICS_DIR / "results.csv")


def get_cover_value(
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
                row[
                    "capacity_percent"
                ]
            )
        )

        x = [
            int(
                row[
                    "capacity_percent"
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

    cover = get_cover_value(
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


def plot_rs_curves(
    rows,
    method,
):
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
            row[
                "capacity_percent"
            ]
        )
    )

    x = [
        0
    ] + [
        int(
            row[
                "capacity_percent"
            ]
        )
        for row in subset
    ]

    cover = next(
        row
        for row in rows
        if row["image_type"] == "cover"
    )

    metrics = {
        "R_m": "mean_r_m_ratio",
        "S_m": "mean_s_m_ratio",
        "R_-m": "mean_r_neg_m_ratio",
        "S_-m": "mean_s_neg_m_ratio",
    }

    plt.figure(
        figsize=(9, 6)
    )

    for label, metric in metrics.items():
        y = [
            float(
                cover[metric]
            )
        ]

        y.extend(
            float(
                row[metric]
            )
            for row in subset
        )

        plt.plot(
            x,
            y,
            marker="o",
            label=label,
        )

    plt.xlabel(
        "Capacity used (%)"
    )

    plt.ylabel(
        "Group ratio"
    )

    plt.title(
        f"RS curves — {method}"
    )

    plt.legend()
    plt.grid(True)

    plt.savefig(
        PLOTS_DIR
        / f"rs_curves_{method}.png",
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
        "mean_rs_gap_m",
        "R_m - S_m",
        "capacity_vs_rs_gap_m.png",
    )

    plot_metric(
        rows,
        "mean_rs_gap_neg_m",
        "R_-m - S_-m",
        "capacity_vs_rs_gap_negative.png",
    )

    for method in METHODS:
        plot_rs_curves(
            rows,
            method,
        )

    print(
        "Plots created."
    )


if __name__ == "__main__":
    main()
