# AI, Built — Part 15: Images and Video

Part 15 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). How the
transformer and the diffusion machinery of Parts 11 and 14 meet pictures and video. The pictures are Part 14's 20 × 20
capital letters from the system's fonts, and every model is trained here. A hook and four chapters:

* **Letters from noise.** A word spelled by a small diffusion transformer, letter by requested letter.
* **An image is a sequence.** 4 × 4 patches as tokens; a small vision transformer naming letters in fonts it never
  saw; where its summary token looks; its learned position vectors rediscovering the 5 × 5 grid.
* **A smaller space.** An autoencoder squeezing 400 pixels into 16 numbers and back; the letters in that space; flow
  matching in it, decoded (latent diffusion).
* **Transformers as denoisers.** A diffusion transformer with adaptive layer norm, trained by flow matching and asked
  for each letter of the alphabet; MM-DiT's joint sequence of prompt and patches; published sizes.
* **Video, and other orders.** Spacetime tokens and their count for clips; next-scale prediction, coarse to fine.
* **Recap**, where it comes back, Part 16's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai15.compute
python tools/build.py ai15                # English
python tools/build.py ai15 --lang zh      # Chinese
```

References: Dosovitskiy et al., ViT (2020); Rombach et al., latent diffusion (2022); Peebles & Xie, DiT (2023); Esser
et al., Stable Diffusion 3 (2024); Tian et al., VAR (2024).
