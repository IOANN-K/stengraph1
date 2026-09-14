import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp12_config import (
    METHODS,
    METRICS_DIR,
    PLOTS_DIR,
)


def load_rows():
    return load_csv_rows(METRICS_DIR / "results.csv")


def main():
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = load_rows()

    plt.figure(
        figsize=(8, 7)
    )

    for method in METHODS:
        subset = [
            row
            for row in rows
            if row["method"] == method
        ]

        x = [
            float(row["true_rate"])
            for row in subset
        ]

        y = [
            float(row["estimated_rate"])
            for row in subset
        ]

        plt.plot(
            x,
            y,
            marker="o",
            label=method,
        )

    plt.plot(
        [0, 100],
        [0, 100],
        linestyle="--",
        label="perfect estimate",
    )

    plt.xlabel(
        "True embedding rate (%)"
    )

    plt.ylabel(
        "Estimated embedding rate (%)"
    )

    plt.title(
        "RS-based Embedding Rate Estimation"
    )

    plt.legend()
    plt.grid(True)

    plt.savefig(
        PLOTS_DIR
        / "true_vs_estimated.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()

    print(
        "Plots created."
    )


if __name__ == "__main__":
    main()
