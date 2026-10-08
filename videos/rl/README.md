# Reinforcement Learning for Language Models, Derived: From the Policy Gradient to GRPO

A math-heavy explainer, in five parts, of the reinforcement learning used to
post-train language models, **as of October 2026**. Every algorithm is derived
on screen from the one before it, starting with the log-derivative trick:

1. **The policy gradient**: a language model as a policy, the log-derivative
   trick (REINFORCE), baselines and the optimal baseline, values, TD errors
   and generalized advantage estimation.
2. **Taking safe steps**: importance sampling, the performance-difference
   lemma, TRPO's lower bound, the natural gradient and the Fisher geometry
   of the probability simplex, PPO's clipped objective.
3. **Learning what people want**: Bradley–Terry from Gumbel noise, reward
   models, the closed-form optimum of the KL-regularized objective, KL
   estimators k1/k2/k3 (and why k3's gradient points at the reversed KL), DPO.
4. **Reasoning, with a checker**: GRPO, its group baseline as RLOO in
   disguise, its std-normalization as an arcsine objective (with exact
   finite-group weights), zero-variance groups, the length bias of its token
   averaging (DAPO, Dr. GRPO), entropy collapse as a covariance, clip-higher,
   pass@k, sharpening vs discovery, on-policy distillation.
5. **RL at scale**: the sampler/learner mismatch measured on a real reasoning
   model (TIS, masking, GSPO, CISPO), asynchronous RL, ScaleRL's sigmoid
   compute law, agentic environments, reward hacking, the state of play.

**Watch:** [`published/rl.mp4`](../../published/rl.mp4) (1080p, subtitles and chapters embedded).

CHAPTERS_TBD

```bash
python -m videos.rl.compute          # once: all real footage (about 3 hours on 4 cores; cached in .cache/rl)
python -m videos.rl.compute mismatch # ...or single items: gauss cloud simplex kl_est base runs tree tilt passk critic scaling dpo mismatch
python tools/build.py rl -q l        # preview
python tools/build.py rl             # final 1080p30 + subtitles + chapters
python tools/export_script.py rl     # regenerate SCRIPT.md from the code (and the last render, for data-driven lines)
python tools/check_narration.py rl   # Whisper listen test of every narration line
python tools/publish.py rl           # GitHub-sized copy -> published/rl.mp4
```

## What is real in this video

Charts are labeled `real run`, `exact` (computed, no sampling noise beyond what
is stated), `schematic` or `illustrative`. Everything real was computed on the
4-core CPU that rendered the video, by `python -m videos.rl.compute`:

* **The adder**: a 3-layer, 335k-parameter transformer
  ([`explainer/lm/pocket.py`](../../explainer/lm/pocket.py)) pretrained on
  4-digit additions. A quarter of the training answers *show their work* (the
  sum written right-to-left, digit by digit, then the answer; always right);
  the rest answer at once and forget each carry with probability 0.25. Its
  answer tree, critic, KL-tilted optimum, reward–KL frontier, pass@k and DPO
  run all come from this model and the RL runs below.
* **RL runs**: GRPO (the hero run), REINFORCE without a baseline, RLOO,
  Dr. GRPO, a DAPO-style variant (token-mean loss, clip-higher 0.2/0.28,
  dynamic sampling), PPO with a learned critic and GAE (λ = 0.95), and
  1-vs-16 updates per batch with and without PPO's clip; 3 seeds each.
* **Exact toys**: a Gaussian policy on a two-hill reward (score-function
  arrows, REINFORCE paths with and without a baseline), a 2-D Gaussian policy
  (gradient-estimate clouds, variance as a function of the baseline), a
  3-action softmax policy (vanilla vs natural gradient flows, iso-KL
  contours, the tilted family), Schulman's KL estimators by Monte Carlo
  (2 million samples, matching his published table).
* **A real reasoning model**: [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)
  writes eight thinking traces (the first 768 tokens of each, sampled together
  in bfloat16 with a KV cache, at temperature 1, as an inference engine does);
  the identical tokens are re-scored in one full bfloat16 pass and in float32,
  as a trainer does.

## What the real runs found

All numbers are means over 3 seeds at the end of 120 RL steps (32 problems × 8
answers per step, reward 1 if the final answer is right), measured on 500
held-out problems at temperature 1, unless stated otherwise.

* **The base adder** shows its work 27.5% of the time (then right 99.9%), answers
  directly otherwise (then right 59.9%): **70.9%** right overall.
* **RL sharpened rather than taught.** GRPO reaches 98.4%, mostly by removing
  slips: direct answers go from 60% to 97% right, while showing work only rises
  from 27% to 41%. pass@k before RL: 70.4% (k = 1), 99.9% (k = 8), 100%
  (k ≥ 16); after RL, pass@1 is 99.2%. No problem the base model could solve
  was lost. On the running example, 5675 + 5563, the probability of a right
  answer goes from 56.2% to 99.8%.
* **Same accuracy, different behavior.** Every algorithm ends at 98–99%
  accuracy, but how often the model shows its work differs: REINFORCE averaged
  per answer (GRPO's 1/|o_i|) **0%**, GRPO 41%, RLOO 44%, DAPO-style 48%,
  Dr. GRPO 50%, PPO with a critic 54%.
* **The length bias, isolated.** The same REINFORCE with a constant normalizer
  instead of 1/|o_i| ends at **50%**: without a baseline, only right answers are
  pushed, and per token a 6-token direct answer pushes twice as hard as a
  13-token worked one.
* **The critic localizes credit.** A value network trained on the base model's
  answers gives the running example 58%; its value jumps +0.39 at the token that
  starts showing work, and drops −0.50 at the one digit where a carry was
  forgotten. With a critic this accurate, GAE's λ barely matters.
* **Reusing batches.** One update per batch: 75% after 5 steps; 16 clipped
  updates per batch: 93% (ending at 99.1%); 16 unclipped: just as fast, but one
  seed falls back to 91% around step 40 and the mean ends lower (97.7%).
* **The KL-regularized optimum** (exact, 48 problems): being right every time
  costs 0.39 nats of KL from the base model; the GRPO run (no KL penalty)
  reaches 98% at about 0.8 nats, below the frontier, because it also reshuffles
  the probabilities among right answers.
* **DPO** (4,096 fixed right-vs-wrong pairs, β = 0.1, lr 1e-5): accuracy rises
  from 69% to 80% at step 100, then collapses to 0.7% by step 300 as the log
  probability of the *preferred* answers falls by 10 nats and the rejected ones
  by 18 (likelihood displacement; at lr 1e-4 it collapses within 50 steps).
* **Entropy** of the next-token distribution falls about 4× during the GRPO run;
  the batch covariance between token log-probability and advantage is positive
  in 87% of batches (90% and 94% in the other two seeds), and, averaged over
  9 steps, correlates −0.64 with the per-step entropy change (−0.63, −0.77).
* **ScaleRL's sigmoid**, fitted to GRPO with 1, 4 and 16 updates per batch: the
  same ceiling (A = 1.00, 1.00, 1.00), with the compute to get halfway spanning
  7.5× (1.1×10¹¹, 3.0×10¹⁰, 1.4×10¹⁰ FLOPs).
* **The sampler and the learner disagree** (Qwen3-0.6B, 6,144 sampled tokens):
  re-scored in float32, 25% of tokens have a log-probability more than 1% away
  from the sampler's, and 1.4% more than 10%. Re-scored in the *same* bfloat16
  but in one pass instead of token by token: 24%, so it is the order of the
  arithmetic, not only the precision. Near-certain tokens (p > 0.9) almost
  never move (0.8% of them), while 92% of the tokens the sampler gave less than
  a 10% chance do. Multiplied over 768 tokens, the whole-answer importance
  weights range from 0.48 to 8.45, with no change to the model's weights.
* **Baselines**: in the 2-D toy, subtracting the mean reward cuts the variance
  of a 16-sample gradient estimate 27×; the optimal baseline (2.371) is within
  0.3% of the mean reward (2.364). Schulman's KL estimators reproduce his table:
  for KL = 0.005, std/KL is 20.0 (k1), 1.42 (k2), 1.42 (k3); for KL = 0.5, k2's
  bias is 0.25.

## Color legend

| Concept | Color |
|---|---|
| policy π_θ | blue |
| reference π_ref | grey |
| old / sampling policy π_old, the inference engine | teal |
| reward, right answers | green |
| wrong answers, negative advantage | red |
| advantage A | yellow |
| score ∇log π, gradient arrows | orange |
| baselines b, values V, the critic | light purple |
| importance ratio ρ | pink |
| KL divergence, β | gold |
| entropy | light pink |
| answer length | brown |
| "show your work" tokens | light blue |

## Sources

Derivations follow the primary sources; on-screen numbers from outside this
repository are quoted from them.

* Williams, *Simple statistical gradient-following algorithms for connectionist RL*, Machine Learning 8 (1992).
* Schulman et al., *High-Dimensional Continuous Control Using Generalized Advantage Estimation*, arXiv 1506.02438.
* Kakade & Langford, *Approximately Optimal Approximate RL*, ICML 2002; Kakade, *A Natural Policy Gradient*, NIPS 2001.
* Schulman et al., *Trust Region Policy Optimization*, arXiv 1502.05477; *Proximal Policy Optimization Algorithms*, arXiv 1707.06347.
* Ouyang et al., *Training language models to follow instructions with human feedback* (InstructGPT), arXiv 2203.02155.
* Bradley & Terry, Biometrika 39 (1952); Gao, Schulman & Hilton, *Scaling Laws for Reward Model Overoptimization*, arXiv 2210.10760.
* Rafailov et al., *Direct Preference Optimization*, arXiv 2305.18290; Korbak, Perez & Buckley, arXiv 2205.11275.
* Schulman, [*Approximating KL Divergence*](http://joschu.net/blog/kl-approx.html) (2020); Tang & Munos, arXiv 2506.09477; DeepSeek-V3.2, arXiv 2512.02556.
* Shao et al., *DeepSeekMath* (GRPO), arXiv 2402.03300; Ahmadian et al., *Back to Basics* (RLOO), arXiv 2402.14740.
* Davis & Recht, *What is the objective of reasoning with reinforcement learning?*, arXiv 2510.13651 (GRPO's arcsine objective).
* Yu et al., *DAPO*, arXiv 2503.14476; Liu et al., *Understanding R1-Zero-Like Training* (Dr. GRPO), arXiv 2503.20783.
* Cui et al., *The Entropy Mechanism of RL for Reasoning Language Models*, arXiv 2505.22617.
* Chen et al., *Evaluating LLMs Trained on Code* (pass@k), arXiv 2107.03374; Yue et al., arXiv 2504.13837; ProRL, arXiv 2505.24864.
* Schulman, [*LoRA Without Regret*](https://thinkingmachines.ai/blog/lora/) (2025); Mukherjee et al., arXiv 2505.11711; Shenfeld et al., *RL's Razor*, arXiv 2509.04259.
* Lu, [*On-Policy Distillation*](https://thinkingmachines.ai/blog/on-policy-distillation/) (2025); Qwen3 technical report, arXiv 2505.09388; DeepSeek-V4, arXiv 2606.19348.
* Yao et al., [*Your Efficient RL Framework Secretly Brings You Off-Policy RL Training*](https://fengyao.notion.site/off-policy-rl) (2025); Zheng et al., *GSPO*, arXiv 2507.18071; MiniMax-M1 (CISPO), arXiv 2506.13585; Qi et al., arXiv 2510.26788; IcePop, arXiv 2510.18855.
* OLMo 3, arXiv 2512.13961; Khatri et al., *The Art of Scaling RL Compute for LLMs* (ScaleRL), arXiv 2510.13786.
* DeepSeek-R1, arXiv 2501.12948 (Nature 645, 2025); GLM-5, arXiv 2602.15763; Qwen SWE-Universe, arXiv 2602.02361.
* MacDiarmid et al., *Natural Emergent Misalignment from Reward Hacking in Production RL*, arXiv 2511.18397; Baker et al., arXiv 2503.11926.
* Open-source code read for the defaults table (commits of Oct 2026): [verl](https://github.com/volcengine/verl), [TRL](https://github.com/huggingface/trl), [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF), [open-instruct](https://github.com/allenai/open-instruct), [nanochat](https://github.com/karpathy/nanochat), [prime-rl](https://github.com/PrimeIntellect-ai/prime-rl), [slime](https://github.com/THUDM/slime), [AReaL](https://github.com/inclusionAI/AReaL), [SkyRL](https://github.com/NovaSky-AI/SkyRL), [ROLL](https://github.com/alibaba/ROLL), [ART](https://github.com/OpenPipe/ART).
