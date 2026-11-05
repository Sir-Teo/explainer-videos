# Quant, Built — Part 35: Who Trades With Whom

Part 35 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act VI, Market Microstructure, built to the series' PhD layer. It
asks:
* who is on the other side of a trade: dealers, informed traders, noise traders and other algorithms;
* what their orders reveal;
* what that costs everyone else.

Theory is derived and simulated. Measurement uses Binance's public one-minute bars, whose taker-buy volume gives the
signed order flow directly:
* BTCUSDT spot and its USD-margined perpetual, 2021–2024;
* five coins in 2024.

It also uses Yahoo Finance's daily bars for ten US ETFs (2015–2020).

The part covers:

* **The dealer's problem:**
  * Garman's (1976) random-walk inventory;
  * Ho and Stoll's (1981) quote shading;
  * Avellaneda–Stoikov's optimal spread;
  * today's dealers;
  * the three components of a spread.
* **Glosten and Milgrom (1985):** ask = E[V | buy]; the spread equals the informed share at an even prior; learning in
  odds; spreads around news; lemons.
* **Kyle (1985):**
  * the one-auction equilibrium derived, β = σ_u/σ_v and λ = σ_v/(2σ_u), checked by Monte Carlo and by deviation;
  * the N-auction recursion computed;
  * tightness, depth and resiliency;
  * Kyle against Glosten–Milgrom;
  * who Kyle's insiders are (Collin-Dufresne and Fos 2015).
* **Measuring liquidity from prices:**
  * Roll, Corwin–Schultz and Amihud on ten ETFs, and why daily spread estimators fail on liquid funds;
  * effective, realised and impact spreads.
* **Kyle's lambda, measured on Bitcoin:**
  * its level and fit;
  * its concavity and the square-root law;
  * the persistence of order flow against unpredictable returns;
  * λ by month and by hour, across coins and across horizons.
* **Toxic flow:** PIN and its troubles; bulk-volume VPIN, tested against the true taker imbalance; markouts.
* **Price discovery:** Hasbrouck's information shares between spot and perpetual, with the bounds' width and the
  lead-lag; the funding basis; Hasbrouck's NYSE result.
* **Market structure:**
  * Reg NMS and the NBBO;
  * maker-taker pricing, venues, dark pools (Zhu 2014) and segmentation;
  * the 2024 tick and fee amendments, IEX and the closing auction;
  * T+1;
  * an order's journey.
* **High-frequency traders:** Menkveld (2013); Hendershott, Jones and Menkveld (2011); Brogaard, Hendershott and
  Riordan (2014); sniping (Budish, Cramton and Shim 2015) and its measured tax (Aquilina, Budish and O'Neill 2022);
  back-running (Yang and Zhu 2020); manipulation.
* **When liquidity vanishes:**
  * 6 May 2010 (the CFTC–SEC report; Kirilenko, Kyle, Samadi and Tuzun 2017);
  * Bitcoin's daily λ;
  * liquidation cascades;
  * 15 October 2014;
  * frequent batch auctions.
* **For the researcher: Kyle in continuous time (Kyle 1985; Back 1992).**
  * Lemmas on the Kalman–Bucy filter and Back's value function; the HJB check; the theorem.
  * The two filtrations and the Brownian bridge; intensity and horizon.
  * Simulations; the discrete limit; a test against Bitcoin's R².

No strategy is registered in this part; the trial counter stands at 23,550.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: what an insider's orders reveal** (2.3). A continuous Kyle market; three findings; where this sits; fifty
  years; the plan.
* **1. The dealer's problem** (3.2).
  * Inventory is a random walk without shading (sd 85 units against 3.2 with γ = 0.05).
  * The mean/spread of P&L across runs rises from 3.1 to 43.
  * Avellaneda–Stoikov; today's dealers; three components.
* **2. Glosten and Milgrom** (3.6).
  * The quotes, with μ = 0.3: bid 0.35 and ask 0.65 at p = 0.5; at p = 0.8, bid 0.683 and ask 0.881.
  * 400 runs: belief past 99% after a median 22 trades. In odds, about 7 net buys, so about 25 trades.
  * News; lessons.
* **3. Kyle** (4.5).
  * The model, guess, best response and theorem; checks (profit 0.499 against 0.5; noise loss 0.500).
  * Deviation parabola; N auctions (λ_1 0.50 → 0.99, Σ_{1/2} 0.75 → 0.51).
  * Liquidity's three dimensions; the two models compared; who the insiders are.
* **4. Measuring the spread from prices alone** (3.9).
  * Roll's bounce, and its power: T ≈ 10¹² days for SPY.
  * SPY Roll 99 bp and Corwin–Schultz 22 bp, against a true third of a basis point; n/a for HYG and GLD.
  * Amihud against dollar volume: slope −0.94, correlation −0.90.
  * Effective, realised and impact spreads.
* **5. Kyle's lambda, measured** (4.9).
  * λ = 4.61 bp per $1m of net taker flow (t = 757, R² 0.21; flow sd $0.93m a minute).
  * Concave: about 12–17 bp per $1m for small minutes, 7 for the largest. Reconciled with the square-root law.
  * Flow autocorrelation 0.18 at one minute and 0.004 at four hours; returns ≈ 0.
  * By month 2.2–8.2, correlation +0.21 with volatility; by hour.
  * Across coins: BTC 3.5, ETH 7.9, SOL 19.6, DOGE 26.9, XRP 30.9 bp per $1m; log slope on σ_r/σ_flow 0.91.
  * Horizons: λ 4.6 → 3.2 and R² 0.21 → 0.32 from 1 minute to 1 hour.
* **6. Toxic flow: PIN and VPIN** (3.3).
  * PIN and its troubles; VPIN with bulk classification.
  * Four years of BTC VPIN (mean 0.18).
  * The May 2021 and FTX crashes: VPIN rises with the crash, not before.
  * Correlation 0.67 with realised volatility and 0.09 with the true taker imbalance; markouts.
* **7. Price discovery across markets** (3.2).
  * The VECM and information shares.
  * Spot and perpetual one-minute returns correlate 0.987, and the IS bounds average 0.95 wide.
  * Lead correlations +0.020 (perp → spot) and +0.001; the perp trades 5.3× spot's dollar volume.
  * Hasbrouck's NYSE; the funding basis (−5 to +14 bp a month).
* **8. Market structure** (4.6). Reg NMS; maker-taker; venues; dark pools; segmentation; the 2024 amendments; the
  closing auction; T+1; an order's journey.
* **9. High-frequency traders as market makers** (2.9). Menkveld; the evidence; sniping; back-running; the race tax;
  manipulation.
* **10. When liquidity vanishes** (4.0).
  * The flash crash and its mechanics; after.
  * Bitcoin's daily λ: median 5.3, worst days 2022, correlation 0.31 with volatility.
  * Cascades; 15 October 2014; batch auctions and their arithmetic (0.12 ticks).
* **11. Rule 35: know who is on the other side** (3.0). The first sheet; the House's footprint; labs (`gm_quotes`,
  `kyle_lambda`, `hasbrouck_is`, `kyle_continuous`); the module; Rule 35; three cases.
* **For the researcher: Kyle in continuous time** (5.9). The setup; three lemmas; the HJB check; the theorem; two
  views; bridges; variance (600 markets) and profit (0.989 against 1); the discrete limit; intensity; comparison; a
  test against data; related; open problems.
* **Recap, desk questions, problems** (3.4). Fourteen lines; six desk questions; the pause questions answered; twelve
  problems, two of qualifying-exam level, solved below.

## Hands-on

* **Built and run here:**
  * an inventory dealer;
  * Glosten–Milgrom quotes and markets;
  * Kyle's one-shot, N-auction and continuous models;
  * Roll, Corwin–Schultz and Amihud;
  * Kyle's λ from Binance taker flow by month, hour, size, coin and horizon;
  * flow autocorrelation;
  * bulk-volume VPIN against the true imbalance;
  * Hasbrouck information shares;
  * daily λ.
* **Labs, from the House's source:** `gm_quotes`, `kyle_lambda`, `hasbrouck_is`, and `kyle_continuous`.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| O'Hara, *Market Microstructure Theory* (1995) | inventory, sequential trade, Kyle | 1–3 |
| Hasbrouck, *Empirical Market Microstructure* (2007) | Roll, price impact, information shares | 4, 5, 7 |
| Foucault, Pagano and Röell, *Market Liquidity* (2013) | measures, market structure, HFT | 4, 8, 9 |
| Harris, *Trading and Exchanges* (2003) | order types, venues, dealers | 1, 8 |

## Papers, chapter by chapter

* ch. 1: Garman (1976), *JFE*; Ho and Stoll (1981), *JFE*; Avellaneda and Stoikov (2008), *Quantitative Finance*.
* ch. 2: Glosten and Milgrom (1985), *JFE*; Akerlof (1970), *QJE*.
* ch. 3: Kyle (1985), *Econometrica*; Collin-Dufresne and Fos (2015), *JF*.
* ch. 4: Roll (1984), *JF*; Corwin and Schultz (2012), *JF*; Amihud (2002), *JFM*.
* ch. 5: Lillo and Farmer (2004) on the persistence of order flow; the square-root law of Part 31.
* ch. 6: Easley, Kiefer, O'Hara and Paperman (1996), *JF*; Easley, Lopez de Prado and O'Hara (2012), *RFS*; Andersen and
  Bondarenko (2014), *JFM*; Duarte and Young (2009), *JFE*.
* ch. 7: Hasbrouck (1995), *JF*; Gonzalo and Granger (1995).
* ch. 8: Regulation NMS (2005); the SEC's 2024 amendments on tick sizes and access fees; Zhu (2014), *RFS*; T+1 (2024).
* ch. 9: Menkveld (2013), *JFM*; Hendershott, Jones and Menkveld (2011), *JF*; Brogaard, Hendershott and Riordan (2014),
  *RFS*; Budish, Cramton and Shim (2015), *QJE*; Aquilina, Budish and O'Neill (2022), *QJE*; Yang and Zhu (2020), *RFS*.
* ch. 10: the CFTC–SEC report on 6 May 2010; Kirilenko, Kyle, Samadi and Tuzun (2017), *JF*; the joint staff report on
  15 October 2014 (2015).
* Research: Kyle (1985); Back (1992), *RFS*; Holden and Subrahmanyam (1992), *JF*; Back and Baruch (2004),
  *Econometrica*.

## For the researcher

* **The theorem.**
  * Setting: v ~ N(p_0, Σ_0) is known to the insider; total flow is dY = θ dt + σ_u dW; the price is
    p_t = E[v | F^Y_t].
  * The equilibrium on [0, 1] has λ = √Σ_0/σ_u, θ_t = (v − p_t)/(λ(1 − t)), Σ_t = Σ_0(1 − t), and E π = √Σ_0 σ_u.
  * To the market the price is a martingale with volatility √Σ_0; to the insider it is a Brownian bridge to v.
* **The proof.**
  * Lemma 1 (Kalman–Bucy): with θ = β_t(v − p), dp = λ_t dY, λ_t = β_tΣ_t/σ_u², and dΣ/dt = −λ_t²σ_u².
  * Lemma 2 (Back): J(t, p) = ((v − p)² + λ²σ_u²(1 − t))/(2λ) solves the HJB equation for every θ, so any strategy is
    optimal that leaves J(1, p) = 0.
  * Lemma 3: a constant λ with Σ_1 = 0 forces λ = √Σ_0/σ_u, and the bridge strategy is the one that makes p_1 = v.
* **Measured.**
  * Simulated Var(v − p_t) follows 1 − t, and the insider's profit is 0.989 against 1.
  * Kyle's recursion converges to the limit: λ_1 = 0.988 and Σ_1 = 0.0056 at N = 256.
  * On Bitcoin, Kyle's implied R² = 1 meets 0.21–0.32: the rest is public information.
* **Simplifications.**
  * Normal values and noise, one insider, a risk-neutral market maker.
  * Taker volume as the signed flow (no hidden or cross-venue flow).
  * One-minute bars only, which is why the information shares are uninformative.
* **Open problems.**
  * Equilibria with public and private information together, matching the R².
  * Strategic noise traders.
  * An insider choosing among lit, dark and derivative venues.

## Build it

```bash
python -m videos.quant.quant35.compute                            # every item; a few minutes, ~0.4 GB of Binance bars
python -m pytest -q tests/test_quant_house.py -k micro
EXPLAINER_TTS=silent python tools/qa_scene.py quant35 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant35                                      # the narrated part
```

## Desk questions, with solutions

1. **Why a spread with competitive, risk-neutral dealers?** Adverse selection. Zero profit on each side means
   ask = E[V | buy] and bid = E[V | sell]; at p = ½ the spread is μ.
2. **Kyle's lambda?** The price impact of a unit of net flow. In one auction, λ = σ_v/(2σ_u): it rises with what is
   unknown and falls with noise.
3. **Why shade quotes?** Inventory under symmetric arrivals is a random walk. Shading the mid by −γq makes trades
   mean-revert it.
4. **When does Roll fail?** When s²/4 is tiny relative to the noise in the autocovariance, σ²/√T, or to genuine
   reversal.
5. **What does VPIN measure?** Bulk-classified imbalance, which grows with |Δp|/σ by construction. On Bitcoin it
   correlates 0.67 with volatility and 0.09 with true imbalance.
6. **The flash crash?** It was made possible by:
   * a volume-targeted seller;
   * intermediaries passing inventory among themselves;
   * liquidity withdrawn as inventory risk spiked.

## Problems, with solutions

1. **Shaded dealer.** The mid is v − 40 × 0.05 = v − 2. The quotes are v − 2.5 and v − 1.5.
2. **Glosten–Milgrom after a buy (μ = 0.4).** The belief goes to (1 + μ)/2 = 0.7.
   * Ask = 0.7·0.7/(0.7·0.7 + 0.3·0.3) = 0.845.
   * Bid = 0.7·0.3/(0.7·0.3 + 0.3·0.7) = 0.5.
3. **Kyle, more noise.** σ_u → √2 σ_u: λ falls by √2, β and the order rise by √2, and the profit σ_uσ_v/2 rises by √2.
4. **Roll.** s = 2√0.0004 = $0.04.
5. **λ's cost.** 4.6 × 10 = 46 bp on the line. Concavity makes a single large order cheaper than linear, and small
   orders more costly per dollar.
6. **Bulk classification.** Φ(2) = 0.977, so about 977 BTC are "bought" and 23 "sold", whatever the true split.
7. **Information shares.** The adjustment speeds are α_A = 0.9 and α_B = 0.1. The common-trend weights are
   ψ ∝ α⊥, so B, which adjusts least, carries weight 0.9 against A's 0.1. B leads, with a share near 0.9 when the
   residuals are uncorrelated.
8. **Maker-taker.** The taker pays ½ cent plus a fee of about the rebate (0.2–0.3 cents): about three times the natural
   half-spread of 1/6 cent. A half-cent tick lets the spread narrow, which helps takers.
9. **Sniping.** s/2 ≥ 0.02 × 3, so s ≥ 0.12 ticks.
10. **Volume-targeted seller.** At 9% participation, time = 5%/(9% × volume rate). Doubling the volume halves the
    time, which accelerates the selling.
11. **(qual) Continuous Kyle.**
    * **HJB.** It reads 0 = max_θ[(v − p)θ + J_p λθ] + J_t + ½J_pp λ²σ_u². With J_p = −(v − p)/λ the θ terms cancel,
      and J_t + ½J_pp λ²σ_u² = −λσ_u²/2 + λσ_u²/2 = 0.
    * **Terminal condition.** Optimality requires J(1, p_1) = 0, that is, p_1 = v.
    * **λ.** By Lemma 1 with constant λ, Σ_1 = Σ_0 − λ²σ_u² = 0, so λ = σ_v/σ_u.
    * **Profit.** E J(0, p_0) = (Σ_0 + λ²σ_u²)/(2λ) = σ_vσ_u.
12. **(qual) One auction and horizons.**
    * **One auction.** Given λ, x* = (v − p_0)/(2λ), so β = 1/(2λ). The market maker sets
      λ = βσ_v²/(β²σ_v² + σ_u²); solving gives β = σ_u/σ_v and λ = σ_v/(2σ_u).
    * **Who pays.** The insider's E π = λ E[x²] = λβ²σ_v² = σ_uσ_v/2. The market maker breaks even, so noise traders
      lose E[(p − v)u] = λσ_u² = σ_uσ_v/2.
    * **Horizon T.** Rescale time: Σ_T = Σ_0 − λ²σ_u²T = 0 gives λ = σ_v/(σ_u√T). Then
      E π = (Σ_0 + λ²σ_u²T)/(2λ) = σ_vσ_u√T.

## Data and reproducibility

* **Binance.** Public one-minute klines with SHA-256 checksums against Binance's published files:
  * BTCUSDT spot and USD-M perpetual, 2021–2024 (2.1 million minutes);
  * BTC, ETH, SOL, XRP and DOGE spot, 2024.
  * The loader now returns `taker_buy`, the base volume bought by takers.
* **Yahoo Finance.** Daily bars for SPY, QQQ, IWM, EEM, TLT, HYG, GLD, XBI, PFF and IWC (2015–2020), frozen and
  checked.
* **No registration.** The counter stays at 23,550.
* **Quoted, not computed:**
  * the CFTC–SEC and joint staff reports;
  * the SEC's rules;
  * Menkveld; Hendershott et al.; Brogaard et al.; Aquilina et al.;
  * Hasbrouck's NYSE shares;
  * Collin-Dufresne–Fos;
  * Duarte–Young.

---

# 量化金融，从零搭建 — 第35部分：谁与谁交易

这是一套共四十三部分的量化金融系列的第35部分（见[系列计划](../README.md)与[教学大纲](../SYLLABUS.md)），也是第六幕"市场微观结构"的第一部分，按系列的博士层次构建。它问的是：

* 一笔交易的另一方是谁：交易商、知情交易者、噪声交易者，以及其他算法；
* 他们的订单透露了什么；
* 其他所有人为此付出什么代价。

理论部分加以推导和模拟。测量部分使用Binance公开的一分钟K线，其主动买入量直接给出带方向的订单流：

* BTCUSDT现货及其U本位永续合约，2021–2024年；
* 2024年的五种币。

还使用十只美国ETF的Yahoo Finance日度K线（2015–2020年）。本部分没有登记策略，计数器为23,550。

*这是方法的教育，不是投资建议。*

## 章节（约55分钟）

* **开篇：内幕交易者的订单透露了什么**（2.3）。
* **1. 交易商的问题**（3.2）。
  * 不偏移时存货是随机游走（标准差85个单位，γ = 0.05时为3.2）。
  * 各次运行损益的均值与离散度之比从3.1升到43。
  * Avellaneda–Stoikov；今天的交易商；价差的三个组成部分。
* **2. Glosten与Milgrom**（3.6）。
  * μ = 0.3时，p = 0.5处买价0.35、卖价0.65；p = 0.8处为0.683与0.881。
  * 中位数22笔交易后信念超过99%；用赔率计约7次净买入，约25笔交易。
* **3. Kyle**（4.5）。
  * 单次拍卖均衡的推导与检验（利润0.499对0.5）；偏离抛物线。
  * N次拍卖（λ_1从0.50到0.99）；流动性的三个维度；两个模型的比较；内幕交易者是谁。
* **4. 只用价格衡量价差**（3.9）。
  * Roll的反弹及其功效（SPY需约10¹²天）。
  * SPY的Roll价差99个基点、Corwin–Schultz 22个基点，真实值为三分之一个基点。
  * Amihud对美元成交量：斜率−0.94，相关系数−0.90；有效、已实现与冲击价差。
* **5. 测量Kyle的lambda**（4.9）。
  * λ = 每百万美元净主动订单流4.61个基点（R² 0.21）。
  * 凹性：小的分钟约12–17个基点每百万美元，最大的约7；订单流自相关一分钟0.18，四小时0.004，收益约为零。
  * 按月2.2–8.2；跨币种BTC 3.5、ETH 7.9、SOL 19.6、DOGE 26.9、XRP 30.9；对数斜率0.91。
  * 从一分钟到一小时，λ由4.6降到3.2，R²由0.21升到0.32。
* **6. 有毒订单流**（3.3）。
  * PIN及其问题；VPIN（均值0.18）在崩盘时而非崩盘前上升。
  * 与已实现波动率相关0.67，与真实主动不平衡相关0.09；事后损益。
* **7. 跨市场的价格发现**（3.2）。
  * 现货与永续一分钟收益相关0.987，信息份额区间平均宽0.95。
  * 领先相关+0.020对+0.001；永续成交额是现货的5.3倍；资金费率基差。
* **8. 市场结构**（4.6）。全国市场系统规则；做市-吃单收费；场所；暗池；分流；2024年修订；收盘拍卖；T+1；一笔订单的旅程。
* **9. 高频交易者**（2.9）。Menkveld；证据；狙击；反向跟单；竞赛税；操纵。
* **10. 当流动性消失时**（4.0）。闪电崩盘；比特币的日度λ（中位数5.3，最坏的日子在2022年）；连锁平仓；2014年10月15日；批量拍卖。
* **11. 第35条规则：知道对手是谁**（3.0）。
* **写给研究者：连续时间的Kyle模型**（5.9）。
* **回顾、交易台问题与习题**（3.4）。

## 写给研究者

* **定理。**
  * 设定：v ~ N(p_0, Σ_0)为内幕交易者所知，dY = θ dt + σ_u dW，p_t = E[v | F^Y_t]。
  * 均衡为λ = √Σ_0/σ_u，θ_t = (v − p_t)/(λ(1 − t))，Σ_t = Σ_0(1 − t)，E π = √Σ_0 σ_u。
  * 对市场而言价格是鞅，对内幕交易者而言是一座通向v的布朗桥。
* **证明。**
  * 引理1（Kalman–Bucy）：dp = λ_t dY，dΣ/dt = −λ_t²σ_u²。
  * 引理2（Back）：J = ((v − p)² + λ²σ_u²(1 − t))/(2λ)对任意θ满足HJB方程。
  * 引理3：Σ_1 = 0迫使λ = √Σ_0/σ_u。
* **测量。**
  * 模拟的Var(v − p_t)沿1 − t下降，利润0.989对1；N = 256时离散递推的λ_1 = 0.988。
  * 比特币的R² 0.21–0.32对Kyle隐含的1，其余部分是公开信息。
* **开放问题。**
  * 同时含公开与私人信息且与R²相符的均衡。
  * 策略性的噪声交易者。
  * 在多个场所之间选择的内幕交易者。

## 交易台问题与解答

1. **为什么竞争性、风险中性的交易商仍有价差？** 逆向选择：卖价 = E[V | 买入]，p = ½时价差为μ。
2. **Kyle的lambda？** 一单位净订单流的价格冲击；单次拍卖中λ = σ_v/(2σ_u)。
3. **为什么偏移报价？** 对称到达下存货是随机游走；把中点偏移−γq使其均值回复。
4. **Roll何时失效？** 当s²/4相对于自协方差的噪声σ²/√T或真实反转很小时。
5. **VPIN测量什么？** 批量分类的不平衡，按构造随|Δp|/σ增长；在比特币上与波动率相关0.67，与真实不平衡相关0.09。
6. **闪电崩盘？** 以下三者使它成为可能：
   * 按成交量比例卖出的卖家；
   * 中介在彼此之间传递存货；
   * 存货风险飙升时撤走的流动性。

## 习题与解答

1. 中点为v − 2；报价为v − 2.5与v − 1.5。
2. 信念变为0.7；卖价0.845，买价0.5。
3. σ_u乘以√2：λ除以√2，订单与利润乘以√2。
4. s = 2√0.0004 = 0.04美元。
5. 按直线46个基点；凹性使单笔大订单更便宜，小订单每美元更贵。
6. Φ(2) = 0.977：约977个"买入"、23个"卖出"，无论真实拆分如何。
7. B调整最少，领先；残差不相关时其份额接近0.9。
8. 吃单方支付半美分加约等于返佣的费用，约为自然半价差的三倍；半美分最小价位有利于吃单方。
9. s/2 ≥ 0.02 × 3，s ≥ 0.12个最小价位。
10. 成交量翻倍使时间减半，卖出随之加速。
11. **（资格考试）连续Kyle模型。** J_p = −(v − p)/λ使θ项抵消，J_t + ½J_pp λ²σ_u² = 0；最优性要求p_1 = v；由引理1得λ = σ_v/σ_u；E J(0, p_0) = σ_vσ_u。
12. **（资格考试）单次拍卖与期限。**
    * **单次拍卖。** β = 1/(2λ)，λ = βσ_v²/(β²σ_v² + σ_u²)，解得β = σ_u/σ_v、λ = σ_v/(2σ_u)。
    * **谁付钱。** 内幕交易者的利润σ_uσ_v/2等于噪声交易者的损失。
    * **期限T。** λ = σ_v/(σ_u√T)，利润σ_vσ_u√T。

## 数据与复现

* **Binance。** 公开一分钟K线，按其公布的SHA-256校验：
  * BTCUSDT现货与U本位永续，2021–2024年（210万分钟）；
  * 五种币的现货，2024年。
  * 加载器现在返回`taker_buy`。
* **Yahoo Finance。** 十只ETF的日度K线（2015–2020年）。
* **本部分没有登记。** 计数器为23,550。
