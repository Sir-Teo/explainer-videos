# Statistics, Built — Part 4: Matrices for Statistics

Part 4 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. This part is the toolkit every later part
reaches into.

It opens with the hat matrix H = X(XᵀX)⁻¹Xᵀ of a full-column-rank regression on the World's families. Because H is a projection, its
eigenvalues can only be 0 and 1. From that one fact come degrees of freedom, the n − p of the residual variance,
χ² quadratic forms, Student's t, regression and the analysis of variance.

Every identity on screen is checked numerically in [`compute.py`](compute.py), and every distributional claim against
a seeded simulation.

**Built in this part:** the projection lab (`ProjectionLab` in [`common.py`](common.py)). It is a turnable ℝ³, drawn
with `NSpace`, that shows:
- a column space;
- a data vector, its projection and the residual;
- the right angle between the residual and the column space.

It is used for centring (projection onto **1**), for a plane spanned by two columns, and for Gram–Schmidt.

## Build it

```bash
python -m videos.stats.stats4.compute          # once: every computed item (seconds; cached in .cache/stats4)
python tools/build.py stats4 -q l              # fast 480p preview
python tools/build.py stats4                   # 1080p30 -> renders/stats4.mp4
python tools/qa_scene.py stats4 Projection     # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats4 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | The hat matrix | 40 World families. H as a heat map; H² = H ⇒ eigenvalues 0 and 1; tr H = p. 2,000 simulated data sets: E RSS = (n − p)σ². | eigenvalues two 1s, 38 0s; RSS/σ² averages 37.95; RSS/n is 0.949σ² vs RSS/(n − p) 0.999σ² |
| 1 | Vectors as data | A sample as a point in ℝⁿ; centring as projection onto **1** in the lab; why n − 1; the upgrade card for Part 1's r = cos θ, and slope = r s_y/s_x; the data matrix's two views. | — |
| 2 | Projections | P = A(AᵀA)⁻¹Aᵀ derived; the lab; Pythagoras; Gram–Schmidt and QR; eigenvalues of a projection; ANOVA as nested projections; leverage. | 19.00 = 8.71 + 10.29; SS 3,736 = 946 + 2,790, R² = 0.253; leverages sum to 2 |
| 3 | Trace tricks | tr(AB) = tr(BA); E[xᵀAx] = tr(AΣ) + μᵀAμ (Monte Carlo); MSE = tr Cov + bias²; rank = trace; tr and det of Σ. | 13.456 exact vs 13.481 MC; det S = 1,677 = λ₁λ₂ |
| 4 | The spectral theorem | Statement and proof sketch; ellipses of the families' covariance; the Rayleigh quotient around the circle; Mahalanobis distance and whitening; power iteration. | λ = 85.06, 19.71; 3.75% outside the χ²₂ 95% circle; power iteration converges in about 5 steps |
| 5 | Positive semidefinite matrices | Covariances are PSD; an impossible "correlation" matrix, repaired by Higham's Dykstra-corrected alternating projections; Cholesky makes correlated normals; Var(Ax) = AΣAᵀ; the Loewner order. | λ_min = −0.8 → nearest valid matrix with all correlations ±0.5; simulated r = 0.795 for target 0.8 |
| 6 | The SVD | Orthogonal maps and stretches on the unit circle (reflections allowed in general); Mᵀ M; Eckart–Young; low-rank approximations of the World's population map; PCA as the SVD of the centred data. | errors match √(Σ_{k>r} σ²_k) exactly; first PC 81% |
| 7 | Generalized inverses | Minimum-norm solution of x₁ + 2x₂ = 4; Moore–Penrose; the dummy-variable trap and estimable contrasts; the ridge path converging to X⁺y. | A⁺b = (0.8, 1.6); region difference 11.00 in every solution |
| 8 | Block matrices | Schur complement; block inverse and determinant; Woodbury and Sherman–Morrison; Frisch–Waugh–Lovell on mother's height given father's; leave-one-out residuals eᵢ/(1 − hᵢᵢ). | FWL 0.4552 = full-regression coefficient; LOO formula vs 40 refits: 1e−12; PRESS 3,105 vs RSS 2,790 |
| 9 | Kronecker products and vec | A ⊗ B; site × time covariance; vec(ABC) = (Cᵀ ⊗ A)vec B; eigenvalues are products; a simulated space–time field. | max error 9e−16 |
| 10 | Matrix calculus | ∂aᵀx, ∂xᵀAx, least squares in three lines; the Hessian 2XᵀX; ∂ log det Σ = Σ⁻¹; the Gaussian MLE of Σ; score and Fisher information for μ. | Σ̂_MLE for 400 families |
| 11 | Quadratic forms in normal vectors | zᵀPz ~ χ²_rank; 20,000 simulations of zᵀHz and zᵀ(I − H)z; Cochran's theorem (1934); noncentral χ² and power; independence of x̄ and s² (normal) vs strong dependence (exponential); Student's t from projections. | means 3.01 and 6.92; power 25% and 85% at ‖Pμ‖ = 2, 4; corr(x̄, s²) −0.002 vs 0.70 |
| 12 | Conditioning and numerics | 0.1 + 0.2; condition numbers; κ(XᵀX) = κ(X)²; normal equations vs QR on near-collinear columns (exact floating-point errors depend on the platform); centring a quadratic in height; catastrophic cancellation in the one-pass variance; how software solves least squares. | at κ = 2×10⁷, error 0.17 vs 4×10⁻¹⁰; κ 6.2×10⁶ → 220 after centring; offset 10⁸: s² = 90.20 vs 93.26 |
| 13 | Outro | Recap, payoffs, problems, references, the Transcript, Part 5's question. | — |

## Sources

- **The hat matrix.** D. C. Hoaglin & R. E. Welsch, "The hat matrix in regression and ANOVA", *The American
  Statistician* 32 (1978).
- **Spectral theorem.** A.-L. Cauchy (1829); later Sylvester and Hilbert. The proof sketched on screen is the
  variational one (maximize uᵀAu on the sphere).
- **Mahalanobis.** P. C. Mahalanobis, "On the generalised distance in statistics" (1936).
- **Generalized variance.** S. S. Wilks (1932).
- **SVD.** C. Eckart & G. Young, "The approximation of one matrix by another of lower rank", *Psychometrika* 1
  (1936).
- **Pseudoinverse.** E. H. Moore (1920); R. Penrose, "A generalized inverse for matrices", *Proc. Camb. Phil. Soc.*
  51 (1955). Ridge: A. Hoerl & R. Kennard (1970).
- **Nearest correlation matrix.** N. J. Higham, *IMA J. Numer. Anal.* 22 (2002).
- **Woodbury.** M. Woodbury (1950); J. Sherman & W. Morrison (1950).
- **Frisch–Waugh–Lovell.** R. Frisch & F. Waugh (1933); M. Lovell (1963).
- **Cochran.** W. G. Cochran, "The distribution of quadratic forms in a normal system" (1934).
- **Independence of x̄ and s².** R. C. Geary (1936) characterizes the normal by it.
- **Cholesky.** A.-L. Cholesky's method, published posthumously by Benoît (1924).
- **Numerics.**
  - J. von Neumann & H. Goldstine (1947).
  - J. H. Wilkinson, *Rounding Errors in Algebraic Processes* (1963).
  - G. Golub, "Numerical methods for solving linear least squares problems" (1965).
  - B. P. Welford (1962).
  - L. Trefethen & D. Bau, *Numerical Linear Algebra* (1997).
- **Textbooks.**
  - D. Harville, *Matrix Algebra From a Statistician's Perspective* (1997).
  - S. Searle & A. Khuri, *Matrix Algebra Useful for Statistics* (2nd ed., 2017).
  - J. Magnus & H. Neudecker, *Matrix Differential Calculus* (3rd ed., 2019).
  - G. Seber, *A Matrix Handbook for Statisticians* (2008).
  - G. Strang, *Introduction to Linear Algebra*.

## Problems and solutions

**1. The complementary projection.**

*Solution.*
- **It is a projection.** (I − P)² = I − 2P + P² = I − P, and (I − P)ᵀ = I − P.
- **The two are orthogonal.** P(I − P) = P − P² = 0.
- **Eigenvalues.** If Pv = λv with λ ∈ {0, 1}, then (I − P)v = (1 − λ)v. So the eigenvalues of I − P are also 0 and
  1, with the roles swapped. Hence rank(I − P) = n − rank P.

**2. tr H = p.**

*Solution.* tr(X(XᵀX)⁻¹Xᵀ) = tr((XᵀX)⁻¹XᵀX) = tr(I_p) = p, by cycling X from the front to the back.

**3. E s² = σ².**

*Solution.* (n − 1)s² = xᵀ(I − J/n)x. Apply E[xᵀAx] = tr(AΣ) + μᵀAμ with Σ = σ²I and μ = μ₀**1**:
- tr((I − J/n)σ²) = σ²(n − 1);
- (I − J/n)**1** = **0**, so the mean term vanishes.

So E[(n − 1)s²] = (n − 1)σ², and E s² = σ². No normality is needed.

**4. An ellipse.**

*Solution.* For A = [[2, 1], [1, 2]]:
- eigenvalue 3 with eigenvector (1, 1)/√2;
- eigenvalue 1 with eigenvector (1, −1)/√2.

The ellipse xᵀA⁻¹x = 1 has semi-axes √3 along (1, 1) and 1 along (1, −1), tilted at 45°.

**5. Sherman–Morrison.**

*Solution.* Multiply (A + uvᵀ) by A⁻¹ − A⁻¹uvᵀA⁻¹/(1 + vᵀA⁻¹u):

I + uvᵀA⁻¹ − [uvᵀA⁻¹ + u(vᵀA⁻¹u)vᵀA⁻¹]/(1 + vᵀA⁻¹u)
= I + uvᵀA⁻¹ − u(1 + vᵀA⁻¹u)vᵀA⁻¹/(1 + vᵀA⁻¹u)
= I.

This needs 1 + vᵀA⁻¹u ≠ 0.

**6. Σ(zᵢ − z̄)² ~ χ²_{n−1}.**

*Solution.* Σ(zᵢ − z̄)² = zᵀ(I − J/n)z. Here I − J/n is a projection (symmetric and idempotent, since J² = nJ), with
trace n − 1 and so rank n − 1. By chapter 11, zᵀPz ~ χ²_{rank P} for z ~ N(0, I).

## Where it comes back

| Idea | Returns in |
|---|---|
| projections, n − p, leverage | 8, 12, 13, 30 |
| Schur complements, conditional covariance | 5, 25 |
| the spectral theorem, Mahalanobis, PCA | 5, 31 |
| the SVD, low rank, ridge | 19, 31, 32, 52 |
| Cochran's theorem, t and F | 8, 12, 13 |
| matrix calculus, information | 9, 22, 23 |
| Woodbury, Kronecker structure | 25, 38, 39 |
| conditioning, QR | 21, 23 |
