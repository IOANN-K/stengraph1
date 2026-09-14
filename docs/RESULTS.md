# Stored Results

This summary comes from existing CSV files; values were not recomputed from images.

- **Exp01:** SSIM: 0.99939046 sequential, 0.99958437 random, 0.99994969 adaptive; changed channels stayed near 4.68–4.69%.
- **Exp02:** distortion increased from 10% to 100%; adaptive retained stronger SSIM at lower/moderate loads.
- **Exp03:** zlib reduced 148,574 B to 53,408 B (64.05%); adaptive SSIM rose from 0.99994969 to 0.99998809.
- **Exp04:** adaptive embedded sizes: 148,574 B raw, 198,180 B encrypted, 53,408 B compressed, 71,308 B compressed+encrypted.
- **Exp05:** no-op, PNG resave, and optimization recovered payloads; resize, crop, and JPEG roundtrip failed for all methods.
- **Exp06:** distortion rose at depths 1–4; adaptive retained strongest SSIM; maximum differences were 1, 3, 7, 15.
- **Exp07:** adaptive benefit varied strongly with cover texture.
- **Exp08:** gradient 7×7 had highest tested SSIM, 0.9999819816, on one textured cover only.
- **Exp09A:** maximum payload was 1,585,148 B. All methods decoded at 100%; changed channels were ~50% and pixels ~87.5%.
- **Exp09B:** Moby-Dick used 78.0737% and fit; War and Peace required 148.0367% and did not.
- **Exp10:** high-entropy embedding moved pair behavior toward randomized LSB behavior; normalized chi-square was descriptively useful.
- **Exp11:** the RS gap approached zero near 100%; adaptive retained a positive gap longer. Boundary simplifications apply.
- **Exp12:** interpolation MAE: 1.023768 pp sequential, 0.276409 pp random, 1.119612 pp adaptive.
- **Exp13:** transferred-calibration MAE: 17.036951 pp sequential, 14.829468 pp random, 13.075887 pp adaptive.
- **Exp14:** Ridge MAE: 5.765299 pp sequential, 4.416240 pp random, 7.115504 pp adaptive. Random Forest was worse.
- **Exp15:** best MAE: 21.197310 pp sequential, 19.270442 pp random, 14.308920 pp adaptive. Hybrid features worsened transfer and caused clipped extremes.

Historical schemas and numeric values remain unchanged.
