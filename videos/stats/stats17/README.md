# Statistics, Built — Part 17: Time Series

Part 17 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Every method so far assumed independent, or at
least exchangeable, observations. This part asks what to do when each observation remembers the last.

It opens with Yule's presidential address of 1926: Church of England marriages and mortality in England and Wales,
1866–1911, correlate at r = 0.95 in levels and 0.02 in year-on-year changes. Independent random walks of 46 steps
reach |r| > 0.5 in 39% of pairs, against 0.04% for independent noise. Then Yule's pendulum pelted with peas (1927).

From there the part covers:
- **Stationarity and the ACF.** White noise, an AR(1) and a random walk side by side with their correlograms;
  Bartlett's bands. The variance of an autocorrelated mean: inflation (1 + ρ)/(1 − ρ) = 5.67 at ρ = 0.7, an effective
  sample size of 17.6 from 100. Newey–West and the basic moving-block bootstrap; three Board rows.
- **AR, MA, ARMA.** The AR(1) as an MA(∞); a gallery of four models; φ = 0.5, 1 and 1.08 on the same shocks; roots
  outside the unit circle on the `RootPlane`; the AR(2) stationarity triangle and its parabola of complex roots; MA
  invertibility; Wold's theorem.
- **Pseudo-cycles.** The damped-cosine ACF of complex roots; Slutsky's summed shocks; Yule's sunspot AR(2),
  (1.336, −0.650), period 10.6 years; where the AR(2) falls short of the data's ACF.
- **Identification.** The PACF; the table of signatures; simulated AR(2) and MA(2); the sunspots' correlograms; the
  Box–Jenkins cycle; differencing and ARIMA.
- **Estimation.** Yule–Walker and least squares; AIC over orders 0–12 (best: 8); residual correlograms; Ljung–Box.
- **Forecasting.** Best linear prediction; widening intervals; the random walk's "no change"; the sunspots of
  1925–1955 forecast from 1924 by AR(2) and AR(8); MASE; cautions.
- **Trend and seasonality.** Keeling's Mauna Loa record; the classical decomposition in four panels; the seasonal
  figure (May +2.9, October −3.2 ppm); the accelerating trend (0.75 → 1.64 ppm a year); the remainder's leftover
  memory; STL and X-13.
- **Exponential smoothing.** Brown and Holt's level; Yule's mortality smoothed; Holt–Winters forecasting CO₂ for
  1998–2001 (MASE 0.78 vs 4.02 for the seasonal naive); the damped trend; Muth and ETS.
- **Spurious regression.** Two independent walks with t = −13.2; Granger and Newbold's experiment (75% significant);
  Phillips's √n; Durbin–Watson and the R² > DW rule; differencing; cointegration; two Board rows.
- **The M-competitions.** Makridakis and Hibon (1979) to M4 (2018); a 63-series competition of our own, in which the
  combination wins on average; Bates and Granger; rolling-origin evaluation.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- Yule's series (as Hipel and McLeod read them from his graph), the sunspots and the Mauna Loa CO₂ record (as
  statsmodels ships them) come from the Museum;
- everything else is a seeded simulation.

**Built in this part:**
- **`statkit.ts` (I)** ([`explainer/stats/kit/ts.py`](../../../explainer/stats/kit/ts.py)), checked against
  statsmodels in `tests/test_stats_kit_ts.py`:
  - the sample ACVF, ACF and PACF (Durbin–Levinson);
  - ARMA simulation, AR and MA roots, ψ weights, the theoretical ACF, the AR(2) period;
  - Yule–Walker, conditional least squares, AIC over AR orders, Ljung–Box;
  - AR forecasts with intervals, simple exponential smoothing, additive Holt–Winters with fitted constants,
    classical decomposition, MASE;
  - the AR(1) effective sample size, the Newey–West SE and the moving-block bootstrap.
- **The correlogram** (`Correlogram` in `explainer/stats/viz.py`): ACF or PACF bars with Bartlett's bands, the bars
  outside them lit, and theoretical values as dots.
- **The root plane** (`RootPlane`): the unit circle with polynomial roots coloured by side.
- **Yule's pendulum** (`YulePendulum`): a pendulum whose swing follows a series.

The Coverage Board gains five rows, R = 10,000.

| Method | Setting | Kind | Achieved | Verdict |
|---|---|---|---|---|
| iid t-interval, the mean | AR(1), ρ = 0.7, n = 100 | coverage | 58.07% | broken |
| Newey–West (HAC), the mean | AR(1), ρ = 0.7, n = 100 | coverage | 81.17% | broken |
| moving-block bootstrap (blocks of 10), the mean | AR(1), ρ = 0.7, n = 100 | coverage | 84.15% | broken |
| slope t-test, levels | two independent random walks, n = 100 | size | 76.68% | broken |
| slope t-test, differences | two independent random walks, n = 100 | size | 5.04% | kept |

## Build it

```bash
python -m videos.stats.stats17.compute         # once (about a minute; cached in .cache/stats17)
python tools/build.py stats17 -q l             # fast 480p preview
python tools/build.py stats17                  # 1080p30 -> renders/stats17.mp4
python tools/qa_scene.py stats17 Forecast
python tools/lecture_length.py stats17 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Nonsense correlations, 1926 | r = 0.9515 (Yule 0.9512), differences 0.0185; random walks \|r\| > 0.5 in 39%, noise 0.04% |
| 1 | Stationarity and the ACF | bands ±0.14 (n = 200); inflation 5.67, n_eff 17.6; one series: iid SE 0.145, NW 0.260, block 0.303, true 0.329; Board 58.1%, 81.2%, 84.2% |
| 2 | AR, MA, ARMA | MA(1) ρ(1) = 0.49; sunspot roots 1.03 ± 0.69i, modulus 1.24; ARMA(1,1) ψ = 1, 1.2, 0.84, 0.588 |
| 3 | Pseudo-cycles | (1.3, −0.6): r = 0.775, period 10.9; sunspots LS (1.336, −0.650), SE 0.058, period 10.6 years; ACF at lag 10–11: 0.5 vs 0.1 implied |
| 4 | Identification | simulated PACF 0.79, −0.65; sunspot PACF 0.81, −0.64 |
| 5 | Estimation | YW (1.326, −0.642); AIC best p = 8, p = 2 is 4.9 higher; Ljung–Box Q(20) = 24.1 (p = 0.15) and 11.6 (p = 0.48) |
| 6 | Forecasting | AR(1) φ = 0.8: SE → 1.67σ; MASE over 1925–35: naive 1.69, mean 1.38, AR(2) 1.20, AR(8) 0.58; 87% and 90% of 31 outcomes inside the 95% bands |
| 7 | Trend and seasonality | 316 → 371 ppm; seasonal May +2.9, October −3.2; trend 0.75 → 1.64 ppm/yr; remainder SD 0.27, ρ̂(1) = 0.40 |
| 8 | Exponential smoothing | Holt–Winters α = 0.51, β = 0.01, γ = 0.50; MASE 4.53 (flat), 4.02 (seasonal naive), 1.53 (+ drift), 0.78 (Holt–Winters) |
| 9 | Spurious regression | example t = −13.2, R² = 0.64, DW = 0.29; 75% significant; median R² 0.17, DW 0.15; differences 5.4%; Board 76.7%, 5.0% |
| 10 | The M-competitions | 63 series, 6 ahead: mean MASE 1.84, 1.84, 1.86, 1.83, combination 1.78; mean rank 2.59 for the combination |
| 11 | Outro | — |

## Sources

- **Yule, Slutsky and the founders.**
  - G. U. Yule, *JRSS* 89 (1926), 1–63; *Phil. Trans. R. Soc. A* 226 (1927), 267–298.
  - E. Slutsky, *Problems of Economic Conditions* 3 (1927; English in *Econometrica* 5, 1937).
  - G. Walker, *Proc. R. Soc. A* 131 (1931); H. Wold, *A Study in the Analysis of Stationary Time Series* (1938).
  - M. Bartlett, *JRSS Suppl.* 8 (1946); J. Durbin & G. Watson, *Biometrika* 37 (1950).
- **Models and methods.**
  - G. Box & G. Jenkins, *Time Series Analysis: Forecasting and Control* (1970); G. Ljung & G. Box, *Biometrika* 65
    (1978); H. Akaike, in *2nd Int. Symp. Information Theory* (1973).
  - R. Brown, *Statistical Forecasting for Inventory Control* (1959); C. Holt, ONR memorandum 52 (1957; reprinted
    *IJF* 20, 2004); P. Winters, *Management Science* 6 (1960); J. Muth, *JASA* 55 (1960).
  - E. Gardner & E. McKenzie, *Management Science* 31 (1985); R. Hyndman, A. Koehler, R. Snyder & S. Grose, *IJF* 18
    (2002); R. Hyndman & A. Koehler, *IJF* 22 (2006).
  - R. Cleveland, W. Cleveland, J. McRae & I. Terpenning, *J. Official Statistics* 6 (1990).
  - W. Newey & K. West, *Econometrica* 55 (1987); H. Künsch, *Ann. Stat.* 17 (1989).
- **Spurious regression and forecasting practice.**
  - C. Granger & P. Newbold, *J. Econometrics* 2 (1974); P. Phillips, *J. Econometrics* 33 (1986); R. Engle &
    C. Granger, *Econometrica* 55 (1987).
  - J. Bates & C. Granger, *Oper. Res. Q.* 20 (1969); S. Makridakis & M. Hibon, *JRSS A* 142 (1979); S. Makridakis
    et al., *J. Forecasting* 1 (1982); *IJF* 16 (2000); *IJF* 36 (2020).
- **Books.**
  - G. Box, G. Jenkins, G. Reinsel & G. Ljung, *Time Series Analysis* (5th ed., 2015); P. Brockwell & R. Davis,
    *Introduction to Time Series and Forecasting* (3rd ed., 2016); R. Hyndman & G. Athanasopoulos, *Forecasting:
    Principles and Practice* (3rd ed., 2021); R. Shumway & D. Stoffer, *Time Series Analysis and Its Applications*
    (4th ed., 2017).
- **Data.** K. Hipel & A. McLeod's time-series collection (StatLib), `roberts/yule1.1`, `yule2.1`; the sunspot and
  CO₂ datasets in statsmodels.

## Problems and solutions

**1. An AR(1).**

*Solution.* ρ(2) = φ² = 0.36. Var(Xₜ) = σ²/(1 − φ²) = σ²/0.64 = 1.5625σ². The two-step forecast is
φ²xₙ = 0.36 × 5 = 1.8, with error eₙ₊₂ + φeₙ₊₁, so its SE is σ√(1 + φ²) = σ√1.36 ≈ 1.166σ.

**2. An MA(1)'s autocorrelation.**

*Solution.* ρ(1) = θ/(1 + θ²). Since (1 − |θ|)² ≥ 0, 1 + θ² ≥ 2|θ|, so |ρ(1)| ≤ ½, with equality only when
|θ| = 1. The population lag-one ACF cannot exceed ½ in magnitude under this MA(1) model. A sample ACF can exceed the bound through sampling error, so a single observed spike does not rule out the model.

**3. An effective sample size.**

*Solution.* For large n, n_eff ≈ n(1 − ρ)/(1 + ρ) = 200 × 0.5/1.5 ≈ 66.7. The mean's SE is about √3 ≈ 1.73 times the iid formula.

**4. Is it stationary?**

*Solution.* φ(z) = 1 − 0.5z − 0.3z². Its roots solve 0.3z² + 0.5z − 1 = 0: z = (−0.5 ± √(0.25 + 1.2))/0.6, that is
z ≈ 1.174 and z ≈ −2.840. Both lie outside the unit circle, so the model is causal and stationary with the model innovations. The triangle agrees:
φ₁ + φ₂ = 0.8 < 1, φ₂ − φ₁ = −0.2 < 1 and |φ₂| < 1. The roots are real (φ₁² + 4φ₂ = 1.45 > 0), so there is no complex-root pseudo-cycle; a negative real root can still contribute alternating signs.

**5. Yule–Walker for an AR(2).**

*Solution.* Solving ρ₁ = φ₁ + φ₂ρ₁ and ρ₂ = φ₁ρ₁ + φ₂ gives
φ₁ = ρ₁(1 − ρ₂)/(1 − ρ₁²) and φ₂ = (ρ₂ − ρ₁²)/(1 − ρ₁²).
- **φ₁:** 0.7 × 0.5/0.51 ≈ 0.686.
- **φ₂:** (0.5 − 0.49)/0.51 ≈ 0.020.

The second lag adds almost nothing: these autocorrelations are close to an AR(1)'s (0.7, 0.49).

**6. The weights of exponential smoothing.**

*Solution.* Σⱼ α(1 − α)ʲ = α/(1 − (1 − α)) = 1. Their average age is Σⱼ jα(1 − α)ʲ = α(1 − α)/α² = (1 − α)/α:
2.33 periods for α = 0.3, 0.25 for α = 0.8.

## Glossary

- **Time series**: observations indexed by time, usually dependent.
- **(Weak) stationarity**: a constant mean and a covariance γ(h) depending only on the lag h.
- **Autocorrelation function (ACF), ρ(h)**: the correlation of a series with itself h steps back.
- **Partial autocorrelation (PACF), α(h)**: the last coefficient of the best AR(h) predictor; the correlation at lag h
  after removing the lags in between.
- **White noise**: uncorrelated shocks with mean 0 and constant variance.
- **Correlogram; Bartlett's bands**: a sample ACF plot; ±2/√n are approximate pointwise 95% reference bands under IID noise with suitable moments, not simultaneous limits for arbitrary uncorrelated noise.
- **Effective sample size**: the number of independent observations carrying the same information about the mean.
- **HAC (Newey–West) standard error**: an SE built from weighted sample autocovariances.
- **Moving-block bootstrap**: resampling blocks of consecutive observations to keep their dependence.
- **AR(p), MA(q), ARMA(p, q)**: autoregressive, moving-average and mixed models built from shocks.
- **ψ weights; Wold decomposition**: a finite-variance weakly stationary series is a linearly deterministic component plus an MA(∞) of uncorrelated innovations.
- **Causal stationary and invertible**: AR and MA polynomial roots outside the unit circle.
- **Unit root; random walk**: φ = 1; shocks never fade and the variance grows without limit.
- **Pseudo-cycle**: a quasi-periodic swing from complex roots, with varying amplitude and length.
- **Box–Jenkins cycle**: identify, estimate, check, forecast.
- **Differencing; ARIMA(p, d, q)**: modelling the d-th differences as an ARMA.
- **Yule–Walker equations**: moment equations linking AR coefficients to autocorrelations.
- **AIC**: n log σ̂² + 2(number of parameters); smaller is better.
- **Ljung–Box Q**: a portmanteau test that residual autocorrelations are all zero.
- **MASE**: mean absolute error scaled by the in-sample error of a naive forecast.
- **Classical decomposition; seasonal figure**: trend by a centred moving average, season by monthly averages.
- **Exponential smoothing; Holt–Winters; damped trend**: forecasts from smoothed level, slope and season.
- **Spurious regression**: a significant regression between independent nonstationary series.
- **Durbin–Watson statistic**: ≈ 2(1 − ρ̂₁) of the residuals; far below 2 signals autocorrelation.
- **Cointegration**: nonstationary series with a stationary combination.
- **Forecast combination**: averaging forecasts so that their errors partly cancel.
- **Rolling-origin evaluation**: cross-validation for time, always forecasting from the past.

## Where it comes back

| Idea | Returns in |
|---|---|
| time-series cross-validation, rolling origins | 19 |
| spectra, unit-root tests, cointegration, GARCH, the Kalman filter | 38 |
| dependence in space | 39 |
| martingales, mixing, ergodic theorems | 44 |
| monitoring a stream with anytime-valid guarantees | 58 |
| forecasting with machine learning | 64 |
| the Coverage Board | every part; 65 |

## Review clarifications

The historical Yule arrays were checked against the archived TSDL files `data-raw/roberts/yule1.dat` and `yule2.dat` at commit `e56a918d210eb637a2683c1cc6f4abb4c1bd8922` of FinYang/tsdl. Their reported units and all 46 values match the Museum. The source describes values read from Yule's graph; they are not original individual observations.

The CO₂ record fills missing historical monthly values by interpolation. No missing-month gap crosses the 1998 forecast split. Classical decomposition is retrospective: its centred filter uses future observations and itself induces residual dependence. The remainder's Ljung–Box Q is descriptive after this fitted filtering; it does not by itself prove an evolving season.

Forecast intervals are pointwise Gaussian innovation intervals with plug-in parameters. The causal root condition, decaying ARMA forecasts, partial versus conditional correlation, finite smoothing initialization, and repeating seasonal index are explicit in the scenes. The spurious-regression example uses fixed seeds 0 and 1 without selecting a striking pair; histograms omit rather than fold off-screen tail mass. Its differenced test uses 97 residual degrees of freedom. The small forecasting competition is an illustrative 63-series experiment, not a general guarantee that averaging improves every loss.
