# AI, Built — Part 28: Reasoning

Part 28 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). How language models learned to reason, from "let's think step by step" (2022) to
o1 (2024), DeepSeek-R1 (2025) and the 2026 frontier: why a chain of thought adds computation; many chains and a vote;
grading answers or grading steps; reinforcement learning from a checker, with GRPO derived, its KL estimators and its
successors (Dr. GRPO, DAPO, GSPO, CISPO); entropy collapse; how long to think; whether RL widens what a model can
solve; spending computation at answer time; search over thoughts; thinking without words and tiny recursive models;
proofs a machine can check; and ARC-AGI. Every experiment runs on three tiny transformers trained on this computer:
parity, two-digit addition, and a "think or answer" model that sums lists of digits and may write its running total
first.

* **From "let's think step by step" to o1 and R1.** Chain-of-thought prompting (Wei et al. 2022: PaLM 540B on GSM8K,
  17.9% → 56.9%, with the paper's Figure 1 example); zero-shot "Let's think step by step" (Kojima et al. 2022:
  MultiArith 17.7% → 78.7%); o1 (September 2024; AIME 2024: GPT-4o 12%, o1 74% with one try, 83% by a vote of 64, 93%
  reranking 1,000 with a learned scorer); R1-Zero (15.6% → 71.0%, 86.7% by a vote of 64; DeepSeek-AI 2025); gold-medal
  IMO 2025 solutions in natural language; ARC-AGI-3 (March 2026), where every frontier model started below 1%; the
  questions of the part and what it covers.
* **1. Thinking out loud is computing.** Parity of 16 bits for a 2-layer transformer: answering at once stays at
  chance (49.9%, three runs 49.4–50.9%), writing the running parity first reaches 99.6% (98.8–100%); 4 bits:
  everything 100%; 8 bits: at once 46.7%, chain 100%. Depth: L steps in a row at once, L(k + 1) with k tokens of
  thought. Merrill & Sabharwal (2023): fixed depth with O(log n)-bit numbers stays in TC⁰; Li, Liu, Zhou & Ma (2024):
  T steps of thought simulate a circuit of size T, polynomially many decide P; Furst–Saxe–Sipser (1984), Barrington
  (1989), Hahn (2020), Feng et al. (2023); filler dots add positions but not sequential steps (Pfau, Merrill & Bowman
  2024; ours: 49.4%); the chain model's training replayed with its chains at each checkpoint.
* **2. Many chains, one vote.** The testbed: a 2-layer transformer that sums lists of 2–9 digits and may write the
  running total first (1,500 supervised steps; one sample at temperature 1: 90% → 38% at once, 96% → 64% thinking;
  left to choose, it thinks 65% of the time). Self-consistency (Wang et al. 2022, +17.9 points on GSM8K). One 7-digit
  list and 64 chains. When voting works, derived (Hoeffding and a union bound: P(vote wrong) ≤ (m − 1)e^{−kΔ²/2}); on
  300 lists of 2–9 digits: one chain 81%, a vote of 64 98% (the limit: the most frequent answer right, 98%), any of 64
  right 100%, a vote over answers given at once 74%.
* **3. Checking the steps.** A right answer from a broken argument (ours, made to think: 27% of right answers have a
  wrong step); outcome and process reward models; Cobbe et al. (2021: a verifier worth a 30× larger model), Uesato et
  al. (2022), Lightman et al. (2023: PRM800K; best of 1,860 on MATH: vote 69.6%, ORM 72.4%, PRM 78.2%). Ours, both
  graders trained on the same 8,000 solutions, 300 new questions: one sample 80%; the graders' picks get worse as N
  grows (best of 64: process grader 50%, outcome grader 44%; vote 96%); AUC 0.76 and 0.66; 71% of the process grader's
  picks from 64 had stopped thinking early, against 35% of all solutions (a product of step scores favours short
  chains). One solution graded both ways. DeepSeek-R1's "unsuccessful attempts" with process reward models;
  Math-Shepherd's automatic step labels.
* **4. Learning from a checker.** DeepSeekMath's GRPO (February 2024), o1 (September 2024), Tülu 3 names RLVR
  (November 2024), DeepSeek-R1 (January 2025); the reward 1[checker accepts]; the policy, a group of 8 answers,
  advantages against the group; on our two-digit addition model, 300 steps of 32 questions: 35% → 72–86% (three runs,
  mean 80%), replayed with six questions' answers at every checkpoint.
* **5. GRPO, derived.** The log-derivative trick and a baseline (Part 26); the group mean and spread; PPO's ratio and
  clip; the published per-token objective with its KL term; the KL estimators k1 = −log r, k2 = ½(log r)², k3 = r − 1
  − log r (Schulman 2020) on our model, where the true KL is exact (0.840 nats): k1 0.839 (10% negative, spread 0.91),
  k2 0.767 (biased low, spread 1.36), k3 0.744 (never negative, spread 6.25: unbiased, but heavy-tailed this far from
  the reference); Tang & Munos (2025) on estimating the KL's gradient; GRPO's training replayed on three uncertain
  questions (the right answer's probability 25% → 71% on average, not smoothly; entropy 0.92 → 0.17 bits a digit).
* **6. The successors.** Dr. GRPO's length and difficulty biases (Liu et al. 2025); DAPO (clip-higher 0.2/0.28,
  dynamic sampling, token-level averaging, overlong shaping; Yu et al. 2025); GSPO's sequence ratio (Zheng et al.
  2025); CISPO's clipped, stop-gradient weight (MiniMax 2025). Seven objectives on our model, three runs each, 300
  steps: GRPO as published, the only one with a KL penalty (k3, β = 0.04), collapsed in two of three runs (to 2% and
  5%; the third reached 88%); among the runs that learned (start 35%): plain 79%, Dr. GRPO 84%, DAPO 91%, GSPO 86%,
  CISPO 79%, a 12-point span against 19 points between runs of one method; the share of groups with no signal (the
  plain gradient's rises to 31% by the end); DAPO drew 2.9× the questions; offline DPO on pairs from the starting
  model (35% → 26%: on held-out pairs both the right and the wrong answers' log-probabilities fell, by 0.74 and 2.07
  bits; likelihood displacement).
* **7. Entropy collapse.** ∂H/∂z_b = −π_b(log π_b − E log π) and ΔH ≈ −Cov(log π, Δz), derived (Cui et al. 2025);
  entropy over training for four objectives (0.92 bits a digit at the start; at the end Dr. GRPO 0.14, DAPO 0.08,
  CISPO 0.16, the plain gradient 0.28: clip-higher did not hold the entropy up on three-digit answers); the fit R = −a
  e^H + b on every checkpoint (R² = 0.80 over the 16 runs that did not collapse; the ceiling at H = 0, 86%); remedies:
  clip-higher, entropy bonuses, Clip-Cov and KL-Cov, ProRL's long runs (more than 2,000 steps).
* **8. How long to think.** R1-Zero's growing chains and its "aha moment" (DeepSeek-AI 2025, Table 3); RL with a
  reward for the right sum only, replayed as a map of how many steps it chooses for each length of list (thinking 66%
  → ~100% of the time, mean 3.0 → 5.5 steps, accuracy 77% → 96%); overthinking (Chen et al. 2024; on two-digit lists,
  90% at once against 96% thinking, yet it thinks on 100% after RL); a cost per step of thought, three values, three
  runs each: c = 0 thinks on nearly everything (96% right), c = 0.005 thinks on 7% of two-digit lists and 90% of
  nine-digit ones (87%), c = 0.02 almost never thinks (77%; 39% on nine digits); Kimi k1.5's length reward, L1, DAPO's
  overlong penalty, products' thinking budgets.
* **9. Sharper, or wider?** pass@k; the plug-in estimate's bias and the unbiased estimator 1 − C(n − c, k)/C(n, k),
  derived (Chen et al. 2021), on our model against the exact values (the plug-in falls short by up to 2 points); Yue
  et al. (NeurIPS 2025 oral) and ProRL's counterpoint; exact pass@k up to 1,024 before and after four RL objectives
  (one try: 33% before, about 82% after; at 1,024 tries 100% before, against 98.2% for Dr. GRPO, 98.8% for DAPO, 97.8%
  for CISPO and 99.99% for the plain gradient; the untrained model ahead of Dr. GRPO from 16 tries on; on about 3 of
  the 200 questions RL drained the right answer below one in a thousand); a uniform guesser among the 179 possible
  sums passes at 1,024 tries 99.7% of the time.
* **10. Thinking at answer time.** Parallel against sequential; Snell et al. (2024: 4× more efficient than best-of-N,
  a small model plus test-time compute beating a 14× larger one); s1 (Muennighoff et al. 2025: 1,000 examples, budget
  forcing, AIME 2024 50% → 57%); ours on 9-digit lists: no thought 37%, thinking cut off part-way no better, the whole
  chain 63% with 12 tokens, a vote over answers at once at most 40% with up to 32 tokens; after RL, the whole chain
  84%. Best-of-N with a 0/1 checker, derived: KL(π_N ‖ π) = KL(Bern(1 − q) ‖ Bern(p)) → log(1/p), below Part 27's log
  N − (N − 1)/N, an upper bound in general (Beirami et al. 2024); ours: 1.18 nats at N = 256 against 4.55; best-of-8
  matches one try after RL.
* **11. Searching over thoughts.** AlphaZero (Part 26) mapped onto reasoning; Tree of Thoughts (Yao et al. 2023: Game
  of 24, 4% → 74%), rStar-Math (Guan et al. 2025: MATH 58.8% → 90.0% at 7B), AlphaProof, R1's unsuccessful MCTS; beam
  search over running totals guided by the process grader, one tree drawn; beam search against best-of-N at equal
  tokens on 9-digit lists: beam search ahead at every budget (78% against 64% at 2 samples per step), but both fall as
  they widen (beam 78% → 52%, best-of-N 64% → 31%).
* **12. Thinking without words.** The token bottleneck (about 17 bits per token, against tens of thousands in a hidden
  state); Coconut (Hao et al. 2024); HRM (Wang et al. 2025: 27M parameters, about 1,000 examples; Sudoku-Extreme 55%,
  Maze-Hard 74.5%, ARC-AGI-1 40.3%, ARC-AGI-2 5%) and ARC Prize's analysis (August 2025); TRM (Jolicoeur-Martineau
  2025: 7M parameters, 87.4%, 85.3%, 44.6%, 7.8%); chain-of-thought monitorability (Korbak et al. 2025).
* **13. Proofs a machine can check.** Lean and Mathlib; AlphaProof (Hubert et al., *Nature* 2025: about a million
  problems formalized into about 80 million statements; test-time RL) and IMO 2024 (28 of 42, one short of gold); IMO
  2025: Gemini Deep Think 35 (certified by the IMO's coordinators) and OpenAI's experimental model 35, in natural
  language; Harmonic's Aristotle and ByteDance's Seed-Prover formally (five of six); the spectrum of checkers.
* **14. Puzzles nobody has seen.** Chollet (2019); ARC-AGI-1 from about 20% (2020) to 53.5% (test-time training, 2024)
  and o3's 75.7% and 87.5% (December 2024); ARC-AGI-2 (March 2025; people 60% on average): NVARC 24%, Claude Opus 4.5
  37.6%, Poetiq on Gemini 3 Pro 54% (2025), Gemini 4 Argon 91% (verified October 2026); ARC-AGI-3 (March 2026):
  frontier models below 1% at launch, GPT-6 Astra 62.7% on ARC Prize's standard harness (September 2026).
* **Recap** in eight pictures from the part's own results, where it comes back (Parts 19, 29, 30, 31), six problems,
  Part 29's teaser (our model's steps are right 98.2% of the time, so a chain of n steps is all right with
  probability 0.982^n: a coin flip by about 39 steps).

Run from the repo root:

```
python tools/make.py ai28                 # everything: the numbers, then the English and Chinese builds (resumes)
python -m videos.ai.ai28.compute          # only the numbers: every experiment, on one thread (resumable)
python tools/build.py ai28                # English
python tools/build.py ai28 --lang zh      # Chinese
```

`compute.py` holds the parity and addition experiments, `objectives.py` the seven RL objectives, and `think.py` the
think-or-answer model (its supervised training, RL with and without a cost on thought, budgets, the outcome and
process graders, and beam search). Every random choice is seeded. Long items save each finished run under
`.cache/ai28/runs/` and each trained model under `.cache/ai28/` (retrained, seeded, if missing), so an interrupted
run resumes; nothing here depends on another part's results. On this machine, shared with other jobs, the whole
computation took about 3 hours on one thread; the parity experiments are about half of it.

References: J. Wei et al., *Chain-of-thought prompting elicits reasoning in large language models* (2022); T. Kojima
et al., *Large language models are zero-shot reasoners* (2022); M. Nye et al., *Show your work: scratchpads* (2021);
X. Wang et al., *Self-consistency* (2022); W. Merrill & A. Sabharwal, *The parallelism tradeoff* (2023) and *The
expressive power of transformers with chain of thought* (ICLR 2024); Z. Li, H. Liu, D. Zhou & T. Ma, *Chain of thought
empowers transformers to solve inherently serial problems* (ICLR 2024); G. Feng et al. (2023); M. Hahn (2020); J. Pfau,
W. Merrill & S. Bowman, *Let's think dot by dot* (2024); K. Cobbe et al., *Training verifiers to solve math word
problems* (2021); J. Uesato et al. (2022); H. Lightman et al., *Let's verify step by step* (2023); P. Wang et al.,
*Math-Shepherd* (2023); M. Chen et al., *Codex* (2021); Z. Shao et al., *DeepSeekMath* (2024); OpenAI, *Learning to
reason with LLMs* (2024); N. Lambert et al., *Tülu 3* (2024); DeepSeek-AI, *DeepSeek-R1* (2025; *Nature* 2025); Kimi
Team, *Kimi k1.5* (2025); J. Schulman, *Approximating KL divergence* (2020); Y. Tang & R. Munos, *On a few pitfalls in
KL divergence gradient estimation for RL* (2025); Z. Liu et al., *Understanding R1-Zero-like training* (Dr. GRPO,
2025); Q. Yu et al., *DAPO* (2025); C. Zheng et al., *GSPO* (2025); MiniMax, *MiniMax-M1* (CISPO, 2025); R. Rafailov
et al., *DPO* (2023); G. Cui et al., *The entropy mechanism of RL for reasoning language models* (2025); X. Chen et
al., *Do NOT think that much for 2+3=?* (2024); P. Aggarwal & S. Welleck, *L1* (2025); Y. Yue et al., *Does
reinforcement learning really incentivize reasoning capacity in LLMs beyond the base model?* (NeurIPS 2025); M. Liu
et al., *ProRL* (2025); C. Snell et al., *Scaling LLM test-time compute optimally* (2024); N. Muennighoff et al., *s1:
simple test-time scaling* (2025); A. Beirami et al., *Theoretical guarantees on the best-of-n alignment policy* (2024);
S. Yao et al., *Tree of thoughts* (2023); X. Guan et al., *rStar-Math* (2025); S. Hao et al., *Coconut* (2024); G.
Wang et al., *Hierarchical reasoning model* (2025); ARC Prize, *The hidden drivers of HRM's performance on ARC-AGI*
(2025); A. Jolicoeur-Martineau, *Less is more: recursive reasoning with tiny networks* (2025); T. Korbak et al.,
*Chain of thought monitorability* (2025); T. Hubert et al., *Olympiad-level formal mathematical reasoning with
reinforcement learning* (AlphaProof, *Nature* 2025); Google DeepMind, IMO 2024 and 2025 announcements; Harmonic,
*Aristotle* (2025); ByteDance Seed, *Seed-Prover* (2025); F. Chollet, *On the measure of intelligence* (2019); ARC
Prize Foundation: *ARC-AGI-2* (2025), *ARC Prize 2025 results* (2025), *ARC-AGI-3* technical report (April 2026), *GPT-6
Astra on ARC-AGI-3* (September 2026), results page for Gemini 4 Argon (October 2026); N. Lambert, *Reinforcement
Learning from Human Feedback* (2025).

## Problems, with solutions

**1. GRPO's baseline.** GRPO compares each answer's reward with the group's mean, which includes the answer's own
reward. Show that the leave-one-out mean b_i = (1/(G−1)) Σ_{j≠i} r_j gives an unbiased gradient estimate, and that the
plain group mean scales it by (G−1)/G.

*Solution.* The estimate is (r_i − b_i) ∇ log π(y_i). With the leave-one-out mean, b_i depends only on the other
answers, which are independent of y_i, so E[b_i ∇ log π(y_i)] = E[b_i] · E[∇ log π(y_i)] = 0 (the score has mean
zero: Σ_y π ∇ log π = ∇ Σ_y π = 0). What remains is E[r_i ∇ log π(y_i)] = ∇J. With the plain mean r̄,
r_i − r̄ = r_i − (r_i + (G−1) b_i)/G = ((G−1)/G)(r_i − b_i): the same estimate, times (G−1)/G. (GRPO also divides by
the group's spread, which Dr. GRPO removes.)

**2. The k3 estimator.** With y ~ π_θ and r = π_ref(y)/π_θ(y), show that k3 = (r − 1) − log r is never negative
and that E[k3] = KL(π_θ ‖ π_ref).

*Solution.* E[r] = Σ_y π_θ(y) π_ref(y)/π_θ(y) = Σ_y π_ref(y) = 1, so E[r − 1] = 0 and E[k3] = E[−log r] =
E[log π_θ(y)/π_ref(y)] = KL(π_θ ‖ π_ref). And f(r) = r − 1 − log r has f(1) = 0, f′(r) = 1 − 1/r, f″(r) = 1/r² > 0:
a convex function with its minimum at r = 1, so f ≥ 0. (This is log r ≤ r − 1.)

**3. The unbiased pass@k estimator.** If c of n independent samples are right, each with probability p, prove
E[C(n − c, k) / C(n, k)] = (1 − p)^k for k ≤ n.

*Solution.* Pick k of the n samples uniformly at random, independently of their values. Given the samples, the chance
all k picked are wrong is C(n − c, k)/C(n, k). Unconditionally, the k picked samples are k independent draws, so the
chance they are all wrong is (1 − p)^k. The second is the expectation of the first, by the law of total probability.

**4. When the vote is right.** The right answer has probability p\*, every wrong answer y has p_y ≤ p\* − Δ, and there
are m possible answers. Bound the chance that a majority vote over k samples is wrong.

*Solution.* The vote is wrong only if some wrong y appears at least as often as the right one. For a fixed y, N_{y\*} −
N_y = Σ_i X_i with X_i = 1[Y_i = y\*] − 1[Y_i = y] ∈ {−1, 0, 1}, independent, with mean at least Δ. Hoeffding's
inequality for variables with range 2 gives P(Σ X_i ≤ 0) ≤ exp(−2(kΔ)²/(4k)) = exp(−kΔ²/2). A union bound over the m −
1 wrong answers: P(vote wrong) ≤ (m − 1) e^{−kΔ²/2}, which goes to zero as k grows. If instead some wrong answer is
more likely than the right one, the same argument shows the vote is wrong with probability tending to one.

**5. Best-of-N with a checker.** Draw N answers from π and keep a right one if there is one (otherwise a wrong one).
With a 0/1 reward and q = (1 − p)^N, show KL(π_N ‖ π) = KL(Bern(1 − q) ‖ Bern(p)), and find its limit as N → ∞.

*Solution.* The result is right with probability 1 − q; given that, it is a draw from π conditioned on being right,
and given failure, from π conditioned on being wrong. So π_N(y) = π(y)(1 − q)/p for a right y and π(y) q/(1 − p) for a
wrong one. The log-ratio log π_N/π is constant on each set, so KL = (1 − q) log((1 − q)/p) + q log(q/(1 − p)), the KL
between two coins. As N → ∞, q → 0 and q log q → 0, so KL → log(1/p): bounded, unlike log N − (N − 1)/N, which is
the KL only for rewards without ties and an upper bound in general (Beirami et al. 2024).

**6. Why entropy falls.** For π = softmax(z), show ∂H/∂z_b = −π_b (log π_b − E_π[log π]), and that a small step Δz
changes the entropy by −Cov_{a∼π}(log π_a, Δz_a).

*Solution.* With ∂π_a/∂z_b = π_a(δ_ab − π_b): ∂H/∂z_b = −Σ_a (∂π_a/∂z_b)(log π_a + 1) = −π_b(log π_b + 1) +
π_b Σ_a π_a (log π_a + 1) = −π_b (log π_b − E_π[log π]). To first order, ΔH = Σ_b (∂H/∂z_b) Δz_b = −E_π[(log π −
E_π log π) Δz] = −Cov_π(log π, Δz). A policy-gradient step raises z_a by η π_a A_a, so when likely answers have
positive advantages the covariance is positive and the entropy falls (Cui et al. 2025).

## 习题与解答

**1. GRPO的基线。** GRPO把每个回答的奖励和全组的平均比较，而这个平均里包含了它自己的奖励。证明：用"留一"平均
b_i = (1/(G−1)) Σ_{j≠i} r_j 作基线，梯度估计是无偏的；而用全组平均，梯度会被乘上 (G−1)/G。

*解答。* 估计量是 (r_i − b_i) ∇log π(y_i)。用留一平均时，b_i 只依赖其他回答，与 y_i 独立，所以
E[b_i ∇log π(y_i)] = E[b_i]·E[∇log π(y_i)] = 0（得分函数的均值为零：Σ_y π ∇log π = ∇ Σ_y π = 0）。剩下的是
E[r_i ∇log π(y_i)] = ∇J。用全组平均 r̄ 时，r_i − r̄ = r_i − (r_i + (G−1) b_i)/G = ((G−1)/G)(r_i − b_i)：同一个估计量，
乘以 (G−1)/G。（GRPO还要除以组内的标准差，Dr. GRPO把它去掉了。）

**2. k3估计量。** 设 y ~ π_θ，r = π_ref(y)/π_θ(y)。证明 k3 = (r − 1) − log r 永不为负，并且 E[k3] = KL(π_θ ‖ π_ref)。

*解答。* E[r] = Σ_y π_θ(y) π_ref(y)/π_θ(y) = Σ_y π_ref(y) = 1，所以 E[r − 1] = 0，E[k3] = E[−log r] =
E[log π_θ(y)/π_ref(y)] = KL(π_θ ‖ π_ref)。又 f(r) = r − 1 − log r 满足 f(1) = 0，f′(r) = 1 − 1/r，f″(r) = 1/r² > 0：
一个在 r = 1 处取最小值的凸函数，所以 f ≥ 0。（这就是 log r ≤ r − 1。）

**3. pass@k的无偏估计。** n个独立样本中有c个正确，每个正确的概率为p。证明对 k ≤ n，
E[C(n − c, k) / C(n, k)] = (1 − p)^k。

*解答。* 从n个样本里随机选k个，选法与样本的取值无关。给定样本，选出的k个全错的概率是 C(n − c, k)/C(n, k)。不加条件时，
选出的k个样本就是k次独立抽取，全错的概率是 (1 − p)^k。由全概率公式，后者正是前者的期望。

**4. 投票什么时候对。** 正确答案的概率是p\*，每个错误答案y的概率 p_y ≤ p\* − Δ，一共有m种可能的答案。给对k个样本做多数
投票出错的概率一个上界。

*解答。* 只有当某个错误答案y出现的次数不少于正确答案时，投票才会错。固定y，N_{y\*} − N_y = Σ_i X_i，其中
X_i = 1[Y_i = y\*] − 1[Y_i = y] ∈ {−1, 0, 1}，相互独立，均值至少为Δ。对取值范围为2的变量用霍夫丁不等式：
P(Σ X_i ≤ 0) ≤ exp(−2(kΔ)²/(4k)) = exp(−kΔ²/2)。对m − 1个错误答案取并集上界：P(投票出错) ≤ (m − 1) e^{−kΔ²/2}，
随k增大趋于零。反过来，如果某个错误答案比正确答案更可能，同样的论证说明投票出错的概率趋于1。

**5. 有检查器时的最优N选1。** 从π中抽N个回答，有正确的就留一个正确的（否则留一个错的）。奖励是0或1，记 q = (1 − p)^N。
证明 KL(π_N ‖ π) = KL(Bern(1 − q) ‖ Bern(p))，并求 N → ∞ 时的极限。

*解答。* 结果正确的概率是 1 − q；在正确的条件下，它是π限制在正确答案上的一次抽取；失败时，是π限制在错误答案上的一次抽取。
所以正确的y有 π_N(y) = π(y)(1 − q)/p，错误的y有 π_N(y) = π(y) q/(1 − p)。对数比 log π_N/π 在每个集合上是常数，
所以 KL = (1 − q) log((1 − q)/p) + q log(q/(1 − p))，正是两枚硬币之间的KL。N → ∞ 时 q → 0，q log q → 0，
所以 KL → log(1/p)：有界，不像 log N − (N − 1)/N 那样无限增长；后者只在奖励没有并列时才等于KL，一般情况下是上界
（Beirami等，2024）。

**6. 熵为什么会下降。** 对 π = softmax(z)，证明 ∂H/∂z_b = −π_b (log π_b − E_π[log π])，并且一个小步长 Δz 使熵改变
−Cov_{a∼π}(log π_a, Δz_a)。

*解答。* 由 ∂π_a/∂z_b = π_a(δ_ab − π_b)：∂H/∂z_b = −Σ_a (∂π_a/∂z_b)(log π_a + 1) = −π_b(log π_b + 1) +
π_b Σ_a π_a (log π_a + 1) = −π_b (log π_b − E_π[log π])。一阶近似下，ΔH = Σ_b (∂H/∂z_b) Δz_b =
−E_π[(log π − E_π log π) Δz] = −Cov_π(log π, Δz)。策略梯度的一步把 z_a 提高 η π_a A_a，所以当高概率的回答优势为正时，
协方差为正，熵就下降（Cui等，2025）。

## Glossary (new terms in Part 28)

| English | 中文 |
|---|---|
| reasoning, reasoning model | 推理，推理模型 |
| chain of thought, scratchpad | 思维链，草稿（中间步骤） |
| "let's think step by step" | "让我们一步一步地思考" |
| thinking out loud, tokens of thought | 出声思考，思考词元 |
| filler tokens | 填充词元 |
| threshold circuit, TC⁰, NC¹ | 阈值电路，TC⁰，NC¹ |
| self-consistency, majority vote | 自洽性，多数投票 |
| verifier, checker | 验证器，检查器 |
| outcome reward model (ORM) | 结果奖励模型（ORM） |
| process reward model (PRM) | 过程奖励模型（PRM） |
| step label, right for the wrong reason | 步骤标签，歪打正着 |
| AUC (how well a grader tells right from wrong) | AUC（评分器区分对错的能力） |
| reinforcement learning with verifiable rewards (RLVR) | 可验证奖励的强化学习（RLVR） |
| group relative policy optimization (GRPO) | 组相对策略优化（GRPO） |
| group, group baseline, leave-one-out | 组，组基线，留一 |
| importance ratio, clip, clip-higher | 重要性比值，裁剪，放宽上界的裁剪（clip-higher） |
| KL estimator (k1, k2, k3), control variate | KL估计量（k1、k2、k3），控制变量 |
| length bias, difficulty bias | 长度偏差，难度偏差 |
| dynamic sampling, groups with no signal | 动态采样，没有信号的组 |
| sequence-level ratio, geometric mean | 序列级比值，几何平均 |
| entropy collapse, entropy bonus | 熵坍缩，熵奖励 |
| overthinking, underthinking, length penalty | 过度思考，思考不足，长度惩罚 |
| aha moment | 顿悟时刻（aha moment） |
| pass@k, unbiased estimator, plug-in estimator | pass@k，无偏估计量，代入估计量 |
| sharpen, widen (the reasoning boundary) | 锐化，拓宽（推理边界） |
| test-time compute, parallel, sequential | 测试时计算，并行，串行 |
| budget forcing | 预算强制 |
| best-of-N | 最优N选1 |
| beam search, tree search, Tree of Thoughts | 束搜索，树搜索，思维树 |
| latent reasoning, continuous thought | 隐式推理，连续思维 |
| recursion, deep supervision, refinement loop | 递归，深度监督，精炼循环 |
| proof assistant, kernel, formalization | 证明助手，内核，形式化 |
| harness (for ARC-AGI-3) | 测试框架（harness） |
| chain-of-thought monitorability | 思维链的可监控性 |

Names stay in Latin script: GRPO, Dr. GRPO, DAPO, GSPO, CISPO, DPO, o1, o3, R1, R1-Zero, s1, L1, Kimi k1.5, ProRL,
rStar-Math, Coconut, HRM, TRM, AlphaProof, AlphaGeometry, Lean, Mathlib, Aristotle, Seed-Prover, ARC-AGI, NVARC, Poetiq.
