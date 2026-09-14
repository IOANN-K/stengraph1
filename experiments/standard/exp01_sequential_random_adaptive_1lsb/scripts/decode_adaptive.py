import numpy as np
from PIL import Image

from adaptive_lsb import calculate_texture_scores


def extract_adaptive(image_path):
    image = Image.open(image_path).convert("RGB")

    image_array = np.array(
        image,
        dtype=np.uint8,
    )

    height, width, _ = image_array.shape

    scores = calculate_texture_scores(
        image_array
    )

    pixel_positions = [
        (y, x)
        for y in range(height)
        for x in range(width)
    ]

    pixel_positions.sort(
        key=lambda position: (
            scores[position[0], position[1]],
            -position[0],
            -position[1],
        ),
        reverse=True,
    )

    bits = []

    for y, x in pixel_positions:
        for channel_index in range(3):
            bits.append(
                str(
                    image_array[
                        y,
                        x,
                        channel_index,
                    ] & 1
                )
            )

    bit_string = "".join(bits)

    payload_length = int(
        bit_string[:32],
        2,
    )

    payload_bits = bit_string[
        32:32 + payload_length * 8
    ]

    payload = bytearray()

    for i in range(0, len(payload_bits), 8):
        payload.append(
            int(payload_bits[i:i + 8], 2)
        )

    return bytes(payload)