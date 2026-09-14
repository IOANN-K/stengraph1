import math

import numpy as np
from PIL import Image
from scipy.stats import chi2


def load_rgb(path):
    return np.asarray(
        Image.open(path).convert("RGB"),
        dtype=np.uint8,
    )


def binary_entropy(probability):
    if probability <= 0.0 or probability >= 1.0:
        return 0.0

    return -(
        probability * math.log2(probability)
        + (1.0 - probability)
        * math.log2(1.0 - probability)
    )


def lsb_statistics(channel):
    lsb = (
        channel.reshape(-1)
        & 1
    ).astype(
        np.uint8
    )

    one_ratio = float(
        np.mean(lsb)
    )

    entropy = binary_entropy(
        one_ratio
    )

    return {
        "lsb_one_ratio": one_ratio,
        "lsb_zero_ratio": 1.0 - one_ratio,
        "lsb_entropy": entropy,
    }


def pov_chi_square(channel):
    values = channel.reshape(-1)

    histogram = np.bincount(
        values,
        minlength=256,
    ).astype(
        np.float64
    )

    even = histogram[0::2]
    odd = histogram[1::2]

    pair_total = even + odd

    valid = pair_total > 0

    even = even[valid]
    odd = odd[valid]
    pair_total = pair_total[valid]

    expected = pair_total / 2.0

    statistic = np.sum(
        (
            (even - expected) ** 2
            + (odd - expected) ** 2
        )
        / expected
    )

    dof = int(
        len(expected)
    )

    p_value = float(
        chi2.sf(
            statistic,
            dof,
        )
    )

    normalized = (
        float(statistic / dof)
        if dof > 0
        else 0.0
    )

    return {
        "chi_square": float(statistic),
        "chi_square_dof": dof,
        "chi_square_normalized": normalized,
        "chi_square_p_value": p_value,
    }


def spatial_lsb_statistics(channel):
    lsb = (
        channel
        & 1
    ).astype(
        np.uint8
    )

    horizontal_agreement = np.mean(
        lsb[:, :-1]
        == lsb[:, 1:]
    )

    vertical_agreement = np.mean(
        lsb[:-1, :]
        == lsb[1:, :]
    )

    return {
        "horizontal_lsb_agreement": float(
            horizontal_agreement
        ),
        "vertical_lsb_agreement": float(
            vertical_agreement
        ),
    }


def analyze_channel(channel):
    return {
        **lsb_statistics(channel),
        **pov_chi_square(channel),
        **spatial_lsb_statistics(channel),
    }


def analyze_image(path):
    image = load_rgb(path)

    result = {}

    channel_names = [
        "r",
        "g",
        "b",
    ]

    for index, name in enumerate(
        channel_names
    ):
        metrics = analyze_channel(
            image[:, :, index]
        )

        for metric_name, value in metrics.items():
            result[
                f"{name}_{metric_name}"
            ] = value

    pooled = image.reshape(-1)

    pooled_lsb = lsb_statistics(
        pooled
    )

    pooled_chi = pov_chi_square(
        pooled
    )

    for metric_name, value in {
        **pooled_lsb,
        **pooled_chi,
    }.items():
        result[
            f"pooled_{metric_name}"
        ] = value

    result["mean_spatial_agreement"] = float(
        np.mean(
            [
                result[
                    "r_horizontal_lsb_agreement"
                ],
                result[
                    "r_vertical_lsb_agreement"
                ],
                result[
                    "g_horizontal_lsb_agreement"
                ],
                result[
                    "g_vertical_lsb_agreement"
                ],
                result[
                    "b_horizontal_lsb_agreement"
                ],
                result[
                    "b_vertical_lsb_agreement"
                ],
            ]
        )
    )

    return result