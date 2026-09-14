import hashlib

import numpy as np


SEED = b"stengraph-exp09-capacity-study"


def seed_to_uint64():
    digest = hashlib.sha256(
        SEED
    ).digest()

    return int.from_bytes(
        digest[:8],
        "big",
    )


def generate_payload(
    size_bytes,
):
    rng = np.random.default_rng(
        seed_to_uint64()
    )

    data = rng.integers(
        0,
        256,
        size=size_bytes,
        dtype=np.uint8,
    )

    return data.tobytes()