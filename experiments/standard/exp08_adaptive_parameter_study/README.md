# Experiment 08

Adaptive LSB parameter study.

## Container

`data/images/exp07/03_texture_nature.png`

## Payload

`data/payload/text.txt`

## LSB depth

1 LSB.

## Texture metrics

- local variance
- gradient magnitude
- Laplacian magnitude

## Window sizes

- 3x3
- 5x5
- 7x7
- 9x9

## Metrics

- decode success
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels

## Goal

Determine which texture metric and neighborhood size provide the best placement strategy for adaptive 1-LSB embedding.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Gradient 7×7 led with SSIM 0.9999819816 on this single textured image; it is not a universal optimum. The scores are literature-inspired project implementations.
