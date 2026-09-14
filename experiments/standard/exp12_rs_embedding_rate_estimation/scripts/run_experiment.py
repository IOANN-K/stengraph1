import csv

from exp12_config import (
    EXP11_METRICS,
    IMAGES_DIR,
    MASK,
    METHODS,
    METRICS_DIR,
    TEST_RATES,
    ensure_directories,
)

from stengraph.estimation.rs_rate import (
    estimate_rate,
)


from stengraph.steganalysis.rs import (
    analyze_image,
)


def load_calibration():
    calibration = {
        method: []
        for method in METHODS
    }

    with open(
        EXP11_METRICS,
        encoding="utf-8",
    ) as file:
        rows = list(
            csv.DictReader(file)
        )

    cover = next(
        row
        for row in rows
        if row["image_type"] == "cover"
    )

    cover_gap = float(
        cover["mean_rs_gap_m"]
    )

    for method in METHODS:
        calibration[method].append(
            (
                0,
                cover_gap,
            )
        )

    for row in rows:
        if row["image_type"] != "stego":
            continue

        method = row["method"]

        if method not in calibration:
            continue

        calibration[
            method
        ].append(
            (
                int(
                    row[
                        "capacity_percent"
                    ]
                ),
                float(
                    row[
                        "mean_rs_gap_m"
                    ]
                ),
            )
        )

    return calibration


def run():
    ensure_directories()

    calibration = load_calibration()

    results = []

    print("Experiment 12")
    print(
        "RS embedding-rate estimation"
    )
    print()

    for rate in TEST_RATES:
        print(
            f"===== TRUE {rate}% ====="
        )

        for method in METHODS:
            path = (
                IMAGES_DIR
                / f"{rate:03d}_{method}.png"
            )

            metrics = analyze_image(
                path,
                MASK,
            )

            gap = metrics[
                "mean_rs_gap_m"
            ]

            estimated = estimate_rate(
                gap,
                calibration[method],
            )

            absolute_error = abs(
                estimated - rate
            )

            results.append(
                {
                    "method": method,
                    "true_rate": rate,
                    "estimated_rate": estimated,
                    "absolute_error": absolute_error,
                    "rs_gap": gap,
                }
            )

            print(
                f"{method:<10} | "
                f"gap={gap:.6f} | "
                f"estimated="
                f"{estimated:.2f}% | "
                f"error="
                f"{absolute_error:.2f} pp"
            )

        print()

    output = (
        METRICS_DIR
        / "results.csv"
    )

    fieldnames = [
        "method",
        "true_rate",
        "estimated_rate",
        "absolute_error",
        "rs_gap",
    ]

    with open(
        output,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(
            results
        )

    print(
        "Experiment completed."
    )

    for method in METHODS:
        errors = [
            row["absolute_error"]
            for row in results
            if row["method"] == method
        ]

        mae = sum(errors) / len(errors)

        print(
            f"{method:<10} "
            f"MAE = {mae:.2f} percentage points"
        )

    print(
        f"Results: {output}"
    )


if __name__ == "__main__":
    run()
