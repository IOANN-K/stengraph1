import random

from PIL import Image

from random_lsb import RANDOM_KEY


def extract_random(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())

    capacity = len(pixels) * 3

    positions = list(range(capacity))

    rng = random.Random(RANDOM_KEY)
    rng.shuffle(positions)

    def read_bit(position_index):
        position = positions[position_index]

        pixel_index = position // 3
        channel_index = position % 3

        return (
            pixels[pixel_index][channel_index]
            & 1
        )

    header_bits = "".join(
        str(read_bit(i))
        for i in range(32)
    )

    payload_length = int(header_bits, 2)

    payload_bits = "".join(
        str(read_bit(i))
        for i in range(
            32,
            32 + payload_length * 8,
        )
    )

    payload = bytearray()

    for i in range(0, len(payload_bits), 8):
        payload.append(
            int(payload_bits[i:i + 8], 2)
        )

    return bytes(payload)