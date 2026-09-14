import csv
import hashlib
import zlib

from exp03_config import (
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
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

    compressed_payload = zlib.compress(
        original_payload,
        level=9,
    )

    compression_ratio = (
        len(compressed_payload)
        / len(original_payload)
    )

    compression_saving = (
        1.0 - compression_ratio
    ) * 100

    print("Experiment 03")
    print(f"Container: {INPUT_IMAGE}")
    print(
        f"Original payload: "
        f"{len(original_payload)} bytes"
    )
    print(
        f"Compressed payload: "
        f"{len(compressed_payload)} bytes"
    )
    print(
        f"Compression ratio: "
        f"{compression_ratio:.4f}"
    )
    print(
        f"Space saving: "
        f"{compression_saving:.2f}%"
    )
    print(
        f"Original SHA-256: "
        f"{original_hash}"
    )
    print()

    variants = {
        "raw": original_payload,
        "zlib": compressed_payload,
    }

    results = []

    for method, implementation in METHODS.items():
        for compression, embedded_payload in variants.items():
            variant_name = (
                f"{method}_{compression}"
            )

            output_path = (
                IMAGES_DIR
                / f"{variant_name}.png"
            )

            print(
                f"Embedding {variant_name}..."
            )

            implementation["embed"](
                INPUT_IMAGE,
                output_path,
                embedded_payload,
            )

            extracted = implementation["decode"](
                output_path
            )

            if compression == "zlib":
                try:
                    recovered_payload = (
                        zlib.decompress(
                            extracted
                        )
                    )

                    decompression_success = True

                except zlib.error:
                    recovered_payload = b""
                    decompression_success = False

            else:
                recovered_payload = extracted
                decompression_success = True

            recovered_hash = sha256(
                recovered_payload
            )

            decode_success = (
                decompression_success
                and recovered_payload
                == original_payload
            )

            metrics = analyze_images(
                INPUT_IMAGE,
                output_path,
            )

            create_binary_difference_map(
                INPUT_IMAGE,
                output_path,
                DIFF_DIR
                / f"{variant_name}_binary.png",
            )

            if compression == "zlib":
                embedded_size = len(
                    compressed_payload
                )
                ratio = compression_ratio
            else:
                embedded_size = len(
                    original_payload
                )
                ratio = 1.0

            row = {
                "method": method,
                "compression": compression,
                "original_payload_bytes": (
                    len(original_payload)
                ),
                "embedded_payload_bytes": (
                    embedded_size
                ),
                "compression_ratio": ratio,
                "compression_saving_percent": (
                    (1.0 - ratio) * 100
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
                f"{variant_name:<20} "
                f"{'PASS' if decode_success else 'FAIL'} | "
                f"embedded={embedded_size} B | "
                f"PSNR={metrics['psnr']:.2f} | "
                f"SSIM={metrics['ssim']:.6f}"
            )

        print()

    output_csv = (
        METRICS_DIR / "results.csv"
    )

    fieldnames = [
        "method",
        "compression",
        "original_payload_bytes",
        "embedded_payload_bytes",
        "compression_ratio",
        "compression_saving_percent",
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
        f"original_payload_bytes="
        f"{len(original_payload)}\n"
        f"compressed_payload_bytes="
        f"{len(compressed_payload)}\n"
        f"compression=zlib\n"
        f"compression_level=9\n"
        f"compression_ratio="
        f"{compression_ratio}\n"
        f"compression_saving_percent="
        f"{compression_saving}\n"
        f"payload_sha256="
        f"{original_hash}\n"
        f"lsb=1\n"
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
