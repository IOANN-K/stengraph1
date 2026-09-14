"""Stable, content-adaptive LSB ordering and Exp08 scoring variants."""

import hashlib
from pathlib import Path

import numpy as np
from scipy.ndimage import laplace, sobel, uniform_filter

from stengraph.embedding.lsb import _embed, extract_from_channels, validate_depth
from stengraph.io.images import load_rgb, save_rgb

_ORDER_CACHE: dict[tuple[tuple[int, ...], int, bytes], np.ndarray] = {}


def stable_gray(image: np.ndarray, depth: int = 1) -> np.ndarray:
    validate_depth(depth)
    mask = np.uint8(0xFF ^ ((1 << depth) - 1))
    stable = (image & mask).astype(np.float32, copy=False)
    return (0.299 * stable[:, :, 0] + 0.587 * stable[:, :, 1] + 0.114 * stable[:, :, 2]).astype(np.float32, copy=False)


def variance_score(gray: np.ndarray, window_size: int) -> np.ndarray:
    mean = uniform_filter(gray, size=window_size, mode="reflect")
    score = uniform_filter(gray * gray, size=window_size, mode="reflect") - mean * mean
    np.maximum(score, 0.0, out=score)
    return score


def texture_score(image: np.ndarray, metric: str = "variance", window_size: int = 3, depth: int = 1) -> np.ndarray:
    if window_size < 1 or window_size % 2 == 0:
        raise ValueError("Window size must be a positive odd integer")
    gray = stable_gray(image, depth)
    if metric == "variance":
        return variance_score(gray, window_size)
    if metric == "gradient":
        score = np.hypot(sobel(gray, axis=1, mode="reflect"), sobel(gray, axis=0, mode="reflect"))
    elif metric == "laplacian":
        score = np.abs(laplace(gray, mode="reflect"))
    else:
        raise ValueError(f"Unknown metric: {metric}")
    return uniform_filter(score, size=window_size, mode="reflect") if window_size > 1 else score


def pixel_order(image: np.ndarray, depth: int = 1, metric: str = "variance", window_size: int = 3) -> np.ndarray:
    if metric == "variance" and window_size == 3:
        stable = image & np.uint8(0xFF ^ ((1 << depth) - 1))
        key = (image.shape, depth, hashlib.blake2b(stable.tobytes(), digest_size=8).digest())
        cached = _ORDER_CACHE.get(key)
        if cached is not None:
            return cached
    order = np.argsort(-texture_score(image, metric, window_size, depth).reshape(-1), kind="stable").astype(np.uint32, copy=False)
    if metric == "variance" and window_size == 3:
        _ORDER_CACHE[key] = order
    return order


def channel_order(image: np.ndarray, depth: int = 1, metric: str = "variance", window_size: int = 3) -> np.ndarray:
    pixels = pixel_order(image, depth, metric, window_size).astype(np.uint64, copy=False)
    base = pixels * 3
    order = np.empty(len(pixels) * 3, dtype=np.uint32)
    order[0::3], order[1::3], order[2::3] = base, base + 1, base + 2
    return order


def embed_adaptive(input_path: str | Path, output_path: str | Path, payload: bytes, depth: int = 1) -> None:
    image = load_rgb(input_path)
    _embed(image, channel_order(image, depth), payload, depth)
    save_rgb(image, output_path)


def extract_adaptive(image_path: str | Path, depth: int = 1) -> bytes:
    image = load_rgb(image_path)
    channels = image.reshape(-1)
    return extract_from_channels(channels[channel_order(image, depth)], depth)


def embed_adaptive_variant(input_path: str | Path, output_path: str | Path, payload: bytes, metric: str, window_size: int) -> None:
    image = load_rgb(input_path)
    _embed(image, channel_order(image, 1, metric, window_size), payload, 1)
    save_rgb(image, output_path)


def extract_adaptive_variant(image_path: str | Path, metric: str, window_size: int) -> bytes:
    image = load_rgb(image_path)
    channels = image.reshape(-1)
    return extract_from_channels(channels[channel_order(image, 1, metric, window_size)], 1)
