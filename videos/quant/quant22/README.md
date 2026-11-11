# Quant, Built — Part 22: FX, Commodities and the Basis

Part 22 of the [forty-three-part series](../README.md), following the
[syllabus](../SYLLABUS.md): currencies, commodity storage and delivery, Treasury
financing and inflation prices. This is an education in methods, not investment advice.
Published episodes and firm figures are attributed to the public records below.

Visual pass complete on `quantitative-finance`: 32 bilingual endpoint sheets,
16 English motion sheets and 32 focused native frames reviewed on the
frozen source. The chaptered silent preview runs 69:10. Full continuous
production-voice listening remains pending; signal checks do not certify pronunciation.
See [the evidence record](../../../docs/qa/quant22-polish-evidence.json).

## Scope of this revision

- Ten original items restore under their recorded public-data checks. The original
  `oil`, `gas` and `storage_theory` items stop on EIA workbook hash mismatches.
  They are blocked before the scene loader touches a cache, even if an old file exists.
  No original compute driver, House algorithm or global registry is modified.
- [Separately pinned public workbooks](public_example_pins.json) support the named
  `oil_public_example`, `gas_public_example` and `storage_public_example` caches
  in [review_examples.py](review_examples.py). Their bytes differ from the legacy
  pins; without the old bytes we cannot attribute the difference to workbook metadata.
  These examples describe dated prices and inventory association. They do not certify
  the blocked originals or reconstruct a historical futures strategy return.
- The original fixed storage law, grid, quadrature and seed are retained in the named
  numerical example. The two roll screens instead use fixed arithmetic: entry future
  105, settlement 100, one-times cash backing, zero cash yield and no costs. Monthly
  loss is `100/105 - 1`; twelve identical resets lose about 44.3%. A new future has
  zero initial value. Initial contango does not determine its later profit.
- Fama's retained dates bridge March to May 2020 for all nine currencies while using
  a one-month rate differential. This is an actual calendar error in the protected
  legacy calculation, not a new corrected regression. The slopes, standard errors
  and mechanical pooled t ratio are descriptive; they do not certify significance.
  Three-lag HAC errors by currency and pooled White errors also treat dependence
  differently. A missing-data filter can bridge gaps even after its adjacency test.
- The FX panel uses month-end noon spots and full-month average three-month rates,
  with current-vintage/publication clocks, rather than matched executable one-month
  funding. Carry eligibility tests the next realized return; the audit finds no extra
  exclusion from that condition in this saved panel, but the rule does not establish
  historical information availability. The cumulative series sums gross log proxies. The shared panel also puts the
  March-to-May two-month currency move against one month of carry, so the legacy
  nominal-month annualization is not a calendar-adjusted account return.
- The sterling basis reconstruction mixes monthly forward/spot averages with LIBOR
  proxies. Dollar TED plus a discount-basis Treasury-bill yield is not an exact
  contemporaneous deposit quote. Neither that residual nor a standard-deviation
  multiple certifies executable arbitrage, a causal mechanism or a tail probability.
- Garman–Kohlhagen assumes positive lognormal spot and deterministic rates. Delta,
  premium and ATM conventions are stated. Zero straddle delta does not remove gamma,
  theta or rate risk. Vanna–volga is a heuristic, not a guarantee of static arbitrage
  freedom or a uniquely identified path law. Total-variance interpolation alone is
  insufficient to certify a whole surface.
- The plant option strip is a discounted pricing expectation for an idealized flexible
  plant; startup, ramp, outage, emissions and fixed costs remain. Electricity storage
  exists but is constrained. At correlation one, volatilities 45% and 40% still leave
  5% relative volatility; the illustrative Margrabe option is worth about $0.5924,
  rather than zero. Actual power spot is not a freely tradable lognormal asset.
- CTD comparison needs implied repo or carry-adjusted net basis, with dates and
  delivery options. Gross-basis minimization alone is insufficient. Signed
  mark-to-market gain, economic loss and variation-margin cash demands are distinct.
  Financing and delivery assumptions still matter at maturity. CFTC net shorts are
  face-value positioning proxies, neither basis-book sizes nor universal upper bounds.
- TIPS coupons use lagged index ratios and redemption includes a deflation floor.
  Yield-difference decompositions are approximate. Overlapping ex-post CPI windows
  cannot identify forecast skill or isolate a liquidity premium. Inflation swaps still
  require credit, collateral, capital and funding; the fair compounded payment equals
  a forward-measure expected index ratio, with an annualized root for the fixed rate.

## Chapters (about 59 minutes)

1. **A floor that broke.** The Swiss floor and its abandonment; New York noon cross-rates
   distinguished from intraday/executable quotes; a sample volatility multiple is not a probability.
2. **Covered interest parity.** Matched ideal investments, quote direction, simple and
   continuous rates, a descriptive sterling basis proxy, funding and intermediation constraints.
3. **Uncovered parity.** The log-linear zero-premium hypothesis; Fama's covariance
   identity; nine proxy slopes and the actual calendar/dependence limitations.
4. **Carry and crashes.** The original fixed three-versus-three gross reconstruction,
   left tails, the yen/Nikkei episode as co-movement, and dollar plus carry factors.
5. **FX options.** Garman–Kohlhagen, put–call symmetry, units, four deltas and ATM conventions.
6. **FX smile.** ATM/RR/BF under the smile-strangle convention, strike inversion,
   vanna–volga pillars, invented term inputs and surface/path model risk.
7. **Pegs and attacks.** A deterministic linearized monetary model, conditional attack
   timing, the ERM and policy willingness; no implied option mispricing from calm volatility alone.
8. **Storage and convenience.** Accessible-storage cash-and-carry bounds, net convenience
   proxies and dated named WTI curves. The slope viewport explicitly marks both off-scale tails.
9. **Roll and commodity premia.** Convergence assumptions and WTI's delivery calendar;
   two fixed arithmetic screens replace unavailable legacy performance. Initial contango permits
   different hypothetical settlements. Historical literature is distinguished from a new trial.
10. **Gas and power.** Normalized historical spot seasonality, near-contract context for
    Amaranth, regional gas benchmarks, constrained flexibility and Margrabe's assumptions.
11. **Negative oil.** May versus June delivery, continuous-contract renumbering, accessible
    capacity, Black's positive domain and an ATM-matched Bachelier illustration.
12. **Treasury basis.** Invoice, delivery options, implied repo, haircut equity versus
    total capital, signed marks and funding liquidity; public positions versus inferred books.
13. **Inflation.** TIPS cash-flow conventions, breakeven components, overlapping CPI
    comparisons, horizon differences and collateralized inflation swaps.
14. **The macro desk.** Prices and statistics with units, dates, conventions and limitations;
    the original House source is shown without alteration; scenarios do not guarantee prevention.
15. **Research: competitive storage.** Complementarity, the exact full-carry identity,
    finite-grid residual and boundary checks, full-range spread/scatter displays, and an explicit
    persistence-comparison caveat. A worked storage-bound answer follows the pause.
16. **Recap and problems.** Eleven wrapped recap lines, six conditional desk answers,
    and twelve problems in three pages numbered 1–6, 7–10 and 11–12.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Clark, *Foreign Exchange Option Pricing* | 1–3 (FX markets, Garman–Kohlhagen, conventions), 4 (smile, vanna–volga), 6 (barriers) | ch. 4–5 |
| Wystup, *FX Options and Structured Products* | 1 (deltas, premium adjustment, ATM conventions), 1.5 (vanna–volga) | ch. 4–5 |
| Geman, *Commodities and Commodity Derivatives* | 2 (storage, convenience yield), 3 (the roll, indices), 9–10 (oil, gas), 13 (power) | ch. 7–10 |
| Eydeland and Wolyniec, *Energy and Power Risk Management* | 5 (spread options), 7–8 (power plants as options) | ch. 9 |
| Hull, *Options, Futures, and Other Derivatives* | 5 (forwards, cost of carry), 6 (Treasury futures, CTD), 17 (currency options) | ch. 1, 4, 7, 11 |

## Papers, chapter by chapter

* Hook: SNB press release (15 January 2015); FXCM, 10-K for 2015.
* ch. 1: Du, Tepper and Verdelhan (2018); Borio, McCauley, McGuire and Sushko (2016); the Fed's swap lines (2007–08,
  2020).
* ch. 2–3: Fama (1984); Chinn and Meredith (2004); Brunnermeier, Nagel and Pedersen (2008); Lustig, Roussanov and
  Verdelhan (2011).
* ch. 4–5: Garman and Kohlhagen (1983); Castagna and Mercurio (2007); Reiswich and Wystup (2010) on delta conventions.
* ch. 6: Krugman (1979); Flood and Garber (1984); Obstfeld (1994); HM Treasury papers on Black Wednesday (2005).
* ch. 7–8: Keynes (1930); Kaldor (1939); Working (1949); Gorton and Rouwenhorst (2006); Gorton, Hayashi and Rouwenhorst
  (2013); CFTC releases 5521-08 and 6239-12 (Optiver).
* ch. 9: Margrabe (1978); US Senate PSI, *Excessive Speculation in the Natural Gas Market* (2007).
* ch. 10: Bachelier (1900); CME Clearing advisories 20-152 and 20-171 (April 2020).
* ch. 11: Barth and Kahn (OFR, 2021); Glicoes, Iorio, Monin and Petrasek (FEDS Notes, March 2024); Monin (FEDS Notes,
  June 2026); FOMC statement (23 March 2020); SEC, Treasury clearing rule (2023).
* ch. 12: D'Amico, Kim and Wei (2018); FRED's TIPS breakeven series.

## Desk questions and solutions

1. **Dollar 5%, yen 0%: premium or discount?** Under simple annual rates, in yen per
   dollar, `F/S = 1/1.05`. Equivalently a yen is dearer in forward dollars. The exact
   percentage depends on quote direction; uncovered carry still has exchange-rate risk.
2. **Why can a covered basis persist?** Matched ideal parity is a replication result.
   Actual funding, lending credit, collateral, settlement, hedging demand and balance-sheet
   capacity differ. A proxy residual is not automatically an available riskless profit.
3. **Does contango mechanically charge a roll fee?** No. A new future starts at zero
   value. Under an explicitly fixed convergence scenario, its higher delivery price can
   produce a loss as it converges; subsequent curve/spot moves and account sizing matter.
4. **Why the May 2020 contract?** Its immediate Cushing delivery obligations and accessible
   storage/transport differed from later contracts. A negative futures settlement is not
   a statement that every physical barrel or every delivery month has a negative price.
5. **Is protection on a calm peg necessarily cheap?** Calm realized volatility does not
   establish an option price or mispricing. Policy-jump assumptions, contemporary option
   quotes, risk premia and contract terms are needed.
6. **Does delivery remove all basis-trade risk?** A convergence calculation assumes
   financing, carry, execution and delivery terms. Repo renewal, haircuts, variation
   margin and forced exit remain; holding to maturity alone does not eliminate them.

## Problems and solutions

1. **CIP.** For domestic per foreign spot `S`, matched frictionless deposits imply
   `F = S(1+r_d τ)/(1+r_f τ)`. For continuous rates, `ln(F/S)=(y_d-y_f)τ`.
2. **Basis.** With `S=1.30, F=1.3025, r_d=.02, r_f=.012, τ=.25`,
   `x=ln(1+.02τ)/τ-ln(1+.012τ)/τ-ln(F/S)/τ`, about **+3 bp/year**.
   This made-up calculation ignores differing day counts and execution costs.
3. **Fama identity.** If `f-s=E_t[Δs]+p` and the forecast error is orthogonal to the
   time-t forward premium, `β=1-cov(p,f-s)/var(f-s)`. A negative beta requires the
   covariance to exceed the forward-premium variance. The assumption is part of the result.
4. **Deltas.** Under the stated convention, forward delta is `N(d1)`; premium-adjusted
   forward delta is `(K/F)N(d2)`. The unnormalized price derivative is discounted.
5. **DNS strike.** With unadjusted deltas, call plus put delta is zero when `d1=0`,
   giving `K=F exp(σ²T/2)`. Premium adjustment gives the opposite exponent.
6. **Pillar vols.** In the smile-strangle convention, ATM 8%, RR −1 vol point and BF
   0.3 vol points give call **7.8%**, put **8.8%**. A market-strangle convention differs.
7. **Attack.** Under the specified linearized deterministic model,
   `T*=(1-.1-.4)/.1=5`, reserves taken `αμ=.1`; mechanical exhaustion would be time 6.
8. **Convenience.** `y-u=.05-12 ln(71.5/70)`, about **−20.4%/year** under the
   positive-price one-month carry approximation. It does not separately identify storage,
   inventories or a risk premium.
9. **Implied repo.** Invoice `112×.89+1.1=100.78`; no intervening coupons gives
   `(100.78/100.2-1)×360/92`, about **2.27%**. Locked financing, day counts, accrued
   conventions, costs and delivery options matter for an actual trade.
10. **Correlation.** Relative variance is `σ1²+σ2²−2ρσ1σ2`, decreasing in correlation
    for positive volatilities. At `ρ=1` it is `(σ1−σ2)²`, not generally zero.
11. **Full carry and threshold.** Positive inventory implies `p+k=βE[p′]`.
    If `F=E[p′]`, then **`F-p=(β⁻¹−1)p+k/β`**. At zero inventory the same expression
    is an upper bound, not necessarily backwardation. With decreasing demand and a
    well-defined interior threshold, `P(x*)=βE[f(z′)]−k`; the right side must be in
    the inverse-demand range. Below the threshold `f=P`.
12. **Monotonicity and skew.** With decreasing continuous demand and a decreasing
    candidate continuation price, the storage Euler root has inventory increasing by
    no more than availability, under appropriate regularity and uniqueness. Consumption
    therefore does not fall as availability rises, and the updated price is nonincreasing.
    Stock-out regions need the boundary inequality too. Right skewness is an outcome
    of the chosen demand/shock law, not a theorem of nonnegative inventory alone.

## Numerical storage scope and worked answer

The original fixed numerical law uses 400 points on `[.55,3]`, 15 Gauss–Hermite nodes,
`β=1/1.01`, absolute upfront cost `.005`, and seed 2222. Reported iteration index 163
means **164 updates**. Euler residuals at positive inventory are below `10⁻⁹`, and
stock-out complementarity holds on the grid. Interpolation clamps tails: at the
worst grid state about **1.90%** of quadrature mass is clamped above the upper edge,
with a tiny lower-tail mass too. The original 200,000-period simulation stays inside
this grid; 1,000 burn-in observations leave **199,000** periods for the saved statistics.
None of these facts certifies a continuous-state equilibrium or quadrature error bound. The reference-price unit is the normalization `P(1)=1`; the absolute
fee `.005` is not an estimated 0.5% of the simulated stationary mean price.

The model spread down to **−66.34%** and all descriptive inventory/spread points,
including the **+26.56%** maximum, are displayed. Price-level model autocorrelation
is distinct from monthly log-price autocorrelation in oil; the table is not a
like-for-like calibrated test. Public inventory association is not a causal validation.

For the pause question, $70 oil, one-month simple rate .4%, and $.30 storage paid
**today** give `F≤(70+.30)1.004=70.5812`, about $.58 contango. If storage is paid at
delivery the bound is $.58 exactly under these inputs. One-way cash-and-carry supplies
no analogous lower carry bound without the reverse trade. The positive-price storage
model does not represent the contract's possible negative-price states.

## Reproduce the review inputs

From the repository root with Manim, TeX, SciPy and xlrd installed:

```bash
python -m videos.quant.quant22.compute snb cip fama carry yen2024 fxopt erm negoil basis inflation
python -m videos.quant.quant22.review_examples
EXPLAINER_TTS=silent python tools/qa_series.py quant22 --cached-only --resume
EXPLAINER_TTS=silent python tools/qa_series.py quant22 --lang zh --cached-only --resume
EXPLAINER_TTS=silent python tools/qa_series.py quant22 --motion --cached-only --resume
python tools/zh_lines.py quant22 --todo
python tools/lecture_length.py quant22 --floor 50
```

The named examples require the exact independently pinned public workbook bytes in
the paths listed by `public_example_pins.json`; restore those exact bytes or fail,
rather than accepting changed upstream data. Do not use force or refresh to replace
legacy pins. Original trials remain **317 through Part 22**, **23,562 globally**;
no market trial or sealed holdout is added or opened. Eight existing focused
numerical tests pass. The artifact-bound review record states the completed sampled visual checks and
separate pending production listening.

FRED, BoE and CFTC windows retain their original checks. EIA named examples have
independent hashes. Published firm losses, policy decisions, regulatory releases
and Fed book estimates are quoted from the references, rather than inferred from
these descriptive price charts.

---

# 量化金融，从零搭建 — 第22部分：外汇、商品与基差

本轮视觉复核完成：已实际检查32张双语旁白节点画面表、16张英文动画画面表及32张原尺寸重点画面。配音开场及分章静音预览已核验。完整成片连续听审与发音验证仍待完成，信号检查不能替代听审。

本讲涵盖抛补与非抛补平价、套息与崩盘、外汇期权及报价约定、挂钩攻击、储存与便利收益、展期算术、天然气与电力、负油价、国债基差与通胀价格。16章顺序见上文，科学限定与英文完全一致。

## 数据、统计与定价范围

- 10个原始项目通过原有检查恢复；`oil`、`gas`、`storage_theory`因EIA工作簿哈希不符被阻止，在读缓存前即拒绝。原计算驱动、House算法与全局登记均未改动。
- 三个单独命名例子采用`public_example_pins.json`独立固定的公共价格与库存文件。没有旧字节就不能断言变化仅属元数据；这些例子不认证受阻原结果，也不重构历史期货策略回报。展期业绩屏改为固定算术示例，不以新历史业绩填补。
- 九种货币的Fama保留日期都从2020年3月跳至5月，却配一月利差；该旧计算的实际日历错误未通过新回归掩盖。斜率、单币HAC及合并White误差只作描述，机械t比值不能证明显著性。
- 月末中午即期与整月平均三月利率，既不期限匹配，也不代表历史时点可成交数据。套息资格测试未来回报存在性；本保存面板中该条件没有另排除记录，但不建立可实施性。累计曲线求和毛对数代理，不等于完整融资账户。相同面板也把2020年3月至5月两个月汇率变动配上一月利息，旧名义月度年化并非日历调整账户回报。
- 英镑基差混合报价时钟、日计数与融资代理，TED加贴现报价国库券并非精确同期存款利率。价差不自动证明套利或单一因果机制；SNB样本标准差倍数也不是尾部概率。
- Garman–Kohlhagen依赖正对数正态价格及确定利率。delta、期权费与平值约定须明确；零初始delta仍有伽马、时间与利率风险。Vanna–volga及总方差插值不能独自保证全曲面无套利或识别路径分布。
- 电力可以储存但容量受限。理想灵活机组类似正调度利润的贴现定价期望之和，实际还受启停、爬坡、故障、排放与固定成本约束。相关为1、波动率45%和40%时仍有5%相对波动，本例交换期权约值0.5924美元，不为零。
- 最便宜可交割券需比较隐含回购或持有成本调整净基差，不能只最小化毛基差。盯市盈亏、经济损失与追加保证金现金需求不同；交割本身不消除融资风险。CFTC净空面值既非基差账簿规模，也非普适上界。
- TIPS采用滞后参考指数，兑付含通缩下限；收益率差分解是近似。重叠五年CPI窗口不能识别预测能力或单独流动性溢价。通胀互换仍需信用、抵押、资本与融资；公平固定复合总支付等于远期测度预期指数比，取年化根才得固定利率。

## 交易台问题与解答

1. **美元5%、日元0%，日元远期升水吗？** 指定单利及日元每美元报价下`F/S=1/1.05`，倒数报价的百分比不同；套息仍有汇率风险。
2. **基差为何持续？** 理想平价要求信用、期限与交割匹配，实际融资、抵押、中介容量和需求不同，代理残差不自动等于无风险利润。
3. **期货升水等于展期手续费吗？** 新期货初值为零。固定收敛场景可能亏损，但初始曲线不决定未来盈亏。105收敛到100，以105现金支持、每月重置，一月亏约4.76%，重复12月约亏44.3%，不是历史基金业绩。
4. **为何5月油约为负？** 即期交割义务与可取得储存、运输有别于远月，不表示所有实物与月份均值负数。
5. **平静挂钩的终止期权必然便宜吗？** 不能仅凭低历史波动断言，须结合政策跳变假设、同期报价、风险溢价及条款。
6. **交割是否消除基差风险？** 不，融资续期、折扣、保证金、退出及交割选择依然重要。

## 习题与解答

1. **平价：**`F=S(1+r_dτ)/(1+r_fτ)`；连续复利下`ln(F/S)=(y_d-y_f)τ`，前提为理想匹配复制。
2. **基差：**给定S=1.30、F=1.3025、两利率2%与1.2%、τ=.25，连续复利转换后约+3基点/年，未计成本与日计数差异。
3. **Fama：**若预期误差与当期远期溢价正交，`β=1-cov(p,f-s)/var(f-s)`，负β要求协方差大于远期溢价方差。
4. **Delta：**约定远期delta为`N(d1)`，溢价调整后为`(K/F)N(d2)`，不同于未归一化贴现价格导数。
5. **中性跨式：**未调整delta下`d1=0`，`K=F exp(σ²T/2)`；调整后指数反号。
6. **柱点：**微笑宽跨式约定下ATM 8%、RR −1点、BF .3点，得看涨7.8%、看跌8.8%。
7. **攻击：**指定线性确定模型中时点5，储备.1；无攻击的机械耗尽时点6。
8. **便利收益：**`y-u=.05-12ln(71.5/70)`约−20.4%/年，不能分离库存、储存与风险溢价。
9. **隐含回购：**发票100.78，`(100.78/100.2-1)360/92`约2.27%，无中间付息且条款、成本须匹配。
10. **相关：**相对方差`σ1²+σ2²−2ρσ1σ2`，相关1时仍为`(σ1−σ2)²`，不一定为零。
11. **完整持有成本：**正库存时`p+k=βE[p′]`，故`F-p=(β⁻¹−1)p+k/β`；零库存只给上界，并不必然现货升水。阈值须满足逆需求定义域及最优条件。
12. **单调性与偏度：**在递减连续需求、良定义储存最优及适当正则条件下，可比较根的变化证明价格更新不增；边界亦须检查。正偏是指定需求与冲击的结果，不是非负库存约束本身的定理。

数值模型采用400点网格[.55,3]、15求积节点及原种子2222，索引163对应164次更新。网格欧拉残差小于10⁻⁹，但最差上界状态约1.90%求积权重被钳制；原20万期路径未出界，舍弃1000期后统计199000期。这不认证全局连续均衡。图中参考价格单位采用归一化P(1)=1，绝对成本.005并非模拟平稳平均价格的实测0.5%。显示完整−66.34%模型价差及+26.56%经验极值；价格水平与月度对数价格的自相关不可当作同口径校准比较。

暂停题若30美分储存费今天支付，`F≤(70+.30)1.004=70.5812`，升水约58美分；到期支付则恰为.58美元。没有反向交易，单向持有套利不给对应下界，但正价格模型本身不能描述负油价。

原累计试验数保持本部分317、全系列23562，不新增市场试验、不打开封存留出数据、不强制刷新登记。8项已有数值测试通过；当前源码的抽样视觉证据已记录，完整成片听审另列待办。
