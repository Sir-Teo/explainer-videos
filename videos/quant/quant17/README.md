# Quant, Built — Part 17: Deep Pricing and Hedging

Part 17 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the frontier of Act III, Derivatives. It covers:

* learning a pricing formula from prices (Hutchinson, Lo and Poggio 1994), and hedging with it;
* the neural calibrator for rough Bergomi (Horvath, Muguruza and Tomas 2021), on the Surface and on two years of
  weekly surfaces;
* differential machine learning (Huge and Savine 2020);
* high dimensions: the deep BSDE solver (Han, Jentzen and E 2018) and deep optimal stopping (Becker, Cheridito and
  Jentzen 2019);
* the deep hedger (Buehler, Gonon, Teichmann and Wood 2019): costs, risk measures, indifference prices, and where
  it learns not to trade;
* neural SDEs and robust bounds for exotics (Gierjatowicz et al. 2022);
* market generators, judged by the stylized facts of Part 1;
* production and model risk (SR 11-7, replaced by SR 26-2 in April 2026).

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`deep`](../../../explainer/quant/house/deep.py) module), and every network was trained on a CPU in minutes. The
production version retrains them at full size. Data: Part 13's Deribit BTC option surfaces, and Binance daily BTC
closes.

*An education in methods, not investment advice. Firms and episodes are described from the public record.*

## Chapters (about 60 minutes)

* **A machine that hedges.** A band network learns, from costs alone, a no-trade corridor narrower than
  Whalley–Wilmott's and needs a lower price (3.02 against 3.55 for daily delta hedging at 0.5% costs). J.P. Morgan:
  about 70% of its Euro Stoxx flow options quoted and hedged by machine by 2022, as reported by Risk.net.
* **1. Learning a pricing formula.** HLP's simulated experiment redone with a small MLP. Trained on 66,150 prices,
  its call price sits within 0.02% of the strike of Black–Scholes. Its own derivative hedges 200 fresh options with a
  tracking error within 4% of the true delta's. HLP found the same in simulation, and on S&P 500 futures options,
  1987–1991, their networks beat Black–Scholes in many cases.
* **2. The neural calibrator.**
  * A pointwise network (H, η, ρ, ξ₀, ξ₁, T, k) → implied volatility, trained on 895,000 rough Bergomi Monte Carlo
    prices from 12,000 parameter sets.
  * Held-out error 1.90 vol points, below the 2.86 noise of its own labels.
  * The Surface calibrated in 27 s: H = 0.07, η = 1.9, ρ = −0.40. Error 0.97 vol points through the network,
    1.08 by fresh Monte Carlo.
  * One pass over the surface takes 6 ms against 2 s of simulation.
* **3. Rough volatility, week by week.**
  * Rough Bergomi calibrated to Part 13's 100 weekly surfaces (2024–2025), about 2 s each.
  * In 77% of weeks H sits at 0.02, the lowest value the network was trained on. Fresh Monte Carlo confirms these
    fits, so the market asks for more roughness than the training box allows.
  * Against Heston refitted to the same quotes: median errors 1.19 and 1.22, with rough Bergomi ahead in 56% of
    weeks. Part 14's one-day win becomes a near tie.
* **4. Differential machine learning.**
  * A 7-asset Bachelier basket, where the exact price and deltas are known.
  * With 256 samples, derivatives cut the price error from 5.03 to 0.43 and the delta error 31 times.
  * 256 samples with derivatives price as well as 4,096 without.
* **5. A hundred dimensions: the deep BSDE.** Han–Jentzen–E's claim on 100 assets with default risk:
  u₀ = 57.37 against the reference 57.300 (0.12% error) in 16 minutes. Without default it is worth 59.57 (Monte
  Carlo). The paper's 60.781 also leaves out discounting.
* **6. Deep optimal stopping.**
  * The learned exercise region of a two-asset max-call has the textbook two lobes.
  * Lower bounds: 13.886 for two assets (binomial 13.902) and 26.107 ± 0.04 for five. The five-asset value is 0.2%
    below the paper's lower bound of 26.156, after 500 training steps per date on a CPU.
* **7. The deep hedger.**
  * Entropic risk, indifference prices (Hodges–Neuberger 1989).
  * With no costs the network rebuilds Black–Scholes delta to within 0.06 shares, at a price of 2.36 (delta
    hedging: 2.36).
  * With costs of 0.1–1%, the band network beats daily delta hedging and the Whalley–Wilmott band at every level:
    3.52 against 4.86 and 3.69 at 1%.
* **8. Where not to trade.**
  * A plain network trained with 0.5% costs, told nothing about bands: its do-nothing zone at the money widens from
    0.02 to 0.10 shares, and from far away it moves only part of the way. Its price, 3.08, equals the
    Whalley–Wilmott band's.
  * The band network (Imaki et al. 2021) learns a band 0.7 times Whalley–Wilmott's width at the money. Its band is
    nearly flat across prices, where theirs peaks at the strike.
* **9. Neural SDEs and robust bounds.**
  * A neural stochastic volatility model calibrated to 36 Heston calls, within 0.12 vol points.
  * A down-and-out call ranges from 0.0671 to 0.0703 (Heston: 0.0685) while every vanilla stays within 0.19 vol
    points.
  * A lower estimate of the true range.
* **10. Market generators.**
  * BTC daily returns in 32-day windows: 2017–2023 for training, 2024–2025 held out, and calmer (kurtosis 2.4
    against 14.7).
  * Independent draws, GJR-GARCH, a signature-matching volatility×noise LSTM and a small diffusion model.
  * By signature distance alone, independent normal draws sit closest to the training years, yet they have no
    clustering. Only the signature network reproduces the tails, clustering and leverage.
  * The diffusion model is nearest the held-out years because its tails are thin.
* **11. Production and model risk.** J.P. Morgan and Danske Bank, as reported; SR 26-2 (April 2026), which replaced SR 11-7; validating a network:
  held-out error, input ranges, known answers, the simulator as the model, nightly checks.
* **12. The deep hedger in the House.** Rule 17: no network without a slower, independent engine to check it;
  inputs outside the training region go to that engine; hedgers are tested on at least two generators and on
  replayed history. The trial counter stays at 73.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant17.compute calib_data          # 60 resumable chunks, ~1 h (two processes share them)
python -m videos.quant.quant17.compute                     # everything else: tens of minutes per item on a CPU
EXPLAINER_TTS=silent python tools/qa_scene.py quant17 Band # one chapter, silent, with a contact sheet
python tools/make.py quant17 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Your hedger has costs. Why does the optimal hedge have a band?**
   * Holding δ instead of the frictionless Δ adds hedging variance of order (δ − Δ)² Γ²-weighted per unit time, so
     the risk grows with the square of the gap.
   * Trading back costs c|δ − Δ|S, linear in the gap.
   * Near Δ the quadratic risk is smaller than the linear cost, so it pays to wait until the gap is large enough.
     Balancing the two gives a band of half-width (3cSΓ²/2γ)^{1/3} (Whalley–Wilmott), widest where gamma is large.
   * The deep hedger learns the same principle without the asymptotics.
2. **A neural calibrator fits the surface beautifully. How do you know it is right?**
   * Re-price the calibrated parameters with the slow engine (fresh Monte Carlo) and compare errors.
   * Check every input lies inside the training ranges. In chapter 3, H pressed against the floor of the box.
   * Know the network's held-out error and the noise of its own labels.
   * A network extrapolates silently, so these checks are part of the model, not an extra.
3. **You have a thousand simulated payoffs. Why also record their derivatives?**
   * With adjoint differentiation each sample's pathwise derivatives cost about one extra pricing, and give d labels
     more per sample.
   * They are less noisy than the payoffs near the money and pin down the function's shape between samples.
   * Prices, and above all Greeks, need far fewer samples.

## Problems, with solutions

1. **Indifference price.**
   * ρ(X + c) = (1/γ) log E e^{−γX − γc} = ρ(X) − c, so the entropic risk is cash invariant.
   * Without the claim, not trading is optimal under costs, and ρ = 0. With it, the seller is indifferent when
     ρ(−Z + hedge − costs + p) = 0, i.e. at p = min_δ ρ(−Z + (δ·S)_T − C_T).
2. **The band's scaling.**
   * Over a time dt, a gap ε costs (γ/2) ε² σ²S² dt of certainty equivalent.
   * Keeping the gap within ±h means trading about (σ²S²Γ²/h) dt shares per unit time at cost c S per share.
   * Minimizing γh²σ²S²/6 + cSσ²S²Γ²/h over h gives h³ ∝ cSΓ²/γ.
3. **The BSDE behind the solver.**
   * By Itô, dY = (u_t + μx·∇u + ½σ²Σx_i²u_ii) dt + σ x∇u · dW.
   * The PDE turns the drift into f(t, X, Y, Z) with a minus sign, giving dY = −f dt + Z dW, Z = σx∇u, Y_T = g(X_T).
4. **Differential regression.** With features Φ (n × p) and their input gradients ∇Φ, minimize
   ‖Φw − y‖² + λ‖∇Φ w − ∂y‖². The normal equations are (ΦᵀΦ + λ ∇Φᵀ∇Φ) w = Φᵀy + λ ∇Φᵀ∂y.
5. **Deep stopping's bound.**
   * Given X_n, the objective g_n F + E[G_{n+1}|X_n](1 − F) is linear in F, maximized by F = 1{g_n ≥ E[G_{n+1}|X_n]}.
   * Any {0,1} rule defines a stopping time τ, and E[g_τ] ≤ sup_τ E[g_τ], the Bermudan price.

## Data and reproducibility

* Deribit BTC option surfaces of Part 13 (Wednesdays 2024–2025); Binance BTCUSDT daily closes (Aug 2017 – Dec 2025).
* The rough Bergomi training set: 12,000 parameter sets × 80 points, 10,000 paths each, one step a day; parameter box
  H ∈ [0.02, 0.5], η ∈ [0.3, 4], ρ ∈ [−0.9, 0.6], vol ∈ [25%, 120%].
* References checked against the papers: HJE (2018) 57.300 by multilevel Picard; BCJ (2019) Table 1; HLP (1994)
  abstract and section 3.
* No strategy was tested; the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第17部分：深度定价与对冲

本部分讲：

* 从价格中学习定价公式（Hutchinson、Lo与Poggio，1994），并用它对冲；
* 粗糙Bergomi的神经网络校准器（Horvath、Muguruza与Tomas，2021），用在曲面和两年的周度曲面上；
* 差分机器学习（Huge与Savine，2020）；
* 高维：深度BSDE求解器（Han、Jentzen与E，2018）和深度最优停时（Becker、Cheridito与Jentzen，2019）；
* 深度对冲器（Buehler、Gonon、Teichmann与Wood，2019）：成本、风险度量、无差异价格，以及它学会在哪里不交易；
* 神经SDE与奇异期权的稳健界（Gierjatowicz等，2022）；
* 用第1部分的典型事实评判的市场生成器；
* 投产与模型风险（SR 11-7，2026年4月由SR 26-2取代）。

所有网络都在CPU上用几分钟训练；投产版本会以完整规模重新训练。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录。*

## 交易台问题与解答

1. **你的对冲器有成本。为什么最优对冲有一个区间？**
   * 持有δ而不是无摩擦的Δ，带来的对冲方差与(δ − Δ)²成正比：风险随偏差的平方增长。
   * 交易回去的成本是c|δ − Δ|S，与偏差成线性关系。
   * 在Δ附近，平方的风险小于线性的成本，所以值得等到偏差足够大。两者平衡给出半宽度(3cSΓ²/2γ)^{1/3}的区间（Whalley–Wilmott），在Gamma大的地方最宽。
   * 深度对冲器不借助渐近分析就学到了同样的原理。
2. **神经网络校准器把曲面拟合得很漂亮。怎么知道它是对的？**
   * 用慢速引擎（新的蒙特卡洛）在校准参数下重新定价并比较误差。
   * 检查每个输入都在训练范围内：第3章里，H就顶在了范围的下限。
   * 知道网络在保留数据上的误差，以及它自己标签的噪声。网络外推时不会发出警告，所以这些检查是模型的一部分，而不是附加项。
3. **你有一千个模拟收益。为什么还要记录它们的导数？**
   * 用伴随微分，每个样本的路径导数只需约一次额外定价，每个样本多出d个标签。
   * 在平值附近它们比收益的噪声更小，并确定了样本之间函数的形状：价格，尤其是希腊字母，所需样本少得多。

## 习题与解答

1. **无差异价格。** ρ(X + c) = (1/γ) log E e^{−γX − γc} = ρ(X) − c，所以熵风险具有现金不变性。没有权益时，有成本下不交易是最优的，ρ = 0；有权益时，卖方在ρ(−Z + 对冲 − 成本 + p) = 0时无差异，即p = min_δ ρ(−Z + (δ·S)_T − C_T)。
2. **区间的标度。** 在dt时间内，偏差ε的确定性等价成本为(γ/2)ε²σ²S²dt；把偏差保持在±h内，单位时间约需交易(σ²S²Γ²/h)dt股，每股成本cS。对h最小化γh²σ²S²/6 + cSσ²S²Γ²/h，得h³ ∝ cSΓ²/γ。
3. **求解器背后的BSDE。** 由伊藤公式，dY = (u_t + μx·∇u + ½σ²Σx_i²u_ii)dt + σx∇u·dW；偏微分方程把漂移项变成带负号的f(t, X, Y, Z)，得dY = −f dt + Z dW，Z = σx∇u，Y_T = g(X_T)。
4. **差分回归。** 设特征Φ（n × p）及其对输入的梯度∇Φ，最小化‖Φw − y‖² + λ‖∇Φw − ∂y‖²；正规方程为(ΦᵀΦ + λ∇Φᵀ∇Φ)w = Φᵀy + λ∇Φᵀ∂y。
5. **深度停时的下界。** 给定X_n，目标g_nF + E[G_{n+1}|X_n](1 − F)对F是线性的，在F = 1{g_n ≥ E[G_{n+1}|X_n]}处取最大；任何{0,1}规则都定义一个停时τ，而E[g_τ] ≤ sup_τ E[g_τ]，即百慕大期权的价格。
