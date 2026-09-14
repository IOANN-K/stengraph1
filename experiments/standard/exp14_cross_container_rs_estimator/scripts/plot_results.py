import csv

import matplotlib.pyplot as plt
import numpy as np
from stengraph.io.csv_utils import load_csv_rows

from exp14_config import (
    CONTAINERS,
    METHODS,
    PLOTS_DIR,
    RESULTS_CSV,
)


MODELS = [
    "ridge",
    "random_forest",
]


def load_rows():
    return load_csv_rows(RESULTS_CSV)


def plot_true_vs_estimated(
    rows,
    method,
    model,
):
    subset = [
        row
        for row in rows
        if (
            row["method"] == method
            and row["model"] == model
        )
    ]

    plt.figure(
        figsize=(8, 7)
    )

    for container in CONTAINERS:
        group = [
            row
            for row in subset
            if (
                row["test_container"]
                == container
            )
        ]

        group.sort(
            key=lambda row: float(
                row["true_rate"]
            )
        )

        x = [
            float(
                row["true_rate"]
            )
            for row in group
        ]

        y = [
            float(
                row["estimated_rate"]
            )
            for row in group
        ]

        plt.plot(
            x,
            y,
            marker="o",
            label=container,
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
        f"{method} — {model}"
    )

    plt.legend()
    plt.grid(True)

    plt.savefig(
        PLOTS_DIR
        / (
            f"true_vs_estimated_"
            f"{method}_"
            f"{model}.png"
        ),
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()


def plot_model_mae(rows):
    labels = []
    values = []

    for method in METHODS:
        for model in MODELS:
            subset = [
                float(
                    row["absolute_error"]
                )
                for row in rows
                if (
                    row["method"] == method
                    and row["model"]
                    == model
                )
            ]

            labels.append(
                f"{method}\n{model}"
            )

            values.append(
                np.mean(subset)
            )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        labels,
        values,
    )

    plt.ylabel(
        "MAE (percentage points)"
    )

    plt.title(
        "Cross-container estimation error"
    )

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        PLOTS_DIR
        / "global_mae.png",
        dpi=160,
        bbox_inches="tight",
    )

    plt.close()


def plot_container_mae(rows):
    labels = list(
        CONTAINERS
    )

    x = np.arange(
        len(labels)
    )

    width = 0.13

    plt.figure(
        figsize=(12, 7)
    )

    offset_index = 0

    for method in METHODS:
        for model in MODELS:
            values = []

            for container in labels:
                errors = [
                    float(
                        row[
                            "absolute_error"
                        ]
                    )
                    for row in rows
                    if (
                        row["method"]
                        == method
                        and row["model"]
                        == model
                        and row[
                            "test_container"
                        ]
                        == container
                    )
                ]

                values.append(
                    np.mean(errors)
                )

            offset = (
                offset_index
                - 2.5
            ) * width

            plt.bar(
                x + offset,
                values,
                width,
                label=(
                    f"{method}/"
                    f"{model}"
                ),
            )

            offset_index += 1

    plt.xticks(
        x,
        labels,
        rotation=20,
        ha="right",
    )

    plt.ylabel(
        "MAE (percentage points)"
    )

    plt.title(
        "Error by unseen container"
    )

    plt.legend()

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


def main():
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = load_rows()

    for method in METHODS:
        for model in MODELS:
            plot_true_vs_estimated(
                rows,
                method,
                model,
            )

    plot_model_mae(
        rows
    )

    plot_container_mae(
        rows
    )

    print(
        "Plots created."
    )


if __name__ == "__main__":
    main()
