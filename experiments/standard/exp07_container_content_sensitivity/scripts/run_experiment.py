import csv
import hashlib

from PIL import Image

from exp07_config import (
    CONTAINERS,
    DIFF_DIR,
    IMAGES_DIR,
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
    return hashlib.sha256(
        data
    ).hexdigest()


def image_info(path):
    image = Image.open(path).convert("RGB")

    return {
        "width": image.width,
        "height": image.height,
        "pixels": image.width * image.height,
    }


def run():
    ensure_directories()

    payload = read_payload()
    payload_hash = sha256(payload)

    results = []

    print("Experiment 07")
    print(f"Payload: {len(payload)} bytes")
    print(f"SHA-256: {payload_hash}")
    print()

    for (
        container_name,
        input_path,
    ) in CONTAINERS.items():

        if not input_path.exists():
            print(
                f"SKIP {container_name}: "
                f"{input_path.name} not found"
            )
            continue

        info = image_info(input_path)

        capacity_bits = (
            info["pixels"] * 3
        )

        required_bits = (
            32 + len(payload) * 8
        )

        capacity_percent = (
            required_bits
            / capacity_bits
            * 100
        )

        print(
            f"===== {container_name.upper()} ====="
        )

        print(
            f"{info['width']}x{info['height']} | "
            f"capacity used={capacity_percent:.2f}%"
        )

        if required_bits > capacity_bits:
            print(
                "SKIP: payload does not fit"
            )
            print()
            continue

        for (
            method,
            implementation,
        ) in METHODS.items():

            output_path = (
                IMAGES_DIR
                / f"{container_name}_{method}.png"
            )

            implementation["embed"](
                input_path,
                output_path,
                payload,
            )

            decoded = implementation["decode"](
                output_path
            )

            decode_success = (
                decoded == payload
            )

            decoded_hash = sha256(
                decoded
            )

            metrics = analyze_images(
                input_path,
                output_path,
            )

            create_binary_difference_map(
                input_path,
                output_path,
                DIFF_DIR
                / (
                    f"{container_name}_"
                    f"{method}_binary.png"
                ),
            )

            row = {
                "container": container_name,
                "method": method,
                "width": info["width"],
                "height": info["height"],
                "pixels": info["pixels"],
                "payload_bytes": len(payload),
                "capacity_used_percent": (
                    capacity_percent
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
        "container",
        "method",
        "width",
        "height",
        "pixels",
        "payload_bytes",
        "capacity_used_percent",
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

    print("Experiment completed.")
    print(f"Results: {output_csv}")


if __name__ == "__main__":
    run()
