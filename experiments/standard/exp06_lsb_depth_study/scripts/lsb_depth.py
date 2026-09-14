import hashlib

import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter


_RANDOM_ORDER_CACHE = {}
_ADAPTIVE_ORDER_CACHE = {}


def payload_to_bits(payload):
    header = len(payload).to_bytes(4, "big")
    data = np.frombuffer(header + payload, dtype=np.uint8)

    return np.unpackbits(data)


def bits_to_payload(bits):
    header_bytes = np.packbits(bits[:32]).tobytes()
    payload_length = int.from_bytes(
        header_bytes,
        "big",
    )

    payload_bits = bits[
        32:
        32 + payload_length * 8
    ]

    return np.packbits(
        payload_bits
    ).tobytes()[:payload_length]


def bits_to_chunks(bits, depth):
    padding = (-len(bits)) % depth

    if padding:
        bits = np.pad(
            bits,
            (0, padding),
            mode="constant",
        )

    reshaped = bits.reshape(-1, depth)

    weights = (
        1 << np.arange(
            depth - 1,
            -1,
            -1,
            dtype=np.uint8,
        )
    )

    return (
        reshaped * weights
    ).sum(
        axis=1,
        dtype=np.uint8,
    )


def chunks_to_bits(chunks, depth):
    shifts = np.arange(
        depth - 1,
        -1,
        -1,
        dtype=np.uint8,
    )

    return (
        (
            chunks[:, None]
            >> shifts
        )
        & 1
    ).astype(
        np.uint8
    ).reshape(-1)


def load_rgb(path):
    return np.asarray(
        Image.open(path).convert("RGB"),
        dtype=np.uint8,
    ).copy()


def save_rgb(array, path):
    Image.fromarray(
        array,
        mode="RGB",
    ).save(path)


def extract_from_channels(
    channels,
    depth,
):
    mask = (1 << depth) - 1

    header_chunk_count = (
        32 + depth - 1
    ) // depth

    header_chunks = (
        channels[:header_chunk_count]
        & mask
    )

    header_bits = chunks_to_bits(
        header_chunks,
        depth,
    )[:32]

    header = np.packbits(
        header_bits
    ).tobytes()

    payload_length = int.from_bytes(
        header,
        "big",
    )

    total_bits = (
        32
        + payload_length * 8
    )

    total_chunks = (
        total_bits + depth - 1
    ) // depth

    if total_chunks > len(channels):
        raise ValueError(
            "Encoded payload length exceeds image capacity"
        )

    chunks = (
        channels[:total_chunks]
        & mask
    )

    bits = chunks_to_bits(
        chunks,
        depth,
    )[:total_bits]

    return bits_to_payload(bits)


# ============================================================
# SEQUENTIAL
# ============================================================

def embed_sequential(
    input_path,
    output_path,
    payload,
    depth,
):
    image = load_rgb(input_path)

    channels = image.reshape(-1)

    bits = payload_to_bits(payload)
    chunks = bits_to_chunks(
        bits,
        depth,
    )

    if len(chunks) > len(channels):
        raise ValueError(
            "Payload too large"
        )

    mask = np.uint8(
        0xFF ^ ((1 << depth) - 1)
    )

    n = len(chunks)

    channels[:n] = (
        channels[:n] & mask
    ) | chunks

    save_rgb(
        image,
        output_path,
    )


def extract_sequential(
    image_path,
    depth,
):
    image = load_rgb(image_path)

    channels = image.reshape(-1)

    return extract_from_channels(
        channels,
        depth,
    )


# ============================================================
# RANDOM
# ============================================================

def _seed_from_key(key):
    digest = hashlib.sha256(
        key.encode("utf-8")
    ).digest()

    return int.from_bytes(
        digest[:8],
        "big",
    )


def random_order(
    channel_count,
    key,
):
    cache_key = (
        channel_count,
        key,
    )

    cached = _RANDOM_ORDER_CACHE.get(
        cache_key
    )

    if cached is not None:
        return cached

    rng = np.random.default_rng(
        _seed_from_key(key)
    )

    order = rng.permutation(
        channel_count
    )

    # channel_count far below uint32 limit.
    order = order.astype(
        np.uint32,
        copy=False,
    )

    _RANDOM_ORDER_CACHE[
        cache_key
    ] = order

    return order


def embed_random(
    input_path,
    output_path,
    payload,
    depth,
    key,
):
    image = load_rgb(input_path)

    channels = image.reshape(-1)

    bits = payload_to_bits(payload)
    chunks = bits_to_chunks(
        bits,
        depth,
    )

    if len(chunks) > len(channels):
        raise ValueError(
            "Payload too large"
        )

    order = random_order(
        len(channels),
        key,
    )

    positions = order[
        :len(chunks)
    ]

    mask = np.uint8(
        0xFF ^ ((1 << depth) - 1)
    )

    channels[positions] = (
        channels[positions]
        & mask
    ) | chunks

    save_rgb(
        image,
        output_path,
    )


def extract_random(
    image_path,
    depth,
    key,
):
    image = load_rgb(image_path)

    channels = image.reshape(-1)

    order = random_order(
        len(channels),
        key,
    )

    ordered_channels = channels[
        order
    ]

    return extract_from_channels(
        ordered_channels,
        depth,
    )


# ============================================================
# ADAPTIVE
# ============================================================

def calculate_texture_scores(
    image_array,
    depth,
):
    stable_mask = np.uint8(
        0xFF ^ ((1 << depth) - 1)
    )

    stable = (
        image_array
        & stable_mask
    ).astype(
        np.float32,
        copy=False,
    )

    gray = (
        0.299 * stable[:, :, 0]
        + 0.587 * stable[:, :, 1]
        + 0.114 * stable[:, :, 2]
    ).astype(
        np.float32,
        copy=False,
    )

    mean = uniform_filter(
        gray,
        size=3,
        mode="reflect",
    )

    squared = gray * gray

    mean_squared = uniform_filter(
        squared,
        size=3,
        mode="reflect",
    )

    variance = (
        mean_squared
        - mean * mean
    )

    np.maximum(
        variance,
        0.0,
        out=variance,
    )

    return variance


def adaptive_pixel_order(
    image_array,
    depth,
):
    stable_mask = np.uint8(
        0xFF ^ ((1 << depth) - 1)
    )

    stable = (
        image_array
        & stable_mask
    )

    fingerprint = hashlib.blake2b(
        stable.tobytes(),
        digest_size=8,
    ).digest()

    cache_key = (
        image_array.shape,
        depth,
        fingerprint,
    )

    cached = _ADAPTIVE_ORDER_CACHE.get(
        cache_key
    )

    if cached is not None:
        return cached

    scores = calculate_texture_scores(
        image_array,
        depth,
    )

    flat_scores = scores.reshape(-1)

    # C implementation. No Python tuple list.
    order = np.argsort(
        -flat_scores,
        kind="stable",
    ).astype(
        np.uint32,
        copy=False,
    )

    _ADAPTIVE_ORDER_CACHE[
        cache_key
    ] = order

    return order


def adaptive_channel_order(
    image_array,
    depth,
):
    pixel_order = adaptive_pixel_order(
        image_array,
        depth,
    ).astype(
        np.uint64,
        copy=False,
    )

    base = (
        pixel_order * 3
    )

    result = np.empty(
        len(pixel_order) * 3,
        dtype=np.uint32,
    )

    result[0::3] = base
    result[1::3] = base + 1
    result[2::3] = base + 2

    return result


def embed_adaptive(
    input_path,
    output_path,
    payload,
    depth,
):
    image = load_rgb(input_path)

    channels = image.reshape(-1)

    bits = payload_to_bits(payload)

    chunks = bits_to_chunks(
        bits,
        depth,
    )

    if len(chunks) > len(channels):
        raise ValueError(
            "Payload too large"
        )

    order = adaptive_channel_order(
        image,
        depth,
    )

    positions = order[
        :len(chunks)
    ]

    mask = np.uint8(
        0xFF ^ ((1 << depth) - 1)
    )

    channels[positions] = (
        channels[positions]
        & mask
    ) | chunks

    save_rgb(
        image,
        output_path,
    )


def extract_adaptive(
    image_path,
    depth,
):
    image = load_rgb(
        image_path
    )

    channels = image.reshape(-1)

    order = adaptive_channel_order(
        image,
        depth,
    )

    ordered_channels = channels[
        order
    ]

    return extract_from_channels(
        ordered_channels,
        depth,
    )