from pathlib import Path

from PIL import Image


def resave_png(input_path: Path, output_path: Path) -> None:
    Image.open(input_path).save(output_path, format="PNG")


def optimize_png(input_path: Path, output_path: Path) -> None:
    Image.open(input_path).save(output_path, format="PNG", optimize=True)


def resize_image(input_path: Path, output_path: Path) -> None:
    image = Image.open(input_path).convert("RGB")
    image.resize((int(image.width * 0.75), int(image.height * 0.75)), Image.Resampling.LANCZOS).save(output_path, format="PNG")


def crop_image(input_path: Path, output_path: Path) -> None:
    image = Image.open(input_path).convert("RGB")
    x, y = int(image.width * 0.05), int(image.height * 0.05)
    image.crop((x, y, image.width - x, image.height - y)).save(output_path, format="PNG")


def jpeg_roundtrip(input_path: Path, output_path: Path) -> None:
    image = Image.open(input_path).convert("RGB")
    temporary = output_path.with_suffix(".jpg")
    image.save(temporary, format="JPEG", quality=95)
    Image.open(temporary).convert("RGB").save(output_path, format="PNG")
    temporary.unlink()
