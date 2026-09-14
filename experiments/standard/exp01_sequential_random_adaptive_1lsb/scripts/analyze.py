import csv
import math

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def analyze_images(original_path, stego_path):
    original = np.array(
        Image.open(original_path).convert("RGB"),
        dtype=np.float64,
    )

    stego = np.array(
        Image.open(stego_path).convert("RGB"),
        dtype=np.float64,
    )

    if original.shape != stego.shape:
        raise ValueError("Image dimensions do not match")

    diff = original - stego

    mse = np.mean(diff ** 2)

    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * math.log10((255 ** 2) / mse)

    ssim_value = ssim(
        original,
        stego,
        channel_axis=2,
        data_range=255,
    )

    changed_channels_mask = original != stego
    changed_pixels_mask = np.any(
        changed_channels_mask,
        axis=2,
    )

    changed_channels = np.count_nonzero(
        changed_channels_mask
    )

    total_channels = changed_channels_mask.size

    changed_pixels = np.count_nonzero(
        changed_pixels_mask
    )

    total_pixels = changed_pixels_mask.size

    max_difference = np.max(
        np.abs(diff)
    )

    return {
        "mse": mse,
        "psnr": psnr,
        "ssim": ssim_value,
        "changed_pixels": changed_pixels,
        "changed_pixels_percent": (
            changed_pixels / total_pixels * 100
        ),
        "changed_channels": changed_channels,
        "changed_channels_percent": (
            changed_channels / total_channels * 100
        ),
        "max_difference": max_difference,
    }


def create_binary_difference_map(
    original_path,
    stego_path,
    output_path,
):
    original = np.array(
        Image.open(original_path).convert("RGB")
    )

    stego = np.array(
        Image.open(stego_path).convert("RGB")
    )

    changed = np.any(
        original != stego,
        axis=2,
    )

    diff_image = np.zeros(
        (original.shape[0], original.shape[1], 3),
        dtype=np.uint8,
    )

    diff_image[changed] = 255

    Image.fromarray(diff_image).save(output_path)


def write_results_csv(results, output_path):
    fieldnames = [
        "method",
        "payload_bytes",
        "payload_sha256",
        "decode_success",
        "decoded_sha256",
        "decoded_bytes",
        "changed_pixels",
        "changed_pixels_percent",
        "changed_channels",
        "changed_channels_percent",
        "mse",
        "psnr",
        "ssim",
        "max_difference",
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)