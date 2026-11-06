# Statistics, Built — Part 51: High-Dimensional Probability

Part 51 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the ninth part of Stage IV, the PhD core.

It opens with Lévy's equator: pick a point uniformly on the sphere in a thousand dimensions, and its first coordinate
is within 0.062 of zero with probability 95%, whichever coordinate you choose. The part asks what randomness looks
like when the dimension is large, and finds it predictable:
- sub-Gaussian and sub-exponential variables, Orlicz norms, and Hoeffding, Bernstein and Chernoff against exact tails;
- thin shells, near-orthogonality and the Johnson–Lindenstrauss lemma;
- the concentration of Lipschitz functions of Gaussians (Tsirelson–Ibragimov–Sudakov), with Herbst's argument; the
  sphere; Talagrand's convex-distance inequality;
- random matrices without asymptotics: ε-nets, √n ± √p, covariance estimation at rate √(p/n), Marchenko–Pastur, and
  a real correlation spectrum against it;
- matrix Bernstein (Tropp 2012), and when its log p is real;
- chaining revisited: Dudley's integral, Sudakov's minoration, Talagrand's ellipsoid and generic chaining;
- Gaussian comparison: Slepian, Sudakov–Fernique, Gordon, and the convex Gaussian min-max theorem;
- Gaussian widths and Gordon's escape through the mesh;
- the statistical dimension (Amelunxen, Lotz, McCoy & Tropp 2014), which explains the Donoho–Tanner curve;
- intervals from concentration, on the Board.

It keeps three promises:
- **Part 43** proved the LLN, the CLT and large deviations as n → ∞ with the dimension fixed. Chapters 1–3 give tail
  bounds valid at every n, in any dimension.
- **Part 48** built chaining and Talagrand's inequality for empirical processes. Chapters 6–7 make them general tools
  for Gaussian processes, with matching lower bounds.
- **Part 32** found the Donoho–Tanner phase transition of basis pursuit by experiment. Chapters 8–9 compute it.

**Built in this part:**
- **`statkit.hdp`** ([`explainer/stats/kit/hdp.py`](../../../explainer/stats/kit/hdp.py)), tested in
  `tests/test_stats_kit_hdp.py`:
  - the sphere: the exact law of one coordinate, band masses, the angle between random directions, uniform sampling;
  - the χ law of ‖g‖; Johnson–Lindenstrauss distortions and dimensions;
  - Hoeffding, Bernstein and Chernoff tails against the exact binomial; ψ₂ and ψ₁ norms, exact and empirical;
  - Gaussian concentration; the exact expected maximum of n normals by quadrature;
  - extreme singular values, covariance error in operator norm and its Marchenko–Pastur limit, the Marchenko–Pastur
    density; matrix Bernstein for rank-one sums;
  - exchangeable maxima (Slepian), Sudakov's minoration; Brownian motion's grid maximum, Dudley's integral and the
    union bound;
  - Gaussian widths of the ℓ₁ and ℓ₂ balls; the statistical dimension of the ℓ₁ descent cone and the Donoho–Tanner
    curve.
- **The `SphereShell`** (in `explainer/stats/viz.py`), the part's instrument: the sphere drawn as a circle, with its
  equatorial band of the true half-width for the stated n, the Gaussian shell, scattered points, and (chapter 8) the
  descent cone with random null spaces that hit or miss it.

**Data.**
- From the Museum: the Wisconsin breast cancer data (Wolberg, Street & Mangasarian 1995), 569 biopsies and 30
  features, last seen in Part 34.
- The rest is exact arithmetic or seeded simulation.

The Coverage Board gains six rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| Wald interval | Bernoulli(p = 0.02), n = 200 | 95% | 90.9% | broken |
| Hoeffding interval | Bernoulli(p = 0.02), n = 200 | 95% | 100% | conservative |
| empirical Bernstein interval | Bernoulli(p = 0.02), n = 200 | 95% | 100% | conservative |
| Wald interval | Bernoulli(p = 0.5), n = 200 | 95% | 94.2% | broken |
| Hoeffding interval | Bernoulli(p = 0.5), n = 200 | 95% | 99.4% | conservative |
| empirical Bernstein interval | Bernoulli(p = 0.5), n = 200 | 95% | 100% | conservative |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats51.compute   # once (a few minutes)
python tools/build.py stats51 -q l                         # fast 480p preview
python tools/build.py stats51                              # 1080p30 -> renders/stats51.mp4
python tools/qa_scene.py stats51 StatisticalDimension
python tools/lecture_length.py stats51 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The sphere's equator | 95% half-width of x₁: 0.95 (n = 3), 0.60 (10), 0.196 (100), 0.062 (1,000), 0.0196 (10,000); mass within 0.1: 10% → 100% |
| 1 | Sub-Gaussian and sub-exponential | ψ₂(N(0, 1)) = √(8/3) = 1.63, ψ₂(Rademacher) = 1/√(log 2) = 1.20; Hoeffding vs Bernstein vs exact at p = 0.02, n = 200 |
| 2 | Geometry | SD of ‖g‖: 0.65 (n = 2) → 0.72 (n = 10,000); angle SD 51.6° → 0.58°; JL with N = 200 in R⁵⁰⁰⁰: k = 500 worst distortion 26%, 89% of pairs within 10% |
| 3 | Lipschitz functions | n = 1,000: Var‖g‖ = 0.49, Var max gᵢ = 0.125 (bound 1); E max: 1.54 (n = 10) → 3.85 (10,000) |
| 4 | Random matrices | n = 400: s_max 29.72 vs 30 and s_min 10.14 vs 10 at p = 100; MP with γ = 1/4: eigenvalues 0.26–2.24; cancer: 5 eigenvalues above the MP edge 1.51, top 13.28 (44%), top five 85%; shuffled top 1.47 |
| 5 | Matrix Bernstein | p = 50: E‖S − I‖ 1.73 (n = 100) → 0.25 (n = 3,200); bound about 1.6× the truth; MP edge close |
| 6 | Chaining | Brownian grid max 0.80 = √(2/π); union bound 4.29 at N = 10⁴; Dudley's integral → √(π/2) = 1.25; ellipsoid aₖ = 1/√k: E sup 1.67 → 3.11 vs log p 2.3 → 9.2 |
| 7 | Gaussian comparison | 1,000 exchangeable normals: E max 3.24 √(1 − ρ); ρ = 1/2 attains Sudakov's 2.29 |
| 8 | Widths | w(B₂) = 3.08 → 100.0; w(B₁) = 1.88 → 4.02 for p = 10 → 10,000 |
| 9 | Statistical dimension | p = 100: δ = 6.1 (s = 1), 32.9 (s = 10), 75.0 (s = 40); half-success at m = 35 for s = 10; simulated E min dist² 32.2 vs 32.9 |
| 10 | The Board | Wald 90.9% at p = 0.02; Hoeffding half-width 0.096 vs Wald 0.019; 4/200: Clopper–Pearson [0.0055, 0.0504] |
| 11 | Outro | — |

## Sources

- **The sphere and concentration.**
  - P. Lévy, *Leçons d'analyse fonctionnelle* (1922); *Problèmes concrets d'analyse fonctionnelle* (1951).
  - B. Tsirelson, I. Ibragimov & V. Sudakov, in *Proc. Third Japan–USSR Symp.* (1976); L. Gross, *Amer. J. Math.* 97
    (1975); M. Ledoux, *The Concentration of Measure Phenomenon* (2001).
  - M. Talagrand, *Publ. Math. IHÉS* 81 (1995); S. Chatterjee, *Superconcentration and Related Topics* (2014).
- **Tails.** W. Hoeffding, *JASA* 58 (1963); S. Bernstein (1924); H. Chernoff, *Ann. Math. Stat.* 23 (1952);
  A. Maurer & M. Pontil, *COLT* (2009).
- **Geometry.** W. Johnson & J. Lindenstrauss, *Contemp. Math.* 26 (1984); S. Dasgupta & A. Gupta, *Random Struct.
  Alg.* 22 (2003).
- **Random matrices.**
  - V. Marchenko & L. Pastur, *Mat. Sb.* 72 (1967); K. Davidson & S. Szarek, *Handbook of the Geometry of Banach
    Spaces* (2001).
  - R. Ahlswede & A. Winter, *IEEE Trans. Inf. Theory* 48 (2002); J. Tropp, *Found. Comput. Math.* 12 (2012);
    A. Bandeira, M. Boedihardjo & R. van Handel, *Invent. Math.* 234 (2023).
  - J. Horn, *Psychometrika* 30 (1965); W. Wolberg, W. Street & O. Mangasarian (1995), UCI.
- **Chaining and comparison.**
  - R. Dudley, *J. Funct. Anal.* 1 (1967); V. Sudakov, *Dokl. Akad. Nauk SSSR* (1969); X. Fernique, *École d'Été de
    Saint-Flour* (1975); M. Talagrand, *Acta Math.* 159 (1987).
  - D. Slepian, *Bell Syst. Tech. J.* 41 (1962); Y. Gordon, *Israel J. Math.* 50 (1985); *GAFA Seminar* (1988).
  - M. Stojnic, arXiv:1303.7291 (2013); C. Thrampoulidis, S. Oymak & B. Hassibi, *COLT* (2015).
- **Widths and phase transitions.**
  - V. Chandrasekaran, B. Recht, P. Parrilo & A. Willsky, *Found. Comput. Math.* 12 (2012).
  - D. Amelunxen, M. Lotz, M. McCoy & J. Tropp, *Inf. Inference* 3 (2014); M. McCoy & J. Tropp, *Found. Comput. Math.*
    14 (2014).
  - D. Donoho & J. Tanner, *Phil. Trans. R. Soc. A* 367 (2009); S. Oymak & J. Tropp, *Inf. Inference* 7 (2018).
- **Confidence sequences.** J. Ville, *Étude critique de la notion de collectif* (1939); S. Howard, A. Ramdas,
  J. McAuliffe & J. Sekhon, *Ann. Stat.* 49 (2021).
- **Books.** R. Vershynin, *High-Dimensional Probability* (2018); M. Wainwright, *High-Dimensional Statistics*
  (2019), ch. 2–6; S. Boucheron, G. Lugosi & P. Massart, *Concentration Inequalities* (2013); J. Tropp, *An
  Introduction to Matrix Concentration Inequalities* (2015); M. Talagrand, *Upper and Lower Bounds for Stochastic
  Processes* (2021).

## Problems and solutions

1. **Hoeffding's lemma.**
   - Let ψ(λ) = log E e^{λX}. Then ψ(0) = 0, ψ′(0) = EX = 0, and ψ″(λ) is the variance of X under the tilted law
     dQ ∝ e^{λX} dP.
   - Any law on [a, b] has variance at most (b − a)²/4, so ψ″ ≤ (b − a)²/4. Taylor's theorem gives
     ψ(λ) ≤ λ²(b − a)²/8.
2. **The sphere's coordinate.**
   - By symmetry, E x₁² = … = E xₙ², and they sum to 1, so E x₁² = 1/n.
   - Write x = g/‖g‖. Then √n x₁ = g₁/(‖g‖/√n), and ‖g‖/√n → 1 by the LLN, so √n x₁ → N(0, 1) by Slutsky.
3. **Johnson–Lindenstrauss for one pair.**
   - For a k × d matrix G with N(0, 1) entries and a unit u, Gu ~ N(0, I_k), so ‖Gu‖² ~ χ²_k.
   - χ²_k − k is sub-exponential, and Bernstein gives P(|χ²_k/k − 1| > ε) ≤ 2e^{−kε²/8} for ε ≤ 1.
   - A union bound over N² pairs needs k ≥ 16 log N/ε².
4. **Three Lipschitz functions.**
   - The reverse triangle inequality gives |‖x‖ − ‖y‖| ≤ ‖x − y‖. Also |max xᵢ − max yᵢ| ≤ max|xᵢ − yᵢ| ≤ ‖x − y‖.
   - |s_max(A) − s_max(B)| ≤ ‖A − B‖_op ≤ ‖A − B‖_F, the Euclidean norm of the entries.
5. **The exchangeable maximum.**
   - max_i(√(1 − ρ)Zᵢ + √ρ W) = √(1 − ρ) max_i Zᵢ + √ρ W, since W is common to every i.
   - Take expectations: E W = 0.
6. **Two statistical dimensions.**
   - The projection onto a k-dimensional subspace L gives ‖Π_L g‖² ~ χ²_k, with mean k.
   - The projection onto the orthant is (gᵢ)₊ coordinatewise, and E(gᵢ)₊² = 1/2, so δ = p/2.

## Glossary

- **Tails.**
  - Sub-Gaussian; sub-exponential; Orlicz norm ψ₂, ψ₁; variance proxy; MGF bound: tail classes.
  - Hoeffding's inequality and lemma; Bernstein's inequality; Chernoff bound; empirical Bernstein: inequalities.
- **Geometry and concentration.**
  - Concentration of measure; thin shell; near-orthogonality; Johnson–Lindenstrauss lemma: high-dimensional geometry.
  - Lipschitz function; Gaussian concentration; Poincaré inequality; log-Sobolev inequality; Herbst's argument;
    tensorization; isoperimetry; convex-distance inequality; superconcentration: the machinery.
- **Random matrices.**
  - Operator norm; ε-net; singular values; Marchenko–Pastur law; spiked spectrum; parallel analysis: spectra.
  - Matrix variance; matrix Bernstein; trace exponential; Lieb's theorem; intrinsic freeness: sums of matrices.
- **Gaussian processes.**
  - Canonical metric; covering number; Dudley's entropy integral; Sudakov's minoration; γ₂ functional; generic
    chaining; majorizing measures: the size of a supremum.
  - Slepian's lemma; Sudakov–Fernique; Gordon's inequality; CGMT; contraction: comparison.
- **Widths.**
  - Gaussian width; descent cone; null-space property; escape through the mesh; statistical dimension; kinematic
    formula; phase transition; universality: when convex recovery works.
  - Confidence sequence; Ville's inequality: concentration over time.

## Where it comes back

- **Part 52**: restricted eigenvalues of random designs, the lasso's rate, sparse PCA, matrix completion.
- **Part 54**: Rademacher complexity, contraction and uniform laws for learning theory.
- **Part 58**: confidence sequences from Ville's inequality.
- **Part 59**: proportional asymptotics, where Marchenko–Pastur and the CGMT give exact risks.
