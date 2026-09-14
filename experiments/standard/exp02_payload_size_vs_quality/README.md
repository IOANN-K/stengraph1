# Experiment 02

Study of the relationship between payload size and image quality.

## Container

`data/images/input2.png`

## Payload

`data/payload/text.txt`

Fractions tested:

- 10%
- 25%
- 50%
- 75%
- 100%

## Methods

- sequential 1-LSB
- pseudorandom 1-LSB
- adaptive texture-based 1-LSB

## Metrics

- MSE
- PSNR
- SSIM
- changed pixels
- changed channels
- payload recovery

## Goal

Determine how increasing payload size affects image distortion and compare the three embedding strategies under identical conditions.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Outputs are images, binary maps, metric CSV, and plots under `results/`. Distortion rose with load and adaptive SSIM was stronger at lower/moderate loads. One cover and payload limit generality; the load comparison is project-specific.
