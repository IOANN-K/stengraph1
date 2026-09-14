import csv

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from exp14_config import (
    CONTAINERS,
    DATASET_CSV,
    METHODS,
    RESULTS_CSV,
    SUMMARY_CSV,
    ensure_directories,
)


FEATURES = [
    "mean_r_m",
    "mean_s_m",
    "mean_r_neg_m",
    "mean_s_neg_m",
    "gap_m",
    "gap_neg_m",
    "gap_ratio",
    "r_difference",
    "s_difference",
    "r_gap_m",
    "g_gap_m",
    "b_gap_m",
    "r_gap_neg_m",
    "g_gap_neg_m",
    "b_gap_neg_m",
]


def load_dataset():
    with open(
        DATASET_CSV,
        encoding="utf-8",
    ) as file:
        return list(
            csv.DictReader(file)
        )


def to_x(rows):
    return np.array(
        [
            [
                float(row[feature])
                for feature in FEATURES
            ]
            for row in rows
        ],
        dtype=np.float64,
    )


def to_y(rows):
    return np.array(
        [
            float(row["rate"])
            for row in rows
        ],
        dtype=np.float64,
    )


def create_models():
    return {
        "ridge": make_pipeline(
            StandardScaler(),
            Ridge(
                alpha=1.0,
            ),
        ),

        "random_forest": (
            RandomForestRegressor(
                n_estimators=500,
                max_depth=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
            )
        ),
    }


def run():
    ensure_directories()

    rows = load_dataset()

    results = []

    print("Experiment 14")
    print(
        "Leave-one-container-out RS estimation"
    )
    print()

    for method in METHODS:
        print(
            f"######## {method.upper()} ########"
        )
        print()

        method_rows = [
            row
            for row in rows
            if row["method"] == method
        ]

        for test_container in CONTAINERS:
            train_rows = [
                row
                for row in method_rows
                if (
                    row["container"]
                    != test_container
                )
            ]

            test_rows = [
                row
                for row in method_rows
                if (
                    row["container"]
                    == test_container
                )
            ]

            x_train = to_x(
                train_rows
            )

            y_train = to_y(
                train_rows
            )

            x_test = to_x(
                test_rows
            )

            y_test = to_y(
                test_rows
            )

            print(
                f"===== TEST "
                f"{test_container} ====="
            )

            models = create_models()

            for (
                model_name,
                model,
            ) in models.items():

                model.fit(
                    x_train,
                    y_train,
                )

                predictions = model.predict(
                    x_test
                )

                predictions = np.clip(
                    predictions,
                    0.0,
                    100.0,
                )

                errors = np.abs(
                    predictions
                    - y_test
                )

                fold_mae = float(
                    np.mean(errors)
                )

                print(
                    f"{model_name:<14} "
                    f"MAE={fold_mae:.2f} pp"
                )

                for (
                    row,
                    true_rate,
                    prediction,
                    error,
                ) in zip(
                    test_rows,
                    y_test,
                    predictions,
                    errors,
                ):
                    results.append(
                        {
                            "method": method,
                            "model": model_name,
                            "test_container": (
                                test_container
                            ),
                            "true_rate": (
                                float(
                                    true_rate
                                )
                            ),
                            "estimated_rate": (
                                float(
                                    prediction
                                )
                            ),
                            "absolute_error": (
                                float(
                                    error
                                )
                            ),
                        }
                    )

                    print(
                        f"  true="
                        f"{true_rate:5.1f}% "
                        f"est="
                        f"{prediction:6.2f}% "
                        f"err="
                        f"{error:5.2f}"
                    )

            print()

    with open(
        RESULTS_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        fieldnames = [
            "method",
            "model",
            "test_container",
            "true_rate",
            "estimated_rate",
            "absolute_error",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    summary = []

    print(
        "===== GLOBAL SUMMARY ====="
    )

    for method in METHODS:
        for model_name in (
            "ridge",
            "random_forest",
        ):
            subset = [
                row
                for row in results
                if (
                    row["method"] == method
                    and row["model"]
                    == model_name
                )
            ]

            errors = np.array(
                [
                    row["absolute_error"]
                    for row in subset
                ]
            )

            mae = float(
                np.mean(errors)
            )

            median = float(
                np.median(errors)
            )

            maximum = float(
                np.max(errors)
            )

            summary.append(
                {
                    "method": method,
                    "model": model_name,
                    "mae": mae,
                    "median_absolute_error": (
                        median
                    ),
                    "max_absolute_error": (
                        maximum
                    ),
                }
            )

            print(
                f"{method:<10} "
                f"{model_name:<14} "
                f"MAE={mae:6.2f} pp | "
                f"median={median:6.2f} | "
                f"max={maximum:6.2f}"
            )

    with open(
        SUMMARY_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "method",
                "model",
                "mae",
                "median_absolute_error",
                "max_absolute_error",
            ],
        )

        writer.writeheader()
        writer.writerows(
            summary
        )

    print()
    print(
        f"Results: {RESULTS_CSV}"
    )

    print(
        f"Summary: {SUMMARY_CSV}"
    )


if __name__ == "__main__":
    run()