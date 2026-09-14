"""Дослідницька реалізація RS, збережена з Exp11, включно з обрізанням від’ємних переворотів."""

from pathlib import Path

import numpy as np

from stengraph.io.images import load_rgb


def discrimination(groups: np.ndarray) -> np.ndarray:
    return np.abs(np.diff(groups.astype(np.int16, copy=False), axis=1)).sum(axis=1)


def flip_positive(values: np.ndarray) -> np.ndarray:
    values = values.astype(np.int16, copy=False); result = values.copy(); even = values % 2 == 0
    result[even] += 1; result[~even] -= 1
    return result


def flip_negative(values: np.ndarray) -> np.ndarray:
    values = values.astype(np.int16, copy=False); result = values.copy(); even = values % 2 == 0
    result[even] -= 1; result[~even] += 1
    np.clip(result, 0, 255, out=result)
    return result


def apply_mask(groups: np.ndarray, mask: list[int]) -> np.ndarray:
    if groups.ndim != 2 or groups.shape[1] != len(mask):
        raise ValueError("Довжина маски має відповідати ширині групи RS")
    result = groups.astype(np.int16, copy=True)
    for index, value in enumerate(mask):
        if value == 1: result[:, index] = flip_positive(result[:, index])
        elif value == -1: result[:, index] = flip_negative(result[:, index])
        elif value != 0: raise ValueError("Значення маски RS мають бути -1, 0 або 1")
    return result


def classify_groups(groups: np.ndarray, mask: list[int]) -> dict[str, int]:
    original, flipped = discrimination(groups), discrimination(apply_mask(groups, mask))
    return {"regular": int(np.count_nonzero(flipped > original)), "singular": int(np.count_nonzero(flipped < original)), "unusable": int(np.count_nonzero(flipped == original))}


def prepare_groups(channel: np.ndarray) -> np.ndarray:
    flat = channel.reshape(-1); usable = len(flat) // 4 * 4
    if not usable: raise ValueError("Для RS-аналізу потрібно щонайменше чотири значення каналів")
    return flat[:usable].reshape(-1, 4)


def analyze_channel(channel: np.ndarray, mask: list[int]) -> dict[str, float | int]:
    groups = prepare_groups(channel); positive = classify_groups(groups, mask); negative = classify_groups(groups, [-v for v in mask]); total = len(groups)
    return {"groups": total, "r_m": positive["regular"], "s_m": positive["singular"], "u_m": positive["unusable"], "r_neg_m": negative["regular"], "s_neg_m": negative["singular"], "u_neg_m": negative["unusable"], "r_m_ratio": positive["regular"] / total, "s_m_ratio": positive["singular"] / total, "r_neg_m_ratio": negative["regular"] / total, "s_neg_m_ratio": negative["singular"] / total, "rs_gap_m": (positive["regular"] - positive["singular"]) / total, "rs_gap_neg_m": (negative["regular"] - negative["singular"]) / total}


def analyze_image(path: str | Path, mask: list[int]) -> dict[str, float | int]:
    image = load_rgb(path, copy=False); result = {}
    for index, name in enumerate(("r", "g", "b")):
        result.update({f"{name}_{key}": value for key, value in analyze_channel(image[:, :, index], mask).items()})
    for target, key in (("mean_r_m_ratio", "r_m_ratio"), ("mean_s_m_ratio", "s_m_ratio"), ("mean_r_neg_m_ratio", "r_neg_m_ratio"), ("mean_s_neg_m_ratio", "s_neg_m_ratio"), ("mean_rs_gap_m", "rs_gap_m"), ("mean_rs_gap_neg_m", "rs_gap_neg_m")):
        result[target] = float(np.mean([result[f"{c}_{key}"] for c in "rgb"]))
    return result
