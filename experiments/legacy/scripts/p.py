from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT_IMAGE = ROOT / "data" / "images" / "input.png"
OUTPUT_IMAGE = ROOT / "experiments" / "legacy" / "results" / "transparency" / "secret.png"

def text_to_bits(text):
    data = text.encode("utf-8")
    return ''.join(f'{byte:08b}' for byte in data)


def hide_message(input_path, output_path, message):
    image = Image.open(input_path).convert("RGBA")
    pixels = list(image.getdata())

    message_bytes = message.encode("utf-8")
    length = len(message_bytes)

    bits = f'{length:032b}' + text_to_bits(message)

    capacity = len(pixels) * 3

    if len(bits) > capacity:
        raise ValueError("Повідомлення занадто велике для цього зображення")

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b, a = pixel

        channels = [r, g, b]

        for i in range(3):
            if bit_index < len(bits):
                channels[i] = (
                    channels[i] & 0b11111110
                ) | int(bits[bit_index])

                bit_index += 1

        new_pixels.append((
            channels[0],
            channels[1],
            channels[2],
            a
        ))

    image.putdata(new_pixels)
    image.save(output_path)

    print("Повідомлення приховано")


hide_message(
    INPUT_IMAGE,
    OUTPUT_IMAGE,
    "Привіт! Це секретне повідомлення."
)
