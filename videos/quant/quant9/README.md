# Quant, Built — Part 9: No Arbitrage

Part 9 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), opening Act III, Derivatives. Two ways to get the same payoff must cost the same.
From that one idea, a lecture of about 56 minutes in eighteen chapters, a hook and a closing: parity, the
fundamental theorem of asset pricing in one period and in continuous time, state prices and the risk-neutral measure,
trees, incomplete markets, changing numeraire, the density inside option prices, Ross recovery, model-free bounds by
martingale optimal transport, how arbitrage is traded, and the 2023–2026 research.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's
[`arbitrage`](../../../explainer/quant/house/arbitrage.py) checker, tested in
[`tests/test_quant_house.py`](../../../tests/test_quant_house.py)) from the Surface (Deribit BTC option trades on
10 December 2025) and, new in this part, Deribit's BTC futures trades over the same hours.

*An education in methods, not investment advice.*

## Chapters (about 57 minutes)

* **Hook: one price, and how we got here.** The desk question (call 10, put 7, strike 100, spot 103, no rates: no
  arbitrage, C − P = 3 = S − K). Parity on Deribit's inverse options, C − P = 1 − K/F: 339 call–put pairs, half within
  3.4 bp of their expiry's median forward (1.5 bp on marks), nine in ten within 9.9 bp; an implied basis of 3–5% a
  year. The era strip from Farkas (1902) to GameStop (2021); the objectives; the House.
* **1. Parity, assembled.** Definition of arbitrage and the law of one price; the long call and short put fused into a
  forward; the four-leg arbitrage at a put of 6, 200 simulated outcomes all landing on +1. **Lab:**
  `arbitrage.implied_forward` on the morning's trades. **New data:** all 62,223 Deribit BTC futures trades of the same
  hours (fetched through the data layer, checksummed in the manifest): on the 6 expiries with both, the
  options-implied forward and the dated futures agree to a median 0.66 bp of price (largest 3.6 bp).
* **2. Where parity breaks.** Parity with a borrow fee h, derived; reading h from option prices (Ofek, Richardson and
  Whitelaw 2004). Palm/3Com (2 March 2000): 3Com $81.81 against 1.525 × $95.06 = $144.97 of Palm, a stub of −$63.16
  a share; Palm short interest 147.6% of float; on 16 March a synthetic short at $39.12 against $55.25 (Lamont and
  Thaler 2003). GameStop (SEC staff report). Box spreads; Robinhood 2019. Pause: why not buy 3Com and short Palm?
* **3. The geometry of arbitrage (3D).** Payoffs in ℝ³, the orthant of payoffs that never lose, the line of zero-cost
  payoffs; a stock-price slider rotates the line and the separating plane; its normal is the state-price vector, whose
  third component hits zero at 125. The algebra: Dψ = p.
* **4. The fundamental theorem, proved and solved.** Theorem card (Harrison and Kreps 1979; Farkas 1902; Stiemke
  1915); both directions proved by separation. The price-space cone with the same slider. **Lab and replay:** the
  House's teaching `simplex` (Bland's rule) on the FTAP LP: at 100, 5 pivots to ψ = (0.385, 0.308, 0.308); at 130,
  infeasible after 6 pivots, and the phase-1 duals give the arbitrage (125 bonds, short 1 share: cost −5, payoff
  (45, 25, 0)).
* **5. State prices, the discount factor, and Q.** Arrow (1964), Ross (1978): p = Σψd = E^P[md] = E^Q[d]/(1+r),
  dQ/dP = (1+r)m. P bars morph into m and into Q; the risk-neutral simplex and the segment of martingale measures.
  **Experiment:** Bitcoin's empirical pricing kernel, Q from the Surface's 16-day density over P from 106
  non-overlapping 16-day returns (Binance, April 2021 – November 2025), 1,000 stationary-bootstrap draws: a hump,
  peaking at 1.26 near 1.06 × F and falling beyond the band on the right; the left side cannot be told from flat (the
  pricing-kernel puzzle, Jackwerth 2000).
* **6. The tree.** One-step replication in the (S, V) plane (Δ = ½, B = −40, V = 10, q = ½), derived; the four-step
  tree folding back with Δ at every node, and the hedge run along a path: the book equals the payoff on all 1,000
  paths to 1e−14. **Lab:** `trees.crr`, N = 1…200 drawn as it computes (12.44, 8.82, 10.79, 9.35, …, 9.935 at 200
  against Black–Scholes 9.948). An American put at 5% rates: exercise at 3 nodes, 7.71 against 6.87 European.
* **7. Incomplete markets: the interval as an LP.** Three states, the lid lowered onto the payoff (11.11) and the
  floor pushed up (0); the (B, Δ) plane with the level line sliding to the vertex (−44.44, 0.556); LP duality with the
  risk-neutral segment; the second FTAP (Harrison and Pliska 1981). The same `simplex` on the seller's LP agrees with
  HiGHS. The interval is constant from 3 to 33 states.
* **8. Completing the market; super-replication through time.** A digital's interval as calls are added strike by
  strike: [0, 0.779] → [0.032, 0.713] → … → [0.253, 0.338] around a true 0.290 (Ross 1976). A trinomial tree's
  super-replication chooses the outer branches (Kramkov 1996; Föllmer–Schied ch. 7): 12.44, 9.35, 9.79, 9.91, 9.94
  for N = 1, 4, 16, 64, 256 against Black–Scholes(25%) 9.948 (Avellaneda, Levy and Parás 1995; Lyons 1995).
* **9. Continuous time: Girsanov as reweighting.** Harrison–Kreps, Harrison–Pliska; the derivation of Q by Girsanov;
  150 P-paths re-weighted (not moved) into Q-paths. 200,000 paths: unweighted 16.61, weighted 9.971 ± 0.024 against
  9.948; effective sample 85.2% measured and predicted; at a 60% drift it collapses to 0.33%.
* **10. Free lunches, doubling, and bubbles.** The continuous-time doubling strategy (Dambis–Dubins–Schwarz),
  simulated on 20,000 paths with bridge-corrected crossings: 50.8% fall below −1 before winning (theory 50%), 25.0%
  below −3 (25%), 9.3% below −10 (9.1%). Admissibility; Kreps (1981), Dalang–Morton–Willinger (1990), NFLVR
  (Delbaen–Schachermayer 1994, 1998). The inverse Bessel bubble: E[S_T] = 2Φ(1/√T) − 1, simulated to four decimals;
  parity fails with a bubble (Cox and Hobson 2005).
* **11. Change of numeraire.** Geman, El Karoui and Rochet (1995); the density dQ^N/dQ derived; N(d₁) = 0.5497 and
  N(d₂) = 0.4503 as one event under two measures (the density re-weighted by s/S₀ on screen). Margrabe (1978):
  formula 11.92, Monte Carlo 11.92 ± 0.02 under Q and 11.95 ± 0.02 under Q^{S₂}. Bitcoin as numeraire: the Surface's
  107-day call at 95,000 is $8,597 under Q and 0.0915 BTC under the bitcoin measure; Q(ITM) 0.466 against 0.562.
* **12. Butterflies build the density.** The butterfly as a state price; butterflies of width 8,000 → 500 dollars
  converging to the Breeden–Litzenberger density (mass 0.99999, mean = the forward); the derivation; slope and
  curvature riding along the call curve. **Lab:** `static_checks`: 7 negative butterflies among 40 raw-trade strikes,
  7 on the Surface's median quotes, 0 on the SVI fit.
* **13. The density on the Surface.** The SVI fit replayed (`TrainingReplay`, error 3.76 → 0.156 vol points in about
  25 evaluations) with its density; SVI, calendar and Lee conditions; all 7 expiries from 9 to 289 days as a 3D ridge
  (standard deviation 7.8% → 32% of spot; skewness −0.29 at 16 days, +0.31 at 289; 0 calendar violations); four
  specifications at 107 days within 0.7 vol points of every quote, Q(down 30%) from 9.8% to 12.0%, and the spline's
  density negative (Shikhman et al. 2026: 95 of 126 pricing directions numerically null).
* **14. Ross recovery, and its critique.** The theorem derived (Perron–Frobenius). **Lab:** `power_iteration`,
  δ_k → 0.98. The synthetic test (exact to 1e−15; with a permanent component, error 0.051 and a pessimistic long run,
  −2.5% against +2.0%). Borovička–Hansen–Scheinkman (2016), Martin–Ross (2019), Qin–Linetsky (2016). Sweep over 200
  random economies: error grows smoothly with the permanent part (median 0.047 at full strength). Evidence:
  Jensen–Lando–Pedersen (2019), Jackwerth–Menner (2020), Horvath (2025).
* **15. Bounds without a model.** Convex order (Strassen 1965) on the Surface's call curves; the MOT LP and its dual
  derived (Beiglböck, Henry-Labordère and Penkner 2013; Galichon, Henry-Labordère and Touzi 2014). **3D:** the dual
  hedge surface u(x) + v(y) + h(x)(y − x) lowered onto the claim |y/x − 1|, touching where the optimal coupling sits.
  Bounds: straddle [0.1375, 0.2175] (log-normal 0.180), forward-start call exactly half, (S₂ − S₁)² a single number,
  (ln S₂/S₁)² [0.0572, 0.0741]; Hobson (1998).
* **16. Model-free bounds, computed and converging.** **Lab:** `mot_bounds`. Grid refinement 9×25 → 81×361: the band
  widens from [0.172, 0.200] to [0.127, 0.221], converging. Entropic MOT (Sinkhorn with a martingale Newton step),
  replayed as ε shrinks 0.1 → 0.003: 0.196, 0.208, 0.216, 0.2174 against the LP's 0.2175.
* **17. How arbitrage is traded, and why it is limited.** Authorized participants and the March 2020 bond-ETF
  discounts (Haddad, Moreira and Muir 2021); box rates 35 bp above Treasuries 1996–2023 (NY Fed), the 40 bp
  convenience yield (van Binsbergen, Diamond and Grotteria 2022), BOXX ($8.08 bn net assets on 30 September 2025, its
  annual report); Royal Dutch/Shell (9.53% mean deviation, 1980–1995); negative stubs (Mitchell, Pulvino and Stafford
  2002). **Simulation:** Shleifer and Vishny's limits of arbitrage: forced liquidation before certain convergence in
  0%, 2.7%, 17.5% and 64.9% of 1,000 paths as the redemption sensitivity goes 0, ½, 1, 2, and liquidation at the
  widest mispricing. Crisis file: LTCM (Federal Reserve History; the President's Working Group report).
* **18. The frontier, 2023 to 2026.** Neural MOT (Neufeld and Sester 2023), martingale Sinkhorn (Hasenbichler,
  Joseph, Loeper, Obłój and Pammer), multi-marginal MOT (Engström, Källblad and Karlsson 2024). **Trained:** a neural
  dual (u, v, h as networks, penalty method), 3 seeds × 10,000 steps: bounds 0.2194, 0.2192, 0.2191, 0.73–0.85% above
  the LP's 0.2175. Guyon (2024), Neufeld–Papapantoleon–Xiang (2023), Bartl–Beiglböck–Pammer (2026), Heston–Jacobs–Kim
  (2023).
* **The arbitrage checker, recap, desk questions, problems.** Rule 10; the trial counter stays at 308.

Hands-on: six labs (`implied_forward`, `simplex`, `crr`, `static_checks`, `power_iteration`, `mot_bounds`), replays
(simplex pivots, the SVI fit, power iteration, MOT grid walls, entropic iterations, the neural dual with three seeds),
and simulations run on screen (the arbitrage ledger, the hedge along a tree path, Girsanov re-weighting, doublers,
bubbles, the limits-of-arbitrage fund).

## Textbook audit

| Book, section | Chapter |
|---|---|
| Shreve I ch. 1, the binomial no-arbitrage model | 6 |
| Shreve I ch. 3, state prices, Radon–Nikodým | 5, 9 |
| Shreve I ch. 4, American derivatives | 6 (one beat); Parts 8 and 10 |
| Shreve I ch. 6, interest-rate assets | 11 (one line); Part 19 |
| Shreve II ch. 5, risk-neutral pricing, Girsanov, the two FTAPs | 9, 10 |
| Shreve II ch. 9, change of numéraire | 11 |
| Björk (4th ed.) ch. 2–3, binomial and general one-period models | 3–8 |
| Björk ch. 9, a primer on incomplete markets | 7–8 |
| Björk ch. 10, parity relations | 1–2 |
| Björk ch. 11–12, the martingale approach and its mathematics | 9–10 |
| Björk ch. 15, change of numeraire | 11 |
| Björk ch. 29, 34, incomplete markets, good-deal bounds | 8 (named); Part 13 |
| Duffie DAPT ch. 1, arbitrage and state prices, risk-neutral probabilities | 3–5 |
| Duffie ch. 2, the multiperiod model | 6, 9 |
| Duffie ch. 6, state prices and equivalent martingale measures in continuous time | 9–11 |
| Delbaen–Schachermayer, Part I (finite Ω, Dalang–Morton–Willinger, Kreps–Yan, NFLVR overview) | 3–4, 10 |
| Föllmer–Schied ch. 1, arbitrage, martingale measures, completeness | 3–5, 7 |
| Föllmer–Schied ch. 5, binomial model, convergence to Black–Scholes | 6 |
| Föllmer–Schied ch. 7, superhedging | 8, 15 |
| Henry-Labordère, *Model-Free Hedging* (MOT, model-independent options) | 15–16, 18 |
| Hull OFOD, binomial trees; martingales and measures | 6, 11 |
| Cochrane, *Asset Pricing* Part I (contingent claims, SDF) | 5; Part 23 |

Section titles for Duffie, Delbaen–Schachermayer and Föllmer–Schied are given at chapter level only (their exact
section lists were not checked against the books).

## Reading guide

All papers with full citations are in [`../READING.md`](../READING.md), Part 9. Each appears on screen:
Farkas 1902, Stiemke 1915 (ch 4); Arrow 1964, Ross 1978 (ch 5); Stoll 1969 (hook, ch 1); Ross 1976 (ch 8);
Breeden–Litzenberger 1978 (ch 12); Margrabe 1978 (ch 11); Cox–Ross–Rubinstein, Harrison–Kreps 1979 (ch 4, 6, 9);
Harrison–Pliska 1981 (ch 7, 9); Kreps 1981, Dalang–Morton–Willinger 1990, Delbaen–Schachermayer 1994/1998,
Cox–Hobson 2005 (ch 10); Geman–El Karoui–Rochet 1995, Jamshidian 1989 (ch 11); Avellaneda–Levy–Parás, Lyons 1995,
Kramkov 1996 (ch 8); Hobson 1998, Strassen 1965, Beiglböck–Henry-Labordère–Penkner 2013, Galichon–Henry-Labordère–Touzi
2014 (ch 15); Jackwerth 2000 (ch 5); Ofek–Richardson–Whitelaw 2004, Lamont–Thaler 2003, Mitchell–Pulvino–Stafford 2002
(ch 2, 17); Ross 2015, Borovička–Hansen–Scheinkman 2016, Martin–Ross 2019, Qin–Linetsky 2016,
Jensen–Lando–Pedersen 2019, Jackwerth–Menner 2020, Horvath 2025 (ch 14); Shleifer–Vishny 1997, Froot–Dabora 1999,
Haddad–Moreira–Muir 2021, van Binsbergen–Diamond–Grotteria 2022 (ch 17); the frontier list (ch 18). Schachermayer's
Hilbert-space proof (1992) is the README's alternative proof of chapter 4.

## Build it

```bash
python -m videos.quant.quant9.compute                         # every number, cached in .cache/quant9/ (about 10 CPU-minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant9 MOT       # one chapter, silent, with a contact sheet
python tools/make.py quant9 --cpu-voice -q m                  # English and Chinese, narrated by Kokoro on the CPU
```

`futures_basis` fetches the Deribit futures trades through `explainer.quant.data.deribit_trades(..., kind="future")`:
hour by hour, cached in `.cache/quant_data/`, each hour's SHA-256 recorded in `videos/quant/data/manifest.json`.
`neural_mot` (about 4 minutes, torch, one thread) resumes seed by seed.

## Desk questions, with solutions

1. **Call 10, put 7, K = 100, S = 103, r = 0.** C − P = 3 and S − K = 3: no arbitrage. If the put were 6
   (C − P = 4 > 3), sell the call, buy the put, buy the stock (cost 103 + 6 − 10 = 99) and borrow 99; at expiry the
   package is worth exactly 100, so you keep 1. If the put were 8, reverse every leg.
2. **A box on 100/110, one year, r = 4%.** It pays 10 in every state, so it is worth 10e^{−0.04} ≈ 9.61; buying it
   cheaper lends above 4%, selling it dearer borrows below. With American options the short leg can be exercised early,
   leaving a stock position to finance (Robinhood, 2019).
3. **A digital from two calls at 99.5 and 100.5, priced 6.20 and 5.70.** (C(99.5) − C(100.5))/1 = 0.50. As the strikes
   close in, the call spread over its width tends to −∂C/∂K = e^{−rT}Q(S_T > K), the digital's price.
4. **A parent below its stake in a listed subsidiary.** Not a riskless arbitrage: the short leg must be borrowed, may
   be recalled or be unavailable (Palm's short interest was 147.6% of float), convergence can outlast your funding, and
   in 30% of 82 cases the link was severed before the gap closed.

## Problems, with solutions

1. **Parity with a borrow fee.** A share lent out earns h, so e^{−hT} shares grow to one share. A = call + Ke^{−rT}
   bonds and B = put + e^{−hT} shares lent both pay max(S_T, K), so C + Ke^{−rT} = P + Se^{−hT}. If C − P is larger,
   sell the call, buy the put, buy and lend e^{−hT} shares, borrow the rest: a positive amount today, nothing at T.
2. **The one-period FTAP from Stiemke's lemma.** L = {(−θ·p, D^⊤θ)} ⊂ ℝ^{1+m} is a subspace; no arbitrage means
   L ∩ ℝ^{1+m}_+ = {0}. By Stiemke's lemma (separate L from the simplex), there is λ ≫ 0 orthogonal to L:
   λ₀(−θ·p) + Σ_j λ_j(D^⊤θ)_j = 0 for all θ, so p = Dψ with ψ = λ_{1:m}/λ₀ ≫ 0. Conversely p = Dψ, ψ ≫ 0, gives
   θ·p = ψ·D^⊤θ > 0 whenever D^⊤θ ≥ 0, ≠ 0. (Schachermayer 1992 gives a Hilbert-space proof.)
3. **The binomial probability.** Replicating both states gives V = e^{−rΔt}(qV_u + (1 − q)V_d) with
   q = (e^{rΔt} − d)/(u − d) ∈ (0, 1) iff d < e^{rΔt} < u; otherwise the stock dominates the bond in every state or
   the reverse.
4. **Butterflies and the density.** C′(K) = −e^{−rT}∫_K^∞ q, C″(K) = e^{−rT}q(K); the butterfly over h² is the second
   difference of C, which tends to C″(K) by Taylor's theorem.
5. **The trinomial interval.** With S ∈ {80, 100, 125}, the call pays (0, 0, 25). The cheapest dominating portfolio
   rests on states 1 and 3: Δ = 5/9, B = −400/9, cost 100/9 ≈ 11.11; the dual's q = (5/9, 0, 4/9) gives 25 × 4/9. The
   richest dominated portfolio is zero (q → (0, 1, 0)). The interval is (0, 100/9), open since strictly positive
   measures never reach its ends.
6. **The forward-start call's band.** (R − 1)^+ = ½|R − 1| + ½(R − 1), and for any martingale coupling
   E[R − 1] = E[(S₂ − S₁)/S₁] = E[E[S₂ − S₁ | S₁]/S₁] = 0, so every model's forward-start call price is half its
   straddle price, and the sup and inf halve.
7. **Margrabe.** With asset 2 as numeraire, V₀/S²₀ = E^{Q^{S²}}[(R_T − 1)^+], R = S¹/S² a Q^{S²}-martingale with
   d ln R volatility σ_R² = σ₁² + σ₂² − 2ρσ₁σ₂ (Itô on a ratio), so V₀ = S¹₀N(d₁) − S²₀N(d₂) with
   d₁,₂ = (ln(S¹₀/S²₀) ± σ_R²T/2)/(σ_R√T).

## Data and reproducibility

* The Surface: Deribit BTC option trades on 10 December 2025, 00:00–12:00 UTC; the futures trades of the same hours
  (new in this part); Binance BTCUSDT daily closes (for P in chapter 5). All checksummed in
  [`../data/manifest.json`](../data/manifest.json).
* Synthetic and labelled as such on screen: the one-period markets, the Ross economies, the doubling and bubble
  simulations, the trinomial super-replication, the limits-of-arbitrage fund. Every random choice is seeded.
* Published numbers and their sources: GameStop (SEC staff report, October 2021); Palm/3Com (Lamont and Thaler 2003;
  Chicago Booth Review); box rates (NY Fed Liberty Street Economics, October 2023); BOXX (annual report on Form N-CSR,
  30 September 2025); Royal Dutch/Shell (RBA RDP 2003-06); LTCM (Federal Reserve History; President's Working Group,
  April 1999).
* No strategy was tested; the trial counter stays at 308.

---

# 量化金融，从零搭建 — 第9部分：无套利

衍生品篇的开篇：得到同一收益的两种方法必须同价。由这个想法出发，约56分钟、十八章加开场与结尾：平价关系；单期与连续时间中的资产定价基本定理；
状态价格与风险中性测度；二叉树；不完备市场；计价单位变换；期权价格里的密度；罗斯复原；用鞅最优传输得到不依赖模型的界；业界如何做套利；
以及2023—2026年的研究前沿。

数据是Deribit在2025年12月10日的比特币期权成交（"曲面"），以及本部分新增的同一时段比特币期货成交。

*讲的是方法，不构成投资建议。*

## 各章（约57分钟）

* **开场：同一个价格。** 交易台问题；Deribit反向期权的平价C − P = 1 − K/F：339对，一半与中位数相差3.4个基点以内；隐含基差每年3%—5%。从法卡斯（1902）到游戏驿站（2021）的时间线。
* **1. 平价，亲手拼出来。** 套利与一价定律；看涨加看跌拼成远期；看跌为6时四条腿锁定1元。**实验：** `implied_forward`。**新数据：** 同时段62,223笔期货成交，6个到期日上期权隐含远期与期货的差中位数0.66个基点。
* **2. 平价在哪里失效。** 借券费用h下的平价；Palm/3Com：每股3Com隐含−63.16美元；借券稀缺的价格；游戏驿站；箱式组合与罗宾汉2019。
* **3. 套利的几何（三维）。** 收益空间、非负象限、零成本收益直线、分离平面；法向量就是状态价格。
* **4. 基本定理：证明与求解。** 两个方向的证明；价格空间中的锥；**实验与回放：** 教学用单纯形法，100时5次转轴得到状态价格，130时6次转轴后不可行，对偶给出套利组合。
* **5. 状态价格、贴现因子与Q。** P柱变为m再变为Q；风险中性单纯形；比特币的经验定价核：呈驼峰形。
* **6. 二叉树。** 单步复制；四步树倒推并沿路径对冲，1,000条路径误差1e−14；**实验：** `crr`，N到200收敛到9.948；美式看跌。
* **7. 不完备市场：区间即线性规划。** 盖子与地板；(B, Δ)平面；对偶；第二基本定理。
* **8. 让市场完备；跨时间的超复制。** 逐个加入看涨期权，数字期权区间收缩到[0.253, 0.338]；三叉树超复制价格收敛到最宽波动率下的布莱克—斯科尔斯。
* **9. 连续时间：哥萨诺夫即重新加权。** 200,000条路径，加权价9.971 ± 0.024；有效样本85.2%。
* **10. 免费午餐、加倍策略与泡沫。** 加倍策略模拟：50.8%跌破−1；可容许性；NFLVR；逆贝塞尔泡沫与平价失效。
* **11. 计价单位变换。** N(d₁)与N(d₂)；马格雷布公式；以比特币为计价单位。
* **12. 蝶式价差拼出密度。** 宽度8,000到500美元的蝶式收敛到BL密度；**实验：** `static_checks`：原始成交有7个负蝶式，SVI拟合为0。
* **13. 曲面上的密度。** SVI拟合回放；7个到期日的三维密度山脊；四种设定下30%下跌的概率相差2.2个百分点。
* **14. 罗斯复原及其批评。** 幂迭代；合成经济中的检验；BHS批评；200个随机经济的误差扫描；实证证据。
* **15. 不依赖模型的界。** 凸序；MOT线性规划与对偶；**三维：** 对冲曲面落到收益曲面上，接触集即最优耦合。
* **16. 不依赖模型的界：计算与收敛。** 网格加密，区间从[0.172, 0.200]扩展到[0.127, 0.221]；熵正则化迭代收敛到线性规划值。
* **17. 套利怎样做，为什么受限。** ETF授权参与者与2020年3月；箱式利率与BOXX；荷兰皇家/壳牌；负残值；施莱弗—维什尼模拟；LTCM。
* **18. 研究前沿。** 神经网络对偶（3个种子，高于线性规划0.73%—0.85%）；鞅Sinkhorn；多边际MOT；Guyon；多资产界；适应Wasserstein。
* **结尾。** 套利检查器、十句回顾、四个交易台问题、七道习题。

## 交易台问题与解答

1. **看涨10、看跌7、执行价100、现价103、利率为零。** C − P = 3 = S − K：没有套利。若看跌为6，卖出看涨、买入看跌、买入股票（成本99）并借入99，到期组合恰值100，留下1。若看跌为8，把每一腿反过来。
2. **100/110的一年期箱式组合，利率4%。** 在每种状态下支付10，价值10e^{−0.04} ≈ 9.61；它是一笔贷款。用美式期权时，空头腿可能被提前行权（罗宾汉，2019）。
3. **用执行价99.5和100.5、价格6.20和5.70的两个看涨期权给数字期权定价。** (6.20 − 5.70)/1 = 0.50；执行价靠拢时，价差除以宽度趋于−∂C/∂K = e^{−rT}Q(S_T > K)。
4. **母公司市值低于其所持上市子公司股份的价值。** 不是无风险套利：空头腿要借券，可能被召回或借不到，收敛可能比融资期限更久，82个案例中30%在价差收敛前联系就被切断。

## 习题与解答

1. **含借券费用的平价。** 出借的股票赚取费用h，e^{−hT}股增长为一股。组合A（看涨加Ke^{−rT}债券）与组合B（看跌加出借的e^{−hT}股）在T都支付max(S_T, K)，所以C + Ke^{−rT} = P + Se^{−hT}。
2. **由施蒂姆克引理证明单期基本定理。** L = {(−θ·p, D^⊤θ)}是子空间；无套利即L与非负象限只交于0。由施蒂姆克引理存在与L正交的λ ≫ 0，于是p = Dψ，ψ = λ_{1:m}/λ₀ ≫ 0。反之，p = Dψ、ψ ≫ 0时，任何D^⊤θ ≥ 0且不为0的θ都有θ·p > 0。
3. **二叉树概率。** 复制两种状态得V = e^{−rΔt}(qV_u + (1 − q)V_d)，q = (e^{rΔt} − d)/(u − d)，它在(0, 1)中当且仅当d < e^{rΔt} < u。
4. **蝶式价差与密度。** C′(K) = −e^{−rT}∫_K^∞ q，C″(K) = e^{−rT}q(K)；蝶式价差除以h²是二阶差分，由泰勒定理趋于C″(K)。
5. **三叉区间。** 收益(0, 0, 25)；最便宜的超复制落在状态1和3上：Δ = 5/9，B = −400/9，成本100/9；对偶q = (5/9, 0, 4/9)。下界为0。区间(0, 100/9)是开的。
6. **远期开始看涨期权的区间。** (R − 1)^+ = ½|R − 1| + ½(R − 1)，而对任何鞅耦合E[R − 1] = 0，所以每个模型中远期看涨价格都是跨式价格的一半，上下界也减半。
7. **马格雷布公式。** 以资产2为计价单位，V₀/S²₀ = E^{Q^{S²}}[(R_T − 1)^+]，R = S¹/S²是鞅，波动率σ_R² = σ₁² + σ₂² − 2ρσ₁σ₂，所以V₀ = S¹₀N(d₁) − S²₀N(d₂)。

## 数据与可复现性

* 曲面：Deribit 2025年12月10日00:00—12:00 UTC的比特币期权成交；同时段期货成交（本部分新增）；币安BTCUSDT日收盘价。全部在数据清单中记录校验和。
* 合成数据在屏幕上标注：单期市场、罗斯经济、加倍与泡沫模拟、三叉超复制、套利受限基金。所有随机数都设定了种子。
* 本部分没有检验任何策略；试验计数器保持308。
