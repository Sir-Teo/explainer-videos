# AI, Built — Part 21: Diffusion and Flow

Part 21 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). How
models make things from noise, with every model trained here on a CPU: points, pictures and text. A hook and six
chapters:

* **From noise.** A network trained here walking 300 random points into Part 5's letters "AI".
* **Learning to denoise.** x_t = α_t x_0 + σ_t ε; learning to guess ε; the guess as the score; the trained network's
  arrows at four noise levels; the same noise sampled at checkpoints during training, beside the loss.
* **Walking back from noise.** DDPM's stochastic steps and DDIM's deterministic path; distance from the data against
  the number of steps.
* **Flow matching.** Straight lines from noise to data and their velocity; learned paths that bend; reflow, which
  straightens them so that one step suffices. Few-step models: MeanFlow learns the average velocity u over a jump,
  through the identity u = v + (t − s) du/ds (one Jacobian-vector product per step); shortcut models learn jumps of
  size d from two jumps of d/2; one-jump samples from flow matching, reflow, MeanFlow and a shortcut model.
* **Guidance.** A model of two letters told which to draw, or nothing; classifier-free guidance at weights 0, 1 and 4.
* **From points to pictures.** 20 × 20 capital letters from the system's fonts; the same flow model in 400
  dimensions; a sample's journey from noise.
* **Diffusion for text.** Blanks as noise; a small two-way transformer trained on the novels, writing 64 characters
  by unmasking the surest guesses first (LLaDA's method); block diffusion, left to
  right across blocks and diffusion inside each one, so finished blocks can be cached.
* **Recap**, where it comes back, Part 22's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai21.compute          # needs Part 1's books for the text model
python tools/build.py ai21                # English
python tools/build.py ai21 --lang zh      # Chinese
```

References: Sohl-Dickstein et al. (2015); Ho, Jain & Abbeel, DDPM (2020); Song et al., score-based SDEs (2021); Song,
Meng & Ermon, DDIM (2021); Lipman et al., flow matching (2023); Liu et al., rectified flow (2023); Ho & Salimans,
classifier-free guidance (2022); Esser et al., Stable Diffusion 3 (2024); Austin et al., D3PM (2021); Sahoo et al.,
MDLM (2024); Nie et al., LLaDA (2025); Geng et al., MeanFlow (2025); Frans et al., shortcut models (2024); Arriola
et al., block diffusion (2025).
