# Quant, Built — Part 13: Stochastic Volatility and Jumps

Part 13 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It covers:

* why volatility must move: the vol of vol, the leverage effect, and the skew after 1987;
* Heston's model, its characteristic function, Feller's condition, and Andersen's QE scheme;
* SABR: Hagan's formula, the backbone, and its arbitrage at long maturities;
* jumps and Lévy models: Merton, Kou, Bates, variance gamma, NIG, CGMY, and time changes;
* stochastic local volatility by the particle method;
* Bergomi's forward variance curves;
* the forward smile, cliquets and model risk, and the SPX/VIX puzzle;
* calibration: the loss landscape and parameter instability.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`stochvol`](../../../explainer/quant/house/stochvol.py) calibrator, tested). The data are Deribit's trades (the
Surface and 100 weekly surfaces), Binance's BTCUSDT (daily and hourly) and Deribit's DVOL.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **The second river.** DVOL from 2021 to 2025, with its floods: Terra–Luna, FTX, and August 2024. Five models are
  fitted to the same options and price one cliquet 8% apart. Then the objectives, and the calibrator.
* **1. Why volatility must move.**
  * 30-day realized volatility ranged from 17% to 122%, and the vol of vol (DVOL's own) is 89% a year.
  * On days Bitcoin fell more than 5%, DVOL rose 6.4% on average; on days it rose that much, DVOL rose 0.5%.
  * The return/DVOL correlation is −0.23 overall: −0.58 in 2022, but +0.30 in 2023's rally.
  * The 1987 crash and the skew since (Rubinstein 1994; Bates 2000).
  * Hull–White (1987): random volatility makes a smile, and correlation tilts it.
* **2. Heston's model.**
  * The Riccati characteristic function, priced by COS (Fang–Oosterlee 2008), reproduces their benchmark to 10⁻⁸.
  * Fitted to the Surface's 193 quotes, it misses by 1.33 vol points, against 3.89 for one Black–Scholes vol.
  * The fit needs κ = 14.8, ξ = 4.6 and ρ = −0.31. Feller's ratio 2κθ/ξ² is 0.37.
  * The 3-day expiry is still missed by 5.3 points.
  * Pricing a 3-month ATM call by Monte Carlo: Euler with 2 steps is 20% too high, Andersen's QE scheme 1% too low;
    from 16 steps QE is inside the noise.
* **3. SABR.**
  * Hagan et al. (2002), fitted slice by slice (β = 1): 0.38 vol points, with 27 parameters.
  * The vol of vol each slice needs falls like T^−0.49.
  * The backbone (β), and Part 12's sticky test.
  * Hagan's density at 10 years for a rates-like smile is negative below a 0.7% strike and integrates to 0.63.
  * The fixes: arbitrage-free SABR (2014) and Antonov–Konikov–Spector.
* **4. Jumps and Lévy models.**
  * Merton, Kou, Bates; variance gamma, NIG, CGMY; Carr–Wu time changes.
  * Fits: variance gamma 2.89 vol points, NIG 2.70, Bates 1.31. Bates's jumps went to the bound (20 a year, −4%
    each), a second diffusion: the Surface priced no crash.
  * The market's ATM skew grows like T^−0.49 as expiry nears. Heston's flattens and the Lévy models' explode like
    1/T: the doorway to Part 14.
* **5. Stochastic local volatility.**
  * Leverage times Heston, made consistent by Gyöngy and calibrated by the particle method (Guyon–Henry-Labordère
    2012).
  * The leverage function by date.
  * It reprices the Surface's smile to 0.68 vol points at 30 days and 0.44 at 120.
* **6. Forward variance as the state.**
  * The Surface's forward variance curve, from variance-swap strikes. Saturday 13 to Sunday 14 December is priced at
    32% volatility, against about 50% on either side.
  * Bitcoin's Saturdays realized 29% in 2024–2025, against 54% on weekdays.
  * Heston's single exponential. Bergomi's two-factor variance curve model.
* **7. The forward smile, and model risk.**
  * 30-day smiles 60 days ahead: local vol flattens the skew to 3.4 points, against 6.5 today. Heston keeps 6.1,
    Bates 6.3; variance gamma 5.0 and SLV 5.1.
  * A cliquet (four monthly returns, floored at 0 and capped at 10%) costs 13.1–14.2% across the five models, 8%
    apart. A forward-start ATM call is 11% apart.
  * The SPX/VIX puzzle: Gatheral (2008), and Guyon (2020).
* **8. Calibration.**
  * Heston's loss over (κ, ξ) is a long, curved valley: at κ = 5 instead of 15 the error rises only from 1.30 to
    1.43. Twelve random starts all reach the same minimum.
  * Refitted to 100 weekly surfaces, κ moves 25% a typical week and sits at its bound in 20% of weeks.
  * Feller fails in 91% of weeks, and ρ > 0 in 54%, with call-side smiles.
  * Regularization (Cont–Tankov 2004).
* **9. The calibrator.** Rule 13: every model is fitted by the calibrator, which logs its error and its parameter
  drift. Every exotic is priced under at least two models fitted to the same surface, and the spread is reported as
  model risk. No strategy was tested; the trial counter stays at 73.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant13.compute                   # every number (a few minutes; the weekly fits ~3 min)
EXPLAINER_TTS=silent python tools/qa_scene.py quant13 Heston  # one chapter, silent, with a contact sheet
python tools/make.py quant13 --cpu-voice -q m            # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **In Heston, what sets the skew? And the curvature?**
   * The correlation ρ sets the skew, scaled by the vol of vol. At short maturity the ATM slope is about ρξ/(4√v₀).
     On the Surface's fit that is −0.73, and the model gives −0.74 at two days.
   * The curvature comes from ξ².
   * Mean reversion κ flattens both as maturity grows.
2. **Local vol and a stochastic vol model both fit today's surface. You must price a cliquet.**
   * Not local vol alone: a cliquet is a bet on future smiles, and local vol flattens them (3.4 points against 6.5
     here).
   * Use a stochastic or stochastic-local model with a stated mixing fraction, and report the spread across models
     (8% here) as model risk.
3. **Overnight, Heston's κ jumped from 3 to 20 and the fit barely moved.**
   * You moved along the valley. The quotes pin a combination of κ and ξ, so vanilla prices hardly change.
   * Exotics and hedges depend on each parameter separately. Regularize toward yesterday's values, and judge the
     model by its hedge P&L.

## Problems, with solutions

1. **Heston's Riccati equations.**
   * Write x = ln S and τ = T − t. The price of a claim on x_T solves
     ∂_τ f = ½v(f_xx − f_x) + ρξv f_xv + ½ξ²v f_vv + κ(θ − v)f_v.
   * Substituting f = exp(C(τ) + D(τ)v + iux) and collecting the terms in v gives
     D′ = ½ξ²D² − (κ − ρξiu)D − ½(u² + iu), with D(0) = 0.
   * The terms without v give C′ = κθD, with C(0) = 0.
   * The solution is the little-trap form used in the House: d = √((κ − ρξiu)² + ξ²(iu + u²)).
2. **The short-maturity skew.**
   * As T → 0, the implied variance at log-moneyness k is the local variance averaged along the straight line to k
     (Berestycki–Busca–Florent). The local variance is E[v | S]. Over a short time v − v₀ ≈ ξ√v₀W², and
     x ≈ √v₀W¹, so E[v | x] ≈ v₀ + ρξx.
   * Averaging along the line gives σ²_imp(k) ≈ v₀ + (ρξ/2)k, and hence ∂_kσ_imp = (ρξ/2)/(2√v₀) = ρξ/(4√v₀).
3. **The Lévy forward smile.**
   * The forward-start payoff (S_{t+τ}/S_t − e^k)⁺ depends only on the increment X_{t+τ} − X_t.
   * For a Lévy process that increment has the law of X_τ and is independent of the past.
   * So the price equals today's τ-option at the same moneyness, and the forward smile is today's smile.
4. **Feller's condition.**
   * The scale density of CIR is s′(v) = v^{−2κθ/ξ²}·e^{2κv/ξ²}.
   * Zero is reached exactly when ∫₀ s′(v)dv < ∞, that is, when 2κθ/ξ² < 1.
5. **Why the leverage function works.**
   * The density p(S, t) of dS/S = L√v dW solves ∂_t p = ½∂_SS(S²L² E[v | S] p) (Gyöngy's mimicking theorem).
   * That is Dupire's forward equation exactly when L²E[v | S] = σ²_loc.
   * The two models then share every marginal, and so every vanilla price.

## Data and reproducibility

* The Surface: Deribit BTC option trades on 10 December 2025 (193 quotes, expiries from 3 to 289 days).
* Weekly surfaces: every Wednesday from 3 January 2024 to 26 November 2025 (100 days), as in Part 12.
* Binance BTCUSDT daily (2021-04 to 2025-11) and hourly (2024-2025); Deribit DVOL daily.
* No strategy was tested; the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第13部分：随机波动率与跳跃

本部分讲：

* 波动率为什么必须变动：波动率的波动率、杠杆效应，以及1987年以后的偏斜；
* 赫斯顿模型、它的特征函数、费勒条件和安德森的QE格式；
* SABR：哈根公式、骨架，以及它在长期限处的套利；
* 跳跃与莱维模型：默顿、寇、贝茨、方差伽马、NIG、CGMY，以及时间变换；
* 用粒子方法实现的随机局部波动率；
* 贝尔戈米的远期方差曲线；
* 远期微笑、棘轮期权与模型风险，以及SPX/VIX难题；
* 校准：损失地形与参数的不稳定。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **在赫斯顿模型里，什么决定偏斜？曲率呢？**
   * 相关系数ρ决定偏斜，并由波动率的波动率放大：短期限时平值斜率约为ρξ/(4√v₀)。在曲面的拟合上这是−0.73，模型在两天期给出−0.74。
   * 曲率来自ξ²。
   * 均值回复κ让两者随期限变平。
2. **局部波动率和一个随机波动率模型都拟合今天的曲面，你要给棘轮期权定价。**
   * 不能只用局部波动率：棘轮期权押注的是未来的微笑，而局部波动率把它压平（这里为3.4点，今天为6.5点）。
   * 用随机或随机局部波动率模型，并说明混合比例；把各模型之间的差距（这里8%）作为模型风险报告。
3. **一夜之间，赫斯顿的κ从3跳到20，拟合几乎没变。**
   * 你沿着山谷走了一段。报价只确定κ与ξ的一个组合，所以香草期权价格几乎不变。
   * 奇异期权和对冲分别依赖每个参数。要向昨天的值正则化，并用对冲损益来评判模型。

## 习题与解答

1. **赫斯顿的里卡蒂方程。**
   * 记x = ln S，τ = T − t。关于x_T的权益价格满足∂_τ f = ½v(f_xx − f_x) + ρξv f_xv + ½ξ²v f_vv + κ(θ − v)f_v。
   * 代入f = exp(C(τ) + D(τ)v + iux)，收集含v的项得D′ = ½ξ²D² − (κ − ρξiu)D − ½(u² + iu)，D(0) = 0。
   * 不含v的项给出C′ = κθD，C(0) = 0。
   * 其解就是公司使用的“小陷阱”形式：d = √((κ − ρξiu)² + ξ²(iu + u²))。
2. **短期限偏斜。**
   * 当T → 0时，对数价值状态k处的隐含方差是沿直线到k的局部方差的平均（Berestycki–Busca–Florent）。局部方差是E[v | S]；短时间内v − v₀ ≈ ξ√v₀W²，x ≈ √v₀W¹，所以E[v | x] ≈ v₀ + ρξx。
   * 沿直线平均得σ²_imp(k) ≈ v₀ + (ρξ/2)k，从而∂_kσ_imp = (ρξ/2)/(2√v₀) = ρξ/(4√v₀)。
3. **莱维模型的远期微笑。**
   * 远期起始收益(S_{t+τ}/S_t − e^k)⁺只依赖增量X_{t+τ} − X_t。
   * 对莱维过程，这个增量与X_τ同分布，且独立于过去。
   * 所以价格等于今天同一价值状态的τ期期权，远期微笑就是今天的微笑。
4. **费勒条件。**
   * CIR的尺度密度为s′(v) = v^{−2κθ/ξ²}·e^{2κv/ξ²}。
   * 当且仅当∫₀ s′(v)dv < ∞，即2κθ/ξ² < 1时，零点可达。
5. **杠杆函数为什么有效。**
   * dS/S = L√v dW的密度p(S, t)满足∂_t p = ½∂_SS(S²L² E[v | S] p)（久永的模仿定理）。
   * 当L²E[v | S] = σ²_loc时，这正是杜皮尔的前向方程。
   * 于是两个模型的每个边际分布都相同，每个香草期权价格也都相同。
