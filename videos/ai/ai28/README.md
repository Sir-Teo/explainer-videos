# AI, Built — Part 28: Reasoning

Part 28 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). Why
writing out steps adds computation, how a model learns from a checker, and what more tries at answer time buy. Every
model here is a tiny transformer trained on this computer. A hook and four chapters:

* **Sixteen bits.** The parity of 16 bits: a two-layer transformer trained to answer at once is right 49% of the time
  (a coin flip); the same model trained to write the running parity first, 100%.
* **Thinking out loud is computing.** A fixed stack of L layers does at most L steps in a row; each written token goes
  back in, so k tokens of thought allow L(k + 1) (Merrill & Sabharwal). Parity at 4, 8 and 16 bits: at once 100%,
  47%, 49%; with the chain 100% each time; the two training curves.
* **Learning from a checker.** GRPO on two-digit addition: 8 answers per question, the advantage
  (r − mean) / std within the group, the push on log π; accuracy from 36% to 81% over 300 steps, and six questions'
  answers before and after. Outcome against process rewards (Lightman et al.); DeepSeek-R1.
* **The objective, exactly.** GRPO's clipped ratio and its k3 estimate of the KL to the reference; the model's
  probability over answers to three questions, step by step as it trains; DPO derived from the KL-regularized reward
  objective, trained here on preference pairs, and its likelihood displacement (both answers of a pair can fall);
  Dr. GRPO, DAPO and GSPO, each trained here; groups with no signal; pass@k before and after RL, and whether RL
  only sharpens what the base model could already find.
* **Thinking longer.** The model before RL, 32 tries at each of 200 questions; pass@k = 1 − C(n − c, k) / C(n, k)
  with a checker (33% → 100% at 32 tries), against a majority vote without one (32% → 61%); the RL model's single try
  (81%) for comparison.
* **Recap**, where it comes back, Part 29's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai28.compute
python tools/build.py ai28                # English
python tools/build.py ai28 --lang zh      # Chinese
```

References: Sutton & Barto (2018); Wei et al. (2022); Merrill & Sabharwal (2024); Shao et al., DeepSeekMath (2024);
DeepSeek-AI, DeepSeek-R1 (2025); Lightman et al. (2023); Chen et al. (2021); Wang et al. (2023); Snell et al. (2024); Schulman et al., PPO (2017); Rafailov et al., DPO (2023); Liu et al., Dr. GRPO
(2025); Yu et al., DAPO (2025); Zheng et al., GSPO (2025); Yue et al. (2025).
