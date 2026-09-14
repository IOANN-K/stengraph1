from pathlib import Path

import numpy as np
from PIL import Image


def load_rgb(path: str | Path, *, copy: bool = True) -> np.ndarray:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Input image not found: {path}")
    array = np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)
    return array.copy() if copy else array


def save_rgb(array: np.ndarray, path: str | Path) -> None:
    if array.ndim != 3 or array.shape[2] != 3:
        raise ValueError("Expected an RGB array with shape (height, width, 3)")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array.astype(np.uint8, copy=False), mode="RGB").save(path)


def image_info(path: str | Path) -> dict[str, int | str]:
    with Image.open(path) as image:
        return {"width": image.width, "height": image.height, "mode": image.mode}
