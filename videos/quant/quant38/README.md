# Quant, Built — Part 38: Market Making, ETFs and the Speed Race

Part 38 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth and last part of Act VI, Market Microstructure, built to the series' PhD
layer. It runs the business on the other side of every order in Parts 35–37: how a market maker earns a living, what
it costs, why that business has become a contest of microseconds, and how the same business keeps exchange-traded
funds near their holdings.

Measurement uses Binance's public best-quote stream and aggregated trades for the BTCUSDT perpetual (16, 17 and 20 May
2023, Part 36's 100-ms grid), and Yahoo Finance daily bars for HYG and TLT (2015–2020). The models are Avellaneda–
Stoikov and Guéant–Lehalle–Fernandez-Tapia (GLFT), fill intensities fitted to the tape, and Budish, Cramton and Shim's
sniping equilibrium, simulated and calibrated to Bitcoin.

The part covers:

* **The maker's business:**
  * profit = half-spread + rebate − markout ± inventory; three risks (adverse selection, inventory, operations);
  * the spread's components (Stoll 1989; Huang and Stoll 1997);
  * Avellaneda and Stoikov (2008) recalled: with γ = 0.1, σ²(T − t) = 4 and k = 1.5 the total spread is 1.69 and the
    reservation price sits 0.8 below the mid at two units;
  * the core trade-off δ* = 1/k, and GLFT's stationary quotes with an inventory skew;
  * specialists, Christie and Schultz's odd-eighths (1994), wholesalers, electronic makers; flow that is not equal;
    many books hedged at once.
* **A maker on the tape:** a replay that joins the best bid and offer at the back of each queue, checks every 100 ms
  and holds at most five units.
  * On 17 May the slow maker is filled 42,019 times, earns about half a tick a fill, loses 8.1 ticks inside the fill's
    own 100 ms and 19.8 ticks a fill after a minute (about $83k on one bitcoin a side).
  * An idealised fast maker that cancels before every sweep loses 8.7 ticks a fill (about $17k); one that also
    withdraws the side the imbalance threatens loses 4.6, mostly by trading a third as often.
  * The ordering holds on all three days; the best is −2.9 ticks a fill. A tick is 0.037 bp, so the best rule needs
    a rebate of about 0.1 bp a fill to break even.
  * Who hits the quote; the inventory (standard deviation 3.9 units against a limit of 5); what the replay leaves out.
* **Fill rates and optimal quotes:**
  * the intensity λ(δ) = Ae^{−kδ} fitted to every second: A = 0.23 a second, k = 0.035 per tick (half every 20 ticks);
    k is 0.026 and 0.051 on the two weekdays;
  * GLFT on Bitcoin: a half-spread of 30 ticks at γ = 10⁻⁴, 39 at 10⁻², 76 at 10⁻¹, with skews of 2.6 to 125 ticks a
    unit;
  * tested on the tape: fills lose 17.8 ticks at 5 ticks out and 8.3 at 20; break even near 30 (+1.0); earn +19.7 at
    45, about 355 fills and 7,000 ticks an hour, before queues and fees — an upper bound, from sweeps' overshoot;
  * what the model gets wrong (fills are news) and how alpha enters the quotes (Cartea, Jaimungal and Ricci 2014).
* **Tick size and queue position:**
  * a pinned spread turns price competition into a queue race; a rough calibration of the sniping half-spread on
    Bitcoin (0.31 tick, below the half-tick floor);
  * time priority against pro-rata; Part 36's value of the front of the queue;
  * the optimal tick (Dayri and Rosenbaum 2015); fees off the grid; who gains when the tick shrinks; the US tick-size
    pilot (2016–2018) and the 2024 half-cent amendments.
* **Making markets in ETFs:**
  * creation and redemption in kind; the arbitrage band; the pause's $80 fund with an $84 NAV and a 2% cost, worked;
  * two layers of makers; tax efficiency, custom baskets (the SEC's 2019 ETF rule); indicative values;
  * March 2020: HYG fell 22% from its January high to 23 March with volume 5.4 times its 2019 median (TLT fell 16% in
    nine days, with volume 9.3 times); stale NAVs and full dealer balance sheets (as reported by BIS economists and
    others; Haddad, Moreira and Muir 2021); the Federal Reserve's facility;
  * leveraged and inverse funds' rebalancing, L(L − 1) × return × assets (Cheng and Madhavan 2009).
* **The speed race:**
  * Budish, Cramton and Shim (2015): with N equally fast firms a stale quote is sniped (N − 1)/N of the time, and the
    half-spread λ_J J/(λ_I + λ_J) does not depend on N;
  * simulated with λ_I = 1, λ_J = 0.1 and J = 4: profits cross at 0.364, and stay equal for N = 2 to 30;
  * the arms race; Aquilina, Budish and O'Neill (2022) on the LSE (races in about a fifth of volume, a tax of about
    half a basis point);
  * the physics: Chicago to New Jersey in 3.8 ms by air, 5.6 in fibre;
  * remedies: batch auctions, speed bumps, an auction cleared by hand; why they have not spread (Budish, Lee and Shim).
* **The economics of fast market making:** Menkveld (2013); Baron, Brogaard, Hagströmer and Kirilenko (2019); what
  speed costs; hedging; stress (6 May 2010, 15 October 2014); obligations (MiFID II, designated makers); the size of
  the prize; options makers; crypto fee tiers and token-issuer contracts.
* **Rule 38: quote only what you can measure.** The House's sheet; controls before edge; going live; capital; four
  labs; two desks under one roof; three cases.
* **For the researcher: the sniping equilibrium.** Three lemmas, the theorem for any jump distribution, batch auctions,
  welfare and the arms race as a prisoner's dilemma; checked by simulation and on Bitcoin.

No strategy is registered in this part; the trial counter stands at 23,550.

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: how does a market maker earn a living?** The question; three findings; who makers are and what they sell;
  three things market making is not; where this sits; fifty years; the plan.
* **1. The maker's business.** The P&L; three risks; components; Avellaneda–Stoikov; the trade-off; in numbers; GLFT;
  how we got here; who does it today; flow types; many books.
* **2. A maker on the tape.** The design; the day's table; the waterfall; markout curves; the filter; who hits;
  slowness; inventory; three days; fees; what is missing.
* **3. Fill rates and optimal quotes.** The method; the curve; by day; GLFT's quotes; the test on the tape; per hour;
  why far quotes earn; the assumption; alpha in the quotes.
* **4. Tick size and queue position.** Pinned spreads; the rent; the queue race; pro rata; waiting; the optimal tick;
  sub-tick pricing; who gains; rules.
* **5. Making markets in ETFs.** Mechanics; the band; a worked arbitrage; two layers of makers; in kind; iNAV; March
  2020; price discovery; the Fed; leveraged funds; lessons.
* **6. The speed race.** The race; the model; the simulation; by N; the prize on Bitcoin; the arms race; measured;
  physics; remedies; a batch auction; adoption.
* **7. The economics of fast market making.** Inside one maker; across firms; costs; hedging; stress; obligations;
  rents; options; crypto.
* **8. Rule 38.** The sheet; limits; going live; capital; four labs; two desks; the module; three cases.
* **For the researcher: the sniping equilibrium.** Model; payoffs; undercutting; existence; the theorem; statics; the
  general case; four checks; batch logic and formula; welfare; the arms race; related work; open problems.
* **Outro.** Thirteen lines; three lessons; the part on one card; connections; six desk questions; the pause answer;
  twelve problems (two of qualifying-exam level, solved below); payoffs; references.

## Hands-on

* **Built and run here:**
  * fill intensities from Binance's best quotes and trades, fitted to Ae^{−kδ};
  * GLFT quotes from the fitted intensities and the measured volatility;
  * a market-making replay on Part 36's queue model, slow, fast and filtered, with markouts at 1, 10 and 60 seconds;
  * deep-quote markouts at seven distances;
  * the sniping game simulated, with batch auctions and with Bitcoin's empirical jump sizes;
  * HYG and TLT through March 2020.
* **Labs, from the House's source:** `fill_intensity`, `glft`, `maker_replay`, and `bcs_spread` with `bcs_simulate`.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Guéant, *The Financial Mathematics of Market Liquidity* (2016) | market making, GLFT | 1, 3 |
| Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015) | ch. 10, market making with alpha | 1, 3 |
| Lehalle and Laruelle, *Market Microstructure in Practice* (2018) | tick size, HFT, venues | 4, 6, 7 |
| Gastineau, *The Exchange-Traded Funds Manual* (2010) | creation, redemption, arbitrage | 5 |

## Papers, chapter by chapter

* ch. 1: Garman (1976), *JFE*; Ho and Stoll (1981), *JFE*; Glosten and Milgrom (1985), *JFE*; Stoll (1989), *JF*;
  Huang and Stoll (1997), *RFS*; Avellaneda and Stoikov (2008), *Quantitative Finance*; Guéant, Lehalle and
  Fernandez-Tapia (2013), *Mathematics and Financial Economics*; Christie and Schultz (1994), *JF*.
* ch. 2: Menkveld (2013), *JFM*; Part 36's queue model.
* ch. 3: Avellaneda and Stoikov (2008); Guéant, Lehalle and Fernandez-Tapia (2013); Cartea, Jaimungal and Ricci
  (2014), *SIAM J. Financial Math.*
* ch. 4: Dayri and Rosenbaum (2015), *Market Microstructure and Liquidity*; the SEC tick-size pilot (2016–2018).
* ch. 5: Pan and Zeng (2019); Aramonte and Avalos (2020), *BIS Bulletin*; Haddad, Moreira and Muir (2021), *RFS*;
  Cheng and Madhavan (2009), *J. Investment Management*.
* ch. 6: Budish, Cramton and Shim (2015), *QJE*; Aquilina, Budish and O'Neill (2022), *QJE*; Budish, Lee and Shim
  (2019).
* ch. 7: Menkveld (2013); Baron, Brogaard, Hagströmer and Kirilenko (2019), *JFQA*.
* Research: Budish, Cramton and Shim (2015); Baldauf and Mollner (2020), *JF*; Menkveld and Zoican (2017), *RFS*.

## For the researcher

* **The model.** A public value jumps by ±J at rate λ_J; uninformed investors arrive at rate λ_I and pay the
  half-spread h; N equally fast firms, whose simultaneous messages are processed in random order. One provides
  liquidity; the others snipe.
* **The proof.**
  * Lemma 1 (payoffs): the provider earns λ_I h − λ_J (J − h)(N − 1)/N; a sniper earns λ_J (J − h)/N. Their
    difference, λ_I h − λ_J (J − h), does not contain N.
  * Lemma 2 (indifference): if providing paid more, a rival would undercut; if less, the provider would snipe. So
    the two roles pay the same.
  * Lemma 3 (existence and uniqueness): the difference is −λ_J J < 0 at h = 0, λ_I J > 0 at h = J, and strictly
    increasing, so it has one root.
* **The theorem.** h* = λ_J J/(λ_I + λ_J), independent of N. The sniping rent per unit time equals what investors pay
  in the spread.
  * For random jump sizes, h* is the unique root of λ_I h = λ_J E[(|J| − h)⁺]. Mean-preserving spreads widen h* or
    leave it unchanged, because (|J| − h)⁺ is convex.
  * In a batch auction stale quotes are never filled. With latency δ and interval τ the sniping term scales like
    δ/τ, so 1 µs against 100 ms shrinks it by five orders of magnitude.
  * The arms race is a prisoner's dilemma: buying speed is dominant whenever its cost is below the races it would
    otherwise lose, and the total N·c is a social cost.
* **Measured.**
  * Simulation (λ_I = 1, λ_J = 0.1, J = 4): the profit curves cross at the formula's 0.364.
  * The two roles pay the same for N = 2, 3, 5, 10 and 30 (0.183 and 0.181 at N = 2; 0.0135 and 0.0121 at N = 30).
  * With frequent batch auctions, sniping earns nothing (20,093 jumps).
  * Bitcoin's own jump sizes, 0.63 changes a second averaging 13 ticks against takers' 24 a second, give
    h* ≈ 0.33 tick. That is below the half-tick floor, so the tick, not sniping, binds the spread; Chapter 2's losses
    come from information in the order flow.
* **Simplifications.**
  * No private information and no inventory.
  * Identical speeds.
  * Every mid change treated as public news.
* **Open problems.**
  * An equilibrium spread with private information, public jumps and inventory, estimated from message data.
  * Where liquidity goes when continuous and batch markets coexist, and whether the outcome is efficient.
  * Sniping across crypto's many venues, with unequal latencies and no consolidated quote.

## Build it

```bash
python -m videos.quant.quant38.compute                            # every item; a few minutes; reuses Part 36's data
python -m pytest -q tests/test_quant_house.py -k making
EXPLAINER_TTS=silent python tools/qa_scene.py quant38 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant38                                      # the narrated part
```

## Desk questions, with solutions

1. **Where does a market maker's profit come from?** The half-spread plus the rebate, minus the markout after fills,
   plus or minus inventory. On Bitcoin at the touch the markout is about forty times the half-spread.
2. **Why skew quotes with inventory?** So that the next fills reduce it. GLFT's skew per unit is
   √(σ²γ(1 + γ/k)^{1 + k/γ}/(2Ak)).
3. **What do fill rates say about where to quote?** Intensities that decay slowly with distance put the optimal
   quotes far out: on Bitcoin, about 30 ticks.
4. **Why does a pinned spread create a speed race?** Makers cannot undercut on price, so they compete for queue
   position, and position goes to the fastest.
5. **What keeps an ETF near its NAV, and when does it fail?** Creation and redemption arbitrage, bounded by trading
   costs and balance sheet. It failed in March 2020 for bond funds whose NAVs were stale and whose dealers were full.
6. **Why doesn't competition in speed narrow the spread?** The sniping half-spread λ_J J/(λ_I + λ_J) does not depend
   on the number of firms. Batch auctions remove the prize.

## Problems, with solutions

1. **Edge.** 0.5 + 0.2 − 0.9 = −0.2 tick a fill: the rebate does not cover the markout.
2. **Avellaneda–Stoikov.**
   * The total spread is γσ²(T − t) + (2/γ)ln(1 + γ/k) = 0.4 + 20 ln(1.0667) = 1.69.
   * The reservation price shifts by −qγσ²(T − t) = −0.8.
3. **k from fill probabilities.** k = ln(0.3/0.05)/(45 − 1) = 0.041 per tick; the intensity halves every 17 ticks.
4. **The value of speed.**
   * The slow maker loses 20 × 40,000 = 800,000 ticks a day; the fast one loses 9 × 20,000 = 180,000.
   * Speed is worth 620,000 ticks a day, but both still lose.
5. **Rent in a pinned spread.** The 0.7 cent above the natural spread is rent, earned by makers who get filled. Under
   time priority it goes to the front of the queue, so to the fastest; under pro rata, to size.
6. **ETF arbitrage.**
   * Buy at $80 and redeem for bonds marked at $84; selling them costs 2% ($1.68). The profit is $2.32 a share,
     2.9%, on paper.
   * It may not happen: the NAV may be stale, so the bonds cannot be sold at $84. Dealers' balance sheets may be full,
     and participants have no obligation to act.
7. **Sniping probability.** The provider wins its race to cancel 1/N of the time, so a stale quote is sniped 4/5 of
   the time with five firms and 9/10 with ten.
8. **Sniping half-spread.**
   * h* = 2 × 3/(10 + 2) = 0.5.
   * With jumps of 1 or 5, 10h = 2 × ½[(1 − h) + (5 − h)] for h < 1, so h = 0.5 again: both sizes exceed the
     half-spread, so the excess is linear in the jump.
9. **Batch auctions.** δ/τ = 5 µs/50 ms = 10⁻⁴: the sniping component shrinks ten-thousand-fold.
10. **Speed investment, N = 4.** Let R be the sniping rent per unit time, shared R/N each when speeds are equal.
    * If rivals do not invest, investing raises the share from R/4 to R, so investing pays when c < 3R/4.
    * If all rivals invest, not investing loses every race, so investing pays when c < R/4.
    * Investing is dominant for c < R/4. In equilibrium everyone invests, the shares return to R/4, and 4c is wasted.
11. **(qual) The sniping equilibrium.**
    * **Payoffs.** The provider earns λ_I h − λ_J E[(|J| − h)⁺](N − 1)/N; each sniper earns λ_J E[(|J| − h)⁺]/N.
    * **Indifference.** Undercutting and switching roles force the two to be equal:
      Φ(h) = λ_I h − λ_J E[(|J| − h)⁺] = 0. N cancels.
    * **Uniqueness.** Φ(0) = −λ_J E|J| < 0. Φ is strictly increasing, since λ_I h rises and E[(|J| − h)⁺] does not,
      and Φ(h) → ∞ as h grows. So it has exactly one root.
    * **Constant J.** The root is h* = λ_J J/(λ_I + λ_J).
    * **Rents.** At h*, investors pay λ_I h* = λ_J E[(|J| − h*)⁺] per unit time: exactly the value of the races.
      The N firms split it equally, 1/N each, so every dollar of sniping rent is paid by investors.
12. **(qual) GLFT from the HJB.**
    * **Value function.** For exponential utility, u(t, x, q, S) = −exp(−γ(x + qS + θ_q(t))).
    * **Optimal quotes.** With intensities Ae^{−kδ}, the HJB in θ gives
      δ^b_q = θ_q − θ_{q+1} + (1/γ)ln(1 + γ/k) and δ^a_q = θ_q − θ_{q−1} + (1/γ)ln(1 + γ/k).
    * **Linearisation.** Substituting w_q = e^{kθ_q} gives a linear system ẇ = Mw: a tridiagonal matrix, with
      −(k/2)γσ²q² on the diagonal and A(1 + γ/k)^{−(1 + k/γ)} off it.
    * **Long horizon.** As T → ∞, w tends to the principal eigenvector. A continuous approximation (a Hermite
      equation) gives θ_q − θ_{q±1} ≈ ±((2q ± 1)/2)·√(σ²γ(1 + γ/k)^{1 + k/γ}/(2Ak)).
    * **The limit γ → 0.** (1/γ)ln(1 + γ/k) → 1/k and the skew vanishes, so the half-spread tends to 1/k: the
      revenue-maximising distance of Chapter 1.

## Data and reproducibility

* **Binance.**
  * Public daily `bookTicker` and `aggTrades` for the BTCUSDT USD-M perpetual, 16, 17 and 20 May 2023, all checked
    against Binance's published SHA-256 files.
  * Part 36's 100-ms grid and queue model.
* **Yahoo Finance.** Daily bars for HYG and TLT, 2015–2020, for prices and volume only. NAV histories and premiums are
  quoted from the cited studies, not computed.
* **Simulation.**
  * The sniping game, with seeds fixed in `compute.py`.
  * Continuous trading against frequent batch auctions.
  * Bitcoin's empirical jump sizes.
* **No registration.** The counter stays at 23,550.
* **Quoted, not computed.**
  * The proprietary HFT studies (Menkveld; Baron et al.; Aquilina et al.) and firm disclosures.
  * Enforcement cases about crypto market-making contracts, described as reported.

---

# 量化金融，从零搭建 — 第38部分：做市、ETF与速度竞赛

四十三部分量化金融系列的第38部分，第六幕“市场微观结构”的第四部分，也是最后一部分，按本系列的博士层次构建。它讨论第35至37部分每一笔订单对面的那门生意：做市商如何谋生、成本是什么、为什么这门生意变成了微秒之争，以及同一门生意如何让交易所交易基金贴近其持仓价值。

测量使用币安BTCUSDT永续合约的公开最优报价流和归集成交（2023年5月16、17、20日，第36部分的100毫秒网格），以及雅虎财经上HYG和TLT的日线（2015–2020）。

本部分涵盖：
* **做市商的生意**：利润 = 半价差 + 返佣 − 事后损失 ± 存货；Avellaneda–Stoikov与GLFT。
* **成交记录上的做市商**：
  * 5月17日，慢速做市商成交42,019次，每笔亏19.8跳；
  * 理想化的快速做市商每笔亏8.7跳；
  * 加上失衡过滤后每笔亏4.6跳；
  * 三天中最好的一天是−2.9跳。
* **成交率与最优报价**：
  * k = 0.035/跳；GLFT半价差约30跳；
  * 在成交记录上检验：30跳处约持平（+1.0），45跳处每笔+19.7跳，这是未计排队和手续费的上限。
* **跳价与队列位置**：被钉住的价差把价格竞争变成队列竞赛；比特币上的狙击半价差约0.31跳，低于半跳下限。
* **ETF做市**：申购赎回、套利区间；2020年3月HYG从1月高点到3月23日下跌22%，成交量达2019年中位数的5.4倍。
* **速度竞赛**：Budish–Cramton–Shim的狙击价差与公司数量无关；模拟在0.364处相交；批量拍卖消除奖金。
* **高频做市的经济学**、**第38条规则：只为你能测量的东西报价**。
* **写给研究者**：狙击均衡的证明，推广到任意跳动分布，批量拍卖、福利和军备竞赛，并用模拟和比特币数据检验。

本部分不登记策略，试验计数仍为23,550。

*这是方法教育，不是投资建议。*

## 章节（约55分钟）

* **开场**：问题、三个发现、做市商是谁、做市不是什么、五十年的历史、计划。
* **1. 做市商的生意**：损益、三种风险、价差构成、Avellaneda–Stoikov、核心权衡、GLFT、历史、今天谁在做、订单流类型。
* **2. 成交记录上的做市商**：设计、全天结果、分解、事后损益曲线、过滤器、对手是谁、慢的代价、存货、三天、手续费、遗漏了什么。
* **3. 成交率与最优报价**：方法、曲线、分日、GLFT报价、在成交记录上检验、每小时、远处报价为何赚钱、假设、阿尔法如何进入报价。
* **4. 跳价与队列位置**：被钉住的价差、租金、队列竞赛、按比例分配、等待、最优跳价、规则。
* **5. ETF做市**：机制、套利区间、算例、两层做市商、实物申赎、2020年3月、价格发现、美联储、杠杆基金、教训。
* **6. 速度竞赛**：比赛、模型、模拟、按公司数量、比特币上的奖金、军备竞赛、实测、物理、补救办法、批量拍卖。
* **7. 高频做市的经济学**：一家做市商的内部、跨公司、速度的代价、对冲、压力、义务、奖金规模、期权、加密市场。
* **8. 第38条规则**：汇总表、控制、上线、资本、四个实验、两个交易台、三个案例。
* **写给研究者**：模型、三个引理、定理、一般情形、四项检验、批量拍卖、福利、军备竞赛、相关工作、开放问题。
* **结尾**：回顾、教训、公式卡、联系、交易台问题、习题（两道资格考试题，解答见下文）。

## 写给研究者

* **模型**：
  * 公开价值以速率λ_J跳动±J；
  * 无信息投资者以速率λ_I到达并支付半价差h；
  * N家同样快的公司，消息按随机顺序处理。
* **证明**：
  * 引理一：两种角色的收益之差 λ_I h − λ_J(J − h) 不含N；
  * 引理二：压价和换角色迫使两者相等；
  * 引理三：该差在0处为负、在J处为正、严格递增，故根唯一。
* **定理**：h* = λ_J J/(λ_I + λ_J)，与N无关，狙击租金等于投资者在价差中付出的。
  * 一般跳动下，h*是 λ_I h = λ_J E[(|J| − h)⁺] 的唯一根。
  * 批量拍卖中狙击项按δ/τ缩小。
  * 军备竞赛是囚徒困境。
* **检验**：
  * 模拟在0.364处相交，N从2到30两种角色收益相等；
  * 批量拍卖中狙击收益为零；
  * 比特币的经验跳动给出约0.33跳，低于半跳下限。
* **开放问题**：
  * 同时含私人信息、公开跳动和存货的均衡价差；
  * 连续市场与批量市场并存；
  * 加密市场多场所之间的狙击。

## 交易台问题与解答

1. 利润：半价差加返佣，减去事后损失，加减存货；比特币上事后损失约为半价差的四十倍。
2. 按存货倾斜报价，让接下来的成交减少存货。
3. 成交率衰减缓慢，最优报价在约30跳之外。
4. 价差被钉住时只能争夺队列位置，位置归最快的人。
5. 申赎套利让ETF贴近净值；2020年3月净值过时、交易商资产负债表已满时失效。
6. 狙击价差与公司数量无关；批量拍卖消除奖金。

## 习题与解答

1. 0.5 + 0.2 − 0.9 = −0.2跳。
2. 总价差1.69，保留价格偏移−0.8。
3. k = ln 6/44 = 0.041/跳。
4. 慢速每天亏80万跳，快速亏18万跳；速度价值62万跳，但两者都亏。
5. 0.7美分是租金；时间优先下归队列前端即最快者，按比例分配下归挂单量。
6. 账面利润每股2.32美元；但净值可能过时、交易商资产负债表可能已满，参与者也没有义务。
7. 五家公司时被狙击概率4/5，十家时9/10。
8. h* = 0.5；跳动为1或5时仍为0.5。
9. δ/τ = 10⁻⁴，缩小一万倍。
10. c < R/4时投资是占优策略；均衡中人人投资，浪费4c。
11. **（资格考试）狙击均衡**：
    * Φ(h) = λ_I h − λ_J E[(|J| − h)⁺] 严格递增、在0处为负，根唯一且不含N；
    * 常数跳动时 h* = λ_J J/(λ_I + λ_J)；
    * 狙击租金等于 λ_I h*。
12. **（资格考试）由HJB推导GLFT**：
    * 指数效用下作变换 w_q = e^{kθ_q}，得到线性系统；
    * 长期限下趋于主特征向量，连续近似给出报价的倾斜项；
    * γ → 0 时半价差趋于1/k。

## 数据与复现

* **币安公开数据**：BTCUSDT永续合约的最优报价和归集成交，均与币安公布的SHA-256核对。
* **雅虎财经**：HYG与TLT的日线；净值与溢价引自所列研究。
* **不登记策略**：试验计数仍为23,550。
* **引用而非计算**：专有的高频研究和公司披露；加密做市合同的执法案件，按报道表述。
