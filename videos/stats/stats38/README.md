# Statistics, Built — Part 38: Time Series in Depth

Part 38 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the eighteenth part of Stage III, Master's. Part 17's series were stationary,
with short memory and constant variance, and fully observed. This part lets each assumption go in turn:
- spectra;
- unit roots, spurious regression and cointegration;
- volatility;
- long memory;
- the state space, with the Kalman filter, smoother and EM;
- nonlinear filters and regime switching;
- vector autoregressions;
- the block bootstrap;
- the forecasting frontier.

The part builds `statkit.ts` (II) and an instrument, the Kalman ellipses (`KalmanEllipses`): the predict and update
steps as moving Gaussian ellipses, with the measurement as a band. Its real data are:
- Toussoun's yearly minima of the Nile at Roda, 622–1284 (R's longmemo package, GPL ≥ 2);
- the Nile's flow at Aswan, 1871–1970;
- yearly sunspot numbers;
- the DAX, 1991–1998 (R's `EuStockMarkets`);
- US quarterly macro data, 1959–2009 (statsmodels).

It opens with Hurst (1951). The Nile minima's rescaled range grows like n^0.85. White noise of the same length gives
0.56 (0.48–0.63), and an AR(1) fitted to the Nile 0.69. The range of the cumulative surplus is 10,647.

From there the part covers:
- **What Part 17 assumed.** Four seeded departures from it: a random walk, GARCH, ARFIMA, a hidden level. Also Wold's
  decomposition and ergodicity.
- **Spectra.**
  - Herglotz; the periodogram is unbiased but inconsistent. For white noise its spread is 1.11 at n = 128 and 1.08 at
    n = 2,048; Welch's estimate brings it to 0.18.
  - Welch; multitaper.
  - The sunspot peak: periodogram 11.0 years, Welch 10.7, multitaper 10.7, Yule's AR(2) 10.9.
- **Unit roots.**
  - Dickey–Fuller and its Brownian limit. Over 20,000 random walks the 5% point is −2.88, against MacKinnon's −2.89.
    The normal −1.645 rejects 45% of true unit roots.
  - KPSS.
  - US series: log GDP has a unit root; unemployment, the T-bill rate and inflation cannot be told apart; GDP growth is
    stationary.
  - Perron's breaks.
- **Spurious regression and cointegration.**
  - Two independent walks give |t| > 1.96 77% of the time (Granger & Newbold: 76%), with median R² 0.18.
  - Engle–Granger on log consumption and income: β̂ = 1.03, τ = −2.90 against −3.37, so it cannot reject.
  - Johansen with investment: trace 30.2 against 29.8 for rank 0, and 11.5 against 15.5 for rank 1, so one relation,
    barely.
  - Super-consistency; FM-OLS and DOLS.
- **Volatility.** DAX returns:
  - kurtosis 9.3; ARCH LM 70 (p ≈ 10⁻¹³);
  - GARCH(1,1) with α = 0.068, β = 0.888 (persistence 0.956, half-life 15 days);
  - 1% VaR exceedances: constant variance 0.54% when calm and 2.91% when turbulent; GARCH 1.51% and 1.72%;
  - volatility forecasts: 0.39 of today's excess remains after a month.
- **Long memory.**
  - ARFIMA (Granger & Joyeux; Hosking).
  - GPH on the minima ranges from 0.40 to 0.58 by bandwidth; local Whittle gives d = 0.41 (0.06), so H ≈ 0.91.
  - With d = 0.41 the SE of the mean is 47.5 instead of 3.4: an effective sample of 3.5 of 663 years.
  - Long memory elsewhere; breaks that mimic it.
- **Kalman.**
  - Gaussian conditioning; the ellipses on a tracking example.
  - The Nile local level: MLE σ²_w = 1,469.0 and σ²_v = 15,099, matching Durbin & Koopman.
  - The steady-state gain is 0.27, which is exponential smoothing (Muth 1960).
  - The smoothed level's largest fall is into 1899; a shift there of −316 has LR 10.5.
- **Smoothing and learning.**
  - RTS.
  - Missing years 1891–1910 and 1931–1950.
  - The prediction-error likelihood. EM raises the likelihood at every step and converges to the MLE (1,469 and
    15,099).
  - Structural time-series models; Apollo.
- **Nonlinear filtering.**
  - Kitagawa–Gordon's benchmark, RMSE over 30 series: EKF 20.6, UKF 10.5, particle filter 4.4.
  - PMCMC.
  - Hamilton's regimes in US growth: −1.1% and +4.1% a year, lasting 4 and 18 quarters. The filtered recession
    probability averages 0.64 inside NBER recessions and 0.06 outside.
- **VARs.** A VAR(4) of inflation, unemployment and the T-bill rate.
  - Granger tests: inflation → unemployment p = 0.007, unemployment → T-bill p = 0.010, T-bill → inflation p = 0.038.
  - Responses to a rate shock: unemployment rises over 2–3 years; inflation rises at first (the price puzzle).
  - Variance decompositions; local projections.
- **Block bootstrap.**
  - AR(1) with φ = 0.5 and n = 500, SE of the mean: i.i.d. 0.055, moving-block 0.091, stationary 0.092, Newey–West
    0.088, truth 0.089.
  - The Nile minima's block SE keeps rising with the block length (5.8 → 16.5), so it never plateaus under long
    memory.
  - Choosing b.
- **Forecasting.**
  - M4 and M5; pretrained forecasters.
  - Rolling-origin MASE on CO₂ (11 origins, 2 years ahead): naive 2.16, seasonal naive 1.80, seasonal naive plus trend
    0.60, Holt–Winters 0.48.
  - Leakage: 0.15 against the honest 0.19.

Data:
- the Nile, its minima, the sunspots, the DAX, the macro series and CO₂ are the Museum's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.ts` (II)** ([`explainer/stats/kit/ts.py`](../../../explainer/stats/kit/ts.py)), checked against
  statsmodels in `tests/test_stats_kit_ts2.py`:
  - **Spectra and long memory:** Hurst's R/S; the periodogram, Welch and multitaper; ARMA spectra; fractional
    differencing weights, the ARFIMA ACF and exact simulation (Davies–Harte); GPH and local Whittle.
  - **Unit roots and cointegration:** ADF with MacKinnon's critical values; KPSS; Engle–Granger; Johansen's trace.
  - **Volatility:** the ARCH LM test; GARCH(1,1) by maximum likelihood.
  - **State space:** the Kalman filter with missing data and its likelihood; RTS; local-level MLE and EM; EKF, UKF and
    a bootstrap particle filter; Hamilton's filter and its MLE.
  - **Several series and resampling:** VARs, Granger tests and orthogonalized impulse responses; the stationary
    bootstrap.
- **The Museum** gains `nile()`, `nile_minima()`, `eustock()` and `us_macro()`.
- **The Kalman ellipses** (`KalmanEllipses` in `explainer/stats/viz.py`).

The Coverage Board gains seven rows:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| Dickey–Fuller t, normal critical value (size) | random walks, T = 100 | 44.7% | broken |
| Dickey–Fuller t, MacKinnon's value (size) | same | 5.4% | kept |
| KPSS, Bartlett long-run variance (size) | AR(1), φ = 0.5, T = 200 | 5.2% | kept |
| regression t-test, two random walks (size) | independent walks, T = 100 | 77.1% | broken |
| Engle–Granger, MacKinnon's values (size) | same | 4.6% | kept |
| i.i.d. bootstrap 90% CI for the mean | AR(1), φ = 0.5, n = 500 | 66.4% | broken |
| moving-block bootstrap CI (blocks of 30) | same | 89.0% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats38.compute   # once (a few minutes)
python tools/build.py stats38 -q l                         # fast 480p preview
python tools/build.py stats38                              # 1080p30 -> renders/stats38.mp4
python tools/qa_scene.py stats38 Kalman
python tools/lecture_length.py stats38 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Hurst's Nile | H = 0.85 vs 0.56 |
| 1 | What Part 17 assumed | four departures; ergodicity |
| 2 | Spectra | 11-year sunspot cycle |
| 3 | Unit roots | 45% vs 5% |
| 4 | Spurious regression and cointegration | 77%; trace 30.2 vs 29.8 |
| 5 | Volatility | α + β = 0.956 |
| 6 | Long memory | d = 0.41; n_eff = 3.5 |
| 7 | State space and the Kalman filter | 1,469 / 15,099; K = 0.27 |
| 8 | Smoothing and learning | EM → MLE |
| 9 | Nonlinear filtering and regimes | RMSE 20.6 / 10.5 / 4.4 |
| 10 | VARs and Granger causality | the price puzzle |
| 11 | The block bootstrap | 0.055 vs 0.091 |
| 12 | The forecasting frontier | MASE 0.48; leakage |
| 13 | Outro | — |

## Sources

- **Long memory.**
  - H. Hurst, *Trans. ASCE* 116 (1951); B. Mandelbrot & J. Wallis, *Water Resour. Res.* 4 (1968).
  - C. Granger & R. Joyeux, *J. Time Ser. Anal.* 1 (1980); J. Hosking, *Biometrika* 68 (1981).
  - J. Geweke & S. Porter-Hudak, *J. Time Ser. Anal.* 4 (1983); P. Robinson, *Ann. Stat.* 23 (1995).
  - F. Diebold & A. Inoue, *J. Econometrics* 105 (2001); W. Leland et al., *IEEE/ACM Trans. Netw.* 2 (1994).
  - J. Beran (1994); O. Toussoun (1925).
- **Spectra.**
  - H. Wold (1938); P. Welch, *IEEE Trans. Audio Electroacoust.* 15 (1967); D. Thomson, *Proc. IEEE* 70 (1982).
- **Unit roots and cointegration.**
  - D. Dickey & W. Fuller, *JASA* 74 (1979); J. MacKinnon (2010); D. Kwiatkowski, P. Phillips, P. Schmidt & Y. Shin,
    *J. Econometrics* 54 (1992).
  - C. Nelson & C. Plosser, *J. Monet. Econ.* 10 (1982); P. Perron, *Econometrica* 57 (1989); E. Zivot & D. Andrews,
    *JBES* 10 (1992).
  - C. Granger & P. Newbold, *J. Econometrics* 2 (1974); P. Phillips, *J. Econometrics* 33 (1986).
  - R. Engle & C. Granger, *Econometrica* 55 (1987); S. Johansen, *J. Econ. Dyn. Control* 12 (1988); J. Stock,
    *Econometrica* 55 (1987).
  - P. Phillips & B. Hansen, *REStud* 57 (1990); J. Stock & M. Watson, *Econometrica* 61 (1993).
- **Volatility.**
  - B. Mandelbrot, *J. Business* 36 (1963); R. Engle, *Econometrica* 50 (1982); T. Bollerslev, *J. Econometrics* 31
    (1986).
- **State space.**
  - R. Kalman, *J. Basic Eng.* 82 (1960); H. Rauch, F. Tung & C. Striebel, *AIAA J.* 3 (1965); F. Schweppe, *IEEE
    Trans. Inf. Theory* 11 (1965).
  - R. Shumway & D. Stoffer, *J. Time Ser. Anal.* 3 (1982); J. Muth, *JASA* 55 (1960); A. Harvey, *Forecasting,
    Structural Time Series Models and the Kalman Filter* (1989).
  - J. Durbin & S. J. Koopman (2012); G. Cobb, *Biometrika* 65 (1978).
- **Nonlinear filtering.**
  - S. Julier & J. Uhlmann (1997); N. Gordon, D. Salmond & A. Smith, *IEE Proc. F* 140 (1993).
  - C. Andrieu, A. Doucet & R. Holenstein, *JRSS B* 72 (2010); J. Hamilton, *Econometrica* 57 (1989).
- **VARs.**
  - C. Granger, *Econometrica* 37 (1969); C. Sims, *Econometrica* 48 (1980), *Eur. Econ. Rev.* 36 (1992).
  - Ò. Jordà, *AER* 95 (2005).
- **Bootstrap.**
  - H. Künsch, *Ann. Stat.* 17 (1989); D. Politis & J. Romano, *JASA* 89 (1994); D. Politis & H. White, *Econometric
    Rev.* 23 (2004).
- **Forecasting.**
  - S. Makridakis et al., *IJF* 36 (2020), 38 (2022); R. Hyndman & A. Koehler, *IJF* 22 (2006).
  - A. Ansari et al. (Chronos, 2024); A. Das et al. (TimesFM, 2024); G. Woo et al. (Moirai, 2024); K. Rasul et al.
    (Lag-Llama, 2024); A. Garza & M. Mergenthaler-Canseco (TimeGPT, 2023). These are current as of the mid-2020s;
    check the latest benchmarks.

## Problems and solutions

1. **White-noise periodogram.** At the Fourier frequency f_j, the cosine and sine sums are uncorrelated Gaussians with
   variance nσ²/2 each, and different j are orthogonal. So I(f_j) = (C² + S²)/n is σ²/2 times a χ²₂, that is σ² Exp(1),
   and the ordinates are independent.
2. **The Dickey–Fuller numerator.** Squaring x_t = x_{t−1} + ε_t gives x_t² = x_{t−1}² + 2x_{t−1}ε_t + ε_t².
   - Summing, Σx_{t−1}ε_t = (x_T² − x_0² − Σε_t²)/2.
   - Divide by Tσ²: with x_0 = 0 this is ½(x_T²/(Tσ²) − σ̂²/σ²) → ½(W(1)² − 1) = ∫W dW.
3. **GARCH(1,1).**
   - Taking expectations of σ_t² = ω + αε_{t−1}² + βσ_{t−1}², with E ε² = E σ², gives Eσ² = ω/(1 − α − β).
   - Let ν_t = ε_t² − σ_t², a martingale difference. Then ε_t² = ω + (α + β)ε_{t−1}² + ν_t − βν_{t−1}, an ARMA(1,1).
4. **ARFIMA ρ₁.** From ρ_k = ∏(j − 1 + d)/(j − d), taking k = 1 gives ρ₁ = d/(1 − d). For d = 0.4 this is 0.67.
5. **Local-level gain.** With H = 1, K = P(P + r)⁻¹ = P/(P + r).
   - The predicted variance recursion P' = P − P²/(P + r) + q has the steady state P² = q(P + r), so
     P = (q + √(q² + 4qr))/2.
   - For the Nile, with q/r = 0.097, K = 0.27.
6. **AR(1) mean.** n Var(X̄) = γ₀ Σ_{|h|<n}(1 − |h|/n)φ^{|h|} → γ₀(1 + 2φ/(1 − φ)) = γ₀(1 + φ)/(1 − φ). For φ = 0.5
   that is 3γ₀, so the i.i.d. SE is too small by √3.

## Glossary

- **Rescaled range; Hurst exponent H**: the range of cumulative deviations over the SD; its growth exponent.
- **Spectral density; periodogram; Welch; multitaper**: the variance by frequency; its raw, inconsistent estimate;
  segment averaging; Slepian tapers.
- **Unit root; Dickey–Fuller; KPSS**: a permanent-shock process; the test with a unit-root null; the test with a
  stationarity null.
- **Spurious regression; cointegration; error correction**: significant-looking regressions between independent
  walks; a stationary combination of unit-root series; the pull back to it.
- **ARCH; GARCH; persistence**: conditional variance driven by past squared shocks (and past variance); α + β.
- **Long memory; ARFIMA; d**: autocorrelations decaying like a power; fractional differencing; H = d + ½.
- **State space; Kalman filter; RTS smoother; gain**: hidden linear Gaussian dynamics; the forward recursion; the
  backward pass; the weight on the surprise.
- **Prediction-error decomposition; EM**: the likelihood from innovations; Shumway–Stoffer's iteration.
- **EKF; UKF; particle filter; PMCMC**: linearize; sigma points; weighted samples; particle likelihoods inside MCMC.
- **Markov switching**: a discrete hidden regime (Hamilton).
- **VAR; Granger causality; impulse response; price puzzle**: joint autoregression; forecasting improvement; dynamic
  effects of identified shocks; inflation rising after a tightening.
- **Block and stationary bootstraps**: resampling blocks to keep dependence.
- **Rolling origin; MASE; leakage**: honest forecast evaluation; a scale-free error; test information in training.

## Where it comes back

- **Part 39**: dependence in space; kriging.
- **Part 41**: EM and missing data.
- **Part 44**: Brownian motion and Donsker's theorem behind Dickey–Fuller.
- **Part 47**: non-standard limits.
- **Part 53**: Gaussian processes.
- **Part 58**: sequential, anytime-valid inference.
- **Part 60**: nonstationarity as distribution shift.
- **Part 64**: pretrained forecasters, honestly.
