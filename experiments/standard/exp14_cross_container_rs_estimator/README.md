# Experiment 14

Cross-container RS embedding-rate estimation.

## Goal

Evaluate whether multiple RS features can estimate LSB embedding rate
for a completely unseen image container.

## Dataset

Stego images generated in Experiment 13.

Containers:

- smooth light
- smooth dark
- textured nature
- mixed photograph
- graphics

Embedding rates:

- 15%
- 35%
- 60%
- 85%

Embedding methods:

- sequential
- pseudorandom
- adaptive

## Validation

Leave-one-container-out cross-validation.

For every fold:

- four containers are used for training;
- one complete container is held out;
- the held-out container is never used during model fitting.

## Features

RS statistics include:

- R_m
- S_m
- R_-m
- S_-m
- positive and negative RS gaps
- gap ratio
- R and S differences
- per-channel RS gaps

## Models

- Ridge regression
- Random Forest regression

## Metrics

- mean absolute error
- median absolute error
- maximum absolute error
- true vs estimated embedding rate

## Important

The experiment tests generalization across containers rather than
memorization of one cover image.

## Stored result and limitation

Ridge MAE was 5.765299 pp sequential, 4.416240 pp random, and 7.115504 pp adaptive. Random+Ridge was the strongest configuration; Random Forest was worse for every method. Each method has only 20 samples (five covers × four rates), leaving 16 training and four test samples per fold. This is a project-specific regression extension and not evidence of general performance beyond this dataset.

Run `python3 scripts/build_dataset.py`, then `python3 scripts/run_experiment.py` and `python3 scripts/plot_results.py` after package installation. Outputs are dataset, predictions, summary metrics, and plots under `results/`.
