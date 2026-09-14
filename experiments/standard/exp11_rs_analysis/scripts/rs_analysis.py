import numpy as np
from PIL import Image


def load_rgb(path):
    return np.asarray(
        Image.open(path).convert("RGB"),
        dtype=np.uint8,
    )


def discrimination(groups):
    groups = groups.astype(
        np.int16,
        copy=False,
    )

    return np.abs(
        np.diff(
            groups,
            axis=1,
        )
    ).sum(
        axis=1
    )


def flip_positive(values):
    values = values.astype(
        np.int16,
        copy=False,
    )

    even = (
        values % 2 == 0
    )

    result = values.copy()

    result[even] += 1
    result[~even] -= 1

    return result


def flip_negative(values):
    values = values.astype(
        np.int16,
        copy=False,
    )

    even = (
        values % 2 == 0
    )

    result = values.copy()

    result[even] -= 1
    result[~even] += 1

    np.clip(
        result,
        0,
        255,
        out=result,
    )

    return result


def apply_mask(
    groups,
    mask,
):
    result = groups.astype(
        np.int16,
        copy=True,
    )

    mask = np.asarray(
        mask,
        dtype=np.int8,
    )

    for index, value in enumerate(
        mask
    ):
        if value == 1:
            result[:, index] = flip_positive(
                result[:, index]
            )

        elif value == -1:
            result[:, index] = flip_negative(
                result[:, index]
            )

    return result


def classify_groups(
    groups,
    mask,
):
    original_score = discrimination(
        groups
    )

    flipped = apply_mask(
        groups,
        mask,
    )

    flipped_score = discrimination(
        flipped
    )

    regular = int(
        np.count_nonzero(
            flipped_score
            > original_score
        )
    )

    singular = int(
        np.count_nonzero(
            flipped_score
            < original_score
        )
    )

    unusable = int(
        np.count_nonzero(
            flipped_score
            == original_score
        )
    )

    return {
        "regular": regular,
        "singular": singular,
        "unusable": unusable,
    }


def prepare_groups(channel):
    flat = channel.reshape(-1)

    usable = (
        len(flat) // 4
    ) * 4

    return flat[
        :usable
    ].reshape(
        -1,
        4,
    )


def analyze_channel(
    channel,
    mask,
):
    groups = prepare_groups(
        channel
    )

    positive = classify_groups(
        groups,
        mask,
    )

    negative_mask = [
        -value
        for value in mask
    ]

    negative = classify_groups(
        groups,
        negative_mask,
    )

    total = len(groups)

    return {
        "groups": total,

        "r_m": positive["regular"],
        "s_m": positive["singular"],
        "u_m": positive["unusable"],

        "r_neg_m": negative["regular"],
        "s_neg_m": negative["singular"],
        "u_neg_m": negative["unusable"],

        "r_m_ratio": (
            positive["regular"]
            / total
        ),

        "s_m_ratio": (
            positive["singular"]
            / total
        ),

        "r_neg_m_ratio": (
            negative["regular"]
            / total
        ),

        "s_neg_m_ratio": (
            negative["singular"]
            / total
        ),

        "rs_gap_m": (
            positive["regular"]
            - positive["singular"]
        ) / total,

        "rs_gap_neg_m": (
            negative["regular"]
            - negative["singular"]
        ) / total,
    }


def analyze_image(
    path,
    mask,
):
    image = load_rgb(
        path
    )

    result = {}

    for index, channel_name in enumerate(
        ["r", "g", "b"]
    ):
        metrics = analyze_channel(
            image[:, :, index],
            mask,
        )

        for key, value in metrics.items():
            result[
                f"{channel_name}_{key}"
            ] = value

    result["mean_r_m_ratio"] = float(
        np.mean(
            [
                result["r_r_m_ratio"],
                result["g_r_m_ratio"],
                result["b_r_m_ratio"],
            ]
        )
    )

    result["mean_s_m_ratio"] = float(
        np.mean(
            [
                result["r_s_m_ratio"],
                result["g_s_m_ratio"],
                result["b_s_m_ratio"],
            ]
        )
    )

    result["mean_r_neg_m_ratio"] = float(
        np.mean(
            [
                result["r_r_neg_m_ratio"],
                result["g_r_neg_m_ratio"],
                result["b_r_neg_m_ratio"],
            ]
        )
    )

    result["mean_s_neg_m_ratio"] = float(
        np.mean(
            [
                result["r_s_neg_m_ratio"],
                result["g_s_neg_m_ratio"],
                result["b_s_neg_m_ratio"],
            ]
        )
    )

    result["mean_rs_gap_m"] = float(
        np.mean(
            [
                result["r_rs_gap_m"],
                result["g_rs_gap_m"],
                result["b_rs_gap_m"],
            ]
        )
    )

    result["mean_rs_gap_neg_m"] = float(
        np.mean(
            [
                result["r_rs_gap_neg_m"],
                result["g_rs_gap_neg_m"],
                result["b_rs_gap_neg_m"],
            ]
        )
    )

    return result