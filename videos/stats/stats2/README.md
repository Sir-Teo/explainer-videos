# Statistics, Built — Part 2: Chance, Counted

Part 2 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. Part 1 ended with the discovery that every
summary of a sample is random. This part builds the language for reasoning about chance exactly. It begins in 1654,
with an interrupted dice game in the letters of Pascal and Fermat, and ends with the old argument about what a
probability is. Between them:
- counting, and its traps;
- Bertrand's paradox and Kolmogorov's axioms;
- conditioning, Bayes' theorem, a courtroom and three doors;
- independence;
- random variables, expectation, variance and generating functions.

**Built in this part:** `explainer.stats.prob`, an exact probability engine on finite spaces. A `Dist` is a finite
probability space whose outcomes carry exact rational probabilities. Its operations are the ones the part
introduces:
- `P`, `given` (conditioning) and `map` (a random variable's distribution);
- `E`, `var` and `moment`;
- independent products `*` / `**`, and sums `+` / `iid_sum`, by convolution;
- two-stage experiments with `then`, which is the multiplication rule as a tree;
- `pgf`.

Every exact answer on screen is checked against a seeded simulation. The screening example uses the World's new
`screening` block (`World.screening`, about 1% prevalence, two tests independent given the condition).

## Build it

From the repo root, after the one-time setup in the [top-level README](../../README.md):

```bash
python -m videos.stats.stats2.compute          # once: every computed item (seconds; cached in .cache/stats2)
python tools/build.py stats2 -q l              # fast 480p preview
python tools/build.py stats2                   # 1080p30 -> renders/stats2.mp4
python tools/qa_scene.py stats2 Monty          # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats2 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | The problem of points | Pascal and Fermat, 1654. Pacioli's split by the past (1494) and Tartaglia's objection. Fermat completes the future: 4 equally likely continuations. Pascal's backward recursion, the table of values for a game to three, and expectation. | A's share 3/4 → 48 of 64 pistoles; 10,000 simulated finishes 0.7515 |
| 1 | Before the axioms | Cardano's circuit and the classical definition. Galileo's three dice: 25 vs 27 orderings. De Méré's two bets, exactly and simulated. Huygens' *value of a chance* (1657). | 671/1296 = 0.5177 vs 0.4914; a double six needs 25 throws |
| 2 | Counting | The multiplication principle; n!, and 52! with its 68 digits. C(n, k) derived on screen. Pascal's triangle and the general problem of points. Stars and bars: 56 unordered rolls of three dice, *not* equally likely (Bose–Einstein aside). | C(49, 6) = 13,983,816 |
| 3 | Bertrand's paradox | Three ways to pick a random chord: 1/3, 1/2, 1/4, each simulated 3,000 times. The chords' midpoints form three different clouds, three measures on the same set. Jaynes's invariance argument (1973). | 0.343, 0.495, 0.242 |
| 4 | Kolmogorov's axioms | Probability as area (1933). Complement, monotonicity, inclusion–exclusion and the union bound derived. De Méré's bet by inclusion–exclusion, with Bonferroni's alternating partial sums. Montmort's hat-check problem → 1/e (exact for n ≤ 8 by enumeration; 10,000 shuffles). Continuity. | 9 of 24 derangements of 4; 1/e = 0.3679, simulated 0.3701 |
| 5 | Conditioning | The two-dice grid sliced by "the sum is 8". The definition as renormalized area. The multiplication rule (two aces 1/221). Total probability on a tree of three urns, and its reversal. The two-child problem. | P(six \| sum 8) = 2/5; P(BB \| ≥ 1 boy) = 1/3, simulated 0.334 |
| 6 | Bayes' theorem | Bayes (1763) and Laplace (1774). The World's screening test as an icon array and a natural-frequency tree (Gigerenzer & Hoffrage 1995). Odds form: prior odds × likelihood ratio 18. The posterior by age group. A second test. | P(condition \| +) = 0.150 exactly, 0.151 in the World; two positives 0.760 (World 0.758) |
| 7 | The prosecutor's fallacy | *R v Clark*, from the published record. Squaring 1/8,543 assumes independence (Hill's dependence factor 5–10). P(E \| innocent) ≠ P(innocent \| E). Double SIDS vs double murder in odds form (Hill 2004: 4.5–9 : 1). The RSS statement (2001) and the quashed convictions (2003). | 8,543² = 72,982,849 |
| 8 | Monty Hall | Selvin (1975) and vos Savant (1990). The tree, renormalized: 2/3. 3,000 simulated games. Four host protocols computed exactly: 2/3, 1/2, 0 and 1/(1+q). The data include how they were shown. | switching wins 0.658 in simulation |
| 9 | Independence | The product rule; independent is not disjoint. Bernstein's tetrahedron (rotating, painted): pairwise but not mutually independent. The World's two tests: dependent overall, independent given the condition. | P(B \| A) = 0.18 vs P(B) = 0.06 overall; 0.90 vs 0.90 given the condition |
| 10 | Random variables | The sum of two dice as a function on Ω, sorted into its distribution (the push-forward). The CDF and its properties. Discrete, continuous and mixed; then the Cantor distribution: continuous, no density (devil's staircase, five levels, 20,000 draws). | E X = 1/2, Var X = 1/8; simulated 0.5004, 0.1259 |
| 11 | Expectation | The balance point; LOTUS. The layer-cake formula on a die. Linearity without independence. Matches in a shuffle (E = Var = 1, exact for n ≤ 8; 10,000 decks against e⁻¹/k!). Birthdays (23 people). The coupon collector, n H_n. | P₂₃ = 0.507 (sim 0.505); 50 stickers: 225.0 packs (sim 224.0) |
| 12 | Variance, and a game worth infinity | Var X = E X² − μ², derived. Variances of sums and σ/√n. The St. Petersburg game (N. Bernoulli 1713, D. Bernoulli 1738): infinite expectation; 2²⁰ simulated games, the running mean tracking log₂ n (Feller 1945). Log utility: a fair price of 4 ducats. | Var(die) = 35/12; Var(10 dice) = 175/6 |
| 13 | Generating functions | G(s) = E sˣ. Sums become products: the convolution grid. Moments by differentiation. Sicherman's dice by factoring (Gardner 1978), checked by the engine. | G'(1) = 7/2, G''(1) = 35/3 |
| 14 | What probability means | Frequency (Venn, von Mises), logic (Keynes), belief (Ramsey, de Finetti). The Dutch book. Cox's theorem (1946; Halpern 1999). Frequentist and Bayesian, and how the series uses both. | — |
| 15 | Outro | Fifteen-line recap, where the ideas return, problems, references, the Transcript, and Part 3's question. | — |

## Sources

- **The problem of points.** The Pascal–Fermat correspondence of 1654 (Pascal's letter of 29 July 1654 states the
  game to three at 32 pistoles a side). Pacioli, *Summa de arithmetica* (1494). Tartaglia, *General trattato*
  (1556). Huygens, *De ratiociniis in ludo aleae* (1657), Proposition III. Background: A. Hald, *A History of
  Probability and Statistics and Their Applications before 1750* (1990).
- **Galileo,** *Sopra le scoperte dei dadi* (c. 1620). **Cardano,** *Liber de ludo aleae* (written c. 1564, printed
  1663).
- **Bertrand,** *Calcul des probabilités* (1889). **Jaynes,** "The well-posed problem", *Foundations of Physics* 3
  (1973).
- **Kolmogorov,** *Grundbegriffe der Wahrscheinlichkeitsrechnung* (1933). **Montmort,** *Essay d'analyse sur les jeux
  de hazard* (1708).
- **Bayes,** "An essay towards solving a problem in the doctrine of chances", *Phil. Trans.* (1763). **Gigerenzer &
  Hoffrage,** "How to improve Bayesian reasoning without instruction: frequency formats", *Psychological Review*
  (1995).
- ***R v Clark*.** Conviction November 1999; first appeal dismissed 2000; convictions quashed on a second appeal,
  January 2003. Royal Statistical Society, statement of 23 October 2001. R. Hill, "Multiple sudden infant deaths —
  coincidence or beyond coincidence?", *Paediatric and Perinatal Epidemiology* 18 (2004), 320–326: a dependence
  factor of 5–10 for a second SIDS, and double SIDS : double homicide of 4.5–9 : 1. The chapter's comparison uses
  Hill's ratio as published and is tagged *schematic*.
- **Monty Hall.** S. Selvin, letters to *The American Statistician* 29 (1975). M. vos Savant, *Parade* (1990) and
  *The Power of Logical Thinking* (1996), for the letters. P. Hoffman, *The Man Who Loved Only Numbers* (1998), for
  Erdős.
- **St. Petersburg.** D. Bernoulli, "Specimen theoriae novae de mensura sortis" (1738). W. Feller, "Note on the law
  of large numbers and 'fair' games", *Ann. Math. Statist.* 16 (1945).
- **Sicherman's dice.** M. Gardner, "Mathematical Games", *Scientific American*, February 1978.
- **Interpretations.** J. Venn, *The Logic of Chance* (1866); R. von Mises, *Wahrscheinlichkeit, Statistik und
  Wahrheit* (1928); J. M. Keynes, *A Treatise on Probability* (1921); F. P. Ramsey, "Truth and probability" (1926);
  B. de Finetti, "La prévision" (1937); R. T. Cox, "Probability, frequency and reasonable expectation", *Am. J.
  Phys.* (1946); J. Y. Halpern, "A counterexample to theorems of Cox and Fine", *JAIR* (1999).
- **Textbooks.** Feller, vol. 1 (3rd ed., 1968). Blitzstein & Hwang (2nd ed., 2019). Ross, *A First Course in
  Probability* (10th ed., 2019). Grimmett & Stirzaker (4th ed., 2020). I. Hacking, *An Introduction to Probability
  and Inductive Logic* (2001).

## Problems and solutions

**1. Points, both ways.** A needs 2 more points and B needs 3, fair rounds.

*Solution.* **Fermat.** At most 2 + 3 − 1 = 4 more rounds settle it; imagine all four played. A wins the match
exactly when A wins at least 2 of the 4, so P(A) = [C(4,2) + C(4,3) + C(4,4)] / 2⁴ = (6 + 4 + 1)/16 = 11/16.

**Pascal.** Let V(a, b) be A's chance when A needs a and B needs b. Then V(0, b) = 1, V(a, 0) = 0, and
V(a, b) = ½ V(a−1, b) + ½ V(a, b−1). This gives:
- V(1,1) = ½ and V(2,2) = ½;
- V(1,2) = ¾ and V(1,3) = ⅞;
- V(2,3) = ½(⅞ + ½) = 11/16.

**2. Inclusion–exclusion and Bonferroni.**

*Solution.* Apply the two-event rule to (A ∪ B) ∪ C:

P(A∪B∪C) = P(A∪B) + P(C) − P((A∩C) ∪ (B∩C)).

Expand the first term and the last one by the two-event rule again; the last uses (A∩C) ∩ (B∩C) = A∩B∩C. The
result is

P(A∪B∪C) = ΣP(A) − ΣP(A∩B) + P(A∩B∩C).

For the lower bound, let N be the number of the events Aᵢ that occur. Then 1{N ≥ 1} ≥ N − C(N, 2) for every
integer N ≥ 0:
- for N = 0 both sides are 0;
- for N ≥ 1 the inequality is (N − 1)(N − 2) ≥ 0.

Take expectations. E N = Σ P(Aᵢ) and E C(N, 2) = Σ_{i<j} P(Aᵢ ∩ Aⱼ), both by indicators and linearity.

**3. A rarer condition.** Sensitivity = specificity = 0.99; prevalence 1/1,000.

*Solution.*
- **One positive.** Prior odds 1 : 999; likelihood ratio 0.99/0.01 = 99. Posterior odds 99/999, so
  P = 99/1,098 ≈ 0.090.
- **Two positives** that err independently given the condition: odds 99²/999 = 9,801/999 ≈ 9.81, so
  P = 9,801/10,800 ≈ 0.908.

Even a 99%-accurate test mostly raises false alarms for a condition this rare.

**4. Monty Hall with n doors.**

*Solution.* Whatever your pick, the host can always open n − 2 goat doors, so his action has the same probability
whatever is behind your door. Your door therefore keeps probability 1/n. When your pick is a goat (probability
(n − 1)/n), the car must be behind the single other closed door. Switching wins with probability (n − 1)/n.

**5. Different faces in n rolls.**

*Solution.* Let I_f indicate that face f appears at least once. Then E I_f = 1 − (5/6)ⁿ, and by linearity
E[#faces] = 6(1 − (5/6)ⁿ). This exceeds 5 iff (5/6)ⁿ < 1/6, that is n > ln 6 / ln 1.2 ≈ 9.83. So n = 10, which
gives 5.03; at n = 9 it is 4.84.

**6. A finite casino.** The prize is min(2ᵏ, 2²⁰) when the first head is on toss k.

*Solution.*

E = Σ_{k=1}^{20} 2ᵏ · 2⁻ᵏ + Σ_{k≥21} 2²⁰ · 2⁻ᵏ = 20 + 2²⁰ · 2⁻²⁰ = 21.

A bankroll of about a million ducats makes the "infinite" game worth 21 ducats; each doubling of the bankroll adds
only one more.

## Where it comes back

| Idea | Returns in |
|---|---|
| expectation and linearity | 6 (laws of averages), 9 (estimation), 22 (likelihood) |
| conditioning and Bayes | 15 (first Bayes), 26 (Bayesian data analysis), 33 (false discovery rate) |
| conditional independence | 5 (joint distributions), 36 (causal graphs) |
| the likelihood (Monty Hall's protocol) | 9, 22; the design of data collection in 18 |
| generating functions | 3 (named distributions, mgfs), 6 (characteristic functions and the CLT) |
| the union bound | 33, 51, 54 |
| measure, singular distributions | 43 |
| what probability means | 15, 26 |
