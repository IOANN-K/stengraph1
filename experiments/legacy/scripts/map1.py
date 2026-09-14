from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT_IMAGE = ROOT / "data" / "images" / "input.png"
SECRET_IMAGE = ROOT / "experiments" / "legacy" / "results" / "transparency" / "secret.png"
DIFFERENCE_RESULTS = ROOT / "experiments" / "legacy" / "results" / "difference_maps"

def create_binary_difference_map(original_path, stego_path):
    original = Image.open(original_path).convert("RGBA")
    stego = Image.open(stego_path).convert("RGBA")

    if original.size != stego.size:
        raise ValueError("Зображення мають бути однакового розміру")

    orig_pixels = list(original.getdata())
    stego_pixels = list(stego.getdata())

    result_pixels = []

    for p1, p2 in zip(orig_pixels, stego_pixels):
        if p1[:3] == p2[:3]:
            result_pixels.append((0, 0, 0, 255))
        else:
            result_pixels.append((255, 255, 255, 255))

    result = Image.new("RGBA", original.size)
    result.putdata(result_pixels)
    result.save(DIFFERENCE_RESULTS / "diff_binary1.png")

    print("Створено diff_binary1.png")


create_binary_difference_map(INPUT_IMAGE, SECRET_IMAGE)
