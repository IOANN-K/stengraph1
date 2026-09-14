import csv
import hashlib

from PIL import Image

from exp09_config import (
    CAPACITY_FRACTIONS,
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
    METRICS_DIR,
    RANDOM_KEY,
    ensure_directories,
)

from payload_generator import (
    generate_payload,
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


def sha256(data):
    return hashlib.sha256(
        data
    ).hexdigest()


def get_capacity():
    image = Image.open(
        INPUT_IMAGE
    ).convert("RGB")

    total_channels = (
        image.width
        * image.height
        * 3
    )

    total_capacity_bits = (
        total_channels
    )

    header_bits = 32

    max_payload_bits = (
        total_capacity_bits
        - header_bits
    )

    max_payload_bytes = (
        max_payload_bits // 8
    )

    return {
        "width": image.width,
        "height": image.height,
        "channels": total_channels,
        "capacity_bits": total_capacity_bits,
        "max_payload_bytes": max_payload_bytes,
    }


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

    capacity = get_capacity()

    max_payload_bytes = capacity[
        "max_payload_bytes"
    ]

    print("Experiment 09")
    print(
        f"Container: "
        f"{capacity['width']}x"
        f"{capacity['height']}"
    )

    print(
        f"RGB channels: "
        f"{capacity['channels']}"
    )

    print(
        f"Maximum payload: "
        f"{max_payload_bytes} bytes"
    )

    print()

    master_payload = generate_payload(
        max_payload_bytes
    )

    results = []

    for fraction in CAPACITY_FRACTIONS:
        requested_bytes = int(
            max_payload_bytes
            * fraction
        )

        if fraction == 1.0:
            requested_bytes = (
                max_payload_bytes
            )

        payload = master_payload[
            :requested_bytes
        ]

        payload_hash = sha256(
            payload
        )

        fraction_percent = int(
            fraction * 100
        )

        actual_capacity_percent = (
            (
                32
                + len(payload) * 8
            )
            / capacity[
                "capacity_bits"
            ]
            * 100
        )

        print(
            f"===== "
            f"{fraction_percent}% CAPACITY "
            f"====="
        )

        print(
            f"Payload: "
            f"{len(payload)} bytes | "
            f"actual="
            f"{actual_capacity_percent:.4f}%"
        )

        for (
            method,
            (
                embedder,
                decoder,
            ),
        ) in METHODS.items():

            output_path = (
                IMAGES_DIR
                / (
                    f"{fraction_percent:03d}_"
                    f"{method}.png"
                )
            )

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

            success = (
                decoded == payload
            )

            decoded_hash = sha256(
                decoded
            )

            metrics = analyze_images(
                INPUT_IMAGE,
                output_path,
            )

            diff_path = (
                DIFF_DIR
                / (
                    f"{fraction_percent:03d}_"
                    f"{method}_binary.png"
                )
            )

            create_binary_difference_map(
                INPUT_IMAGE,
                output_path,
                diff_path,
            )

            results.append(
                {
                    "capacity_target_percent": (
                        fraction_percent
                    ),
                    "capacity_actual_percent": (
                        actual_capacity_percent
                    ),
                    "method": method,
                    "payload_bytes": (
                        len(payload)
                    ),
                    "max_payload_bytes": (
                        max_payload_bytes
                    ),
                    "payload_sha256": (
                        payload_hash
                    ),
                    "decode_success": (
                        success
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
                    "mse": (
                        metrics["mse"]
                    ),
                    "psnr": (
                        metrics["psnr"]
                    ),
                    "ssim": (
                        metrics["ssim"]
                    ),
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
                f"{'PASS' if success else 'FAIL'} | "
                f"PSNR="
                f"{metrics['psnr']:.2f} | "
                f"SSIM="
                f"{metrics['ssim']:.6f} | "
                f"changed="
                f"{metrics['changed_pixels_percent']:.2f}%"
            )

        print()

    output_csv = (
        METRICS_DIR
        / "results.csv"
    )

    fieldnames = [
        "capacity_target_percent",
        "capacity_actual_percent",
        "method",
        "payload_bytes",
        "max_payload_bytes",
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

    print(
        "Experiment completed."
    )

    print(
        f"Results: {output_csv}"
    )


if __name__ == "__main__":
    run()
