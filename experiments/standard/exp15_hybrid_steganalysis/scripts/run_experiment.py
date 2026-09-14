import csv

import numpy as np
from sklearn.linear_model import (
    ElasticNet,
    Ridge,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from exp15_config import (
    CONTAINERS,
    DATASET_CSV,
    METHODS,
    RESULTS_CSV,
    SUMMARY_CSV,
    ensure_directories,
)


FEATURES = [
    "rs_r_m",
    "rs_s_m",
    "rs_r_neg_m",
    "rs_s_neg_m",
    "rs_gap_m",
    "rs_gap_neg_m",
    "rs_gap_ratio",
    "rs_r_gap",
    "rs_g_gap",
    "rs_b_gap",
    "lsb_one_ratio",
    "lsb_entropy",
    "chi_square_normalized",
    "spatial_agreement",
    "r_chi_square_normalized",
    "g_chi_square_normalized",
    "b_chi_square_normalized",
    "r_lsb_one_ratio",
    "g_lsb_one_ratio",
    "b_lsb_one_ratio",
]


def load_rows():
    with open(
        DATASET_CSV,
        encoding="utf-8",
    ) as file:
        return list(
            csv.DictReader(file)
        )


def matrix(rows):
    return np.array(
        [
            [
                float(row[name])
                for name in FEATURES
            ]
            for row in rows
        ],
        dtype=np.float64,
    )


def targets(rows):
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

        "elastic_net": make_pipeline(
            StandardScaler(),
            ElasticNet(
                alpha=0.1,
                l1_ratio=0.25,
                max_iter=10000,
                random_state=42,
            ),
        ),
    }


def run():
    ensure_directories()

    rows = load_rows()

    results = []

    print(
        "Experiment 15"
    )

    print(
        "Hybrid steganalysis features"
    )

    print()

    for method in METHODS:
        print(
            f"######## {method.upper()} ########"
        )

        method_rows = [
            row
            for row in rows
            if row["method"] == method
        ]

        for test_container in CONTAINERS:
            train = [
                row
                for row in method_rows
                if row["container"]
                != test_container
            ]

            test = [
                row
                for row in method_rows
                if row["container"]
                == test_container
            ]

            x_train = matrix(
                train
            )

            y_train = targets(
                train
            )

            x_test = matrix(
                test
            )

            y_test = targets(
                test
            )

            print(
                f"===== TEST "
                f"{test_container} ====="
            )

            for (
                model_name,
                model,
            ) in create_models().items():

                model.fit(
                    x_train,
                    y_train,
                )

                predictions = np.clip(
                    model.predict(
                        x_test
                    ),
                    0,
                    100,
                )

                errors = np.abs(
                    predictions
                    - y_test
                )

                print(
                    f"{model_name:<12} "
                    f"MAE="
                    f"{np.mean(errors):.2f} pp"
                )

                for (
                    row,
                    true,
                    prediction,
                    error,
                ) in zip(
                    test,
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
                            "true_rate": float(
                                true
                            ),
                            "estimated_rate": float(
                                prediction
                            ),
                            "absolute_error": float(
                                error
                            ),
                        }
                    )

            print()

    with open(
        RESULTS_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "method",
                "model",
                "test_container",
                "true_rate",
                "estimated_rate",
                "absolute_error",
            ],
        )

        writer.writeheader()
        writer.writerows(
            results
        )

    summary = []

    print(
        "===== GLOBAL SUMMARY ====="
    )

    for method in METHODS:
        for model_name in (
            "ridge",
            "elastic_net",
        ):
            errors = np.array(
                [
                    row[
                        "absolute_error"
                    ]
                    for row in results
                    if (
                        row["method"]
                        == method
                        and row["model"]
                        == model_name
                    )
                ]
            )

            row = {
                "method": method,
                "model": model_name,
                "mae": float(
                    np.mean(errors)
                ),
                "median_absolute_error": float(
                    np.median(errors)
                ),
                "max_absolute_error": float(
                    np.max(errors)
                ),
            }

            summary.append(
                row
            )

            print(
                f"{method:<10} "
                f"{model_name:<12} "
                f"MAE="
                f"{row['mae']:.2f} pp | "
                f"median="
                f"{row['median_absolute_error']:.2f} | "
                f"max="
                f"{row['max_absolute_error']:.2f}"
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


if __name__ == "__main__":
    run()