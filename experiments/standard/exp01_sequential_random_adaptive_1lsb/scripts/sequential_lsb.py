from PIL import Image

from common import bytes_to_bits


def embed_sequential(input_path, output_path, payload):
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

    bit_index = 0

    for pixel in pixels:
        for channel_index in range(3):
            if bit_index >= len(bits):
                break

            pixel[channel_index] = (
                pixel[channel_index] & 0b11111110
            ) | int(bits[bit_index])

            bit_index += 1

        if bit_index >= len(bits):
            break

    image.putdata([tuple(pixel) for pixel in pixels])
    image.save(output_path)