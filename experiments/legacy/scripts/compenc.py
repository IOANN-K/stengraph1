from PIL import Image
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STEGO_IMAGE = ROOT / "experiments" / "legacy" / "results" / "random_lsb" / "input2_random_1lsb.png"


def extract_random(image_path, key):
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())

    capacity = len(pixels) * 3

    channel_positions = list(range(capacity))

    rng = random.Random(key)
    rng.shuffle(channel_positions)

    def read_bits(count, offset=0):
        bits = ""

        for i in range(offset, offset + count):
            position = channel_positions[i]

            pixel_index = position // 3
            channel_index = position % 3

            value = pixels[pixel_index][channel_index]

            bits += str(value & 1)

        return bits

    length_bits = read_bits(32)
    message_length = int(length_bits, 2)

    message_bits = read_bits(
        message_length * 8,
        32
    )

    data = bytearray()

    for i in range(0, len(message_bits), 8):
        data.append(
            int(message_bits[i:i + 8], 2)
        )

    return data.decode("utf-8")


print(
    extract_random(
        STEGO_IMAGE,
        "my-secret-key"
    )
)
