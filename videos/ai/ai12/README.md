# AI, Built — Part 12: The Mathematics of Scale

Part 12 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the end of Act II. What happens to a network as it grows, and how the field
learned to predict it: infinitely wide networks (Gaussian processes, the neural tangent kernel, lazy training); μP,
derived, and the learning rate carried across width and depth; the critical batch; scaling laws measured on our own
sweep and Chinchilla's compute-optimal split derived by Lagrange; what Kaplan missed and the 2024 replication;
over-training for inference, repeated data, experts and precision; why power laws at all (data manifolds and quanta);
emergence against metric artifacts; grokking and its Fourier circuit; and the frontier of 2024–26 (test-time compute,
reinforcement-learning scaling, densing, and the argument over whether pretraining has stalled). Every model is trained
by `compute.py` on the CPU (PyTorch), several times over where a comparison is made. Part 14 tells the story of
GPT-3, Gopher and Chinchilla and of tokens per parameter model by model, and Part 18 does the FLOP accounting of a
real run; this part does the mathematics behind them.

* **A straight line on log axes.** The sweep's runs drawn at the compute each cost; the frontier, a floor plus a power
  law; how we got here, 1994–2026 (Neal; Banko & Brill 2001; Hestness et al. 2017; Jacot et al. 2018; Kaplan et al.
  2020; Chinchilla, μTransfer and grokking 2022; data limits and the mirage 2023; o1 2024; RL at pretraining scale
  2025; larger base models 2026); the plan.
* **1. Infinitely wide.** A one-layer ReLU net's output over 6,000 random starts tends to a Gaussian of variance
  (x² + 1)/2 as the width grows (excess kurtosis falling to 0; Neal 1994/1996; Lee et al. 2018); five random wide nets as
  samples of a Gaussian process; the tangent kernel defined and gradient flow derived as kernel regression (Jacot,
  Gabriel & Hongler 2018); measured at widths 30 … 30,000, three seeds: how far the weights move (∝ n^−1/2) and the
  kernel (closer to n^−1, as Dyer & Gur-Ari 2019 derived for its expected change), and the trained function against its
  own linearization, replayed (Lee et al. 2019).
* **2. Lazy.** Part 11's character model trained with neural-tangent step sizes at widths 32 … 2,048: its features
  change less and less; Chizat, Oyallon & Bach (2019); the lazy network is a kernel method (Part 6; Part 8's
  over-parametrized fits); a task that needs a feature, y = (w*·x)² − 1 in 32 dimensions from 256 examples, trained in
  the neural-tangent and the mean-field (μP) parametrizations at width 1,024, three seeds each, against kernel regression
  with the initial kernel; every hidden unit's weights replayed through training (the rich units turn toward w*).
* **3. μP, derived.** The central limit theorem against the law of large numbers: random weights add like √n, an
  update aligned with its input like n; η ∝ 1/n; μP's table for Adam (Yang & Hu 2021; Yang et al. 2022, Table 3); the
  coordinate check at widths 64 … 4,096 in both parametrizations.
* **4. One learning rate for every width.** Learning-rate sweeps at widths 64, 256 and 1,024, standard and μP, two
  seeds; the cost of copying the small model's rate; Tensor Programs V (40M → 6.7B GPT-3, 7% of the cost); Everett
  et al. (2024); Llama 4's MetaP (2025).
* **5. Deeper and deeper.** Branch multipliers L^−α: none, depth-μP (1/√L; Yang et al. 2023; Bordelon et al. 2023)
  and CompleteP (1/L; Dey et al. 2025, Table 1); a deep residual character model at depths 2 … 32 swept over nine
  learning rates in all three, two seeds; the best loss by depth and the cost of copying the shallow model's rate;
  CompleteP's 12–34% compute savings.
* **6. How big a batch?** McCandlish et al. (2018) derived: the best step, the noise scale, steps against examples
  (S/S_min − 1)(E/E_min − 1) = 1; measured at batches 32 … 4,096 (the best of three learning rates each) to three loss
  levels, with the critical batch fitted, against the noise scale measured from gradients; Kaplan's B_crit(L); the
  critical batch grows with data, not size (Zhang et al. 2024; Bergsma et al. 2025); DeepSeek-V3's batch ramp.
* **7. Scaling laws, measured.** Hestness et al. (2017): power laws in four domains and three regions; Kaplan et al.
  (2020); our sweep: 11 widths × lengths 2¹⁶ … 2²⁴ characters, one constant-rate trunk per width with a cool-down branch
  at each length (Hägele et al. 2024); L(N) and L(D) with power-law-plus-floor fits; seed-to-seed spread.
* **8. Chinchilla's valley.** L(N, D) = E + A/N^α + B/D^β fitted (Huber on log loss, L-BFGS from a grid, as Hoffmann et
  al. 2022); the compute-optimal split by a Lagrange multiplier; the fitted surface in 3D with the iso-FLOP lines and
  the valley floor; Chinchilla's three methods on our runs (envelope, iso-FLOP parabolas, the fit, with bootstrap
  intervals) against Chinchilla's 0.50 / 0.49 / 0.46 and Kaplan's 0.73.
* **9. What Kaplan missed.** Gopher (280B, 300B tokens) against Chinchilla (70B, 1.4T) at the same compute; counting
  parameters without the embedding and output layers, on our own runs (Pearce & Song 2024); last-layer cost, warmup and
  β₂ (Porian et al. 2024); Epoch AI's replication of approach 3 (Besiroglu et al. 2024: a = 0.51, about 20 tokens per
  parameter; the published interval would need 600,000 runs).
* **10. Trained for the long run.** The price of a smaller model for the same loss, from the fit, checked against our
  runs; inference in the budget (Sardana et al. 2023): minimize 6ND + 2NT at fixed loss; the best tokens per parameter
  against lifetime use; Llama 3's 1,900 tokens per parameter.
* **11. When the data runs out.** 4.2 million characters of training drawn from 4.2 million down to 16,384 distinct
  ones (1 … 256 epochs), three seeds; the effective data read off the fresh-data curve and Muennighoff et al.'s R*
  fitted; the stock of public text (Villalobos et al. 2024); Qwen3's 36 trillion tokens.
* **12. Experts and bits.** The hidden layer split into 1 … 32 experts, one used per character, two seeds, against the
  dense sweep (Clark et al. 2022; Krajewski et al. 2024; DeepSeek-V3); post-training quantization to 8 … 3 bits on
  every endpoint of the sweep, the damage against training length, and Kumar et al.'s form fitted.
* **13. Why power laws?** The data-manifold derivation (Sharma & Kaplan 2020), checked with N linear pieces on
  manifolds of dimension 1, 2, 4, 8; the quantization model (Michaud et al. 2023), derived, and its multitask sparse
  parity in small (32 Zipfian subtasks, widths 8 … 512, two seeds): subtasks learned suddenly, one at a time; the
  average smooth; the final loss against the number of subtasks learned, on the theory's curve Σ_{k>n} p_k, and the
  finite task's tail running out.
* **14. Emergence, or a mirage?** Wei et al. (2022); Schaeffer, Miranda & Koyejo (2023): p^L; our models on a checkable
  task (write the next characters exactly), per-character against whole-answer scores; quanta's real cliffs (every
  subtask at every width, as a grid); Du et al. (2024); Snell et al. (2024).
* **15. Grokking.** (a + b) mod 97 from 40% of the table (Power et al. 2022), the run replayed; weight decay swept over
  five values, three seeds; the number vectors' Fourier spectrum lighting up through training, the five key
  frequencies, the circles; the trigonometric circuit and how much of the trained scores it explains (Nanda et al.
  2023); the tangent kernel's distance from its start (Fort et al. 2020), with and without weight decay, against Kumar
  et al.'s lazy-to-rich account (2023).
* **16. Scaling the answer.** o1 (2024; its two scaling plots drawn as a labelled schematic); pass@k on our checkable
  task over five orders of magnitude of tries; the power law of −log pass@k derived from the hardest problems
  (Schaeffer et al. 2025) and checked against the measured tail; tries against size, and what the tries cost in
  operations; reinforcement learning's sigmoid (Khatri et al. 2025); Grok 4 (2025).
* **17. Has pretraining stalled?** The debate, 2024–26 (Sutskever; GPT-4.5; Grok 4; Epoch AI on GPT-5; Gemini 3;
  Pichai on Gemini 4; Microsoft's MAI-Base-2); our law fitted on the cheapest runs and predicting the rest; the
  slowness of the curve; efficiency (Ho et al. 2024; the densing law, Xiao et al. 2024).
* **Recap** in eight pictures from the part's own results, where it comes back, six problems, Part 13's teaser,
  references.

Every chapter follows the series' lecture standard: its card asks the motivating question; the derivations run
step by step with a reason in the margin; a pause-and-predict card comes before each chapter's main experiment;
the computed check answers it; and a takeaway card closes the chapter with a link forward.

Run from the repo root:

```
python tools/make.py ai12                 # compute what is missing, then build (English and Chinese)
python -m videos.ai.ai12.compute          # every experiment on its own (about 3 CPU-hours on one thread)
python -m videos.ai.ai12.compute sweep    # one item; the others: nngp ntk lazy rich coord mup depth batch chinchilla
                                          #   repeat moe precision quanta manifold emerge testtime grok
python tools/build.py ai12                # English
python tools/build.py ai12 --lang zh      # Chinese
```

`compute.py` needs Part 1's novels (`.cache/ai1`, read through Part 11's `char_data()`). Everything is seeded and
runs single-threaded (`AI12_THREADS`, default 1); `AI12_WORKERS=4` runs the learning-rate sweeps in four processes
(spawn) with the same results. The long items resume where they stopped: the scaling sweep (`sweep`, about an hour)
saves each finished endpoint in `.cache/ai12/sweep.partial.json` (its arrays in `.cache/ai12/sweep_parts/`) and the
run in progress in `.cache/ai12/sweep_s<seed>_w<width>.ckpt.pt`; `mup`, `depth`, `batch`, `repeat`, `moe`, `quanta`
and `grok` save each finished run in their `.partial.json`. No other part reads `.cache/ai12/`.

## Computed results

*(filled in from `.cache/ai12/` by the run that made the video; the narration says whichever way they come out.)*

RESULTS_PLACEHOLDER

## Fact-check notes

Recent claims were checked against their primary reports: Sutskever's NeurIPS 2024 talk ("Pre-training as we know it
will unquestionably end"; "we have but one internet", from transcripts of the recorded talk); the GPT-4.5 system card
(27 February 2025: "our largest and most knowledgeable model yet", "scales pre-training further"); xAI's Grok 4
announcement (9 July 2025: reinforcement learning "at pretraining scale", "over an order of magnitude more compute");
Epoch AI's *Why GPT-5 used less training compute than GPT-4.5* (26 September 2025); Microsoft AI's *Frontier
Pre-training at Microsoft AI* (15 October 2026: MAI-Base-2, 80B active / 2.8T total parameters, 16k GB200s for 38 days,
forecast from scaling ladders); Meta's Llama 4 post (5 April 2025: MetaP; more than 30 trillion tokens); Dey et al.,
CompleteP (Table 1; 11.8% and 34.4% FLOP savings); Khatri et al. (2025: the sigmoid, 400,000 GPU-hours, a
100,000-GPU-hour run); Besiroglu et al. (2024: Table 1; 600,000 against fewer than 500 experiments); Hoffmann et al.
(2022: Table 2, a = 0.50, 0.49, 0.46); Kaplan et al. (2020: Eqs. 1.1–1.8, B_crit); Hestness et al. (2017: exponents
−0.07 to −0.35; word LMs −0.066; three regions); Muennighoff et al. (2023: Eq. 5, R*_D = 15.39); Villalobos et al.
(2024: an effective stock of about 4 × 10¹⁴ tokens, full use between 2026 and 2032, median 2028); Kumar et al. (2024:
Eq. 2, N_eff = N(1 − e^(−P/γ)), 7–8 bits); DeepSeek-V3 (671B / 37B, 256 routed experts with 8 active; batch 3,072 →
15,360 over 469B tokens); Schaeffer et al. (2025: −log pass@k ∼ CΓ(b)k^(−b)); Brown et al. (2024: 15.9% → 56% on
SWE-bench Lite); Ho et al. (2024: halving every 8 months, 5–14); Xiao et al. (2024: density doubles about every three
months). Two items rest on reports of a primary source that could not be fetched directly: Oriol Vinyals's post on
Gemini 3 (X, November 2025: "The delta between 2.5 and 3.0 is as big as we've ever seen", quoted identically by
several outlets) and Sundar Pichai's words on Alphabet's Q2 2026 earnings call (22 July 2026: "For the next generation
of frontier, you're going to need much larger base models. We are now training Gemini 4", from transcripts and
9to5Google). OpenAI's o1 post (September 2024) was blocked to the fetcher; its scaling claim is quoted from
reproductions of the post.

## References

Books: D. A. Roberts, S. Yaida & B. Hanin, *The Principles of Deep Learning Theory* (2022); S. J. D. Prince,
*Understanding Deep Learning* (2023).

Papers: Neal (1996); Lee et al., *Deep Neural Networks as Gaussian Processes* (2018); Jacot, Gabriel & Hongler (2018);
Lee et al., *Wide Neural Networks of Any Depth Evolve as Linear Models* (2019); Dyer & Gur-Ari, *Asymptotics of Wide
Networks from Feynman Diagrams* (2019); Fort et al., *Deep Learning versus Kernel Learning* (2020); Chizat, Oyallon &
Bach, *On Lazy Training* (2019); Yang & Hu, *Tensor Programs IV* (2021); Yang et al., *Tensor Programs V* (2022); Yang,
Yu, Zhu & Hayou, *Tensor Programs VI* (2023); Bordelon et al., *Depthwise Hyperparameter Transfer in Residual Networks*
(2023); Everett et al., *Scaling Exponents Across Parameterizations and Optimizers* (2024); Dey et al., *Don't be lazy:
CompleteP* (2025); McCandlish et al., *An Empirical Model of Large-Batch Training* (2018); Zhang et al., *How Does
Critical Batch Size Scale in Pre-training?* (2024); Bergsma et al., *Power Lines* (2025); Banko & Brill (2001); Hestness
et al., *Deep Learning Scaling is Predictable, Empirically* (2017); Kaplan et al., *Scaling Laws for Neural Language
Models* (2020); Hoffmann et al., *Training Compute-Optimal Large Language Models* (2022); Besiroglu et al., *Chinchilla
Scaling: A Replication Attempt* (2024); Pearce & Song, *Reconciling Kaplan and Chinchilla Scaling Laws* (2024); Porian
et al., *Resolving Discrepancies in Compute-Optimal Scaling of Language Models* (2024); Hägele et al., *Scaling Laws and
Compute-Optimal Training Beyond Fixed Training Durations* (2024); Sardana et al., *Beyond Chinchilla-Optimal* (2023);
Muennighoff et al., *Scaling Data-Constrained Language Models* (2023); Villalobos et al., *Will We Run Out of Data?*
(2024); Clark et al., *Unified Scaling Laws for Routed Language Models* (2022); Krajewski et al., *Scaling Laws for
Fine-Grained Mixture of Experts* (2024); Kumar et al., *Scaling Laws for Precision* (2024); Sharma & Kaplan, *A Neural
Scaling Law from the Dimension of the Data Manifold* (2020); Michaud et al., *The Quantization Model of Neural Scaling*
(2023); Wei et al., *Emergent Abilities of Large Language Models* (2022); Schaeffer, Miranda & Koyejo, *Are Emergent
Abilities of Large Language Models a Mirage?* (2023); Du et al., *Understanding Emergent Abilities from the Loss
Perspective* (2024); Snell et al., *Predicting Emergent Capabilities by Finetuning* (2024); Power et al., *Grokking*
(2022); Nanda et al., *Progress Measures for Grokking via Mechanistic Interpretability* (2023); Kumar, Bordelon,
Gershman & Pehlevan, *Grokking as the Transition from Lazy to Rich Training Dynamics* (2023); Brown et al., *Large
Language Monkeys* (2024); Schaeffer et al., *How Do Large Language Monkeys Get Their Power (Laws)?* (2025); Khatri et
al., *The Art of Scaling Reinforcement Learning Compute for LLMs* (2025); Ho et al., *Algorithmic Progress in Language
Models* (2024); Xiao et al., *Densing Law of LLMs* (2024); DeepSeek-AI, DeepSeek-V3 (2024); Qwen Team, Qwen3 (2025);
Meta, Llama 3 (2024), Llama 4 (2025).

## Problems, with solutions

**1. The tangent kernel freezes.** For f(x) = (1/√n) Σⱼ aⱼ φ(wⱼ x) with independent 𝒩(0, 1) weights, write the tangent
kernel Θ(x, x′) as an average over the n units, and show that its fluctuation is O(1/√n). By how much does one gradient
step move each aⱼ?

*Solution.* The gradient with respect to aⱼ is φ(wⱼx)/√n, and with respect to wⱼ it is aⱼ φ′(wⱼx) x/√n, so
Θ(x, x′) = (1/n) Σⱼ [φ(wⱼx) φ(wⱼx′) + aⱼ² φ′(wⱼx) φ′(wⱼx′) x x′]: an average of n independent, identically distributed
terms. By the law of large numbers it tends to its expectation, a fixed kernel; by the central limit theorem its
fluctuation around it is O(1/√n). A gradient step on the squared error changes aⱼ by −η (1/m) Σᵢ rᵢ φ(wⱼxᵢ)/√n =
O(1/√n): each weight moves by O(1/√n), and the vector of n weights, of length O(√n), by a relative O(1/√n).

**2. μP's learning rate.** A hidden layer h = Wx has n inputs of size Θ(1). Show that the update ΔW = −η g xᵀ changes
hᵢ by η gᵢ ‖x‖² = Θ(ηn), while a random W with variance σ² gives |hᵢ| = Θ(σ√n). Deduce μP's η ∝ 1/n.

*Solution.* (ΔW x)ᵢ = −η gᵢ Σⱼ xⱼ xⱼ = −η gᵢ ‖x‖², and ‖x‖² is a sum of n positive terms of size Θ(1), so Θ(n): the
change is Θ(ηn). For a random W, hᵢ = Σⱼ Wᵢⱼ xⱼ is a sum of n independent terms with mean 0 and variance σ²xⱼ², so its
standard deviation is σ‖x‖ = Θ(σ√n). Keeping h of size Θ(1) needs σ ∝ 1/√n; keeping its change Θ(1) needs η ∝ 1/n.
With Adam the step is about η per entry whatever the gradient's size, so ΔW x is again a sum of n aligned terms, and the
hidden learning rate must again shrink like 1/n.

**3. Chinchilla's split.** From L = E + AN^(−α) + BD^(−β) and C = 6ND, derive N_opt and D_opt. With Chinchilla's
published fit and Besiroglu et al.'s refit, compute the tokens per parameter at C = 5.76 × 10²³.

*Solution.* Substituting D = C/6N and setting dL/dN = 0: αA N^(−α−1) = βB (C/6)^(−β) β⁻¹·β N^(β−1), i.e.
αA N^(−α) = βB D^(−β). With G = (αA/βB)^(1/(α+β)) this gives N_opt = G (C/6)^(β/(α+β)) and D_opt = G⁻¹ (C/6)^(α/(α+β)).
Published fit (E = 1.69, A = 406.4, B = 410.7, α = 0.3392, β = 0.2849): N_opt ≈ 4.0 × 10¹⁰, D_opt ≈ 2.4 × 10¹², about
59 tokens per parameter, far from Chinchilla's own 70B on 1.4T. Refit (A = 482.0, B = 2085.4, α = 0.3478, β = 0.3658):
N_opt ≈ 7.2 × 10¹⁰, D_opt ≈ 1.3 × 10¹², about 18 tokens per parameter, close to the 20 of approaches 1 and 2 and to
Chinchilla itself.

**4. Training for inference.** Minimize 6ND + 2NT subject to L(N, D) = L*. Show that the optimal N decreases as the
inference tokens T grow, and find its limit as T → ∞.

*Solution.* With a multiplier μ: 6D + 2T = μαA N^(−α−1) and 6N = μβB D^(−β−1). Eliminating μ,
αA N^(−α) / (βB D^(−β)) = 1 + T/(3D). At T = 0 the two marginal gains are equal (Chinchilla); as T grows the parameter
term's marginal gain must exceed the data term's, which on the level set L = L* means a smaller N and a larger D. As
T → ∞ the cost is dominated by 2NT, so N is pushed to the smallest value from which L* can be reached at all:
N_min = (A/(L* − E))^(1/α), with D → ∞.

**5. Repeated data.** Show that D′ = U + U R*(1 − e^(−R/R*)) satisfies D′ ≈ U(1 + R) for R ≪ R*, and D′ → U(1 + R*)
as R → ∞.

*Solution.* For R ≪ R*, 1 − e^(−R/R*) ≈ R/R*, so D′ ≈ U + U R* · R/R* = U(1 + R): the total read, every repeat as good
as new. As R → ∞, e^(−R/R*) → 0 and D′ → U + U R* = U(1 + R*): no amount of repetition is worth more than 1 + R* passes
of new data.

**6. The power law of many tries.** If one try succeeds with probability p, and p has density c p^(b−1) near 0, show
that 1 − pass@k ∼ c Γ(b) k^(−b). What is b for p uniform on [0, 1]?

*Solution.* 1 − pass@k = ∫₀¹ (1 − p)^k f(p) dp. For large k, (1 − p)^k ≈ e^(−kp) is negligible unless p ≲ 1/k, where
f(p) ≈ c p^(b−1); so 1 − pass@k ≈ c ∫₀^∞ e^(−kp) p^(b−1) dp = c Γ(b) k^(−b) (substitute u = kp). Each problem's failure
falls exponentially; the power law comes from the problems with tiny p. For p uniform, f = 1, so b = 1 and c = 1:
indeed ∫₀¹ (1 − p)^k dp = 1/(k + 1) ≈ k⁻¹.

## 习题与解答

**1. 切线核被冻结。** 对 f(x) = (1/√n) Σⱼ aⱼ φ(wⱼ x)，权重相互独立、服从 𝒩(0, 1)，把切线核 Θ(x, x′) 写成 n 个单元上的平均，
并证明它的涨落是 O(1/√n)。一步梯度下降让每个 aⱼ 移动多少？

*解答。* 对 aⱼ 的梯度是 φ(wⱼx)/√n，对 wⱼ 的梯度是 aⱼ φ′(wⱼx) x/√n，所以
Θ(x, x′) = (1/n) Σⱼ [φ(wⱼx) φ(wⱼx′) + aⱼ² φ′(wⱼx) φ′(wⱼx′) x x′]：n 个独立同分布项的平均。由大数定律，它趋于自己的期望，
一个固定的核；由中心极限定理，它在这个期望附近的涨落是 O(1/√n)。在平方误差上走一步梯度下降，aⱼ 变化
−η (1/m) Σᵢ rᵢ φ(wⱼxᵢ)/√n = O(1/√n)：每个权重移动 O(1/√n)，长度为 O(√n) 的 n 维权重向量的相对变化也是 O(1/√n)。

**2. μP的学习率。** 一个隐藏层 h = Wx 有 n 个大小为 Θ(1) 的输入。证明更新 ΔW = −η g xᵀ 让 hᵢ 变化 η gᵢ ‖x‖² = Θ(ηn)，
而方差为 σ² 的随机 W 给出 |hᵢ| = Θ(σ√n)。由此推出 μP 的 η ∝ 1/n。

*解答。* (ΔW x)ᵢ = −η gᵢ Σⱼ xⱼ xⱼ = −η gᵢ ‖x‖²，而 ‖x‖² 是 n 个大小为 Θ(1) 的正项之和，所以是 Θ(n)：变化量是 Θ(ηn)。
对随机的 W，hᵢ = Σⱼ Wᵢⱼ xⱼ 是 n 个独立、均值为0、方差为 σ²xⱼ² 的项之和，标准差为 σ‖x‖ = Θ(σ√n)。要让 h 保持 Θ(1)，需要
σ ∝ 1/√n；要让它的变化保持 Θ(1)，需要 η ∝ 1/n。用Adam时，每个元素的步长大约就是 η，与梯度大小无关，所以 ΔW x 仍是 n 个
同向项之和，隐藏层的学习率同样要按 1/n 缩小。

**3. Chinchilla的分配。** 由 L = E + AN^(−α) + BD^(−β) 和 C = 6ND，推导 N_opt 和 D_opt。分别用Chinchilla发表的拟合和
Besiroglu等人的重新拟合，计算 C = 5.76 × 10²³ 时每个参数的词元数。

*解答。* 代入 D = C/6N，令 dL/dN = 0，得 αA N^(−α) = βB D^(−β)。记 G = (αA/βB)^(1/(α+β))，就有
N_opt = G (C/6)^(β/(α+β))，D_opt = G⁻¹ (C/6)^(α/(α+β))。发表的拟合（E = 1.69，A = 406.4，B = 410.7，α = 0.3392，
β = 0.2849）：N_opt ≈ 4.0 × 10¹⁰，D_opt ≈ 2.4 × 10¹²，每个参数约59个词元，与Chinchilla自己的700亿参数、1.4万亿词元相去甚远。
重新拟合（A = 482.0，B = 2085.4，α = 0.3478，β = 0.3658）：N_opt ≈ 7.2 × 10¹⁰，D_opt ≈ 1.3 × 10¹²，每个参数约18个词元，
接近方法一和方法二的20，也接近Chinchilla本身。

**4. 为推理而训练。** 在 L(N, D) = L* 的约束下最小化 6ND + 2NT。证明最优的 N 随推理词元数 T 增大而减小，并求 T → ∞ 时的极限。

*解答。* 引入乘子 μ：6D + 2T = μαA N^(−α−1)，6N = μβB D^(−β−1)。消去 μ，得 αA N^(−α) / (βB D^(−β)) = 1 + T/(3D)。
T = 0 时两个边际收益相等（Chinchilla）；T 增大时，参数项的边际收益必须超过数据项的，在 L = L* 这条等值线上，这意味着更小的
N、更大的 D。T → ∞ 时成本由 2NT 主导，N 被压到还能达到 L* 的最小值：N_min = (A/(L* − E))^(1/α)，同时 D → ∞。

**5. 重复的数据。** 证明 D′ = U + U R*(1 − e^(−R/R*)) 在 R ≪ R* 时满足 D′ ≈ U(1 + R)，在 R → ∞ 时 D′ → U(1 + R*)。

*解答。* R ≪ R* 时，1 − e^(−R/R*) ≈ R/R*，所以 D′ ≈ U + U R* · R/R* = U(1 + R)：读了多少就值多少，每次重复都和新数据一样好。
R → ∞ 时，e^(−R/R*) → 0，D′ → U + U R* = U(1 + R*)：无论重复多少遍，都抵不上 1 + R* 遍新数据。

**6. 多次尝试的幂律。** 若一次尝试成功的概率为 p，且 p 在0附近的密度为 c p^(b−1)，证明 1 − pass@k ∼ c Γ(b) k^(−b)。
p 在 [0, 1] 上均匀分布时，b 是多少？

*解答。* 1 − pass@k = ∫₀¹ (1 − p)^k f(p) dp。k 很大时，(1 − p)^k ≈ e^(−kp)，只有 p ≲ 1/k 时才不可忽略，而那里
f(p) ≈ c p^(b−1)；所以 1 − pass@k ≈ c ∫₀^∞ e^(−kp) p^(b−1) dp = c Γ(b) k^(−b)（令 u = kp）。每道题的失败率按指数下降，
幂律来自 p 极小的那些题。p 均匀分布时 f = 1，所以 b = 1，c = 1：确实 ∫₀¹ (1 − p)^k dp = 1/(k + 1) ≈ k⁻¹。

## Glossary (new terms of this part)

| English | 中文 |
|---|---|
| scaling law, power law plus a floor | 规模定律，幂律加下限 |
| irreducible loss, reducible loss | 不可约损失，可约损失 |
| infinite-width limit | 无限宽极限 |
| neural network Gaussian process (NNGP) | 神经网络高斯过程（NNGP） |
| neural tangent kernel (NTK), tangent features | 神经正切核（NTK），切线特征 |
| linearization (of a network) | （网络的）线性化 |
| lazy training, lazy regime | 惰性训练，惰性区 |
| rich regime, feature learning | 丰富区，特征学习 |
| mean-field parametrization | 平均场参数化 |
| standard parametrization (SP) | 标准参数化（SP） |
| maximal update parametrization (μP) | 最大更新参数化（μP） |
| coordinate check | 坐标检查 |
| hyperparameter transfer (μTransfer) | 超参数迁移（μTransfer） |
| fan-in, fan-out | 扇入，扇出 |
| branch multiplier, depth-μP, CompleteP | 分支乘子，深度μP，CompleteP |
| lazy in depth | 深度上的惰性 |
| critical batch size, gradient noise scale | 临界批量大小，梯度噪声尺度 |
| steps–examples trade-off | 步数与样本数的权衡 |
| warmup-stable-decay (WSD), cool-down branch | 预热-稳定-衰减（WSD），冷却分支 |
| compute-optimal, Chinchilla-optimal | 计算最优，Chinchilla最优 |
| iso-FLOP curve, iso-FLOP valley | 等算力曲线，等算力谷 |
| Lagrange multiplier | 拉格朗日乘子 |
| non-embedding parameters | 非嵌入参数 |
| bootstrap (resampling) | 自助法（重抽样） |
| over-training, inference-aware scaling | 过度训练，计入推理的规模定律 |
| data-constrained scaling, epochs, effective data | 数据受限的规模定律，轮数（epoch），有效数据量 |
| effective parameter count | 有效参数量 |
| post-training quantization (PTQ), round to nearest | 训练后量化（PTQ），就近取整 |
| precision scaling law | 精度规模定律 |
| fine-grained experts, granularity | 细粒度专家，粒度 |
| data manifold, intrinsic dimension | 数据流形，内在维数 |
| quantization model of scaling, quanta | 规模的量子化模型，量子 |
| multitask sparse parity, Zipf's law | 多任务稀疏奇偶性，齐普夫定律 |
| emergent ability, exact match, metric artifact | 涌现能力，精确匹配，度量造成的假象 |
| grokking, memorization, generalization | 顿悟（grokking），记忆，泛化 |
| weight decay | 权重衰减 |
| Fourier spectrum, key frequencies | 傅里叶频谱，关键频率 |
| kernel distance | 核距离 |
| pass@k, coverage, repeated sampling | pass@k，覆盖率，重复采样 |
| test-time compute | 测试时计算 |
| sigmoidal compute–performance curve | S形的算力-性能曲线 |
| densing law, capability density | 致密化定律，能力密度 |
| algorithmic progress | 算法进步 |
| scaling ladder | 规模阶梯 |
