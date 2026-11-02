# Quant, Built — Part 14: Rough and Path-Dependent Volatility

Part 14 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It is the series' frontier part on volatility. It covers:

* the exploding at-the-money skew, and the power law against a bounded alternative;
* the Gatheral–Jaisson–Rosenbaum roughness estimator, run on Bitcoin;
* rough Bergomi (hybrid scheme) and rough Heston (fractional Adams), calibrated to the Surface;
* where roughness may come from: nearly unstable Hawkes order flow;
* Markovian lifts;
* the debate over whether volatility is rough at all;
* Guyon–Lekeufack path-dependent volatility, fitted to DVOL out of sample;
* the frontier: quadratic rough Heston, Guyon's joint SPX/VIX fit, signature models, and neural calibration.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`rough`](../../../explainer/quant/house/rough.py) module, tested). The data are the Surface (Deribit trades),
Binance's BTCUSDT (5-minute, 2024–2025; daily since 2018) and Deribit's DVOL.

*An education in methods, not investment advice.*

## Chapters (about 60 minutes)

* **Rough.** A Brownian path and an H = 0.1 path, zoomed 16 and 256 times. Then the objectives, and the rough lab.
* **1. The fact: an exploding skew.**
  * The Surface's ATM skew follows T^−0.49 as a power law, which implies H ≈ 0.01 (Alòs–León–Vives 2007; Fukasawa
    2011).
  * A bounded form, (T + 21 days)^−0.88, fits better (log error 0.19 against 0.23), as Guyon and El Amrani (2023)
    argue for the S&P 500.
  * What a Volterra kernel and Δ^H mean.
* **2. Volatility is rough.**
  * Bitcoin's daily log realized variance (5-minute returns, 700 days) gives m(q, Δ) ∝ Δ^{qH} with H = 0.08. Once
    the weekly pattern of calm weekends is removed, H = 0.12.
  * The estimator, run on fBm, recovers H = 0.1, 0.3 and 0.5 closely. It reads a true 0.05 as 0.01.
* **3. Rough Bergomi.**
  * Bayer–Friz–Gatheral (2016), simulated by the Bennedsen–Lunde–Pakkanen hybrid scheme, with Part 13's forward
    variance curve.
  * Calibrated on 20,000 paths and re-priced on fresh ones: H = 0.03, η = 2.0, ρ = −0.56.
  * Error 0.83 vol points on the 175 quotes up to 200 days, against 1.37 for Part 13's Heston on the same quotes.
* **4. Rough Heston.**
  * El Euch–Rosenbaum (2019): the fractional Riccati equation, solved by Adams, with COS prices; it reduces to
    Heston at H = ½, and the tests check this.
  * Left free on the Surface, it chooses H = 0.45, with Heston's extreme ν = 4.5 and λ = 16: error 1.28.
  * Held at H = 0.1, its error is 1.49, with ν = 1.0 and λ = 2.0. At H = 0.2 the error is 1.41; at 0.05, 2.25.
  * Skew term structure: rough Bergomi follows the quotes from 4 to 200 days but misses the 3-day point. The rough
    Hestons reach that point and overshoot the days just after it.
* **5. Where roughness comes from.**
  * Hawkes order flow at branching ratios 0.5, 0.9 and 0.99.
  * Jaisson–Rosenbaum (2016) and El Euch–Fukasawa–Rosenbaum (2018): nearly unstable Hawkes processes become rough
    Heston at a distance.
* **6. Markovian lifts.** Abi Jaber–El Euch (2019): the kernel as a sum of N exponentials, and the 30-day smile's
  error falls from 4.7 vol points (one factor) to 1.1 (ten), 0.57 (twenty) and 0.26 (fifty), against rough
  Heston with H = 0.1.
* **7. The debate.**
  * The weekend trap: Saturday's typical realized volatility is about half a weekday's.
  * Three smooth (H = ½) volatilities, as variable as Bitcoin's and measured the same way:
    * one factor with a 10-day half-life reads H = 0.38;
    * two factors (1 and 60 days) read 0.42;
    * one factor with a 5-hour half-life reads 0.02.
  * Cont–Das (2024), Guyon–El Amrani (2023).
* **8. Path-dependent volatility.**
  * Guyon–Lekeufack (2023): σ = β₀ + β₁R₁ + β₂√R₂, with time-shifted power-law kernels. Bitcoin's returns since
    2018 are used to fit DVOL on 2021–2023.
  * R² is 0.88 in sample and 0.42 out of sample (2024–2025). A line in the past 30 days' realized vol scores 0.68
    and −0.27.
  * The activity term moves implied vol by 18.7 points (one standard deviation), the trend term by 0.9: Bitcoin's
    implied vol cares how much it moved, hardly which way.
* **9. The frontier, and what desks use.**
  * Quadratic rough Heston (Gatheral–Jusselin–Rosenbaum 2020).
  * Guyon's dispersion-constrained martingale Schrödinger problem (2022).
  * Signature volatility (Cuchiero–Gazzetta–Svaluto-Ferro 2023).
  * Deep-learning calibration (Horvath–Muguruza–Tomas 2021).
* **10. The rough lab.** Rule 14: a new model is adopted only if it beats the simpler one out of sample, on the
  quantity it is meant for, with its estimator checked on synthetic data whose answer is known. The trial counter
  stays at 73.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant14.compute                    # every number (rough Heston fits take ~1 hour on 4 cores)
EXPLAINER_TTS=silent python tools/qa_scene.py quant14 Rough   # one chapter, silent, with a contact sheet
python tools/make.py quant14 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **With H ≈ 0.1, a one-day option against a one-month one?**
   * The ATM skew scales like T^{H−½}, so (1/30)^{−0.4} ≈ 3.9: the one-day skew is about four times the one-month.
   * Volatility itself moves by about Δ^H over Δ, so short-dated options carry most of the vol-of-vol exposure.
2. **Roughness or fast mean reversion?** Use several measurements:
   * the scaling of realized variance at sub-daily lags, after removing intraday and weekly seasonality and
     correcting for microstructure noise;
   * the skew's term structure at the shortest expiries;
   * out-of-sample forecasts and hedges, rough against multi-factor.
   Any one can be fooled, as chapter 7 shows.
3. **Calibrating in milliseconds.** The options:
   * a neural surrogate trained once on the model's prices (Horvath–Muguruza–Tomas 2021);
   * a Markovian lift with a few factors and a closed-form Riccati system;
   * rough Heston's Fourier form with a coarse Adams grid.
   Then check the surrogate against the full model regularly.

## Problems, with solutions

1. **Variance of W^H.** By the Itô isometry, Var W^H_t = 2H ∫₀ᵗ (t − s)^{2H−1} ds = 2H · t^{2H}/(2H) = t^{2H}.
2. **Scaling.**
   * fBm has stationary Gaussian increments with Var(B^H_{t+Δ} − B^H_t) = Δ^{2H}.
   * So B^H_{t+Δ} − B^H_t has the law of Δ^H Z, and E|·|^q = Δ^{qH} E|Z|^q.
   * Hence ζ_q = qH.
3. **Rough Bergomi's martingale property.**
   * W^H_t is Gaussian with variance t^{2H}, so E[exp(ηW^H_t − ½η²t^{2H})] = 1, and E[v_t] = ξ₀(t).
   * Conditionally on F_s, W^H_t is Gaussian with a known mean and variance. The same computation gives
     ξ_s(t) = E_s[v_t] as an exponential martingale in s.
4. **The lift's identity.**
   * Write ∫₀^∞ e^{−xt} x^{−α} dx = Γ(1 − α) t^{α−1}.
   * Dividing by Γ(α)Γ(1 − α) gives t^{α−1}/Γ(α).
   * Discretizing the measure x^{−α}dx/(Γ(α)Γ(1 − α)) on a geometric grid gives the weights c_i and the nodes x_i.
5. **The Hawkes mean rate.**
   * Take expectations in λ_t = μ + ∫φ(t − s)dN_s at stationarity: Λ = μ + Λ‖φ‖₁, so Λ = μ/(1 − ‖φ‖₁).
   * As ‖φ‖₁ → 1 the mean rate diverges for fixed μ, and each event's expected number of descendants,
     ‖φ‖₁/(1 − ‖φ‖₁), explodes: hence "nearly unstable".

## Data and reproducibility

* The Surface: Deribit BTC option trades, 10 December 2025 (quotes up to 200 days for the rough fits).
* Binance BTCUSDT 5-minute (January 2024 to November 2025, 700 complete days) and daily (2018 to 2025); Deribit DVOL
  daily.
* No strategy was tested; the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第14部分：粗糙与路径依赖波动率

本部分讲：

* 爆炸的平值偏斜，以及幂律与有界替代形式之争；
* 盖瑟尔–杰松–罗森鲍姆粗糙度估计量，在比特币上重做；
* 粗糙贝尔戈米（混合格式）与粗糙赫斯顿（分数阶亚当斯），拟合到曲面；
* 粗糙可能从何而来：近乎不稳定的霍克斯订单流；
* 马尔可夫提升；
* 关于波动率究竟是否粗糙的争论；
* 居永–勒克富克路径依赖波动率，在样本外拟合DVOL；
* 前沿：二次粗糙赫斯顿、居永的SPX/VIX联合拟合、签名模型与神经校准。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **H ≈ 0.1时，一天期期权和一个月期期权有何不同？**
   * 平值偏斜按T^{H−½}缩放，(1/30)^{−0.4} ≈ 3.9：一天期的偏斜约为一个月期的四倍。
   * 在Δ时间内波动率本身约变动Δ^H，所以波动率的波动率风险大多落在短期期权上。
2. **粗糙还是快速均值回复？** 用多种测量：
   * 日内滞后上已实现方差的标度（先去除日内与周内季节性，并校正微观结构噪声）；
   * 最短到期日上偏斜的期限结构；
   * 粗糙模型与多因子模型在样本外的预测和对冲。
   任何单一测量都可能被骗，正如第7章所示。
3. **在几毫秒内校准。** 可选办法：
   * 用模型价格训练一次的神经替代模型（Horvath–Muguruza–Tomas 2021）；
   * 少数因子、带闭式里卡蒂系统的马尔可夫提升；
   * 用粗网格亚当斯求解的粗糙赫斯顿傅里叶形式。
   并定期用完整模型检查替代模型。

## 习题与解答

1. **W^H的方差。** 由伊藤等距，Var W^H_t = 2H ∫₀ᵗ (t − s)^{2H−1} ds = t^{2H}。
2. **标度。**
   * 分数布朗运动的增量平稳且服从高斯分布，Var(B^H_{t+Δ} − B^H_t) = Δ^{2H}。
   * 所以增量与Δ^H Z同分布，E|·|^q = Δ^{qH} E|Z|^q。
   * 因此ζ_q = qH。
3. **粗糙贝尔戈米的鞅性质。**
   * W^H_t是方差为t^{2H}的高斯变量，故E[exp(ηW^H_t − ½η²t^{2H})] = 1，E[v_t] = ξ₀(t)。
   * 对F_s取条件时同样计算可得，ξ_s(t) = E_s[v_t]作为s的函数是指数鞅。
4. **提升背后的恒等式。**
   * ∫₀^∞ e^{−xt} x^{−α} dx = Γ(1 − α) t^{α−1}，除以Γ(α)Γ(1 − α)即得t^{α−1}/Γ(α)。
   * 在几何网格上离散化该测度，就得到权重c_i和节点x_i。
5. **霍克斯平均速率。**
   * 在平稳状态下对λ_t = μ + ∫φ(t − s)dN_s取期望：Λ = μ + Λ‖φ‖₁，故Λ = μ/(1 − ‖φ‖₁)。
   * 当‖φ‖₁ → 1时，平均速率发散，每个事件的期望后代数‖φ‖₁/(1 − ‖φ‖₁)爆炸：所以称为“近乎不稳定”。
