# Statistics, Built — Part 3: The Family of Distributions

Part 3 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. Part 2 built the language of chance; this
part names the shapes that chance keeps making. It opens with Bortkiewicz's horse kicks (1898), which follow
Poisson's formula, and asks why the same few distributions turn up everywhere. The answer is that they are one
family. Every member is related to the others by a sum, a limit, a transformation or a mixture.

**Built in this part:** the family-tree explorer (`explainer.stats.FamilyTree`), 18 distributions joined by 24
arrows. Each chapter lights the arrows it derives, and the finale walks the whole tree.

**New in the World and the Museum:**
- the World's lake (`World.lake`, about 8,000 fish, for capture–recapture);
- Bortkiewicz's 200 corps-years (`museum.HORSEKICK_*`).

## Build it

From the repo root, after the one-time setup in the [top-level README](../../README.md):

```bash
python -m videos.stats.stats3.compute          # once: every computed item (seconds; cached in .cache/stats3)
python tools/build.py stats3 -q l              # fast 480p preview
python tools/build.py stats3                   # 1080p30 -> renders/stats3.mp4
python tools/qa_scene.py stats3 Tree           # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats3 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | Deaths by horse kick | Bortkiewicz's 200 corps-years against 200 × Poisson(0.61); mean and variance; the dark family tree; objectives. | 109, 65, 22, 3, 1 vs 108.7, 66.3, 20.2, 4.1, 0.7 |
| 1 | Bernoulli to binomial | Lattice paths; the formula from Part 2's counting; mean and variance by indicators; a World poll of 100 adults (how many over 180 cm). | p = 0.1446; 2,000 polls: mean 14.42, variance 12.60 |
| 2 | The law of rare events | Binomial(n, λ/n) → Poisson, derived on screen; total variation as n grows; Le Cam's inequality; the Poisson's mean and variance. | TV 0.174 (n = 4) → 0.0005 (n = 1,000) |
| 3 | Waiting | The geometric; memorylessness shown by rescaling the tail; first-step analysis (Pascal's method) for E T = 1/p; the negative binomial. | simulated mean wait 5.996; P(T > 8 \| T > 5) = 0.578 vs 0.579 |
| 4 | Without replacement | The hypergeometric; capture–recapture on the World's lake; Lincoln–Petersen and Chapman over 2,000 repetitions. | N = 8,107; one estimate 6,452; L–P mean 8,525, Chapman 8,198 |
| 5 | Continuous time | The Poisson process; exponential gaps; the gamma wait; superposition and thinning; the inspection paradox. | wait 10.04 min, gap you land in 20.09 min |
| 6 | The normal, three ways | de Moivre (1733) and Stirling; Gauss (1809); Herschel–Maxwell rotation invariance; ∫e^{−x²/2} = √(2π) in polar coordinates; 68–95–99.7 on the World's men. | 68.24%, 95.41%, 99.73% vs 68.27%, 95.45%, 99.73% |
| 7 | Transformations | The CDF method (−log U); the Jacobian in 1D and nD; Box–Muller (1958) as a square morphing into a bell; the log-normal as a product of 60 factors. | skewness 4.6 → −0.005 after the log |
| 8 | The sampling family | χ² (Helmert 1876, Pearson 1900) and its gamma identity; Student's t (1908); F (Fisher 1924, Snedecor 1934); the lighthouse Cauchy and its running mean. | χ²₃ simulated mean 2.99, variance 6.23 |
| 9 | Order statistics | The density of the k-th; uniform order statistics are beta; the sample median; the German tank problem (Ruggles & Brodie 1947). | 8 serials, N = 300: estimate 270; 5,000 repetitions average 300.0 |
| 10 | Heavy tails | Pareto and the log–log line; Zipf on the World's 200 towns; the 80/20 rule against the World's incomes; log–log least squares vs maximum likelihood (Clauset, Shalizi & Newman 2009). | slope −1.05; top 20% earn 43.8%; LS 2.24 ± 0.14 vs MLE 2.50 ± 0.07 (true 2.5) |
| 11 | Generating functions | MGFs and moments; the normal's by completing the square; Poisson sums; sums of exponentials are gamma; characteristic functions. | — |
| 12 | Mixtures and hierarchies | Beta-binomial overdispersion; the law of total variance (4 + 16 = 20); gamma–Poisson = negative binomial; a normal scale mixture is t. | variance 20.0 vs 4.9; NB mean 3.04, variance 7.71 |
| 13 | Exponential families | h(x) exp(ηT − A(η)); Bernoulli, Poisson, normal, exponential, binomial; A′ = E T, A″ = Var T; what the form buys (Parts 9, 15, 22, 24). | A′ checked numerically |
| 14 | The family tree | All 24 arrows walked and lit; Leemis & McQueston (2008). | — |
| 15 | Outro | Recap, where it comes back, problems, references, the Transcript, Part 4's question. | — |

## Sources

- **Horse kicks.** L. von Bortkiewicz, *Das Gesetz der kleinen Zahlen* (1898). The 200 corps-years as usually
  quoted come from M. P. Quine & E. Seneta, "Bortkiewicz's data and the law of small numbers", *Int. Statist. Rev.*
  55 (1987). S. D. Poisson, *Recherches sur la probabilité des jugements* (1837).
- **Rare events.** L. Le Cam, "An approximation theorem for the Poisson binomial distribution", *Pacific J. Math.*
  10 (1960).
- **Capture–recapture.** C. G. J. Petersen (1896); F. C. Lincoln (1930); D. G. Chapman (1951). Laplace's 1802
  estimate of the population of France.
- **The normal.** A. de Moivre (1733), later *The Doctrine of Chances* (1738, 1756). C. F. Gauss, *Theoria motus*
  (1809). J. Herschel, *Edinburgh Review* (1850). J. C. Maxwell (1860). Background: S. Stigler, *The History of
  Statistics* (1986).
- **Transformations.** G. E. P. Box & M. E. Muller, "A note on the generation of random normal deviates", *Ann. Math.
  Statist.* 29 (1958).
- **The sampling family.** F. R. Helmert (1876). K. Pearson (1900). "Student", "The probable error of a mean",
  *Biometrika* 6 (1908). R. A. Fisher (1924). G. W. Snedecor (1934).
- **Order statistics.** R. Ruggles & H. Brodie, "An empirical approach to economic intelligence in World War II",
  *JASA* 42 (1947).
- **Heavy tails.** F. Auerbach (1913). G. K. Zipf, *Human Behavior and the Principle of Least Effort* (1949).
  A. Clauset, C. R. Shalizi & M. E. J. Newman, "Power-law distributions in empirical data", *SIAM Review* 51 (2009).
- **Exponential families.** G. Darmois (1935); B. O. Koopman (1936); E. J. G. Pitman (1936).
- **The tree.** L. M. Leemis & J. T. McQueston, "Univariate distribution relationships", *The American Statistician*
  62 (2008).
- **Textbooks.**
  - J. Blitzstein & J. Hwang, *Introduction to Probability* (2nd ed., 2019).
  - G. Casella & R. Berger, *Statistical Inference* (2nd ed., 2002).
  - N. L. Johnson, S. Kotz & N. Balakrishnan, *Univariate Discrete* and *Continuous Univariate Distributions*.
  - W. Feller, vols. 1–2.

## Problems and solutions

**1. Splitting a Poisson sum.** X ~ Poisson(a) and Y ~ Poisson(b), independent.

*Solution.* Use P(X + Y = n) = e^{−(a+b)}(a + b)ⁿ/n!, from chapter 11:

P(X = k | X + Y = n) = [e^{−a}aᵏ/k! · e^{−b}b^{n−k}/(n−k)!] / [e^{−(a+b)}(a+b)ⁿ/n!]
= C(n, k) (a/(a+b))ᵏ (b/(a+b))^{n−k}.

That is the binomial(n, a/(a+b)) pmf. It is thinning, run backwards.

**2. Only the exponential is memoryless.**

*Solution.* Let G(t) = P(T > t). Memorylessness says G(s + t) = G(s)G(t) for all s, t ≥ 0, with G non-increasing and
G(0) = 1. Then:
- g = −log G is additive and non-decreasing;
- additivity gives g(q) = q·g(1) for rationals q;
- monotonicity extends this to all t.

So G(t) = e^{−λt} with λ = g(1). (λ = 0 is excluded for a proper waiting time.)

**3. Two transformations of a uniform.**

*Solution.*
- P(U² ≤ y) = P(U ≤ √y) = √y, so U² has density 1/(2√y) on (0, 1): **beta(½, 1)**.
- P(−2 log U ≤ y) = P(U ≥ e^{−y/2}) = 1 − e^{−y/2}. This is an exponential with mean 2, which is **χ²₂ = gamma(1, 2)**.

The second is half of Box–Muller: it is R², where R is the Box–Muller radius.

**4. The first of several buses.**

*Solution.* P(min Tᵢ > t) = ∏ P(Tᵢ > t) = e^{−nλt}, so the minimum is exponential(nλ). With three routes of mean 10
minutes, the rate is 3/10 and the expected wait is 10/3 ≈ 3.3 minutes. This is superposition.

**5. Capture–recapture.** n₁ = 200, n₂ = 150, m = 12.

*Solution.*
- Lincoln–Petersen: 200·150/12 = **2,500**.
- Chapman: 201·151/13 − 1 = 30,351/13 − 1 ≈ **2,334**.

The Chapman version is smaller because the naive ratio is biased upward (chapter 4; Part 9).

**6. The gamma as an exponential family** (α known).

*Solution.*

f(x) = x^{α−1}e^{−x/θ}/(Γ(α)θ^α) = [x^{α−1}/Γ(α)] · exp(−x/θ − α log θ).

So η = −1/θ, T(x) = x, and A(η) = α log θ = −α log(−η). Then:
- A′(η) = −α/η = αθ = E X;
- A″(η) = α/η² = αθ² = Var X.

## Where it comes back

| Idea | Returns in |
|---|---|
| the normal and sums | 6 (laws of averages, CLT), 8 (sampling distributions) |
| χ², t, F | 8, 10, 11, 12 |
| order statistics, the tank problem | 9 (UMVUE), 16 (ranks) |
| exponential families | 9, 22, 24, 45 |
| mixtures, overdispersion, total variance | 15, 24, 25 |
| the Poisson process | 17, 40 |
| heavy tails | 30, 60 |
| capture–recapture | 18, 41 |
