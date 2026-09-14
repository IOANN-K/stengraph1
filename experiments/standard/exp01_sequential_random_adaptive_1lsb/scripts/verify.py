import hashlib

from decode_adaptive import extract_adaptive
from decode_random import extract_random
from decode_sequential import extract_sequential


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def verify_payload(
    original_payload,
    image_paths,
):
    original_hash = sha256(
        original_payload
    )

    decoders = {
        "sequential": extract_sequential,
        "random": extract_random,
        "adaptive": extract_adaptive,
    }

    results = {}

    for method, decoder in decoders.items():
        decoded = decoder(
            image_paths[method]
        )

        decoded_hash = sha256(decoded)

        success = (
            decoded == original_payload
        )

        results[method] = {
            "decode_success": success,
            "decoded_sha256": decoded_hash,
            "decoded_bytes": len(decoded),
        }

        status = (
            "PASS"
            if success
            else "FAIL"
        )

        print(
            f"{method:<10} "
            f"{status} "
            f"{decoded_hash}"
        )

    print()
    print(
        "Original SHA-256:",
        original_hash,
    )

    return results