# Quant, Built — Part 9: No Arbitrage

Part 9 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), opening Act III, Derivatives. Two ways to get the same payoff must cost the same.
From that one idea, a lecture in eighteen numbered chapters, plus a hook, researcher section and closing (21 scenes): parity, the
fundamental theorem of asset pricing in one period and in continuous time, state prices and the risk-neutral measure,
trees, incomplete markets, changing numeraire, the density inside option prices, Ross recovery, model-free bounds by
martingale optimal transport, how arbitrage is traded, and the 2023–2026 research.

Numerical examples use the series' own code ([`compute.py`](compute.py), the House's
[`arbitrage`](../../../explainer/quant/house/arbitrage.py) checker, tested in
[`tests/test_quant_house.py`](../../../tests/test_quant_house.py)) from the Surface (Deribit BTC option trades on
10 December 2025) and, new in this part, Deribit's BTC futures trades over the same hours.

*An education in methods, not investment advice.*

These results have explicit domains. Finite FTAP uses full-support states, frictionless unrestricted trades and a positive bank asset; a weak state-price vector with zeros alone does not imply arbitrage. Continuous NFLVR gives an equivalent local martingale measure, while expectation pricing and numeraire changes need true-martingale/integrability conditions. Borrow-fee parity assumes a tradable reinvestable yield. Inverse BTC parity is C_BTC−P_BTC = D_BTC(1−K/F), with D_BTC=1 assumed here; asynchronous trade/mark comparisons are not executable bid–ask profits.

The empirical q/p illustration compares a fitted Q density with historical unconditional P and is not an identified conditional stochastic discount factor. BL curvature is a measure generally, and a density only under absolute continuity. Numerical shape checks are sampled diagnostics. The spline's cached plot is its positive part (without normalization), and its tail integrals are invalid Q probabilities because its raw curvature is negative. MOT uses X=S1/F1 and Y=S2/F2 under deterministic carry/common-measure assumptions; truncated, renormalized, unit-mean finite marginals give conditional finite-grid bounds. The ATM lognormal proxy does not fit both full marginals. Non-nested rebinning is sensitivity analysis, not a continuum convergence certificate. Neural dual costs are uncertified while constraints remain violated; stored shortfalls are weighted averages, not maxima.

Published historical quantities are attributed observations rather than outputs of the numerical code. The existing 28 compute items and data registry remain unchanged; 310 cumulative trials through Part 9, no new registrations or sealed holdouts opened by this pass.

## Chapters

* **Hook: one price, and how we got here.** The desk question (call 10, put 7, strike 100, spot 103, no rates: parity
  consistency, C − P = 3 = S − K). Parity on Deribit's inverse options, C − P = 1 − K/F: 339 call–put pairs, half within
  3.4 bp of their expiry's median forward (1.5 bp on marks), nine in ten within 9.9 bp; an implied basis of 3–5% a
  year. The era strip from Farkas (1902) to GameStop (2021); the objectives; the House.
* **1. Parity, assembled.** Definition of arbitrage and the law of one price; the long call and short put fused into a
  forward; the four-leg arbitrage at a put of 6, 200 simulated outcomes all landing on +1. **Lab:**
  `arbitrage.implied_forward` on the morning's trades. **New data:** all 62,223 Deribit BTC futures trades of the same
  hours (fetched through the data layer, checksummed in the manifest): on the 6 expiries with both, the
  options-implied forward and the dated futures agree to a median 0.66 bp of price (largest 3.6 bp).
* **2. Where parity breaks.** Parity with a borrow fee h, derived; reading h from option prices (Ofek, Richardson and
  Whitelaw 2004). Palm/3Com (2 March 2000): 3Com $81.81 against 1.525 × $95.06 = $144.97 of Palm, a stub of −$63.16
  a share; Palm short interest 147.6% of float; on 16 March a synthetic short at $39.12 against $55.25 (Lamont and
  Thaler 2003). GameStop (SEC staff report). Box spreads; Robinhood 2019. Pause: why not buy 3Com and short Palm?
* **3. The geometry of arbitrage (3D).** Payoffs in ℝ³, the orthant of payoffs that never lose, the line of zero-cost
  payoffs; a stock-price slider rotates the line and the separating plane; its normal is the state-price vector, whose
  first two components vanish at 125, leaving ψ = (0, 0, 1). The algebra: Dψ = p.
* **4. The fundamental theorem, proved and solved.** Theorem card (Harrison and Kreps 1979; Farkas 1902; Stiemke
  1915); both directions proved by separation. The price-space cone with the same slider. **Lab and replay:** the
  House's teaching `simplex` (Bland's rule) on the FTAP LP: at 100, 5 pivots to ψ = (0.385, 0.308, 0.308); at 130,
  infeasible after 6 pivots, and the phase-1 duals give the arbitrage (125 bonds, short 1 share: cost −5, payoff
  (45, 25, 0)).
* **5. State prices, the discount factor, and Q.** Arrow (1964), Ross (1978): p = Σψd = E^P[md] = E^Q[d]/(1+r),
  dQ/dP = (1+r)m. P bars morph into m and into Q; the risk-neutral simplex and the segment of martingale measures.
  **Experiment:** Bitcoin's empirical pricing kernel, Q from the Surface's 16-day density over P from 106
  non-overlapping 16-day returns (Binance, April 2021 – November 2025), 1,000 stationary-bootstrap draws: a hump,
  peaking at 1.26 near 1.06 × F and falling on the right. Bands are pointwise, historical-P-only bootstrap intervals with Q fixed, not a selected-peak significance test (the
  pricing-kernel puzzle, Jackwerth 2000).
* **6. The tree.** One-step replication in the (S, V) plane (Δ = ½, B = −40, V = 10, q = ½), derived; the four-step
  tree folding back with Δ at every node, and the hedge run along a path: the book equals the payoff on all 1,000
  paths to 1e−14. **Lab:** `trees.crr`, N = 1…200 drawn as it computes (12.44, 8.82, 10.79, 9.35, …, 9.935 at 200
  against Black–Scholes 9.948). An American put at 5% rates: exercise at 3 nodes, 7.71 against 6.87 European.
* **7. Incomplete markets: the interval as an LP.** Three states, the lid lowered onto the payoff (11.11) and the
  floor pushed up (0); the (B, Δ) plane with the level line sliding to the vertex (−44.44, 0.556); LP duality with the
  risk-neutral segment; the second FTAP (Harrison and Pliska 1981). The same `simplex` on the seller's LP agrees with
  HiGHS. The interval is constant from 3 to 33 states.
* **8. Completing the market; super-replication through time.** A digital's interval as calls are added strike by
  strike: [0, 0.779] → [0.032, 0.713] → … → [0.253, 0.338] around a true 0.290 (Ross 1976). A trinomial tree's
  super-replication chooses the outer branches (Kramkov 1996; Föllmer–Schied ch. 7): 12.44, 9.35, 9.79, 9.91, 9.94
  for N = 1, 4, 16, 64, 256 against Black–Scholes(25%) 9.948 (Avellaneda, Levy and Parás 1995; Lyons 1995).
* **9. Continuous time: Girsanov as reweighting.** Harrison–Kreps, Harrison–Pliska; the derivation of Q by Girsanov;
  150 P-paths re-weighted (not moved) into Q-paths. 200,000 paths: unweighted 16.61, weighted 9.971 ± 0.024 against
  9.948; effective sample 85.2% measured and predicted; at a 60% drift it collapses to 0.33%.
* **10. Free lunches, doubling, and bubbles.** The continuous-time doubling strategy (Dambis–Dubins–Schwarz),
  simulated on 20,000 paths with bridge-corrected crossings: 50.8% fall below −1 before winning (theory 50%), 25.0%
  below −3 (25%), 9.3% below −10 (9.1%). Admissibility; Kreps (1981), Dalang–Morton–Willinger (1990), NFLVR
  (Delbaen–Schachermayer 1994, 1998). The inverse Bessel bubble: E[S_T] = 2Φ(1/√T) − 1, simulated to four decimals;
  minimal expectation call/put prices can fail stock-price parity under a bubble; collateral and admissibility matter (Cox and Hobson 2005).
* **11. Change of numeraire.** Geman, El Karoui and Rochet (1995); the density dQ^N/dQ derived; N(d₁) = 0.5497 and
  N(d₂) = 0.4503 as one event under two measures (the density re-weighted by s/S₀ on screen). Margrabe (1978):
  formula 11.92, Monte Carlo 11.92 ± 0.02 under Q and 11.95 ± 0.02 under Q^{S₂}. Bitcoin as numeraire: the fitted 107-day call at 95,000 has an undiscounted forward dollar value of $8,597 and a BTC premium of 0.0915. With a chosen consistent dollar discount factor 0.98620 and BTC discount one, its spot dollar PV is about $8,479 = spot × BTC premium. Q(ITM) is 0.466 against 0.562 under the BTC measure.
* **12. Butterflies build the density.** The butterfly as a state price; butterflies of width 8,000 → 500 dollars
  converging to the Breeden–Litzenberger density (mass 0.99999, mean = the forward); the derivation; slope and
  curvature riding along the call curve. **Lab:** `static_checks`: 7 negative butterflies among 40 raw-trade strikes,
  7 on the Surface's median quotes, 0 on the SVI fit.
* **13. The density on the Surface.** The SVI fit replayed (`FullRangeReplay`, error 3.76 → 0.156 vol points across
  fresh fits with increasing function-evaluation budgets from a common initialization) with its density; SVI, calendar and Lee conditions; all 7 expiries from 9 to 289 days as a 3D ridge
  (standard deviation 7.8% → 32% of spot; skewness −0.29 at 16 days, +0.31 at 289; 0 calendar violations); four
  specifications at 107 days with vega-weighted RMSE no larger than 0.7 vol points (not every quote): valid-candidate downside tail integrals range from 9.79% to 10.25%; the spline's
  density has negative curvature, so its positive-part integral of 12.03% is invalid as a Q probability (Shikhman et al. 2026: 95 of 126 pricing directions numerically null).
* **14. Ross recovery, and its critique.** The theorem derived (Perron–Frobenius). **Lab:** `power_iteration`,
  δ_k → 0.98. The synthetic test (exact to 1e−15; with a permanent component, error 0.051 and a pessimistic long run,
  −2.5% against +2.0%). Borovička–Hansen–Scheinkman (2016), Martin–Ross (2019), Qin–Linetsky (2016). Sweep over 200
  random economies: error grows smoothly with the permanent part (median 0.047 at full strength). Evidence:
  Jensen–Lando–Pedersen (2019), Jackwerth–Menner (2020), Horvath (2025).
* **15. Bounds without a model.** Convex order (Strassen 1965) on the Surface's call curves; the MOT LP and its dual
  derived (Beiglböck, Henry-Labordère and Penkner 2013; Galichon, Henry-Labordère and Touzi 2014). **3D:** the dual
  hedge surface u(x) + v(y) + h(x)(y − x) lowered onto the claim |y/x − 1|, touching where the optimal coupling sits.
  Bounds: straddle [0.1375, 0.2175] (log-normal 0.180), forward-start call exactly half, (S₂ − S₁)² a single number,
  (ln S₂/S₁)² [0.0572, 0.0741]; Hobson (1998).
* **16. Finite-grid bounds and numerical sensitivity.** **Lab:** `mot_bounds`. Grid refinement 9×25 → 81×361: the band
  widens from [0.172, 0.200] to [0.127, 0.221], as a non-nested grid-sensitivity check, without a continuum error certificate. Entropic MOT (Sinkhorn with a martingale Newton step),
  replayed as ε shrinks 0.1 → 0.003: 0.196, 0.208, 0.216, 0.2174 against the LP's 0.2175.
* **17. How arbitrage is traded, and why it is limited.** Authorized participants and the March 2020 bond-ETF
  discounts (Haddad, Moreira and Muir 2021); box rates 35 bp above Treasuries 1996–2023 (NY Fed), the 40 bp
  convenience yield (van Binsbergen, Diamond and Grotteria 2022), BOXX ($8.08 bn net assets on 30 September 2025, its
  annual report); Royal Dutch/Shell (9.53% mean absolute deviation, 1980–1995); negative stubs (Mitchell, Pulvino and Stafford
  2002). **Simulation:** Shleifer and Vishny's limits of arbitrage: forced liquidation before certain convergence in
  0%, 2.7%, 17.5% and 64.9% of 1,000 paths as the redemption sensitivity goes 0, ½, 1, 2, and liquidation at the
  widest mispricing. Crisis file: LTCM (Federal Reserve History; the President's Working Group report).
* **18. The frontier, 2023 to 2026.** Neural MOT (Neufeld and Sester 2023), martingale Sinkhorn (Hasenbichler,
  Joseph, Loeper, Obłój and Pammer), multi-marginal MOT (Engström, Källblad and Karlsson 2024). **Trained:** a neural
  dual (u, v, h as networks, penalty method), 3 seeds × 10,000 steps: raw dual costs 0.21927, 0.21891, 0.21899, 0.64–0.81% above
  the LP's 0.2175. Their weighted mean positive constraint shortfalls are about 0.000333; these are neither maximum violations nor certified upper bounds. Guyon (2024), Neufeld–Papapantoleon–Xiang (2023), Bartl–Beiglböck–Pammer (2026), Heston–Jacobs–Kim
  (2023).
* **For the researcher: fractional prices and frictions.** For 0 < H < 1, adjacent fBM increments have correlation ρ = 2^{2H−1} − 1. If H < 1/2, quadratic variation diverges. If H > 1/2, it is zero and total variation is infinite; both facts are needed to exclude a continuous semimartingale. The fixed sign-increment score ΣπΔ minus linear turnover charges is a proxy on log increments, not exact self-financing wealth in exp(σB^H). The √n Sharpe formula is an iid reference that ignores serial covariance, not an arbitrage proof. Its mean-score optimum is n* = [(1−H)σ√(2/π)|ρ|/(2εp)]^{1/H}: H=0.6 and ε=1 bp give about 2,333/year and 0.3166 log points, not 31.7% investment return. Doubling ε multiplies n* by 2^{−1/H} ≈ 0.315. A finite optimum does not prove no arbitrage. An equivalent-measure consistent price system inside a bid–ask band is sufficient under admissibility; positive continuous prices with conditional full support, including exp(σB^H), admit systems for arbitrarily small spreads. Rough-variance semimartingale prices still need a valid pricing measure. The existing 2019–2020 Bitcoin illustration uses full-sample correlation to choose direction retrospectively, inverts one correlation to label H, and omits spread, impact and funding; it is neither an fBM identification test nor untouched forecasting evidence. The three closing topics are project research directions.
* **The arbitrage checker, recap, desk questions, nine problems (two at qualifying-exam level).** Rule 10; the trial
  counter stays at 310.

Hands-on: six labs (`implied_forward`, `simplex`, `crr`, `static_checks`, `power_iteration`, `mot_bounds`), replays
(simplex pivots, the SVI fit, power iteration, MOT grid walls, entropic iterations, the neural dual with three seeds),
and simulations run on screen (the arbitrage ledger, the hedge along a tree path, Girsanov re-weighting, doublers,
bubbles, the limits-of-arbitrage fund).

## Textbook audit

| Book, section | Chapter |
|---|---|
| Shreve I ch. 1, the binomial no-arbitrage model | 6 |
| Shreve I ch. 3, state prices, Radon–Nikodým | 5, 9 |
| Shreve I ch. 4, American derivatives | 6 (one beat); Parts 8 and 10 |
| Shreve I ch. 6, interest-rate assets | 11 (one line); Part 19 |
| Shreve II ch. 5, risk-neutral pricing, Girsanov, the two FTAPs | 9, 10 |
| Shreve II ch. 9, change of numéraire | 11 |
| Björk (4th ed.) ch. 2–3, binomial and general one-period models | 3–8 |
| Björk ch. 9, a primer on incomplete markets | 7–8 |
| Björk ch. 10, parity relations | 1–2 |
| Björk ch. 11–12, the martingale approach and its mathematics | 9–10 |
| Björk ch. 15, change of numeraire | 11 |
| Björk ch. 29, 34, incomplete markets, good-deal bounds | 8 (named); Part 13 |
| Duffie DAPT ch. 1, arbitrage and state prices, risk-neutral probabilities | 3–5 |
| Duffie ch. 2, the multiperiod model | 6, 9 |
| Duffie ch. 6, state prices and equivalent martingale measures in continuous time | 9–11 |
| Delbaen–Schachermayer, Part I (finite Ω, Dalang–Morton–Willinger, Kreps–Yan, NFLVR overview) | 3–4, 10 |
| Föllmer–Schied ch. 1, arbitrage, martingale measures, completeness | 3–5, 7 |
| Föllmer–Schied ch. 5, binomial model, convergence to Black–Scholes | 6 |
| Föllmer–Schied ch. 7, superhedging | 8, 15 |
| Henry-Labordère, *Model-Free Hedging* (MOT, model-independent options) | 15–16, 18 |
| Hull OFOD, binomial trees; martingales and measures | 6, 11 |
| Cochrane, *Asset Pricing* Part I (contingent claims, SDF) | 5; Part 23 |

Section titles for Duffie, Delbaen–Schachermayer and Föllmer–Schied are given at chapter level only (their exact
section lists were not checked against the books).

## Reading guide

All papers with full citations are in [`../READING.md`](../READING.md), Part 9. Each appears on screen:
Farkas 1902, Stiemke 1915 (ch 4); Arrow 1964, Ross 1978 (ch 5); Stoll 1969 (hook, ch 1); Ross 1976 (ch 8);
Breeden–Litzenberger 1978 (ch 12); Margrabe 1978 (ch 11); Cox–Ross–Rubinstein, Harrison–Kreps 1979 (ch 4, 6, 9);
Harrison–Pliska 1981 (ch 7, 9); Kreps 1981, Dalang–Morton–Willinger 1990, Delbaen–Schachermayer 1994/1998,
Cox–Hobson 2005 (ch 10); Geman–El Karoui–Rochet 1995, Jamshidian 1989 (ch 11); Avellaneda–Levy–Parás, Lyons 1995,
Kramkov 1996 (ch 8); Hobson 1998, Strassen 1965, Beiglböck–Henry-Labordère–Penkner 2013, Galichon–Henry-Labordère–Touzi
2014 (ch 15); Jackwerth 2000 (ch 5); Ofek–Richardson–Whitelaw 2004, Lamont–Thaler 2003, Mitchell–Pulvino–Stafford 2002
(ch 2, 17); Ross 2015, Borovička–Hansen–Scheinkman 2016, Martin–Ross 2019, Qin–Linetsky 2016,
Jensen–Lando–Pedersen 2019, Jackwerth–Menner 2020, Horvath 2025 (ch 14); Shleifer–Vishny 1997, Froot–Dabora 1999,
Haddad–Moreira–Muir 2021, van Binsbergen–Diamond–Grotteria 2022 (ch 17); the frontier list (ch 18). Schachermayer's
Hilbert-space proof (1992) is the README's alternative proof of chapter 4.

## Build it

```bash
python -m videos.quant.quant9.compute                         # every number, cached in .cache/quant9/ (about 10 CPU-minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant9 MOT       # one chapter, silent, with a contact sheet
python tools/make.py quant9 --cpu-voice -q m                  # English and Chinese, narrated by Kokoro on the CPU
```

`futures_basis` fetches the Deribit futures trades through `explainer.quant.data.deribit_trades(..., kind="future")`:
hour by hour, cached in `.cache/quant_data/`, each hour's SHA-256 recorded in `videos/quant/data/manifest.json`.
`neural_mot` (about 4 minutes, torch, one thread) resumes seed by seed.

## Desk questions, with solutions

1. **Call 10, put 7, K = 100, S = 103, r = 0.** C − P = 3 and S − K = 3: no arbitrage. If the put were 6
   (C − P = 4 > 3), sell the call, buy the put, buy the stock (cost 103 + 6 − 10 = 99) and borrow 99; at expiry the
   package is worth exactly 100, so you keep 1. If the put were 8, reverse every leg.
2. **A box on 100/110, one year, r = 4%.** It pays 10 in every state, so it is worth 10e^{−0.04} ≈ 9.61; buying it
   cheaper lends above 4%, selling it dearer borrows below. With American options the short leg can be exercised early,
   leaving a stock position to finance (Robinhood, 2019).
3. **A digital from two calls at 99.5 and 100.5, priced 6.20 and 5.70.** (C(99.5) − C(100.5))/1 = 0.50. As the strikes
   close in, the call spread over its width tends to −∂C/∂K = e^{−rT}Q(S_T > K), the digital's price.
4. **A parent below its stake in a listed subsidiary.** Not a riskless arbitrage: the short leg must be borrowed, may
   be recalled or be unavailable (Palm's short interest was 147.6% of float), convergence can outlast your funding, and
   in 30% of 82 cases the link was severed before the gap closed.

## Problems, with solutions

1. **Parity with a borrow fee.** A share lent out earns h, so e^{−hT} shares grow to one share. A = call + Ke^{−rT}
   bonds and B = put + e^{−hT} shares lent both pay max(S_T, K), so C + Ke^{−rT} = P + Se^{−hT}. If C − P is larger,
   sell the call, buy the put, buy and lend e^{−hT} shares, borrow the rest: a positive amount today, nothing at T.
2. **The one-period FTAP from Stiemke's lemma.** L = {(−θ·p, D^⊤θ)} ⊂ ℝ^{1+m} is a subspace; no arbitrage means
   L ∩ ℝ^{1+m}_+ = {0}. By Stiemke's lemma (separate L from the simplex), there is λ ≫ 0 orthogonal to L:
   λ₀(−θ·p) + Σ_j λ_j(D^⊤θ)_j = 0 for all θ, so p = Dψ with ψ = λ_{1:m}/λ₀ ≫ 0. Conversely p = Dψ, ψ ≫ 0, gives
   θ·p = ψ·D^⊤θ > 0 whenever D^⊤θ ≥ 0, ≠ 0. (Schachermayer 1992 gives a Hilbert-space proof.)
3. **The binomial probability.** Replicating both states gives V = e^{−rΔt}(qV_u + (1 − q)V_d) with
   q = (e^{rΔt} − d)/(u − d) ∈ (0, 1) iff d < e^{rΔt} < u; otherwise the stock dominates the bond in every state or
   the reverse.
4. **Butterflies and the density.** C′(K) = −e^{−rT}∫_K^∞ q, C″(K) = e^{−rT}q(K); the butterfly over h² is the second
   difference of C, which tends to C″(K) by Taylor's theorem.
5. **The trinomial interval.** With S ∈ {80, 100, 125}, the call pays (0, 0, 25). The cheapest dominating portfolio
   rests on states 1 and 3: Δ = 5/9, B = −400/9, cost 100/9 ≈ 11.11; the dual's q = (5/9, 0, 4/9) gives 25 × 4/9. The
   richest dominated portfolio is zero (q → (0, 1, 0)). The interval is (0, 100/9), open since strictly positive
   measures never reach its ends.
6. **The forward-start call's band.** (R − 1)^+ = ½|R − 1| + ½(R − 1), and for any martingale coupling
   E[R − 1] = E[(S₂ − S₁)/S₁] = E[E[S₂ − S₁ | S₁]/S₁] = 0, so every model's forward-start call price is half its
   straddle price, and the sup and inf halve.
7. **Margrabe.** With asset 2 as numeraire, V₀/S²₀ = E^{Q^{S²}}[(R_T − 1)^+], R = S¹/S² a Q^{S²}-martingale with
   d ln R volatility σ_R² = σ₁² + σ₂² − 2ρσ₁σ₂ (Itô on a ratio), so V₀ = S¹₀N(d₁) − S²₀N(d₂) with
   d₁,₂ = (ln(S¹₀/S²₀) ± σ_R²T/2)/(σ_R√T).
8. **(qual) The memory of fractional Brownian motion.** With step h, Var Δ = h^{2H} and E[B_h(B_{2h} − B_h)] =
   E[B_hB_{2h}] − h^{2H} = ½(h^{2H} + (2h)^{2H} − h^{2H}) − h^{2H} = h^{2H}(2^{2H−1} − 1), and stationarity of the
   increments gives the same correlation 2^{2H−1} − 1 for every pair of neighbours, on every grid. Over n steps of
   [0, 1], E Σ|Δ_k|² = n·n^{−2H} = n^{1−2H}: for H > ½ this tends to 0, and a non-negative variable with mean → 0
   tends to 0 in L¹. For H < ½ the mean tends to ∞ and the variance of the sum, 2Σ_{j,k}Cov(Δ_j, Δ_k)², is of order
   n·n^{−4H}, so the sum over its mean tends to 1: the sum tends to ∞. A semimartingale with continuous paths has a
   finite quadratic variation. For H > 1/2, zero quadratic variation would force a continuous semimartingale to have finite total variation, whereas fBM has infinite total variation (p-variation index 1/H). Thus B^H is not a semimartingale when H ≠ 1/2. Zero quadratic variation alone would not suffice.
9. **(qual) The best frequency.** Per trade, E[π_kΔ_k] = sign(ρ)E[sign(Δ_{k−1})Δ_k] = |ρ|E|Δ| = σn^{−H}√(2/π)|ρ|,
   and the position changes by 2 when consecutive increments differ in sign, probability p = ½ − arcsin(ρ)/π by
   Sheppard's formula, so the yearly cost is n·2εp and m(n) = n[σn^{−H}√(2/π)|ρ| − 2εp]. Setting m′(n) = 0:
   (1 − H)σn^{−H}√(2/π)|ρ| = 2εp, so n* = [(1 − H)σ√(2/π)|ρ|/(2εp)]^{1/H}; substituting, m(n*) = n*·g*·(1 − (1 − H))
   = Hn*g* with g* = σ(n*)^{−H}√(2/π)|ρ|. At H = 0.6, σ = 0.2, ε = 1 bp: ρ = 0.1487, p = 0.4525, n* ≈ 2,330,
   m* ≈ 0.317 log points/year in this proxy, not a wealth return. Initial and terminal turnover terms are ignored. n* ∝ ε^{−1/H}, so doubling the cost divides it by 2^{1/0.6} = 3.17.
## For the researcher

The sign-increment examples are descriptive proxies. Their mean/SD ratios are not proofs of admissible arbitrage, and the iid reference does not establish long-run risk under serial dependence. Consistent-price-system theorems use an equivalent measure and specified admissibility/spread conventions.

* **The theorems.** Delbaen and Schachermayer (1994), *Math. Ann.* 300 (a locally bounded price that is not a
  semimartingale admits a free lunch with vanishing risk with simple integrands); Rogers (1997), "Arbitrage with fractional Brownian motion," *Math. Finance* 7; Cheridito (2003),
  *Finance Stoch.* 7; Jouini and Kallal (1995), *JET* 66; Guasoni (2006), *Math. Finance* 16; Guasoni, Rásonyi and
  Schachermayer (2008), *Ann. Appl. Probab.* 18; Guasoni, Nika and Rásonyi (2019), "Trading fractional Brownian
  motion," *SIAM J. Financial Math.* 10(3), optimal trading under temporary price impact.
* **Simplifications.** One fixed log-increment score proxy, not an optimal investment strategy; the iid Sharpe reference ignores serial covariance between scores (simulated and formula Sharpe ratios differ by up to 15%; the means
  agree to within simulation error). Bitcoin's autocorrelations are sensitive to the largest moves.
* **Project directions.** Construct a consistent price system for a specified model; solve an explicit utility/control problem; predefine a prospective empirical protocol. No claim is made that all variants are globally open problems.

## Data and reproducibility

* The Surface: Deribit BTC option trades on 10 December 2025, 00:00–12:00 UTC; the futures trades of the same hours
  (new in this part); Binance BTCUSDT daily closes (for P in chapter 5). All checksummed in
  [`../data/manifest.json`](../data/manifest.json).
* Synthetic and labelled as such on screen: the one-period markets, the Ross economies, the doubling and bubble
  simulations, the trinomial super-replication, the limits-of-arbitrage fund. Every random choice is seeded.
* Published numbers and their sources: GameStop (SEC staff report, October 2021); Palm/3Com (Lamont and Thaler 2003;
  Chicago Booth Review); box rates (NY Fed Liberty Street Economics, October 2023); BOXX (annual report on Form N-CSR,
  30 September 2025); Royal Dutch/Shell (RBA RDP 2003-06); LTCM (Federal Reserve History; President's Working Group,
  April 1999).
* All 28 existing compute items are restored without changing their protocol. The part contains retrospective sign-score illustrations, but this pass registers no new market trial or holdout evaluation. The cumulative counter through Part 9 is 310.

---

# 量化金融，从零搭建 — 第9部分：无套利

衍生品篇的开篇：得到同一收益的两种方法必须同价。由这个想法出发，十八个编号章节，加开场、研究者部分与结尾（共21个场景）：平价关系；单期与连续时间中的资产定价基本定理；
状态价格与风险中性测度；二叉树；不完备市场；计价单位变换；期权价格里的密度；罗斯复原；用鞅最优传输得到不依赖模型的界；业界如何做套利；
以及2023—2026年的研究前沿。

数据是Deribit在2025年12月10日的比特币期权成交（"曲面"），以及本部分新增的同一时段比特币期货成交。

*讲的是方法，不构成投资建议。*

有限状态基本定理假定状态全支持、无摩擦多空交易与正银行资产；单个带零分量的弱状态价格不能证明套利。连续NFLVR给出等价局部鞅测度；期望定价与计价单位变换另需真鞅和可积性。借券费等式假定可交易、可再投资的出借收益。反向BTC平价为C_BTC−P_BTC = D_BTC(1−K/F)，本例假定D_BTC=1；异步成交和标记价比较不是可执行买卖价套利。

q/p示例比较拟合Q与历史无条件P，不是已识别的条件随机贴现因子。BL曲率一般是测度，绝对连续时才有密度。数值无套利检查仅覆盖采样点。样条缓存只存未归一化正部，原始曲率有负值，其尾部积分不是有效概率。MOT用X=S1/F1、Y=S2/F2，假定确定持有成本与共同定价测度；边缘分布经截断、归一化、单位均值缩放和离散化，因此只是有限网格条件界。平值对数正态代理不匹配完整边缘分布。非嵌套网格是敏感性分析，不能认证连续域收敛。约束仍被违反时，神经对偶成本不能认证上界；缓存短缺是加权平均，不是最大值。

文献中的历史数值是注明来源的观测，与数值计算输出有别。原有28个计算项目和数据登记不变，第9部分累计310次试验；本次没有新增登记或打开封存留出集。

## 各章

* **开场：同一个价格。** 交易台问题；Deribit反向期权的平价C − P = 1 − K/F：339对，一半与中位数相差3.4个基点以内；隐含基差每年3%—5%。从法卡斯（1902）到游戏驿站（2021）的时间线。
* **1. 平价，亲手拼出来。** 套利与一价定律；看涨加看跌拼成远期；看跌为6时四条腿锁定1元。**实验：** `implied_forward`。**新数据：** 同时段62,223笔期货成交，6个到期日上期权隐含远期与期货的差中位数0.66个基点。
* **2. 平价在哪里失效。** 借券费用h下的平价；Palm/3Com：每股3Com隐含−63.16美元；借券稀缺的价格；游戏驿站；箱式组合与罗宾汉2019。
* **3. 套利的几何（三维）。** 收益空间、非负象限、零成本收益直线、分离平面；125边界时状态价格为(0, 0, 1)，前两分量归零。
* **4. 基本定理：证明与求解。** 两个方向的证明；价格空间中的锥；**实验与回放：** 教学用单纯形法，100时5次转轴得到状态价格，130时6次转轴后不可行，对偶给出套利组合。
* **5. 状态价格、贴现因子与Q。** 一种选定正状态价格扩张将P柱变为m再变为Q；不完备市场不唯一。比特币历史无条件密度比呈驼峰，区间仅重采样P。
* **6. 二叉树。** 单步复制；四步树倒推并沿路径对冲，1,000条路径误差1e−14；**实验：** `crr`，N到200收敛到9.948；美式看跌。
* **7. 不完备市场：区间即线性规划。** 盖子与地板；(B, Δ)平面；对偶；第二基本定理。
* **8. 让市场完备；跨时间的超复制。** 逐个加入看涨期权，数字期权区间收缩到[0.253, 0.338]；三叉树超复制价格收敛到最宽波动率下的布莱克—斯科尔斯。
* **9. 连续时间：哥萨诺夫即重新加权。** 200,000条路径，加权价9.971 ± 0.024；有效样本85.2%。
* **10. 免费午餐、加倍策略与泡沫。** 加倍策略模拟：50.8%跌破−1；可容许性；NFLVR；逆贝塞尔泡沫；最小期望期权价格下的平价差异取决于抵押与可容许约定。
* **11. 计价单位变换。** N(d₁)与N(d₂)；马格雷布公式；比特币权利金约0.0915，未贴现远期美元价值8597；选定一致贴现0.98620后，即期美元现值约8479，等于现价乘BTC权利金。
* **12. 蝶式价差拼出密度。** 宽度8,000到500美元的蝶式收敛到BL密度；**实验：** `static_checks`：原始成交有7个负蝶式，SVI拟合为0。
* **13. 曲面上的密度。** SVI拟合回放；7个到期日的三维密度山脊；有效拟合候选的30%下跌尾部积分相差约0.45个百分点；无效样条的正部积分不能解释为概率。
* **14. 罗斯复原及其批评。** 幂迭代；合成经济中的检验；BHS批评；200个随机经济的误差扫描；实证证据。
* **15. 不依赖模型的界。** 凸序；MOT线性规划与对偶；**三维：** 对冲曲面落到收益曲面上，接触集即最优耦合。
* **16. 有限网格界与数值敏感性。** 非嵌套分箱改变边缘分布，区间从[0.172, 0.200]移到[0.127, 0.221]，不是连续域收敛证明。熵迭代报告终值与可行性残差，中间不可行值可高于LP。
* **17. 套利怎样做，为什么受限。** ETF授权参与者与2020年3月；箱式利率与BOXX；荷兰皇家/壳牌；负残值；施莱弗—维什尼模拟；LTCM。
* **18. 研究前沿。** 神经网络原始对偶成本（3个种子，高于LP约0.64%—0.81%；平均正短缺约0.000333，并非认证上界）；鞅Sinkhorn；多边际MOT；Guyon；多资产界；适应Wasserstein。
* **写给研究者：分数价格与摩擦。** 相邻分数布朗增量相关系数为ρ = 2^{2H−1} − 1。H < 1/2时二次变差无限；H > 1/2时二次变差为零且总变差无限，两者合起来才排除连续半鞅。固定的符号增量和减线性换手费是对数增量得分代理，不是exp(σB^H)市场的精确自融资财富。根号n夏普线是假定得分独立的参考，忽略序列协方差，不能证明套利。H=0.6、1基点时代理最优频率约2333/年、均值得分0.3166对数点，不是31.7%投资收益。收费翻倍，频率乘以2^{−1/H} ≈ 0.315。有限最优点不能证明无套利。等价测度下一致价格系统在可容许条件下足以排除套利；有条件全支持的正连续价格，包括分数布朗指数价格，对任意小正价差都有这样的系统。粗糙方差下的半鞅价格仍需有效定价测度。2019至2020年比特币示例用全样本相关系数事后选方向，单个相关反演的H不能识别分数模型，且遗漏价差、冲击与融资；不是未触碰预测检验。最后三个主题是项目研究方向。
* **结尾。** 套利检查器、十句回顾、四个交易台问题、九道习题（两道为资格考试水平）。

## 交易台问题与解答

1. **看涨10、看跌7、执行价100、现价103、利率为零。** C − P = 3 = S − K：该平价一致。若看跌为6，卖出看涨、买入看跌、买入股票（成本99）并借入99，到期在偿还借款前值100，偿还99后净支付1。若看跌为8，把每一腿反过来。
2. **100/110的一年期箱式组合，利率4%。** 在每种状态下支付10，价值10e^{−0.04} ≈ 9.61；它是一笔贷款。用美式期权时，空头腿可能被提前行权（罗宾汉，2019）。
3. **用执行价99.5和100.5、价格6.20和5.70的两个看涨近似数字期权。** (6.20 − 5.70)/1 = 0.50只是有限宽度近似，不唯一识别精确数字价格；执行价处连续且宽度趋零时，价差除以宽度趋于−∂C/∂K = e^{−rT}Q(S_T > K)。
4. **母公司市值低于其所持上市子公司股份的价值。** 不是无风险套利：空头腿要借券，可能被召回或借不到，收敛可能比融资期限更久，82个案例中30%在价差收敛前联系就被切断。

## 习题与解答

1. **含借券费用的平价。** 出借的股票赚取费用h，e^{−hT}股增长为一股。组合A（看涨加Ke^{−rT}债券）与组合B（看跌加出借的e^{−hT}股）在T都支付max(S_T, K)，所以C + Ke^{−rT} = P + Se^{−hT}。
2. **由施蒂姆克引理证明单期基本定理。** L = {(−θ·p, D^⊤θ)}是子空间；无套利即L与非负象限只交于0。由施蒂姆克引理存在与L正交的λ ≫ 0，于是p = Dψ，ψ = λ_{1:m}/λ₀ ≫ 0。反之，p = Dψ、ψ ≫ 0时，任何D^⊤θ ≥ 0且不为0的θ都有θ·p > 0。
3. **二叉树概率。** 复制两种状态得V = e^{−rΔt}(qV_u + (1 − q)V_d)，q = (e^{rΔt} − d)/(u − d)，它在(0, 1)中当且仅当d < e^{rΔt} < u。
4. **蝶式价差与密度。** C′(K) = −e^{−rT}∫_K^∞ q，C″(K) = e^{−rT}q(K)；蝶式价差除以h²是二阶差分，由泰勒定理趋于C″(K)。
5. **三叉区间。** 收益(0, 0, 25)；最便宜的超复制落在状态1和3上：Δ = 5/9，B = −400/9，成本100/9；对偶q = (5/9, 0, 4/9)。下界为0。区间(0, 100/9)是开的。
6. **远期开始看涨期权的区间。** (R − 1)^+ = ½|R − 1| + ½(R − 1)，而对任何鞅耦合E[R − 1] = 0，所以每个模型中远期看涨价格都是跨式价格的一半，上下界也减半。
7. **马格雷布公式。** 以资产2为计价单位，V₀/S²₀ = E^{Q^{S²}}[(R_T − 1)^+]，R = S¹/S²是鞅，波动率σ_R² = σ₁² + σ₂² − 2ρσ₁σ₂，所以V₀ = S¹₀N(d₁) − S²₀N(d₂)。
8. **（资格考试）分数布朗运动的记忆。** 步长h时Var Δ = h^{2H}，E[B_h(B_{2h} − B_h)] = ½(2h)^{2H} − h^{2H} = h^{2H}(2^{2H−1} − 1)；增量平稳，所以任何网格上每对相邻增量的相关系数都是2^{2H−1} − 1。[0, 1]上n步时E Σ|Δ_k|² = n^{1−2H}：H > ½时趋于0（非负变量均值趋于0，L¹收敛）；H < ½时均值趋于∞，和的方差为n·n^{−4H}阶，和与均值之比趋于1，所以和趋于∞。连续半鞅的二次变差有限。H > 1/2时，若为连续半鞅，零二次变差将要求总变差有限；但分数布朗运动总变差无限（p变差指数为1/H），因此H不等于1/2时不是半鞅。仅有零二次变差不够。
9. **（资格考试）最佳频率。** 每笔交易E[π_kΔ_k] = |ρ|E|Δ| = σn^{−H}√(2/π)|ρ|；相邻增量符号不同时仓位变化2，概率p = ½ − arcsin(ρ)/π（谢泼德公式），年成本n·2εp，所以m(n) = n[σn^{−H}√(2/π)|ρ| − 2εp]。令m′(n) = 0得(1 − H)σn^{−H}√(2/π)|ρ| = 2εp，n* = [(1 − H)σ√(2/π)|ρ|/(2εp)]^{1/H}，代入得m(n*) = Hn*g*，g* = σ(n*)^{−H}√(2/π)|ρ|。H = 0.6、σ = 0.2、ε = 1个基点时，ρ = 0.1487，p = 0.4525，n* ≈ 2,330，m* ≈ 每年0.317对数得分点，不是财富收益；忽略初始与终止换手项。n* ∝ ε^{−1/H}，成本翻倍时它除以2^{1/0.6} = 3.17。

## 数据与可复现性

* 曲面：Deribit 2025年12月10日00:00—12:00 UTC的比特币期权成交；同时段期货成交（本部分新增）；币安BTCUSDT日收盘价。全部在数据清单中记录校验和。
* 合成数据在屏幕上标注：单期市场、罗斯经济、加倍与泡沫模拟、三叉超复制、套利受限基金。所有随机数都设定了种子。
* 原有28个计算项目按既有协议恢复。本部分包含回顾性符号得分示例，但本次不新增市场试验登记，也不打开留出集。第9部分累计计数310。

## 写给研究者

符号增量例子是描述性得分代理，均值／标准差之比不能证明可容许套利，独立参考公式忽略序列协方差。一致价格系统需要等价测度、明确的可容许条件和价差约定。

* **定理。** 德尔班与沙赫迈尔（1994），*Math. Ann.* 300（局部有界且非半鞅的价格，用简单被积函数即有带消失风险的免费午餐）；罗杰斯（1997），*Math. Finance* 7；切里迪托（2003），*Finance Stoch.* 7；茹伊尼与卡拉勒（1995），*JET* 66；瓜索尼（2006），*Math. Finance* 16；瓜索尼、拉索尼与沙赫迈尔（2008），*Ann. Appl. Probab.* 18；瓜索尼、尼卡与拉索尼（2019），*SIAM J. Financial Math.* 10(3)，暂时性价格冲击下的最优交易。
* **简化。** 只用一种固定对数增量得分代理，不是最优投资策略；独立夏普参考忽略得分间序列协方差（模拟与公式的夏普比率最多相差15%；均值在模拟误差内一致）。比特币的自相关对最大的几次波动很敏感。
* **项目方向。** 为指定模型构造一致价格系统；求解明确的效用与控制问题；预先定义前瞻实证协议。不声称所有变体都是全球未解决问题。

The MOT return claims are unit-notional functions of X and Y, not ordinary cash straddles |S2−S1|. Replicating the squared change uses static square payoffs plus the dynamic position −2X between dates. The doubler visualization appends schematic +1 endpoints at cached discrete hit times; 17/120 visual paths are still unhit at clock 60, and 0.595% of the separate 20,000 paths are unhit at the simulation clock limit 20,000. Finite-step bridge/minimum corrections are approximate.

MOT收益支付是X、Y的单位名义本金函数，不是普通现金跨式|S2−S1|。平方变化复制需两个静态平方支付及两日间−2X动态头寸。加倍策略可视化在缓存离散首达时刻附加+1示意端点；时钟60时120条中17条未到达，另一组两万路径在最大时钟20000处仍有0.595%未到达。有限步长桥与最低点修正是近似。

Surface dollar call curves in the numerical density examples are undiscounted forward values, not spot-dollar premiums. The numeraire illustration preserves the cached expectations and chooses discount factors consistently with the finite-grid mean; it does not independently estimate both currency curves. A selected state-price extension in an incomplete market does not uniquely price an untraded call. Black swaption pricing requires an additional lognormal swap-rate assumption. LTCM's cited $129bn assets/$4.8bn equity imply about 27 times assets/equity, distinct from debt/equity.

密度数值例子中的曲面美元看涨曲线是未贴现远期价值，不是即期美元权利金。计价单位例子保留缓存期望，按有限网格均值选择一致贴现，并非独立估计两条货币曲线。不完备市场中选定的状态价格扩张不能唯一给未交易看涨定价。Black互换期权价格另需利率对数正态假设。LTCM引用的1290亿美元资产与48亿美元权益对应约27倍资产／权益，不等于债务／权益。

A finite two-call spread approximates a digital, rather than identifying its exact point-strike price. The equality with minus the call derivative needs a suitable one-sided derivative, and at a continuity strike the narrow-spread limit is unambiguous.
