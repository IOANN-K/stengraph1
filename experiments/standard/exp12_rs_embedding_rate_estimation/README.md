# Experiment 12 — Empirically Calibrated RS Rate Estimation

## Research question

Can the RS gap estimate unseen embedding rates when calibration and testing use the same `input2.png` cover?

## Inputs and methods

Exp11 stored RS results provide known calibration pairs (rate, mean positive-mask RS gap). Sequential, random, and adaptive stego images are tested at 15%, 35%, 60%, and 85%. Monotonic interpolation maps an observed gap to a clipped 0–100% estimate. This is not canonical closed-form RS message-length estimation.

## Outputs and metrics

`results/metrics/results.csv` stores method, true/estimated rate, absolute error, and RS gap; `results/plots/` visualizes estimates and errors. Run `python3 scripts/generate_test_images.py`, then `python3 scripts/run_experiment.py` and `python3 scripts/plot_results.py` from this experiment directory (or use their repository-relative paths after package installation).

## Result and interpretation

Stored MAE is 1.023768 pp sequential, 0.276409 pp random, and 1.119612 pp adaptive. Accuracy is excellent only within this same-container calibration regime.

## Limitations and provenance

The calibration cover and test cover are identical; content transfer is not tested until Exp13. The interpolation estimator is a project-specific extension inspired by quantitative steganalysis, while the underlying RS concept is literature-established and the repository implementation is exploratory.
