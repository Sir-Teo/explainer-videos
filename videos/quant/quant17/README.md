# Quant, Built — Part 17: Deep Pricing and Hedging

Part 17 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the frontier of Act III, Derivatives. It covers:

* learning a pricing formula from prices (Hutchinson, Lo and Poggio 1994), hedging with it, and a network's Greeks;
* the neural calibrator for rough Bergomi (Horvath, Muguruza and Tomas 2021): learning the map, label noise,
  calibrating through the network, and two years of weekly surfaces;
* differential machine learning (Huge and Savine 2020) and its classical twin, a Gaussian process with gradients;
* high dimensions: the deep BSDE solver (E, Han and Jentzen 2017; Han, Jentzen and E 2018) and deep optimal stopping
  (Becker, Cheridito and Jentzen 2019);
* the deep hedger (Buehler, Gonon, Teichmann and Wood 2019): the indifference price, entropic risk and CVaR, the drift
  trap, and where it learns not to trade (Leland 1985; Whalley and Wilmott 1997; Imaki et al. 2021);
* neural SDEs and robust bounds for exotics (Gierjatowicz et al. 2022);
* market generators, judged by the stylized facts of Part 1, and hedgers tested across them;
* production and model risk (SR 26-2, 17 April 2026, replacing SR 11-7; PRA SS1/23), what has reached desks, and the
  frontier of 2023–2026.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`deep`](../../../explainer/quant/house/deep.py) module), and every network was trained on one shared CPU, most of
them several times (seeds), with checkpoints so the training can be replayed on screen. The production version
retrains them at full size. Data: Part 13's Deribit BTC option surfaces, and Binance daily BTC closes.

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 58 minutes)

CHAPTERS_EN

## Hands-on

* **Labs** (the House's own code on screen, then run): `train_mlp_regressor` (ch. 1), `calibrate_neural` (ch. 4),
  `train_differential` (ch. 6), `deep_bsde`'s forward sweep (ch. 9), `deep_stopping` (ch. 10), `hedge_pnl` (ch. 11),
  `Hedger.band` with `quoting.ww_band` (ch. 14).
* **Training replays** (seeds as bands): HLP's network (3 seeds), the calibrator (2 seeds), the calibration itself
  (12 starts), differential ML (3 seeds), the deep BSDE (2 seeds and the linear run), deep stopping date by date, the
  no-cost hedger converging onto delta (3 seeds), the drift-trained hedger onto Merton's line (3 seeds), the band
  opening in the trade map (3 seeds), a Whalley–Wilmott start against the default (2 seeds each), the neural SDE's
  calibration and push, the diffusion model (3 seeds).
* **3D:** the learned price surface and its error; the network's implied-volatility surface converging onto the
  Surface's quotes; tangent planes and the Gaussian-process shell; the exercise tunnel; the band's two sheets over
  (time, price) with a path riding between them; the low and high neural-SDE surfaces over Heston's.

## Textbook audit

| Book · chapter | Where |
|---|---|
| Dixon–Halperin–Bilokon 1 (statistical learning, ML in finance) | ch. 1 |
| DHB 2 (probabilistic modelling) | Parts 6, 27 |
| DHB 3 (Bayesian regression, Gaussian processes) | ch. 7: a GP with gradient observations as the twin of differential ML |
| DHB 4 (feedforward networks, universal approximation, back-propagation) | ch. 1 (UAT, the training replay), ch. 2 |
| DHB 5 (interpretability: sensitivities, Jacobians) | ch. 2: a pricing network's Greeks are its Jacobian and Hessian |
| DHB 6–7 (sequence models, HMMs, filters) | Part 7; ch. 16 uses GJR-GARCH as a baseline |
| DHB 8 (RNNs, LSTMs, CNNs) | ch. 16 (the LSTM generator; Quant GANs' convolutions) |
| DHB 9 (introduction to RL) | Part 8 |
| DHB 10 (RL in finance: QLBS) | ch. 12 (QLBS and RL hedging as the RL view of the same objective) |
| DHB 11 (inverse RL) | Part 29 |
| DHB 12 (frontiers) | ch. 18 |
| Kelly–Xiu, *Financial Machine Learning* (the virtue of complexity) | ch. 1 (an over-parameterized network fits 66,150 prices without overfitting); returns → Parts 25–30. Derivatives are not a core topic of the survey |
| Jentzen–Kuckuck–von Wurstemberger, *Mathematical Introduction to Deep Learning* | ch. 9 (why the cost is polynomial in the dimension) |
| Glasserman ch. 7 (pathwise and likelihood-ratio Greeks) | Part 16; ch. 6 proves the pathwise label unbiased, ch. 7 sends the digital back to the LR method |
| Glasserman ch. 8; Savine (AAD) | Part 16 (LSM, duality, the tape); ch. 10 uses Part 16's LSM number, ch. 6 its adjoint labels |
| Shreve II 6.4/6.6; Øksendal 8 (Feynman–Kac) | Part 5; ch. 8 derives the non-linear version (Pardoux–Peng) |
| Gatheral 2–3 | Parts 12–13; ch. 15 calibrates a neural SV model to Heston prices |

## Papers, chapter by chapter

* ch. 1 Hutchinson, Lo and Poggio (1994); Cybenko (1989); Hornik (1991); Ruf and Wang (2020, a review of "far over a
  hundred" papers). ch. 2 Breeden–Litzenberger (Part 12); Dugas et al. (2009); Ackerer, Tagasovska and Vatter (2020).
* ch. 3–5 Hernandez (2016); Bayer and Stemper (2018); Liu, Oosterlee and Bohte (2019); Horvath, Muguruza and Tomas
  (2021).
* ch. 6–7 Huge and Savine (2020); DHB ch. 3.
* ch. 8–9 E, Han and Jentzen (2017); Han, Jentzen and E (2018); Pardoux and Peng (1990); Sirignano and Spiliopoulos
  (2018); Hutzenthaler, Jentzen, Kruse and Nguyen (2020).
* ch. 10 Becker, Cheridito and Jentzen (2019, Table 1: [26.156, 26.162] for five assets); Broadie and Detemple (1997);
  Longstaff and Schwartz (2001, Part 16).
* ch. 11–12 Hodges and Neuberger (1989); Buehler, Gonon, Teichmann and Wood (2019); Rockafellar and Uryasev (2000);
  Merton (1969); François, Gauthier, Godin and Pérez Mendoza (2024); Buehler, Murray, Pakkanen and Wood (2021);
  Halperin (QLBS); Kolm and Ritter (2019); Cao, Chen, Hull and Poulos (2021); Buehler, Murray and Wood (2022).
* ch. 13–14 Leland (1985); Whalley and Wilmott (1997); Davis, Panas and Zariphopoulou (1993); Imaki, Imajo, Ito,
  Minami and Nakagawa (2021); Arzel and Lehdili (2026).
* ch. 15 Gierjatowicz, Sabate-Vidales, Šiška, Szpruch and Žurič (2022); Cuchiero, Khosrawi and Teichmann (2020);
  Guyon and Mustapha (SSRN 4309576).
* ch. 16 Ho, Jain and Abbeel (2020); Wiese, Knobloch, Korn and Kretschmer (2020); Buehler, Horvath, Lyons, Perez
  Arribas and Wood (2020); Liao, Ni, Szpruch, Wiese, Sabate-Vidales and Xiao (2020); Ni, Szpruch, Sabate-Vidales, Xiao,
  Wiese and Liao (2021); Kidger, Foster, Li, Oberhauser and Lyons (2021); Chevyrev and Oberhauser (2022).
* ch. 17 SR 11-7 (2011); SR 26-2 (2026); PRA SS1/23; Risk.net on J.P. Morgan and Danske; Cherrat et al. (2023,
  *Quantum* 7, 1191); Ferguson and Green (2018).
* ch. 18 SANOS (2026), DYSANOS (2026), GROMM (2026); Zernikov (2026); Godin (2026); Mueller, Akkari, Gonon and Wood
  (2024); François et al. (2025); Reppen, Soner and Tissot-Daguette (2022); Bayer, Pelizzari and Schoenmakers (2023);
  Ye and Wong (2025); Issa, Horvath, Lemercier and Salvi (2023).

## Build it

```bash
python -m videos.quant.quant17.compute calib_data          # 60 resumable chunks, ~1 h (two processes share them)
python -m videos.quant.quant17.compute                     # everything else; every training item checkpoints and resumes
EXPLAINER_TTS=silent python tools/qa_scene.py quant17 Band # one chapter, silent, with a contact sheet
python tools/make.py quant17 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Your hedger has costs. Why does the optimal hedge have a band?**
   * Holding δ instead of the frictionless Δ adds hedging variance of order (δ − Δ)²σ²S² per unit time, so the risk
     grows with the square of the gap.
   * Trading back costs c|δ − Δ|S, linear in the gap.
   * Near Δ the quadratic risk is smaller than the linear cost, so it pays to wait until the gap is large enough.
     Balancing the two gives a band of half-width (3cSΓ²/2γ)^{1/3} (Whalley–Wilmott), widest where gamma is large.
   * The deep hedger learns the same principle without the asymptotics (chapters 13–14).
2. **A neural calibrator fits the surface beautifully. How do you know it is right?**
   * Re-price the calibrated parameters with the slow engine (fresh Monte Carlo) and compare errors.
   * Check every input lies inside the training ranges: in chapter 5, H pressed against the floor of the box, where
     the tanh map's gradient vanishes (chapter 4).
   * Know the network's error against fresh simulation, separated from the noise of its own labels (chapter 3).
   * A network extrapolates silently, so these checks are part of the model, not an extra.
3. **You have a thousand simulated payoffs. Why also record their derivatives?**
   * With adjoint differentiation each sample's pathwise derivatives cost about one extra pricing, and give d labels
     more per sample; for a Lipschitz payoff they are unbiased estimates of the delta.
   * They pin down the function's shape between samples: prices, and above all Greeks, need far fewer samples.
   * Not for a digital: its pathwise derivative is zero almost surely (use likelihood-ratio labels or smoothing).
4. **Your deep hedger makes money on average with no costs. Is it hedging?**
   * Partly it is speculating. Under a drift μ the exponential-utility hedge is Δ + μ/(γσ²S): Merton's portfolio on
     top of the replicating hedge (chapter 12).
   * Compare its holdings with delta and price it on driftless paths; it needs more there than a driftless hedger.
   * Train under a (near-)martingale measure (Buehler et al. 2021), or use a risk measure that weighs bad outcomes
     enough (François et al. 2024), unless the drift is a view you mean to hold.

## Problems, with solutions

1. **Indifference price.**
   * ρ(X + c) = (1/γ) log E e^{−γX − γc} = ρ(X) − c, so the entropic risk is cash invariant.
   * Without the claim and with a martingale stock, not trading is optimal and the minimal risk is 0. With it, the
     seller is indifferent when ρ(−Z + hedge − costs + p) = 0, i.e. at p = min_δ ρ(−Z + (δ·S)_T − C_T).
2. **The band's scaling.**
   * Over dt, a gap ε costs (γ/2) ε² σ²S² dt of certainty equivalent.
   * Keeping the gap within ±h means trading about (σ²S²Γ²/h) dt shares at cost cS per share; inside, E ε² = h²/3.
   * Minimizing γh²σ²S²/6 + cSσ²S²Γ²/h over h gives h³ = 3cSΓ²/2γ.
3. **The BSDE behind the solver.**
   * By Itô, dY = (u_t + 𝓛u) dt + ∇uᵀσ(X) dW.
   * The PDE says u_t + 𝓛u = (1 − δ)Q(u)u + Ru = f(Y), so dY = f(Y) dt + Z·dW with Z = σ(X)ᵀ∇u and Y_T = min_i X_T^i.
4. **Differential regression.** With features Φ (n × p) and their input gradients ∇Φ, minimize
   ‖Φw − y‖² + λ‖∇Φ w − ∂y‖². The normal equations are (ΦᵀΦ + λ ∇Φᵀ∇Φ) w = Φᵀy + λ ∇Φᵀ∂y.
5. **Deep stopping's bound.**
   * Given X_n, the objective g_n F + E[G_{n+1}|X_n](1 − F) is linear in F, maximized by F = 1{g_n ≥ E[G_{n+1}|X_n]}.
   * Any {0,1} rule defines a stopping time τ, and E[g_τ] ≤ sup_τ E[g_τ], the Bermudan price.
6. **Leland's volatility.** Between rebalances ΔΔ ≈ ΓΔS, so E|ΔΔ|S = ΓS²σ√Δt √(2/π). The cost per unit time is
   (k/2)ΓS²σ√(2/π)/√Δt with round-trip cost k = 2c. Adding it to ½σ²S²Γ in the pricing equation of a short option gives
   ½σ̂²S²Γ with σ̂² = σ²(1 + √(2/π) k/(σ√Δt)).
7. **Merton's term.** In a complete market with zero rates, the terminal wealth with the claim is −Z + (δ·S)_T. Write
   δ = Δ + η: the Δ part replicates Z exactly, leaving max E[−e^{−γ(x − p + (η·S)_T)}], the no-claim CARA problem, whose
   solution holds μ/(γσ²) in money, i.e. η = μ/(γσ²S).
8. **Label noise.** If y = F + ε with ε independent of the network's prediction F̂, E(F̂ − y)² = E(F̂ − F)² + E ε² ≥ E ε².
   Doubling the label variance raises this floor, but a smooth fit to many labels near each θ averages their noise, so
   the network's own error E(F̂ − F)² grows much less than the labels' variance.

## Data and reproducibility

* Deribit BTC option surfaces of Part 13 (Wednesdays 2024–2025); Binance BTCUSDT daily closes (Aug 2017 – Dec 2025).
* The rough Bergomi training set: 12,000 parameter sets × 80 points, 10,000 paths each, one step a day; parameter box
  H ∈ [0.02, 0.5], η ∈ [0.3, 4], ρ ∈ [−0.9, 0.6], vol ∈ [25%, 120%].
* References checked against the sources: HJE (2018) 57.300 by multilevel Picard; BCJ (2019) Table 1; HLP (1994);
  Part 16's Longstaff–Schwartz on the same max-call, read from its cache; the Risk.net reports (J.P. Morgan's
  data-driven hedging of vanilla index books since 2018, a large share of its Euro Stoxx vanilla book priced with deep
  hedging, the extension to cliquets); SR 26-2 (Federal Reserve, 17 April 2026); PRA SS1/23; the arXiv abstracts of
  the 2023–2026 papers.
* No strategy was tested; the trial counter is unchanged at 310.

---

# 量化金融，从零搭建 — 第17部分：深度定价与对冲

本部分讲：

* 从价格中学习定价公式（Hutchinson、Lo与Poggio，1994），用它对冲，以及网络的希腊字母；
* 粗糙Bergomi的神经网络校准器（Horvath、Muguruza与Tomas，2021）：学习映射、标签噪声、通过网络校准，以及两年的周度曲面；
* 差分机器学习（Huge与Savine，2020），以及它的经典孪生方法：带梯度观测的高斯过程；
* 高维：深度BSDE求解器（E、Han与Jentzen，2017；Han、Jentzen与E，2018）和深度最优停时（Becker、Cheridito与Jentzen，2019）；
* 深度对冲器（Buehler、Gonon、Teichmann与Wood，2019）：无差异价格、熵风险与条件风险价值、漂移陷阱，以及它学会在哪里不交易
  （Leland 1985；Whalley与Wilmott 1997；Imaki等 2021）；
* 神经SDE与奇异期权的稳健界（Gierjatowicz等，2022）；
* 用第1部分的典型事实评判的市场生成器，以及跨生成器检验的对冲器；
* 投产与模型风险（2026年4月17日的SR 26-2取代SR 11-7；英国PRA SS1/23）、已经进入交易台的应用，以及2023–2026年的前沿。

所有网络都在一台共享CPU上训练，多数训练了不止一次（多个种子），并保存检查点，以便在屏幕上回放训练过程；投产版本会以完整规模重新训练。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约58分钟）

CHAPTERS_ZH

## 交易台问题与解答

1. **你的对冲器有成本。为什么最优对冲有一个区间？**
   * 持有δ而不是无摩擦的Δ，单位时间的对冲方差约为(δ − Δ)²σ²S²：风险随偏差的平方增长。
   * 交易回去的成本是c|δ − Δ|S，与偏差成线性关系。
   * 在Δ附近，平方的风险小于线性的成本，所以值得等到偏差足够大。两者平衡给出半宽度(3cSΓ²/2γ)^{1/3}的区间（Whalley–Wilmott），在Gamma大的地方最宽。
   * 深度对冲器不借助渐近分析就学到了同样的原理（第13–14章）。
2. **神经网络校准器把曲面拟合得很漂亮。怎么知道它是对的？**
   * 用慢速引擎（新的蒙特卡洛）在校准参数下重新定价并比较误差。
   * 检查每个输入都在训练范围内：第5章里，H顶在了训练框的下限，那里双曲正切映射的梯度消失（第4章）。
   * 知道网络相对新模拟的误差，并把它与自身标签的噪声区分开（第3章）。
   * 网络外推时不会发出警告，所以这些检查是模型的一部分，而不是附加项。
3. **你有一千个模拟收益。为什么还要记录它们的导数？**
   * 用伴随微分，每个样本的路径导数只需约一次额外定价，每个样本多出d个标签；对利普希茨收益，它们是Delta的无偏估计。
   * 它们确定了样本之间函数的形状：价格，尤其是希腊字母，所需样本少得多。
   * 数字期权例外：它的路径导数几乎处处为零（改用似然比标签或光滑化）。
4. **你的深度对冲器在没有成本时平均能赚钱。它是在对冲吗？**
   * 部分是在投机。在漂移μ下，指数效用的对冲是Δ + μ/(γσ²S)：复制对冲之上叠加了默顿的投资组合（第12章）。
   * 在无漂移路径上把它的持仓与Delta比较并定价；在那里它比无漂移训练的对冲器需要更多。
   * 在（近似）鞅测度下训练（Buehler等，2021），或使用对不利结果赋予足够权重的风险度量（François等，2024），除非漂移是你有意持有的观点。

## 习题与解答

1. **无差异价格。** ρ(X + c) = (1/γ) log E e^{−γX − γc} = ρ(X) − c，所以熵风险具有现金不变性。没有权益且股票为鞅时，不交易是最优的，最小风险为0；有权益时，卖方在ρ(−Z + 对冲 − 成本 + p) = 0时无差异，即p = min_δ ρ(−Z + (δ·S)_T − C_T)。
2. **区间的标度。** 在dt时间内，偏差ε的确定性等价成本为(γ/2)ε²σ²S²dt；把偏差保持在±h内，约需交易(σ²S²Γ²/h)dt股，每股成本cS；区间内E ε² = h²/3。对h最小化γh²σ²S²/6 + cSσ²S²Γ²/h，得h³ = 3cSΓ²/2γ。
3. **求解器背后的BSDE。** 由伊藤公式，dY = (u_t + 𝓛u)dt + ∇uᵀσ(X)dW；偏微分方程给出u_t + 𝓛u = (1 − δ)Q(u)u + Ru = f(Y)，所以dY = f(Y)dt + Z·dW，Z = σ(X)ᵀ∇u，Y_T = min_i X_T^i。
4. **差分回归。** 设特征Φ（n × p）及其对输入的梯度∇Φ，最小化‖Φw − y‖² + λ‖∇Φw − ∂y‖²；正规方程为(ΦᵀΦ + λ∇Φᵀ∇Φ)w = Φᵀy + λ∇Φᵀ∂y。
5. **深度停时的下界。** 给定X_n，目标g_nF + E[G_{n+1}|X_n](1 − F)对F是线性的，在F = 1{g_n ≥ E[G_{n+1}|X_n]}处取最大；任何{0,1}规则都定义一个停时τ，而E[g_τ] ≤ sup_τ E[g_τ]，即百慕大期权的价格。
6. **利兰的波动率。** 两次再平衡之间ΔΔ ≈ ΓΔS，所以E|ΔΔ|S = ΓS²σ√Δt √(2/π)；单位时间成本为(k/2)ΓS²σ√(2/π)/√Δt，往返成本k = 2c。把它加到卖出期权定价方程中的½σ²S²Γ项上，得½σ̂²S²Γ，σ̂² = σ²(1 + √(2/π) k/(σ√Δt))。
7. **默顿项。** 在零利率的完备市场中，带权益的终值财富为−Z + (δ·S)_T。令δ = Δ + η：Δ部分精确复制Z，剩下max E[−e^{−γ(x − p + (η·S)_T)}]，即没有权益的CARA问题，其解持有金额μ/(γσ²)，即η = μ/(γσ²S)。
8. **标签噪声。** 若y = F + ε且ε独立于网络的预测F̂，则E(F̂ − y)² = E(F̂ − F)² + Eε² ≥ Eε²。标签方差加倍会抬高这个下限，但对每个θ附近许多标签的光滑拟合会平均掉它们的噪声，所以网络自身的误差E(F̂ − F)²增长远小于标签的方差。
