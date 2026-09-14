"""Standardized vectorized LSB implementation derived from validated Exp06 code."""

import hashlib
from pathlib import Path

import numpy as np

from stengraph.io.images import load_rgb, save_rgb

_RANDOM_ORDER_CACHE: dict[tuple[int, str], np.ndarray] = {}


def validate_depth(depth: int) -> None:
    if depth not in range(1, 5):
        raise ValueError("LSB depth must be between 1 and 4")


def payload_to_bits(payload: bytes) -> np.ndarray:
    if not isinstance(payload, bytes):
        raise TypeError("Payload must be bytes")
    header = len(payload).to_bytes(4, "big")
    return np.unpackbits(np.frombuffer(header + payload, dtype=np.uint8))


def bits_to_payload(bits: np.ndarray) -> bytes:
    bits = np.asarray(bits, dtype=np.uint8).reshape(-1)
    if len(bits) < 32:
        raise ValueError("Malformed payload: missing 32-bit length header")
    length = int.from_bytes(np.packbits(bits[:32]).tobytes(), "big")
    required = 32 + length * 8
    if required > len(bits):
        raise ValueError("Encoded payload length exceeds image capacity")
    return np.packbits(bits[32:required]).tobytes()[:length]


def bits_to_chunks(bits: np.ndarray, depth: int) -> np.ndarray:
    validate_depth(depth)
    padding = (-len(bits)) % depth
    if padding:
        bits = np.pad(bits, (0, padding), mode="constant")
    weights = 1 << np.arange(depth - 1, -1, -1, dtype=np.uint8)
    return (bits.reshape(-1, depth) * weights).sum(axis=1, dtype=np.uint8)


def chunks_to_bits(chunks: np.ndarray, depth: int) -> np.ndarray:
    validate_depth(depth)
    shifts = np.arange(depth - 1, -1, -1, dtype=np.uint8)
    return (((chunks[:, None] >> shifts) & 1).astype(np.uint8).reshape(-1))


def extract_from_channels(channels: np.ndarray, depth: int) -> bytes:
    validate_depth(depth)
    header_chunks = (32 + depth - 1) // depth
    if len(channels) < header_chunks:
        raise ValueError("Malformed payload: image cannot contain a length header")
    mask = (1 << depth) - 1
    header_bits = chunks_to_bits(channels[:header_chunks] & mask, depth)[:32]
    length = int.from_bytes(np.packbits(header_bits).tobytes(), "big")
    total_bits = 32 + length * 8
    total_chunks = (total_bits + depth - 1) // depth
    if total_chunks > len(channels):
        raise ValueError("Encoded payload length exceeds image capacity")
    bits = chunks_to_bits(channels[:total_chunks] & mask, depth)[:total_bits]
    return bits_to_payload(bits)


def _embed(image: np.ndarray, positions: np.ndarray, payload: bytes, depth: int) -> None:
    bits = payload_to_bits(payload)
    chunks = bits_to_chunks(bits, depth)
    if len(chunks) > len(positions):
        raise ValueError(f"Payload too large: {len(chunks)} chunks required, {len(positions)} available")
    flat = image.reshape(-1)
    selected = positions[:len(chunks)]
    mask = np.uint8(0xFF ^ ((1 << depth) - 1))
    flat[selected] = (flat[selected] & mask) | chunks


def embed_sequential(input_path: str | Path, output_path: str | Path, payload: bytes, depth: int = 1) -> None:
    image = load_rgb(input_path)
    _embed(image, np.arange(image.size), payload, depth)
    save_rgb(image, output_path)


def extract_sequential(image_path: str | Path, depth: int = 1) -> bytes:
    image = load_rgb(image_path)
    return extract_from_channels(image.reshape(-1), depth)


def _seed_from_key(key: str) -> int:
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")


def random_order(channel_count: int, key: str) -> np.ndarray:
    cache_key = (channel_count, key)
    if cache_key not in _RANDOM_ORDER_CACHE:
        order = np.random.default_rng(_seed_from_key(key)).permutation(channel_count)
        _RANDOM_ORDER_CACHE[cache_key] = order.astype(np.uint32, copy=False)
    return _RANDOM_ORDER_CACHE[cache_key]


def embed_random(input_path: str | Path, output_path: str | Path, payload: bytes, depth: int = 1, key: str = "stengraph") -> None:
    image = load_rgb(input_path)
    _embed(image, random_order(image.size, key), payload, depth)
    save_rgb(image, output_path)


def extract_random(image_path: str | Path, depth: int = 1, key: str = "stengraph") -> bytes:
    image = load_rgb(image_path)
    channels = image.reshape(-1)
    return extract_from_channels(channels[random_order(len(channels), key)], depth)
