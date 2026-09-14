from PIL import Image


def extract_sequential(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.getdata())

    bits = []

    for pixel in pixels:
        for channel in pixel:
            bits.append(str(channel & 1))

    bit_string = "".join(bits)

    header_bits = bit_string[:32]
    payload_length = int(header_bits, 2)

    payload_bits = bit_string[
        32:32 + payload_length * 8
    ]

    payload = bytearray()

    for i in range(0, len(payload_bits), 8):
        payload.append(
            int(payload_bits[i:i + 8], 2)
        )

    return bytes(payload)