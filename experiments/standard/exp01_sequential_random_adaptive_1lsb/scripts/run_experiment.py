from adaptive_lsb import (
    WINDOW_SIZE,
    embed_adaptive,
)
from analyze import (
    analyze_images,
    create_binary_difference_map,
    write_results_csv,
)
from common import (
    DIFF_DIR,
    IMAGES_DIR,
    INPUT_IMAGE,
    METRICS_DIR,
    calculate_sha256,
    ensure_directories,
    read_payload_bytes,
)
from random_lsb import (
    RANDOM_KEY,
    embed_random,
)
from sequential_lsb import embed_sequential
from verify import verify_payload


def run():
    ensure_directories()

    payload = read_payload_bytes()
    payload_sha256 = calculate_sha256(payload)

    outputs = {
        "sequential": (
            IMAGES_DIR / "sequential_1lsb.png"
        ),
        "random": (
            IMAGES_DIR / "random_1lsb.png"
        ),
        "adaptive": (
            IMAGES_DIR / "adaptive_1lsb.png"
        ),
    }

    print("Experiment 01")
    print(f"Container: {INPUT_IMAGE}")
    print(f"Payload bytes: {len(payload)}")
    print(f"Payload SHA-256: {payload_sha256}")
    print(f"Random key: {RANDOM_KEY}")
    print(
        f"Adaptive window: "
        f"{WINDOW_SIZE}x{WINDOW_SIZE}"
    )
    print()

    #
    # 1. EMBEDDING
    #

    print("Embedding sequential...")
    embed_sequential(
        INPUT_IMAGE,
        outputs["sequential"],
        payload,
    )

    print("Embedding random...")
    embed_random(
        INPUT_IMAGE,
        outputs["random"],
        payload,
    )

    print("Embedding adaptive...")
    embed_adaptive(
        INPUT_IMAGE,
        outputs["adaptive"],
        payload,
    )

    #
    # 2. VERIFY NEWLY GENERATED FILES
    #

    print()
    print("Verifying payload recovery...")

    verification = verify_payload(
        payload,
        outputs,
    )

    #
    # 3. IMAGE ANALYSIS
    #

    results = []

    for method, image_path in outputs.items():
        metrics = analyze_images(
            INPUT_IMAGE,
            image_path,
        )

        create_binary_difference_map(
            INPUT_IMAGE,
            image_path,
            DIFF_DIR / f"{method}_binary.png",
        )

        row = {
            "method": method,
            "payload_bytes": len(payload),
            "payload_sha256": payload_sha256,
            **verification[method],
            **metrics,
        }

        results.append(row)

        print()
        print(f"===== {method.upper()} =====")

        print(
            "Decode: "
            f"{'PASS' if verification[method]['decode_success'] else 'FAIL'}"
        )

        print(
            "Decoded bytes: "
            f"{verification[method]['decoded_bytes']}"
        )

        print(
            "Decoded SHA-256: "
            f"{verification[method]['decoded_sha256']}"
        )

        print(f"MSE: {metrics['mse']:.6f}")
        print(
            f"PSNR: {metrics['psnr']:.2f} dB"
        )
        print(
            f"SSIM: {metrics['ssim']:.6f}"
        )

        print(
            "Changed pixels: "
            f"{metrics['changed_pixels']} "
            f"({metrics['changed_pixels_percent']:.2f}%)"
        )

        print(
            "Changed channels: "
            f"{metrics['changed_channels']} "
            f"({metrics['changed_channels_percent']:.2f}%)"
        )

        print(
            "Max difference: "
            f"{metrics['max_difference']:.0f}"
        )

    #
    # 4. SAVE RESULTS
    #

    write_results_csv(
        results,
        METRICS_DIR / "results.csv",
    )

    metadata = (
        f"container={INPUT_IMAGE.name}\n"
        f"payload=text.txt\n"
        f"payload_bytes={len(payload)}\n"
        f"payload_sha256={payload_sha256}\n"
        f"lsb=1\n"
        f"random_key={RANDOM_KEY}\n"
        f"adaptive_window={WINDOW_SIZE}\n"
    )

    (
        METRICS_DIR / "metadata.txt"
    ).write_text(
        metadata,
        encoding="utf-8",
    )

    print()
    print("Experiment completed.")
    print(
        f"Results: "
        f"{METRICS_DIR / 'results.csv'}"
    )


if __name__ == "__main__":
    run()