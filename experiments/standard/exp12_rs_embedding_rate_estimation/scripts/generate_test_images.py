import hashlib

import numpy as np
from PIL import Image

from exp12_config import (
    IMAGES_DIR,
    INPUT_IMAGE,
    METHODS,
    RANDOM_KEY,
    TEST_RATES,
)


from stengraph.embedding.lsb import (
    embed_random,
    embed_sequential,
)
from stengraph.embedding.adaptive import embed_adaptive


def seed_from_rate(rate):
    digest = hashlib.sha256(
        f"stengraph-exp12-{rate}".encode()
    ).digest()

    return int.from_bytes(
        digest[:8],
        "big",
    )


def max_payload_bytes():
    image = Image.open(
        INPUT_IMAGE
    ).convert("RGB")

    channels = (
        image.width
        * image.height
        * 3
    )

    return (
        channels - 32
    ) // 8


def generate_payload(
    size,
    rate,
):
    rng = np.random.default_rng(
        seed_from_rate(rate)
    )

    return rng.integers(
        0,
        256,
        size=size,
        dtype=np.uint8,
    ).tobytes()


def run():
    maximum = max_payload_bytes()

    for rate in TEST_RATES:
        size = int(
            maximum
            * rate
            / 100
        )

        payload = generate_payload(
            size,
            rate,
        )

        for method in METHODS:
            output = (
                IMAGES_DIR
                / f"{rate:03d}_{method}.png"
            )

            if method == "sequential":
                embed_sequential(
                    INPUT_IMAGE,
                    output,
                    payload,
                    1,
                )

            elif method == "random":
                embed_random(
                    INPUT_IMAGE,
                    output,
                    payload,
                    1,
                    RANDOM_KEY,
                )

            else:
                embed_adaptive(
                    INPUT_IMAGE,
                    output,
                    payload,
                    1,
                )

            print(
                f"{rate:3d}% "
                f"{method:<10} "
                f"{size} bytes"
            )


if __name__ == "__main__":
    run()
