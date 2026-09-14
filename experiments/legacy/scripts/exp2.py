from PIL import Image, ImageChops
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT_IMAGE = ROOT / "data" / "images" / "input2.png"
LSB_STRENGTH_RESULTS = ROOT / "experiments" / "legacy" / "results" / "lsb_strength"
DIFFERENCE_RESULTS = LSB_STRENGTH_RESULTS / "differences"


def text_to_bits(text):
    return ''.join(f'{byte:08b}' for byte in text.encode("utf-8"))


def hide_message(input_path, output_path, message, lsb_count=1):
    image = Image.open(input_path).convert("RGB")
    pixels = list(image.getdata())

    message_bytes = message.encode("utf-8")
    bits = f'{len(message_bytes):032b}' + text_to_bits(message)

    capacity = len(pixels) * 3 * lsb_count

    if len(bits) > capacity:
        raise ValueError(
            f"Повідомлення завелике. "
            f"Потрібно {len(bits)} біт, доступно {capacity}"
        )

    mask_clear = 0xFF ^ ((1 << lsb_count) - 1)

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        channels = list(pixel)

        for i in range(3):
            if bit_index >= len(bits):
                break

            chunk = bits[bit_index:bit_index + lsb_count]
            chunk = chunk.ljust(lsb_count, "0")

            channels[i] = (
                channels[i] & mask_clear
            ) | int(chunk, 2)

            bit_index += lsb_count

        new_pixels.append(tuple(channels))

    image.putdata(new_pixels)
    image.save(output_path)


def create_binary_diff(original_path, stego_path, output_path):
    original = Image.open(original_path).convert("RGB")
    stego = Image.open(stego_path).convert("RGB")

    result = []

    for p1, p2 in zip(original.getdata(), stego.getdata()):
        if p1 == p2:
            result.append((0, 0, 0))
        else:
            result.append((255, 255, 255))

    diff = Image.new("RGB", original.size)
    diff.putdata(result)
    diff.save(output_path)


def calculate_mse_psnr(original_path, stego_path):
    original = Image.open(original_path).convert("RGB")
    stego = Image.open(stego_path).convert("RGB")

    total_error = 0
    count = 0

    for p1, p2 in zip(original.getdata(), stego.getdata()):
        for a, b in zip(p1, p2):
            total_error += (a - b) ** 2
            count += 1

    mse = total_error / count

    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * math.log10((255 ** 2) / mse)

    return mse, psnr


message = "Це тестове секретне повідомлення. " * 3000

for n in range(1, 5):
    output = LSB_STRENGTH_RESULTS / f"input2_secret_{n}lsb.png"

    hide_message(
        INPUT_IMAGE,
        output,
        message,
        n
    )

    create_binary_diff(
        INPUT_IMAGE,
        output,
        DIFFERENCE_RESULTS / f"input2_diff_{n}lsb.png"
    )

    mse, psnr = calculate_mse_psnr(
        INPUT_IMAGE,
        output
    )

    print(
        f"{n} LSB | "
        f"MSE = {mse:.4f} | "
        f"PSNR = {psnr:.2f} dB"
    )
