# Analysis, From the Real Line to Functional Analysis: the series plan

A ten-part, 3Blue1Brown-style explainer series that builds analysis from the holes in the
rational numbers to the spectral theorem for unbounded operators, following the arc of Walter
Rudin's three books: *Principles of Mathematical Analysis* ("Baby Rudin"), *Real and Complex
Analysis* ("Papa Rudin") and *Functional Analysis* ("Grandpa Rudin"). Every video is math-heavy
in the way the repo's stochastic-calculus, quantum and relativity videos are: every theorem is
proved on screen, one line at a time, every counterexample is a real computed object you can
zoom into, and every number the narration says is computed and asserted at render time.

This document is the plan: how the series is organized and why, what each video contains chapter
by chapter, the visual language shared by all ten, and how the production maps onto this repo's
tooling. Nothing is rendered yet.

---

## 0. The series on one page

**Working title:** *Analysis, Built: From the Real Line to Functional Analysis*
(each part keeps its own title; the series title is for the playlist and the READMEs).

**Thesis (the sentence every video returns to):** *Analysis is the art of interchanging two
limits, and each new space in this series is invented to make one more interchange legal.*
Rudin says it himself at the start of chapter 7 ("the main problem"): continuity, derivatives,
integrals and sums are all limits, and almost every theorem in the series is a statement of the
form "under these hypotheses, lim lim = lim lim". Uniform convergence, the dominated convergence
theorem, Fubini, differentiation under the integral sign, the Banach–Steinhaus theorem, the
spectral theorem: all of them.

**The hero problem (the concrete thread):** *Fourier's claim of 1807 that any function is a sum
of sines.* Historically this one claim forced the invention of the modern definitions of function,
limit, integral, set, measure and Hilbert space, and the series tells it that way, with one fixed
hero function (a sawtooth) and one fixed continuous function whose Fourier series diverges at a
point. Each video adds a new, sharper answer to "in what sense does the Fourier series of f
converge?":

| Part | Answer so far |
|---|---|
| 1 | We cannot even ask: we need to say what a limit, and a number, is. |
| 2 | Convergence of a series is defined; rearrangements can change the sum. |
| 3 | For a Riemann-integrable f, the Fourier series converges in mean square (Parseval); at a point where f is Lipschitz it converges to f(x); Gibbs' overshoot is 8.9%. |
| 5 | The integral is rebuilt so that limits can pass under it. |
| 6 | For every f in L², the series converges in L²; Fejér's means converge for continuous f. |
| 8 | There is a continuous f whose Fourier series diverges at a point (Baire); the dual of C(T) is the space of measures; Carleson is quoted. |
| 9 | Every distribution has a Fourier series (and a Fourier transform), and it always converges. |
| 10 | The Fourier transform is the spectral theorem for d/dx: it diagonalizes translation. |

**The structural thread:** completeness. Part 1 builds the one complete ordered field; every later
part proves one new space complete (R^k, C(X), L^p, H, the Fréchet spaces of test functions, a
Banach algebra) and immediately cashes it in (Bolzano–Weierstrass, Arzelà–Ascoli, the contraction
principle, Riesz–Fischer, the projection theorem, Baire and its three children, Neumann series and
the spectrum).

**Ten parts in three seasons** (one season per book), 50–65 minutes each, about 9.5 hours in all:

| # | Part | Source chapters | Length |
|---|---|---|---|
| **Season 1: the real line and its functions (Baby Rudin)** | | | |
| 1 | The Real Numbers and the Shape of Space | PMA 1–2 | ~55 min |
| 2 | Limits: Sequences, Series, Continuity and the Derivative | PMA 3–5 | ~60 min |
| 3 | Integration and the First Function Space: Uniform Convergence, Arzelà–Ascoli, Weierstrass | PMA 6–8 | ~60 min |
| 4 | Calculus in Many Dimensions: Linear Maps, Contractions and the Inverse Function Theorem | PMA 9 (+ a tour of 10) | ~45 min |
| **Season 2: measure, Hilbert space and the complex plane (Papa Rudin)** | | | |
| 5 | Measure: The Lebesgue Integral and Why Limits Pass Under It | PMA 11; RCA 1–2, 8 | ~65 min |
| 6 | L^p, Hilbert Space and the Geometry of Functions | RCA 3–4, 6–7 | ~60 min |
| 7 | Complex Analysis, the Part the Rest of Analysis Needs | RCA prologue, 10–14, 17 (highlights) | ~55 min |
| **Season 3: functional analysis (Grandpa Rudin)** | | | |
| 8 | Banach Spaces: Baire's Theorem and Its Three Children, Hahn–Banach, and Weak Topologies | RCA 5; FA 1–5 | ~65 min |
| 9 | Distributions and the Fourier Transform: Differentiating Anything | RCA 9; FA 6–9 | ~60 min |
| 10 | Banach Algebras and the Spectral Theorem | RCA 18; FA 10–13 | ~65 min |

**Audience:** someone who has seen calculus and a little linear algebra and wants the real thing.
The series is self-contained: nothing is assumed beyond what an earlier part proved, and each part
opens on the "ledger" of what has been built so far.

**What the series deliberately compresses** (section 1.4 has the reasoning): differential forms and
Stokes' theorem (PMA 10) become a 6-minute guided tour inside Part 4; the complex-analysis half of
Papa Rudin (RCA 10–17, 19–20) becomes one video, Part 7, that proves exactly what Parts 8–10 need
(Cauchy's theorem, power series, Liouville, the open mapping and maximum modulus theorems, Runge,
normal families and the Riemann mapping theorem) and tours the rest; Grandpa Rudin's chapter 5 of
applications is sampled, not covered.

---

## 1. Why this organization

### 1.1 Follow the mathematics, not the tables of contents

The three books are not a sequence; they overlap (Baby Rudin 11 and Papa Rudin 1 both build the
Lebesgue integral; Papa Rudin 5 and Grandpa Rudin 2 both prove the Banach–Steinhaus and open
mapping theorems; Papa 9, Papa 19 and Grandpa 7 all do Fourier transforms and Paley–Wiener). The
series therefore merges each topic into the one place where it has the best story and the
prerequisites are fresh:

* The Lebesgue integral is built once, in Part 5, from Papa Rudin's abstract chapter 1 (the
  cleanest proofs of the convergence theorems) with Baby Rudin 11's comparison to the Riemann
  integral as its payoff.
* Baire's theorem and its children are proved once, in Part 8, in Grandpa Rudin's generality
  (F-spaces), with Papa Rudin 5's Fourier-series application as the showpiece.
* Fourier transforms are done once, in Part 9, going straight from L¹ and L² (Papa 9) to tempered
  distributions and Paley–Wiener (Grandpa 7).

### 1.2 Each part is a stand-alone video with a hook, a derivation arc and a payoff

The repo's house style (see the README's "How a video is made") is kept: a concrete hook in the
first two minutes, intuition before symbols, then the derivation line by line, then a payoff that
the hook promised. Every part also ends on the **ledger** (section 2.3), so the series can be
watched in order as one course, or any part can be watched alone after a two-minute recap.

### 1.3 The Fourier thread is historically honest

The sequence Fourier (1807) → Dirichlet's convergence theorem (1829) → Riemann's integral, invented
in his 1854 paper on trigonometric series → Cantor's sets, invented for the uniqueness of
trigonometric series (1870–72) → Dedekind's and Cantor's real numbers (1872) → Weierstrass's
function (1872) → Borel/Lebesgue measure (1898–1902) → Hilbert, Schmidt, Riesz and Fischer (1906–07)
→ Banach (1922–32) → Banach–Steinhaus (1927) → Schwartz's distributions (1945–50) → Carleson (1966)
is the real history, and it is exactly the order of the series. A timeline strip that lights up as
the series proceeds makes this visible (section 2.2, instrument 9).

### 1.4 What is compressed, and why

* **PMA 10 (differential forms, Stokes).** Rudin's own preface says it may be omitted; nothing in
  Seasons 2–3 uses it. Part 4 ends with a six-minute tour (change of variables with the Jacobian
  as the area factor, partitions of unity, what a k-form is, Stokes' theorem stated) that is
  labeled as a tour: statements, pictures, no proofs. If you want the full chapter, it becomes an
  optional Part 4b (see section 6).
* **Papa Rudin's complex half.** The road to functional analysis needs: holomorphic functions have
  power series (Neumann series, the resolvent), Liouville (Gelfand–Mazur), the Cauchy integral
  formula (the holomorphic functional calculus, the spectral radius formula), the maximum modulus
  principle (Phragmén–Lindelöf, the Riesz–Thorin interpolation sketch), Runge (rational
  approximation in the functional calculus), and normal families (Montel's theorem is
  Arzelà–Ascoli's grandest payoff: the Riemann mapping theorem). Part 7 proves those and tours the
  rest (harmonic functions and the Poisson integral, Weierstrass products and Blaschke products,
  analytic continuation and Picard, H^p spaces and Beurling's theorem on the shift, Mergelyan).
* **Grandpa Rudin 5 (applications).** Three are kept because they pay off earlier threads: the
  generalized Stone–Weierstrass via Krein–Milman, Haar measure via a fixed-point theorem, and
  Grothendieck's theorem on closed subspaces of L^p (a closed-graph application). The rest are
  named in the recap.
* **Not compressed:** the proofs. The house rule stands: no theorem is stated without its proof
  (or, for the three or four giants, its complete proof map with every step shown and the routine
  epsilon management summarized in one labeled line).

### 1.5 Length

Ten parts at 50–65 minutes is about 9.5 hours; about 155 chapters of 2.5–4 minutes. That is the
length of a two-semester course in Baby Rudin plus a one-year graduate course in Papa Rudin plus a
one-semester course in Grandpa Rudin, told at lecture pace but with no time lost to homework. The
repo's precedent is two-part series (relativity, quantum) of 56–69 minutes per part; this plan
keeps that part length and adds parts rather than stretching any one.

---

## 2. The visual language of the series

The repo's rules apply (one color per concept everywhere; narration is the clock; derive on screen;
real objects, not cartoons; schematics labeled `schematic`). On top of them the series adds a
shared color legend, nine recurring "instruments", and conventions for proofs. All of it lives in a
new shared package, `explainer/analysis/`, so that Part 8 can reuse Part 1's widgets unchanged.

### 2.1 Color legend (series-wide; new entries for `explainer/style.py`)

Where a concept already has a color in another video of the repo, the series reuses it, so that a
viewer who has seen the quantum or relativity videos finds the same meanings.

| Concept | Color | Reused from |
|---|---|---|
| ε: a tolerance, a target band, "how close" | yellow | — |
| δ, N: the response, "how near / how far out" | teal | the repo's time/clock color (teal) is close; this is a new meaning, so a slightly different teal |
| points of a sequence x_n, the hero sequence | blue | — |
| the limit, the true value, the exact object | white | MEAN in stochastic |
| the hero function f | blue | XPOS/position space in quantum |
| approximants: f_n, partial sums, polynomials, Fejér means | magenta `#F0ABFC` | APPROX in quantum2 |
| open sets, neighborhoods, balls (dashed edge, airy fill) | light blue | — |
| closed sets, closures, boundaries (solid edge) | orange | — |
| compact sets, finite subcovers, "finiteness in disguise" | gold | — |
| connected sets, intervals, paths | green | — |
| rationals, countable scaffolding, dust | grey | DIM |
| upper sums / lower sums, suprema / infima | soft red / soft green | RIGHT_PT / LEFT_PT in stochastic |
| measure μ, lengths, areas, outer-measure covers | amber `#F2A541` | HOT in stochastic |
| null sets, "almost everywhere" exceptions | dark grey, hatched | FAINT |
| simple functions, step functions, integrators α | light brown | — |
| norms, distances, tubes around graphs | gold | — |
| inner products, orthogonality, projections | lilac | HBAR in quantum (same family: Hilbert space) |
| functionals, dual spaces, hyperplanes (drawn as stacks of level sets) | light brown stacks | COVECTOR in relativity |
| weak and weak-* topologies, "shadows" of a sequence | ghosted blue, dashed | — |
| the frequency side: Fourier coefficients, Fourier transforms | orange | MOMENTUM in quantum |
| operators T, A; their graphs | indigo `#7C7FE0` | — |
| spectra, eigenvalues, resolvent sets | green / dark | ENERGY in quantum |
| test functions φ (bumps) | light green | — |
| distributions, δ, principal values | rose `#FF6B8B` | — |
| counterexamples and pathologies (museum-card corner tag) | red | DANGER in riemann |
| theorem names, the ledger, chapter cards | white on the house background | — |

Complex numbers on screen use the repo's phase-as-hue map (quantum's `colormap.py`), with the phase
wheel in the corner, so domain colorings in Parts 7 and 9 look like the Riemann and quantum videos.

### 2.2 The nine instruments (recurring visual devices)

These are the series' signature visuals. Each is one reusable Manim component, introduced in the
first part that needs it and then used without re-explanation.

1. **The ε–δ game board.** Quantifiers are moves in a two-player game, and the order of the moves
   is the whole content of a definition. The board shows the graph of f; player ε (yellow)
   chooses a horizontal band; player δ (teal) answers with a vertical band; the graph must pass
   through the box they make. The same board, with different rules about who moves when and what
   is fixed before the game starts, defines: a limit, continuity at a point, uniform continuity
   (δ is chosen before x is revealed), uniform convergence (N before x), equicontinuity (δ before
   both x and the function in the family), Cauchy sequences, and in Part 8 boundedness of a
   family of operators. The board plays itself: for the actual function on screen and the actual
   ε, the widget computes the largest working δ and the narration quotes it (asserted). The
   counterexamples are the games the responder loses (1/x on (0, 1): no δ works for every x).
2. **The convergence dashboard.** One sequence of functions, five lenses at once: pointwise (a
   vertical probe at a chosen x), uniform (the yellow tube of height 2ε around the limit), L¹
   (the shaded area between), L² (the energy), and "tested" (∫ f_n φ for a bump φ, which becomes
   weak and distributional convergence later). Each lens shows its own number and lights up when
   it converges. The dashboard's regulars, introduced in Part 3 and recurring through Part 10:
   x^n on [0, 1]; the moving bump n·x(1 − x²)^n; the tall spike n·1_[0,1/n]; the spreading
   mass (1/n)·1_[0,n]; the typewriter sequence; sin(nx); the unit vectors e_n of ℓ².
3. **The function-as-a-point camera.** A split screen. Left: the graph of f_n. Right: a map of
   the function space in which each function is one dot, with coordinates taken from the first
   two or three Fourier coefficients (or two sampled values), so a sequence of functions becomes a
   trail of dots. Balls in different norms are different regions of the map; the camera is what
   makes "C(X) is a metric space", "the unit ball is not compact", "e_n goes weakly to 0 but not
   in norm" (the trail runs off along ever-new axes while every shadow converges) and "an operator
   moves points" into pictures. Introduced in Part 3, used in Parts 6, 8, 9, 10.
4. **The R^n ↔ function-space dictionary.** A two-column card: the same theorem in R^n (with its
   picture) and in the function space, with the words that changed highlighted. Pythagoras ↔
   Parseval; projection onto a line ↔ projection onto a closed subspace; Bolzano–Weierstrass ↔
   Arzelà–Ascoli (bounded needs equicontinuous); "the gradient" ↔ the Fréchet derivative;
   rank–nullity ↔ the open mapping theorem; "diagonalize a symmetric matrix" ↔ the spectral
   theorem; "eigenvalues" ↔ the spectrum (which can be a continuum with no eigenvalues at all).
5. **The counterexample museum.** Every pathological object gets a museum card (name, who and
   when, what it breaks, where it is in Rudin) and a real, computed, zoomable exhibit. Rudin's
   books are famous for sharp counterexamples and the series keeps every one of them on screen:
   the Dirichlet function, Thomae's popcorn function, x² sin(1/x), e^(−1/x²), the Cantor set and
   function, the fat Cantor set, the topologist's sine curve, Weierstrass's nowhere-differentiable
   function, the moving bump, the typewriter, the Vitali set (the one exhibit that is a labeled
   schematic, because it cannot be computed), Fubini's counterexample, the unit ball of ℓ² (not
   compact), e_n (weakly null, not null), the Dirichlet kernel (its L¹ norm grows like log n), the
   divergent Fourier series of a continuous function, the shift operator (spectrum a disk, no
   eigenvalues for the forward shift), and the symmetric-but-not-self-adjoint derivative.
6. **The proof map.** Long proofs (the Riesz representation theorem, Arzelà–Ascoli, Hahn–Banach,
   the open mapping theorem, the spectral theorem) get a small flowchart of their four or five
   steps that sits in a corner and lights up as the narration passes each step; each step then
   opens into the line-by-line derivation in the repo's usual style (only the changed term is
   colored; a grey note says why the line follows). Routine epsilon bookkeeping is summarized in
   one line that is visibly labeled `ε-bookkeeping, routine`, so the viewer knows exactly which
   steps were abbreviated.
7. **Zoom as argument.** Infinite zooms are the signature of self-similar pathology, and the
   series computes each at the depth the zoom needs: the Cantor set (ternary digits ticking as
   we descend), Weierstrass's function (the next partial sums added as the scale demands), the
   nested intervals of Heine–Borel, the Koch curve as a rectifiability counterexample, and, in a
   cameo, the Brownian path from the stochastic video.
8. **The ledger.** A table that persists across the series and grows by one row per part: the
   space | its completeness theorem | its compactness theorem | the new interchange of limits it
   makes legal | the Fourier answer so far. Each part opens on the ledger as it stood and closes
   by adding its row. It is the series' recap device and its table of contents.
9. **The timeline strip.** The history of section 1.3 as a strip along the bottom of the chapter
   cards; the year of the idea being proved lights up. Portraits are not used (no licensing risk,
   and the repo's style is about the mathematics); names and years are.

### 2.2b The engines: five animations built once and reused everywhere

Underneath the instruments are five animations that recur so often that they are built once, as
parametrized components, and cross-checked against the published visual treatments listed in
section 4.3:

* **Bisection and nested intervals.** Decimal expansions (Part 1), Heine–Borel and
  Bolzano–Weierstrass (Part 1), the intermediate value theorem (Part 2, also run over Q to show it
  fail), Goursat's proof of Cauchy's theorem (Part 7), Baire's shrinking balls (Part 8).
* **The diagonal grid.** Cantor's diagonal (Part 1), Arzelà–Ascoli (Part 3), the fast subsequence
  in Riesz–Fischer (Part 6), sequential Banach–Alaoglu (Part 8).
* **The bump and its evil twins.** One narrowing bump of unit mass is the Landau kernel (Part 3),
  the Fejér and Poisson kernels (Parts 6, 7), the mollifier and δ itself (Part 9), and the
  approximate eigenvectors of the position operator (Part 10). Its evil twins, named after Tao's
  zoo of modes of convergence, are the sliding bump (mass escapes sideways), the tall thin bump
  (escapes upward), the widening bump (spreads thin), the typewriter and the slowly moving
  typewriter: the dashboard's regulars, which return in Fatou, dominated convergence, weak
  convergence and the failure of compactness.
* **The right triangle.** Projection in Hilbert space, Bessel, Parseval, Fourier series as
  projections, Plancherel (Parts 3, 6, 9): one triangle, with the hypotenuse's square filling up.
* **A new direction forever.** The unit vectors e_n as bars sliding to the right: the unit ball of
  ℓ² is not compact (Part 1's preview, Part 3), Riesz's lemma and "locally compact means
  finite-dimensional" (Part 8), and e_n → 0 weakly but not in norm (Part 8).

### 2.3 Conventions for mathematics on screen

* **Picture first, then the ε.** Every theorem is first shown as the picture it is (compactness is
  a finite subcover; the MVT is a tilted tangent; the projection theorem is the nearest point),
  then proved. The proof's one-sentence idea is stated before any symbol appears.
* **Numbers, not just symbols.** Whenever the narration says "for every ε there is a δ", the screen
  shows an actual ε (0.1) and the actual δ that works (0.013 for this f at this x), computed and
  asserted. Whenever a series converges, the partial sums are on screen with their values.
* **Every theorem comes with the counterexample that shows its hypotheses are needed** (Rudin's
  own habit). The card says which hypothesis was dropped.
* **Misconceptions stated and refuted aloud** (as in the quantum videos, after Muller et al.):
  "compact means closed and bounded" (true in R^n only; the unit ball of C[0,1] is the refutation),
  "Lebesgue integrates by slicing horizontally" (half true: the real change is which sets have a
  length; the series uses the honest version, dyadic slicing of the range into measurable level
  sets), "a continuous function is differentiable somewhere", "you can rearrange a convergent
  series", "weak convergence is almost norm convergence", "the spectrum is the set of
  eigenvalues", "an unbounded operator is just a big bounded one".
* **Three-column derivations for inequalities.** Hölder, Minkowski, Bessel, Cauchy–Schwarz and the
  like are derived with the inequality's geometric meaning in a third column (Young's inequality
  is two areas under y = x^(p−1); Bessel is Pythagoras with a leftover).
* **Labeling.** `computed` is the default and is not labeled; `schematic` is labeled; `one step,
  enlarged` is labeled; `tour, no proof` is labeled (used only in Part 4's forms tour and Part 7's
  closing tour).
* **Pictures known to mislead, and the honest version used instead.** The mean value theorem's
  "tilt" is a vertical shear (y ↦ y − chord), never a rotation (a rotation does not preserve
  graphs). Cantor's diagonal flips digits with a rule that avoids 0 and 9, so no 0.4999… = 0.5000…
  duplicate can sneak in, and the screen says why. "Draw it without lifting the pencil" is named
  as the lie it is (Thomae). Uniform continuity is separated from Lipschitz by √x on [0, 1] (the
  box works, the slope does not). Gibbs' overshoot is quoted as 8.95% of the jump, and the
  peak-to-peak 18% convention is named once. The Dirichlet kernel's divergence lives in its side
  lobes, so \|D_n\| is drawn with the lobes shaded, next to the Fejér kernel that has none.
  Hahn–Banach's "one dimension at a time" is shown in R² and the narration says aloud that the
  infinite-dimensional step is Hausdorff maximality, not a picture. Egorov's theorem is shown with
  its finite-measure hypothesis and the counterexample 1_[n, ∞). The Fourier transform uses one
  convention for the whole series, Rudin's f̂(t) = (1/√2π) ∫ f(x) e^(−ixt) dx, and the shift
  operator's direction is fixed on screen before its spectrum is discussed. Zoom animations
  (Cantor, Weierstrass) reach the pixel limit after a dozen levels, and the screen says so rather
  than letting the last frame look smooth.

### 2.4 What is computed

Every exhibit, curve and number is computed in each part's `compute.py` and cached in
`.cache/analysis<N>/`, with checks, in the repo's style. The main kinds: rational approximations
and Dedekind cuts; Cantor-set intervals to depth 30 and the Cantor function; greedy rearrangements
of the alternating harmonic series to any target; largest working δ for given ε by bisection;
Riemann upper and lower sums; Weierstrass partial sums at 20 zoom levels; Landau- and Fejér-kernel
convolutions; Fourier coefficients, Dirichlet and Fejér kernels, Lebesgue constants to n = 10⁶,
Gibbs' overshoot; outer-measure covers and fat Cantor sets; dyadic simple-function approximations;
the escaping-mass sequences under every lens; Fubini's counterexample on a grid; ℓ^p unit balls;
Hilbert-space projections in a sine basis; Picard and Newton iterations; the Riemann mapping of a
polygon (Schwarz–Christoffel, checked against conformality); mollifiers and distributional
derivatives; Fourier transforms by FFT with Plancherel asserted; Paley–Wiener growth of a bump's
transform in the complex plane (domain coloring); discretized operators' spectra and pseudospectra
(the shift, multiplication operators, d/dx with each boundary condition, a Sturm–Liouville
operator); the Schrödinger unitary group from the quantum video's split-operator solver, reused.

---

## 3. The ten parts, chapter by chapter

Each table follows the repo's README convention (`# | Scene | What it establishes | The picture |
Computed on screen`). Chapter counts and minutes are targets; the repo's finished videos run 15–20
chapters at 2.5–4 minutes each. Theorem numbers are from the third editions of PMA and RCA and the
second edition of FA, and are to be re-checked against the books when each script is written.

### Part 1. The Real Numbers and the Shape of Space (PMA 1–2) — ~55 min, 13 chapters

**Hook.** Fourier, 1807: "any function is a sum of sines," with a sawtooth being built from sines
on screen (the hero function, computed; the series' first Fourier partial sums). Lagrange's
objection. To settle it, one has to say what a limit is, and for that, what a number is: the
rational line has holes. The series' plan, on the ledger.
**Payoff.** Compactness as finiteness in disguise, the Cantor set (uncountable, length zero), and a
first look at a space of functions, where closed and bounded is not enough.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | Fourier's claim; the sawtooth from sines; the century of questions it raised; the series' plan. | Sines stacking into a sawtooth; the timeline strip lights 1807. | Partial sums S_1 … S_50 of the sawtooth's Fourier series. |
| 2 | `Holes` | Ordered fields; Q is one. The set {p ∈ Q : p² < 2} has no largest element (PMA 1.1, with Rudin's map q = p − (p² − 2)/(p + 2)). Sup and inf. The least-upper-bound property is "no holes". | Rationals as pegs on a line; the knife at √2; the map q(p) as arrows hopping toward the gap and never arriving. | The hops from p = 1: 4/3, 1.4, 1.4118, 1.4138, …, each with p² shown, asserted < 2 and increasing. |
| 3 | `Cuts` | Dedekind's construction (PMA appendix to ch. 1): a cut is a downward-closed set of rationals with no largest element; order; the LUB property is a one-line proof (the union of a bounded set of cuts is a cut); addition; the hard part (multiplication of negatives) named and skipped; Q embeds; R is unique up to isomorphism (stated). The Cauchy-sequence construction mentioned as the method that will complete every later space. | The cut as a knife through the pegs; a set of cuts stacking into their union. | The cut of √2 drawn from its rational members to 10⁻⁹. |
| 4 | `Archimedes` | The Archimedean property and the density of Q (PMA 1.20); n-th roots exist (1.21, the sup argument animated); decimal expansions; nested intervals shrink to one point (bisection). | A line of unit steps overtaking any real; the nested intervals of √2's decimal digits. | Bisection for √2 to 40 digits; each interval asserted to contain √2. |
| 5 | `Counting` | Countable and uncountable (PMA 2.1–2.14): N × N and Q are countable (the zigzag); a countable union of countable sets is countable (2.12); the set of 0–1 sequences is not (2.14, Cantor's diagonal). R is uncountable; algebraic numbers are countable, so almost every real is transcendental, though showing one (e, π) took a century. | The zigzag over the grid; the diagonal flipping bits; the "list" that is always missing a row. | A table of 12 listed binary sequences and the diagonal sequence not in it. |
| 6 | `Distance` | R^k and C; the Cauchy–Schwarz inequality (1.35) with its proof and its picture; metric spaces (2.15): a distance is anything with the three properties; a gallery: Euclidean, taxicab, the discrete metric, and the sup distance between two functions, d(f, g) = sup \|f − g\| (the first appearance of a function space; the camera, instrument 3, is previewed). | The gallery of unit balls; the sup distance as the widest gap between two graphs. | Unit balls drawn for each metric; the sup distance of two given functions found by maximization and asserted. |
| 7 | `OpenClosed` | Neighborhoods, limit points, open and closed sets, closure, interior (2.18–2.30); a set is open iff its complement is closed; arbitrary unions of open sets are open, finite intersections (2.24) and the ∩(−1/n, 1/n) = {0} counterexample; relative openness (2.30). In the sup metric a ball is a tube. | Dashed airy open sets vs solid-edged closed sets; the shrinking intersection collapsing to a point; the tube around a graph. | — |
| 8 | `Compact` | Open covers and the finite-subcover definition (2.31) as a game: you cover, I choose finitely many. (0, 1) covered by (1/n, 1) has no finite subcover; compact sets are closed (2.34) and closed subsets of compact sets are compact (2.35); the nested-sets property (2.36). | The cover-game board: colored intervals raining onto [0, 1]; the finite selection highlighted gold; the (1/n, 1) cover visibly failing at the left end. | The finite subcover found by the Lebesgue-number algorithm for a random cover of [0, 1] (asserted to cover). |
| 9 | `HeineBorel` | k-cells are compact (2.40, bisection: a nested sequence of boxes, one of which cannot be finitely covered, shrinking to a point that some open set swallows); Heine–Borel (2.41): in R^k compact ⟺ closed and bounded; Weierstrass (2.42): every bounded infinite set in R^k has a limit point; sequential compactness. | Zoom (instrument 7) into the nested boxes until one open set of the cover contains the box. | The bisection run on a given cover, asserted to terminate. |
| 10 | `Cantor` | Perfect sets; every nonempty perfect set in R^k is uncountable (2.43); the Cantor set (2.44): closed, perfect, totally disconnected, uncountable, total length 0 (foreshadowing measure). Ternary expansions. The Cantor function (devil's staircase) built for later use (Part 3's integrators, Part 5's singular measures, Part 6's non-absolutely-continuous functions). | The infinite zoom with ternary digits ticking; the staircase. | Intervals to depth 30 (lengths asserted (2/3)^n); the staircase sampled to depth 20. |
| 11 | `Connected` | Separated sets and connectedness (2.45); the connected subsets of R are the intervals (2.47); the topologist's sine curve is connected but not path-connected (stated, exhibit; not in Rudin, Munkres §24). | Two sets pulled apart; an interval that cannot be split; the sine curve's accumulation on a segment. | sin(1/x) on (0, 0.05], 10⁵ points. |
| 12 | `FirstFunctionSpace` | A preview: in the sup metric on C[0, 1], the closed unit ball is closed and bounded but the sequence of moving bumps has no convergent subsequence; so Heine–Borel is a theorem about R^k, not about "space". What replaces it (Part 3) and what it will cost (Part 8). | The camera: the bump trail running along the unit sphere with no cluster point; the dictionary card (instrument 4) with "closed and bounded" struck out. | The moving bumps and their pairwise sup distances (asserted = 1). |
| 13 | `Ledger` | Recap on the ledger (row 1: R; complete by construction; Heine–Borel; the Fourier answer: not yet). Preview of Part 2. | The ledger. | — |

(Chapters 2 and 3 are the longest; 11 and 12 are short. Target 13 chapters, ~55 min.)

**Research and script notes for Part 1.** Use Rudin's 1.1 argument exactly (it is a computation,
which the series shows as one). The Dedekind construction is kept to the LUB proof and addition,
with multiplication named as the ugly part (Rudin says so too). The uncountability of R is proved
twice on purpose: by the diagonal (2.14) and, in chapter 10, by the perfect-set theorem (2.43),
to show that the second proof is a compactness proof.

### Part 2. Limits: Sequences, Series, Continuity and the Derivative (PMA 3–5) — ~60 min, 16 chapters

**Hook.** The alternating harmonic series 1 − 1/2 + 1/3 − … = ln 2, rearranged on screen to sum to
π, then to −1, then to run off to +∞ (Riemann's rearrangement theorem, computed by the greedy
algorithm). "Infinite sums are not sums." Which rearrangements are safe is the first of the
series' interchange-of-limits questions.
**Payoff.** Taylor's theorem and the smooth function e^(−1/x²) that its own Taylor series cannot
see; Darboux's theorem; the vector-valued mean value inequality that survives into every later
space.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | Rearranging the alternating harmonic series to any target; the plan for the part. | Blue positive and red negative terms consumed greedily; partial sums crossing the target line with shrinking amplitude. | Greedy rearrangement to π, −1, +∞ (after 10⁶ terms the sum is within 10⁻⁶ of π; asserted). |
| 2 | `Sequences` | Convergence (3.1), uniqueness, boundedness; subsequences and subsequential limits (3.6); the limit laws (3.3) with the ε/2 trick shown once on the game board (instrument 1). | The game board for a sequence: the yellow band and the teal N. | For 1/n and (−1)^n/n at ε = 0.01: N = 101, asserted. |
| 3 | `Cauchy` | Cauchy sequences (3.8); diameters of tails shrink to 0 (3.9–3.10); in R^k every Cauchy sequence converges (3.11, via Heine–Borel and 3.10); complete metric spaces; compact metric spaces are complete; monotone bounded sequences converge (3.14). The picture of completeness: the tails close in on a point of the space, and in Q they close in on a hole. | The tail set E_N as a shrinking interval; the same sequence in Q closing in on nothing. | Diameters of the tails of the √2 bisection sequence, asserted to halve. |
| 4 | `LimSup` | Upper and lower limits (3.16–3.17) as the highest and lowest cluster values; the special sequences (3.20): n^(1/n) → 1, p^n → 0, (1 + 1/n)^n. | The high- and low-water marks of the tail. | n^(1/n) to n = 10⁶. |
| 5 | `Series` | Series as sequences of partial sums; the Cauchy criterion (3.22); terms → 0 is necessary not sufficient (the harmonic series diverges); comparison (3.25); geometric series; Cauchy's condensation test (3.27) and Σ 1/n^p (3.28). | Terms as bars; condensation as regrouping the bars into blocks of 2^k. | Partial sums of Σ 1/n^p for p = 1, 1.5, 2 to 10⁶ terms. |
| 6 | `NumberE` | e = Σ 1/n! = lim (1 + 1/n)^n (3.30–3.31); e is irrational (3.32): the tail bound 0 < q!(e − s_q) < 1/q is a computation the screen performs. | The tail squeezed between 0 and 1/q. | The tail for q = 5…12, asserted in (0, 1/q). |
| 7 | `Tests` | Root and ratio tests (3.33–3.34) as comparisons with a geometric envelope; the ratio test is weaker (3.35 example); power series and the radius of convergence (3.39), drawn as a disk in C: the series of 1/(1 + x²) stops converging at \|x\| = 1 because of the poles at ±i, invisible from the real line, the first place the series needs C (Part 7). | Terms falling under an exponential envelope; the disk of convergence. | Σ z^n/n at \|z\| = 0.9, 1 (z = −1 converges; z = 1 diverges), 1.1. |
| 8 | `Abel` | Summation by parts (3.41) with its picture (the discrete integration by parts); the alternating series test (3.43) and Dirichlet's test (3.42); absolute convergence (3.45); the Cauchy product (3.48–3.50, Mertens' theorem) as the grid a_i b_j summed by anti-diagonals rather than by rows (the order of a double sum matters: a preview of Fubini, Part 5), and the example (3.49) where it fails without absolute convergence. | The rectangle picture of summation by parts. | The Cauchy product of Σ (−1)^n/√(n+1) with itself, terms asserted not → 0. |
| 9 | `Rearrangement` | Riemann's theorem (3.54), proved by the hook's algorithm: the positive and negative parts each diverge, so the greedy walk reaches any target and overshoots by at most one term; absolutely convergent series are safe (3.55). The Fourier thread: the sawtooth's series is conditionally convergent. | The hook's animation, now with the proof's quantities (the overshoot bounded by the last term used) on screen. | The overshoot sequence, asserted ≤ the last term. |
| 10 | `Continuity` | Limits of functions (4.1–4.4); continuity (4.5) on the game board; continuity ⟺ preimages of open sets are open (4.8): the definition that will survive into every later space, and the reason topology was invented; compositions; the ε/2 and ε/3 proofs shown once. | The game board; a blue open set in the codomain pulled back to an open set in the domain. | For f(x) = x² at x = 3, ε = 0.1: the largest δ (0.0166), found by bisection and asserted. |
| 11 | `Compactness` | Continuous images of compact sets are compact (4.14); extreme values (4.16); a continuous bijection of a compact space has a continuous inverse (4.17) and the counterexample on [0, 2π) → circle (4.21). Uniform continuity (4.18–4.19): the same game, but δ is chosen before x; the proof via the Lebesgue number / finite subcover. 1/x on (0, 1) is the game the responder loses (4.20); √x on [0, 1] is uniformly continuous but not Lipschitz, so the box is not about slopes. | The window of fixed size sliding along the whole graph (uniform) vs the window that must shrink near 0 (1/x). | The largest δ at each x for 1/x at ε = 0.1, shown → 0. |
| 12 | `Connectedness` | Continuous images of connected sets are connected (4.22); the intermediate value theorem (4.23), with bisection as its algorithm, run once over Q on x² − 2 where the nested intervals close on nothing (the theorem needs completeness); discontinuities of the first and second kind (4.26); monotone functions have at most countably many discontinuities (4.30: each jump owns a rational); the museum (Example 4.27 and Exercise 4.18): Dirichlet's function (nowhere continuous), x·1_Q (continuous only at 0), Thomae's function (continuous exactly at the irrationals). | Bisection homing in on a root; each jump of a staircase tagged with its own rational; the popcorn function at three zooms. | Thomae's function at 2,000 rationals of denominator ≤ 60. |
| 13 | `Derivative` | The derivative (5.1) as the best linear approximation: zoom until straight; Thurston's seven conceptions of the derivative (infinitesimal, symbolic, logical, geometric, rate, approximation, microscopic) as the chapter's transitions; differentiable ⇒ continuous (5.2); the rules (5.3); the chain rule proved with Rudin's u(t) trick (5.5); the museum: x² sin(1/x) (differentiable everywhere, derivative discontinuous at 0; 5.6). | The zoom to straightness; the chain rule as two zooms composed. | Difference quotients of x² sin(1/x) at 0, asserted → 0, and f′ oscillating. |
| 14 | `MeanValue` | Local extrema have f′ = 0 (5.8); the generalized mean value theorem (5.9) and the MVT (5.10) via Rolle via the extreme value theorem (compactness pays); monotonicity from the sign of f′ (5.11); Darboux: derivatives have the intermediate value property even when discontinuous (5.12); L'Hôpital (5.13), derived from 5.9 with its hypotheses highlighted. | The chord subtracted by a vertical shear (not a rotation) so that Rolle applies, then sheared back: the tangent parallel to the chord; Darboux on the museum function. | f′ of x² sin(1/x) taking every value in [−1, 1] near 0 (asserted on a grid). |
| 15 | `Taylor` | Higher derivatives; Taylor's theorem with Lagrange's remainder (5.15) proved by applying the MVT to the right auxiliary function; polynomial fits of e^x, sin x, log(1 + x) (radius 1: the fits fail beyond it); the museum (Exercise 5.6): e^(−1/x²) is C^∞ with every Taylor coefficient 0, so its series converges everywhere to the wrong function. Analytic vs smooth; a promise for Part 7 (in C this cannot happen) and Part 9 (Paley–Wiener sees it). | Polynomials of growing degree hugging the graph; the flat function with its "invisible" series. | Remainders asserted ≤ the Lagrange bound on a grid; the first 10 derivatives of e^(−1/x²) at 0 computed symbolically (sympy), asserted 0. |
| 16 | `Vector` | Vector-valued functions (5.16–5.19): the MVT fails (e^(it) on [0, 2π] has f(2π) − f(0) = 0 but \|f′\| = 1), but the inequality \|f(b) − f(a)\| ≤ (b − a) sup \|f′\| holds (5.19), and this is the form that generalizes to every later space. Ledger row 2. | The circle's chord of length 0 vs its speed 1. | — |

### Part 3. Integration and the First Function Space: Uniform Convergence, Arzelà–Ascoli and Weierstrass (PMA 6–8) — ~60 min, 17 chapters

**Hook.** Rudin's "main problem" (7.1): when is lim_m lim_n = lim_n lim_m? The double sequence
s_mn = m/(m + n) (7.2) as a grid whose row limits and column limits disagree. Three concrete
failures on the convergence dashboard (instrument 2, introduced here): continuity lost (x^n),
the integral lost (n²x(1 − x²)^n, Example 7.6), the derivative lost (sin(nx)/√n, Example 7.5). Then the Fourier
question stated properly: a Fourier series is a limit; integrating it term by term is an
interchange.
**Payoff.** C(X) is complete and what compactness costs there (Arzelà–Ascoli); a continuous function
with no derivative anywhere; every continuous function is a limit of polynomials (Weierstrass) and
of trigonometric polynomials; Parseval for Riemann-integrable functions and Gibbs' 8.9%.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | The main problem; the double-sequence grid; three failures on the dashboard; the plan. | The grid with row/column limits in two colors; the dashboard's five lenses. | s_mn grid; x^n, the bump, sin(nx)/√n under every lens (sup error, ∫ error, probe at x). |
| 2 | `UpperLower` | Partitions, U(P, f, α) and L(P, f, α) (6.1–6.2); refinements only help (6.4); the integrability criterion U − L < ε (6.6); the Riemann integral as the case α(x) = x. | Red upper and green lower rectangles squeezing the area as the partition refines. | U − L for x² on [0, 1] at n = 2…2¹⁴, asserted ~ 1/n. |
| 3 | `WhoIsIntegrable` | Continuous ⇒ integrable (6.8: uniform continuity pays); monotone ⇒ integrable (6.9); finitely many discontinuities (6.10); compositions (6.11); the oscillation ω_f(x) colored along the axis so that U − L is visibly ∫ ω, previewing Lebesgue's criterion (Part 5); the museum (Exercise 6.4): Dirichlet's function has U = 1 and L = 0 for every partition; Thomae's function is integrable with integral 0 (the first hint of "small sets don't matter"). | The game board's uniform δ turning into a partition mesh; the Dirichlet function's rectangles never closing. | U and L for Thomae's function at mesh 1/2⁸ … 1/2¹⁴, U asserted → 0. |
| 4 | `Stieltjes` | Why α: a jump in α turns the integral into a sum (6.15, the unit step); α = the Cantor function (Exercise 6.6) gives an integral that is neither a sum nor a Riemann integral (a preview of singular measures, Part 5); ∫ f dα = ∫ f α′ dx when α is smooth (6.17); the stretched-ruler picture. | The x-axis drawn stretched by α: dα is the local density of tick marks; a jump is a concentrated tick. | ∫ x d(Cantor function) computed from the depth-20 staircase (= 1/2, asserted). |
| 5 | `FTC` | Properties (6.12–6.13); change of variables (6.19); F(x) = ∫_a^x f is continuous, and differentiable where f is (6.20); the fundamental theorem (6.21); integration by parts (6.22); rectifiable curves and length = ∫\|γ′\| (6.27); the museum: the Koch curve has no length. | The running integral's slope read off the integrand; the Koch zoom. | Polygonal lengths of the Koch curve at depth 1…12 (asserted (4/3)^n). |
| 6 | `Uniform` | Uniform convergence (7.7) on the game board (N before x); the Cauchy criterion (7.8); the yellow tube; sup\|f_n − f\| → 0 (7.9); the Weierstrass M-test (7.10) as stacked tubes. | The tube; tubes of width M_n stacking into a convergent total. | Σ sin(nx)/n² partial sums with the stacked M_n bound. |
| 7 | `Continuity` | Interchanging limits under uniform convergence (7.11); the uniform limit of continuous functions is continuous (7.12), with the 3ε proof animated as three hops; Dini's theorem (7.13: monotone + continuous limit + compact ⇒ uniform); C(X) with the sup norm is a complete metric space (7.14–7.15): the first Banach space, not yet named. The museum: Lebesgue's space-filling curve (Exercise 7.14), a uniform limit of continuous curves, hence continuous, that covers the whole square and maps the Cantor set onto it. | Three hops: f(x) → f_n(x) → f_n(y) → f(y); the camera (instrument 3) showing a Cauchy trail converging in C[0, 1]. | A Cauchy sequence of polynomials in C[0, 1] and its limit; the sup distances asserted. |
| 8 | `IntegralsDerivatives` | Uniform convergence lets the integral pass through the limit (7.16); for derivatives one needs the derivatives to converge uniformly (7.17), and sin(nx)/√n shows why; the dashboard records which lens each theorem needs. | The dashboard with the L¹ lens lit by uniform convergence. | ∫ f_n − ∫ f for a uniformly convergent sequence, asserted ≤ (b − a) sup\|f_n − f\|. |
| 9 | `Weierstrass` | A continuous, nowhere-differentiable function (7.18): Rudin's Σ (3/4)^n φ(4^n x) with φ the distance to the nearest integer; the proof's idea: at scale 4^(−m) one term dominates the difference quotient and the rest cancel in pairs; zoom. Cameo: the Brownian path from the stochastic video, "the same phenomenon, met by chance". | The zoom (instrument 7) adding partial sums as the scale demands; the dominating term highlighted. | Partial sums at 20 zoom levels; difference quotients at h = ±4^(−m) asserted ≥ (3^m + 1)/2, growing without bound. |
| 10 | `Equicontinuity` | The sup-norm unit ball is not compact (sin(nx) has no pointwise convergent subsequence, Example 7.20; the bumps x²/(x² + (1 − nx)²) of Example 7.21 converge pointwise but not uniformly); pointwise bounded, uniformly bounded (7.19); equicontinuity (7.22): the game board played against a whole family (δ before x and before f); a uniformly convergent sequence on a compact set is equicontinuous (7.24). | The game board with a fan of graphs sharing one box size. | The largest common δ for the family {sin(kx)/k} (asserted ≈ ε) vs for {sin(kx)} (asserted → 0). |
| 11 | `ArzelaAscoli` | Pointwise convergence on a countable dense set by the diagonal argument (7.23: the grid of subsequence indices with the diagonal); equicontinuity upgrades it to uniform convergence on the compact set (7.25); the dictionary card: Bolzano–Weierstrass ↔ Arzelà–Ascoli. Payoff named for Part 4 (Peano's theorem) and Part 7 (Montel, the Riemann mapping theorem). | The infinite index grid with the diagonal; the finite net of points at which agreement spreads to the whole interval. | A uniformly bounded equicontinuous family (random Lipschitz-1 functions) and the extracted uniformly convergent subsequence, sup errors asserted → 0. |
| 12 | `Approximation` | The Weierstrass approximation theorem (7.26) with Rudin's proof: the Landau kernel Q_n = c_n(1 − x²)^n, c_n < √n, convolution P_n = ∫ f(x + t) Q_n(t) dt is a polynomial, and the kernel concentrates. Convolution as blurring, then the blur sharpening. Bernstein's probabilistic polynomials shown as the other route. | The kernel narrowing; the sliding weighted average; the error curve shrinking. | P_n for f = \|x\| and for a piecewise-linear f at n = 10…10⁴; sup errors asserted decreasing; c_n asserted < √n. |
| 13 | `StoneWeierstrass` | Algebras, uniform closure, separating points, vanishing nowhere (7.28–7.31); the proof's four steps on a proof map (instrument 6): \|f\| is in the closure (via Weierstrass on \|t\|), hence max and min; two-point interpolation; the lattice argument that builds the approximant from "caps"; the complex version needs self-adjointness (7.33) and the disk algebra shows why. | The lattice construction: a cap over each point, the max of a few caps, the min over a finite cover. | The construction run on f(x) = e^x with the polynomial algebra on [0, 1], sup error asserted < ε. |
| 14 | `PowerSeries` | Power series are C^∞ inside the radius, differentiable term by term (8.1, uniform convergence on compact subsets); Abel's theorem (8.2) and the Fourier thread (Σ (−1)^(n+1)/n = ln 2 by Abel); exp, log and the trigonometric functions from their series (8.6–8.7), π defined as twice the first zero of cos; the algebraic completeness of C (8.8) stated and previewed for Part 7. | The series' disk; the trigonometric functions appearing from their series as degree grows. | cos's first zero by bisection on the series (asserted = π/2 to 12 digits). |
| 15 | `FourierSeries` | Trigonometric polynomials; orthogonality (8.9–8.10); the Fourier coefficients give the best mean-square approximation (8.11: the projection argument, the first appearance of the Hilbert idea); Bessel's inequality (8.12); the Dirichlet kernel and the partial sums as a convolution (8.13); Dini's localization test (8.14): where f is Lipschitz, s_N(x) → f(x). | The error ∫\|f − t\|² as a distance minimized by orthogonal projection (lilac); the Dirichlet kernel's growing side lobes. | The sawtooth's coefficients; D_N for N = 5…500; the best-approximation inequality asserted on random trigonometric polynomials. |
| 16 | `Parseval` | Trigonometric polynomials are dense in C(T) (8.15, from Stone–Weierstrass); Parseval (8.16): for Riemann-integrable f, ∫\|f − s_N\|² → 0 and Σ\|c_n\|² = (1/2π)∫\|f\|²; the Fourier answer so far: convergence in mean square, pointwise where Lipschitz, and Gibbs' phenomenon at the jump (the overshoot → 8.95%, computed). Payoff: ζ(2) = π²/6 from Parseval applied to f(x) = x (Exercise 8.13), the series' nod to 3Blue1Brown's Basel video, by a different proof. The gamma function (8.17–8.22) is cut to one card (Bohr–Mollerup, Stirling). | The dashboard: the L² lens lights, the uniform lens does not; the Gibbs overshoot not shrinking. | Parseval's two sides for the sawtooth at N = 10⁴ (asserted equal to 10⁻⁴); the overshoot at N = 10³ asserted → 0.0895. |
| 17 | `Ledger` | Row 3: C(X), complete (7.15), compact iff closed + bounded + equicontinuous, the interchange made legal: lim ∫ = ∫ lim under uniform convergence; the Fourier answer. Preview: to pass limits under integrals without uniformity, the integral must change (Part 5); first, calculus in many variables (Part 4). | The ledger. | — |

### Part 4. Calculus in Many Dimensions: Linear Maps, Contractions and the Inverse Function Theorem (PMA 9, tour of 10) — ~45 min, 11 chapters

**Hook.** Newton's method on a two-variable system, converging in four steps; a contraction
shrinking the plane onto one point. "Every equation you can solve, you solve by a contraction."
**Payoff.** The inverse and implicit function theorems from one contraction; the existence and
uniqueness theorem for ODEs (Picard) as a contraction in C[a, b], the function space of Part 3
earning its keep.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | Newton in 2D (PMA Exercise 5.25 in one variable); the contraction picture; the plan. | The plane shrinking under iteration; Newton's steps on a contour map. | Newton on (x² + y² − 4, xy − 1), residuals asserted to square each step. |
| 2 | `LinearMaps` | Linear transformations, the operator norm ‖A‖ = sup\|Ax\|/\|x\| (9.6–9.7); the image of the unit ball is an ellipse (or ellipsoid); the set Ω of invertible maps is open and inversion is continuous (9.8), via the Neumann series \|A^(−1)\|·‖B − A‖ < 1 (the first appearance of the series that runs the spectral theory of Part 10). | The unit circle mapped to an ellipse; an invertible matrix perturbed inside its "safe ball". | ‖A‖ as the largest singular value; the Neumann series for (A + B)^(−1) summed and asserted. |
| 3 | `Derivative` | The derivative as a linear map (9.11): f(x + h) = f(x) + Ah + o(h), unique (9.12); zoom into a surface until it is a plane; the chain rule as a composition of linear maps (9.15); partial derivatives and the Jacobian (9.16–9.17); the gradient and directional derivatives (9.18). | The zoom on a surface; the tangent plane; the dictionary card: "the derivative is a number" ↔ "the derivative is a linear map". | The tangent plane's residual \|f(x + h) − f(x) − Ah\|/\|h\| asserted → 0 on a grid of h. |
| 4 | `C1` | The mean value inequality (9.19); continuous partials ⟺ continuously differentiable (9.21); the museum: xy/(x² + y²) (partials everywhere, not even continuous at 0) and a function with partials but not differentiable. | The museum function's surface with its crease at the origin. | The surface sampled; the directional derivatives at 0 asserted to disagree with the gradient. |
| 5 | `Contraction` | The contraction principle (9.23): the proof animated as a sequence of points with geometrically shrinking steps, Cauchy, convergent because the space is complete, the limit fixed by continuity; uniqueness. Newton's method as a contraction near a simple root. | The shrinking steps; the error bar ≤ c^n/(1 − c) · \|x_1 − x_0\|. | The iteration for cos x = x and for Newton; errors asserted ≤ the bound. |
| 6 | `Picard` | Picard–Lindelöf (not in PMA's text; the standard contraction argument, e.g. Pugh ch. 4): y′ = f(x, y), Lipschitz in y, is a contraction T(y)(x) = y_0 + ∫ f(t, y(t)) dt on C[a, a + h] for small h; the iterates computed; uniqueness and the interval of existence; the function space of Part 3 pays off. | The camera: the Picard iterates as a trail in C[a, b] converging to the solution's dot; on the left, the graphs. | Picard iterates for y′ = y and y′ = x + sin y; sup errors asserted to shrink geometrically. |
| 7 | `InverseFunction` | The inverse function theorem (9.24): φ(x) = x + A^(−1)(y − f(x)) is a contraction on a small ball, so f(x) = y has one solution near a; the inverse is C¹; the proof map. Open mapping consequence (9.25). | A curved grid under f, with a small square mapped bijectively onto a neighborhood; the contraction φ run for one y. | The local inverse found by iterating φ for f(x, y) = (e^x cos y, e^x sin y); residuals asserted → 0. |
| 8 | `ImplicitFunction` | The implicit function theorem (9.28), derived from 9.24 applied to (x, y) ↦ (f(x, y), y); the surface f = 0 sliced; the local graph; the derivative of the implicit function; the rank theorem (9.32) in one card ("a C¹ map of constant rank is locally a projection"). | The zero set of f as a surface sliced into a graph; the slice failing where the y-derivative is singular (the fold). | The implicit curve of x³ + y³ − 3xy = 0 traced by continuation, with the fold points where f_y = 0 marked and asserted. |
| 9 | `HigherOrder` | Mixed partials commute when continuous (9.41) and the museum function (9.40) where they do not; differentiation under the integral sign (9.42), stated as an interchange of limits and tied to the thesis. | The two orders of differencing on a small square; the derivative passing through the integral on the dashboard. | f_xy(0, 0) = −1 ≠ f_yx(0, 0) = 1 for the museum function, computed by sympy and asserted. |
| 10 | `FormsTour` | *Tour, no proof* (labeled): the change-of-variables formula (10.9) with the Jacobian as the area factor; partitions of unity (10.8) as blending bumps; what a k-form is and why forms are what you integrate; Stokes' theorem (10.33) stated, with Green, Gauss and the classical Stokes as its faces; closed vs exact forms and the hole in the plane (10.35–10.39). | A grid deformed by a map with little area-parallelograms; bumps blending; the boundary of a surface. | Area factors on a grid asserted equal to \|det J\|. |
| 11 | `Ledger` | Row 4: R^n and C[a, b] again; the contraction principle; the interchange made legal: differentiation under the integral; the Fourier answer unchanged. Preview: Season 2. | The ledger. | — |

### Part 5. Measure: The Lebesgue Integral and Why Limits Pass Under It (PMA 11; RCA 1–2, 8) — ~65 min, 14 chapters

**Hook.** The Dirichlet function is a double limit of continuous functions, lim_m lim_n
cos(m! π x)^(2n), and Riemann cannot integrate it. Three ways mass escapes a sequence of functions
(the spike, the runaway, the spreading) on the dashboard, and the one thing that stops it: a lid.
Lebesgue's 1926 image of sorting coins by value instead of by order, shown and then corrected: the
real change is not the direction of the slicing but which sets are allowed to have a length.
**Payoff.** The dominated convergence theorem; the Riesz representation theorem (every positive
functional on C_c is an integral); Lusin ("measurable is nearly continuous"); Lebesgue's criterion
for Riemann integrability; Fubini and its counterexample; the Fourier thread: convolution, and
∫ of a Fourier series term by term, legalized.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | The Dirichlet double limit; escaping mass; the lid; Lebesgue's coins and the honest correction; the plan. | cos(m!πx)^(2n) sharpening into spikes at rationals; the dashboard's three escapes; a lid g stopping them. | cos(m!πx)^(2n) on a grid for m = 1…5, n = 1…50; ∫ of the three escapes asserted = 1 while the limit is 0. |
| 2 | `Length` | Outer measure m*(E) = inf Σ lengths of countable interval covers; monotone, countably subadditive; the Cantor set has m* = 0 and so does Q; a fat Cantor set has positive measure yet contains no interval (so "small" and "measure zero" are different ideas); m* of an interval is its length (the compactness step: a finite subcover of a closed interval, Heine–Borel pays). | Clouds of amber intervals shrinking onto a set; the fat Cantor set's zoom with its leftover lengths. | Outer-measure covers of the Cantor set at depth n (total (2/3)^n); the fat Cantor set with removed lengths 1/4^n, measure asserted 1/2. |
| 3 | `Vitali` | Why not every set: countable additivity plus translation invariance is impossible for all sets. The Vitali set via the circle: rotate by an irrational angle, one orbit per class (the axiom of choice, named), countably many disjoint rotated copies fill the circle, so the set has neither measure 0 nor positive measure. Labeled `schematic`. This is RCA 2.22 (if every subset of A is measurable then m(A) = 0; its proof is the construction). Banach–Tarski named as the three-dimensional sequel. | The circle with one orbit of the irrational rotation drawn (computed, dense), the chosen representatives (schematic), and copies rotating to tile the circle. | 2,000 points of the orbit of rotation by 1 radian, asserted to come within 10⁻³ of every point. |
| 4 | `SigmaAlgebras` | σ-algebras, measurable spaces, Borel sets (RCA 1.3–1.11); measurable functions as "preimages of open sets are measurable", the same template as continuity (1.12; the dictionary card); continuous ∘ measurable is measurable (1.7); sup, inf, lim sup of measurable functions are measurable (1.14): limits are free. Simple functions and the approximation theorem (1.17): the dyadic slicing of the range, the honest version of Lebesgue's picture. | A blue open set pulled back to a measurable set; dyadic horizontal bands of the range each becoming a measurable level set; s_n climbing to f. | s_n for f(x) = x² + sin(5x) at n = 1…8; sup\|s_n − f\| asserted ≤ 2^(−n) where f < n. |
| 5 | `Measures` | Measures and their properties (1.18–1.19): continuity from below and above (with the counterexample for "above" without finiteness: E_n = (n, ∞)); counting measure, Dirac measure, the Lebesgue measure to come; "almost everywhere" (1.35–1.36). | Nested sets growing to a union with their measures converging. | — |
| 6 | `Integral` | ∫ s dμ for simple s; ∫ f dμ = sup over simple s ≤ f (1.23); linearity on simple functions (1.25); the monotone convergence theorem (1.26) with its full proof: the trick E_n = {f_n ≥ c·s} swallows X, and continuity from below finishes it. Σ ∫ = ∫ Σ (1.27). | The sets E_n growing across the x-axis under a fixed simple s, the integral over E_n climbing. | MCT on f_n = min(f, n)·1_[−n,n] for f = 1/√x; integrals asserted increasing to 2. |
| 7 | `Fatou` | Fatou's lemma (1.28), proved from MCT applied to inf_{k≥n} f_k; strict inequality on the escapes; the three escapes revisited with the dashboard. | The inf envelopes under the spikes staying flat while the spikes keep their area. | ∫ lim inf = 0 vs lim inf ∫ = 1, asserted. |
| 8 | `Dominated` | L¹(μ) (1.32); linearity (1.32); the dominated convergence theorem (1.34): the proof applies Fatou to 2g − \|f_n − f\| ≥ 0; the lid g is the whole story; the typewriter sequence (converges in L¹ and in measure, nowhere pointwise) and the dashboard's verdict; the almost-everywhere versions (1.38); Egorov's theorem (Exercise 3.16) on the dashboard: a.e. convergence is uniform off a set of measure ε when the measure is finite, and 1_[n, ∞) shows why finiteness is needed. | The lid g over the whole sequence; the typewriter sweeping. | DCT on f_n = n sin(x/n)·1_[0,1]/x → 1 with lid 1; the typewriter's ∫\|f_n\| asserted → 0 while lim sup f_n = 1 everywhere. |
| 9 | `RieszRepresentation` | Urysohn's lemma for locally compact Hausdorff spaces (2.12) and partitions of unity (2.13); the Riesz representation theorem (2.14): a positive linear functional Λ on C_c(X) is integration against a unique regular Borel measure; the proof map (define μ(V) = sup{Λf : f ≺ V}, extend to an outer measure, show the class of outer-regular sets with finite measure is a σ-algebra on which μ is countably additive, then Λf = ∫ f dμ by slicing f into thin layers). The honest slicing picture appears once more, in Rudin's own proof. | The machine: a functional goes in, a measure comes out; the proof map with its five boxes; f sliced into layers of height ε. | The construction run numerically for Λ = the Riemann integral on [0, 1]: μ of random open sets asserted equal to their length within 10⁻⁶. |
| 10 | `Lebesgue` | Lebesgue measure as the Riesz measure of the Riemann integral (2.19–2.20): translation invariance, m(box) = volume, regularity; the comparison with Riemann (PMA 11.33 / the criterion): f is Riemann-integrable iff bounded and continuous a.e., and then the integrals agree; Thomae and Dirichlet revisited (the first is Riemann-integrable, both are Lebesgue-integrable). | The museum cards updated with a "Lebesgue: yes" stamp. | Lebesgue measure of the discontinuity set of Thomae's function (Q: measure 0) asserted; Riemann sums of Thomae → 0. |
| 11 | `NearlyContinuous` | Lusin's theorem (2.24): a measurable function agrees with a continuous one outside a set of measure < ε; the Vitali–Carathéodory theorem (2.25) in one card; C_c is dense in L¹ (previewed for Part 6, 3.14). Littlewood's three principles stated. | The measurable function and its continuous repair, the exceptional set hatched. | Lusin's repair for 1_(Cantor set) ... for a random step function with 100 steps: the continuous f and the measure of {f ≠ g} asserted < ε. |
| 12 | `Products` | Product σ-algebras and product measures (8.1–8.7); sections are measurable; the Fubini–Tonelli theorem (8.8) with its proof map (monotone class, then simple functions, then MCT); the counterexample where the iterated integrals differ (8.9(c)): f(x, y) = (x² − y²)/(x² + y²)² on the unit square, iterated integrals ±π/4; completion of product measures (8.11). | The function's heat map; the two integration orders sweeping in different directions and landing on different numbers. | The two iterated integrals computed by adaptive quadrature, asserted +π/4 and −π/4. |
| 13 | `Convolution` | Convolution f ∗ g on R (8.14): defined a.e., ‖f ∗ g‖₁ ≤ ‖f‖₁‖g‖₁ by Fubini; the Fourier thread: the partial sums are D_N ∗ f, and Fubini is what lets a Fourier series be integrated term by term; distribution functions and the layer-cake formula (8.16) (the honest slicing, now as a theorem). | Convolution as a sliding weighted average (from Part 3's Landau kernel, now in L¹); the layer cake. | ‖f ∗ g‖₁ for two random L¹ functions asserted ≤ the product; the layer-cake identity asserted. |
| 14 | `Ledger` | Row 5: (X, 𝔐, μ); the new integral; the interchange made legal: lim ∫ = ∫ lim under a lid; the Fourier answer: term-by-term integration is legal. Preview: distances between functions (Part 6). | The ledger. | — |

(Target 14 chapters, ~65 min: chapters 6, 8, 9 and 12 are long.)

**Script notes for Part 5.** The order follows Papa Rudin 1 → 2 → 8, with Baby Rudin 11's
Riemann-vs-Lebesgue comparison folded into chapter 10. Egorov's theorem is an exercise in Rudin
(RCA Exercise 3.16); it is shown on the dashboard in chapter 8 as "a.e. convergence is uniform off a small
set", because it is the honest reason Littlewood's principles hold. The Vitali set is the only
labeled schematic in the part.

### Part 6. L^p, Hilbert Space and the Geometry of Functions (RCA 3–4, 6–7) — ~60 min, 17 chapters

**Hook.** The unit ball {\|x\|^p + \|y\|^p ≤ 1} morphing from the diamond (p = 1) through the circle
to the square (p = ∞), and the question: which distance between two functions is the right one?
Then the scandal: C[0, 1] with the L¹ distance is not complete (a sequence of continuous ramps
converging to a step), and Lebesgue's integral is exactly what completes it.
**Payoff.** Riesz–Fischer; the projection theorem and the Riesz representation theorem in Hilbert
space; Fourier series converge in L² for every square-integrable f, and Fejér's means converge
uniformly for continuous f; the Radon–Nikodym theorem by von Neumann's Hilbert-space trick; the
dual of L^p; the Lebesgue differentiation theorem and the fundamental theorem of calculus for
absolutely continuous functions (and the Cantor function as the function for which it fails).

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | The p-ball morph; the incomplete C[0, 1]; the plan. | The morphing ball; the camera: the ramps' trail leaving C[0, 1]. | ‖ramp_n − step‖₁ asserted → 0 while no continuous limit exists (sup distance to any continuous g ≥ 1/2). |
| 2 | `Convexity` | Convex functions (3.1); Jensen's inequality (3.3) with the picture (the chord above the graph; the measure as weights); the AM–GM inequality as a corollary. | The chord and the graph; weighted points sliding along the chord. | Jensen asserted on 10⁴ random weightings. |
| 3 | `Holder` | Conjugate exponents; Young's inequality ab ≤ a^p/p + b^q/q as two areas under y = x^(p−1) (the picture is the proof); Hölder (3.5), Minkowski (3.5), Cauchy–Schwarz as p = 2; equality cases. | The two areas; Minkowski as the triangle inequality for the p-ball (its convexity). | Young's two areas computed and asserted ≥ ab; Hölder checked on random vectors. |
| 4 | `Lp` | L^p(μ) (3.6–3.8), ‖·‖_p, L^∞ and the essential sup; L^p is a normed space; functions equal a.e. are identified (the quotient, said once and honestly). | The ball in L^p as a region on the camera's map; a function and its a.e.-equal twin as one dot. | — |
| 5 | `RieszFischer` | L^p is complete (3.11): the proof extracts a subsequence with Σ ‖f_{k+1} − f_k‖_p < ∞, stacks it into a convergent series by MCT, and DCT finishes; the hook's ramps converge in L¹ to the step. C_c is dense in L^p for p < ∞ (3.14), simple functions too (3.13); L^∞ is the exception and why. | The stacked increments; the camera: the trail now has a limit dot, in the bigger space. | The subsequence stacking for the ramps; ‖f_n − f‖₁ asserted → 0. |
| 6 | `Hilbert` | Inner products (4.1); Cauchy–Schwarz again, from the inner product (4.2); the norm; Hilbert spaces; L² and ℓ²; the parallelogram law (ch. 4) as the test for "is this norm from an inner product?" (it fails for p ≠ 2: computed). | The parallelogram; the dictionary card "R^n ↔ H" opened. | ‖x + y‖² + ‖x − y‖² vs 2‖x‖² + 2‖y‖² on L^p for p = 1, 2, 3, asserted equal only at p = 2. |
| 7 | `Projection` | Closed convex sets have a unique nearest point (4.10, via the parallelogram law: the minimizing sequence is Cauchy, completeness pays); orthogonal complements and H = M ⊕ M^⊥ (4.11); the dictionary: projection onto a line ↔ onto a closed subspace. | The nearest point; the minimizing sequence closing in; the perpendicular. | Projection of a function onto span{1, x, x²} in L²[0, 1] vs the normal-equations solution, asserted equal. |
| 8 | `RieszHilbert` | Continuous linear functionals (ch. 4); the Riesz representation theorem for Hilbert space (4.12): every bounded functional is ⟨·, y⟩, found as the normal to its kernel (a hyperplane); the covector stacks (relativity's picture) meet Hilbert space. | The kernel hyperplane and its normal; the stacks of level sets. | The representing y for the functional f ↦ ∫ f·w, asserted = w. |
| 9 | `Orthonormal` | Orthonormal sets (4.13–4.15); Bessel's inequality (4.14); the Riesz–Fischer theorem for coefficients (4.17–4.18): Σ\|c_n\|² < ∞ ⟺ the series converges in H; maximal orthonormal sets and Parseval (4.18); every Hilbert space has a maximal orthonormal set (4.22, by Hausdorff maximality) and separable ones have countable bases (Gram–Schmidt); the dictionary: Pythagoras ↔ Parseval. | Bessel as Pythagoras with a leftover; Gram–Schmidt as successive perpendiculars. | Gram–Schmidt on 1, x, x², … in L²[−1, 1] producing the Legendre polynomials (asserted to 10⁻¹²). |
| 10 | `FourierL2` | The trigonometric system is complete in L²(T) (4.25–4.26: trigonometric polynomials are dense in C(T) by convolution with the positive kernel c_k(1 + cos t)^k, the Landau kernel's cousin, and C(T) is dense in L²); for every f ∈ L², s_N → f in L² and Parseval holds; the Fourier thread's answer in L²; Fejér's theorem (RCA ex. / stated with the kernel): σ_N → f uniformly for continuous f; Gibbs disappears under Fejér. The dashboard: s_N lights the L² lens, σ_N lights the uniform one. | The Fejér kernel vs the Dirichlet kernel (positive, no side lobes); the sawtooth's σ_N without overshoot. | ‖f − s_N‖₂ and ‖f − σ_N‖_∞ for the sawtooth and for a continuous f, asserted → 0; the Fejér kernel's integral asserted 1. |
| 11 | `ComplexMeasures` | Complex measures and total variation (6.1–6.4): \|μ\| is a measure and \|μ\|(X) < ∞; absolute continuity and mutual singularity (6.7–6.8); the Cantor measure (the derivative of the Cantor function) as a measure singular to Lebesgue measure with no atoms. | The variation as the length of a polygonal path of partial sums; the Cantor measure's mass on a set of length 0. | \|μ\| for a signed measure with density sin(5x), asserted = ∫\|sin 5x\|. |
| 12 | `RadonNikodym` | The Lebesgue–Radon–Nikodym theorem (6.10) by von Neumann's proof: the functional f ↦ ∫ f dλ is bounded on L²(φ), φ = λ + μ, so by Riesz it is ⟨f, g⟩; the set where g = 1 carries the singular part; the rest gives the density h = g/(1 − g). A proof map; the density as a local ratio dλ/dμ. Hahn and Jordan decompositions (6.14); the polar representation dμ = h d\|μ\| (6.12). | The ratio of two measures on shrinking boxes becoming the density; the proof map's three boxes. | dλ/dμ recovered numerically for λ = Lebesgue restricted to a density, asserted. |
| 13 | `DualLp` | The dual of L^p is L^q for 1 ≤ p < ∞, σ-finite μ (6.16): the proof via Radon–Nikodym (Φ(1_E) defines a measure; its density is the representing g); the Riesz representation theorem for C_0(X)^* = M(X) (6.19), stated with its proof map; the Fourier thread for Part 8: the dual of C(T) is the space of measures. | The dictionary card: "a functional is a vector" ↔ "a functional is a function in L^q" ↔ "a functional on C is a measure"; a functional on C[0, 1] probed with narrowing bumps (the bump engine) reveals its measure point by point. | The representing g for a random functional on ℓ^p (finite case), asserted. |
| 14 | `Differentiation` | Derivatives of measures (7.1–7.3); the Hardy–Littlewood maximal function and the weak-type inequality (7.4), proved with the Vitali covering lemma (3× enlargements, 7.3); Lebesgue points (7.6–7.7); the Lebesgue differentiation theorem (7.10): for f ∈ L¹, averages over shrinking balls converge to f(x) a.e.; the Radon–Nikodym derivative is the a.e. limit of ratios (7.8). | Balls shrinking at a point; the covering lemma's disjoint subfamily with its triple enlargements; the maximal function as a "worst average". | Averages of a discontinuous f over shrinking intervals at 1,000 random points, asserted → f at 99.8% of them (a.e.); the Vitali selection on random intervals. |
| 15 | `AbsolutelyContinuous` | Functions of bounded variation; absolutely continuous functions (7.17); the fundamental theorem of calculus for the Lebesgue integral (7.18–7.20): f(x) − f(a) = ∫_a^x f′ iff f is absolutely continuous; the Cantor function has f′ = 0 a.e. and rises from 0 to 1: the museum card, "differentiable a.e., FTC fails". | The staircase with its derivative 0 almost everywhere and its total rise 1. | The Cantor function's increments over the removed intervals (0) vs its rise (1), asserted. |
| 16 | `ChangeOfVariables` | Differentiable transformations and the Lebesgue change of variables (7.24–7.26) in one card (the Jacobian from Part 4, now a.e.). | The grid of area factors from Part 4. | — |
| 17 | `Ledger` | Row 6: L^p and H, complete (Riesz–Fischer), the projection theorem, the interchange made legal: Fourier series converge in L²; the Fourier answer in L² and under Fejér. Preview: the complex plane (Part 7), then the general Banach space (Part 8). | The ledger. | — |

### Part 7. Complex Analysis, the Part the Rest of Analysis Needs (RCA prologue, 10–14, 17; highlights of 11, 15–16, 19–20) — ~55 min, 15 chapters

**Hook.** A function that is complex-differentiable once is differentiable infinitely often, is
its own power series, and is determined on a whole region by its values on a tiny arc. None of
this is true on the real line (Part 2's e^(−1/x²)). "Why is C so much better behaved than R?"
Domain colorings throughout, with the repo's phase-as-hue map.
**Payoff.** Everything Season 3 needs, proved: power series and the Neumann series picture
(resolvents), Liouville (Gelfand–Mazur), the Cauchy integral formula (the holomorphic functional
calculus), the maximum modulus principle and Phragmén–Lindelöf (interpolation), Runge (rational
approximation), and Montel's theorem as Arzelà–Ascoli's grandest payoff: the Riemann mapping
theorem, computed for a real polygon. Then a tour of the rest of the complex half.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | The three miracles; the exponential function as Rudin's prologue (periodicity, e^z ≠ 0, the definition of π); the plan. | Domain coloring of e^z; the phase wheel. | e^z on a grid; e^(2πi) asserted = 1 from the series. |
| 2 | `Holomorphic` | Complex differentiability (ch. 10); the Cauchy–Riemann equations as "the derivative is a rotation-scaling"; holomorphic functions are conformal where f′ ≠ 0; power series are holomorphic (10.6) and the zeros of a nonconstant holomorphic function are isolated (10.18). | A small grid mapped by f: squares stay squares (rotated and scaled); angles preserved. | Angles between grid curves under z² and e^z, asserted preserved; the Jacobian asserted a rotation-scaling. |
| 3 | `Integration` | Integration over paths (10.8); the index (winding number) of a closed path (10.10), integer-valued and computed; Cauchy's theorem for a triangle (10.13, Goursat's bisection: a zoom argument, instrument 7, the fourth time bisection has proved a theorem in this series) and in a convex set (10.14). | The winding number as the number of turns; Goursat's nested triangles shrinking to the point where f is "linear + small". | Winding numbers of a random closed curve about 20 points, computed by the integral and asserted integer. |
| 4 | `CauchyFormula` | The Cauchy integral formula (10.15); holomorphic ⇒ power series (10.16), the first miracle; Morera (10.17); Cauchy's estimates and Liouville (10.23); the fundamental theorem of algebra (10.25) as a corollary, paying Part 3's promise (8.8). | The value at the center as the average over a circle; the coefficients as integrals; a bounded entire function flattening. | A polynomial's roots found from the argument principle on a circle; Cauchy's formula asserted on random points. |
| 5 | `OpenMapping` | The zeros of holomorphic functions and the identity theorem (10.18): "determined by its values on any arc"; the open mapping theorem (10.32) and the local m-to-1 structure (10.30); the maximum modulus principle (10.24) with its proof from the open mapping theorem. | A tiny disk's image under f is an open set; the mountain with no interior peak (\|f\| on a disk). | \|f\| on a disk for f = z² + e^z; its maximum asserted on the boundary. |
| 6 | `GlobalCauchy` | The global Cauchy theorem (10.35) with Dixon's proof sketched on a proof map; homotopy and simply connected regions; the calculus of residues (10.42) and three integrals (∫ sin x / x, ∫ 1/(1 + x⁴), ∫ e^(−x²) cos 2bx) computed by residues and asserted against quadrature; Rouché (10.43); the nine equivalent faces of "simply connected" (13.11: homotopy, Cauchy's theorem, logarithms, square roots, polynomial approximation, no holes) on one card. | A contour deforming through a region where f is holomorphic, hopping over poles. | The three residue integrals vs quadrature, asserted. |
| 7 | `Schwarz` | The Schwarz lemma (12.2) and the automorphisms of the disk (12.6); Phragmén–Lindelöf (12.7–12.9) stated and used for the three-lines theorem (12.8) and its payoff, the Riesz–Thorin interpolation idea (a card; Hausdorff–Young previewed for Part 9). | The disk shrinking under a self-map; the strip with its three lines. | — |
| 8 | `Runge` | Runge's theorem (13.6–13.9): rational functions with poles outside a compact set approximate holomorphic functions uniformly; polynomials when the complement is connected; the proof map (the Cauchy formula as a Riemann sum of Cauchy kernels, then pole pushing); Mittag-Leffler (13.10) in one card. The payoff named: the functional calculus of Part 10. | Poles being pushed along a path to the outside; the Cauchy integral approximated by finitely many 1/(z − a_k). | A Runge approximant of 1/z on an annular compact set, sup error asserted < ε. |
| 9 | `NormalFamilies` | Normal families; Montel's theorem (14.6): a uniformly bounded family of holomorphic functions is normal (the Cauchy estimates give equicontinuity, then Arzelà–Ascoli, Part 3's theorem paying off). | The dictionary card: Arzelà–Ascoli ↔ Montel. | A uniformly bounded family (random polynomials bounded on a disk) and an extracted locally uniformly convergent subsequence, asserted. |
| 10 | `RiemannMapping` | The Riemann mapping theorem (14.8): every simply connected proper region is conformally a disk; the proof map (the family of injective maps into the disk is nonempty by a square-root trick, normal by Montel, the extremal map with largest derivative is onto, by the square-root trick again); the conformal map of a polygon computed and shown. | A polygon's interior flowing onto the disk with its grid staying orthogonal; the extremal selection as a maximization. | A Schwarz–Christoffel map of an L-shaped polygon, conformality asserted (angles preserved to 10⁻⁴), boundary mapped to the circle. |
| 11 | `Harmonic` | *Tour, no proof* (labeled) of ch. 11: harmonic functions, the Poisson integral (11.8–11.9) and the Dirichlet problem for the disk; the mean value property and the maximum principle; the relation to the stochastic video's walkers (Kakutani). | The Poisson kernel; the disk solution. | The Poisson integral of a boundary function on a grid, asserted harmonic (Laplacian < 10⁻⁶). |
| 12 | `ZerosProducts` | *Tour* of ch. 15: infinite products, the Weierstrass factorization theorem (every entire function is a product over its zeros), Jensen's formula, Blaschke products (the zeros of bounded functions in the disk satisfy Σ(1 − \|α_n\|) < ∞), and the Müntz–Szász theorem (which powers x^λ span C[0, 1]: Σ 1/λ_n = ∞) as a Hahn–Banach application previewed for Part 8. | A Blaschke product's domain coloring. | sin(πz) vs its product formula on a grid, asserted equal to 10⁻⁸. |
| 13 | `Continuation` | *Tour* of ch. 16: analytic continuation along curves and the monodromy theorem; the modular function and Picard's little theorem stated (an entire function misses at most one value), with the Riemann video's analytic continuation of ζ recalled. | Continuation of log around 0 as a spiral staircase. | — |
| 14 | `Hp` | *Tour* of ch. 17: H^p spaces and the Poisson integral; the F. and M. Riesz theorem; Beurling's theorem on invariant subspaces of the shift (every closed invariant subspace of H² is φH² for an inner function φ): the first spectral-theory fact of the series, previewed for Part 10's shift operator; ch. 19's Paley–Wiener previewed for Part 9; ch. 20's Mergelyan stated. | The shift moving a function's Fourier coefficients one step; an inner function's domain coloring. | — |
| 15 | `Ledger` | Row 7: H(Ω) with the topology of locally uniform convergence; complete; Montel; the interchange made legal: term-by-term differentiation of power series, and the Cauchy integral commuting with limits. Preview: Banach spaces. | The ledger. | — |

**Script notes for Part 7.** The part exists to serve Parts 8–10, and its chapter order is the order
in which those parts will cite it. The four "tour" chapters are labeled on screen; nothing stated
in them is used later without being named as "stated, not proved, in Part 7". If the series is
shortened (section 6), this is the first part to cut back to chapters 1–6 and 9–10.

### Part 8. Banach Spaces: Baire's Theorem and Its Three Children, Hahn–Banach, and Weak Topologies (RCA 5; FA 1–5) — ~65 min, 18 chapters

**Hook.** There is a continuous function whose Fourier series diverges at a point. Nobody can
write one down in closed form (du Bois-Reymond's 1873 construction is shown and computed), yet
Baire's theorem proves that *most* continuous functions are like this, in three lines, once one
knows the Dirichlet kernel's L¹ norm grows like (4/π²) log n (computed to n = 10⁶). "A theorem
about the existence of monsters, proved by counting."
**Payoff.** The four pillars of functional analysis (Baire ⇒ uniform boundedness, open mapping,
closed graph; Hahn–Banach), duality, the unit ball is never compact in infinite dimensions and what
replaces it (Banach–Alaoglu), Krein–Milman, compact operators, and three applications from
Grandpa Rudin's chapter 5.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | The divergent Fourier series; the Dirichlet kernel's norm; the plan. | D_n's side lobes; the Lebesgue constants climbing a log curve; the partial sums at 0 of the museum function creeping up. | ‖D_n‖₁ for n ≤ 10⁶, asserted within 1% of (4/π²) ln n + 1.27; du Bois-Reymond / Fejér-type example's s_N(0) to N = 2²⁰. |
| 2 | `Banach` | Normed spaces and Banach spaces (RCA 5.1–5.4): C(X), L^p, ℓ^p, c_0; bounded = continuous for linear maps (5.4); the operator norm; B(X, Y) is a Banach space when Y is; the dictionary: "matrix" ↔ "bounded operator". | The camera's map with the unit ball and an operator's image of it. | ‖T‖ for the Volterra operator Tf(x) = ∫_0^x f on L²[0, 1] (2/π, asserted numerically). |
| 3 | `TVS` | Grandpa Rudin's starting point: spaces that have no norm. The topology of C^∞(Ω) and of test functions needs countably many seminorms (FA 1.1–1.8); topological vector spaces, local convexity, Fréchet spaces (1.36–1.37), metrizability (1.24); finite-dimensional subspaces are closed (1.21); **a locally compact TVS is finite-dimensional (1.22)**, the honest end of Heine–Borel; the museum: L^p for 0 < p < 1 has no nonzero continuous linear functional (1.47). | Nested seminorm "ellipsoids" defining neighborhoods of 0; the p < 1 ball (non-convex, a star). | The ℓ^p ball for p = 1/2 (non-convex); the unit ball of ℓ² with e_n at distance √2 from each other (no finite ε-net; asserted). |
| 4 | `Baire` | The Baire category theorem (RCA 5.6 / FA 2.2): a complete metric space is not a countable union of nowhere dense sets; the proof as nested closed balls dodging each F_n (completeness pays); "meager" and "residual"; Q is meager in R; a residual set is "almost everything" in the topological sense (and this sense disagrees with measure: a residual set of measure zero exists, computed as a fat-Cantor complement). | Nested balls shrinking while avoiding a sequence of thin closed sets; the dust that cannot fill the space. | The fat-Cantor construction of a measure-zero residual set, measures asserted. |
| 5 | `UniformBoundedness` | Banach–Steinhaus (RCA 5.8 / FA 2.5–2.6): pointwise bounded ⇒ uniformly bounded, by Baire on the sets {x : sup‖T_n x‖ ≤ k}; the gliding-hump picture as the other proof; the application (RCA 5.11): the functionals f ↦ s_n(f)(0) have norms ‖D_n‖₁ → ∞, so for a dense G_δ of f ∈ C(T) the Fourier series diverges at 0; the Riemann–Lebesgue lemma (5.14) and the Fourier map L¹ → c_0 is not onto (5.15, open mapping used in reverse). Carleson (1966) quoted: for L² the series converges a.e. | The game board for a family of operators (ε before the operator); the gliding hump. | The operator norms asserted equal to ‖D_n‖₁; the explicit divergent f's partial sums. |
| 6 | `OpenMapping` | The open mapping theorem (RCA 5.9–5.10 / FA 2.11–2.12): a bounded surjection between Banach spaces maps open sets to open sets; the proof map (Baire gives that some n·T(B) is dense in a ball; completeness upgrades "dense in" to "contains"); the inverse mapping theorem; the closed graph theorem (FA 2.15) and the Hellinger–Toeplitz theorem (an everywhere-defined symmetric operator is bounded: the reason unbounded operators have domains, Part 10). | The image of the unit ball containing a small ball; the graph of T as a closed set in X × Y. | A bounded bijection of ℓ² (finite section) and the radius of the ball inside T(B), asserted ≥ 1/‖T^(−1)‖. |
| 7 | `HahnBanach` | Hahn–Banach, the dominated extension (RCA 5.16 / FA 3.2): extend one dimension at a time (the sandwich: sup of lower bounds ≤ inf of upper bounds, a one-line computation shown), then Hausdorff maximality; the norm-preserving version (3.3); consequences (RCA 5.19–5.21): functionals separate points, the norm is a sup over the dual ball; the separation theorems (FA 3.4) with the Minkowski functional (gauge) of a convex set. | The sandwich inequality's picture; a hyperplane (the covector stacks) sliding between two convex sets; the gauge as "how far to scale the set to reach x". | Separation of two random convex polygons by a computed hyperplane; the gauge of an ellipse. |
| 8 | `Applications` | Three Hahn–Banach payoffs: the abstract Poisson integral (RCA 5.22–5.24: the Dirichlet problem solved by extending a functional, the harmonic function of Part 7 reappearing); Müntz–Szász stated (RCA 15.26); the Banach limit (FA ex.) as a functional no formula can give. | A boundary function extended into the disk by the Poisson kernel. | The Poisson integral checked harmonic as in Part 7. |
| 9 | `Dual` | The normed dual (FA 4.1–4.7): annihilators, (X/M)* and M*; reflexivity; the duals computed: (ℓ^p)* = ℓ^q, (c_0)* = ℓ¹, (ℓ¹)* = ℓ^∞, C(K)* = M(K) (the Riesz representation theorem of Part 6, now in its place); ℓ¹ is not reflexive; the dictionary: "a row vector" ↔ "a functional". | The dual-ball shapes: the diamond's dual is the square. | (ℓ^p)* = ℓ^q checked on finite sections: the dual norm of a random functional asserted equal to its ℓ^q norm. |
| 10 | `Weak` | Weak and weak-* topologies (FA 3.8–3.14): e_n → 0 weakly in ℓ² but ‖e_n‖ = 1; sin(nx) → 0 weakly in L² (Riemann–Lebesgue); three ways to go weakly to 0 without going to 0 in norm: oscillation (sin nx), concentration (tall thin bumps), translation (the sliding bump), the bump engine's evil twins once more; the camera: the trail runs off along ever-new axes while every shadow converges; weakly convergent sequences are bounded (Banach–Steinhaus again); the weak closure of the unit sphere is the whole ball (FA ch. 3 exercises; the sphere is "weakly dense in the ball", shown on a 3D section as a labeled schematic). Mazur: convex closed sets are weakly closed. | The trail and its shadows (instrument 3); the dashboard's "tested" lens lit while the norm lens stays dark. | ⟨e_n, y⟩ → 0 for 50 random y asserted; convex combinations of sin(nx) with small L² norm, asserted. |
| 11 | `Alaoglu` | The Banach–Alaoglu theorem (FA 3.15): the closed unit ball of X* is weak-* compact, because it embeds in a product of discs and Tychonoff's theorem applies (Appendix A); the dual ball of ℓ¹ as [−1, 1]^N, a Hilbert cube; sequential version for separable X (3.17); the payoff: existence of extremal functionals, of invariant means, of limits of measures (Prokhorov in disguise); Goldstine's theorem (FA ch. 4 exercises) and the characterization of reflexivity (the ball is weakly compact). | The Hilbert cube; a sequence of functionals with a weak-* cluster point found by the diagonal argument. | A sequence of probability measures on [0, 1] (random histograms) and its weak-* limit extracted by the diagonal argument, moments asserted to converge. |
| 12 | `KreinMilman` | Extreme points; the Krein–Milman theorem (FA 3.23): a compact convex set in a locally convex space is the closed convex hull of its extreme points; Milman's converse (3.25); the extreme points of the balls of ℓ^p: 2n points (p = 1), the whole sphere (p = 2), 2^n corners (p = ∞), none at all for the ball of L¹[0, 1] (so L¹ is no dual space); the extreme points of the probability measures are the Dirac masses. | The p-ball morph with its extreme points highlighted; the L¹ ball with no corners (any f splits into two halves). | Extreme points of the ℓ^p balls in R³, asserted by the splitting test. |
| 13 | `Compact` | Compact operators (FA 4.16–4.25): the limit of finite-rank operators (in Hilbert space, the converse); the Volterra operator and the Green's function operator of a string; T compact ⇒ T* compact; the Riesz–Schauder theory (4.18–4.25): the spectrum is countable with 0 the only accumulation point, each nonzero eigenvalue has finite multiplicity, and the Fredholm alternative (dim N(T − λ) = codim R(T − λ)); the dictionary: "square matrices" ↔ "compact operators" (the operators for which linear algebra survives). The spectral theorem itself waits for Part 10. | The unit ball mapped to a "thin" set (an ellipsoid with axes shrinking to 0); the eigenvalues of the string operator accumulating at 0. | The Green's function operator for −u″ on [0, 1] discretized at N = 2,000: eigenvalues asserted ~ 1/(n²π²); the eigenvectors asserted to be sines. |
| 14 | `Grothendieck` | FA 5.2: a closed subspace of L^p[0, 1] consisting of bounded functions is finite-dimensional, by the closed graph theorem; the proof shown in full as the model closed-graph application. | The dictionary card for the closed graph theorem. | — |
| 15 | `Haar` | Kakutani's fixed-point theorem (FA 5.11) and the existence of Haar measure on compact groups (5.14): a fixed point of a group of affine isometries of a compact convex set (the probability measures, weak-* compact by Alaoglu); Haar measure on the circle and on SO(3) shown. | A compact convex set with a group acting; the fixed point; uniform measure on the sphere of rotation axes. | Averages over 10⁴ Haar-random rotations (from quaternions) asserted invariant. |
| 16 | `Uncomplemented` | FA 5.19: c_0 is not complemented in ℓ^∞ (no bounded projection), by the counting argument with an uncountable almost-disjoint family; the moral: Hilbert space's projections are a luxury. | An uncountable almost-disjoint family of subsets of N drawn as branches of a tree. | — |
| 17 | `Interpolation` | FA 5.9–5.10 (Bishop's and the Rudin–Carleson theorems) in one card, and the generalized Stone–Weierstrass theorem (5.7) via Krein–Milman: a proof-map sketch. | The proof map. | — |
| 18 | `Ledger` | Row 8: Banach and Fréchet spaces; Baire; Alaoglu; the interchange made legal: pointwise bounds become uniform bounds, and limits of functionals exist; the Fourier answer: divergence for a residual set of continuous functions, a.e. convergence for L² (Carleson, quoted). Preview: distributions. | The ledger. | — |

**Script notes for Part 8.** Chapters 14–17 are the sampled applications and run 2–3 minutes each.
Chapter 3 is where the series explains, once and honestly, why Grandpa Rudin works in topological
vector spaces: the test-function spaces of Part 9 are not normable, and the viewer meets that fact
here, before meeting the spaces. The Hellinger–Toeplitz theorem is planted in chapter 6 so that
Part 10's unbounded operators arrive as a necessity, not a complication.

### Part 9. Distributions and the Fourier Transform: Differentiating Anything (RCA 9; FA 6–9) — ~60 min, 17 chapters

**Hook.** Dirac's δ, "the function that is zero everywhere except at one point, with integral one",
which cannot exist (an integral cannot see one point) and which physicists used for twenty years
anyway; Heaviside's operational calculus; the derivative of a step. Then the move that fixes
everything: stop asking what δ *is* and ask what it *does* to a test function. Every function
becomes differentiable infinitely often.
**Payoff.** The Fourier transform on L¹, L², S and S′ (Plancherel: a unitary map; the Gaussian as
its own transform); every distribution is locally a derivative of a continuous function;
Paley–Wiener (support ↔ growth, the honest end of Part 2's e^(−1/x²)); Sobolev's lemma; a
fundamental solution for every constant-coefficient PDE (Malgrange–Ehrenpreis); and Wiener's
Tauberian theorem with the prime number theorem as its corollary, the series' handshake with the
repo's Riemann video.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | δ and the impossibility; Heaviside; the move to test functions; the plan. | Bumps narrowing to a spike (height blowing up) while ∫ φ·bump → φ(0); H′ = δ as a limit of smoothed steps' derivatives. | ∫ φ(x) n·ρ(nx) dx → φ(0) for 10 test functions, asserted; the smoothed step's derivative integrating to 1. |
| 2 | `TestFunctions` | Mollifiers (a C^∞ bump with compact support, built from e^(−1/x) of Part 2, which finally earns its keep); D(Ω) and its topology (FA 6.2–6.5: an inductive limit of Fréchet spaces, the reason for Part 8's chapter 3); convergence in D; the Fourier thread: a trigonometric polynomial tested against a test function. | The bump family; the seminorm nests of Part 8 shrinking around a test function. | The mollifier's derivatives to order 10, asserted continuous and compactly supported. |
| 3 | `Distributions` | D′(Ω) (6.7–6.10): continuous linear functionals on D; functions and measures as distributions; the characterization by local seminorm bounds (6.8); order of a distribution; the museum: δ, δ′, the principal value of 1/x (a distribution of order 1 that no measure gives), the Dirac comb. | The covector stacks of Part 8 applied to a test function; p.v. 1/x as the symmetric cancellation of two divergent halves. | ⟨p.v. 1/x, φ⟩ by symmetric truncation at ε = 10^(−k), asserted convergent; ⟨δ′, φ⟩ = −φ′(0). |
| 4 | `Calculus` | Derivatives of distributions (6.11–6.15): the definition is integration by parts with the derivative thrown onto the test function (the animation moves the prime across); every distribution has derivatives of all orders and they commute; H′ = δ, \|x\|′ = sign, (log\|x\|)′ = p.v. 1/x, (sign)′ = 2δ; multiplication by C^∞ functions and Leibniz; the Fourier thread: the sawtooth's distributional derivative is 1 − 2π·(Dirac comb), and its Fourier series differentiated term by term is the series of the comb, which converges in D′ (Fourier was right, in the right space). | The prime hopping from f to φ with a sign change; the sawtooth's derivative as a flat line with downward spikes. | ⟨H′, φ⟩ = φ(0) asserted; the sawtooth's series differentiated term by term tested against φ, asserted to converge to the comb's action. |
| 5 | `Localization` | Supports, localization and the sheaf property (6.19–6.21); distributions with compact support are the dual of C^∞ (6.24); **a distribution supported at one point is a finite sum of derivatives of δ (6.25)**; **every distribution is locally a derivative of some continuous function (6.26–6.27)**: the whole space D′ is "functions, differentiated". | A distribution's support as the region where it is awake; δ′′ at a point; a wild distribution revealed as the 5th derivative of a continuous function. | A random distribution of order 3 integrated five times (as a distribution) into a continuous function, re-differentiated and tested, asserted equal. |
| 6 | `Convolution` | Convolution with a test function smooths (6.30–6.33): T ∗ φ is C^∞; approximate identities (6.32): every distribution is a limit of test functions; convolution of distributions with compact support; the Fourier thread: Fejér's kernel as an approximate identity. | A rough distribution convolved with a shrinking mollifier, regaining its roughness as the mollifier narrows. | Mollified Cantor measure and mollified δ′ at ε = 1/2^k; sup norms asserted to blow up like ε^(−2) for δ′. |
| 7 | `FourierL1` | The Fourier transform on L¹ (RCA 9.1–9.6): f̂ is continuous and vanishes at infinity (Riemann–Lebesgue); the formal properties (translation ↔ modulation, derivative ↔ multiplication by iξ, convolution ↔ product); the Gaussian is its own transform (9.7), proved by the ODE f′ = −xf; the uncertainty principle in one card (narrow ↔ wide), with the quantum video's version recalled; Rudin's convention f̂(t) = (1/√2π) ∫ f(x) e^(−ixt) dx is fixed here for the rest of the series. | The dictionary of pairs: a box ↔ sinc, a Gaussian ↔ a Gaussian, a derivative ↔ a ramp; the frequency side in orange. | FFT transforms vs closed forms asserted to 10⁻⁶; the Gaussian's self-duality. |
| 8 | `Inversion` | The inversion theorem (9.11) via the Gaussian trick (multiply by e^(−ε²ξ²) and let ε → 0, an approximate identity again); uniqueness (9.12); the Plancherel theorem (9.13): the transform is an isometry of L¹ ∩ L² extended to a unitary of L²; the dictionary: "orthogonal change of basis" ↔ "the Fourier transform". | The Gaussian lid shrinking in frequency and spreading in space; the L² lens of the dashboard lit by Plancherel. | Plancherel asserted for random L² functions by FFT; the inversion on a discontinuous f converging in L² but not uniformly (Gibbs again). |
| 9 | `Schwartz` | The Schwartz space S (FA 7.3–7.7): the Fourier transform is a continuous bijection of S onto itself (7.7); tempered distributions S′ (7.11–7.15), where δ, polynomials and L^p functions live, and the transform extends by duality: δ̂ = 1, 1̂ = δ, the Dirac comb is its own transform (Poisson summation, the Riemann video's Jacobi identity recalled). | Rapidly decreasing functions as those that outrun every polynomial; the comb transforming into a comb. | Poisson summation Σ e^(−πn²t) = t^(−1/2) Σ e^(−πn²/t) asserted to 10⁻¹²; the FFT of a sampled Gaussian comb. |
| 10 | `PaleyWiener` | The Paley–Wiener theorems (FA 7.22–7.23; RCA 19.2–19.3): a function has compact support in [−A, A] iff its transform extends to an entire function of exponential type A; Part 2's flat function and Part 7's analytic continuation meet; domain coloring of a bump's transform in the complex plane; the Denjoy–Carleman theorem stated (quasi-analytic classes). | The transform of a bump, colored by phase, decaying along the real axis and growing like e^(A\|Im z\|) vertically. | The transform of a bump evaluated on a complex grid (quadrature), growth asserted ≤ C e^(A\|Im z\|). |
| 11 | `Sobolev` | Sobolev spaces H^s via the transform (7.25): the norm ∫ (1 + \|ξ\|²)^s \|f̂\|²; Sobolev's lemma: H^s ⊂ C^k when s > k + n/2 (the proof is Cauchy–Schwarz in frequency, three lines); the Fourier thread: the sawtooth is in H^s exactly for s < 1/2. | A function's regularity read off the decay of its transform; the critical s for the sawtooth. | The sawtooth's H^s norms vs s, asserted finite iff s < 1/2 (partial sums to 10⁶). |
| 12 | `Fundamental` | Fundamental solutions (FA 8.1–8.4): P(D)E = δ; the heat kernel, the Newtonian potential (−1/4π\|x\|) and 1/(2π) log\|x\| in 2D, with their checks; solving P(D)u = f as u = E ∗ f (the Green's function of Part 8's string, now in general). | A spike of heat spreading; the potential of a point charge; the convolution building u from f. | ΔE tested against test functions, asserted = φ(0); the heat kernel's integral asserted 1. |
| 13 | `MalgrangeEhrenpreis` | The Malgrange–Ehrenpreis theorem (8.5): every nonzero constant-coefficient operator has a fundamental solution; Rudin's proof on a proof map (shift the integration contour in one variable to dodge the zeros of P, average over directions, use Paley–Wiener-type estimates); elliptic regularity (8.12) stated: elliptic operators are hypoelliptic. | The zero set of a polynomial in C and the contour stepping around it; the direction average. | A fundamental solution of u″ + u = δ, whose symbol 1 − ξ² vanishes at ξ = ±1 so that the naive 1/P is not integrable, built by the contour recipe numerically and tested against bumps. |
| 14 | `Wiener` | Wiener's Tauberian theorem (FA 9.3–9.7): the translates of f ∈ L¹(R) span L¹ iff f̂ never vanishes; the Banach-algebra reading (L¹ with convolution; the complex homomorphisms are evaluations of f̂, RCA 9.22–9.23, previewing Part 10's Gelfand theory); Pitt's theorem. | Translates of a kernel spanning; a transform with a zero failing to. | Translates of a Gaussian approximating a random L¹ function to 10⁻³, vs translates of a sinc (whose transform vanishes) failing, asserted. |
| 15 | `PrimeNumbers` | The prime number theorem (FA 9.12) from Wiener's theorem by Rudin's route (Ingham's Tauberian argument, a Lambert series, the non-vanishing of ζ on Re s = 1); the repo's Riemann video is recalled for ζ, and this chapter shows the analytic engine behind its chapter 2. | The timeline strip meets the Riemann video's prime staircase. | π(x)/(x/ln x) and π(x)/li(x) to 10⁹ (reused from videos/riemann's cache), asserted → 1 slowly. |
| 16 | `Renewal` | The renewal equation (9.15) in one card: the Tauberian theorem applied to a convolution equation. | — | — |
| 17 | `Ledger` | Row 9: D, S, D′, S′; Fréchet completeness; the interchange made legal: differentiation under everything (every distributional limit commutes with every derivative); the Fourier answer: every distribution's Fourier series converges in D′. Preview: the spectrum. | The ledger. | — |

### Part 10. Banach Algebras and the Spectral Theorem (RCA 18; FA 4 (compact operators), 10–13) — ~65 min, 18 chapters

**Hook.** "Spectrum" is the same word for the lines of hydrogen and for the set of λ where T − λ
has no inverse, and that is not a coincidence: the energies of an atom are the spectrum of an
unbounded self-adjoint operator. The series ends by proving what the repo's quantum videos
assumed: that self-adjoint operators can be diagonalized, even when they have no eigenvectors at
all. First, the simplest surprise: the shift on ℓ² has no eigenvalues, yet its spectrum is the
whole closed unit disc (computed, with the backward shift's eigenvectors (1, λ, λ², …) filling the
open disc).
**Payoff.** Gelfand's theory (Wiener's 1/f theorem in three lines; Gelfand–Naimark), the spectral
theorem for compact self-adjoint, bounded normal and unbounded self-adjoint operators, the
continuous functional calculus, projection-valued measures, Stone's theorem, and the quantum
mechanics connection closed: position, momentum and the Hamiltonian as unbounded self-adjoint
operators, with the Born rule as a spectral measure.

| # | Scene | What it establishes | The picture | Computed on screen |
|---|---|---|---|---|
| 1 | `Hook` | The two spectra; the shift; the plan. | The hydrogen lines next to a spectrum drawn in the complex plane; the shift moving coefficients one slot. | The backward shift's eigenvectors for 200 λ in the disc; the forward shift has none (asserted: (S − λ)x = 0 ⇒ x = 0); the ε-pseudospectrum of a 2,000 × 2,000 section filling the disc. |
| 2 | `BanachAlgebras` | Banach algebras (RCA 18.1–18.5 / FA 10.1–10.4): C(K), B(X), L¹ with convolution, ℓ¹(Z), the disc algebra; the Neumann series and the invertible elements form an open set (18.4 / 10.7) with inversion continuous, the theorem of Part 4 (9.8) in its final home. | The invertibles as an open region; the Neumann series as a geometric series of operators. | (I − A)^(−1) = Σ A^n for a random A with ‖A‖ < 1, asserted. |
| 3 | `Spectrum` | The spectrum σ(x) (18.5 / 10.10–10.12): nonempty and compact, with the resolvent λ ↦ (x − λ)^(−1) holomorphic (Part 7's power series) and Liouville giving nonemptiness; Gelfand–Mazur (18.7 / 10.14): a Banach field is C; the spectral radius formula ρ(x) = lim ‖xⁿ‖^(1/n) (18.9 / 10.13), from the radius of convergence of the resolvent's Laurent series (Part 2's 3.39 and Part 7's 10.16 pay); the museum: the Volterra operator has spectrum {0} and ‖Vⁿ‖^(1/n) → 0 though ‖V‖ = 2/π. | Domain coloring of the resolvent (a matrix's) in λ; the spectral radius as the smallest circle outside which the Laurent series converges. | ‖Vⁿ‖^(1/n) for the discretized Volterra operator, asserted → 0; ρ(A) vs max\|eigenvalue\| for random matrices, asserted equal. |
| 4 | `SymbolicCalculus` | The holomorphic functional calculus (FA 10.21–10.27): f(x) = (1/2πi) ∮ f(λ)(λ − x)^(−1) dλ over a contour around the spectrum (the Cauchy formula of Part 7, with an operator in the slot); the spectral mapping theorem σ(f(x)) = f(σ(x)); exponentials, logarithms and square roots of operators; Runge's theorem (Part 7) as the reason rational functions suffice; Lomonosov's invariant subspace theorem (10.35) stated with its idea (Schauder's fixed point). | A contour around a computed spectrum with the resolvent colored by phase; e^(tA) built by the contour integral. | e^A by the contour integral vs scipy's expm for a random 6 × 6 A, asserted equal to 10⁻⁸. |
| 5 | `Gelfand` | Commutative Banach algebras (RCA 18.10–18.18 / FA 11.1–11.9): maximal ideals ↔ complex homomorphisms (18.17 / 11.5); the Gelfand transform x̂(h) = h(x) on the compact space Δ of homomorphisms; σ(x) = range of x̂; ℓ¹(Z): Δ is the circle and the Gelfand transform is the Fourier series; **Wiener's theorem (RCA 18.21; FA ch. 11)**: if f has an absolutely convergent Fourier series and never vanishes, so does 1/f, proved in three lines; the Gleason–Kahane–Żelazko theorem (10.9) stated. | The Gelfand transform as "an element becomes a function on the maximal ideals"; the circle as the maximal ideal space of ℓ¹(Z). | 1/f's Fourier coefficients for a nonvanishing f with absolutely summable coefficients, Σ\|c_n\| asserted finite (partial sums to 10⁵, tail bounded). |
| 6 | `Cstar` | Involutions and B*-algebras (FA 11.14–11.18): the Gelfand–Naimark theorem (11.18): a commutative B*-algebra is C(Δ); the continuous functional calculus for normal elements (11.19–11.20); spectral permanence; every B*-algebra is an operator algebra (12.41, GNS) stated with its idea (positive functionals, 11.31–11.33). | The dictionary: "a commutative C*-algebra" ↔ "continuous functions on a compact space". | The functional calculus f(A) for a normal 6 × 6 A computed two ways (eigen-decomposition and the Gelfand picture), asserted equal. |
| 7 | `HilbertOperators` | Bounded operators on Hilbert space (FA 12.1–12.15): adjoints, normal, self-adjoint, unitary, projections; ‖T*T‖ = ‖T‖²; the numerical range; the Fuglede–Putnam commutativity theorem (12.16) stated; the dictionary: "symmetric / orthogonal / projection matrices" ↔ the same words. | The adjoint as the reflected operator in the camera; a projection as a shadow. | ‖T*T‖ = ‖T‖² asserted for random operators; a self-adjoint operator's numerical range asserted real. |
| 8 | `CompactSelfAdjoint` | The spectral theorem for compact self-adjoint operators (from FA 4.18–4.25 plus 12.29): an orthonormal basis of eigenvectors with eigenvalues → 0, proved by the Rayleigh quotient (the largest \|λ\| is attained, by compactness: Part 3's Arzelà–Ascoli spirit) and iteration; the vibrating string: the Green's function operator's eigenfunctions are the sines, so Fourier series are the spectral theorem for −d²/dx²; the heat equation solved by the eigen-expansion, and the quantum video's chapter 9 recalled. | The string's modes appearing one by one as the operator is "peeled" (deflation); the dictionary: "diagonalize a symmetric matrix" ↔ this. | The Green's operator's eigenpairs at N = 4,000 vs n²π² and sin(nπx), asserted; the heat solution vs the eigen-expansion. |
| 9 | `NoEigenvectors` | The multiplication operator (Mf)(x) = x f(x) on L²[0, 1]: self-adjoint, spectrum [0, 1], no eigenvectors at all (the equation (x − λ)f = 0 forces f = 0 a.e.); approximate eigenvectors (narrowing bumps); the position operator of quantum mechanics is this; what "diagonalizing" must mean when there is nothing to diagonalize: f(M) = multiplication by f, and "the spectral measure of a state ψ is \|ψ\|²dx". | Bumps narrowing at λ with ‖(M − λ)ψ‖ → 0; the Born rule's \|ψ(x)\|² as a measure on the spectrum. | ‖(M − λ)ψ_n‖/‖ψ_n‖ asserted → 0; the spectral measure of a packet asserted to integrate to 1. |
| 10 | `ResolutionsOfIdentity` | Projection-valued measures (FA 12.17–12.21): E(ω) a projection for each Borel set, countably additive in the strong topology; integration ∫ f dE as a *-isomorphism from L^∞(E) into B(H); the operator ∫ λ dE; the measures E_{x,y}(ω) = ⟨E(ω)x, y⟩; for M, E(ω) = multiplication by 1_ω; for a compact self-adjoint operator, E(ω) = the projection onto the eigenvectors with eigenvalues in ω. | The spectrum as an axis with projections "cutting out" bands; a state's spectral measure as amber mass along the axis. | For a 50 × 50 self-adjoint matrix and random x, the measure E_{x,x} as a histogram over eigenvalues, asserted total ‖x‖². |
| 11 | `SpectralTheorem` | The spectral theorem for bounded normal operators (FA 12.22–12.23): T = ∫ λ dE over σ(T), with E unique and commuting with everything that commutes with T; Rudin's proof on a proof map (the commutative B*-algebra generated by T and T*, Gelfand–Naimark, then the Riesz representation theorem of Part 5 applied to x, y ↦ ⟨f̂(T)x, y⟩ to manufacture the measures: the whole series in one proof); eigenvalues of normal operators (12.29); the functional calculus f(T) for Borel f; positive operators and square roots (12.32–12.33), polar decomposition (12.35); von Neumann's ergodic theorem (12.44) as a payoff (the averages of a unitary converge to the projection onto its fixed vectors). | The proof map with Parts 3, 5, 6, 7, 8 lit as each is used; the polar decomposition as "rotation × stretch" on the camera. | The spectral theorem checked on a random normal 8 × 8 operator; the ergodic averages of a random unitary converging to the fixed-space projection, asserted. |
| 12 | `Unbounded` | Why unbounded (FA 13.1–13.9): d/dx and multiplication by x are not bounded, but the Hellinger–Toeplitz theorem (Part 8) says an everywhere-defined symmetric operator is bounded, so domains are forced; graphs, closed operators, adjoints via graphs; symmetric vs self-adjoint, the distinction that matters; the museum: D = i d/dx on L²[0, 1] with domain C_c^∞(0, 1) is symmetric, not self-adjoint; its closure has deficiency indices (1, 1) and a one-parameter family of self-adjoint extensions (boundary conditions f(1) = e^(iθ) f(0)), each with a different spectrum {2πn − θ}: the spectrum depends on the boundary condition. | The graph of an operator as a subspace; the family of self-adjoint extensions as a circle of boundary conditions, each with its own ladder of eigenvalues sliding with θ. | The spectrum of i d/dx with twisted boundary conditions at θ = 0, π/2, π, computed by finite differences and asserted {2πn − θ} to 10⁻⁴. |
| 13 | `Cayley` | The Cayley transform (13.17–13.19): U = (T − i)(T + i)^(−1) turns symmetric operators into isometries and self-adjoint ones into unitaries with 1 not an eigenvalue; deficiency indices as the dimensions of the gaps; von Neumann's classification of self-adjoint extensions. | The real line bent onto the circle (λ ↦ (λ − i)/(λ + i)), with the spectrum going along. | The Cayley transform of the θ-extensions' spectra landing on the circle, asserted. |
| 14 | `UnboundedSpectral` | The spectral theorem for unbounded self-adjoint operators (13.30): T = ∫ λ dE over an unbounded spectrum, obtained from the bounded theorem for the Cayley transform; the functional calculus; the position and momentum operators diagonalized by, respectively, nothing and the Fourier transform (Part 9's Plancherel is the spectral theorem for −i d/dx on L²(R)); the dictionary's last card: "eigenvalues" ↔ "the spectrum, a measure's worth of them". | The Fourier transform as the change of basis that turns d/dx into multiplication by iξ. | P = −i d/dx on a packet: F P F^(−1) asserted = multiplication by ξ on the FFT grid to 10⁻⁸. |
| 15 | `Stone` | Semigroups (13.34–13.37, Hille–Yosida stated) and Stone's theorem (13.38): strongly continuous one-parameter unitary groups are U(t) = e^(itA) with A self-adjoint; the Schrödinger equation as the statement that time evolution is a unitary group (the quantum sequel's chapter 2 recalled), and the generator's self-adjointness is what the quantum videos assumed; the heat semigroup as the contraction case. | Each spectral band of a state rotating at its own rate λ (the quantum video's "bank of clocks", now proved to be the general case); the repo's Schrödinger packet evolving, labeled U(t) = e^(−itH), with H's spectral measure fixed in time. | The quantum video's split-operator solution vs e^(−itH) by the spectral decomposition of a discretized H, asserted equal to 10⁻⁶; unitarity asserted. |
| 16 | `QuantumClosure` | What the series has proved about quantum mechanics: observables are self-adjoint operators (so they have spectral measures); the Born rule is a spectral measure; x and p have continuous spectra and no eigenvectors; [x, p] = iħ forces unboundedness (Wintner / Wielandt: a trace argument, the quantum sequel's chapter 3, now with the honest reason); the hydrogen spectrum is point spectrum below 0 and continuous above. | The hydrogen levels as point spectrum, the continuum as a band; the Born rule as amber mass on the spectral axis. | The finite-difference hydrogen (radial, ℓ = 0) spectrum: bound states asserted at −1/(2n²) to 10⁻³, continuum above 0. |
| 17 | `Outro` | The ledger's last row (B(H) and the algebra it generates; complete; Alaoglu again; the interchange made legal: f(T) for any Borel f, limits of functions becoming limits of operators; the Fourier answer: the Fourier transform *is* the spectral theorem). The full ledger, the full timeline, and what lies beyond (operator algebras, index theory, nonlinear analysis, PDE). | The ledger and the timeline, complete. | — |
| 18 | `Credits` | Sources and the honest list of what was toured rather than proved. | — | — |

**Script notes for Part 10.** The proof of the spectral theorem (chapter 11) is the series' climax and
is written to use every earlier part visibly: the proof map lights Part 3 (Stone–Weierstrass behind
Gelfand–Naimark), Part 5 (the Riesz representation theorem makes the measures), Part 6 (Hilbert
space), Part 7 (Liouville and the Cauchy formula behind the spectrum and the calculus), Part 8
(Hahn–Banach and Alaoglu behind the maximal ideal space). Chapters 12–16 are the reason Grandpa
Rudin's chapter 13 is in the plan at all: the repo's quantum videos assumed self-adjointness and the
spectral theorem, and this is where they are paid for.

---

## 4. Research notes

Two background investigations fed this plan: a chapter-by-chapter map of the three books (from the
scanned third-edition contents of PMA on archive.org, the published tables of contents of RCA and
FA, and the syllabi of courses that teach from them), and a catalog of published visual and
animated treatments of every topic in the series. Theorem numbers marked [verified] below were read
from the PMA scan; the others are from the tables of contents and standard references and are to be
re-checked when each script is written.

### 4.1 Where each Rudin chapter goes

| Book chapter | Series location |
|---|---|
| PMA 1 (number systems; appendix: Dedekind cuts) | Part 1, ch. 2–6 |
| PMA 2 (basic topology) | Part 1, ch. 7–12 |
| PMA 3 (sequences and series) | Part 2, ch. 1–9 |
| PMA 4 (continuity) | Part 2, ch. 10–12 |
| PMA 5 (differentiation) | Part 2, ch. 13–16 |
| PMA 6 (Riemann–Stieltjes) | Part 3, ch. 2–5 |
| PMA 7 (sequences of functions, Arzelà–Ascoli, Stone–Weierstrass) | Part 3, ch. 1, 6–13 |
| PMA 8 (special functions, Fourier series) | Part 3, ch. 14–16 (the gamma function cut to a card) |
| PMA 9 (several variables) | Part 4, ch. 2–9 |
| PMA 10 (differential forms) | Part 4, ch. 10 (a labeled tour) |
| PMA 11 (Lebesgue theory) | Part 5 (the comparison with Riemann, 11.33, in ch. 10); L² and Riesz–Fischer (11.42–11.45) in Part 6 |
| RCA prologue (the exponential) | Part 7, ch. 1 |
| RCA 1 (abstract integration) | Part 5, ch. 4–8 |
| RCA 2 (positive Borel measures, Riesz representation, Lusin) | Part 5, ch. 2–3, 9–11 |
| RCA 3 (L^p) | Part 6, ch. 2–5 |
| RCA 4 (Hilbert space) | Part 6, ch. 6–10 |
| RCA 5 (Banach-space techniques, divergent Fourier series, Hahn–Banach, Poisson) | Part 8, ch. 2, 4–8 |
| RCA 6 (complex measures, Radon–Nikodym, duals of L^p and C_0) | Part 6, ch. 11–13 |
| RCA 7 (differentiation, maximal function, FTC) | Part 6, ch. 14–16 |
| RCA 8 (product measures, Fubini, convolution) | Part 5, ch. 12–13 |
| RCA 9 (Fourier transforms, Plancherel, L¹ as a Banach algebra) | Part 9, ch. 7–8, 14 |
| RCA 10 (holomorphic functions, Cauchy, residues) | Part 7, ch. 2–6 |
| RCA 11 (harmonic functions) | Part 7, ch. 11 (tour); Part 8, ch. 8 (the abstract Poisson integral) |
| RCA 12 (maximum modulus, Schwarz, Phragmén–Lindelöf) | Part 7, ch. 5, 7 |
| RCA 13 (Runge, Mittag-Leffler, simple connectivity) | Part 7, ch. 6, 8 |
| RCA 14 (conformal mapping, normal families, Riemann mapping) | Part 7, ch. 9–10 |
| RCA 15 (zeros, products, Blaschke, Müntz–Szász) | Part 7, ch. 12 (tour); Part 8, ch. 8 |
| RCA 16 (analytic continuation, Picard) | Part 7, ch. 13 (tour) |
| RCA 17 (H^p, Beurling) | Part 7, ch. 14 (tour) |
| RCA 18 (Banach algebras, Wiener's theorem) | Part 10, ch. 2–5 |
| RCA 19 (Paley–Wiener, Denjoy–Carleman) | Part 9, ch. 10 |
| RCA 20 (Mergelyan) | Part 7, ch. 14 (stated) |
| FA 1 (topological vector spaces) | Part 8, ch. 3 |
| FA 2 (completeness: Baire and its children) | Part 8, ch. 4–6 |
| FA 3 (convexity: Hahn–Banach, weak topologies, Alaoglu, Krein–Milman) | Part 8, ch. 7, 10–12 |
| FA 4 (duality, adjoints, compact operators) | Part 8, ch. 9, 13; the Riesz–Schauder theory also in Part 10, ch. 8 |
| FA 5 (applications) | Part 8, ch. 14–17 (four of ten, the rest named) |
| FA 6 (test functions and distributions) | Part 9, ch. 2–6 |
| FA 7 (Fourier transforms, tempered distributions, Paley–Wiener, Sobolev) | Part 9, ch. 9–11 |
| FA 8 (differential equations: fundamental solutions, Malgrange–Ehrenpreis) | Part 9, ch. 12–13 |
| FA 9 (Tauberian theory, the prime number theorem) | Part 9, ch. 14–16 |
| FA 10 (Banach algebras, symbolic calculus, Lomonosov) | Part 10, ch. 2–4 |
| FA 11 (commutative Banach algebras, Gelfand, B*-algebras) | Part 10, ch. 5–6 |
| FA 12 (bounded operators on Hilbert space, the spectral theorem) | Part 10, ch. 7–11 |
| FA 13 (unbounded operators, Cayley, Stone) | Part 10, ch. 12–15 |
| FA appendix A (compactness, Tychonoff) | Part 8, ch. 11 |

What courses skip, for the record: a one-semester course in PMA is chapters 1–7 (MIT 18.100B, with
the Weierstrass function and the devil's staircase as an optional last lecture); PMA 10 is widely
replaced by Spivak or Munkres and PMA 11 deferred to a graduate course. A one-year graduate course
in RCA covers "the first nine chapters" (Cornell) or chapters 1–3 and 6–8 as the core (the UT Austin
prelim guide, which notes that chapter 4 "rarely appears" and chapters 17–20 are "mostly not on
the syllabus"); the chapter an MAA reviewer called "a gem", 18, is almost never taught. FA is taught
in order (Harvard 212b: 1 → 1–5 fast → 6 → 7 → 8 → 9 → 10 → 11–12), with chapter 5 cherry-picked,
chapter 9 usually skipped despite being a highlight, and chapter 13 skipped unless the course aims
at quantum mechanics. The series covers all three "usually skipped highlights" (RCA 18, FA 9, FA 13)
because each is a payoff of the thread the series follows.

### 4.2 The counterexample index

| Exhibit | What it breaks | Where in Rudin | Series |
|---|---|---|---|
| Dirichlet's function 1_Q | continuity everywhere; Riemann integrability; it is a double limit of continuous functions | PMA Example 4.27(a) [verified], Example 7.4 [verified], Exercise 6.4 [verified]; Lebesgue-integrable in PMA 11 | Parts 2, 3, 5 |
| x·1_Q | continuous at exactly one point | PMA Example 4.27(b) [verified] | Part 2 |
| Thomae's function | "continuous means drawable"; Riemann-integrable with integral 0 | PMA Exercise 4.18 | Parts 2, 3, 5 |
| sin(1/x), x² sin(1/x) | second-kind discontinuity; a derivative that exists everywhere and is discontinuous | PMA Example 4.27(d) [verified]; ch. 5 | Part 2 |
| e^(−1/x²) | Taylor series converging to the wrong function | PMA Exercise 5.6 | Parts 2, 9 |
| the Cantor set | uncountable yet of length 0; perfect yet nowhere dense | PMA 2.44 [verified], Exercises 3.19, 6.6, 7.14 [verified] | Parts 1, 3, 5 |
| the Cantor function | a continuous increasing function with derivative 0 a.e. that rises by 1; the FTC fails; a singular measure | not constructed in PMA's text (MIT's optional lecture); RCA ch. 7 territory (7.18–7.20) | Parts 1, 3, 5, 6 |
| the fat Cantor set | nowhere dense with positive measure; its indicator is Lebesgue- but not Riemann-integrable | RCA ch. 2 exercises | Parts 5, 8 |
| Lebesgue's space-filling curve | a continuous curve covering a square | PMA Exercise 7.14 [verified] | Part 3 |
| the topologist's sine curve | connected but not path-connected | not in Rudin (Munkres §24) | Part 1 |
| Rudin's nowhere-differentiable function | "continuous functions are differentiable somewhere" | PMA 7.18 [verified] (the sawtooth series, not Weierstrass's cosine series) | Part 3 |
| the Koch curve | a continuous curve with no length | not in Rudin | Part 3 |
| sin(nx); the bumps x²/(x² + (1 − nx)²) | bounded families with no convergent subsequence; pointwise without uniform | PMA Examples 7.20, 7.21 [verified] | Parts 1, 3 |
| the escaping bumps (sliding, tall, wide) and the typewriter | Fatou's strict inequality; L¹ convergence without a.e. convergence | RCA ch. 1 exercises; Tao's zoo | Parts 3, 5, 8 |
| the Vitali set | that every set could have a length | RCA 2.22 (the construction is the proof) | Part 5 (schematic) |
| Fubini's counterexample (x² − y²)/(x² + y²)² | interchanging integrals without absolute integrability | RCA ch. 8 exercises | Part 5 |
| the incomplete (C[0, 1], ‖·‖₁) | that continuous functions suffice | RCA 3 (Riesz–Fischer is the fix) | Part 6 |
| the unit ball of ℓ², e_n | "closed and bounded means compact"; weak vs norm convergence | PMA 11; FA 1.22 and ch. 3 | Parts 1, 3, 8 |
| the Dirichlet kernel; the divergent Fourier series | pointwise convergence for continuous f | PMA 8.13 [verified]; RCA 5.11 | Parts 3, 8 |
| L^p for 0 < p < 1 | that every TVS has functionals | FA 1.47 | Part 8 |
| c_0 inside ℓ^∞ | that projections exist | FA 5.19 | Part 8 |
| the Volterra operator | that ‖T‖ bounds the spectrum tightly (spectrum {0}, norm 2/π) | standard; FA ch. 10 | Part 10 |
| the shift on ℓ² | "the spectrum is the eigenvalues" (spectrum a disk; no eigenvalues for the forward shift) | FA ch. 12 exercises; RCA 17.21 (Beurling) | Part 10 |
| the multiplication operator | an operator with spectrum [0, 1] and no eigenvectors | FA ch. 12–13 | Part 10 |
| i d/dx with twisted boundary conditions | "symmetric means self-adjoint"; the spectrum depends on the domain | FA ch. 13 | Part 10 |

### 4.3 Visual sources consulted (and what each contributed)

* Terence Tao, *Compactness and compactification* (compactness as "the next best thing to
  finiteness") and the 245B notes (Hilbert spaces, L^p, Hahn–Banach, Baire and its consequences, the
  strong and weak topologies): the narration's framing for Parts 1, 6, 8. Tao's multiple-choice
  quiz on modes of convergence names the bump zoo the dashboard uses.
* Thurston, *On proof and progress in mathematics*: the seven conceptions of the derivative (Part 2).
* Pugh, *Real Mathematical Analysis*: picture proofs of MCT, DCT and Fubini via Cavalieri; the best
  diagram source for Parts 1–3.
* Bressoud, *A Radical Approach to Lebesgue's Theory of Integration*: the historical route from
  Riemann's definition to Lebesgue's, the spine of Part 5's hook.
* Körner, *Fourier Analysis*: du Bois-Reymond's example and the Dirichlet kernel (Parts 3, 8).
* Needham, *Visual Complex Analysis*: the amplitwist and the picture proof of Cauchy's theorem
  (Part 7).
* Tao, *An Introduction to Measure Theory*: Littlewood's three principles as guiding intuition
  (Part 5).
* Existing animations checked so the series' versions improve on them rather than repeat them:
  Conroy's Weierstrass zoom (UW), the UCI Cantor-set animations, the Innsbruck bisection applet,
  the GeoGebra ε–δ game and p-norm balls, Falstad's Fourier applet (Gibbs), David Bau's conformal
  viewer and Arnold's complex-function gallery, Axiom Academy's interactive lessons (rearrangement,
  uniform convergence, Darboux sums, Baire, contour deformation), the Wikipedia Gibbs animation,
  and Max Cooper's *Aleph 2* (the diagonal argument).
* No published animation was found for: Arzelà–Ascoli's diagonal over a dense set, the
  frozen-Jacobian Newton iteration behind the inverse function theorem, Paley–Wiener's "support
  width equals growth rate", the approximate eigenvectors of the multiplication operator, and the
  open mapping theorem's geometric-series correction. Those are the series' original storyboards.

### 4.4 Prior art to cite, and the gap the series fills

3Blue1Brown has covered pieces of Season 1 from other angles: *Hilbert's Curve* (space-filling
curves), *Taylor series* (which omits the remainder term, which Part 2 supplies), *Limits,
L'Hôpital's rule and ε-δ definitions* (Essence of Calculus 7), *Newton's fractal* (the contraction
behind Part 4), *But what is a convolution?* (the sliding window of Parts 3 and 9), *But what is a
Fourier series?* and *But what is the Fourier transform?* (Parts 3 and 9), *The more general
uncertainty principle* (Part 9's card), *Why is pi here? And why is it squared?* (the Basel problem,
which Part 3 proves by Parseval instead), *Fractals are typically not self-similar* (the Cantor
set's dimension). Mathologer's *The best A − A ≠ 0 paradox* does the rearrangement theorem; PBS
Infinite Series did *The Devil's Staircase*; Vsauce and Veritasium did Banach–Tarski and the axiom
of choice; The Bright Side of Mathematics has whiteboard-style playlists on measure theory and
functional analysis. There is no animated, derive-everything treatment of measure theory, L^p and
Hilbert spaces, the Banach-space theorems, distributions, or spectral theory anywhere: Seasons 2 and
3 are open territory, and the series' READMEs will say so and cite the above.

### 4.5 Companion references

Abbott, *Understanding Analysis* (each chapter opens on a historical crisis; projects on Thomae,
Volterra, the Cantor function); Pugh (pictures); Tao, *Analysis I/II* (the number systems built
from scratch, careful quantifier logic); Bergman's *Supplements to Rudin* (errata and the examples
students find hardest); Folland, *Real Analysis* (the Carathéodory route where Rudin uses Riesz);
Stein & Shakarchi (four volumes; the most visual graduate set: Dirichlet and Fejér kernels, Gibbs,
the Cantor–Lebesgue function, the Vitali set, Hausdorff dimension); Royden & Fitzpatrick (concrete
before abstract); Brezis (Banach and Hilbert spaces aimed at PDE, with worked solutions); Conway
(operator theory and the spectral theorem); Reed & Simon I (why unbounded operators and
self-adjointness matter in quantum mechanics); Kreyszig (the most elementary functional analysis,
for an audience-level sanity check); Lax (historically rich); Gelbaum & Olmsted, *Counterexamples
in Analysis* (the museum's catalog); Katznelson (the Dirichlet-kernel divergence and Fourier
transforms); Munkres (the topologist's sine curve).

---

## 5. Production plan (how this maps onto the repo)

### 5.1 Layout

One folder per part, in the repo's convention, with a series folder for what is shared:

```
videos/analysis/                 the series hub: this PLAN.md, later SERIES.md (ledger, color legend, the
                                 cross-part dependency table, the counterexample index)
videos/analysis1/ … analysis10/  one video each: manifest.py, sNN_*.py, compute.py, common.py, README.md, SCRIPT.md
explainer/analysis/              the shared instruments (section 2.2) and math helpers:
  epsdelta.py                    the ε–δ game board (largest working δ by bisection; quantifier-order variants)
  dashboard.py                   the convergence dashboard (five lenses, verdict lights)
  camera.py                      the function-as-a-point camera (coefficient projections, norm balls, trails)
  dictionary.py                  the R^n ↔ function-space two-column cards
  museum.py                      counterexample cards (name, year, what it breaks, Rudin reference) and exhibits
  proofmap.py                    the step flowchart for long proofs
  ledger.py, timeline.py         the series' recap table and the history strip
  fourier.py                     coefficients, Dirichlet/Fejér kernels, Lebesgue constants, Gibbs, Poisson summation
  sets.py                        Cantor sets (standard and fat), the Cantor function, outer-measure covers, Vitali orbit
  spaces.py                      ℓ^p balls, Gram–Schmidt in L², projections, extreme-point tests
  operators.py                   discretized operators (shift, Volterra, multiplication, d/dx with boundary
                                 conditions, Sturm–Liouville), spectra and pseudospectra, functional calculus
  distributions.py               mollifiers, distributional derivatives tested against bumps, principal values
  conformal.py                   Schwarz–Christoffel maps, winding numbers, domain coloring (reusing videos/riemann's)
```

`style.py` gets one block, `# Analysis (videos/analysis1-10)`, with the legend of section 2.1.
`tts.py`'s lexicon gets the series' names and symbols (section 5.4). Everything else (build,
publish, export_script, check_narration, contact_sheet, score_voice) is used unchanged.

### 5.2 Cross-part reuse

| Reused | From | In |
|---|---|---|
| the phase-as-hue colormap and the phase wheel | videos/quantum/colormap.py | Parts 7, 9, 10 |
| the split-operator Schrödinger solver | videos/quantum/compute.py | Part 10 (Stone's theorem, the quantum closure) |
| the hero Brownian path | videos/stochastic (.cache) | Part 3's cameo (nowhere differentiable) |
| domain coloring and the prime counts | videos/riemann/compute.py | Parts 7 (colorings), 9 (the prime number theorem chapter) |
| the "tank", "part card", `label`/`note`/`boxed` helpers | videos/stochastic/common.py | promoted into explainer/analysis as the series' common.py |

### 5.3 Computation and checks

Each part's `compute.py` follows the repo's pattern: named items, cached as `.npz` in
`.cache/analysisN/`, with an assertion for every number the narration quotes. The expected cost is
small next to the physics videos (minutes, not hours), with four exceptions worth planning:
Lebesgue constants to n = 10⁶ (exact quadrature of \|D_n\|; ~10 min), the Weierstrass function at 20
zoom levels (cheap but memory-heavy at the deepest levels; decimate as stochastic's `decimate`
does), the Schwarz–Christoffel map (use `scipy` plus a hand-written parameter solve, or vendor
`pySCToolbox`; verify conformality numerically), and the pseudospectra of the 2,000 × 2,000 shift
section (dense SVDs on a grid of λ; ~5 min).

Items that cannot be computed are exactly two, and both are labeled schematics: the Vitali set's
choice of representatives (the orbit itself is computed) and the uncountable almost-disjoint family
in Part 8's uncomplemented-subspace chapter (drawn as a tree).

### 5.4 Narration and pronunciation

The lexicon needs entries before the first render, because the Whisper listen test will otherwise
flag them in every part: Dedekind, Cauchy, Weierstrass, Bolzano, Heine–Borel, Darboux, L'Hôpital,
Stieltjes, Thomae, Dini, Arzelà, Ascoli, Fejér, Dirichlet, du Bois-Reymond, Lebesgue, Borel,
Carathéodory, Vitali, Lusin, Egorov, Fubini, Tonelli, Radon–Nikodym, Hölder, Minkowski, Riesz,
Fischer, Fréchet, Banach, Steinhaus, Hahn, Alaoglu, Krein, Milman, Kakutani, Grothendieck, Goursat,
Morera, Liouville, Runge, Mittag-Leffler, Montel, Phragmén–Lindelöf, Blaschke, Müntz–Szász,
Mergelyan, Beurling, Schwartz, Sobolev, Paley, Malgrange, Ehrenpreis, Tauberian, Gelfand, Mazur,
Naimark, Gleason, Kahane, Żelazko, Lomonosov, Fuglede, Putnam, Cayley, Hille, Yosida, Stone.
Symbols read aloud: ℓ^p ("little ell p"), L^p ("L p"), σ-algebra ("sigma algebra"), lim sup ("lim
soup"), a.e. ("almost everywhere"), C_c ("C sub c"), D′ ("D prime"), S′ ("S prime"), ⟨x, y⟩ ("the
inner product of x and y"), ∫ f dμ ("the integral of f d mu"), T* ("T star"), B(H) ("B of H").

### 5.5 Order of work and milestones

The parts are built in order, because each reuses the previous one's instruments and the ledger.
Per part, the repo's workflow: outline (this plan's table, refined into the README's outline) →
`compute.py` with checks → scenes with narration → `--dry_run` → 480p preview and contact sheets →
listen test → 1080p → publish → README with chapters and fact-check notes → SCRIPT.md.

| Milestone | Deliverable |
|---|---|
| M0 | `explainer/analysis/` instruments 1–9 working in a demo scene; the legend in `style.py`; the lexicon |
| M1 | Part 1 published (also validates the game board, the museum, the zoom and the ledger) |
| M2 | Parts 2–3 (the dashboard, the camera and the dictionary get their first real use) |
| M3 | Part 4 (short) and Part 5 (the measure instruments) |
| M4 | Parts 6–7 (Hilbert geometry; conformal maps and domain coloring) |
| M5 | Parts 8–9 (operators, weak topologies, distributions) |
| M6 | Part 10, then the series README with the full ledger, the counterexample index and the playlist order |

Each part is about the size of the repo's quantum2 (20 scenes, ~5,000 lines of scene code, a
`compute.py` of ~1,000 lines); the series is ten of those.

### 5.6 Quality bar, per part

As for every repo video, plus three series-specific checks:

* **Every proof is complete or labeled.** `export_script.py` output is read against the chapter
  table; each theorem in the table is either proved on screen, or its chapter is labeled `tour`,
  or the abbreviated step is labeled `ε-bookkeeping, routine`. No third state.
* **Every counterexample is computed or labeled `schematic`.** The museum index in SERIES.md lists
  which.
* **Every Rudin reference is checked against the books** (3rd editions of PMA and RCA, 2nd of FA)
  when the script is written; the plan's numbers are a starting point.

---

## 6. Decisions for you

The plan is complete under the choices below. Each is a place where a different choice changes the
series' shape, so they are listed rather than silently taken.

1. **Ten parts, or fewer.** The recommended cut is the ten above. The lean alternative is eight:
   fold Part 4 into the end of Part 3 (keep the contraction principle, the inverse function
   theorem and Picard; drop the rank theorem, mixed partials and the forms tour), and cut Part 7 to
   its chapters 1–6 and 9–10 appended to Part 8's start (the complex analysis Part 10 needs, no
   tours). That saves about 100 minutes and loses the Riemann mapping computation's context, the
   forms tour and the complex tours.
2. **Differential forms.** As planned, PMA 10 is a six-minute labeled tour. The alternative is a
   full optional Part 4b (~40 min: change of variables proved, forms, Stokes for chains, the
   Poincaré lemma), which this repo's relativity videos partly cover from the physics side.
3. **Grandpa Rudin's chapter 1 generality.** As planned, topological vector spaces get one chapter
   (Part 8, chapter 3) and are used honestly in Part 9. The alternative is to stay in Banach and
   Fréchet spaces throughout and state the test-function topology without the TVS language; that
   is what most courses do, and it would shorten Part 8 by five minutes at the cost of some rigor
   in Part 9.
4. **The quantum closure.** Part 10's chapters 15–16 reuse the quantum videos' solver and recall
   their chapters. If the series should stand entirely alone, those two chapters become one
   shorter chapter that does not depend on having seen the quantum videos.
5. **Series title and part titles.** The working titles are in section 0; they follow the repo's
   pattern ("X, Visualized: A, B and Why C"). Happy to retitle.

Everything else (the thesis, the Fourier thread, the ledger, the instruments, the chapter tables)
is the recommended design and is ready to be turned into Part 1's outline and `compute.py`.
