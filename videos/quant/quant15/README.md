# Quant, Built — Part 15: Exotics and Structured Products

Part 15 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives: a hook, eighteen chapters and an outro, about 58 minutes.
It covers:

* a structured note taken apart into priced pieces, the issuer's funding and margin, and what buyers earned;
* barriers: reflection, the closed form and its PDE image, discrete monitoring, and static hedges;
* digitals, one-touches and the call-spread hedge, simulated; Asians and lookbacks;
* the snowball (雪球): the coupon as a linear solve, its outcomes, carry, and the issuer's Greeks in 3D;
* January 2024 rebuilt on the real CSI 500 path; Korea's HSCEI-linked ELS in 2015–16 and 2021–24; Natixis (2018);
* worst-of payoffs, correlation and the correlation skew; cliquets and the risk vega cannot see;
* uncertain volatility, model risk measured on the bitcoin Surface, and a book's hedging flows;
* a neural surrogate trained on screen against a polynomial; how desks reserve; the 2023–2026 frontier.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`exotics`](../../../explainer/quant/house/exotics.py) pricer, tested in `tests/test_quant_house.py`).

*An education in methods, not investment advice. Firms and episodes are described from the public record;
investors' losses are reported as the regulators and the press reported them.*

## Chapters (about 58 minutes)

| # | Chapter | Min | Signature visual · experiment |
|---|---|---|---|
| — | The snowball (hook) | 2.4 | CSI 500 path with 2022–23 knock-in levels; the history strip 1973–2024 |
| 1 | Anatomy of a note, and the margin | 3.0 | the note's value stacked block by block (`decompose`); coupon against funding spread |
| 2 | Who buys, and what they earned | 2.2 | 84 vintages 2017–2023 riding the real path (`buyers`); the research record |
| 3 | Barriers: reflection, the closed form, the PDE | 2.9 | mirrored paths and their histograms; DOC value and delta surfaces in 3D (`barrier_surface`); lab |
| 4 | Watched at the close, hedged without trading | 3.5 | unseen excursions; BGK table (`barrier`); Derman–Ergener–Kani (`dek`); Carr–Ellis–Gupta under skew (`static`) |
| 5 | Digitals, one-touches and the call-spread hedge | 3.2 | delta spike; the two hedges on one path and on 40,000 (`digital_hedge`); one-touch (`onetouch`); skew (`digital_skew`) |
| 6 | Averages and extremes: Asians and lookbacks | 2.3 | running average and minimum; the control-variate scatter (`asian_scatter`); lab |
| 7 | The snowball, priced | 3.6 | lab; 150 paths stopping and reddening (`outcomes`); V(c) = A + cB; carry and knock-in (`coupon_q`) |
| 8 | The issuer's Greeks, in three dimensions | 4.0 | value with the knock-in cliff; hedge, gamma, vega surfaces (`greeks3d`); bump-size replay (`bump_curve`) |
| 9 | January 2024: the snowballs melt | 3.2 | crisis file; the 36-note book run day by day (`book2024`); the hedgers' daily trades |
| 10 | Korea's ELS, twice, and a dealer's loss | 3.2 | 2015 vintages (`korea2015`); FSC 2016; 2021 vintages (`korea`); FSS 2024–25; Natixis firm file |
| 11 | Worst-of, correlation and the correlation skew | 3.9 | the folded payoff in 3D with the correlated cloud collapsing; regimes (`corr_regimes`); worst-of snowball (`worstof_ac`) |
| 12 | Cliquets: the risk vega cannot see | 2.7 | monthly resets; the cliquet surface over (σ, cap) with its zero-vega ridge (`cliquet`) |
| 13 | Uncertain volatility: the price of not knowing | 2.8 | the BSB solve marching back with its σ map (`uvm_film`); lab; non-additivity and the Lagrangian replay (`uvm_book`) |
| 14 | Same vanillas, different exotics | 3.0 | four models' path fans and smiles; exotics table (`modelrisk`); the entropic tilt (`robust`) |
| 15 | Dealer flows: when the hedges move the market | 2.5 | a book's vega 2021–2024 on the real path (`book_vega`); the vega supply (schematic) |
| 16 | A neural pricer for the book, trained on screen | 2.6 | lab; `TrainingReplay` with 3 seeds (`surrogate_replay`); the polynomial baseline; speed |
| 17 | Industry: how desks mark, reserve and report | 2.9 | prudent valuation, day-one P&L, FRTB, conduct, validation; the House's Rule 15 |
| 18 | Frontier, 2023–2026 | 2.3 | three digital-delta estimators racing, 5 seeds (`pathwise_digital`); the papers |
| — | Recap, desk questions, problems | 2.5 | twelve lines, three desk questions, eight problems |

**Labs** (House code on screen, then run): `down_out_call` (ch. 3), `static_dic_hedge` (ch. 4),
`geometric_asian_call` (ch. 6), `snowball_payoff` (ch. 7), `uvm_price` (ch. 13), the surrogate's training loop
(ch. 16). **Replays:** the surrogate (3 seeds, polynomial baseline, label-noise floor), the Lagrangian UVM optimiser,
the bump-size curve (3 seeds), the entropic tilt, the three delta estimators (5 seeds). **3D:** chapters 3, 8, 11, 12.

## Textbook audit

| Book · section | Where |
|---|---|
| Hull, *OFOD* 11th ed., "Exotic options" (ch. 27; ch. 26 in the Global Edition): packages | ch. 1 |
| — gap options; nonstandard American | gap = digital + call (ch. 5); American → Part 16 |
| — forward start; cliquets | ch. 12 |
| — compound; chooser | chooser by parity (problem 7); compound options as equity on assets → Part 20 |
| — barrier; binary; lookback; shout; Asian | ch. 3–4; ch. 5; ch. 6 (shout named as the lookback's cousin) |
| — exchange options; options on several assets | ch. 11 (Margrabe derived; Stulz named) |
| — volatility and variance swaps | Part 12 |
| — static options replication | ch. 4 (Derman–Ergener–Kani built, Carr–Ellis–Gupta derived and tested) |
| Hull, "More on models and numerical procedures" (path-dependent numerics) | ch. 6 (state augmentation, Vecer), Part 16 |
| Shreve II ch. 7: 7.2 maximum of BM with drift; 7.3 knock-out barriers | ch. 3 (reflection, Girsanov, the PDE) |
| — 7.4 lookbacks; 7.5 Asians (augmentation, change of numéraire) | ch. 6 |
| Bouzoubaa–Osseiran ch. 2 (structured products); 3.10 (structuring) | ch. 1–2 |
| — 3.9 Asians; 5.7–5.8 vanna, volga, multi-asset sensitivities | ch. 6; ch. 8, 11 |
| — ch. 7 correlation; ch. 8–9 dispersion, worst-of, best-of, rainbow | ch. 11; dispersion trading → Part 11; quantos → Part 22 |
| — ch. 10 barriers; ch. 11 digitals; ch. 12 autocallables | ch. 3–4; ch. 5; ch. 7–8, 11 |
| — ch. 13–14 cliquets (reverse, Napoleon) | ch. 12 |
| — ch. 15 mountain range | ch. 11 (named) |
| — ch. 16 volatility derivatives; ch. 17–21 hybrids, dynamic strategies | Part 12; Parts 19, 21, 22, 32 |
| Guyon–Henry-Labordère: the uncertain volatility model; local correlation, particle method | ch. 13; ch. 11 (named); LSV → Part 13; BSDEs → Part 17 |
| Wilmott, *PWOQF*: exotic and path-dependent options, barriers, Asians, lookbacks, uncertain parameters, static hedging | ch. 3–6, 12–13, 4 |
| Gatheral, *The Volatility Surface*: barrier options (put–call symmetry, static hedge); exotic cliquets | ch. 4; ch. 12 |
| Taleb, *Dynamic Hedging*: binaries, barriers, multi-asset options | ch. 5, 3–4, 11 |

## Papers

Classics: Merton (1973); Margrabe (1978); Goldman, Sosin, Gatto (1979); Stulz (1982); Johnson (1987); Kemna, Vorst
(1990); Reiner, Rubinstein (1991); Conze, Viswanathan (1991); Rubinstein (1991, "Somewhere over the rainbow");
Avellaneda, Levy, Parás (1995); Lyons (1995); Derman, Ergener, Kani (1995); Avellaneda, Parás (1996); Broadie,
Glasserman, Kou (1997); Carr, Ellis, Gupta (1998); Boyer, Gibson, Loretan (1999); Vecer (2001); Forbes, Rigobon
(2002); Cont (2006); Carr, Lee (2009); Glasserman, Xu (2014).
Investors: Henderson, Pearson (2011); Célérier, Vallée (2017); Egan (2019); Vokata, "Engineering lemons" (working
paper); Calvet, Célérier, Sodini, Vallée (2023).
Frontier: Zeron, Wu, Ruiz (2023); Sharma, Chen, Noh, DeJesus, Schlener (2024, two papers); Cibrario et al. (2025);
Goudenège, Molent, Zanette (2025); Glasserman, Karmarkar (2025); Higgins (2026); Che, Lim, Sun (2026); Lakshtanov
(2026); Fukasawa (2026); Lopez-Piqueres, Acharya, Sun, Kumar (2026). Full citations and the public-record sources
are in [READING.md](../READING.md).

*Reading notes.* Compound options (Geske 1979) return in Part 20 as equity priced as an option on a firm. Thematic
and risk-control indices (Bouzoubaa–Osseiran ch. 21) belong to Part 32. Branching diffusions (Guyon–Henry-Labordère)
are beyond this part. A digital's price is minus the call's slope in strike, so the digital-vega identity in
Bouzoubaa–Osseiran's appendix B is chapter 5's skew term.

## Build it

```bash
python -m videos.quant.quant15.compute                    # every number (greeks3d, surrogate, cliquet take minutes)
EXPLAINER_TTS=silent python tools/qa_scene.py quant15 Greeks   # one chapter, silent, with a contact sheet
python tools/make.py quant15 --cpu-voice -q m             # English and Chinese, narrated by Kokoro on the CPU
```

`modelrisk` reads Part 13's calibrations (`.cache/quant13/calibrate.json`) and `digital_skew` Part 12's Surface;
build Parts 12 and 13 first. About 25 CPU-minutes on an idle core in all.

## Desk questions, with solutions

1. **A digital as a call spread.**
   * Buy the K − ε call and sell the K call, ×1/ε. It pays at least the digital everywhere.
   * The extra cost is about ε/2 times the risk-neutral density at K (chapter 5: 0.541 against 0.486 at ε = 2).
   * Its delta is bounded by 1/ε. Wider is dearer but hedgeable: in chapter 5 its hedging error falls about
     three-fold when rebalancing 16 times as often, the digital's under two-fold.
2. **The snowball issuer's vega: sign, and where it peaks.**
   * The issuer is long the down-and-in put the buyer sold and short the coupons: more volatility makes a knock-in
     likelier, so the issuer is long vega.
   * It peaks with spot between the barrier and the start (about 0.9 of the start for a 75% knock-in), not at the
     barrier, where a knock-in is nearly certain and the put already behaves like a deep vanilla.
   * Once knocked in, the vega collapses. The issuer sells long-dated options against it: a vega supply that
     turns into demand when barriers break (chapter 15).
3. **A one-touch with zero drift, given the digital.** Twice the digital. Every path that ends beyond the barrier
   touched it, and by reflection every path that touched it is matched by a mirror path that ends beyond it. With
   r = q = 0 the log price drifts at −σ²/2 and the exact price is N(−d₂) + (S/H) N(−d₁), a little less than twice.
4. **(Extra) A worst-of on three indices.** You own the put on the worst performer, so you are short correlation (the
   put's cross-gamma is negative). No market quotes that input directly, and in a crash correlations rise (chapter
   11: 0.76 to 0.91 for the CSI 500 and CSI 1000): your marks move on a number you cannot hedge. Desks charge
   through the correlation skew and a reserve.

## Problems, with solutions

1. **Reflection.**
   * With r = q = 0, a path that touches H and ends at S_T > K has a mirror image ending at H²/S_T, below H²/K.
   * Counting the touched paths and weighting by S/H (the change of measure that keeps the mirrored path a
     martingale) gives DOC = C(S, K) − (S/H) C(H²/S, K).
2. **BGK.**
   * Between monitoring dates the path can cross and return unseen.
   * Siegmund's corrected diffusion approximation: the overshoot of a random walk at first passage has limiting mean
     β σ√Δt, β = −ζ(½)/√(2π) ≈ 0.5826.
   * So the discrete barrier acts like a continuous one moved away by that amount. Check: chapter 4's table.
3. **Geometric average.**
   * log G = (1/n) Σ log S_{t_i} is a linear map of a Gaussian vector: Gaussian, mean log S₀ + (r − q − σ²/2) t̄.
   * Variance σ² Σ_{i,j} min(t_i, t_j)/n² → σ²T/3 in continuous time.
   * Black–Scholes with these moments gives the closed form.
4. **The call spread's bound.**
   * The payoff [(S − K + ε)⁺ − (S − K)⁺]/ε is 1 for S ≥ K, (S − K + ε)/ε on [K − ε, K], 0 below.
   * It is never less than 1_{S>K}, so it dominates the digital; it converges as ε → 0.
5. **The snowball taken apart.**
   * Notional repaid unless knocked in and below 1 at maturity: a zero-coupon bond minus a down-and-in put.
   * The coupons: claims contingent on knock-out, or on survival without knock-in.
   * The buyer is short the put, so short vega, apart from a small long-vega piece in the coupons. The issuer is the
     reverse.
6. **The coupon as a linear solve.**
   * On each path the payoff is a + c·b, with a and b independent of c (a: the repaid principal or the knocked-in
     index; b: months/12 at a knock-out, 2 if alive and never knocked in, 0 otherwise, all discounted).
   * Taking expectations, V(c) = A + cB; V(c*) = 1 gives c* = (1 − A)/B (chapter 7: 13.35%).
7. **The chooser.** At t₁ the holder takes max(C, P). By parity P = C − S e^{−q(T−t₁)} + K e^{−r(T−t₁)}, so
   max(C, P) = C + (K e^{−r(T−t₁)} − S e^{−q(T−t₁)})⁺: a call to T plus e^{−q(T−t₁)} puts to t₁ struck at
   K e^{−(r−q)(T−t₁)}.
8. **Margrabe.**
   * Use S₂ as numéraire: E^Q[e^{−rT}(S₁ − S₂)⁺] = S₂(0) E^{Q2}[(S₁/S₂ − 1)⁺].
   * Under Q2, X = S₁/S₂ is a martingale with volatility σ² = σ₁² + σ₂² − 2ρσ₁σ₂ (Itô for a ratio).
   * So the price is S₁(0)N(d₁) − S₂(0)N(d₂), d₁ = [log(S₁/S₂) + σ²T/2]/(σ√T), d₂ = d₁ − σ√T.

## Data and reproducibility

* China Southern CSI 500 ETF (510500.SS), China CSI 1000 ETF (512100.SS) and the HSCEI (^HSCE), daily closes, from
  Yahoo Finance's chart API (CSI index levels themselves have no history there); 2015–2025, checksummed.
* The snowball book, the Korean notes and the surrogate are stylized and labelled so; the episodes' facts come from
  Bloomberg, Reuters (via Asia Financial), Risk.net, StructuredRetailProducts and the Korean press.
* 512100.SS's Yahoo closes jump by a factor of 2.7 on 4 November 2016 (a rebasing): correlations use it from 2017.
* The bitcoin Surface (Deribit, 10 December 2025) and the four calibrated models come from Parts 12 and 13's caches.
* Regulators' and companies' own documents are cited where they exist (FSC 2016, Natixis 2018, EU 2016/101); press
  reports are labelled "as reported"; preliminary penalties are labelled preliminary.
* No strategy was tested; the trial counter is unchanged.

---


# 量化金融，从零搭建 — 第15部分：奇异期权与结构化产品

开场、十八章和结尾，约58分钟。本部分讲：

* 把一张结构化票据拆成有价格的零件：发行人的融资与利润，以及买家赚了什么；
* 障碍期权：反射原理、闭式解与偏微分方程的镜像、离散观察，以及静态对冲；
* 数字期权、一触即付和看涨价差对冲的模拟；亚式期权与回望期权；
* 雪球：票息是一个线性求解，它的结局分布、持有收益，以及发行人三维的希腊字母；
* 在中证500真实路径上重建2024年1月；韩国挂钩国企指数的ELS（2015–16与2021–24）；法国外贸银行（2018）；
* 最差表现、相关性与相关性偏斜；棘轮期权与vega看不见的风险；
* 不确定波动率、在比特币曲面上度量的模型风险，以及一本账的对冲流量；
* 在屏幕上训练、与多项式对比的神经网络替代定价器；交易台如何计提准备；2023–2026年的前沿。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录；投资者亏损按监管机构和媒体的报道描述。*

## 章节

| # | 章节 | 分钟 |
|---|---|---|
| — | 雪球（开场） | 2.4 |
| 1 | 票据的解剖，以及利润 | 3.0 |
| 2 | 谁在买，他们赚了什么 | 2.2 |
| 3 | 障碍期权：反射、闭式解与偏微分方程 | 2.9 |
| 4 | 收盘时观察，以及不交易的对冲 | 3.5 |
| 5 | 数字期权、一触即付和看涨价差对冲 | 3.2 |
| 6 | 平均与极值：亚式期权和回望期权 | 2.3 |
| 7 | 雪球的定价 | 3.6 |
| 8 | 发行人的希腊字母，三维呈现 | 4.0 |
| 9 | 2024年1月：雪球融化 | 3.2 |
| 10 | 韩国的ELS：两次危机与一家交易商的亏损 | 3.2 |
| 11 | 最差表现、相关性与相关性偏斜 | 3.9 |
| 12 | 棘轮期权：vega看不见的风险 | 2.7 |
| 13 | 不确定波动率：不知道的代价 | 2.8 |
| 14 | 同样的香草期权，不同的奇异期权 | 3.0 |
| 15 | 交易商流量：当对冲推动市场 | 2.5 |
| 16 | 账本的神经网络定价器，在屏幕上训练 | 2.6 |
| 17 | 业界：交易台如何估值、计提准备和报告 | 2.9 |
| 18 | 前沿，2023-2026 | 2.3 |
| — | 回顾、交易台问题与习题 | 2.5 |

教科书对照表与论文清单见上面的英文部分。

## 交易台问题与解答

1. **用看涨价差做数字期权。**
   * 买入K − ε看涨、卖出K看涨，乘以1/ε。它在任何地方的赔付都至少和数字期权一样多。
   * 额外成本约为ε/2乘以K处的风险中性密度（第5章：ε = 2时0.541对0.486）。
   * delta不超过1/ε。越宽越贵，但越能对冲：第5章中调仓频率提高16倍时，价差的对冲误差降为约三分之一，数字期权还不到一半。
2. **雪球发行人的vega：符号，以及峰值在哪里。**
   * 发行人持有买家卖出的向下敲入看跌期权，并欠着票息：波动率越高，敲入越可能，所以发行人做多vega。
   * 峰值出现在现价位于障碍和起点之间时（敲入线75%时约为起点的0.9），而不在障碍处：那里敲入几乎已成定局，看跌期权已经像深度实值的香草期权。
   * 敲入之后vega崩塌。发行人对冲时卖出长期期权：这种vega供给在障碍被击穿时变成需求（第15章）。
3. **零漂移的一触即付，已知数字期权。** 两倍的数字期权。每条在障碍外结束的路径都碰过障碍；由反射原理，每条碰过障碍的路径都对应一条在障碍外结束的镜像路径。
   r = q = 0时对数价格以−σ²/2漂移，精确价格是N(−d₂) + (S/H) N(−d₁)，略低于两倍。
4. **（附加）挂钩三个指数的最差表现。** 你持有表现最差者的看跌期权，交叉gamma为负，所以做空相关性。没有市场直接报价这个输入，
   而危机中相关性上升（第11章：中证500与中证1000从0.76升到0.91）：你的估值随一个无法对冲的数字变动。交易台通过相关性偏斜和准备金收费。

## 习题与解答

1. **反射。** r = q = 0时，一条触及H并收于S_T > K的路径有一条收于H²/S_T的镜像，位于H²/K之下。计数被触及的路径并乘以S/H
   （让镜像路径保持为鞅的测度变换），得DOC = C(S, K) − (S/H) C(H²/S, K)。
2. **BGK修正。** 在两个观察日之间，路径可能越过又回来而不被看见。西格蒙德的修正扩散近似表明，随机游走首次穿越时的超出量极限均值为
   β σ√Δt，β = −ζ(½)/√(2π) ≈ 0.5826。所以离散障碍相当于向外移动这么多的连续障碍。验证：第4章的表。
3. **几何平均。** log G = (1/n) Σ log S_{t_i}是高斯向量的线性变换，均值为log S₀ + (r − q − σ²/2) t̄，方差为σ² Σ_{i,j} min(t_i, t_j)/n²，
   连续时间下趋于σ²T/3。代入布莱克-斯科尔斯即得闭式解。
4. **看涨价差的界。** 收益[(S − K + ε)⁺ − (S − K)⁺]/ε在S ≥ K时为1，在[K − ε, K]上为(S − K + ε)/ε，以下为0。它不小于1_{S>K}，
   所以占优于数字期权，并在ε → 0时收敛。
5. **拆开雪球。** 除非敲入且到期时低于1，本金都会偿还：零息债券减去向下敲入看跌期权。票息是以敲出、或未敲入而存续为条件的权益。
   买方做空看跌期权，所以做空vega，票息中只有一小部分做多vega；发行人正好相反。
6. **票息作为线性求解。** 每条路径上的收益是a + c·b，a和b与c无关（a：偿还的本金或敲入后的指数；b：敲出时为月数/12，存续且未敲入时为2，否则为0，均已贴现）。
   取期望得V(c) = A + cB；令V(c*) = 1得c* = (1 − A)/B（第7章：13.35%）。
7. **选择期权。** 在t₁时持有人取max(C, P)。由平价P = C − S e^{−q(T−t₁)} + K e^{−r(T−t₁)}，所以max(C, P) = C + (K e^{−r(T−t₁)} − S e^{−q(T−t₁)})⁺：
   一份到T的看涨期权，加上e^{−q(T−t₁)}份到t₁、执行价为K e^{−(r−q)(T−t₁)}的看跌期权。
8. **马格拉布公式。** 以S₂为计价单位：E^Q[e^{−rT}(S₁ − S₂)⁺] = S₂(0) E^{Q2}[(S₁/S₂ − 1)⁺]。在Q2下X = S₁/S₂是鞅，
   波动率σ² = σ₁² + σ₂² − 2ρσ₁σ₂（比值的伊藤公式）。所以价格为S₁(0)N(d₁) − S₂(0)N(d₂)，d₁ = [log(S₁/S₂) + σ²T/2]/(σ√T)，d₂ = d₁ − σ√T。
