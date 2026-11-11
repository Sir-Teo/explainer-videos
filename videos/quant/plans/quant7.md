# Part 7 · Time Series and Volatility: expansion plan (19 min → about 59 min)

Research and planning only; nothing in the repository was edited. Sources were checked on 2026-11-02. Anything marked
**(unverified)** must be checked before it goes on screen. **(expected)** marks the result a computation should
give. It is not a number for the screen: narration branches on the cached value (LECTURE_GUIDE, "Narration follows
the data").

**Three reconciliations.**
1. *Length.* The brief asks for chapters of 4–6 min, and the addendum asks for 16–20 chapters. Twenty chapters at
   4–6 min would run 80–120 min. This plan follows the AI series' practice (17–19 chapters, 50–56 min): **20
   chapters, 1.5–4 min each, about 59 min, about 8,200 narration words at the tool's ~139 wpm.** Items with a
   derivation, an experiment and a case get two or three chapters: item 4 (regimes, Kalman), item 5 (GARCH, the
   zoo, DCC) and item 10 (training, the race).
2. *Word targets.* Each chapter below gives a word budget equal to minutes × 139, not 600–800 words. Items 5, 7–8
   and 10 total more than 800 words across their chapters.
3. *Research window.* Every experiment uses data to 31 Dec 2020 (`pit.RESEARCH_END`); the 2021+ envelope stays
   sealed. Deribit DVOL (2021+) is therefore not used here.

---

## 1. Current state (measured: `python tools/lecture_length.py quant7` = **19.2 min**; README claims "about 40")

| Scene | Min | What it covers | Depth |
|---|---|---|---|
| s01 Hook "The river under the noise" | 1.7 | BTC daily returns (bars), daily 5-min RV, Kalman-filtered log vol (q/r = 0.38); objectives; House | Good real-data image, but a finished plot drawn with `Create`; no live filter; no era/history block (the standard requires 2–3 min) |
| s02 "1. Unit roots, spurious regression, cointegration" | 2.2 | AR(1) next to a random walk; Box–Jenkins and DF in one sentence each; Granger–Newbold simulation (89% / 5%, median R² 0.17); BTC against the US market (t = 24 in levels); BTC spot–perp Engle–Granger (t = −7.2, half-life 1.2 d) | Experiments are real. No derivation (no DF distribution, no ARMA, no ACF, no Ljung–Box). Johansen is one caption |
| s03 "2. Hidden states and the GARCH family" | 3.2 | Hamilton 2-regime on monthly French 1926–2020 (calm +12%/13%/55 mo; turbulent −15%/36%/10 mo); Kalman in one caption; ARCH→GARCH ladder (2 rows); GARCH on 24,896 days (α .105, β .884, half-life 63 d); GJR γ .111; logL GARCH 84,088 / GJR 84,336 / EGARCH 84,342; BTC GJR γ .14; DCC stock–bond by decade | Four syllabus items in 3.2 min. Only derivation: the 2-line ladder. No likelihood, stationarity, QMLE, news-impact derivation, Kalman equations or Hamilton filter. Nothing is shown learning |
| s04 "3. Realized volatility and HAR" | 1.9 | Bar chart RV1 106%, RV5 96%, TSRV/RK 93%, BV 92%, jumps 10%; HAR on BTC 2017–19 (b_d .41, b_w .03, b_m .43, R² .38); HARQ b_q −3.0 (t −0.7) | No QV theory, no signature plot built (it points to Part 5), no noise algebra, no jump test, HAR not derived |
| s05 "4. The race" | 2.9 | Hansen–Lunde; train/val/test calendar; 8 models; QLIKE + DM vs HAR (log-HAR .363, LSTM .371, Transf .410, HARQ .426, HAR .427, GJR .444, GARCH .452, EWMA .512); seed dots; MSE order flips; 2020 forecasts against realized | Honest and well branched. But the networks are never shown training (no replay or loss curve), QLIKE is not derived, and there is no Patton experiment, no MZ and no MCS |
| s06 "5. March 2020" | 3.1 | Crisis card; every forecast for 12 Mar (62–76%) against realized 457%; Feb–Apr window; √T desk question with the GARCH term structure (85% → 52%, long run 18%) | Good. Keep and tighten |
| s07 "6. The volatility forecaster" | 1.0 | House module table; Rule 8; trial counter 71 | Table only; no lab |
| s08 Outro | 3.0 | Recap (8 lines), 3 desk questions, 5 problems, payoffs, references | Fine |

Missing from every chapter: the era/history block, a signature visual built before the formula (most visuals are
static plots drawn by `Create`), pause-and-predict questions, training replays, lab moments (`code_block`), an
industry chapter, a frontier chapter, items 9 (roughness) and 11 (foundation models, "deferred"), and the README
textbook audit table.

---

## 2. Audit

### (a) Syllabus items (SYLLABUS §6, Part 7)

| # | Item | Now | Verdict |
|---|---|---|---|
| 1 | Stationarity, ARMA, Box–Jenkins | one AR(1) plot and one sentence | **thin** (ARMA, ACF/PACF, Wold, identification and diagnostics missing) |
| 2 | Unit roots; spurious regression | DF named; GN simulation; BTC against the US market | **thin** (no DF distribution, no Phillips 1986) |
| 3 | Cointegration (EG, Johansen) | EG on spot–perp | **thin** (no ECM, Granger representation or Johansen) |
| 4 | Regimes; Kalman | regime plot; Kalman one caption | **thin / Kalman missing** |
| 5 | ARCH/GARCH by MLE; EGARCH, GJR; DCC | parameters reported | **thin** (no likelihood, stationarity, QMLE, news-impact derivation or DCC algebra) |
| 6 | Hansen–Lunde; Patton robust losses | quoted in the race; QLIKE in a caption | **thin** (no proof, no simulation, no MZ/MCS) |
| 7 | Realized vol; signature plot; TSRV, kernels | one bar chart | **thin** (signature plot not shown in this part) |
| 8 | HAR, HARQ; jumps by BV | fitted and reported | **thin** (no HAR derivation, no BNS jump test, no HAR-CJ) |
| 9 | Roughness measured | — | **missing** (Part 14 measures H = 0.08 on BTC; Part 7 should measure it on its own RV and link forward) |
| 10 | LSTM and transformer against HAR, trained here | trained and raced | **covered in result, missing in process** (no replay or loss curves) |
| 11 | Chronos / TimesFM / Moirai zero-shot | — | **missing** (deferred for lack of packages) |
| — | Era block, industry chapter, frontier chapter, firm file | — | **missing** |

### (b) Textbooks: core sections → proposed chapter (TOCs from memory; chapter numbers marked *(verify)*)

| Book / section | Proposed chapter |
|---|---|
| **Tsay** 3e ch. 1 stylized facts | 00 Hook, 01 (ACF of r, \|r\|, r²) |
| Tsay ch. 2 ACF, AR/MA/ARMA, Ljung–Box, unit roots, long memory | 01, 02; long memory → 10 (HAR) |
| Tsay ch. 3 ARCH, GARCH, IGARCH, GARCH-M, EGARCH, TGARCH, SV, long-memory SV | 06, 07; SV → 05; GARCH-M named in 07 |
| Tsay ch. 4 nonlinear: TAR, STAR, **Markov switching**, neural nets | 04; NN → 13; TAR/STAR named only, as a forward link to Part 27 |
| Tsay ch. 5 high-frequency: bid–ask bounce, nonsynchronous trading, durations (ACD) | 09 (noise); ACD → Part 36 |
| Tsay ch. 7 extreme values, VaR | → Part 40 (said in 16) |
| Tsay ch. 8 VAR, **cointegration**, ECM, pairs trading | 03; pairs → Part 33 |
| Tsay ch. 10 multivariate volatility (EWMA, BEKK, DCC) | 08 |
| Tsay ch. 11 state space, **Kalman filter** and smoother | 05 |
| Tsay ch. 12 MCMC for SV | named in 05 (QML instead); Bayesian → Part 6 |
| **Hamilton** ch. 3–4 ARMA, forecasting; 5 MLE | 01, 06 |
| Hamilton ch. 6 spectral analysis | **dropped, stated:** one line in 01 (the ACF and the spectrum are Fourier pairs); not core for volatility |
| Hamilton ch. 10–11 VARs | 03 (VECM form); VAR impulse responses → Part 32 *(say so)* |
| Hamilton ch. 13 **Kalman filter** | 05 |
| Hamilton ch. 15–17 unit roots, DF asymptotics (functional CLT) | 02 |
| Hamilton ch. 18–20 multivariate unit roots, **cointegration, Johansen FIML** | 03 |
| Hamilton ch. 21 heteroskedasticity (ARCH/GARCH) | 06, 07 |
| Hamilton ch. 22 **regime switching** | 04 |
| **Brockwell–Davis** (*Intro. to Time Series and Forecasting*, 3e) ch. 1–3, 5 stationarity, ARMA, forecasting | 01 |
| B–D ch. 6 ARIMA, unit roots; ch. 7 financial time series (GARCH, SV) *(verify ch. numbers)*; ch. 9 state space | 02, 06, 05 |
| B–D ch. 4 spectral | dropped (as Hamilton ch. 6) |
| **Francq–Zakoian** *GARCH Models* (2e 2019) ch. 2 GARCH stationarity (strict, Lyapunov) | 07 |
| F–Z ch. 4 EGARCH/GJR/APARCH; ch. 7 QMLE consistency and asymptotic normality; ch. 8 tests | 07 |
| F–Z ch. 10–11 multivariate GARCH (BEKK, CCC, DCC) | 08 |
| **Aït-Sahalia–Jacod** ch. 3/6 integrated volatility without noise (RV → IV, CLT) | 09 |
| A-S–J ch. 7 noise (TSRV, MSRV, kernels, pre-averaging) | 09; pre-averaging named |
| A-S–J ch. 8 spot volatility; ch. 9 irregular sampling | named in 09 *(one line each)* |
| A-S–J ch. 10–12 jump tests, activity index | 10 (BNS test); activity index → Part 13 |
| **Andersen–Bollerslev–Christoffersen–Diebold** (2006), "Volatility and correlation forecasting", *Handbook of Economic Forecasting* vol. 1 ch. 15: uses of forecasts, GARCH, SV, RV, multivariate, evaluation | 06–12, 17 (industry) |
| Andersen–Bollerslev–Diebold (2010), "Parametric and nonparametric volatility measurement", *Handbook of Financial Econometrics* | 09 |
| **CLM** ch. 12 nonlinearities: changing volatility, ANNs, data snooping | 06, 13, 12 |
| **QRM** ch. 4 *(verify ch. number)* financial time series: stylized facts, GARCH, EWMA, filtered HS | 00, 06, 17; FHS → Part 40 |
| Hayashi ch. 6, 9–10 (HAC, unit roots, cointegration) | 02, 03 (HAC itself is Part 6) |

Proposed additions to READING.md §1 for Part 7: Brockwell–Davis, Francq–Zakoian, and the two handbook chapters.

### (c) Papers in READING.md "Part 7" → proposed placement

| Paper | Now | Proposed |
|---|---|---|
| Kalman (1960) | mentioned (caption) | **on screen** 05 (equations; history card) |
| Box–Jenkins (1970) | mentioned | on screen 01 (identify–estimate–check loop) |
| Granger–Newbold (1974) | on screen | on screen 02 |
| Dickey–Fuller (1979) | mentioned | on screen 02 (distribution derived and simulated) |
| Engle (1982) | on screen | on screen 06 (UK inflation, history card) |
| Bollerslev (1986) | on screen | on screen 06 |
| Engle–Granger (1987) | on screen | on screen 03 (two-step + ECM) |
| Hamilton (1989) | on screen | on screen 04 (filter equations) |
| Nelson (1991) EGARCH | caption | on screen 07 (equation, news impact) |
| Johansen (1991) | caption | on screen 03 (reduced rank, trace test, run) |
| GJR (1993) | caption | on screen 07 |
| Engle (2002) DCC | on screen | on screen 08 (recursion) |
| Barndorff-Nielsen–Shephard (2002, 2004) | bipower named | on screen 09 (CLT), 10 (BV) |
| ABDL (2003) | named in README | on screen 09 (history card + RV→IV) |
| Zhang–Mykland–Aït-Sahalia (2005) | caption | on screen 09 (TSRV algebra) |
| Hansen–Lunde (2005) | on screen | on screen 12, 14 |
| BNHLS (2008) | caption | on screen 09 (kernel formula) |
| Corsi (2009) | on screen | on screen 10 (derived) |
| Patton (2011) | caption | on screen 12 (proof + simulation) |
| Bollerslev–Patton–Quaedvlieg (2016) | on screen | on screen 10 (attenuation derivation) |
| Gatheral–Jaisson–Rosenbaum (2018) | absent | on screen 11 |
| Christensen–Siggaard–Veliyev (2023) — **verified**: *JFEc* 21(5):1680–1727, doi 10.1093/jjfinec/nbac020 ([RePEc](https://ideas.repec.org/a/oup/jfinec/v21y2023i5p1680-1727..html)); drop "(verify)" | absent | on screen 15 |
| Ansari et al. (2024) Chronos, *TMLR*, arXiv 2403.07815 | absent | on screen 15 (run) |
| Das et al. (2024) TimesFM, *ICML*, arXiv 2310.10688 | absent | on screen 15 (run) |
| Woo et al. (2024) Moirai, *ICML*, arXiv 2402.02592 | absent | on screen 15 (named; run if `uni2ts` installs) |

Proposed **additions** (all used below): Yule (1927, *Phil. Trans. A*, sunspots → AR); Mandelbrot (1963, *J.
Business*); Ljung–Box (1978, *Biometrika*); Phillips (1986, *J. Econometrics* 33) spurious-regression asymptotics;
Nelson (1990, *Econometric Theory*) GARCH(1,1) stationarity; Bollerslev–Wooldridge (1992, *Econometric Reviews*)
QMLE standard errors; Hall–Anderson–Granger (1992, *REStat*) T-bill yields cointegrated; Murray (1994, *American
Statistician*) "A drunk and her dog" *(volume/pages unverified)*; Harvey–Ruiz–Shephard (1994, *REStud*) QML SV;
J.P. Morgan/Reuters, *RiskMetrics Technical Document*, 4th ed. (1996) **verified**; BNS (2006, *JFEc*) jump test;
Andersen–Bollerslev–Diebold (2007, *REStat*) HAR-CJ; Bandi–Russell (2008, *REStud*) optimal sampling;
Mincer–Zarnowitz (1969); Diebold–Mariano (1995, *JBES*); Hansen–Lunde–Nason (2011, *Econometrica*) MCS;
Patton–Sheppard (2015, *REStat*) semivariances; Moskowitz–Ooi–Pedersen (2012, *JFE*); Moreira–Muir (2017, *JF*);
Harvey et al. (2018, *JPM*) **verified**; Bollerslev–Hood–Huss–Pedersen (2018, *RFS*) "Risk everywhere"; MSCI USE4
methodology (Menchero–Orr–Wang 2011) *(document not retrieved; see §4)*; the frontier list in chapter 15.

---

## 3. The proposed chapter list (20 chapters, about 59 min)

Shared new instruments (proposed for `explainer/quant/viz.py`):
- `LeakyBucket`: water level = σ², a tap ω, a leak (1−β), splashes αr²;
- `BeliefBell`: a Gaussian riding the time axis, with predict-widen and update-pull;
- `RegimeJars`: two jars with probability liquid flowing between them;
- `LiveLeaderboard`: cumulative-loss bars racing as a cursor runs through the test year;
- `SquaresPath`: a price path with its increments drawn as squares whose total area is RV.

Labs use `code_block` from `explainer/ai/viz.py`, at most 12 lines of the House's real code, followed by a live
run. Replays follow AI Part 21 `s12_reflow.replay`: a `ValueTracker` over checkpoints, a loss curve with a riding
dot, model outputs morphing, and seeds drawn as `band`s.

Timeline years to add to `TIMELINE` in `explainer/quant/__init__.py` (a shared file; append only, so other parts
are unaffected): 1927 Yule; 1960 Kalman; 1970 (extend: "Box–Jenkins"); 1979 (extend: "Dickey–Fuller"); 1986
(extend: "Bollerslev: GARCH"); 1989 Hamilton; 2003 "Nobel: Engle (ARCH), Granger (cointegration)"; 2009 (extend:
"Corsi: HAR").

---

### 00 · The river under the noise (2.5 min, ~350 words) — *keep s01, rebuild the opening*
**Goal.** Volatility clusters, and it is forecastable when direction is not. Where the ideas came from.
**Beats.** 94 years of the US market's daily returns run across the screen. Each day's |r| lights up in proportion
to its size, so clusters glow as bands (1929–33, 1987, 2008, 2020). Mandelbrot 1963: "large changes tend to be
followed by large changes." Pause-and-predict: will tomorrow's sign be predictable, and will tomorrow's size? Then
the ACF of r (flat) against the ACF of |r| (high, slow decay) is built bar by bar. The BTC river follows: the
existing Kalman image, now **run live** (a cursor; the BeliefBell's mean traces the river as each day's dot
lands). History strip, 90 s: Yule 1927 (sunspots, the first AR), Kalman 1960, Box–Jenkins 1970, Dickey–Fuller
1979, Engle 1982 (ARCH on UK inflation), Bollerslev 1986, Engle–Granger 1987, Hamilton 1989, RiskMetrics 1994
(J.P. Morgan, launched October 1994, data free on the Internet: *TD 4e*, preface, verified), ABDL 1998–2003, the
2003 Nobel (Engle "for methods of analyzing economic time series with time-varying volatility (ARCH)", quoted in
Harvey et al. 2018 fn. 1; Granger for cointegration), Corsi 2009, roughness 2018, foundation models 2024.
Objectives, then the House.
**Signature visual.** The century of returns with clusters lighting up: brightness ∝ |r| through a smoothed glow, so
the viewer *sees* a slow hidden variable before it is named.
**Experiment.** `acf_arma` item (below): ACF of r, |r| and r², lags 1–250, on 24,896 days. *(expected:* |r| at lag 1
≈ 0.3 and still ≈ 0.1 at lag 250; r within ±0.05 after lag 1).

### 01 · Stationarity, ARMA and Box–Jenkins (3.5 min, ~490 words) — *new*
**Goal.** Weak stationarity, ACF/PACF, AR/MA/ARMA, Wold; Box–Jenkins identify → estimate → check.
**Beats.** Definition card (constant mean, autocovariance depends only on the lag). The AR(1) as a ball on a spring
kicked by shocks; a slider runs φ from 0 → 0.5 → 0.9 → 0.99, and the path, ACF bars and variance readout change
together. Derivation (below). MA(1): the ACF cuts off after lag 1, while AR's PACF cuts off. Wold: every stationary
series is an MA(∞) of its innovations. Box–Jenkins loop as a 3-node cycle. Run on **log VIX 1990–2020** (FRED
VIXCLS, cached). The ACF decays slowly, so candidate models are fitted. The AIC table fills in. Ljung–Box on the
residuals, then on the squared residuals of daily returns: returns pass and squares fail by a mile, which is the
door to GARCH. One line: spectral analysis is the same information in frequency, not used here.
**Derivation.**
- $x_t=\phi x_{t-1}+\varepsilon_t=\sum_{k\ge0}\phi^k\varepsilon_{t-k}$ — substitute back (needs $|\phi|<1$)
- $\operatorname{Var}x_t=\sigma^2\sum\phi^{2k}=\sigma^2/(1-\phi^2)$ — independent shocks, geometric sum
- $\gamma_k=\phi^k\gamma_0,\ \rho_k=\phi^k$ — multiply by $x_{t-k}$, take expectations
- $\mathbb E_t x_{t+h}=\phi^h x_t$, half-life $\ln\tfrac12/\ln\phi$ — iterate the recursion
- $Q=T(T+2)\sum_{k=1}^m\hat\rho_k^2/(T-k)\sim\chi^2_m$ — Ljung–Box, under white noise
**Lab 1** `vol.ar_fit` (6 lines: build lag matrix, `lstsq`, residual σ) → run on log VIX; φ̂ and half-life appear.
*(expected:* AR(1) φ ≈ 0.97–0.99, half-life ≈ 1–2 months; the AIC prefers ARMA(1,1) or AR(2) *(unverified, computed)*.)
**Pause-and-predict.** "As φ → 1, what happens to the variance and the half-life?" (Both → ∞, which is the next chapter.)

### 02 · Unit roots and spurious regression (3.5 min, ~490 words) — *rebuild s02 parts 1–2*
**Goal.** Why the DF t-stat is not normal; why levels regressions lie.
**Beats.** The spring snaps at φ = 1: the variance funnel opens as √t. The DF regression. **Signature:** 20,000
simulated random walks stream in, and their t-statistics pile into a histogram live, visibly left of the
dashed N(0,1). The 5% line settles at −2.86. Derivation of the limit. Run ADF (Lab 2) on BTC log price (t =
0.96, cached), log VIX, the 10-year yield and the French log index. Then spurious regression: two independent
walks, the OLS line pivoting as T grows, and a t-counter climbing like √T (Phillips 1986). Keep the cached GN
numbers (89% / 5%, median R² .17) and BTC–US (t = 24 → 6.7).
**Derivation** (ρ = 1, x₀ = 0):
- $x_t^2=x_{t-1}^2+2x_{t-1}\varepsilon_t+\varepsilon_t^2\Rightarrow \sum x_{t-1}\varepsilon_t=\tfrac12\big(x_T^2-\sum\varepsilon_t^2\big)$ — square and telescope
- $T^{-1/2}x_{\lfloor rT\rfloor}\Rightarrow\sigma W(r)$ — Donsker
- $T(\hat\rho-1)=\dfrac{T^{-1}\sum x_{t-1}\varepsilon_t}{T^{-2}\sum x_{t-1}^2}\Rightarrow\dfrac{\tfrac12(W(1)^2-1)}{\int_0^1W^2dr}$ — continuous mapping; $T^{-1}\sum\varepsilon^2\to\sigma^2$
- $t_{DF}\Rightarrow\tfrac12(W(1)^2-1)/\sqrt{\int W^2}$ — skewed left: $W(1)^2<1$ with prob. 0.68
- spurious: $\hat\beta\Rightarrow\int W_1W_2/\int W_2^2$ (random, not 0), $t=O_p(\sqrt T)$ — Phillips (1986)
**Lab 2** `vol.adf` (9 lines) → run on the four series.
**Experiment** `unitroot` (new). *(expected:* simulated 5% quantile −2.86 ± 0.03 (constant); BTC 0.96 (cached); the 10y
yield 1962–2020 does not reject *(expected; the narration branches)*.)
**Pause-and-predict.** "The 10-year yield can't go to infinity. Does it have a unit root?" (Statistically it is
indistinguishable from one over 60 years. Unit-root tests have low power near φ = 1.)

### 03 · Cointegration (3.5 min, ~490 words) — *rebuild s02 part 3*
**Goal.** Engle–Granger two-step, error correction, Granger representation; Johansen for many series.
**Beats.** **Signature:** "a drunk and her dog" (Murray 1994): two walkers on a 2D plane, each a random walk, tied by
an elastic leash. Their paths wander off-screen, and the camera follows. A side gauge shows the leash length,
which stays bounded. Error-correction arrows show each walker pulled toward the other in proportion to the gap.
Then the real pair: BTC spot and perpetual (cached: ADF .96/.94, EG t −7.2, half-life 1.2 d, −74 bp on 12 Mar). The
ECM is fitted, with α (the speed of each leg's correction) and a note on which leg does the correcting.
**Johansen in 3D** (`ThreeDScene`): daily (3m bill, 5y, 10y) yields 1990–2020 as a point cloud. The camera orbits
until the cloud is seen edge-on: thin directions are cointegrating vectors, the long direction is the common
trend. The trace statistic is read off. Forward links to Part 33 (pairs) and Part 19 (yield factors).
**Derivation.**
- $y_t-\beta x_t=u_t\sim I(0)$ while $x_t,y_t\sim I(1)$ — definition
- $\Delta y_t=\alpha_y(y_{t-1}-\beta x_{t-1})+\dots+e_t$ — ECM; Granger representation theorem: cointegration ⇔ ECM
- EG critical value −3.34, not −2.86 — $\hat\beta$ is chosen to make $u$ look stationary
- VECM $\Delta X_t=\Pi X_{t-1}+\sum\Gamma_i\Delta X_{t-i}+\varepsilon_t,\ \Pi=\alpha\beta'$, rank $r$ — levels/differences split
- $\lambda_{trace}(r)=-T\sum_{i>r}\ln(1-\hat\lambda_i)$, with $\hat\lambda_i$ the squared canonical correlations of $\Delta X$ and $X_{t-1}$ — reduced-rank regression (Johansen)
**Experiment** `coint` (extended). New FRED pulls: DGS5 (DTB3 and DGS10 are cached), checksummed. *(expected:* rank ≥ 1 at
5%, one or two common trends; Hall–Anderson–Granger (1992) found one common trend in T-bill yields. Branch on the
computed rank.)
**Pause-and-predict.** "If spot and perp are cointegrated, which one moves to close the gap?" (Read α: the
narration states whichever leg has the larger |α|.)

### 04 · Hidden regimes (2.5 min, ~350 words) — *split from s03*
**Goal.** The Hamilton filter as Bayes on a 2-state Markov chain; EM; expected durations.
**Beats.** **Signature:** `RegimeJars`, two jars (calm, storm) holding probability liquid. Each month, *predict*:
liquid flows between jars by P (a leak of 1−p₁₁). Then *update*: the month's return lands as a dot under two
Gaussian densities, and each jar is rescaled by its density height, then renormalised. Run month by month through
1929–33, then fast-forward. The red area of the cached regime plot is drawn *by* this process. **EM replay:** the
log-likelihood climbs over EM iterations while the two fitted densities slide apart (checkpoints every 10
iterations). Cached results: calm +12%/13%/55 months, turbulent −15%/36%/10 months, 14% of months turbulent.
**Derivation.**
- $\xi_{t|t}=\dfrac{\xi_{t|t-1}\odot\eta_t}{\mathbf 1'(\xi_{t|t-1}\odot\eta_t)}$ — Bayes ($\eta_{t,j}$ = density of $r_t$ in regime $j$)
- $\xi_{t+1|t}=P'\xi_{t|t}$ — Markov prediction
- $\Pr(D=d)=p_{ii}^{d-1}(1-p_{ii})\Rightarrow\mathbb E D=1/(1-p_{ii})$ — geometric duration
- $\pi_{storm}=(1-p_{11})/(2-p_{11}-p_{22})$ — stationary distribution
**Experiment** `regimes` (+ EM checkpoints; cheap).
**Pause-and-predict.** "A −8% month arrives in the calm regime. Does the storm jar fill completely?" (No. Its
height is the posterior; show the number.)

### 05 · The Kalman filter (3.0 min, ~420 words) — *new*
**Goal.** Predict–update as Gaussian conditioning; the gain; steady state; stochastic volatility by QML.
**Beats.** **Signature:** `BeliefBell`. A Gaussian belief about today's hidden log-vol rides the time axis. *Predict*:
it widens (P + Q). *Observe*: a measurement dot arrives with its own (wider) noise bell. *Update*: the posterior
bell is the product, narrower and pulled a fraction K of the way to the dot (an arrow labelled K(y − m)). Slow, then
faster, on BTC's log RV, which redraws the hook's river. Derivation by completing the square. Steady-state gain on
screen as a curve K(q), with the BTC point q = 0.38 → K ≈ 0.45 (README problem 5). **Lab 3** `kalman_local_level.run`
(10 lines) → run, with the river appearing live. Then **stochastic volatility**: the hidden log-variance is AR(1),
and log r² is its noisy measurement (Harvey–Ruiz–Shephard 1994). Fitted by QML on 94 years of the US market. The SV
volatility path is overlaid on GARCH's (next chapter), and the two nearly coincide. Smoother, in one line.
**Derivation.**
- $x_t=x_{t-1}+w_t,\ y_t=x_t+v_t$; prior $N(m,P)$ → $N(m,P+Q)$ — predict
- $p(x|y)\propto e^{-(x-m)^2/2P^-}e^{-(y-x)^2/2R}$ — Bayes
- precision $1/P^+=1/P^-+1/R$, mean $m^+=m+K(y-m)$, $K=P^-/(P^-+R)$ — complete the square
- steady state: $P^-=P^++Q$, $P^+=(1-K)P^-$ ⇒ $p^2-qp-q=0$, $p=\tfrac{q+\sqrt{q^2+4q}}2$, $K=\tfrac p{1+p}$ — divide by $R$
- SV: $\ln r_t^2=h_t+\ln z_t^2$, $\mathbb E\ln\chi^2_1=\psi(\tfrac12)+\ln2=-1.27$, $\operatorname{Var}=\pi^2/2=4.93$ — moments of $\ln\chi^2_1$
**Experiment** `kalman` (new). *(expected:* SV φ ≈ 0.98–0.99, σ_η ≈ 0.1–0.2; the SV vol correlates > 0.9 with GARCH vol.)
**Pause-and-predict.** "If the measurement gets noisier (R up), does the belief move more or less toward each dot?"

### 06 · ARCH and GARCH by maximum likelihood (3.5 min, ~490 words) — *rebuild s03 garch*
**Goal.** The recursion, its long-run level, the likelihood, the term structure; GARCH as ARMA for r²; EWMA as IGARCH.
**Beats.** Engle 1982 history card (UK inflation). **Signature:** `LeakyBucket`. The water level is σ². A steady tap
pours ω. The bucket keeps β of yesterday's water. Each day a return is drawn *with size ∝ √level*, and its splash αr²
is added. Run the simulation: a high level makes big draws, which make big splashes, so clusters appear by
themselves. The long-run level is where the leak balances the inflow, derived from the picture. Then real data:
**Lab 4** `vol.garch_filter` (7 lines) → run on 24,896 days, the variance drawn day by day (fast). **Training
replay:** the log-likelihood surface over (α, β), with ω set by variance targeting, as a 3D `loss_surface`. The
optimiser's path is a ball climbing it (`surface_ball`), the fitted vol path morphs at each iterate, and a logL
readout climbs to 84,088. Cached α .105, β .884, half-life 63 d. RiskMetrics' EWMA is GARCH with ω = 0, α + β = 1:
the bucket never drains to a long-run level (TD 4e §5.2 says so, footnote 4).
**Derivation.**
- $r_t=\sigma_tz_t,\ \sigma_t^2=\omega+\alpha r_{t-1}^2+\beta\sigma_{t-1}^2$ — definition
- $\bar\sigma^2=\omega+(\alpha+\beta)\bar\sigma^2\Rightarrow\bar\sigma^2=\omega/(1-\alpha-\beta)$ — take expectations, $\mathbb E r^2=\mathbb E\sigma^2$
- $\sigma_t^2=\tfrac{\omega}{1-\beta}+\alpha\sum_{k\ge1}\beta^{k-1}r_{t-k}^2$ — unroll: an EWMA of squares plus a floor
- $\ell(\theta)=-\tfrac12\sum[\ln2\pi+\ln\sigma_t^2+r_t^2/\sigma_t^2]$ — Gaussian density, prediction-error decomposition
- $\mathbb E_t\sigma^2_{t+h}=\bar\sigma^2+(\alpha+\beta)^{h-1}(\sigma^2_{t+1}-\bar\sigma^2)$ — tower property (README problem 1)
- $r_t^2=\omega+(\alpha+\beta)r_{t-1}^2+\nu_t-\beta\nu_{t-1}$ — ARMA(1,1) in $r^2$, $\nu=r^2-\sigma^2$
**Experiment** `garch` (extended): the optimiser trajectory via `optimize.minimize(callback=…)`; the likelihood grid
81×81 via `scipy.signal.lfilter([α],[1,−β], r²)` (seconds).
**Pause-and-predict.** "α + β = 0.989. After a shock, how many days until half of it is gone?" (63.)

### 07 · Stationarity, QMLE and asymmetry: the GARCH zoo (3.0 min, ~420 words) — *new + s03 leverage*
**Goal.** Nelson's strict-stationarity condition; QMLE robustness; Student-t; GJR and EGARCH via news impact.
**Beats.** **Signature 1:** the (α, β) plane. The covariance-stationary triangle α + β < 1 is shaded. Nelson's curve
E ln(αz² + β) = 0 is drawn *beyond* it. Fitted assets appear as dots (US, BTC, and the stock–bond leg). IGARCH sits
on the line yet is strictly stationary. **Signature 2:** news-impact curves morph GARCH → GJR → EGARCH (cached γ
.111: a fall raises variance about 4× a rise). Student-t GARCH: ν estimated; the QQ plot of standardized residuals
straightens. QMLE: the Gaussian score has mean zero whenever E z² = 1, so the estimates stay consistent under fat
tails, with sandwich standard errors (Bollerslev–Wooldridge 1992). GARCH-M is named, with a link to Part 23.
**Derivation.**
- $\sigma_t^2=\omega\sum_{k\ge0}\prod_{j=1}^{k}(\alpha z_{t-j}^2+\beta)$ — unroll the recursion
- $\tfrac1k\ln\prod_{j\le k}(\alpha z^2+\beta)\to\mathbb E\ln(\alpha z^2+\beta)$ — SLLN, so the series converges iff $<0$ (Nelson 1990)
- $\mathbb E\ln(\alpha z^2+\beta)<\ln\mathbb E(\alpha z^2+\beta)=\ln(\alpha+\beta)$ — Jensen: IGARCH is strictly stationary
- $\mathbb E[\partial\ell_t/\partial\theta]=\tfrac12\mathbb E[(z_t^2-1)\,\partial\ln\sigma_t^2/\partial\theta]=0$ — needs only $\mathbb E z^2=1$; $\operatorname{Var}\hat\theta=A^{-1}BA^{-1}$
- GJR $\sigma_t^2=\omega+(\alpha+\gamma\mathbf 1_{r<0})r_{t-1}^2+\beta\sigma_{t-1}^2$, persistence $\alpha+\gamma/2+\beta$ — symmetric $z$
- EGARCH $\ln\sigma_t^2=\omega+\alpha(|z|-\mathbb E|z|)+\gamma z+\beta\ln\sigma_{t-1}^2$ — no positivity constraints
**Experiment** `garch` (t-GARCH; the Nelson boundary by Gauss–Hermite quadrature on a grid). *(expected:* ν ≈ 6–9 on the
US market.)
**Pause-and-predict.** "α = 0.3, β = 0.75: the sum is 1.05. Does the variance explode?" (No. With Gaussian z, E ln(αz² + β) =
−0.008 < 0, so it is strictly stationary with infinite variance. At α = 0.25, β = 0.80, also summing to 1.05, it is +0.008: explosive. Both values were checked by 4M-draw Monte Carlo.)

### 08 · Correlations that move: DCC (2.5 min, ~350 words) — *rebuild s03 dcc*
**Goal.** Why multivariate GARCH needs structure; DCC's two-step likelihood.
**Beats.** **Signature:** the covariance ellipse of daily (stock, bond) returns, one ellipse per year 1962–2020. It
breathes in size (volatility) and *tilts* through vertical (correlation) around 2000, with a ρ dial tracking it.
Parameter count: full VEC and BEKK for N = 100 (counter rolls) against DCC's 2 + 3N. Cached a .029, b .969, decade
averages +.19 … −.46; 2022 named outside the window. EWMA correlation (λ = .94) is overlaid: noisier.
**Derivation.**
- $H_t=D_tR_tD_t$ — separate the vols from the correlations
- $Q_t=(1-a-b)\bar Q+a\,z_{t-1}z_{t-1}'+bQ_{t-1},\ R_t=\operatorname{diag}(Q_t)^{-1/2}Q_t\operatorname{diag}(Q_t)^{-1/2}$ — GARCH for correlations, renormalised
- $\ell=\ell_{vol}(\theta_1)+\ell_{corr}(\theta_2\mid\theta_1)$ — the log-det splits, so estimation runs in two steps
- BEKK parameters $N(N+1)/2+2N^2$ (N = 100: 25,050) — count
**Pause-and-predict.** "Your 60/40 risk model assumed ρ = +0.3 in 2010. Was the portfolio riskier or safer than
the model said?" (Safer.)

### 09 · Realized volatility: measuring it after the fact (3.5 min, ~490 words) — *rebuild s04 measures*
**Goal.** QV, RV → IV and its CLT; microstructure noise; the signature plot built; TSRV and kernels; optimal sampling.
**Beats.** ABDL history card. **Signature:** `SquaresPath`. Zoom into one BTC day. Every 30-min increment gets a
square drawn on it, and the total area reads out. Refine to 5-min and 1-min: the squares multiply and the total
*converges*, which is QV. Then turn on bid–ask bounce: at the finest scale tiny squares sprout on every tick, and
the area runs away. **Signature plot built live**: a slider on Δ (1→60 min) adds one point at a time for 2019,
with RV(Δ) rising as Δ shrinks. The noise algebra follows. TSRV is drawn as K offset sparse grids (colour-coded
interleaved squares) averaged, minus the dense-grid bias. The realized kernel adds weighted autocovariances.
Cached bars (106/96/93/93/92%). The CLT error band per day uses RQ. Spot volatility and irregular sampling get one
line each; pre-averaging is named.
**Derivation.**
- $p_t=\int\mu\,ds+\int\sigma\,dW$; $RV_n=\sum r_i^2\to\int_0^1\sigma_s^2ds$ — quadratic variation (Part 5)
- $\sqrt n\,(RV_n-IV)\Rightarrow MN\!\big(0,2\int\sigma^4\big)$, $\widehat{IQ}=\tfrac n3\sum r_i^4$ — BNS (2002)
- $r_i=r_i^*+u_i-u_{i-1}\Rightarrow\mathbb E RV_n=IV+2n\eta^2$ — iid noise; cross terms vanish (README problem 3)
- $MSE(n)\approx4n^2\eta^4+2IQ/n\Rightarrow n^*=(IQ/4\eta^4)^{1/3}$ — set the derivative to zero (Bandi–Russell 2008)
- $TSRV=\overline{RV}^{(K)}-\tfrac{\bar n}{n}RV^{(all)}$, rate $n^{-1/6}$ — ZMA (2005)
- $RK=\gamma_0+\sum_{h=1}^{H}k(\tfrac{h}{H+1})(\gamma_h+\gamma_{-h})$, Parzen $k$ — BNHLS (2008)
**Experiment** `realized` (extended): the signature plot at Δ ∈ {1,2,3,5,10,15,20,30,60} min per day and noise
η² = RV_all/2n per day. *(expected:* 1-min RV about 20% above the 5-min level; flat beyond 5–10 min; n* ≈ 5–15 min.)
**Pause-and-predict.** "Sampling every second gives 86,400 returns a day. Better than every 5 minutes?" (No: the bias
2nη² grows with n.)

### 10 · Jumps and HAR (3.5 min, ~490 words) — *rebuild s04 har*
**Goal.** Bipower variation and the BNS jump test; HAR as a restricted AR(22) that mimics long memory; HAR-CJ; HARQ.
**Beats.** A path with one jump. RV's squares include a giant square for the jump. BV's rectangles |r_i||r_{i−1}|
pair the jump with a tiny neighbour, so the rectangle stays thin. That *is* the idea. BNS z per day; the share of
jump days; 12 Mar 2020. **Signature:** three rivers (yesterday, last week, last month) flow into a forecast pool, with
the weights as widths. Then the **lag-weight staircase**: HAR's implied AR(22) weights against GARCH's geometric
decay, with the empirical ACF of log RV on log-log axes, where HAR follows the slow decay and GARCH falls off.
**Lab 5** `vol._har_design` + `har_fit` (10 lines) → run; rolling 252-day re-estimation as a **replay**: the three
coefficients drift as bars while a cursor runs 2018–2020. Cached b_d .41, b_w .03, b_m .43, R² .38. HARQ:
errors-in-variables attenuation, b_q −3.0 (t −0.7). HAR-CJ splits the continuous and jump parts; log-HAR introduced.
**Derivation.**
- $BV=\tfrac{\pi}{2}\sum|r_i||r_{i-1}|\to\int\sigma^2$, since $\mathbb E|z|=\sqrt{2/\pi}$ — a jump meets an $O(\sqrt{\Delta})$ neighbour, so it vanishes
- $RV-BV\to\sum_{s\le1}J_s^2$ — jump variation
- $z=\dfrac{(RV-BV)/RV}{\sqrt{(\tfrac{\pi^2}4+\pi-5)\tfrac1n\max(1,TQ/BV^2)}}\sim N(0,1)$ — BNS (2006) ratio test
- HAR ⇒ AR(22) weights $\phi_1=b_d+\tfrac{b_w}5+\tfrac{b_m}{22},\ \phi_{2..5}=\tfrac{b_w}5+\tfrac{b_m}{22},\ \phi_{6..22}=\tfrac{b_m}{22}$ — expand the averages
- $RV_t=IV_t+u_t,\ \operatorname{Var}u_t\approx2IQ_t/n$ ⇒ $b_{eff}=b\,\tfrac{\operatorname{Var}IV}{\operatorname{Var}IV+\operatorname{Var}u}$ ⇒ $b_{d,t}=b_d+b_q\sqrt{RQ_t}$ — attenuation (BPQ 2016)
**Experiment** `har` (rolling coefficients; HAR-CJ) and `realized` (BNS z). *(expected:* 10–20% of days with jumps at 1%.)
**Pause-and-predict.** "If yesterday's RV is very noisy, should HAR trust it more or less?" (Less, which is HARQ.)

### 11 · Is volatility rough? (2.0 min, ~280 words) — *new; item 9; Part 14 does the models*
**Goal.** The scaling m(q, Δ) ∝ Δ^{qH} measured on our own log RV; what H ≈ 0.1 means for forecasting.
**Beats.** Zoom into the log-vol path twice; it looks equally jagged at each scale (against a smooth H = 0.5
comparison). **Lab 6** `rough.log_rv_scaling` (12 lines) → run on simulated fBm with H = 0.1 and 0.5, recovering H,
then on BTC's 1,223 days: log m against log Δ, five parallel lines with slopes qH, and ζ_q against q a straight line.
The RFSV forecast formula is shown as a power-law kernel next to HAR's staircase: HAR is a cheap approximation
of it. Forward link to Part 14.
**Derivation.**
- $m(q,\Delta)=\langle|\log\sigma_{t+\Delta}-\log\sigma_t|^q\rangle\propto\Delta^{\zeta_q}$ — definition
- fBm: $\mathbb E|B^H_{t+\Delta}-B^H_t|^q=c_q\Delta^{qH}\Rightarrow\zeta_q=qH$ — self-similarity
- $\mathbb E[\log\sigma^2_{t+\Delta}\mid\mathcal F_t]=\tfrac{\cos H\pi}{\pi}\Delta^{H+\frac12}\!\int_{-\infty}^t\!\tfrac{\log\sigma_s^2\,ds}{(t-s+\Delta)(t-s)^{H+\frac12}}$ — GJR (2018) *(check the constant against the paper)*
**Experiment** `rough`. *(expected:* H ≈ 0.08–0.12, consistent with Part 14's 0.08 on 700 days and 0.12 de-weekended.)
**Pause-and-predict.** "If H = 0.5, what slope would the q = 2 line have?" (1.)

### 12 · Scoring forecasts honestly (3.0 min, ~420 words) — *new; item 6*
**Goal.** Why the target is noisy; Patton's robust losses (proved); MZ; DM; MCS; Hansen–Lunde.
**Beats.** Hansen–Lunde card (330 models; the DM/$ rate against IBM). **Signature:** a forecast slider ĥ with
expected-loss curves for QLIKE and MSE-on-vol against a *noisy proxy*. A second tracker turns the proxy noise up
(squared return → 5-min RV → "true" variance). QLIKE's minimum stays at the true h, while the MSE-on-volatility
minimum slides left. The narration states that this sliding is the proof. **Lab 7** `vol.qlike` + `diebold_mariano`
(11 lines). Simulation table (Patton experiment). MZ regression: forecast against realized, with the a = 0, b = 1
line. Model confidence set: models eliminated one by one.
**Derivation.**
- $L_Q(h,\hat h)=h/\hat h-\ln(h/\hat h)-1$; $\partial_{\hat h}\mathbb E[L\mid\mathcal F]=(\hat h-\mathbb E[h\mid\mathcal F])/\hat h^2$ — zero only at the conditional variance
- $\mathbb E[\tilde h\mid\mathcal F]=\mathbb E[h\mid\mathcal F]$ ⇒ an unbiased proxy adds a constant ⇒ rankings preserved — README problem 4
- MSE on vol: $\arg\min_{\hat\sigma}\mathbb E(\sqrt{\tilde h}-\hat\sigma)^2=\mathbb E\sqrt{\tilde h}<\sqrt{\mathbb E\tilde h}$ — Jensen: it rewards under-forecasts
- Patton family $L_b=\tfrac{h^{b+2}-\hat h^{b+2}}{(b+1)(b+2)}-\tfrac{\hat h^{b+1}(h-\hat h)}{b+1}$; $b=0$ MSE, $b=-2$ QLIKE — *(verify form against Patton 2011, eq. 24)*
- $d_t=L_{A,t}-L_{B,t},\ DM=\bar d/\sqrt{\widehat{LRV}/T}$ — Newey–West (Part 6)
**Experiment** `scoring` (new): GARCH-simulated truth, 10,000 days × 200 reps; forecasts = truth, truth × 0.8, truth
× 1.2, a 60-day moving average; proxies r², 78-obs RV and the truth. *(expected:* QLIKE and MSE-var rank the truth
first under every proxy; MSE-vol and MAE rank "truth × 0.8" first under the r² proxy.)
**Pause-and-predict.** "Judged against squared returns, which wins under MAE: the true variance or 80% of it?" (80%.)

### 13 · Training the networks (3.0 min, ~420 words) — *new; item 10a*
**Goal.** Watch an LSTM, a transformer and HARNet learn log RV; see seeds disagree; see HARNet start *at* HAR.
**Beats.** Architecture cards (LSTM gates in one line; attention over 22 days as a heat strip). **Replay**
(`ValueTracker`, as in ai21 `replay`): left, the train and validation loss curves for 5 seeds as a `band` with the
mean line; right, the H2 2019 validation window, with realized log RV dots and the network's forecast line morphing
at checkpoints (epochs 0, 5, 10, 20, 40, best). Early stopping marked per seed. **HARNet** (Reisenhofer–Bayer–
Hautsch 2022, dilated convolutions initialised to reproduce HAR exactly, trained on QLIKE): its first frame lies on
HAR's line, then drifts. Equal budgets are stated (epochs, parameters: LSTM 1,233; transformer 2,625; HARNet ~30).
The log-normal back-transform.
**Derivation.**
- LSTM: $c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t$ — a learned, data-dependent EWMA (link to 06's unrolled GARCH)
- attention $\operatorname{softmax}(QK^\top/\sqrt d)V$ over 22 lags — a learned, data-dependent HAR weighting
- $\mathbb E[RV]=\exp(m+s^2/2)$ for $\ln RV\sim N(m,s^2)$ — log-normal mean; without it log forecasts are biased low
- HARNet: dilations 1, 5, 22 with weights set to $1/5$, $1/22$ ⇒ HAR at initialisation — by construction
**Experiment** `race` extended: save checkpoints (loss per epoch, validation forecasts at 6 epochs) for every seed;
add HARNet × 5 seeds. *(+10 min.)*
**Pause-and-predict.** "Five seeds, same data, same architecture. Will they agree on 2020?" (No: the seed spread
.366–.378 is cached.)

### 14 · The race (3.0 min, ~420 words) — *rebuild s05*
**Goal.** The out-of-sample verdict, scored correctly, with the trial counter.
**Beats.** Calendar (cached 675/183/365). **Signature:** `LiveLeaderboard`. A cursor runs through 2020 day by day,
each model's cumulative mean QLIKE bar re-sorts live, and 12 March is a visible lurch. Final ranks keep the
cached narration branches: log-HAR .363 first; LSTM .371, with t +1.5 against log-HAR; the MSE order flips. HARNet
is inserted with branched narration. MZ coefficients and the MCS survivors are shown. The existing 2020 overlay
remains as the coda.
**Experiment** `race` (+HARNet, MZ, MCS). *(expected:* HARNet within noise of log-HAR. Branch: if DM t < −2 against
log-HAR, "the network found something beyond the log"; else "the log again".)
**Pause-and-predict.** "On MSE, which model do you expect to win: the smoothest or the most reactive?" (Cached: GJR.)

### 15 · Foundation models and the 2023–2026 frontier (3.5 min, ~490 words) — *new; item 11 + frontier*
**Goal.** What a time-series foundation model is; zero-shot on our test year; what the recent papers find.
**Beats.** **Signature:** Chronos's "language of numbers". The context window of log RV is mean-scaled, each value
snaps to one of 4,096 bins (a coloured ladder), and the series becomes a token strip. The model reads it, emits a
distribution over the next token, and a **quantile fan** grows a day ahead as the cursor walks 2020. Run zero-shot:
Chronos-Bolt (small), TimesFM 2.5, TTM-r2, and Moirai-small if `uni2ts` installs. All see the same 512-day
context of log RV, and none is trained by us. The bars join the leaderboard, with narration branched on the
result. Then the frontier cards (each checked on arXiv or the journal page, 2026-11-02):
- Christensen–Siggaard–Veliyev (2023, *JFEc* 21(5)): ML (RF, GBM, NN, regularised) against HAR on DJIA
  constituents' RV; ML improves one-day forecasts.
- Zhang–Zhang–Cucuringu–Qian (2022, arXiv 2202.08962): NNs pooled across stocks, with a market-vol feature,
  generalise to unseen stocks ("universal volatility mechanism"); arXiv working paper.
- Reisenhofer–Bayer–Hautsch (2022, arXiv 2205.07719): HARNet beats HAR on three indices; yesterday dominates the
  learned filter.
- Goel–Pasricha–Magris–Kanniainen (2025, arXiv 2505.11163): TimesFM is a reasonable baseline zero-shot;
  incremental fine-tuning is essential, and fine-tuned variants beat econometric models (DM, Giacomini–White).
- Brini (2026, arXiv 2607.05291): nine zero-shot TSFMs against eight econometric models on 50 assets (VOLARE).
  Per-asset loss ratios against log-HAR: only TTM beats it, narrowly. Mincer–Zarnowitz recalibration erases much
  of the short-horizon edge. The TTM + log-HAR average enters the MCS for 98–100% of assets.
- Rahimikia–Ni–Wang (2025, arXiv 2511.18578): off-the-shelf TSFMs underperform zero-shot on daily excess returns;
  finance-pretrained models (FinText) gain.
- Shi et al. (2025, arXiv 2508.02739; AAAI 2026 per the authors' README): Kronos, pretrained on 12 B+ K-line
  records from 45 exchanges; reports 9% lower MAE on volatility forecasting (the authors' own benchmark).
- Ekambaram et al. (2024, *NeurIPS*, arXiv 2401.03955): TTM, ~1M parameters, runs on CPU.
- Ansari et al. (2025, arXiv 2510.15821): Chronos-2, with group attention for multivariate and covariate
  forecasting.

The takeaway is narrated from our numbers *and* the literature: architecture matters more than "foundation against
econometric", and the log-HAR bar stands.
**Derivation.**
- Chronos: $\tilde x=x/s,\ s=\tfrac1C\sum|x_i|$; token $=\operatorname{bin}(\tilde x)$; train by cross-entropy — scaling + quantisation
- zero-shot: $\hat y_{t+1}=f_\theta(x_{t-C+1:t})$, $\theta$ frozen — no fitting on our data, so no look-ahead *except through pretraining corpora* (say this: pretraining data may include 2020 market series; flag as a leakage caveat *(unverified per model)*)
**Experiment** `foundation` (new, ≈10 min CPU; resumable per model; record HF model revision hashes in the cache).
*(expected:* no zero-shot model beats log-HAR on QLIKE with DM t < −2; TTM closest. Branch on the result.)
**Pause-and-predict.** "A model trained on electricity, traffic and weather, never on Bitcoin: better or worse than
four least-squares coefficients?"

### 16 · March 2020 (2.5 min, ~350 words) — *keep s06, trim*
Keep the crisis card, the forecast bars for 12 March (62–76% against 457%), and the Feb–Apr window, now drawn by a
running cursor. Keep the √T desk question with the GARCH term structure (85% → 52%, long run 18%). Add RiskMetrics'
own warning (TD 4e §5.2.2, verified): √T assumes constant variance; it is "nonsensical" for mean-reverting
or band-bounded rates (the NLG/DEM ERM chart). Add the regulatory consequence: the 1996 Basel market-risk amendment
let banks scale 1-day VaR to 10 days by √10 *(the BIS text, bcbs24, could not be retrieved; secondary sources agree
— mark (unverified) until read)*. Link to Part 40.
**Pause-and-predict.** "GARCH says 85% tomorrow. What does it say for the average over the next year?" (Cached: 52%.)

### 17 · Industry: how volatility is forecast for money (3.5 min, ~490 words) — *new*
**Goal.** What the risk vendors, CTAs and options desks actually run, from the public record, each with a computed
replica.
**Beats and facts (verified unless marked).**
1. **RiskMetrics** (J.P. Morgan; launched Oct 1994; Reuters partnership June 1996; TD 4e Dec 1996, preface).
   EWMA $\sigma^2_{t+1|t}=0.94\sigma^2_{t|t-1}+0.06r_t^2$ (eq. 5.23). One decay factor for the whole covariance
   matrix, 0.94 daily and 0.97 monthly, chosen by minimising variance-forecast RMSE across ~450–480 series (§5.3.2,
   Table 5.8, where US equity indices give 0.980). EWMA is IGARCH without intercept (§5.2, fn. 4). MSCI acquired
   RiskMetrics Group on 1 June 2010 for about $1.55 bn ([MSCI/SEC](https://www.sec.gov/Archives/edgar/data/1408198/000095010310001695/dp18031_ex9901.htm)).
   **Replica:** λ grid on the US market 1990–2020 under RMSE *and* QLIKE. *(expected:* RMSE-optimal λ ≈ 0.94–0.98;
   QLIKE-optimal different.)
2. **MSCI Barra USE4** (2011). It uses a *longer half-life for factor correlations than for volatilities*, "to
   ensure that the factor covariance matrix remains well-conditioned" ([MSCI, "Market Factor: Not Just For Show",
   Dec 2011](https://www.msci.com/documents/10199/ed6e42a3-c1fa-4430-89ba-efd5a5b52558)). The **Volatility Regime
   Adjustment** "calibrates factor volatilities to current market levels", reducing under-prediction entering
   high-vol regimes and over-prediction leaving them ([USE4 fact sheet](https://www.msci.com/documents/10199/242721/Barra_US_Equity_Model_USE4.pdf)).
   It scales "based on a time-series of cross-sectional factor bias statistics" (same Dec 2011 note). The exact
   formula and half-lives are in the USE4 Methodology Notes (Aug 2011), which could not be retrieved (403):
   formula *(unverified)* $B_t^2=\tfrac1K\sum_k(f_{kt}/\sigma_{kt})^2,\ \lambda_t^2=\text{EWMA}(B^2),\ \sigma'=\lambda\sigma$.
   **Replica:** VRA on French's 10 daily size deciles (cached), with λ_t spiking in 1987, 2008 and 2020.
3. **CTAs and volatility targeting (Man AHL).** Harvey, Hoyle, Korgaonkar, Rattray, Sargaison, Van Hemert (2018),
   *JPM* 45(1):14–33 ([PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf)). On
   60+ assets from 1926, scaled returns are $r_t\,\sigma^{target}/\sigma_{t-2}$ with a **10%** target. Vol is an
   EWMA of squared returns (the slowest uses a 90-day half-life; 270-day warm-up), plus 5-min intraday RV for S&P
   500 and 10y futures. Sharpe improves for risk assets (equities, credit) through the leverage effect, is
   negligible for bonds, FX and commodities, and left tails shrink everywhere. Moskowitz–Ooi–Pedersen (2012) TSMOM
   sizes by an EWMA with a **60-day centre of mass** (per replications; the 40% target per position is
   *(unverified)*). Moreira–Muir (2017) are the academic counterpart. **Replica:** vol-target French's market at 10%
   with σ_{t−2}; Sharpe and 1% mean shortfall, scaled against unscaled; the position-size bar breathes. *(expected:*
   higher Sharpe, smaller left tail.)
4. **Options desks.** Implied against forecast realized: the VIX (Cboe; 30-day model-free variance; record close
   82.69 on 16 Mar 2020) is regressed on next-month realized together with GARCH (MZ-style, Christensen–Prabhala
   1998 *(add)*). The variance risk premium VIX² − RV is positive on most days (Carr–Wu 2009, *RFS*). **Replica:**
   VIXCLS (cached) against French-market 21-day realized, 1990–2020. *(expected:* VIX above realized on ~80–90% of
   days *(computed)*.) Forward links to Parts 11–12.
5. **Academic infrastructure used by practitioners:** NYU Stern V-Lab (Engle's group) publishes daily volatility,
   correlation and systemic-risk forecasts ([vlab.stern.nyu.edu](https://vlab.stern.nyu.edu/)). AQR's
   Bollerslev–Hood–Huss–Pedersen (2018, *RFS*, "Risk everywhere") apply HAR-type RV models across asset classes.

Firm file card: RiskMetrics → RiskMetrics Group → MSCI (numbers above). Bloomberg's risk models are **not** used:
no public methodology found *(unverified; omit)*.
**Pause-and-predict.** "Why one λ for 480 series instead of 480 λs?" (A consistent, positive-definite covariance
matrix: TD §5.3.2.)

### 18 · The volatility forecaster (1.5 min, ~210 words) — *rebuild s07*
House chart; the module table grows by the new functions (below). **Lab 8**: `forecast(asset, horizon)` wraps
log-HAR + GARCH term structure (8 lines) → called live for BTC and the US market on 31 Dec 2020. Rule 8, and the
trial counter: the cached count plus HARNet (1) and the FMs (3–4), registered *before* running.

### 19 · Recap, desk questions, problems (2.5 min, ~350 words) — *update s08*
Recap 10 lines. Desk questions: keep 3, plus "α + β = 1: is the process stationary?" (strictly yes, Nelson). Problems:
keep 5, plus DF limit (02), Bandi–Russell n* (09), HARQ attenuation (10). Payoffs and references updated with §2c.

---

## 3b. Compute plan (about 100 CPU-minutes on 4 cores; seeded; each item cached and resumable)

| Item | New/ext | Content | Est. min |
|---|---|---|---|
| `daily` | — | BTC daily | <1 |
| `acf_arma` | new | ACFs of r, \|r\|, r² (24,896 d, 250 lags); Ljung–Box; ARMA(p,q≤3) on log VIX by CSS/MLE; AIC table | 5 |
| `unitroot` | new | 20,000 DF walks (vectorised, T = 500), streamed in 40 snapshots; ADF on 4 series | 2 |
| `spurious` | ext | + Phillips t-growth: T ∈ {50…2000} × 1,000 pairs | 2 |
| `coint` | ext | + ECM α's; Johansen trace (DTB3, DGS5 new fetch, DGS10); drunk–dog sim | 2 |
| `regimes` | ext | + EM checkpoints every 10 iters; monthly filter states for animation | 3 |
| `kalman` | new | local-level filter states (m, P⁻, P⁺, K per day); SV QML on 24,896 d (Nelder–Mead) | 6 |
| `garch` | ext | + optimiser callback path; logL grid 81² via `lfilter`; t-GARCH; Nelson boundary | 6 |
| `dcc` | ext | + yearly ellipses; EWMA correlation | 3 |
| `realized` | ext | + signature plot (9 Δ per day); per-day η²; BNS z | 15 |
| `har` | ext | + rolling 252-d coefficients; HAR-CJ; lag-weight staircase; ACF of log RV | 2 |
| `rough` | new | fBm (H = 0.1, 0.5) check; m(q,Δ) on 1,223 d | 2 |
| `scoring` | new | Patton simulation 200 reps; MZ; MCS on race forecasts | 4 |
| `race` | ext | + checkpoints per seed; HARNet × 5 seeds | 30 |
| `foundation` | new | Chronos-Bolt-small, TimesFM-2.5, TTM-r2, (Moirai-small) zero-shot, 365 forecasts each | 10 |
| `scaling` | — | √T vs GARCH | <1 |
| `industry` | new | RiskMetrics λ grid (RMSE, QLIKE); VRA on 10 size deciles; vol targeting 1927–2020; VIX VRP + MZ | 4 |
| `envelope` | ext | register HARNet + FMs before running | <1 |

Dependencies: `chronos-forecasting`, `timesfm`, `granite-tsfm`, and optionally `uni2ts`, in a `[quant7-fm]` extra.
Compatibility with the installed `transformers 5.20.1` and `torch 2.14.1` is *(unverified)*. Pin versions and
record weight hashes. `statsmodels` and `arch` are **not** installed: implement Johansen, Ljung–Box, ARMA-CSS, BNS
and MCS in `vol.py` (≈150 lines) with tests against simulations (tests/test_quant_house.py).

New House functions (`explainer/quant/house/vol.py`): `ljung_box`, `arma_fit`, `df_simulate`, `johansen`,
`ecm_fit`, `hamilton_filter` (exposed from `markov_switching`), `kalman_states`, `sv_qml`, `garch_t_fit`,
`news_impact`, `nelson_elog`, `signature_plot`, `bns_jump_z`, `har_cj`, `mincer_zarnowitz`,
`model_confidence_set`, `vol_target`, `vra`, `forecast`.

Scene files (caches are keyed by module name, so renamed modules re-render; compute caches are keyed by item and
survive): s00_hook, s01_arma, s02_unitroot, s03_coint, s04_regimes, s05_kalman, s06_garch, s07_zoo, s08_dcc,
s09_realized, s10_har, s11_rough, s12_scoring, s13_training, s14_race, s15_frontier, s16_march, s17_industry,
s18_house, s19_outro. Existing s01/s02/s03/s04/s05/s06/s07/s08 code moves into s00/s02–s03/s04+s06–s08/s09–s10/
s14/s16/s18/s19.

---

## 4. Industry and frontier sources
All URLs are given inline in chapters 15 and 17. Additional sources: the RiskMetrics TD 4e was read in full at the copy hosted by hpirotte.ulb.be; MSCI's page is gated at https://www.msci.com/research-and-insights/paper/1996-riskmetrics-technical-document. The MOP 60-day centre of mass is from a replication (https://nbviewer.jupyter.org/github/quantopian/research_public/blob/master/advanced_sample_analyses/TSMOM/TS%20MOM.ipynb); read the *JFE* paper before it goes on screen. The Basel 1996 amendment is at https://www.bis.org/publ/bcbs24.htm; its PDF was blocked by a bot check, so √10 is *(unverified)*. Frontier arXiv pages: https://arxiv.org/abs/2607.05291, https://arxiv.org/abs/2505.11163, https://arxiv.org/abs/2511.18578, https://arxiv.org/abs/2508.02739, https://arxiv.org/abs/2205.07719, https://arxiv.org/abs/2202.08962, https://arxiv.org/abs/2401.03955, https://arxiv.org/abs/2510.15821.

## 5. Revised SYLLABUS.md §6 entry (ready to paste)

```markdown
### Part 7 · Time Series and Volatility (~59)
1. Stationarity, ACF, ARMA, Box–Jenkins (Yule 1927; Box–Jenkins 1970; Ljung–Box 1978); log VIX identified.
2. Unit roots: the Dickey–Fuller distribution derived and simulated (1979); spurious regression (Granger–Newbold
   1974; Phillips 1986).
3. Cointegration: Engle–Granger (1987) and the error-correction model; Johansen (1991) on Treasury yields.
4. Hidden states: Hamilton's regime filter (1989) by EM; the Kalman filter (1960) and stochastic volatility by QML
   (Harvey–Ruiz–Shephard 1994).
5. ARCH (Engle 1982) and GARCH (Bollerslev 1986) by MLE; Nelson's stationarity (1990), QMLE (Bollerslev–Wooldridge
   1992), Student-t; EGARCH, GJR; DCC (Engle 2002).
6. Scoring forecasts: "does anything beat a GARCH(1,1)?" (Hansen–Lunde 2005); robust losses proved (Patton 2011);
   Mincer–Zarnowitz, Diebold–Mariano, the model confidence set.
7. Realized volatility (ABDL 2003; BNS 2002): the CLT, noise and the signature plot built, optimal sampling
   (Bandi–Russell 2008), two-scale and realized kernels.
8. HAR-RV (Corsi 2009) derived as a restricted AR(22); HARQ; jumps by bipower variation and the BNS test; HAR-CJ.
9. Roughness in the data: log realized vol at H ≈ 0.1 (Gatheral–Jaisson–Rosenbaum 2018), measured.
10. Deep volatility forecasting: an LSTM, a small transformer and HARNet against HAR, trained here and replayed.
11. Time-series foundation models (Chronos-Bolt, TimesFM, TTM, Moirai) zero-shot on volatility; the 2023–2026 papers.
12. Industry: RiskMetrics' EWMA, Barra's volatility regime adjustment, volatility targeting (Man AHL), implied
    against realized on the options desk.

*Textbooks:* Tsay *Analysis of Financial Time Series* ch. 1–5, 8, 10–11; Hamilton *Time Series Analysis* ch. 3–5,
13, 15–22; Brockwell–Davis *Introduction to Time Series and Forecasting*; Francq–Zakoian *GARCH Models*;
Aït-Sahalia–Jacod *High-Frequency Financial Econometrics* ch. 3, 6–7, 10; Andersen et al., "Volatility and
correlation forecasting" (*Handbook of Economic Forecasting*, 2006); CLM ch. 12; QRM ch. 4.
*Trained:* GARCH family (likelihood replay); HAR; LSTM, transformer and HARNet forecasters (5 seeds each, replayed);
foundation models zero-shot.
*Visuals:* clusters lighting up a century of returns; the GARCH leaky bucket; the Kalman belief as a moving
Gaussian; regime jars; the drunk and her dog; the yield cloud seen edge-on; QV as squares; the signature plot
built; the live 2020 leaderboard.
*Labs:* `ar_fit`, `adf`, `kalman_local_level`, `garch_filter`, `har_fit`, `log_rv_scaling`, `qlike`/`diebold_mariano`.
*Crisis:* March 2020: each model's forecast the day before.
*Industry:* RiskMetrics (1994–96 Technical Document); MSCI Barra USE4; Harvey et al. (2018); the VIX.
*Desk:* "Daily vol is 1%. What is the vol over a year? Over a week? When is √T wrong?"; "α + β = 1: stationary?"
*House:* the volatility forecaster.
```

## 6. Minutes
00 Hook + era 2.5 · 01 ARMA 3.5 · 02 Unit roots 3.5 · 03 Cointegration 3.5 · 04 Regimes 2.5 · 05 Kalman 3.0 · 06 GARCH 3.5 · 07 Zoo 3.0 · 08 DCC 2.5 · 09 Realized 3.5 · 10 Jumps+HAR 3.5 · 11 Rough 2.0 · 12 Scoring 3.0 · 13 Training 3.0 · 14 Race 3.0 · 15 Foundation models + frontier 3.5 · 16 March 2020 2.5 · 17 Industry 3.5 · 18 House 1.5 · 19 Outro 2.5 → **59.0 min** (≈ 8,200 narration words; gate `--floor 50` passes with 9 min of margin; if a chapter runs long, cut 08 and 11 toward 2.0 first).
