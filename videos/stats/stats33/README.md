# Statistics, Built — Part 33: Thousands of Questions

Part 33 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the thirteenth part of Stage III, Master's. Part 32 selected a few variables
among thousands. This part asks what happens to error rates when thousands of questions are asked at once:
- family-wise error and the false discovery rate;
- adaptive and empirical-Bayes versions, and the spread of the false discovery proportion;
- knockoffs;
- the research practices (forking paths, replication, publication bias) that multiply questions silently;
- the false coverage rate.

Its build is the p-hacking simulator (`statkit.multiple.phack`). Its instrument is the p-value sea (`PValueSea`):
sorted p-values against rank, with the Benjamini–Hochberg line sweeping through them, and a grid view of every
p-value. Its kit is `statkit.multiple`.

It opens with Bennett, Baird, Miller & Wolford's dead salmon (2009/2010), illustrated with a toy fish of 9,141 voxels of
spatially smoothed Gaussian noise with 15 independent contrast images (not the original fMRI task design):
- 446 voxels have p < 0.05 (457 expected);
- 78 voxels in 27 clusters have p < 0.01;
- 3 voxels have p < 0.001 (≈ 9 expected);
- Bonferroni and BH find 0.

From there the part covers:
- **The problem.** The World's gene-expression study: 25 patients and 25 controls, 5,000 genes in 200 pathways of 25
  (correlation 0.3), 250 truly differential.
  - Uncorrected p < 0.05 gives 430 discoveries, 214 of them false.
  - The p-value histogram's floor gives π̂0 = 0.962 (truth 0.95).
  - V, S and R; FWER, FDR, FDP.
- **Family-wise error.**
  - Bonferroni and Šidák; Holm's step-down as closed testing (a three-hypothesis lattice); Simes and Hochberg;
    Westfall–Young's permutation maxT.
  - Genes at α = 0.05: Bonferroni 49 (0 false), Holm 50 (1), Westfall–Young 53 (1); power about 20%.
- **The false discovery rate** (Benjamini & Hochberg 1995).
  - The proof that FDR = π0q under independence; BH as a plug-in.
  - PRDS and BY (harmonic factor 9.09 for m = 5,000).
  - Genes: BH at q = 0.05 makes 155 discoveries (6 false); at q = 0.1, 184 (19 false, FDP 10.3%, power 66%); BY at
    q = 0.1, 112 (2 false).
- **Adaptive FDR.** Storey's π̂0 and q-values; Benjamini–Krieger–Yekutieli's two-stage procedure.
- **Empirical Bayes** on Singh et al.'s prostate data (6,033 genes, 50 vs 52 men; z-values from the `sda` package's
  expression matrix).
  - 90 genes have |z| > 3 against 16 expected; local fdr by Lindsey's method.
  - The theoretical null gives π̂0 = 0.954. The empirical null by central matching has δ0 = 0.000 and σ0 = 1.041
    (π̂0 = 0.972).
  - Discoveries:

    | Method | Genes |
    |---|---|
    | Bonferroni | 2 |
    | BH (q = 0.1) | 59 |
    | local fdr < 0.2, theoretical null | 51 |
    | local fdr < 0.2, empirical null | 27 |

- **FDR is an average.** m = 1,000, 900 nulls, effects of 2.5, BH at q = 0.1, 2,000 studies:

  | | independent | equicorrelated ρ = 0.5 |
  |---|---|---|
  | mean FDP | 0.090 | 0.059 |
  | P(FDP > 0.2) | 0.9% | 9.2% |
  | P(no discoveries) | 0% | 19.6% |
  | discoveries | 52 ± 8 | 59 ± 87 |

  Also FDX and simultaneous FDP bounds.
- **Knockoffs** (Barber & Candès 2015; Candès, Fan, Janson & Lv 2018).
  - Exchangeability, Gaussian model-X construction, the lasso coefficient-difference W, the coin-flip proof,
    knockoff+; fixed-X knockoffs.
  - n = 400, p = 150 (AR 0.5), 20 effects, 20 replications. Knockoff+ at q = 0.1 has FDR 8.2% and power 97%; the CV
    lasso has FDR 62% and power 100%.
- **The garden of forking paths.**
  - Simmons, Nelson & Simonsohn's 'When I'm Sixty-Four'; Gelman & Loken.
  - Optional stopping with 10 looks gives a 19% false-positive rate.
  - The p-hacking simulator, 5,000 null studies (Simmons et al. 2011 in brackets):

    | Flexibility | False-positive rate |
    |---|---|
    | none | 5.6% |
    | A: two DVs | 9.9% (9.5%) |
    | B: add 10 per group | 8.3% (7.7%) |
    | C: a covariate | 12.6% (11.7%) |
    | D: drop a condition | 12.7% (12.6%) |
    | A+B+C | 32.6% (30.9%) |
    | all four | 61.3% (60.7%) |

  - Multiverse analysis; many analysts (Silberzahn et al. 2018).
- **Replication.**
  - Ioannidis's PPV, derived. PPV is 94%, 65%, 14% and 1.5% for the four scenarios shown.
  - Power (Button et al. 2013); type M and S errors.
  - OSC (2015): 97% of originals significant against 36% of replications; mean r from 0.40 to 0.20.
  - Camerer et al. (2016, 2018): 11 of 18 economics experiments and 13 of 21 social-science experiments replicated.
  - Errington et al. (2021).
- **Publication bias.** 800 simulated studies of a true effect of 0.2; 278 published (every positive-direction significant study, plus 10%
  of the rest).
  - All studies pool to 0.194, the published ones to 0.301.
  - Egger's intercept is 1.00 (p ≈ 10⁻⁵) for the published studies and −0.06 for all.
  - PET gives 0.176.
  - Exact p-curves (n = 30 per group): the share of significant p-values below 0.01 is 20%, 37% and 72% for d = 0,
    0.3 and 0.7.
  - Selection models; trim-and-fill.
- **Remedies argued.**
  - Preregistration: Kaplan & Irvin (2015), 57% → 8% positive trials. Registered reports: Scheel et al. (2021), 44% vs
    96%.
  - α = 0.005 against 'justify your alpha'; 'abandon significance'; the ASA statement; Bayes factors, estimation,
    equivalence tests.
- **The false coverage rate** (Benjamini & Yekutieli 2005).
  - m = 1,000 with 100 real effects; BH selects about 41.
  - Unadjusted 90% intervals cover 78.7%. FCR-adjusted intervals (multiplier 2.88) cover 90.7%.

Data:
- the prostate microarray (Singh et al. 2002) is the Museum's;
- the gene study is the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.multiple`** ([`explainer/stats/kit/multiple.py`](../../../explainer/stats/kit/multiple.py)), checked in
  `tests/test_stats_kit_multiple.py` against statsmodels' `multipletests`:
  - **Adjusted p-values:** Bonferroni, Šidák, Holm, Hochberg, BH and BY; brute-force closed testing; Westfall–Young
    maxT.
  - **Adaptive and empirical Bayes:** Storey's π0 and q-values; local fdr (Lindsey's method; theoretical and empirical
    null).
  - **Simulation and selection:** FDP simulation under equicorrelation; Gaussian model-X knockoffs, the knockoff(+)
    threshold and lasso W; FCR intervals.
  - **Research practice:** the p-hacking simulator; Ioannidis's PPV; Egger and PET; publication and p-curve models.
- **The World** gains `genes`, and **the Museum** `prostate_z()`.
- **The p-value sea** (`PValueSea` in `explainer/stats/viz.py`).

The Coverage Board gains six rows (1,000 replications each). The FDR rows are 'size' rows with nominal q = 0.1:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| no correction (each p < 0.1), FDR | m = 1,000, 90% null, independent | 0.502 | broken |
| BH, q = 0.1 | independent | 0.090 | conservative |
| BH, q = 0.1 | equicorrelated ρ = 0.5 | 0.065 | conservative |
| BY, q = 0.1 | equicorrelated ρ = 0.5 | 0.011 | conservative |
| unadjusted 90% CIs, BH-selected (FCR) | 100 real effects | 78.5% | broken |
| FCR-adjusted CIs, BH-selected | 100 real effects | 90.6% | conservative |

## Build it

```bash
python -m videos.stats.stats33.compute         # once (a few minutes)
python tools/build.py stats33 -q l             # fast 480p preview
python tools/build.py stats33                  # 1080p30 -> renders/stats33.mp4
python tools/qa_scene.py stats33 FDR
python tools/lecture_length.py stats33 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The dead salmon | 446 of 9,141 at p < .05; 0 corrected |
| 1 | The problem | 430 discoveries, 214 false |
| 2 | Family-wise error | Bonferroni 49, Holm 50, WY 53 |
| 3 | The false discovery rate | BH 184 (19 false); BY 112 |
| 4 | Adaptive FDR | π̂0 = 0.962 |
| 5 | Empirical Bayes | σ0 = 1.041; 51 → 27 genes |
| 6 | FDR is an average | P(FDP > 0.2) 0.9% vs 9.2% |
| 7 | Knockoffs | FDR 8.2%, power 97% vs lasso 62% |
| 8 | The garden of forking paths | 61.3% false positives |
| 9 | Replication | PPV 94% … 1.5%; OSC 36% |
| 10 | Publication bias | 0.301 vs 0.2; Egger p ≈ 10⁻⁵ |
| 11 | Remedies argued | 57% → 8%; 44% vs 96% |
| 12 | The false coverage rate | 78.7% vs 90.7% |
| 13 | Outro | — |

## Sources

- **Imaging.**
  - C. Bennett, A. Baird, M. Miller & G. Wolford, *J. Serendipitous Unexpected Results* 1 (2010); poster at OHBM
    (2009).
- **FWER.**
  - C. Bonferroni (1936); O. J. Dunn, *JASA* 56 (1961); Z. Šidák, *JASA* 62 (1967); S. Holm, *Scand. J. Stat.* 6
    (1979).
  - R. Marcus, E. Peritz & K. Gabriel, *Biometrika* 63 (1976); R. Simes, *Biometrika* 73 (1986); Y. Hochberg,
    *Biometrika* 75 (1988).
  - P. Westfall & S. Young, *Resampling-Based Multiple Testing* (1993).
- **FDR.**
  - Y. Benjamini & Y. Hochberg, *JRSS B* 57 (1995); Y. Benjamini & D. Yekutieli, *Ann. Stat.* 29 (2001).
  - J. Storey, *JRSS B* 64 (2002), *Ann. Stat.* 31 (2003); J. Storey & R. Tibshirani, *PNAS* 100 (2003).
  - Y. Benjamini, A. Krieger & D. Yekutieli, *Biometrika* 93 (2006).
  - E. Lehmann & J. Romano, *Ann. Stat.* 33 (2005); C. Genovese & L. Wasserman, *JASA* 101 (2006); J. Goeman &
    A. Solari, *Stat. Sci.* 26 (2011).
- **Empirical Bayes.**
  - B. Efron, *JASA* 99 (2004), 102 (2007), 106 (2011); B. Efron, R. Tibshirani, J. Storey & V. Tusher, *JASA* 96
    (2001).
  - D. Singh et al., *Cancer Cell* 1 (2002); J. Lindsey (1974).
- **Knockoffs.**
  - R. F. Barber & E. Candès, *Ann. Stat.* 43 (2015); E. Candès, Y. Fan, L. Janson & J. Lv, *JRSS B* 80 (2018).
  - M. Sesia, C. Sabatti & E. Candès, *Biometrika* 106 (2019).
- **Research practice.**
  - J. Simmons, L. Nelson & U. Simonsohn, *Psych. Sci.* 22 (2011); A. Gelman & E. Loken, *Amer. Sci.* 102 (2014).
  - S. Steegen et al., *Persp. Psych. Sci.* 11 (2016); R. Silberzahn et al., *AMPPS* 1 (2018).
  - J. Ioannidis, *PLoS Med.* 2 (2005); K. Button et al., *Nat. Rev. Neurosci.* 14 (2013); A. Gelman & J. Carlin,
    *Persp. Psych. Sci.* 9 (2014).
  - Open Science Collaboration, *Science* 349 (2015); C. Camerer et al., *Science* 351 (2016), *Nat. Hum. Behav.* 2
    (2018); T. Errington et al., *eLife* 10 (2021).
  - R. Rosenthal, *Psych. Bull.* 86 (1979); M. Egger, G. Davey Smith, M. Schneider & C. Minder, *BMJ* 315 (1997).
  - T. Stanley & H. Doucouliagos, *Res. Synth. Methods* 5 (2014); U. Simonsohn, L. Nelson & J. Simmons, *J. Exp.
    Psych. Gen.* 143 (2014).
  - L. Hedges, *J. Educ. Stat.* 9 (1984); I. Andrews & M. Kasy, *AER* 109 (2019); S. Duval & R. Tweedie,
    *Biometrics* 56 (2000).
  - R. Kaplan & V. Irvin, *PLoS One* 10 (2015); C. Chambers, *Cortex* 49 (2013); A. Scheel, M. Schijen & D. Lakens,
    *AMPPS* 4 (2021).
  - D. Benjamin et al., *Nat. Hum. Behav.* 2 (2018); D. Lakens et al., *Nat. Hum. Behav.* 2 (2018).
  - B. McShane et al., *Amer. Stat.* 73 (2019); V. Amrhein, S. Greenland & B. McShane, *Nature* 567 (2019);
    R. Wasserstein & N. Lazar, *Amer. Stat.* 70 (2016).
- **FCR.** Y. Benjamini & D. Yekutieli, *JASA* 100 (2005); W. Fithian, D. Sun & J. Taylor, arXiv (2014).
- **Books.**
  - B. Efron, *Large-Scale Inference* (2010).
  - P. Westfall & S. Young, *Resampling-Based Multiple Testing* (1993).
  - S. Dudoit & M. van der Laan, *Multiple Testing Procedures with Applications to Genomics* (2008).
  - M. Borenstein, L. Hedges, J. Higgins & H. Rothstein, *Introduction to Meta-Analysis* (2009).

## Problems and solutions

**1. Holm controls the FWER under any dependence.**

*Solution.* Let I₀ be the true nulls, m₀ = |I₀|, and let j be the true null with the smallest p-value. A false
rejection requires Holm to reach and reject j. When it does, at most m − m₀ hypotheses have been rejected before it,
so j's step has threshold α/(m − k + 1) ≤ α/m₀. Hence a false rejection implies min_{i∈I₀} p_i ≤ α/m₀, and by the
union bound P(min_{i∈I₀} p_i ≤ α/m₀) ≤ m₀·α/m₀ = α.

**2. BH's exact FDR.**

*Solution.* With R⁽ⁱ⁾ the number BH rejects when p_i is set to 0, the events {i rejected, R = k} and
{p_i ≤ qk/m, R⁽ⁱ⁾ = k} coincide. Then E[1{i rej}/R] = Σ_k (1/k)P(p_i ≤ qk/m)P(R⁽ⁱ⁾ = k) by independence. This is
Σ_k (1/k)(qk/m)P(R⁽ⁱ⁾ = k) = q/m. Summing over the m₀ true nulls gives FDR = m₀q/m = π₀q.

**3. The BY bound.**

*Solution.* Let c = Σ_{j≤m} 1/j and Δ = q/(mc), and let i be a true null rejected with R = k. Then p_i ≤ kΔ, so
p_i ∈ ((j − 1)Δ, jΔ] for some j ≤ k, and then 1/R = 1/k ≤ 1/j. Hence 1{i rejected}/R ≤ Σ_{j=1}^m (1/j)·1{p_i ∈
((j − 1)Δ, jΔ]}, whatever the dependence. For exactly uniform nulls, taking expectations, the contribution is at most
Σ_j (1/j)Δ = cΔ = q/m. Summing over m₀ ≤ m nulls gives FDR ≤ q. For super-uniform nulls, use summation by parts with the nonincreasing step weight and P(p_i≤jΔ)≤jΔ; individual bin probabilities need not be bounded by Δ.

**4. Storey’s uncapped estimate at a fixed λ has conservative expectation.**

*Solution.* E#{p_i > λ} ≥ E#{null p_i > λ} = m₀(1 − λ), because null p-values are uniform. So
E π̂₀(λ) = E#{p_i > λ}/(m(1 − λ)) ≥ m₀/m = π₀. This refers to the uncapped estimator. Clipping at one can bias it downward (under an all-null uniform model, its expectation is strictly below one). An upward mean alone does not prove finite-sample FDR control for a plug-in adaptive procedure.

**5. The knockoff coin flip.**

*Solution.* Swapping a null variable j with its knockoff leaves the joint law of (X, X̃, y) unchanged: it leaves that
of (X, X̃) unchanged by exchangeability, and y depends on X only through non-null variables, given which X̃ is
irrelevant. But the swap maps W_j to −W_j and leaves |W_j| and the other W's unchanged. So (W_j, |W|) and (−W_j, |W|)
have the same law: conditional on all magnitudes and nonnull statistics, the nonzero null signs are independent fair coins. Zero W values are excluded. The joint flip-sign property is essential. The knockoff+ threshold then gives
FDR ≤ q by a supermartingale (optional stopping) argument over the ordered |W|.

**6. Ioannidis's formula.**

*Solution.* Per unit of null studies there are R real ones. True positives come from real effects significant by
power, (1 − β)R, plus a share u of the real-but-missed ones, uβR. False positives come from nulls, α, plus a share u
of the null negatives, u(1 − α). So PPV = [(1 − β)R + uβR]/[(1 − β)R + uβR + α + u(1 − α)], which is the formula in
the code. With u = 0, PPV = (1 − β)R/((1 − β)R + α), and PPV < ½ iff R < α/(1 − β). For power 0.8 that is
R < 0.0625, a prior below 0.0625/1.0625 ≈ 5.9%.

## Glossary

- **Multiplicity; family; V, S, R; FWER; FDR; FDP; per-comparison error rate**: the bookkeeping of many tests.
- **Bonferroni; Šidák; Holm; closed testing; Simes; Hochberg; Westfall–Young maxT**: family-wise procedures.
- **Benjamini–Hochberg; PRDS; Benjamini–Yekutieli**: false discovery rate procedures.
- **π₀; Storey's estimator; q-value; two-stage BH**: adaptive FDR.
- **Two-groups model; local fdr; Fdr; Lindsey's method; theoretical and empirical null; central matching**: Efron's
  empirical Bayes.
- **FDX; simultaneous FDP bounds**: controlling one study's proportion.
- **Knockoffs (fixed-X, model-X); exchangeability; W statistic; knockoff+**: selection with FDR control.
- **Researcher degrees of freedom; garden of forking paths; p-hacking; optional stopping; multiverse**: hidden
  multiplicity.
- **PPV; power; type M and type S errors; replication**: what a literature's positives mean.
- **File drawer; funnel plot; Egger's test; PET; p-curve; selection model; trim-and-fill**: publication bias.
- **Preregistration; registered report; α = 0.005; equivalence test**: remedies.
- **False coverage rate; FCR-adjusted interval**: intervals after selection.

## Where it comes back

| Idea | Returns in |
|---|---|
| exchangeability and conformal prediction | 34 |
| many outcomes in one trial | 35 |
| multiplicity in imputation | 41 |
| testing many hypotheses optimally | 46 |
| sparse-signal detection; higher criticism | 50 |
| selective inference and PoSI | 56 |
| e-values: FDR at any stopping time | 58 |
| genome-scale causal discovery | 62 |
| the Coverage Board | every part; 65 |


## Scientific QA — 2026-11-07

All 14 English chapters, calculations, solutions and shared helpers were reviewed.
FDR is an average across studies; a single realized FDP near q does not verify its theorem.
Bonferroni/Holm require valid marginal p-values; Simes/Hochberg need suitable joint dependence.
Westfall–Young needs null exchangeability and, for strong control, subset pivotality; permutation counts use +1.
The independent BH equality requires uniform nulls and an admissible level. Adaptive plug-in estimates,
model-based local fdr, and conditional null fits need their own assumptions.

The six Board uncertainties now use sample SD of study-level proportions divided by sqrt(1000),
including zero-selection families. Its interval rows display **1−FCR**, not pooled coverage of
individual intervals. An empty family has noncoverage zero. With these correct uncertainties,
BH under independence and the adjusted intervals are slightly conservative against their nominal
levels; their mean values have not changed. Rα/m intervals are justified here for simple selection
rules such as BH with independent estimates; arbitrary selection needs the minimum selection-count
construction. Conditional selected-model inference additionally requires its stated sampling model.

Knockoff lasso CV now refits centering and scaling in each training fold on a fixed 25-penalty grid.
The 20-replicate mean FDP is 0.0821 ± 0.0166 (MC SE) for knockoff+ and 0.6251 ± 0.0159 for CV lasso;
this small simulation illustrates the theorem rather than establishing it. The compiled audit solver
checks every lasso KKT residual below 2e−7 and retains all study-level FDP/power values.
The teaching computation retains its original coordinate-descent solver.

The primary `sda::singh2002` R matrix (102×6033, cancer minus healthy pooled t with 100 df) was
independently transformed to t/z. It agrees with the Museum table within 5.62e−7 for t and 5.87e−7
for z; small differences slightly exceed half a unit in the table’s sixth decimal. This is a numerical
agreement check, not a claim of bit-identical rounding. The finite-window local-fdr density agrees
with an independent converged statsmodels Poisson GLM to 1.4e−15 absolute error.

Full FDP histograms show [0,1] with uncapped bar heights. Knockoff plots include both signs without
clipping, formula sequences retain context headings, and the recap heading appears before narration.
The p-hacking simulator is illustrative: its combined A+B+C result differs from the historical table
by about 2.6 Monte Carlo SE. Funnel asymmetry and p-curve patterns are diagnostics with alternative
explanations, and PET extrapolation is model-dependent. Registration comparisons are observational.

Source checks, independent numerical tests and reproducible input hashes are archived in
[the Part 33 evidence](../../../docs/qa/evidence/stats33-polish-20261107/README.md). The recorded English sampled visual checkpoint is complete; continuous listening/playback, Chinese production and final narrated masters remain open.
