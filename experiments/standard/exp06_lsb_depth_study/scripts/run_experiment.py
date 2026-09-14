import csv
import hashlib

from exp06_config import (
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
    LSB_DEPTHS,
    METRICS_DIR,
    RANDOM_KEY,
    ensure_directories,
    read_payload,
)

from stengraph.metrics.image_quality import (
    analyze_images,
    create_binary_difference_map,
)

from stengraph.embedding.lsb import (
    embed_random, embed_sequential, extract_random, extract_sequential,
)
from stengraph.embedding.adaptive import (
    embed_adaptive,
    extract_adaptive,
)


def sha256(data):
    return hashlib.sha256(
        data
    ).hexdigest()


METHODS = {
    "sequential": (
        embed_sequential,
        extract_sequential,
    ),
    "random": (
        embed_random,
        extract_random,
    ),
    "adaptive": (
        embed_adaptive,
        extract_adaptive,
    ),
}


def run():
    ensure_directories()

    payload = read_payload()
    payload_hash = sha256(payload)

    results = []

    print("Experiment 06")
    print(
        f"Payload: {len(payload)} bytes"
    )
    print(
        f"SHA-256: {payload_hash}"
    )
    print()

    for depth in LSB_DEPTHS:
        print(
            f"===== {depth} LSB ====="
        )

        for method, (
            embedder,
            decoder,
        ) in METHODS.items():

            output_path = (
                IMAGES_DIR
                / f"{method}_{depth}lsb.png"
            )

            if method == "random":
                embedder(
                    INPUT_IMAGE,
                    output_path,
                    payload,
                    depth,
                    RANDOM_KEY,
                )

                decoded = decoder(
                    output_path,
                    depth,
                    RANDOM_KEY,
                )

            else:
                embedder(
                    INPUT_IMAGE,
                    output_path,
                    payload,
                    depth,
                )

                decoded = decoder(
                    output_path,
                    depth,
                )

            decode_success = (
                decoded == payload
            )

            decoded_hash = sha256(
                decoded
            )

            metrics = analyze_images(
                INPUT_IMAGE,
                output_path,
            )

            create_binary_difference_map(
                INPUT_IMAGE,
                output_path,
                DIFF_DIR
                / f"{method}_{depth}lsb_binary.png",
            )

            results.append(
                {
                    "method": method,
                    "lsb_depth": depth,
                    "payload_bytes": (
                        len(payload)
                    ),
                    "payload_sha256": (
                        payload_hash
                    ),
                    "decode_success": (
                        decode_success
                    ),
                    "decoded_sha256": (
                        decoded_hash
                    ),
                    "changed_pixels": (
                        metrics[
                            "changed_pixels"
                        ]
                    ),
                    "changed_pixels_percent": (
                        metrics[
                            "changed_pixels_percent"
                        ]
                    ),
                    "changed_channels": (
                        metrics[
                            "changed_channels"
                        ]
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
                        1.0
                        - metrics["ssim"]
                    ),
                    "max_difference": (
                        metrics[
                            "max_difference"
                        ]
                    ),
                }
            )

            print(
                f"{method:<10} "
                f"{'PASS' if decode_success else 'FAIL'} | "
                f"PSNR={metrics['psnr']:.2f} | "
                f"SSIM={metrics['ssim']:.6f} | "
                f"max={metrics['max_difference']:.0f}"
            )

        print()

    output_csv = (
        METRICS_DIR / "results.csv"
    )

    fieldnames = [
        "method",
        "lsb_depth",
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
        writer.writerows(
            results
        )

    print("Experiment completed.")
    print(
        f"Results: {output_csv}"
    )


if __name__ == "__main__":
    run()
