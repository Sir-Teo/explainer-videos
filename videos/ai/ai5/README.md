# AI, Built — Part 5: Randomness in Motion

Current QA checkpoint: all 28 corrected numerical items completed in the cloud, and all 56 payloads passed
strict currentness and guarded-load checks without invoking a producer. Bilingual silent visual and motion review
is in progress; narration, listening and production acceptance remain open. Current decoding results below use
metric v3 and supersede the historical v2 table. See [the Part 5 checklist](../../../docs/qa/ai5-chapter-checklist.md).

Part 5 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). A model hands us distributions: it is fitted by maximum likelihood, it is sampled
to write, its gradients are averages over random choices, and the newest image generators are random motion run
backwards. This part is the probability behind all of that, from Pascal and Fermat's letters to the Fokker–Planck
equation, with the history of each idea and where it shows up in today's models. Every number on screen is computed
here, small and on a CPU, or cited.

## Chapters

* **Out of noise.** 600 random dots flow, by the reverse-time SDE with the exact score of the noised letters, into
  "AI"; run forwards, the letters dissolve. How we got here, 1654–2020 (Pascal and Fermat, Bernoulli, de Moivre,
  Bayes and Laplace, Gauss, Einstein, Fisher, Itô, Metropolis et al., diffusion models and nucleus sampling); the plan.
* **1. The bell curve.** Bernoulli's law of large numbers (1713): six runs of 5,000 flips settle between 0.489 and
  0.512. A Galton board, 1,000 balls through 12 rows (χ² = 12.1 against the binomial); C(12, k)/2¹² and de Moivre's
  curve (1733); dice sums for k = 1 … 12; the central limit theorem (Laplace 1810). *Why:* the density of a sum is a
  convolution, derived and pictured (an exponential's flipped copy sliding, the overlap tracing s e⁻ˢ); repeated
  convolution on a grid (checked against the exact Gamma CDF) turns the exponential into the bell. *How fast:* the
  Kolmogorov distance falls with slope −0.50 for the exponential (0.158 → 0.017 at n = 64), under the Berry–Esseen
  bound C ρ/σ³√n with C = 0.4748 (Berry 1941, Esseen 1942, Shevtsova 2011); for the symmetric uniform, slope −1.02.
* **2. Bells in many dimensions.** Every Gaussian is μ + Lz; Σ = LLᵀ; elliptical contours along Σ's eigenvectors.
  Conditioning derived (precision, completing the square, the Schur complement). Checked: of 400,000 points, the 2,568
  in the strip x₂ = 1.5 ± 0.02 have mean 0.796 and variance 0.448 against the predicted 0.804 and 0.4375; in four
  dimensions, two given two, off by at most 0.036. Galton's regression (1886); the Kalman filter (1960), Gaussian
  processes, and diffusion's Gaussian posteriors (Part 21).
* **3. Fitting a bell: maximum likelihood.** The log-likelihood as a score, the probability density, the (μ, σ)
  landscape climbed by gradient ascent to μ̂ = 5.96, σ̂ = 1.71 (√3 predicted); maximum likelihood is minimum
  cross-entropy. The bias of σ̂², derived (E = (n−1)/n σ²) and measured on 40,000 samples of each size (0.800 at n = 5;
  Bessel's correction 0.999); Fisher (1922).
* **4. How precise can an estimate be?** The Cauchy location: the sample average never improves (its interquartile
  range stays near 2 from n = 5 to 500); the median and a multistart likelihood fit do (global optimality is not certified). Score, Fisher information (measured
  variance of the Cauchy score 0.4998 against 1/2) and the Cramér–Rao bound derived (Fisher 1925; Rao 1945; Cramér
  1946). Measured on 4,000 samples of each size: n·Var(the likelihood fit) falls from 4.74 at n = 5 to 2.02 at n = 500 (bound 2);
  the median levels at 2.49 (π²/4). The Fisher matrix in training: natural gradient (Amari 1998), EWC (Kirkpatrick et
  al. 2017), K-FAC and Shampoo (Part 11).
* **5. Belief as a distribution.** Bayes's rule (Bayes 1763, Laplace 1774) on the frequency of "e" in Part 1's
  passage, live from a flat prior: 95% of the belief between 0.1205 and 0.1335 after 10,000 letters, the whole passage
  at 0.1221. Beta–binomial conjugacy derived; Laplace's rule of succession; three priors pulled together by the same
  letters. MAP as regularization derived: a Gaussian prior is weight decay, λ = σ²/τ². Ten points from sin 2πx and a
  degree-9 polynomial (Bishop's example): median test error 0.247 for maximum likelihood, 0.025 for MAP at
  λ ≈ 3 × 10⁻⁴, over 200 training sets.
* **6. Maximum entropy.** Jaynes's Brandeis die (average 4.5); the maximum-entropy solution derived with Lagrange
  multipliers (p_k ∝ e^{λk}); the dual fitted by gradient steps from the fair die, replayed: λ = 0.371,
  p = (0.054, 0.079, 0.114, 0.165, 0.240, 0.347), entropy 1.6136 nats, above all 20,000 random dice with the same
  average (highest 1.6135). On the line: fixing mean and variance gives the bell (to 3 × 10⁻¹⁴), fixing E|x| gives
  Laplace's double exponential; fixing the average energy gives Boltzmann and Gibbs's distribution, the softmax; the
  exponential family and moment matching.
* **7. How far from the average?** A million runs of 100 fair flips; Markov, Chebyshev, Chernoff and Hoeffding
  derived in a chain; against the exact tail at ε = 0.1 (0.0284): 0.83, 0.25, 0.134, 0.135. Flips needed to guarantee
  P(overshoot ≥ 0.05) ≤ 0.05: Chebyshev 2,000, Hoeffding 600, Chernoff 599, the smallest qualifying fixed sample size 262; all sample sizes from 281 onward qualify (the exact binomial tail oscillates with integer counts). Part 8's generalization
  bounds; Part 26's UCB.
* **8. Rolling loaded dice.** Inverse-CDF sampling (letters; exponentials: KS 0.006); von Neumann's rejection
  sampling (1951; Beta(2, 5), 40.3% kept, 1/M = 40.7% predicted); Box–Muller derived (1958; KS 0.002, correlation
  −0.008); the Gumbel-max trick derived and checked (200,000 picks against the softmax, χ² = 3.9 on 5 degrees of
  freedom; Gumbel 1954, Luce 1959, Yellott 1977, Maddison et al. 2014); Gumbel-softmax at τ = 0.1, 1, 5 (largest
  entry 0.95, 0.58, 0.25; Jang, Gu & Poole 2017; Maddison, Mnih & Teh 2017).
* **9. How a language model chooses.** GPT-2's next-word distribution under a temperature dial (entropy 4.7, 9.0,
  13.5 bits at T = ½, 1, 2) and its samples; top-k (Fan et al. 2018), top-p (Holtzman et al. 2020) and min-p (Nguyen
  et al. 2024; re-analysed by Schaeffer et al. 2025), the top-p cut sliding over two real GPT-2 distributions (an open
  one and a nearly certain one: at p = 0.9, 1,210 words against 1; min-p 0.1, 40 against 1). The experiment: the series' novels
  model uses 16 settings on 12 held-out passages: 8 continuations per stochastic setting, one for greedy; GPT-2 judges each by its surprise; at equal
  diversity 0.85, top-k has the lowest interpolated surprise in this run (0.959 against 1.043 nats per character
  for temperature alone); greedy repeats 35.1% of its token 4-grams (see *Computed results*).
* **10. Chains with short memories.** A three-state chain from Part 1's letters; its stationary distribution as the
  eigenvector of eigenvalue 1 (Markov 1906, 1913); all 27 letters from "q", forgotten within five steps at the rate of
  the second eigenvalue, 0.30. Detailed balance derived; English is not reversible ("e" then space is 10 times as common
  as space then "e"). The spectral gap: a walk on 41 sites in a double well; its mixing time against 1/gap over eight
  barrier heights rises from 638 to 26 million steps, slope 0.98, between the bounds (t_rel − 1) ln 2 and
  t_rel ln(4/π_min) (Levin & Peres).
* **11. Answers from random samples.** Los Alamos: Ulam's solitaire (1946), von Neumann's neutrons, ENIAC (1948).
  π from 4,000 darts; the error's slope −0.50 over 200 runs at nine sizes; a rare event, P(Z > 4) = 3.17 × 10⁻⁵:
  two hits in 10,000 plain draws, within 1% by importance sampling. The effective sample size of importance weights
  against dimension (proposal 1.25× wider): 4,671 of 5,000 in one dimension, 184 in fifty, 10.5 measured in two
  hundred, where the population-moment large-sample proxy is 0.005; this proxy is not the exact finite-sample ESS.
* **12. The gradient of an average.** The log-derivative trick derived; baselines (Glynn 1990; Williams 1992). For
  ∇ E[x²], x ~ N(1, 1): the estimate averages 1.998 (truly 2) with per-sample variance 30.0, 13.9 with the best
  baseline (b = 3.99), and 4.0 reparameterized (Kingma & Welling 2013). Evolution strategies (Salimans et al. 2017)
  on a curved valley, 8 runs each at equal iteration caps (early divergence uses fewer probes). For the Gaussian-smoothed objective, the mean squared gradient-estimation error is 398.7 plain, 16.8 with an
  unbiased leave-one-out-equivalent baseline, and 15.6 with mirrored probes (the squared reference-gradient norm is
  37.2164). The smoothed optimum differs from the original objective's optimum. With the same step size,
  2 of 8 plain runs diverge, none with the baseline.
* **13. Sampling the unsampleable.** Metropolis et al. (1953, MANIAC): the walk on a two-bump density, proposals
  accepted and rejected, 65% of the time in the bump that holds two thirds. Metropolis–Hastings derived from detailed
  balance (Hastings 1970). Langevin dynamics (Langevin 1908; MALA, Roberts & Tweedie 1996; SGLD, Welling & Teh 2011):
  1,500 particles from noise with their density evolving in 3D; L¹ distance from the target 1.19 → 0.23; 59% in the left
  bump. Mixing measured, four samplers × 5 seeds × 20,000 steps: hops between the bumps and the conditional variance within the left
  one (conditional variance 0.3414) — random-walk Metropolis 70 hops, 0.34; small-step Langevin 13, 0.36; big-step Langevin 228 but
  0.56 (biased); MALA 6, 0.34.
* **14. Brownian motion.** Brown (1827); random walks with 8, 64, 1,024 steps of ±1/√n; Bachelier (1900), Wiener
  (1923), Donsker's scaling limit; 60 paths shown against the mean ± one standard deviation, ±√t (not pathwise bounds), variances 0.25, 0.49, 0.74, 0.98 on 20,000 paths. Quadratic
  variation derived and measured on 400 paths: Σ(ΔW)² = 0.99 ± 0.32 with 16 steps, 0.999 ± 0.011 with 16,384, while
  Σ|ΔW| reaches 102 (Lévy 1940). A cloud in the plane; the heat equation; Einstein (1905), Perrin (1908).
* **15. Itô's lemma.** ∫W dW with left points derived (½W² − ½) and checked on 2,000 paths (error 0.22 → 0.007 from
  10 to 10,000 steps; midpoints give ½W² exactly). Itô's lemma derived; checked path by path on e^W (gap 0.66 → 0.012,
  slope −0.56; without the ½f″ dt term it stalls at 0.79) and on average, E[e^{W₁}] = 1.649 against e^{1/2} = 1.6487.
  Doeblin's sealed envelope (1940, opened 2000), Itô (1944, 1951), Stratonovich (1966), Black–Scholes–Merton (1973).
* **16. Randomness with a push.** dx = f dt + g dW; Euler–Maruyama; the Ornstein–Uhlenbeck process (1930) settling to
  its bell. Euler–Maruyama's convergence on geometric Brownian motion against the exact solution from the same noise,
  20,000 paths: strong error slope 0.54, weak error slope 0.95 (Maruyama 1955).
* **17. The density's own law.** The Fokker–Planck equation derived from Itô's lemma by integration by parts (Fokker
  1914, Planck 1917, Kolmogorov 1931); solved on a grid for the OU process against 20,000 particles (histograms within
  0.0382 of exact bin-average densities conditioned on the plotted interval, the grid within 0.000411 of the exact density); Langevin's stationary density is the target, derived;
  Anderson's reverse-time SDE (1982) and the score, in 1D and in the plane (Part 21).
* **Recap**, where it comes back, six problems, Part 6's teaser, references.

## Computed results

`python -m videos.ai.ai5.compute` writes every item to `.cache/ai5/`. The numbers quoted above, plus:

* **Decoding** (`decoding`, resumable by setting). The novels model continues twelve deterministic held-out
  prompts of 32 generator tokens. Each of fifteen stochastic settings generates eight 40-token continuations per
  prompt; greedy generates one. These configuration totals are 1,452 generated continuations and 58,080 tokens.
  Full generated strings and character counts were not retained for an independent raw-row recount.

  GPT-2 revision `607a30d783dfa663caf39e06633721c8d4cfcd7e` scores separately tokenized prompt/continuation
  boundaries in nats per true continuation Unicode character, without silent truncation. This convention and
  changed prompt selection make these results numerically incomparable with the old metric-v2 table. Diversity
  pools generator-token bigrams within a prompt; repetition counts generator-token 4-grams, not word sequences.

| Setting | NLL (nats/character) | Distinct token bigrams | Repeated token 4-grams | Mean tokens kept |
|---|---:|---:|---:|---:|
| greedy0.0 | 0.540234 | — | 35.1351% | 1.000 |
| temp0.5 | 0.851139 | 0.695246 | 2.1396% | 4096.000 |
| temp0.7 | 0.997609 | 0.833600 | 0.4223% | 4096.000 |
| temp1.0 | 1.281646 | 0.936165 | 0.0282% | 4096.000 |
| temp1.3 | 1.613097 | 0.989049 | 0.0000% | 4096.000 |
| topk5 | 0.827322 | 0.733707 | 0.9009% | 5.000 |
| topk20 | 0.997796 | 0.883814 | 0.0282% | 20.000 |
| topk100 | 1.170755 | 0.923077 | 0.0845% | 100.000 |
| topp0.5 | 0.885511 | 0.767628 | 0.5349% | 11.448 |
| topp0.8 | 1.059453 | 0.889957 | 0.1126% | 63.650 |
| topp0.9 | 1.147806 | 0.930288 | 0.0000% | 145.573 |
| topp0.95 | 1.189928 | 0.928152 | 0.0282% | 272.284 |
| minp0.02 | 1.042255 | 0.894765 | 0.0563% | 45.579 |
| minp0.05 | 0.983257 | 0.846955 | 0.5068% | 21.750 |
| minp0.1 | 0.902881 | 0.810897 | 0.4223% | 11.161 |
| minp0.2 | 0.841291 | 0.709402 | 1.4640% | 5.484 |
| Held-out human reference | 1.012341 | — | 0.0000% | — |


  At diversity 0.85, linear interpolation within observed supports gives temperature 1.043026, top-k 0.959394,
  top-p 1.002637 and min-p 0.987015 nats/character. All four rules cover this target; their common support is
  [0.767628, 0.894765]. Top-k is lowest in this descriptive interpolation of one run. This does not establish
  significance or generalization. Greedy has the lowest surprise and the most repetition; likelihood alone
  does not measure text quality.

  The mean across sixteen settings of SD(promptwise NLL/character)/√12 is 0.051391 nats/character; the mean
  passage SD is 0.178025. This descriptive SE concerns an unweighted average of promptwise ratios. It is not
  the uncertainty of the character-weighted headline score, passage-to-passage spread, a calibrated confidence
  interval, or model/run-to-run uncertainty. Raw character weights were not saved to estimate weighted uncertainty.

  Parent-recorded elapsed intervals were 651.410 seconds for decoding and 781.241 seconds summed across all
  28 child processes, including setup/imports. The 56 payload files total 3,090,034 bytes. These observations
  describe this cloud run, not a portable runtime promise.

## Run

```
python tools/make.py ai5                         # compute, then the narrated cut in English and Chinese
python -m videos.ai.ai5.compute                  # the numbers alone (needs Part 1's books, .cache/ai1; GPT-2 small;
                                                 #   the series' novels model, python -m explainer.ai.novels)
python tools/build.py ai5                        # English
python tools/build.py ai5 --lang zh              # Chinese
python tools/qa_scene.py ai5 Decoding            # one chapter, silent, with a contact sheet
```

The compute is seeded throughout. Decoding saves each setting and resumes only with matching consumed-input,
producer and runtime identities. Runtime depends on hardware, dependencies and load; the measured cloud run is
reported above. Use cached-only QA for frozen reviewed data rather than triggering a producer during rendering.

## Fact-check notes

* Min-p (Nguyen et al., arXiv 2407.01082, ICLR 2025) was challenged by Schaeffer et al., *Min-p, Max Exaggeration*
  (arXiv 2506.13681, 2025); the chapter says so.
* Itô's stochastic integral is 1944 (Proc. Imp. Acad. Tokyo 20); the formula ("Itô's lemma") is 1951 (Nagoya Math. J.
  3). Doeblin's *pli cacheté* was sent in February 1940 and opened in 2000; he died in June 1940.
* The Brandeis dice problem is from Jaynes's 1962 Brandeis Summer School lectures; the maximum-entropy principle is
  Jaynes (1957).
* The Berry–Esseen constant 0.4748 for identically distributed summands is Shevtsova (2011, arXiv 1111.6554).
* Kalman filtering in the Apollo guidance computer; ES training of simulated robots and Atari (Salimans et al. 2017);
  the first DALL-E's discrete VAE trained with a Gumbel-softmax relaxation (Ramesh et al. 2021).

## References

Books: J. K. Blitzstein & J. Hwang, *Introduction to Probability* (2019); L. Wasserman, *All of Statistics* (2004);
D. J. C. MacKay, *Information Theory, Inference, and Learning Algorithms* (2003); D. A. Levin & Y. Peres, *Markov
Chains and Mixing Times* (2017); B. Øksendal, *Stochastic Differential Equations* (2003); S. Boucheron, G. Lugosi &
P. Massart, *Concentration Inequalities* (2013); C. M. Bishop, *Pattern Recognition and Machine Learning* (2006).

Papers: de Moivre (1733); Laplace (1774, 1810); Bayes (1763); Gauss (1809); Galton (1886, 1889); Markov (1906, 1913);
Einstein (1905); Bachelier (1900); Langevin (1908); Fokker (1914); Planck (1917); Wiener (1923); Fisher (1922, 1925);
Ornstein & Uhlenbeck (1930); Kolmogorov (1931); Lévy (1940); Berry (1941); Esseen (1942); Itô (1944, 1951); Rao (1945);
Cramér (1946); Metropolis & Ulam (1949); von Neumann (1951); Chernoff (1952); Metropolis, Rosenbluth, Rosenbluth,
Teller & Teller (1953); Gumbel (1954); Maruyama (1955); Jaynes (1957); Box & Muller (1958); Kalman (1960); Hoeffding
(1963); Stratonovich (1966); Hastings (1970); Anderson (1982); Glynn (1990); Williams (1992); Roberts & Tweedie (1996);
Amari (1998); Shevtsova (2011); Welling & Teh (2011); Kingma & Welling (2013); Maddison, Tarlow & Minka (2014);
Sohl-Dickstein et al. (2015); Jang, Gu & Poole (2017); Maddison, Mnih & Teh (2017); Kirkpatrick et al. (2017);
Salimans et al. (2017); Fan, Lewis & Dauphin (2018); Holtzman et al. (2020); Song et al. (2021); Nguyen et al. (2024);
Schaeffer et al. (2025).

## Problems, with solutions

**1. Sums are convolutions.** Show that the density of X + Y, for independent X, Y with densities f, g, is f ∗ g. For
f = g = e⁻ˣ on x > 0, compute f ∗ f and f ∗ f ∗ f.

*Solution.* P(X + Y ≤ s) = ∫ f(x) P(Y ≤ s − x) dx = ∫ f(x) G(s − x) dx; differentiating in s gives
∫ f(x) g(s − x) dx = (f ∗ g)(s). For the exponential, (f ∗ f)(s) = ∫₀ˢ e⁻ˣ e^{−(s−x)} dx = s e⁻ˢ, and
(f ∗ f ∗ f)(s) = ∫₀ˢ x e⁻ˣ e^{−(s−x)} dx = s² e⁻ˢ / 2: the Gamma densities, sⁿ⁻¹e⁻ˢ/(n − 1)!.

**2. Fisher information.** Compute the Fisher information of N(θ, σ²) in θ, and of the Cauchy location; which
estimators reach the Cramér–Rao bound?

*Solution.* For the normal, s = (x − θ)/σ², I = E[s²] = 1/σ²: the bound is σ²/n, which the sample mean reaches exactly
for every n. For the Cauchy, s = 2u/(1 + u²) with u = x − θ, and I = (1/π)∫ 4u²/(1 + u²)³ du = 1/2: the bound is 2/n.
The maximum-likelihood estimate reaches it as n → ∞ (it is asymptotically efficient), the median does not (π²/(4n)),
and the average has no variance at all.

**3. Maximum entropy on the integers.** Show that the maximum-entropy distribution on {0, 1, 2, …} with mean m is
geometric.

*Solution.* With multipliers for Σp_k = 1 and Σk p_k = m, stationarity gives log p_k = α − 1 + λk, so p_k = C r^k with
r = e^λ < 1 (for the sum to converge). Normalizing, p_k = (1 − r) r^k, whose mean is r/(1 − r) = m, so r = m/(1 + m).

**4. How many samples.** Use Hoeffding's inequality to find n so that an average of n values in [0, 1] is within 0.01 of
its mean with probability 0.999.

*Solution.* Two-sided, P(|X̄ − μ| ≥ ε) ≤ 2e^{−2nε²}. Setting 2e^{−2n · 10⁻⁴} ≤ 10⁻³ gives n ≥ ln(2000)/(2 · 10⁻⁴) =
38,004.5, so n = 38,005. (Chebyshev would ask for 1/(4ε²δ) = 2,500,000.)

**5. The Gumbel-max trick.** Show that argmaxᵢ(zᵢ + Gᵢ), with independent standard Gumbel Gᵢ, picks i with probability
e^{zᵢ}/Σⱼe^{zⱼ}.

*Solution.* A Gumbel has CDF F(x) = exp(−e^{−x}) and density e^{−x}F(x). Option i wins when zᵢ + Gᵢ = y beats every
other: P = ∫ e^{−(y−zᵢ)} F(y − zᵢ) Πⱼ≠ᵢ F(y − zⱼ) dy = ∫ e^{zᵢ} e^{−y} exp(−e^{−y} Z) dy with Z = Σⱼ e^{zⱼ}. Substituting
t = e^{−y}: e^{zᵢ} ∫₀^∞ e^{−tZ} dt = e^{zᵢ}/Z.

**6. The Ornstein–Uhlenbeck stationary bell.** For dx = −θx dt + σ dW, find the stationary density from the
Fokker–Planck equation.

*Solution.* ∂p/∂t = ∂(θxp)/∂x + (σ²/2) ∂²p/∂x². Stationary: the flux θxp + (σ²/2)p′ is constant, and zero since p
vanishes at infinity. So p′/p = −2θx/σ², p ∝ exp(−θx²/σ²): a bell with variance σ²/(2θ), as in chapter 16.

## 习题与解答

**1. 和就是卷积。** 证明：独立的X、Y，密度分别为f、g，则X + Y的密度是f ∗ g。对x > 0上的f = g = e⁻ˣ，计算f ∗ f与f ∗ f ∗ f。

*解答。* P(X + Y ≤ s) = ∫ f(x) G(s − x) dx，对s求导得∫ f(x) g(s − x) dx = (f ∗ g)(s)。对指数分布，
(f ∗ f)(s) = ∫₀ˢ e⁻ˣ e^{−(s−x)} dx = s e⁻ˢ，(f ∗ f ∗ f)(s) = s² e⁻ˢ / 2：即伽马分布的密度sⁿ⁻¹e⁻ˢ/(n − 1)!。

**2. 费希尔信息。** 求N(θ, σ²)关于θ的费希尔信息，以及柯西分布位置参数的费希尔信息；哪些估计量能达到克拉默-拉奥下界？

*解答。* 正态分布的分数s = (x − θ)/σ²，I = 1/σ²，下界σ²/n，样本均值对任何n都恰好达到。柯西分布的s = 2u/(1 + u²)，
I = 1/2，下界2/n；最大似然估计在n → ∞时达到（渐近有效），中位数达不到（π²/(4n)），平均值连方差都没有。

**3. 整数上的最大熵。** 证明：在{0, 1, 2, …}上、均值为m的最大熵分布是几何分布。

*解答。* 对Σp_k = 1与Σk p_k = m引入乘子，驻点条件给出log p_k = α − 1 + λk，即p_k = C r^k，r = e^λ < 1。归一化得
p_k = (1 − r) r^k，均值r/(1 − r) = m，故r = m/(1 + m)。

**4. 需要多少样本。** 用霍夫丁不等式求n，使n个[0, 1]内取值的平均以0.999的概率落在均值的0.01以内。

*解答。* 双侧形式P(|X̄ − μ| ≥ ε) ≤ 2e^{−2nε²}。令2e^{−2n · 10⁻⁴} ≤ 10⁻³，得n ≥ ln(2000)/(2 × 10⁻⁴) = 38004.5，故n = 38005。
（切比雪夫不等式要求1/(4ε²δ) = 250万。）

**5. 冈贝尔最大值技巧。** 证明：对独立的标准冈贝尔噪声Gᵢ，argmaxᵢ(zᵢ + Gᵢ)选中i的概率是e^{zᵢ}/Σⱼe^{zⱼ}。

*解答。* 冈贝尔分布的累积分布函数F(x) = exp(−e^{−x})，密度e^{−x}F(x)。选项i获胜的概率为
∫ e^{−(y−zᵢ)} F(y − zᵢ) Πⱼ≠ᵢ F(y − zⱼ) dy = ∫ e^{zᵢ} e^{−y} exp(−e^{−y} Z) dy，其中Z = Σⱼ e^{zⱼ}。令t = e^{−y}，
得e^{zᵢ} ∫₀^∞ e^{−tZ} dt = e^{zᵢ}/Z。

**6. 奥恩斯坦-乌伦贝克过程的平稳钟形曲线。** 对dx = −θx dt + σ dW，由福克-普朗克方程求平稳密度。

*解答。* ∂p/∂t = ∂(θxp)/∂x + (σ²/2) ∂²p/∂x²。平稳时通量θxp + (σ²/2)p′为常数，又因p在无穷远处为零，常数为零。
于是p′/p = −2θx/σ²，p ∝ exp(−θx²/σ²)：方差为σ²/(2θ)的钟形曲线，与第16章一致。

## Glossary (new terms of this part)

| English | 中文 |
|---|---|
| law of large numbers | 大数定律 |
| central limit theorem | 中心极限定理 |
| normal (Gaussian) distribution, bell curve | 正态（高斯）分布，钟形曲线 |
| convolution (of densities) | （密度的）卷积 |
| Berry–Esseen theorem, Kolmogorov distance | 贝里-埃森定理，柯尔莫哥洛夫距离 |
| covariance matrix, precision matrix | 协方差矩阵，精度矩阵 |
| conditioning, Schur complement | 条件化，舒尔补 |
| regression (Galton's), regression to the mean | （高尔顿的）回归，向均值回归 |
| Kalman filter, Gaussian process | 卡尔曼滤波，高斯过程 |
| bias (of an estimator), Bessel's correction | （估计量的）偏差，贝塞尔校正 |
| score (of a parameter), Fisher information | （参数的）分数，费希尔信息 |
| Cramér–Rao bound, efficient estimator | 克拉默-拉奥下界，有效估计量 |
| Cauchy distribution | 柯西分布 |
| natural gradient, elastic weight consolidation | 自然梯度，弹性权重巩固 |
| conjugate prior, Beta distribution | 共轭先验，贝塔分布 |
| rule of succession | 接续法则 |
| maximum a posteriori (MAP), weight decay | 最大后验（MAP），权重衰减 |
| maximum entropy, Lagrange multiplier | 最大熵，拉格朗日乘子 |
| exponential family, log-partition function | 指数族，对数配分函数 |
| Gibbs (Boltzmann) distribution | 吉布斯（玻尔兹曼）分布 |
| Markov's, Chebyshev's, Chernoff's, Hoeffding's inequality | 马尔可夫不等式，切比雪夫不等式，切尔诺夫界，霍夫丁不等式 |
| inverse-CDF sampling, rejection sampling | 逆累积分布函数采样，拒绝采样 |
| Box–Muller transform | 博克斯-穆勒变换 |
| Gumbel-max trick, Gumbel-softmax | 冈贝尔最大值技巧，冈贝尔-softmax |
| greedy decoding, top-k, top-p (nucleus), min-p | 贪心解码，top-k，top-p（核采样），min-p |
| stationary distribution, transition matrix | 平稳分布，转移矩阵 |
| detailed balance, reversible chain | 细致平衡，可逆链 |
| spectral gap, mixing time, relaxation time | 谱间隙，混合时间，弛豫时间 |
| importance sampling, effective sample size | 重要性采样，有效样本量 |
| score-function (log-derivative) estimator, baseline | 分数函数（对数导数）估计量，基线 |
| reparameterization trick | 重参数化技巧 |
| evolution strategies | 进化策略 |
| Metropolis–Hastings | 梅特罗波利斯-黑斯廷斯算法 |
| Langevin dynamics, MALA | 朗之万动力学，MALA |
| integrated autocorrelation time | 积分自相关时间 |
| Brownian motion, scaling limit | 布朗运动，标度极限 |
| quadratic variation | 二次变差 |
| Itô integral, Itô's lemma, Stratonovich integral | 伊藤积分，伊藤引理，斯特拉托诺维奇积分 |
| stochastic differential equation, Euler–Maruyama | 随机微分方程，欧拉-丸山方法 |
| strong / weak convergence order | 强 / 弱收敛阶 |
| Ornstein–Uhlenbeck process | 奥恩斯坦-乌伦贝克过程 |
| Fokker–Planck equation | 福克-普朗克方程 |
| reverse-time SDE | 反向时间SDE |
