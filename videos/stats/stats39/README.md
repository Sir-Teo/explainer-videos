# Statistics, Built — Part 39: Space

Part 39 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the nineteenth part of Stage III, Master's. Part 38's dependence ran in one
direction, from the past. In space it runs in every direction, with no natural order to filter along. This part
covers:
- random fields, Bochner's theorem and variograms;
- kriging as the best linear unbiased predictor, and as a Gaussian-process posterior;
- the Matérn family, and the parameter that cannot be learned;
- ML and REML, and scaling to a hundred thousand locations (Vecchia, NNGP, GMRFs and the SPDE);
- areal data and disease maps; point patterns and Snow's map;
- spatial confounding; space–time covariances; Gaussian processes in machine learning;
- honest prediction.

The part builds `statkit.spatial` and an instrument, the field surface (`FieldSurface`): a kriging or GP surface on a
grid, with its standard error as a darkening overlay and the data as dots in the same coordinates. Its real data are:
- the Meuse flood plain's 155 topsoil samples of heavy metals, and the 3,103-node prediction grid (Rikken & van Rijn
  1993, as distributed with R's `sp` package, GPL ≥ 2);
- John Snow's 1854 cholera deaths and pumps, as digitized by Waldo Tobler (from R's `HistData`, GPL-2).

It opens with Krige (1951): valuing blocks of ore from boreholes by weights that account for how grades covary with
each other and with the block. Then the World's pollution field, hidden but for 300 stations.

From there the part covers:
- **Spatial data.**
  - Tobler's first law; Cressie's three kinds of data.
  - Meuse's log zinc, high by the river; the World's field, 20 + 3 × traffic + a Matérn field (σ² = 6.25, ρ = 1.5,
    ν = 3/2) with a nugget of 0.64.
  - Under the nominal known covariance, the trend-removed station average estimates an ensemble mean level with effective sample size 5.7: model-based SE 1.10, not
    σ/√n = 0.15. This is not the prediction error for the realized island's spatial average; that requires covariances with the target area average.
- **Random fields.** Stationarity, isotropy, Gaussianity; Bochner's theorem; four seeded fields of different
  smoothness and range; the standard families.
- **Variograms.**
  - Matheron's estimator. Meuse's log zinc, spherical fit by Cressie's WLS: nugget 0.054, partial sill 0.585 (total sill 0.639), range 0.90 km.
  - Robust (Cressie–Hawkins) estimates are close, consistent with the logs reducing large-value influence; agreement is not proof that no outliers remain.
  - Raw directional variograms: lowest along the river (north-east), highest across it. A river-distance trend can mimic anisotropy; these alone do not identify geometric residual anisotropy.
  - The World's empirical variogram tracks the truth at short lags and keeps rising beyond.
- **Kriging.**
  - The BLUP derived with a Lagrange multiplier; simple, ordinary and universal.
  - Universal kriging of Meuse with √(river distance): β̂ = 7.01 − 2.61 √d; the standard-error map.
  - Leave-one-out RMSE of log zinc: overall mean 0.724, inverse-distance weighting 0.514, ordinary kriging 0.393,
    universal 0.375.
  - The World: RMSE 0.54 over the island against 2.64 for the traffic trend alone; the REML plug-in's 90% intervals
    cover 83% of the island in this one field.
  - Known-covariance simple kriging equals Gaussian conditioning. Universal kriging corresponds to a flat trend prior when the design and resulting posterior are proper. BLUP moment properties and Gaussian interval coverage are distinct. Latent-field prediction excludes a new measurement nugget; observed-value validation includes it.
- **Matérn and identifiability.**
  - The family, its closed forms, its spectrum and Whittle's SPDE; Stein's "use the Matérn".
  - 80 seeded fields (n = 300, exponential, ρ = 0.3, σ² = 1): ML estimates of ρ and σ² vary by 38% and 34% along a
    ridge, while σ²/ρ varies by 9% (Zhang 2004). This fixed-n experiment illustrates variability, not a proof of consistency. For Gaussian Matérn fields of known ν in dimensions at most three on a fixed bounded domain, variance and range cannot both be consistently estimated under infill. Equivalent Gaussian measures are not identical finite-dimensional distributions; increasing the domain changes the result. Finite predictions still depend on both parameters.
  - Kriging the World along the ridge (ρ × 2 with σ² × 8, or ρ × 0.7 with σ² × 0.34) leaves the RMSE at 0.51–0.53 and
    coverage at 87–90%. Off it, ρ × 2 alone gives 63% and ρ × 0.5 alone 98%.
- **Likelihood.**
  - ML and REML (Patterson & Thompson). On the World with ν = 3/2: REML ρ̂ = 2.09, σ̂² = 8.30, τ̂² = 0.72,
    β̂ = (19.35, 2.83); ML ρ̂ = 1.96, σ̂² = 7.11.
  - Choosing ν: REML log-likelihoods −457.68 (ν = 1/2), −455.69 (3/2, the truth), −457.11 (5/2).
  - The cubic wall: likelihood time and the n = 100,000 cubic extrapolation are machine- and load-dependent measurements, not an actual exact 100,000-site fit. The covariance matrix alone would require 80 GB. REML need not always give larger covariance parameters or eliminate all variance bias.
- **Scaling.**
  - Vecchia's approximation. On 2,000 points (ν = 3/2, with a nugget), the log-likelihood error is 523 with m = 1,
    35 with m = 10 and 2.8 with m = 30. The displayed range profiles have nearby grid maxima in this realization. Approximation can move estimates and distort curvature in either direction. The fast candidate search selects earlier points among 4m nearest overall and can use fewer than m, rather than always finding the exact m nearest predecessors.
  - 100,000 jittered land-node locations provide a timing benchmark with m = 10. Values reuse selected grid-node latent values, so this is not an exact Matérn simulation at the jittered coordinates; timing depends on the machine and load.
  - NNGP; tapering, low rank, and Heaton et al.'s competition.
- **GMRFs and the SPDE.**
  - Precision zeros as conditional independence (Besag 1974).
  - A 60 × 40 SPDE lattice: 30,204 nonzeros of 5.76 million. Conditioning on 150 noisy values by one sparse solve
    gives a reconstruction error reported below after regenerating the coherent-prior example. Its deterministic scale gives unit average marginal prior variance; the realized sample is not divided by its random spatial SD. This small teaching sampler uses dense Cholesky, while conditioning is sparse. The free-boundary grid approximates a whole-space Matérn/SPDE construction. Practical range √(8ν)/κ is twice the scale ρ used in this part's Matérn definition.
  - Lindgren, Rue & Lindström; INLA.
- **Areal data.**
  - Moran's I for the World's 200 towns' log case rates: 0.085, permutation p = 0.018 under an exchangeable-value reference. Unequal expected counts imply unequal raw-rate variance, so that reference is not the null of independent equal-risk Poisson counts. This is exploratory. The plotted curve is a normal approximation to permutation moments, not the actual permutation distribution.
  - SMRs: the smallest quarter of towns range from 0 to 3.16; 20 towns have no cases.
  - Compatible CAR conditionals require a symmetric positive precision T⁻¹(I−ρW); intrinsic normalized CAR needs constraints and a proper posterior. The teaching BYM-style fit uses fixed precisions, a small proper ridge and posterior modes, rather than integrated posterior means. CAR, SAR and their parameter restrictions are distinct. The smoothed relative risks have RMSE 0.18 against the truth, against 0.58 for the raw SMRs,
    and are too flat (slope 0.56): shrinkage's bias.
- **Point patterns.**
  - Snow's map: 359 of 578 digitized deaths (62%) are nearest the Broad Street pump by straight-line map distance; the next pump has 64. These are not reconstructed walking-distance catchments or all London deaths.
  - Ripley's K and Besag's L. Snow's deaths exceed the pointwise 95% reference from 199 fixed-count uniform patterns at the displayed scales. The case-derived window and many-distance comparison make this exploratory, not a calibrated simultaneous global test.
  - But CSR is the wrong null: the inhomogeneous K and case–control designs. Cox processes and the LGCP.
- **Spatial confounding.** 60 seeded fields, n = 250, with an unmeasured spatial confounder correlated 0.8 with the
  exposure and the same range, β = 1.
  - OLS averages 1.80 (SD 0.21); spatial GLS with a Matérn random effect by REML averages 1.81 (SD 0.08): just as
    biased, and more confident.
  - With the spatial term independent of the exposure, both are unbiased (1.01 and 1.02), and GLS's SD is 0.13
    against OLS's 0.37.
  - Hodges & Reich; Paciorek's scales; restricted spatial regression; spatial+. Fine-scale exposure variation needs identifying assumptions, and no random-effect model automatically removes confounding. RSR's OLS equivalence concerns the standard Gaussian linear formulation; interval undercoverage is a risk, not a universal identity.
- **Space and time.**
  - Separable covariances; Gneiting's family, whose spatial correlation spreads with the time lag.
  - The World's daily readings: the island-wide daily mean has a lag-1 ACF of 0.72 (AR(1) weather with φ = 0.7).
    Daily anomaly correlations are approximately distance-independent, with model value 0.64 = 4/(4 + 1.5²). A common weather effect contributes constant spatial covariance but cancels from same-day spatial differences and is invisible to that variogram. The daily station average is not a direct census of the island's spatial mean.
  - Dynamic models; advection–diffusion SPDEs.
- **Gaussian processes in machine learning.**
  - The dictionary; the marginal likelihood's Occam factor; emulators (Sacks et al. 1989).
  - Expected improvement (Jones, Schonlau & Welch 1998): on a two-dip function it finds x = −0.48 (true −0.47) within
    eight evaluations counting the three initial observations; eleven evaluations are made overall. The 401-point grid is a reference at that resolution, not a proof of a continuous global optimum.
  - Snoek et al.; Neal's infinite networks; kernel ridge and splines.
- **Honest prediction.**
  - The plug-in variance; Zimmerman & Cressie.
  - Kriging the World's stations: random 10-fold CV RMSE 0.99 against 1.34 for 3 × 3 spatial blocks, whose held-out
    stations are 2.8 times further from the training data. The covariance and trend are refitted inside each training fold. Empirical coverage is reported separately for each validation design after the rerun; distance-aware variance does not guarantee calibration.
  - Meuse's LOO z-scores under universal kriging: mean z² 1.05, 90% coverage 86%, with a long right tail.
  - The Board; a checklist.

Data:
- Meuse and Snow's map are the Museum's;
- the pollution field, its stations, the daily readings and the towns' counts are the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.spatial`** ([`explainer/stats/kit/spatial.py`](../../../explainer/stats/kit/spatial.py)), checked in
  `tests/test_stats_kit_spatial.py`:
  - **Covariances and variograms:** Matérn; the classical and robust empirical variograms; exponential, spherical and
    Matérn models fitted by Cressie's WLS.
  - **Kriging and likelihood:** simple, ordinary and universal kriging with the GLS trend and its covariance (checked
    against Gaussian conditioning); the Gaussian log-likelihood; ML and REML fits; exact and Vecchia likelihoods (a
    k-d tree version for large n).
  - **Lattices and areas:** the SPDE precision on a grid, sampling by dense Cholesky in this small implementation and conditioning by a sparse solve; Moran's I with
    a permutation test; BYM-style smoothing of relative risks.
  - **Points, space–time and design:** Ripley's K and CSR envelopes; Gneiting's space–time covariance; expected
    improvement.
- **The World** gains its `pollution` block (the field on a 0.1-unit grid by circulant embedding, 300 stations, a
  year of daily readings with AR(1) weather).
- **The Museum** gains `meuse()`, `meuse_grid()`, `meuse_river()` and `snow_map()`.
- **The field surface** (`FieldSurface` in `explainer/stats/viz.py`).

The Coverage Board gains five rows:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| kriging 90% PI, true covariance | Matérn ν = 5/2 fields, n = 200 | 89.9% | kept |
| kriging PI, REML plug-in | same | 88.9% | broken (a small, systematic shortfall) |
| kriging PI, exponential fitted | same | 97.9% | conservative |
| OLS 90% CI for a covariate | spatially correlated errors, n = 200 | 28.0% | broken |
| GLS (REML) CI for the covariate | same | 86.0% | kept |

The local field gallery now expands its circulant embedding until its eigenvalues are nonnegative to numerical tolerance, instead of truncating substantive negative modes. The existing World generator retains a very fine spectral approximation: at nominal variance 6.25 its maximum covariance perturbation from spectral truncation is about 0.000125. It is distinguished from the exact nominal Matérn model used in the independent-field Board simulations. Continuous Bochner covariance representations, mean-square smoothness, boundary approximations, Gneiting parameter ranges and fixed-domain assumptions are explicit.

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats39.compute   # once (about half an hour)
python tools/build.py stats39 -q l                         # fast 480p preview
python tools/build.py stats39                              # 1080p30 -> renders/stats39.mp4
python tools/qa_scene.py stats39 Kriging
python tools/lecture_length.py stats39 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Krige's boreholes | 1951 |
| 1 | Spatial data | n_eff = 5.7 of 300 |
| 2 | Random fields | Bochner |
| 3 | Variograms | nugget 0.054, partial sill 0.585 (total sill 0.639), range 0.90 km |
| 4 | Kriging | LOO RMSE 0.724 → 0.375 |
| 5 | Matérn and identifiability | CV 38% vs 9% |
| 6 | Likelihood | ν = 3/2 wins; 27 hours |
| 7 | Scaling | 100,000 sites in 4.6 s |
| 8 | GMRFs and the SPDE | 30,204 of 5.76M |
| 9 | Areal data | I = 0.085; RMSE 0.58 → 0.18 |
| 10 | Point processes | 359 of 578 |
| 11 | Spatial confounding | 1.80 vs 1.81 |
| 12 | Space and time | 0.64 at every distance |
| 13 | GPs in machine learning | 8 evaluations vs 401 |
| 14 | Honest prediction | 0.99 vs 1.34 |
| 15 | Outro | — |

## Sources

- **Geostatistics.**
  - D. Krige, *J. Chem. Metall. Min. Soc. S. Afr.* 52 (1951); G. Matheron, *Traité de géostatistique appliquée*
    (1962–63), *Econ. Geol.* 58 (1963); L. Gandin (1963).
  - W. Tobler, *Econ. Geogr.* 46 (1970); N. Cressie, *Statistics for Spatial Data* (rev. ed. 1993); N. Cressie,
    *Math. Geol.* 17 (1985); N. Cressie & D. Hawkins, *Math. Geol.* 12 (1980).
  - S. Bochner (1933); B. Matérn, *Spatial Variation* (1960); P. Whittle, *Biometrika* 41 (1954).
  - M. Stein, *Interpolation of Spatial Data* (1999); H. Zhang, *JASA* 99 (2004).
  - K. Mardia & R. Marshall, *Biometrika* 71 (1984); H. Patterson & R. Thompson, *Biometrika* 58 (1971);
    D. Zimmerman & N. Cressie, *Ann. Inst. Stat. Math.* 44 (1992).
  - M. Rikken & R. van Rijn (1993); E. Pebesma, *Comput. Geosci.* 30 (2004) (gstat).
- **Scaling.**
  - A. Vecchia, *JRSS B* 50 (1988); M. Stein, *Ann. Stat.* 30 (2002) (screening); A. Datta, S. Banerjee, A. Finley &
    A. Gelfand, *JASA* 111 (2016); M. Katzfuss & J. Guinness, *Stat. Sci.* 36 (2021).
  - M. Heaton et al., *JABES* 24 (2019).
  - J. Besag, *JRSS B* 36 (1974); H. Rue & L. Held, *Gaussian Markov Random Fields* (2005); F. Lindgren, H. Rue &
    J. Lindström, *JRSS B* 73 (2011); H. Rue, S. Martino & N. Chopin, *JRSS B* 71 (2009).
- **Areas and points.**
  - P. Moran, *Biometrika* 37 (1950); J. Besag, J. York & A. Mollié, *Ann. Inst. Stat. Math.* 43 (1991).
  - B. Ripley, *J. Appl. Prob.* 13 (1976); D. Cox, *JRSS B* 17 (1955); J. Møller, A. Syversveen & R. Waagepetersen,
    *Scand. J. Stat.* 25 (1998); A. Baddeley, J. Møller & R. Waagepetersen, *Stat. Neerl.* 54 (2000).
  - J. Snow, *On the Mode of Communication of Cholera* (2nd ed. 1855); P. Diggle (2013).
- **Confounding.**
  - J. Hodges & B. Reich, *Am. Stat.* 64 (2010); C. Paciorek, *Stat. Sci.* 25 (2010); E. Hanks et al.,
    *Environmetrics* 26 (2015); K. Khan & C. Calder, *JASA* 117 (2022); E. Dupont, S. Wood & N. Augustin,
    *Biometrics* 78 (2022).
- **Space–time.**
  - T. Gneiting, *JASA* 97 (2002); N. Cressie & C. Wikle, *Statistics for Spatio-Temporal Data* (2011).
- **Gaussian processes.**
  - J. Sacks, W. Welch, T. Mitchell & H. Wynn, *Stat. Sci.* 4 (1989); D. Jones, M. Schonlau & W. Welch, *J. Global
    Optim.* 13 (1998); J. Snoek, H. Larochelle & R. Adams, *NeurIPS* (2012).
  - C. Rasmussen & C. Williams (2006); R. Neal, *Bayesian Learning for Neural Networks* (1996); D. MacKay, *Neural
    Comput.* 4 (1992); G. Kimeldorf & G. Wahba, *Ann. Math. Stat.* 41 (1970); A. O'Hagan, *JRSS B* 40 (1978).
- **Honest prediction.**
  - D. Roberts et al., *Ecography* 40 (2017).

## Problems and solutions

1. **The ordinary kriging variance.** Minimize λᵀKλ − 2λᵀk₀ + C(0) + 2m(1ᵀλ − 1). Setting the gradient to zero gives
   Kλ + m1 = k₀, which with 1ᵀλ = 1 is the system in chapter four. Substituting λᵀKλ = λᵀk₀ − m gives
   σ²_OK = C(0) − λᵀk₀ − m.
2. **Screening on a line.** With C(h) = e^{−|h|}, the process is Markov (it is the stationary Ornstein–Uhlenbeck
   process). Given Z(s₁) and Z(s₂), Z(s₀) is independent of every value outside [s₁, s₂]. So the conditional mean,
   which is simple kriging, has zero weight on them.
3. **Brownian motion's variogram.** γ(h) = ½E[W(t + h) − W(t)]² = σ²h/2, which grows without bound: no sill. It is a
   valid variogram (intrinsically stationary) without a covariance function, the reason geostatistics prefers γ.
4. **Moran's mean.** Under random permutation, E[e_i e_j] for i ≠ j is −Σe_k²/(n(n − 1)), since Σ_{i≠j} e_i e_j =
   −Σe_k². So E[eᵀWe] = −S₀ Σe_k²/(n(n − 1)) when W has a zero diagonal, and E[I] = (n/S₀)(−S₀/(n(n − 1))) =
   −1/(n − 1).
5. **K under CSR.** For a homogeneous Poisson process of intensity λ, by Slivnyak's theorem the other points seen from
   a typical point are again Poisson(λ). The expected number within r is λπr², so K(r) = πr² and L(r) = r.
6. **Expected improvement.** With f = μ + sZ, (f* − f)₊ = s(z − Z)₊ where z = (f* − μ)/s. Then
   E(z − Z)₊ = ∫_{−∞}^{z} (z − u)φ(u) du = zΦ(z) + φ(z). Multiplying by s gives (f* − μ)Φ(z) + sφ(z).

## Glossary

- **Random field; stationary; isotropic**: random values over a region; a constant mean and a covariance depending on
  displacement only; on distance only.
- **Bochner's theorem**: covariances are the Fourier transforms of non-negative measures.
- **Variogram; nugget, sill, range**: half the expected squared difference at lag h; the jump at zero, the plateau,
  the distance where it is reached.
- **Anisotropy**: dependence that differs by direction.
- **Kriging (simple, ordinary, universal)**: the BLUP with a known mean, an unknown constant, an unknown trend.
- **Matérn; smoothness ν**: the covariance family with a differentiability parameter.
- **Infill asymptotics; microergodic parameter**: more data in a fixed region; the combination σ²/ρ^{2ν} it can
  learn.
- **REML**: likelihood of error contrasts that removes fixed-trend parameters; a scale correction for known correlation shape does not imply unbiased estimation of every covariance parameter.
- **Vecchia approximation; NNGP; screening**: conditioning on a few nearest earlier neighbours; its use as a prior;
  why it works.
- **GMRF; SPDE; INLA**: a Gaussian field with sparse precision; Matérn fields as solutions of a stochastic PDE;
  nested Laplace approximations.
- **Moran's I; CAR; SAR; BYM**: spatial correlation for areas; conditional and simultaneous autoregressions; the
  disease-mapping model.
- **CSR; Ripley's K; Besag's L; Cox process; LGCP**: complete spatial randomness; neighbour counts by distance; the
  linearized K; a Poisson process with random intensity; a log-Gaussian one.
- **Spatial confounding; restricted spatial regression**: a random effect competing with a smooth covariate; forcing
  it orthogonal.
- **Separable; Gneiting covariance**: space–time covariance as a product; a family with interaction.
- **Emulator; expected improvement; Bayesian optimization**: a GP surrogate for a simulator; the acquisition rule;
  the loop.
- **Spatial block cross-validation**: holding out regions, to test extrapolation.

## Where it comes back

- **Part 40**: shared frailties, random effects for lifetimes.
- **Part 41**: prediction at unmeasured places as imputation; measurement error as a nugget.
- **Part 44**: Brownian motion, the first Gaussian process.
- **Part 53**: Gaussian-process priors and how fast posteriors contract.
- **Part 60**: predicting in a new region as distribution shift.
