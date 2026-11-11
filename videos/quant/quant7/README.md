# Quant, Built — Part 7: Time Series and Volatility

Part 7 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act II, the Mathematical Toolkit. Return autocorrelations in these samples
are small; magnitudes show stronger persistence. This part builds models for conditional risk, from autoregression to
foundation models. The reused 2020 comparison is retrospective, with later entrants explicitly counted; the separate
2021-onward holdout stays sealed.

Empirical examples use the series' code ([`compute.py`](compute.py), the House's
[`vol`](../../../explainer/quant/house/vol.py), tested in `tests/test_quant_house.py`) and public sources:
Kenneth French's daily and monthly market returns and size deciles, FRED's Treasury yields (DTB3, DGS5, DGS10) and
VIX (VIXCLS), and Binance's one-minute, daily and perpetual-futures prices for Bitcoin. Simulations are seeded and
labeled on screen. Published results we did not run (the foundation-model comparison) are labeled as data from the
paper.

*An education in methods, not investment advice.*

## Chapters (about 60 minutes)

* **The river under the noise.** A century of the US market's daily moves, clusters lighting up (1929–33, 1987,
  2008, 2020); pause and predict: sign or size? The autocorrelation of returns is 0.05 at lag 1 with small linear correlations thereafter;
  of absolute returns 0.31 at lag 1, still 0.14 at lag 100 and 0.12 at lag 250 (24,896 days). Bitcoin's river drawn
  live by a Kalman filter. History: Yule 1927, Kalman 1960, Box–Jenkins 1970, Dickey–Fuller 1979, Engle 1982,
  Bollerslev 1986, Engle–Granger 1987, Hamilton 1989, RiskMetrics 1994, the 2003 Nobel, Corsi 2009, roughness 2018,
  foundation models 2024. Objectives; the House.
* **1. Stationarity, ARMA and Box–Jenkins.** An AR(1) on a slider (φ = 0 → 0.99) with its ACF and variance; weak
  stationarity; the derivation (MA(∞) form, variance, ACF, forecast and half-life, Ljung–Box); Wold; ACF/PACF
  fingerprints; the identify–estimate–check loop. **Lab:** `ar_fit` on log VIX 1990–2020 (7,810 days): φ = 0.982,
  half-life 39 days; AIC picks ARMA(2,1), whose residuals still fail Ljung–Box (Q₂₀ = 43): residual serial dependence within the tested candidate set, not proof of long memory. Ljung–Box
  on 94 years of returns: Q = 179; on squared returns Q = 14,593.
* **2. Unit roots and spurious regression.** Sixty stationary paths in a band against sixty random walks in a √t
  funnel. 20,000 simulated Dickey–Fuller t-statistics stream into a histogram left of N(0,1): mean −1.54, 46% below
  −1.645, 5% point −2.89. The limit derived (telescoping, Donsker and demeaning for the fitted-constant specification).
  **Lab:** `adf` (5 lags): Bitcoin's log price t = −0.93, the US log index 0.64, the 10-year yield −1.03 (non-rejection, not proof of a unit root), log VIX −6.48 (rejects). Granger–Newbold: 89% false rejections in levels, 5% in differences, median
  R² 0.17; Phillips (1986): median |t| grows from 3.0 at T = 50 to 20.1 at T = 2,000. Bitcoin on the US market: t = 24
  in levels, 6.7 in changes.
* **3. Cointegration.** Murray's (1994) drunk and her dog, simulated: ADF −0.95 on her position, −11.5 on the gap.
  Bitcoin spot and perpetual, 2020: ADF 0.96 and 0.94; Engle–Granger t = −7.2 (5%: −3.34); the basis is AR(1) with
  ρ = 0.55, half-life 1.2 days. ECM, Granger representation, the EG critical value, the VECM and Johansen's trace
  statistic derived. **3D:** daily 3-month, 5-year and 10-year yields 1990–2020 as a cloud seen edge-on: principal
  axes 95.2%, 4.7% and 0.15% of the variance; trace statistics 68.0, 8.0, 2.0 against 29.8, 15.5, 3.8: rank 1, two
  common trends, the leash a curvature-like combination (−0.36, 1, −0.74).
* **4. Hidden regimes.** Hamilton's filter as two jars of belief, predicted and updated month by month through 1929,
  then over the century; the filter, durations and stationary share derived. EM replay: most log-likelihood gain occurs early, with convergence continuing to a local solution. Calm +12%/13%/55 months, storm −15%/36%/10 months, 16% of the time in the storm. Pause:
  one −8% month moves the storm probability from 0.02 to 0.09.
* **5. The Kalman filter and stochastic volatility.** The belief bell: predict (widen), observe, update (product of
  bells, gain K). Derivation by completing the square; the steady-state gain K(q/r); Bitcoin q/r = 0.38, K = 0.45.
  **Lab:** `kalman_states`, the river redrawn with its band. Stochastic volatility by QML (Harvey–Ruiz–Shephard
  1994) on 94 years: φ = 0.992, σ_η = 0.125, half-life 88 days; correlation with GARCH volatility 0.88.
* **6. ARCH and GARCH by maximum likelihood.** Engle 1982; the leaky bucket (tap ω, leak 1 − β, splash αr²) simulated
  with US parameters; the long-run level, the EWMA unrolling, the likelihood, the term structure, GARCH as ARMA(1,1)
  for r², derived. **Lab:** `garch_filter` and its likelihood: α = 0.105, β = 0.884, log L 84,088, half-life 63
  days. **3D replay:** the variance-targeted likelihood surface over α and the persistence α + β (0.84 to 0.999, all
  stationary), a simplex search racing up the persistence slope and crawling across α in 66 iterations to (0.104,
  0.884); coordinate slopes differ; precision requires a covariance calculation; EWMA at the far edge α + β = 1.
* **7. The GARCH zoo.** The (α, β) plane: the covariance-stationary triangle and Nelson's (1990) strict-stationarity
  boundary beyond it; pause: α + β = 1.05 both times, E ln(αz² + β) = −0.0074 (0.30, 0.75: stationary) and
  +0.0084 (0.25, 0.80: explosive). Derived: the unrolled product, the LLN argument, strict Jensen (nondegenerate IGARCH can be strictly stationary with infinite variance), the QMLE score. News-impact curves morph GARCH → GJR (a fall raises variance 4× a rise; log L 84,336)
  → EGARCH (84,342); Bitcoin γ = 0.14. Fat tails: GARCH residuals' kurtosis 7.8; Student-t ν = 5.6, log L +911.
* **8. Correlations that move.** One stock–bond covariance ellipse per year 1962–2020, breathing and tilting, with a
  correlation dial. VEC 51 million, BEKK 25,050, DCC 302 parameters for 100 assets; the DCC recursion and two-step
  likelihood; a = 0.027, b = 0.969; EWMA overlay. Pause: a 60/40 model assuming ρ = +0.3 in 2010 said 12.5%; the
  correlation was −0.49 and the portfolio's volatility 9.9%.
* **9. Realized volatility.** One wild Bitcoin day (26 June 2019) cut into squares at 30, 10, 5 and 1 minutes. The
  signature plot built point by point: in 2019, 1-minute RV reads 1.6% more than 5-minute; over the whole sample, 10%.
  Derived: RV → IV, the BNS CLT, the noise bias 2nη², Bandi–Russell's n* (median Δ* ≈ 9 minutes), TSRV, realized
  kernel. Averages: 106% (1-min), 96% (5-min), 93% (TSRV and kernel), 92% (bipower); the daily CLT band.
* **10. Jumps and HAR.** Squares against bipower rectangles; the BNS (2006) ratio test: 27% of days jump at 1%, 16%
  at 0.1%; 12 March 2020 has z = 0.05: no jump detected by this nominal test, not proof of no jump. HAR as an AR(22) staircase against GARCH's geometric
  weights; the ACF of log RV against the simulated log-HAR and an AR(1). **Lab:** `har_fit`: b_d 0.41, b_w 0.03,
  b_m 0.43, R² 0.38; the rolling-252-observation replay (about eight Bitcoin months) (the week and month trade places). HARQ attenuation derived; b_q = −3.0
  (t −0.7); HAR-CJ jump coefficient 1.50; log-HAR.
* **11. Is volatility rough?** fBm with H = 0.1 and 0.5, zoomed twice. **Lab:** `log_rv_scaling` recovers H = 0.11
  and 0.50 on simulated paths; Bitcoin's log RV gives H = 0.13. The RFSV predictor's power-law kernel; HAR as its
  cheap approximation; Part 14 builds the models.
* **12. Scoring forecasts honestly.** Hansen–Lunde. Expected-loss curves as the proxy gets noisier: QLIKE's minimum
  stays at the truth, MSE on volatility slides to 0.64 (Patton 2011, proved). Simulation (200 runs × 2,500 days):
  QLIKE and MSE on variance pick the truth under every proxy; MSE and MAE on volatility pick 0.8 × truth against
  squared returns. **Lab:** `qlike`, `diebold_mariano`; Mincer–Zarnowitz slopes (HAR 0.98, log-HAR 1.35). The model
  confidence set (Hansen–Lunde–Nason 2011): at 90% all nine survive; at 75% EWMA, HAR and GARCH drop out.
* **13. Training the networks.** LSTM, transformer and HARNet (Reisenhofer–Bayer–Hautsch 2022, initialised at
  log-HAR): 1,233, 2,625 and 111 parameters. Training replays with five-seed bands and the validation forecasts at
  epochs 0, 5, 10, 20, 40 and best; seed spreads (LSTM 0.366–0.378, transformer 0.401–0.433, HARNet 0.359–0.362);
  HARNet starts at validation loss 0.272 and ends at 0.270.
* **14. The race.** Networks train to June 2019 and validate H2; classical fits use all of 2019. The reused 2020 comparison is retrospective. A live leaderboard: EWMA leads until 11 March,
  12 March reshuffles everything. QLIKE: HARNet 0.360, log-HAR 0.363, LSTM 0.371, transformer 0.410, HARQ 0.426, HAR
  0.427, GJR 0.444, GARCH 0.452, EWMA 0.512; DM t against log-HAR: HARNet −0.99, LSTM +1.46. On MSE, GJR first. The
  2020 overlay.
* **15. Foundation models and the frontier.** Chronos's tokenisation drawn; a toy Chronos-style model trained here on 3,000 synthetic volatility series (128 bins, context 64, a 42,176-parameter numpy network, 3 seeds, replayed) and run zero-shot on Bitcoin 2020: QLIKE 0.416 against log-HAR's 0.363 (DM t = +1.7, within noise; between HAR and the transformer), its 10–90% fan covering 85% of days.
  Brini (2026), Table 6, h = 1, as published: TTM 0.982, HAR 0.998, Sundial 0.998, log-HAR 1.000, ARMA 1.000,
  Moirai-2.0-S 1.038, TimesFM-2.5 1.086, Moirai-MoE-S 1.090, Chronos-Bolt-S 1.110, Chronos-Bolt-B 1.121, Toto 1.214,
  Lag-Llama 1.532. The 2022–2026 papers.
* **16. March 2020.** The crisis file; every model's forecast for 12 March (62–76%) against 457%; the weeks
  around it; √T against GARCH's term structure (85% next day, 52% over a year, 18% long run).
* **17. Industry.** RiskMetrics (λ = 0.94 daily, 0.97 monthly; MSCI's 2010 acquisition): our λ grid on the US market
  1990–2020, RMSE best at the grid edge 0.85, QLIKE at 0.94. Barra USE4's longer correlation half-life and
  volatility regime adjustment (MSCI's words); our replica on ten size deciles peaks at 2.1 (1929–33), 2.7 (1987),
  2.2 (2020); QLIKE 1.70 → 1.66. Volatility targeting (Harvey et al. 2018; MOP 2012's 40% target and 60-day centre
  of mass): on the US market 1927–2020 at 10%, Sharpe 0.44 → 0.58, worst-1% mean −2.78% → −2.55%, maximum drawdown of additive cumulative simple excess returns
  1.04 → 0.67. The VIX above next-month realized on 85% of days (by 4.1 points); R² 0.52 (VIX), 0.50 (GARCH); both
  significant together (t 7.2 and 3.2).
* **18. The volatility forecaster.** The module table; Rule 8; eleven models registered in this part, the series' trial
  counter at 307. **Lab:** `forecast` on 31 Dec 2020: Bitcoin 91% tomorrow, 84% over 22 days; the US term structure
  9.1% (1 day) → 15.3% (1 year), long run 17.6%.
* **For the researcher: comparing nested forecasts.** Why Diebold–Mariano fails when one model nests another (the population differential is zero; estimation noise makes $E[\bar d] < 0$; Clark and McCracken's non-standard limit), and Clark and West's (2007) adjusted MSPE. Simulation (2,000 runs, $R$ = 100, $P$ = 200, a persistent regressor): with the null true DM rejects 0.4% at a nominal 5% (mean −0.84), CW 2.9% (−0.35); power at a slope of 0.05: 1.0% against 8.0%; at 0.1: 3.6% against 25.4%. Bitcoin's RV, recursive 2019–2020: HAR over one lag MSE ratio 1.013, DM −0.23, CW 0.82; HARQ over HAR 1.654 (March 2020), both −1.05. Three open problems.
* **Recap, four desk questions, eight problems (two at qualifying-exam level), payoffs, references.**

## Textbook audit

| Book / section | Chapter |
|---|---|
| Tsay, *Analysis of Financial Time Series* (3e) ch. 1 (stylized facts) | Hook, 1 |
| Tsay ch. 2 (ACF, AR/MA/ARMA, Ljung–Box, unit roots; long memory) | 1, 2; long memory in 10 |
| Tsay ch. 3 (ARCH, GARCH, IGARCH, GARCH-M, EGARCH, TGARCH, SV) | 6, 7; SV in 5; GARCH-M named in 7 (Part 23) |
| Tsay ch. 4 (nonlinear: TAR, STAR, Markov switching, neural networks) | 4; networks in 13; TAR/STAR → Part 27 |
| Tsay ch. 5 (high-frequency: bid–ask bounce, nonsynchronous trading, durations) | 9; durations → Part 36 |
| Tsay ch. 7 (extreme values, VaR) | → Part 40 (said in 16) |
| Tsay ch. 8 (VAR, cointegration, ECM, pairs) | 3; pairs → Part 33 |
| Tsay ch. 10 (multivariate volatility: EWMA, BEKK, DCC) | 8 |
| Tsay ch. 11 (state space, Kalman filter and smoother) | 5 |
| Tsay ch. 12 (MCMC for SV) | named in 5 (QML used); Bayesian methods → Part 6 |
| Hamilton, *Time Series Analysis*, ch. 3–5 (ARMA, forecasting, MLE) | 1, 6 |
| Hamilton ch. 6 (spectral analysis) | named in 1 (same information in frequency); not used |
| Hamilton ch. 10–11 (VARs) | 3 (VECM); impulse responses → Part 32 |
| Hamilton ch. 13 (Kalman filter) | 5 |
| Hamilton ch. 15–17 (unit roots, functional CLT, DF asymptotics) | 2 |
| Hamilton ch. 18–20 (multivariate unit roots, cointegration, Johansen FIML) | 3 |
| Hamilton ch. 21 (ARCH/GARCH) | 6, 7 |
| Hamilton ch. 22 (regime switching) | 4 |
| Brockwell–Davis, *Introduction to Time Series and Forecasting* (stationarity, ARMA, forecasting; ARIMA; GARCH/SV; state space) | 1, 2, 6, 5 |
| Francq–Zakoian, *GARCH Models* (stationarity; EGARCH/GJR; QMLE; multivariate GARCH) | 7, 8 |
| Aït-Sahalia–Jacod, *High-Frequency Financial Econometrics* (IV without noise and its CLT; noise; jump tests) | 9, 10; spot volatility and irregular sampling named in 9; activity index → Part 13 |
| Andersen, Bollerslev, Christoffersen and Diebold (2006), "Volatility and correlation forecasting", *Handbook of Economic Forecasting* | 6–12, 17 |
| Campbell–Lo–MacKinlay ch. 12 (changing volatility, ANNs, data snooping) | 6, 13, 12 |
| McNeil–Frey–Embrechts, *QRM*, financial time series (stylized facts, GARCH, EWMA; filtered historical simulation) | Hook, 6, 17; FHS → Part 40 |

## Reading guide

Classics: Yule (1927); Kalman (1960); Box and Jenkins (1970); Granger and Newbold (1974); Ljung and Box (1978);
Dickey and Fuller (1979); Engle (1982); Bollerslev (1986, 1987); Phillips (1986); Engle and Granger (1987); Engle,
Lilien and Robins (1987); Hamilton (1989); Nelson (1990, 1991); Johansen (1991); Bollerslev and Wooldridge (1992);
Hall, Anderson and Granger (1992); Glosten, Jagannathan and Runkle (1993); Engle and Ng (1993); Murray (1994), "A
drunk and her dog: an illustration of cointegration and error correction", *The American Statistician* 48(1):37–39;
Harvey, Ruiz and Shephard (1994); Diebold and Mariano (1995); J.P. Morgan/Reuters, *RiskMetrics Technical Document*
(4th ed., 1996). Realized volatility: Andersen, Bollerslev, Diebold and Labys (2000, 2003); Barndorff-Nielsen and
Shephard (2002, 2004, 2006); Zhang, Mykland and Aït-Sahalia (2005); Andersen, Bollerslev and Diebold (2007);
Bandi and Russell (2008); Barndorff-Nielsen, Hansen, Lunde and Shephard (2008); Corsi (2009). Evaluation:
Mincer and Zarnowitz (1969); Hansen and Lunde (2005); Patton (2011); Hansen, Lunde and Nason (2011); Bollerslev,
Patton and Quaedvlieg (2016). Roughness: Gatheral, Jaisson and Rosenbaum (2018). Industry: Moskowitz, Ooi and
Pedersen (2012), *JFE* (40% ex-ante volatility per position, 60-day centre of mass, verified in the paper); Moreira and
Muir (2017); Harvey, Hoyle, Korgaonkar, Rattray, Sargaison and Van Hemert (2018), *JPM*; Bollerslev, Hood, Huss and
Pedersen (2018), *RFS*; Carr and Wu (2009); Christensen and Prabhala (1998); MSCI, "Market Factor: Not Just For Show"
(Dec. 2011). Frontier: Zhang, Zhang, Cucuringu and Qian (2022); Reisenhofer, Bayer and Hautsch (2022); Christensen,
Siggaard and Veliyev (2023), *JFEc* 21(5); Ansari et al. (2024, Chronos; 2025, Chronos-2); Das et al. (2024,
TimesFM); Woo et al. (2024, Moirai); Ekambaram et al. (2024, TTM); Goel, Pasricha, Magris and Kanniainen (2025);
Rahimikia, Ni and Wang (2025); Shi et al. (2025, Kronos); Brini (2026), arXiv 2607.05291.

## Build it

```bash
python -m videos.quant.quant7.compute                    # every number, cached in .cache/quant7/ (resumable)
EXPLAINER_TTS=silent python tools/qa_scene.py quant7 Race     # one chapter, silent, with a contact sheet
python tools/make.py quant7 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

Compute: about 25 CPU-minutes in all (networks about 4 minutes on one thread; the toy foundation model about 6, in numpy, because on the shared build machine the PyTorch version was repeatedly killed for memory).
Training uses one thread on purpose: with renders running, PyTorch's default thread pool was measured forty times
slower. The network runs are cached one file per seed in `.cache/quant7/training_runs/`.

**What a production run with the real foundation models would add.** Chronos-Bolt, TimesFM 2.5, TTM-r2 and Moirai
were not installed in this environment (and installing them was not possible here), so chapter 15 shows the published
comparison (Brini 2026) and a tokenizer-inspired embedding MLP trained here, rather than a transformer replication. A production run would add their zero-shot
forecasts of Bitcoin's 2020 realized variance from the same 2017–2019 context, scored by the same QLIKE, DM, MZ and MCS
as the race, with model revisions and weight hashes recorded, and a check that their pretraining corpora exclude 2020
market data (the leakage caveat on screen).

## Desk questions, with solutions

1. **Daily volatility is 1%.** With independent returns and constant variance, variances add: over a week
   1% × √5 ≈ 2.2%, over a year 1% × √252 ≈ 15.9%. The rule fails in three ways. Volatility mean-reverts, so from a
   high level the average over a horizon is lower than today's level (GARCH: E_t[σ²_{t+h}] = σ̄² +
   (α + β)^{h−1}(σ²_{t+1} − σ̄²)); chapter 16 shows 85% falling to 52% over a year. Autocorrelated returns change the
   sum's variance by the factor 1 + 2Σ(1 − k/h)ρ_k (Lo–MacKinlay's variance ratio). And quantiles of fat-tailed
   returns do not scale by √T, because the sum of fat-tailed returns is closer to normal than each one.
2. **A t of 24 between two prices.** First check both series for unit roots (ADF). If both have one, the t-statistic
   is meaningless (chapter 2: 89% false rejections, and it grows like √T). Test the residual of the levels regression
   with Engle–Granger critical values (about −3.34 at 5% for two series, not −2.86), or regress changes on changes.
3. **A model beats GARCH on MSE over a year with a crash in it.** Squared errors of variance forecasts are dominated
   by the largest days, so one day can decide the race. Score with QLIKE, which is robust to noise in the realized
   proxy (Patton 2011), compare against HAR rather than a weak benchmark, use a Diebold–Mariano test with a HAC
   variance and a model confidence set, and check that the ranking survives without the crisis weeks.
4. **A GARCH fit gives α + β = 1. Is the process stationary?** Not covariance-stationary: the unconditional variance
   ω/(1 − α − β) is infinite. With positive α, nonconstant squared iid shocks and log integrability, it can be strictly stationary: unrolling gives σ_t² = ω Σ_k Π_{j≤k}(αz²_{t−j} + β),
   which converges when E ln(αz² + β) < 0 (Nelson 1990), and by Jensen E ln(αz² + β) < ln E(αz² + β) = ln(α + β) = 0.
   Forecasts of the variance never revert (the RiskMetrics EWMA is this case with ω = 0).

## Problems, with solutions

1. **GARCH's term structure.** Write σ̄² = ω/(1 − α − β). Since E_t[r²_{t+k}] = E_t[σ²_{t+k}], taking expectations of
   σ²_{t+k+1} − σ̄² = α(r²_{t+k} − σ̄²) + β(σ²_{t+k} − σ̄²) gives E_t[σ²_{t+k+1}] − σ̄² = (α + β)(E_t[σ²_{t+k}] − σ̄²),
   and by induction E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²). A shock halves after log 0.5/log(α + β)
   days: 63 days for the US market's 0.989.
2. **GARCH as ARMA, and its kurtosis.** Let ν_t = r_t² − σ_t², a martingale difference. Substituting σ_t² = r_t² − ν_t
   into the GARCH recursion gives r_t² = ω + (α + β)r²_{t−1} + ν_t − βν_{t−1}: an ARMA(1, 1) with autoregressive root
   α + β. With normal shocks, E[r⁴] = 3E[σ⁴]. Taking expectations of the squared recursion gives
   E[σ⁴](1 − (α + β)² − 2α²) = ω² + 2ωσ̄²(α + β), and the kurtosis is 3(1 − (α + β)²)/(1 − (α + β)² − 2α²). This
   exceeds 3 whenever α > 0, and is finite only if (α + β)² + 2α² < 1.
3. **Noise in realized variance, and the optimal sampling rate.** If observed log prices are p_i = p*_i + u_i with
   iid noise of variance η², observed returns are r_i = r*_i + u_i − u_{i−1}, and E[Σr_i²] = ∫σ²dt + 2nη²: the bias
   grows with n (the signature plot). The estimation error of RV without noise has variance 2IQ/n (BNS). The mean
   squared error is about (2nη²)² + 2IQ/n = 4n²η⁴ + 2IQ/n; setting its derivative 8nη⁴ − 2IQ/n² to zero gives
   n* = (IQ/(4η⁴))^{1/3} (Bandi and Russell 2008). Two-scale RV removes the bias instead: it averages K sparse grids
   (bias 2n̄η² each) and subtracts (n̄/n)RV_all, converging at rate n^{−1/6}.
4. **QLIKE.** E[h/ĥ − log(h/ĥ) − 1 | F] = E[h|F]/ĥ + log ĥ − E[log h | F] − 1. Its derivative in ĥ is
   −E[h|F]/ĥ² + 1/ĥ, which is zero only at ĥ = E[h|F], and the function is convex there. The loss depends on h only
   through E[h|F] plus a term free of ĥ, so an unbiased proxy (E[h̃|F] = E[h|F]) adds the same constant to every
   forecast's expected loss and preserves the ranking (Patton 2011). For MSE on volatility, argmin E(√h̃ − σ̂)² =
   E√h̃ < √E h̃ by Jensen: with a squared return as the proxy, the minimiser is (2/π)h ≈ 0.64h.
5. **The Kalman gain.** For x_t = x_{t−1} + w_t and y_t = x_t + v_t, with variances Q and R, the filter predicts
   P⁻ = P + Q, uses the gain K = P⁻/(P⁻ + R), and updates P = (1 − K)P⁻. In steady state KP⁻ = Q, and P⁻ solves
   P⁻² − QP⁻ − QR = 0. Dividing by R² and writing q = Q/R gives p = P⁻/R = (q + √(q² + 4q))/2 and K = p/(p + 1),
   a function of q alone. For Bitcoin's q = 0.38, K ≈ 0.45.
6. **The Dickey–Fuller limit with a constant.** Assume x₀ = 0 and iid mean-zero finite-variance shocks.
   Let x̄₋ be the mean lagged level. The centered numerator is Σ(xₜ₋₁ − x̄₋)εₜ = ½(x_T² − Σεₜ²) − x̄₋x_T.
   Write Wμ(r) = W(r) − ∫₀¹W(s)ds and A = ½(W(1)² − 1) − W(1)∫₀¹W(r)dr. Donsker and continuous mapping give
   T(ρ̂ − 1) ⇒ A/∫Wμ² and t_DF ⇒ A/√∫Wμ². The notation ∫Wμ dW abbreviates this explicit path functional,
   rather than an ordinary adapted Itô integrand. This matches the fitted-constant/no-trend simulation. The uncentered
   no-intercept law differs; adding a deterministic trend changes the law and critical values again.

7. **(qual) Why DM leans small.** Under the null the big model's forecast is $\hat y_2 = \hat y_1 + g$, where the gap $g$
   is the full fitted forecast difference, including refitted common coefficients and regressors at $t$, known before the shock
   $\varepsilon_{t+1}$. Then $e_2 = e_1 - g$ and $e_2^2 - e_1^2 = g^2 - 2ge_1$; under additional estimation and orthogonality conditions, $E[g\,e_1] = E[g\,\varepsilon_{t+1}] +
   E[g(\text{model 1's estimation error})] \approx 0$ to first order, $E[e_2^2 - e_1^2] \approx E[g^2] > 0$. So $E\bar d =
   E[e_1^2 - e_2^2] < 0$: the statistic is centred below zero, and Clark and West's $f = e_1^2 - (e_2^2 - g^2)$ is centred
   near zero.
8. **(qual) How much.** With one extra regressor of variance $\sigma_x^2$, the recursive slope estimate at time $t$ has
   variance $\approx \sigma^2/(t\sigma_x^2)$, so $E[g_t^2] \approx \sigma_x^2 \cdot \sigma^2/(t\sigma_x^2) = \sigma^2/t$.
   Averaging over $t = R, \dots, R + P - 1$: $\frac{\sigma^2}{P}\sum 1/t \approx \sigma^2\ln(1 + P/R)/P$. With $R$ = 100 and
   $P$ = 200: $1.10\sigma^2/200$ per forecast, an order-of-magnitude estimation penalty in this idealized example, not a universal detection threshold.

**The research chapter's pause question.** DM $= -0.02/0.03 = -0.67$, favouring the small model; CW's mean is $-0.02 +
0.05 = 0.03$, so with a similar standard error CW $\approx 1.0$: it leans to the big model, without significance.

## For the researcher

* **The theorems.** Diebold and Mariano (1995); West (1996) on parameter estimation error; Clark and McCracken (2001)
  and McCracken (2007) for nested-model limits; Clark and West (2006, 2007); Giacomini and White (2006) for conditional
  predictive ability; Hansen, Lunde and Nason (2011).
* **Simplifications.** The simulations use squared loss and one extra regressor; CW is approximately, not exactly,
  normal (it is mildly undersized here, 2.9%).
* **Open problems.** Joint inference over many nested and non-nested models; method against model; non-quadratic losses.

## Data and reproducibility

* Binance (data.binance.vision): BTCUSDT one-minute and daily spot candles, August 2017 to December 2020, and the
  USD-M perpetual's daily closes for 2020. Every downloaded file is checksummed in
  [`../data/manifest.json`](../data/manifest.json).
* Kenneth French's daily market and size-decile returns and monthly factors, 1926–2020; FRED DTB3, DGS5, DGS10 and
  VIXCLS. The hold-out from 2021 is sealed.
* Recorded in the trial registry (the 2020 comparison includes retrospective additions): the forecasting race (8 models; log-HAR added after the first
  results and counted), HARNet (1) and the toy foundation model (2: a PyTorch version registered first and never scored, then the numpy version that was).
* Facts checked for this expansion: Murray (1994) is *The American Statistician* 48(1):37–39 (Crossref); Moskowitz,
  Ooi and Pedersen's 40% target and 60-day centre of mass (the *JFE* paper's text); MSCI's descriptions of USE4's
  half-lives and volatility regime adjustment (MSCI, Dec. 2011). Dropped as unverifiable here: the exact USE4
  regime-adjustment formula and half-lives (our replica is labeled as ours), and the Basel 1996 amendment's √10 text
  (the BIS document could not be retrieved; the chapter states only the mathematics).

---

# 量化金融，从零搭建 — 第7部分：时间序列与波动率

收益的线性自相关较小，幅度的持续性更强；低自相关不证明不可预测。本部分是一门关于预测它的模型的课程，从尤尔的自回归一直讲到时间序列基础模型；每个模型都在屏幕上拟合或训练，
并作回顾性预测评估；2020年曾用于追加模型，另一个2021年起的保留集仍封存。实证示例由本系列代码按公开数据计算，模拟固定种子；没有运行、直接引用的结果（基础模型的比较）标注为论文数据。

*讲的是方法，不构成投资建议。*

## 章节（约57分钟）

开场（波动聚集、收益与绝对收益的自相关、卡尔曼河流、历史）；1. 平稳性、ARMA与博克斯–詹金斯方法；2. 单位根与伪回归；3. 协整（醉汉与狗、
比特币基差、三维国债收益率的约翰森检验）；4. 隐藏机制；5. 卡尔曼滤波与随机波动率；6. 用最大似然估计ARCH与GARCH（漏水桶、三维似然面）；
7. GARCH家族（纳尔逊平稳性边界、新闻冲击曲线、学生t）；8. 会变的相关性（DCC）；9. 已实现波动率（签名图、噪声、最优采样）；10. 跳跃与HAR；
11. 波动率是粗糙的吗？；12. 诚实地给预测评分（QLIKE、DM、MZ、模型置信集）；13. 训练神经网络；14. 竞赛；15. 基础模型与前沿；16. 2020年3月；
17. 业界（RiskMetrics、Barra、波动率目标、VIX）；18. 波动率预测器；回顾、交易台问题与习题。各章数字见上面英文部分。

## 教材对照

见上面英文部分的表格：Tsay第1–5、7、8、10–12章，Hamilton第3–6、10–11、13、15–22章，Brockwell–Davis，Francq–Zakoian，
Aït-Sahalia–Jacod，Andersen等（2006）手册章节，CLM第12章，QRM，均对应到本部分的章节或本系列的其他部分。

## 交易台问题与解答

1. **日波动率为1%。** 若收益独立且方差恒定，方差可加：一周1% × √5 ≈ 2.2%，一年1% × √252 ≈ 15.9%。这个法则有三种失效方式。
   第一，波动率均值回归，从高位出发，一段期限内的平均低于今天的水平（GARCH：E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²)），
   第16章中85%在一年里降到52%。第二，收益自相关时，总和的方差会乘以1 + 2Σ(1 − k/h)ρ_k（Lo–MacKinlay方差比）。第三，厚尾收益的分位数不按√T缩放，
   因为厚尾收益之和比单个收益更接近正态。
2. **两个价格之间t = 24。** 先检验两个序列有没有单位根（ADF）。如果都有，这个t统计量没有意义（第2章：89%的错误拒绝，而且按√T增长）。
   对水平回归的残差做单位根检验，用恩格尔–格兰杰临界值（两个序列时5%水平约−3.34，而不是−2.86），或者用变化量对变化量回归。
3. **一个模型在包含崩盘的一年里按MSE胜过GARCH。** 方差预测的平方误差由最大的几天主导，一天就可能决定胜负。应当用QLIKE评分，
   它对已实现代理变量中的噪声稳健（Patton 2011）；对比HAR而不是弱基准；用带HAC方差的Diebold–Mariano检验和模型置信集；并检查去掉危机几周后排名是否依然成立。
4. **GARCH拟合得到α + β = 1。过程平稳吗？** 不是协方差平稳的：无条件方差ω/(1 − α − β)为无穷。但它是严平稳的：展开得
   σ_t² = ω Σ_k Π_{j≤k}(αz²_{t−j} + β)，当E ln(αz² + β) < 0时收敛（Nelson 1990），而由詹森不等式E ln(αz² + β) < ln E(αz² + β) = ln(α + β) = 0。
   方差预测永远不回归（RiskMetrics的EWMA就是ω = 0的这种情形）。

## 习题与解答

1. **GARCH的期限结构。** 记σ̄² = ω/(1 − α − β)。由于E_t[r²_{t+k}] = E_t[σ²_{t+k}]，对σ²_{t+k+1} − σ̄² = α(r²_{t+k} − σ̄²) + β(σ²_{t+k} − σ̄²)
   取期望，得E_t[σ²_{t+k+1}] − σ̄² = (α + β)(E_t[σ²_{t+k}] − σ̄²)，归纳得E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²)。
   冲击在log 0.5/log(α + β)天后减半：美国市场的0.989对应63天。
2. **GARCH即ARMA，及其峰度。** 令ν_t = r_t² − σ_t²，它是鞅差。把σ_t² = r_t² − ν_t代入GARCH递推，得r_t² = ω + (α + β)r²_{t−1} + ν_t − βν_{t−1}：
   自回归根为α + β的ARMA(1, 1)。正态冲击下E[r⁴] = 3E[σ⁴]。对递推式平方取期望得E[σ⁴](1 − (α + β)² − 2α²) = ω² + 2ωσ̄²(α + β)，
   峰度为3(1 − (α + β)²)/(1 − (α + β)² − 2α²)。只要α > 0它就大于3，且仅当(α + β)² + 2α² < 1时有限。
3. **已实现方差中的噪声与最优采样频率。** 若观测对数价格为p_i = p*_i + u_i，噪声独立同分布、方差η²，则观测收益为r_i = r*_i + u_i − u_{i−1}，
   E[Σr_i²] = ∫σ²dt + 2nη²：偏差随n增长（签名图）。无噪声时RV的估计误差方差为2IQ/n（BNS）。均方误差约为(2nη²)² + 2IQ/n = 4n²η⁴ + 2IQ/n；
   令导数8nη⁴ − 2IQ/n²为零得n* = (IQ/(4η⁴))^{1/3}（Bandi与Russell 2008）。双尺度RV则消除偏差：对K个稀疏网格取平均（各自偏差2n̄η²），
   再减去(n̄/n)RV_all，以n^{−1/6}的速度收敛。
4. **QLIKE。** E[h/ĥ − log(h/ĥ) − 1 | F] = E[h|F]/ĥ + log ĥ − E[log h | F] − 1。对ĥ的导数为−E[h|F]/ĥ² + 1/ĥ，只在ĥ = E[h|F]处为零，
   且函数在那里是凸的。损失只通过E[h|F]依赖于h，另加一项与ĥ无关的量，所以无偏代理（E[h̃|F] = E[h|F]）只给每个预测的期望损失加上同一个常数，
   排名不变（Patton 2011）。对波动率上的MSE，argmin E(√h̃ − σ̂)² = E√h̃ < √E h̃（詹森）：以平方收益为代理时，最小点是(2/π)h ≈ 0.64h。
5. **卡尔曼增益。** 对x_t = x_{t−1} + w_t、y_t = x_t + v_t，方差分别为Q与R，滤波器先预测P⁻ = P + Q，用增益K = P⁻/(P⁻ + R)，
   再更新P = (1 − K)P⁻。稳态时KP⁻ = Q，且P⁻满足P⁻² − QP⁻ − QR = 0。除以R²并记q = Q/R，得p = P⁻/R = (q + √(q² + 4q))/2，
   K = p/(p + 1)，只是q的函数。比特币的q = 0.38给出K ≈ 0.45。
6. **带常数项的迪基–富勒极限。** 假设x₀ = 0、冲击独立同分布、均值零且方差有限。记x̄₋为滞后水平的样本均值，
   则Σ(xₜ₋₁ − x̄₋)εₜ = ½(x_T² − Σεₜ²) − x̄₋x_T。令Wμ = W − ∫₀¹W、A = ½(W(1)² − 1) − W(1)∫₀¹W，
   得T(ρ̂ − 1) ⇒ A/∫Wμ²，t_DF ⇒ A/√∫Wμ²。∫Wμ dW只是这个显式路径函数的简写，不是普通适应性Itô被积过程。
   这与带常数、无趋势的模拟一致。无截距和带趋势的检验有不同极限与临界值。

7. **（资格考试）为什么DM偏向小模型。** 原假设下$\hat y_2 = \hat y_1 + g$，$g$在冲击之前已知；$e_2^2 - e_1^2 = g^2 - 2ge_1$，还需估计误差的正交等条件才能作一阶近似
   $E[ge_1] \approx 0$，所以$E[e_2^2 - e_1^2] \approx E[g^2] > 0$：统计量中心低于零，而克拉克–韦斯特的$f = e_1^2 - (e_2^2 - g^2)$中心接近零。
8. **（资格考试）偏多少。** 一个额外回归变量时，$E[g_t^2] \approx \sigma^2/t$；在$t = R, \dots, R + P - 1$上平均得约$\sigma^2\ln(1 + P/R)/P$。

## 写给研究者

迪博尔德–马里亚诺（1995）；参数估计误差（West 1996）；嵌套模型极限（Clark与McCracken 2001；McCracken 2007）；Clark与West（2006、2007）；
条件预测能力（Giacomini与White 2006）；模型置信集（Hansen、Lunde与Nason 2011）。开放问题：多个嵌套与非嵌套模型的联合推断；方法与模型之辨；非二次损失。


## Interpretation and scope

The registered computations, data checksums and experiment history are preserved. The as-of-Part-7 trial count is
307 (296 through Part 6 plus eleven here); later parts' registrations are excluded. No 2021-onward holdout was opened.
The 2020 comparison is exploratory because results informed later additions. Networks use June training/H2 validation;
classical baselines fit all 2019. HARNet's initial log-HAR fit therefore differs from the displayed race baseline.

DCC's exact multi-step Q recursion includes a EₜRₜ₊ₕ₋₁ term because standardized shock covariance is R, not Q.
The a+b half-life is a linearized persistence summary, not an exact normalized-correlation forecast identity.
The displayed parameter count excludes the correlation target entries. Annual covariance ellipses are one-SD return
contours. The 60/40 comparison fixes realized marginal volatilities and changes correlation retrospectively.

GARCH long-run variance assumes positive omega, nonnegative alpha/beta, sum below one and conditional unit shock
variance. Its squared-return ARMA identity is algebraic; a covariance-ARMA interpretation needs finite fourth moments.
Strict Jensen for IGARCH needs positive alpha and nonconstant squared shocks. QMLE consistency and asymptotic normal
sandwich errors require distinct regularity and moment assumptions. In SV, exp(mu/2) is stationary median volatility;
mean volatility also includes exp(Var(h)/8), and RMS volatility exp(Var(h)/4).

Realized-variance CLTs and jump tests need their noise/continuity/regularity assumptions. Non-detection does not establish
no jumps. The sampling-rate calculation is a two-term MSE illustration with a noise-dominance proxy; it is not a validated
optimum. TSRV includes the finite-sample divisor 1−nbar/n. Rough scaling measured on an RV proxy does not prove latent
roughness; the adjacent-increment correlation is fBm-implied. QLIKE ranking robustness requires positive conditionally
unbiased proxies, measurable forecasts and integrability. Normal DM and bootstrap MCS statements need their dependence,
estimation and fixed-candidate-set assumptions. Non-rejection is neither equivalence nor proof of no useful signal.

Bitcoin's 5/22 observations and rolling 252 days are trading-market conventions, not calendar weeks/months/years.
The House's 22-day log-HAR term forecast is a recursive plug-in approximation, not exact multi-step lognormal moments.
The horizon graph shows annualized RMS from averaged conditional variances, not cumulative horizon standard deviation.
Physical-measure GARCH forecasts and risk-neutral option-implied volatility differ.

Industry P&L comparisons are gross of trading/funding costs with a two-day position lag and leverage cap ten; the plain
benchmark is matched to full-period volatility after the fact. Drawdown is additive cumulative simple excess-return
drawdown, despite the legacy cache field name maxdd_log. The VIX gap uses a broader US-market realized proxy with an
approximate horizon match and is not an identified variance risk premium. Encompassing regressions are retrospective;
pre-1990 GARCH parameters do not remove full-research-sample demeaning. Overlapping outcomes use HAC errors.

Brini (2026), Table 6, reports average per-asset loss ratios. Sundial and HAR are also just below log-HAR at h=1;
TTM is the only foundation model ahead at all three reported horizons. The local synthetic toy is a token-embedding
MLP, not a transformer or Chronos replication. Its March-13 context already includes the March-12 crash. Its interval
is nominal; realized coverage is not guaranteed. Same-sample recalibration diagnoses scale rather than validating a
new forecast. Nested-comparison research must account for re-estimated common coefficients and the cross term in the
exact identity e₂²−e₁²=δ²−2e₁δ. Future-innovation independence alone is insufficient to discard that cross term.

## 解释与适用范围

原登记计算、数据校验与实验历史保留，未打开2021年起的保留集。本部分累计307次试验；2020年比较曾复用，属于探索性。
网络训练至2019年6月、下半年验证，传统基线拟合全年。DCC多步Q预测必须包含期望R项，a+b半衰期仅为线性化持续性摘要。
QMLE一致性与正态标准误有不同矩条件；IGARCH严格詹森结论需alpha为正且平方冲击非恒定。SV的exp(mu/2)是平稳中位波动率，
不是均值。RV区间和跳跃检验依赖无噪声、连续性等条件；未检出不证明没有跳跃。TSRV含1−nbar/n分母，采样最优值只是近似演示。
代理的粗糙缩放不能直接证明潜在粗糙性；QLIKE、DM、MCS须满足各自的代理、依赖、估计和固定候选集条件。
比特币5/22期不是日历周月，252日约八个月；22日递归log-HAR是插件近似。期限图展示预期方差平均后的年化均方根。
业界示例未扣成本，普通基准事后匹配波动率；回撤是累计简单超额收益的回撤。VIX与未来实现波动率的差不直接识别方差风险溢价，
回顾性涵盖回归不等于新预测验证。论文TTM的结论限于所述基准；本地玩具是词元嵌入MLP，3月13日上下文已含12日危机。
嵌套比较的delta包含共同系数重新估计，恒等式的交叉项不能只凭未来新息独立而忽略。


The screen's API table lists representative pairs; the House module contains the complete toolkit. Trial counts use
the registered model/protocol units, including an abandoned foundation-model attempt. The fixed five-seed neural
averages are one protocol per architecture; selecting a winning seed would create an additional selection choice.
The toy's probability snapshots share fixed axes, and the DF histogram includes the tallest early Monte Carlo bars
while omitting contaminated tail bins. The Kalman bells use data coordinates rather than the axes wrapper's internal
range. EWMA has no fixed variance-reversion target; the bucket metaphor refers to no net expected leak.
