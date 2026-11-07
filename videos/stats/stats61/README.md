# Statistics, Built — Part 61: Optimal Transport in Statistics

Part 61 of [the 65-part course](../README.md), covering Kantorovich duality, Wasserstein geometry, empirical rates, Sinkhorn, transport maps, barycenters, multivariate ranks, gradient flows and generative models.

Monge's 1781 earthworks motivate the hook. Monotone pairing is optimal for convex displacement costs on a line; plain-distance optima need not be unique. A general no-crossing slogan does not replace cyclic monotonicity or its assumptions. For uniform equal-size discrete laws an optimal permutation plan exists, but other optima may be mixtures.

## Checked computation and example scope

[Audited local kernels](checked.py) are used by this part; [statkit.ot](../../../explainer/stats/kit/ot.py) retains its educational implementations. The instrument is TransportFlow.

- **LP:** check solver success, both marginals, dual feasibility and gap. The 6-by-7 example has 12 positive entries; a general transport vertex has *at most* n+m-1.
- **Quantiles:** integrate exact empirical step quantiles for W distances, the location/spread/shape decomposition and barycenter moments. Linear interpolation of sample quantiles is a different empirical law. KDE displays use a finite quantile grid only for illustration.
- **Sinkhorn:** distinguish raw plan cost from the regularized objective cost + epsilon KL(P || a tensor b). Log scaling checks both marginal residuals and fails on exhaustion. An initial map fit exhausted 50,000 iterations at residual 9.96e-8 rather than the requested 1e-8. Map fitting now uses log scaling plus a line-searched reduced-dual Newton refinement, with marginal tolerance **1e-10**; primal/dual differences are recorded. This is the same entropic optimization problem, not an altered statistical target. Scalar convergence iteration counts in the Sinkhorn chapter still use unaccelerated log scaling.
- **Sinkhorn divergence:** with squared-Euclidean cost the small-epsilon limit is W2 squared, and the large-epsilon limit is squared distance between means. It need not separate laws in that limit. Ordinary-distance cost yields a different energy-distance limit. Continuous regularized-value expansions are not a bias formula for the finite discrete raw-cost plot.
- **Rates:** record replicate draws and empirical standard errors. Dimension-independent fixed-epsilon exponents do not imply dimension-independent constants or uniformity as epsilon tends to zero. Tail, order, support and null-versus-alternative assumptions matter.
- **Maps:** the Gaussian simulation uses one specific nearest-neighbor extension versus the entropic barycentric extension, with heuristic epsilon=.5 n^(-1/3), four training datasets and a shared 500-point Monte Carlo integration sample. It does not validate the compact-support minimax theorem or prove universal dominance. Hutter–Rigollet's stated-model squared-risk rate includes a parametric 1/n floor. Pooladian–Niles-Weed's original entropic bound is generally slower than that minimax rate.
- **Ranks:** the testing reference is a fixed distinct Halton set; pooled row order is randomized before assignment to keep tie resolution independent of sample labels. Pairwise rank distances are cached. Use plus-one permutation p-values and reject at p<=.05. Population center-outward regions and smoothed finite-data ring polygons are different objects; the polygons are not exact finite-sample confidence regions.
- **Flows:** record exact continuous Gaussian Langevin and exact discrete Gaussian Euler laws separately. Only 300 of 600 simulated particles are drawn. KL of a fitted Gaussian is not KL of the atomic empirical measure, which is infinite relative to a continuous target. Euler bias and sampling noise both affect comparisons.
- **Generation:** show every generated point without coordinate clamping. Five fresh-noise draws are conditional on one fitted kernel velocity field; errors are distances to the training empirical law, not held-out generalization estimates. Population endpoint and straight-path theorems need regularity and do not automatically hold for a finite fitted field or one Euler step.

## Fixed empirical datasets and results

NHANES results concern the same **unweighted empirical complete-case extract** used in Part 60, not a national survey-weighted distribution; age is top-coded at 80. CDC field verification and Old Faithful's independent R-package comparison are retained in the [data receipt](../../../docs/qa/evidence/stats61-polish-20261107/source-data.json). Historical originals of Old Faithful were not separately retrieved.

| Example | Revised result |
|---|---|
| NHANES BMI, men versus women | W1=1.25007, W2=1.85902 |
| Exact W2-squared decomposition | location 0.68185 + spread 2.60262 + shape 0.17148 = 3.45594; residual -3.6e-15 |
| Empirical age-group SBP barycenter | exact mean 126.18670, SD 17.37092; mixture SD 19.90141 |
| Gaussian map error at n=800, four fits | empirical 0.12689 (empirical SE 0.01192); entropic 0.07694 (SE 0.01434) |
| Cauchy null, 1,000 datasets, nominal 5% | Hotelling 1.6% (MC SE 0.40 points); rank energy 6.3% (SE 0.77) |
| Cauchy location shift (1,1), 300 datasets | Hotelling power 5.3%; rank energy 84.7% |

A barycenter variance is a weighted sum of pairwise covariances of quantile functions. Its SD equals the weighted average group SD only in a common location-scale family; in general it is at most that average. It is not literally the mixture's within-group variance. General Gaussian barycenters solve an implicit matrix fixed point; only special commuting cases have a simple explicit covariance formula.

## Build and verification

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m videos.stats.stats61.compute --force
pytest -q tests/test_stats61_checked.py tests/test_stats_kit_ot.py
python tools/build.py stats61 -q l
python tools/lecture_length.py stats61 --floor 50
```

All 13 numerical inputs regenerated. Seventeen checks cover audited kernels and legacy behavior. Narration/list bookmarks match their rows; estimated English narration is 52.5 minutes. [Scientific QA evidence](../../../docs/qa/evidence/stats61-polish-20261107/README.md). The recorded English sampled visual checkpoint is complete; Chinese narration/caption tables, continuous listening/playback and final narrated masters remain open. This is not bilingual production approval.

## Sources

- **History.** G. Monge, *Mémoire sur la théorie des déblais et des remblais* (1781); L. Kantorovich, *Dokl. Akad. Nauk
  SSSR* 37 (1942); L. Kantorovich & G. Rubinstein (1958); L. Vaserstein (1969).
- **Duality and maps.**
  - Y. Brenier, *CPAM* 44 (1991); R. McCann, *Adv. Math.* 128 (1997);
  - L. Caffarelli, *JAMS* 5 (1992); F. Otto, *Comm. PDE* 26 (2001);
  - H. Kuhn, *Naval Res. Logist. Q.* 2 (1955); D. Bertsekas (1979);
  - C. Villani, *Optimal Transport: Old and New* (2009).
- **Rates.**
  - R. Dudley, *Ann. Math. Stat.* 40 (1969); N. Fournier & A. Guillin, *PTRF* 162 (2015);
  - J. Weed & F. Bach, *Bernoulli* 25 (2019); J. Niles-Weed & Q. Berthet, *Ann. Stat.* 50 (2022);
  - E. del Barrio, E. Giné & C. Matrán, *Ann. Prob.* 27 (1999); E. del Barrio & J.-M. Loubes, *Ann. Prob.* 47 (2019);
  - S. Hundrieser, T. Staudt & A. Munk (2024);
  - J. Rabin et al. (2011); N. Bonneel et al., *JMIV* 51 (2015); K. Nadjahi et al., NeurIPS (2020).
- **Entropic transport.**
  - R. Sinkhorn, *Ann. Math. Stat.* 35 (1964); M. Cuturi, NeurIPS (2013);
  - A. Genevay, L. Chizat, F. Bach, M. Cuturi & G. Peyré, AISTATS (2019);
  - G. Mena & J. Niles-Weed, NeurIPS (2019); J. Feydy et al., AISTATS (2019);
  - L. Chizat, G. Peyré, B. Schmitzer & F.-X. Vialard, *Math. Comp.* 87 (2018);
  - E. del Barrio, A. González-Sanz, J.-M. Loubes & J. Niles-Weed, *SIMODS* (2023).
- **Maps.**
  - J.-C. Hütter & P. Rigollet, *Ann. Stat.* 49 (2021); A.-A. Pooladian & J. Niles-Weed (2021);
  - G. Schiebinger et al., *Cell* 176 (2019); Q. Mérigot (2011); B. Lévy (2015).
- **Barycenters.**
  - M. Agueh & G. Carlier, *SIAM J. Math. Anal.* 43 (2011);
  - P. Álvarez-Esteban, E. del Barrio, J. Cuesta-Albertos & C. Matrán, *J. Math. Anal. Appl.* 441 (2016);
  - M. Cuturi & A. Doucet, ICML (2014); J.-D. Benamou et al., *SIAM J. Sci. Comput.* 37 (2015);
  - T. Le Gouic & J.-M. Loubes, *PTRF* 168 (2017); A. Ahidar-Coutrix, T. Le Gouic & Q. Paris, *PTRF* 177 (2020);
  - V. Panaretos & Y. Zemel, *An Invitation to Statistics in Wasserstein Space* (2020).
- **Ranks.**
  - V. Chernozhukov, A. Galichon, M. Hallin & M. Henry, *Ann. Stat.* 45 (2017);
  - M. Hallin, E. del Barrio, J. Cuesta-Albertos & C. Matrán, *Ann. Stat.* 49 (2021);
  - N. Deb & B. Sen, *JASA* 118 (2023); G. Carlier, V. Chernozhukov & A. Galichon, *Ann. Stat.* 44 (2016).
- **Flows and sampling.**
  - R. Jordan, D. Kinderlehrer & F. Otto, *SIAM J. Math. Anal.* 29 (1998);
  - D. Bakry & M. Émery (1985); A. Wibisono, COLT (2018);
  - A. Dalalyan, *JRSS B* 79 (2017); A. Durmus & É. Moulines, *Ann. Appl. Prob.* 27 (2017);
  - Q. Liu & D. Wang, NeurIPS (2016); S. Mei, A. Montanari & P.-M. Nguyen, *PNAS* 115 (2018);
  - L. Chizat & F. Bach, NeurIPS (2018); S. Chewi, *Log-Concave Sampling*.
- **Generative models.**
  - M. Arjovsky, S. Chintala & L. Bottou, ICML (2017); I. Gulrajani et al., NeurIPS (2017); T. Miyato et al., ICLR (2018);
  - Y. Lipman et al., ICLR (2023); X. Liu, C. Gong & Q. Liu, ICLR (2023);
  - A. Tong et al., *TMLR* (2024); A.-A. Pooladian et al., ICML (2023);
  - K. Oko, S. Akiyama & T. Suzuki, ICML (2023); S. Chen, S. Chewi et al., ICLR (2023);
  - N. Carlini et al., USENIX Security (2023); J. Niles-Weed & P. Rigollet, *Bernoulli* 28 (2022).
- **Books.** Villani (2009); G. Peyré & M. Cuturi, *Computational Optimal Transport* (2019); Panaretos & Zemel (2020);
  S. Chewi, J. Niles-Weed & P. Rigollet, *Statistical Optimal Transport* (2025).
- **Data.** NHANES (CDC); A. Azzalini & A. Bowman, *Appl. Stat.* 39 (1990).

## Problems and solutions

1. **W₁ as an area.**
   - W₁ = ∫₀¹ |F⁻¹(u) − G⁻¹(u)| du is the area between the two quantile curves.
   - Swapping the roles of the axes, it is the area between the graphs of F and G, which is ∫ |F(x) − G(x)| dx.
   - Equivalently, by Kantorovich–Rubinstein, sup over 1-Lipschitz f of ∫ f d(μ − ν) = ∫ f′(x)(G(x) − F(x)) dx is
     maximized by f′ = sign(G − F).
2. **Sparse vertices.**
   - The transport polytope has n + m equality constraints, of which n + m − 1 are independent (both sets of marginals
     sum to one).
   - A vertex of a polytope {P ≥ 0 : AP = r} has at most rank(A) = n + m − 1 positive coordinates.
3. **Normal laws.**
   - The monotone coupling of N(m₁, σ₁²) and N(m₂, σ₂²) is Y = m₂ + (σ₂/σ₁)(X − m₁).
   - So E(X − Y)² = (m₁ − m₂)² + E(Z(σ₁ − σ₂))² = (m₁ − m₂)² + (σ₁ − σ₂)².
4. **Sinkhorn as dual ascent.**
   - The dual of the entropic problem is max over f, g of a′f + b′g − ε Σᵢⱼ aᵢbⱼ e^{(fᵢ + gⱼ − Cᵢⱼ)/ε} + ε.
   - Setting its derivative in fᵢ to zero gives fᵢ = −ε log Σⱼ bⱼ e^{(gⱼ − Cᵢⱼ)/ε}, and the same in gⱼ: these are the
     log-domain Sinkhorn updates.
   - Each is an exact block maximization of a concave function, so the dual objective increases monotonically.
5. **Location-scale barycenter.**
   - If F_k⁻¹(u) = m_k + σ_k Q(u) for a fixed quantile function Q, then Σ w_k F_k⁻¹(u) = Σ w_k m_k + (Σ w_k σ_k) Q(u).
   - This is the same family, with mean Σ w_k m_k and scale Σ w_k σ_k.
   - The mixture instead has variance Σ w_k(σ_k² + m_k²) − (Σ w_k m_k)², which includes the spread of the means.
6. **Langevin's rate.**
   - With S₀ = Σ, the covariance stays Σ and the mean is m(t) = e^{−Σ⁻¹t}m₀, so KL_t = ½ m(t)′Σ⁻¹m(t).
   - In Σ's eigenbasis, each coordinate decays like e^{−t/λᵢ} and contributes e^{−2t/λᵢ} times its initial share.
   - Every factor is at most e^{−2t/λ_max}, so KL_t ≤ e^{−2t/λ_max}KL₀.


## Where it comes back

Part 62 discusses transporting causal effects, Part 63 barycenter score adjustment, Part 64 generative-model generalization, and Part 65 research comparisons of distributions.
