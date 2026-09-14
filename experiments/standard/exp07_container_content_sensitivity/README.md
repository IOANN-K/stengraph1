# Experiment 07

Study of how image content affects 1-LSB steganographic distortion.

## Payload

`data/payload/text.txt`

## Container categories

- smooth light image
- smooth dark image
- textured natural image
- mixed photographic image
- artificial graphics

## Embedding methods

- sequential
- pseudorandom
- adaptive texture-based

## LSB depth

1 bit per RGB channel.

## Metrics

- decode success
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels
- container capacity usage

## Goal

Determine how image texture and visual structure affect the distortion caused by LSB embedding, and whether adaptive embedding provides greater benefits on some types of containers than others.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Adaptive benefit was strongest in textured content and weaker in smooth covers. Five selected images do not represent a population. The cross-content design is project-specific.
