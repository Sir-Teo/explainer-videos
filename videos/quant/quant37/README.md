# Quant, Built — Part 37: Market Impact and Execution

Part 37 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act VI, Market Microstructure, built to the series' PhD layer. It
asks how much a large order moves the price against the trader who sends it, and how to send it so that it costs the
least.

Measurement uses Binance's public aggregated trades for the BTCUSDT perpetual (16–25 May 2023, ten days), its
best-quote stream on four of those days (Part 36's 100-ms grid), and its one-minute bars for 2023. The models are the
latent order book, Almgren–Chriss, decay kernels and Obizhaeva–Wang, and a learned executor in Part 36's queue-reactive
simulator.

The part covers:

* **Metaorders:**
  * implementation shortfall (Perold 1988) and its decomposition;
  * the impact path, concave while running, with about two-thirds remaining after (Moro et al. 2009; Bershova and
    Rakhlin 2013);
  * who receives the cost;
  * how researchers see metaorders.
  * Aggregate impact on Bitcoin is sigmoid in the imbalance (after Patzelt and Bouchaud 2018). A minute's move grows
    like signed volume to the power 0.81.
* **The square-root law:**
  * I ≈ Yσ√(Q/V) (Loeb 1983; Torre 1997; Almgren et al. 2005; Tóth et al. 2011), its universality, and Bitcoin's Mt.
    Gox metaorders (Donier and Bonart 2015);
  * what it says for Bitcoin's perpetual: 5, 17 and 54 bp at 0.1%, 1% and 10% of a day;
  * the puzzle; dimensional analysis;
  * the visible book (about 0.003% of a day);
  * the latent book (Donier, Bonart, Mastromatteo and Bouchaud 2015) derived (Δ = √(2Q/𝓛)) and simulated. The
    exponent falls from 1.02 to 0.42 (Bucci et al. 2019), and the impact decays after the order;
  * fair pricing (Farmer, Gerig, Lillo and Waelbroeck 2013), which gives the two-thirds;
  * microstructure invariance (Kyle and Obizhaeva 2016).
* **The propagator (Bouchaud, Gefen, Potters and Wyart 2004):**
  * the response function on 3.4 million Bitcoin trades, peaking at about 14 ticks after 500 trades;
  * the fitted propagator, which peaks at 0.72 tick after 77 trades and then decays as ℓ^−0.17, against
    (1 − γ)/2 = 0.10;
  * a metaorder through it; the fit's pitfalls;
  * history-dependent impact.
* **No dynamic arbitrage:**
  * permanent impact must be linear (Huberman and Stanzl 2004), with a numerical money machine;
  * Gatheral (2010): positive-definite kernels, and a box kernel's round trip that earns 0.06 per unit;
  * Alfonsi, Schied and Slynko (2012): convex decreasing kernels never sell. A Gaussian kernel buys by selling, and
    explodes as the grid refines;
  * Bitcoin's fitted kernel passes (Pólya).
* **Almgren and Chriss (2000):**
  * the model, objective and sinh solution, discrete and continuous;
  * 5,000 BTC ($135m) over an hour: TWAP costs $21k (1.6 bp) with a standard deviation of $267k, and λ = 10⁻⁶ costs
    $35k for $178k;
  * the frontier; the meaning of λ.
  * The linear model's 1.6 bp against the square root's 20 bp.
  * Almgren et al.'s 3/5 power; extensions (Almgren 2003; Bertsimas and Lo 1998; Almgren and Lorenz 2007; Schied and
    Schöneborn 2009).
* **A book that recovers:**
  * Obizhaeva and Wang (2013): blocks X/(2 + ρT) at the ends and the rate ρX/(2 + ρT) between;
  * the optimum on a grid; by resilience; the power-law U;
  * Bitcoin's sweeps. Displayed depth refills within 100–200 ms, but the price keeps drifting about 42 ticks after
    two minutes: news, not a dent;
  * signals (Cartea and Jaimungal; Lehalle and Neuman 2019); crowding (Cardaliaguet and Lehalle 2018); predatory
    trading (Brunnermeier and Pedersen 2005).
* **A learned executor:**
  * tabular Q-learning, 60,000 episodes in the House simulator, selling 20 units in 20 steps;
  * TWAP 50.7, Q-learning 52.7, front-loaded 54.2, thin-bid rule 55.8, dump 60.2 half-ticks;
  * why, and what would do better.
* **The algorithms, and the bill:**
  * TWAP, VWAP, POV and IS; Bitcoin's volume curve (2.3% to 7.5% an hour) and weekend volume (about 52%);
  * participation under the square root; the close; routing and dark pools; crypto venues;
  * a pre-trade estimate; TCA, a worked shortfall and benchmark gaming.
* **Rule 37: price the trade before you make it.**
  * The House's sheet; sizing against a 10-bp alpha (about $35m on Bitcoin); the order record; five labs.
* **For the researcher: the optimal schedule under transient impact.**
  * Uniqueness by strict convexity; the Fredholm first-order condition; the exponential solution and cost.
  * Why measures are needed; intuition; limits linking the permanent, Obizhaeva–Wang and Almgren–Chriss models.
  * Checks: grid convergence; the saving over TWAP, peaking at 12% at ρT ≈ 3; Bitcoin's power-law kernel, with 4.2%
    blocks, a shallow U, no sales and a 1.5% saving.

No strategy is registered in this part; the trial counter stands at 23,550.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: ten percent costs thirty basis points; what does forty cost?** The desk question; three findings; why it
  matters; three myths; where this sits; fifty years; the plan.
* **1. Metaorders.** Vocabulary; implementation shortfall; the impact path; who pays; what we can measure; how
  metaorders are seen; aggregate impact by imbalance; against size.
* **2. The square-root law.**
  * The law; how universal; Bitcoin's numbers; the puzzle; dimensions; the visible book.
  * The latent book, its derivation, simulation and decay; fair pricing; invariance.
* **3. The propagator.** The model; the response; the fit; a metaorder through it; pitfalls; the balance β = (1 − γ)/2;
  what it says; history-dependent impact.
* **4. No dynamic arbitrage.** The cost functional; permanent impact and a money machine; the box; Gatheral; convexity;
  the Gaussian and its refinement; Bitcoin's kernel passes; lessons.
* **5. Almgren and Chriss.** Model; objective; solution; continuous form; trajectories; frontier; numbers; λ; against
  the square root; practice; extensions; beyond variance.
* **6. A book that recovers.** The model; blocks; on a grid; by resilience; Bitcoin's sweeps; its displayed
  resilience; the power law; signals; crowds.
* **7. A learned executor.** Literature; environment; learner; learning curve; results; the policy; why not; what would
  do better; a better experiment.
* **8. The algorithms, and the bill.** The menu; the volume curve; the week; participation; the close; routing;
  crypto; a pre-trade estimate; TCA; a worked example; benchmarks.
* **9. Rule 37.** The sheet; sizing; capacity; the record; five labs; the module; three cases.
* **For the researcher: the optimal schedule under transient impact.** Setting; three lemmas; solution; why measures;
  the theorem; intuition; limits; three checks; the power-law case; related work; open problems.
* **Outro.** Thirteen lines; three lessons; the part on one card; connections; six desk questions; the pause answer;
  twelve problems (two of qualifying-exam level, solved below); payoffs; references.

## Hands-on

* **Built and run here:**
  * response function, propagator fit and aggregate impact on Binance trades;
  * the latent order book;
  * Almgren–Chriss schedules and frontier;
  * kernel costs and optimal schedules (exponential, power law, Gaussian, box), and the Obizhaeva–Wang closed form;
  * Bitcoin's book after sweeps;
  * an execution environment on the queue-reactive simulator with Q-learning;
  * the 2023 volume curve.
* **Labs, from the House's source:** `latent_book`, `almgren_chriss`, `kernel_optimal` with `ow_closed_form`,
  `propagator_fit`, and `QueueExec._sell`.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices* (2018) | square-root law, propagator, latent liquidity | 1–4, 6 |
| Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015) | optimal execution, signals | 5, 6 |
| Guéant, *The Financial Mathematics of Market Liquidity* (2016) | Almgren–Chriss, extensions | 5 |
| Lehalle and Laruelle, *Market Microstructure in Practice* (2018) | algorithms, TCA, routing | 8 |

## Papers, chapter by chapter

* ch. 1: Perold (1988), *JPM*; Kraus and Stoll (1972), *JF*; Moro et al. (2009), *PRE*; Bershova and Rakhlin (2013),
  *Quantitative Finance*; Patzelt and Bouchaud (2018), *PRE*.
* ch. 2:
  * Loeb (1983), *FAJ*; Torre (1997); Almgren, Thum, Hauptmann and Li (2005), *Risk*; Tóth et al. (2011), *PRX*;
  * Donier and Bonart (2015), *Market Microstructure and Liquidity*; Donier, Bonart, Mastromatteo and Bouchaud (2015),
    *Quantitative Finance*;
  * Zarinelli et al. (2015); Bucci et al. (2019), *PRL*; Farmer, Gerig, Lillo and Waelbroeck (2013), *Quantitative
    Finance*; Kyle and Obizhaeva (2016), *Econometrica*.
* ch. 3: Bouchaud, Gefen, Potters and Wyart (2004), *Quantitative Finance*; Lillo and Farmer (2004); Taranto et al.
  (2018).
* ch. 4: Huberman and Stanzl (2004), *Econometrica*; Gatheral (2010), *Quantitative Finance*; Alfonsi, Schied and Slynko
  (2012), *SIAM J. Financial Math.*
* ch. 5:
  * Almgren and Chriss (2000), *J. Risk*; Bertsimas and Lo (1998), *JFM*; Almgren (2003), *Applied Mathematical
    Finance*;
  * Almgren and Lorenz (2007); Schied and Schöneborn (2009), *Finance and Stochastics*.
* ch. 6:
  * Obizhaeva and Wang (2013), *JFM*;
  * Cartea and Jaimungal (2016); Lehalle and Neuman (2019), *Finance and Stochastics*;
  * Cardaliaguet and Lehalle (2018); Brunnermeier and Pedersen (2005), *JF*.
* ch. 7: Nevmyvaka, Feng and Kearns (2006), *ICML*; Ning, Lin and Jaimungal (2021), *Applied Mathematical Finance*.
* ch. 8: Konishi (2002), *JFM*; Humphery-Jenner (2011), *J. Banking and Finance*.
* Research: Gatheral, Schied and Slynko (2012), *Mathematical Finance*; Alfonsi, Fruth and Schied (2010),
  *Quantitative Finance*; Obizhaeva and Wang (2013).

## For the researcher

* **The theorem.**
  * Strategies are signed measures dX on [0, T] with ∫dX = X.
  * The cost is 𝒞[X] = ½∬G(|t − s|) dX_s dX_t, for a continuous, strictly positive-definite G.
  * Then the minimiser is unique, and characterised by f(t) = ∫G(|t − s|) dX*_s = λ on [0, T]. Its cost is ½λX.
  * For G = e^{−ρt}/q: dX* = X/(2 + ρT)·(δ_0 + ρ dt + δ_T), with cost X²/(q(2 + ρT)).
* **The proof.**
  * Lemma 1 (uniqueness): 𝒞 is a quadratic form, strictly convex on the convex set 𝒜.
  * Lemma 2 (first order):
    * perturbing by δ_a − δ_b gives f(a) = f(b), so f is constant;
    * conversely, constant f with convexity gives optimality;
    * integrating f against dX* gives the cost.
  * Lemma 3 (exponential): for blocks a and rate b,
    f(t) = a(e^{−ρt} + e^{−ρ(T−t)}) + (b/ρ)(2 − e^{−ρt} − e^{−ρ(T−t)}). It is constant iff a = b/ρ, and 2a + bT = X.
  * Why measures: among rates only, the infimum is approached by bursts but not attained.
* **Measured.**
  * On a grid (ρT = 10): the cost 0.08333 and block 0.0838 at n = 1000, converging from 0.1138 and 0.2104 at n = 5.
    Every trade is a purchase.
  * The saving over TWAP is 1.6%, 9.4%, 12.2%, 7.4%, 3.0% and 1.0% at ρT = 0.1, 1, 3, 10, 30 and 100.
  * Bitcoin's fitted kernel (1 + ℓ/77)^−0.17 over 20,000 trades gives blocks of 4.2%, a shallow U with no sales, and
    a saving of 1.5%.
  * Bitcoin's displayed resilience is at least 30 per second, so ρT ≈ 10⁵ for an hour and the blocks vanish. The
    resilience that matters is latent.
* **Simplifications.**
  * Linear transient impact (no square root in the instantaneous response).
  * Deterministic schedules (no adaptation).
  * The propagator in trade time, fitted on four days with a 100-ms mid.
* **Open problems.**
  * Square-root impact with decay, free of dynamic arbitrage, with computable optima.
  * Separating informational from mechanical impact in public data.
  * The equilibrium of many executors with private signals, and its stability.

## Build it

```bash
python -m videos.quant.quant37.compute                            # every item; a few minutes; ~0.15 GB of extra trades
python -m pytest -q tests/test_quant_house.py -k execution
EXPLAINER_TTS=silent python tools/qa_scene.py quant37 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant37                                      # the narrated part
```

## Desk questions, with solutions

1. **10% of volume costs 30 bp; 40%?** The square root gives 30√4 = 60 bp; a straight line would give 120 bp.
2. **Why is impact concave?**
   * Latent liquidity has a density that grows linearly away from the price: ρ(x) = 𝓛|x|.
   * Moving the price by Δ consumes 𝓛Δ²/2, so Δ = √(2Q/𝓛).
3. **Signs are predictable; why are prices not?**
   * Each trade's impact decays as G(ℓ) ∼ ℓ^−β.
   * With sign correlations ∼ ℓ^−γ, Var(p_n) ∼ n^{2−γ−2β}. This is diffusive iff β = (1 − γ)/2.
4. **What must an impact model satisfy?**
   * A positive-definite kernel, so that no round trip has negative expected cost (Gatheral).
   * Linear permanent impact (Huberman–Stanzl).
   * Preferably a convex, decreasing kernel, so the optimal buy never sells (Alfonsi–Schied–Slynko).
5. **How does a risk-averse seller trade?** Holdings follow x(t) = X sinh κ(T − t)/sinh κT, with κ = √(λσ²/η).
6. **When the book recovers?** Equal blocks X/(2 + ρT) at both ends, and the recovery rate ρX/(2 + ρT) between.

## Problems, with solutions

1. **Square root.** 4% gives 10√4 = 20 bp and 9% gives 30 bp. Linear impact would give 40 and 90.
2. **Latent book.** Δ = √(2 × 9/2) = 3 ticks.
3. **Propagator exponent.** β = (1 − 0.6)/2 = 0.2.
4. **A money machine.** Trade +1, −1, +1, −1 at spacing 0.7τ.
   * Adjacent pairs are within τ: Γ = 1. Pairs two apart are not: Γ = 0.
   * The cost is ½(4 × 1 + 2 × 3 × (−1)) = −1. The kernel is not positive definite.
5. **Urgency.** κ = √0.01 = 0.1 per minute. With T = 60 the share held after 20 minutes is
   sinh(4)/sinh(6) = 0.135, about e^{−2}.
6. **TWAP risk.** sd ≈ σX√(T/3) = 12 × 5,000 × √20 ≈ $268k, matching the computed $267k.
7. **Obizhaeva–Wang, ρT = 2.** The blocks are 1/4, the rate 1/2 and the cost 1/4. TWAP costs
   ½(1 − (1 − e^{−2})/2) = 0.284, so the optimum saves 12%.
8. **VWAP hour.** 1,000 × 7.5% = 75 BTC.
9. **Participation.** The order takes 2%/5% = 0.4 day at 5% participation and 0.1 day at 20%. The expected impact is
   about the same, Yσ√0.02. The risk, ∝ σ√T, is twice as large at 5%.
10. **Sizing.** Q < (0.001/0.02)² × $10bn = $25m.
11. **(qual) The transient-impact theorem.**
    * **Uniqueness.** Strict convexity gives at most one minimiser. Perturbing by δ_a − δ_b gives the Fredholm
      condition f ≡ λ, and convexity makes it sufficient.
    * **Exponential kernel.** Inserting blocks and a rate gives f constant iff a = b/ρ; 2a + bT = X solves for a and b.
    * **Cost.** The cost is ½λX = X²/(q(2 + ρT)).
    * **Limits.** As ρ → 0 the cost tends to X²/2q, the same for every schedule. As ρT → ∞ it tends to X²/(qρT), which
      is Almgren–Chriss temporary impact with η = 1/(qρ).
12. **(qual) Almgren–Chriss.**
    * **Objective.** Minimise (η̃/τ)Σ(x_{k−1} − x_k)² + λσ²τΣx_k².
    * **First-order condition.** x_{k+1} − 2x_k + x_{k−1} = (λσ²τ²/η̃)x_k.
    * **Trial solution.** x_k = e^{±κt_k} works iff 2cosh κτ − 2 = λσ²τ²/η̃, that is,
      cosh κτ = 1 + λσ²τ²/(2η̃). The boundary conditions x_0 = X and x_N = 0 select the sinh.
    * **λ → 0.** κ → 0 and x is linear: TWAP.
    * **λ → ∞.** κ → ∞, and everything is sold in the first interval.

## Data and reproducibility

* **Binance.**
  * Public daily `aggTrades` for BTCUSDT USD-M perpetual, 16–25 May 2023, and `bookTicker` for 16, 17, 20 and
    21 May; one-minute klines for 2023.
  * All are checked against Binance's published SHA-256 files.
* **Simulation.** The latent book (explicit finite differences), kernels on grids, and the queue-reactive environment
  fitted to 17 May (seeds 1, 7, 37 and 99).
* **No registration.** The counter stays at 23,550.
* **Quoted, not computed.** The proprietary metaorder studies (Moro et al., Bershova–Rakhlin, Tóth et al., Almgren
  et al., Zarinelli et al., Bucci et al.) and Donier–Bonart's Mt. Gox analysis. Those data are not public.

---

# 量化金融，从零搭建 — 第37部分：市场冲击与执行

四十三部分量化金融系列的第37部分，第六幕“市场微观结构”的第三部分，按本系列的博士层次构建。它问：一笔大订单会让价格朝不利于下单者的方向移动多少，以及怎样下单才能让成本最低。

测量使用币安BTCUSDT永续合约的公开归集成交记录（2023年5月16日至25日共十天）、其中四天的最优报价流，以及2023年的一分钟K线。

本部分涵盖：
* **元订单与执行差额**：比特币上的总体冲击按带方向成交量的0.81次方增长。
* **平方根法则及潜在订单簿的推导和模拟**：模拟中的指数从1.02降到0.42；公平定价给出三分之二；微观结构不变性。
* **传播子**：峰值0.72跳，按ℓ^−0.17衰减，理论值为0.10。
* **无动态套利**：
  * 永久冲击必须是线性的；
  * 正定核；
  * 方框核的往返交易能赚钱；
  * 高斯核会为了买入而卖出；
  * 比特币拟合的核能通过检验。
* **Almgren–Chriss**：五千个比特币一小时，TWAP成本2.1万美元（1.6个基点），标准差26.7万美元；平方根法则则给出约20个基点。
* **Obizhaeva–Wang的整块**：比特币的扫单之后，可见深度迅速恢复，价格却继续漂移。
* **Q学习执行者**：成本52.7个半跳，TWAP为50.7个半跳。
* **TWAP、VWAP、POV、IS、路由和交易成本分析。**
* **第37条规则**：交易之前先定价。
* **写给研究者**：暂时性冲击下最优时间表的定理及证明。

本部分不登记策略，试验计数仍为23,550。

*这是方法教育，不是投资建议。*

## 章节（约55分钟）

* **开场**：交易台问题、三个发现、为什么重要、三个误解、五十年的历史、计划。
* **1. 元订单**：术语、执行差额、冲击路径、谁收到成本、能测量什么、总体冲击。
* **2. 平方根法则**：法则、普适性、比特币上的数字、谜题、量纲、可见订单簿、潜在订单簿的推导与模拟、公平定价、不变性。
* **3. 传播子**：模型、响应函数、拟合、通过它的元订单、陷阱、平衡条件、历史依赖冲击。
* **4. 无动态套利**：成本泛函、永久冲击、方框核、Gatheral、凸性、高斯核、比特币的核、教训。
* **5. Almgren与Chriss**：模型、目标、解、连续形式、轨迹、前沿、数字、λ的含义、与平方根比较、实践、推广。
* **6. 会恢复的订单簿**：模型、整块、网格、按韧性、比特币的扫单、幂律、信号、拥挤。
* **7. 学出来的执行者**：文献、环境、学习者、学习曲线、结果、策略、为什么不行、怎样做得更好。
* **8. 算法与账单**：菜单、成交量曲线、参与率、收盘、路由、加密市场、交易前估计、交易成本分析、例子、基准。
* **9. 第37条规则**：汇总表、规模确定、容量、记录、五个实验、模块、三个案例。
* **写给研究者**：设定、三个引理、求解、为什么需要测度、定理、直观、极限、三项检验、幂律情形、相关工作、开放问题。
* **结尾**：回顾、教训、公式卡、联系、交易台问题、习题（两道资格考试题，解答见下文）。

## 写给研究者

* **定理。** 对连续且严格正定的核G，在总量为X的带符号测度中：
  * 最小化 𝒞 = ½∬G(|t−s|)dX dX 的解唯一，由 ∫G(|t−s|)dX*_s = λ 刻画，成本为 ½λX。
  * 对 G = e^{−ρt}/q，dX* = X/(2+ρT)·(δ_0 + ρdt + δ_T)，成本为 X²/(q(2+ρT))。
* **证明。** 严格凸性给出唯一性；以 δ_a − δ_b 扰动得到弗雷德霍姆条件；对指数核，整块等于速率乘恢复时间时指数项相消。
* **测量。**
  * 网格收敛；
  * 相对TWAP的节省在 ρT ≈ 3 时达到峰值12%；
  * 比特币拟合的幂律核：两端各4.2%的整块，浅U形，不卖出，节省1.5%。
* **开放问题。**
  * 带衰减的平方根冲击模型；
  * 区分信息性冲击与机械性冲击；
  * 多执行者均衡。

## 交易台问题与解答

1. 百分之四十的成本：30√4 = 60个基点。
2. 冲击为何是凹的：潜在密度线性增长，Q = 𝓛Δ²/2。
3. 价格为何不可预测：冲击按 ℓ^−β 衰减，β = (1−γ)/2 时价格扩散。
4. 冲击模型必须满足：正定核、线性永久冲击，最好是凸递减核。
5. 厌恶风险的卖方：双曲正弦，κ = √(λσ²/η)。
6. 订单簿会恢复：两端各 X/(2+ρT) 的整块，中间速率 ρX/(2+ρT)。

## 习题与解答

1. 4%：20个基点；9%：30个基点（线性则为40和90）。
2. Δ = 3跳。
3. β = 0.2。
4. 间隔0.7τ交替交易 +1、−1、+1、−1，成本为−1。
5. κ = 0.1/分钟，20分钟后持有13.5%。
6. 标准差约26.8万美元。
7. ρT = 2：整块1/4，速率1/2，成本1/4；TWAP为0.284，节省12%。
8. 75个比特币。
9. 5%参与率需0.4天，20%需0.1天；冲击相近，风险相差一倍。
10. 上限2500万美元。
11. **（资格考试）暂时性冲击定理**：
    * 由严格凸性和扰动得到弗雷德霍姆条件；
    * 对指数核，a = b/ρ 且 2a + bT = X；
    * 两个极限分别对应永久冲击和Almgren–Chriss。
12. **（资格考试）Almgren–Chriss**：
    * 一阶条件给出二阶差分方程，cosh κτ = 1 + λσ²τ²/(2η̃)；
    * λ → 0 时为TWAP，λ → ∞ 时在第一个区间卖完。

## 数据与复现

* **币安公开数据**：BTCUSDT永续合约的归集成交、最优报价和一分钟K线，均与币安公布的SHA-256核对。
* **不登记策略**：试验计数仍为23,550。
* **引用而非计算**：专有的元订单研究，以及Donier–Bonart对Mt. Gox数据的分析。
