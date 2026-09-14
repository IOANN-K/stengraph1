import numpy as np
from PIL import Image
from scipy.ndimage import (
    laplace,
    sobel,
    uniform_filter,
)


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


def payload_to_bits(payload):
    header = len(payload).to_bytes(
        4,
        "big",
    )

    data = np.frombuffer(
        header + payload,
        dtype=np.uint8,
    )

    return np.unpackbits(data)


def bits_to_payload(bits):
    header = np.packbits(
        bits[:32]
    ).tobytes()

    payload_length = int.from_bytes(
        header,
        "big",
    )

    payload_bits = bits[
        32:
        32 + payload_length * 8
    ]

    return np.packbits(
        payload_bits
    ).tobytes()[:payload_length]


def stable_gray(image_array):
    stable = (
        image_array
        & np.uint8(0b11111110)
    ).astype(
        np.float32,
        copy=False,
    )

    return (
        0.299 * stable[:, :, 0]
        + 0.587 * stable[:, :, 1]
        + 0.114 * stable[:, :, 2]
    ).astype(
        np.float32,
        copy=False,
    )


def variance_score(
    gray,
    window_size,
):
    mean = uniform_filter(
        gray,
        size=window_size,
        mode="reflect",
    )

    mean_sq = uniform_filter(
        gray * gray,
        size=window_size,
        mode="reflect",
    )

    variance = (
        mean_sq
        - mean * mean
    )

    np.maximum(
        variance,
        0,
        out=variance,
    )

    return variance


def gradient_score(gray):
    gx = sobel(
        gray,
        axis=1,
        mode="reflect",
    )

    gy = sobel(
        gray,
        axis=0,
        mode="reflect",
    )

    return np.hypot(
        gx,
        gy,
    )


def laplacian_score(gray):
    return np.abs(
        laplace(
            gray,
            mode="reflect",
        )
    )


def texture_score(
    image_array,
    metric,
    window_size,
):
    gray = stable_gray(
        image_array
    )

    if metric == "variance":
        return variance_score(
            gray,
            window_size,
        )

    if metric == "gradient":
        score = gradient_score(
            gray
        )

        if window_size > 1:
            score = uniform_filter(
                score,
                size=window_size,
                mode="reflect",
            )

        return score

    if metric == "laplacian":
        score = laplacian_score(
            gray
        )

        if window_size > 1:
            score = uniform_filter(
                score,
                size=window_size,
                mode="reflect",
            )

        return score

    raise ValueError(
        f"Unknown metric: {metric}"
    )


def pixel_order(
    image_array,
    metric,
    window_size,
):
    scores = texture_score(
        image_array,
        metric,
        window_size,
    )

    return np.argsort(
        -scores.reshape(-1),
        kind="stable",
    ).astype(
        np.uint32,
        copy=False,
    )


def channel_order(
    image_array,
    metric,
    window_size,
):
    pixels = pixel_order(
        image_array,
        metric,
        window_size,
    ).astype(
        np.uint64,
        copy=False,
    )

    base = pixels * 3

    order = np.empty(
        len(pixels) * 3,
        dtype=np.uint32,
    )

    order[0::3] = base
    order[1::3] = base + 1
    order[2::3] = base + 2

    return order


def embed_adaptive_variant(
    input_path,
    output_path,
    payload,
    metric,
    window_size,
):
    image = load_rgb(
        input_path
    )

    channels = image.reshape(-1)

    bits = payload_to_bits(
        payload
    )

    if len(bits) > len(channels):
        raise ValueError(
            "Payload too large"
        )

    order = channel_order(
        image,
        metric,
        window_size,
    )

    positions = order[
        :len(bits)
    ]

    channels[positions] = (
        channels[positions]
        & np.uint8(0b11111110)
    ) | bits

    save_rgb(
        image,
        output_path,
    )


def extract_adaptive_variant(
    image_path,
    metric,
    window_size,
):
    image = load_rgb(
        image_path
    )

    channels = image.reshape(-1)

    order = channel_order(
        image,
        metric,
        window_size,
    )

    ordered = channels[
        order
    ]

    header_bits = (
        ordered[:32]
        & 1
    ).astype(
        np.uint8
    )

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

    if total_bits > len(ordered):
        raise ValueError(
            "Payload length exceeds capacity"
        )

    bits = (
        ordered[:total_bits]
        & 1
    ).astype(
        np.uint8
    )

    return bits_to_payload(
        bits
    )