# Quant, Built — Part 18: Money, Bonds and the Curve

The scientific and bilingual polish pass and current-source visual review are complete. Full production-voice listening remains pending. See the [sequential QA record](../../../docs/qa/quantitative-finance-polish.md).

Part 18 of [43 parts](../README.md), following the [syllabus](../SYLLABUS.md) and [reading map](../READING.md). Narration is approximately 64.7 minutes at the standard estimation rate; animation, pauses and actual speech change playback length. The calculations below describe the pinned historical samples through 2025, rather than current market conditions.

## Scope and reproducibility

The protected [original compute driver](compute.py), House algorithms and global data/trial registries are unchanged. Fourteen permitted original items were restored normally. The original `term` attempt failed because the live NY Fed file no longer matches its pinned historical hash; no refresh or manifest change was used. Two distinctions matter:

- [term_example.py](term_example.py) is a separately named full-sample GSW illustration using the original regression/ACM settings, without the unavailable NY Fed comparison. Its yield-fit RMSE is 5.88 bp. It is neither an independent replication of NY Fed estimates nor an accurate-observed-premium certificate.
- [futures_example.py](futures_example.py) restricts the original 19-note synthetic-price cache to **11** notes satisfying the December 2025 CBOT grade, 6½ to under 8 years remaining after quarter rounding. It recovers the same prices from `P = basis + F × CF`, then recomputes the carry-free price envelope. The original builder's wider grade is preserved for provenance, not presented as correct. The factor reference is 6% nominal with semiannual compounding, while the plotted zero-yield coordinate is continuous. The synthetic price F* and selected-note index i* are distinct.

The active butterfly is a descriptive factor-exposure example and an unfinished validation design. **Do not run or load the legacy `fly` or `envelope` items:** they register/open a sealed strategy-return window. This pass neither executes that trial nor reports its legacy performance statistics. Cumulative trials through Part 18 remain **313**; the global counter remains **23,562**. These are existing metadata, not evidence of a new validated strategy.

## Chapters

| Chapter | Content and qualifications |
| --- | --- |
| Hook: the safest asset | SVB **Financial Group** consolidated facts; predominantly agency-MBS HTM securities. A fixed-notional, constant-duration proxy is distinguished from reported gross unrecognized losses, book capital and complete economic equity. |
| 1. Money, reserves and the floor | Reserve access, bank/nonbank transactions, administered-rate incentives and market frictions. All 887 saved weekly scatter observations are drawn; weekly sampling misses daily dislocations. |
| 2. QE and QT | Assets = currency + reserves + ON RRP + TGA + other liabilities + capital. The April 2022 peak predates formal QT; liability movements need not be one-for-one. Aggregate runoff ended 1 December 2025, without freezing portfolio composition. |
| 3. Taylor benchmark | Conditional policy arithmetic using revised historical inflation/output-gap inputs, not a real-time decision rule or proof of causation. The three-dimensional plane retains the full range. |
| 4. Bonds, yields and forwards | A hypothetical regular-coupon-date bond, all coupon cash flows and separate principal, compounding/day-count conventions and conditional forward replication. Yield to maturity is an IRR, not a guaranteed holding-period return. |
| 5. Bootstrap | Fourteen 2025 and thirteen 2023 CMT nodes. The protected routine uses a single-payment approximation at ≤1 year; its tiny repricing error applies **only to coupon nodes beyond one year**. One-year residuals are about 0.095 and 0.117 bp. Interpolation couples coupon dates to an unknown endpoint. This is not Treasury's official methodology. |
| 6. Duration and convexity | PV-weighted time, modified duration, local convexity and signed sensitivity. The full yield sweep retains even the negative far-away tangent approximation, clearly distinguished from a physical bond price. Greater convexity alone gives no universal price ranking. |
| 7. Key rates and immunization | One-sided finite key bumps aggregate only approximately. Redington's conditions are local; this positive 5y/30y barbell has a stronger parallel-shift Jensen result. Twist is explicitly `Δz(T)=a+b(15−T)/10`; at b=−1 percentage point its shortfall is 6.27 dollars, 11.42% of initial liability PV. All 25×25 stress nodes are retained. |
| 8. Nelson–Siegel–Svensson | Four betas and two positive time scales; hump maximum near 1.793τ. Full derived-zero-yield samples, RMSE 3.34/6.95 bp, restricted-grid initialization and local nonlinear refinement. Smoothness is not dynamic no-arbitrage or parameter identification. |
| 9. Curve history | 648 consecutive month ends, January 1972–December 2025. **123/648 = 19.0%** have 10y below 1y; the legacy daily 10y−2y statistic is not substituted. Month labels use the original calendar encoding correctly. Seven selected NBER peak leads are 8,17,35,18,12,22,9 months under the stated available-prior-36-month rule; the first window is left-censored and windows overlap. No forecast or causal score is claimed. The 3D surface is quarterly plus the final sample, 1–15y, with interpolation and no date extrapolation. |
| 10. PCA | 10,005 consecutive-observation changes at nine maturities; covariance shares 83.88/10.58/3.36%. Components are centred, sample-dependent and not independent by construction. The selected 20 October 1987 raw projection leaves a **16.64 bp** largest error at 1y; raw changes range −76.47 to −34.20 bp. The cumulative path uses centred full-sample scores, saved every fifth observation. Parallel neutrality differs from neutrality to non-flat PC1. |
| 11. Swaps | Synthetic reset-date single-curve pricing, per unit notional; near-par versus away-from-par sensitivity. Historical LIBOR swap spreads differ from SOFR swaps. Persistence dates use a retrospective >80%-negative rule looking forward up to 250 observations; the pre-2008 mean begins July 2000. All weekly spread values, including 151 bp, are shown. Repo, basis, collateral and balance-sheet risks prevent a locked arbitrage. |
| 12. Futures | Corrected 11-note grade; House conversion factors and a synthetic `F*=min(P/CF)` envelope. Cash-flow/accrual origin 1 December differs from the 28 November curve date; intervening carry, repo and delivery timing are omitted. All 81 shocks and all basis curves are retained. Five switch-grid yield readings are 3.70,3.80,5.40,5.60,6.10%; they are not exact thresholds. Six percent is a factor reference, not a universal switch point. |
| 13. Repo/SOFR/LIBOR | Annualized repo rates, eligible GC baskets, specials, reserve-access frictions, transaction-based volume-weighted-median SOFR and LIBOR cessation. The realized compounding windows target 91 days but keep full fixing intervals: 1,789 windows of 91 days, 73 of 92 and 12 of 94. The DTB3 bank-discount quote includes negative values and is not a pure future-SOFR forecast. |
| 14. Term premium | Campbell–Shiller conventional OLS versus overlapping Fama–Bliss HAC(12); approximate expectations restrictions, not zero expected excess-return intercepts. The named 5-PC ACM illustration uses 6–120m return maturities and PCs from ≥3m. Its zero-risk-price yield includes model/convexity effects. Decomposition and low yield RMSE do not identify latent premia or a causal policy channel. |
| 15. FOMC days | 215 scheduled meeting observations, 1994–2020. Full-sample SDs 6.18 versus 5.12 bp; the other-day histogram is thinned every seventh observation. No endpoint pooling. All scatter points are retained. Intercept −0.00788 bp, slope 0.32694, conventional OLS SE 0.07141 for the fitted **instantaneous nominal** forward at 10y. Daily OLS is not a high-frequency identification replication. |
| 16. Butterfly | Salomon public-record context; full-sample descriptive 2s5s10s DV01 weights approximately (−0.5888,1,−0.5282), locally neutral to two fitted loadings. Bond P&L has the **opposite** sign to the weighted yield change. A +1 bp combination costs about $1,000 when belly DV01 is $1,000/bp. Return validation remains unfinished. |
| 17. Gilts/LDI | Pension funding, pool NAV and available collateral differ. `1/(LD)` is a tangent zero, not exact default or a measured buffer. The 2.0-impact path reaches the 30-round limit at 335.47 bp with 10.81% NAV; no infinite-run convergence claim. All 315 surface nodes and values up to 3,000 bp are shown, with explicit model limitations. Resilience guidance includes a ≥~250 bp market-stress buffer **plus** an operational buffer. |
| 18. SVB | Group versus bank scope, predominantly agency MBS, constant 6.2-duration proxy and gross/tax distinctions. The $1.8bn AFS loss is after tax; March 10 expected outflows are not completed withdrawals. BTFP was a liquidity loan program for eligible institutions/qualifying collateral, not cancellation of losses; new lending ended March 2024. Asset DV01 alone is incomplete bank EVE. |
| 19. House rates desk | Four illustrative positions, local key-bump and signed factor exposure reports; fund liability PV is 54.9, not 100. Model/basis risks and a proposed validation standard are distinguished from an implemented complete service. |
| Research | Oscillatory means all minors nonnegative and some power has **all minors strictly positive**, not merely positive entries. Sign counts do not establish flatness, three-factor variance concentration or economics. The Markov example is TN, not strictly TP. Gaussian simulations include diagonal regularization; empirical negative minors violate the condition. Covariance averaging alone guarantees neither TN nor concentration. A 3×3 eigenpair answer follows a pause. |
| Recap and problems | Four desk questions and ten worked problems, with English and Chinese solutions below. |

## Build and checks

Run from the repository root in the configured environment. Avoid the unqualified original compute-all command because it includes the sealed-return items and unavailable comparison.

```bash
for item in oscillation_theory policy taylor bonds curve_day morph pca swaps futures sofr fomc immunize ldi svb; do
  python -m videos.quant.quant18.compute "$item"
done
python -m videos.quant.quant18.term_example term_example
python tools/qa_series.py quant18 --cached-only --resume --timeout 1200
python tools/qa_series.py quant18 --lang zh --cached-only --resume --timeout 1200
python tools/qa_series.py quant18 --motion --cached-only --resume --timeout 1800
python tools/zh_lines.py quant18 --todo
python tools/lecture_length.py quant18 --floor 50
```

A vendor-vintage hash mismatch is a reproducibility failure to report, not permission to refresh. A successful render is not visual approval. Current source compilation, narration-template/bookmark coverage and all 98 protected hashes pass; nine existing synthetic numerical tests passed. Actual current-source endpoint and motion sheets were inspected; selected speech checks and an actual narrated opening were completed. See the [artifact-bound evidence](../../../docs/qa/quant18-polish-evidence.json). Full continuous production listening is a separate pass; sampled signal/alignment checks cannot certify it.

## Desk questions, with solutions

1. **10-year zero at 4% annual yield.** P=100/1.04¹⁰=67.5564; Macaulay D=10, modified D=10/1.04=9.6154. A +1 bp shift gives ΔP≈−0.06496 per 100 face. This is a local approximation.
2. **Does greater convexity impose a universal price ranking?** No. For a specified frozen price function, ΔP/P≈−DΔy+½C(Δy)². A larger quadratic coefficient is a local comparison under matched assumptions, not dominance for arbitrary finite moves. Cash flows, starting prices, options, drift, carry and financing matter; ½Cσ² is not a universal yield discount.
3. **Why can swaps fix below Treasuries?** Their funding, liquidity, collateral, balance-sheet and hedging-demand exposures differ. Buying a coupon Treasury in repo and paying fixed retains floating-index/repo basis, timing, coupon and rollover risks. Jermann's holding-friction model supports negative equilibrium spreads without proving that regulation alone explains every observation.
4. **What does SVB motivate reporting?** Joint asset-and-liability economic-value stress, deposit behavior, cash, usable collateral, withdrawal scenarios and funding capacity. The gross HTM fair-value gap, book capital and local asset DV01 answer different questions. Uninsured status does not itself identify deposit duration.

## Ten problems, with worked solutions

1. **Forwards.** For positive Z and 0≤t₁<t₂, `f(t₁,t₂)=[t₂z(t₂)−t₁z(t₁)]/(t₂−t₁)` follows from the discount-factor ratio. If z is differentiable at t>0, `f(t)=z(t)+t z′(t)`; hence f>z iff z′>0 there. At interpolation knots use a specified one-sided/derivative convention. These are curve-implied rates under matching valuation assumptions, not physical expectations by identity.
2. **Durations.** A zero pays once at T, so Macaulay duration T and annual modified duration T/(1+y). An annual perpetuity with c>0 and y>0 has P=c/y and modified duration 1/y; Macaulay duration is (1+y)/y, or 21 years at 5%. The perpetuity sum requires y>0.
3. **Local convexity.** At frozen time, D=−P_y/P and C=P_yy/P. With EΔy=μdt and E(Δy)²=σ²dt, the local expected price mark is `EΔP/P≈(−Dμ+½Cσ²)dt`. Actual total return also includes explicit time/roll-down and coupons, and may include funding, changing cash flows or options. Assuming carry equals quoted yield is an additional model assumption. This calculation alone sets no no-arbitrage yield discount.
4. **Hand bootstrap.** Under annual compounding, 100=5/1.04+105/(1+z₂)². Thus `z₂=sqrt[105/(100−5/1.04)]−1≈5.025%`. The first coupon is discounted using the given one-year zero, with the final coupon and principal jointly determining z₂.
5. **Swap.** At a reset date in the ideal single-curve unit-notional model, floating coupon PV is 1−Z(T) and fixed PV KA, A=ΣτᵢZ(tᵢ); K*=(1−Z(T))/A. Receiver V=(K−K*)A, so `dV=−A dK*+(K−K*)dA`. At par a 1 bp fall gives ≈A×10⁻⁴ per unit notional. Multi-curve discounting, payment lags and accrued/fixed coupons require the appropriate adjustments.
6. **Immunization.** Liability PV L=100e⁻⁰·⁶=54.8812. PV weights solve w₅+w₃₀=1 and 5w₅+30w₃₀=15, giving .6/.4; asset PVs 32.9287 and 21.9525. Their continuous-shift convexity is .6×25+.4×900=375 versus 225. General Redington conditions give a local result. Here `S(a)/L=.6e^(−5a)+.4e^(−30a)−e^(−15a)≥0` for every parallel a by Jensen. This special global result does not control twists, credit or funding.
7. **Taylor benchmark.** i=2+4+.5(4−2)+.5(−1)=6.5%. This depends on the assumed neutral rate, target, input measurements and coefficients; it is neither a mandatory action nor an optimal-policy theorem.
8. **Local LDI model.** With initial NAV 1, assets 4 and D=25, the tangent zero is Δy=1/(4×25)=.01. After +50 bp, the model gives NAV .5 and assets 4(1−25×.005)=3.5. Restoring the initial .01 NAV-to-duration buffer targets assets `.5/(25×.01)=2`; sell 1.5, **42.86% of remaining assets**, or 37.5% of initial assets. This ignores impact during that sale and treats the local price approximation as the model, not exact solvency or collateral economics.
9. **Markov TN and sign counts.** Let Bᵢⱼ=ρ^(i−j) for i≥j, zero otherwise, and D=diag(1,1−ρ²,…,1−ρ²). Direct multiplication gives C=BDBᵀ. B factors into nonnegative elementary lower-bidiagonal matrices, so B, D and their product are TN by Cauchy–Binet. D>0 gives nonsingularity; C has positive adjacent off-diagonal entries. A nonsingular TN matrix with positive adjacent super/subdiagonals is oscillatory. For n=3, `a±=(−ρ±sqrt(ρ²+8))/2`, `v±=(1,a±,1)`, `λ±=1+ρ²/2±(ρ/2)sqrt(ρ²+8)`; `v₂=(1,0,−1)`, λ₂=1−ρ². For 0<ρ<1, λ+>λ₂>λ−>0, so the ordered sign counts are 0,1,2, ignoring the middle zero. Entries/eigenvalues vary with ρ. At ρ=0 eigenvalues are degenerate; at ρ=1 the matrix is singular.
10. **Averaging covariance.** Assuming finite second moments and valid interchange of integration and covariance, `Cov(Δy(m₁),Δy(m₂))=(m₁m₂)⁻¹∫₀^m₁∫₀^m₂ c(s,t) ds dt`. Integration can damp fine-scale variation, but arbitrary smooth or distance-decaying covariance kernels need not be TN. Averaging alone establishes neither the all-minors condition, an oscillatory power, increased correlation at every pair nor a universal three-factor variance share. Additional kernel assumptions and proof are needed.

## Textbooks and primary records

[Tuckman–Serrat, Veronesi, Hull and Fabozzi coverage](../READING.md) includes cash-flow valuation, DV01, key rates, repo, futures and swaps. Research: Macaulay (1938), Redington (1952), Fisher–Weil (1971), Poole (1968), Fama–Bliss (1987), Nelson–Siegel (1987), Litterman–Scheinkman (1991), Campbell–Shiller (1991), Taylor (1993), Svensson (1994), Kuttner (2001), Gürkaynak–Sack–Swanson (2005), Gürkaynak–Sack–Wright (2007), Adrian–Crump–Moench (2013), Hanson–Stein (2015), Duffie–Stein (2015), Nakamura–Steinsson (2018), Jermann (2020), Jiang et al. (2024). Matrix background: Gantmacher–Krein, Karlin, Forzani–Tolmasky (2003), Salinelli–Sgarra (2006), Lekkos (2000). A theorem's assumptions are distinguished from the empirical diagnostics and numerical illustrations.

- [Fed GSW methodology and vintage limitations](https://www.federalreserve.gov/data/nominal-yield-curve.htm): daily fitted estimates, revisable research product, NS before 1980, NSS thereafter.
- [Treasury methodology](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/treasury-yield-curve-methodology): indicative bid-side inputs and official monotone-convex method.
- [NBER peak/trough chronology](https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions): peak is the last expansion month; contraction follows through the trough.
- [CBOT filing 25-099](https://www.cmegroup.com/content/dam/cmegroup/market-regulation/rule-filings/2025/2/25-099.pdf): December 2025 grade in Exhibit A; [factor conventions](https://www.cmegroup.com/articles/2024/calculating-us-treasury-futures-conversion-factors.html).
- [NY Fed reference-rate conventions](https://www.newyorkfed.org/markets/reference-rates/additional-information-about-reference-rates), [CFTC Barclays penalties](https://www.cftc.gov/PressRoom/PressReleases/6289-12), [FCA LIBOR end](https://www.fca.org.uk/news/press-releases/end-libor).
- [October 2025 FOMC runoff decision](https://www.federalreserve.gov/newsevents/pressreleases/monetary20251029a.htm) and [March 2009 purchase announcement](https://www.federalreserve.gov/newsevents/pressreleases/monetary20090318a.htm).
- [BoE gilt intervention case study](https://www.bankofengland.co.uk/quarterly-bulletin/2023/2023/financial-stability-buy-sell-tools-a-gilt-market-case-study), [LDI minimum resilience](https://www.bankofengland.co.uk/financial-policy-summary-and-record/2023/bank-staff-paper-ldi-minimum-resilience), [Pensions Regulator guidance](https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/funding-and-investment-detailed-guidance/liability-driven-investment).
- [Fed SVB evolution](https://www.federalreserve.gov/publications/2023-April-SVB-Evolution-of-Silicon-Valley-Bank.htm), SVB Financial Group 2022 10-K/XBRL, [original BTFP terms](https://www.federalreserve.gov/newsevents/pressreleases/files/monetary20230312a1.pdf), [Jiang et al.](https://www.nber.org/papers/w31048).

Data: pinned GSW through 31 December 2025, Treasury CMT/auction records, FRED rates/balances/output data and EDGAR group facts. Published crisis dates, purchase totals and penalties are cited figures rather than computed estimates. No NY Fed agreement statistic or legacy sealed-return performance is asserted.

---

# 量化金融，从零搭建 — 第18部分：货币、债券与收益率曲线

本轮科学与双语润色、当前源代码的视觉验收已完成；完整制作旁白的连续试听仍待进行。旁白估计约64.7分钟，动画、停顿及实际语速会改变播放时长。历史计算截至二〇二五年，不表示当前市场状态。

## 范围与复现

原始compute驱动、工坊算法及全局数据和试验登记均未修改。正常恢复了十四项允许的原始缓存。原始term因纽约联储文件历史版本哈希不匹配而失败，没有刷新或修改登记。另行命名的term_example保留原始回归及五主成分ACM设置，使用固定GSW数据，省略无法复现的纽约联储比较。收益率拟合均方根误差为5.88基点，不证明潜在期限溢价准确。

futures_example从原始十九券缓存的基差恒等式恢复同一合成价格，按二〇二五年十二月CBOT规定的六年半至不足八年、向下舍入到季度的品级，筛选为**十一券**并重算忽略持有成本的包络。原始过宽品级只保留作来源记录。转换因子参考为六厘名义收益率、半年复利，而图示零息收益率为连续复利；合成价格F星与选券索引i星是不同量。

蝶式章节展示描述性敞口及未完成的验证设计。**不要运行或加载旧fly或envelope项**，它们会登记并打开封存策略回报窗口。本轮未执行该试验，也不报告旧绩效。至第十八部分累计计数保持313，全局保持23,562。这些是既有元数据，并非新增验证证据。复现请使用上方明确白名单命令，不使用无参数compute全部执行，也不绕过供应商哈希失败。

## 章节要点

| 章节 | 内容及限定 |
| --- | --- |
| 开场 | SVB金融集团合并报表；以机构按揭证券为主的持有至到期组合。固定名义金额及久期的损失代理，不等于每日公允价值、完整权益经济价值或资不抵债结论。 |
| 1 货币与准备金 | 区分账户资格、银行及非银行交易、管理利率激励与市场摩擦；绘制全部887个周度散点，但周频不能捕捉所有日内或每日异常。 |
| 2 QE及QT | 完整资产负债恒等式；二〇二二年四月资产峰值早于正式QT。各负债变化不必一比一。二〇二五年十二月一日结束总量缩减，不冻结资产构成。 |
| 3 泰勒基准 | 修订后的历史输入及条件系数，不是实时决策规则、最优政策定理或因果证据。三维平面保留全范围。 |
| 4 债券及远期 | 假定规则付息日估值，展示全部票息及独立本金；计息及复利惯例决定数值。到期收益率是内部收益率，不是保证持有回报。 |
| 5 自举 | 二〇二五年十四节点、二〇二三年十三节点；一年以内采用单笔支付近似。极小重定价误差仅适用于一年以上附息节点，一年残差约0.095及0.117基点。不是财政部官方算法。 |
| 6 久期凸性 | 完整现值权重、修正久期及局部凸性；全收益率扫描保留远处为负的切线近似，明确它不是真实债券价格。凸性较大不构成普遍价格排序。 |
| 7 关键利率与免疫 | 有限单边微调之和仅近似平行敏感度。一般雷丁顿条件是局部的，正权重五年及三十年杠铃则有特殊的詹森平行移动结果。扭曲定义为Δz(T)=a+b(15−T)/10；b为负一个百分点时缺口6.27美元，即初始负债现值11.42%。保留25乘25网格。 |
| 8 曲线拟合 | 四个贝塔及两个正时间尺度；驼峰在约1.793τ。拟合推导零息节点的均方根误差3.34及6.95基点；有限网格初始化及局部优化不证明全局最优或参数精确识别。 |
| 9 曲线历史 | 一九七二年一月至二〇二五年十二月648个连续月末；十年低于一年为123/648，即19.0%。不能换用旧日度十年减两年比例。七个选定峰值的领先月数为8、17、35、18、12、22、9；首窗口左截断且窗口重叠，不是预测或因果评分。曲面为一年至十五年、每三月取样并加最后月份，不外推日期。 |
| 10 主成分 | 九期限10,005次相邻观测变化；前三方差占比83.88%、10.58%、3.36%。一九八七年十月二十日原始投影最大误差在一年点，为16.64基点；原始变化为负76.47至负34.20基点。累积轨迹使用全样本中心化得分。平行中性不等于非水平PC1中性。 |
| 11 互换 | 重置日单曲线单位名义本金示例；区分平价附近及偏离平价的敏感度。历史LIBOR互换不同于SOFR互换。持续性日期是向前查看至多250次观测、超过80%为负的事后规则。显示包括151基点在内的全部周度值，保留融资、回购及基差风险。 |
| 12 期货 | 正确十一券品级；工坊转换因子及F星=min(P/CF)合成包络。十一月二十八日曲线与十二月一日现金流起点不同，省略期间持有成本及交割时间选择权。保留81冲击及全部基差曲线，五次网格切换读数约3.70%、3.80%、5.40%、5.60%、6.10%，不是精确阈值。 |
| 13 回购及SOFR | 回购年化报价、合格一般抵押品篮子、特殊券及准备金资格摩擦。SOFR为交易量加权中位数。实现复利窗口保留完整定盘区间：91天1,789次，92天73次，94天12次。国库券银行贴现报价含负值，不能直接当作未来SOFR预测。 |
| 14 期限溢价 | CS常规OLS与重叠FB的HAC十二阶误差；五主成分模型的零风险价格反事实收益率含凸性等效应。分解及低收益率拟合误差，不识别潜在溢价或政策因果渠道。 |
| 15 FOMC | 215个计划会议观测；全样本标准差6.18对5.12基点，其他日直方图每七次保留一次。保留全部散点；十年处瞬时名义远期日度回归截距负0.00788、斜率0.32694、常规标准误0.07141。未复现高频因果识别。 |
| 16 蝶式 | 描述性DV01权重约负0.5888、一、负0.5282，局部抵消两个拟合载荷。债券盈亏与加权收益率变化符号相反；腹部DV01为每基点一千美元时，组合收益率上升一基点约亏一千美元。回报验证未完成。 |
| 17 国债及LDI | 计划资金状况、资产池净值及可用抵押品不同。1/(LD)只是切线零点。冲击系数二时路径到达三十轮上限，记录335.47基点及10.81%净值，不是无穷失控证明。保留315个曲面节点及最高3,000基点，并说明局部模型局限。市场压力缓冲至少约250基点，另加运营缓冲。 |
| 18 SVB | 集团与银行口径、总损失与税后损失不同；可供出售亏损18亿美元为税后。预期提款不等于完成付款。BTFP是合格机构及抵押品的流动性贷款，不消除损失；二〇二四年三月停止新贷款。资产DV01并非完整银行风险系统。 |
| 19 工坊 | 四个示例头寸，有限关键利率及有符号因子报告；基金负债现值54.9而非100。拟议验证标准不同于已实现服务。 |
| 研究及回顾 | 振荡要求全非负且某个幂的所有子式严格正，非仅元素正。符号变化数不决定形状、方差集中或经济意义。经验负子式使假设不成立；平均本身不保证全非负。暂停后展示三阶特征对；四个交易台问题及十道题解见下。 |

## 四个交易台问题

1. **十年零息，年收益率4%。** 价格67.5564，麦考利久期10，修正久期9.6154。收益率上升一基点，局部每百元面值损失约0.06496。
2. **凸性较大就必然更贵或收益率更低吗？** 不是。局部二阶变化为−DΔy+½C(Δy)²，不能推出任意有限变化下的支配。现金流、初始价格、期权、漂移、持有收益及融资都重要，½Cσ²并非普遍收益率折价。
3. **为什么互换固定利率能低于国债？** 融资、流动性、抵押、资产负债表及对冲需求不同。回购买国债加互换付固定，仍有浮动指数与回购基差、票息、时点及展期风险。持债摩擦模型可支持负均衡利差，却不证明监管解释每个观测。
4. **SVB案例需要什么报告？** 联合资产负债经济价值压力、存款行为、现金、可用抵押品、提款情景及融资能力。总HTM缺口、账面资本及资产DV01回答不同问题。未保险状态本身不识别存款久期。

## 十道题及解答

1. **远期。** 正贴现因子且t₂>t₁≥0时，f(t₁,t₂)=[t₂z(t₂)−t₁z(t₁)]/(t₂−t₁)。若z在t>0可微，则f(t)=z(t)+t z′(t)，因此f>z等价于z′>0。插值结点应指定单侧或导数惯例。这是匹配估值假设下的隐含利率恒等式，不是物理预期恒等式。
2. **久期。** 零息只在T支付，麦考利久期为T，年复利修正久期T/(1+y)。c>0、y>0的年付永续债，价格c/y，修正久期1/y，麦考利久期(1+y)/y；5%时为21年。永续求和要求y>0。
3. **局部凸性。** 冻结时点，D=−P_y/P、C=P_yy/P。若EΔy=μdt、E(Δy)²=σ²dt，局部预期价格重估约为(−Dμ+½Cσ²)dt。实际总回报还包含明确时间变化、沿曲线滚动及票息，也可能有融资、现金流变化及期权。持有收益等于报价收益率是额外假设，不能由此推出无套利收益率折价。
4. **手算自举。** 年复利下100=5/1.04+105/(1+z₂)²，故z₂=sqrt[105/(100−5/1.04)]−1，约5.025%。先用已知一年零息贴现首笔票息，末笔票息与本金共同确定两年零息。
5. **互换。** 理想重置日单曲线、单位名义本金下，浮息腿1−Z(T)，固定腿KA，A=ΣτᵢZ(tᵢ)，故K*=(1−Z(T))/A。收固定价值V=(K−K*)A，微分dV=−A dK*+(K−K*)dA。平价附近下降一基点约收益A乘10⁻⁴。多曲线、付款滞后及已固定票息需相应调整。
6. **免疫。** 负债现值54.8812；权重由w₅+w₃₀=1及5w₅+30w₃₀=15得0.6、0.4，资产现值32.9287及21.9525。平行连续利率凸性375，对负债225。一般雷丁顿条件给局部结果；这里S(a)/L=.6e^(−5a)+.4e^(−30a)−e^(−15a)由詹森不等式对任意平行a非负。这一特殊全局结果不控制扭曲、信用或融资。
7. **泰勒基准。** 2+4+.5(4−2)+.5(−1)=6.5%。它取决于中性利率、目标、测量及系数，不是强制行动或最优政策定理。
8. **局部LDI。** 初始净值一、资产四、久期二十五，切线零点为1/(4×25)=一个百分点。上升五十基点后，模型净值0.5，资产3.5。恢复初始0.01净值对久期风险缓冲，目标资产为.5/(25×.01)=2，出售1.5，即剩余资产42.86%，或初始资产37.5%。这忽略出售时的市场冲击，并把局部价格近似当作模型，不是精确偿付或保证金经济。
9. **马尔可夫全非负。** Bᵢⱼ在i≥j时为ρ^(i−j)，否则零，D=diag(1,1−ρ²,…,1−ρ²)，直接相乘得C=BDBᵀ。B可分解为非负初等下双对角矩阵，利用柯西比内公式，乘积全非负。D为正使其非奇异，C相邻副对角为正，故具有振荡性质。三阶时a±=(−ρ±sqrt(ρ²+8))/2，v±=(1,a±,1)，λ±=1+ρ²/2±(ρ/2)sqrt(ρ²+8)；另有v₂=(1,0,−1)，λ₂=1−ρ²。当0<ρ<1，λ+>λ₂>λ−>0，忽略中间零后的变号数为零、一、二。元素及特征值随ρ变化；零端点特征值退化，一端点矩阵奇异。
10. **协方差平均。** 有限二阶矩且允许交换积分及协方差时，Cov(Δy(m₁),Δy(m₂))=(m₁m₂)⁻¹∫₀^m₁∫₀^m₂ c(s,t)dsdt。积分能抑制细尺度变化，但任意光滑或随距离递减的协方差核未必全非负。仅靠平均，不能证明所有子式条件、振荡幂、每对相关性增加或普遍三因子方差占比；需要额外核假设及证明。

教材、论文及官方来源见上方链接。数据为固定GSW、财政部平价及拍卖记录、FRED及EDGAR集团事实。危机日期、购买总额及罚款为引用数字，不是自行计算；不宣称与纽约联储一致的统计量，也不报告封存回报绩效。渲染成功不等于视觉通过；完整生产旁白的连续听审仍是独立验收。
