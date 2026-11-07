# Statistics, Built — Part 31: Multivariate Analysis

Part 31 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the eleventh part of Stage III, Master's. Part 30 survived bad data in one
dimension. This part asks what structure hides in many correlated variables at once:
- distance and the Wishart distribution;
- tests of mean vectors (Hotelling's T², MANOVA);
- low-dimensional structure (principal components, factor analysis, canonical correlation);
- groups, known and unknown (discriminant analysis, clustering);
- graphs of conditional independence;
- what goes wrong when the number of variables p grows with the sample size n.

Its instrument is the map from distances (`DistanceMap`): a map rebuilt from a table of distances, drawn over the
truth with its residuals. Its kit is `statkit.multi`.

It opens with the World's 200 towns:
- roads join each town to its four nearest neighbours, each road 10–30% longer than straight, giving 19,900
  shortest-route distances;
- a typical route is 1.44 times the straight line;
- classical scaling (Torgerson 1952), Procrustes-rotated onto the truth, rebuilds the island with an RMSE of 0.55 on
  an island 10 units across;
- two dimensions hold 84.7% of the positive eigenvalue mass; the absolute negative sum is 13.95% of the positive sum because roads are not
  straight;
- from exact Euclidean distances the error is 10⁻¹⁵.

Then the Cambridge Encyclopaedia road distances between 21 European cities. Two dimensions hold 86.8%, the stated normalized raw distance stress is 0.090.
The orientation uses known Stockholm/Lisbon geography; north is not learned from distances alone. The worst-fitting pairs:

| Pair | Table (km) | Map (km) |
|---|---|---|
| Cologne–Geneva | 1,662 | 713 |
| Athens–Rome | 817 | 1,725 |
| Lisbon–Lyons | 1,178 | 1,714 |

These are entries worth checking against their sources. A low-rank map residual alone cannot establish a transcription error or historical route mode.

From there the part covers:
- **The data matrix.**
  - x̄, S, R; the multivariate normal and its ellipsoids; whitening.
  - Mahalanobis distance (1936) on Fisher's 50 versicolors. The χ²₄ QQ plot is a rough radial diagnostic, not a test that establishes joint normality. The largest D² is 12.5. Because mean and covariance are fitted to the same observations, its exact Gaussian marginal reference is a scaled beta; the distances are dependent. The most outlying flower by Mahalanobis distance (index 18) is not the farthest by
    Euclid (index 48).
- **Wishart** (1928) and Bartlett's decomposition (1933).
  - With p = 3 and m = 10, 20,000 Bartlett draws give E W/m with displayed Monte Carlo standard errors, Var W₁₁ = 80.4 against 2mσ₁₁² = 80,
    and Var W₁₂ = 26.6 against 26.4.
  - The inverse-Wishart prior and its update after integrating an independently flat unknown-mean prior: IW(ν+n−1, Ψ+(n−1)S).
  - The fanning-out of sample eigenvalues. With p = 50, n = 100 and Σ = I they run from 0.10 to 2.76, inside the
    Marchenko–Pastur edges [0.084, 2.926] (p/(n−1) for the centered covariance).
- **Hotelling's T²** (1931), by Roy's union–intersection principle (1953). Versicolor against virginica:

  | Statistic | Value |
  |---|---|
  | univariate t (sepal length, sepal width, petal length, petal width) | −5.63, −3.21, −12.60, −14.63 |
  | T² | 355.5 |
  | F on (4, 95) df | 86.1 |
  | p | 9.5 × 10⁻³¹ |
  | the best combination's t | 18.85, with t² = T² |

  - The simultaneous confidence ellipsoid.
  - MANOVA on all three species. The eigenvalues of E⁻¹H are 32.19 and 0.285:

    | Statistic | Value |
    |---|---|
    | Wilks's Λ | 0.02344 (F = 199.1 on 8 and 288 df) |
    | Pillai's trace | 1.192 |
    | Hotelling–Lawley trace | 32.48 |
    | Roy's largest root | 32.19 |

  - statkit matches statsmodels to every printed digit.
- **Principal components** (Pearson 1901; Hotelling 1933).
  - The SVD and Eckart–Young (1936); classical scaling as PCA.
  - US arrests (1973), standardized: 62.0, 24.7, 8.9 and 4.3% of the variance.
    - PC1 loadings are (0.54, 0.58, 0.28, 0.54), an overall arrest-rate score; arrests are a proxy, not crime incidence.
    - PC2 loadings are (−0.42, −0.19, 0.87, 0.17), mostly urbanization.
    - Gabriel's biplot.
  - Units matter. On the irises the first component holds 92.5% raw but 73.0% standardized.
  - Choosing the number of components: Kaiser, the scree plot and parallel analysis (Horn 1965).
- **Factor analysis** (Spearman 1904; Thurstone; Lawley 1940; Jöreskog 1967) on Holzinger and Swineford's 24 tests
  (n = 145).
  - 275 of 276 off-diagonal correlations are positive (one is −0.075), averaging 0.30. The first eigenvalue is 8.14 of 24 (then 2.10, 1.69, 1.50, 1.03).
  - Bartlett's LR test p-values for k = 1–5 factors: 2.3 × 10⁻³³, 2.0 × 10⁻¹³, 5.1 × 10⁻⁵, 0.022 and 0.128.
  - The unrotated first factor loads on every test (0.34–0.75).
  - Varimax (Kaiser 1958) gives verbal (tests 5–9), speed (10–13), spatial (1–4) and memory (14–19) factors with the
    same Σ.
  - Uniquenesses run from 0.24 to 0.78, with no active numerical lower-bound flag (the constrained optimizer is checked for convergence).
  - Factor scores (Thomson, Bartlett); oblique rotation; FA against PCA.
- **Canonical correlation** (Hotelling 1936) on the savings data (50 countries, the 1960s).
  - Demography (pop15, pop75) against the economy (savings rate, income per head, income growth).
  - r₁ = 0.825 (Bartlett p = 7 × 10⁻¹¹) and r₂ = 0.365 (p = 0.037).
  - Structure correlations: pop15 −0.98 and pop75 +0.97; income +0.95 and savings +0.49.
  - The principal angles are 34.4° and 68.6°.
  - Regularized and sparse CCA; PLS.
- **Discriminant analysis** (Fisher 1936; Rao 1948).
  - The first discriminant carries 99.1% of the separation.
  - On petal length and width, LDA's lines and QDA's curves have leave-one-out errors of 4.0% and 3.3%.
  - On all four measurements, the training error is 2.0% for both. Leave-one-out, LDA stays at 2.0% and QDA rises to
    2.7%.
  - LDA against logistic regression (Efron 1975). The history is acknowledged.
- **Clustering.**
  - Lloyd's k-means (1957) from a bad start: 9 rounds, WSS 328 → 31.4, ARI 0.89 on the petals.
  - k-means as hard EM. A full-covariance Gaussian mixture has ARI 0.90, against k-means's 0.73 on all four variables.
  - The WSS elbow. BIC for k = 1–6 is 830, 574, 581, 622, 666 and 685, so it prefers two clusters.
  - Mixture pitfalls; the adjusted Rand index.
- **Graphical models.**
  - Partial correlations from Σ⁻¹. For the 24 tests, 60% are below 0.1. Word classification and word meaning
    correlate 0.53 but have partial correlation 0.00.
  - Dempster's covariance selection (1972). The graphical lasso (Friedman, Hastie & Tibshirani 2008) gives 164, 135,
    133, 97, 45 and 16 edges at λ = 0.05, 0.1, 0.2, 0.3, 0.4 and 0.5. The verbal clique appears first.
  - Neighbourhood selection (Meinshausen & Bühlmann 2006).
- **A high-dimensional warning.**
  - The chi-squared calibration fails as p/n grows; the exact F holds.
  - Bai–Saranadasa (1996) drops S⁻¹; Ledoit–Wolf shrinkage.
  - Power with a 0.15-SD shift in every coordinate:

    | p | exact T² (F) | Bai–Saranadasa |
    |---|---|---|
    | 10 | 0.27 | 0.34 |
    | 25 | 0.41 | 0.53 |
    | 40 | 0.45 | 0.72 |
    | 90 | 0.16 | 0.95 |

Data:
- Cambridge Encyclopaedia European road distances (1990), Fisher's irises (Anderson 1935; Fisher 1936), Holzinger and Swineford's
  24 tests (1939, via Harman 1976), the savings data (Sterling 1977; Belsley, Kuh & Welsch 1980) and US arrests
  (McNeil 1977) are the Museum's;
- the towns are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.multi`** ([`explainer/stats/kit/multi.py`](../../../explainer/stats/kit/multi.py)), checked in
  `tests/test_stats_kit_multi.py`:
  - **Distances:** classical MDS, Procrustes, Mahalanobis distance.
  - **Wishart and tests:** Bartlett's Wishart sampler; one- and two-sample T²; Bai–Saranadasa; MANOVA (Wilks, Pillai,
    Hotelling–Lawley, Roy, with Rao's F).
  - **Structure:** PCA; maximum-likelihood factor analysis with Bartlett's test and a Heywood flag; varimax; CCA with
    Bartlett's tests.
  - **Groups:** LDA and QDA with leave-one-out error; k-means++ and Lloyd; Gaussian mixtures by EM with BIC; the
    adjusted Rand index.
  - **Graphs:** partial correlations; the graphical lasso.
- **The Museum** gains `eurodist()`, `iris()`, `harman74()`, `lifecycle()` and `usarrests()`.
- **The map from distances** (`DistanceMap` in `explainer/stats/viz.py`).

The Coverage Board gains five rows. Size of the two-sample T² test at 5%, two samples of 50 from one normal, 2,000
data sets each:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| T² with a χ²_p calibration | p = 2 | 5.4% | kept |
| T² with a χ²_p calibration | p = 25 | 32.5% | broken |
| T² with a χ²_p calibration | p = 40 | 72.2% | broken |
| T² with the exact F | p = 40 | 5.4% | kept |
| Bai–Saranadasa | p = 40 | 6.25% | kept |

At p = 10, the χ² calibration rejects 10.4% (not a Board row).

Part-specific numerical corrections: the undirected road graph samples one detour factor per unique physical edge, preventing reciprocal-neighbor CSR entries from being summed. The graphical lasso enforces an unpenalized diagonal as its stated off-diagonal objective requires; the six edge counts above are recomputed from that objective. The local factor optimizer checks convergence, and factor columns are explicitly assigned to the named test groups after varimax. Orthogonal rotation preserves a four-factor covariance; it cannot turn four factors into one. Four factors have p = 0.022 and are rejected at 5%; five give p = 0.128. Four are used for an illustrative interpretation, not accepted by that test.

The Gaussian-mixture implementation evaluates likelihood and responsibilities at the returned parameters and checks convergence in absolute likelihood change. Fits use a declared 1e−6 covariance ridge and multiple starts. Mixture BIC is a regularized local-fit heuristic, not a proof of two biological species or two density modes. K-means' small-variance connection assumes positive fixed mixture weights away from ties; deterministic assignment handling matters for finite termination.

The LDA/QDA four-variable covariance counts are 10 and 30, not 15 and 45. The one-error leave-one-out difference does not establish a general ranking. Shared-covariance Gaussian inference requires independent samples, nonsingular covariance and adequate degrees of freedom. MANOVA's displayed Rao F is an approximation in general. Partial correlation measures adjusted linear association; an estimated Gaussian graph is not verified population independence or a causal graph. PLS requires normalization of its weights. Covariance shrinkage is positive definite with positive weight and positive trace; plugging it into T² does not preserve the classical exact F law. At p = 90 with two samples of 50, the exact F denominator has 9 degrees of freedom, not 8.

Classical scaling minimizes Gram-matrix approximation error rather than distance stress. The Marchenko–Pastur curve is an asymptotic independent-noise reference; gamma above one also has a zero atom. Neither a finite eigenvalue plot nor parallel analysis guarantees recovered structure. The arrest biplot arrows are loadings multiplied by 2.6 for display, not unscaled reconstruction coordinates. Factor scores retain uncertainty with positive uniqueness, and oblique rotation uses LΦLᵀ + Ψ. Maximum-likelihood factor fitting is equivariant under unit changes with free uniquenesses; numerical loadings rescale.

## Build it

```bash
python -m videos.stats.stats31.compute         # once (a few minutes)
python tools/build.py stats31 -q l             # fast 480p preview
python tools/build.py stats31                  # 1080p30 -> renders/stats31.mp4
python tools/qa_scene.py stats31 Graphs
python tools/lecture_length.py stats31 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | A map from distances | towns RMSE 0.55; Europe 87%, Cologne–Geneva 1,662 vs 713 |
| 1 | The data matrix | max D² 12.5 vs cut 11.1 |
| 2 | Wishart | Var W₁₁ 80.4 vs 80; MP edges [0.084, 2.926] (p/(n−1) for the centered covariance) |
| 3 | Hotelling's T² and MANOVA | T² 355.5; Wilks 0.0234 |
| 4 | Principal components | 62% + 25%; iris 92.5% raw vs 73% standardized |
| 5 | Factor analysis | k = 4, p = 0.022; varimax: four named factors |
| 6 | Canonical correlation | r = 0.82, 0.37; 34°, 69° |
| 7 | Discriminant analysis | 99.1% on LD1; LOO 2.0% vs 2.7% |
| 8 | Clustering | ARI 0.89 / 0.90 / 0.73; BIC picks 2 |
| 9 | Graphical models | 276 → 97 → 45 → 16 edges |
| 10 | A high-dimensional warning | χ² size 72% at p = 40; power 0.16 vs 0.95 |
| 11 | Outro | — |

## Sources

- **Scaling.**
  - W. Torgerson, *Psychometrika* 17 (1952); G. Young & A. Householder, *Psychometrika* 3 (1938).
  - R. Shepard, *Psychometrika* 27 (1962); J. Kruskal, *Psychometrika* 29 (1964).
  - J. Gower, *Biometrika* 53 (1966); J. Hartigan, *Clustering Algorithms* (1975).
- **Distance and distribution.**
  - P. C. Mahalanobis, *Proc. Nat. Inst. Sci. India* 2 (1936).
  - J. Wishart, *Biometrika* 20A (1928); M. Bartlett, *Proc. Roy. Soc. Edinburgh* 53 (1933).
  - V. Marchenko & L. Pastur, *Mat. Sb.* 72 (1967).
- **Tests.**
  - H. Hotelling, *Ann. Math. Stat.* 2 (1931); S. N. Roy, *Ann. Math. Stat.* 24 (1953).
  - S. Wilks, *Biometrika* 24 (1932); K. C. S. Pillai, *Ann. Math. Stat.* 26 (1955); G. Box, *Biometrika* 36 (1949).
  - Z. Bai & H. Saranadasa, *Statistica Sinica* 6 (1996).
- **Structure.**
  - K. Pearson, *Phil. Mag.* 2 (1901); H. Hotelling, *J. Educ. Psych.* 24 (1933), *Biometrika* 28 (1936).
  - C. Eckart & G. Young, *Psychometrika* 1 (1936); K. Gabriel, *Biometrika* 58 (1971).
  - R. Cattell, *Multivar. Behav. Res.* 1 (1966); J. Horn, *Psychometrika* 30 (1965).
  - C. Spearman, *Amer. J. Psych.* 15 (1904); L. Thurstone, *Multiple-Factor Analysis* (1947).
  - D. Lawley, *Proc. Roy. Soc. Edinburgh* 60 (1940); K. Jöreskog, *Psychometrika* 32 (1967).
  - H. Kaiser, *Psychometrika* 23 (1958); H. B. Heywood, *Proc. Roy. Soc. A* 134 (1931).
  - C. Jordan, *Bull. SMF* 3 (1875).
  - H. Wold (1966); D. Witten, R. Tibshirani & T. Hastie, *Biostatistics* 10 (2009).
- **Groups.**
  - R. A. Fisher, *Ann. Eugen.* 7 (1936); E. Anderson, *Bull. Amer. Iris Soc.* 59 (1935).
  - C. R. Rao, *JRSS B* 10 (1948); B. Efron, *JASA* 70 (1975).
  - S. Lloyd, Bell Labs memo (1957), *IEEE Trans. Inf. Theory* 28 (1982).
  - D. Arthur & S. Vassilvitskii, *SODA* (2007); A. Dempster, N. Laird & D. Rubin, *JRSS B* 39 (1977).
  - L. Hubert & P. Arabie, *J. Classification* 2 (1985).
- **Graphs.**
  - A. Dempster, *Biometrics* 28 (1972); N. Meinshausen & P. Bühlmann, *Ann. Stat.* 34 (2006).
  - J. Friedman, T. Hastie & R. Tibshirani, *Biostatistics* 9 (2008).
  - O. Ledoit & M. Wolf, *J. Multivar. Anal.* 88 (2004).
- **Data.**
  - K. Holzinger & F. Swineford, *Supplementary Educational Monographs* 48 (1939); H. Harman, *Modern Factor
    Analysis* (3rd ed., 1976).
  - A. Sterling, *Unpublished BS thesis*, MIT (1977); D. Belsley, E. Kuh & R. Welsch, *Regression Diagnostics*
    (1980); R. McNeil, *Interactive Data Analysis* (1977).
- **Books.**
  - T. W. Anderson, *An Introduction to Multivariate Statistical Analysis* (3rd ed., 2003).
  - K. Mardia, J. Kent & J. Bibby, *Multivariate Analysis* (1979).
  - R. Muirhead, *Aspects of Multivariate Statistical Theory* (1982).
  - I. Jolliffe, *Principal Component Analysis* (2nd ed., 2002).
  - S. Lauritzen, *Graphical Models* (1996).
  - T. Hastie, R. Tibshirani & J. Friedman, *The Elements of Statistical Learning* (2nd ed., 2009).

## Problems and solutions

**1. Double-centring.**

*Solution.* Let x_i be the rows of X and X₀ = JX the centred rows x̃_i. Then d²_ij = ‖x̃_i‖² + ‖x̃_j‖² − 2x̃_iᵀx̃_j,
so D⁽²⁾ = a1ᵀ + 1aᵀ − 2X₀X₀ᵀ with a_i = ‖x̃_i‖². Since J1 = 0, J(a1ᵀ)J = 0 and J(1aᵀ)J = 0. Hence
−½JD⁽²⁾J = J X₀X₀ᵀ J = X₀X₀ᵀ, because JX₀ = X₀.

**2. Union–intersection.**

*Solution.* Let c = n₁n₂/(n₁ + n₂) and d = x̄₁ − x̄₂. Then t²(a) = c(aᵀd)²/(aᵀSa). Write b = S^{1/2}a. Then aᵀd = bᵀS^{−1/2}d, and
Cauchy–Schwarz gives (aᵀd)² ≤ ‖b‖²·‖S^{−1/2}d‖² = (aᵀSa)(dᵀS⁻¹d). So t²(a) ≤ c·dᵀS⁻¹d = T², with equality
iff b ∝ S^{−1/2}d, i.e. a ∝ S⁻¹d.

**3. Eckart–Young.**

*Solution.* Let X₀ = UDVᵀ and let B have rank ≤ k. By Weyl's inequality for singular values,
σ_{i+k}(X₀) ≤ σ_i(X₀ − B) + σ_{k+1}(B) = σ_i(X₀ − B). So ‖X₀ − B‖²_F = Σ_i σ_i(X₀ − B)² ≥ Σ_i σ_{i+k}(X₀)² =
Σ_{j>k} d_j². The truncated SVD attains this.

**4. Invariance of canonical correlations.**

*Solution.* Replace x by Ax + a and y by By + b, with A and B invertible. Then for any weights, corr(αᵀ(Ax), βᵀ(By)) =
corr((Aᵀα)ᵀx, (Bᵀβ)ᵀy). As α and β range over all vectors, so do Aᵀα and Bᵀβ. The sequence of constrained maxima,
each uncorrelated with the earlier variates (also invariant), is therefore the same.

**5. Zeros of the precision matrix.**

*Solution.* Partition x = (x_i, x_{−i}). For the normal, E(x_i | x_{−i}) = μ_i + Σ_{i,−i}Σ_{−i,−i}⁻¹(x_{−i} − μ_{−i}).
By the block-inverse formula, the i-th row of Θ = Σ⁻¹ gives Θ_{i,−i} = −θ_ii Σ_{i,−i}Σ_{−i,−i}⁻¹. So the regression
coefficient of x_j is β_ij = −θ_ij/θ_ii, which is zero iff θ_ij = 0. For the normal, the conditional distribution of
x_i given the rest then does not involve x_j: conditional independence.

**6. Lloyd's algorithm stops.**

*Solution.* With the assignment fixed, Σ_{i∈C_j}‖x_i − c‖² is minimized by the mean (its gradient is
2Σ(c − x_i)), so the update step cannot increase the objective. With the centres fixed, sending each point to its
nearest centre minimizes each term separately. So the objective is non-increasing. There are finitely many partitions
of n points into k groups. If ties are broken consistently, a strict decrease is needed to change the partition, so no
partition repeats and the algorithm stops in finitely many steps, at a Lloyd fixed point. This is not necessarily a global optimum; tie and empty-cluster handling must be specified.

## Glossary

- **Classical (metric) scaling; Gram matrix; double-centring; Procrustes; stress; nonmetric scaling**: maps from
  distances and how well they fit.
- **Mahalanobis distance; whitening**: distance in the data's own units; the transformation that makes it Euclidean.
- **Wishart; Bartlett decomposition; inverse-Wishart; Marchenko–Pastur law**: the distribution of a sample
  covariance, its triangular structure, its conjugate prior, and its eigenvalues when p/n → γ.
- **Hotelling's T²; union–intersection; simultaneous confidence ellipsoid**: the multivariate t-test and its
  intervals.
- **MANOVA; H and E; Wilks, Pillai, Hotelling–Lawley, Roy**: between- and within-group matrices and four summaries
  of E⁻¹H.
- **Principal component; loading; score; scree plot; biplot; parallel analysis**: directions of greatest variance
  and how to read and count them.
- **Factor; loading; communality; uniqueness; rotation (varimax, oblique); Heywood case; factor score**: the latent
  factor model and its vocabulary.
- **Canonical correlation; canonical variate; structure correlation; principal angle; PLS**: the best-correlated
  pairs of combinations of two blocks.
- **LDA; QDA; discriminant direction; leave-one-out error**: classifying into known groups.
- **k-means; Lloyd's algorithm; Gaussian mixture; EM; BIC; adjusted Rand index**: finding unknown groups and judging
  them.
- **Partial correlation; precision matrix; Gaussian graphical model; covariance selection; graphical lasso;
  neighbourhood selection**: conditional independence and its graph.
- **Bai–Saranadasa test; Ledoit–Wolf shrinkage**: tools that survive p comparable to n.

## Where it comes back

| Idea | Returns in |
|---|---|
| sparsity; the graphical lasso's penalty | 32 |
| thousands of correlated tests | 33 |
| Mahalanobis matching | 36 |
| latent variables and measurement error | 41 |
| sparse PCA's computational barrier | 50 |
| Marchenko–Pastur; the spiked model; Ledoit–Wolf | 52 |
| proportional asymptotics | 59 |
| robust covariance in high dimensions | 60 |
| the Coverage Board | every part; 65 |
