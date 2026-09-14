import csv
import hashlib

from PIL import Image

from exp09b_config import (
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
    METRICS_DIR,
    PAYLOADS,
    RANDOM_KEY,
    ensure_directories,
)

from stengraph.embedding.lsb import (
    embed_random,
    embed_sequential,
    extract_random,
    extract_sequential,
)
from stengraph.embedding.adaptive import (
    embed_adaptive,
    extract_adaptive,
)
from stengraph.metrics.image_quality import (
    analyze_images,
    create_binary_difference_map,
)


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


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(path.read_bytes())


def get_capacity():
    image = Image.open(INPUT_IMAGE).convert("RGB")

    total_channels = image.width * image.height * 3
    total_capacity_bits = total_channels
    max_payload_bits = total_capacity_bits - 32
    max_payload_bytes = max_payload_bits // 8

    return {
        "width": image.width,
        "height": image.height,
        "channels": total_channels,
        "capacity_bits": total_capacity_bits,
        "max_payload_bytes": max_payload_bytes,
    }


def empty_metrics_row():
    return {
        "changed_pixels": "",
        "changed_pixels_percent": "",
        "changed_channels": "",
        "changed_channels_percent": "",
        "mse": "",
        "psnr": "",
        "ssim": "",
        "ssim_loss": "",
        "max_difference": "",
    }


def run():
    ensure_directories()

    capacity = get_capacity()

    print("Experiment 09B")
    print(f"Container: {capacity['width']}x{capacity['height']}")
    print(f"Max payload: {capacity['max_payload_bytes']} bytes")
    print()

    rows = []

    for payload_name, payload_path in PAYLOADS.items():
        if not payload_path.exists():
            print(f"===== {payload_name.upper()} =====")
            print("File not found")
            print()

            rows.append(
                {
                    "payload_name": payload_name,
                    "file_name": payload_path.name,
                    "payload_bytes": "",
                    "payload_sha256": "",
                    "capacity_used_percent": "",
                    "fits_container": False,
                    "payload_status": "FILE_NOT_FOUND",
                    "method": "",
                    "decode_success": "",
                    "decoded_sha256": "",
                    **empty_metrics_row(),
                }
            )
            continue

        payload = payload_path.read_bytes()
        payload_bytes = len(payload)
        payload_hash = sha256_bytes(payload)

        print(f"===== {payload_name.upper()} =====")
        print(f"Bytes: {payload_bytes}")
        print(f"SHA-256: {payload_hash}")

        if payload_bytes == 0:
            print("Status: EMPTY_PAYLOAD")
            print()

            rows.append(
                {
                    "payload_name": payload_name,
                    "file_name": payload_path.name,
                    "payload_bytes": payload_bytes,
                    "payload_sha256": payload_hash,
                    "capacity_used_percent": 0.0,
                    "fits_container": False,
                    "payload_status": "EMPTY_PAYLOAD",
                    "method": "",
                    "decode_success": "",
                    "decoded_sha256": "",
                    **empty_metrics_row(),
                }
            )
            continue

        required_bits = 32 + payload_bytes * 8
        capacity_used_percent = (
            required_bits / capacity["capacity_bits"] * 100
        )
        fits_container = payload_bytes <= capacity["max_payload_bytes"]

        print(f"Capacity used: {capacity_used_percent:.2f}%")

        if not fits_container:
            print("Status: CAPACITY_EXCEEDED")
            print()

            rows.append(
                {
                    "payload_name": payload_name,
                    "file_name": payload_path.name,
                    "payload_bytes": payload_bytes,
                    "payload_sha256": payload_hash,
                    "capacity_used_percent": capacity_used_percent,
                    "fits_container": False,
                    "payload_status": "CAPACITY_EXCEEDED",
                    "method": "",
                    "decode_success": "",
                    "decoded_sha256": "",
                    **empty_metrics_row(),
                }
            )
            continue

        print("Status: EMBEDDING")

        for method, (embedder, decoder) in METHODS.items():
            output_path = IMAGES_DIR / f"{payload_name}_{method}.png"

            if method == "random":
                embedder(
                    INPUT_IMAGE,
                    output_path,
                    payload,
                    1,
                    RANDOM_KEY,
                )

                decoded = decoder(
                    output_path,
                    1,
                    RANDOM_KEY,
                )
            else:
                embedder(
                    INPUT_IMAGE,
                    output_path,
                    payload,
                    1,
                )

                decoded = decoder(
                    output_path,
                    1,
                )

            decode_success = decoded == payload
            decoded_hash = sha256_bytes(decoded)

            metrics = analyze_images(
                INPUT_IMAGE,
                output_path,
            )

            create_binary_difference_map(
                INPUT_IMAGE,
                output_path,
                DIFF_DIR / f"{payload_name}_{method}_binary.png",
            )

            rows.append(
                {
                    "payload_name": payload_name,
                    "file_name": payload_path.name,
                    "payload_bytes": payload_bytes,
                    "payload_sha256": payload_hash,
                    "capacity_used_percent": capacity_used_percent,
                    "fits_container": True,
                    "payload_status": "EMBEDDED",
                    "method": method,
                    "decode_success": decode_success,
                    "decoded_sha256": decoded_hash,
                    "changed_pixels": metrics["changed_pixels"],
                    "changed_pixels_percent": metrics["changed_pixels_percent"],
                    "changed_channels": metrics["changed_channels"],
                    "changed_channels_percent": metrics["changed_channels_percent"],
                    "mse": metrics["mse"],
                    "psnr": metrics["psnr"],
                    "ssim": metrics["ssim"],
                    "ssim_loss": 1.0 - metrics["ssim"],
                    "max_difference": metrics["max_difference"],
                }
            )

            print(
                f"{method:<10} "
                f"{'PASS' if decode_success else 'FAIL'} | "
                f"PSNR={metrics['psnr']:.2f} | "
                f"SSIM={metrics['ssim']:.6f} | "
                f"changed={metrics['changed_pixels_percent']:.2f}%"
            )

        print()

    output_csv = METRICS_DIR / "results.csv"

    fieldnames = [
        "payload_name",
        "file_name",
        "payload_bytes",
        "payload_sha256",
        "capacity_used_percent",
        "fits_container",
        "payload_status",
        "method",
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
        writer.writerows(rows)

    print("Experiment completed.")
    print(f"Results: {output_csv}")


if __name__ == "__main__":
    run()
