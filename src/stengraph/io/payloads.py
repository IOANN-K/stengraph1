from pathlib import Path

import numpy as np


def read_payload(path: str | Path) -> bytes:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Навантаження не знайдено: {path}")
    return path.read_bytes()


def bytes_to_bits(data: bytes) -> np.ndarray:
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))


def bits_to_bytes(bits: np.ndarray) -> bytes:
    bits = np.asarray(bits, dtype=np.uint8).reshape(-1)
    if len(bits) % 8:
        raise ValueError("Кількість бітів має ділитися на 8")
    return np.packbits(bits).tobytes()


def max_payload_bytes(width: int, height: int, depth: int = 1) -> int:
    if depth not in range(1, 5):
        raise ValueError("Глибина LSB має бути від 1 до 4")
    return max(0, (width * height * 3 * depth - 32) // 8)


def deterministic_payload(size_bytes: int, seed: bytes | str) -> bytes:
    import hashlib
    if size_bytes < 0:
        raise ValueError("Розмір навантаження не може бути від’ємним")
    seed_bytes = seed.encode() if isinstance(seed, str) else seed
    value = int.from_bytes(hashlib.sha256(seed_bytes).digest()[:8], "big")
    rng = np.random.default_rng(value)
    return rng.integers(0, 256, size=size_bytes, dtype=np.uint8).tobytes()
