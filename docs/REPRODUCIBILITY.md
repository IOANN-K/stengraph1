# Reproducibility

## Environment and installation

The validated snapshot is Python 3.14.2 with Pillow 12.3.0, NumPy 2.5.3, SciPy 1.18.1, scikit-image 0.26.0, scikit-learn 1.9.1, Matplotlib 3.11.1, and cryptography 50.0.1. `pyproject.toml` is the dependency source of truth; `requirements-lock.txt` records this exact environment.

Install with `python3 -m pip install -e .`; add `.[dev]` for pytest. Run an individual experiment through its existing `scripts/run_experiment.py`, then its plot script where applicable. Some later experiments consume recorded images/metrics from earlier stages; follow numeric order, treating 09A before 10–12 and Exp13 image generation before 14–15 dataset building.

## Determinism

Fixed semantic keys and seeds remain in experiment configs. Exp01's random method uses `random.Random`; standardized Exp06 uses a SHA-256-derived NumPy generator, so the two permutations are conceptually similar but not byte-identical. Exp09A/12/13 derive deterministic synthetic payloads from documented strings/cases. Exp14/15 use model `random_state=42` where relevant.

Fernet ciphertext is intentionally randomized. A saved key supports decryption but does not make a rerun produce identical ciphertext; deterministic encryption was not introduced.

## Integrity and artifacts

Verify `checksums/research-inputs.sha256` and `checksums/result-metrics.sha256` with `python3 scripts/validate_repository.py`. Metric CSVs, summaries, keys, selected plots, configuration, and manifests are canonical research records. Bulk stego PNGs, difference maps, and transformed images are reproducible intermediates in principle, but existing copies are retained as historical artifacts and are not removed or rewritten by this refactor.

Future work should keep compact metrics/configuration/manifests and selected plots under version control, while deciding explicitly whether large intermediates need archival storage. Existing runners may overwrite paths, so reproduce in a copied checkout or back up `results/` first.
