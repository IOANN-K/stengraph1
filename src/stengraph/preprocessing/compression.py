import zlib


def compress(data: bytes, level: int = -1) -> bytes:
    return zlib.compress(data, level)


def decompress(data: bytes) -> bytes:
    return zlib.decompress(data)
