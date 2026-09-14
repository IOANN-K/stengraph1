import csv

from exp02_config import (
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
    METRICS_DIR,
    PAYLOAD_FRACTIONS,
    ensure_directories,
    read_payload,
    sha256,
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


def run():
    ensure_directories()

    full_payload = read_payload()

    print("Experiment 02")
    print(f"Container: {INPUT_IMAGE}")
    print(
        f"Full payload: {len(full_payload)} bytes"
    )
    print()

    results = []

    for fraction in PAYLOAD_FRACTIONS:
        payload_size = int(
            len(full_payload) * fraction
        )

        payload = full_payload[:payload_size]

        payload_hash = sha256(payload)

        percentage = int(
            fraction * 100
        )

        print(
            f"===== PAYLOAD {percentage}% "
            f"({payload_size} bytes) ====="
        )

        for method, implementation in METHODS.items():
            output_path = (
                IMAGES_DIR
                / f"{method}_{percentage}.png"
            )

            print(
                f"Embedding {method}..."
            )

            implementation["embed"](
                INPUT_IMAGE,
                output_path,
                payload,
            )

            decoded = implementation["decode"](
                output_path
            )

            decoded_hash = sha256(decoded)

            decode_success = (
                decoded == payload
            )

            metrics = analyze_images(
                INPUT_IMAGE,
                output_path,
            )

            diff_path = (
                DIFF_DIR
                / f"{method}_{percentage}_binary.png"
            )

            create_binary_difference_map(
                INPUT_IMAGE,
                output_path,
                diff_path,
            )

            row = {
                "method": method,
                "payload_fraction": fraction,
                "payload_percent": percentage,
                "payload_bytes": payload_size,
                "payload_sha256": payload_hash,
                "decode_success": decode_success,
                "decoded_sha256": decoded_hash,
                **metrics,
            }

            results.append(row)

            print(
                f"{method:<10} "
                f"{'PASS' if decode_success else 'FAIL'} | "
                f"PSNR={metrics['psnr']:.2f} | "
                f"SSIM={metrics['ssim']:.6f}"
            )

        print()

    output_csv = (
        METRICS_DIR / "results.csv"
    )

    fieldnames = [
        "method",
        "payload_fraction",
        "payload_percent",
        "payload_bytes",
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

    print("Experiment completed.")
    print(f"Results: {output_csv}")


if __name__ == "__main__":
    run()
