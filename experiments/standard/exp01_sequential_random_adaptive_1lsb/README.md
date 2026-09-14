# Experiment 01

Comparison of three 1-LSB embedding strategies:

- sequential
- pseudorandom
- adaptive texture-based

## Container

`data/images/input2.png`

## Payload

`data/payload/text.txt`

The same payload is used for all methods.

## Methods

### Sequential

Bits are embedded sequentially into RGB channels.

### Random

RGB channel positions are pseudorandomly shuffled using a fixed key.

### Adaptive

Pixels are ranked by local grayscale variance in a 3x3 neighborhood.
Payload bits are embedded starting from the most textured regions.

## Metrics

- MSE
- PSNR
- SSIM
- changed pixels
- changed channels
- maximum channel difference

## Results

Generated files are stored in `results/`.

Run `python3 scripts/run_experiment.py` and then `python3 scripts/plot_results.py` where available after package installation. Stored SSIM was 0.99939046 sequential, 0.99958437 random, and 0.99994969 adaptive. This one-cover comparison preserves the original Python permutation/variance semantics; adaptive ranking is literature-inspired and the comparison is project-specific.
