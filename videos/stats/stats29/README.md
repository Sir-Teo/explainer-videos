# Statistics, Built — Part 29: Smoothing

Part 29 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the ninth part of Stage III, Master's. Part 28 chose among models with a fixed
number of parameters. This part estimates whole curves, densities and regression functions, and asks how fast it can
be done:
- histograms and kernel density estimates, their bias, variance and rates; bandwidth selection; the curse of
  dimensionality;
- local polynomials, smoothing splines (with GCV and REML), reproducing kernels and Gaussian processes, wavelets, and
  additive models;
- honest intervals for curves (robust bias correction) and estimation under shape constraints.

Its instrument is the spline spectrum (`SplineSpectrum`): the Demmler–Reinsch basis of a smoothing spline with the
shrinkage factor 1/(1 + λdⱼ) on each component. Its kit is `statkit.smooth`.

It opens with Old Faithful: 272 eruptions logged in August 1978 and 1979, 36% of them under three minutes. Shifted or
halved histogram bins change the picture. Kernel estimates have 12, 3, 2 and 1 modes at h = 0.05, 0.1, 0.25 and 1.
Silverman's critical bandwidths are h₁ = 0.831, h₂ = 0.127 and h₃ = 0.086. His smoothed-bootstrap test (500
resamples):

| H₀ | Critical h | p-value | Verdict |
|---|---|---|---|
| at most 1 mode | 0.831 | 0.00 | rejected |
| at most 2 modes | 0.127 | 0.50 | not rejected |
| at most 3 modes | 0.086 | 0.93 | not rejected |

Two humps, short and long eruptions; the third is noise.

From there the part covers:
- **Histograms.**
  - The upgrade of Part 1's bin rules: exact MISE from bin probabilities; AMISE = 1/(nh) + h²R(f′)/12;
    h* = (6/(nR(f′)))^{1/3}, Scott's 3.49σn^{−1/3}.
  - The truth is a two-humped stand-in for Old Faithful, 0.35 N(2, 0.27²) + 0.65 N(4.3, 0.42²). Its exact MISE is
    minimized at h = 0.339, 0.153 and 0.071 for n = 100, 1,000 and 10,000 (the formula gives 0.329, 0.153, 0.071).
  - The best MISE falls with slope −0.647 in log n (theory −2/3).
- **Kernel estimates.**
  - Bias ½h²μ₂f″ and variance f R(K)/(nh), derived. AMISE, h* ∝ n^{−1/5}, rate n^{−4/5}.
  - Marron & Wand's exact MISE: best h = 0.179, 0.106 and 0.066 (AMISE formula 0.162, 0.102, 0.065).
  - The best MISE falls with slope −0.759, on its way to −4/5. It is 2.5, 3.2 and 4.2 times smaller than the best
    histogram at n = 100, 1,000 and 10,000.
  - Epanechnikov's kernel by the calculus of variations. Efficiencies: biweight 0.994, triangular 0.986, Gaussian
    0.951, uniform 0.930.
- **Bandwidths.**
  - On Old Faithful: normal reference 0.394, Silverman 0.335, Sheather–Jones 0.166 (2 modes), LSCV 0.103 (3 modes).
  - 300 samples of n = 200 from the stand-in (h_MISE = 0.154):

    | Selector | ĥ/h_MISE: median (10%–90%) | Mean ISE |
    |---|---|---|
    | normal reference | 2.77 (2.66–2.87) | 0.0511 |
    | Silverman | 2.35 (2.26–2.44) | 0.0359 |
    | LSCV | 1.05 (0.72–1.20) | 0.0115 |
    | Sheather–Jones | 1.23 (1.17–1.30) | 0.0107 |

    The best possible MISE is 0.0099.
- **The curse of dimensionality.**
  - The rate n^{−4/(4+d)}. Silverman's table, reproduced exactly: the sample size for relative MSE 0.1 at the centre
    of a d-variate standard normal.

    | d | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
    |---|---|---|---|---|---|---|---|---|---|---|
    | n | 4 | 19 | 67 | 223 | 768 | 2,789 | 10,731 | 43,736 | 187,503 | 841,616 |

  - The inscribed ball holds 78.5% of the square, 52.4% of the cube and 0.25% of the 10-cube.
  - For 1,000 uniform points, the nearest neighbour is at median distance 0.0004 in 1-D, 0.48 in 10-D and 2.12 in
    50-D; the nearest-to-farthest ratio reaches 0.59 at 50-D.
  - Norms concentrate: ‖X‖ ≈ √d ± 0.7.
- **Local polynomials.**
  - Nadaraya–Watson vs local linear (Fan 1992): the equivalent kernels at the boundary.
  - On the noise-free line y = 2x, NW gives 0.15 at 0 and 1.85 at 1.
  - Old Faithful's waiting time after an eruption: about 33.5 + 10.7 × length.
  - The motorcycle crash (133 readings): NW and local linear differ by up to 14 g on the steep descent.
  - LOESS and its robustness iterations (Cleveland 1979).
- **Smoothing splines.**
  - The Reinsch–Schoenberg theorem, proved; the Reinsch form (I + λK)⁻¹y. Statkit agrees with SciPy's
    `make_smoothing_spline` to 10⁻¹⁰.
  - Motorcycle fits at 4, 8, 12 and 25 df.
  - The Demmler–Reinsch spectrum (eigenvalues growing roughly like the fourth power of the index); ridge regression
    in that basis.
- **Choosing λ.**
  - GCV (Craven & Wahba 1979); splines as mixed models; REML (Wahba 1985); Wahba's Bayesian bands (Nychka 1988).
  - Motorcycle: GCV chooses df 12.4, REML df 14.4 (on the 94 distinct times); residual SD 22.6 g.
  - 300 simulated data sets (n = 100, noise SD 0.3):

    | Criterion | Chosen df: 10% / median / 90% | Mean error | Worst 5% |
    |---|---|---|---|
    | oracle | 9.6 / 11.0 / 12.7 | 0.0082 | 0.0178 |
    | GCV | 9.6 / 11.0 / 14.6 | 0.0098 | 0.0220 |
    | REML | 10.3 / 11.0 / 12.3 | 0.0089 | 0.0187 |

- **Kernels.**
  - RKHS, the reproducing property, the representer theorem (Kimeldorf & Wahba 1970), proved; kernel ridge
    regression.
  - Motorcycle fits with Gaussian kernels: 7.4 df at ℓ = 6.5 ms; 17.8 df at 2.0 ms (the GP band, σ̂ = 22.9 g); 56 df at
    0.65 ms with small λ.
  - The Gaussian-process reading: the posterior mean equals the kernel ridge fit.
- **Wavelets.**
  - Haar and Daubechies-4 by Mallat's pyramid; the MAD noise estimate; VisuShrink σ√(2 log n); SureShrink.
  - The maximum of n normals against √(2 log n): medians 1.83 / 2.66 / 3.40 / 3.99 / 4.52 for n = 10 … 100,000.
  - Donoho–Johnstone signals, n = 1,024, SNR 7, MSE per point:

    | Signal | Noisy | VisuShrink | SureShrink | GCV spline |
    |---|---|---|---|---|
    | blocks | 0.99 | 1.32 | 0.40 | 0.71 (356 df) |
    | doppler | 0.96 | 1.21 | 0.43 | 0.35 |
    | heavisine | 1.01 | 0.40 | 0.10 | 0.11 |
    | bumps | 1.01 | 2.01 | 0.62 | 0.72 |

- **Additive models.**
  - Backfitting (Friedman & Stuetzle 1981; Buja, Hastie & Tibshirani 1989); concurvity.
  - New York's ozone in 1973 (cube root, 111 days), with 4 df each for temperature, wind and solar radiation. The fit
    converges in 17 sweeps and gives R² 0.759 against 0.681 for the linear model. 10-fold CV error is 0.241 vs 0.270,
    11% lower.
- **Inference for curves.**
  - Bias/SE does not vanish at h* ∝ n^{−1/5}. At the stand-in's long-eruption mode (x = 4.3, n = 300, pointwise
    MSE-optimal h = 0.137), the estimates average 0.587 against the truth 0.617. That bias of −0.031 (theory −0.033)
    is 0.58 SD.
  - Undersmoothing; Hall (1992); robust bias correction (Calonico, Cattaneo & Farrell 2018) with the fourth-order
    kernel M = K − ½K″.
  - Simultaneous bands (Bickel & Rosenblatt 1973).
- **Shape constraints.**
  - Isotonic regression by PAVA (18 steps for 60 readings); Grenander's estimator.
  - At x = 1 for exponential data, SD × n^{1/3} = 0.37, 0.41 and 0.39 for n = 100, 1,000 and 10,000. Chernoff's
    limit is 0.42. The kernel estimate's SD × n^{2/5} = 0.20, 0.26 and 0.28.
  - Log-concave MLEs.

Data:
- Old Faithful (Azzalini & Bowman 1990; Härdle 1991), the motorcycle crash test (Schmidt, Mattern & Schüler 1981;
  Silverman 1985) and New York's 1973 air quality (Chambers, Cleveland, Kleiner & Tukey 1983) are the Museum's, via
  R's `datasets` and `MASS`;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.smooth`** ([`explainer/stats/kit/smooth.py`](../../../explainer/stats/kit/smooth.py)), checked in
  `tests/test_stats_kit_smooth.py`:
  - **Kernels and histograms:**
    - kernels with R(K), μ₂ and efficiencies;
    - the histogram's exact MISE;
    - `NormalMixture`, with exact R(f^{(r)}) and Marron–Wand MISE.
  - **Bandwidths:** normal reference, Silverman, closed-form LSCV, the Sheather–Jones plug-in.
  - **Modes and dimension:** Silverman's critical bandwidths and mode test; Silverman's table.
  - **Regression smoothers:** local polynomials and LOESS (with robustness); `SmoothingSpline` (Reinsch form,
    weights and ties, the smoother matrix, df, GCV, REML, the Demmler–Reinsch basis, evaluation); kernel ridge.
  - **Wavelets:** Haar and D4 DWT/IDWT, the MAD σ, VisuShrink and SureShrink, Donoho–Johnstone test signals.
  - **The rest:** backfitting; conventional and robust bias-corrected KDE intervals; the Grenander estimator.
- **The Museum** gains `faithful()`, `mcycle()` and `airquality()`.
- **The spline spectrum** (`SplineSpectrum` in `explainer/stats/viz.py`): the first k Demmler–Reinsch basis curves
  and their shrinkage bars; `bars(lam)` turns the dial.

The Coverage Board gains three rows. Pointwise 95% intervals for f(4.3), at the stand-in's long-eruption mode, over
2,000 samples of n = 300:

| Method | Reps | Achieved | Mean width | Verdict |
|---|---|---|---|---|
| conventional, at the MSE-optimal h | 2,000 | 91.0% | 0.214 | broken |
| undersmoothed, h·n^{−1/10} | 2,000 | 95.1% | 0.309 | kept |
| robust bias-corrected | 2,000 | 95.4% | 0.298 | kept |

## Build it

```bash
python -m videos.stats.stats29.compute         # once (about two minutes)
python tools/build.py stats29 -q l             # fast 480p preview
python tools/build.py stats29                  # 1080p30 -> renders/stats29.mp4
python tools/qa_scene.py stats29 Splines
python tools/lecture_length.py stats29 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Old Faithful | h₁ 0.83, h₂ 0.13; p = 0.00 / 0.50 / 0.93 |
| 1 | Histograms as estimators | h* 0.34 / 0.15 / 0.07; slope −0.65 |
| 2 | Kernel density estimates | slope −0.76; Gaussian efficiency 0.951 |
| 3 | Choosing the bandwidth | SJ 0.166, LSCV 0.103; NR 2.8× too wide |
| 4 | The curse of dimensionality | 4 → 841,616 points from 1-D to 10-D |
| 5 | Local polynomials | NW 0.15 at the boundary; 14 g apart on the crash |
| 6 | Smoothing splines | df 4 / 8 / 12 / 25; the spectrum |
| 7 | Choosing λ | GCV df 12.4, REML 14.4; REML's worst 5% 0.0187 vs 0.0220 |
| 8 | Kernels and the representer theorem | df 7 / 18 / 56; GP band |
| 9 | Wavelets | SureShrink 0.40 vs spline 0.71 on blocks |
| 10 | Additive models | R² 0.76 vs 0.68; CV −11% |
| 11 | Inference for curves | 91.0% vs 95.4% (RBC) |
| 12 | Shape constraints | SD·n^{1/3} ≈ 0.39 vs Chernoff 0.42 |
| 13 | Outro | — |

## Sources

- **History and data.**
  - A. Azzalini & A. Bowman, *Applied Statistics* 39 (1990); W. Härdle, *Smoothing Techniques* (1991).
  - B. Silverman, *JRSS B* 43 (1981) and 47 (1985); G. Schmidt, R. Mattern & F. Schüler (1981).
  - J. Chambers, W. Cleveland, B. Kleiner & P. Tukey, *Graphical Methods for Data Analysis* (1983).
- **Densities.**
  - M. Rosenblatt, *Ann. Math. Stat.* 27 (1956); E. Parzen, *Ann. Math. Stat.* 33 (1962); V. Epanechnikov, *Theory
    Prob. Appl.* 14 (1969).
  - D. Scott, *Biometrika* 66 (1979); H. Sturges, *JASA* 21 (1926).
  - J. S. Marron & M. Wand, *Ann. Stat.* 20 (1992); P. Hall, *Ann. Stat.* 20 (1992).
- **Bandwidths.** M. Rudemo, *Scand. J. Stat.* 9 (1982); A. Bowman, *Biometrika* 71 (1984); S. Sheather & M. C. Jones,
  *JRSS B* 53 (1991); M. C. Jones, J. S. Marron & S. Sheather, *JASA* 91 (1996); P. Chaudhuri & J. S. Marron, *JASA* 94
  (1999).
- **Dimension.** R. Bellman, *Adaptive Control Processes* (1961); C. Stone, *Ann. Stat.* 8 (1980) and 13 (1985);
  K. Beyer, J. Goldstein, R. Ramakrishnan & U. Shaft, *ICDT* (1999).
- **Regression.**
  - E. Nadaraya, *Theory Prob. Appl.* 9 (1964); G. Watson, *Sankhyā A* 26 (1964); W. Cleveland, *JASA* 74 (1979).
  - J. Fan, *JASA* 87 (1992); J. Fan & I. Gijbels, *Local Polynomial Modelling* (1996).
- **Splines and kernels.**
  - I. Schoenberg, *PNAS* 52 (1964); C. Reinsch, *Numer. Math.* 10 (1967); A. Demmler & C. Reinsch, *Numer. Math.*
    24 (1975).
  - P. Craven & G. Wahba, *Numer. Math.* 31 (1979); G. Wahba, *JRSS B* 45 (1983), *Ann. Stat.* 13 (1985); D. Nychka,
    *JASA* 83 (1988).
  - T. Speed, *Stat. Sci.* 6 (1991); P. Reiss & R. T. Ogden, *JRSS B* 71 (2009).
  - N. Aronszajn, *Trans. AMS* 68 (1950); G. Kimeldorf & G. Wahba, *Ann. Math. Stat.* 41 (1970).
- **Wavelets.** A. Haar, *Math. Ann.* 69 (1910); I. Daubechies, *Comm. Pure Appl. Math.* 41 (1988); S. Mallat, *IEEE
  PAMI* 11 (1989); D. Donoho & I. Johnstone, *Biometrika* 81 (1994), *JASA* 90 (1995).
- **Additive models.**
  - J. Friedman & W. Stuetzle, *JASA* 76 (1981); A. Buja, T. Hastie & R. Tibshirani, *Ann. Stat.* 17 (1989).
  - T. Hastie & R. Tibshirani, *Generalized Additive Models* (1990); S. Wood, *JRSS B* 73 (2011).
- **Inference.** P. Bickel & M. Rosenblatt, *Ann. Stat.* 1 (1973); S. Calonico, M. Cattaneo & M. Farrell, *JASA* 113
  (2018).
- **Shape.**
  - M. Ayer, H. Brunk, G. Ewing, W. Reid & E. Silverman, *Ann. Math. Stat.* 26 (1955); U. Grenander, *Skand.
    Aktuarietidskr.* 39 (1956).
  - B. L. S. Prakasa Rao, *Sankhyā A* 31 (1969); R. Barlow, D. Bartholomew, J. Bremner & H. Brunk, *Statistical
    Inference under Order Restrictions* (1972).
  - G. Walther, *JASA* 97 (2002); M. Cule, R. Samworth & M. Stewart, *JRSS B* 72 (2010).
- **Books.**
  - B. Silverman, *Density Estimation for Statistics and Data Analysis* (1986).
  - M. Wand & M. C. Jones, *Kernel Smoothing* (1995).
  - P. Green & B. Silverman, *Nonparametric Regression and Generalized Linear Models* (1994).
  - G. Wahba, *Spline Models for Observational Data* (1990).
  - L. Wasserman, *All of Nonparametric Statistics* (2006).
  - S. Wood, *Generalized Additive Models* (2nd ed., 2017).

## Problems and solutions

**1. The histogram's bias and optimal bin.**

*Solution.* For x in bin B_j = [t_j, t_j + h), E f̂(x) = p_j/h with
p_j = ∫_{B_j} f = h f(t_j) + ½h² f′(t_j) + O(h³). So the bias at x is f′(t_j)(h/2 − (x − t_j)) + O(h²). Squaring and
integrating over the bin gives f′(t_j)² h³/12 per bin, so the integrated squared bias is (h²/12) R(f′) + o(h²). The
variance is p_j(1 − p_j)/(nh²) ≈ f(x)/(nh), so the integrated variance is about 1/(nh). Minimizing
1/(nh) + h²R(f′)/12 gives h* = (6/(nR(f′)))^{1/3}. For N(0, σ²), R(f′) = 1/(4√π σ³), so
h* = (24√π)^{1/3} σ n^{−1/3} = 3.49 σ n^{−1/3}.

**2. The kernel estimate's bias and variance.**

*Solution.* E f̂_h(x) = ∫K(u) f(x − hu) du. Expand f(x − hu) = f − huf′ + ½h²u²f″ + o(h²). Then ∫K = 1 and ∫uK = 0
give bias ½h²μ₂f″(x) + o(h²). The variance is n⁻¹ Var(h⁻¹K((x − X)/h)), and
E h⁻²K²((x − X)/h) = h⁻¹ ∫K²(u) f(x − hu) du = f(x)R(K)/h + O(1). So Var = f(x)R(K)/(nh) + O(1/n). Integrating,
AMISE = R(K)/(nh) + ¼h⁴μ₂²R(f″). Its minimizer is h* = (R(K)/(μ₂²R(f″)n))^{1/5}, and the minimum is
(5/4)(μ₂R(K)²)^{2/5}R(f″)^{1/5} n^{−4/5}.

**3. Epanechnikov's kernel.**

*Solution.* The functional μ₂^{1/2}R(K) is invariant to K ↦ K(u/a)/a, so fix μ₂ = 1/5 and minimize ∫K²
subject to ∫K = 1, ∫u²K = 1/5 and K ≥ 0. For the candidate K₀ = ¾(1 − u²)₊ and any admissible K, write K = K₀ + δ with
∫δ = 0 and ∫u²δ = 0. Then ∫K² = ∫K₀² + 2∫K₀δ + ∫δ². On |u| ≤ 1, K₀ = ¾ − ¾u², so ∫_{|u|≤1} K₀δ = −∫_{|u|>1} (¾ − ¾u²)δ.
Outside, δ = K ≥ 0 and ¾ − ¾u² < 0, so this term is ≥ 0. Hence ∫K² ≥ ∫K₀², with equality only at K = K₀.

**4. The Reinsch–Schoenberg theorem.**

*Solution.* Let s be the natural cubic spline with s(x_i) = g(x_i), and h = g − s, so h(x_i) = 0. Integrating by
parts on [x₁, x_n], ∫s″h″ = [s″h′] − ∫s‴h′. The boundary term is zero since s″(x₁) = s″(x_n) = 0. On each
(x_i, x_{i+1}), s‴ is a constant c_i, so ∫s‴h′ = Σ c_i (h(x_{i+1}) − h(x_i)) = 0. Outside [x₁, x_n], s is linear, so
s″ = 0 there. Thus ∫g″² = ∫s″² + ∫h″² ≥ ∫s″², with the same fit to the data. The penalized criterion is therefore
minimized by a natural cubic spline, with equality only if h is linear and vanishes at the x_i, i.e. h = 0.

**5. The representer theorem.**

*Solution.* Write f = f∥ + f⊥ with f∥ ∈ span{k(x_i, ·)} and f⊥ orthogonal to it. By the reproducing property,
f(x_i) = ⟨f, k(x_i, ·)⟩ = f∥(x_i), so the loss depends only on f∥. Meanwhile ‖f‖² = ‖f∥‖² + ‖f⊥‖², so the minimizer
has f⊥ = 0 and f = Σα_j k(x_j, ·). Substituting gives ‖y − Kα‖² + λα′Kα. Setting the gradient
−2K(y − Kα) + 2λKα to zero gives K((K + λI)α − y) = 0, solved by α = (K + λI)⁻¹y.

**6. The maximum of n normals.**

*Solution.* Let M = max|Z_i|. For t > 0, Jensen gives e^{tEM} ≤ E e^{tM} ≤ Σ E e^{t|Z_i|} ≤ 2n e^{t²/2}. So
EM ≤ log(2n)/t + t/2, and t = √(2 log 2n) gives EM ≤ √(2 log(2n)). A matching lower bound shows
EM ~ √(2 log n), which is why the universal threshold σ√(2 log n) kills pure noise with probability → 1.

## Glossary

- **Density estimate; ISE; MISE; AMISE**: an estimate of a whole density; its integrated squared error for one sample;
  the average over samples; the leading terms.
- **Histogram; bin width; bin origin; Scott's and Freedman–Diaconis rules**: the step estimate and its tuning.
- **Kernel; bandwidth; μ₂(K); R(K); Epanechnikov kernel; efficiency**: the bump, its width, its variance and
  roughness, the optimal shape, and the sample-size price of others.
- **Normal reference; Silverman's rule; LSCV; plug-in (Sheather–Jones); ψ_r functionals; pilot bandwidth**: ways to
  choose h.
- **Mode; critical bandwidth; Silverman's test; smoothed bootstrap**: counting humps, and testing how many there are.
- **Curse of dimensionality; n^{−4/(4+d)}; Silverman's table**: the rate's decay in d.
- **Nadaraya–Watson; local linear; local polynomial; equivalent kernel; boundary and design bias; LOESS; tricube;
  bisquare robustness**: local regression and its parts.
- **Smoothing spline; natural cubic spline; Reinsch form; smoother matrix; effective df; Demmler–Reinsch basis**: the
  penalized fit, its form, and its spectrum.
- **GCV; REML/GML; splines as mixed models; Bayesian bands**: choosing λ, and the posterior view.
- **RKHS; reproducing property; representer theorem; kernel ridge regression; Gaussian process**: the general
  penalized framework and its Bayesian twin.
- **Wavelet; multiresolution; DWT; soft and hard thresholding; MAD σ; VisuShrink; SureShrink; universal threshold**:
  sparse representations and denoising by thresholding.
- **Additive model; GAM; backfitting; partial residual; concurvity**: sums of one-dimensional smooths.
- **Pointwise vs simultaneous bands; undersmoothing; bias correction; robust bias-corrected (RBC) intervals;
  fourth-order kernel**: honest inference for curves.
- **Isotonic regression; PAVA; Grenander estimator; least concave majorant; Chernoff's distribution; log-concave
  MLE**: shape-constrained estimation.

## Where it comes back

| Idea | Returns in |
|---|---|
| robust smoothing; influence | 30 |
| sparse additive models | 32 |
| conformal bands for smoothers | 34 |
| local linear at a cutoff (RD), robust bias correction | 37 |
| Gaussian processes, kriging | 39 |
| hazard smoothing; monotone hazards | 40 |
| minimax rates (Le Cam, Assouad, Fano) | 50 |
| posterior contraction for curves | 53 |
| the Coverage Board | every part; 65 |
