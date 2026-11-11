# Computer Science, Built — Part 52: Computing with Real Numbers

Part 52 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act X, *Horizons and Trust*. In 2000 a journal named the ten
algorithms that most shaped twentieth-century science and engineering, and eight of them compute with real numbers.
With rounding in every operation, the question Part 4 left open is which answers we can trust; the answer separates a
problem's conditioning from an algorithm's backward stability. We build the classic algorithms small enough to read,
from pivoted elimination and Householder's mirrors to the shifted QR algorithm, conjugate gradients, multigrid,
Newton's fractal, Chebyshev interpolation, stiff and symplectic integrators, and mixed-precision refinement, and run
each one.

The instruments are in `explainer/cs/numeric/` (tested in `tests/test_cs52_numeric.py`):
* `linalg.py`: relative condition numbers of functions and of Hilbert matrices; forward against backward error on
  Hilbert systems; LU with and without partial pivoting, returning the growth factor; Wilkinson's matrix and growth
  on random matrices, and on Wilkinson's matrix perturbed by Gaussian noise; Cholesky; Householder QR (each mirror
  kept for drawing) and Givens rotations; classical and modified Gram–Schmidt; least squares by the normal equations
  against QR; the SVD of a blur matrix, with truncated-SVD regularization; and the randomized SVD of Halko, Martinsson
  and Tropp, timed against a full SVD.
* `eigen.py`: power and inverse iteration; Householder reduction to Hessenberg form; the QR algorithm, unshifted and
  with Wilkinson's shift, with deflation, recording the last subdiagonal entry at every step and the measured order
  of convergence.
* `iterative.py`: the 2D Poisson matrix; steepest descent and conjugate gradients, with Jacobi and SSOR
  preconditioners and CG's bound; GMRES on a nonsymmetric convection–diffusion problem; CSR storage; Cholesky fill-in
  under row-by-row, reverse Cuthill–McKee, minimum-degree and nested-dissection orderings (factored by SciPy's
  SuperLU); the weighted-Jacobi error spectrum in 1D; and a geometric multigrid V-cycle in 2D (full-weighting
  restriction, bilinear interpolation, two sweeps before and after).
* `analysis.py`: bisection, secant and Newton raced on √2; Newton's basins for z³ − 1; Runge's function interpolated
  at equispaced and Chebyshev points, evaluated by the barycentric formula; trapezoid, Simpson, Gauss–Legendre and
  Monte Carlo quadrature, and adaptive Simpson; Dormand–Prince RK45 with step control; stiffness against backward
  Euler; the stability regions of Euler, RK4 and backward Euler; and a thousand Kepler orbits by RK4 and by leapfrog.
* `speed.py`: BLAS levels 1, 2 and 3 timed through NumPy, with their arithmetic intensity; and iterative refinement
  with an LU factorization in single precision and residuals in double.

## Chapters

* **Hook.** Dongarra and Sullivan's ten algorithms of the twentieth century (2000), eight of them numerical. Two
  equations, 10⁻²⁰x₁ + x₂ = 1 and x₁ + x₂ = 2, whose answer is almost exactly (1, 1): elimination as taught gives
  x₁ = 0, x₂ = 1; swapping the rows first gives 1 and 1. The problem is well conditioned; the algorithm was unstable.
  The part's six objectives.
* **1. Conditioning and stability.** The relative condition number derived as κ = |x f′(x)/f(x)|, belonging to the
  problem alone. Four problems, computed: x − 1 at x = 1.000001 (κ = 1,000,001, Part 4's cancellation), √x (0.5),
  eˣ at x = 100 (100), tan x at x = 1.5707 (16,306); about log₁₀ κ of sixteen digits are lost. The matrix condition
  number ‖A‖‖A⁻¹‖ = σ_max/σ_min derived (Turing, 1948), and the unit circle turned into an ellipse. Hilbert's matrix:
  κ = 1.6 × 10⁴, 1.5 × 10¹⁰ and 1.6 × 10¹⁶ at sizes 4, 8 and 12, so about 12, 6 and 0 digits survive. Backward
  stability: the computed answer is the exact answer for nearby data.
* **2. Backward error analysis.** Wilkinson's model fl(a ∘ b) = (a ∘ b)(1 + δ), |δ| ≤ u = 2⁻⁵³; a sum of three
  numbers is the exact sum of data changed by about two roundings. Forward error ≲ κ × backward error derived; for
  Ax = b the residual gives the backward error η = ‖r‖/(‖A‖‖x̂‖) exactly, and the forward error is at most κη. On
  Hilbert systems solved by LAPACK's pivoted elimination, η stays between 2.4 × 10⁻¹⁷ and 6.1 × 10⁻¹⁷, the forward
  error climbs from 2.0 × 10⁻¹³ at n = 4 to 0.055 at n = 12, always below κη; 12, 7 and 1 correct digits at sizes 4,
  8 and 12.
* **3. Gaussian elimination.** Elimination on a 3 × 3 example is A = LU with the multipliers 2, 4 and 3 in L; the
  cost Σ 2(n − k)² ≈ ⅔n³, triangular solves about n² each, and the inverse three times dearer ("to solve, never
  invert"). The tiny pivot [[ε, 1], [1, 1]]: at ε = 10⁻²⁰ the computed factors are the exact factors of a matrix with
  a 0 where the 1 was; the largest error without pivoting grows from 2.8 × 10⁻¹³ at ε = 10⁻⁴ to 1.0 at ε = 10⁻²⁰,
  with partial pivoting it stays at most 2.2 × 10⁻¹⁶. The growth factor ρ ≤ 2ⁿ⁻¹ derived and attained by Wilkinson's
  matrix (9.2 × 10¹⁸ at n = 64), against a mean of 4.2 and a largest of 6.4 over 50 random 64 × 64 matrices
  (Trefethen and Schreiber, 1990; why growth is small in practice is unproved). Cholesky derived on a 2 × 2 matrix;
  n³/3 flops against LU's 2n³/3 and Householder QR's 4n³/3.
* **4. Least squares and QR.** The normal equations Aᵀ(b − Ax̂) = 0 from the perpendicular, and κ(AᵀA) = κ(A)². QR
  (Golub, 1965) solves Rx̂ = (Qᵀb)₁:ₙ with κ(R) = κ(A): on a tall fit at κ = 10², 10⁴, 10⁶ and 10⁸ the normal
  equations' error reaches 0.37 against QR's 3.5 × 10⁻¹⁰. Householder's mirror carries (3, 4) to (−5, 0) and the
  second column (1, 3) to (−3, 1); one mirror per column. Givens rotations, one zero at a time: our 3 × 3 example
  needs 2, not 3. Classical against modified Gram–Schmidt on Hilbert matrices: ‖I − QᵀQ‖ is 1.4 for the classical
  version at n = 8, 0.16 for the modified one at n = 12 (proportional to κ, Björck 1967), and at worst 2.0 × 10⁻¹⁵
  for Householder.
* **5. The SVD.** Rotate, stretch, rotate: A = UΣVᵀ and κ = σ₁/σₙ. The truncated sum is the best rank-k
  approximation (Eckart and Young, 1936). The eighty singular values of a blur matrix: 56 above the rounding level
  80σ₁ε, 25 above the data's noise of 10⁻³. Undoing the blur of a two-box signal: κ(K) = 1.4 × 10¹⁶ and the naive
  solve's error is 1.1 × 10¹³ times the signal; truncation brings the error from 77 percent with one term to 19 percent
  at k = 23, then back up to 10¹³ with all eighty; Tikhonov's damping (1963). Golub–Kahan bidiagonalization (1965),
  the pseudo-inverse, and the SVD as the tool of last resort.
* **6. Eigenvalues: the QR algorithm.** Eigenvalues are roots of det(A − λI); Abel (1824) and the companion matrix
  mean every eigenvalue algorithm must iterate. On a random symmetric 8 × 8 matrix, the power method with
  |λ₂/λ₁| = 0.66 needs 36 steps to reach 10⁻¹³; inverse iteration with a shift 0.3 away needs 8. The QR algorithm
  (Francis; Kublanovskaya, 1961) as a similarity, with the off-diagonal entries fading on a log scale: 623 iterations
  for all eight eigenvalues unshifted. Hessenberg (here tridiagonal) form, Wilkinson's shift and deflation: 16
  iterations, not 623. The last subdiagonal entry goes 7.9 × 10⁻⁴ → 4.4 × 10⁻¹² → 2.8 × 10⁻³⁵ (about 3, 11 and 34
  digits; measured orders 3.66 and 3.04), cubic convergence; the largest error against LAPACK's eigenvalues is
  8.0 × 10⁻¹⁵ with shifts, 1.3 × 10⁻¹⁴ without.
* **7. Conjugate gradients.** Solving as going downhill on φ(x) = ½xᵀAx − bᵀx; steepest descent zigzags in a narrow
  bowl, CG arrives in two steps. CG as the best point of the Krylov space in the A-norm, with conjugate directions
  (Hestenes and Stiefel, 1952), and our instrument's ten-line loop. The bound 2((√κ − 1)/(√κ + 1))ᵏ, so steps grow
  like √κ. On the Poisson problem with 256, 1,024 and 4,096 unknowns (κ = 116, 441, 1,712; residual to 10⁻⁸):
  steepest descent 897, 3,297 and over 8,000 steps; CG 52, 101 and 198, against bounds of 103, 201 and 396.
  Preconditioning: Jacobi changes nothing (the diagonal is all fours); SSOR with ω = 1.5 cuts CG to 16, 26 and 47.
  GMRES (Saad and Schultz, 1986) through Arnoldi on a nonsymmetric convection–diffusion problem with 1,024
  unknowns: 10⁻⁸ in 82 steps.
* **8. Sparse matrices.** Poisson's equation and the five-point stencil derived from Taylor series. CSR storage and
  its matrix–vector loop, limited by memory bandwidth: the 64 × 64 grid's 4,096 unknowns have 20,224 nonzeros,
  259.1 kB in CSR against 134 MB dense. Fill-in by Parter's graph view (1961): an arrow matrix fills completely with
  the hub first and not at all with it last; row by row, the grid's Cholesky factor has 262,207 nonzeros, 13 times the
  matrix. Minimum degree (after Markowitz, 1957) and nested dissection (George, 1973). Measured with SciPy's SuperLU:
  262,207 row by row, 180,832 for reverse Cuthill–McKee, 63,266 for minimum degree, 89,164 for our nested dissection;
  when the grid side doubles from 32, fill grows ×8.0, ×7.7, ×5.5 and ×5.5.
* **9. Multigrid.** Weighted Jacobi on the 1D Poisson matrix with 63 unknowns multiplies sine mode k by
  1 − (4/3)sin²(kπ/2(n + 1)): at most ⅓ on the upper half of the modes, 0.999 on mode 1. The error spectrum after 0,
  1, 3 and 10 sweeps: mode 1 goes from 0.126 to 0.125, the upper half's largest from 1.96 to 2.9 × 10⁻⁵; relaxation
  smooths. A smooth mode on the fine grid is rough on the coarse one (Fedorenko, 1964; Brandt in the 1970s); the
  two-grid scheme, then recursion. The V-cycle on 2D Poisson with 225, 961, 3,969 and 16,129 unknowns: 0.20, 0.20,
  0.21 and 0.21 per cycle, ten cycles to a few parts in 10⁸ on every grid. Work W(n) = cn + W(n/4) = (4/3)cn, against
  n³, n² and n^(3/2) for dense, banded and nested-dissection or CG solvers; algebraic multigrid.
* **10. Roots and Newton's fractal.** Bisection gains one bit a step: 12.2 digits after 40 steps. Newton's step from
  the tangent and its quadratic error, from x₀ = 2 to 1.5 and 1.4167; the secant method's order 1.618. The race,
  computed: the secant method's digits 1.1, 1.8, 3.4, 5.7, 9.5, 15.7; Newton's 1.1, 2.6, 5.7, 11.8, 16.0; bisection
  7.0 after 20 steps; per evaluation Newton's order is √2 and the secant method is faster. Newton's basins for
  z³ − 1 (Cayley, 1879) on 360 × 360 starts, 0.003 percent never settling in 40 steps; a window 15 times smaller on
  the boundary shows the same structure, one 300 times smaller inside a basin is flat, every start reaching the same
  root in 6 steps; hence safeguarded root finders such as Brent's (1973).
* **11. Approximation.** Runge's phenomenon (1901) for 1/(1 + 25x²): the error at 11 equally spaced points is 1.92,
  at 21 points 59.8, at 81 points 6.3 × 10¹⁴. Chebyshev points from a semicircle; the error formula's node
  polynomial is 8.5 × 10⁻³ near the ends and 9.8 × 10⁻⁵ in the middle for 11 equispaced points, at most 1.9 × 10⁻³
  ≈ 2¹⁻ⁿ for Chebyshev points. Geometric convergence: 0.018 with 21 Chebyshev points, 1.2 × 10⁻⁷ at degree 80
  against 6.3 × 10¹⁴ equispaced, at the rate ρ = (1 + √26)/5 ≈ 1.220 set by the poles at ±i/5. The barycentric
  formula derived, O(n) per point and stable (Higham, 2004). Chebfun (Battles and Trefethen, 2004): sample on 17,
  33, 65, … points until the coefficients reach rounding level; for Runge's function the rate predicts about 185.
* **12. Quadrature.** The test integral ∫₀² eˣ cos 3x dx = −0.0099098. Trapezoids (error 0.274 with four) and
  Simpson's rule by cancelling the h² terms. Gauss's two-point rule derived (weights 1 at ±1/√3); n points exact to
  degree 2n − 1; Golub and Welsch (1969). Four rules computed: trapezoid 1.0 × 10⁻³ and Simpson 1.0 × 10⁻⁶ at 64
  intervals, Gauss 4.1 × 10⁻¹⁵ with 16 points, Monte Carlo 0.64 with 65 samples (root mean square over 200 runs).
  Adaptive Simpson's error estimate (S₂ − S₁)/15: on √|x − 0.7| the accepted intervals crowd at the cusp (9 for a
  tolerance of 10⁻³, illustrative); on the smooth test integral at 10⁻¹⁰, 985 evaluations and an error of
  2.3 × 10⁻¹⁴, where Gauss needed 16. Monte Carlo's σ/√N in any dimension against a grid's N^(−2/d): above d = 4
  Monte Carlo wins.
* **13. Differential equations.** Euler and RK4 on y′ = y, four steps of ½: 5.06 and 7.384 against e² = 7.389. Step
  control by Dormand and Prince's 5(4) pair (1980), SciPy's RK45. Stiffness on y′ = λ(y − cos t) − sin t over [0, 2]:
  adaptive RK45 at tolerance 10⁻⁶ takes 11, 132 (3 rejected) and 6,067 (214 rejected) steps for λ = −1, −100 and
  −10⁴; backward Euler takes 200 every time, with errors 2.2 × 10⁻³, 2.0 × 10⁻⁵ and 2.1 × 10⁻⁷. Stability regions
  computed: Euler reaches −2 on the real axis, RK4 about −2.8, backward Euler the whole left half-plane (A-stability,
  Dahlquist, 1963). Leapfrog as kick–drift–kick, a symplectic shear of phase space; a Kepler orbit of eccentricity
  0.5 for 1,000 orbits at 100 steps each: RK4's orbit shrinks and its energy error reaches −2.99 percent and is still
  falling, leapfrog's turns but never exceeds 1.08 percent, and leapfrog is ahead from orbit 367. The modified
  Hamiltonian: backward error analysis again.
* **14. Speed: BLAS, LAPACK and mixed precision.** Arithmetic intensity derived for the three BLAS levels: 1/12, ¼
  and n/12 flops per byte (0.083, 0.25 and 21.3 at n = 256). Timed on this machine through NumPy (best of 3–5 runs,
  on a shared machine): at n = 2,048, `axpy` 0.71, `gemv` 26.69 and `gemm` 289.3 GFLOP/s, so `gemm` runs 408 and 11
  times faster than the other two. LAPACK's blocked LU: only the panels run at level 2, a fraction 3b/4n of the work
  (0.5 percent for n = 10,000 and b = 64). Mixed-precision refinement at κ = 10⁵, n = 400: correct digits 2.7 → 5.5 →
  8.4 → 11.2 → 11.5, matching a full double-precision solve. HPL and the Top500 since 1993: Frontier's first exaflop
  (1.102 × 10¹⁸, June 2022) is 3.8 × 10⁶ times our `gemm`; HPCG reaches a few percent of peak.
* **15. Frontier: randomized and low-precision numerics.** The randomized SVD (Halko, Martinsson and Tropp, 2011) on a
  1,200 × 600 matrix at rank 20: with no extra columns the error is 2.77, 1.32 and 1.16 times the best possible after
  0, 1 and 2 power steps (1.72, 2.02 and 1.98 s); with 10 extra columns 1.00 in each case (1.36, 3.55 and 2.50 s),
  against 69.1 s for a full SVD.
  Iterative refinement in low precision: at κ = 10² double-precision accuracy (5.4 × 10⁻¹⁵) in two steps, at κ = 10⁵
  in three to four, at κ = 10⁸ the error grows from 1.06 to 357, since κ times single precision's epsilon exceeds one.
  Smoothed growth: Wilkinson's 32 × 32 matrix grows by 2,147,483,648, but plus 10⁻⁸ Gaussian noise by 2.00 (median
  and largest of 20); random 64 × 64 matrices grow by about 4; smoothed analysis (Spielman and Teng, 2001; Sankar,
  Spielman and Teng, 2006) and the missing theorem for partial pivoting. Four open problems (the exponent ω, stable
  fast solvers, low precision with guarantees, communication) and the ★ research problem.
* **Outro.** Recap, payoffs (Parts 51, 53, 54, 56 and 57), practice, problems, next part.

## Build

```bash
python -m videos.cs.cs52.compute
python -m unittest tests.test_cs52_numeric
python tools/build.py cs52
```

## Problems, with solutions

1. **Cancellation.** Show that the relative condition number of f(x) = x − 1 is |x|/|x − 1|, and explain catastrophic
   cancellation with it.

   *Solution.* The relative condition number is κ(x) = |x f′(x)/f(x)|, and f′(x) = 1, so κ = |x|/|x − 1|. It is
   near 1 away from x = 1 and unbounded as x → 1: at x = 1.000001 it is 1,000,001. Rounding the data alone, x ↦ fl(x)
   with relative error at most u = 2⁻⁵³, therefore moves the answer by a relative amount up to κu ≈ 1.1 × 10⁻¹⁰. In
   double precision fl(1.000001) − 1 = 9.999999999177334 × 10⁻⁷, a relative error of 8.2 × 10⁻¹¹: about ten correct
   digits of sixteen. The subtraction itself is exact (Sterbenz: if y/2 ≤ x ≤ 2y then x − y is a floating-point
   number), so nothing went wrong in the arithmetic; the leading digits of x and 1 cancel, and what is left are the
   digits that rounding had already spoiled, promoted to leading position. Catastrophic cancellation is a large
   condition number, not a bad algorithm: in general κ(x − y) = (|x| + |y|)/|x − y| with respect to perturbations of x
   and y, large exactly when x ≈ y. The cure is to reformulate before subtracting (for example
   √(x + 1) − √x = 1/(√(x + 1) + √x)), not to subtract more carefully.

2. **Growth.** Prove that partial pivoting's growth factor is at most 2ⁿ⁻¹, and that Wilkinson's matrix attains it.

   *Solution.* Let ρ = max over all stages k and all i, j of |a⁽ᵏ⁾ᵢⱼ|, divided by max |aᵢⱼ|. Partial pivoting
   brings the entry of largest magnitude in column k to the pivot position, so every multiplier satisfies
   |ℓᵢₖ| ≤ 1. Step k replaces a⁽ᵏ⁾ᵢⱼ by a⁽ᵏ⁺¹⁾ᵢⱼ = a⁽ᵏ⁾ᵢⱼ − ℓᵢₖa⁽ᵏ⁾ₖⱼ, so
   max |A⁽ᵏ⁺¹⁾| ≤ (1 + 1) max |A⁽ᵏ⁾|; after n − 1 steps, max |U| ≤ 2ⁿ⁻¹ max |A|. Wilkinson's matrix W has 1 on
   the diagonal, −1 below it, 1 in the last column and 0 elsewhere, so max |W| = 1. In column 1 every candidate has
   magnitude 1; with ties broken in favour of the row already in place (as `numpy.argmax` does in our `lu`), no row
   is swapped and every multiplier is −1, so each lower row has row 1 added to it. That zeroes the subdiagonal of
   column 1, leaves the −1s of columns 2, …, n − 1 unchanged (row 1 is zero there), and doubles the last column below
   row 1 from 1 to 2. The trailing (n − 1) × (n − 1) block is again Wilkinson's matrix with its last column scaled by 2,
   so by induction the last column of U is 1, 2, 4, …, 2ⁿ⁻¹ and ρ = 2ⁿ⁻¹. Our instrument confirms it exactly:
   8, 128, 32,768, 2,147,483,648 and 2⁶³ ≈ 9.2 × 10¹⁸ at n = 4, 8, 16, 32 and 64.

3. **Gram–Schmidt.** Show that classical Gram–Schmidt and modified Gram–Schmidt are equal in exact arithmetic, and
   give a 3 × 3 example where they differ in floating point.

   *Solution.* Classical Gram–Schmidt uses rᵢⱼ = qᵢᵀaⱼ; modified uses rᵢⱼ = qᵢᵀv⁽ⁱ⁾ with
   v⁽ⁱ⁾ = aⱼ − Σₗ₍ₗ₌₁…ᵢ₋₁₎ rₗⱼqₗ, the column as updated so far. By induction on i, if q₁, …, qᵢ are orthonormal then
   qᵢᵀv⁽ⁱ⁾ = qᵢᵀaⱼ − Σₗ rₗⱼ qᵢᵀqₗ = qᵢᵀaⱼ, since qᵢᵀqₗ = 0 for l < i. So the coefficients, the vectors v and the
   normalized qⱼ are identical, and orthonormality passes to the next column. In floating point the qₗ are only
   nearly orthogonal and the step qᵢᵀqₗ = 0 fails. Take ε = 10⁻⁸, so that 1 + ε² rounds to 1, and
   A = [[1, 1, 1], [ε, 0, 0], [0, ε, 0]] (columns a₁ = (1, ε, 0), a₂ = (1, 0, ε), a₃ = (1, 0, 0)). Both versions give
   q₁ = (1, ε, 0) (its norm rounds to 1) and q₂ = (0, −1, 1)/√2. For the third column, classical Gram–Schmidt
   computes q₁ᵀa₃ = 1 and q₂ᵀa₃ = 0, so v = (0, −ε, 0) and q₃ = (0, −1, 0): q₂ᵀq₃ = 1/√2 ≈ 0.707, orthogonality
   completely lost. Modified Gram–Schmidt subtracts q₁ first, then measures q₂ᵀ(0, −ε, 0) = ε/√2, so
   v = (0, −ε/2, −ε/2) and q₃ = (0, −1, −1)/√2, with q₂ᵀq₃ = 0. Running both in double precision gives
   ‖I − QᵀQ‖ = 1.0 for the classical version and 1.4 × 10⁻⁸ for the modified one; κ(A) = 3.0 × 10⁸, so the modified
   version loses about κu ≈ 3.3 × 10⁻⁸, as Björck's bound says, while Householder QR would lose nothing beyond u.

4. **CG's rate.** Derive CG's bound 2((√κ − 1)/(√κ + 1))ᵏ from Chebyshev polynomials.

   *Solution.* With x₀ = 0, CG's iterate xₖ minimizes ‖x − x*‖_A over the Krylov space 𝒦ₖ = span{b, Ab, …, Aᵏ⁻¹b}.
   Every x in it has error x − x* = p(A)(x₀ − x*) for a polynomial p of degree at most k with p(0) = 1, so
   ‖eₖ‖_A = min over such p of ‖p(A)e₀‖_A. Expand e₀ = Σ cᵢvᵢ in the orthonormal eigenvectors of A:
   ‖p(A)e₀‖²_A = Σ λᵢp(λᵢ)²cᵢ² ≤ maxᵢ p(λᵢ)² ‖e₀‖²_A, hence ‖eₖ‖_A ≤ min_p max over λ ∈ [λ_min, λ_max] of |p(λ)|
   times ‖e₀‖_A. Choose p(λ) = Tₖ((λ_max + λ_min − 2λ)/(λ_max − λ_min)) / Tₖ((λ_max + λ_min)/(λ_max − λ_min)),
   where Tₖ is the Chebyshev polynomial; it has p(0) = 1, and the numerator is at most 1 on the interval because
   |Tₖ| ≤ 1 on [−1, 1]. So ‖eₖ‖_A/‖e₀‖_A ≤ 1/Tₖ(z) with z = (κ + 1)/(κ − 1), κ = λ_max/λ_min. For z > 1,
   Tₖ(z) = ½[(z + √(z² − 1))ᵏ + (z − √(z² − 1))ᵏ] ≥ ½(z + √(z² − 1))ᵏ, and
   z + √(z² − 1) = (κ + 1 + 2√κ)/(κ − 1) = (√κ + 1)²/((√κ − 1)(√κ + 1)) = (√κ + 1)/(√κ − 1). Therefore
   ‖eₖ‖_A ≤ 2((√κ − 1)/(√κ + 1))ᵏ ‖e₀‖_A. For the 1,024-unknown Poisson grid, κ = 440.7, the ratio is 0.909, and
   reaching 10⁻⁸ needs k = ⌈ln(0.5 × 10⁻⁸)/ln 0.909⌉ = 201, the table's bound; CG took 101, since the bound
   ignores how the eigenvalues are spread inside the interval (and the instrument stops on the residual rather than
   the A-norm of the error).

5. **Build.** Write a two-grid solver for the 1D Poisson problem, and measure its convergence factor against n.

   *Solution notes.* Take A = tridiag(−1, 2, −1) of size n = 2n_c + 1 (`scipy.sparse.diags`, as in
   `iterative.smoothing_spectrum`), so the coarse grid has n_c points at the odd fine points. One cycle: ν sweeps of
   weighted Jacobi with ω = ⅔ (`iterative._jacobi`); the residual r = b − Ax; full-weighting restriction
   r_c[i] = (r[2i] + 2r[2i + 1] + r[2i + 2])/4 (0-based); an exact coarse solve of tridiag(−1, 2, −1) e_c = 4r_c with
   `scipy.sparse.linalg.spsolve` (the factor 4 is (2h)²/h², because our matrices are h² times the operator, the same
   scaling `iterative.vcycle` applies); linear interpolation back (coarse values at the odd points, averages of
   neighbours at the even ones, zero beyond the ends); x ← x + Pe_c; ν more sweeps. Measure the factor as the median
   ratio of successive residual norms, as `iterative.multigrid_experiment` does, for n = 15, 31, 63, …, 511 with a
   random b. Our check of this design gives exactly 1/9 ≈ 0.111 per cycle with ν = 1 at n = 31 and 127, and with ν = 2
   a spectral radius of the cycle's error operator of 5/81 ≈ 0.062 at every n from 15 to 511 (measured residual
   ratios 0.05–0.06), against 0.987 at n = 15 and 0.99995 at n = 255 for one Jacobi sweep alone. The factor is
   independent of n because the smoother removes the upper half of the modes at a rate of at least ⅓ per sweep, and
   the coarse correction removes the smooth half almost exactly. A complete answer adds a test that the factor stays
   below, say, 0.2 for every n, then replaces the exact coarse solve by a recursive call to get a V-cycle.

6. **★ Research.** Polynomial smoothed growth for elimination with partial pivoting.

   *Discussion.* Open. The question is whether, for every n × n matrix A with ‖A‖ ≤ 1 and G Gaussian, Gaussian
   elimination with partial pivoting on A + σG has growth factor bounded by a polynomial in n and 1/σ with high
   probability. Our instrument shows the phenomenon: Wilkinson's 32 × 32 matrix grows by 2³¹, but with σ = 10⁻⁸ the
   median growth over 20 trials is 2.00, because the exponential case needs exact ties in every pivot column. Sankar,
   Spielman and Teng (2006) proved smoothed bounds for elimination without pivoting, where each Schur complement of a
   perturbed matrix can be analysed directly. With partial pivoting the row chosen at each step depends on the
   perturbation, so the later Schur complements are conditioned on the outcomes of earlier comparisons, and the
   independence those arguments use is lost; and the bound must hold for every A, including adversarial ones built
   to steer the pivot sequence. A good partial answer would be a quasi-polynomial bound, a polynomial bound for a
   natural restricted class (for example perturbations of Wilkinson-like matrices, or growth measured in the first
   few steps), or a bound on the expected logarithm of the growth; results for the purely Gaussian case, with no fixed
   matrix underneath, have recently been announced (H. Huang and K. Tikhomirov), and extending them to an arbitrary
   centre is the heart of the problem.

## 习题与解答

1. **抵消。** 证明 f(x) = x − 1 的相对条件数是 |x|/|x − 1|，并用它解释灾难性抵消。

   *解答。* 相对条件数是 κ(x) = |x f′(x)/f(x)|，而 f′(x) = 1，所以 κ = |x|/|x − 1|。远离 x = 1 时它接近 1，x → 1 时
   无界：在 x = 1.000001 处为 1,000,001。仅仅对数据舍入一次，x ↦ fl(x)，相对误差至多 u = 2⁻⁵³，就会使答案产生至多
   κu ≈ 1.1 × 10⁻¹⁰ 的相对变化。在双精度下 fl(1.000001) − 1 = 9.999999999177334 × 10⁻⁷，相对误差 8.2 × 10⁻¹¹：十六位
   中大约十位正确。减法本身是精确的（斯特本茨引理：若 y/2 ≤ x ≤ 2y，则 x − y 是一个浮点数），所以运算没有出错；x 与 1
   的前几位相互抵消，剩下的正是早已被舍入破坏的那几位，被提升到了最前面。灾难性抵消是条件数大，而不是算法差：一般地，
   相对于 x 和 y 的扰动，κ(x − y) = (|x| + |y|)/|x − y|，恰在 x ≈ y 时很大。补救办法是在相减之前改写公式（例如
   √(x + 1) − √x = 1/(√(x + 1) + √x)），而不是更小心地相减。

2. **增长。** 证明部分主元（列主元）消去法的增长因子至多为 2ⁿ⁻¹，并证明威尔金森矩阵达到这个界。

   *解答。* 令 ρ 为所有阶段 k、所有 i、j 上 |a⁽ᵏ⁾ᵢⱼ| 的最大值除以 max |aᵢⱼ|。部分主元把第 k 列中绝对值最大的元素换到
   主元位置，所以每个乘数都满足 |ℓᵢₖ| ≤ 1。第 k 步把 a⁽ᵏ⁾ᵢⱼ 换成 a⁽ᵏ⁺¹⁾ᵢⱼ = a⁽ᵏ⁾ᵢⱼ − ℓᵢₖa⁽ᵏ⁾ₖⱼ，因此
   max |A⁽ᵏ⁺¹⁾| ≤ (1 + 1) max |A⁽ᵏ⁾|；n − 1 步之后，max |U| ≤ 2ⁿ⁻¹ max |A|。威尔金森矩阵 W 对角线上为 1，对角线以下
   为 −1，最后一列为 1，其余为 0，所以 max |W| = 1。第 1 列的所有候选元素绝对值都是 1；若平局时保留已在原位的行（我们
   的 `lu` 中 `numpy.argmax` 正是如此），就不交换任何行，每个乘数都是 −1，于是下面每一行都加上第 1 行。这使第 1 列对角线
   以下变为零，第 2 到 n − 1 列的 −1 保持不变（第 1 行在那里为零），并把第 1 行以下最后一列的元素从 1 加倍为 2。右下角
   (n − 1) × (n − 1) 的块又是一个最后一列乘以 2 的威尔金森矩阵，所以归纳地，U 的最后一列是 1, 2, 4, …, 2ⁿ⁻¹，
   ρ = 2ⁿ⁻¹。我们的工具精确地证实了这一点：n = 4、8、16、32、64 时分别为 8、128、32,768、2,147,483,648 和
   2⁶³ ≈ 9.2 × 10¹⁸。

3. **格拉姆–施密特。** 证明经典格拉姆–施密特与修正格拉姆–施密特在精确算术中相同，并给出一个在浮点运算中二者不同的
   3 × 3 例子。

   *解答。* 经典格拉姆–施密特用 rᵢⱼ = qᵢᵀaⱼ；修正的版本用 rᵢⱼ = qᵢᵀv⁽ⁱ⁾，其中 v⁽ⁱ⁾ = aⱼ − Σₗ₍ₗ₌₁…ᵢ₋₁₎ rₗⱼqₗ 是
   到目前为止更新过的列。对 i 归纳：若 q₁, …, qᵢ 标准正交，则 qᵢᵀv⁽ⁱ⁾ = qᵢᵀaⱼ − Σₗ rₗⱼ qᵢᵀqₗ = qᵢᵀaⱼ，因为 l < i 时
   qᵢᵀqₗ = 0。所以系数、向量 v 以及归一化后的 qⱼ 都相同，标准正交性也传到下一列。在浮点运算中 qₗ 只是近似正交，
   qᵢᵀqₗ = 0 这一步不再成立。取 ε = 10⁻⁸，使 1 + ε² 舍入为 1，令 A = [[1, 1, 1], [ε, 0, 0], [0, ε, 0]]（各列为
   a₁ = (1, ε, 0)，a₂ = (1, 0, ε)，a₃ = (1, 0, 0)）。两种版本都得到 q₁ = (1, ε, 0)（它的范数舍入为 1）和
   q₂ = (0, −1, 1)/√2。对第三列，经典版本算出 q₁ᵀa₃ = 1、q₂ᵀa₃ = 0，于是 v = (0, −ε, 0)，q₃ = (0, −1, 0)：
   q₂ᵀq₃ = 1/√2 ≈ 0.707，正交性完全丧失。修正版本先减去 q₁，再计算 q₂ᵀ(0, −ε, 0) = ε/√2，于是
   v = (0, −ε/2, −ε/2)，q₃ = (0, −1, −1)/√2，q₂ᵀq₃ = 0。在双精度下运行两者，经典版本 ‖I − QᵀQ‖ = 1.0，修正版本为
   1.4 × 10⁻⁸；κ(A) = 3.0 × 10⁸，所以修正版本损失约 κu ≈ 3.3 × 10⁻⁸，与 Björck 的界一致，而豪斯霍尔德 QR 的损失不会
   超过 u 的量级。

4. **共轭梯度法的收敛速度。** 用切比雪夫多项式推导共轭梯度法的界 2((√κ − 1)/(√κ + 1))ᵏ。

   *解答。* 取 x₀ = 0，共轭梯度法的迭代 xₖ 在克雷洛夫子空间 𝒦ₖ = span{b, Ab, …, Aᵏ⁻¹b} 上最小化 ‖x − x*‖_A。其中每个
   x 的误差都是 x − x* = p(A)(x₀ − x*)，p 是次数至多为 k、满足 p(0) = 1 的多项式，所以 ‖eₖ‖_A 等于对所有这样的 p 取
   ‖p(A)e₀‖_A 的最小值。把 e₀ = Σ cᵢvᵢ 按 A 的标准正交特征向量展开：‖p(A)e₀‖²_A = Σ λᵢp(λᵢ)²cᵢ² ≤ maxᵢ p(λᵢ)²
   ‖e₀‖²_A，因此 ‖eₖ‖_A ≤（对 p 取最小、对 λ ∈ [λ_min, λ_max] 取最大的 |p(λ)|）× ‖e₀‖_A。取
   p(λ) = Tₖ((λ_max + λ_min − 2λ)/(λ_max − λ_min)) / Tₖ((λ_max + λ_min)/(λ_max − λ_min))，其中 Tₖ 是切比雪夫多项式；
   它满足 p(0) = 1，并且因为在 [−1, 1] 上 |Tₖ| ≤ 1，分子在区间上至多为 1。所以 ‖eₖ‖_A/‖e₀‖_A ≤ 1/Tₖ(z)，其中
   z = (κ + 1)/(κ − 1)，κ = λ_max/λ_min。当 z > 1 时，Tₖ(z) = ½[(z + √(z² − 1))ᵏ + (z − √(z² − 1))ᵏ] ≥
   ½(z + √(z² − 1))ᵏ，而 z + √(z² − 1) = (κ + 1 + 2√κ)/(κ − 1) = (√κ + 1)²/((√κ − 1)(√κ + 1)) = (√κ + 1)/(√κ − 1)。
   因此 ‖eₖ‖_A ≤ 2((√κ − 1)/(√κ + 1))ᵏ ‖e₀‖_A。对 1,024 个未知数的泊松网格，κ = 440.7，比值为 0.909，达到 10⁻⁸ 需要
   k = ⌈ln(0.5 × 10⁻⁸)/ln 0.909⌉ = 201，正是表中的界；共轭梯度法用了 101 步，因为这个界不考虑特征值在区间内部如何分布
   （而且工具以残差而不是误差的 A 范数作为停止标准）。

5. **动手。** 为一维泊松问题写一个两重网格求解器，并测量它的收敛因子随 n 的变化。

   *解答要点。* 取 n = 2n_c + 1 阶的 A = tridiag(−1, 2, −1)（用 `scipy.sparse.diags`，与 `iterative.smoothing_spectrum`
   相同），粗网格的 n_c 个点位于细网格的奇数点上。一个循环：ν 次 ω = ⅔ 的加权雅可比迭代（`iterative._jacobi`）；残差
   r = b − Ax；全加权限制 r_c[i] = (r[2i] + 2r[2i + 1] + r[2i + 2])/4（下标从 0 开始）；用 `scipy.sparse.linalg.spsolve`
   精确求解粗网格方程 tridiag(−1, 2, −1) e_c = 4r_c（因子 4 是 (2h)²/h²，因为我们的矩阵是算子的 h² 倍，与
   `iterative.vcycle` 的缩放相同）；线性插值回细网格（奇数点取粗网格值，偶数点取相邻两值的平均，两端之外为零）；
   x ← x + Pe_c；再做 ν 次迭代。像 `iterative.multigrid_experiment` 那样，把收敛因子取为相邻两次残差范数之比的中位数，
   对 n = 15、31、63、…、511 和随机的 b 测量。我们按这个设计验证的结果：ν = 1 时在 n = 31 和 127 上每个循环恰为
   1/9 ≈ 0.111；ν = 2 时，循环误差算子的谱半径在 n = 15 到 511 的每个 n 上都是 5/81 ≈ 0.062（实测残差比 0.05–0.06）；
   而单独一次雅可比迭代在 n = 15 时为 0.987，在 n = 255 时为 0.99995。收敛因子与 n 无关，因为光滑迭代以每次至少 ⅓ 的
   速度消除上半部分的模态，而粗网格校正几乎精确地消除光滑的那一半。完整的答案应加一个测试，检查每个 n 上的因子都低于
   （比如）0.2，然后把精确的粗网格求解换成递归调用，得到 V 循环。

6. **★ 研究。** 部分主元消去法的多项式光滑增长。

   *讨论。* 尚未解决。问题是：对每个满足 ‖A‖ ≤ 1 的 n × n 矩阵 A 和高斯矩阵 G，对 A + σG 做部分主元高斯消元，其增长
   因子是否以高概率受 n 和 1/σ 的一个多项式约束。我们的工具展示了这一现象：威尔金森的 32 × 32 矩阵增长 2³¹ 倍，但在
   σ = 10⁻⁸ 时 20 次试验的增长中位数为 2.00，因为指数增长需要每个主元列中都恰好出现平局。Sankar、Spielman 和 Teng
   （2006）证明了不选主元消去法的光滑界，那里被扰动矩阵的每个舒尔补都可以直接分析。选部分主元时，每一步选中的行依赖于
   扰动，于是后面的舒尔补是以前面各次比较的结果为条件的，那些论证所用的独立性就丧失了；而且这个界必须对每个 A 成立，
   包括专门构造来操纵主元序列的对手矩阵。好的部分结果可以是一个拟多项式界、对某个自然的受限类（例如类威尔金森矩阵的
   扰动，或只看前几步的增长）的多项式界，或对增长的对数的期望的界；对纯高斯情形（下面没有固定矩阵）的结果最近已有人
   宣布（H. Huang 和 K. Tikhomirov），把它推广到任意的中心矩阵，正是问题的核心。

## Glossary additions

* **condition number (relative), well and ill conditioned** — how much a problem's answer moves, relatively, when its
  data moves; κ(A) = ‖A‖‖A⁻¹‖ = σ_max/σ_min for a matrix.
* **forward error, backward error, backward stable, residual** — how wrong the answer is; how far the data must move
  to make it exact; an algorithm whose backward error is a small multiple of u; b − Ax̂.
* **unit roundoff u, Wilkinson's model** — 2⁻⁵³ in double precision; fl(a ∘ b) = (a ∘ b)(1 + δ), |δ| ≤ u.
* **LU factorization, partial pivoting, growth factor, Cholesky** — elimination as A = LU; swapping up the largest
  entry of each column; the largest entry produced over the largest in A; A = LLᵀ for symmetric positive definite A.
* **least squares, normal equations, QR, Householder mirror, Givens rotation, Gram–Schmidt (classical, modified)** —
  the closest fit; AᵀAx = Aᵀb; orthogonal times triangular; a reflection I − 2vvᵀ; a plane rotation; orthogonalizing
  against the original or the updated column.
* **singular value decomposition, numerical rank, truncated SVD, Tikhonov regularization, pseudo-inverse** —
  A = UΣVᵀ; the number of singular values above a tolerance; dropping or damping the small ones; the shortest
  least-squares solution.
* **power and inverse iteration, the QR algorithm, Hessenberg form, Wilkinson's shift, deflation** — finding
  eigenvalues by iteration; zeros below the first subdiagonal; a shift from the trailing 2 × 2 block; splitting off a
  converged eigenvalue.
* **Krylov space, conjugate gradients, A-norm, preconditioner (Jacobi, SSOR), Arnoldi, GMRES** — span{b, Ab, …};
  the optimal method for symmetric positive definite systems; √(eᵀAe); M ≈ A cheap to solve with; an orthonormal
  Krylov basis; minimal residuals without symmetry.
* **sparse matrix, CSR, fill-in, minimum degree, nested dissection, reverse Cuthill–McKee** — storing only nonzeros;
  values, column numbers, row pointers; new nonzeros created by elimination; orderings that limit it.
* **weighted Jacobi, smoothing, restriction, interpolation (prolongation), V-cycle, algebraic multigrid** — relaxation
  that damps rough error; moving residuals to a coarser grid and corrections back; the recursive cycle; coarse levels
  built from the matrix alone.
* **bisection, secant method, Newton's method, order of convergence, basin of attraction, safeguarded root finder** —
  bracketing; slopes through two points or from f′; digits multiplied per step; the starts that reach one root;
  Brent's combination of bisection and fast steps.
* **interpolation, Runge's phenomenon, Chebyshev points, node polynomial, barycentric formula** — a polynomial through
  samples; divergence at equispaced points; cos(jπ/n); ∏(x − xⱼ); evaluation in O(n) per point.
* **quadrature: trapezoid, Simpson, Gauss–Legendre, adaptive, Monte Carlo** — rules of order h², h⁴, degree 2n − 1;
  refining where the error estimate is large; random samples, σ/√N in any dimension.
* **Runge–Kutta, embedded pair, step control, stiffness, stability region, A-stable, backward Euler** — multi-stage
  steps; two orders from one set of slopes; |R(z)| ≤ 1; stable on the whole left half-plane.
* **symplectic integrator, leapfrog (velocity Verlet), modified Hamiltonian** — a step that keeps phase-space area;
  kick–drift–kick; the nearby energy it conserves almost exactly.
* **BLAS (levels 1, 2, 3), arithmetic intensity, LAPACK, blocked factorization, mixed-precision iterative refinement,
  HPL, Top500** — vector, matrix–vector and matrix–matrix kernels; flops per byte; panels at level 2 and trailing
  updates at level 3; low-precision factors with high-precision residuals; the ranking benchmark.
* **randomized SVD, oversampling, power iteration; smoothed analysis** — a random sketch of the range; extra columns
  and multiplications by AAᵀ; worst cases surrounded by easy ones.

## Sources

* L. N. Trefethen and D. Bau, *Numerical Linear Algebra* (1997); G. H. Golub and C. F. Van Loan, *Matrix
  Computations* (4th ed., 2013); N. J. Higham, *Accuracy and Stability of Numerical Algorithms* (2nd ed., 2002);
  J. W. Demmel, *Applied Numerical Linear Algebra* (1997).
* J. H. Wilkinson, *Rounding Errors in Algebraic Processes* (1963) and *The Algebraic Eigenvalue Problem* (1965).
* Y. Saad, *Iterative Methods for Sparse Linear Systems* (2nd ed., 2003); W. L. Briggs, V. E. Henson and
  S. F. McCormick, *A Multigrid Tutorial* (2nd ed., 2000).
* L. N. Trefethen, *Approximation Theory and Approximation Practice* (2013); E. Hairer, C. Lubich and G. Wanner,
  *Geometric Numerical Integration* (2nd ed., 2006).
* J. Dongarra and F. Sullivan, "Guest editors' introduction: the top 10 algorithms", Computing in Science and
  Engineering, January 2000.
* J. G. F. Francis, "The QR transformation", The Computer Journal 1961; M. R. Hestenes and E. Stiefel, "Methods of
  conjugate gradients for solving linear systems", J. Res. Nat. Bur. Standards 1952; Y. Saad and M. H. Schultz,
  "GMRES: a generalized minimal residual algorithm for solving nonsymmetric linear systems", SIAM J. Sci. Stat.
  Comput. 1986.
* L. N. Trefethen and R. S. Schreiber, "Average-case stability of Gaussian elimination", SIAM J. Matrix Anal. Appl.
  1990; A. Sankar, D. A. Spielman and S.-H. Teng, "Smoothed analysis of the condition numbers and growth factors of
  matrices", SIAM J. Matrix Anal. Appl. 2006.
* N. Halko, P.-G. Martinsson and J. A. Tropp, "Finding structure with randomness: probabilistic algorithms for
  constructing approximate matrix decompositions", SIAM Review 2011; E. Carson and N. J. Higham, "Accelerating the
  solution of linear systems by iterative refinement in three precisions", SIAM J. Sci. Comput. 2018.
