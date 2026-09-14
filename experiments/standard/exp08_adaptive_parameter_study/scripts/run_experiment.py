import csv
import hashlib

from exp08_config import (
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
    METRICS_DIR,
    TEXTURE_METRICS,
    WINDOW_SIZES,
    ensure_directories,
    read_payload,
)

from stengraph.metrics.image_quality import (
    analyze_images,
    create_binary_difference_map,
)

from stengraph.embedding.adaptive import (
    embed_adaptive_variant,
    extract_adaptive_variant,
)


def sha256(data):
    return hashlib.sha256(
        data
    ).hexdigest()


def run():
    ensure_directories()

    payload = read_payload()
    payload_hash = sha256(
        payload
    )

    results = []

    print("Experiment 08")
    print(
        f"Container: {INPUT_IMAGE}"
    )
    print(
        f"Payload: {len(payload)} bytes"
    )
    print()

    for metric in TEXTURE_METRICS:
        for window_size in WINDOW_SIZES:
            name = (
                f"{metric}_"
                f"{window_size}x{window_size}"
            )

            print(
                f"Running {name}..."
            )

            output_path = (
                IMAGES_DIR
                / f"{name}.png"
            )

            embed_adaptive_variant(
                INPUT_IMAGE,
                output_path,
                payload,
                metric,
                window_size,
            )

            decoded = extract_adaptive_variant(
                output_path,
                metric,
                window_size,
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
                / f"{name}_binary.png",
            )

            row = {
                "texture_metric": metric,
                "window_size": (
                    window_size
                ),
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

            results.append(row)

            print(
                f"{name:<20} "
                f"{'PASS' if decode_success else 'FAIL'} | "
                f"PSNR={metrics['psnr']:.2f} | "
                f"SSIM={metrics['ssim']:.8f}"
            )

    output_csv = (
        METRICS_DIR / "results.csv"
    )

    fieldnames = [
        "texture_metric",
        "window_size",
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

    print()
    print("Experiment completed.")
    print(
        f"Results: {output_csv}"
    )


if __name__ == "__main__":
    run()
