# Statistics, Built — Part 12: Least Squares

Part 12 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Part 11 put honest intervals on single
quantities. This part fits relationships.

It opens with Ceres: Piazzi finds it on 1 January 1801 and loses it in the Sun's glare, and Gauss predicts where it
will reappear. Then comes the Legendre (1805) vs Gauss (1809) priority dispute. From there the part covers:
- the principle, drawn as squares that shrink as the line turns, and the normal equations;
- why squares (Legendre's convenience, Gauss's derivation of the normal law, Gauss–Markov, geometry), and Boscovich's
  absolute errors;
- least squares as a projection (`NSpace`), the hat matrix and QR, and Pythagoras for R²;
- Gauss–Markov, proved, with a rival estimator losing; weighted least squares;
- normal theory, the coefficient table, the nested F-test and the ANOVA table, and robustness to skewed errors;
- Frisch–Waugh–Lovell, omitted-variable bias (with the World's clinic as Simpson's paradox);
- dummies, region factors, interactions, logs and splines, standardized coefficients, extrapolation;
- confidence, Working–Hotelling and prediction bands;
- collinearity, VIFs and confidence ellipses, the condition number;
- diagnostics: Anscombe's quartet, leverage, the influence probe, Cook's distance, residual and QQ plots;
- heteroskedasticity, White's sandwich and HC3;
- the regression fallacy: Galton's 1886 table, the World's fathers both ways, Secrist (1933), Bland & Altman.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- the families, heights, incomes and clinic come from the World (seed 1662);
- Anscombe's quartet and Galton's table come from the Museum;
- everything else is a seeded simulation.

**Built in this part:**
- **`statkit.ols`** ([`explainer/stats/kit/ols.py`](../../../explainer/stats/kit/ols.py)): QR-based fits with:
  - classical and HC0–HC3 covariances;
  - t, p and intervals, R² and adjusted R², nested F-tests;
  - confidence, Working–Hotelling and prediction bands;
  - leverage, studentized residuals and Cook's distance;
  - VIFs and a least-absolute-deviations line.

  Every output is checked against statsmodels in `tests/test_stats_kit_ols.py`.
- **The influence probe** (`InfluenceProbe` in `explainer/stats/viz.py`): drag one point and watch the fit, its
  leverage and Cook's distance respond.

The Coverage Board gains six rows: 95% intervals for the slope, R = 10,000. In the last four, x ~ Exp(1) and the
error SD ∝ x.

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| OLS slope, classical SE | child on mid-parent, n = 30 | 95.31% | kept |
| OLS slope, HC3 SE | child on mid-parent, n = 30 | 95.17% | kept |
| OLS slope, classical SE | n = 50 | 60.47% | broken |
| OLS slope, HC3 SE | n = 50 | 90.36% | broken |
| OLS slope, classical SE | n = 500 | 55.42% | broken |
| OLS slope, HC3 SE | n = 500 | 93.80% | broken (approaching 95% as n grows) |

## Build it

```bash
python -m videos.stats.stats12.compute         # once (about a minute; cached in .cache/stats12)
python tools/build.py stats12 -q l             # fast 480p preview
python tools/build.py stats12                  # 1080p30 -> renders/stats12.mp4
python tools/qa_scene.py stats12 Diagnostics
python tools/lecture_length.py stats12 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Ceres, lost and found | — |
| 1 | The principle | 30 families: b̂ = 0.53; Anscombe 3: LS slope 0.500 vs LAD 0.345 |
| 2 | Geometry | R² = 0.181 = r²; residual sums ≈ 10⁻¹⁵ |
| 3 | Gauss–Markov | slope SD 0.208 (OLS) vs 0.341 (end points); WLS 0.165 vs OLS 0.214 |
| 4 | Normal theory | true slope 0.703; coverage 95.3%; adding mother: F = 22.8, p = 6.5 × 10⁻⁶; R² 0.029 → 0.214; skewed errors: 95% coverage at n = 10, 30, 100 |
| 5 | Controlling for | FWL 0.4354 = 0.4354 (father alone 0.483); OVB: 0.110 vs truth 0.080, formula 0.11; clinic −0.112 vs +0.078 |
| 6 | Interpreting coefficients | son dummy +12.8 cm (R² 0.10 → 0.60); interaction 0.089 ± 0.120; regions F = 0.90, p = 0.52; log-income R² 0.013 / 0.123 / 0.153 |
| 7 | Bands | t = 2.05 vs √(2F) = 2.58; one son: 178.9, mean CI [177.9, 180.0], PI [167.8, 190.1] |
| 8 | Collinearity | VIF 1.0 vs 7.2; SE 0.12 vs 0.34; SE of the sum 0.15 vs 0.13 |
| 9 | Diagnostics | Anscombe: all 3.00 + 0.500x, R² 0.67; max Cook's D 1.39 (set 3); leverage 1 (set 4) |
| 10 | Uneven noise | funnel data: classical SE 0.095 vs HC3 0.267; the board rows above |
| 11 | The regression fallacy | Galton 1886: slope 0.646; World: fathers +1.94σ → children +0.77σ; children +1.94σ → fathers +0.76σ; a useless remedy "gains" 1.30 SD |
| 12 | Outro | — |

## Sources

- **The founding papers.**
  - A.-M. Legendre, *Nouvelles méthodes pour la détermination des orbites des comètes* (1805).
  - C. F. Gauss, *Theoria motus* (1809); *Theoria combinationis* (1821–23).
  - R. Boscovich (1757).
  - F. Galton, *J. Anthropol. Inst.* 15 (1886).
  - A. Markov (1912); A. Aitken, *Proc. R. Soc. Edinburgh* 55 (1935).
- **Regression in practice.**
  - R. Frisch & F. Waugh, *Econometrica* 1 (1933); M. Lovell, *JASA* 58 (1963).
  - H. Working & H. Hotelling, *JASA* 24 (1929).
  - F. Anscombe, *Am. Stat.* 27 (1973); D. Cook, *Technometrics* 19 (1977).
  - H. White, *Econometrica* 48 (1980); J. MacKinnon & H. White, *J. Econometrics* 29 (1985).
  - P. Huber, *Ann. Math. Stat.* 35 (1964); A. Hoerl & R. Kennard, *Technometrics* 12 (1970).
- **The regression fallacy and history.**
  - H. Secrist, *The Triumph of Mediocrity in Business* (1933), and H. Hotelling's review, *JASA* 28 (1933).
  - J. M. Bland & D. G. Altman, *BMJ* 308 (1994).
  - S. Stigler, *Ann. Stat.* 9 (1981); *The History of Statistics* (1986).
- **Textbooks.**
  - S. Weisberg, *Applied Linear Regression* (4th ed., 2014).
  - A. Gelman, J. Hill & A. Vehtari, *Regression and Other Stories* (2020).
  - G. Seber & A. Lee, *Linear Regression Analysis* (2nd ed., 2003).
  - J. Fox, *Applied Regression Analysis* (3rd ed., 2016).

## Problems and solutions

**1. Simple regression.**

*Solution.* The first normal equation, Σ(yᵢ − a − bxᵢ) = 0, gives a = ȳ − bx̄. Substitute into the second,
Σxᵢ(yᵢ − a − bxᵢ) = 0. Since Σx̄(yᵢ − ȳ − b(xᵢ − x̄)) = 0 as well, this becomes
Σ(xᵢ − x̄)(yᵢ − ȳ) = bΣ(xᵢ − x̄)².

Hence b̂ = Sxy/Sxx = r·√(Syy/Sxx) = r·s_y/s_x.

**2. The hat matrix.**

*Solution.*
- **Symmetric:** Hᵀ = X((XᵀX)⁻¹)ᵀXᵀ = H, since XᵀX is symmetric.
- **Idempotent:** H² = X(XᵀX)⁻¹XᵀX(XᵀX)⁻¹Xᵀ = H.
- **Trace:** tr H = tr((XᵀX)⁻¹XᵀX) = tr Iₚ = p, by tr(AB) = tr(BA) (Part 4).

**3. FWL.**

*Solution.* Let M₂ = I − X₂(X₂ᵀX₂)⁻¹X₂ᵀ. Multiply y = X₁β̂₁ + X₂β̂₂ + e by M₂. Since M₂X₂ = 0 and M₂e = e (e is
orthogonal to X₂), this gives M₂y = M₂X₁β̂₁ + e.

e is also orthogonal to X₁, hence to M₂X₁ = X₁ − X₂(⋯). So this is exactly the least squares decomposition of M₂y
on M₂X₁, and its coefficient is β̂₁.

**4. An omitted variable.**

*Solution.* y = β₁x₁ + β₂(0.5x₁ + u) + ε = (β₁ + 0.5β₂)x₁ + (β₂u + ε). If u is uncorrelated with x₁, the short
regression estimates β₁ + 0.5β₂: the bias is γδ with γ = β₂ and δ = 0.5.

**5. Standard errors along the line.**

*Solution.* SE(ŷ(x₀)) = s√(1/n + (x₀ − x̄)²/Sxx).
- At x₀ = 10: 2√(1/25) = 0.40.
- At x₀ = 20: 2√(0.04 + 100/100) = 2√1.04 = 2.04.
- Prediction at x₀ = 20: 2√(1 + 1.04) = 2.86.

**6. The VIF for two predictors.**

*Solution.* Regressing x₁ on x₂ gives R₁² = ρ², so VIF₁ = 1/(1 − ρ²). By symmetry VIF₂ is the same. At ρ = 0.95 the
VIF is 10.3.

## Where it comes back

| Idea | Returns in |
|---|---|
| ANOVA, orthogonal designs | 13 |
| GLMs: logistic and Poisson regression | 14, 24 |
| the linear model in depth (GLS, the Gauss–Markov theorem generalized) | 23 |
| mixed models, shrinkage | 25 |
| splines, smoothing | 29 |
| robust regression, Huber's loss | 30 |
| ridge, lasso, p > n | 32 |
| sandwich SEs for clusters and time | 17, 23 |
| causal regression, IV, DiD | 35, 36, 37 |
| the Coverage Board | every part; 65 |
