import csv

from exp14_config import (
    CONTAINERS,
    DATASET_CSV,
    EXP13_IMAGES,
    MASK,
    METHODS,
    RATES,
    ensure_directories,
)


from stengraph.steganalysis.rs import analyze_image


def safe_ratio(a, b):
    if abs(b) < 1e-12:
        return 0.0

    return a / b


def extract_features(metrics):
    gap_m = metrics["mean_rs_gap_m"]
    gap_neg = metrics["mean_rs_gap_neg_m"]

    r_m = metrics["mean_r_m_ratio"]
    s_m = metrics["mean_s_m_ratio"]

    r_neg = metrics["mean_r_neg_m_ratio"]
    s_neg = metrics["mean_s_neg_m_ratio"]

    return {
        "mean_r_m": r_m,
        "mean_s_m": s_m,
        "mean_r_neg_m": r_neg,
        "mean_s_neg_m": s_neg,
        "gap_m": gap_m,
        "gap_neg_m": gap_neg,
        "gap_ratio": safe_ratio(
            gap_m,
            gap_neg,
        ),
        "r_difference": (
            r_m - r_neg
        ),
        "s_difference": (
            s_m - s_neg
        ),

        "r_gap_m": (
            metrics["r_rs_gap_m"]
        ),
        "g_gap_m": (
            metrics["g_rs_gap_m"]
        ),
        "b_gap_m": (
            metrics["b_rs_gap_m"]
        ),

        "r_gap_neg_m": (
            metrics["r_rs_gap_neg_m"]
        ),
        "g_gap_neg_m": (
            metrics["g_rs_gap_neg_m"]
        ),
        "b_gap_neg_m": (
            metrics["b_rs_gap_neg_m"]
        ),
    }


def run():
    ensure_directories()

    rows = []

    print("Building Exp14 dataset")
    print()

    for container in CONTAINERS:
        print(
            f"===== {container} ====="
        )

        for rate in RATES:
            for method in METHODS:
                path = (
                    EXP13_IMAGES
                    / (
                        f"{container}_"
                        f"{rate:03d}_"
                        f"{method}.png"
                    )
                )

                if not path.exists():
                    raise FileNotFoundError(
                        path
                    )

                metrics = analyze_image(
                    path,
                    MASK,
                )

                features = extract_features(
                    metrics
                )

                rows.append(
                    {
                        "container": container,
                        "method": method,
                        "rate": rate,
                        **features,
                    }
                )

                print(
                    f"{rate:3d}% "
                    f"{method:<10} "
                    f"gap={features['gap_m']:.6f}"
                )

        print()

    fieldnames = list(
        rows[0].keys()
    )

    with open(
        DATASET_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Dataset rows: {len(rows)}"
    )

    print(
        f"Dataset: {DATASET_CSV}"
    )


if __name__ == "__main__":
    run()
