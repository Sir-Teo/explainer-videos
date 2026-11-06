# Statistics, Built — Part 56: Inference After Selection

Part 56 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the first part of Stage V, the research frontier.

It opens with Ioannidis (2008), *Why most discovered true associations are inflated*, and the World's gene study: the
twenty genes with the largest test statistics have estimated effects 49% larger than their true effects, and a
replication finds the truth, although all twenty are real. The part asks how to give honest uncertainty about a
question chosen by looking at the data, and gives five answers at five prices:
- the problem: the winner's curse by K, conditional against unconditional guarantees, the false coverage rate, the
  Bayesian view and Tweedie's correction;
- PoSI (Berk, Brown, Buja, Zhang & Zhao 2013): the submodel target, the simultaneous constant by simulation against
  Bonferroni and Scheffé, its √(2 log p) to √p range;
- conditional selective inference: the polyhedral lemma (Lee, Sun, Sun & Taylor 2016), proved; the truncated-normal
  pivot and its inversion, shown in the selection window; marginal screening; the lasso's selection event; selective
  intervals on Stamey's prostate data; the costs (Kivaranovic & Leeb 2021; Fithian, Sun & Taylor 2014) and asymptotic
  validity (Tibshirani, Rinaldo, Tibshirani & Wasserman 2018);
- randomization and carving (Tian & Taylor 2018): the selective likelihood, interval lengths by the amount of noise, the
  randomized lasso;
- data fission (Leiner, Duan, Wasserman & Ramdas 2025) and thinning (Neufeld, Dharamshi, Gao & Witten 2024): the
  independence, the τ trade-off, fission for regression, count splitting;
- knockoff theory: fixed-X (Barber & Candès 2015) and model-X (Candès, Fan, Janson & Lv 2018), the sign-flip property,
  the supermartingale proof of FDR control, robustness (Barber, Candès & Samworth 2020), derandomization;
- conformal selection (Jin & Candès 2023) on the Wisconsin breast cancer biopsies;
- inference on winners (Andrews, Kitagawa & McCloskey 2024): conditional, median-unbiased and hybrid, on the prostate
  microarray's top gene;
- post-clustering inference (Gao, Bien & Witten 2024) on Old Faithful and Newcomb's passage times;
- open problems, and a referee's checklist.

It keeps two promises:
- **Part 33** controlled the FDR over thousands of questions and read the discoveries' estimates at face value.
  Chapters 1–8 give honest intervals for what was selected.
- **Part 52**'s lasso selected variables while its intervals assumed a fixed question. Chapter 3 gives inference on the
  lasso's own model.

**Built in this part:**
- **`statkit.selective`** ([`explainer/stats/kit/selective.py`](../../../explainer/stats/kit/selective.py)), tested in
  `tests/test_stats_kit_selective.py`:
  - truncated-normal pivots (stable in the tails) and their inversion, with an expanding search for unbounded intervals;
  - the polyhedral lemma's truncation limits; the lasso at a fixed λ, its selection polyhedron and selective intervals;
  - inference on winners: conditional intervals, the median-unbiased estimate, the hybrid and projection intervals;
  - the PoSI constant by simulation over all submodels, with Bonferroni and Scheffé;
  - selective intervals after a randomized threshold rule;
  - data fission for normals and Poisson thinning;
  - conformal selection with BH;
  - exact two-means clustering in one dimension and the selective test of its clusters' means.
- **The selection window** (`SelectionWindow` in `explainer/stats/viz.py`), the part's instrument: a statistic's law,
  its selection region, the law truncated to that region and rescaled, the observed value, and the shaded tail whose area
  is the selective pivot; `at(mu)` redraws it for any mean, so the pivot's inversion can be watched.

**Data.**
- From the Museum: Stamey's prostate data, Singh's prostate microarray, the Wisconsin breast cancer data, Old Faithful,
  and Newcomb's passage times.
- From the World: the gene-expression study, with a fresh replication.
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| Wald interval for the winner | the largest of 10 means | 95% | 78.9% | broken |
| conditional interval (truncated normal) | the largest of 10 means | 95% | 94.8% | kept |
| hybrid interval (Andrews et al.) | the largest of 10 means | 95% | 95.3% | kept |
| OLS intervals after the lasso | Stamey's design, fixed λ | 95% | 86.3% | broken |
| selective intervals (polyhedral lemma) | Stamey's design, fixed λ | 95% | 95.5% | kept |
| data fission, τ = 1 | the largest of 20 means | 95% | 95.0% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats56.compute   # once (about ten minutes)
python tools/build.py stats56 -q l                         # fast 480p preview
python tools/build.py stats56                              # 1080p30 -> renders/stats56.mp4
python tools/qa_scene.py stats56 Winners
python tools/lecture_length.py stats56 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Inflated discoveries | top 20 of 5,000 genes: estimated 1.84 SD, true 1.23, replication 1.22; selected-window pivot 0.42 at μ = 0 for y = 2.3 |
| 1 | The problem | K nulls, report the max: bias 1.55 (K = 10), 3.25 (1,000); naive coverage 77% (10), 8% (100), 0% (1,000) |
| 2 | PoSI | p = 10, n = 60: K = 2.78 (orthogonal), 3.44 (ρ = 0.5), Bonferroni 4.42 over 5,120 contrasts, Scheffé 4.28 |
| 3 | Conditional inference | Stamey, λ = 20: lcavol 0.617 (0.45, 0.79), lweight 0.282 (0.08, 0.43) vs naive (0.14, 0.43), svi 0.274 (0.05, 0.44) vs (0.11, 0.44); simulation: naive 86.3%, selective 95.5%, median length 2.1× |
| 4 | Randomization | μ = 1, c = 2: median length 10.8 (hard), 8.6 (γ = 0.25), 6.4 (0.5), 5.0 (1), 4.2 (2), all ≈ 95% |
| 5 | Fission | 20 means: naive coverage 73.2% (picks the best 49%), splitting 94.6% (32%), fission 95.0% (33%); τ = ¼ … 4: picks 48% … 11%, length 16.2 … 4.0 |
| 6 | Knockoffs | n = 300, p = 100, 15 real, q = 0.1: FDR 0.065, power 81%, E M(T) = 1.00 |
| 7 | Conformal selection | breast cancer, 50 splits: 70 of 169 test tumours selected, FDR 9.3%, power 97.4% |
| 8 | Winners | K = 10 by the lead: conditional median length 10.6 → 4.1, hybrid 5.2 → 4.2, projection 6.96; prostate top gene z = 5.25 (runner-up 4.80): naive (3.29, 7.21), conditional (−3.13, 7.02), hybrid (0.36, 7.07) |
| 9 | Clustering | Old Faithful: split at 3.19 min, selective p ≈ 6 × 10⁻¹⁰; Newcomb: split at 28.5, naive p ≈ 5 × 10⁻¹⁰, selective 0.84; null: 5.5% below 0.05 (naive 100%) |
| 10 | Open problems | — |
| 11 | Outro | — |

## Sources

- **The problem.** J. Ioannidis, *Epidemiology* 19 (2008); D. Cox, *Biometrika* 62 (1975); H. Leeb & B. Pötscher,
  *Ann. Stat.* 34 (2006); Y. Benjamini & D. Yekutieli, *JASA* 100 (2005); A. P. Dawid, in *Multivariate Analysis and
  its Applications* (1994); B. Efron, *JASA* 106 (2011).
- **PoSI.** R. Berk, L. Brown, A. Buja, K. Zhang & L. Zhao, *Ann. Stat.* 41 (2013).
- **Conditional inference.** J. Lee, D. Sun, Y. Sun & J. Taylor, *Ann. Stat.* 44 (2016); W. Fithian, D. Sun &
  J. Taylor, arXiv:1410.2597 (2014); D. Kivaranovic & H. Leeb, *JASA* 116 (2021); R. Tibshirani, A. Rinaldo,
  R. Tibshirani & L. Wasserman, *Ann. Stat.* 46 (2018).
- **Randomization.** X. Tian & J. Taylor, *Ann. Stat.* 46 (2018); S. Panigrahi & J. Taylor, *JASA* 118 (2023).
- **Fission and thinning.** J. Leiner, B. Duan, L. Wasserman & A. Ramdas, *JASA* 120 (2025); A. Neufeld,
  A. Dharamshi, L. Gao & D. Witten, *JMLR* 25 (2024); A. Neufeld, L. Gao, J. Popp, A. Battle & D. Witten,
  *Biostatistics* (2022).
- **Knockoffs.** R. Foygel Barber & E. Candès, *Ann. Stat.* 43 (2015); E. Candès, Y. Fan, L. Janson & J. Lv, *JRSS B*
  80 (2018); R. Foygel Barber, E. Candès & R. Samworth, *Ann. Stat.* 48 (2020); Z. Ren & R. Foygel Barber, *JRSS B* 86
  (2024).
- **Conformal selection.** Y. Jin & E. Candès, *JMLR* 24 (2023); S. Bates, E. Candès, L. Lei, Y. Romano & M. Sesia,
  *Ann. Stat.* 51 (2023); Y. Benjamini & D. Yekutieli, *Ann. Stat.* 29 (2001).
- **Winners.** I. Andrews, T. Kitagawa & A. McCloskey, *QJE* 139 (2024).
- **Clustering.** L. Gao, J. Bien & D. Witten, *JASA* 119 (2024); Y. Chen & D. Witten, *JMLR* 24 (2023); S. Jewell,
  P. Fearnhead & D. Witten, *JRSS B* 84 (2022).
- **Data.** T. Stamey et al., *J. Urology* 141 (1989); D. Singh et al., *Cancer Cell* 1 (2002); B. Efron,
  *Large-Scale Inference* (2010); W. Wolberg, W. Street & O. Mangasarian (1995); S. Newcomb (1891).

## Problems and solutions

1. **The decomposition's independence.** (η′Y, Z) is jointly Gaussian, and Cov(Z, η′Y) = Ση − c η′Ση = Ση − Ση = 0,
   so Z and η′Y are independent.
2. **Marginal screening.** {|Y_j| > t} = {Y_j > t} ∪ {−Y_j > t}, each a single linear inequality. Conditioning also on
   the other coordinates (which are independent of Y_j under Σ = I), Y_j given selection is N(μ_j, 1) truncated to
   (−∞, −t) ∪ (t, ∞); with the sign also conditioned on, one of the two pieces.
3. **Monotonicity.** The truncated family {N(μ, 1) restricted to [a, b]} is an exponential family in y with natural
   parameter μ, so it has a monotone likelihood ratio, and P_μ(Y > y | Y ∈ [a, b]) is increasing in μ.
4. **The winner's curse rate.** By Jensen, e^{λE max} ≤ E e^{λ max} ≤ K e^{λ²/2}, so E max ≤ log K/λ + λ/2; with
   λ = √(2 log K), E max ≤ √(2 log K).
5. **Fission.** Cov(f, g) = σ² − τ(1/τ)σ² = 0 and joint Gaussianity give independence. Var f = (1 + τ²)σ² ≤ v forces
   τ² ≤ v/σ² − 1, and Var g = (1 + 1/τ²)σ² is decreasing in τ, so take τ² = v/σ² − 1.
6. **Conformal p-values.** For a null test unit, its score and the scores of the n calibration units are exchangeable,
   so its rank among them is uniform on {1, …, n + 1} (ties broken at random); counting only calibration nulls with
   larger scores makes p_j stochastically larger, so P(p_j ≤ t) ≤ t.

## Glossary

- **The problem.** Selection rule; selected target; winner's curse; marginal, conditional and simultaneous coverage;
  false coverage rate; data snooping; garden of forking paths.
- **Simultaneous.** Submodel target β_{j·M}; PoSI constant; Scheffé; Bonferroni; projection interval.
- **Conditional.** Selection event; polyhedron; polyhedral lemma; truncated normal; pivot; selective interval;
  median-unbiased; conditioning on less; KKT conditions.
- **Randomized and split.** Randomized response; selective likelihood; carving; sample splitting; data fission; data
  thinning; count splitting.
- **Error rates over sets.** Knockoff (fixed-X, model-X); sign-flip; knockoff+; supermartingale; conformal p-value;
  PRDS; conformal selection.
- **Winners and clusters.** Hybrid interval; double dipping; post-clustering test.

## Where it comes back

- **Part 57**: distribution-free inference, conformal methods to their limits.
- **Part 58**: e-values, which derandomize knockoffs.
- **Part 59**: the lasso when p and n grow together.
- **Part 62**: subgroups selected in causal analyses.
- **Part 65**: the dissertation's analysis plan.
