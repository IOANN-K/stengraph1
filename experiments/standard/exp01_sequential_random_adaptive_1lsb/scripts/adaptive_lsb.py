import numpy as np
from PIL import Image

from common import bytes_to_bits


WINDOW_SIZE = 3


def calculate_texture_scores(image_array):
    height, width, _ = image_array.shape

    stable = image_array & 0b11111110

    gray = (
        0.299 * stable[:, :, 0]
        + 0.587 * stable[:, :, 1]
        + 0.114 * stable[:, :, 2]
    )

    padding = WINDOW_SIZE // 2

    padded = np.pad(
        gray,
        padding,
        mode="reflect",
    )

    scores = np.zeros((height, width), dtype=np.float64)

    for y in range(height):
        for x in range(width):
            region = padded[
                y:y + WINDOW_SIZE,
                x:x + WINDOW_SIZE,
            ]

            scores[y, x] = np.var(region)

    return scores


def embed_adaptive(input_path, output_path, payload):
    image = Image.open(input_path).convert("RGB")
    image_array = np.array(image, dtype=np.uint8)

    height, width, _ = image_array.shape

    header = len(payload).to_bytes(4, "big")
    bits = bytes_to_bits(header + payload)

    capacity = height * width * 3

    if len(bits) > capacity:
        raise ValueError(
            f"Payload too large: {len(bits)} bits required, "
            f"{capacity} bits available"
        )

    scores = calculate_texture_scores(image_array)

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

    bit_index = 0

    for y, x in pixel_positions:
        for channel_index in range(3):
            if bit_index >= len(bits):
                break

            image_array[y, x, channel_index] = (
                image_array[y, x, channel_index]
                & 0b11111110
            ) | int(bits[bit_index])

            bit_index += 1

        if bit_index >= len(bits):
            break

    result = Image.fromarray(image_array, mode="RGB")
    result.save(output_path)