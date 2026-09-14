import hashlib

import numpy as np
from PIL import Image

from exp13_config import (
    CONTAINERS,
    IMAGES_DIR,
    METHODS,
    RANDOM_KEY,
    TEST_RATES,
)


from stengraph.embedding.lsb import (
    embed_random,
    embed_sequential,
)
from stengraph.embedding.adaptive import embed_adaptive


def seed_from_case(
    container,
    rate,
):
    digest = hashlib.sha256(
        f"exp13-{container}-{rate}".encode()
    ).digest()

    return int.from_bytes(
        digest[:8],
        "big",
    )


def max_payload_bytes(path):
    image = Image.open(
        path
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
    container,
    rate,
):
    rng = np.random.default_rng(
        seed_from_case(
            container,
            rate,
        )
    )

    return rng.integers(
        0,
        256,
        size=size,
        dtype=np.uint8,
    ).tobytes()


def run():
    for container_name, image_path in CONTAINERS.items():
        maximum = max_payload_bytes(
            image_path
        )

        print(
            f"===== {container_name} ====="
        )

        for rate in TEST_RATES:
            size = int(
                maximum
                * rate
                / 100
            )

            payload = generate_payload(
                size,
                container_name,
                rate,
            )

            for method in METHODS:
                output = (
                    IMAGES_DIR
                    / (
                        f"{container_name}_"
                        f"{rate:03d}_"
                        f"{method}.png"
                    )
                )

                if method == "sequential":
                    embed_sequential(
                        image_path,
                        output,
                        payload,
                        1,
                    )

                elif method == "random":
                    embed_random(
                        image_path,
                        output,
                        payload,
                        1,
                        RANDOM_KEY,
                    )

                else:
                    embed_adaptive(
                        image_path,
                        output,
                        payload,
                        1,
                    )

                print(
                    f"{rate:3d}% "
                    f"{method:<10} "
                    f"{size} bytes"
                )

        print()


if __name__ == "__main__":
    run()
