# Quant, Built — Part 41: Leverage, Liquidity and Crises

Fourteen scenes connect leverage, collateral, common holdings, network clearing and runs. The proposed House rule is a teaching design using public market returns and chosen financing assumptions. It is not an approved live leverage limit or evidence about a sealed strategy. Current artifact-bound visual evidence is linked below; continuous production listening remains separately pending.

## Data and execution scope

All thirteen unchanged ordinary originals were classified by a transitive source audit before output-path inspection. Each was invoked once and succeeded: `desk`, `spiral`, `firesale`, `network`, `systemic`, `gfc`, `dash`, `china`, `y2023`, `research`, `ltcm`, `dd`, `house`. Their closed output hashes are pinned in `common.py`. This part's `compute_house` is an ordinary public-French-return margin simulation; it has no experiment-output dependency. Unknown names and experiment-related names are rejected before counted loading or cache-path access.

The audit identifies twelve possible immutable public keys. French daily factors and 49 industries are frozen through 2020-12-31; FRED supplies TEDRATE, BAA10Y, DGS10, DGS2, DCPF3M and DPSACBW027SBOG over the specified windows; Yahoo supplies Shanghai Composite closes. French, FRED and Yahoo daily readers inspect raw files before their normal checker, so each received an exact-key guard before any raw-file/network access. The unchanged checker verified the inputs. All eleven inherited rejected keys remain barred; none intersects this part's audited inputs. No failed key was retried, no source was refreshed and no replacement fit was made.

Every `compute.py`, the financial algorithms and all 98 protected files remain unchanged. No registration, new market trial, sealed experiment opening, strategy payload reading or outcome scoring occurred. Existing registrations remain 23,561 through Part 41 and 23,562 globally. The ordinary output called `house` must not be confused with a strategy cache: its source closure was explicitly classified before access. Do not run an unguarded default computation or use force/refresh to reproduce this review. Missing or changed pins fail before implicit computation.

## Chapters

| Scene | Focus |
| --- | --- |
| Hook | Chosen leverage, network and run examples; a quantitative prediction |
| Cycles | Balance-sheet leverage, binding haircuts, Minsky and collateral cycles |
| Spirals | Chosen loss/margin dynamics, finite rounds and depth sensitivity |
| FireSales | Common holdings; the original high-leverage sales approximation |
| Networks | Pro-rata clearing, senior-resource buffers and conditional topology comparisons |
| Systemic | Conditional CoVaR, MES sign conventions and qualified SRISK proxies |
| LTCM | A uniform-loss balance-sheet bridge, crowding and privately funded recapitalization |
| GFC | Wholesale funding, mixed-component yield spreads and contractual collateral calls |
| Dash | Actual calendar dates in March 2020; basis, funding and intermediation limits |
| China | Shanghai observations versus CSI300 triggers; historical halt rules |
| Y2023 | Historical LDI/bank stress, chosen run payoffs and recourse liquidity facilities |
| House | Public-return margin simulation; grid and volume-arithmetic limits |
| Research | Clearing existence/uniqueness, numerical checks and threshold conditions |
| Outro | Qualified recap and twelve solved problems in 6/4/2 groups |

## Scientific conventions and limitations

For assets A, equity E and debt D, A=E+D and leverage λ=A/E. A loss x>0 gives assets A−x and equity E−x if debt is fixed. Selling assets to repay debt leaves equity unchanged. Exact restoration of initial leverage therefore sells `(λ−1)x`. The unchanged `glt_firesale` implementation instead sells `λx`, a high-leverage approximation. Its second-round marks use chosen holdings and linear impact on post-shock holdings; this is not a full multi-round calibrated GLT equilibrium. The numerical outputs are preserved and the approximation is disclosed.

A single collateral book financed with equity and a haircut h has cap A≤E/h. A haircut rise forces a sale only if that cap binds. The geometric spiral multiplier is a local linearization requiring a feedback coefficient below one; nonlinear defaults, changing holdings and finite wealth can invalidate a global extrapolation. Minsky's cash-flow categories do not make asset prices or operating cash flows riskless. Collateral-cycle comparisons require their model assumptions.

CoVaR is a conditional system-return quantile at a specified institution-return state. Its probability equality requires an appropriate continuous, correctly specified conditional distribution. The unchanged estimator uses finite IRLS, with specification and numerical error. Delta CoVaR compares fitted tail-state and median-state quantiles; it does not identify a causal institutional contribution. Industry portfolios are proxies for firms. MES here is the typically negative average return on the market's worst 5% of days. The long-run heuristic changes sign to a positive loss m and uses `1−exp(−18m)`. Its usual motivation uses a 2% daily tail; feeding it a 5% industry MES is an explicit mismatch. The Lehman illustration also substitutes book equity for market capitalization, so its result is not standard firm-specific estimated SRISK. The correct shortfall is `kD−(1−k)(1−LRMES)E`, with a chosen k=.08; system shortfall sums positive parts.

TED is three-month LIBOR minus the Treasury-bill yield, reflecting bank credit, funding liquidity and safe-haven demand. BAA10Y also mixes credit, liquidity and maturity effects; neither is a default probability. AIG collateral calls depended on valuation as well as rating terms. Stable money-fund NAV was not an FDIC deposit guarantee. LTCM's gross derivatives notional is not net exposure; 4.7/125 is a uniform asset-value-loss bridge, not a spread-basis-point or complete trading-loss calculation. The New York Fed facilitated a privately funded recapitalization; that description does not settle broader debates about rescue incentives.

March 2020 dates use actual days since 2020-02-01: March 1 is day 29, April 1 day 60 and May 1 day 90; March 9–18 spans days 37–46. Other historical plots use actual fractions of their calendar year. Equity wealth is compounded from the first selected February return, relative to the preceding unit base; it is not a peak-to-trough drawdown. The pandemic episode combined economic losses and market dysfunction. Yield/index charts do not identify one causal seller, the effect of policy alone, or a meaningful comparison of a two-week acute episode with an eighteen-month crisis. Treasury basis shorthand needs conversion factors, cheapest-to-deliver, delivery options, repo specials and residual risk. Regulatory balance-sheet constraints were one component of intermediation capacity.

Shanghai Composite returns are not CSI300 circuit-trigger values. The short-lived January 2016 market-wide rules applied to moves in either direction, with late-day closure exceptions. Historical US lower-level pauses likewise have time-of-day qualifications. Index returns alone do not measure how much of a collapse margin calls caused or establish a universal magnet effect.

The chosen run game has nonatomic risk-neutral depositors, unit withdrawal claims, liquidation value r<1 and later asset payoff θ. It is inspired by Diamond–Dybvig, not the complete original liquidity-type contract model. Waiting has a zero branch once f≥r. The uniform-rank threshold additionally assumes a suitable flat/local prior and vanishing-signal construction. A positive root and finite noisy-signal quadrature do not establish general uniqueness for all games. The original r=.85 is chosen, not a calibration of SVB. The pretax HTM fair/book gap subtracted from group book equity omits taxes, other marks and bank/group differences; it is not a complete solvency determination. A historical BTFP par-collateral recourse loan provides liquidity without erasing economic losses, interest or repayment obligations. Historical policy and AT1 descriptions do not certify current law or litigation outcomes.

The House path rebalances daily toward target leverage subject to its haircut cap, and can re-lever after gains. Recorded `forced` sales are haircut-attributable reductions relative to the target, not all turnover. The fixed haircut is the coded floor/cap applied to half a pre-2008 99th-percentile volatility multiplier; it is not a certified stress quantile. Funding headroom differs between paths. Their realized equity ordering does not identify a causal margin-policy effect or general benefit from forced selling. The shock is the worst day within 2008, not the worst historical day. Leverage above four violates the chosen initial 25% haircut; the extended sweep is hypothetical. Its quarter-step maximum is a discrete grid result. Ten-percent participation in normal volume yields volume-equivalent time, not executable stressed depth. No actual term-funding lock, live strategy financing or deployment approval is established.

## Clearing theory

Let L≥0 be nominal interbank debts, `pbar_i=Σ_j L_ij`, outside assets e≥0, and `Π_ij=L_ij/pbar_i` for pbar_i>0. Set a zero-debt row to zero. The clearing map is `Φ(p)=min(pbar,e+Πᵀp)` on `[0,pbar]`, with equal priority and no default costs.

The map is monotone, so Tarski gives greatest and least fixed points. Continuity also lets decreasing iteration from pbar and increasing iteration from zero converge to them. A sufficient regularity condition is that every bank has an obligation path to a bank with positive outside assets. Under it the two fixed points coincide. A two-bank zero-outside-asset cycle instead has every `(t,t)`, 0≤t≤1, as a fixed point. Regularity is sufficient, not a claim that every failure of the condition causes multiplicity.

Exact fictitious-default reasoning permits at most n strict default-set additions; a final no-change check can be additional. The unchanged implementation uses finite inner Picard iterations and tolerances, so its recorded outer checks are not identical to strict additions. The 200 chosen random examples agree within 1e-8, supporting those numerical cases without replacing the proof.

In the symmetric complete senior-debt model, write b=a−v>0 and assume `y>(n−1)b`. The hit bank's shortfall, if others pay, is `s=min(y,(ε−b)_+)`. Every other bank loses s/(n−1). Hence there are zero defaults for ε≤b, one for b<ε≤nb, and all for ε>nb. At equality others can still pay. If y is too small, even a zero-paying hit bank may not exhaust others' buffers. Large negative `a−ε` is interpreted as a stylized net-resource shortfall against senior obligations, not negative gross assets. The cluster/fire-sale examples use chosen links, finite shock grids and finite iteration; no universal cluster cap or global convergence theorem follows. Maximum-entropy reconstruction and payment-amplification bounds have metric- and model-dependent conclusions.

## Problems and complete solutions — foundations 1–6

1. **A=4, E=1; a 5% asset loss; restore 4×.** Debt is fixed at 3. Assets become 3.8 and equity .8; leverage is 3.8/.8=4.75. Restoring 4× permits assets 3.2. Sell .6 and repay debt, leaving debt 2.4 and equity .8. The sale is .6/3.8=15.789% of remaining assets. This assumes no fees, financing return or price impact.

2. **A=8, E=1, h=.10; lose 3% and double h.** Fixed debt is 7. New assets are 7.76 and equity .76. With h=.20, the cap is .76/.20=3.8; sell 7.76−3.8=3.96, or 51.0309% of remaining assets. Repaying debt leaves 3.04 debt, .76 equity and leverage 5, exactly 1/h. The original 8× position was feasible under the original cap 10.

3. **Local spiral multiplier.** At initial unit price, assets A and target λ, a small mark-to-market loss Aδ lowers equity by Aδ. Exact debt-repaying restoration sells `(λ−1)Aδ`. With linear marginal impact γ, the next loss fraction is gδ, where `g=γ(λ−1)A`. If the approximation holds for each increment and 0≤g<1, total fall is `δΣ_k g^k=δ/(1−g)`. At g≥1 that geometric approximation has no finite convergent sum. It does not prove an actual finite-wealth market falls without bound; nonlinear impact, bankruptcy, holdings and funding can intervene. This local approximation is distinct from the unchanged finite-round spiral implementation.

4. **A=100, E=5; lose 1%; restore 20×.** Loss is 1, so assets 99 and equity 4. Target assets are 80, requiring a sale of 19 and debt repayment. Debt falls from 95 to 76 and 80/4=20. Exact sale is `(20−1)×1=19`; the original high-leverage GLT approximation would sell 20. State which rule is used.

5. **Three-bank clearing.** A owes B 2, B owes C 2, C owes A 1; outside assets are (.5,0,.3). Thus pbar=(2,2,1), and the equations are `p_A=min(2,.5+p_C)`, `p_B=min(2,p_A)`, `p_C=min(1,.3+p_B)`. Candidate `(1.5,1.5,1)` satisfies each: min(2,1.5)=1.5, min(2,1.5)=1.5, min(1,1.8)=1. Equities `e+Πᵀp−p` are (0,0,.8). A and B default strictly; C pays in full. Every bank reaches positive outside assets along the ring, so the sufficient regularity condition holds and the clearing vector is unique. Debts and payment bounds are essential to this verification.

6. **Complete network n=20, a=2, v=1.5, y=12.** Buffer b=.5 and `(n−1)b=9.5<12`, so the stated threshold conditions hold. There are no defaults for ε≤.5; only the hit bank defaults for .5<ε≤10; all default for ε>10. At ε=10 each other bank exactly absorbs .5 and can pay in full. The shortfall cap y does not invalidate the all-default threshold because y exceeds 9.5. Omitting y would leave the problem under-specified.

## Advanced practice 7–10

7. **Conditional quantile slope .5, tail state −4%, median +.1%.** The fitted difference is `.5×(−4%−.1%)=−2.05` percentage points. The fitted system-return quantile is lower in the tail state by that amount. The intercept cancels. This is not a causal loss attributed to the institution, nor a probability or a 2.05% reduction relative to a denominator.

8. **k=.08, D=500, E=20, LRMES=.5.** Remaining equity is 10. The ratio-k shortfall is `.08×500−.92×.5×20=40−9.2=30.8`. Equivalently, required capital is .08×(500+10)=40.8 against existing capital 10. Its positive part is also 30.8. Negative shortfalls elsewhere are not automatically transferable capital when aggregating system need. The ratio and crisis-loss input are chosen assumptions.

9. **θ=1.2, r=.8 and f=.5 in the chosen run game.** Withdrawals require f/r=.625 units of liquidation, below the available unit. Early payoff is 1; late payoff is `1.2(1−.625)/(1−.5)=.9`. An atomless individual prefers to withdraw when others withdraw at this share. This is a best-response comparison at a chosen aggregate share, not a proof that f=.5 is an equilibrium. For f≥r, late payoff is zero and early payoff is min(1,r/f), using the f=0 convention separately.

10. **Chosen bank: deposits 100, equity 8, bonds 90 and cash 18.** The balance sheet balances at assets 108. With bond modified duration 6 and a parallel +.03 yield change, first-order bond loss is `90×6×.03=16.2`. Bonds mark to 73.8, total assets to 91.8 and equity to −8.2 if cash and liabilities are unchanged. Omitted convexity usually matters for such a large yield move; a positive-convexity plain bond would lose less than its duration-only approximation, but no exact price follows without cash flows and yields. Taxes, hedges, other assets and funding also matter. This chosen arithmetic is not a real-bank solvency or regulatory-capital determination.

## Qualifying problems 11–12

11. **Existence, regularity-based uniqueness and fictitious default.** For nonnegative e and L with zero-debt rows defined as zero, Φ is a continuous monotone map from the compact order interval [0,pbar] into itself. Tarski gives least and greatest fixed points. Alternatively, `p^(0)=pbar` and `p^(k+1)=Φ(p^(k))` decrease and stay nonnegative. Their limit is fixed by continuity; every fixed q≤pbar stays below all iterates, so this limit is greatest. Iteration from zero gives the least.

    For uniqueness under the stated path-to-positive-e condition, let `d=p+−p−≥0` and `S={i:d_i>0}`. A bank in S is below its liability cap under p−, so `p−_i=e_i+(Πᵀp−)_i`; under p+, `p+_i≤e_i+(Πᵀp+)_i`. Thus `Σ_S d_i≤Σ_{j∈S}d_j Σ_{i∈S}Π_ji≤Σ_S d_j`. Both inequalities must be equalities. Every j∈S sends all payment shares into S, and both clearing vectors satisfy equality with available resources there. Summing the p+ resource equations on S and canceling internal payments gives `0=Σ_S e_i+Σ_{j∉S}p+_j Σ_{i∈S}Π_ji`. All terms are nonnegative, so e=0 on S. Since S has no outward obligation path, it cannot reach a positive-e bank, contradicting regularity unless S is empty. Hence p+=p−.

    For exact fictitious default, begin with no defaults/full payments. Recompute the defaulting subsystem while nondefaulters pay in full and enlarge the default set when needed. Monotonicity keeps payments above the greatest clearing vector and makes default sets grow. There are at most n strict enlargements. When the set stabilizes, the solved payments satisfy Φ(p)=p and remain at least p+, hence equal p+. A final stability check may be additional. This proof assumes exact subsystem solutions under the appropriate regularity conditions. Finite inner Picard limits, numerical tolerances and recorded outer checks in the unchanged implementation are separate implementation facts, not literal finite exact convergence in n floating-point loop evaluations.

12. **Chosen uniform-rank run threshold with insurance.** Assume nonatomic risk-neutral depositors, unit early claims, liquidation value 0<r<1, late payoff θ, the stated locally flat-prior/vanishing-private-signal construction, and an insured share s assumed never to run. Let a=1−s>0. Rank u is uniform on [0,1], so f=au is uniform on [0,a]. Define `E(f)=min(1,r/f)` with E(0)=1, and `W(f;θ)=θ w(f)`, where `w(f)=(1−f/r)/(1−f)` for f<r and w=0 otherwise. The expected gap is linear in θ with positive coefficient `I_w=∫_0^a w(f)df`, so the selected indifference root is unique and equals `θ*=I_E/I_w`, with `I_E=∫_0^a E(f)df`. Root uniqueness of this integral is not a general equilibrium-uniqueness theorem.

    If 0<a≤r, `I_E=a` and `I_w=a/r+(1/r−1)log(1−a)`. If r<a≤1, `I_E=r[1+log(a/r)]` and `I_w=1+(1/r−1)log(1−r)`. For θ=1, w(f)<E(f) on a positive-measure subset for every a>0, so I_w<I_E and θ*>1. When a≤r, w decreases in f, so its average over [0,a] falls as a grows and θ*=1/average(w) rises. When a>r, I_w is constant and I_E rises, so θ* again rises with a. Therefore increasing the insured non-running share lowers the threshold. As a→0, both integrals are asymptotic to a and θ*→1. At a=0 there is no uninsured marginal depositor; the limiting number is not an indifference equation for an existing runner. Likewise r→1 makes payoffs approach the no-liquidation-loss case. An actual recourse loan at par is not literally r=1: interest, repayment, collateral eligibility and institutional behavior remain.

## Primary historical sources and verification

The [Federal Reserve SVB review](https://www.federalreserve.gov/publications/files/svb-review-20230428.pdf) distinguishes the over-$40bn March 9 outflow from management's expectation of over $100bn more on March 10. The [March 12, 2023 BTFP announcement](https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312a.htm) and [original term sheet](https://www.federalreserve.gov/newsevents/pressreleases/files/monetary20230312a1.pdf) state eligible collateral, up-to-one-year loans, the interest rule and recourse beyond collateral. [Greenspan's October 1, 1998 testimony](https://www.federalreserve.gov/boarddocs/testimony/1998/19981001.htm) describes the private-sector LTCM adjustment and says no Federal Reserve funds were put at risk. [FINMA's March 23, 2023 statement](https://www.finma.ch/en/news/2023/03/20230323-mm-at1-kapitalinstrumente/) explains its historical AT1 decision using contractual terms and the emergency ordinance; this is the authority's dated account, not a current court ruling. Local lookup receipts retain successful bytes/hashes and unsuccessful BoE HTTP403 responses without treating those responses as read evidence. Paper coverage remains in [READING.md](../READING.md).

One existing pure crisis test passed. Fresh construction, actual bilingual image inspection, sampled speech signals and final motion review remain pending; successful computation or a source edit is not visual approval.

# 第41部分：杠杆、流动性与危机

十四个场景讨论杠杆、抵押品、共同持仓、清算与挤兑。本部分的公司规则是用公开市场收益和选定融资参数构成的教学方案，并非已批准的实盘杠杆或封存策略业绩。十三个经传递源码审计的普通原始计算各运行一次，全部成功；其中`house`仅使用公开市场收益，不读取策略结果。十二个可能的公开输入键由原检查器验证，十一项继承拒绝键继续在原始读取之前拦截。金融算法、所有`compute.py`及98个受保护文件不变；无刷新、失败键重试、新市场试验或封存策略读取。第41部分累计登记仍为23,561，全局23,562。

## 科学约定

固定债务下，资产损失x后，恢复原杠杆λ的精确卖出量为(λ−1)x；原`glt_firesale`使用λx，是保留不改的高杠杆近似。保证金上升只有在新的权益/折扣率上限约束持仓时才迫使卖出。几何螺旋仅是反馈系数小于一时的局部线性模型。

CoVaR是条件分位数，ΔCoVaR是尾部状态与中位状态的拟合差，不是因果贡献。这里MES是市场最差5%日期的平均行业收益，通常为负；长期启发式先改为正损失m，再用1−exp(−18m)，但其常见动机使用2%日尾部，存在明确的代理不匹配。雷曼例子还以账面权益代替市值，因此不是标准的公司级SRISK估计。正确式为kD−(1−k)(1−LRMES)E；本例k=.08，总需求应加总各项正部。

TED混合银行信用、融资流动性和国库券避险需求；Baa减十年期国债还包含期限与流动性差异。AIG追加抵押品取决于估值和评级条款。货币基金的稳定净值目标不是存款保险。LTCM的4.7/125仅是均匀资产价值损失桥梁，不是利差基点或完整衍生品损失模型。2020年图使用真实日历：以2月1日为第0天，3月1日为29、4月1日为60、5月1日为90；3月9—18日为37—46。公开指数与收益率不能单独识别卖方、政策因果效应或整个危机持续期。上证指数不是CSI300熔断触发指数，历史熔断还包含方向和时段例外。

挤兑例子假设无原子、风险中性存款人、单位提前取款、清算价值r和未来支付θ；并非原戴蒙德—迪布维格模型的完整流动性类型合约。f≥r时等待收益为零。均匀排序阈值还需要所述局部平坦先验与私人信号极限；数值根唯一并不证明所有银行博弈的均衡唯一。r=.85不是SVB标定。持有至到期证券税前市值差减集团账面权益，遗漏税、其他估值和实体差异，不能单独判断偿付能力。BTFP按面值计抵押品的有追索权贷款提供流动性，不消除损失、利息和还款义务。

公司日路径会按目标杠杆再平衡，盈利后也可能重新加杠杆；`forced`只计相对目标的折扣率额外减仓，不是全部成交。固定折扣率与波动关联方案的融资余量不同，某段历史的权益排序不能识别政策因果效应。压力日仅是2008年内最差日期；初始25%折扣率下超过4倍原本就不可行。离散网格最大值不是连续精确边界，正常成交量十分之一只产生“成交量等价时间”，不保证压力执行。没有证明实际三十日融资锁定或实盘可行性。

## 基础题1—6：完整解答

1. **资产4、权益1，资产跌5%，恢复4倍。** 固定债务3。资产3.8、权益.8，杠杆4.75；目标资产3.2，卖出.6并还债，债务2.4，权益仍.8。卖出占剩余资产15.789%。忽略费用、融资收益和价格冲击。

2. **资产8、权益1，初始折扣率10%，资产跌3%，折扣率翻倍。** 债务7，冲击后资产7.76、权益.76。新上限.76/.20=3.8；卖出3.96，占剩余资产51.0309%。还债后债务3.04，资产/权益=5=1/h。初始8倍低于原上限10倍。

3. **局部螺旋。** 初始单位价格、资产A、目标杠杆λ，小损失Aδ后精确恢复杠杆须卖出(λ−1)Aδ。线性边际冲击γ产生下一轮跌幅gδ，其中g=γ(λ−1)A。假设每个增量都维持此线性近似，0≤g<1时总跌幅δΣg^k=δ/(1−g)。g≥1时几何近似不收敛；并不表示真实有限财富市场会无限下跌，破产、持仓、融资与非线性会改变模型。不要与保留不改的有限轮数值实现混同。

4. **资产100、权益5，跌1%，恢复20倍。** 损失1，资产99、权益4。目标资产80，卖出19并还债，债务从95减至76；80/4=20。精确式(20−1)×1=19；原高杠杆近似会卖20，须说明使用哪一种。

5. **三家清算。** A欠B 2，B欠C 2，C欠A 1；外部资产(.5,0,.3)，总债务(2,2,1)。方程为pA=min(2,.5+pC)、pB=min(2,pA)、pC=min(1,.3+pB)。代入(1.5,1.5,1)，分别得min(2,1.5)、min(2,1.5)、min(1,1.8)，全部成立。权益e+Πᵀp−p=(0,0,.8)。A、B严格违约，C全额支付。各银行沿债务链可达外部资产为正的节点，满足充分正则性条件，所以解唯一。缺少债务上限便无法完成这项验证。

6. **完全网络n=20、a=2、v=1.5、y=12。** 缓冲b=.5，(n−1)b=9.5<12，阈值条件成立。ε≤.5无违约；.5<ε≤10仅受冲击银行违约；ε>10全部违约。ε=10时其他银行恰好吸收.5，仍能全额支付。短缺上限y足够大，不破坏阈值；若不指定y，题目不充分。

## 进阶题7—10：完整解答

7. **分位回归斜率.5、机构尾部−4%、中位+.1%。** 拟合差为.5×(−4%−.1%)=−2.05个百分点，截距抵消。它是系统收益条件分位数在两种机构状态的差，不是因果损失归因、概率或以某基数计算的2.05%相对变化。

8. **k=.08、债务500、权益20、LRMES=.5。** 剩余权益10。短缺=.08×500−.92×.5×20=40−9.2=30.8；亦可算要求资本.08×(500+10)=40.8，减已有10。正部仍为30.8。汇总系统资本需求时，其他机构负短缺不能自动转移来填补此数。k和危机损失都是选定假设。

9. **θ=1.2、r=.8、f=.5。** 需清算f/r=.625单位，未耗尽资产；提前收益1，等待收益1.2×(1−.625)/(1−.5)=.9。无原子的个人在他人处于此提款比例时偏好提前提款；这并不证明f=.5为均衡。f≥r时等待为零，提前为min(1,r/f)，f=0另用提前收益1的约定。

10. **选定银行：存款100、权益8、债券90、现金18。** 资产108，表平衡。修正久期6、平行收益率上升.03时，一阶损失90×6×.03=16.2。债券73.8，总资产91.8，若现金与负债不变，权益−8.2。如此大的利率变化，凸性不可忽略；普通正凸性债券实际损失通常小于纯久期近似，但没有现金流和收益率不能给出精确价格。税、对冲、其他资产与融资也会改变结果；不是现实银行偿付或监管资本判断。

## 资格题11—12：完整证明

11. **清算存在、充分正则性下唯一及虚拟违约。** 令L≥0、e≥0，pbar为各行债务和；正债务行Πij=Lij/pbar_i，零债务行定义为零。Φ(p)=min(pbar,e+Πᵀp)在[0,pbar]上连续、单调且自映射。塔斯基给出最小和最大不动点。或从pbar出发，下一步不大于前一步，序列非负单调下降；连续性使极限为不动点。任一不动点q始终低于各步，所以极限最大；从零向上同理得到最小。

    对唯一性，令d=p+−p−≥0、S={i:di>0}。S内银行在最小解下未达债务上限，故p−_i=e_i+(Πᵀp−)_i；最大解下p+_i≤e_i+(Πᵀp+)_i。相减求和得ΣSdi≤Σj∈S djΣi∈SΠji≤ΣSdj，两处必取等。S内每个j只向S付款，两解在S上都等于全部可用资源。对最大解的资源方程在S求和、抵消内部支付，得到0=ΣS e_i+Σj∉S p+_jΣi∈SΠji。各项非负，故S上外部资产全为零。S又无向外债务链，不可能通往外部资产为正的银行，与所述正则性矛盾，除非S为空。因此p+=p−。这是充分条件；不满足它不必然多解。

    精确虚拟违约从无违约、全额支付开始，在非违约者全额支付的条件下解违约子系统并加入新违约者。单调性使支付不低于最大清算解，违约集合只增不减。严格扩张最多n次；集合稳定后，精确解满足不动点方程且不低于最大解，只能等于最大解。最后一次“无变化”检查可能另外需要一次。本证明使用适当正则性与精确子系统解；原代码的有限内层Picard次数、容差和外层检查数是不同概念，不能宣称n次浮点循环必得精确答案。

12. **带保险的选定均匀排序阈值。** 假设无原子、风险中性、单位提前债权、0<r<1、未来收益θ，并采用所述局部平坦先验与消失私人噪声构造。保险比例s被假设从不挤兑，令a=1−s>0；排序u在[0,1]均匀，则f=au在[0,a]均匀。提前E(f)=min(1,r/f)，E(0)=1；等待W(f;θ)=θw(f)，其中f<r时w=(1−f/r)/(1−f)，f≥r时为零。平均差关于θ线性，系数Iw=∫0^a w df>0，故选定无差异根唯一：θ*=IE/Iw。此积分根唯一不是所有博弈均衡唯一的证明。

    0<a≤r时，IE=a，Iw=a/r+(1/r−1)log(1−a)；r<a≤1时，IE=r[1+log(a/r)]，Iw=1+(1/r−1)log(1−r)。θ=1时，在正测度区间上w<E，因此θ*>1。a≤r时w随f下降，在[0,a]的平均值随a增大而下降，θ*=其平均值倒数随a上升；a>r时Iw不变、IE上升，θ*仍随a上升。所以提高被假设不挤兑的保险比例，会降低阈值。a→0时两积分都等价于a，θ*→1；a=0已无未保险的边际挤兑者，此极限不能说成一个实际存在者的无差异方程。r→1亦趋近无清算损失情形。真实按面值计抵押品的有追索权贷款不等于把r改成1：利息、偿还、资格与行为假设仍然存在。

已通过一个既有纯危机测试。新的双语构造、实际画面审阅、语音信号与最终动画检查仍待完成；计算成功不构成视觉批准。

## Current visual review

Visual review is complete on source `8e6af0dda687be43cd364a684217444ab450a000`, fingerprint `b36f17ee8c330b169d12a6663674c3119e94863b9ebd359e74486888fc8910db`. [Artifact-bound evidence](../../../docs/qa/quant41-polish-evidence.json) binds all 28 bilingual endpoint sheets, 14 English forty-frame motion sheets and 18 native frames actually viewed across fourteen scenes. Automated flags and manually noticed concerns have individual observations and decisions. All 28 current bilingual construction sheets were actually viewed; 105 formatted fields and 52 plotted ranges agree with runtime captures. Earlier diagnostics, the interrupted construction and the retired first final attempt remain independently preserved and confer no final approval. The retired attempt exposed a blank funding introduction; the first data row now appears during the introductory phrase, verified in fresh English and Chinese output.

All 135 actual narration contexts agree across construction, bilingual endpoints and English motion: 72 manually revised Mandarin pairs and 63 exact unchanged pairs. English narration contains 9,506 words, about 56.6 minutes at 168 words per minute. Twelve fully solved bilingual problems retain 6/4/2 grouping. The 99 additive captions preserve all 35,926 baseline values, yielding 36,025. One existing pure crisis test passes.

All thirteen audited unchanged ordinary originals were invoked once and succeeded. This part's `house` is an audited descriptive public-return calculation. Eleven inherited rejected public keys remain barred; all 98 protected files and financial algorithms are unchanged. No refresh, new market trial, sealed strategy access or outcome scoring occurred.

The fourteen-chapter silent preview is 70:07, with English subtitles. Eleven CPU speech reports cover 122 sampled lines; the actual narrated opening lasts 211.400 seconds. Continuous production listening, pronunciation and mastering remain separately pending. Exact observations retain accepted pacing and animation limitations; sampled visual review does not certify every intermediate frame.

## 当前视觉审阅

已实际审阅28张英中文旁白节点画面表、14张英文四十帧动画表及18张原尺寸重点画面，覆盖十四个场景。自动标记和人工关注均有逐项观察与决定，早期诊断及中断尝试均保留独立档案，不向最终画面转移批准。

135处实际旁白在各模式一致：72处人工中文修订，63处英中原样复用；核对105个格式字段与52处图形范围。十二道完整双语题保留六、四、二分组。新增99条字幕保留35,926个原值，总计36,025。一个既有纯危机模型测试通过。

十三个获审计普通原始计算各调用一次且全部成功；本部分house为公开收益的描述性教学计算。十一项拒绝键继续生效，98个受保护文件与金融算法不变，无刷新、新市场试验、封存策略读取或结果评分。十四章静音预览为70:07，含英文字幕；十一份CPU报告检查122句段，配音开场长211.400秒。完整成片连续听审、发音及混音仍单独待办，已接受的节奏和动画限制见逐项证据。
