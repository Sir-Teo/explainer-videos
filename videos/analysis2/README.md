# Analysis, Built — Part 2: Limits: Sequences, Series, Continuity and the Derivative

Part 2 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the
spectral theorem, following the arc of Walter Rudin's three textbooks. This part covers chapters 3 to 5 of
*Principles of Mathematical Analysis*, in a hook, fourteen chapters and an outro:

* **Sequences.** Convergence as a game (ε moves first, then N), uniqueness, the limit laws and the ε/2 trick,
  subsequences. Cauchy sequences: the tails' diameters, convergence checked without knowing the limit, Rᵏ and
  compact spaces are complete, Q is not (the convergents of √2 close in on a hole). Monotone bounded sequences.
  Upper and lower limits as the high- and low-water marks of the tail; a sequence listing every rational has
  E = [0, 1]; the special limits n^(1/n) → 1 and nᵅ/(1 + p)ⁿ → 0.
* **Series.** The Cauchy criterion, Oresme's harmonic blocks, comparison, Cauchy condensation and Σ 1/nᵖ, no sharp
  line between convergence and divergence. The number e, its two definitions and its irrationality. Root and ratio
  tests (Rudin's example where only the root test decides), power series and their disks of convergence, and why
  the series of 1/(1 + x²) stops at |x| = 1 (the poles at ±i). Summation by parts, Dirichlet's test, and the
  sawtooth series Σ sin(kx)/k converging at every x. The Cauchy product, Mertens, and its failure without absolute
  convergence. Riemann's rearrangement theorem, proved by the hook's algorithm; absolutely convergent series are
  safe; the sawtooth series at x = 1 reordered to sum to 3.
* **Continuity.** Limits of functions; continuity on the ε–δ game board (for x² at 3, ε = 0.1, the largest δ is
  0.0166); sin(1/x) by sequences; preimages of open sets; compactness gives extreme values, continuous inverses and
  uniform continuity (the sliding box; 1/x's best δ shrinking to 0); connectedness gives intermediate values (and
  their failure over Q); the kinds of discontinuity; monotone functions jump only countably often, and Rudin's
  function that jumps at every rational; Thomae's function, which is Part 1's rational ruler with tick height 1/q,
  continuous exactly at the irrationals.
* **The derivative.** Secants to tangents; zooming in until straight (and Rudin's nowhere-differentiable function,
  which never straightens); the chain rule with Rudin's u(t) trick; x² sin(1/x). The mean value theorem by a
  vertical shear; monotonicity; Darboux's theorem; L'Hôpital's rule as chord and tangent slopes of the curve
  (g, f). Taylor's theorem with Lagrange's remainder, its error bound for e, and e^(−1/x²), smooth but not the sum of
  its Taylor series. The vector-valued mean value inequality and the ledger's second row.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted; most scenes also assert
the specific values they display.

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the
[top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis2.compute                # once: every computed item (a few seconds; cached in .cache/analysis2)
python tools/build.py analysis2 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis2_2160p.mp4
python tools/build.py analysis2                   # 1080p30 -> renders/analysis2.mp4
python tools/build.py analysis2 -q l              # fast 480p preview
python tools/export_script.py analysis2           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis2         # Whisper listen test of every narration line
```

Part 2 imports helpers from Part 1 (`videos/analysis1/common.py`): the zoomable window with its rational ruler,
and the sawtooth.

## Outline

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | The ledger so far; 1 − 1/2 + 1/3 − ⋯ = ln 2 in its natural order; the greedy rearrangement to π, to −1 and to +∞; the plan. | The rearrangements to 10⁶ terms (within 10⁻⁵ of π and −1); Pringsheim's ratio of positive to negative terms (≈ 134 for π). |
| 1 | `Sequences` | Convergence (3.1) on the sequence game board; (−1)ⁿ diverges; uniqueness and boundedness (3.2); limit laws and the ε/2 trick (3.3); subsequences (3.5–3.6). | For pₙ = 1 + (−1)ⁿ1.5/n, the smallest N for ε = 0.5, 0.2, 0.05: 3, 7, 30. |
| 2 | `Cauchy` | Cauchy sequences (3.8); diam Eₙ → 0 (3.9); convergent ⇒ Cauchy (3.11a); Q is incomplete; compact ⇒ complete, Rᵏ complete (3.11b–c), via nested closed tails; complete spaces (3.12); monotone bounded sequences (3.14). | The tails of 1 − 1/2 + ⋯ have diameter 1/(N + 1) (N = 10 for ε = 0.1, 20 for 0.05); the convergents p/q of √2, diam Eₙ = 1/(qₙqₙ₊₁) exactly; hulls of a spiral's tails, nested; (1 + 1/n)ⁿ within 0.1 of e from n = 13 on. |
| 3 | `LimSup` | Upper and lower limits (3.16), the tail sup and inf; 3.17; convergence ⇔ lim sup = lim inf; every rational listed gives E = [0, 1]; the special sequences (3.20). | Tail sups and infs; the subsequence nearest 1/√2; n^(1/n) to 10⁶ under the bound 1 + √(2/(n − 1)); n¹⁰/1.1ⁿ peaking near 7 × 10¹⁵ at n = 105, below 1 from n = 686. |
| 4 | `Series` | Series and the Cauchy criterion (3.22); terms → 0 (3.23); Oresme's blocks; comparison (3.25); the geometric series (3.26); condensation (3.27); Σ 1/nᵖ (3.28); Σ 1/(n log n) (3.29); Exercises 3.11–3.12. | Oresme's blocks ≥ 1/2 in exact fractions; Σ 1/nᵖ for p = 1, 1.5, 2 to 10⁶ terms (14.39; ζ(3/2) still 0.002 away; π²/6); the condensation inequalities; Σ 1/(n log n) ≈ 3.42 at 10⁶. |
| 5 | `NumberE` | e = Σ 1/n! and the tail bound 1/(n!·n); lim (1 + 1/n)ⁿ = e (3.31) by the binomial bars; e is irrational (3.32). | The tail bound for n ≤ 15 (60-digit arithmetic); the binomial terms of (1 + 1/n)ⁿ for n up to 200; q!(e − s_q) ∈ (0, 1/q) for q = 1 … 15. |
| 6 | `Tests` | Root test (3.33) as a geometric envelope; ratio test (3.34) and Rudin's example 3.35(b); 3.37; power series (3.39); 1/(1 + x²) and its poles at ±i. | Ratios → 0 and → ∞ while the n-th roots → 1/√2; partial-sum paths of Σ zⁿ/n at \|z\| = 0.9, z = −1, z = 1, \|z\| = 1.1 (−ln 2 at z = −1). |
| 7 | `Abel` | Summation by parts (3.41) as two ways to slice an area; Dirichlet's test (3.42); alternating series (3.43); the sawtooth converges at every x; absolute convergence (3.45); the Cauchy product, Mertens (3.50) and the counterexample (3.49). | Summation by parts checked; Σ e^(ikx) on its circle of radius 1/(2\|sin(x/2)\|); Σ sin(k)/k → (π − 1)/2 inside Dirichlet's bound; \|cₙ\| ≥ 2(n + 1)/(n + 2). |
| 8 | `Rearrangement` | Riemann's theorem (3.54): two infinite piles, the greedy walk, the overshoot bounded by the last term; two targets give any lim sup and lim inf; 3.55; the sawtooth is conditionally convergent. | The overshoot envelope to 4,000 terms; a rearrangement swinging between 0 and 1 (turning points approaching both); Σ sin(k)/k reordered to 3 within 3 × 10⁻⁵ after 2 × 10⁶ terms. |
| 9 | `Continuity` | Limits of functions (4.1); continuity (4.5) on the function game board; sequences (4.2, 4.6) and sin(1/x); preimages of open sets (4.8); compositions (4.7), sums and products (4.9). | For x² at 3: the largest δ for ε = 1, 0.5, 0.1 (0.0166 = √9.1 − 3), by bisection, asserted. |
| 10 | `Compactness` | Continuous images of compact sets (4.14); extreme values (4.16) and three failures; continuous inverses (4.17) and [0, 2π) → circle (4.21); uniform continuity (4.18) as a sliding box; 1/x; 4.19 via a finite subcover. | √x with δ = ε² on a grid; the best δ for 1/x at seven points, matching x − 1/(1/x + ε); a finite subcover of √x's δ-intervals. |
| 11 | `Connectedness` | Connected images (4.22); intermediate values (4.23); x² − 2 on Q; kinds of discontinuity (4.26); monotone functions (4.29–4.31); Thomae's function (Exercise 4.18). | The rationals of denominator ≤ 60 (1,103 points); δ = 0.0071 at 1/√2 for ε = 0.1 (to 7/10); a staircase with jumps at the 489 rationals of denominator ≤ 40. |
| 12 | `Derivative` | The derivative (5.1); zooming to straightness, \|x\|, and Rudin's 7.18 function; the best linear approximation; 5.2; the chain rule (5.5); x² sin(1/x) (5.6). | Difference quotients of Rudin's function at 0.3 exceeding (3ᵐ + 1)/2; h sin(1/h) → 0. |
| 13 | `MeanValue` | Local extrema (5.8); the mean value theorem by a vertical shear (5.9–5.10); monotonicity (5.11); Darboux (5.12); L'Hôpital (5.13) as chord and tangent slopes. | The tangent point ξ by root-finding; f′ of x² sin(1/x) crossing every level in [−0.9, 0.9] near 0. |
| 14 | `Taylor` | Taylor polynomials of sin x and log(1 + x); Taylor's theorem (5.15) by repeated mean value theorems; Lagrange's error bound for e; e^(−1/x²) (Exercise 8.1). | Errors of e's Taylor polynomials under e/(n + 1)!; the first ten derivatives of e^(−1/x²) at 0 (sympy, all 0); e^(−1/x²) < x¹⁰ on (0, 0.2]. |
| 15 | `Outro` | e^(it): the mean value theorem fails for vector-valued functions, the inequality (5.19) survives; recap; the ledger's second row; Part 3's main problem (m/(m + n), Rudin 7.2); sources. | — |

## The visual language

Part 2 adds two instruments to Part 1's (the rational ruler, ladders of derivation lines, museum cards, the ledger):

* **The ε–δ game board** ([`explainer/analysis/gameboard.py`](../../explainer/analysis/gameboard.py)): a yellow
  band of half-width ε, a teal strip of half-width δ (or a threshold N for sequences), and the graph over the strip
  colored green where it stays in the band and red where it escapes. The largest winning δ is found by bisection
  and asserted. The same board with δ fixed before the point moves is uniform continuity.
* **Log-scale plots** for slow phenomena: harmonic growth, condensation, the swinging rearrangement, n^(1/n).

| Concept | Color |
|---|---|
| ε, tolerances, highlights | yellow |
| δ, N, responses | teal |
| sequences, partial sums, the hero function | blue |
| approximants, rearranged sums | magenta |
| winning / losing parts of the graph | green / red |
| a hole: where a limit should be and is not | red ring |
| the rationals | grey |

## Computations (`compute.py`)

| Item | What | Checks |
|---|---|---|
| `rearrange` | greedy rearrangements of 1 − 1/2 + ⋯ to π, −1, +∞ (10⁶ terms) | within 10⁻⁵ of π and −1; overshoots bounded by the last term; Pringsheim's ratio e^(2(π − ln 2)) within 1%; the natural order → ln 2 |
| `swing` | a rearrangement swinging between 0 and 1; Σ sin(k)/k reordered to 3 | turning points within the last term of 0 and 1, approaching them; the reordered sum within 10⁻⁴ of 3; the natural order within 10⁻⁵ of (π − 1)/2 |
| `sequences` | 1/n, (−1)ⁿ/n, n^(1/n), (1 + 1/n)ⁿ | thresholds; n^(1/n) peaks at n = 3 |
| `cauchy` | tails of 1 − 1/2 + ⋯; convergents of √2; a spiral's hulls; (1 + 1/n)ⁿ | diam Eₙ = 1/(N + 1); p² − 2q² = ±1 and diam = 1/(qₙqₙ₊₁) exactly; hull diameters decreasing; increasing, below 3 |
| `limsup` | tail sups/infs; the rationals by denominator; n^(1/n); n¹⁰/1.1ⁿ | the tail sups match the closed form; the binomial bound; peak at n = 105, below 1 from n = 686 |
| `pseries` | Σ 1/nᵖ to 10⁶; Oresme's blocks; condensation; Σ 1/(n log n) | ln N + γ, π²/6, ζ(3/2) with the tail size; blocks ≥ 1/2 exactly; ½ t_k ≤ s ≤ t_k |
| `etail` | q!(e − s_q); the binomial terms of (1 + 1/n)ⁿ | in (0, 1/q); 0 < e − sₙ < 1/(n!·n); the terms sum to (1 + 1/n)ⁿ (to 10⁻⁴⁰) and stay below s_n |
| `tests` | Rudin 3.35(b) | ratios → 0 and ∞; roots → 1/√2; the sum is 3/2 |
| `power` | Σ zⁿ/n at four points; the series of 1/(1 + x²) | −ln 2 at z = −1; −log(1 − z) inside; divergence outside; converges at 0.9, not at 1.1 |
| `abel` | summation by parts; Σ e^(ikx); Σ sin(k)/k | the identity on random data; the circle; Dirichlet's tail bound |
| `product` | the Cauchy product of Σ (−1)ⁿ/√(n + 1) with itself | \|cₙ\| ≥ 2(n + 1)/(n + 2) |
| `deltas` | largest δ for x² at 3, 1/x on (0, 1), √x on [0, 1] | √9.1 − 3; x − 1/(1/x + ε); δ = ε² works for √x |
| `thomae` | Thomae's function; a monotone function jumping at every rational | δ at 1/√2 is the distance to 7/10; every value inside the strip is below ε; monotone |
| `wiggle` | x² sin(1/x); Rudin's nowhere-differentiable function | \|h sin(1/h)\| ≤ h; Darboux's crossings; quotients ≥ (3ᵐ + 1)/2 |
| `taylor` | e^(−1/x²); Lagrange's bound for e; log(1 + x) | ten derivatives 0 at 0 (sympy); errors under the bound; radius 1; below x¹⁰ |

## Fact-check notes and sources

The mathematics follows W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (McGraw-Hill, 1976), chapters 3–5
(and Exercise 8.1, Example 7.2, Definition 9.11, Theorem 7.18 for forward references); theorem numbers on screen
are that edition's.

* **Bolzano**'s 1817 paper (*Rein analytischer Beweis …*) on the intermediate value theorem; **Cauchy**'s *Cours
  d'analyse* (1821) and *Résumé des leçons* (1823), where e^(−1/x²) appears as a function not given by its Taylor
  series.
* **Oresme** (c. 1350) for the divergence of the harmonic series; **Euler** (1734) for π²/6.
* **Riemann**'s rearrangement theorem is in his 1854 Habilitationsschrift on trigonometric series (published
  posthumously), the same work that introduced his integral.
* Summation by parts goes back to **Abel** (1826); the test is named for **Dirichlet** (published posthumously
  in 1862 as a proof of a theorem of Abel's). The narration does not date it.
* **Mertens** (1875) for the Cauchy product theorem; **Darboux** (1875) for the intermediate value property of
  derivatives; **Thomae** (1875) for his function; **Hermite** (1873): e is transcendental (Rudin points to a proof).
* The claim that no function is continuous exactly at the rationals is a consequence of Baire's theorem (Part 8);
  it is not in Rudin's chapter 4.

On-screen simplifications:

* The hulls of a spiral's tails stand in for the closures of the tails (same diameter); the screen says so.
* Rudin's nowhere-differentiable function is rescaled vertically in the zoom panel; the panel says so.
* The monotone function with a jump at every rational is drawn with denominators up to 40.
