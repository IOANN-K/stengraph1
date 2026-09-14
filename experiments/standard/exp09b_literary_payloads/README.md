# Experiment 09B

Literary payload study for 1-LSB image steganography.

## Container

`data/images/input2.png`

## Payloads

- alice.txt
- jekyll_hyde.txt
- frankenstein.txt
- sherlock_holmes.txt
- moby_dick.txt
- war_and_peace.txt

## Embedding methods

- sequential
- pseudorandom
- adaptive texture-based

## LSB depth

1 LSB.

## Possible payload statuses

- EMPTY_PAYLOAD
- CAPACITY_EXCEEDED
- EMBEDDED

## Metrics

- payload size
- capacity used
- decode success
- MSE
- PSNR
- SSIM
- SSIM loss
- changed pixels
- changed channels

## Goal

Evaluate how real literary texts of different sizes affect image quality
and whether they fit into the selected PNG container.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Moby-Dick fit at 78.0737%; War and Peace exceeded capacity at 148.0367%. Texts differ in size/content, so this is illustrative rather than entropy-controlled.
