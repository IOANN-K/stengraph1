import csv
import hashlib
import zlib

from cryptography.fernet import InvalidToken
from PIL import Image

from exp05_config import (
    BASELINE_DIR,
    INPUT_IMAGE,
    KEY_FILE,
    METRICS_DIR,
    TRANSFORMED_DIR,
    ensure_directories,
    read_payload,
)

from stengraph.embedding.legacy_exp01 import (
    embed_adaptive, embed_random, embed_sequential,
    extract_adaptive, extract_random, extract_sequential,
)
from stengraph.preprocessing.crypto import (
    decrypt,
    encrypt,
    generate_key,
)

from stengraph.preprocessing.transformations import (
    crop_image,
    jpeg_roundtrip,
    optimize_png,
    resave_png,
    resize_image,
)


METHODS = {
    "sequential": {
        "embed": embed_sequential,
        "decode": extract_sequential,
    },
    "random": {
        "embed": embed_random,
        "decode": extract_random,
    },
    "adaptive": {
        "embed": embed_adaptive,
        "decode": extract_adaptive,
    },
}


TRANSFORMATIONS = {
    "resave": resave_png,
    "optimize": optimize_png,
    "resize": resize_image,
    "crop": crop_image,
    "jpeg_roundtrip": jpeg_roundtrip,
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def recover_payload(
    decoder,
    image_path,
    key,
    original_payload,
):
    try:
        extracted = decoder(image_path)

        extracted_bytes = len(extracted)

        decrypted = decrypt(
            extracted,
            key,
        )

        recovered = zlib.decompress(
            decrypted
        )

        success = (
            recovered == original_payload
        )

        return {
            "decode_success": success,
            "extracted_bytes": extracted_bytes,
            "recovered_bytes": len(recovered),
            "decoded_sha256": sha256(recovered),
            "error": "",
        }

    except (
        InvalidToken,
        zlib.error,
        ValueError,
        IndexError,
        OverflowError,
        MemoryError,
    ) as error:
        return {
            "decode_success": False,
            "extracted_bytes": 0,
            "recovered_bytes": 0,
            "decoded_sha256": "",
            "error": type(error).__name__,
        }

    except Exception as error:
        return {
            "decode_success": False,
            "extracted_bytes": 0,
            "recovered_bytes": 0,
            "decoded_sha256": "",
            "error": type(error).__name__,
        }


def image_info(path):
    image = Image.open(path)

    return {
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "file_bytes": path.stat().st_size,
    }


def run():
    ensure_directories()

    original_payload = read_payload()
    original_hash = sha256(original_payload)

    compressed = zlib.compress(
        original_payload,
        level=9,
    )

    key = generate_key()
    KEY_FILE.write_bytes(key)

    embedded_payload = encrypt(
        compressed,
        key,
    )

    print("Experiment 05")
    print(f"Container: {INPUT_IMAGE}")
    print(
        f"Original payload: "
        f"{len(original_payload)} bytes"
    )
    print(
        f"Compressed: "
        f"{len(compressed)} bytes"
    )
    print(
        f"Encrypted embedded payload: "
        f"{len(embedded_payload)} bytes"
    )
    print(
        f"Payload SHA-256: "
        f"{original_hash}"
    )
    print()

    rows = []

    for method, implementation in METHODS.items():
        print(
            f"===== {method.upper()} ====="
        )

        baseline_path = (
            BASELINE_DIR
            / f"{method}.png"
        )

        print("Creating baseline...")

        implementation["embed"](
            INPUT_IMAGE,
            baseline_path,
            embedded_payload,
        )

        #
        # BASELINE
        #

        baseline_recovery = recover_payload(
            implementation["decode"],
            baseline_path,
            key,
            original_payload,
        )

        info = image_info(
            baseline_path
        )

        rows.append(
            {
                "method": method,
                "transformation": "none",
                "decode_success": (
                    baseline_recovery[
                        "decode_success"
                    ]
                ),
                "original_payload_bytes": (
                    len(original_payload)
                ),
                "embedded_payload_bytes": (
                    len(embedded_payload)
                ),
                "extracted_bytes": (
                    baseline_recovery[
                        "extracted_bytes"
                    ]
                ),
                "recovered_bytes": (
                    baseline_recovery[
                        "recovered_bytes"
                    ]
                ),
                "payload_sha256": (
                    original_hash
                ),
                "decoded_sha256": (
                    baseline_recovery[
                        "decoded_sha256"
                    ]
                ),
                "error": (
                    baseline_recovery[
                        "error"
                    ]
                ),
                "width": info["width"],
                "height": info["height"],
                "mode": info["mode"],
                "file_bytes": (
                    info["file_bytes"]
                ),
            }
        )

        print(
            "baseline: "
            f"{'PASS' if baseline_recovery['decode_success'] else 'FAIL'}"
        )

        #
        # TRANSFORMATIONS
        #

        for (
            transformation_name,
            transformation_function,
        ) in TRANSFORMATIONS.items():

            output_path = (
                TRANSFORMED_DIR
                / transformation_name
                / f"{method}.png"
            )

            print(
                f"{transformation_name}..."
            )

            transformation_function(
                baseline_path,
                output_path,
            )

            recovery = recover_payload(
                implementation["decode"],
                output_path,
                key,
                original_payload,
            )

            info = image_info(
                output_path
            )

            rows.append(
                {
                    "method": method,
                    "transformation": (
                        transformation_name
                    ),
                    "decode_success": (
                        recovery[
                            "decode_success"
                        ]
                    ),
                    "original_payload_bytes": (
                        len(original_payload)
                    ),
                    "embedded_payload_bytes": (
                        len(embedded_payload)
                    ),
                    "extracted_bytes": (
                        recovery[
                            "extracted_bytes"
                        ]
                    ),
                    "recovered_bytes": (
                        recovery[
                            "recovered_bytes"
                        ]
                    ),
                    "payload_sha256": (
                        original_hash
                    ),
                    "decoded_sha256": (
                        recovery[
                            "decoded_sha256"
                        ]
                    ),
                    "error": (
                        recovery[
                            "error"
                        ]
                    ),
                    "width": info["width"],
                    "height": info["height"],
                    "mode": info["mode"],
                    "file_bytes": (
                        info["file_bytes"]
                    ),
                }
            )

            print(
                f"{transformation_name}: "
                f"{'PASS' if recovery['decode_success'] else 'FAIL'}"
                + (
                    ""
                    if not recovery["error"]
                    else f" ({recovery['error']})"
                )
            )

        print()

    output_csv = (
        METRICS_DIR / "results.csv"
    )

    fieldnames = [
        "method",
        "transformation",
        "decode_success",
        "original_payload_bytes",
        "embedded_payload_bytes",
        "extracted_bytes",
        "recovered_bytes",
        "payload_sha256",
        "decoded_sha256",
        "error",
        "width",
        "height",
        "mode",
        "file_bytes",
    ]

    with open(
        output_csv,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    metadata = (
        f"container={INPUT_IMAGE.name}\n"
        f"payload=text.txt\n"
        f"payload_sha256={original_hash}\n"
        f"original_payload_bytes="
        f"{len(original_payload)}\n"
        f"compressed_payload_bytes="
        f"{len(compressed)}\n"
        f"embedded_payload_bytes="
        f"{len(embedded_payload)}\n"
        f"compression=zlib\n"
        f"compression_level=9\n"
        f"encryption=fernet\n"
        f"lsb=1\n"
        f"resize_scale=0.75\n"
        f"crop_margin_percent=5\n"
        f"jpeg_quality=95\n"
    )

    (
        METRICS_DIR / "metadata.txt"
    ).write_text(
        metadata,
        encoding="utf-8",
    )

    print("Experiment completed.")
    print(f"Results: {output_csv}")


if __name__ == "__main__":
    run()
