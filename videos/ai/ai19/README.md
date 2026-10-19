# AI, Built — Part 19: Inference

Part 19 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). Why
running a model is a problem of moving numbers, and three ways to move fewer. A hook and three chapters:

* **The speed limit.** Writing one token reads every weight: tokens per second ≤ memory bandwidth / bytes of weights,
  about 24 a second for a 70-billion-parameter model in 16 bits on an H100, using a third of one percent of its
  arithmetic (published figures).
* **Guess ahead, check at once.** Speculative decoding with Part 13's transformer as the big model and a counting model
  on the last two characters as the draft: the acceptance rule min(1, p/q) with the leftover max(0, p − q), checked by
  200,000 samples to reproduce the big model's probabilities exactly; the characters per run, (1 − αᵏ⁺¹)/(1 − α).
* **Fewer bits per number.** Part 13's transformer rounded to 8, 4 and 3 bits, and to FP4 (E2M1) with a scale per
  block of 32: the weight histogram against the levels, and the bits per character lost; GPTQ and low-precision
  training; MXFP4 (E2M1, a power-of-two scale per 32: 4.25 bits a weight) and NVFP4 (E2M1, an E4M3 scale per 16 and
  one per tensor: 4.5 bits) exactly: 2.022 and 2.020 bits a character against 2.043 for 4-bit integers (1.996
  unrounded); GPTQ's column-by-column error compensation (at 3 bits: 2.119 against 2.251), animated on a small layer;
  and a Hadamard rotation, which our outlier-free model doesn't need (2.323 at 3 bits).
* **Moving numbers is the cost.** This computer's own roofline (matrix products of growing size against its memory
  bandwidth); FlashAttention's tiles and online softmax, checked against the plain formula; vLLM's pages against
  blocks reserved at the maximum length, for 200 requests of random lengths.
* **Recap**, where this came from (Parts 15, 16, 28, 29), Part 30's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai19.compute          # needs Part 13's transformer (python -m videos.ai.ai13.compute tf)
python tools/build.py ai19                # English
python tools/build.py ai19 --lang zh      # Chinese
```

The roofline is measured on the machine that runs the compute step, so run it on an otherwise idle computer.

References: Hennessy & Patterson (2017); Leviathan, Kalman & Matias (2023); Chen et al. (2023); Frantar et al., GPTQ
(2023); Dettmers et al., LLM.int8() (2022); Rouhani et al., Microscaling formats (2023); Dao et al., FlashAttention
(2022); Milakov & Gimelshein (2018); Williams, Waterman & Patterson, Roofline (2009); Kwon et al., vLLM (2023).
