# Quant, Built — Part 12: The Volatility Surface

Part 12 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It covers:

* smile, skew and term structure, and quoting by delta;
* sticky strike against sticky moneyness;
* static arbitrage, and SSVI fitted to the Surface;
* Dupire's local volatility and its forward smile;
* variance swaps and the VIX, rebuilt from options;
* the variance risk premium on two years of weekly Bitcoin surfaces, and Martin's SVIX bound;
* Volmageddon and dealer gamma;
* a variational autoencoder over surfaces.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`volsurface`](../../../explainer/quant/house/volsurface.py) builder, tested) from Deribit's trades (the Surface and
100 weekly surfaces), Binance's hourly BTCUSDT, Deribit's DVOL and FRED's VIX.

*An education in methods, not investment advice.*

## Chapters (about 45 minutes)

* **The shape of fear.** A 3D tour of the Surface (10 December 2025): 254 quotes and an SSVI fit at 0.74 vol points,
  vega-weighted. Then the objectives, and the surface builder.
* **1. Smile, skew, term structure.** Three expiries with SVI fits, and the 25-delta risk reversal and butterfly. A
  sticky test predicts 11 December's quotes from 10 December's surface: sticky moneyness misses by 2.6 vol points,
  sticky strike by 3.0.
* **2. Static arbitrage, and SSVI.** Gatheral's g ≥ 0, calendar monotonicity and Lee's bound. SSVI (Gatheral–Jacquier
  2014) gives ρ = −0.23, η = 0.73 and γ = 0.56. The smallest g is 0.075 across the per-expiry SVI fits and 0.26 for
  SSVI: no butterfly arbitrage.
* **3. Local volatility.** Dupire (1994), Derman–Kani, and Gyöngy's projection. Local vol is taken from the SSVI fit,
  and a Monte Carlo of 40,000 paths gives the 30-day forward smile 60 days out. Its skew (90% minus 110%) is
  3.4 points, against 6.5 today: local vol flattens the future smile.
* **4. Variance swaps and the VIX.** Itô and Carr–Madan give the 1/K² strip (DDKZ 1999). On the Surface, √K_var is
  48.8% against 43.7% at the money. The VIX recipe, run at Deribit-like strikes and interpolated to 30 days, gives
  48.8%, against DVOL's 45.9% at the same moment.
* **5. The variance risk premium, measured.** Over 100 weekly surfaces (January 2024 to November 2025), the 30-day
  variance-swap rate averaged 54% vol against 47.6% realized over the following 30 days. The premium was positive in
  76% of weeks, with a Newey–West t of 3.6. Martin's (2017) SVIX bound for Bitcoin averages 31% a year, valid only
  under his negative-covariance condition.
* **6. Volmageddon, and dealer gamma.** The crisis file comes from FRED and the public record: the VIX went from 17.31
  to 37.32 on 5 February 2018 (+116%, its largest one-day rise); XIV lost more than 90%, and Credit Suisse announced
  its redemption. The chapter explains the inverse note's rebalancing feedback and the roll. Then dealer gamma
  exposure, intraday momentum (Baltussen et al. 2021) and 0DTE.
* **7. Learning surfaces.** A VAE (Kingma–Welling) is trained over 100 weekly 17 × 6 implied-vol grids.
  * Its 2-d latent space rebuilds them to 1.9 vol points.
  * z₁ tracks the ATM level (correlation 0.96); walking it moves 30-day ATM vol from 35% to 69%.
  * z₂ tilts the smile from put skew toward call skew (correlation with skew −0.39).
  * Generated surfaces still pass through the arbitrage checker.
* **8. The surface builder.** Rule 12: quote only from a fitted, checked surface, and state the dynamics behind every
  exotic price. The trial counter is unchanged.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant12.compute                   # every number (fetches 100 days of Deribit trades once, ~10 min)
EXPLAINER_TTS=silent python tools/qa_scene.py quant12 VarSwap # one chapter, silent, with a contact sheet
python tools/make.py quant12 --cpu-voice -q m            # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Why is the VIX above realized on average?** Implied variance is the price of variance under Q, and variance
   rises in bad times, when marginal utility is high. Buyers of variance therefore pay a premium: the variance risk
   premium (Carr–Wu 2009). Here it was positive in 76% of weeks, with a t of 3.6.
2. **Replicate a variance swap.** Hold (2/T)·ΔK/K² of each out-of-the-money option, puts below the forward and calls
   above, and delta-hedge with the forward (1/F per unit of variance notional, rebalanced). The strip is a log
   contract. By Itô, −2 log(S_T/S_0) + 2∫dS/S = ∫σ²dt. So the strip plus the hedge pays realized variance, and the
   strip's cost is the fair strike.
3. **Dealer short gamma into expiry.** To stay delta-neutral, a short-gamma book buys as the price rises and sells as
   it falls, which amplifies moves. Long gamma does the opposite and tends to pin the price near large strikes.

## Problems, with solutions

1. **Dupire's formula.** The risk-neutral density p(K, T) solves the forward (Fokker–Planck) equation
   ∂_T p = ½∂_KK(σ²_loc K² p) at zero rates. Since C_KK = p, integrating twice in K (the boundary terms vanish) gives
   ∂_T C = ½σ²_loc K² C_KK.
2. **The log contract's strip.** Taylor's theorem with integral remainder, around F, gives
   f(S) = f(F) + f′(F)(S − F) + ∫_0^F f″(K)(K − S)⁺dK + ∫_F^∞ f″(K)(S − K)⁺dK. With f = −log, f″ = 1/K². By Itô,
   ∫_0^T σ²dt = 2∫dS/S − 2 log(S_T/S_0). Taking Q-expectations (zero rates) gives
   K_var = (2/T)∫ OTM(K)/K² dK.
3. **SSVI's calendar condition** (Gatheral–Jacquier 2014, Theorem 4.1). The surface is free of calendar arbitrage iff
   θ_T is non-decreasing and 0 ≤ ∂_θ(θφ(θ)) ≤ ((1 + √(1 − ρ²))/ρ²)·φ(θ). For the power law φ = η/(θ^γ(1 + θ)^{1−γ})
   with γ ∈ (0, 1), θφ = ηθ^{1−γ}/(1 + θ)^{1−γ} is increasing. Checking the upper bound reduces to
   (1 − γ)/(1 + θ) ≤ (1 + √(1 − ρ²))/ρ², which holds for any |ρ| < 1.
4. **Local skew is twice implied skew.** Near the money at short expiry, implied volatility is approximately the
   average of local volatility along the straight line from the spot to the strike (Berestycki–Busca–Florent):
   σ_imp(k) ≈ (1/k)∫_0^k σ_loc(u)du. Differentiating at k = 0 gives σ′_imp(0) = ½σ′_loc(0).
5. **Martin's bound.** With E^Q[X] = R_f·E[mX] and E[mR] = 1: var^Q(R) = R_f E[mR²] − R_f². Also
   cov(mR, R) = E[mR²] − E[R]. Hence E[R] − R_f = var^Q(R)/R_f − cov(mR, R), and if cov(mR, R) ≤ 0 the bound
   E[R] − R_f ≥ var^Q(R)/R_f = R_f·SVIX² follows.

## Data and reproducibility

* The Surface: Deribit BTC option trades on 10 and 11 December 2025.
* Weekly surfaces: Deribit trades (00:00–12:00 UTC) every Wednesday from 3 January 2024 to 26 November 2025, 100 days
  with no gaps, each built by `surface.build` and checksummed.
* Binance BTCUSDT hourly; Deribit DVOL; FRED VIXCLS.
* No strategy was tested; the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第12部分：波动率曲面

本部分讲：

* 微笑、偏斜与期限结构，以及按delta报价；
* 粘性执行价与粘性价值状态之争；
* 静态套利，以及拟合到曲面上的SSVI；
* 杜皮尔局部波动率及其远期微笑；
* 用期权重建的方差互换和VIX；
* 两年周度比特币曲面上的方差风险溢价，以及马丁的SVIX下界；
* 波动率末日与交易商伽马；
* 曲面上的变分自编码器。

*讲的是方法，不构成投资建议。*

## 交易台问题与解答

1. **为什么VIX平均高于已实现波动率？** 隐含方差是方差在Q下的价格，而方差在坏时期上升，那时边际效用高，所以方差的买方要支付溢价，
   即方差风险溢价（Carr–Wu 2009）。这里它在76%的周里为正，t为3.6。
2. **复制方差互换。** 持有每个虚值期权(2/T)·ΔK/K²份（远期以下用看跌，以上用看涨），并用远期做delta对冲（每单位方差名义本金1/F，持续再平衡）。
   这串期权就是对数合约；由伊藤公式，−2 log(S_T/S_0) + 2∫dS/S = ∫σ²dt。所以期权串加对冲支付已实现方差，期权串的成本就是公平执行价。
3. **到期前做空伽马的交易商。** 为保持delta中性，伽马空头的账本在价格上涨时买入、下跌时卖出，放大了波动；伽马多头则相反，倾向于把价格钉在大额执行价附近。

## 习题与解答

1. **杜皮尔公式。** 风险中性密度p(K, T)满足零利率下的前向（福克–普朗克）方程∂_T p = ½∂_KK(σ²_loc K² p)。因为C_KK = p，
   对K积分两次（边界项消失）得∂_T C = ½σ²_loc K² C_KK。
2. **对数合约的期权串。** 在F处带积分余项的泰勒定理给出f(S) = f(F) + f′(F)(S − F) + ∫_0^F f″(K)(K − S)⁺dK + ∫_F^∞ f″(K)(S − K)⁺dK。
   取f = −log，则f″ = 1/K²。由伊藤公式，∫_0^T σ²dt = 2∫dS/S − 2 log(S_T/S_0)。取Q期望（零利率）得K_var = (2/T)∫ OTM(K)/K² dK。
3. **SSVI的日历条件**（Gatheral–Jacquier 2014，定理4.1）。曲面无日历套利，当且仅当θ_T不减且0 ≤ ∂_θ(θφ(θ)) ≤ ((1 + √(1 − ρ²))/ρ²)·φ(θ)。
   对幂律φ = η/(θ^γ(1 + θ)^{1−γ})、γ ∈ (0, 1)，θφ = ηθ^{1−γ}/(1 + θ)^{1−γ}递增。上界的检验化为(1 − γ)/(1 + θ) ≤ (1 + √(1 − ρ²))/ρ²，
   对任何|ρ| < 1都成立。
4. **局部偏斜是隐含偏斜的两倍。** 在平值附近、短期限时，隐含波动率约为从现价到执行价的直线上局部波动率的平均（Berestycki–Busca–Florent）：
   σ_imp(k) ≈ (1/k)∫_0^k σ_loc(u)du。在k = 0处求导得σ′_imp(0) = ½σ′_loc(0)。
5. **马丁下界。** 由E^Q[X] = R_f·E[mX]和E[mR] = 1，var^Q(R) = R_f E[mR²] − R_f²；又cov(mR, R) = E[mR²] − E[R]。
   因此E[R] − R_f = var^Q(R)/R_f − cov(mR, R)；若cov(mR, R) ≤ 0，即得下界E[R] − R_f ≥ var^Q(R)/R_f = R_f·SVIX²。
