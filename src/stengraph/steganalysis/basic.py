import math
from pathlib import Path

import numpy as np
from scipy.stats import chi2

from stengraph.io.images import load_rgb


def binary_entropy(probability: float) -> float:
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return -(probability * math.log2(probability) + (1.0 - probability) * math.log2(1.0 - probability))


def lsb_statistics(channel: np.ndarray) -> dict[str, float]:
    one_ratio = float(np.mean(channel.reshape(-1) & 1))
    return {"lsb_one_ratio": one_ratio, "lsb_zero_ratio": 1.0 - one_ratio, "lsb_entropy": binary_entropy(one_ratio)}


def pov_chi_square(channel: np.ndarray) -> dict[str, float | int]:
    histogram = np.bincount(channel.reshape(-1), minlength=256).astype(np.float64)
    even, odd = histogram[0::2], histogram[1::2]
    total = even + odd
    valid = total > 0
    even, odd, total = even[valid], odd[valid], total[valid]
    expected = total / 2.0
    statistic = float(np.sum(((even - expected) ** 2 + (odd - expected) ** 2) / expected))
    dof = int(len(expected))
    return {"chi_square": statistic, "chi_square_dof": dof, "chi_square_normalized": statistic / dof if dof else 0.0, "chi_square_p_value": float(chi2.sf(statistic, dof))}


def spatial_lsb_statistics(channel: np.ndarray) -> dict[str, float]:
    if channel.ndim != 2 or min(channel.shape) < 2:
        raise ValueError("Для просторової статистики потрібен 2D-канал розміром щонайменше 2x2")
    lsb = (channel & 1).astype(np.uint8)
    return {"horizontal_lsb_agreement": float(np.mean(lsb[:, :-1] == lsb[:, 1:])), "vertical_lsb_agreement": float(np.mean(lsb[:-1, :] == lsb[1:, :]))}


def analyze_channel(channel: np.ndarray) -> dict[str, float | int]:
    return {**lsb_statistics(channel), **pov_chi_square(channel), **spatial_lsb_statistics(channel)}


def analyze_image(path: str | Path) -> dict[str, float | int]:
    image = load_rgb(path, copy=False)
    result = {}
    for index, name in enumerate(("r", "g", "b")):
        result.update({f"{name}_{key}": value for key, value in analyze_channel(image[:, :, index]).items()})
    result.update({f"pooled_{key}": value for key, value in {**lsb_statistics(image.reshape(-1)), **pov_chi_square(image.reshape(-1))}.items()})
    result["mean_spatial_agreement"] = float(np.mean([result[f"{c}_{axis}_lsb_agreement"] for c in "rgb" for axis in ("horizontal", "vertical")]))
    return result
