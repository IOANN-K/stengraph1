"""Exp01-compatible 1-LSB behavior.

This module deliberately preserves Python ``random.Random`` placement and the
original float64 local-variance ordering used by Exp01–Exp05 and Exp07.
"""

import random
from pathlib import Path

import numpy as np
from PIL import Image

RANDOM_KEY = "stengraph-exp01"


def _bits(data: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in data)


def _framed(payload: bytes) -> str:
    return _bits(len(payload).to_bytes(4, "big") + payload)


def _decode(bits: str) -> bytes:
    if len(bits) < 32:
        raise ValueError("Malformed payload: missing length header")
    length = int(bits[:32], 2); required = 32 + length * 8
    if required > len(bits):
        raise ValueError("Encoded payload length exceeds image capacity")
    return bytes(int(bits[index:index + 8], 2) for index in range(32, required, 8))


def embed_sequential(input_path: str | Path, output_path: str | Path, payload: bytes) -> None:
    image = Image.open(input_path).convert("RGB"); pixels = [list(pixel) for pixel in image.getdata()]; bits = _framed(payload)
    if len(bits) > len(pixels) * 3: raise ValueError("Payload too large")
    for index, bit in enumerate(bits):
        pixel, channel = divmod(index, 3); pixels[pixel][channel] = (pixels[pixel][channel] & 0b11111110) | int(bit)
    image.putdata([tuple(pixel) for pixel in pixels]); image.save(output_path)


def extract_sequential(image_path: str | Path) -> bytes:
    image = Image.open(image_path).convert("RGB")
    return _decode("".join(str(channel & 1) for pixel in image.getdata() for channel in pixel))


def _random_positions(capacity: int) -> list[int]:
    positions = list(range(capacity)); random.Random(RANDOM_KEY).shuffle(positions); return positions


def embed_random(input_path: str | Path, output_path: str | Path, payload: bytes) -> None:
    image = Image.open(input_path).convert("RGB"); pixels = [list(pixel) for pixel in image.getdata()]; bits = _framed(payload)
    if len(bits) > len(pixels) * 3: raise ValueError("Payload too large")
    for bit, position in zip(bits, _random_positions(len(pixels) * 3)):
        pixel, channel = divmod(position, 3); pixels[pixel][channel] = (pixels[pixel][channel] & 0b11111110) | int(bit)
    image.putdata([tuple(pixel) for pixel in pixels]); image.save(output_path)


def extract_random(image_path: str | Path) -> bytes:
    image = Image.open(image_path).convert("RGB"); pixels = list(image.getdata()); positions = _random_positions(len(pixels) * 3)
    return _decode("".join(str(pixels[position // 3][position % 3] & 1) for position in positions))


def calculate_texture_scores(image_array: np.ndarray) -> np.ndarray:
    height, width, _ = image_array.shape; gray = 0.299 * (image_array & 0b11111110)[:, :, 0] + 0.587 * (image_array & 0b11111110)[:, :, 1] + 0.114 * (image_array & 0b11111110)[:, :, 2]
    padded = np.pad(gray, 1, mode="reflect"); scores = np.zeros((height, width), dtype=np.float64)
    for y in range(height):
        for x in range(width): scores[y, x] = np.var(padded[y:y + 3, x:x + 3])
    return scores


def _adaptive_positions(array: np.ndarray) -> list[tuple[int, int]]:
    scores = calculate_texture_scores(array); width = scores.shape[1]
    indices = np.argsort(-scores.ravel(), kind="stable")
    return [(int(index // width), int(index % width)) for index in indices]


def embed_adaptive(input_path: str | Path, output_path: str | Path, payload: bytes) -> None:
    image = Image.open(input_path).convert("RGB"); array = np.array(image, dtype=np.uint8); bits = _framed(payload)
    if len(bits) > array.size: raise ValueError("Payload too large")
    index = 0
    for y, x in _adaptive_positions(array):
        for channel in range(3):
            if index == len(bits): break
            array[y, x, channel] = (array[y, x, channel] & 0b11111110) | int(bits[index]); index += 1
        if index == len(bits): break
    Image.fromarray(array, mode="RGB").save(output_path)


def extract_adaptive(image_path: str | Path) -> bytes:
    array = np.array(Image.open(image_path).convert("RGB"), dtype=np.uint8)
    return _decode("".join(str(array[y, x, channel] & 1) for y, x in _adaptive_positions(array) for channel in range(3)))
