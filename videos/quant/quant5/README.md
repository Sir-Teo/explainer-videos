# Quant, Built — Part 5: Stochastic Calculus

Part 5 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act II, the Mathematical Toolkit. It assumes the gentle introduction in
[`videos/math/stochastic`](../../math/stochastic/), which covers Brownian motion, Itô's lemma and Black–Scholes.
From there it builds the working tools:

* quadratic variation measured on real prices;
* Itô against Stratonovich;
* numerical schemes with their orders computed;
* mean reversion fitted to Treasury bills, and Feynman–Kac;
* Girsanov as both theory and variance reduction, and martingale representation;
* local time, which resolves the stop-loss start-gain paradox;
* jumps and self-exciting jumps on Bitcoin;
* rough volatility and path signatures.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`sim`](../../../explainer/quant/house/sim.py) library) from public data: Binance's Bitcoin candles (one-minute and
one-hour) and FRED's Treasury bill and bond yields. Simulations are seeded and labeled on screen.

*An education in methods, not investment advice.*

## Chapters (about 45 minutes)

* **A hedge that cannot lose, and does.** Hold one share whenever the stock is above the strike, and none below. On
  4,000 simulated paths this "free" hedge of a call (K = 100, σ = 20%, one year) loses 7.90, 8.10, 7.98, 8.00 and
  7.94 at 13, 52, 252, 1,000 and 4,000 rebalances a year. That is the call's whole price, 7.97. Then the objectives,
  and the House's simulation library.
* **1. Brownian motion and quadratic variation.** Donsker's invariance principle. On one path, Σ|ΔW| grows like √n,
  Σ(ΔW)² → 1 and Σ|ΔW|³ → 0. Bitcoin's 2020 volatility from realized variance falls from 80% (one-minute sampling) to
  68–71% (hours to a day): the volatility signature plot, with subsampling over offsets.
* **2. The Itô integral and its numerics.** ∫W dW by left points converges to ½(W² − T) = −0.330 (−0.328 at 8,192
  steps). By midpoints in time it converges to ½W² = 0.170. Then the isometry and Itô's lemma. Euler–Maruyama and
  Milstein on GBM (μ = 5%, σ = 40%, 20,000 shared paths): strong orders 0.50 and 0.93, and weak orders 0.99 and 1.00,
  the weak ones computed exactly from second moments.
* **3. Mean reversion and Feynman–Kac.** On FRED's DTB3, monthly from 1954 to 2020:
  * Vasicek: κ = 0.099 (half-life 7 years), θ = 4.1%, σ = 1.4%. Simulated rates are below zero 12% of the time.
  * CIR: 2κθ/σ² = 0.58 < 1, so the rate can touch zero.
  * Feynman–Kac: the Vasicek bond formula from December 2020's bill rate (0.09%) gives a 10-year yield of 1.38%,
    against the actual 0.93% (FRED DGS10, 31 December 2020).
* **4. Girsanov and martingale representation.** Drift is a change of measure and volatility is not. A digital
  paying 1 above 160 (S₀ = 100, σ = 20%) has exact value 0.00714. Plain Monte Carlo gives 0.0074 ± 0.0006 (148 of
  20,000 paths pay). With Girsanov reweighting it gives 0.00707 ± 0.00008 (10,012 pay), a variance 52 times smaller.
  Martingale representation, and why a hedge exists (Clark–Ocone).
* **5. Local time: the paradox resolved.** Tanaka's formula, local time as occupation density, and Carr and Jarrow
  (1990). On the 4,000 paths, the hedge's shortfall and half the local time at K (estimated with ε = 0.5)
  correlate at 0.97, with mean 7.84 against the call's 7.97.
* **6. Jumps, and jumps that cause jumps.** Merton (1976), the Lévy–Itô decomposition, and Itô for jumps. Bitcoin
  hours, 2018–2020, scaled by weekly bipower variation: 204 beyond 5 sd (62, 78, 64 a year), against 0.015 expected
  for a Gaussian, carrying 24% of all variance. A Hawkes process fitted to the 229 hours with |r| above four times the
  past month's volatility: branching ratio 0.36 and half-life 7.6 hours, with log-likelihood −506 against −588 for
  a Poisson clock.
* **7. Beyond semimartingales.** Fractional Brownian motion (Mandelbrot and Van Ness 1968) at H = 0.1, 0.5 and 0.9,
  and arbitrage when prices follow it (Rogers 1997). Bitcoin's daily log volatility from 5-minute returns, 2019–2020
  (729 days): ζ_q is linear in q with H ≈ 0.15 (0.13–0.16 across q). The estimator recovers 0.10 and 0.48 on
  simulated fBM. Gatheral, Jaisson and Rosenbaum (2018). Then path signatures (Chen 1957, Lyons 1998): two paths with
  the same increments and Lévy areas of +½ and −½.
* **8. The simulation library.** Every routine is tested against a known answer, and Rule 6 says no desk prices with
  an untested simulator. The trial counter reads 12.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant5.compute                     # every number, cached in .cache/quant5/ (a few minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant5 LocalTime  # one chapter, silent, with a contact sheet
python tools/make.py quant5 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **E[W_t⁴].** W_t is N(0, t), and a Gaussian's fourth moment is 3σ⁴, so E[W_t⁴] = 3t². Alternatively, by Itô,
   d(W⁴) = 4W³dW + 6W²dt. Taking expectations, d/dt E[W⁴] = 6E[W²] = 6t, so E[W_t⁴] = 3t².
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
   close to the 12% of the simulation, which started from 1954's low rate.
5. **Hawkes.** In stationarity E[λ] = μ + (α/β)E[λ], so the rate is μ/(1 − α/β) = 0.1/(1 − 0.4) ≈ 0.167 a day. Each
   event triggers α/β = 0.4 children on average, so a fraction 0.4 of all events are triggered by earlier ones (the
   cluster size is 1/(1 − 0.4)).

## Data and reproducibility

* Binance BTCUSDT one-minute candles for 2019–2020 (24 monthly files, each checked against Binance's SHA-256), and
  one-hour candles for 2018–2020.
* FRED DTB3 (3-month bill), 1954–2020, and DGS10 (10-year yield), read for one date.
* Two tests registered with the trial counter: the Hawkes fit and the rough-volatility Hurst estimate. The one-minute
  data's hold-out (2021 onward) is not downloaded here, so it is unsealed; any later part that tests a strategy on it
  must seal it first.

---

# 量化金融，从零搭建 — 第5部分：随机微积分

本部分假定观众看过系列中的入门篇《随机微积分可视化》，在此基础上建立实用工具：用真实价格测量二次变差，伊藤与斯特拉托诺维奇积分，
计算出精度阶数的数值格式，拟合到国库券利率的均值回复与费曼–卡茨公式，作为理论与方差缩减工具的吉尔萨诺夫定理与鞅表示定理，
化解止损–启动悖论的局部时，比特币上的跳跃与自激跳跃，以及粗糙波动率与路径签名。所有数字都由本系列自己的代码根据公开数据算出。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **E[W_t⁴]。** W_t服从N(0, t)，高斯分布的四阶矩是3σ⁴，所以E[W_t⁴] = 3t²。或者用伊藤引理：d(W⁴) = 4W³dW + 6W²dt，取期望得
   d/dt E[W⁴] = 6t，所以E[W_t⁴] = 3t²。
2. **先碰到+1再碰到−2的概率。** W是鞅，在首次离开(−2, 1)时停止后有界；由可选停止，1·p − 2(1 − p) = 0，p = 2/3。
3. **用吉尔萨诺夫为数字期权定价。** 价格为e^{−rT} E_Q[1{S_T > K}]。在Q下log S_T = log S₀ + (r − σ²/2)T + σW̃_T，所以Q(S_T > K) = N(d₂)，
   价格为e^{−rT}N(d₂)。在P下同一事件的概率是把r换成μ的N(d₂)：漂移变了，波动率不变。

## 习题与解答

1. **变差。** 每个ΔW服从N(0, 1/n)：E|ΔW| = √(2/(πn))，所以E Σ|ΔW| = √(2n/π) → ∞；E(ΔW)² = 1/n、Var((ΔW)²) = 2/n²，
   所以Σ(ΔW)²的均值为1、方差为2/n → 0。
2. **∫W dW。** 左端点：Σ W_k ΔW_k = ½Σ(W²_{k+1} − W²_k) − ½Σ(ΔW_k)² → ½(W_T² − T)。时间中点：额外的和Σ(W_{k+½} − W_k)ΔW_k趋于½T，
   结果为½W_T²。只有伊藤积分½(W_T² − T)关于T是鞅：它对每个T的均值都是零。
3. **Milstein修正。** 一步之内，b(X_s) ≈ b(X_t) + b'b(X_t)(W_s − W_t)，所以∫b(X_s)dW_s ≈ bΔW + b'b∫(W_s − W_t)dW_s =
   bΔW + ½b'b(ΔW² − h)。
4. **Vasicek。** r_T是高斯的，均值θ + (r₀ − θ)e^{−κT}，方差σ²(1 − e^{−2κT})/(2κ)。长期分布为N(θ, σ²/2κ)：标准差0.014/√0.197 = 3.2%，
   P(r < 0) = N(−4.1/3.2) ≈ 10%，与模拟的12%接近（模拟从1954年的低利率出发）。
5. **Hawkes过程。** 平稳时E[λ] = μ + (α/β)E[λ]，所以长期速率为μ/(1 − α/β) = 0.1/0.6 ≈ 每天0.167次；每个事件平均触发α/β = 0.4个子事件，
   所以40%的事件由先前的事件触发。
