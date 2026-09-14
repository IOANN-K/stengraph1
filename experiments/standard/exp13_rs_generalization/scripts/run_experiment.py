import csv

from exp13_config import (
    CONTAINERS,
    EXP11_METRICS,
    IMAGES_DIR,
    MASK,
    METHODS,
    METRICS_DIR,
    TEST_RATES,
    ensure_directories,
)


from stengraph.steganalysis.rs import (
    analyze_image,
)


from stengraph.estimation.rs_rate import (
    estimate_rate,
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

        calibration[method].append(
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

    print("Experiment 13")
    print(
        "RS estimator generalization"
    )
    print()

    for container_name in CONTAINERS:
        print(
            f"===== {container_name.upper()} ====="
        )

        for rate in TEST_RATES:
            for method in METHODS:
                path = (
                    IMAGES_DIR
                    / (
                        f"{container_name}_"
                        f"{rate:03d}_"
                        f"{method}.png"
                    )
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

                error = abs(
                    estimated - rate
                )

                results.append(
                    {
                        "container": container_name,
                        "method": method,
                        "true_rate": rate,
                        "estimated_rate": estimated,
                        "absolute_error": error,
                        "rs_gap": gap,
                    }
                )

                print(
                    f"{rate:3d}% "
                    f"{method:<10} | "
                    f"est={estimated:6.2f}% | "
                    f"err={error:5.2f} pp"
                )

        print()

    output = (
        METRICS_DIR
        / "results.csv"
    )

    fieldnames = [
        "container",
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
        "===== SUMMARY ====="
    )

    for method in METHODS:
        errors = [
            row["absolute_error"]
            for row in results
            if row["method"] == method
        ]

        mae = (
            sum(errors)
            / len(errors)
        )

        print(
            f"{method:<10} "
            f"global MAE = {mae:.2f} pp"
        )

    print()

    for container in CONTAINERS:
        errors = [
            row["absolute_error"]
            for row in results
            if row["container"] == container
        ]

        mae = (
            sum(errors)
            / len(errors)
        )

        print(
            f"{container:<16} "
            f"MAE = {mae:.2f} pp"
        )

    print()
    print(
        f"Results: {output}"
    )


if __name__ == "__main__":
    run()
