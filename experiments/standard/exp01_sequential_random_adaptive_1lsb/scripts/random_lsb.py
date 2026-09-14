import random

from PIL import Image

from common import bytes_to_bits


RANDOM_KEY = "stengraph-exp01"


def embed_random(input_path, output_path, payload):
    image = Image.open(input_path).convert("RGB")
    pixels = [list(pixel) for pixel in image.getdata()]

    header = len(payload).to_bytes(4, "big")
    bits = bytes_to_bits(header + payload)

    capacity = len(pixels) * 3

    if len(bits) > capacity:
        raise ValueError(
            f"Payload too large: {len(bits)} bits required, "
            f"{capacity} bits available"
        )

    positions = list(range(capacity))

    rng = random.Random(RANDOM_KEY)
    rng.shuffle(positions)

    for bit_index, bit in enumerate(bits):
        position = positions[bit_index]

        pixel_index = position // 3
        channel_index = position % 3

        pixels[pixel_index][channel_index] = (
            pixels[pixel_index][channel_index]
            & 0b11111110
        ) | int(bit)

    image.putdata([tuple(pixel) for pixel in pixels])
    image.save(output_path)