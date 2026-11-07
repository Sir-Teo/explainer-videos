# Statistics, Built — Part 49: Semiparametric Efficiency

Part 49 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the seventh part of Stage IV, the PhD core.

It opens with Stein's question of 1956: can the centre of a symmetric distribution be estimated as well without knowing
its shape? Stone (1975) and Bickel (1982) answered yes, and a simulation shows an adaptive estimator, never told the
law, near the bound 1/I_f under five laws. This fixed-trim KDE one-step is an illustration inspired by adaptive score estimation, not a proof of the exact asymptotic adaptation theorem. The part asks how well a finite-dimensional quantity can be estimated when
the rest of the model is infinite dimensional, and answers with one function, the efficient influence function. It
builds the theory in five steps:
- tangent spaces as the directions a model can move (drawn to scale for a 2 × 2 table under independence);
- pathwise derivatives, gradients, and the efficient influence function as a projection;
- the bound, as the hardest one-dimensional submodel, and a local minimax statement;
- worked influence functions: the mean, quantiles, the ATE and ATT (Hahn 1998), Robinson's partially linear model,
  Cox's partial likelihood;
- the nuisance tangent space and the efficient score, which explains adaptation.

It then uses the theory on:
- constructing efficient estimators: one-step, estimating equations, TMLE (with the NSW data);
- double robustness, as the product structure of the second-order remainder;
- the theory of double machine learning: Neyman orthogonality, cross-fitting, the product rate a + b > ½ for fixed order bounds, or a little-o product at equality;
- missing data under MAR (Robins, Rotnitzky & Zhao 1994), on the World's survey;
- higher-order influence functions, with the integrated squared density;
- the World test: plug-in, IPW, one-step and TMLE on Part 36's observational world (Board).

It keeps three promises:
- **Part 36** used AIPW and DML and called them doubly robust and root-n consistent with machine-learned nuisances.
  Chapters 5–8 prove both and say why.
- **Part 47** proved the convolution theorem for parametric models. Chapters 1–3 extend it to semiparametric models.
- **Part 48** found that a plugged-in nuisance costs its footprint. Chapters 4–5 turn the footprint into geometry: the
  efficient score is orthogonal to the nuisance tangent space.

**Built in this part:**
- **`statkit.semipar`** ([`explainer/stats/kit/semipar.py`](../../../explainer/stats/kit/semipar.py)), tested in
  `tests/test_stats_kit_semipar.py`:
  - L₂⁰(p) geometry on a finite sample space: inner products, projections, pathwise derivatives, numerical gradients,
    orthonormal bases, the bound; the independence model's tangent space;
  - Fisher informations for location; symmetric laws; Hodges–Lehmann; Stone's adaptive one-step estimator;
  - the ATE by plug-in, IPW, one-step and TMLE with influence-function SEs; the ATT one-step;
  - the product-rate experiment (nuisances corrupted at n^{−a}, n^{−b});
  - a mean under MAR by complete cases, IPW, regression and AIPW;
  - the integrated squared density: plug-in, one-step and the second-order U-statistic.
- **The tangent-space picture** (`TangentSpace` in `explainer/stats/viz.py`), the part's instrument: an oblique 3D view
  of L₂⁰(P) with the model's tangent plane, nuisance lines, score and gradient arrows, and their orthogonal projections.

**Data.**
- From the Museum: the NSW job-training data (LaLonde 1986; Dehejia & Wahba 1999).
- From the World: the survey of Part 41 (income missing at random) and Part 36's observational world (doctors choose, a little more gently than in Part 36).
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains five rows, all nominal 90%, on the World (doctors choose, n = 2,000):

| Method | Achieved ± MCSE | Verdict |
|---|---|---|
| plug-in, \ $k$-NN outcome models | 3.33% ± 1.04% | broken |
| IPW, \ logistic propensity | 96.33% ± 1.09% | conservative |
| one-step, \ $k$-NN $+$ logistic, \ cross-fitted | 91.00% ± 1.66% | kept |
| TMLE, \ $k$-NN $+$ logistic, \ cross-fitted | 90.33% ± 1.71% | kept |
| one-step, \ $k$-NN for both | 71.33% ± 2.62% | broken |

Each row uses 300 independent samples drawn with replacement from the fixed eligible World pool. The target is the pool ATE, −9.9303, rather than each sample's own effect. Preprocessing is fitted within training folds. The plug-in shares a one-step reference width to isolate bias; the IPW SE treats fitted weights as fixed and is not a general fitted-model interval guarantee.

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats49.compute   # once (about fifteen minutes)
python tools/build.py stats49 -q l                         # fast 480p preview
python tools/build.py stats49                              # 1080p30 -> renders/stats49.mp4
python tools/qa_scene.py stats49 Pathwise
python tools/lecture_length.py stats49 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Adaptive estimation | n·Var at n = 400 (t₃): mean 2.96, median 1.87, HL 1.61, adaptive 1.68, bound 1.5; mixture: adaptive 1.83 vs bound 1.38 |
| 1 | Tangent spaces | 2 × 2 table under independence: L₂⁰ has 3 dimensions, the tangent space 2 |
| 2 | Pathwise derivatives | ‖φ‖² = 0.1476, ‖φ*‖² = 0.0972; simulated n·Var 0.1448 and 0.0957 |
| 3 | Bounds | least favourable direction 28°; known margin: 0.0756; ATE bound 4.70, one-step 4.53, Hajek 6.81, HT 13.75 |
| 4 | Worked influence functions | the mean, quantiles, the ATE and ATT (Hahn 1998), the PLR (Robinson 1988), Cox |
| 5 | The efficient score | adaptation: odd score ⟂ even nuisance scores; heteroskedastic PLR: orthogonal but not efficient |
| 6 | Efficient estimators | √n·bias at n = 16,000: plug-in 6.94, one-step -0.32, TMLE -0.26; NSW: 1,794 (671) vs 1,622 (656); PSID ATT 1,218 (889; refitted bootstrap) |
| 7 | Double robustness | one-step bias: +0.004, -0.004, +0.002, +0.198 |
| 8 | DML theory | nonzero limiting √n·bias at a + b = ½; centred inference needs a little-o product; ⅛ + ⅛: -6.2 → -16.2; 5-NN: coverage 82.5% reused vs 87.0% cross-fitted |
| 9 | Missing data | survey: complete cases +0.0252, AIPW +0.0050 (SE 0.0182) |
| 10 | Higher order | √n·bias at h = 0.05: plug-in +0.25, one-step -0.56, U-statistic -0.02 (SD 0.218 vs 0.222) |
| 11 | The World test | coverage: plug-in 3.3%, IPW 96.3%, one-step 91.0%, TMLE 90.3%, k-NN both 71.3% |
| 12 | Outro | — |

## QA checkpoint

All thirteen scenes and six solutions have been read; fourteen focused checks pass. Scientific corrections are recorded in the [source review](../../../docs/qa/evidence/stats49-polish-20261107/source-review.md). All eleven inputs have now been regenerated and the numerical summary reconciled. The NSW observational ATT SE is 888.61 from 399 stratified resamples refitting both nuisances (the naive IF SE was 870.69). Exact Gaussian-kernel expectations and quadrature product remainders are retained alongside their simulations. Visual review and bilingual/listening/master gates remain open.

## Sources

- **Adaptation and the bound.**
  - C. Stein, *Proc. Third Berkeley Symp.* 1 (1956); C. Stone, *Ann. Stat.* 3 (1975); P. Bickel, *Ann. Stat.* 10 (1982).
  - Y. Koshevnik & B. Levit, *Theory Probab. Appl.* 21 (1976); J. Pfanzagl, *Contributions to a General Asymptotic
    Statistical Theory* (1982); A. Schick, *Ann. Stat.* 14 (1986).
  - B. Efron, *JASA* 72 (1977); J. Begun, W. Hall, W.-M. Huang & J. Wellner, *Ann. Stat.* 11 (1983).
- **Influence functions in causal inference and missing data.**
  - J. Robins, A. Rotnitzky & L. P. Zhao, *JASA* 89 (1994); J. Hahn, *Econometrica* 66 (1998).
  - P. Robinson, *Econometrica* 56 (1988); J. Neyman, in *Probability and Statistics: the Harald Cramér Volume*
    (1959).
  - J. Kang & J. Schafer, *Stat. Sci.* 22 (2007).
- **Estimators.**
  - M. van der Laan & D. Rubin, *Int. J. Biostat.* 2 (2006); V. Chernozhukov, D. Chetverikov, M. Demirer, E. Duflo,
    C. Hansen, W. Newey & J. Robins, *Econometrics J.* 21 (2018).
  - J. Robins, L. Li, E. Tchetgen Tchetgen & A. van der Vaart, in *Probability and Statistics: Essays in Honor of
    David A. Freedman* (2008); P. Bickel & Y. Ritov, *Sankhyā A* 50 (1988).
- **Data.** R. LaLonde, *Am. Econ. Rev.* 76 (1986); R. Dehejia & S. Wahba, *JASA* 94 (1999).
- **Books and reviews.**
  - P. Bickel, C. Klaassen, Y. Ritov & J. Wellner, *Efficient and Adaptive Estimation for Semiparametric Models* (1993).
  - A. Tsiatis, *Semiparametric Theory and Missing Data* (2006); A. van der Vaart, *Asymptotic Statistics*, ch. 25
    (1998).
  - M. van der Laan & S. Rose, *Targeted Learning* (2011); E. Kennedy, *Semiparametric doubly robust targeted double
    machine learning: a review* (2022).

## Problems and solutions

1. **The independence projection.**
   - A path p_t = p(1 + ts) stays in the independence model to first order iff s(x₁, x₂) = a(x₁) + b(x₂): the
     log-density of a product law is log p₁(x₁) + log p₂(x₂), and its derivatives are exactly such sums.
   - The projection of φ = 1{x = (1,1)} − p₁₁ onto that space is the influence function of p̂₁q̂₁:
     q₁(1{x₁ = 1} − p₁) + p₁(1{x₂ = 1} − q₁). (The residual is orthogonal to every a(x₁) and b(x₂) because under
     independence E[1{x₁ = 1}1{x₂ = 1} | x₁] = 1{x₁ = 1} q₁.)
   - Its variance is q₁²p₁(1 − p₁) + p₁²q₁(1 − q₁) = 0.0972 at p₁ = 0.3, q₁ = 0.6.
2. **Two influence functions.**
   - The mean: d/dt ∫x p(1 + ts) = ∫x s p = E[(X − μ)s], so φ = x − μ.
   - The quantile: differentiate F_t(ξ_t) = p along p(1 + ts): E[1{X ≤ ξ}s] + f(ξ)ξ̇ = 0, so
     ξ̇ = −E[1{X ≤ ξ}s]/f(ξ) = E[((p − 1{X ≤ ξ})/f(ξ)) s], and φ = (p − 1{x ≤ ξ_p})/f(ξ_p).
3. **The ATE.**
   - Differentiate ψ = ∫∫ y [p(y | 1, x) − p(y | 0, x)] dy p(x) dx along a nonparametric path, factor the score into its
     X, T | X and Y | T, X parts, and collect terms: φ* = μ₁ − μ₀ − ψ + T(Y − μ₁)/e − (1 − T)(Y − μ₀)/(1 − e).
   - The three pieces are orthogonal: Var(μ₁ − μ₀) + E[T(Y − μ₁)²/e²] + E[(1 − T)(Y − μ₀)²/(1 − e)²]
     = Var τ(X) + E[σ₁²/e + σ₀²/(1 − e)].
4. **The one-step's bias.**
   - E[μ̂₁ + T(Y − μ̂₁)/ê] − Eμ₁ = E[(μ̂₁ − μ₁)(1 − e/ê)] = E[(e − ê)(μ₁ − μ̂₁)/ê].
   - Similarly for the controls, E[μ̂₀ + (1 − T)(Y − μ̂₀)/(1 − ê)] − Eμ₀ = E[(ê − e)(μ₀ − μ̂₀)/(1 − ê)].
   - Subtract: both terms are products of a propensity error and an outcome error.
5. **Orthogonality behind adaptation.**
   - With f symmetric, f′ is odd, so −f′/f is odd. For even h, E[−(f′/f)(ε) h(ε)] = −∫ f′(u) h(u) du = 0, because the
     integrand is odd.
   - So the location score is orthogonal to the nuisance tangent space of symmetric shape changes, the efficient score
     is the full score, and the efficient information is I_f.
6. **TMLE solves the efficient equation.**
   - The update μ̂*_t = μ̂_t + ε̂H_t with ε̂ the least-squares coefficient of Y − μ̂_T on H = T/ê − (1 − T)/(1 − ê)
     makes Σ H_i(Y_i − μ̂*_{T_i}) = 0.
   - With ψ̂ = mean(μ̂*₁ − μ̂*₀), P_nφ* = mean(μ̂*₁ − μ̂*₀ − ψ̂) + mean(H(Y − μ̂*_T)) = 0 + 0.

## Glossary

- **The geometry.**
  - Model; submodel; score; tangent space; L₂⁰(P); closure: the directions a model can move.
  - Pathwise differentiability; gradient; influence function; canonical gradient; efficient influence function:
    derivatives as functions.
  - Regular estimator; asymptotically linear; convolution theorem; least favourable submodel; efficiency bound:
    how well anyone can do.
  - Nuisance parameter; nuisance tangent space; efficient score; efficient information; adaptation: projecting the
    nuisance away.
- **The estimators.**
  - Plug-in; von Mises expansion; second-order remainder; one-step; estimating equation; TMLE; clever covariate:
    removing the first-order bias.
  - Double robustness; Neyman orthogonality; cross-fitting; product rate; DML1, DML2: machine-learned nuisances.
  - MAR; IPW; augmentation; AIPW; Horvitz–Thompson; Hajek: missing data.
  - Higher-order influence function; U-statistic; integrated squared density; minimax rate: beyond the first order.

## Where it comes back

- **Part 50**: minimax rates when root-n is impossible.
- **Part 52**: the debiased lasso and high-dimensional inference use the same one-step correction.
- **Part 53**: Bernstein–von Mises theorems for semiparametric models.
- **Part 60**: double robustness under distribution shift.
- **Part 62**: proximal causal inference, policy learning and efficient estimators on the frontiers.
