# Analysis, Built — Part 1: The Real Numbers and the Shape of Space

Part 1 of a ten-part series that builds mathematical analysis from the holes in the rational numbers to the
spectral theorem, following the arc of Walter Rudin's three textbooks (*Principles of Mathematical Analysis*,
*Real and Complex Analysis*, *Functional Analysis*). This part covers chapters 1 and 2 of *Principles*, in an
hook and eleven chapters:

* **The real numbers.** Fourier's 1807 claim and the century of questions it raised. The rationals as an ordered
  field, dense and full of holes: √2 is irrational, and Rudin's Theorem 1.1, proved by the map p ↦ (2p + 2)/(p + 2),
  run step by step. Suprema and the least-upper-bound property. Dedekind's cuts: the order, the one-line proof
  that the supremum of a set of cuts is their union, arithmetic, and the Cantor–Méray construction by Cauchy
  sequences. The Archimedean property, the density of Q, √2 = sup A, nested intervals, and the bisection engine.
* **Counting.** Countable and uncountable sets, the zigzag through the fractions, countable unions, Cantor's
  diagonal, R uncountable, and transcendental numbers.
* **The shape of space.** Cauchy–Schwarz (as "the gap between x and its shadow has nonnegative length"), the
  triangle inequality, metric spaces, four metrics on the plane and their balls, and the sup distance between
  two functions. Open and closed sets, closures, relative openness. Compactness as a game of open covers;
  compact sets are closed; nested compact sets; limit points. Heine–Borel by bisection, with the same hunt run on
  (0, 1] to show exactly where closedness is used. Perfect sets are uncountable; the Cantor set and the Cantor
  function. Connected subsets of R are the intervals; Q splits at √2; the topologist's sine curve.
* **A warning.** In C[0, 1] the closed unit ball is closed and bounded but not compact.

Every theorem is proved on screen; every number the narration states is computed in
[`compute.py`](compute.py) (exactly, with Python fractions and integers, wherever possible) and asserted.
Schematics are labeled `schematic`.

The series plan is kept outside the repository; the shared instruments live in
[`explainer/analysis`](../../explainer/analysis/__init__.py).

## Build it

The finished video is not stored in the repository. From the repo root, after the one-time setup in the
[top-level README](../../README.md#quick-start):

```bash
python -m videos.analysis1.compute                # once: every computed item (a few seconds; cached in .cache/analysis1)
python tools/build.py analysis1 -q k --fps 60     # the full-quality cut: 2160p60 + subtitles + chapters -> renders/analysis1_2160p.mp4
python tools/build.py analysis1                   # 1080p30 -> renders/analysis1.mp4
python tools/build.py analysis1 -q l              # fast 480p preview
python tools/export_script.py analysis1           # regenerate SCRIPT.md from the code
python tools/check_narration.py analysis1         # Whisper listen test of every narration line
```

## Chapters (49:26)

```
0:00 Fourier's question, and the holes in the fractions
4:28 1. Holes in the rational line
9:15 2. Filling the holes: Dedekind cuts
14:28 3. Archimedes, density and decimals
18:11 4. Counting infinities
22:34 5. What “close” means: metric spaces
26:44 6. Open and closed sets
31:25 7. Compactness
35:09 8. Heine–Borel, by bisection
38:43 9. The Cantor set
42:36 10. Connectedness
45:24 11. A first space of functions
47:48 Recap, and the first row of the ledger
```

## Outline

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Fourier's sawtooth as a sum of sines; a limit of smooth functions with a jump; every partial sum is 0 at the jump; the 8.95% overshoot. Lagrange's objection and the questions that followed (limit, function, integral, number). The sequence 1, 1.4, 1.41, … has nowhere to land in Q. The series and its ten parts; the thesis (when may two limits be swapped? m/(m + n), Rudin 7.2); the ledger. | Partial sums of Σ sin(kx)/k up to n = 200; the overshoot checked against Si(π) at n = 5000; the rationals in windows down to width 2.5 × 10⁻⁶ around √2. |
| 1 | `Holes` | Q as an ordered field; density by averages; the picture is the real line, Q is only the ticks. √2 is irrational. Rudin 1.1: A = {p² < 2} has no largest element, B no smallest, by q = (2p + 2)/(p + 2) and q² − 2 = 2(p² − 2)/(p + 2)². Upper bounds, sup; the upper bounds of A in Q are exactly B, so sup A does not exist in Q. The least-upper-bound property; Rudin 1.19. | The hops 1 → 4/3 → 7/5 → 24/17 → 41/29 and 2 → 3/2 → 10/7 → 17/12 in exact fractions, with their squares; the ruler colored by the sign of p² − 2q² (exact integers). |
| 2 | `Cuts` | Dedekind cuts (I)–(III); (1/2)* and the cut of √2, whose condition (III) is Rudin 1.1. R = all cuts, ordered by inclusion; totality in three lines. sup = union: the five-step proof. Arithmetic, 0*, the embedding r ↦ r*. Rudin 1.19 (existence and uniqueness). Cantor–Méray: two Cauchy sequences for √2 whose difference → 0. | The cuts drawn from their exact rational members; the decimals and hops of √2 and their differences. |
| 3 | `Archimedes` | The Archimedean property (1.20) by contradiction with α = sup{nx}. Density of Q: a ruler with spacing 1/28 < 0.45 − (√2 − 1) must land inside. √2 exists: y = sup A, and both y² < 2 and y² > 2 contradict the hop. Decimals as nested intervals; the nested-interval theorem via sup aₙ; why both "closed" and "complete" matter. The bisection engine. | 40 digits of √2 by integer square roots, every decimal interval asserted to contain it; 30 bisection steps in exact dyadics. |
| 4 | `Counting` | Pairings; countable; Z; the zigzag through p/q (skipping repeats) lists Q; countable unions (2.12); the diagonal (2.14); s ↦ Σ 2sₖ/3ᵏ is one-to-one, so R is uncountable; algebraic numbers are countable, so almost every real is transcendental (Cantor 1874; Liouville, Hermite, Lindemann). | The first 40 rationals in zigzag order; a seeded 12 × 16 table of 0–1 sequences and its flipped diagonal, asserted different from every row. |
| 5 | `Distance` | Rᵏ, the inner product and norm. Cauchy–Schwarz (1.35) from 0 ≤ \|Bx − Cy\|², with B = \|y\|², C = x·y, as "the gap between x and its shadow". The triangle inequality. Metric spaces (2.15; Fréchet 1906). Euclidean, taxicab, max and discrete balls; d∞ ≤ d₂ ≤ d₁ ≤ 2d∞. C[0, 1] with the sup distance; balls are tubes. | The sup distance between f = 0.25 + 0.5x² and g = 0.55 + 0.25 sin 7x: 0.5267 at x = 0.2074 (grid search refined by bounded minimization). |
| 6 | `OpenClosed` | Neighborhoods, interior and limit points, open and closed (2.18); balls are open (2.19); limit points see infinitely many points (2.20); E open ⇔ Eᶜ closed (2.23); unions and finite intersections (2.24) and ⋂(−1/n, 1/n) = {0}; Rudin's table of plane sets; perfect sets; closure, density, sup E ∈ Ē (2.26–2.28); relative openness (2.30). | — |
| 7 | `Compact` | Finite sets have maxima and repeat values; open covers and compactness (2.31–2.32); the cover game; (0, 1) and R lose; compactness is intrinsic (2.33). Compact ⇒ closed (2.34), with the disjoint-disks proof; closed subsets (2.35); nested compact sets (2.36); infinite subsets have limit points (2.37). | A seeded random cover of [0, 1] by 70 open intervals and the 9-interval subcover the greedy walk finds (coverage asserted on a 10⁵-point grid). |
| 8 | `HeineBorel` | k-cells are compact (2.40) by bisection (schematic); the same hunt on (0, 1] closes in on the missing 0. Heine–Borel (2.41) with its three implications; (a) ⇒ (b) is special to Rᵏ. Bolzano–Weierstrass (2.42). | 4,000 points (cos n, sin √2 n), the quarter with the most points chosen four times. |
| 9 | `Cantor` | Nonempty perfect sets are uncountable (2.43), by nested compact sets. The Cantor set (2.44): compact, nonempty, no interval, perfect, uncountable, removed length 1. Base-3 digits 0 and 2; 1/4 = 0.0202…₃ is in it but is never an endpoint; zooming by 9 about 1/4 repeats the picture. The Cantor function. | The intervals to depth 12 (2ⁿ pieces, total (2/3)ⁿ, asserted); the digits of 1/4 in exact arithmetic; F(1/4) = 1/3. |
| 10 | `Connected` | Separated sets and connectedness (2.45); the connected subsets of R are the intervals (2.47), the seam found by a supremum; Q splits at √2 and is totally disconnected; preview of the intermediate value theorem; the topologist's sine curve. | sin(1/x) sampled uniformly in phase (60,000 points). |
| 11 | `FunctionSpace` | The closed unit ball of C[0, 1] is closed and bounded; the tents on [1/(n + 1), 1/n] are pairwise at distance 1, so it is not compact; infinitely many directions; the dictionary Rᵏ ↔ C[0, 1] and what replaces Heine–Borel (Arzelà–Ascoli, Part 3; Riesz, Part 8). | The 12 × 12 table of sup distances between tents (off-diagonal entries asserted equal to 1). |
| 12 | `Outro` | Recap in eleven lines; the ledger's first row; Part 2's opening (the rearrangement theorem); sources. | — |

## The visual language

* **The rational ruler.** Q is drawn as ticks, the tick of p/q (in lowest terms) rising in proportion to
  q^−0.6, so both the density of the fractions and their hierarchy are visible. The fractions in each window are
  enumerated exactly at every frame by a Stern–Brocot search in integer arithmetic (about 1,400 fractions per
  frame in under a millisecond, even at window width 10⁻¹²), so a zoom shows the right fractions at every depth.
  Part 2 reuses it for Thomae's function.
* **The narration says what the picture is.** The line under the ticks is named as already being the real line,
  and pictures of things that cannot be drawn exactly (the k-cell bisection, the equidistant tents) are labeled
  `schematic`.
* **Proofs as ladders.** Each derivation line grows out of the previous one, with a grey note saying why it
  follows; long proofs get numbered steps.
* **Counterexample cards** (a red corner tag): the Cantor set, the Cantor function, the topologist's sine curve.
* **The chapter cards** carry a strip of the history from 1800 to 1970, with the years of the chapter lit.

| Concept | Color |
|---|---|
| the lower set of a cut, A = {p² < 2}, its elements | blue |
| the upper set, B = {p² > 2}, upper bounds | coral |
| a hole: where a limit should be and is not | red ring |
| ε, tolerances, highlights | yellow |
| δ, N, responses, rulers | teal |
| sequences, the hero function f | blue |
| approximants (partial sums), the second function g | magenta |
| open sets, neighborhoods (dashed edge, airy fill) | light blue |
| closed sets, closures | orange |
| compact sets, finite subcovers, nested cells | gold |
| connected sets | green |
| distances, norms, tubes | pale gold |
| inner products, projections | lilac |
| the rationals | grey |
| counterexamples (museum tag) | red |

## Computations (`compute.py`)

| Item | What | Checks |
|---|---|---|
| `sawtooth` | (π − x)/2 on (0, 2π) and Σ_{k≤n} sin(kx)/k for n = 1 … 200 | every partial sum is 0 at the jumps; at x = 1, 2, 4 the sum to 20,000 terms is within 2 × 10⁻⁴; the first peak at n = 5000 is within 10⁻³ of Si(π) = 1.8519; (Si(π) − π/2)/π = 8.95% |
| `hops` | Rudin's map from 1 upward and from 2 downward, nine steps each, as exact fractions | q² < 2 and q > p on the way up, q² > 2 and q < p on the way down; q = (2p + 2)/(p + 2) and q² − 2 = 2(p² − 2)/(p + 2)² exactly |
| `sqrt2` | 40 digits of √2 by `isqrt`; 30 bisection steps on [1, 2] | each decimal interval [⌊√2·10ᵏ⌋, +1]/10ᵏ contains √2 (integer comparison); aₖ² < 2 < bₖ² |
| `diagonal` | 12 seeded 0–1 sequences (16 digits shown) | the flipped diagonal differs from row k at place k |
| `qorder` | the zigzag order of p/q | starts 1, 2, 1/2, 3, 1/3, 4; 2/2 is skipped |
| `supdist` | sup \|f − g\| on [0, 1] | grid maximum and bounded minimization agree to 10⁻⁶ |
| `cover` | 70 random open intervals covering [0, 1]; the greedy subcover | the cover covers a 10⁵-point grid with margin; the subcover (9 intervals) covers it |
| `cantor` | the Cantor set's intervals to depth 12; the digits of 1/4; the Cantor function | 2ⁿ intervals of total length (2/3)ⁿ; 1/4 = 0.0202…₃, inside the depth-12 set but never an endpoint; F(1/4) = 1/3; F nondecreasing |
| `bumps` | the tents on [1/(n + 1), 1/n], n ≤ 12 | sup distances are exactly 1 off the diagonal |

## Fact-check notes and sources

The mathematics follows W. Rudin, *Principles of Mathematical Analysis*, 3rd ed. (McGraw-Hill, 1976), chapter 1
and its appendix, and chapter 2; theorem numbers on screen are that edition's. Companion treatments: S. Abbott,
*Understanding Analysis*; C. Pugh, *Real Mathematical Analysis*; T. Tao, *Analysis I*.

* **Fourier** submitted *Mémoire sur la propagation de la chaleur dans les corps solides* to the Institut de France
  in December 1807; the examiners included Lagrange, Laplace, Monge and Lacroix, and Lagrange objected to expanding
  arbitrary functions in trigonometric series. The theory appeared as *Théorie analytique de la chaleur* (1822).
* **Cauchy**, *Cours d'analyse* (1821); **Dirichlet**, on the convergence of Fourier series (1829), where the
  indicator of the rationals appears; **Riemann**'s Habilitationsschrift on trigonometric series (1854, published
  1867) introduced his integral; **Cantor**'s work on the uniqueness of trigonometric series (1870–1872) led to set
  theory.
* **Dedekind**, *Stetigkeit und irrationale Zahlen* (1872), the cuts (conceived 1858); **Cantor** (1872) and
  **Méray** (1869, 1872): reals from Cauchy sequences of rationals.
* **Cantor** (1874): the algebraic numbers are countable and the reals are not (by nested intervals); the diagonal
  argument is from 1891. **Liouville** (1844) gave the first explicit transcendental numbers; **Hermite** (1873)
  proved e transcendental, **Lindemann** (1882) π.
* **Fréchet**'s thesis (1906) introduced metric spaces; **Hausdorff** (1914) named them.
* **Heine** (1872) and **Borel** (1895) for the covering theorem (the name is Schoenflies's, 1900).
* **The Cantor set**: Cantor (1883); H. J. S. Smith described such sets in 1875. The Cantor function: Cantor (1884).
* "The next best thing to being finite" is a common description of compactness; it is not quoted from a specific
  author. T. Tao's essay *Compactness and compactification* describes compact spaces as "almost finite".
* The **topologist's sine curve** is not in Rudin (see Munkres, *Topology*, §24).

On-screen simplifications, stated here for the record:

* The ruler's ticks are capped in height (at 1.6 times the reference height), and the window's tick density targets
  about 1,300 fractions; the narration says the line under the ticks is the real line.
* The bisection of a k-cell is labeled `schematic`: a cover with no finite subcover does not exist, so the nested
  squares are drawn toward a chosen point. The equidistant tents are drawn as a complete graph, labeled
  `schematic` and "impossible to draw flat".
* The Cantor set is drawn to depth 12 at each zoom; the screen says so.
