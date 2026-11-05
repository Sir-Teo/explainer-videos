# Quant, Built — Part 36: The Limit Order Book

Part 36 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act VI, Market Microstructure, built to the series' PhD layer. It
asks:
* what the queues of resting orders say about the next price;
* where fair value sits, given the book;
* what a place in the queue is worth, and what a fill tells you.

Everything is measured on Binance's public best-bid/best-offer stream (`bookTicker`) and aggregated trade tape for
the BTCUSDT perpetual:
* 16 and 17 May 2023 (weekdays, the first days of the stream in the archive) to fit;
* 20 and 21 May 2023 (a weekend) to test.

The stream is reduced to a 100-millisecond grid of best prices and sizes.

The part covers:

* **The book:**
  * price-time priority, the four events, order types;
  * spread, depth and update rates through the day;
  * large and small ticks. Bitcoin's perpetual has a one-tick spread more than 99% of the time, but when its mid moves
    between snapshots the median jump is 8 ticks, so by Dayri and Rosenbaum's measure its tick is small.
* **Queues and the next tick:**
  * Cont, Stoikov and Talreja (2010); Cont and de Larrard's (2013) P(up) = 1 − (2/π) arctan(q^a/q^b), derived from the
    harmonic measure of a quadrant;
  * against the data, P(up) rises from 16% to 86% across imbalance buckets, and the model is too steep at the edges;
  * the queue-reactive model (Huang, Lehalle and Rosenbaum 2015).
* **Events that cause events:**
  * a Hawkes fit to trades, with branching ratio 0.68 and the cluster representation;
  * near-criticality (Hardiman, Bercot and Bouchaud 2013);
  * trade-sign memory ℓ^−0.85 (Lillo and Farmer 2004) and metaorder splitting;
  * a signature plot that rises about 30% from 0.1 s to 10 s;
  * same-direction pairs of mid moves.
* **Order-flow imbalance (Cont, Kukanov and Stoikov 2014):**
  * the definition, worked by hand;
  * R² of 0.25–0.32 at 1 s, 0.37–0.45 at 10 s and 0.35–0.48 at 1 min, on every day;
  * impact against depth with slope −1.17 (theory −1);
  * multi-level, integrated and deep OFI.
* **The microprice (Stoikov 2018):**
  * the weighted mid is not a martingale;
  * the Markov-chain estimator, with every mid move counted.
  * On Bitcoin it leans ±25 ticks and fails out of sample: it is 3 to 5 times the mid's squared error at 1 s, and
    still worse at 1 min.
  * A per-horizon table of mean moves cuts the 10-s error by 3–5% on both test days.
  * Why: a small tick and a non-Markov state.
  * The interview answer, from a large-tick book: about $100.008.
* **Deep order books:**
  * DeepLOB, its architecture and labels;
  * Sirignano and Cont's universality, stationarity and path-dependence;
  * the LOBCAST re-test (Prata et al. 2024).
  * Our test on 30 inputs: next-second direction 87.2% for a linear rule against 84.0% for a network; R² under 1%.
  * The linear rule's calls capture about 1.5 ticks per second traded, against a one-tick spread and taker fees of
    several basis points (1 bp ≈ 27 ticks).
* **A book of our own:**
  * zero intelligence (Smith, Farmer, Gillemot and Krishnamurthy 2003; Farmer, Patelli and Zovko 2005);
  * the queue-reactive simulator fitted to 17 May;
  * a five-fact scorecard (after Vyetrenko et al. 2020): queue size right; move rate, burstiness, sign pairs and fat
    tails wrong.
* **Trading in the queue:**
  * a passive order replayed against the book and the tape, 6,532 orders. At the back of the queue, 82% fill within a
    minute, and the 1-s markout is −14.7 ticks. At the front, 94% fill and the markout is −1.6.
  * By queue size, the front of a long queue turns positive.
  * The value of queue position is about 11 ticks.
  * The free option (Copeland and Galai 1983) and the race to cancel.
* **Rule 36: score the book against the spread.**
* **For the researcher: the microprice theorem.**
  * The Markov-additive setting H1–H3; the first-step, strong-Markov and convergence lemmas; the theorem, the
    martingale property and uniqueness.
  * Why symmetry is needed.
  * Checks:
    * the algebra: |λ₂| = 0.668, π'g¹ ≈ 10⁻¹⁶, series against closed form 10⁻¹³;
    * the half-life of a lean;
    * the simulator, where the microprice does not drift and the realised drift reaches about 1 × g;
    * Bitcoin, where it peaks at 0.46 × g;
    * a direct test of H1: the next-sign gap given the state is −0.05 in the simulator and +0.46 on Bitcoin.

No strategy is registered in this part; the trial counter stands at 23,550.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: where is fair value?** (3.3)
  * The interview book (bid 500 at $100.00, ask 100 at $100.01).
  * Three findings; why the book matters even to slow investors; where this sits; twenty years of research; the plan.
* **1. The book** (3.9). Rules; the picture; four events; the data; a minute; a day; order types; tick size.
* **2. Queues and the next tick** (3.5). The race; the quadrant; the formula; its assumptions; the data; why the data
  are flatter; the queue-reactive fix.
* **3. Events that cause events** (4.0). Hawkes, fitted; near-criticality; the cluster representation; sign memory;
  splitting; the signature plot; same-direction pairs.
* **4. Order-flow imbalance** (3.9). The definition; two minutes; by hand; R² by horizon; impact against depth; against
  Kyle; deeper and integrated OFI.
* **5. The microprice** (5.6).
  * The pause answer; three candidates; why the weighted mid fails; the chain.
  * The fitted lean against realised moves; the out-of-sample test; the martingale test; why the theory fails here.
  * The interview; uses.
* **6. Deep order books** (5.2). DeepLOB, universal features and OFI inputs; architecture; Sirignano–Cont in detail;
  LOBCAST; labels; our test; how to read it; lessons.
* **7. A book of our own** (4.5). Why simulate; four families; zero intelligence; the fitted rates; an hour simulated;
  the scorecard; the diagnosis; three rules.
* **8. Trading in the queue** (4.9). Price-time priority; the replay; back against front; by queue size; the value of
  position; the free option; the race; how makers survive.
* **9. Rule 36** (4.3). The pause answer; the sheet; what was not measured; five labs; the module; three cases.
* **For the researcher: the microprice theorem** (7.5). Setting; three lemmas; the theorem; uniqueness; symmetry; four
  checks; related work; open problems.
* **Outro** (4.2). Thirteen lines; three lessons; six desk questions; the pause answers; twelve problems (two of
  qualifying-exam level, solved below); payoffs; references.

## Hands-on

* **Built and run here:**
  * loaders for Binance's `bookTicker` and `aggTrades` daily files;
  * imbalance, weighted mid and OFI on a grid;
  * Stoikov's microprice chain with its convergence check, and a per-horizon table of mean moves;
  * sign ACF and the signature plot; a Hawkes fit;
  * a 30-input linear rule and an MLP ensemble;
  * the queue-reactive fit and simulator with a scorecard;
  * a passive-order replay with markouts;
  * the microprice theorem's numerical checks.
* **Labs, from the House's source:** `ofi`, `microprice_fit`, `qr_simulate`, `queue_fills` and `horizon_fit`.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices* (2018) | LOB, order-flow memory, signature plots, impact | 1–4, 8 |
| Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015) | microstructure, order flow, market making | 1, 4, 8 |
| Abergel, Anane, Chakraborti, Jedidi and Toke, *Limit Order Books* (2016) | stylised facts, queue models, simulation | 2, 3, 7 |
| Gould, Porter, Williams, McDonald, Fenn and Howison, "Limit order books" (2013), *Quantitative Finance* | survey | 1, 7 |

## Papers, chapter by chapter

* ch. 1: Dayri and Rosenbaum (2015), *Market Microstructure and Liquidity*, on tick size.
* ch. 2: Cont, Stoikov and Talreja (2010), *Operations Research*; Cont and de Larrard (2013), *SIAM J. Financial Math.*;
  Huang, Lehalle and Rosenbaum (2015), *JASA*.
* ch. 3: Hawkes (1971); Hawkes and Oakes (1974); Hardiman, Bercot and Bouchaud (2013), *EPJ B*; Lillo and Farmer
  (2004), *SNDE*; Lillo, Mike and Farmer (2005), *PRE*.
* ch. 4: Cont, Kukanov and Stoikov (2014), *J. Financial Econometrics*; Xu, Gould and Howison (2018); Kolm, Turiel and
  Westray (2023), *Mathematical Finance*; Cont, Cucuringu and Zhang (2023), *Quantitative Finance*.
* ch. 5: Stoikov (2018), *Quantitative Finance*.
* ch. 6: Zhang, Zohren and Roberts (2019), *IEEE Trans. Signal Processing*; Sirignano and Cont (2019), *Quantitative
  Finance*; Ntakaris et al. (2018), *J. Forecasting*; Prata et al. (2024), *Artificial Intelligence Review*.
* ch. 7: Smith, Farmer, Gillemot and Krishnamurthy (2003), *Quantitative Finance*; Farmer, Patelli and Zovko (2005),
  *PNAS*; Byrd, Hybinette and Balch (2020), ABIDES; Vyetrenko et al. (2020) and Coletta et al. (2021), ICAIF; Nagy et
  al. (2023), ICAIF.
* ch. 8: Moallemi and Yuan (2017), on queue position; Copeland and Galai (1983), *JF*; Budish, Cramton and Shim
  (2015), *QJE*.
* Research: Stoikov (2018); Avellaneda, Reed and Stoikov (2011), *Algorithmic Finance*; Gould and Bonart (2016),
  *Market Microstructure and Liquidity*.

## For the researcher

* **The theorem (Stoikov 2018, proved here).**
  * Setting: a finite state X (imbalance bucket, spread) and the mid M.
  * H1: (X, M) is a Markov additive process, so each mid change depends only on the transition it rides on.
  * H2: mirroring the book (bid ↔ ask) maps the dynamics to themselves with ΔM → −ΔM.
  * H3: every state eventually moves (ρ(Q) < 1), and B is irreducible and aperiodic.
  * Conclusion: P^micro = lim E[M_{τ_n} | F_t] = M_t + g(X_t) exists, with g = Σ_k B^k g¹ = (1 − B + 1π')⁻¹ g¹. It
    converges at the rate |λ₂(B)|, and it is a martingale at mid-change times. It is the unique antisymmetric
    state-adjusted martingale.
* **The proof.**
  * Lemma 1 (first step): g¹ = R + Q g¹, so g¹ = (1 − Q)⁻¹ R.
  * Lemma 2 (strong Markov): the post-move law is B = (1 − Q)⁻¹ T, stochastic, and E[M_{τ_n}] − M = Σ_{k<n} B^k g¹.
  * Lemma 3 (convergence): B^k → 1π'. By H2, π'g¹ = 0, so B^k g¹ = (B − 1π')^k g¹ decays like |λ₂|^k. The sum is a
    Neumann series.
  * Martingale: E[P_{τ₁}] = M + g¹ + Bg = M + g.
  * Uniqueness: f = g¹ + Bf has solutions g + c1, since harmonic functions of an irreducible chain are constant, and
    antisymmetry forces c = 0.
* **Measured.**
  * **Bitcoin's fitted chain:**
    * λ₁ = 1, |λ₂| = 0.668 (a half-life of 1.7 moves, a multiplier ≈ 3);
    * π'g¹ = 7 × 10⁻¹⁶, and the series matches the closed form to 1.7 × 10⁻¹³;
    * without mirroring, a drift of 0.03 tick per move makes the partial sums grow linearly (11 ticks after 400 moves).
  * **The simulator (H1 approximately true):**
    * the microprice's 1-s drift is at most 0.015 tick, against the mid's 0.16;
    * the realised drift reaches about 0.93 × g at 10 s and settles at 1.15 × g, the excess being the coarseness of
      ten buckets;
    * the next-sign gap is −0.05.
  * **Bitcoin (H1 false):**
    * the realised drift peaks at 0.46 × g at 30 s and falls back;
    * the next-sign gap is +0.46 over 36,981 moves;
    * out of sample, the microprice is 3 to 5 times worse than the mid at 1 s.
* **Simplifications.**
  * Best quotes only, on a 100-ms grid, one venue and four days.
  * Ten imbalance buckets and a spread of at most two ticks.
  * Fills replayed with pro-rata cancellations, no latency and no fees.
* **Open problems.**
  * The smallest Markov state for a small-tick book.
  * Microprices under Hawkes order flow, with error bounds.
  * The fair price of a fragmented, multi-venue book.

## Build it

```bash
python -m videos.quant.quant36.compute                            # every item; ~10 minutes, ~1 GB of Binance files
python -m pytest -q tests/test_quant_house.py -k lob
EXPLAINER_TTS=silent python tools/qa_scene.py quant36 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant36                                      # the narrated part
```

## Desk questions, with solutions

1. **What is OFI, and why does it beat signed trades?**
   * e = q^b_t 1[p^b_t ≥ p^b_{t−1}] − q^b_{t−1} 1[p^b_t ≤ p^b_{t−1}] − (the ask's mirror), summed over an interval.
   * It counts additions and cancellations as well as trades. Its R² at 1 min (0.35–0.48) roughly doubles that of
     signed trades (0.21, Part 35), and the response is nearly linear.
2. **Why does queue imbalance predict the next tick?** With a one-tick spread the price moves when a best queue
   empties. The shorter queue tends to empty first: in Cont–de Larrard, P(up) = 1 − (2/π) arctan(q^a/q^b).
3. **What is the microprice, and when can you trust it?**
   * It is lim E[M_{τ_n} | I, S]: a martingale when (I, S) is Markov and the book is symmetric.
   * Trust it on large-tick books. Test the Markov property first: on Bitcoin it fails, and the microprice overshoots.
4. **Why is the weighted mid not a fair price?** It moves to the thin side before the tick and partly back after it,
   when a fresh queue arrives. Its changes are predictable, so it is not a martingale.
5. **Why is a back-of-queue fill bad news?** It happens only after the whole queue ahead has been eaten, usually by a
   sweep that carries on. Here the markout was −14.7 ticks after one second.
6. **How would you score a simulator?** On stylised facts out of sample, and on its reaction to the user's own orders:
   * move rate;
   * burstiness;
   * sign memory;
   * tails;
   * queue sizes.

## Problems, with solutions

1. **Queue time.** The queue ahead falls at 0.2 + 0.1 = 0.3 BTC/s, so you reach the front in 5/0.3 = 16.7 s. Your
   1 BTC then fills at 0.2 BTC/s in 5 s, 21.7 s in all.
2. **Up-tick probability.** Cont–de Larrard gives 1 − (2/π) arctan(3/9) = 1 − 0.637 × 0.322 = 0.795. The imbalance
   rule gives 9/12 = 0.75. The data lie nearer the second.
3. **Hawkes.** The mean rate is μ/(1 − n): 2/0.32 = 6.25 per second, and 2/0.05 = 40 at n = 0.95. The endogenous
   share is n: 68% and 95%.
4. **Sign memory.** Var(Σ_{i≤n} s_i) = n + 2Σ_{ℓ<n}(n − ℓ)C(ℓ). With C(ℓ) ∝ ℓ^−γ and γ < 1, the double sum grows like
   n^{2−γ} = n^{1.15}: superdiffusive. Prices stay diffusive only because impact decays (Part 37's propagator).
5. **OFI impact.** Δp ≈ tick/(2q̄) × OFI = 0.10/16 × 12 = $0.075, three-quarters of a tick.
6. **The interview book.**
   * Mid = $100.005. Weighted mid = 100 + 0.01 × 500/600 = $100.0083.
   * The microprice leans toward the offer, but less than the weighted mid. In the House's large-tick simulator,
     g(0.83) = 0.29 tick, so P ≈ $100.0079.
7. **Reporting a network.** Report:
   * direction accuracy next to the base rate and the linear baseline (84% against 87%);
   * R² (under 1%);
   * train against test conditions (the weekend was quieter);
   * the value per trade in ticks (about 1.5) against the spread (1) and fees (one basis point is about 27 ticks).
8. **A memoryless simulator.**
   * It can match queue sizes.
   * It cannot match:
     * the move rate, because it changes one unit per step and has no sweeps;
     * burstiness and fat tails, because it has no self-excitation;
     * sign pairs, because queues are redrawn after each move.
9. **Back-of-queue P&L.** 0.82 × (−14.7) ≈ −12.1 ticks per order placed. The markout already includes the half-spread
   earned.
10. **Cancelling on the microprice.**
    * The fill rate falls, mostly in the states that predicted adverse moves, so the markout improves.
    * The improvement is only as good as the microprice. On Bitcoin, where it overshoots, the maker would cancel far
      too often; a per-horizon table is the safer signal.
11. **(qual) The microprice theorem.**
    * **Lemma 1.** First-step analysis gives g¹ = R + Qg¹. Since ρ(Q) < 1, g¹ = Σ_n Q^n R = (1 − Q)⁻¹R.
    * **Lemma 2.** The strong Markov property at τ_i gives E[M_{τ_{i+1}} − M_{τ_i} | X_{τ_i} = y] = g¹(y), and
      X_{τ_i} ~ B^i(x, ·). So E[M_{τ_n}] − M = Σ_{k<n}(B^k g¹)(x).
    * **Lemma 3.** B is stochastic, irreducible and aperiodic, so B^k → 1π' geometrically. The mirror map σ satisfies
      Bσ = σB, πσ = π and σg¹ = −g¹, so π'g¹ = 0. For k ≥ 1, B^k − 1π' = (B − 1π')^k, so ‖B^k g¹‖ ≤ C|λ₂|^k. The
      series converges to (1 − B + 1π')⁻¹g¹, because (1 − (B − 1π'))⁻¹ = Σ(B − 1π')^k and the k = 0 term contributes
      g¹.
    * **Martingale.** E[M_{τ₁} + g(X_{τ₁}) | X_0 = x] = M + g¹(x) + (Bg)(x) = M + g(x), since g = g¹ + Bg.
    * **Uniqueness.** If M + f(X) is a martingale, then f = g¹ + Bf, so (1 − B)(f − g) = 0. By irreducibility,
      f − g = c1, and antisymmetry gives c = 0.
12. **(qual) Two states.**
    * **Setting.** Every step is a mid change (Q = 0), so g¹(H) = q − (1 − q) = 2q − 1 and g¹(L) = −(2q − 1). The
      post-move law is B = [[p, 1 − p], [1 − p, p]], with π = (½, ½), so π'g¹ = 0.
    * **The lean.** The vector (1, −1) is an eigenvector with eigenvalue 2p − 1. So g = Σ_k(2p − 1)^k g¹ =
      g¹/(2(1 − p)), that is, g(H) = (2q − 1)/(2(1 − p)) ticks. For q = p = ¾ this is 1 tick, and it is unbounded as
      p → 1.
    * **Bitcoin.** The fitted |λ₂| = 0.67 multiplies the first move about three times. The realised drift says the
      market keeps less of each lean than the chain believes: the persistence is overstated because the state is not
      Markov.

## Data and reproducibility

* **Binance.**
  * Public daily `bookTicker` and `aggTrades` files for the BTCUSDT USD-M perpetual (16, 17, 20 and 21 May 2023, and
    trades for 16–17 May), checked against Binance's published SHA-256 files.
  * The best-quote stream is reduced to a 100-ms grid and cached beside the raw file.
* **Simulation.** The queue-reactive simulator is fitted to 17 May; long runs (400,000 steps, seeds 1–5 and 36) are
  used for the theorem's checks.
* **No registration.** The counter stays at 23,550.
* **Quoted, not computed:**
  * DeepLOB's, Sirignano–Cont's and LOBCAST's results;
  * Hardiman et al.'s branching ratios;
  * Farmer–Patelli–Zovko;
  * Cont–Cucuringu–Zhang;
  * Kolm–Turiel–Westray;
  * Gould–Bonart;
  * Moallemi–Yuan.
* **Not run here.** External models and code, such as published DeepLOB weights and LOBCAST, were not run. The network
  here is the House's own MLP ensemble.

---

# 量化金融，从零搭建 — 第36部分：限价订单簿

四十三部分量化金融系列的第36部分（见[系列计划](../README.md)和[教学大纲](../SYLLABUS.md)），第六幕“市场微观结构”的第二部分，按本系列的博士层次构建。它要回答三个问题：
* 挂单排成的队列，透露了下一个价格的什么信息；
* 给定订单簿，公允价值在哪里；
* 队列中的位置值多少，一次成交又告诉了你什么。

所有测量都基于币安公开的BTCUSDT永续合约最优买卖报价流（`bookTicker`）和归集成交记录。2023年5月16日和17日（工作日）用于拟合，5月20日和21日（周末）用于检验。报价流被整理成100毫秒的网格。

本部分涵盖：
* **订单簿**：
  * 规则、事件与订单类型；
  * 大跳价与小跳价。比特币永续合约超过99%的时间价差为一跳，但中间价在快照之间一旦移动，中位跳动为8跳，所以跳价是小的。
* **队列与下一跳**：
  * Cont–de Larrard公式 P(上涨) = 1 − (2/π) arctan(q^a/q^b)；
  * 数据中上涨概率从16%升到86%，模型在两端太陡；
  * 队列反应模型。
* **事件引发事件**：
  * 霍克斯分支比0.68；
  * 成交方向记忆 ℓ^−0.85；
  * 签名图在0.1秒到10秒间上升约30%。
* **订单流不平衡**：
  * 10秒R²为0.37–0.45；
  * 冲击对深度的斜率为−1.17（理论值−1）。
* **微观价格**：
  * Stoikov的链在比特币上偏离±25跳，样本外失败；
  * 按时间跨度的平均变动表把10秒误差降低3–5%。
* **深度订单簿**：
  * 线性规则对下一秒方向的准确率87.2%，网络84.0%；
  * 每笔交易约1.5跳的收益，远不足以覆盖价差和手续费（一个基点约27跳）。
* **我们自己的订单簿**：队列反应模拟器的五项评分卡，一项对，四项错。
* **在队列中交易**：
  * 排在末尾时1秒后损益为−14.7跳，排在最前时为−1.6跳；
  * 队列位置的价值约11跳。
* **第36条规则**：用价差衡量订单簿。
* **写给研究者**：
  * 微观价格定理的证明；
  * 在模拟器中它成立，在比特币上实现的漂移只达到0.46倍；
  * 对马尔可夫性的直接检验：比特币上的方向差距为+0.46。

本部分不登记策略，试验计数仍为23,550。

*这是方法教育，不是投资建议。*

## 章节（约55分钟）

* **开场：公允价值在哪里？**：面试题中的订单簿、三个发现、为什么订单簿重要、二十年的研究、计划。
* **1. 订单簿**：规则、图像、四种事件、数据、一分钟、一天、订单类型、跳价大小。
* **2. 队列与下一跳**：赛跑、象限、公式、假设、数据、为什么数据更平缓、队列反应模型。
* **3. 引发事件的事件**：霍克斯拟合、接近临界、家族树表示、方向记忆、拆单、签名图、同向成对移动。
* **4. 订单流不平衡**：定义、两分钟、手算、各尺度的R²、冲击与深度、与Kyle比较、更深与综合的不平衡。
* **5. 微观价格**：三个候选、加权中间价为何失败、马尔可夫链、拟合与实现、样本外检验、鞅检验、理论为何失败、面试答案、用途。
* **6. 深度学习看订单簿**：DeepLOB、普适特征、架构、LOBCAST、标签、我们的检验与解读、教训。
* **7. 我们自己的订单簿**：为什么要模拟、四大类、零智能模型、拟合的速率、评分卡、诊断、三条规则。
* **8. 在队列中交易**：价格-时间优先、回放实验、末尾对最前、按队列大小、位置的价值、免费期权、赛跑、做市商如何生存。
* **9. 第36条规则**：汇总表、未测量的东西、五个实验、模块、三个案例。
* **写给研究者：微观价格定理**：设定、三个引理、定理、唯一性、对称性、四项检验、相关工作、开放问题。
* **结尾**：十三行回顾、三条教训、六个交易台问题、暂停问题的答案、十二道习题（其中两道为资格考试难度，解答见下文）。

## 写给研究者

* **定理（Stoikov 2018，本部分给出证明）。**
  * 设定：有限状态X（不平衡分组、价差）与中间价M。
  * 假设一：(X, M)是马尔可夫可加过程。
  * 假设二：镜像（交换买卖）使动力学映射到自身，且ΔM → −ΔM。
  * 假设三：每个状态终将移动，B不可约且非周期。
  * 结论：P^micro = M + g(X)，其中 g = Σ_k B^k g¹ = (1 − B + 1π')⁻¹ g¹。它以|λ₂(B)|的速率收敛，在中间价变化时刻是鞅，并且是唯一的反对称鞅调整。
* **证明。**
  * 引理一：首步分析，g¹ = (1 − Q)⁻¹R。
  * 引理二：强马尔可夫性，B = (1 − Q)⁻¹T是随机矩阵。
  * 引理三：B^k → 1π'；由对称性 π'g¹ = 0，于是几何衰减，求和为诺伊曼级数。
  * 鞅性：g = g¹ + Bg。
  * 唯一性：不可约链的调和函数是常数，再由反对称性得到常数为零。
* **测量。**
  * 比特币的拟合链：|λ₂| = 0.668，π'g¹ ≈ 10⁻¹⁶；不做镜像时，漂移使部分和线性增长。
  * 模拟器：微观价格不漂移，实现漂移达到约1倍g；方向差距为−0.05。
  * 比特币：实现漂移峰值只有0.46倍g；方向差距为+0.46；样本外误差是中间价的3到5倍。
* **简化。** 只有最优报价、100毫秒网格、一个交易所、四天；成交回放假设按比例撤单、无延迟、无手续费。
* **开放问题。**
  * 小跳价订单簿的最小马尔可夫状态；
  * 霍克斯订单流下带误差界的微观价格；
  * 多交易场所合并订单簿的公允价格。

## 交易台问题与解答

1. **什么是订单流不平衡，为什么胜过带方向的成交？** 它把挂单、撤单和成交都算进去。一分钟R²为0.35–0.48，大约是带方向成交（0.21）的两倍，而且响应近似线性。
2. **为什么队列不平衡能预测下一跳？** 价差为一跳时，最优队列被清空价格才动，短的队列先被清空。
3. **什么是微观价格，何时可信？** 它是 lim E[M_{τ_n} | I, S]，在马尔可夫、对称的订单簿上是鞅。在大跳价订单簿上可以信任，但要先检验马尔可夫性。
4. **为什么加权中间价不是公允价格？** 它在跳价前移向薄的一侧，跳价后又部分回来，变化可以预测。
5. **为什么排在队列末尾的成交是坏消息？** 只有前面的整个队列被吃光才会成交，这通常是一次会继续下去的扫单。这里1秒后损益为−14.7跳。
6. **怎样为模拟器打分？** 在样本外，用以下程式化事实，并看它对自己订单的反应：
   * 移动速率；
   * 成串程度；
   * 方向记忆；
   * 尾部；
   * 队列大小。

## 习题与解答

1. 前面的队列以每秒0.3个比特币减少，16.7秒到最前，再过5秒成交完，共21.7秒。
2. Cont–de Larrard给出0.795，不平衡规则给出0.75，数据更接近后者。
3. 平均速率：每秒6.25笔；n = 0.95时每秒40笔。内生比例分别为68%和95%。
4. 方向和的方差按 n^{2−γ} = n^{1.15} 增长，是超扩散的；价格仍保持扩散，是因为冲击会衰减（第37部分的传播子）。
5. Δp ≈ 0.10/16 × 12 = 0.075美元，即四分之三跳。
6. 中间价100.005美元，加权中间价100.0083美元；微观价格偏向卖方，但不如加权中间价那么多，在大跳价模拟器中约为100.0079美元。
7. 要报告：
   * 方向准确率及其基准（84%对87%）；
   * R²（不到1%）；
   * 训练与检验条件的差异；
   * 每笔约1.5跳的价值，并与价差和手续费对比。
8. 无记忆模拟器：
   * 能匹配队列大小；
   * 匹配不了移动速率（没有扫单）、成串程度和厚尾（没有自激）、同向成对移动（每次移动后重新抽取）。
9. 每挂一笔订单约 0.82 × (−14.7) ≈ −12.1跳，已含赚到的半跳价差。
10. 按微观价格撤单：
    * 成交率下降，成交后损益改善；
    * 但改善程度取决于微观价格是否准确。在比特币上它过头，会导致过度撤单，按时间跨度的表格更稳妥。
11. **（资格考试）微观价格定理**：
    * 首步分析得 g¹ = (1 − Q)⁻¹R；
    * 强马尔可夫性得部分和为 Σ_{k<n}B^k g¹；
    * 镜像对称使 π'g¹ = 0，因此 (B − 1π')^k 几何衰减，级数收敛到 (1 − B + 1π')⁻¹g¹；
    * 鞅性来自 g = g¹ + Bg；
    * 唯一性来自不可约链的调和函数为常数，再加反对称性。
12. **（资格考试）两状态**：
    * g¹(H) = 2q − 1，B = [[p, 1 − p], [1 − p, p]]；
    * (1, −1) 是特征值为 2p − 1 的特征向量，因此 g(H) = (2q − 1)/(2(1 − p))；
    * q = p = ¾ 时为1跳，p → 1 时无界；
    * 比特币的 |λ₂| = 0.67 意味着约三倍的放大，而市场并不兑现这种持续性。

## 数据与复现

* **币安。**
  * BTCUSDT永续合约的公开日度`bookTicker`和`aggTrades`文件，均与币安公布的SHA-256文件核对；
  * 报价流整理为100毫秒网格并缓存。
* **模拟。** 队列反应模拟器用5月17日拟合，定理检验使用40万步的长模拟。
* **不登记策略。** 试验计数仍为23,550。
* **引用而非计算。** DeepLOB、Sirignano–Cont、LOBCAST、Hardiman等、Farmer–Patelli–Zovko、Cont–Cucuringu–Zhang、Kolm–Turiel–Westray、Gould–Bonart和Moallemi–Yuan的结果。
* **未在此运行。** 外部模型和代码（如已发表的DeepLOB权重和LOBCAST）没有在这里运行，这里的网络是本系列公司自己的多层感知机集成。
