# Quant, Built — Part 7: Time Series and Volatility

Part 7 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act II, the Mathematical Toolkit. Returns are nearly unpredictable; their size is
not. This part builds the models that forecast it:

* stationarity, unit roots, spurious regression and cointegration;
* hidden states: Hamilton's regimes and the Kalman filter;
* ARCH, GARCH, GJR and EGARCH by maximum likelihood, and dynamic conditional correlation;
* realized volatility measured properly: microstructure noise, jumps, two-scale and kernel estimators;
* HAR and HARQ;
* an out-of-sample race between the classical models and two neural networks trained here;
* March 2020, and the square-root-of-time rule.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`vol`](../../../explainer/quant/house/vol.py) module, tested) from public data: Kenneth French's daily and monthly
market returns, FRED's 10-year Treasury yield, and Binance's one-minute, daily and perpetual-futures prices for
Bitcoin. Simulations are seeded and labeled on screen.

*An education in methods, not investment advice.*

## Chapters (about 40 minutes)

* **The river under the noise.** Bitcoin's daily returns, August 2017 to December 2020, and each day's realized
  volatility from five-minute returns. A Kalman filter on log volatility (signal-to-noise ratio 0.38) shows the slow
  hidden level beneath the noise. Then the objectives, and the House's volatility forecaster.
* **1. Unit roots, spurious regression, cointegration.** A stationary AR(1) next to a random walk; Box–Jenkins; the
  Dickey–Fuller test (Bitcoin's log price: t = 0.96). In 2,000 pairs of independent random walks, regressing one on
  the other in levels gives |t| > 1.96 in 89% of pairs (median R² 0.17); in differences, 5%. Bitcoin against the US
  market, 2017–2020: t = 24 and R² = 0.40 in log levels; t = 6.7 and R² = 0.05 in daily changes. Bitcoin's spot and
  its USD-M perpetual in 2020: each has a unit root (ADF t = 0.96 and 0.94), the Engle–Granger residual rejects one
  (t = −7.2 against a 5% critical value of −3.34), and the basis has a half-life of 1.2 days, with a −74 bp
  dislocation on 12 March. An independent walk against Bitcoin: t = −2.0, not cointegrated.
* **2. Hidden states and the GARCH family.** Hamilton's two-regime model on US monthly excess returns, 1926–2020:
  a calm regime (mean +12%, volatility 13%, lasting 55 months on average) and a turbulent one (−15%, 36%, 10
  months), turbulent in 14% of months. GARCH(1,1) on 24,896 days of the US market: α = 0.105, β = 0.884, persistence
  0.989, a shock's half-life of 63 trading days. GJR: γ = 0.111, so a fall raises tomorrow's variance about four
  times as much as a rise of the same size; log-likelihoods 84,088 (GARCH), 84,336 (GJR) and 84,342 (EGARCH).
  Bitcoin: GJR γ = 0.14, GARCH half-life 13 days. DCC (a = 0.029, b = 0.969) on stocks against 10-year Treasuries,
  1962–2020: the decade averages run +0.19, +0.26, +0.29, +0.27, then −0.33 in the 2000s and −0.46 in 2010–20.
* **3. Realized volatility and HAR.** Bitcoin's average volatility over 1,223 days: 106% from one-minute RV, 96%
  from five-minute RV, 93% by two-scale RV and by the realized kernel, and 92% by bipower variation; jumps are 10%
  of the variance. HAR on Bitcoin, 2017–2019 (836 days, Newey–West t): b_d = 0.41 (6.6), b_w = 0.03 (0.4),
  b_m = 0.43 (3.9), R² = 0.38. HARQ's b_q = −3.0 (t = −0.7): the right sign, not significant.
* **4. The race.** Hansen and Lunde (2005) raced 330 models: on the Deutschmark–dollar rate none beat
  GARCH(1,1), and on IBM stock models with leverage did. Our race used Bitcoin: fitted from August 2017 to June 2019
  (675 days), validated on the second half of 2019 (183 days, for the networks' early stopping) and tested on all of
  2020 (365 days). The task was one-step forecasts of the next day's five-minute realized variance, scored by QLIKE.
  The contestants were EWMA (RiskMetrics, λ = 0.94), GARCH, GJR, HAR, HARQ, an LSTM (1,233 parameters) and a
  one-layer transformer (2,625), both reading 22 days of log RV and each averaged over 5 seeds. After the first
  results we added a log-HAR, which made eight registered trials.
  * QLIKE, with the Diebold–Mariano t against HAR: log-HAR 0.363 (−3.3), LSTM 0.371 (−3.0), transformer 0.410
    (−0.8), HARQ 0.426 (0.0), HAR 0.427, GJR 0.444 (+0.6), GARCH 0.452 (+1.0) and EWMA 0.512 (+1.8).
  * The LSTM against log-HAR gives t = +1.5. The network's edge over HAR was the log transform.
  * The LSTM's seeds range from 0.366 to 0.378; the transformer's from 0.401 to 0.433.
  * On MSE the order changes: GJR is first and HARQ last.
* **5. March 2020.** The crisis file: on 12 March the US market fell 9.6% and Bitcoin 39.5%; on 16 March the
  market fell 12.0%, and the VIX closed at a record 82.69. Every model's forecast for 12 March, made on the 11th, lay between 62% and 76% (annualised); the day's
  realized volatility was 457%. Then the desk question: on 13 March 2020
  GARCH put the US market's next-day volatility at 85% a year; the square-root rule carries that forward, while
  GARCH's average over the coming year is 52%, mean-reverting toward 18%.
* **6. The volatility forecaster.** Rule 8: every forecast is scored out of sample, against a simple benchmark, with
  a loss that is robust to noise in what it is judged against. The race was registered, including the model added after the
  first look; the trial counter reads 71.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant7.compute                    # every number, cached in .cache/quant7/ (minutes; downloads one-minute data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant7 Race     # one chapter, silent, with a contact sheet
python tools/make.py quant7 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

The networks are small (1,233 and 2,625 parameters) and train on a CPU in minutes. Training uses one thread on
purpose: with the renders running, PyTorch's default thread pool was measured forty times slower.

## Desk questions, with solutions

1. **Daily volatility is 1%.** With independent returns and constant variance, variances add: over a week
   1% × √5 ≈ 2.2%, over a year 1% × √252 ≈ 15.9%. The rule fails in three ways. Volatility mean-reverts, so from a
   high level the average over a horizon is lower than today's level (GARCH: E_t[σ²_{t+h}] = σ̄² +
   (α + β)^{h−1}(σ²_{t+1} − σ̄²)); chapter 5 shows 85% falling to 52% over a year. Autocorrelated returns change the
   sum's variance by the factor 1 + 2Σ(1 − k/h)ρ_k (Lo–MacKinlay's variance ratio). And quantiles of fat-tailed
   returns do not scale by √T, because the sum of fat-tailed returns is closer to normal than each one.
2. **A t of 24 between two prices.** First check both series for unit roots (ADF). If both have one, the t-statistic
   is meaningless (chapter 1: 89% false rejections). Test the residual of the levels regression for a unit root with
   Engle–Granger critical values (about −3.34 at 5% for two series, not −2.86), or regress changes on changes.
3. **A model beats GARCH on MSE over a year with a crash in it.** Squared errors of variance forecasts are dominated
   by the largest days, so one day can decide the race. Score with QLIKE, which is robust to noise in the realized
   proxy (Patton 2011), compare against HAR rather than a weak benchmark, use a Diebold–Mariano test with a HAC
   variance, and check that the ranking survives without the crisis weeks.

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
3. **Noise in realized variance.** If observed log prices are p_i = p*_i + u_i with iid noise of variance η², then
   observed returns are r_i = r*_i + u_i − u_{i−1}. With n returns, E[Σr_i²] = ∫σ²dt + 2nη², so the bias grows
   with the sampling frequency, which is the signature plot. Two-scale RV averages the RV of K sparse sub-grids, each
   with bias 2n̄η² where n̄ ≈ n/K. It estimates η² from the dense grid as RV_all/(2n) and subtracts (n̄/n)RV_all.
   That removes the bias, and the estimator converges at rate n^{−1/6} (Zhang, Mykland and Aït-Sahalia 2005).
4. **QLIKE.** E[h/ĥ − log(h/ĥ) − 1 | F] = E[h|F]/ĥ + log ĥ − E[log h | F] − 1. Its derivative in ĥ is
   −E[h|F]/ĥ² + 1/ĥ, which is zero only at ĥ = E[h|F], and the function is convex there. The loss depends on h
   only through E[h|F] plus a term free of ĥ. So replacing the true variance h by an unbiased proxy (E[h̃|F] = E[h|F]) adds the
   same constant to every forecast's expected loss, and the ranking is preserved. Patton (2011) shows that MSE and
   QLIKE belong to the family with this property, and that losses on volatility (rather than variance), or on
   absolute errors, do not.
5. **The Kalman gain.** For x_t = x_{t−1} + w_t and y_t = x_t + v_t, with variances Q and R, the filter predicts
   P⁻ = P + Q, uses the gain K = P⁻/(P⁻ + R), and updates P = (1 − K)P⁻. In steady state KP⁻ = Q, and P⁻ solves
   P⁻² − QP⁻ − QR = 0. Dividing by R² and writing q = Q/R gives p = P⁻/R = (q + √(q² + 4q))/2 and K = p/(p + 1),
   a function of q alone. For the hook's q = 0.38, K ≈ 0.45: each new day moves the filtered volatility a little
   under halfway toward what was measured.

## Data and reproducibility

* Binance (data.binance.vision): BTCUSDT one-minute and daily spot candles, August 2017 to December 2020, and the
  USD-M perpetual's daily closes for 2020. Every downloaded file is checksummed in
  [`../data/manifest.json`](../data/manifest.json).
* Kenneth French's daily market return, 1926–2020, and monthly excess returns; FRED DGS10 for the bond return
  (carry minus 8 × the yield change). The hold-out from 2021 is sealed.
* Registered with the trial counter: the forecasting race, 8 models. Seven were planned; log-HAR was added after
  the first results and is counted.
* Deferred to the production build: the syllabus's zero-shot time-series foundation models (Chronos, TimesFM,
  Moirai), which need packages this build environment does not yet carry.

---

# 量化金融，从零搭建 — 第7部分：时间序列与波动率

收益几乎无法预测，但收益的大小可以。本部分搭建预测它的模型：平稳性、单位根、伪回归与协整；隐藏状态（汉密尔顿的机制转换与卡尔曼滤波）；
用最大似然估计的ARCH、GARCH、GJR与EGARCH，以及动态条件相关；正确测量的已实现波动率（微观结构噪声、跳跃、双尺度与核估计量）；HAR与HARQ；
经典模型与在这里训练的两个神经网络之间的样本外竞赛；以及2020年3月和时间平方根法则。所有数字都由本系列自己的代码根据公开数据算出。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **日波动率为1%。** 若收益独立且方差恒定，方差可加：一周1% × √5 ≈ 2.2%，一年1% × √252 ≈ 15.9%。这个法则有三种失效方式。
   第一，波动率均值回归，从高位出发，一段期限内的平均低于今天的水平（GARCH：E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²)），
   第5章中85%在一年里降到52%。第二，收益自相关时，总和的方差会乘以1 + 2Σ(1 − k/h)ρ_k（Lo–MacKinlay方差比）。第三，厚尾收益的分位数不按√T缩放，
   因为厚尾收益之和比单个收益更接近正态。
2. **两个价格之间t = 24。** 先检验两个序列有没有单位根（ADF）。如果都有，这个t统计量没有意义（第1章：89%的错误拒绝）。
   对水平回归的残差做单位根检验，用恩格尔–格兰杰临界值（两个序列时5%水平约−3.34，而不是−2.86），或者用变化量对变化量回归。
3. **一个模型在包含崩盘的一年里按MSE胜过GARCH。** 方差预测的平方误差由最大的几天主导，一天就可能决定胜负。应当用QLIKE评分，
   它对已实现代理变量中的噪声稳健（Patton 2011）；对比HAR而不是弱基准；用带HAC方差的Diebold–Mariano检验；并检查去掉危机几周后排名是否依然成立。

## 习题与解答

1. **GARCH的期限结构。** 记σ̄² = ω/(1 − α − β)。由于E_t[r²_{t+k}] = E_t[σ²_{t+k}]，对σ²_{t+k+1} − σ̄² = α(r²_{t+k} − σ̄²) + β(σ²_{t+k} − σ̄²)
   取期望，得E_t[σ²_{t+k+1}] − σ̄² = (α + β)(E_t[σ²_{t+k}] − σ̄²)，归纳得E_t[σ²_{t+h}] = σ̄² + (α + β)^{h−1}(σ²_{t+1} − σ̄²)。
   冲击在log 0.5/log(α + β)天后减半：美国市场的0.989对应63天。
2. **GARCH即ARMA，及其峰度。** 令ν_t = r_t² − σ_t²，它是鞅差。把σ_t² = r_t² − ν_t代入GARCH递推，得r_t² = ω + (α + β)r²_{t−1} + ν_t − βν_{t−1}：
   自回归根为α + β的ARMA(1, 1)。正态冲击下E[r⁴] = 3E[σ⁴]。对递推式平方取期望得E[σ⁴](1 − (α + β)² − 2α²) = ω² + 2ωσ̄²(α + β)，
   峰度为3(1 − (α + β)²)/(1 − (α + β)² − 2α²)。只要α > 0它就大于3，且仅当(α + β)² + 2α² < 1时有限。
3. **已实现方差中的噪声。** 若观测到的对数价格为p_i = p*_i + u_i，噪声独立同分布、方差η²，则观测收益为r_i = r*_i + u_i − u_{i−1}。
   有n个收益时E[Σr_i²] = ∫σ²dt + 2nη²，偏差随采样频率增长，这就是签名图。双尺度RV对K个稀疏子网格的RV取平均，每个的偏差为2n̄η²，
   其中n̄ ≈ n/K。它用稠密网格估计η² = RV_all/(2n)，再减去(n̄/n)RV_all，消除偏差，估计量以n^{−1/6}的速度收敛（Zhang、Mykland与Aït-Sahalia 2005）。
4. **QLIKE。** E[h/ĥ − log(h/ĥ) − 1 | F] = E[h|F]/ĥ + log ĥ − E[log h | F] − 1。对ĥ的导数为−E[h|F]/ĥ² + 1/ĥ，只在ĥ = E[h|F]处为零，
   且函数在那里是凸的。损失只通过E[h|F]依赖于h，另加一项与ĥ无关的量。所以用无偏代理（E[h̃|F] = E[h|F]）替换真实方差h，
   只会给每个预测的期望损失加上同一个常数，排名保持不变。Patton（2011）证明MSE和QLIKE属于具有这一性质的族，而对波动率（而非方差）的损失或绝对误差则不具备。
5. **卡尔曼增益。** 对x_t = x_{t−1} + w_t、y_t = x_t + v_t，方差分别为Q与R，滤波器先预测P⁻ = P + Q，用增益K = P⁻/(P⁻ + R)，
   再更新P = (1 − K)P⁻。稳态时KP⁻ = Q，且P⁻满足P⁻² − QP⁻ − QR = 0。除以R²并记q = Q/R，得p = P⁻/R = (q + √(q² + 4q))/2，
   K = p/(p + 1)，只是q的函数。开场的q = 0.38给出K ≈ 0.45：每个新的一天，把滤波后的波动率向测量值移动不到一半。
