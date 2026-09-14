# Experiment 04

Study of compression and encryption before 1-LSB embedding.

## Container

`data/images/input2.png`

## Payload

`data/payload/text.txt`

## Variants

- raw
- encrypted
- compressed
- compressed + encrypted

## Compression

zlib level 9.

## Encryption

Fernet authenticated symmetric encryption.

## Embedding methods

- sequential
- pseudorandom
- adaptive texture-based

## Verification

Every variant is transformed back into the original payload after extraction.

The recovered payload must match the original byte-for-byte and by SHA-256.

## Goal

Evaluate the effect of compression and encryption on embedded payload size
and stego-image distortion.

Run `python3 scripts/run_experiment.py`, then `python3 scripts/plot_results.py`. Encryption expanded 148,574 B to 198,180 B; compression+encryption used 71,308 B. Fernet is randomized, so a key does not reproduce identical ciphertext. The pipeline comparison is project-specific.
