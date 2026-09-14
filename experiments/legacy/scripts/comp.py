from PIL import Image
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT_IMAGE = ROOT / "data" / "images" / "input2.png"
OUTPUT_IMAGE = ROOT / "experiments" / "legacy" / "results" / "random_lsb" / "input2_random_1lsb.png"


def text_to_bits(text):
    return ''.join(
        f'{byte:08b}'
        for byte in text.encode("utf-8")
    )


def hide_random(
    input_path,
    output_path,
    message,
    key
):
    image = Image.open(input_path).convert("RGB")
    pixels = list(image.getdata())

    message_bytes = message.encode("utf-8")

    bits = (
        f'{len(message_bytes):032b}'
        + text_to_bits(message)
    )

    capacity = len(pixels) * 3

    if len(bits) > capacity:
        raise ValueError("Повідомлення завелике")

    channel_positions = list(range(capacity))

    rng = random.Random(key)
    rng.shuffle(channel_positions)

    new_pixels = [list(pixel) for pixel in pixels]

    for bit_index, bit in enumerate(bits):
        position = channel_positions[bit_index]

        pixel_index = position // 3
        channel_index = position % 3

        new_pixels[pixel_index][channel_index] = (
            new_pixels[pixel_index][channel_index]
            & 0b11111110
        ) | int(bit)

    image.putdata(
        [tuple(pixel) for pixel in new_pixels]
    )

    image.save(output_path)

    print(f"Готово: {output_path}")


message = "Це тестове секретне повідомлення. " * 3000

hide_random(
    INPUT_IMAGE,
    OUTPUT_IMAGE,
    message,
    "my-secret-key"
)
