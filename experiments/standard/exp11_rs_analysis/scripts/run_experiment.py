import csv

from exp11_config import (
    CAPACITIES,
    COVER_IMAGE,
    EXP09A_IMAGES,
    MASK,
    METHODS,
    METRICS_DIR,
    ensure_directories,
)

from stengraph.steganalysis.rs import (
    analyze_image,
)


def get_stego_path(
    capacity,
    method,
):
    return (
        EXP09A_IMAGES
        / f"{capacity:03d}_{method}.png"
    )


def print_metrics(
    label,
    metrics,
):
    print(
        f"{label:<10} | "
        f"R_m={metrics['mean_r_m_ratio']:.6f} | "
        f"S_m={metrics['mean_s_m_ratio']:.6f} | "
        f"gap={metrics['mean_rs_gap_m']:.6f} | "
        f"R_-m={metrics['mean_r_neg_m_ratio']:.6f} | "
        f"S_-m={metrics['mean_s_neg_m_ratio']:.6f}"
    )


def run():
    ensure_directories()

    rows = []

    print("Experiment 11")
    print("RS analysis")
    print(f"Mask: {MASK}")
    print()

    print("===== COVER =====")

    cover_metrics = analyze_image(
        COVER_IMAGE,
        MASK,
    )

    rows.append(
        {
            "image_type": "cover",
            "capacity_percent": 0,
            "method": "none",
            "file_name": COVER_IMAGE.name,
            **cover_metrics,
        }
    )

    print_metrics(
        "cover",
        cover_metrics,
    )

    print()

    for capacity in CAPACITIES:
        print(
            f"===== {capacity}% ====="
        )

        for method in METHODS:
            path = get_stego_path(
                capacity,
                method,
            )

            if not path.exists():
                print(
                    f"SKIP {method}: "
                    f"{path.name} missing"
                )
                continue

            metrics = analyze_image(
                path,
                MASK,
            )

            rows.append(
                {
                    "image_type": "stego",
                    "capacity_percent": capacity,
                    "method": method,
                    "file_name": path.name,
                    **metrics,
                }
            )

            print_metrics(
                method,
                metrics,
            )

        print()

    output_csv = (
        METRICS_DIR
        / "results.csv"
    )

    fieldnames = list(
        rows[0].keys()
    )

    with open(
        output_csv,
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
            rows
        )

    print(
        "Experiment completed."
    )

    print(
        f"Results: {output_csv}"
    )


if __name__ == "__main__":
    run()
