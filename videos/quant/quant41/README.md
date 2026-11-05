# Quant, Built — Part 41: Leverage, Liquidity and Crises

Part 41 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act VII, The System, built to the series' PhD layer. It asks how
borrowed money and short funding turn small losses into forced sales, forced sales into spirals, and one firm's
trouble into everyone's, and what a firm must do to survive it.

Data:
* FRED: the TED spread, Treasury yields (10-year, 2-year), three-month commercial paper, the Baa spread, US
  commercial bank deposits;
* Kenneth French's daily market and 49 industries, to 2020;
* Yahoo Finance: the Shanghai Composite, 2014–2016;
* public filings and official reviews, labelled as reported: LTCM's 1998 balance sheet (President's Working Group,
  1999), Lehman's end-2007 balance sheet, SVB's 2022 annual report and the Federal Reserve's April 2023 review.

Every historical series used for estimation lies in the research window (to 2020); the 2022–23 and 2015 series are
public macro and index data shown as history, not used to fit or select anything. The sealed hold-out is not opened.

The models: leverage arithmetic; Brunnermeier–Pedersen loss and margin spirals in a minimal fixed point;
Greenwood–Landier–Thesmar fire sales; Eisenberg–Noe clearing, with senior debt as in Acemoglu–Ozdaglar–Tahbaz-Salehi;
CoVaR, MES and SRISK; Diamond–Dybvig with a fire-sale value, and its global-games threshold.

## Chapters (about 53 minutes)

| | Chapter | What it shows |
|---|---|---|
| 0 | Hook | four findings; Act VII; forty years of crises; the desk question |
| 1 | Leverage and its cycle | the balance sheet; haircuts cap leverage; the 5× fund sells 56.7 of 90 (63%); the haircut × loss table; Minsky, Kindleberger, Geanakoplos; two liquidities |
| 2 | Spirals | the House's `spiral`; a 3% shock becomes 13.9% with fixed margins and 21.8% (7.25×) with margins that rise as prices fall; by shock size and market depth; Gorton–Metrick repo haircuts; Bagehot |
| 3 | Fire sales | Shleifer–Vishny; Greenwood–Landier–Thesmar on five banks; first round 34% of equity, fire-sale round 28%, 50% if twice as illiquid; Coval–Stafford; price-mediated contagion |
| 4 | Networks | Eisenberg–Noe on five banks (A pays 3.5 of 5, two rounds); ring, complete and clustered networks; the threshold n(a − v) = 5; core–periphery |
| 5 | Measuring systemic risk | CoVaR by quantile regression, 1990–2020: ΔCoVaR banks −1.29%, insurers −1.37%, other finance −1.45%; MES −3.45%, −2.74%, −3.81%; Lehman's SRISK $43bn at 31×; G-SIB surcharges; limits |
| 6 | 1998: LTCM | $125bn on $4.7bn (27×; a 3.8% fall erases it); crowded convergence trades; Baa spread 1.70 → 2.77; the recapitalisation |
| 7 | 2007–08 | the shadow banking structure; TED 0.46 → 4.58 (10 Oct 2008); Baa 1.68 → 6.16; Bear, Lehman, AIG, Reserve Primary; the response |
| 8 | March 2020 | the 10-year yield 0.54% → 1.18% (9–18 March) as stocks fell 31%; who sold; the basis trade; CP 1.59% → 2.53%; the Fed's two weeks |
| 9 | China 2015 | 2,050 → 5,166 (+152%) → 2,927 (−43% in eleven weeks); margin and grey margin; the national team; the 2016 circuit breaker (−6.9%, −7.0%), suspended after four days; the magnet effect |
| 10 | 2022–23 | gilts and LDI; SVB (HTM $91.3bn at cost, $76.2bn fair, against $16.0bn equity; $42bn out in a day); Diamond–Dybvig; the global-games threshold (1.49 at r = 0.85, 1.07 half insured); deposits −$351bn in three weeks; Credit Suisse and AT1; the policy answer |
| 11 | Rule 41 | the worst 2008 day with margins doubled: sell 9.8% at 2×, in 0.5 days; the leverage sweep; Archegos at 5×; 2008–09 with volatility-linked against through-the-cycle margins; the fire-sale externality; the rule |
| R | For the researcher | existence (Tarski) and uniqueness of the clearing vector, proved; fictitious default; checks (200/200; ≤ 5 rounds); the cycle counterexample; the contagion threshold derived and checked; fire sales added |
| 12 | Outro | thirteen lines, lessons, formulas, desk questions, problems, references |

## For the researcher

* **The model.** Bank i owes L_ij to j; p̄_i = Σ_j L_ij; Π_ij = L_ij/p̄_i; outside assets e ≥ 0. A clearing vector
  solves p = Φ(p) = min(p̄, e + Πᵀp).
* **Theorem 1 (existence; Eisenberg–Noe 2001 via Tarski).** Φ is monotone on the lattice [0, p̄], so greatest and least
  fixed points p⁺ ≥ p⁻ exist.
  * **Proof.** Iterate from p̄: Φ(p̄) ≤ p̄, and monotonicity keeps the order, so the iterates fall; they are bounded
    below by 0 and Φ is continuous, so the limit is a fixed point; any fixed point q ≤ p̄ stays below every iterate,
    so the limit is the greatest. From 0 upward, the least.
* **Theorem 2 (uniqueness).** If from every bank a chain of obligations reaches a bank with e_j > 0 (regularity), then
  p⁺ = p⁻.
  * **Proof.** Let d = p⁺ − p⁻ ≥ 0 and S = {d > 0}. For i ∈ S, p⁻_i < p̄_i, so p⁻_i = e_i + (Πᵀp⁻)_i, and p⁺_i ≤
    e_i + (Πᵀp⁺)_i. Subtract and sum over S: Σ_S d_i ≤ Σ_{j∈S} d_j Σ_{i∈S} Π_ji ≤ Σ_S d_j. So every j ∈ S pays only
    into S and the inequalities are equalities. Summing p⁺ over S and cancelling S's own payments leaves Σ_S e_i +
    inflows from outside S = 0: S is a closed group with no outside assets, which regularity forbids. So S = ∅.
* **Algorithm (fictitious default).** D₀ = ∅; D_{k+1} = banks that cannot pay given p⁽ᵏ⁾; solve the linear system with
  D_{k+1} paying all they have. The default sets grow, so it stops within n rounds, at p⁺.
* **Theorem 3 (the contagion threshold; Acemoglu–Ozdaglar–Tahbaz-Salehi 2015, symmetric case).** In the complete
  network of n banks with assets a, senior debt v and interbank debt y, a shock ε to one bank brings down all n iff
  ε > n(a − v).
  * **Derivation.** If the others pay, bank 0 has x₀ = a − ε + y − v; its shortfall y − x₀ = ε − (a − v) is shared by
    n − 1 creditors, each with buffer a − v; each fails iff (ε − (a − v))/(n − 1) > a − v, i.e. ε > n(a − v); by
    symmetry, one failing creditor means all.
* **Measured.**
  * **Uniqueness.** 200 random regular networks of 12 banks: fictitious default = iteration from p̄ = iteration from 0,
    to 10⁻⁸, in 200 of 200; at most 5 rounds (mean 3.19), against the bound of 12.
  * **The counterexample.** Two banks owing each other 1 with e = 0: from above (1, 1), from below (0, 0).
  * **The threshold.** n = 10, y = 6, a = 1.5, v = 1: the complete network jumps from 1 to 10 defaults at 5.05, the
    first point above 5 on a grid of 0.05; the ring climbs one bank at a time; two clusters cap at 5.
  * **Fire sales added** (each bank holds one unit of a common asset; defaulters sell; price e^{−0.15·units}): at a
    shock of 4 the complete network goes from 1 default to 10; at 2 the ring goes from 3 to 10.
* **Also proved in Chapter 10.** The global-games run threshold: with fire-sale value r, early = min(1, r/f), wait =
  θ(1 − f/r)/(1 − f) for f < r, else 0; θ* solves ∫₀¹(wait − early) df = 0. θ* = 1.49 at r = 0.85, 2.33 at r = 0.6;
  half insured, 1.07. Solving the noisy-signal game at σ = 0.3, 0.1, 0.03, 0.01 gives 1.34, 1.44, 1.47, 1.48 → 1.49.
* **Simplifications.** Stylised banks and parameters; industries for firms in CoVaR; one asset in the spiral; the
  House's stress treats its whole book as the market; Lehman's MES is the financial industry's.
* **Open problems.** Contagion when bilateral exposures are unobserved (maximum entropy understates it); clearing with
  prices and runs together (uniqueness and computation); measuring the non-bank network.

## Build it

```bash
python -m videos.quant.quant41.compute                            # every item; under a minute with cached data
python -m pytest -q tests/test_quant_house.py -k crisis
EXPLAINER_TTS=silent python tools/qa_scene.py quant41 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant41                                      # the narrated part
```

## Desk questions, with solutions

1. **A fund at 5× loses 10%; haircuts go from 20% to 30%. What must it sell?**
   * Assets 100 → 90, equity 20 → 10. At a 30% haircut it may hold 10/0.3 = 33.3. Sell 56.7, 63% of the book.
2. **How can a solvent bank fail?**
   * A run. If assets fetch r < 1 when sold early, withdrawing is a best response to others withdrawing
     (Diamond–Dybvig), so a bank worth more than its deposits can still be emptied. SVB, March 2023.
3. **Loss spiral vs margin spiral?**
   * Loss spiral: the holder sells to keep leverage constant as its equity falls.
   * Margin spiral: lenders cut the leverage allowed. Together, here, a 3% shock becomes 21.8%, about 7×.
4. **Is a more connected system safer?**
   * For small shocks yes, losses are shared; past the threshold n(a − v) the complete network fails all at once.
5. **One bank's contribution to systemic risk?**
   * ΔCoVaR: the system's VaR when the bank is in distress, less when it is at its median.
   * Or MES and SRISK: the capital it would lack in a crash.
6. **Why did Treasury yields rise in March 2020?**
   * A dash for cash: foreign official holders, open-end funds and basis traders sold; dealers' balance sheets were
     bound by leverage ratios, until the Fed bought and relaxed the ratio.

## Problems, with solutions

1. **Leverage after a loss.** A = 4, E = 1; a 5% loss gives A = 3.8, E = 0.8, leverage 4.75×. Restoring 4× means
   A = 3.2: sell 0.6, 15.8% of the book.
2. **A forced sale.** A = 8, E = 1, haircut 10%. A 3% fall gives A = 7.76, E = 0.76; at a 20% haircut the most it may
   hold is 3.8: sell 3.96, 51% of the book.
3. **The spiral's multiplier.** After a fall δ, E' = E − Aδ and the target is λE', so the sale is A(1 − δ) − λ(E − Aδ)
   = (λ − 1)Aδ. Its impact is γ(λ − 1)Aδ, which forces another round, and so on: δ_total = δ Σ (γ(λ − 1)A)^k =
   δ/(1 − γ(λ − 1)A), for γ(λ − 1)A < 1. At or above one the spiral does not converge.
4. **Leverage targeting.** λ = 20, A = 100, δ = 1%: sell (λ − 1)Aδ = 19. Check: A = 99, E = 4, target 80.
5. **A clearing vector.** Guess A and B default and C pays: p_A = 0.5 + p_C, p_B = p_A, p_C = min(1, 0.3 + p_B). With
   p_C = 1: p = (1.5, 1.5, 1), consistent. Equity: A 0, B 0, C 0.3 + 1.5 − 1 = 0.8. The system is regular (A and C
   hold outside assets, and B pays C), so it is the only one.
6. **A contagion threshold.** n(a − v) = 20 × 0.5 = 10.
7. **ΔCoVaR.** β(VaR − median) = 0.5 × (−4% − 0.1%) = −2.05%.
8. **SRISK.** kD − (1 − k)(1 − LRMES)E = 40 − 0.92 × 0.5 × 20 = 30.8.
9. **A run's payoffs.** f = 0.5 ≤ r = 0.8, so early = 1; wait = 1.2 × (1 − 0.625)/0.5 = 0.9 < 1: withdrawing is the
   best response.
10. **A bank's rate loss.** 90 × 6 × 3% ≈ 16.2 > 8: insolvent at fair value by about 8.2 (convexity makes the loss a
    little smaller).
11. **(qual) The clearing theorem.**
    * Existence and uniqueness: as above.
    * Fictitious default reaches p⁺: by induction p⁽ᵏ⁾ ≥ p⁺ and D_k ⊆ {i : p⁺_i < p̄_i}. Each step solves Φ restricted
      to the current default set, which is monotone in the set, so payments fall and the set grows. When D_{k+1} =
      D_k, p⁽ᵏ⁾ is a fixed point ≥ p⁺, hence p⁺. The set grows strictly until then, so at most n rounds.
12. **(qual) The global-games threshold.**
    * The marginal depositor at θ* believes the share running is uniform on [0, 1] (the Laplacian belief as noise
      vanishes), so θ* solves G(θ) = ∫₀¹(wait − early) df = 0.
    * G increases in θ (wait is linear in θ, early does not depend on it) wherever wait > 0, so the root is unique.
    * At θ = 1: for 0 < f < r, wait = (1 − f/r)/(1 − f) < 1 = early, since f/r > f; for f ≥ r, wait = 0 < early. So
      G(1) < 0 and θ* > 1: runs fell some solvent banks.
    * With insured share s, f = (1 − s)u. As s → 1, f → 0 for all u, where wait − early → θ − 1, so θ* → 1. As r → 1,
      wait → θ for f < 1 and early → 1, again θ* → 1: insurance and lending at par (r = 1) remove the run premium.

## Data and reproducibility

* FRED series: TEDRATE, BAA10Y, DGS10, DGS2, DCPF3M, DPSACBW027SBOG; Kenneth French's daily factors and 49 industries
  (through 2020); Yahoo Finance 000001.SS. Downloads are cached and checksummed in `videos/quant/data/manifest.json`.
* Every figure in the video comes from `compute.py`, cached in `.cache/quant41/`, and from the House's
  `explainer/quant/house/crisis.py`.
* Firms appear only as the public record describes them; allegations and reported figures are labelled as reported.
  Nothing here is investment advice.

---

# 量化金融，从零搭建 — 第41部分：杠杆、流动性与危机

本系列共四十三部分，这是第41部分，属于第七幕“体系”的第二部分，按本系列的博士层标准构建。它追问借来的钱和短期融资如何把小额亏损变成被迫
抛售，把被迫抛售变成螺旋，把一家公司的麻烦变成所有人的麻烦，以及一家公司要怎样才能挺过去。

数据：FRED（TED利差、十年期和两年期国债收益率、三个月期商业票据、Baa利差、美国商业银行存款）；肯尼斯·弗伦奇截至2020年的日度市场与49个
行业收益；雅虎财经的上证综指（2014—2016）；公开文件与官方报告（据报道）：长期资本管理公司1998年的资产负债表、雷曼2007年底的资产负债表、
硅谷银行2022年年报和美联储2023年4月的审查报告。用于估计的历史数据都在研究窗口内（截至2020年）；2015年和2022—23年的序列是作为历史展示的
公开宏观与指数数据，不用于拟合或选择任何东西。封存的样本外数据没有打开。

## 章节（约53分钟）

| | 章节 | 内容 |
|---|---|---|
| 0 | 开场 | 四个发现；第七幕；四十年的危机；交易台问题 |
| 1 | 杠杆及其周期 | 资产负债表；折扣率限制杠杆；五倍基金在90中卖出56.7（63%）；明斯基、金德尔伯格、吉纳科普洛斯；两种流动性 |
| 2 | 螺旋 | 3%的冲击在固定保证金下变成13.9%，在随价格下跌而上升的保证金下变成21.8%（7.25倍）；回购折扣率；白芝浩 |
| 3 | 甩卖 | 施莱弗—维什尼；五家银行上的格林伍德—兰迪耶—泰斯马模型；首轮损失为权益的34%，甩卖轮28%，流动性减半时50% |
| 4 | 网络 | 五家银行的艾森伯格—诺伊清算；环形、完全与分簇网络；阈值n(a − v) = 5 |
| 5 | 度量系统性风险 | CoVaR、MES；雷曼的SRISK为430亿美元，杠杆31倍；全球系统重要性银行附加资本 |
| 6 | 1998年：长期资本管理公司 | 47亿美元资本对应1250亿美元资产（27倍）；拥挤的收敛交易；Baa利差1.70 → 2.77 |
| 7 | 2007—08年 | 影子银行；TED利差0.46 → 4.58；Baa利差1.68 → 6.16；贝尔斯登、雷曼、AIG、储备主要基金 |
| 8 | 2020年3月 | 十年期收益率0.54% → 1.18%，同时股市下跌31%；基差交易；美联储的两周 |
| 9 | 2015年的中国 | 2050 → 5166（+152%）→ 2927（十一周内−43%）；配资；熔断（−6.9%、−7.0%）四天后暂停；磁吸效应 |
| 10 | 2022—23年 | 金边债券与LDI；硅谷银行；戴蒙德—迪布维格；全局博弈阈值（r = 0.85时1.49，一半受保时1.07）；瑞士信贷与AT1 |
| 11 | 第41条规则 | 2008年最糟糕的一天加保证金加倍：两倍杠杆下卖出9.8%，用时0.5天；Archegos；与波动率挂钩和跨周期的保证金；甩卖外部性 |
| R | 写给研究者 | 清算向量的存在性（塔斯基）与唯一性，给出证明；虚拟违约算法；检验；反例；传染阈值的推导与检验；加入甩卖 |
| 12 | 结尾 | 回顾、教训、公式、交易台问题、习题、参考文献 |

## 写给研究者

* **定理一（存在性）。** Φ(p) = min(p̄, e + Πᵀp)在格[0, p̄]上单调，由塔斯基定理存在最大与最小不动点。从p̄出发迭代单调下降并收敛到最大不动点；
  从0出发得到最小不动点。
* **定理二（唯一性）。** 若从每家银行出发都有一条债务链通向外部资产为正的银行，则p⁺ = p⁻。证明：令d = p⁺ − p⁻，S = {d > 0}；S中的银行在p⁻下
  付出全部所有；相减并对S求和，得到S中的银行只向S内付款，且不等式取等号；再对p⁺在S上求和，得到S既无外部资产也无外部流入，与正则性矛盾。
* **虚拟违约算法**在至多n轮内到达p⁺。
* **定理三（传染阈值，对称情形）。** 完全网络中一家银行受冲击ε，所有银行倒下当且仅当ε > n(a − v)。
* **检验。** 200个随机正则网络全部一致；最多5轮（平均3.19）；两家互欠且无外部资产的反例给出(1, 1)和(0, 0)两个清算向量；完全网络在5.05处从1家
  跳到10家；加入甩卖后，冲击为4时完全网络从1家违约变成10家。
* **第10章的全局博弈阈值：** θ*满足∫₀¹(等待 − 提前) df = 0；r = 0.85时θ* = 1.49；噪声从0.3降到0.01时，均衡阈值1.34、1.44、1.47、1.48收敛到1.49。
* **开放问题：** 双边敞口不可观测时的传染；同时含价格与挤兑的清算；非银行网络的度量。

## 交易台问题与解答

1. **五倍杠杆的基金亏10%，折扣率从20%升到30%，要卖多少？** 资产100 → 90，权益20 → 10；30%折扣率下最多持有10/0.3 = 33.3；卖出56.7，即63%。
2. **有偿付能力的银行怎么会倒闭？** 挤兑：若资产提前卖出只值r < 1，在别人提款时提款是最优反应（戴蒙德—迪布维格）。2023年3月的硅谷银行。
3. **损失螺旋与保证金螺旋？** 前者为维持杠杆而卖出，后者因贷款方降低允许的杠杆而卖出；两者合起来，这里3%的冲击变成21.8%，约7倍。
4. **连接更紧密的体系更安全吗？** 对小冲击是，损失被分担；超过阈值n(a − v)，完全网络会同时全部倒下。
5. **一家银行对系统性风险的贡献？** ΔCoVaR，或MES与SRISK。
6. **2020年3月国债收益率为什么上升？** 现金争夺战：外国官方持有者、开放式基金和基差交易者卖出，交易商受杠杆比率约束无法吸收，直到美联储买入并放宽比率。

## 习题与解答

1. A = 4，E = 1；亏5%后A = 3.8，E = 0.8，杠杆4.75倍；恢复4倍需A = 3.2，卖出0.6，即15.8%。
2. A = 8，E = 1，折扣率10%；下跌3%后A = 7.76，E = 0.76；折扣率20%时最多持有3.8，卖出3.96，即51%。
3. 下跌δ后卖出(λ − 1)Aδ，冲击γ(λ − 1)Aδ，再引发下一轮，几何级数求和得δ/(1 − γ(λ − 1)A)，要求γ(λ − 1)A < 1。
4. 卖出(λ − 1)Aδ = 19；验证：A = 99，E = 4，目标80。
5. p = (1.5, 1.5, 1)；权益A为0，B为0，C为0.8；体系正则，所以唯一。
6. n(a − v) = 10。
7. ΔCoVaR = 0.5 × (−4% − 0.1%) = −2.05%。
8. SRISK = 40 − 0.92 × 0.5 × 20 = 30.8。
9. 提前 = 1，等待 = 1.2 × 0.375/0.5 = 0.9 < 1：提款是最优反应。
10. 90 × 6 × 3% ≈ 16.2 > 8：按公允价值资不抵债约8.2（凸性会让损失略小）。
11. **（资格考试）清算定理：** 存在性与唯一性如上；虚拟违约算法中由归纳法p⁽ᵏ⁾ ≥ p⁺，违约集合单调扩大，停止时得到不小于p⁺的不动点，即p⁺，至多n轮。
12. **（资格考试）全局博弈阈值：** 在噪声消失的极限下，边际存款人认为挤兑比例在[0, 1]上均匀分布，θ*是G(θ) = ∫₀¹(等待 − 提前) df的根；G在θ上
    递增，所以根唯一；θ = 1时对所有f > 0等待严格小于提前，故G(1) < 0，θ* > 1；受保比例趋于一或r趋于一时，θ*趋于1：存款保险和按面值放贷消除了
    挤兑溢价。

## 数据与复现

FRED序列：TEDRATE、BAA10Y、DGS10、DGS2、DCPF3M、DPSACBW027SBOG；肯尼斯·弗伦奇的日度因子与49个行业（截至2020年）；雅虎财经000001.SS。
下载数据缓存并在`videos/quant/data/manifest.json`中校验。视频中的每个数字都来自`compute.py`（缓存于`.cache/quant41/`）和本系列公司的
`explainer/quant/house/crisis.py`。公司只按公开记录出现；报道中的数字和指控都标注为“据报道”。这里的内容不构成投资建议。
