# Statistics, Built — Part 5: Many Variables at Once

Part 5 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. Parts 2–3 built one random variable at a
time and Part 4 built the matrices; this part puts several variables together and asks how they move.

It opens with Francis Galton's table of 928 adult children and their mid-parents (1886). A fitted Gaussian gives nested
ellipses with one centre and shape, approximating the count pattern; the children of tall parents are tall, but less so. From that
one picture come joint, marginal and conditional distributions, conditional expectation as the best predictor (a
projection), Eve's law, the multivariate normal and its conditioning formula, regression to the mean, the three
lines through an ellipse, change of variables, latent variables, copulas, exchangeability and de Finetti, measures of
dependence, and distributions on the simplex.

Every number on screen is computed in [`compute.py`](compute.py). Galton's counts are the Museum's
(`museum.GALTON_*`, from HistData; Hanley 2004). Everything else is the World (seed 1662) or a seeded simulation, and
is tagged as such.

**Built in this part:** the Gaussian slicer (`GaussianSlicer` in [`explainer/stats/viz.py`](../../../../explainer/stats/viz.py)).
It is a bivariate normal density drawn as a turnable wireframe surface over its floor. It cuts the surface at chosen
values of x, and each slice, renormalized, is the conditional density of y given x: a normal whose centre moves along
the regression line and whose width never changes. It is used for the World's families (mid-parent and son), and it
comes back whenever a later part conditions a Gaussian (Parts 15, 25, 26, 39).

Also built: a Pólya urn machine ([`s13_exchange.py`](s13_exchange.py)) that draws a ball, returns it with a twin, and
plots the running fraction of red for thirty urns at once.

## Build it

```bash
python -m videos.stats.stats5.compute          # once: every computed item (seconds; cached in .cache/stats5)
python tools/build.py stats5 -q l              # fast 480p preview
python tools/build.py stats5                   # 1080p30 -> renders/stats5.mp4
python tools/qa_scene.py stats5 Condition      # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats5 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | Galton's ellipses | Galton's 1886 table, counted and smoothed into nested ellipses; "regression towards mediocrity"; the objectives. | 928 children, 205 families; r = 0.459; slope 0.646 (Galton's "two-thirds") |
| 1 | Joint, marginal, conditional | Galton's table in four bands: joint cells, row and column sums, a conditional row; the joint density as a surface; slicing it with the Gaussian slicer; Bayes for densities; the exact joint table of the max and min of two dice. | slices at 162/170/178 cm: conditional means 170.4/176.3/182.3, SD 6.06; Cov(max, min) = (35/36)², corr = 35/73 |
| 2 | Dependence | A gallery of uncorrelated-but-dependent shapes (Y = X², the ring, the random-sign pair); covariance as a bilinear form; the variance of an average of equicorrelated variables (diversification); Bernstein's pairwise-but-not-mutually independent coins. | r ≈ 0.000, −0.006, −0.007; Var(X̄)/σ² → ρ |
| 3 | Conditional expectation | The World's log incomes by age: the best constant, the best line, the conditional mean; the proof that E[Y \| X] minimizes mean squared error; the tower property; E[Y \| X] as an orthogonal projection in L²; the conditional median under absolute loss and conditional quantiles. | MSE 0.408 / 0.405 / 0.360; R² 0.007 for the line vs 0.119 for E[Y \| X] |
| 4 | Eve's law | Var Y = E Var(Y \| X) + Var E[Y \| X], derived; Galton's children; the World's incomes by age; Pearson's correlation ratio η² against r²; a rare switch that makes the conditional variance larger. | Galton 6.33 = 4.93 + 1.40 (η² 0.221 vs r² 0.210); log income 0.408 = 0.367 + 0.041 |
| 5 | The multivariate normal | AZ + μ moving a round cloud into an ellipse; the density from the change of variables; affine images, marginals, Cramér–Wold; two normals that are not jointly normal; squared Mahalanobis distances against χ²₃ as a radial diagnostic (insufficient to establish joint normality). | sample covariance matches AAᵀ; 4,000 draws on the χ²₃ diagonal |
| 6 | Conditioning a Gaussian | The conditioning theorem (Schur complement) and its proof by decorrelation; the two-variable case is the regression line; Galton's numbers; the precision matrix of a chain X → Y → Z, whose zero means conditional independence. | conditional SD √(1 − r²)·s_y; corr(X, Z) = 0.56 but K₁₃ = 0 |
| 7 | Regression to the mean | The World's tallest tenth of mid-parents and their sons; both directions; Galton's stable variance via Eve's law; skill + luck test–retest; Kahneman's flight instructors. | +8.76 → +6.60 cm; 6.33 = 1.33 + 5.00; top tenth about 1.71 → 0.83 SD, bottom about −1.74 → −0.86 |
| 8 | Three lines through one ellipse | Y on X, X on Y and the major axis on Galton's ellipse; what each minimizes; errors in variables and Spearman's attenuation. | slopes 0.646, 1/0.326, 2.02; slope 1.01 → 0.49 with reliability ½ |
| 9 | Change of variables | The density of a transformed vector and its Jacobian; the sum of two uniforms by convolution (a triangle); the ratio of two normals (Cauchy); polar coordinates and the Rayleigh distribution. | E R = √(π/2) = 1.2533 vs simulated 1.2567 |
| 10 | Latent variables | The World's adult heights as a mixture of men and women; marginalizing a latent class; Pearson's crabs (1894); the posterior class probability (the E step of EM); Simpson's paradox in Part 1's clinic as a latent variable. | men 176.0 ± 7.1, women 163.0 ± 6.4, all SD 9.37; clinic: treated 0.624 vs 0.737 overall, but higher within each severity |
| 11 | Copulas | Sklar's theorem (1959); Gaussian, Clayton and Gumbel copulas with the same Kendall's τ and different tails; sampling from a copula with any margins; Li's Gaussian copula and the crisis. | τ = 0.5; joint tail rates (lower/upper) 0.45/0.375, 0.68/0.12, 0.33/0.555; τ 0.507 survives every step |
| 12 | Exchangeability | The Pólya urn machine; its limiting fractions are uniform; exchangeable sequences; de Finetti's theorem (1931); finite exchangeability without replacement and the Diaconis–Freedman bound. | RRB, RBR, BRR each 1/12; urn RRBB: P(RR) = 1/6 vs 1/4, corr −1/3 |
| 13 | Measuring dependence | Pearson, Spearman, Kendall, distance correlation and mutual information on six shapes; rank correlations defined; their invariance under an increasing transform, measured; dCor and MI. | Pearson 0.396 → 0.301; Spearman 0.379 and Kendall 0.259 unchanged |
| 14 | The simplex | The multinomial and its negative covariances; the Dirichlet in four shapes; the Dirichlet as normalized gammas (and independent of their total); Dirichlet–multinomial conjugacy; Pearson's spurious correlation of ratios. | sample corr(X/Z, Y/Z) = 0.46 from independent positive lognormal X, Y, Z |
| 15 | Outro | Recap, payoffs, problems, references, the Transcript, Part 6's question. | — |

## Sources

- **Galton.** F. Galton, "Regression towards mediocrity in hereditary stature", *J. Anthropological Institute* 15
  (1886); *Natural Inheritance* (1889). Data: J. A. Hanley, "'Transmuting' women into men: Galton's family data on
  human stature", *The American Statistician* 58 (2004); the HistData package.
- **Correlation and the correlation ratio.** K. Pearson, "Regression, heredity, and panmixia" (1896); "On a form of
  spurious correlation which may arise when indices are used in the measurement of organs" (1897); η² in
  "On homotyposis in homologous but differentiated organs", *Proc. Royal Society* 71 (1903).
- **Mixtures.** K. Pearson, "Contributions to the mathematical theory of evolution" (1894), on W. F. R. Weldon's
  Naples crabs.
- **Rank correlations.** C. Spearman, "The proof and measurement of association between two things" (1904), which
  also gives the correction for attenuation; M. Kendall, "A new measure of rank correlation", *Biometrika* 30 (1938).
- **Distance correlation.** G. Székely, M. Rizzo & N. Bakirov, *Annals of Statistics* 35 (2007).
- **Copulas.** A. Sklar (1959); R. Nelsen, *An Introduction to Copulas* (2nd ed., 2006); H. Joe, *Dependence Modeling
  with Copulas* (2014); D. X. Li, "On default correlation: a copula function approach", *J. Fixed Income* (2000);
  D. MacKenzie & T. Spears, "'The formula that killed Wall Street'?", *Social Studies of Science* 44 (2014).
- **Exchangeability.** F. Eggenberger & G. Pólya (1923); B. de Finetti (1931); P. Diaconis & D. Freedman, "Finite
  exchangeable sequences", *Annals of Probability* 8 (1980).
- **Covariance selection.** A. P. Dempster, "Covariance selection", *Biometrics* 28 (1972).
- **Pairwise independence.** S. N. Bernstein, *Theory of Probability* (in Russian, 1927).
- **The gamma characterization.** E. Lukacs, "A characterization of the gamma distribution", *Ann. Math. Statist.* 26
  (1955).
- **Compositional data.** J. Aitchison, "The statistical analysis of compositional data", *JRSS B* 44 (1982).
- **Regression to the mean.** A. Tversky & D. Kahneman, "Judgment under uncertainty" (1974); D. Kahneman, *Thinking,
  Fast and Slow* (2011), ch. 17.
- **Textbooks.**
  - J. Blitzstein & J. Hwang, *Introduction to Probability* (2nd ed., 2019), chs. 7, 9, 10.
  - G. Casella & R. Berger, *Statistical Inference* (2nd ed., 2002), ch. 4.
  - T. W. Anderson, *An Introduction to Multivariate Statistical Analysis* (3rd ed., 2003).
  - S. Stigler, *The History of Statistics* (1986), *Statistics on the Table* (1999), *The Seven Pillars of
    Statistical Wisdom* (2016).

## Problems and solutions

**1. Uncorrelated but dependent.** X ~ N(0, 1), Y = X².

*Solution.*
- Cov(X, Y) = E X³ − E X · E X² = 0 − 0 = 0, since the odd moments of a symmetric variable vanish.
- E[Y | X] = X², because Y is a function of X.
- E[X | Y] = 0. Given Y = y, X is ±√y with equal probability, by symmetry.
- Y is a function of X, so they are as dependent as can be; correlation sees none of it, because the relationship
  is not monotone.

**2. Eve's law.** Assume Y has a finite second moment.

*Solution.* Write μ(X) = E[Y | X]. Then
- Var Y = E(Y − EY)² = E(Y − μ(X) + μ(X) − EY)².
- Expand. The cross term E[(Y − μ(X))(μ(X) − EY)] vanishes: condition on X, and E[Y − μ(X) | X] = 0, by the tower
  property.
- The first square is E[E[(Y − μ(X))² | X]] = E Var(Y | X).
- The second is E(μ(X) − EY)² = Var μ(X), since E μ(X) = EY.

So Var Y = E Var(Y | X) + Var E[Y | X].

**3. A bivariate normal.** σ_X = 2, σ_Y = 3, ρ = 0.6.

*Solution.*
- E[Y | X = x] = μ_Y + ρ(σ_Y/σ_X)(x − μ_X) = μ_Y + 0.9(x − μ_X).
- Var(Y | X = x) = σ_Y²(1 − ρ²) = 9 × 0.64 = 5.76, an SD of 2.4, for every x.
- The regression of X on Y has slope ρσ_X/σ_Y = 0.4. Drawn on the same (x, y) axes, that line has slope 1/0.4 = 2.5,
  steeper than the Y-on-X slope of 0.9.

**4. A retest.** Assume a bivariate normal model, 2 SD above the mean, test–retest correlation 0.7.

*Solution.* In standard units, E[Z₂ | Z₁ = 2] = ρ · 2 = 1.4. The predicted retest is 1.4 SD above the mean, with
conditional SD √(1 − 0.49) = 0.71. That is regression to the mean; nobody's skill changed.

**5. Pólya's urn.** One red, one blue; draw, return with another of the same colour.

*Solution.*
- P(first n all red) = (1/2)(2/3)(3/4)⋯(n/(n + 1)) = 1/(n + 1), since the product telescopes.
- For the uniform: if p ~ U(0, 1), then E pⁿ = ∫₀¹ pⁿ dp = 1/(n + 1).
- More generally, any particular sequence with k reds and n − k blues has probability k!(n − k)!/(n + 1)!, which is
  ∫ pᵏ(1 − p)ⁿ⁻ᵏ dp. So the sequence is exchangeable, and it is a mixture of i.i.d. Bernoulli(p) with p uniform.
- By de Finetti, the fraction of red converges to that p, so the limit is uniform on (0, 1). The moments 1/(n + 1)
  determine the distribution, since it lives on a bounded interval.

**6. U₁ + U₂ + U₃.**

*Solution.* The sum of two uniforms has the triangle density t on [0, 1] and 2 − t on [1, 2]. Convolve it with U(0, 1),
so that f₃(s) = ∫_{s−1}^{s} f₂(t) dt:
- On [0, 1]: s²/2.
- On [1, 2]: (−2s² + 6s − 3)/2, which equals 3/4 at s = 3/2.
- On [2, 3]: (3 − s)²/2.

The pieces join smoothly, and the curve is already bell-shaped: Part 6's central limit theorem, beginning.

## Where it comes back

| Idea | Returns in |
|---|---|
| conditional expectation as projection, the tower property | 12, 23, 43, 44 |
| Eve's law | 8, 18, 25, 26 |
| the multivariate normal, conditioning, the Schur complement | 12, 15, 25, 31, 39 |
| the precision matrix, conditional independence | 31, 32, 36 |
| regression to the mean, errors in variables | 12, 23, 35, 37 |
| the Jacobian | 7, 9, 22 |
| latent variables, mixtures | 22, 26, 31 |
| copulas, rank correlation | 16, 40 |
| exchangeability, de Finetti | 15, 16, 53, 57 |
| the Dirichlet and the multinomial | 14, 15, 26 |
