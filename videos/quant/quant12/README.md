# Quant, Built — Part 12: The Volatility Surface

Part 12 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It covers the volatility surface as an object (its shape,
how it is quoted, how it moves), the conditions that keep it free of arbitrage, the parametrizations and models that
fit it (SVI, SSVI, Dupire's local volatility and its implied tree, Gyöngy's projection), volatility as an asset
(variance and volatility swaps, the VIX, the variance risk premium, SVIX and risk-neutral moments, VIX futures and
short-volatility notes), Volmageddon, dealer gamma and same-day options, and surfaces learned by neural networks.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`volsurface`](../../../explainer/quant/house/volsurface.py) builder and [`trees.derman_kani`](../../../explainer/quant/house/trees.py),
[`deep.train_surface_net`](../../../explainer/quant/house/deep.py), all tested in `tests/test_quant_house.py`) from
Deribit's trades (the Surface and 243 weekly surfaces), Binance's hourly BTCUSDT, Deribit's DVOL, FRED's VIX and
VIX3M, Yahoo Finance's S&P 500 and Cboe's VIX futures settlements.

*An education in methods, not investment advice.*

## Chapters (about 63 minutes)

* **The shape of fear.** A 3D tour of the Surface (10 December 2025): 254 quotes and an SSVI fit at 0.74 vol points,
  vega-weighted. How we got here (1973–2024), a flat Black–Scholes plane bending into the Surface, the objectives,
  the House.
* **1. The smile, read.** Three expiries; the smile as the risk-neutral law's skewness and kurtosis (a live
  Gram–Charlier slider and Backus–Foresi–Wu's first-order formula); forward variance. Over 243 weekly surfaces
  (April 2021 – November 2025): mean ATM vol 56% (7 days) to 64% (180 days); the 7-day above the 180-day in 14% of
  weeks; the 30-day smile call-skewed in 45% of weeks (8% in 2022, 67% in 2024).
* **2. How the surface moves.** Sticky strike, sticky moneyness and local vol under a spot slider (Derman 1999); the
  25-delta strike, risk reversal (−5.6) and butterfly (+1.7 vol points) on the Surface; Bergomi's skew-stickiness ratio
  and the delta correction. Weekly test over 242 pairs: sticky moneyness 4.62 vs sticky strike 4.84 vol points
  (strike better 35% of the time); regression ratio R = 2.2 (t = −3.0 on the slope; the mean skew is small, so the
  size is loose). PCA of weekly log-vol changes (30–180 days): 77%, 11%, 7% (level, skew tilt, term twist and
  curvature), as Cont–da Fonseca (2002) found for the S&P 500.
* **3. Static arbitrage.** Gatheral's g derived from Black in total variance; calendar monotonicity; Lee's moment
  formula. Vogt's SVI: g < 0 on k ∈ [0.64, 1.26] (minimum −0.033), a butterfly priced at −7.4·10⁻⁶ of the forward.
  Per-expiry SVI fits of the Surface cross in 2 of 10 neighbouring pairs (the 2–4 day expiries); Part 9's checker
  finds 0 strike-by-strike violations. Lee's wing slopes reach 0.35 (puts) and 0.20 (calls) at 289 days.
* **4. SVI.** Five sliders; wings, vertex, Lee's box b(1+|ρ|) ≤ 2; the jump-wings form; Zeliade's reduction.
  **Lab 1** `fit_svi`. **Replay**: six random starts (12.6–58.7 vol points off) all reach 0.254 in 28–43 evaluations.
  The eleven expiries in JW form; smallest g 0.075.
* **5. SSVI.** θ_T on the wall, smiles hung over it, swept into a surface (3D). **Lab 2** `fit_ssvi`.
  **Replay (3D)**: five starts all end at 0.736 vol points. Gatheral–Jacquier's theorems; the fitted γ = 0.557 > ½,
  so their butterfly condition holds only for θ above ≈ 1.4·10⁻⁷ (every quoted expiry; smallest θ = 0.002), not for
  all θ; measured g_min 0.26. SVI per expiry against SSVI: the cost of consistency is at the short end.
* **6. Dupire's local volatility, derived.** Implied and local surfaces in 3D; the derivation from Fokker–Planck; the
  total-variance form σ²_loc = ∂_T w / g. **Lab 3** `g_function`/`dupire_local_var`. BBF: local/implied skew
  1.70–1.82 at 7–180 days. A Derman–Kani implied tree (40 steps, 91 days) reprices the Surface within 0.62 vol points
  for |k| ≤ 0.2; node local vols within 0.13 points of Dupire's (median).
* **7. Gyöngy.** σ²_loc = E[σ²_T | S_T = K] derived. 100,000 Heston (QE) paths: the conditional variance against
  Dupire from Heston's COS prices, within 0.9 vol points across k ∈ [−0.5, 0.5]. 40,000 local-vol paths reprice the
  Surface within 0.23–1.59 vol points (worst at 9 days); convergence in path count shown live.
* **8. Local volatility's future.** The smile slides against the spot (R_LV = 1.76 measured; Hagan et al. 2002);
  the derivation of R ≈ 2; forward 30-day skews under LV fade from 6.0 (start now) to 2.7 vol points (start in 90 days)
  against 6.5 today.
* **9. Variance swaps.** Hockey sticks summing to the log contract; Itô, Carr–Madan, Neuberger, DDKZ,
  Britten-Jones–Neuberger; the jump term J³/3. The Surface's 30-day strip: √K_var 48.8% against 43.7% ATM; within
  ±20% of the forward 45.0%; 15% of the variance lies beyond ±20%. A −20% log jump leaves the hedge 6% short.
* **10. Replicating on real Bitcoin.** A live ledger (strip, hourly hedge, realized variance) for one month.
  **Lab 4** `strip_replication`. 243 months: hourly-hedged error sd 0.0046 on a mean variance of 0.325; a daily hedge
  against hourly variance, sd 0.129; a listed strike grid reads 1.1 vol points low. Vol swaps: √E[RV] 57.0% against
  E√RV 54.0%; the second-order formula says 4.1 points (overshoots).
* **11. The VIX, and our own.** **Lab 5** `vix` on the Surface's two expiries around 30 days: 49.1% and 48.3%,
  30-day 48.6% against DVOL 45.9%. The correction term derived. 243 weeks: ours 64.0% against DVOL 62.9%,
  correlation 0.993, gap +1.1 ± 2.5. The VIX since 1990 (peak 82.69, 16 March 2020; largest rise +116%, 5 February
  2018); VIX below VIX3M on 90% of days since December 2007.
* **12. The variance risk premium.** 243 weeks, accumulated live: implied 64% against realized 54%, positive 78% of
  weeks, Newey–West t = 4.7; the short side's P&L skewness −1.26, worst month from 12 May 2021. BTZ regression
  (descriptive, not registered): t = 0.13 (2021–25), −0.51 (2024–25). S&P 500 1990–2025: VIX 19.5 against 15.4
  realized; VIX² above realized variance on 86% of days.
* **13. What option prices say about the future.** Three strips (log variance, SVIX, cubic); Martin's bound and BKM
  derived. The Surface at 30 days: Q-vol 49.8%, Q-skew −0.97, Q-kurtosis 6.9. Weekly: Q-skew positive in only 27% of
  weeks (mean −0.40), kurtosis 6.1; SVIX bound 44% a year (31% in 2024–25), valid only under Martin's condition.
* **14. VIX futures, the roll, short-vol notes.** The VX futures curve June 2017 – March 2018 as a 3D ribbon (contango
  on 86% of days, median slope 7.9%). **Lab 6** `vx_index`/`inverse_note`. The rebuilt short-term index rose 96.1% on
  5 February 2018; a −1× note lost the same, after gaining 64% from June to December 2017; the close-of-day hedge was
  1.9 times the note's value (Cheng–Madhavan).
* **15. Volmageddon.** The crisis file (VIX 17.31 → 37.32; Credit Suisse's acceleration event); VIX/VIX3M 1.016 →
  1.327; the amplification mechanism; firm files (XIV allegations and the Second Circuit, SVXY to −0.5×, Griffin–Shams,
  TVIX 2012), and a pointer to Part 11 for LJM and Allianz Structured Alpha.
* **16. Dealer gamma and same-day options.** Long- and short-gamma days simulated live; the fixed-point derivation,
  GEX and its weak point; five seeds: short gamma (k = −0.5) raises volatility ×1.33 with a closing slope +0.26, long
  gamma ×0.80 and −0.23. The public record: Baltussen et al. (2021), Cboe's 62.4% 0DTE share (August 2025), VIX1D,
  Andersen–Fusari–Todorov, Bandi–Fusari–Renò, Dim–Eraker–Vilkov, Beckmeyer et al.
* **17. Learning surfaces.** A VAE over 243 weekly surfaces, replayed (five seeds): 2.93 vol points against 3.59 for
  two principal components; one latent tracks ATM vol (corr −0.96). Latent walks in 3D. An arbitrage-penalised network
  (Ackerer et al. 2020) on the Surface, replayed with its collocation violations: held-out 1.29/0.93/0.82 vol points
  (three splits) in the restored CPU run; zero negative-density grid flags, but one calendar flag in one run, against 0.97/0.84/0.88 unpenalised with 1–10% of the grid in violation and SSVI
  1.96/2.06/2.23. See the saved runs for the distinct vega-weighted metric.
* **18. Who builds surfaces, and who sells them.** Cboe and Deribit as index makers; dealers' quants (Goldman's DDKZ
  and Derman–Kani, Dupire at Paribas, SVI at Merrill Lynch, Andreasen–Huge at Danske Bank); the House's builder.
* **19. Frontier, 2023–2026.** Operator deep smoothing (ICLR 2025), VolGAN (2024), surfaces as images (Kelly et al.
  2023), no-arbitrage SVI and eSSVI (Martini–Mingone 2022); one network for all weeks, trained here (three seeds).
* **For the researcher: reading the density from noisy prices.** The butterfly q̂_h = [C̃(K−h) − 2C̃(K) + C̃(K+h)]/h²
  with independent price errors of sd s: bias (h²/12)q″ + O(h⁴), variance 6s²/h⁴, leading local-MSE half-width
  h* = (864s²/q″²)^{1/8}, MSE_lead(h*) = (√6/6)|q″|s, so the error falls like s^{1/2}. Simulation (a lognormal at 60%, 30
  days, 4,000 draws per width): at the money, s = 0.002/0.01/0.05 per 100 of the forward gives h* = 5.4/8.1/12.1%
  (simulated best 5.5/8.0/10.0 on a 0.25% grid) and a relative error at h* of 1.0/2.3/5.2%; the put wing at 85
  agrees. Deribit BTC options, the Surface's two days, 644 trades of 20–45 days within 15% of spot: trade price
  against mark price, robust sd 0.026 per 100 of the forward; listed strikes 1.08% apart; at the Surface's 46%
  at-the-money volatility h* = 8.4%, about eight strikes on each side; adjacent strikes would leave noise of ±184% of
  the density. Three open problems; pause: errors cut 16-fold halve h* (16^{1/4} = 2) and quarter the error.
* **Outro.** Twelve lines, Rule 12 (the trial counter stays at 312), three desk questions, nine problems (two at
  qualifying-exam level), payoffs, references.

## Build it

```bash
python -m videos.quant.quant12.compute                         # every number (fetches 243 days of Deribit trades once)
EXPLAINER_TTS=silent python tools/qa_scene.py quant12 VarSwap  # one chapter, silent, with a contact sheet
python tools/make.py quant12 --cpu-voice -q m                  # English and Chinese, narrated by Kokoro on the CPU
```

The compute items take about 45 CPU-minutes in all (the neural network items are resumable per seed).

## Textbook audit

| Book · section | Where |
|---|---|
| Gatheral ch. 1 (stochastic and local volatility: Dupire, local variance as conditional expectation, BBF) | ch. 6, 7, 8 |
| Gatheral ch. 2 (Heston) | Part 13 (ch. 7 uses Heston as Gyöngy's test bed) |
| Gatheral ch. 3 (the implied volatility surface: SVI, skew = ½ local skew) | ch. 4, 6; the ATM-skew term structure → Part 14 |
| Gatheral ch. 4 (Heston–Nandi; numerical local vol) | ch. 7 (local vol of a stochastic-vol model, computed); Part 13 |
| Gatheral ch. 5–6 (jumps, default) | Part 13 (ch. 9 shows the jump term of a variance swap) |
| Gatheral ch. 7 (asymptotics: Lee's formula) | ch. 3, ch. 4 (SVI as Heston's long-maturity limit); short expiry → Part 14 |
| Gatheral ch. 8 (dynamics of the surface) | ch. 2, 8 |
| Gatheral ch. 9–10 (barriers, cliquets) | Parts 15, 13 |
| Gatheral ch. 11 (volatility derivatives: variance and volatility swaps, VIX) | ch. 9, 10, 11, 14; VIX options → Part 13 |
| Bergomi, *Stochastic Volatility Modeling*: local volatility (SSR, forward smile of LV) | ch. 2, 6, 8 |
| Bergomi: forward-start options | ch. 8 (LV); Part 13 (SV) |
| Bergomi: variance swaps (forward variance, large returns, strike discreteness) | ch. 9, 10 |
| Bergomi: stochastic volatility, LSV, smile of SV models, ATMF skew | Parts 13, 14 |
| Rebonato, *Volatility and Correlation*: implied vs instantaneous vol, local vol and its dynamics, sticky regimes | ch. 2, 6, 8 |
| Rebonato: correlation | Parts 15, 20, 40 |
| Hull, *OFOD*, "Volatility smiles and volatility surfaces" (put–call parity, implied distribution, the surface, Greeks with a smile) | ch. 1, 2 |
| Hull, "More on models and numerical procedures" (CEV, the implied volatility function model, jumps) | ch. 6 (IVF = local vol); CEV and jumps → Part 13 |
| Sinclair, *Volatility Trading*: variance swaps, the premium, the VIX | ch. 9–12; forecasting → Part 11 |
| Bennett, *Trading Volatility*: skew and term-structure trading, variance and volatility swaps, VIX futures | ch. 2, 9–11, 14; dispersion → Part 11 |

## Papers, and where they appear

Derman–Kani (1994) and Rubinstein (1994) implied trees: ch. 6 · Dupire (1994): ch. 6 · Gyöngy (1986): ch. 7 ·
Neuberger (1994), Carr–Madan (1998), Demeterfi–Derman–Kamal–Zou (1999), Britten-Jones–Neuberger (2000): ch. 9, 10 ·
Derman (1999) "Regimes of volatility": ch. 2 · Cont–da Fonseca (2002): ch. 2 · Berestycki–Busca–Florent (2002): ch. 6,
8 · Hagan–Kumar–Lesniewski–Woodward (2002): ch. 8 · Bakshi–Kapadia–Madan (2003): ch. 13 · Lee (2004): ch. 3 ·
Backus–Foresi–Wu (2004): ch. 1 · Gatheral (2004) SVI: ch. 4 · Carr–Wu (2009), Bollerslev–Tauchen–Zhou (2009): ch. 12 ·
Cheng–Madhavan (2009): ch. 14 · Zeliade (2009): ch. 4 · Roper (2010): ch. 3 · Gatheral–Jacquier (2011, Heston to SVI):
ch. 4 · Andreasen–Huge (2011): ch. 18 · Gatheral–Jacquier (2014): ch. 3, 5 · Martin (2017), Martin–Wagner (2019):
ch. 13 · Dew-Becker–Giglio–Le–Rodriguez (2017): ch. 12 · Andersen–Fusari–Todorov (2017): ch. 16 · Griffin–Shams
(2018): ch. 15 · Hendriks–Martini (2019): ch. 5 · Ackerer–Tagasovska–Vatter (2020): ch. 17 ·
Baltussen–Da–Lammers–Martens (2021): ch. 16 · Bergeron–Fung–Hull–Poulos (2022): ch. 17 · Martini–Mingone (2022):
ch. 4, 5, 19 · Bandi–Fusari–Renò (2023), Beckmeyer–Branger–Gayda (2023), Dim–Eraker–Vilkov (2024): ch. 16 ·
Kelly–Kuznetsov–Malamud–Xu (2023), Vuletić–Cont (2024), Wiedemann–Jacquier–Gonon (2025): ch. 19 · Cboe VIX white
paper; Deribit DVOL methodology: ch. 11.

## Desk questions, with solutions

1. **Why is the VIX above realized on average?** Implied variance is the price of variance under Q, and variance
   rises in bad times, when marginal utility is high: E^Q[RV] − E^P[RV] = cov^P(m, RV)/E^P[m] > 0. Buyers of variance
   pay a premium (Carr–Wu 2009). On Bitcoin since April 2021 it was positive in 78% of weeks (Newey–West t = 4.7); on
   the S&P 500, VIX² exceeded the next 21 days' realized variance on 86% of days since 1990.
2. **Replicate a variance swap.** Hold (2/T)·ΔK/K² of each out-of-the-money option, puts below the forward and calls
   above, and hold (2/T)(1/S_t − 1/F) of the underlying, rebalanced on the contract's sampling clock. The strip is a
   log contract plus a forward; by Itô, −2 log(S_T/S_0) + 2∫dS/S = ∫σ²dt, so strip plus hedge pays realized variance
   and the strip's cost is the fair strike. Errors: the cubic term of discrete returns and jumps, and truncation of
   the strike grid.
3. **Spot falls 5%: where does ATM vol go?** With skew ∂_kσ < 0: sticky strike, ATM moves to the old k = −0.05, so it
   rises by 0.05·|∂_kσ| (R = 1); sticky delta, unchanged (R = 0); local vol, about twice the sticky-strike move
   (R ≈ 2, from BBF). With a skew of 0.4 vol point per 1% of moneyness: +2, 0 and about +4 points.

## Problems, with solutions

1. **Dupire's formula.** The risk-neutral density p(K, T) solves ∂_T p = ½∂_KK(σ²_loc K² p) at zero rates. Since
   C_KK = p, integrate twice in K (the boundary terms vanish): ∂_T C = ½σ²_loc K² C_KK.
2. **The log contract's strip.** Taylor's theorem with integral remainder about F gives
   f(S) = f(F) + f′(F)(S − F) + ∫_0^F f″(K)(K − S)⁺dK + ∫_F^∞ f″(K)(S − K)⁺dK. With f = −log, f″ = 1/K². By Itô,
   ∫_0^T σ²dt = 2∫dS/S − 2 log(S_T/S_0). Taking Q-expectations (zero rates), K_var = (2/T)∫ OTM(K)/K² dK.
3. **SSVI's two conditions.** Calendar (Gatheral–Jacquier 2014, Theorem 4.1): θ_T non-decreasing and
   0 ≤ ∂_θ(θφ) ≤ ((1 + √(1 − ρ²))/ρ²)φ. For φ = η/(θ^γ(1 + θ)^{1−γ}), θφ = η(θ/(1 + θ))^{1−γ} rises, and the upper
   bound reduces to (1 − γ)/(1 + θ) ≤ (1 + √(1 − ρ²))/ρ², true for |ρ| < 1. Butterfly (Theorem 4.2, sufficient):
   θφ(1 + |ρ|) < 4 holds when η(1 + |ρ|) ≤ 2; θφ²(1 + |ρ|) = η²(1 + |ρ|)θ^{1−2γ}(1 + θ)^{2γ−2} ≤ 4 for all θ needs
   γ ≤ ½. For γ > ½ it holds for θ above the root of η²(1 + |ρ|)θ^{1−2γ}(1 + θ)^{2γ−2} = 4: on the Surface
   (γ = 0.557, η(1 + |ρ|) = 0.91) that is θ ≈ 1.4·10⁻⁷, far below the smallest quoted θ (0.002). The calibrated
   surface is therefore free of butterflies at every quoted maturity, but the theorem does not cover θ → 0.
4. **Local skew is twice implied skew.** At short maturity, σ_imp(k) ≈ ((1/k)∫_0^k du/σ_loc(u))^{−1}
   (Berestycki–Busca–Florent). Write σ_loc(u) = σ_0 + s u; then 1/σ_imp ≈ (1/σ_0)(1 − s k/(2σ_0)), so
   σ_imp ≈ σ_0 + (s/2)k: ∂_kσ_imp(0) = ½∂_kσ_loc(0).
5. **Martin's bound.** With E^Q[X] = R_f E[mX] and E[mR] = 1: var^Q(R) = R_f E[mR²] − R_f², and cov(mR, R) =
   E[mR²] − E[R]. Hence E[R] − R_f = var^Q(R)/R_f − cov(mR, R); if cov(mR, R) ≤ 0, E[R] − R_f ≥ var^Q(R)/R_f.
6. **Gatheral's g.** With C/F = N(d₊) − e^k N(d₋), d± = −k/√w ± √w/2 and w = w(k): differentiate in K = F e^k twice.
   Using e^k N′(d₋) = N′(d₊), ∂_k(C/F) = −e^k N(d₋) + N′(d₊)w′/(2√w), and differentiating again and collecting terms
   gives ∂_KK C = (N′(d₋)/(K√w))·[(1 − kw′/(2w))² − (w′²/4)(1/w + 1/4) + w″/2] = g(k)·e^{−d₋²/2}/(K√(2πw)).
7. **The vol swap's convexity.** √V ≈ √K + (V − K)/(2√K) − (V − K)²/(8K^{3/2}) about K = E V. Taking expectations,
   the linear term vanishes: E√V ≈ √K − Var(V)/(8K^{3/2}). For Bitcoin the variance of variance is large and the
   expansion overshoots (4.1 against a measured 3.0 vol points).
8. **(qual) The butterfly's bias and variance.** Taylor-expand C(K ± h) to fourth order: the odd terms cancel in
   C(K−h) − 2C(K) + C(K+h) = h²C″ + (h⁴/12)C⁗ + O(h⁶), and C″ = q, so E q̂_h = q + (h²/12)q″ + O(h⁴). The noise
   (η₋ − 2η₀ + η₊)/h² has variance (1 + 4 + 1)s²/h⁴. MSE = h⁴q″²/144 + 6s²/h⁴; its derivative vanishes at
   h⁸ = 864s²/q″², where the two terms are equal, so MSE(h*) = 12s²/h*⁴ = 12s²|q″|/(√864·s) = (√6/6)|q″|s.
9. **(qual) Correlated errors.** A common error η₀ added to all three prices enters with weights 1 − 2 + 1 = 0 and
   cancels. With corr(η(K), η(K ± h)) = ρ and corr(η(K−h), η(K+h)) = ρ₂, Var = (s²/h⁴)[6 − 8ρ + 2ρ₂]: positively
   correlated neighbours help, which is why smooth (correlated) errors such as a stale forward do less harm than
   independent ones, and why alternating errors (bid–ask bounce, ρ < 0) do more.
## For the researcher

* **The theorems.** Breeden and Litzenberger (1978); Aït-Sahalia and Lo (1998), "Nonparametric estimation of
  state-price densities implicit in financial asset prices," *JF* 53; Aït-Sahalia and Duarte (2003), "Nonparametric
  option pricing under shape restrictions," *J. Econometrics* 116; the second-derivative rate is the standard one of
  nonparametric statistics (Stone 1982).
* **Simplifications.** A lognormal truth, zero rates, three equally spaced strikes, independent errors; the Deribit
  noise is trade against mark, which includes the half-spread and the mark's own error.
* **Open problems.** Optimal rates under shape constraints and correlated errors; stale and alternating errors; tail
  inference.

## Data and reproducibility

* The Surface: Deribit BTC option marks reconstructed from trades on 10 and 11 December 2025. The main fit uses 193 filtered observations from 254 reconstructed marks.
* Weekly surfaces: Deribit trades (00:00–12:00 UTC) every Wednesday from 7 April 2021 to 26 November 2025, 243 days
  with no gaps, each built by `surface.build` and checksummed in `videos/quant/data/manifest.json`.
* Binance BTCUSDT hourly; Deribit DVOL; FRED VIXCLS (1990–2025) and VXVCLS (2007–2025); Yahoo Finance ^GSPC
  (1990–2025); Cboe Futures Exchange VX settlements for the twelve expiries May 2017 – April 2018 (`data.cboe_vx`).
* No strategy was tested; the predictability regression of ch. 12 is descriptive. The trial counter stays at 312.

---

# 量化金融，从零搭建 — 第12部分：波动率曲面

本部分讲波动率曲面本身（形状、报价方式、如何移动）、让它保持无套利的条件、拟合它的参数化与模型（SVI、SSVI、杜皮尔局部波动率及其隐含树、
久恩吉投影）、作为资产的波动率（方差互换与波动率互换、VIX、方差风险溢价、SVIX与风险中性矩、VIX期货与做空波动率票据）、波动率末日、
交易商Gamma与当日到期期权，以及用神经网络学习曲面。每个数字都由本系列自己的代码计算。

*讲的是方法，不构成投资建议。*

## 章节（约63分钟）

* **恐惧的形状。** 基准曲面的三维巡览；1973–2024年的来龙去脉；布莱克–斯科尔斯的平面弯成基准曲面。
* **1. 读懂微笑。** 微笑即风险中性分布的偏度与峰度（Gram–Charlier滑块与Backus–Foresi–Wu公式）；243个周度曲面上的期限结构与偏斜：
  三十天微笑在45%的周里偏向看涨（2022年8%，2024年67%）。
* **2. 曲面如何移动。** 粘性执行价、粘性价值度与局部波动率；二十五delta报价；偏斜粘性比（回归估计R = 2.2）；周度变动的主成分：77%、11%、7%。
* **3. 静态套利。** 从布莱克公式推导g；日历条件；李的矩公式；福格特的SVI中g为负，蝶式价格为负；逐到期日拟合的SVI在10对中有2对相交。
* **4. SVI。** 五个参数；跳跃翼形式；实验1 `fit_svi`；六个随机起点全部收敛到0.254个波动率点。
* **5. SSVI。** 三维中的拟合回放；两条定理；拟合的γ = 0.557 > ½，因此蝶式充分条件只在θ约1.4·10⁻⁷以上成立（覆盖所有报价期限）。
* **6. 杜皮尔局部波动率。** 由福克–普朗克方程推导；实验3；BBF比率1.70–1.82；德曼–卡尼隐含树。
* **7. 久恩吉。** 十万条赫斯顿路径：条件方差与杜皮尔公式相差0.9个波动率点以内；局部波动率蒙特卡洛重新定价基准曲面。
* **8. 局部波动率的未来。** 微笑逆着现价移动（R_LV = 1.76）；远期偏斜从6.0衰减到2.7个波动率点。
* **9. 方差互换。** 对数合约的期权串；截断（±20%以内为45.0%，全部为48.8%）；跳跃项。
* **10. 在真实比特币上复制。** 实验4；243个月：每小时对冲误差标准差0.0046；波动率互换的凸性3.0个波动率点。
* **11. VIX。** 实验5；我们的指数对DVOL：相关系数0.993；1990年以来的VIX与期限结构。
* **12. 方差风险溢价。** 隐含64%对已实现54%，78%的周为正，t = 4.7；预测回归（描述性）t = 0.13；标普500：19.5对15.4。
* **13. 期权价格对未来说了什么。** SVIX与BKM矩；周度风险中性偏度只在27%的周里为正。
* **14. VIX期货与做空波动率票据。** 三维期货带；实验6；重建指数在2018年2月5日上涨96.1%，反向票据损失同样多。
* **15. 波动率末日。** 危机档案；放大机制；机构档案（XIV的指控、SVXY、Griffin–Shams、TVIX）。
* **16. 交易商Gamma与当日到期期权。** 模拟；GEX；公开记录（Cboe：2025年8月0DTE份额62.4%）。
* **17. 学习曲面。** VAE回放（2.93对主成分3.59个波动率点）；带无套利惩罚的网络：留出误差更低且无违规，但按vega加权SSVI更好。
* **18. 业界。** 交易所指数、交易商的量化研究、我们的曲面构建器。
* **19. 前沿。** 算子深度平滑、VolGAN、把曲面当图像、无套利SVI与eSSVI；“一个网络用于所有周”的小规模复现。
* **写给研究者：从含噪价格中读出密度。** 独立价格误差标准差为s时，蝶式q̂_h = [C̃(K−h) − 2C̃(K) + C̃(K+h)]/h²的偏差为(h²/12)q″ + O(h⁴)，方差6s²/h⁴，最佳半宽h* = (864s²/q″²)^{1/8}，MSE_lead(h*) = (√6/6)|q″|s，所以误差按s^{1/2}下降。模拟（60%对数正态、30天、每个宽度4,000次抽取）：平值处s = 每100远期0.002/0.01/0.05时h* = 5.4/8.1/12.1%（0.25%网格上模拟最佳为5.5/8.0/10.0），h*处的相对误差为1.0/2.3/5.2%；85处的看跌翼一致。曲面两天的Deribit BTC期权，644笔20–45天、距现价15%以内的成交：成交价相对标记价的稳健标准差为每100远期0.026；挂牌执行价间距1.08%；在曲面平值波动率46%下h* = 8.4%，每边约八个执行价；用相邻执行价会留下相当于密度±184%的噪声。三个开放问题；暂停题：误差降为十六分之一时h*减半（16^{1/4} = 2），误差降为四分之一。

## 交易台问题与解答

1. **为什么VIX平均高于已实现波动率？** 隐含方差是方差在Q下的价格，而方差在坏时期上升，那时边际效用高：E^Q[RV] − E^P[RV] =
   cov^P(m, RV)/E^P[m] > 0。方差的买方支付溢价（Carr–Wu 2009）。2021年4月以来的比特币上，它在78%的周里为正（纽维–韦斯特t = 4.7）；
   1990年以来的标普500上，VIX²在86%的交易日高于其后21天的已实现方差。
2. **复制方差互换。** 持有每个虚值期权(2/T)·ΔK/K²份（远期以下用看跌，以上用看涨），并按合约的采样时钟持有(2/T)(1/S_t − 1/F)份标的。
   期权串是对数合约加一份远期；由伊藤公式，−2 log(S_T/S_0) + 2∫dS/S = ∫σ²dt，所以期权串加对冲支付已实现方差，期权串的成本就是公平执行价。
   误差来自离散收益和跳跃的三次项，以及执行价网格的截断。
3. **现价下跌5%，平值波动率去哪里？** 偏斜∂_kσ < 0时：粘性执行价下，平值移到原来的k = −0.05，上升0.05·|∂_kσ|（R = 1）；
   粘性delta下不变（R = 0）；局部波动率下约为粘性执行价的两倍（由BBF，R ≈ 2）。若偏斜为每1%价值度0.4个波动率点：+2、0、约+4个点。

## 习题与解答

1. **杜皮尔公式。** 零利率下风险中性密度满足∂_T p = ½∂_KK(σ²_loc K² p)。因为C_KK = p，对K积分两次（边界项消失）得∂_T C = ½σ²_loc K² C_KK。
2. **对数合约的期权串。** 在F处带积分余项的泰勒展开给出f(S) = f(F) + f′(F)(S − F) + ∫_0^F f″(K)(K − S)⁺dK + ∫_F^∞ f″(K)(S − K)⁺dK。
   取f = −log，f″ = 1/K²。由伊藤公式∫_0^T σ²dt = 2∫dS/S − 2 log(S_T/S_0)，取Q期望（零利率）得K_var = (2/T)∫ OTM(K)/K² dK。
3. **SSVI的两个条件。** 日历条件（Gatheral–Jacquier 2014定理4.1）：θ_T不减且0 ≤ ∂_θ(θφ) ≤ ((1 + √(1 − ρ²))/ρ²)φ；对幂律φ，
   θφ = η(θ/(1 + θ))^{1−γ}递增，上界化为(1 − γ)/(1 + θ) ≤ (1 + √(1 − ρ²))/ρ²，对|ρ| < 1成立。蝶式条件（定理4.2，充分）：
   η(1 + |ρ|) ≤ 2时θφ(1 + |ρ|) < 4成立；θφ²(1 + |ρ|) = η²(1 + |ρ|)θ^{1−2γ}(1 + θ)^{2γ−2} ≤ 4对所有θ成立需要γ ≤ ½。γ > ½时，
   它只在方程η²(1 + |ρ|)θ^{1−2γ}(1 + θ)^{2γ−2} = 4的根以上成立：在基准曲面上（γ = 0.557，η(1 + |ρ|) = 0.91）约为θ ≈ 1.4·10⁻⁷，
   远低于最小的报价θ（0.002）。因此校准出的曲面在每个报价期限上都没有蝶式套利，但定理不覆盖θ → 0。
4. **局部偏斜是隐含偏斜的两倍。** 短期限下σ_imp(k) ≈ ((1/k)∫_0^k du/σ_loc(u))^{−1}（Berestycki–Busca–Florent）。设σ_loc(u) = σ_0 + s u，
   则1/σ_imp ≈ (1/σ_0)(1 − s k/(2σ_0))，所以σ_imp ≈ σ_0 + (s/2)k：∂_kσ_imp(0) = ½∂_kσ_loc(0)。
5. **马丁下界。** 由E^Q[X] = R_f E[mX]和E[mR] = 1：var^Q(R) = R_f E[mR²] − R_f²，cov(mR, R) = E[mR²] − E[R]。所以
   E[R] − R_f = var^Q(R)/R_f − cov(mR, R)；若cov(mR, R) ≤ 0，则E[R] − R_f ≥ var^Q(R)/R_f。
6. **盖瑟尔的g。** C/F = N(d₊) − e^k N(d₋)，d± = −k/√w ± √w/2，w = w(k)：对K = F e^k求两次导。利用e^k N′(d₋) = N′(d₊)，
   ∂_k(C/F) = −e^k N(d₋) + N′(d₊)w′/(2√w)，再求导并整理得∂_KK C = g(k)·e^{−d₋²/2}/(K√(2πw))，其中
   g = (1 − kw′/(2w))² − (w′²/4)(1/w + 1/4) + w″/2。
7. **波动率互换的凸性。** 在K = E V处展开√V ≈ √K + (V − K)/(2√K) − (V − K)²/(8K^{3/2})。取期望，线性项消失：
   E√V ≈ √K − Var(V)/(8K^{3/2})。比特币的方差的方差很大，展开会高估（4.1对实测的3.0个波动率点）。

8. **（资格考试）蝶式的偏差与方差。** 把C(K ± h)展开到四阶：C(K−h) − 2C(K) + C(K+h) = h²C″ + (h⁴/12)C⁗ + O(h⁶)，奇数项抵消，C″ = q，所以E q̂_h = q + (h²/12)q″ + O(h⁴)。噪声(η₋ − 2η₀ + η₊)/h²的方差为(1 + 4 + 1)s²/h⁴。MSE = h⁴q″²/144 + 6s²/h⁴，导数在h⁸ = 864s²/q″²处为零，此时两项相等，MSE_lead(h*) = (√6/6)|q″|s。
9. **（资格考试）相关的误差。** 加在三个价格上的共同误差η₀以权重1 − 2 + 1 = 0进入，相互抵消。若corr(η(K), η(K ± h)) = ρ、corr(η(K−h), η(K+h)) = ρ₂，则Var = (s²/h⁴)[6 − 8ρ + 2ρ₂]：正相关的相邻误差有帮助，所以平滑（相关）的误差如陈旧的远期危害较小，而交替的误差（买卖价反弹，ρ < 0）危害更大。

## 数据与可复现性

* 基准曲面：2025年12月10日和11日的Deribit比特币期权成交。
* 周度曲面：2021年4月7日至2025年11月26日每个周三的Deribit成交（UTC 00:00–12:00），共243天，无缺失，每一份都记录校验和。
* 币安BTCUSDT小时数据；Deribit DVOL；FRED的VIXCLS与VXVCLS；雅虎财经^GSPC；Cboe期货交易所的VX结算价（`data.cboe_vx`）。
* 没有检验任何策略；第12章的预测回归是描述性的。试验计数器保持310。

## 写给研究者

* **定理。** Breeden与Litzenberger（1978）；Aït-Sahalia与Lo（1998），*JF* 53；Aït-Sahalia与Duarte（2003），*J. Econometrics* 116；二阶导数的速率是非参数统计中的标准速率（Stone 1982）。
* **简化。** 对数正态真值、零利率、三个等间距执行价、独立误差；Deribit的噪声是成交相对标记价，包含半个价差和标记价自身的误差。
* **开放问题。** 形状约束与相关误差下的最优速率；陈旧与交替的误差；尾部推断。


## Scientific scope of this polish pass

The Surface pools marks from 00:00 through 12:00 UTC around an 08:00 reference.
Later records enter its reference spot and fitted smile. The reconstruction is
neither a simultaneous executable quote sheet nor an established 08:00 trading
information set. All contracts in the replication illustration are hypothetical
zero-carry dollar payoffs; Binance paths and Deribit references need not coincide.
Its running strip curve is intrinsic payoff evaluated at the current spot, not
an option mark with remaining maturity. Discrete hedging and finite strikes leave
replication error. The 243 weekly-start thirty-day windows overlap.

SVI's finite g scan is a diagnostic. The complete density characterization also
requires positive smooth variance and tail boundary conditions; Lee's moment
formula constrains asymptotic limsup slopes. It does not require linear wings or
prove finiteness at a critical moment endpoint. SSVI's eta cap alone does not
certify butterfly freedom when gamma exceeds one half. The final fitted Surface
satisfies the sufficient inequalities above its reported theta threshold, covering
the displayed quoted maturities. Intermediate fits and arbitrarily short expiries
are not all certified. Gyongy's result concerns suitable continuous Ito processes
and marginal distributions under stated existence and integrability conditions.
It does not cover arbitrary jump models or determine joint laws. Forward ratio
payoffs here omit the start-date spot multiplier of asset-weighted forward starts.

The Gram--Charlier illustration clips negative polynomial densities, renormalizes
and martingale-shifts them. Slider values need not be exact moments of the final
law. Its skew relation is local. Log-return moments are distinct from SVIX's
simple-return variance; finite-tail extrapolation matters especially for higher
moments. Martin's covariance condition is not established here for Bitcoin.
Annualizing a thirty-day conditional bound does not guarantee a compounded annual
return. Historical Jensen comparisons are physical sample statistics, not market
fair volatility-swap strikes.

The VAE and PCA reconstructions use all weeks. In the frontier, only the final
latent-conditioned MLP holds out the last 20% of weeks; the full-sample VAE and
those weeks' complete fitted grids supply their codes. The quantity called
`dec_rmse` in the unchanged calculation is a two-component PCA reconstruction,
with coordinates clamped to its grid. It is not the VAE decoder. PCA uses all
weeks, and SSVI fits the test week's own quotes, so these are conditional
reconstruction comparisons with different information, not a predictive race.
The graph-neural-operator paper is discussed separately; the local MLP is an
illustration rather than its implementation. Three same-date quote splits and
seed min--max ranges do not supply confidence intervals or global arbitrage proofs.
The restored penalized runs have no negative-g points on the audit grid, but one
run has one negative-calendar-slope point out of 12,060 (0.00829%); it is shown
without rounding to zero. Unchanged fixed-seed neural fits can vary numerically
with software and hardware, so the evidence binds the actual restored caches.

Dealer gamma's first hedge variable is dollar notional, with a separate share
trade. The simulation defers half the hedge and measures dispersion across days
of the pre-close return. Its singularity belongs to a linear toy. Open interest
does not identify dealer inventory. The August 2025 62.4% figure refers to SPX
options specifically. Daily-reset flows use pre-move NAV; contango does not
promise convergence profit, and target flows alone do not identify actual causal
market impact. The limited-liability note illustration excludes real fees and
intraday acceleration and differs from a variance-swap payoff.

The research bandwidth minimizes a leading local Taylor MSE with non-zero
curvature, not the exact finite-width error. Formula widths of 12.1% (ATM) and
12.7% (put wing) exceed the original simulation grid's 10% maximum; its boundary
minimum is not confirmation of those optima. Trade--mark robust dispersion does
not identify independent measurement noise. The plug-in bandwidth and the
adjacent-strike one-standard-deviation scale remain conditional illustrations.
A common additive or affine price error cancels in a butterfly; generic stale or
forward-related errors need not. The pause has a worked answer: width halves and
approximate RMSE quarters after a sixteenfold reduction in noise standard deviation.

Coinbase completed Deribit on 14 August 2025. Its September 2026 filing records
about $4.3 billion of acquisition consideration; the earlier $2.9 billion
announcement used a different stock valuation. Sources checked include
[Coinbase's filing](https://www.sec.gov/Archives/edgar/data/1679788/000167978826000122/coin-20260930.htm),
[Cboe's SPX volume report](https://www.cboe.com/insights/posts/spx-0-dte-options-jump-to-record-62-share-in-august),
[Cboe's settlement specifications](https://www.cboe.com/tradable_products/vix/vix_futures/specifications),
and [Deribit's DVOL methodology](https://insights.deribit.com/exchange-updates/dvol-deribit-implied-volatility-index/).
VIX futures settle to a special opening quotation; the model proxy and hourly
DVOL observations have different selection and time-aggregation conventions.
Their gap is not attributed solely to the wings.

All 28 original compute items are restored from frozen inputs. The original
compute and House sources, manifest, registry and track record remain unchanged.
The as-of-Part-12 counter is 312 and the global registry 23,562; this pass adds no
market trials and opens no sealed holdout. Visual and playback QA are still in
progress. Full production-voice listening remains pending.
