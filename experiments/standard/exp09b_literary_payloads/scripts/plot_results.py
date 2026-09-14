import csv

import matplotlib.pyplot as plt
from stengraph.io.csv_utils import load_csv_rows

from exp09b_config import (
    METRICS_DIR,
    PLOTS_DIR,
)


METHODS = [
    "sequential",
    "random",
    "adaptive",
]


def load_rows():
    return load_csv_rows(METRICS_DIR / "results.csv")


def embedded_rows(rows):
    return [
        row
        for row in rows
        if row["payload_status"] == "EMBEDDED"
    ]


def ordered_payloads(rows):
    names = []
    for row in rows:
        if row["payload_name"] not in names:
            names.append(row["payload_name"])
    return names


def plot_metric(rows, metric, ylabel, filename):
    rows = embedded_rows(rows)
    payloads = ordered_payloads(rows)

    plt.figure(figsize=(10, 6))

    x = list(range(len(payloads)))
    width = 0.25
    offsets = [-width, 0, width]

    for offset, method in zip(offsets, METHODS):
        method_rows = {
            row["payload_name"]: row
            for row in rows
            if row["method"] == method
        }

        xs = []
        ys = []

        for i, payload_name in enumerate(payloads):
            if payload_name not in method_rows:
                continue

            xs.append(i + offset)
            ys.append(float(method_rows[payload_name][metric]))

        plt.bar(xs, ys, width, label=method)

    plt.xticks(x, payloads, rotation=20, ha="right")
    plt.ylabel(ylabel)
    plt.title(ylabel)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        PLOTS_DIR / filename,
        dpi=160,
        bbox_inches="tight",
    )
    plt.close()


def plot_payload_sizes(rows):
    summary_rows = []
    seen = set()

    for row in rows:
        key = row["payload_name"]
        if key in seen:
            continue

        seen.add(key)
        summary_rows.append(row)

    payloads = [row["payload_name"] for row in summary_rows]
    sizes = [
        int(row["payload_bytes"]) if row["payload_bytes"] else 0
        for row in summary_rows
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(payloads, sizes)
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Payload size (bytes)")
    plt.title("Payload sizes")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        PLOTS_DIR / "payload_sizes.png",
        dpi=160,
        bbox_inches="tight",
    )
    plt.close()


def main():
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_rows()

    plot_payload_sizes(rows)
    plot_metric(rows, "capacity_used_percent", "Capacity used (%)", "capacity_used.png")
    plot_metric(rows, "psnr", "PSNR (dB)", "psnr.png")
    plot_metric(rows, "ssim", "SSIM", "ssim.png")
    plot_metric(rows, "ssim_loss", "SSIM loss", "ssim_loss.png")
    plot_metric(rows, "changed_pixels_percent", "Changed pixels (%)", "changed_pixels.png")

    print("Plots created.")


if __name__ == "__main__":
    main()
