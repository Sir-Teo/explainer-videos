# Analysis, Built — Part 3: Integration and the First Function Space

Part 3 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the
spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapters 6 to 8 of
*Principles of Mathematical Analysis*, in a hook, fifteen chapters and an outro, organized around Rudin's "main
problem" (7.1): when may two limits be swapped?

* **The integral.** Upper and lower sums squeezing the area (U − L = 1/n for x², computed to n = 2¹⁴); refinement;
  the integrability criterion. Continuous functions (uniform continuity pays), monotone functions (the stacked
  differences), Dirichlet's function (never), Thomae's function (yes: U → 0). Riemann–Stieltjes integrals as a
  stretched ruler: a step integrator makes a sum, the Cantor function makes an integral that is neither
  (∫ x dC = 1/2, ∫ x² dC = 3/8). The fundamental theorem by telescoping and the mean value theorem; curve length
  as a supremum of polygons; the Koch curve, whose length would have to be four thirds of itself.
* **Uniform convergence.** Pointwise against uniform as two orders of quantifiers; the convergence dashboard
  (pointwise, sup, area and energy lenses); the Cauchy criterion; the sup norm; the M-test. Uniform limits of
  continuous functions are continuous (three hops), Dini's theorem, and C(X) as a complete metric space, seen on
  the function camera. Schoenberg's space-filling curve. Integrals pass through uniform limits; derivatives need
  more (x/(1 + nx²)).
* **The first function space.** Rudin's nowhere-differentiable function, zoomed at 0.3, and its proof as one panel
  per term. Equicontinuity (one δ for a family), Rudin 7.24, and Arzelà–Ascoli by the diagonal process run on
  400,000 random 1-Lipschitz functions. Weierstrass's approximation theorem with the Landau kernel (and its near/far
  split computed), Bernstein's polynomials. Stone–Weierstrass: the two obstructions, the four-step proof on a proof
  map with the lattice step computed on eˣ, and z̄ on the circle (its error loop has mean exactly 1).
* **Power series and Fourier series.** Uniform convergence inside the radius; Abel's theorem and ln 2; exp, cos
  and sin from one series (the spiral of terms), π as twice the first zero of cos by bisection; the fundamental
  theorem of algebra by d'Alembert's step. Orthogonality, the Fourier partial sum as the best approximation
  (500 random competitors; Pythagoras), Bessel, the Dirichlet kernel and its growing L¹ norm (du Bois-Reymond),
  Dini's test. Fejér's means, Parseval (the missing energy is the tail), Σ 1/n² = π²/6, the dashboard verdicts
  for the sawtooth, Gibbs' 8.95%, and the gamma function on one card.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert
the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the
[top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis3.compute                # once: every computed item (about a minute; cached in .cache/analysis3)
python tools/build.py analysis3 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis3_2160p.mp4
python tools/build.py analysis3                   # 1080p30 -> renders/analysis3.mp4
python tools/build.py analysis3 -q l              # fast 480p preview
python tools/export_script.py analysis3           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis3         # Whisper listen test of every narration line
```

Part 3 imports helpers from Parts 1 and 2 (`polyline`, `endpoint`, `plain_axes`) and three instruments from
`explainer/analysis`: the convergence dashboard and the function camera
([`dashboard.py`](../../explainer/analysis/dashboard.py)) and the proof map
([`proofmap.py`](../../explainer/analysis/proofmap.py)).

## Outline

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | The ledger; the grid m/(m + n) (7.2); three failed swaps: xⁿ (continuity), n²x(1 − x²)ⁿ (integral, 7.6), sin(nx)/√n (derivative, 7.5); the Fourier question; the plan. | ∫ of the bump = n²/(2n + 2); sup sin(nx)/√n = 1/√n and slope √n at 0. |
| 1 | `UpperLower` | Partitions, U and L (6.1–6.2); refinement (6.4); the criterion (6.6); x². | U − L = 1/n exactly, n = 2 … 2¹⁴. |
| 2 | `WhoIsIntegrable` | Continuous (6.8), monotone (6.9); Dirichlet (Exercise 6.4); Thomae. | η = 0.5, δ = 0.2 for the uniform-continuity step; Thomae's U on dyadic partitions to 2¹⁴ (0.0084). |
| 3 | `Stieltjes` | The stretched ruler; the unit step (6.14–6.16); the Cantor integrator (Exercise 6.6 territory); 6.17. | ∫ x dC = 1/2, ∫ x² dC = 3/8 with U − L = 3⁻ᵈ. |
| 4 | `FTC` | F = ∫f is continuous and F′ = f (6.20); the fundamental theorem (6.21); length (6.26–6.27); the Koch curve. | Inscribed polygon lengths; Koch lengths (4/3)ᵏ; the first quarter of the depth-6 curve is the depth-5 curve shrunk by 3. |
| 5 | `Uniform` | Pointwise vs uniform (7.7); the dashboard; Cauchy criterion (7.8) and sup norm (7.9); M-test (7.10). | N = 22 for xⁿ on [0, 0.9] at ε = 0.1; dashboard lenses (exact sup 1, L¹ = 1/(n + 1)); pair gaps of Σ sin kx/k²; sup errors under their M-test tails. |
| 6 | `UniformContinuity` | 7.12 by three hops; Dini (7.13); C(X) complete (7.14–7.15) on the camera; Schoenberg's curve (Exercise 7.14). | (1 + x/n)ⁿ → eˣ errors; Bernstein's trail with nested sup-ball squares; the curve's exact hits from ternary digits. |
| 7 | `IntegralsDerivatives` | 7.16 with the box bound; 7.17 and x/(1 + nx²); the swaps so far. | ∫f_n vs ∫f live; sup x/(1 + nx²) = 1/(2√n), f_n′(0) = 1. |
| 8 | `Nowhere` | Rudin 7.18: construction, the zoom, the proof. | Each term's share of the quotient at x = 0.3, m = 3 (exact rationals: 1, 3, 9, 27 in size, then 0, 0); quotients to m = 10. |
| 9 | `Equicontinuity` | sin(nx) has no convergent subsequence; 7.21's bumps; 7.22; 7.24. | Pairwise sup distances > 1; δ = 0.1 for {sin kx/k}, ε/K for {sin kx}; one δ for 24 uniformly convergent functions. |
| 10 | `ArzelaAscoli` | 7.23 by the diagonal; spreading by equicontinuity; 7.25; the dictionary. | The actual surviving indices among 400,000 random functions; spreads shrinking stage by stage. |
| 11 | `Approximation` | 7.26 with the Landau kernel; the near/far estimate; Bernstein. | c_n < √n; the far mass 0.0051 ≤ 2√n(1 − δ²)ⁿ; sup errors to n = 10⁴ (0.0045). |
| 12 | `StoneWeierstrass` | 7.28–7.33: the obstructions, the theorem, the four steps, z̄. | Even polynomials on [0, 1] approaching x; Bernstein's |y|; caps and their minimum within 0.0189 of eˣ; 1 − zP(z) has mean 1 for random P. |
| 13 | `PowerSeries` | 8.1, Abel (8.2), exp/cos/sin (8.6–8.7), π, 8.8. | r^(N+1)/(1 − r); Abel sums to ln 2; 20 terms of e^(2i); π by 60 bisections (12 digits); a descent to a root of z³ − 2z + 2. |
| 14 | `FourierSeries` | Orthogonality (8.9), 8.11, Bessel (8.12), the Dirichlet kernel (8.13), Dini (8.14). | The 7 × 7 Gram matrix; best = 0.4804 vs 500 competitors; Lebesgue constants to N = 500; s_N(π/2) → π/4. |
| 15 | `Parseval` | 8.15 (Fejér), Parseval (8.16), π²/6 (Exercise 8.13), the dashboard, Gibbs, Γ. | Fejér errors; missing energy = tail; Σ_{n ≤ 10⁶} 1/n²; the overshoot ratio → 0.08949; Stirling's ratio → 1. |
| 16 | `Outro` | Recap; the ledger's third row; Part 4 preview (a map of the plane and its derivative); sources. | — |

## The visual language

Part 3 adds three instruments:

* **The convergence dashboard** ([`dashboard.py`](../../explainer/analysis/dashboard.py)): one sequence of functions
  under several lenses at once (a probe at a point, the sup tube, the area between, the energy), each with a live
  number and a lamp that lights green or red when the verdict is asserted.
* **The function camera**: each function becomes one dot, plotted by two of its values; a Cauchy sequence is a trail,
  and a sup-norm ball casts a square shadow.
* **The proof map** ([`proofmap.py`](../../explainer/analysis/proofmap.py)): a long proof's steps as a flowchart that
  lights up as the narration reaches each one (Stone–Weierstrass, Arzelà–Ascoli).

| Concept | Color |
|---|---|
| ε, tolerances, the sup lens | yellow |
| δ, one δ for a family | teal |
| the sequence, the hero function | blue |
| approximants, partial sums | magenta |
| area between graphs | orange |
| energy, orthogonality | lilac |
| counterexamples | red |

## Computations (`compute.py`)

| Item | What | Checks |
|---|---|---|
| `failures` | the hook's three sequences | ∫ bump = n²/(2n + 2); sup = 1/√n; slope √n |
| `riemann` | U, L for x² | U − L = 1/n |
| `thomae` | Thomae's upper sums on dyadic partitions | decreasing to 0.0084 at 2¹⁴ |
| `stieltjes` | the Cantor integrator from its intervals | ∫ x dC = 1/2, ∫ x² dC = 3/8, U − L = 3⁻ᵈ |
| `koch` | Koch polygons | lengths (4/3)ᵏ exactly |
| `mtest` | partial sums of Σ sin nx/n² | sup errors ≤ Σ_{n > N} 1/n² |
| `dini` | (1 + x/n)ⁿ | increasing, sup errors decreasing |
| `cauchyc` | Bernstein polynomials of |x − ½| | Cauchy bounds; every later dot inside each sup-ball square |
| `peano` | Schoenberg's curve | exact rational hits from ternary digits |
| `weier` | Rudin 7.18 at x = 0.3 | |quotient| ≥ (3ᵐ + 1)/2 for m ≤ 10 |
| `equi` | δ for {sin kx/k} and {sin kx} | brute-force checks of both δ's |
| `arzela` | the diagonal process on 400,000 random functions | spreads monotone; survivors nested |
| `landau` | Landau kernels and approximants; Bernstein | c_n < √n; far mass under its bound; errors decreasing |
| `stone` | the lattice step; |y|; z̄; even polynomials | caps above f − ε; min within ε; mean of 1 − zP exactly 1 |
| `power` | cos and π; Abel; e^(it); d'Alembert | π to 10⁻¹²; ln 2 to 10⁻⁴; |P| decreasing to a root |
| `fourier` | best approximation; Gram; Dirichlet kernels; Dini | 500 competitors worse; Pythagoras; L¹ norms increasing like (4/π²) ln N |
| `parseval` | Parseval, Gibbs, Fejér, Stirling | mse = tail; lhs = rhs = π²/12; overshoot → Si(π)/π − ½; Fejér kernel ≥ 0 |

## Fact-check notes and sources

The mathematics follows W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (McGraw-Hill, 1976), chapters 6–8;
theorem numbers on screen are that edition's.

* **Riemann** (1854) for the integral, **Darboux** (1875) for upper and lower sums, **Stieltjes** (1894).
* **Weierstrass** presented his nowhere-differentiable function to the Berlin Academy in 1872 (published by du
  Bois-Reymond in 1875); the version on screen is Rudin's 7.18. Weierstrass's approximation theorem is from 1885.
* **Ascoli** (1883–84) and **Arzelà** (1889) for the compactness theorem; **Dini** (1878) for his theorems.
* **Stone** (1937; the simpler proof Rudin gives is from 1948). **Bernstein** (1912); **Landau** (1908) for the kernel.
* **Schoenberg** (1938) for the space-filling curve of Rudin's Exercise 7.14; **von Koch** (1904).
* **Fourier** (1807/1822), **Dirichlet** (1829), **Fejér** (1900), **du Bois-Reymond** (1873, a continuous function
  whose Fourier series diverges at a point), **Wilbraham** (1848) and **Gibbs** (1899).
* **Euler** (1734) for Σ 1/n² = π²/6; the 3Blue1Brown video on the Basel problem proves it differently.

On-screen simplifications:

* The Weierstrass zoom rescales each view vertically; the panel says so.
* The Stone–Weierstrass interpolants are lines (the polynomial algebra); the proof needs only some member of the
  algebra through two points.
* The sawtooth's Gibbs table uses N up to 1000; the limit 0.08949 is Si(π)/π − 1/2.
