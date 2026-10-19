# AI, Built — Part 22: Images and Video

Part 22 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). How the
transformer and the diffusion machinery of Parts 13 and 21 meet pictures and video. The pictures are Part 21's 20 × 20
capital letters from the system's fonts, and every model is trained here, with its training shown as well as its
result. A hook and eight chapters:

* **Letters from noise.** A word spelled by a small diffusion transformer, letter by requested letter.
* **An image is a sequence.** 4 × 4 patches as tokens; a small vision transformer naming letters in fonts it never
  saw; where its summary token looks; its learned position vectors rediscovering the 5 × 5 grid.
* **A smaller space.** An autoencoder squeezing 400 pixels into 16 numbers and back; the letters in that space; flow
  matching in it, decoded (latent diffusion). The VAE: the ELBO, rebuild error plus β·KL, and what β trades (sharp
  rebuilds against a smooth space to generate in); one VAE training, held-out letters rebuilt at checkpoints beside
  its two loss terms.
* **Transformers as denoisers.** A diffusion transformer, patch tokens plus a time-and-letter vector; adaLN-Zero
  (scale, shift and gate from that vector, the gate starting at zero so every block starts as the identity); the
  same noise and the same ten requests drawn at checkpoints during training beside the loss; the whole alphabet.
* **Rectified flow at scale.** Stable Diffusion 3: MM-DiT's two streams with one joint attention; logit-normal
  sampling of t (training where the velocity is hardest); the resolution shift σ' = ασ / (1 + (α − 1)σ).
* **Coarse to fine.** VAR's next-scale prediction against raster order; residual quantization across scales, each
  one coding what the coarser ones missed; the block-causal mask between scales.
* **Squeezing time.** Spacetime patches and their count; a causal 3D autoencoder trained here on moving letters (the
  first frame coded alone, so a still image is a one-frame video); 3D rotary positions over time, height and width.
* **Frames that agree.** Image-to-video: given a real first frame, the rest of a clip of a moving letter generated
  jointly, every frame attending to every other, against frames taken from different samples: how often each
  generated frame is recognized, and how smoothly the letter moves.
* **Rolling forward.** Diffusion forcing: a separate noise level per frame, so the model can extend a clip past the
  length it trained on; teacher forcing against rollouts from a real first frame; self forcing.
* **Recap**, where it comes back, Part 23's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai22.compute          # needs Part 21's letters
python tools/build.py ai22                # English
python tools/build.py ai22 --lang zh      # Chinese
```

References: Dosovitskiy et al., ViT (2020); Kingma & Welling, VAE (2013); Rombach et al., latent diffusion (2022);
Peebles & Xie, DiT (2023); Esser et al., Stable Diffusion 3 (2024); Tian et al., VAR (2024); Yao et al., VA-VAE
(2025); Chen et al., diffusion forcing (2024); Huang et al., self forcing (2025).
