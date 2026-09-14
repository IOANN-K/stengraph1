import csv

import matplotlib.pyplot as plt
import numpy as np
from stengraph.io.csv_utils import load_csv_rows

from exp13_config import (
    CONTAINERS,
    METHODS,
    METRICS_DIR,
    PLOTS_DIR,
)


def load_rows():
    return load_csv_rows(METRICS_DIR / "results.csv")


def plot_container(
    rows,
    container,
):
    subset = [
        row
        for row in rows
        if row["container"] == container
    ]

    plt.figure(
        figsize=(8, 7)
    )

    for method in METHODS:
        method_rows = [
            row
            for row in subset
            if row["method"] == method
        ]

        method_rows.sort(
            key=lambda row: float(
                row["true_rate"]
            )
        )

        x = [
            float(
                row["true_rate"]
            )
            for row in method_rows
        ]

        y = [
            float(
                row["estimated_rate"]
            )
            for row in method_rows
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
        label="perfect",
    )

    plt.xlabel(
        "True embedding rate (%)"
    )

    plt.ylabel(
        "Estimated embedding rate (%)"
    )

    plt.title(
        f"RS Generalization — {container}"
    )

    plt.legend()
    plt.grid(True)

    plt.savefig(
        PLOTS_DIR
        / f"true_vs_estimated_{container}.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()


def plot_container_mae(
    rows,
):
    containers = list(
        CONTAINERS.keys()
    )

    values = []

    for container in containers:
        errors = [
            float(
                row["absolute_error"]
            )
            for row in rows
            if row["container"] == container
        ]

        values.append(
            sum(errors)
            / len(errors)
        )

    plt.figure(
        figsize=(9, 6)
    )

    plt.bar(
        containers,
        values,
    )

    plt.ylabel(
        "MAE (percentage points)"
    )

    plt.title(
        "RS Estimator Generalization Error"
    )

    plt.xticks(
        rotation=20,
        ha="right",
    )

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        PLOTS_DIR
        / "container_mae.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()


def plot_method_mae(
    rows,
):
    values = []

    for method in METHODS:
        errors = [
            float(
                row["absolute_error"]
            )
            for row in rows
            if row["method"] == method
        ]

        values.append(
            sum(errors)
            / len(errors)
        )

    x = np.arange(
        len(METHODS)
    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        x,
        values,
    )

    plt.xticks(
        x,
        METHODS,
    )

    plt.ylabel(
        "MAE (percentage points)"
    )

    plt.title(
        "Generalization Error by Method"
    )

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.savefig(
        PLOTS_DIR
        / "method_mae.png",
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

    for container in CONTAINERS:
        plot_container(
            rows,
            container,
        )

    plot_container_mae(
        rows
    )

    plot_method_mae(
        rows
    )

    print(
        "Plots created."
    )


if __name__ == "__main__":
    main()
