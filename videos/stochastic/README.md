# Stochastic Calculus, Visualized: Brownian Motion, Itô's Lemma, and Why dW² = dt

A 49-minute, 15-chapter explainer in five parts that builds stochastic calculus from a coin
flip. **Brownian motion** comes first: the √Δt scaling, self-similarity, nowhere
differentiability, infinite length and the one rule (dW)² = dt. Then **the Itô
integral**: fair games, the left-endpoint rule, the "missing half" of
∫W dW = ½W² − ½t, and the Itô isometry. Then **Itô's lemma**, derived from Taylor's
theorem and shown at work in volatility drag. Then **equations of noise**: SDEs,
Euler–Maruyama, Ornstein–Uhlenbeck, Fokker–Planck, and Kolmogorov/Feynman–Kac.
Last come **two payoffs**: Black–Scholes and Girsanov's theorem.

The emphasis is on the mathematics: every result is derived on screen, one
line at a time. **Every path, histogram and number on screen is a seeded
simulation**: one Brownian path at 4,194,304 steps that the whole video keeps
coming back to, 40,000 Itô integrals, 10,000 players of a coin game, 3,000
particles in a double well beside a numerical Fokker–Planck solve, Brownian
walkers solving Laplace's equation in a disk, 5,000 simulated years of delta
hedging, and 2,000 reweighted paths. Each is asserted against the theory it
illustrates (see [Simulations](#simulations-computepy)). Schematics are labeled
`schematic`; the one enlarged illustrative step is labeled `one step, enlarged`.

**Watch:** [`published/stochastic.mp4`](../../published/stochastic.mp4) (1080p, subtitles and chapters embedded).

<details><summary>Chapters</summary>

- `0:00` A calculus for randomness
- `3:21` Part 1: From coin flips to Brownian motion
- `6:44` Continuous everywhere, smooth nowhere
- `9:33` The one rule: dW² = dt
- `12:59` Part 2: Integrating against noise
- `15:38` Where the missing half comes from
- `19:54` Fair games and the Itô isometry
- `22:32` Part 3: Itô's lemma: the chain rule, corrected
- `27:08` Growth, noise, and volatility drag
- `31:17` Part 4: Stochastic differential equations
- `34:39` From paths to densities: Fokker–Planck
- `37:51` Backwards: averages over paths solve PDEs
- `41:39` Part 5: Black–Scholes: hedging the noise away
- `45:04` Changing the odds: Girsanov's theorem
- `48:00` Recap

</details>

```bash
python -m videos.stochastic.compute          # once: every simulation (~1 min on 4 cores, cached in .cache/stochastic)
python tools/build.py stochastic -q l        # preview
python tools/build.py stochastic             # final 1080p30 + subtitles + chapters
python tools/export_script.py stochastic     # regenerate SCRIPT.md from the code
python tools/check_narration.py stochastic   # Whisper listen test of every narration line
python tools/publish.py stochastic           # GitHub-sized copy -> published/stochastic.mp4
```

## Outline

| # | Scene | What it establishes | Simulated on screen |
|---|---|---|---|
| 1 | `Hook` | Brown's jittering particles; Einstein's ⟨r²⟩ ∝ t. Brownian motion as the model of noise. The puzzle: Σ W ΔW on our path is 0.2847, but ½W₁² is 0.7847. The gap is 0.5000, and it stays ½ on five more paths. The plan. | A 2D particle with a trail; 2,000 particles spreading (mean squared displacement asserted linear); the hero path's left sum at 2²² steps; five more paths at 2¹⁶ steps. |
| 2 | `RandomWalk` | Var X_t = t·(Δx)²/Δt, so only Δx = √Δt gives a limit. The same coin flips scaled by Δt, √Δt, Δt^¼. CLT. W_t ~ N(0, t). The four defining properties; Wiener, Donsker. | Walks at n = 16…4,096; 20,000 walks of 64 flips; 200 Brownian paths with N(0, t) snapshots (68.3% / 95.5% inside ±√t / ±2√t). |
| 3 | `Roughness` | Zooming a smooth curve gives its tangent line. Zooming Brownian motion 4:4 makes it steeper; 4:2 makes it statistically the same (W_ct = √c W_t). Secant slopes ~ 1/√h. Total variation √(2n/π) → ∞, so Riemann–Stieltjes integration fails. | The hero path itself, zoomed 4⁵ = 1,024× in time (min/max decimation keeps the roughness); its secant slopes at h = 4⁻¹…4⁻⁷; its total variation at n = 16…2²². |
| 4 | `QuadraticVariation` | Squares on each increment, poured into a tank of capacity T. Smooth: Σ(Δf)² → 0. Brownian: Σ(ΔW)² → T. E = T and Var = 2TΔt (E Z⁴ = 3). The running sum lies on y = t. (dW)² = dt and the multiplication table. | The hero path's Σ(ΔW)² at n = 16…2²² (1.280 → 1.0000); Σ(ΔW)² on 4,000 fresh paths at n = 16, 256, 4,096 (sd asserted √(2/n)). |
| 5 | `ItoIntegral` | Noise isn't a function (ΔW/Δt spikes grow). The integral form of an SDE. Gambling: stake × move, with the future behind a curtain (adapted). ∫H dW as the limit of left-endpoint sums. | The hero path's slopes; the H = W strategy step by step; its winnings at n = 16…4,096 converging to 0.2847. |
| 6 | `MissingHalf` | Left / right / midpoint sums differ by Σ(ΔW)². The telescoping identity W_T² = 2∫W dW + T. The picture: every left-endpoint rectangle misses a triangle of area ½(ΔW)², and the triangles fill a tank of capacity ½T. Itô vs Stratonovich; only the left end is a fair game. Wong–Zakai. | The three sums at 2²² steps; the triangles of 16 and 256 steps, and their total at 2²² (0.5000). |
| 7 | `ItoRules` | E[∫H dW] = 0 (martingale). The isometry from the cross-term grid. A check with H = W: mean 0, variance ½, a hard left edge at −½; the naive ½W₁² averages ½. | 200 winnings paths and their mean; 40,000 Itô integrals (mean −0.0007, variance 0.505) against the exact density of (Z² − 1)/2. |
| 8 | `ItoLemma` | Taylor's theorem with ΔW ~ √Δt: which sums survive. For f = x³ the expansion is exact. df = f′dW + ½f″dt. Checks on W², W³, e^W. W² against ∫2W dW and ∫2W dW + t on our path. Convexity: the chord's midpoint sits ½f″h² above. The general form via (dX)² = σ²dt. | The three Taylor sums of W³ on the hero path at n = 16…2²² (cubic column → 0, middle → 3∫W dt = 0.338, total = W₁³ = 1.966 exactly); E[W_t²] = t over 200 paths. |
| 9 | `GeometricBM` | The ×1.5 / ×0.6 coin game: E grows 1.05ⁿ (131.5× after 100 rounds), the median shrinks 0.9^(n/2), and 87% of players lose. GBM; the naive solution fails Itô's check; d ln S gives S₀e^((μ−σ²/2)t+σW). Volatility drag: μ − ½σ² = −5.1% vs the game's ½ln 0.9 = −5.3%. | 10,000 players × 100 rounds (losers asserted against the exact binomial, 86.4%); a 10⁶-step Euler–Maruyama run vs both formulas (the naive one off by e^10.1 ≈ 25,000×); 4,000 GBM paths (87.6% below the start, exact 87.3%). |
| 10 | `SDEs` | dX = μdt + σdW as an integral equation. Euler–Maruyama, step by step. Ornstein–Uhlenbeck: the drift field, paths, the integrating-factor solution, mean and variance from the isometry, the stationary N(0, σ²/2θ). | 3,000 OU particles from X₀ = 2 with a live histogram against N(e^(−θt)X₀, σ²(1−e^(−2θt))/2θ) (asserted at t = ¼, 1, 4). |
| 11 | `FokkerPlanck` | The derivation with a test function and integration by parts. The heat equation; curvature arrows. The double well V = (x² − 1)²: hopping over the barrier, histogram vs PDE, the Boltzmann limit e^(−2V/σ²) from zero flux. | 4,000 Brownian particles; 3,000 particles in the double well over t ∈ [0, 40] (σ = 0.8) beside a finite-volume Fokker–Planck solve (both asserted to reach Boltzmann). |
| 12 | `FeynmanKac` | u(t, x) = E[g(X_T) \| X_t = x]. Gambler's ruin: P(top) = x, E τ = x(1 − x). The martingale argument gives Kolmogorov's backward equation, and discounting gives Feynman–Kac. Kakutani: walkers solve Δu = 0 in a disk with three hot and three cold arcs. | 4,000 exits from (0, 1) (29.5% vs 30%; 0.203 vs 0.21); 36 walker paths and 20,000 walk-on-spheres exits from one point (0.5328 vs exact 0.5340); Monte Carlo fields with 1–256 walkers per pixel vs the exact solution. |
| 13 | `BlackScholes` | The call payoff; Itô on V(t, S); Δ = V_S cancels the noise and μ; the PDE; Feynman–Kac and the closed form; replication; hedging error ∝ 1/√n. | The price 10.4506 vs 10⁶ risk-neutral paths (10.4512 ± 0.0147); one weekly-rebalanced replication; 5,000 years of hedging at 4/16/64/256 rebalances (sd 3.25 → 0.43). |
| 14 | `Girsanov` | Reweighting paths by Z = e^(θW − θ²/2) gives drift θ. The density-ratio derivation; Z is a martingale (Itô again). The risk-neutral measure θ = (r − μ)/σ. Importance sampling. | 2,000 paths drawn with opacity ∝ weight (effective sample size asserted > 300 at θ = 1.2); P(W₁ > 4): 1 hit in 10⁵ plain samples vs 3.24 × 10⁻⁵ ± 2% from 10⁴ tilted ones (exact 3.17 × 10⁻⁵). |
| 15 | `Outro` | Recap, while the hero path keeps zooming; the multiplication table; the history of the ideas. | |

## Color legend (consistent across every scene)

| Concept | Color |
|---|---|
| Brownian motion W, dW, the noise term σ dW | blue |
| time, dt, Δt | teal |
| (dW)², quadratic variation, Itô's correction ½f″dt, the missing half | yellow |
| drift μ, μ dt | green |
| the integrand H (stake, position, Δ) | lilac |
| the Itô integral, winnings | gold |
| left / right / midpoint (Stratonovich) sums | pale green / pale red / pink |
| densities, histograms, Fokker–Planck | orange |
| the mean | white |
| the median, typical growth | pale teal |
| option values | pale purple |
| the hedge portfolio | light brown |
| Girsanov weights | rose |
| boundary temperature 1 / 0 | amber / slate blue |

## Simulations (`compute.py`)

Every item is a NumPy simulation with its own seed (PCG64), cached in
`.cache/stochastic/<item>.npz`. The checks run every time the item is computed.
Numbers the narration quotes are also asserted in the scene code, where they
are used.

| Item | What | Checks |
|---|---|---|
| `hero` | One Brownian path on [0, 1] at 2²² = 4,194,304 steps (seed 174, picked by eye among the seeds that pass `hero_ok`, i.e. end in (0.9, 1.3) and stay on screen: 4, 87, 119, 140, 145, 152, 174, …); its left / right / midpoint sums, quadratic and total variation, and the three Taylor sums of W³, at n = 4…2²² | Exact identities at every n: left = ½W² − ½Q, right = ½W² + ½Q, mid = ½W², the Taylor sums add to W³. Q(2²²) = 1.00002; the cubic sum → 0; the middle one → 3∫W dt |
| `others` | Five more paths at 2¹⁶ steps | ½W₁² − Σ W ΔW within 0.02 of ½ on each |
| `walk` | Coin-flip walks at n = 16…4,096; 20,000 walks of 64 flips | mean ≈ 0, variance ≈ 1 |
| `fan` | 200 paths at 512 steps; 20,000 samples of W at t = ¼, ½, 1 | Var = t; 68.3% within ±√t, 95.5% within ±2√t |
| `hook2d` | One 2D particle; 2,000 particles diffusing | ⟨r²⟩ = 2·(0.12)²·k within 8% |
| `qv` | Σ(ΔW)² on 4,000 fresh paths at n = 16, 256, 4,096 | mean 1; sd within 6% of √(2/n) |
| `ito_mc` | 40,000 left-endpoint integrals ∫₀¹ W dW at n = 1,000 | mean within 3 sd of 0; variance within 0.02 of ½; the naive ½W₁² averages ½ |
| `coin` | 10,000 players × 100 rounds of ×1.5 / ×0.6 | share of losers within 1% of the exact binomial P(heads ≤ 55) = 86.4% |
| `gbm` | One path at 10⁶ Euler–Maruyama steps vs the naive and Itô solutions; 4,000 exact GBM paths (μ = 0.05, σ = 0.45, T = 100) | EM within 0.05 (in log) of Itô's formula; the naive formula off by > e⁹; share below the start within 2.5% of Φ(−(μ − σ²/2)T/σ√T) |
| `ou` | 3,000 Ornstein–Uhlenbeck particles (θ = σ = 1, X₀ = 2), Euler–Maruyama | mean and variance at t = ¼, 1, 4 against the exact formulas |
| `heat` | 4,000 Brownian particles from 0 | Var X₁ = 1 |
| `well` | 3,000 particles in V = (x² − 1)², σ = 0.8, t ≤ 40; Fokker–Planck by finite volumes (upwind drift, central diffusion, zero-flux walls) | the PDE conserves mass and ends within 0.03 (total variation) of Boltzmann; the particles within 0.06 |
| `exit` | 4,000 Brownian paths from 0.3 until they leave (0, 1), Δt = 10⁻⁵ | P(top) within 3 se of 0.3; E τ within 0.01 of 0.21 |
| `disk` | 36 walker paths (small Euler steps); 20,000 walk-on-spheres exits from z₀ = (0.32, 0.2); Monte Carlo fields at 1…256 walkers per pixel on a 160 × 160 grid | the mean at z₀ within 3 se of the exact ½ + arctan(2r³ sin 3θ / (1 − r⁶))/π; mean field error at 256 walkers < 0.03 |
| `hedge` | Black–Scholes (S₀ = K = 100, r = 0.05, σ = 0.2, T = 1); 10⁶ risk-neutral payoffs; delta hedging under μ = 0.10 at 4, 16, 64, 256 rebalances × 5,000 paths; one weekly path | MC within 3 se of the formula; sd ratios within 0.35 of 2 per 4× rebalancing |
| `girsanov` | 2,000 paths at 256 steps; 10⁵ plain and 10⁴ tilted samples of W₁ | weighted means of W₁ within 0.12 of θ ∈ {0.5, 1, 1.2, −1}, effective sample size > 300; the importance-sampling estimate within 3 se of Φ(−4) |

## Fact-check notes and sources

The mathematics is standard; the derivations follow the usual textbook
arguments (e.g. Øksendal, *Stochastic Differential Equations*; Shreve,
*Stochastic Calculus for Finance II*; Karatzas & Shreve, *Brownian Motion and
Stochastic Calculus*). Historical claims:

* **Robert Brown** observed the motion of particles from pollen grains (of *Clarkia pulchella*) in water in 1827 (published 1828).
* **Louis Bachelier**, *Théorie de la spéculation* (1900): Brownian motion as a model of prices on the Paris Bourse.
* **Albert Einstein** (1905): mean squared displacement ∝ t and the diffusion equation; **Jean Perrin**'s experiments (1908–1909) confirmed it and measured Avogadro's number.
* **Paul Langevin** (1908): the first stochastic differential equation, for the velocity of a Brownian particle.
* **Norbert Wiener**, *Differential space* (1923): a rigorous construction of Brownian motion.
* **Adriaan Fokker** (1914), **Max Planck** (1917); **Andrey Kolmogorov** (1931): the forward and backward equations.
* **Leonard Ornstein and George Uhlenbeck**, *On the theory of the Brownian motion* (1930).
* **Kiyosi Itô**, *Stochastic integral* (1944) and *On a formula concerning stochastic differentials* (1951).
* **Shizuo Kakutani**, *Two-dimensional Brownian motion and harmonic functions* (1944).
* **Robert Cameron and William Martin** (1944) and **Igor Girsanov** (1960): changes of measure for Brownian motion.
* **Mark Kac**, *On distributions of certain Wiener functionals* (1949), inspired by Richard Feynman's path integrals (1948).
* **Monroe Donsker** (1951): the invariance principle (rescaled random walks converge to Brownian motion).
* **Eugene Wong and Moshe Zakai** (1965): smooth approximations of noise converge to Stratonovich integrals; **Ruslan Stratonovich** (1966).
* **Fischer Black and Myron Scholes**, *The pricing of options and corporate liabilities*, and **Robert Merton**, *Theory of rational option pricing* (both 1973).

On-screen simplifications, stated here for the record:

* "Itô integrals of adapted strategies are martingales" assumes the usual square-integrability (E∫H²dt < ∞).
* The coin-game "median" line is the continuous 0.9^(n/2); the true median of the discrete game moves in steps (it equals 0.9⁵⁰ exactly at n = 100).
* The double-well particles are drawn slightly above the potential curve, so the glow doesn't hide it. The heat-equation particles are spread vertically only for visibility (labeled on screen).
* The molecular-kick picture in chapter 1 is a schematic (labeled). The Euler–Maruyama walkthrough in chapter 10 is a real computation: eight steps of the OU equation with seeded kicks.
