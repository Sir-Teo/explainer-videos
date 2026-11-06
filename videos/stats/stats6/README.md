# Statistics, Built — Part 6: The Laws of Averages

Part 6 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage I, Bachelor's: Foundations. Part 5 put several variables together; this
part asks what happens when we average many of them. It asks three questions: why does averaging work, how fast, and
when does it fail?

It opens with Francis Galton's ox (1907). At a Plymouth fair, 787 legible guesses at the dressed weight of an ox had
a median of 1,207 lb, against a true 1,198. From there the part builds:
- the inequalities that make averaging work: Markov, Chebyshev and Jensen;
- the weak law, with Bernoulli's 1713 urn;
- the kinds of convergence;
- the central limit theorem, seen by exact convolution and on a Galton board, then proved under an MGF-near-zero assumption, with the finite-variance characteristic-function extension stated;
- the normal approximation and the continuity correction;
- the speed of the CLT, which for the World's Pareto-tailed incomes is alarmingly slow;
- the delta method and Slutsky's theorem;
- Cauchy and stable laws, where averaging fails;
- Hoeffding's inequality and large deviations;
- the law of maxima, and with it floods and return levels.

Every number on screen is computed in [`compute.py`](compute.py). The ox, Bernoulli's urn and the Port Pirie sea
levels are the Museum's (`museum.OX_*`, `museum.BERNOULLI`, `museum.PORTPIRIE`); incomes and heights are the World's
(seed 1662); everything else is a seeded simulation or an exact calculation, and is tagged as such.

**Built in this part:** the Galton board (`GaltonBoard` in
[`explainer/stats/viz.py`](../../../../explainer/stats/viz.py)). Balls fall through rows of pegs, bouncing left or
right, and stack in bins:
- `drops(scene, bits)` animates balls along their zig-zag paths, each landing on the current pile;
- `bars(counts)` draws the pile for when there are too many balls to animate;
- `curve(f, scale)` overlays a density in the same units.

## Build it

```bash
python -m videos.stats.stats6.compute          # once: every computed item (seconds; cached in .cache/stats6)
python tools/build.py stats6 -q l              # fast 480p preview
python tools/build.py stats6                   # 1080p30 -> renders/stats6.mp4
python tools/qa_scene.py stats6 CLTSeen        # one chapter, silent, with a contact sheet
python tools/lecture_length.py stats6 --floor 50
```

## Chapters

| # | Chapter | What it does | Numbers (computed) |
|---|---|---|---|
| 0 | Galton's ox | *Vox populi* (1907): the percentile table as an ogive, with a normal of Galton's probable error; a simulated crowd whose error falls like 75/√n until a shared bias stops it; the objectives. | median 1,207 vs 1,198 lb (+0.75%); quartiles 1,162 and 1,236; mean 1,197 |
| 1 | Markov, Chebyshev, Jensen | Markov by the step under the line; tested on the World's incomes; Chebyshev from Markov; the three-point law that attains it; Jensen by chords, with the World's geometric and arithmetic mean incomes. | at 3× mean: 2.3% vs bound 33%; 2σ: heights 3.5%, incomes 1.7% vs 25%; geometric mean 39.6k < 49.5k |
| 2 | The weak law | Chebyshev's three-line proof; 40 coin paths in the √n funnel; the count of extra heads wanders (no gambler's compensation); Bernoulli's golden theorem and his 25,550 against modern bounds. | Chebyshev 600,600; Bernoulli 25,550; Hoeffding 9,503; normal 6,498; exact 6,520 |
| 3 | Kinds of convergence | In probability, in distribution, almost surely; the mirror X_n = −X; the typewriter sequence; the strong law, seen in 2,000 sequences; the hierarchy. | outside 0.5 ± 0.02 after toss 10,000: 1 sequence in 2,000 |
| 4 | The CLT, seen | Exact convolution powers of a lopsided law on {0,…,5}; cumulants: skewness/√n, kurtosis/n; the Galton board; uniform, exponential and lopsided sums of 30. | sup\|F_n − Φ\|: 0.298 (n = 1) → 0.031 (n = 30) |
| 5 | The CLT, proved | M_Y(t/√n)^n; the cumulant expansion; Curtiss's continuity theorem; n log M(t/√n) → t²/2 drawn for the exponential and the lopsided law; Lindeberg–Lévy, Lyapunov, Lindeberg, Feller; Pólya's name. | — |
| 6 | Using it | De Moivre's 1733 pamphlet; the local approximation; the continuity correction; a rare-event binomial where the Poisson wins. | P(S = 50) 0.0796 vs 0.0798; P(S ≥ 60) 0.0284 exact, 0.0228 plain, 0.0287 corrected; p = 0.03: 0.081 exact, 0.071 normal, 0.084 Poisson |
| 7 | Is thirty enough? | Means of heights (normal at n = 5) and of incomes (skewed at n = 1,000); t-interval coverage; Berry–Esseen with Shevtsova's constant; the skewness/√n rule. | income coverage 87.4% (n = 5), 89.5% (30), 92.9% (1,000), misses almost all low; lognormal BE bound 0.219 vs actual 0.029 at n = 30 |
| 8 | The delta method | The tangent-line picture; the derivation; √ of a Poisson (variance → 1/4); arcsine of a share (1/4n); several means and ratios; log of a mean; second order and χ²₁. | Var √X 0.251 at λ = 64; sd(log x̄) 0.00782 predicted vs 0.00780 simulated |
| 9 | Slutsky and continuous mapping | The two theorems; consistency; the t statistic without normality; t for heights and incomes; why Slutsky needs a constant (X_n = Z, Y_n = −Z). | coverage: heights 94.6% (n = 10); incomes 86.8% (10), 91.4% (100) |
| 10 | When averages fail | Running means of normals and Cauchys; the Cauchy mean is Cauchy (characteristic functions); Pareto α = 1.5: the law holds, the CLT fails; stable laws and the generalized CLT. | quartiles of the Cauchy mean ≈ ±1.0 for n = 1, 10, 100 |
| 11 | Concentration | Hoeffding's inequality; its proof (Chernoff's trick, Hoeffding's lemma); against Chebyshev, the normal approximation and the exact tail; the union bound and log m; Cramér's large-deviation rate. | n = 1,000: exact 0.0014, Hoeffding 0.0135, Chebyshev 0.096; 10 → 10⁶ proportions: n = 1,199 → 3,501 |
| 12 | The law of maxima | F^n; max − log n → Gumbel, derived and simulated; the three families (Gumbel, Fréchet, reversed Weibull); the GEV and Fisher–Tippett–Gnedenko. | — |
| 13 | Floods and return levels | The 1953 North Sea flood and the Delta Committee; Port Pirie's 65 annual maxima; the GEV fit by maximum likelihood; return levels; the profile likelihood of the 100-year level; van Dantzig's economic dike height. | (μ, σ, ξ) = (3.875, 0.198, −0.050); z₁₀₀ = 4.69 m, 95% profile interval [4.49, 5.26]; z₁₀₀₀₀ = 5.34 m |
| 14 | Outro | Recap, payoffs, problems, references, the Transcript, Part 7's question. | — |

The displayed CDF distances check both sides of every jump, without a continuity correction. Monte Carlo CDF distances are empirical diagnostics. Histogram densities retain omitted tails in their denominators; path segments leave the viewport rather than flattening onto its edge.

The World is a finite population and has finite moments of every order. Its income-tail generator uses an unbounded Pareto model with index 2.1, which has finite variance but no third moment. These are separate laws: the finite World's Berry--Esseen bound is valid but trivial at the shown sample sizes. The lognormal reference population is a fixed simulation of two million values.

The CLT concerns central deviations; fixed tail probabilities require concentration or large-deviation arguments. Stable and extreme-value limits require non-degenerate limits and appropriate centring/scaling. Return levels and the approximate profile interval assume the fitted stationary annual-maxima model; they do not incorporate all uncertainty in dependence, climate changes or the tail family.

## Sources

- **Galton's ox.** F. Galton, "Vox populi", *Nature* 75 (1907), 450–451, and "The ballot-box", *Nature* 75 (1907),
  509; K. F. Wallis, "Revisiting Francis Galton's forecasting competition", *Statistical Science* 29 (2014).
- **The weak law.** J. Bernoulli, *Ars Conjectandi* (1713), Part IV; I.-J. Bienaymé (1853); P. Chebyshev, "Des valeurs
  moyennes" (1867); E. Borel (1909) and A. Kolmogorov for the strong law.
- **The central limit theorem.**
  - A. de Moivre, *Approximatio ad summam terminorum binomii* (1733).
  - P.-S. Laplace (1810; *Théorie analytique des probabilités*, 1812).
  - A. Lyapunov (1901); J. W. Lindeberg (1922); W. Feller (1935).
  - G. Pólya, "Über den zentralen Grenzwertsatz…" (1920); J. Curtiss, *Ann. Math. Statist.* 13 (1942).
  - H. Fischer, *A History of the Central Limit Theorem* (2011).
- **Speed.** A. Berry (1941); C.-G. Esseen (1942); I. Shevtsova (2011), C ≤ 0.4748.
- **Combining limits.** E. Slutsky, *Metron* 5 (1925); H. Mann & A. Wald, *Ann. Math. Statist.* 14 (1943).
- **Heavy tails.** P. Lévy, *Calcul des probabilités* (1925); B. Gnedenko & A. Kolmogorov, *Limit Distributions for
  Sums of Independent Random Variables* (1949; English 1954); B. Mandelbrot, "The variation of certain speculative
  prices" (1963).
- **Concentration.** H. Chernoff (1952); W. Hoeffding, *JASA* 58 (1963); H. Cramér (1938).
- **Extremes.**
  - R. A. Fisher & L. Tippett, *Proc. Camb. Phil. Soc.* 24 (1928); B. Gnedenko, *Ann. Math.* 44 (1943).
  - E. J. Gumbel, *Statistics of Extremes* (1958); S. Coles, *An Introduction to Statistical Modeling of Extreme
    Values* (2001), §3.4.1 for Port Pirie.
  - D. van Dantzig, "Economic decision problems for flood prevention", *Econometrica* 24 (1956).
- **Textbooks.**
  - J. Blitzstein & J. Hwang, *Introduction to Probability* (2nd ed., 2019), chs. 10–11.
  - G. Grimmett & D. Stirzaker, *Probability and Random Processes* (4th ed., 2020), ch. 7.
  - G. Casella & R. Berger, *Statistical Inference* (2nd ed., 2002), §5.5.
  - A. W. van der Vaart, *Asymptotic Statistics* (1998), chs. 2–3.
  - R. Vershynin, *High-Dimensional Probability* (2018), ch. 2.

## Problems and solutions

**1. Markov, made tight.** X ≥ 0 with E X = 1.

*Solution.* By Markov, P(X ≥ 3) ≤ E X / 3 = 1/3. Equality: let X = 3 with probability 1/3 and 0 otherwise. Then
E X = 1 and P(X ≥ 3) = 1/3. In general, equality in Markov's inequality needs X to take only the values 0 and a.

**2. A poll's sample size.** P(|p̂ − p| ≥ 0.03) ≤ 0.05.

*Solution.*
- **Chebyshev:** P ≤ p(1 − p)/(n ε²) ≤ 1/(4n · 0.0009). Setting this ≤ 0.05 gives n ≥ 5,556.
- **Hoeffding:** 2 exp(−2n · 0.0009) ≤ 0.05 gives n ≥ log(40)/0.0018, so n ≥ 2,050.
- **Normal approximation:** 1.96 · √(1/(4n)) ≤ 0.03 gives n ≥ 1,068, the familiar "a thousand voters, ±3 points".

The first two are guarantees; the third is an approximation, and a good one here, since np(1 − p) is large.

**3. Binomial to Poisson by MGFs.**

*Solution.* The MGF of Binomial(n, λ/n) is (1 − λ/n + (λ/n)e^t)^n = (1 + λ(e^t − 1)/n)^n. As n → ∞ this tends to
exp(λ(e^t − 1)) for every t, using (1 + y/n)^n → e^y. That is the Poisson(λ) MGF, and by Curtiss's theorem the
distributions converge.

**4. The delta method for a rate.** X_i ~ Exponential(rate λ).

*Solution.* E X = 1/λ and Var X = 1/λ², so √n(X̄ − 1/λ) → N(0, 1/λ²). With g(x) = 1/x, g'(1/λ) = −λ², and the delta
method gives

√n(1/X̄ − λ) → N(0, λ⁴ · 1/λ²) = N(0, λ²).

So 1/X̄, which is the maximum-likelihood estimator of λ (Part 9), has standard error about λ/√n.

**5. The maximum of uniforms.**

*Solution.* For 0 ≤ x ≤ n,

P(n(1 − max U_i) > x) = P(max U_i < 1 − x/n) = (1 − x/n)^n → e^{−x}.

So the limit is Exp(1): the reversed Weibull family, with shape 1.

**6. The t statistic, theorem by theorem.** Assume i.i.d. observations with finite positive variance.

*Solution.*
- **CLT:** Z_n = √n(X̄ − μ)/σ → N(0, 1) in distribution.
- **Weak law, twice:** X̄ → μ and (1/n)ΣX_i² → E X² in probability (E X² < ∞).
- **Continuous mapping:** S_n² = (n/(n − 1))((1/n)ΣX_i² − X̄²) → E X² − μ² = σ² in probability, since n/(n − 1) → 1.
  Continuous mapping again (x ↦ σ/√x, continuous at σ² > 0) gives σ/S_n → 1 in probability.
- **Slutsky:** T_n = Z_n · (σ/S_n) → N(0, 1) · 1 = N(0, 1).

The weak law for X² needs only its finite first moment E X², not E X⁴. No normality was used; i.i.d. sampling with finite, non-zero variance.

## Where it comes back

| Idea | Returns in |
|---|---|
| the weak law, consistency | 9, 22, 47 |
| the central limit theorem | 8, 10, 11, 43 |
| the speed of the CLT, Berry–Esseen | 16, 47 |
| the delta method | 9, 14, 18, 22 |
| Slutsky, continuous mapping | 9, 10, 47 |
| concentration, Hoeffding, the union bound | 51, 54, 58 |
| heavy tails, stable laws | 30, 60 |
| extreme values, return levels, profile likelihood | 22, 39, 40 |
