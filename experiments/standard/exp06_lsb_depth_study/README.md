# Experiment 06

Standardized study of LSB depth.

## Container

`data/images/input2.png`

## Payload

`data/payload/text.txt`

## LSB depths

- 1
- 2
- 3
- 4

## Embedding methods

- sequential
- pseudorandom
- adaptive texture-based

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

Measure the trade-off between LSB depth, embedding capacity and visual distortion under standardized conditions.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Distortion rose with depth; adaptive retained strongest SSIM and maximum differences were 1, 3, 7, 15. One cover limits generality. LSB replacement is established; adaptive ranking is literature-inspired.
