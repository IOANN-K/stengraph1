# Experiment Catalogue

All recorded outputs are under each experiment's `results/` directory. CSV schemas are preserved as written by the original runners.

| Exp | Objective; inputs | Variables and methods | Main result; limitations; provenance |
|---|---|---|---|
| 01 | Compare placement; `input2.png`, canonical text | sequential/random/adaptive, 1 LSB; quality/recovery | Adaptive SSIM led. Original Python random and variance implementation; project comparison of established/inspired methods. |
| 02 | Relate load to quality; same cover/payload | 10–100%, three methods | Distortion rose; one cover/payload. Project extension. |
| 03 | Test compression | raw vs zlib level 9, three methods | Size fell 64.05% and quality improved. Standard compression in project pipeline. |
| 04 | Test confidentiality/size | raw/encrypted/compressed/compressed+encrypted | Encryption expanded size; compress-then-encrypt balanced goals. Fernet is standard tooling; pipeline is project-specific. |
| 05 | Test robustness | resave, optimize, resize, crop, JPEG | Lossless PNG survived; geometry/lossy operations failed. Fixed transformation parameters limit scope. |
| 06 | Study depth | depths 1–4, three standardized methods | Error rose with depth; one cover. Standard LSB with project adaptive ranking. |
| 07 | Test cover sensitivity | five content categories | three methods, fixed payload | Texture controlled adaptive benefit; small selected cover set. |
| 08 | Compare adaptive rankings | variance/gradient/Laplacian; 3/5/7/9 windows | quality/recovery | Gradient 7×7 led only on this cover. Literature-inspired rankings, project parameter study. |
| 09A | Approach theoretical capacity | deterministic high-entropy payload, 10–100% | three methods | All decoded at 100%; visual advantage vanished. Synthetic benchmark. |
| 09B | Illustrate real text sizes | six literary files | capacity fit and quality | Moby-Dick fit; War and Peace did not. Not entropy-controlled. |
| 10 | Basic statistical steganalysis | Exp09A images | LSB balance/entropy, PoV-style chi-square, spatial agreement | Detectable trends, but indicators are basic and sample-size-sensitive. Literature-inspired implementation. |
| 11 | Explore RS behavior | Exp09A images | `[1,0,1,0]`, R/S/U and gaps | Gap approached zero. Clipped negative flipping makes this non-canonical exploratory RS. |
| 12 | Estimate rate on one cover | Exp11 calibration; 15/35/60/85% tests | monotonic interpolation | Low same-cover MAE; not closed-form RS or universal. Project-specific extension. |
| 13 | Transfer Exp12 calibration | five heterogeneous covers | three methods/rates | Global MAE rose to 13–17 pp. Negative generalization result. |
| 14 | Learn cross-cover RS estimator | Exp13 images | Ridge/Random Forest; leave-one-cover-out | Random+Ridge MAE 4.416240 pp. Only 20 samples/method and 16 training samples/fold. |
| 15 | Add basic/histogram/spatial features | same images/folds | Ridge/ElasticNet | MAE worsened to 14–21 pp with extreme errors. Negative project-specific result. |

Runner scripts document exact constants and output columns; [Results](RESULTS.md) records headline stored values.
