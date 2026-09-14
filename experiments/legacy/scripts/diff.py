from PIL import Image
import numpy as np
import math
from skimage.metrics import structural_similarity as ssim
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT_IMAGE = ROOT / "data" / "images" / "input2.png"
LSB_STRENGTH_RESULTS = ROOT / "experiments" / "legacy" / "results" / "lsb_strength"


def analyze(original_path, stego_path):
    original = np.array(
        Image.open(original_path).convert("RGB"),
        dtype=np.float64
    )

    stego = np.array(
        Image.open(stego_path).convert("RGB"),
        dtype=np.float64
    )

    if original.shape != stego.shape:
        raise ValueError("Розміри зображень не збігаються")

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
        data_range=255
    )

    changed = np.any(original != stego, axis=2)

    changed_pixels = np.count_nonzero(changed)
    total_pixels = changed.size

    changed_percent = changed_pixels / total_pixels * 100

    max_difference = np.max(np.abs(diff))

    return {
        "MSE": mse,
        "PSNR": psnr,
        "SSIM": ssim_value,
        "Changed pixels": changed_pixels,
        "Changed %": changed_percent,
        "Max difference": max_difference
    }


for n in range(1, 5):
    result = analyze(
        INPUT_IMAGE,
        LSB_STRENGTH_RESULTS / f"input2_secret_{n}lsb.png"
    )

    print(f"\n===== {n} LSB =====")
    print(f"MSE:             {result['MSE']:.6f}")
    print(f"PSNR:            {result['PSNR']:.2f} dB")
    print(f"SSIM:            {result['SSIM']:.6f}")
    print(f"Changed pixels:  {result['Changed pixels']}")
    print(f"Changed:         {result['Changed %']:.2f}%")
    print(f"Max difference:  {result['Max difference']:.0f}")
