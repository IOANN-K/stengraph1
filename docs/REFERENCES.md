# References and Provenance

1. Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image Quality Assessment: From Error Visibility to Structural Similarity,” *IEEE Transactions on Image Processing*, 13(4), 2004, pp. 600–612. DOI: 10.1109/TIP.2003.819861.
2. A. Westfeld and A. Pfitzmann, “Attacks on Steganographic Systems,” *Information Hiding*, LNCS 1768, 2000 (conference held 1999), pp. 61–76. DOI: 10.1007/10719724_5.
3. J. Fridrich, M. Goljan, and R. Du, “Reliable Detection of LSB Steganography in Color and Grayscale Images,” *Proceedings of the 2001 Workshop on Multimedia and Security*, 2001, pp. 27–30.
4. S. Dumitrescu, X. Wu, and N. Memon, “On Steganalysis of Random LSB Embedding in Continuous-Tone Images,” *IEEE International Conference on Image Processing*, 2002.
5. J. Fridrich, M. Goljan, D. Hogea, and D. Soukal, “Quantitative Steganalysis of Digital Images: Estimating the Secret Message Length,” *Multimedia Systems*, 9, 2003, pp. 288–302. DOI: 10.1007/s00530-003-0100-9.

The prompt identifies an initial 2026 Yarema et al. article about modified LSB replacement in SVG images, but no exact title, full author list, or DOI is present in the repository. It is therefore not fabricated here and requires the original source record before inclusion. Likewise, adaptive ranking in this repository is project-designed; no modern paper is claimed as its direct implementation source without verified provenance.

| Repository component | Concept | Provenance | Reference/note |
|---|---|---|---|
| LSB embedding | substitution/replacement | literature-established | General steganography concept. |
| SSIM | structural similarity | literature-established | Wang et al. |
| Exp10 chi-square | PoV-style statistic | literature-inspired | Westfeld–Pfitzmann concept; simplified project implementation. |
| Exp11 RS groups | RS analysis | literature-inspired | Fridrich–Goljan–Du; clipped negative flips are documented. |
| Adaptive scores | content-adaptive placement | literature-inspired/project-specific | Variance, Sobel, and Laplacian ranking; no exact-paper claim. |
| Exp12 interpolation | rate estimation | project-specific extension | Inspired by quantitative steganalysis; not a canonical estimator. |
| Exp14 regression | cross-cover estimation | project-specific extension | Ridge/Random Forest experiment. |
| Exp15 hybrid features | feature combination | project-specific extension | Ridge/ElasticNet negative-result experiment. |
