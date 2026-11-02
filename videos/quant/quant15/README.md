# Quant, Built — Part 15: Exotics and Structured Products

Part 15 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It covers:

* the structuring business: who builds notes, who buys them, and the margin in between;
* barriers, the reflection principle and the discrete-monitoring correction;
* digitals and the call-spread hedge, Asians with a control variate, and lookbacks;
* the snowball (雪球): its fair coupon, the knock-in cliff, and the dealer's delta and vega;
* January 2024 rebuilt on the real CSI 500 path, and Korea's HSCEI-linked ELS;
* worst-of options and correlation;
* uncertain volatility and model reserves;
* a neural surrogate that reprices a book of snowballs.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`exotics`](../../../explainer/quant/house/exotics.py) pricer, tested). The data are daily closes of the China
Southern CSI 500 ETF (510500.SS) and the HSCEI from Yahoo Finance, checksummed.

*An education in methods, not investment advice. Firms and episodes are described from the public record.*

## Chapters (about 55 minutes)

* **The snowball.** The CSI 500 from 2021, the knock-in levels of notes sold in 2022–2023, and January 2024. Then
  the objectives and the House.
* **1. The structuring business.**
  * A note is a zero-coupon bond plus options, priced at fair value plus the issuer's margin.
  * Henderson and Pearson (2011) found Morgan Stanley's US retail notes priced about 8% above fair value.
  * Célérier and Vallée (2017) found European banks raising headline rates through complexity.
  * Buyers, issuers, and why the issuers' hedging is crowded.
* **2. Barriers.**
  * The reflection principle and the down-and-out call (Merton 1973; Reiner–Rubinstein 1991).
  * A barrier watched monthly is worth 7.44, against 7.28 for the continuous formula. Broadie–Glasserman–Kou's shift
    (β ≈ 0.5826) matches Monte Carlo at every frequency to within 0.01.
  * Just above the barrier the hedge still holds 0.43 units, all of it sold on the touch.
* **3. Digitals, Asians and lookbacks.**
  * The digital's delta at the strike: 0.06 a month out, 0.25 a day out, 0.67 an hour out.
  * The call-spread overhedge by width.
  * The arithmetic Asian is worth 6.20, against 10.87 for the vanilla. The geometric Asian, used as a control variate
    (Kemna–Vorst 1990), cuts the noise about 21 times.
  * Lookback: 19.3 watched continuously (Goldman–Sosin–Gatto 1979), 18.5 at daily closes.
* **4. The snowball.**
  * Terms: knock-out at 103% monthly after a 3-month lock-up, knock-in at 75% daily, 24 months.
  * The fair coupon rises from 3.9% at 12% volatility to 26.6% at 32%. At the CSI 500's 2021–2023 volatility (20%)
    it is 13.4%.
  * The note's value surface over (spot, time).
  * The dealer's hedge peaks at 1.7 times notional just above the knock-in and falls to about 1.15 below it. The
    dealer's vega is long above the barrier and slightly short below it.
* **5. January 2024.**
  * The CSI 500 fell 18% from 29 December to 5 February.
  * Bloomberg reported about $13 bn of snowballs near their loss triggers (11 January); UBS estimated the market at
    about $50 bn. Regulators curbed the product in April.
  * A stylized book of 36 monthly notes, followed on the real path: 11 knocked in between 22 January and 5 February.
    The dealers' hedge, priced daily by the surrogate, grew from 15 to 25 notes' worth of futures, then was cut to 15
    at the low.
  * The debate: Risk.net against the sceptics.
* **6. Korea's ELS.**
  * Stylized 3-year step-down ELS on the HSCEI issued monthly in 2021. Six of twelve knocked in and lost 38–54% at
    maturity in 2024.
  * The record: 19.3 tn won outstanding in November 2023; 1.2 tn won lost in January–February 2024; the FSS's
    compensation scheme; 20–50% of losses repaid.
* **7. Worst-of, and correlation.** A worst-of put on the CSI 500 and the HSCEI is worth 0.169 at correlation −0.2
  and 0.115 at 1. The measured correlation was 0.46. The dealer is short correlation; the correlation skew.
* **8. Uncertain volatility.**
  * Avellaneda–Levy–Parás (1995) and Lyons (1995): the Black–Scholes–Barenblatt equation.
  * A 95–105 call spread with volatility anywhere in 15–35%: bounds [0.31, 0.62], against 0.45–0.48 for
    Black–Scholes anywhere in the band. Model reserves.
* **9. A neural pricer.**
  * An MLP trained on 3,000 Monte Carlo snowball prices.
  * Error 0.017 per unit notional against fresh 40,000-path Monte Carlo, at 0.4 µs against 3 s per price.
* **10. The exotics pricer.** Rule 15: price every note under at least two models, hold a reserve for the gap, and
  simulate the hedge through the worst path on record, including the barrier day. The trial counter stays at 73.
* **Recap, desk questions, problems.**

## Build it

```bash
python -m videos.quant.quant15.compute                    # every number (the snowball and surrogate items take minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant15 Snowball   # one chapter, silent, with a contact sheet
python tools/make.py quant15 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **A digital as a call spread.**
   * Buy the K − ε call and sell the K call, ×1/ε. It pays at least the digital everywhere.
   * The extra cost is about ε/2 times the risk-neutral density at K.
   * Its delta is bounded by 1/ε. Wider is dearer but hedgeable.
   * Near expiry the hedge still swings, but within a band the desk can trade.
2. **The snowball issuer's vega.**
   * The issuer is long the down-and-in put the buyer sold: more volatility makes a knock-in likelier, so the issuer
     is long vega.
   * Once knocked in, the put has become a forward-like position, and the vega collapses (and here turns slightly
     short).
   * The issuer offsets long vega by selling options. That supply of vega depresses implied volatility on the
     underlying.
3. **A worst-of on three indices.** You own the put on the worst performer, so you are short correlation. No market
   quotes that input directly, and in a crash correlations jump toward one: your marks move on a number you cannot
   hedge. Desks charge for it through a correlation skew and a reserve.

## Problems, with solutions

1. **Reflection.**
   * With r = q = 0, a path that touches H and ends at S_T > K has a mirror image ending at H²/S_T, which is below
     H²/K.
   * Counting the touched paths and scaling by S/H (the change of measure that keeps the mirrored path a martingale)
     gives DOC = C(S, K) − (S/H) C(H²/S, K).
2. **BGK.**
   * Between monitoring dates the path can cross and return unseen.
   * Siegmund's corrected diffusion approximation shows the overshoot of a random walk at its first passage has a
     limiting mean of β σ√Δt, with β = −ζ(½)/√(2π).
   * So the discrete barrier acts like a continuous one moved away by that amount.
3. **Geometric average.**
   * log G = (1/n) Σ log S_{t_i} is a sum of Gaussians: Gaussian with mean log S₀ + (r − q − σ²/2) t̄.
   * Its variance is σ² Σ_{i,j} min(t_i, t_j)/n².
   * Black–Scholes with these moments gives the closed form.
4. **The call spread's bound.**
   * The payoff (S − K + ε)⁺ − (S − K)⁺, over ε, equals 1 for S ≥ K, (S − K + ε)/ε on [K − ε, K], and 0 below.
   * It is never less than 1_{S>K}, so it dominates the digital, and it converges as ε → 0.
5. **The snowball taken apart.**
   * Notional repaid unless knocked in and below 1 at maturity: a zero-coupon bond minus a down-and-in put.
   * The coupons: a strip of claims contingent on knock-out or survival without knock-in.
   * The buyer is short the put, so short vega, apart from a small long-vega piece in the coupons. The issuer is the
     reverse.

## Data and reproducibility

* China Southern CSI 500 ETF (510500.SS), China CSI 1000 ETF (512100.SS) and the HSCEI (^HSCE), daily closes, from
  Yahoo Finance's chart API (CSI index levels themselves have no history there); 2015–2025, checksummed.
* The snowball book, the Korean notes and the surrogate are stylized and labelled so; the episodes' facts come from
  Bloomberg, Reuters (via Asia Financial), Risk.net, StructuredRetailProducts and the Korean press.
* No strategy was tested; the trial counter is unchanged at 73.

---

# 量化金融，从零搭建 — 第15部分：奇异期权与结构化产品

本部分讲：

* 结构化业务：谁构造票据，谁买，中间的利润；
* 障碍期权、反射原理与离散观察修正；
* 数字期权与看涨价差对冲、带控制变量的亚式期权，以及回望期权；
* 雪球：公平票息、敲入悬崖，以及交易商的delta与vega；
* 在中证500真实路径上重建2024年1月，以及韩国挂钩国企指数的ELS；
* 最差表现期权与相关性；
* 不确定波动率与模型准备金；
* 给一本雪球重新定价的神经网络替代模型。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录。*

## 交易台问题与解答

1. **用看涨价差做数字期权。**
   * 买入K − ε看涨、卖出K看涨，乘以1/ε。它在任何地方的赔付都至少和数字期权一样多。
   * 额外成本约为ε/2乘以K处的风险中性密度。
   * delta不超过1/ε。越宽越贵，但越能对冲。
   * 临近到期时对冲仍会摆动，但在交易台能执行的范围内。
2. **雪球发行人的vega。**
   * 发行人持有买方卖出的向下敲入看跌期权：波动率越高，敲入越可能，所以发行人做多vega。
   * 敲入之后，看跌期权变成类似远期的头寸，vega崩塌（这里甚至略为空头）。
   * 发行人通过卖出期权来抵消做多的vega，这种vega供给压低了标的的隐含波动率。
3. **挂钩三个指数的最差表现。** 你持有表现最差者的看跌期权，所以做空相关性。没有市场直接报价这个输入，而崩盘时相关性跳向一：
   你的估值随一个无法对冲的数字变动。交易台通过相关性偏斜和准备金来收费。

## 习题与解答

1. **反射。**
   * r = q = 0时，一条触及H并收于S_T > K的路径有一条收于H²/S_T的镜像，而H²/S_T低于H²/K。
   * 计数被触及的路径，并乘以S/H（让镜像路径保持为鞅的测度变换），得DOC = C(S, K) − (S/H) C(H²/S, K)。
2. **BGK修正。**
   * 在两个观察日之间，路径可能越过又回来而不被看见。
   * Siegmund的修正扩散近似表明，随机游走首次穿越时的超出量极限均值为β σ√Δt，β = −ζ(½)/√(2π)。
   * 所以离散障碍的作用相当于一个向外移动这么多的连续障碍。
3. **几何平均。**
   * log G = (1/n) Σ log S_{t_i}是高斯变量之和，均值为log S₀ + (r − q − σ²/2) t̄。
   * 方差为σ² Σ_{i,j} min(t_i, t_j)/n²。
   * 代入布莱克-斯科尔斯即得闭式解。
4. **看涨价差的界。**
   * 收益(S − K + ε)⁺ − (S − K)⁺除以ε，在S ≥ K时为1，在[K − ε, K]上为(S − K + ε)/ε，以下为0。
   * 它不小于1_{S>K}，所以占优于数字期权，并在ε → 0时收敛。
5. **拆开雪球。**
   * 除非敲入且到期时低于1，本金都会偿还：零息债券减去向下敲入看跌期权。
   * 票息：一串以敲出、或未敲入而存续为条件的权益。
   * 买方做空看跌期权，所以做空vega，票息中只有一小部分做多vega。发行人正好相反。
