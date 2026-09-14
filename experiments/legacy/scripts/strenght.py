from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT_IMAGE = ROOT / "data" / "images" / "input.png"
LSB_STRENGTH_RESULTS = ROOT / "experiments" / "legacy" / "results" / "lsb_strength"

def text_to_bits(text):
    return ''.join(f'{byte:08b}' for byte in text.encode("utf-8"))


def hide_message(input_path, output_path, message, lsb_count=1):
    image = Image.open(input_path).convert("RGBA")
    pixels = list(image.getdata())

    message_bytes = message.encode("utf-8")
    bits = f'{len(message_bytes):032b}' + text_to_bits(message)

    capacity = len(pixels) * 3 * lsb_count

    if len(bits) > capacity:
        raise ValueError("Повідомлення занадто велике")

    mask_clear = 0xFF ^ ((1 << lsb_count) - 1)

    new_pixels = []
    bit_index = 0

    for r, g, b, a in pixels:
        channels = [r, g, b]

        for i in range(3):
            if bit_index >= len(bits):
                break

            chunk = bits[bit_index:bit_index + lsb_count]
            chunk = chunk.ljust(lsb_count, '0')

            value = int(chunk, 2)

            channels[i] = (channels[i] & mask_clear) | value
            bit_index += lsb_count

        new_pixels.append(
            (channels[0], channels[1], channels[2], a)
        )

    image.putdata(new_pixels)
    image.save(output_path)

    print(
        f"{lsb_count} LSB: "
        f"{len(message_bytes)} bytes hidden in {output_path}"
    )


message = "Привіт! Це секретне повідомлення."

for n in range(1, 5):
    hide_message(
        INPUT_IMAGE,
        LSB_STRENGTH_RESULTS / f"secret_{n}lsb.png",
        message,
        n
    )
