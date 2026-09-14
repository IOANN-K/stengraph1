from PIL import Image, ImageChops
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT_IMAGE = ROOT / "data" / "images" / "input.png"
SECRET_IMAGE = ROOT / "experiments" / "legacy" / "results" / "transparency" / "secret.png"
DIFFERENCE_RESULTS = ROOT / "experiments" / "legacy" / "results" / "difference_maps"

def create_difference_maps(original_path, stego_path):
    original = Image.open(original_path).convert("RGBA")
    stego = Image.open(stego_path).convert("RGBA")

    if original.size != stego.size:
        raise ValueError("Зображення мають бути однакового розміру")

    diff = ImageChops.difference(original, stego)
    diff.save(DIFFERENCE_RESULTS / "diff_raw.png")

    enhanced = diff.copy()
    pixels = list(enhanced.getdata())
    boosted_pixels = []

    factor = 80

    for r, g, b, a in pixels:
        boosted_pixels.append((
            min(r * factor, 255),
            min(g * factor, 255),
            min(b * factor, 255),
            255
        ))

    enhanced.putdata(boosted_pixels)
    enhanced.save(DIFFERENCE_RESULTS / "diff_enhanced.png")

    print("Створено:")
    print("- diff_raw.png")
    print("- diff_enhanced.png")


create_difference_maps(INPUT_IMAGE, SECRET_IMAGE)
