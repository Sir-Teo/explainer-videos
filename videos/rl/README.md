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

## Outline

| # | Scene | What it establishes | Real data on screen |
|---|---|---|---|
| 1 | `Hook` | A real model's answers drawn as a "river" of probability that bends toward the right answer as RL trains it, from one bit of reward per attempt. Reasoning models are made this way (DeepSeek-R1-Zero; OpenAI o1). The GRPO objective, to be derived symbol by symbol. Five-part roadmap. | The adder's exact answer tree for 5675 + 5563 at GRPO checkpoints 0–120: P(right) 56% → 99.8%, the "shows its work" stream thinning. *Quoted:* R1-Zero AIME 2024 15.6% → 77.9%. |
| 2 | `Policy` | Part 1. RL's vocabulary for a language model (state, action, policy, deterministic transition, end-of-answer reward). An answer's probability is the product of its tokens' probabilities along a path; J(θ) is the green part of the reward column. The adder, its training data, and its two habits. | The tree with one path's product, 0.54 × 0.74 × 0.76 × 1 × 1 × 1 = 0.30. The adder (335,328 parameters): shows its work 28% of the time (then right 99.9%), answers directly otherwise (then right 60%), 71% overall. |
| 3 | `LogDerivative` | Why backpropagation can't reach the reward. The five-line derivation of ∇J = E[R ∇log π], a reason beside each line; the score function; REINFORCE (Williams 1992). A 1-D Gaussian policy: score arrows a − μ cancel on average and reward-weighting breaks the symmetry; the policy climbs the tall hill. Sequences: the reward times a sum of token scores; RL as fine-tuning on your own graded samples; the softmax score 𝟏[b = a] − π(b). | Exact toy, 10 real samples: unweighted mean push −0.11, reward-weighted +0.15. One real softmax step on the next-token distribution. |
| 4 | `Baselines` | Subtracting a baseline keeps the mean (the score has mean zero) and cuts the noise. The variance is a parabola in b; the optimal baseline E[R‖g‖²]/E[‖g‖²]. The advantage R − V(x), and why easy and hard prompts need different baselines. | Six REINFORCE runs with reward 2 + R wander; six with the batch-mean baseline climb. 300 gradient estimates (batches of 16) on a 2-D toy: variance 0.73 → 0.027 (27×). b* = 2.371 vs mean reward 2.364. |
| 5 | `Credit` | One reward at the end blames every token equally. The value of a prefix, the Bellman equation for an LM, a token's advantage as the change in value, the TD error. GAE's λ. What GRPO/RLOO give up by dropping the critic. | A critic trained on the base model's answers: V = 58% before the answer; +0.39 at the token that starts showing work; −0.50 at the digit with the forgotten carry; λ barely matters for a critic this good. |
| 6 | `TrustRegions` | Part 2. Sampling is the expensive part, so batches get reused. Importance sampling and the surrogate objective; token-level ratios; the performance-difference lemma; TRPO's lower bound. The 3-action simplex: KL balls shrink near the edges; vanilla vs natural gradient. | Exact: KL contours on the simplex and both gradient flows from the same start (the natural gradient moves every logit by its advantage). The bound is schematic. |
| 7 | `PPO` | The clipped objective; case analysis for A > 0 and A < 0 (where the gradient is zero); the clip as a per-token probability window. RLHF with PPO: four networks and a per-token KL reward. | Windows for ε = 0.2: 0.9 → [0.72, 1], 0.01 → [0.008, 0.012]. Reusing batches on the adder (3 seeds): 1 update per batch reaches 75% after 5 steps; 16 updates reach 93%; unclipped, one seed falls to 91% at step 40; clipped ends at 99.1%. |
| 8 | `Preferences` | Part 3. Comparisons instead of a checker (illustrative pair). Bradley–Terry from Gumbel noise: the difference of two Gumbels is logistic. The reward model's likelihood; a per-prompt offset is just a baseline. Goodhart's law. | Exact Gumbel and logistic densities; P(A ≻ B) = σ(2.2) = 0.90. Over-optimization curve schematic, after Gao, Schulman & Hilton. |
| 9 | `KLOptimum` | The KL-regularized objective solved exactly: π* ∝ π_ref e^{r/β}. The tilt only reweights; it never invents. The tilted family is the natural-gradient path. The reward–KL frontier. Schulman's KL estimators; k3's gradient points at the reversed KL. | The adder's real answer distribution tilted as β falls: P(right) 0.59 → 1.00, right answers keeping their 0.54 : 0.46 proportions. Frontier over 48 problems: always right costs 0.39 nats; the GRPO run sits below it at about twice that KL. Monte Carlo estimator table (2M samples): std/KL 20.0, 1.42, 1.42 at KL = 0.005. |
| 10 | `DPO` | Invert the optimum: every policy implies a reward. Z cancels in Bradley–Terry, leaving the DPO loss; its gradient weight. Offline DPO and likelihood displacement. | DPO on the adder, 4,096 fixed right-vs-wrong pairs (β = 0.1, lr 1e-5): 69% → 80% at step 100 → 0.7% at step 300, as the preferred answers' log-probability falls 10 nats and the rejected ones' 18. |
| 11 | `GRPO` | Part 4. The group mean as a free baseline; mean-centering = (G − 1)/G × leave-one-out (RLOO), so unbiased. The std division turns the objective into 2 arcsin √p (Fisher–Rao arc length); exact finite-G weights. Zero-variance groups. The full GRPO objective, annotated. | A real group of 8 answers to 5675 + 5563: R̄ = 0.625, advantages +0.375 / −0.625. Exact weight curves κ_G(p) for G = 2, 4, 8, 64. P(all equal) = p^G + (1 − p)^G for G = 4, 8, 16. |
| 12 | `RealRun` | GRPO trains the adder; RL sharpened rather than taught: direct answers stopped slipping. Six algorithms reach the same accuracy with different behavior. | GRPO, 3-seed means: 70% → 98% right within 40 steps; showing work 28% → 41%; direct answers 59% → 97% right. The five likeliest answers before and after. REINFORCE, RLOO, GRPO, Dr. GRPO, DAPO-style and PPO + GAE, 3 seeds each: show-work rates from 0% to about 50%. |
| 13 | `Biases` | GRPO's per-answer 1/|o_i| makes a token's push depend on its answer's length (short right answers favored, long wrong ones punished less). DAPO's token mean and Dr. GRPO's constant. What eleven open-source libraries actually do. | Per-token push +0.167 / +0.077 / −0.167 / −0.077. Show-work rate after 120 steps: REINFORCE with 1/|o_i| 0%, with a constant 50%; GRPO 41%, DAPO-style 48%, Dr. GRPO 50%. Defaults read from the code of nine libraries. |
| 14 | `Entropy` | Entropy collapse. ∂H/∂z for a softmax; ΔH ≈ −Cov(log π, Δz); vanilla and natural policy gradients; why rewarding confident tokens drains entropy. Clip-higher. | The GRPO run's next-token entropy falls 0.18 → 0.044 (4.2×). Two exact 5-token examples (H 1.12 → 0.36 vs 1.12 → 1.40). Measured batch covariance: positive in 87% of batches; 9-step averages correlate −0.64 with the entropy change. *Quoted:* DAPO, AIME 30% → 50%. |
| 15 | `Sharpening` | pass@k and its unbiased estimator. Sharpening vs discovery; the optimum cannot leave the reference's support; the 2025–26 debate. Bits per episode, sparse updates, RL's Razor. On-policy distillation. | Worked estimator: 1 − C(5,3)/C(8,3) = 0.821. pass@k from 128 samples × 300 problems: base 70.4% at k = 1, every problem solved by k = 16; after RL 99.2% at k = 1. *Quoted:* Qwen3-8B AIME 2024, RL 67.6% (17,920 GPU-hours) vs on-policy distillation 74.4% (1,800). |
| 16 | `Mismatch` | Part 5. Inference engines and trainers compute different probabilities from the same weights, so "on-policy" RL is off-policy. Sequence-level weights as random walks; GSPO's geometric mean. TIS, masking (IcePop), GSPO, CISPO, numeric fixes. Asynchronous RL and staleness. | Qwen3-0.6B, 8 traces × 768 tokens: 25% of tokens > 1% off when re-scored in fp32 (1.4% > 10%); 24% when re-scored in one bf16 pass; 0.8% of near-certain tokens vs 98% of tokens with p < 0.01. Whole-answer weights from 0.48 to 8.45. |
| 17 | `Scaling` | RL's growing share of compute. ScaleRL's sigmoid law, fitted to our runs: reuse changes the speed, not the ceiling. Agentic RL: environments as reward functions, tool outputs masked. Reward hacking. The state of play in October 2026. | Sigmoid fits for 1 / 4 / 16 updates per batch: A = 1.00 for all, C_mid = 1.1 × 10¹¹, 3.0 × 10¹⁰, 1.4 × 10¹⁰ FLOPs. *Quoted:* compute shares, environment counts, hack patterns and the Anthropic and OpenAI findings. |
| 18 | `Outro` | The whole family as one chain of estimators, each the log-derivative trick plus one idea about noise or trust. | |

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
  slips: direct answers go from 59% to 97% right, while showing work only rises
  from 28% to 41% (the runs' own evaluations, from step 0). pass@k before RL: 70.4% (k = 1), 99.9% (k = 8), 100%
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
