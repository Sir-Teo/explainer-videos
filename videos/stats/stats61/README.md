# Statistics, Built — Part 61: Optimal Transport in Statistics

Part 61 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the sixth part of Stage V, the research frontier.

It opens with Monge's memoir of 1781 on cuttings and fillings: which shovelful of earth should fill which hole, so that
the total distance carried is least? On a line, the monotone plan wins: with squared distance as the cost its root
mean cost is 4.01, against 4.54 for a crossing plan. With Monge's own cost, the distance, the two plans cost almost the
same (4.00 and 4.03). Kantorovich (1942) turned the problem into a linear program over couplings. The part follows
optimal transport into statistics:
- Kantorovich duality:
  - couplings and the transport polytope, with a 6 × 7 example whose optimal plan has n + m − 1 = 12 nonzero entries;
  - the dual potentials and complementary slackness, and Caffarelli's shipper;
  - exact algorithms (Hungarian, auction);
  - the line's quantile solution, and Brenier's theorem (1991).
- Wasserstein distances:
  - the metric, Kantorovich–Rubinstein duality, and a comparison with TV, KL and the MMD;
  - NHANES BMI for men against women, with W₂² split into location, spread and shape;
  - the Gaussian (Bures) formula;
  - McCann's displacement interpolation, shown in the transport flow from a Gaussian cloud to Old Faithful.
- Empirical rates: n^{−1/d} (Dudley 1969; Fournier & Guillin 2015), simulated for d = 1–10; the intrinsic dimension
  (Weed & Bach 2019); sliced Wasserstein; one-dimensional limit theorems (del Barrio et al.).
- Entropic transport (Cuturi 2013):
  - Sinkhorn's scaling (1964), with sharp and blurred plans, convergence as ε shrinks, and the bias;
  - the Sinkhorn divergence's dimension-free rate (Genevay et al. 2019; Mena & Niles-Weed 2019);
  - unbalanced transport (Chizat et al. 2018).
- Transport maps: Hütter & Rigollet's (2021) minimax rate, semi-discrete transport, Caffarelli's regularity, and the
  empirical against the entropic estimator (Pooladian & Niles-Weed 2021).
- Barycenters (Agueh & Carlier 2011):
  - NHANES systolic pressure by age, the barycenter against the mixture;
  - the Gaussian fixed point (Álvarez-Esteban et al. 2016);
  - entropic barycenters, and the statistics of Fréchet means of laws.
- Multivariate ranks and quantiles (Chernozhukov et al. 2017; Hallin et al. 2021): center-outward contours of Old
  Faithful against Mahalanobis ellipses, and the rank energy test (Deb & Sen 2023).
- Gradient flows (Jordan, Kinderlehrer & Otto 1998):
  - Langevin particles against the exact Fokker–Planck flow, with the log-Sobolev rate;
  - Otto's calculus, ULA's bias, and SVGD and mean-field networks.
- Generative models:
  - WGANs (Arjovsky et al. 2017) and the gradient penalty;
  - flow matching and rectified flow (Lipman et al.; Liu et al. 2023);
  - OT pairing (Tong et al.; Pooladian et al. 2023), simulated on Old Faithful.
- Five open problems.

It keeps two promises:
- **Part 21** solved linear programs and their duals. Chapter 1 turns the transport LP into a statistic.
- **Part 60** used Wasserstein balls as uncertainty sets without studying the distance. Chapters 2–5 study it, and ask
  how well it can be estimated.

**Built in this part:**
- **`statkit.ot`** ([`explainer/stats/kit/ot.py`](../../../explainer/stats/kit/ot.py)), tested in
  `tests/test_stats_kit_ot.py`:
  - one-dimensional W_p exactly, and W₁ as the area between CDFs;
  - discrete transport: cost matrices, the Hungarian assignment, and the Kantorovich LP with its dual potentials (HiGHS);
  - Gaussian W₂ (Bures), the linear Brenier map, and McCann's interpolation;
  - an empirical-rate harness;
  - log-domain Sinkhorn with its convergence trace, and the Sinkhorn divergence;
  - the entropic (barycentric-projection) map;
  - one-dimensional and Gaussian barycenters;
  - Hallin's spherical grid, center-outward ranks, the energy distance, the rank energy test, and Hotelling's T²;
  - Langevin particles, the exact Gaussian Fokker–Planck flow, and Gaussian KL;
  - a toy flow-matching sampler (independent or OT pairing) with Euler integration.
- **The transport flow** (`TransportFlow` in `explainer/stats/viz.py`), the part's instrument. It draws a source cloud
  matched to a target cloud by a permutation, moves the cloud along McCann's interpolation, draws the paths, and shows a
  coupling matrix as a heat grid, so the LP's sparse plan and Sinkhorn's blurred ones can be compared cell by cell.

**Data.**
- From the Museum: NHANES (BMI by sex; systolic pressure by age group) and Old Faithful (Azzalini & Bowman 1990).
- The rest is exact arithmetic (LP, assignment, closed forms) or seeded simulation.

The Coverage Board gains two rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| Hotelling's T², two samples | bivariate Cauchy, n = m = 40 | 5% | 2.0% | conservative |
| Rank energy test (OT ranks) | bivariate Cauchy, n = m = 40 | 5% | 4.3% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats61.compute   # once (several minutes)
python tools/build.py stats61 -q l                         # fast 480p preview
python tools/build.py stats61                              # 1080p30 -> renders/stats61.mp4
python tools/qa_scene.py stats61 Wasserstein
python tools/lecture_length.py stats61 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Monge | 40 shovelfuls from N(3, 1) to ½N(6, 0.7²) + ½N(8, 0.5²): monotone W₂ 4.01, crossing 4.54; W₁ 4.00 vs 4.03 |
| 1 | Duality | 6 sources, 7 targets, squared cost: LP cost 6.210 = dual 6.210, max constraint violation 9 × 10⁻¹⁶, 12 nonzero entries |
| 2 | Wasserstein | NHANES BMI, 2,512 men and 2,664 women: means 29.25 and 30.07, sds 6.49 and 8.10; W₁ = 1.25, W₂ = 1.86; W₂² = 0.68 (location) + 2.60 (spread) + 0.16 (shape); Old Faithful matching: mean squared move 13.53 vs 15.53 at random |
| 3 | Rates | E W₁ between two uniform samples, n = 25–1,600: slopes −0.48 (d = 1), −0.44 (2), −0.35 (3), −0.23 (5), −0.13 (10) |
| 4 | Sinkhorn | 6 × 7 plans: LP 6.21, ε = 0.1, 0.5, 2: 6.22, 6.32, 6.75; 60 × 60: 65, 656 and 10,284 iterations at ε = 1, 0.1, 0.03; cost 4.72 (ε = 3) to 3.065 (0.03) vs exact 3.056; N(0, I₅) samples, n = 25–400: W₂² slope −0.38, Sinkhorn divergence (ε = 1) slope −0.60 |
| 5 | Maps | N(0, I₂) → N(0, Σ), Σ = [[3, 1], [1, 1]]: empirical map error 0.99 → 0.127 (n = 50 → 800, slope −0.73), entropic 0.70 → 0.077 (slope −0.78) |
| 6 | Barycenters | NHANES SBP at 18–39, 40–59, 60–80 (n = 1,731, 1,563, 1,882): means 114.8, 126.2, 136.6; barycenter mean 126.2, sd 17.3 vs mixture sd 19.9; Gaussian barycenter of diag(1, 4), diag(4, 1) = 2.25 I |
| 7 | Ranks | Old Faithful on 6 rings × 45 rays: contours at τ = 1/7, …, 6/7 vs Mahalanobis ellipses; Cauchy, n = m = 40, 1,000 nulls: Hotelling 2.0%, rank energy 4.3%; shift (1, 1), 300 reps: power 8% vs 78% |
| 8 | Gradient flows | N(0, Σ), ρ = 0.8, from N((4, −3), 0.2I), 600 particles, h = 0.02: KL 62.0 at t = 0 to 0.034 at t = 1.5 (exact); C_LS = λ_max = 1.8 |
| 9 | Generative | Old Faithful, kernel flow matching, 5 noise draws: W₂ to the data, noise 0.94; independent pairs 1.05 (1 step), 0.63, 0.42, 0.37 (20); OT pairs 0.35 at every step count; straightness 0.76 vs 0.995 |
| 10 | Open problems | — |
| 11 | Outro | — |

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

## Glossary

- **Problems.** Monge's problem; Kantorovich's relaxation; coupling; transport plan; transport polytope; assignment
  problem.
- **Duality.**
  - Dual potentials; complementary slackness; c-concavity.
  - Brenier map; cyclical monotonicity; Monge–Ampère equation; semi-discrete transport; Laguerre cells.
- **Distances.**
  - Wasserstein distance; Kantorovich–Rubinstein duality; Bures metric.
  - Displacement interpolation; displacement convexity.
  - Sliced Wasserstein; Sinkhorn divergence; unbalanced transport.
- **Statistics.**
  - Empirical rate; curse of dimensionality; intrinsic dimension.
  - Entropic map; barycenter; Fréchet mean.
  - Center-outward ranks and quantiles; rank energy test.
- **Flows.**
  - JKO scheme; Wasserstein gradient flow; Fokker–Planck equation; log-Sobolev inequality.
  - ULA; SVGD; WGAN; gradient penalty; flow matching; rectified flow; OT pairing.

## Where it comes back

- **Part 62**: transporting causal effects across populations.
- **Part 63**: fair scores by mapping groups onto their barycenter.
- **Part 64**: generative models, and whether they generalize.
- **Part 65**: the dissertation's comparisons of distributions.
