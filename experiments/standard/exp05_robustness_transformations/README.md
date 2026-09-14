# Experiment 05

Robustness of 1-LSB steganography under common image transformations.

## Container

`data/images/input2.png`

## Payload pipeline

`text.txt`

→ zlib compression

→ Fernet encryption

→ 1-LSB embedding

## Embedding methods

- sequential
- pseudorandom
- adaptive texture-based

## Transformations

- no transformation
- PNG resave
- PNG optimization
- resize to 75%
- 5% crop from each side
- PNG → JPEG quality 95 → PNG

## Verification

After each transformation:

1. extract the embedded data;
2. decrypt it;
3. decompress it;
4. compare it byte-for-byte with the original payload;
5. verify SHA-256.

## Goal

Determine which common image transformations preserve or destroy the hidden payload.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. PNG resave/optimization preserved all payloads; resize, crop, and JPEG roundtrip destroyed recovery. Conclusions apply only to these parameters. Robustness testing is project-specific.
