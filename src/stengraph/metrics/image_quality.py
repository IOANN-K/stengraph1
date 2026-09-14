import math
from pathlib import Path

import numpy as np
from skimage.metrics import structural_similarity

from stengraph.io.images import load_rgb, save_rgb


def analyze_images(original_path: str | Path, stego_path: str | Path) -> dict[str, float | int]:
    original = load_rgb(original_path).astype(np.float64)
    stego = load_rgb(stego_path).astype(np.float64)
    if original.shape != stego.shape:
        raise ValueError("Розміри зображень не збігаються")
    difference = original - stego
    mse = float(np.mean(difference ** 2))
    changed_channels_mask = original != stego
    changed_pixels_mask = np.any(changed_channels_mask, axis=2)
    changed_channels = int(np.count_nonzero(changed_channels_mask))
    changed_pixels = int(np.count_nonzero(changed_pixels_mask))
    return {
        "mse": mse,
        "psnr": float("inf") if mse == 0 else 10 * math.log10(255 ** 2 / mse),
        "ssim": float(structural_similarity(original, stego, channel_axis=2, data_range=255)),
        "changed_pixels": changed_pixels,
        "changed_pixels_percent": changed_pixels / changed_pixels_mask.size * 100,
        "changed_channels": changed_channels,
        "changed_channels_percent": changed_channels / changed_channels_mask.size * 100,
        "max_difference": float(np.max(np.abs(difference))),
    }


def create_binary_difference_map(original_path: str | Path, stego_path: str | Path, output_path: str | Path) -> None:
    original = load_rgb(original_path)
    stego = load_rgb(stego_path)
    if original.shape != stego.shape:
        raise ValueError("Розміри зображень не збігаються")
    result = np.zeros_like(original)
    result[np.any(original != stego, axis=2)] = 255
    save_rgb(result, output_path)
