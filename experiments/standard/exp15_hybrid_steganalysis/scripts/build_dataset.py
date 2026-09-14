import csv

from exp15_config import (
    CONTAINERS,
    DATASET_CSV,
    EXP13_IMAGES,
    MASK,
    METHODS,
    RATES,
    ensure_directories,
)


from stengraph.steganalysis.basic import (
    analyze_image as analyze_basic,
)


from stengraph.steganalysis.rs import (
    analyze_image as analyze_rs,
)


def safe_ratio(a, b):
    if abs(b) < 1e-12:
        return 0.0

    return a / b


def extract_features(
    basic,
    rs,
):
    gap_m = rs[
        "mean_rs_gap_m"
    ]

    gap_neg = rs[
        "mean_rs_gap_neg_m"
    ]

    return {
        "rs_r_m": rs[
            "mean_r_m_ratio"
        ],
        "rs_s_m": rs[
            "mean_s_m_ratio"
        ],
        "rs_r_neg_m": rs[
            "mean_r_neg_m_ratio"
        ],
        "rs_s_neg_m": rs[
            "mean_s_neg_m_ratio"
        ],

        "rs_gap_m": gap_m,
        "rs_gap_neg_m": gap_neg,

        "rs_gap_ratio": safe_ratio(
            gap_m,
            gap_neg,
        ),

        "rs_r_gap": rs[
            "r_rs_gap_m"
        ],
        "rs_g_gap": rs[
            "g_rs_gap_m"
        ],
        "rs_b_gap": rs[
            "b_rs_gap_m"
        ],

        "lsb_one_ratio": basic[
            "pooled_lsb_one_ratio"
        ],

        "lsb_entropy": basic[
            "pooled_lsb_entropy"
        ],

        "chi_square_normalized": basic[
            "pooled_chi_square_normalized"
        ],

        "spatial_agreement": basic[
            "mean_spatial_agreement"
        ],

        "r_chi_square_normalized": basic[
            "r_chi_square_normalized"
        ],

        "g_chi_square_normalized": basic[
            "g_chi_square_normalized"
        ],

        "b_chi_square_normalized": basic[
            "b_chi_square_normalized"
        ],

        "r_lsb_one_ratio": basic[
            "r_lsb_one_ratio"
        ],

        "g_lsb_one_ratio": basic[
            "g_lsb_one_ratio"
        ],

        "b_lsb_one_ratio": basic[
            "b_lsb_one_ratio"
        ],
    }


def run():
    ensure_directories()

    rows = []

    print(
        "Building Exp15 hybrid dataset"
    )
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

                basic = analyze_basic(
                    path
                )

                rs = analyze_rs(
                    path,
                    MASK,
                )

                features = extract_features(
                    basic,
                    rs,
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
                    f"{method:<10} | "
                    f"RS="
                    f"{features['rs_gap_m']:.6f} | "
                    f"chi²/dof="
                    f"{features['chi_square_normalized']:.3f}"
                )

        print()

    with open(
        DATASET_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(
                rows[0].keys()
            ),
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
