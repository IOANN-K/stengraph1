from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SECRET_IMAGE = ROOT / "experiments" / "legacy" / "results" / "transparency" / "secret.png"

def extract_message(image_path):
    image = Image.open(image_path).convert("RGBA")
    pixels = list(image.getdata())

    bits = ""

    for r, g, b, a in pixels:
        bits += str(r & 1)
        bits += str(g & 1)
        bits += str(b & 1)

    length = int(bits[:32], 2)

    message_bits = bits[32:32 + length * 8]

    data = bytearray()

    for i in range(0, len(message_bits), 8):
        data.append(int(message_bits[i:i + 8], 2))

    return data.decode("utf-8")


print(extract_message(SECRET_IMAGE))
