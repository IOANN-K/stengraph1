# Experiment 15 — Hybrid Steganalysis Features

## Research question

Do RS, LSB balance/entropy, histogram chi-square, and spatial features improve cross-container embedding-rate estimation?

## Inputs and methods

The five Exp13 containers provide 20 samples per embedding method (four rates each). Ridge and ElasticNet use leave-one-container-out validation: each fold trains on 16 samples and tests four from a completely held-out cover. Outputs are `dataset.csv`, prediction `results.csv`, `summary.csv`, and plots under `results/`.

Run `python3 scripts/build_dataset.py`, `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py` after installing the package.

## Stored result

Best MAE was 21.197310 pp sequential (ElasticNet), 19.270442 pp random (ElasticNet), and 14.308920 pp adaptive (Ridge). Severe domain-shift failures included estimates clipped to 0% and 100%.

## Interpretation, limitations, and provenance

Hybrid features made generalization substantially worse than Exp14. More features were not an improvement; this negative result is part of the research record. The dataset is extremely small, feature distributions vary by cover, and conclusions must not be generalized. The combination and regression design are project-specific; basic/RS concepts are literature-inspired implementations.
