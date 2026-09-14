import csv
import hashlib
import zlib

from exp04_config import (
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
    KEY_FILE,
    METRICS_DIR,
    ensure_directories,
    read_payload,
)

from stengraph.embedding.legacy_exp01 import (
    embed_adaptive, embed_random, embed_sequential,
    extract_adaptive, extract_random, extract_sequential,
)
from stengraph.metrics.image_quality import (
    analyze_images,
    create_binary_difference_map,
)
from stengraph.preprocessing.crypto import (
    decrypt,
    encrypt,
    generate_key,
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


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def run():
    ensure_directories()

    original_payload = read_payload()
    original_hash = sha256(original_payload)

    key = generate_key()
    KEY_FILE.write_bytes(key)

    compressed = zlib.compress(
        original_payload,
        level=9,
    )

    encrypted = encrypt(
        original_payload,
        key,
    )

    compressed_encrypted = encrypt(
        compressed,
        key,
    )

    variants = {
        "raw": original_payload,
        "encrypted": encrypted,
        "compressed": compressed,
        "compressed_encrypted": compressed_encrypted,
    }

    print("Experiment 04")
    print(f"Original: {len(original_payload)} B")
    print(f"Encrypted: {len(encrypted)} B")
    print(f"Compressed: {len(compressed)} B")
    print(
        "Compressed + encrypted: "
        f"{len(compressed_encrypted)} B"
    )
    print()

    results = []

    for method, implementation in METHODS.items():
        for variant, embedded_payload in variants.items():
            name = f"{method}_{variant}"

            output_path = (
                IMAGES_DIR / f"{name}.png"
            )

            print(f"Embedding {name}...")

            implementation["embed"](
                INPUT_IMAGE,
                output_path,
                embedded_payload,
            )

            extracted = implementation["decode"](
                output_path
            )

            try:
                if variant == "raw":
                    recovered = extracted

                elif variant == "encrypted":
                    recovered = decrypt(
                        extracted,
                        key,
                    )

                elif variant == "compressed":
                    recovered = zlib.decompress(
                        extracted
                    )

                elif variant == "compressed_encrypted":
                    decrypted = decrypt(
                        extracted,
                        key,
                    )

                    recovered = zlib.decompress(
                        decrypted
                    )

                else:
                    raise ValueError(
                        f"Unknown variant: {variant}"
                    )

                transform_success = True

            except Exception:
                recovered = b""
                transform_success = False

            decode_success = (
                transform_success
                and recovered == original_payload
            )

            recovered_hash = sha256(
                recovered
            )

            metrics = analyze_images(
                INPUT_IMAGE,
                output_path,
            )

            create_binary_difference_map(
                INPUT_IMAGE,
                output_path,
                DIFF_DIR / f"{name}_binary.png",
            )

            size_ratio = (
                len(embedded_payload)
                / len(original_payload)
            )

            row = {
                "method": method,
                "variant": variant,
                "original_payload_bytes": (
                    len(original_payload)
                ),
                "embedded_payload_bytes": (
                    len(embedded_payload)
                ),
                "size_ratio": size_ratio,
                "size_change_percent": (
                    (size_ratio - 1.0) * 100
                ),
                "payload_sha256": original_hash,
                "decode_success": decode_success,
                "decoded_sha256": recovered_hash,
                "changed_pixels": (
                    metrics["changed_pixels"]
                ),
                "changed_pixels_percent": (
                    metrics[
                        "changed_pixels_percent"
                    ]
                ),
                "changed_channels": (
                    metrics["changed_channels"]
                ),
                "changed_channels_percent": (
                    metrics[
                        "changed_channels_percent"
                    ]
                ),
                "mse": metrics["mse"],
                "psnr": metrics["psnr"],
                "ssim": metrics["ssim"],
                "ssim_loss": (
                    1.0 - metrics["ssim"]
                ),
                "max_difference": (
                    metrics["max_difference"]
                ),
            }

            results.append(row)

            print(
                f"{name:<30} "
                f"{'PASS' if decode_success else 'FAIL'} | "
                f"{len(embedded_payload)} B | "
                f"PSNR={metrics['psnr']:.2f} | "
                f"SSIM={metrics['ssim']:.6f}"
            )

        print()

    output_csv = METRICS_DIR / "results.csv"

    fieldnames = [
        "method",
        "variant",
        "original_payload_bytes",
        "embedded_payload_bytes",
        "size_ratio",
        "size_change_percent",
        "payload_sha256",
        "decode_success",
        "decoded_sha256",
        "changed_pixels",
        "changed_pixels_percent",
        "changed_channels",
        "changed_channels_percent",
        "mse",
        "psnr",
        "ssim",
        "ssim_loss",
        "max_difference",
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
        writer.writerows(results)

    metadata = (
        f"container={INPUT_IMAGE.name}\n"
        f"payload=text.txt\n"
        f"original_payload_bytes={len(original_payload)}\n"
        f"encrypted_payload_bytes={len(encrypted)}\n"
        f"compressed_payload_bytes={len(compressed)}\n"
        f"compressed_encrypted_bytes={len(compressed_encrypted)}\n"
        f"payload_sha256={original_hash}\n"
        f"compression=zlib\n"
        f"compression_level=9\n"
        f"encryption=fernet\n"
        f"lsb=1\n"
    )

    (
        METRICS_DIR / "metadata.txt"
    ).write_text(
        metadata,
        encoding="utf-8",
    )

    print()
    print("Experiment completed.")
    print(f"Results: {output_csv}")


if __name__ == "__main__":
    run()
