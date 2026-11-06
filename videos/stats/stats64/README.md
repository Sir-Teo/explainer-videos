# Statistics, Built — Part 64: Statistics in the Age of AI

Part 64 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the ninth part of Stage V, the research frontier.

It opens with a leaderboard: a new model scores 85.2% on a 1,000-question benchmark against 84.7% for the previous
best.
- **The numbers.** Each score has a standard error of about 1.1 points. The paired 95% interval for the difference is
  (−1.9, 2.9) points, and McNemar's test on the 76 and 71 discordant questions gives p = 0.74.
- **Re-written benchmarks.** If the true accuracies really are 85.2% and 84.7%, a fresh thousand questions puts the
  previous best ahead 33% of the time.

Every model and benchmark in the part is simulated, so every number is about a method, not about a real system.

The part asks what honest uncertainty looks like when machines make the predictions, generate the data and grade each
other:
- benchmarks as samples from a population of questions (Miller 2024):
  - the CLT error bar, and cluster-robust standard errors on a passage-structured benchmark, on the Board;
  - the design effect, and resampling clusters;
- paired comparisons:
  - the paired variance and McNemar's (1947) test, on the Board;
  - power against benchmark size, and the leaderboard's winner's curse against the number of models;
  - multiplicity, rank sets and fresh confirmation;
- arenas (Chiang et al. 2024):
  - Bradley–Terry (Zermelo 1929; Bradley & Terry 1952) as logistic regression, shown on the new leaderboard;
  - model, sandwich and bootstrap intervals, and Elo's order dependence;
  - style control as confounder adjustment, and the arena's sampling cautions;
- item response theory:
  - Birnbaum's two-parameter model fitted to simulated model responses;
  - estimating a new model from 100 items, random or spread anchors, item information and adaptive testing;
  - tinyBenchmarks (Maia Polo et al. 2024), and multidimensional abilities;
- adaptive reuse of test sets:
  - Dwork et al.'s (2015) noise-feature experiment, with a reused holdout against Thresholdout;
  - the Ladder (Blum & Hardt 2015), and contamination as membership inference;
- labels from models:
  - LLM judges as measurement instruments, and their bias;
  - prediction-powered inference (Angelopoulos et al. 2023) with a few human labels;
  - design-based supervised learning (Egami et al. 2023), and inter-rater agreement;
- synthetic data and model collapse (Shumailov et al. 2024):
  - a Gaussian refitted to its own samples, with E[σ̂²ₜ] = ((n − 1)/n)ᵗ derived;
  - the log variance as a random walk with negative drift, and almost-sure collapse;
  - accumulation instead of replacement (Gerstgrasser et al. 2024);
- uncertainty for language models:
  - calibration (Kadavath et al. 2022), and its loss after preference training (OpenAI 2023);
  - conformal factuality (Mohri & Hashimoto 2024) simulated, and conformal language modeling (Quach et al. 2024);
- watermarks (Kirchenbauer et al. 2023):
  - the green-list z test with its exact binomial power and false-positive rate;
  - entropy, edits and paraphrases, distortion-free schemes, and SynthID-Text (Dathathri et al. 2024);
- simulation-based inference:
  - neural posterior estimation (Cranmer, Brehmer & Louppe 2020), and the trust crisis (Hermans et al. 2022);
  - an amortized posterior's coverage with in-sample against held-out calibration, and SBC;
- generative models as density estimators:
  - Tweedie's formula as the Bayes denoiser, and the probability-flow sampler;
  - the exact empirical score's memorization against a smoothed score, and minimax rates (Oko, Akiyama & Suzuki 2023);
- causal questions about deployments:
  - a two-sided market where the A/B test overstates the global effect, and market-level randomization;
  - switchbacks and two-sided designs (Johari et al. 2022), the surrogate index's risk, and observational rollouts;
- five open problems.

It keeps two promises:
- **Part 11** built intervals from independent observations, each used once. Chapters 1, 2 and 5 handle questions
  that cluster, models that share questions, and test sets used again and again.
- **Part 34** treated a model's predictions as given data. Chapters 6 and 7 ask what happens when the labels, and
  then the training data, come from models.

**Built in this part:**
- **`statkit.evals`** ([`explainer/stats/kit/evals.py`](../../../explainer/stats/kit/evals.py)), tested in
  `tests/test_stats_kit_evals.py`:
  - iid and cluster-robust (CR1) standard errors, a clustered benchmark simulator, and the design effect;
  - paired comparisons, McNemar's exact test, correlated model pairs, the winner's curse, and E[max of k normals];
  - Bradley–Terry by Newton with model and sandwich SEs, the bootstrap, style control, and online Elo;
  - a joint-ML two-parameter IRT fit, ability estimation and predicted accuracy;
  - Thresholdout and the adaptive-overfitting experiment;
  - judged labels, prediction-powered and Wald intervals;
  - Gaussian model collapse, with replacement or accumulation;
  - conformal factuality with a claim simulator;
  - green-list watermark probability, z statistic and exact power;
  - amortized posterior coverage;
  - mixture scores, Tweedie's formula and the probability-flow sampler;
  - a two-sided market with buyer-level and market-level randomization.
- **The leaderboard** (`Leaderboard` in `explainer/stats/viz.py`), the part's instrument. It draws models as rows
  sorted by score, each with its interval, and brackets the honest rank-one set: every model whose interval reaches
  the leader's.

**Data.** All seeded simulation or exact arithmetic. The published figures quoted (tinyBenchmarks' error, Chatbot
Arena's style control, SynthID-Text's live test) are from the papers.

The Coverage Board gains four rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| iid error bar on a benchmark | 100 passages × 10 questions | 95% | 76.1% | broken |
| cluster-robust error bar | 100 passages × 10 questions | 95% | 95.0% | kept |
| unpaired interval for a model difference | two models, same 1,000 questions | 95% | 99.1% | conservative |
| paired interval for a model difference | two models, same 1,000 questions | 95% | 95.05% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats64.compute   # once (about a minute)
python tools/build.py stats64 -q l                         # fast 480p preview
python tools/build.py stats64                              # 1080p30 -> renders/stats64.mp4
python tools/qa_scene.py stats64 Arena
python tools/lecture_length.py stats64 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The leaderboard | 85.2% vs 84.7%, n = 1,000: SEs 1.12, 1.14 points; paired CI (−1.9, 2.9); McNemar 76 vs 71, p = 0.74; order flips 33.4% of 4,000 re-writings |
| 1 | Benchmarks | 100 passages × 10, 2,000 benchmarks: iid SE 1.37 points, coverage 76.1%; CR1 SE 2.27, coverage 95.0%; true sd 2.24; design effect 2.74, ICC 0.19 |
| 2 | Paired | corr 0.38: unpaired SE 1.60, coverage 99.1%; paired SE 1.25, 95.05%; power for 86% vs 84% at n = 1,000: 17% unpaired, 33% paired; winner's curse +2.1 points at k = 20, +2.8 at 100 |
| 3 | Arenas | 8 models, 6,000 battles: SEs ≈ 0.07 by Fisher, sandwich and bootstrap; sandwich coverage 94.7%; Elo over 50 orders wanders ±0.13; style: model D 0.81 raw, 0.27 controlled (true 0.35), γ̂ = 0.57 (true 0.6) |
| 4 | IRT | 60 models × 1,000 items: corr(θ̂, θ) 0.998, (b̂, b) 0.94, (â, a) 0.69; 100-item RMSE: mean 4.4, IRT 3.4, spread anchors 2.9 points |
| 5 | Holdout | 3,000 noise features, n = 3,000: reused holdout up to 63.6% (fresh 49.9%); Thresholdout 52–56% |
| 6 | Judges | truth 0.70, judge sens 0.95, spec 0.80 (bias +2.5 points): judge-only coverage 2.6%; humans (n = 200) 94.3%, width 12.7; PPI 94.8%, width 8.8 |
| 7 | Collapse | n = 20: drift −0.105 per generation; median σ̂² after 300 generations 10⁻¹³·⁴; all 400 lineages below 1%; accumulating: median 0.78 |
| 8 | Uncertainty | 8 claims, each true w.p. 0.8: unfiltered all-true 16%; at α = 0.1, 89.9% all true, 56% of claims kept |
| 9 | Watermarks | γ = 0.25, δ = 2: green 0.71; power at z > 4: 99.6% at 40 tokens; 40% uncertain tokens: 90% at 160; half rewritten: 34% at 40; exact FPR at 10 tokens 0.0004 |
| 10 | SBI | 90% intervals: in-sample 70.7% at N = 30, 89.95% at 4,000; held-out 95.2% at 30 |
| 11 | Diffusion | 20 training points: median distance to one, empirical score 0.006, smoothed 0.058, true sampler 0.061 |
| 12 | Deployments | 4,000 buyers, 1,800 items: A/B 0.225, global 0.050, 20 randomized markets 0.050 |
| 13 | Open problems | — |
| 14 | Outro | — |

## Sources

- **Benchmarks and pairs.** E. Miller, "Adding Error Bars to Evals", arXiv:2411.00640 (2024); Q. McNemar,
  *Psychometrika* 12 (1947); L. Kish, *Survey Sampling* (1965).
- **Arenas.**
  - E. Zermelo, *Math. Z.* 29 (1929); R. Bradley & M. Terry, *Biometrika* 39 (1952); D. Hunter, *Ann. Statist.* 32
    (2004);
  - W.-L. Chiang et al., "Chatbot Arena", ICML (2024); LMSYS, "Does style matter? Disentangling style and substance
    in Chatbot Arena" (28 August 2024).
- **IRT.** A. Birnbaum, in Lord & Novick, *Statistical Theories of Mental Test Scores* (1968); F. Lord (1980);
  F. Maia Polo et al., "tinyBenchmarks", ICML (2024).
- **Holdouts.** C. Dwork, V. Feldman, M. Hardt, T. Pitassi, O. Reingold & A. Roth, *Science* 349 (2015); A. Blum &
  M. Hardt, ICML (2015).
- **Labels from models.** A. Angelopoulos, S. Bates, C. Fannjiang, M. Jordan & T. Zrnic, *Science* 382 (2023);
  N. Egami, M. Hinck, B. Stewart & H. Wei, NeurIPS (2023); J. Cohen, *Educ. Psychol. Meas.* 20 (1960).
- **Collapse.** I. Shumailov et al., *Nature* 631 (2024); M. Gerstgrasser et al., "Is model collapse inevitable?"
  (2024).
- **Uncertainty.**
  - S. Kadavath et al., "Language models (mostly) know what they know" (2022); OpenAI, "GPT-4 technical report"
    (2023);
  - C. Mohri & T. Hashimoto, ICML (2024); V. Quach et al., ICLR (2024).
- **Watermarks.** J. Kirchenbauer et al., ICML (2023); R. Kuditipudi et al. (2023); S. Dathathri et al., *Nature* 634
  (2024).
- **Simulators.** K. Cranmer, J. Brehmer & G. Louppe, *PNAS* 117 (2020); J. Hermans et al., TMLR (2022); S. Talts et
  al. (2018).
- **Diffusion.**
  - J. Sohl-Dickstein et al., ICML (2015); Y. Song & S. Ermon, NeurIPS (2019); J. Ho, A. Jain & P. Abbeel, NeurIPS
    (2020); Y. Song et al., ICLR (2021);
  - H. Robbins (1956); K. Oko, S. Akiyama & T. Suzuki, ICML (2023).
- **Deployments.** R. Johari, H. Li, I. Liskovich & G. Weintraub, *Management Science* (2022); S. Athey, R. Chetty,
  G. Imbens & H. Kang (2019).
- **Open problems.** L. Cronbach & P. Meehl, *Psychol. Bull.* 52 (1955).

## Problems and solutions

1. **CR1 with singleton clusters.**
   - With G = n clusters of one, the cluster sums are the residuals rᵢ.
   - So SE² = n/(n − 1) · Σrᵢ²/n² = Σrᵢ²/(n(n − 1)) = s²/n.
2. **The paired variance and McNemar.**
   - ā − b̄ is the mean of dᵢ = aᵢ − bᵢ, so its variance is Var(d)/n = (σ_a² + σ_b² − 2σ_ab)/n.
   - dᵢ is 1, −1 or 0, so Σdᵢ = n₁₀ − n₀₁. Conditioning on the n₁₀ + n₀₁ discordant questions, each is equally
     likely to be +1 or −1 under the null, so the test uses only n₁₀ and n₀₁.
3. **Bradley–Terry.**
   - The log-likelihood is Σ[yₖ xₖ·θ − log(1 + e^{xₖ·θ})] with xₖ = e_i − e_j. Its Hessian is −Σ pₖ(1 − pₖ)xₖxₖᵀ,
     which is negative semidefinite, so it is concave.
   - Each xₖ sums to zero, so adding c to every θ leaves every xₖ·θ unchanged: only differences are identified.
4. **The Gaussian's collapse.**
   - σ̂²ₜ = Π_{s ≤ t} χ²_{n−1,s}/n with independent factors, so E σ̂²ₜ = ((n − 1)/n)ᵗ.
   - log σ̂²ₜ / t → E log(χ²_{n−1}/n) by the strong law. By Jensen, that is below log((n − 1)/n) < 0, so
     log σ̂²ₜ → −∞ and σ̂²ₜ → 0 almost surely.
5. **Prediction-powered inference.**
   - E f̄_N = E f and E(y − f)‾ₙ = E y − E f, so the sum has expectation E y whatever f is.
   - The two averages are over independent samples, so the variance is Var(f)/N + Var(y − f)/n.
6. **Tweedie.**
   - p_σ(y) = ∫ φ_σ(y − x)p(x)dx. Differentiating under the integral, ∇p_σ(y) = ∫ (x − y)/σ² · φ_σ(y − x)p(x)dx.
   - Dividing by p_σ(y) gives ∇log p_σ(y) = (E[x | y] − y)/σ². Rearranging gives the formula.

## Glossary

- **Benchmarks.** Superpopulation of questions; iid and cluster-robust standard errors; design effect; intraclass
  correlation; paired difference; McNemar's test; power; winner's curse; rank set.
- **Arenas and tests.** Bradley–Terry; Elo; sandwich SE; style control; item response theory; discrimination and
  difficulty; item information; anchor items; adaptive testing.
- **Reuse.** Adaptive data analysis; reusable holdout; Thresholdout; the Ladder; contamination.
- **Machine-made data.** LLM judge; sensitivity and specificity; prediction-powered inference; rectifier;
  design-based supervised learning; model collapse; accumulation.
- **Uncertainty.** Calibration; conformal factuality; conformal language modeling; green list; watermark z test;
  distortion-free watermark; neural posterior estimation; simulation-based calibration.
- **Generation and deployment.** Score; Tweedie's formula; probability-flow ODE; memorization; interference;
  switchback; two-sided randomization; surrogate index.

## Where it comes back

- **Part 65**: a preregistered simulation study reported whatever it shows; the full Coverage Board; an open problem
  from these last parts, attacked as a dissertation.
