# Statistics, Built — Part 8: From Sample to Population

Part 8 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. Parts 6 and 7 gave the laws of averages
and the machinery of simulation. This part turns both on statistics themselves: how much does an estimate wobble from
sample to sample, and how can one sample tell you?

It opens with Student (W. S. Gosset) at Guinness, 1908. He shuffled 3,000 cards bearing the heights of Macdonell's
criminals and dealt 750 samples of four. Redone here with one seeded shuffle, the textbook interval x̄ ± 1.96 s/√n
covers only 87.1% of the time; Student's t₃ multiplier, 3.18, covers 96.7%. From there the part covers:
- sampling distributions and standard errors (the sampling machine);
- the n − 1, as an expectation and as a dimension;
- Fisher's rotation of the sample, and from it χ², Cochran's theorem, Student's t and Snedecor's F;
- bias, variance and mean squared error;
- consistency and plug-in estimators;
- standard errors for ratios, with Laplace's 1802 census of France;
- finite populations;
- the robustness of normal theory (Box 1953).

The Coverage Board opens with its first seven rows.

Every number on screen is computed in [`compute.py`](compute.py). The Museum supplies:
- Macdonell's 3,000 heights (`museum.CRIM_*`, from R's `crimtab`);
- Student's sleep data (`museum.SLEEP_*`);
- Laplace's census figures (`museum.LAPLACE`).

Everything else is the World (seed 1662) or a seeded simulation, and is tagged as such.

**Built in this part:** the first rows of the Coverage Board ([`explainer/stats/board.py`](../../../explainer/stats/board.py)),
written to `.cache/stats8/board.json` by `python -m videos.stats.stats8.compute --force board`. Each row has R = 10,000
replications.

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| z, known σ | heights, n = 5 | 95.05% | kept |
| z with s | heights, n = 5 | 87.60% | broken |
| Student's t | heights, n = 5 | 94.39% | kept |
| Student's t | incomes, n = 20 | 88.24% | broken |
| Student's t | incomes, n = 500 | 92.78% | broken |
| F-test, σ₁ = σ₂ (size) | heights, n = 10, 10 | 4.89% | kept |
| F-test, σ₁ = σ₂ (size) | log incomes, n = 10, 10 | 6.28% | broken |

## Build it

```bash
python -m videos.stats.stats8.compute          # once: every computed item (seconds; cached in .cache/stats8)
python tools/build.py stats8 -q l              # fast 480p preview
python tools/build.py stats8                   # 1080p30 -> renders/stats8.mp4
python tools/qa_scene.py stats8 Board          # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats8 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | Student at Guinness | Gosset's problem; his 1904 brewery report and year with Pearson; Macdonell's heights; 3,000 cards dealt in fours; t against the normal. | z-interval covers 87.1%, t₃ 96.7% (heights rounded to inches); World: 85.1% vs 94.4% |
| 1 | Sampling distributions | The sampling machine on the World's men; n = 4, 16, 64; SE = σ/√n; proportions; the median's sampling distribution and Laplace's SE formula. | SD of x̄: 3.56, 1.76, 0.89 (σ = 7.10); median efficiency 0.65 at n = 64; SE(median) 1.11 vs 1.10 simulated |
| 2 | Why n − 1 | Simulated bias of the n divisor; the algebra; the residual's plane in ℝ³ (turned); c₄ and E s < σ; degrees of freedom. | divisor n at n = 2: 0.504σ²; n − 1: 1.008σ²; c₄(5) = 0.940 |
| 3 | Fisher's geometry | Spherical symmetry; Helmert's rotation; Fisher's 1912 letter; x̄ ⟂ s for normal vs exponential samples; t as the cotangent of an angle; the four consequences. | corr(x̄, s): 0.01 (normal), 0.75 (exponential) |
| 4 | χ² and Cochran | The χ² family; Helmert (1876), Pearson (1900) and Fisher's df correction; World samples; Cochran's theorem; the interval for σ and its coverage on non-normal data; Wilson–Hilferty. | means 3.01, 9.02; n = 10, s = 9: σ ∈ [6.2, 16.4]; coverage 95.2% (men), 96.7% (all adults), 93.0% (log incomes) |
| 5 | Student's t | Density derived as a scale mixture; the family; multipliers; Student's sleep data, paired and unpaired. | t = 4.06, p = 0.003, CI [0.70, 2.46]; unpaired t = 1.86, p = 0.079 (corr 0.80) |
| 6 | The F distribution | Definition; shapes; World variance ratios against F₄,₉; ANOVA preview; t² = F, the beta link. | 95% range 0.11 to 4.72 |
| 7 | Bias, variance, MSE | Dartboards; MSE = Var + bias²; the divisor n + 1; add-two shrinkage for a proportion; the bias–variance trade-off; Cramér–Rao preview. | MSE/σ⁴ at n = 5: 0.500, 0.360, 0.333 for n − 1, n, n + 1; shrinkage wins for 0.21 < p < 0.80 at n = 20 |
| 8 | Consistency and plug-in | T(F̂ₙ); five plug-in paths converging; Fisher's z for r; consistent vs unbiased; the sample maximum; the bootstrap preview. | Fisher z: SD 0.370 vs 1/√7 = 0.378; E max of 10 from 1,000 = 910 |
| 9 | Standard errors for ratios | Laplace's 1802 census; the ratio estimator; the delta-method SE; purposive vs random selection; the World version. | 28.35 people per birth → 28.35 million; World: SD 24,195, mean design-linearized SE 21,402 (FPC included), coverage 89.7% |
| 10 | Finite populations | The negative covariance of draws without replacement; FPC; simulation; sample-size planning; n, not N. | n₀ = 1,068 after rounding up; N = 2,000: 697; N = 10⁷: 1,067 |
| 11 | The Coverage Board opens | The protocol; 40 intervals each way; the first seven rows; what they say. | the table above |
| 12 | How robust is normal theory? | t-test and F-test sizes under four distributions; Var(s²) and kurtosis (3.7 times the normal-theory variance at n = 10 when excess kurtosis is 6); one-sided misses under skew; Box (1953). | t: 4.9–5.4% except exponential 10.0% (9.5% low, 0.4% high); F: 1.0% (uniform) to 23.2% (exponential) |
| 13 | Outro | Recap, payoffs, problems, references, the Transcript, Part 9's question. | — |

## Sources

- **Student.** "Student" (W. S. Gosset), "The probable error of a mean", *Biometrika* 6 (1908).
  - Data: W. R. Macdonell, *Biometrika* 1 (1902); A. Cushny & A. Peebles, *J. Physiology* 32 (1905).
  - E. S. Pearson, *'Student': A Statistical Biography of William Sealy Gosset* (1990).
- **Fisher.**
  - R. A. Fisher, *Biometrika* 10 (1915); "Applications of 'Student's' distribution", *Metron* 5 (1925).
  - *Statistical Methods for Research Workers* (1925).
- **Distributions.** F. R. Helmert (1876); K. Pearson (1900); W. G. Cochran, *Proc. Camb. Phil. Soc.* 30 (1934);
  G. Snedecor (1934); E. B. Wilson & M. Hilferty, *PNAS* 17 (1931); R. C. Geary (1936).
- **Laplace.** P.-S. Laplace, *Théorie analytique des probabilités* (1812).
  - W. G. Cochran, "Laplace's ratio estimator" (1978); S. Stigler, *The History of Statistics* (1986).
  - A. Bowley (1906); J. Neyman, *JRSS* 97 (1934).
- **MSE and bounds.** W. James & C. Stein (1961); A. Agresti & B. Coull, *Am. Stat.* 52 (1998); H. Cramér (1946);
  C. R. Rao (1945).
- **Robustness.** G. E. P. Box, "Non-normality and tests on variances", *Biometrika* 40 (1953).
- **Textbooks.**
  - G. Casella & R. Berger, *Statistical Inference* (2nd ed., 2002), ch. 5.
  - J. Rice, *Mathematical Statistics and Data Analysis* (3rd ed., 2007), chs. 6–8.
  - W. G. Cochran, *Sampling Techniques* (3rd ed., 1977).

## Problems and solutions

**1. E Σ(xᵢ − x̄)² = (n − 1)σ².**

*Solution.* Σ(xᵢ − x̄)² = Σ(xᵢ − μ)² − n(x̄ − μ)². The cross term is 2(x̄ − μ)Σ(xᵢ − x̄) = 0. Taking expectations
gives nσ² − n·σ²/n = (n − 1)σ². Identical means and variances, independence, and a finite variance are sufficient.

**2. Two intervals.** n = 9, x̄ = 50, s = 6.

*Solution.*
- **For μ:** 50 ± t₈,₀.₉₇₅ · 6/3 = 50 ± 2.306 · 2 = [45.39, 54.61].
- **For σ²:** [8 · 36/χ²₈,₀.₉₇₅, 8 · 36/χ²₈,₀.₀₂₅] = [288/17.53, 288/2.180] = [16.4, 132.1]. So σ ∈ [4.05, 11.49].

Both intervals have exact coverage under IID normal data; the variance interval is especially sensitive to nonnormality (chapter 4's coverage check).

**3. t² = F.**

*Solution.* T = Z/√(V/k) with Z ⟂ V ~ χ²ₖ. Then T² = (Z²/1)/(V/k), and Z² ~ χ²₁ is independent of V, so T² is a ratio
of independent χ²s over their df: F₁,ₖ.

**4. The best divisor.**

*Solution.* SS/σ² ~ χ²ₙ₋₁, so

MSE(c)/σ⁴ = ((n − 1)/c − 1)² + 2(n − 1)/c².

The derivative is −2(n − 1)/c² · ((n − 1)/c − 1) − 4(n − 1)/c³. Setting it to zero gives (n − 1) − c + 2 = 0, so
c = n + 1. The minimum is

MSE = σ⁴((n − 1 − n − 1)² + 2(n − 1))/(n + 1)² = 2σ⁴/(n + 1),

against 2σ⁴/(n − 1) for the unbiased divisor.

**5. The SE of a ratio.**

*Solution.* With R = μ_y/μ_x,

ȳ/x̄ − R = (ȳ − Rx̄)/x̄ ≈ (1/μ_x) · mean(yᵢ − Rxᵢ).

So SE(ȳ/x̄) ≈ (1/|μ_x|)√((σ_y² − 2Rσ_xy + R²σ_x²)/n). Estimate it by plugging in x̄, R̂ and the sample variance of the
residuals eᵢ = yᵢ − R̂xᵢ.

**6. A sample size from N = 2,000.**

*Solution.* We need (σ²/n)(N − n)/(N − 1) = σ²/400, so n = 400N/(N + 399) = 800,000/2,399 = 333.5, and the sample
needs 334. Without the correction it would need 400.

## Where it comes back

| Idea | Returns in |
|---|---|
| sampling distributions, standard errors | 9, 11, 16, 47 |
| t, χ², F; Cochran's theorem; degrees of freedom | 10, 12, 13, 23 |
| bias–variance, shrinkage, Cramér–Rao | 9, 25, 29, 32, 45 |
| plug-in, consistency, the bootstrap | 9, 16, 47, 48 |
| ratio estimation, delta-method SEs | 14, 18, 22 |
| finite populations, random vs purposive sampling | 18, 41 |
| the Coverage Board | every part; 65 |
| robustness to non-normality | 16, 30, 60 |
