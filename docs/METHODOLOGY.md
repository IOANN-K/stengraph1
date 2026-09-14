# Methodology

A **cover image** is the original PNG; a **stego image** contains an embedded **payload**. LSB replacement changes the least-significant bits of RGB samples. **Embedding depth** is the number of low bits used per channel. **Capacity** is the maximum framed payload; **embedding rate/capacity usage** is the used fraction. Payloads have a 32-bit byte-length header.

**MSE** averages squared channel error. **PSNR** expresses that error logarithmically; higher is better. **SSIM** compares perceived structure; higher is better. **Changed pixels** count pixels with any altered RGB channel; **changed channels** count altered samples. **Imperceptibility** concerns similarity, while **robustness** concerns survival after processing.

**Compression** reduces redundant bytes; **encryption** provides confidentiality/authentication. The tested pipeline compresses before Fernet encryption.

**Steganalysis** seeks evidence or estimates of hidden data. Exp10 reports LSB balance, **binary entropy**, spatial LSB agreement, and a project implementation of a **Pair-of-Values-style chi-square** statistic. LSB ratio and entropy are weak standalone indicators. Large samples can produce tiny p-values, so normalized chi-square is also used descriptively.

**RS analysis** groups samples, applies masks, and labels groups Regular, Singular, or Unusable. The **RS gap** is normalized Regular minus Singular. Exp11 uses `[1, 0, 1, 0]` and clipped negative flips; it is exploratory, not canonical closed-form estimation.

**MAE** is mean absolute error in percentage points. **Cross-container generalization** asks whether learning transfers to different content. Exp14/15 use **leave-one-container-out validation**, holding out all samples from one cover.

Provenance categories are literature-established concepts, literature-inspired project implementations, and project-specific experimental extensions.
