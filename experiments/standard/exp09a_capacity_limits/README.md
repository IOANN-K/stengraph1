# Experiment 09a

Capacity limit study for 1-LSB image steganography.

## Container

`data/images/input2.png`

## LSB depth

1 LSB per RGB channel.

## Capacity levels

- 10%
- 25%
- 50%
- 75%
- 90%
- 100%

## Embedding methods

- sequential
- pseudorandom
- adaptive texture-based

## Payload

A deterministic pseudorandom high-entropy byte stream is used.

This avoids bias caused by repeating plaintext and approximates the bit distribution of compressed or encrypted payloads.

A 32-bit payload-length header is included in the capacity calculation.

## Metrics

- decode success
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels
- maximum channel difference

## Goal

Determine how close 1-LSB embedding can approach the theoretical capacity of the image while maintaining acceptable image quality.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Maximum payload was 1,585,148 B; all methods decoded at 100%, where ~50% of channels and ~87.5% of pixels changed. Synthetic high-entropy data limits real-payload interpretation; this is a project benchmark.
