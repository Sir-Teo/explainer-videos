# Quant, Built — Part 5: Stochastic Calculus

Part 5 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act II, the Mathematical Toolkit. It assumes the gentle introduction in
[`videos/math/stochastic`](../../math/stochastic/) (Brownian motion, Itô's lemma, Black–Scholes) and goes past it: the
constructions, the proofs and the working tools of a graduate course in stochastic calculus, each one checked by a
simulation whose numbers come from [`compute.py`](compute.py) and the House's
[`sim`](../../../explainer/quant/house/sim.py) library. About 57 minutes, eighteen chapters.

*An education in methods, not investment advice.*

## Build it

```bash
python -m videos.quant.quant5.compute                     # every number, cached in .cache/quant5/ (about 40 CPU-minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant5 Lemma # one chapter, silent, with a contact sheet
python tools/make.py quant5 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
.venv/bin/python -m pytest -q tests/test_quant_house.py   # the House's tests (Rule 6)
```

## Chapters (about 62 minutes)

| # | Chapter (module) | What is shown, built or computed |
|---|---|---|
| — | A hedge that cannot lose, and does (`s01_hook`) | The stop-loss start-gain hedge of a call (K = 100, σ = 20%, 1 year) loses 7.90, 8.10, 7.98, 8.00, 7.94 on 4,000 paths at 13…4,000 rebalances: the call's price, 7.97. How we got here (Bachelier 1900 → negative oil 2020); objectives; the House. |
| 1 | Building Brownian motion (`s11_construct`) | Donsker with three step laws from the same random numbers; Lévy's midpoint construction to level 10 (bridge variance 0.251 against ¼); the reflection principle derived; P(max ≥ 1) = 0.3038 on 20,000 paths of 1,000 steps against 2(1 − Φ(1)) = 0.3173 and the Broadie–Glasserman–Kou shifted barrier 0.3085; the arcsine law (41% of paths spend < 10% or > 90% of the time above zero, 13% between 40% and 60%). |
| 2 | Quadratic variation, accumulating (`s02_brownian`) | Three running sums drawn live on one path and refined from 16 to 4,096 steps; the L² proof; the QV estimate's spread against √(2/n) on 4,000 paths; Bitcoin's 2020 signature plot (80% at one minute, 71% at one day) and the implied microstructure noise, 3.5 basis points a tick. |
| 3 | Constructing the Itô integral (`s03_ito`) | The integral as a ledger of bets; the isometry and martingale property proved; completion; left against midpoint sums (−0.330 and +0.170); Stratonovich's conversion; Wong–Zakai on 20,000 paths: the smoothed ODE gives E X₁ = 1.674 ± 0.016 (e^½ = 1.649), Euler's Itô scheme 1.015 ± 0.010. |
| 4 | Itô's lemma, proved (`s12_lemma`, 3D) | A Brownian path lifted onto z = x²e^{−t/4}; the misses above the tangent plane stack to 0.928 against ½∫f_xx = 0.885; with ρ = −0.7 and f = xy they stack to −0.693 (the covariation, −0.7); the proof; the multivariate lemma and the product rule; GBM's drag (E log S₁ = 0.021 against μ − σ²/2 = 0.020); Lévy's characterization, Dambis–Dubins–Schwarz; E W₁⁴ = 3.013. |
| 5 | SDEs: existence and simulation (`s13_schemes`) | Picard iteration on one path (gaps 1.13 → 0.011 in four rounds, 1.7·10⁻⁶ in nine); Itô's 1951 theorem; strong against weak solutions; **lab**: `euler_maruyama`, `milstein`; Milstein's term derived; strong orders 0.50 and 0.93, weak 0.99 and 1.00. MLMC in one line (Part 16). |
| 6 | Mean reversion: solved and fitted (`s04_meanrev`) | **Lab**: `ou_exact`, 200 paths from 1954's bill rate (terminal mean 4.09%, sd 3.18%, 10% below zero); OU solved by an integrating factor; CIR's non-central χ² law and Feller's test (regression: ν = 0.58); **replay**: exact MLE on DTB3 from five starts, log-likelihood 3,635.3 against 3,633.3 for the regression; ν = 0.99. |
| 7 | From paths to PDEs (`s14_pde`, 3D) | The CIR density surface over a path fan (Feller's wall at ν = 0.58, the pinch at ν = 2; L¹ 0.038 against 20,000 exact paths); Fokker–Planck derived; Feynman–Kac proved; Vasicek's bond ODEs; Monte Carlo 0.8717 ± 0.0012 against the closed form 0.8709; the model's 10-year yield 1.38% against the actual 0.93% (Dec. 2020); Dynkin: E τ = 2.013 ± 0.013 for (−1, 2). |
| 8 | Girsanov: re-weighting paths (`s05_girsanov`) | 300 paths re-weighted and recoloured by Z, against the same paths moved (weighted mean endpoint 0.998 for θ = 1); the proof from Part 4's coin through the product rule and Lévy; Novikov; effective sample size 0.78, 0.36, 0.025, 0.0003 at T = 1, 4, 16, 64 against e^{−θ²T}, and the weights' mean falling to 0.75. |
| 9 | Girsanov at work (`s15_sampling`) | **Lab**: `is_digital` (0.00707 ± 0.00008 against exact 0.00714; plain 0.0074 ± 0.0006; variance ÷52), the two estimates racing; one year of one-minute GBM: σ̂ sd 0.0002, μ̂ sd 0.18 over 200 years; why prices depend on σ and not on μ. |
| 10 | Martingale representation (`s16_representation`) | E[W₁² ∣ 𝓕_t] and the hedge 2W at n = 8 and 512; the proof through exponentials; Clark–Ocone; hedge-error slopes −0.50 (W²), −0.49 (a call), −0.02 (a second noise: the market is incomplete). |
| 11 | Local time and Tanaka (`s06_localtime`) | Tanaka derived by smoothing the kink (ε shrinking live); the occupation sandpile; E L₁⁰ = 0.792 (occupation) and 0.796 (Tanaka) against √(2/π) = 0.798; Carr–Jarrow; shortfall against ½L^K, correlation 0.97. |
| 12 | Jumps: Poisson to Lévy–Itô (`s07_jumps`) | The Poisson clock and its compensator; compound Poisson checked on 50,000 paths; the Lévy–Itô layer cake of a tempered stable path (2 → 1,183 small jumps as ε goes from 0.3 to 0.005); Lévy–Khintchine checked (max error 0.011); Itô for jumps; Merton. |
| 13 | Jumps in data, and the hedge they break (`s17_jumpdata`) | Bipower variation derived; Bitcoin 2018–2020: 204 hours beyond 5 local sd against 0.015 expected, 24% of the variance; a delta hedge on 10,000 Merton paths: no-jump error slope −0.49, the jump error stalls at 2.66 (24× the no-jump error at 4,000 rebalances). |
| 14 | Hawkes: jumps that cause jumps (`s18_hawkes`) | **Lab**: Ogata's thinning, candidates shown (mean count 1,312 against 1,333); the branching tree (mean family 3.43 against 3.33); **replay**: the Bitcoin fit from eight starts (n = 0.36, half-life 7.6 h; log-likelihood −506 against −588); time-rescaling: KS p = 0.83 for Hawkes, 6·10⁻¹⁴ for Poisson. |
| 15 | Fractional Brownian motion (`s08_rough`) | The H dial (one random vector, H from 0.95 to 0.05); Mandelbrot–Van Ness; p-variation; not a semimartingale (Rogers); **lab**: `fbm` (Davies–Harte); Bitcoin H ≈ 0.15; the Cont–Das caveat computed: a smooth OU log-volatility gives Ĥ = 0.26 from the true variance and 0.24 from noisy 5-minute RV. |
| 16 | Rough paths and signatures (`s19_signature`, 3D) | Lyons' helix (‖X‖ = 1/n → 0, Y³₁ → 1); Chen's identity, the shuffle product, universality; **lab**: `signature`; **replay**: ridge regression on signatures of 20,000 two-asset paths, depth 1–5: the average and the Lévy area exact at depth 2 (R² = 1.000; the raw path explains 0.4% of the area), the Asian call 0.618 → 0.980 at depth 4, 0.951 at depth 5 (overfitting), against 0.795 for the raw path. |
| 17 | Industry (`s20_industry`) | Crisis file: WTI, 20 April 2020; GBM against Bachelier; CME's switch; firm file: Interactive Brokers and the CFTC; OCC's STANS Monte Carlo margin; the variance swap as Itô's lemma (Heston replication sd 1.2 and 0.11 in 10⁻⁴; the jump bias −17.1 against −16.8 predicted); SR 11-7 → SR 26-2; the House's validation report. |
| 18 | Frontier (`s21_frontier`) | **Replay**: a neural SDE trained on Bitcoin by expected-signature matching, three seeds; scored on the 2020 hold-out against GBM and a bootstrap (see the numbers below); the 2023–2026 papers. |
| R | For the researcher (`s22_research`) | The CLT for realized variance (Jacod; Barndorff-Nielsen–Shephard), proved by the martingale CLT; on 3,000 simulated stochastic-volatility days the studentized 95% interval covers 89% at 10-minute sampling, 92% at 5, 94% at 1 minute and 95% at 10 and 1 seconds; the error falls from 27% to 1.1%. Noise of 5 bp: $E\,\mathrm{RV} = \mathrm{IV} + 2n\omega^2$ matches simulation to three digits (42.9 times the truth at 1 second, +14% at 5 minutes); TSRV 0.99 ± 0.13. Bipower variation and the Huang–Tauchen test: 10.5% false alarms at a nominal 5%, 51% power against one 1% jump. Three open problems. |
| — | Outro (`s10_outro`) | Recap, three desk questions, nine problems (two at qualifying-exam level), where it comes back, references, the House. |

Hands-on: six labs (`euler_maruyama`/`milstein`, `ou_exact`, `is_digital`, `hawkes_thinning`, `fbm`, `signature`),
four replays (CIR MLE, Hawkes MLE, signature regression, the neural SDE), three 3D scenes (the lemma's tangent planes,
the Fokker–Planck surface, Lyons' helix).

## Textbook audit

| Book · section | Where |
|---|---|
| Shreve II 3.2–3.4 (scaled walks, BM, QV, volatility of GBM) | ch. 1, 2 |
| Shreve II 3.5–3.7 (Markov, first passage, reflection) | ch. 1 (reflection, first passage), ch. 7 (Markov through the generator) |
| Shreve II 4.2–4.3 (Itô integral) | ch. 3 |
| Shreve II 4.4, 4.6 (Itô–Doeblin, multivariable, Lévy's characterization) | ch. 4 |
| Shreve II 4.5 (BSM) | Part 10 |
| Shreve II 4.7 (Brownian bridge) | ch. 1 (Lévy's construction is the bridge) |
| Shreve II 5.2–5.3 (Girsanov, martingale representation) | ch. 8, 9, 10 |
| Shreve II 5.4–5.6 (fundamental theorems, dividends, forwards) | Part 9 |
| Shreve II 6.2–6.5 (SDEs, Markov, interest-rate models, multidimensional FK) | ch. 5, 6, 7; rate models → Part 19 |
| Shreve II 7–10 (exotics, American, numéraire, term structure) | Parts 15, 8/10/16, 9/19/22, 19 |
| Shreve II 11.2–11.5 (Poisson, compound Poisson, jump integrals, Itô for jumps) | ch. 12 |
| Shreve II 11.6–11.7 (change of measure for jumps; a call with jumps) | ch. 13 (Esscher, incompleteness); Part 13 |
| Øksendal 2 (construction, Kolmogorov extension and continuity) | ch. 1 (Lévy's construction; Kolmogorov–Chentsov named) |
| Øksendal 3 (Itô integral, Stratonovich) | ch. 3 |
| Øksendal 4 (Itô formula, martingale representation) | ch. 4, 10 |
| Øksendal 5 (existence and uniqueness; weak and strong) | ch. 5 |
| Øksendal 6 (filtering) | Part 7 (state-space models) |
| Øksendal 7 (diffusions, generator, Dynkin) | ch. 7 |
| Øksendal 8 (Kolmogorov backward, Feynman–Kac, time change, Girsanov) | ch. 7, 4 (Dambis–Dubins–Schwarz), 8 |
| Øksendal 9 (Dirichlet problems) | the gentle `stochastic` video; Dynkin in ch. 7 |
| Øksendal 10–12 (optimal stopping, control, finance) | Parts 8, 9–10 |
| Karatzas–Shreve 1 (martingales, Doob–Meyer) | Part 4 |
| Karatzas–Shreve 2 (BM: construction, strong Markov, reflection, arcsine) | ch. 1 |
| Karatzas–Shreve 3.1–3.4 (integration, change of variables, representation, time change) | ch. 3, 4, 10 |
| Karatzas–Shreve 3.5 (Girsanov, Novikov) | ch. 8 |
| Karatzas–Shreve 3.6–3.7 (local time, Tanaka, Lévy's identity) | ch. 11 |
| Karatzas–Shreve 4 (BM and PDEs, FK) | ch. 7 |
| Karatzas–Shreve 5 (strong and weak solutions, Feller's test, linear SDEs) | ch. 5, 6 |
| Karatzas–Shreve 6 (Lévy's theory of local time, excursions) | ch. 11 (Lévy's identity); excursion theory is not core to finance and is left to the book |
| Cont–Tankov 2–3 (Poisson, compound Poisson, Poisson random measures, Lévy–Itô, Lévy–Khintchine) | ch. 12 |
| Cont–Tankov 4–5 (building Lévy processes, multidimensional) | Part 13 |
| Cont–Tankov 6 (simulation) | ch. 12 (compound Poisson, series truncation); Part 16 |
| Cont–Tankov 7 (Lévy processes and returns) | ch. 13 |
| Cont–Tankov 8 (stochastic calculus for jumps, Esscher) | ch. 12, 13 |
| Cont–Tankov 9–10 (pricing, incompleteness, quadratic hedging) | ch. 13 (incompleteness, computed); Parts 11, 13 |
| Björk 4–5 (stochastic integrals, SDEs, generator, Kolmogorov, FK) | ch. 3, 4, 5, 7 |
| Friz–Hairer 1–3 (rough paths, BM as a rough path) | ch. 16; deeper in Part 14 |
| Friz–Hairer 8+ (RDEs, regularity structures) | beyond the series |

## Papers

Every paper on Part 5's list in [`READING.md`](../READING.md) appears on screen: Wiener (1923, hook); Itô (1944, ch. 3;
1951, ch. 5); Cameron–Martin (1944, ch. 8); Kac (1949, ch. 7); Girsanov (1960, hook and ch. 8); Stratonovich (1966,
ch. 3); Mandelbrot–Van Ness (1968, ch. 15); Hawkes (1971, ch. 14); Ogata (1981, ch. 14 lab); Carr–Jarrow (1990,
ch. 11); Chen (1957, ch. 16); Lyons (1998, ch. 16); Chevyrev–Kormilitzin (2016, the reference card; the reading guide:
the gentlest introduction to signature features). Added this pass, all on screen: Bachelier (1900), Lévy (1948),
Donsker (1951), Feller (1951), Tanaka (1963), Wong–Zakai (1965), Dambis–Dubins–Schwarz (1965), Clark (1970), Novikov
(1972), Merton (1976), Vasicek (1977), Ocone (1984), Cox–Ingersoll–Ross (1985), Broadie–Glasserman–Kou (1997), Rogers
(1997), Demeterfi–Derman–Kamal–Zou (1999), Barndorff-Nielsen–Shephard (2004), Hardiman–Bercot–Bouchaud (2013),
Gatheral–Jaisson–Rosenbaum (2018); the frontier (Issa et al. 2023; Cuchiero et al. 2025; Walker et al. 2024; Cont–Das
2024; Guyon–Lekeufack 2023; *Rough Volatility*, SIAM 2023; *Signature Methods in Finance*; Cass–Salvi 2024; Degenne et
al. 2025; Gierjatowicz et al.; Kidger et al. 2021).

Industry sources, checked against the primary documents: CFTC press release 8432-21 (28 September 2021: $1.75 million
penalty, $82.57 million restitution credited, the May WTI contract's −$37.63 settlement); Interactive Brokers' press
release of 21 April 2020 (provisional loss ≈ $88 million) and Form 10-Q for Q2 2020 (≈ $104 million); CME Clearing
Advisories 20-152, 20-171 (Bachelier from the 22 April 2020 margin cycle, for negative prices and strikes) and 20-320
(back to Black-76/Whaley from 31 August 2020); SEC Release No. 34-90763 (2020) on OCC's STANS ("large-scale Monte
Carlo simulations", 10,000 scenarios per risk factor); FRED DCOILWTICO (−36.98 on 20 April 2020); SR 11-7 (2011) and
SR 26-2 (Fed, OCC and FDIC, 17 April 2026). Adjoint Greeks (Giles–Glasserman 2006, Danske Bank) and STAC-A2 belong to
Part 16, MLMC and the optimal importance-sampling shift too.

## Desk questions, with solutions

1. **Expected exit time from (−a, b).** By Dynkin's formula with f = x² (𝓛f = 1), E W_τ² = E τ. The exit point is b
   with probability a/(a + b) and −a with probability b/(a + b), so E τ = b²·a/(a + b) + a²·b/(a + b) = ab. For
   (−1, 2): 2 (simulated 2.013 ± 0.013).
2. **Hit +1 before −2.** W is a martingale, and stopped at the first exit from (−2, 1) it is bounded. By optional
   stopping, 1·p − 2(1 − p) = 0, so p = 2/3.
3. **A digital by Girsanov.** The price is e^{−rT} E_Q[1{S_T > K}]. Under Q, by Girsanov,
   log S_T = log S₀ + (r − σ²/2)T + σW̃_T, so Q(S_T > K) = N(d₂) and the price is e^{−rT}N(d₂). Under P the same event
   has probability N(d₂ with μ in place of r): the drift changes, the volatility doesn't.

## Problems, with solutions

1. **Variations.** Each ΔW is N(0, 1/n). Then E|ΔW| = √(2/(πn)), so E Σ|ΔW| = n√(2/(πn)) = √(2n/π) → ∞. Also
   E(ΔW)² = 1/n and Var((ΔW)²) = 2/n², so Σ(ΔW)² has mean 1 and variance 2/n → 0.
2. **∫W dW.** Left points: Σ W_k ΔW_k = ½Σ(W²_{k+1} − W²_k) − ½Σ(ΔW_k)² → ½(W_T² − T). Midpoints in time:
   Σ W_{k+½}ΔW_k = ½(W_T² − T) + Σ(W_{k+½} − W_k)ΔW_k, and the last sum tends to ½T, giving ½W_T². Only the Itô
   integral ½(W_T² − T) is a martingale in T: its mean is zero for every T.
3. **Milstein.** Over one step, X_{t+h} − X_t = ∫a ds + ∫b(X_s) dW_s, and b(X_s) ≈ b(X_t) + b'b(X_t)(W_s − W_t) by Itô
   to first order. So ∫_t^{t+h} b(X_s) dW_s ≈ b ΔW + b'b ∫(W_s − W_t)dW_s = b ΔW + ½ b'b (ΔW² − h).
4. **Vasicek.** r_T = θ + (r₀ − θ)e^{−κT} + σ∫e^{−κ(T−s)}dW_s is Gaussian, with mean θ + (r₀ − θ)e^{−κT} and variance
   σ²(1 − e^{−2κT})/(2κ). In the long run it is N(θ, σ²/2κ): sd 0.014/√0.197 = 3.2%, so P(r < 0) = N(−4.1/3.2) ≈ 10%,
   as the lab's 200 paths show (10% below zero).
5. **Hawkes.** In stationarity E[λ] = μ + (α/β)E[λ], so the rate is μ/(1 − α/β) = 0.1/(1 − 0.4) ≈ 0.167 a day. Each
   event triggers α/β = 0.4 children on average, so a fraction 0.4 of all events are triggered by earlier ones (the
   cluster size is 1/(1 − 0.4)).
6. **E τ_a = ∞.** P(τ_a < ∞) = lim_{T→∞} 2(1 − Φ(a/√T)) = 1. But f(t) = a(2πt³)^{−½}e^{−a²/2t} ~ a(2π)^{−½}t^{−3/2}
   for large t, so E τ_a = ∫ t f(t) dt diverges like ∫ t^{−1/2} dt.
7. **Clark–Ocone for W_T³.** D_tW_T³ = 3W_T², so H_t = E[3W_T² ∣ 𝓕_t] = 3(W_t² + T − t). Check: by Itô,
   W_T³ = ∫3W²dW + ∫3W dt, and ∫_0^T W_t dt = ∫_0^T (T − t) dW_t (integration by parts), so
   W_T³ = ∫_0^T 3(W_t² + T − t) dW_t, with mean zero as it should be.

8. **(qual) Realized variance's CLT.** With deterministic $\sigma$, $\Delta_iX \sim N(0, v_i)$ independently,
   $v_i = \int_{(i-1)/n}^{i/n}\sigma^2$. Then $\xi_i = (\Delta_iX)^2 - v_i$ are independent, mean zero, $\operatorname{Var}
   \xi_i = 2v_i^2$, and $n\sum 2v_i^2 \to 2\int\sigma^4$ (a Riemann sum, $v_i \approx \sigma^2_{i/n}/n$). Lyapunov's
   condition holds since $E\xi_i^4 = 60v_i^4$, so $\sum E\xi_i^4/(\sum 2v_i^2)^2 = O(1/n) \to 0$; hence
   $\sqrt n(\mathrm{RV}_n - \mathrm{IV}) \Rightarrow N(0, 2\int\sigma^4)$.
9. **(qual) Noise.** $\mathrm{RV}_n(Y) = \mathrm{RV}_n(X) + 2\sum\Delta_iX\,\Delta_i\varepsilon + \sum(\Delta_i\varepsilon)^2$.
   The middle term has mean zero (independence), and $E\sum(\varepsilon_i - \varepsilon_{i-1})^2 = 2n\omega^2$, so
   $E\,\mathrm{RV}_n(Y) = \mathrm{IV} + 2n\omega^2$. Dividing by $2n$, the first two terms vanish and the last is an
   average of a 1-dependent stationary sequence with mean $2\omega^2$, so the law of large numbers gives
   $\mathrm{RV}_n(Y)/2n \to \omega^2$: the noise variance is estimable from the finest data, which TSRV uses.

**The pause question of the research chapter.** $\operatorname{se} = \sqrt{2\,\mathrm{RQ}/n} = \sqrt{2 \times 2.4 \times
10^{-7}/78} = 7.8 \times 10^{-5}$, so IV $\in [2.5, 5.5] \times 10^{-4}$, a daily volatility between 1.6% and 2.4%
(point estimate 2.0%).

## For the researcher

* **The theorems.** Jacod (1994) and Barndorff-Nielsen and Shephard (2002) for the CLT, stable convergence (Jacod and
  Shiryaev, ch. IX); Barndorff-Nielsen and Shephard (2004) for bipower variation; Huang and Tauchen (2005); Zhang,
  Mykland and Aït-Sahalia (2005) for TSRV; Barndorff-Nielsen, Hansen, Lunde and Shephard (2008) for realized kernels;
  Jacod, Li, Mykland, Podolskij and Vetter (2009) for pre-averaging; Aït-Sahalia and Jacod, *High-Frequency
  Financial Econometrics* (2014).
* **Simplifications.** The proof sketch assumes no drift (it is negligible at the $\sqrt n$ scale) and continuous
  paths; the jump test's false-alarm rate here is inflated by the intraday volatility pattern, which robust versions
  correct.
* **Open problems.** Efficient estimation under endogenous, autocorrelated noise and irregular times; spot volatility
  when volatility is rough; volatility jumps and co-jumps.

## Data and reproducibility

* Binance BTCUSDT one-minute candles for 2019–2020 (and 2020 for the signature plot) and one-hour candles for
  2018–2020, each monthly file checked against Binance's SHA-256; Bitcoin's daily returns for the neural SDE are the
  hourly closes at 00:00 UTC.
* FRED DTB3 (3-month bill), 1954–2020; DGS10 read for one date; **DCOILWTICO (Cushing WTI spot), March–May 2020: one
  new entry in `videos/quant/data/manifest.json`, fetched and checksummed by `explainer/quant/data.py`.**
* Registered with the trial counter: the Hawkes fit, the rough-volatility Hurst estimate, the CIR exact MLE and the
  neural SDE (its 2020 hold-out is inside the research window).
* Compute: about 40 CPU-minutes in all (the neural SDE, three seeds of 1,000 steps, is most of it; it resumes from its
  partial file if killed).

---

# 量化金融，从零搭建 — 第5部分：随机微积分

本部分以系列入门篇《随机微积分可视化》为前提，并走得更远：研究生随机微积分课程中的构造、证明与实用工具，每一样都用模拟检验，所有数字都由
[`compute.py`](compute.py)和我们公司的[`sim`](../../../explainer/quant/house/sim.py)函数库算出。约57分钟，18章。

*讲的是方法，不构成投资建议。*

## 各章内容（约57分钟）

* **开场：一个不会亏、却亏了的对冲。** 止损–启动对冲在四千条路径上每次亏约8美元，恰好是看涨期权的价格7.97；历史脉络；本部分目标。
* **1. 构造布朗运动。** 三种步长分布的唐斯克极限；列维中点构造（布朗桥方差0.251对¼）；反射原理的推导与检验（0.3038对0.3173，平移障碍0.3085）；反正弦定律。
* **2. 二次变差的累积。** 三个累计和在一条路径上实时画出；L²证明；比特币2020年的波动率签名图与反推出的微观结构噪声（每个报价约3.5个基点）。
* **3. 构造伊藤积分。** 下注账本；等距性与鞅性质的证明；左端点与中点之和；斯特拉托诺维奇转换；王–扎凯定理（平滑方程1.674，伊藤格式1.015）。
* **4. 伊藤引理的证明（三维）。** 切平面之上的偏差累积成½∫f_xx；多元引理与乘积法则；波动率拖累；列维刻画；E W₁⁴ = 3.013。
* **5. 随机微分方程。** 皮卡迭代；强解与弱解；**实验**：欧拉–丸山与米尔斯坦；强阶0.50与0.93。
* **6. 均值回复。** **实验**：精确的OU模拟；积分因子求解；CIR与费勒检验；**训练回放**：CIR精确最大似然（五个起点，费勒比率0.99）。
* **7. 从路径到偏微分方程（三维）。** 福克–普朗克曲面与费勒墙；福克–普朗克推导；费曼–卡茨证明与蒙特卡洛检验（0.8717对0.8709）；戴金公式（2.013）。
* **8. 吉尔萨诺夫：给路径重新加权。** 路径不动、权重变；证明；诺维科夫条件；有效样本量随期限崩塌。
* **9. 吉尔萨诺夫的应用。** **实验**：重要性抽样的数字期权（方差缩小52倍）；波动率可观测而漂移不可观测。
* **10. 鞅表示。** 对冲财富追踪鞅；通过指数函数的证明；克拉克–奥科内公式；第二个噪声下对冲误差不再缩小（斜率−0.02）。
* **11. 局部时与田中公式。** 磨圆尖角的推导；占位沙堆；E L₁⁰ = 0.79；卡尔–贾罗悖论的化解（相关系数0.97）。
* **12. 跳跃。** 泊松时钟与补偿子；列维–伊藤分层；列维–辛钦公式的检验；跳跃的伊藤公式；默顿模型。
* **13. 数据中的跳跃。** 双幂次变差；比特币204个超过5倍局部标准差的小时；跳跃使delta对冲误差停在一个下限。
* **14. 霍克斯过程。** **实验**：小形稀疏法；家谱；**训练回放**：比特币拟合（分支比0.36）；时间重标检验（霍克斯p = 0.83，泊松被拒绝）。
* **15. 分数布朗运动。** H旋钮；曼德布罗特–范内斯表示；不是半鞅；**实验**：戴维斯–哈特；比特币H ≈ 0.15；孔特–达斯的保留意见（光滑OU也给出0.26）。
* **16. 粗糙路径与签名（三维）。** 莱昂斯螺旋；陈恒等式；**实验**：签名函数；**训练回放**：签名回归（亚式期权R²在深度4达到0.980）。
* **17. 业界。** 2020年4月的负油价与巴舍利耶模型；盈透证券与美国商品期货交易委员会；期权清算公司的蒙特卡洛保证金；作为伊藤引理的方差互换；SR 11-7到SR 26-2。
* **18. 前沿。** **训练回放**：用期望签名训练的神经随机微分方程，在2020年样本外与几何布朗运动和自助重抽样比较；2023–2026年的论文。

## 交易台问题与解答

1. **离开(−a, b)的期望时间。** 由戴金公式取f = x²（𝓛f = 1），E W_τ² = E τ。离开点以a/(a + b)的概率为b、以b/(a + b)的概率为−a，
   所以E τ = b²·a/(a + b) + a²·b/(a + b) = ab。对(−1, 2)为2（模拟2.013 ± 0.013）。
2. **先碰到+1再碰到−2的概率。** W是鞅，在首次离开(−2, 1)时停止后有界；由可选停止，1·p − 2(1 − p) = 0，p = 2/3。
3. **用吉尔萨诺夫为数字期权定价。** 价格为e^{−rT} E_Q[1{S_T > K}]。在Q下log S_T = log S₀ + (r − σ²/2)T + σW̃_T，所以Q(S_T > K) = N(d₂)，
   价格为e^{−rT}N(d₂)。在P下同一事件的概率是把r换成μ的N(d₂)：漂移变了，波动率不变。

## 习题与解答

1. **变差。** 每个ΔW服从N(0, 1/n)：E|ΔW| = √(2/(πn))，所以E Σ|ΔW| = √(2n/π) → ∞；E(ΔW)² = 1/n、Var((ΔW)²) = 2/n²，
   所以Σ(ΔW)²的均值为1、方差为2/n → 0。
2. **∫W dW。** 左端点：Σ W_k ΔW_k = ½Σ(W²_{k+1} − W²_k) − ½Σ(ΔW_k)² → ½(W_T² − T)。时间中点：额外的和Σ(W_{k+½} − W_k)ΔW_k趋于½T，
   结果为½W_T²。只有伊藤积分½(W_T² − T)关于T是鞅：它对每个T的均值都是零。
3. **米尔斯坦修正。** 一步之内，b(X_s) ≈ b(X_t) + b'b(X_t)(W_s − W_t)，所以∫b(X_s)dW_s ≈ bΔW + b'b∫(W_s − W_t)dW_s =
   bΔW + ½b'b(ΔW² − h)。
4. **瓦西切克。** r_T是高斯的，均值θ + (r₀ − θ)e^{−κT}，方差σ²(1 − e^{−2κT})/(2κ)。长期分布为N(θ, σ²/2κ)：标准差0.014/√0.197 = 3.2%，
   P(r < 0) = N(−4.1/3.2) ≈ 10%，与实验中两百条路径的10%一致。
5. **霍克斯过程。** 平稳时E[λ] = μ + (α/β)E[λ]，所以长期速率为μ/(1 − α/β) = 0.1/0.6 ≈ 每天0.167次；每个事件平均触发α/β = 0.4个子事件，
   所以40%的事件由先前的事件触发。
6. **E τ_a = ∞。** P(τ_a < ∞) = lim 2(1 − Φ(a/√T)) = 1。但t很大时f(t) ~ a(2π)^{−½}t^{−3/2}，所以E τ_a = ∫ t f(t) dt像∫ t^{−1/2} dt一样发散。
7. **W_T³的克拉克–奥科内被积函数。** D_tW_T³ = 3W_T²，所以H_t = E[3W_T² ∣ 𝓕_t] = 3(W_t² + T − t)。检验：由伊藤，W_T³ = ∫3W²dW + ∫3W dt，
   而∫_0^T W_t dt = ∫_0^T (T − t) dW_t（分部积分），所以W_T³ = ∫_0^T 3(W_t² + T − t) dW_t，均值为零，正如应有的那样。
8. **（资格考试）已实现方差的中心极限定理。** σ确定时$\Delta_iX \sim N(0, v_i)$相互独立；$\xi_i = (\Delta_iX)^2 - v_i$独立、
   均值为零、方差为$2v_i^2$，$n\sum 2v_i^2 \to 2\int\sigma^4$；李雅普诺夫条件成立，故$\sqrt n(\mathrm{RV}_n - \mathrm{IV})
   \Rightarrow N(0, 2\int\sigma^4)$。
9. **（资格考试）噪声。** $\mathrm{RV}_n(Y) = \mathrm{RV}_n(X) + 2\sum\Delta_iX\,\Delta_i\varepsilon + \sum(\Delta_i\varepsilon)^2$，
   期望为$\mathrm{IV} + 2n\omega^2$；除以$2n$后由大数定律得$\mathrm{RV}_n(Y)/2n \to \omega^2$。

## 写给研究者

中心极限定理（Jacod 1994；Barndorff-Nielsen与Shephard 2002），双幂变差（2004），黄–陶臣检验（2005），双尺度估计量（Zhang、Mykland与
Aït-Sahalia 2005），已实现核与预平均。开放问题：内生、自相关噪声与不规则时间下的有效估计；粗糙波动率下的即期波动率；波动率跳跃与共同跳跃。
