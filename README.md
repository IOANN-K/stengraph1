# stengraph

`stengraph` is an educational research repository for PNG least-significant-bit (LSB) steganography, image-quality measurement, and basic steganalysis. It is not a production secure steganographic system. The completed program ends at Exp15; Exp09 is split into 09A and 09B.

## Research questions

The experiments compare sequential, pseudorandom, and texture-adaptive placement; payload size, compression, encryption, transformations, LSB depth, cover content, and capacity; and whether statistical, RS, and regression estimators detect or quantify embedding across unseen containers.

## Repository structure

- `src/stengraph/`: reusable scientific code.
- `data/`: cover images and payloads; `data/payload/text.txt` is canonical.
- `experiments/legacy/`: preserved exploratory work and outputs.
- `experiments/standard/`: Exp01–Exp15 definitions and recorded results.
- `docs/`, `tests/`, `checksums/`: documentation, focused tests, and integrity manifests.

## Installation

The validated environment is Python 3.14.2.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

For tests, install `python3 -m pip install -e '.[dev]'`. Exact validated versions are in `requirements-lock.txt`.

## Reproducibility and data

Synthetic payloads and placement use documented fixed seeds/keys. Exp01 preserves its historical `random.Random` permutation; later vectorized experiments use NumPy permutation. Fernet ciphertext is intentionally randomized and is not byte-identical from the key alone. `input2.png` is the main cover; Exp07 adds five varied covers. Exp09B uses six public-domain texts. Existing outputs are historical records and must not be casually overwritten. See [Reproducibility](docs/REPRODUCIBILITY.md).

## Experiment index

| ID | Main question | Key measure | Headline conclusion |
|---|---|---|---|
| [01](experiments/standard/exp01_sequential_random_adaptive_1lsb/README.md) | Placement | SSIM | Adaptive preserved structure best. |
| [02](experiments/standard/exp02_payload_size_vs_quality/README.md) | Payload size | quality | Distortion rose with load. |
| [03](experiments/standard/exp03_compression_before_embedding/README.md) | Compression | bytes/SSIM | 148,574 B compressed to 53,408 B. |
| [04](experiments/standard/exp04_encryption_and_compression/README.md) | Compression + Fernet | size/SSIM | Compress-then-encrypt balanced size/confidentiality. |
| [05](experiments/standard/exp05_robustness_transformations/README.md) | Robustness | recovery | PNG survived; resize/crop/JPEG did not. |
| [06](experiments/standard/exp06_lsb_depth_study/README.md) | Depth 1–4 | quality | Distortion rose; max error was 1, 3, 7, 15. |
| [07](experiments/standard/exp07_container_content_sensitivity/README.md) | Cover content | SSIM | Adaptive benefit depended on texture. |
| [08](experiments/standard/exp08_adaptive_parameter_study/README.md) | Adaptive parameters | SSIM | Gradient 7×7 led on one cover only. |
| [09A](experiments/standard/exp09a_capacity_limits/README.md) | Capacity limit | recovery | All methods decoded at 100%; advantage vanished. |
| [09B](experiments/standard/exp09b_literary_payloads/README.md) | Literary payloads | fit | Moby-Dick fit; War and Peace did not. |
| [10](experiments/standard/exp10_basic_steganalysis/README.md) | Basic statistics | chi-square | Statistics randomized with load. |
| [11](experiments/standard/exp11_rs_analysis/README.md) | Exploratory RS | RS gap | Gap approached zero near full embedding. |
| [12](experiments/standard/exp12_rs_embedding_rate_estimation/README.md) | Same-cover estimation | MAE | Accurate within its calibration regime. |
| [13](experiments/standard/exp13_rs_generalization/README.md) | Calibration transfer | MAE | Single-cover calibration generalized poorly. |
| [14](experiments/standard/exp14_cross_container_rs_estimator/README.md) | RS regression | MAE | Random+Ridge led on a tiny dataset. |
| [15](experiments/standard/exp15_hybrid_steganalysis/README.md) | Hybrid features | MAE | More features worsened generalization. |

## Main findings and provenance

Adaptive placement can improve structural similarity at moderate loads and in textured covers, but the advantage is cover-dependent and disappears near capacity. Compression reduces distortion; raw LSB is fragile under geometric/lossy processing. Same-cover estimation can be accurate while cross-cover estimation remains difficult; Exp13 and Exp15 are valid negative results.

LSB substitution, PSNR, SSIM, chi-square concepts, and RS concepts are literature-established. The exact adaptive rankings, simplified Pair-of-Values-style statistic, and clipped RS code are literature-inspired project implementations. The experiment sequence and empirical estimators are project-specific extensions. See [Methodology](docs/METHODOLOGY.md), [Results](docs/RESULTS.md), and [References](docs/REFERENCES.md).

## Running and limitations

After editable installation, existing commands remain valid, for example:

```bash
python3 experiments/standard/exp12_rs_embedding_rate_estimation/scripts/run_experiment.py
```

Runners may overwrite outputs; use a copy when regeneration is intended. Validate with `pytest` and `python3 scripts/validate_repository.py`. The cover set and ML datasets are small; Exp08 is cover-specific; Exp11 is exploratory; Exp12 is same-cover interpolation; conclusions are observations, not population-level proof.
