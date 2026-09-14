# Experiment 03

Comparison of raw and compressed payload embedding.

## Container

`data/images/input2.png`

## Payload

`data/payload/text.txt`

## Compression

The payload is compressed using zlib level 9 before embedding.

Two variants are compared:

- raw payload
- zlib-compressed payload

## Embedding methods

- sequential 1-LSB
- pseudorandom 1-LSB
- adaptive texture-based 1-LSB

## Verification

After extraction, compressed payloads are decompressed and compared
byte-for-byte with the original `text.txt`.

SHA-256 is also verified.

## Metrics

- embedded payload size
- compression ratio
- compression saving
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels
- maximum channel difference

## Goal

Determine whether compressing the payload before steganographic embedding
reduces image distortion while preserving complete payload recovery.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Stored payload size fell from 148,574 B to 53,408 B (64.05%), improving quality for all methods. Results are payload-specific; zlib is standard while this pipeline comparison is project-specific.
