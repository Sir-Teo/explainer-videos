# Statistics, Built — Part 10: Significance

Part 10 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the last part of Stage I, Bachelor's: Foundations. Parts 8 and 9 built
estimators and their sampling distributions. This part asks when a pattern is too strong to be chance.

It opens with two stories. In 1710 John Arbuthnot found more boys than girls christened in London in each of 82
years: (1/2)⁸² ≈ 2.1 × 10⁻²⁵. Then there is Fisher's lady tasting tea (1935): with eight cups, a perfect score by
guessing has probability 1/70. From there the part covers:
- Fisher's logic, and which null was really rejected (a 51.6% coin makes 82 straight wins a 98% event; Nicolaus
  Bernoulli, 1713);
- exact tests from randomization: the tea, Fisher's exact test, and Darwin's *Zea mays* sign flips (863 of 32,768);
- the p-value, uniform under H₀, and its distribution under alternatives;
- Neyman and Pearson's two errors and the Neyman–Pearson lemma, as a knapsack over all 2,048 rejection regions of a
  dice problem;
- the likelihood ratio test, Wilks' theorem, and the Wald, score and LR trinity;
- the everyday tests, and Student vs Welch;
- Pearson's χ², Mendel's peas and Fisher's "too good to be true", and a χ² association in the World's clinic that is
  confounded;
- power, sample size and Gelman & Carlin's type S and M errors;
- the peeking problem;
- what p-values are not, ending with the ASA statement (2016);
- many tests and Bonferroni.

Every number on screen is computed in [`compute.py`](compute.py). The Museum supplies:
- Arbuthnot's christenings (`museum.ARB_*`);
- Darwin's maize (`museum.DARWIN_ZEA`);
- Mendel's counts (`museum.MENDEL_*`);
- Student's sleep data (`museum.SLEEP_*`).

Heights, incomes and the clinic come from the World (seed 1662). Everything else is a seeded simulation or exact.

**Built in this part:**
- **The permutation machine** (`PermutationMachine` in [`explainer/stats/viz.py`](../../../explainer/stats/viz.py)):
  tokens dealt into two rows, the shuffled statistic stacking into the null distribution.
- **`statkit.tests`** ([`explainer/stats/kit/tests.py`](../../../explainer/stats/kit/tests.py)): z, t, paired,
  Welch, permutation (exact or Monte Carlo), Fisher's sign flips, the sign test, Fisher's exact test, Pearson's χ²,
  the LRT, Bonferroni, power and sample size. Every one is checked against SciPy in
  `tests/test_stats_kit_tests.py`, which also reproduces Fisher's 863/32,768.

The Coverage Board gains five rows. Size rows carry nominal 5%, with R = 10,000 replications; the permutation row has
2,000.

| Method | Setting | Achieved size | Verdict |
|---|---|---|---|
| Student's two-sample t | men's heights, n = 10, 10 | 5.04% | kept |
| Student's two-sample t | σ₁ ≈ 2.7σ₂, n = 10, 40 | 23.63% | broken |
| Welch's t | σ₁ ≈ 2.7σ₂, n = 10, 40 | 5.15% | kept |
| t-test, peeking after every observation | men's heights, n = 10 … 100 | 29.11% | broken |
| permutation test | incomes, n = 8, 8 | 4.85% | kept |

## Build it

```bash
python -m videos.stats.stats10.compute         # once: every computed item (about 20 s; cached in .cache/stats10)
python tools/build.py stats10 -q l             # fast 480p preview
python tools/build.py stats10                  # 1080p30 -> renders/stats10.mp4
python tools/qa_scene.py stats10 Lemma         # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats10 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | More boys than girls, and a cup of tea | Arbuthnot's paper and his 82 years plotted; the tea; objectives. | male share 0.503–0.536; 484,382 boys, 453,841 girls; p = 2.07 × 10⁻²⁵; 1/70 |
| 1 | Fisher's logic | Null, statistic, p; the sign test; Fisher's disjunction; which null was rejected; 's Gravesande and Bernoulli; where 5% came from. | P(T ≥ 15 of 20) = 0.0207; per-year win 0.99975, all 82: 0.98 |
| 2 | Exact tests by design | The tea's hypergeometric null; designs of 6–12 cups and the power of an imperfect taster; Fisher's exact test; Darwin's 15 pairs and all 2¹⁵ sign flips; the permutation machine on the World; randomization as the source of validity. | 1, 16, 36, 16, 1 /70; perfect-score power 0.11, 0.25, 0.51 at q = 0.7, 0.8, 0.9; Darwin p = 0.0263 / 0.0527 (t: 0.0497); regions p = 1,916/3,432 = 0.558 |
| 3 | The p-value | Definition; uniform under H₀ (proof); 20,000 t-tests at δ = 0, 0.3, 0.8; discrete super-uniform p; surprise in bits. | P(p < 0.05) = 0.049, 0.194, 0.819 |
| 4 | Two kinds of error | Neyman & Pearson (1928, 1933); the decision table; sliding the cut; power against n; the two philosophies. | n = 32 (80%), 43 (90%) for δ = 0.5σ |
| 5 | The Neyman–Pearson lemma | Statement; two dice, one loaded; the knapsack; all 2,048 regions and the frontier; the proof; UMP one-sided tests. | best size-1/6 region {10, 11, 12}: power 0.233 |
| 6 | The likelihood ratio test | Λ and W; Wilks (1938) by the quadratic approximation; simulation at n = 3 and 30; Wald, score and LR on the horse kicks; one- vs two-sided. | sizes 3.6%, 5.4%; H₀: λ = 0.5: W = 4.52 (p = 0.034), Wald 3.97 (0.046), score 4.84 (0.028) |
| 7 | The everyday tests | The catalogue; paired vs unpaired sleep data; Behrens–Fisher and Welch; a size grid; advice. | paired t = 4.06, p = 0.0028; unpaired p = 0.079; Student 18.4% / 29.4% at n = 10, 40 |
| 8 | Pearson's χ² | Pearson (1900); the statistic and its df; Mendel's 3:1 and 9:3:3:1; the null by simulation; Fisher (1936); independence in the clinic, and why it is confounded. | X² = 0.263 (p = 0.61), 0.47 (p = 0.93); clinic X² = 9.32, p = 0.0023 |
| 9 | Power and sample size | Power curves; n for 80%; Cohen (1962); type S and M; the winner's curse. | n = 197, 32, 13; at 8% power: 4.8× exaggeration, 8.7% wrong sign |
| 10 | The peeking problem | Running t paths; the false-positive rate against the patience; Wald's SPRT, Armitage et al., group-sequential designs; the Board's Part 10 rows. | 13% (n ≤ 20), 22% (50), 29% (100), 42% (500); every 10th up to 100: 20% |
| 11 | What p-values are not | p ≠ P(H₀ ∣ data) and 1,000 hypotheses; the dance of the p-values; significance ≠ size; absence of evidence; Gelman & Stern; the ASA's six principles. | 36% of significant results false (86% at 1 in 100 real) |
| 12 | Many tests | 1 − 0.95ᵐ; 100 null p-values; Bonferroni by the union bound; the dead salmon; forking paths. | 0.64 at m = 20 → 5.0% with Bonferroni |
| 13 | Outro | Recap, payoffs, problems, references, the Transcript, Part 11's question. | — |

## Sources

- **The founding papers.**
  - J. Arbuthnot, *Phil. Trans.* 27 (1710).
  - K. Pearson, *Phil. Mag.* 50 (1900).
  - R. A. Fisher, *Statistical Methods for Research Workers* (1925); *The Design of Experiments* (1935);
    "Has Mendel's work been rediscovered?", *Ann. Sci.* 1 (1936); *Statistical Methods and Scientific Inference*
    (1956).
  - J. Neyman & E. S. Pearson, *Biometrika* 20A (1928); *Phil. Trans. A* 231 (1933).
  - S. S. Wilks, *Ann. Math. Stat.* 9 (1938).
  - A. Wald, *Trans. AMS* 54 (1943); *Ann. Math. Stat.* 16 (1945).
  - C. R. Rao, *Proc. Camb. Phil. Soc.* 44 (1948).
  - B. L. Welch, *Biometrika* 34 (1947).
- **Tests and designs.**
  - S. Karlin & H. Rubin, *Ann. Math. Stat.* 27 (1956).
  - P. Armitage, C. McPherson & B. Rowe, *JRSS A* 132 (1969).
  - S. Pocock, *Biometrika* 64 (1977); P. O'Brien & T. Fleming, *Biometrics* 35 (1979).
  - S. Holm, *Scand. J. Stat.* 6 (1979); Y. Benjamini & Y. Hochberg, *JRSS B* 57 (1995).
- **Misuse and repair.**
  - J. Cohen, *J. Abnorm. Soc. Psych.* 65 (1962); P. Sedlmeier & G. Gigerenzer, *Psych. Bull.* 105 (1989).
  - J. Ioannidis, *PLoS Med.* 2 (2005); A. Gelman & H. Stern, *Am. Stat.* 60 (2006).
  - G. Cumming, *Persp. Psych. Sci.* 3 (2008); J. Simmons, L. Nelson & U. Simonsohn, *Psych. Sci.* 22 (2011).
  - A. Gelman & J. Carlin, *Persp. Psych. Sci.* 9 (2014); Open Science Collaboration, *Science* 349 (2015).
  - R. Wasserstein & N. Lazar, *Am. Stat.* 70 (2016); S. Greenland, *Am. Stat.* 73 (2019).
  - C. Bennett et al., *J. Serendipitous Unexpected Results* 1 (2010; poster 2009).
  - A. Franklin et al., *Ending the Mendel–Fisher Controversy* (2008).
- **Textbooks and history.**
  - G. Casella & R. Berger, *Statistical Inference* (2nd ed., 2002), ch. 8.
  - E. Lehmann & J. Romano, *Testing Statistical Hypotheses* (4th ed., 2022).
  - D. Salsburg, *The Lady Tasting Tea* (2001); S. Stigler, *The History of Statistics* (1986).

## Problems and solutions

**1. Ten cups.**

*Solution.* With five of each, P(j right) = C(5, j)C(5, 5 − j)/C(10, 5) = C(5, j)²/252.
- Four right: P(≥ 4) = (25 + 1)/252 = 0.103. Not significant: four of five is easy to reach by guessing.
- The smallest possible p is 1/252 = 0.0040, for a perfect score.

**2. The uniform p-value.**

*Solution.* P(p ≤ u) = P(1 − F₀(T) ≤ u) = P(F₀(T) ≥ 1 − u). For continuous F₀, F₀(T) is Uniform(0, 1) (the
probability integral transform: P(F₀(T) ≤ v) = P(T ≤ F₀⁻¹(v)) = v). So P(p ≤ u) = u.

**3. A most powerful Poisson test.**

*Solution.* p₃(x)/p₁(x) = 3ˣe⁻², which increases in x, so the NP test rejects for large x.
- P₁(X ≥ 4) = 0.0190 and P₁(X ≥ 3) = 0.0803, so the best non-randomized test of size at most 0.05 rejects for
  X ≥ 4. It has size 0.019 and power P₃(X ≥ 4) = 0.353.
- For size exactly 0.05, also reject at X = 3 with probability γ = (0.05 − 0.0190)/P₁(X = 3) = 0.506. The power rises
  to 0.353 + 0.506 · 0.224 = 0.466.

**4. The LRT for a proportion.**

*Solution.* W = 2[x log(x/(np₀)) + (n − x) log((n − x)/(n(1 − p₀)))], taking 0 log 0 = 0. For x = n = 82 and
p₀ = ½, W = 2 · 82 log 2 = 113.7. The χ²₁ tail is 1.5 × 10⁻²⁶. That is the same order as the exact two-sided sign
test, 2 · 2⁻⁸² = 4.1 × 10⁻²⁵; Wilks' approximation is poor this far out in the tail.

**5. Sample size.**

*Solution.* For two groups of n, SE(x̄ − ȳ) = σ√(2/n). So n = 2((z₀.₉₇₅ + z₀.₉₀)σ/δ)² = 2(1.960 + 1.282)²/0.16 = 131.3:
132 per group.

**6. Ten tests.**

*Solution.* P(at least one) = 1 − 0.95¹⁰ = 0.401. Testing each at 1 − 0.95^(1/10) = 0.005116 makes it exactly
0.05 for independent tests (Šidák). That is barely larger than Bonferroni's 0.005.

## Where it comes back

| Idea | Returns in |
|---|---|
| tests inverted into intervals | 11, 46 |
| randomization and permutation inference | 13, 16, 35 |
| likelihood ratio, Wald and score tests | 14, 22, 24 |
| χ² tests for tables | 14 |
| power, design, sample size | 13, 35 |
| sequential and anytime-valid testing | 35, 58 |
| multiple testing, FDR, selection | 33, 56 |
| posterior probabilities of hypotheses | 15, 26 |
| the Coverage Board | every part; 65 |
