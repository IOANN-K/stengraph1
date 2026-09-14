# Experiment 13

Generalization study for the RS-based embedding-rate estimator.

## Calibration

The estimator is calibrated only on `input2.png`
using Experiment 11 results.

## Test containers

- smooth light
- smooth dark
- textured natural image
- mixed photograph
- artificial graphics

## Unseen embedding rates

- 15%
- 35%
- 60%
- 85%

## Methods

- sequential
- pseudorandom
- adaptive

## Metrics

- estimated embedding rate
- absolute error
- mean absolute error (MAE)
- RS gap

## Goal

Determine whether an RS estimator calibrated on one image
can estimate LSB embedding rates in previously unseen image containers.

A large increase in error would indicate that the estimator
is container-specific rather than universally transferable.

## Stored result and limitation

Global MAE was 17.036951 pp sequential, 14.829468 pp random, and 13.075887 pp adaptive. The single-cover Exp12 calibration therefore did **not** generalize reliably. Per-cover behavior differed sharply; the `photo_mixed` image, identical to `input2.png`, remained unusually accurate. Five selected covers are insufficient for broad population claims.

Run `python3 scripts/generate_test_images.py`, then `python3 scripts/run_experiment.py` and `python3 scripts/plot_results.py` after package installation. Outputs include stego images, `results/metrics/results.csv`, and plots.

## Provenance

The RS concept is literature-established, while this cross-cover interpolation test is a project-specific extension.
