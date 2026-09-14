import csv

from exp10_config import (
    CAPACITIES,
    COVER_IMAGE,
    EXP09A_IMAGES,
    METHODS,
    METRICS_DIR,
    ensure_directories,
)

from stengraph.steganalysis.basic import (
    analyze_image,
)


def image_path(
    capacity,
    method,
):
    return (
        EXP09A_IMAGES
        / f"{capacity:03d}_{method}.png"
    )


def run():
    ensure_directories()

    rows = []

    print("Experiment 10")
    print("Basic statistical steganalysis")
    print()

    print("===== COVER =====")

    cover_metrics = analyze_image(
        COVER_IMAGE
    )

    cover_row = {
        "image_type": "cover",
        "capacity_percent": 0,
        "method": "none",
        "file_name": COVER_IMAGE.name,
        **cover_metrics,
    }

    rows.append(
        cover_row
    )

    print(
        "LSB ones="
        f"{cover_metrics['pooled_lsb_one_ratio']:.6f} | "
        "entropy="
        f"{cover_metrics['pooled_lsb_entropy']:.6f} | "
        "chi²/dof="
        f"{cover_metrics['pooled_chi_square_normalized']:.4f} | "
        "p="
        f"{cover_metrics['pooled_chi_square_p_value']:.6g}"
    )

    print()

    for capacity in CAPACITIES:
        print(
            f"===== {capacity}% ====="
        )

        for method in METHODS:
            path = image_path(
                capacity,
                method,
            )

            if not path.exists():
                print(
                    f"SKIP {method}: "
                    f"{path.name} not found"
                )
                continue

            metrics = analyze_image(
                path
            )

            row = {
                "image_type": "stego",
                "capacity_percent": capacity,
                "method": method,
                "file_name": path.name,
                **metrics,
            }

            rows.append(row)

            print(
                f"{method:<10} | "
                f"ones="
                f"{metrics['pooled_lsb_one_ratio']:.6f} | "
                f"H="
                f"{metrics['pooled_lsb_entropy']:.6f} | "
                f"chi²/dof="
                f"{metrics['pooled_chi_square_normalized']:.4f} | "
                f"p="
                f"{metrics['pooled_chi_square_p_value']:.4g} | "
                f"spatial="
                f"{metrics['mean_spatial_agreement']:.6f}"
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
