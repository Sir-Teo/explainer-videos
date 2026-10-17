# AI, Built — Part 17: Reasoning

Part 17 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). Why
writing out steps adds computation, how a model learns from a checker, and what more tries at answer time buy. Every
model here is a tiny transformer trained on this computer. A hook and three chapters:

* **Sixteen bits.** The parity of 16 bits: a two-layer transformer trained to answer at once against the same model
  trained to write the running parity first.
* **Thinking out loud is computing.** A fixed stack of L layers does at most L steps in a row; each written token goes
  back in, so k tokens of thought allow L(k + 1) (Merrill & Sabharwal). Parity at 4, 8 and 16 bits, answered at once
  and with the chain, and the two training curves.
* **Learning from a checker.** GRPO on two-digit addition: 8 answers per question, the advantage
  (r − mean) / std within the group, the push on log π; accuracy along 300 steps, and six questions' answers before
  and after. Outcome against process rewards (Lightman et al.); DeepSeek-R1.
* **Thinking longer.** The model before RL, 32 tries at each of 200 questions; pass@k = 1 − C(n − c, k) / C(n, k)
  with a checker, against a majority vote without one, as k doubles; the RL model's single try for comparison.
* **Recap**, where it comes back, Part 18's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai17.compute
python tools/build.py ai17                # English
python tools/build.py ai17 --lang zh      # Chinese
```

References: Sutton & Barto (2018); Wei et al. (2022); Merrill & Sabharwal (2024); Shao et al., DeepSeekMath (2024);
DeepSeek-AI, DeepSeek-R1 (2025); Lightman et al. (2023); Chen et al. (2021); Wang et al. (2023); Snell et al. (2024).
