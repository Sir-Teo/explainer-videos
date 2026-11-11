# Quant, Built — Part 38: Market Making, ETFs and the Speed Race

This is the final part of Act VI in the [forty-three-part series](../README.md). It connects the dealer models of Part 35, queue reconstruction of Part 36 and execution costs of Part 37. The aim is to distinguish a maker's accounting, a quoting model, a tape reconstruction and a market-design argument. None alone demonstrates an executable profitable business.

The eleven chapters cover the opening question; the maker's business; a maker on the tape; reach rates and model quotes; ticks and queues; ETF creation and redemption; the speed race; high-frequency firms; proposed Rule 38; the conditional sniping equilibrium; and the recap and problems.

## Evidence and model scope

Five audited, unchanged ordinary computations succeeded once: `fills`, `glft`, `maker`, `deep` and `bcs`. `glft` loads the previously pinned `fills` output. The sixth original, `etf`, failed the recorded immutable checksum for `yahoo/bars/HYG/2015-01-01_2020-12-31`. It was invoked once; the failed key was recorded, never refreshed or retried, and the function stopped before TLT. No substitute historical fit is used. The ETF chapter uses mechanisms, chosen arithmetic and cited literature rather than a new HYG/TLT chart. The public market manifest, all financial algorithms and all 98 protected files remain unchanged. No strategy is registered: the existing count is **23,552 through Part 38; 23,562 globally**.

The successful measurement inputs are Binance's public `bookTicker` and `aggTrades` for the BTCUSDT perpetual on 16, 17 and 20 May 2023. The 100 ms quote grids are authenticated independently against completed Part 37 provenance; their corresponding raw files still pass the unchanged original checker. Possible key dependencies are audited before dispatch and share a persistent rejection barrier. A possible dependency is not a claim that every original reads every key.

* `fill_intensity` measures a per-side/window threshold-reach probability, averaging buy-side and sell-side events. Its `-log(1-P)/dt` is the rate of a homogeneous Poisson event process with the same no-event probability, not evidence that arrivals are Poisson or that an actual resting queue order fills. Pooled daily probabilities are averaged before the nonlinear conversion. The fitted pooled values are approximately `A=0.2300/s`, `k=0.03530/tick`.
* GLFT assumes an exogenous Brownian reference price, constant trade size, exponential conditional arrival intensities, independent noise drivers and CARA utility. The source computes an interior long-horizon approximation. Its one-second mid-increment standard deviation is about **20.26 ticks/sqrt(second)**; a standard deviation at that sampling interval does not itself establish diffusion scaling. At the four chosen risk aversions, approximate zero-inventory half-spreads are 29.6, 32.1, 38.9 and 75.8 ticks. A reach fit does not validate optimality, queue execution or profit.
* `maker_replay` assumes no impact from its own one-unit orders, pro-rata allocation of net cancellations, displayed-quantity clipping and a specific treatment of old levels. At-price volume must strictly exceed the quantity ahead; a through-price trade fills. The fast flag sees all through-price trades in the current grid step before discarding such fills. That is hindsight selection, not a measured cancel latency or a universal speed bound. Variants produce different selected fills and inventory paths. Final-mid P&L and one-minute signed marks are distinct statistics; late horizons are clipped at the day's end. Funding, fees, executable liquidation and cross-venue hedging are absent.
* On 17 May the slow rule has 42,019 fills, a final-mid mean of -19.785 ticks and a one-minute mean of -19.981. Fast and filtered final-mid means are -8.700 and -4.575, on 19,587 and 7,061 fills. A difference between these selected means is not a causal value of speed. Inventory standard deviation does not report time spent at a boundary.
* `deep` counts at most one reach per side per one-second window. It marks at the mid 1, 10 or 60 seconds **after the window starts**, rather than after a known exact fill time. Threshold prices may require tick rounding in practice. There are no queues, constrained inventory, fees or executable liquidation; positions across windows overlap. Gross marks of about +1.03 ticks at distance 30 and +19.67 at 45, and their sums per elapsed hour, are not a capital-based return or a rigorous upper bound on feasible strategies. The denominator includes full elapsed days while final windows without a full horizon are excluded.
* BCS illustrations assume at least two equally fast firms, independent positive arrival rates, unit uninformed investors, random serial priority and frictionless price undercutting. Snapshots' net mid changes are not identified public-news jumps; aggregate trades are not identified uninformed unit arrivals. The 0.332-tick empirical-magnitude root is a **proxy substitution**, not an estimate of the actual natural spread or an attribution of the replay losses.
* The unchanged batch flag removes stale executions by construction; its numerical interval is unused. It does not simulate latency, a new price-competition equilibrium or welfare. A uniform-phase exposure heuristic and a binary investment game are separately stated below.

Marked wealth obeys a self-financing identity: execution edge at each fill plus rebates plus gains on held inventory, before omitted costs. With taker sign `epsilon`, a horizon adverse mark is `epsilon*(M_h-M_fill)`. The separate horizon edge subtracts that mark **once**. Subtracting it again from the full inventory ledger would double-count the same price move. A signed maker mark from execution price already includes its entry edge.

An ETF band concerns executable basket prices, primary-market terms, funding and settlement, rather than an unconditional bound around published NAV. NAV is marked assets less liabilities divided by shares. Drawdown over time and discount to contemporaneous NAV are different quantities. A close-only series does not measure NAV discount or identify the causal effect of a policy announcement. The March 23, 2020 SMCCF term sheet initially covered investment-grade corporate-bond ETFs; the April 9 expansion included high-yield ETFs. Under a frictionless leveraged-fund calculation with no flows or financing costs, rebalancing exposure is `L(L-1) r A0`, using **beginning-of-day** assets; after a -5% return, a 3x fund sells 30% of starting assets, not ending assets.

Rule 38 is a proposed research standard: use consistent accounting, conservative execution assumptions, past-only validation, measured latency and queue treatment, costs and capital. Live experiments, scaling and deployment approvals have not been performed here.

## Desk questions

1. **Where does profit come from?** Use one marked-wealth ledger. Per-fill horizon edge is another view with a specified horizon, not an independent extra loss. Execution revenues do not establish net profit without all costs and liquidation assumptions.
2. **Why skew inventory?** Within the GLFT approximation a long position widens the bid distance and narrows the ask distance. Risk affects zero-inventory width too. Finite boundaries and the model's assumptions matter.
3. **What do reach rates establish?** Threshold frequencies and Poisson-equivalent rates; they do not establish queue fills, independent price innovations or an optimal executable quote.
4. **What does a binding tick change?** It can move competition from price to priority or size. A selected front/back replay gap is not an identified causal priority price or total rent.
5. **What keeps ETF shares near basket value?** Creation and redemption at executable prices, net of all costs and constraints. A stale published NAV need not be realizable.
6. **What does the sniping root prove?** A unique role-indifference spread under the stated competition assumptions. Industry revenue, pure-sniper transfers, real resource spending and welfare are separate objects.

## Twelve problems, with complete solutions

The first six are basic, the next four advanced, and the final two qualifying-exam level. Their givens match the three enlarged on-screen pages.

1. **Consistent edge.** Execution edge is +0.5 tick, rebate +0.2 and the subsequent adverse taker-direction mid move +0.9. Horizon marked edge is `0.5+0.2-0.9 = -0.2 tick/fill`. A negative signed maker mark and a positive adverse taker mark use opposite signs. This is not a further -0.9 term to subtract from a ledger already including the same inventory price move. Other costs and horizon risk are not included.

2. **Avellaneda–Stoikov approximation.** With gamma 0.1, remaining price variance 4, k 1.5 and inventory 2, approximate total spread is `gamma*variance + (2/gamma)*log(1+gamma/k) = 0.4+20*log(16/15) = 1.6907704` price units. The reservation shift is `-q*gamma*variance = -0.8` price units. Gamma, inventory size and price units must be consistent. This is the stated approximation under its Brownian/CARA/exponential-arrival assumptions.

3. **Convert reach probabilities before fitting.** Over one second, `lambda1=-log(0.70)=0.35667494/s` and `lambda45=-log(0.95)=0.05129329/s`. For two points on `lambda(delta)=A exp(-k delta)`, `k=log(lambda1/lambda45)/44`, approximately **0.0441 per tick**, and the rate halves over `log(2)/k`, approximately **15.7 ticks**. A fit to probability itself gives a different coefficient and does not solve this question. A is `lambda1*exp(k)`. None of this conversion proves actual queue execution or a Poisson process.

4. **Selected replay losses.** Slow loss is `20*40,000=800,000` tick-units; hindsight loss is `9*20,000=180,000`. The total-loss difference is **620,000 tick-units**. With a one-bitcoin unit and $0.10 tick that is $62,000 under the chosen marking convention. Changed selection, number of fills and inventory paths prevent calling it a causal latency value. It is not a universal speed bound or an executable profit forecast.

5. **Tick markup.** In the fixed-mid, no-cost illustration, the full-spread markup is `1-0.3=0.7 cent/unit` for a completed round trip; under symmetry the per-side markup is 0.35 cent per unit filled. Time priority and pro-rata size allocation distribute execution opportunities differently. Actual expected rent additionally depends on fills, adverse selection, capital, cancellations and costs; the markup alone identifies neither who receives it nor net profit.

6. **Executable redemption.** Buy a share for $80. Gross basket proceeds $84 less a selling cost of `0.02*84=$1.68` leave $82.32, hence **$2.32/share**, or 2.9% of $80 before other costs. If executable gross is $79, proceeds are `79*0.98=$77.42`, yielding **-$2.58/share**, even if published NAV still says $84. Financing, primary fees, settlement, basket differences and price risk can change these results. Published NAV alone does not create a locked-in arbitrage.

7. **Random priority and rents.** For a profitable stale quote and N equally likely first messages, cancellation wins with probability `1/N`; a pure sniper wins with probability `1/N` individually, and any sniper wins `(N-1)/N`. Thus the aggregate sniping probabilities are 4/5 and 9/10 at N=5 and 10. At the role root, each role's expected profit is `pi*=lambdaI*h*/N`. Industry profit is `N*pi*=lambdaI*h*`; aggregate profit of the N-1 pure snipers is only `(N-1)/N` of this. Conditional jump gains are transfers from the provider to snipers and cancel from industry profit.

8. **Same root under a particular dispersion.** With rates 10 and 2 and magnitude 3, `h=2*3/(10+2)=0.5 tick`. For an equally weighted mixture of 1 and 5, both magnitudes exceed h when h<1. Then `10h=2*[(1-h)+(5-h)]/2=6-2h`, again giving **0.5**, which verifies the assumed branch. On this support the positive-part payoff is affine, so this mean-preserving spread leaves the root unchanged. Convex-order comparisons need not be strict; variance alone does not give the required order.

9. **Exposure is not a spread ratio.** With uniform news phase, deterministic update latency 5 microseconds and batch length 50 milliseconds, `u=delta/tau=10^-4`. This is a final-window **exposure fraction**, before the probability a rival wins. Preserve the continuous model's conditional race and role structure and replace its jump-opportunity rate by `u*lambdaJ`: then `h_u=lambdaJ*u*J/(lambdaI+lambdaJ*u)`. Consequently `h_u/h_1=u*(lambdaI+lambdaJ)/(lambdaI+lambdaJ*u)`. For rates 10 and 2 this is approximately **0.0001199976**, not 0.0001. The uniform phase, fixed latency, absence of other stale exposure and unchanged conditional competition are extra assumptions. The source batch flag tests none of them.

10. **Four-firm investment game.** Assume a fixed positive prize R per time unit, a binary speed choice, cost c>0, equal sharing among fast firms and zero for slow firms whenever any fast firm exists; if all remain slow each receives R/4. With no fast rival, investing gains `3R/4-c`. With 1, 2 or 3 fast rivals, gains are respectively `R/2-c`, `R/3-c` and `R/4-c`. Thus **0<c<R/4** gives strict dominance of investment. At equality there is a tie in the last case, so dominance is no longer strict. With all investing, each gets R/4-c, worse than all-slow by c; aggregate real resource cost is 4c. This is a fully specified fixed-prize game, not an inference from “a small speed edge wins” alone.

11. **Qualifying: integrable random magnitudes.** Let U>=0, `0<E[U]<infinity`, lambdaI>0, lambdaJ>0 and N>=2. Write `B(h)=lambdaJ E[(U-h)+]` for h>=0. In the equal-speed unit-order role model, `piL=lambdaI*h-(N-1)B(h)/N` and each `piS=B(h)/N`. Continuous undercutting and switching roles give the indifference candidate `Phi(h)=lambdaI*h-B(h)=0`; N cancels. This is a role-model result under the stated assumptions, not a characterization of all market games.

    Positive part is 1-Lipschitz in h, so B is finite, continuous and nonincreasing. `Phi(0)=-lambdaJ E[U]<0`. Since `B(h)<=lambdaJ E[U]`, Phi tends to infinity. The intermediate value theorem gives existence. For h2>h1, `Phi(h2)-Phi(h1)>=lambdaI*(h2-h1)>0`, establishing uniqueness. Constant U=J gives the root in problem 8. Zero jump mass or zero arrival rates require separate boundary cases and are excluded by the givens.

    If `U1 <=cx U2` in convex order, with finite equal means, `(u-h)+` is convex in u and hence `B1(h)<=B2(h)` at every h. At root h1, `Phi2(h1)<=0`; strict monotonicity of Phi2 implies `h2>=h1`. This does not follow from equal means and larger variance alone. Equality is possible, as in problem 8. At the root B=lambdaI*h, each role earns B/N; industry receives B, pure snipers `(N-1)B/N`. Investor payments are transfers to the industry, not automatically an equal deadweight welfare loss. Resource costs and participation effects need a separate analysis.

12. **Qualifying: exact finite-cap HJB versus interior approximation.** Let `dS=sigma dW`, inventory q in the integers -Q,...,Q with Q>=1, unit fills, bid distance delta_b=S-b, ask distance delta_a=a-S, and intensities `A exp(-k delta)` with A,k,gamma>0. Arrival drivers are independent of W, controls predictable and admissible, and a boundary-disallowed side is omitted. Terminal utility is `-exp[-gamma(x+qS)]` with no liquidation penalty. The HJB is

    `0 = u_t + (sigma^2/2)u_SS + sup_delta_b Ae^(-k delta_b)[u(t,x-S+delta_b,q+1,S)-u] + sup_delta_a Ae^(-k delta_a)[u(t,x+S+delta_a,q-1,S)-u]`.

    Set `u=-exp[-gamma(x+qS+theta_q(t))]`, theta_q(T)=0. At an interior admissible optimum, the bid FOC gives `exp[-gamma(delta_b+theta_(q+1)-theta_q)]=k/(k+gamma)`. Hence `delta_b*=theta_q-theta_(q+1)+log(1+gamma/k)/gamma`; replace q+1 by q-1 for the ask. If a separate nonnegative-distance or tick constraint is imposed, this unconstrained FOC must be modified at that constraint.

    Write `a0=log(1+gamma/k)/gamma`, `C=A(1+gamma/k)^(-k/gamma)/(k+gamma)`. Substitution yields `theta'_q=(gamma*sigma^2/2)q^2-C*sum_neighbors exp[k(theta_neighbor-theta_q)]`. With `w_q=exp(k theta_q)`, `alpha=k*gamma*sigma^2/2` and `eta=A(1+gamma/k)^(-(1+k/gamma))`, the exact **calendar-time** system is `w'_q=alpha*q^2*w_q-eta*sum_neighbors w_neighbor`, w_q(T)=1. There is only one neighbor at each inventory endpoint.

    In time to maturity tau=T-t, `w_tau=B w`, with `B_qq=-alpha*q^2` and neighbor entries eta. This finite irreducible symmetric Metzler matrix has a strictly positive eigenvector psi for its largest eigenvalue. As tau grows, w after scalar normalization converges to psi. Therefore stationary quotes are `(1/k)log(psi_q/psi_(q+1))+a0` and `(1/k)log(psi_q/psi_(q-1))+a0` on allowed sides. The scalar exponential growth factor cancels from the ratios; the unnormalized w need not converge.

    Away from relevant finite boundaries, replace neighbor sums by `2psi+psi''`. A Gaussian ansatz `psi(q)=exp[-b*q^2/2]` balances q^2 terms with `b=sqrt(alpha/eta)`. Then `c=b/k=sqrt[sigma^2*gamma*(1+gamma/k)^(1+k/gamma)/(2Ak)]`, giving `delta_b≈a0+(2q+1)c/2`, `delta_a≈a0-(2q-1)c/2`. At zero inventory half-spread is a0+c/2. These are the **interior Gaussian approximations** computed in this lesson, not exact finite-Q formulas.

    Within that approximation, as gamma tends to zero, a0 tends to 1/k and c tends to zero. At **fixed finite Q**, however, the exact risk-neutral long-horizon B has zero diagonal and off-diagonal A/e. Its top eigenvector is `psi_q=cos(q*pi/(2Q+2))` up to scale. Thus at q=0 the exact half-spread tends to `1/k-log[cos(pi/(2Q+2))]/k`, which exceeds 1/k. Taking Q large removes this boundary correction. The orders of the finite-cap, long-horizon and small-risk limits must not be conflated.

## Sources and reproducibility

The primary mathematical reference is Guéant, Lehalle and Fernandez-Tapia, [*Dealing with the Inventory Risk*](https://arxiv.org/abs/1105.3115), especially its setup, linear transformation and spectral approximation. BCS refers to Budish, Cramton and Shim (2015), *The High-Frequency Trading Arms Race*. Further references include Avellaneda and Stoikov (2008); Garman (1976); Ho and Stoll (1981); Glosten and Milgrom (1985); Stoll (1989); Huang and Stoll (1997); Menkveld (2013); Cartea, Jaimungal and Ricci (2014); Dayri and Rosenbaum (2015); Menkveld and Zoican (2017); Baron et al. (2019); Pan and Zeng (2019); Baldauf and Mollner (2020); Haddad, Moreira and Muir (2021); Aquilina, Budish and O'Neill (2022). Textbooks are Guéant (2016), Cartea–Jaimungal–Penalva (2015), Lehalle–Laruelle (2018), and Gastineau (2010).

The historical ETF discussion uses Aramonte and Avalos, [BIS Bulletin 6, *The recent distress in corporate bond markets: cues from ETFs*](https://www.bis.org/publ/bisbull06.htm), and the Federal Reserve's official [March 23 term sheet](https://www.federalreserve.gov/newsevents/pressreleases/files/monetary20200323b2.pdf) and [April 9 term sheet](https://www.federalreserve.gov/newsevents/pressreleases/files/monetary20200409a2.pdf). The 2024 tick amendment is described as an [adoption](https://www.sec.gov/newsroom/press-releases/2024-137), without claiming its historical compliance date is the current rule. Proprietary studies and firm disclosures are attributed literature findings, not numbers generated from the House's public inputs.

Local audit, failures, pinned hashes and subsequent actual visual reviews are preserved under `renders/qa/quant38/`. Use existing pinned ordinary outputs for rendering; do not refresh or retry the rejected ETF original. One existing pure library test is `tests/test_quant_house.py::test_making_glft_fills_and_sniping`. Chosen arithmetic and finite-matrix checks are distinct from new market experiments. Final visual approval will be recorded only after fresh English/Chinese construction and final render inspection; a render exit code is not approval. Continuous production listening remains a separate task.

---

# 量化金融，从零构建 — 第38部分：做市、ETF与速度竞赛

本部分结束第六幕“市场微观结构”，连接第35部分的交易商模型、第36部分的队列重建与第37部分的执行成本。核心是分清做市账本、报价控制模型、成交记录回放及市场设计论证；任何一种结果单独都不能证明可执行的盈利业务。十一章依次讨论开场、生意核算、记录回放、触达率与模型报价、最小价位与队列、ETF、速度竞赛、高频行业、拟议第38条规则、条件狙击模型及总结题。

## 数据、核算与模型范围

五个经审计且未改动的常规原函数各执行一次并成功：`fills`、`glft`、`maker`、`deep`、`bcs`。`glft`只读取先前钉住哈希的`fills`。第六个`etf`在HYG公开数据的不可变校验处失败，错误键已写入共享拒绝表；不刷新、不重试、不使用替代历史拟合，函数也未继续读取TLT。ETF章节因此采用所引文献、机制和指定算例，没有新的HYG/TLT价格图。原金融算法、公开清单和98个受保护文件未变；没有登记策略，既有计数为本部分累计23,552、全局23,562。

成功测量使用2023年5月16、17、20日币安BTCUSDT永续公开最优报价与归集成交。100毫秒派生网格独立对照第37部分完成证据认证，原始文件仍由未改动的原校验器检查。每个函数可能使用的公开键先经审计并共享失败屏障；可能依赖不等于声称每个函数都实际读取每个键。

每秒窗口的双侧触达概率，经`-log(1-P)/dt`转换为具有相同无事件概率的齐次泊松等效速率；这不是实际队列订单成交率，也不能证明事件是泊松过程。汇总时先等权平均每日概率，再作非线性变换，不能称为平均每日强度。拟合约为A=0.2300/秒、k=0.03530/档。

GLFT假设外生布朗参考价、固定单位成交、指数条件强度、独立噪声驱动及CARA效用。代码计算长时限内点近似；一秒中点增量标准差约20.26档/根号秒，单一采样尺度的标准差不能验证扩散尺度关系。指定风险厌恶下零库存半价差约29.6、32.1、38.9、75.8档。触达拟合不验证实际成交或报价最优性。固定库存上限的精确小风险极限与内点近似不同，见第12题。

回放按前方数量、比例分配的净撤单、显示量截断及旧价位优先规则重建队列；同价成交量必须严格超过前方数量，穿价成交视作执行一单位。快速标志先看到当前100毫秒步内所有穿价成交再取消，属于事后筛选，不是测得的撤单延迟或普适速度上限。各规则筛选出的成交与库存路径不同；日终中点损益与一分钟有符号标记不同，日末时限还会被截断。手续费、资金费、可执行平仓和跨市场对冲均缺失。

5月17日慢速规则成交42,019次，日终标记均值-19.785档、一分钟标记-19.981档；快速及过滤规则日终均值为-8.700与-4.575档，成交数分别19,587及7,061。条件均值之差不是速度的因果价值。库存标准差不能说明边界占用比例。远档实验每侧每秒最多算一次触达，以窗口开始后60秒中点标记，未必是实际成交后60秒；没有排队、档位取整、库存限制、费用及平仓，跨窗口头寸重叠。30档约+1.03、45档约+19.67的毛标记及小时加总不是资本收益率，也不是所有可行策略的严格上界。

完整自融资账本为成交价相对同时中点的执行边际、返佣及持仓随中点变化的收益。以主动方符号ε定义不利标记`ε(M_h-M_fill)`，指定时限边际只能减这项一次；不能再从已包含同一价格变化的库存账本中扣一次。以成交价计算的做市方有符号标记已经包含入场边际。

BCS说明模型假设至少两家等速企业、正且独立的到达率、无信息单位投资者、随机串行优先及无摩擦压价。净中点变化不是识别出的公共新闻，归集成交也不是识别出的无信息单位订单。代入经验幅度得0.332档，只是代理模型算例，不是实际自然价差估计或回放亏损归因。原批量标志直接删除陈旧执行，数值间隔未被使用；它不模拟延迟、新均衡或福利。统一相位暴露近似及二元投资博弈另有假设。

ETF净值为资产标记减负债再除以份额。套利取决于可执行篮子价值、申赎条款、资金与结算，而不是围绕公布净值的无条件硬界。跨期跌幅不同于同时点折价；仅收盘价既不能计算净值折价，也不能识别公告因果效果。2020年3月23日SMCCF最初规定投资级公司债ETF，4月9日才扩展至高收益ETF。杠杆基金无资金流、无融资费用的算例中，再平衡量为`L(L-1)rA0`，A0是日初资产；三倍杠杆在标的下跌5%后卖出日初资产30%的敞口，而非日末资产30%。第38条是拟议研究标准，没有进行实盘、扩容或部署审批。

## 六个桌面问题

1. 利润如何核算？使用一个一致的标记财富账本；时限边际是另一种观察，不能重复扣标记。净利润还需费用、资金与平仓。
2. 为什么倾斜库存报价？在指定GLFT近似中，持多使买距增加、卖距减少；风险也改变零库存宽度，边界和模型假设不可省略。
3. 触达率说明什么？阈值频率与等效速率，不是队列成交、价格独立性或可执行最优报价。
4. 被价位约束的价差改变什么？竞争可能转向优先或数量；条件回放差异不是因果优先定价或总租金。
5. ETF靠什么贴近篮子价值？按可执行价格申赎并计全部成本与约束；陈旧公布净值可能无法兑现。
6. 狙击根证明什么？指定等速角色模型下的唯一无差异价差；行业收入、纯狙击者转移、资源支出和福利分别核算。

## 十二道题与完整解答

前六道基础，随后四道进阶，最后两道资格考级；题面与三张放大的屏幕页一致。

1. **一致边际。** 入场边际+0.5档、返佣+0.2、不利主动方向中点变动+0.9，时限标记边际`0.5+0.2-0.9=-0.2档/次成交`。做市方有符号标记与主动方不利标记符号相反。若库存账本已包含同一价格变动，不能另扣0.9；其他费用和风险仍缺失。

2. **AS近似。** γ=0.1、剩余价格方差4、k=1.5、q=2，总价差`γ方差+(2/γ)log(1+γ/k)=0.4+20log(16/15)=1.6907704`价格单位，保留价偏移`-qγ方差=-0.8`。风险厌恶、单位订单及价格的量纲须一致；结论依赖指定布朗/CARA/指数到达近似。

3. **先转换概率。** 一秒触达概率0.30与0.05给`λ1=-log(0.70)=0.35667494/秒`、`λ45=-log(0.95)=0.05129329/秒`。两点指数拟合`k=log(λ1/λ45)/44≈0.0441/档`，速率减半距离`log(2)/k≈15.7档`，`A=λ1 exp(k)`。直接拟合概率比会得到不同参数，不能回答本题；等效转换也不证明实际排队成交或泊松过程。

4. **选定回放损失。** 慢速`20×40,000=800,000`档单位，事后快速`9×20,000=180,000`，相差620,000档单位；一单位为1 BTC且每档0.10美元时为62,000美元。成交筛选、笔数和库存路径均变，不能称为实测延迟的因果价值、普适上界或可执行利润预测。

5. **价位加成。** 固定中点、无费用及逆向选择时，完整往返的全价差加成为`1-0.3=0.7美分/单位`，对称每侧0.35美分。时间优先和按量分配改变成交机会；实际预期租金还需成交、信息、资本、撤单及成本，不能仅由0.7识别净盈利或领取者。

6. **可执行赎回。** 80美元买入，篮子毛卖价84，成本`84×2%=1.68`，净82.32，赚2.32美元/份，即80的2.9%，未计其他成本。若可执行毛卖价仅79，即使公布净值84，净价`79×0.98=77.42`，亏2.58美元。融资、申赎费、结算、篮子差异和价格风险还可改变结果；公布净值不是锁定套利。

7. **随机优先与租金。** 限有利可狙击的陈旧报价，N个等概率首消息中撤单赢1/N，每个纯狙击者赢1/N，至少一家狙击赢`(N-1)/N`；N=5为4/5，N=10为9/10。角色根处每家预期利润`π*=λIh*/N`，行业共`λIh*`，N-1个纯狙击者合计仅占其`(N-1)/N`。跳跃收益由提供者转给狙击者，在行业合计内抵消。

8. **不同幅度同一根。** 到达率10和2、幅度3，`h=2×3/(10+2)=0.5档`。等概率1和5都超过假设根h<1，因此`10h=2[(1-h)+(5-h)]/2=6-2h`，仍得0.5，满足分支条件。正部函数在该支持上线性，所以此均值保持扩散不改变根；凸序比较可以不严格，较大方差本身不足。

9. **暴露不是价差比。** 新闻相位均匀、确定更新延迟5微秒、批长50毫秒，`u=δ/τ=10^-4`是末端未保护暴露比例，尚未乘竞争者胜出概率。额外保持原条件竞赛和角色结构，以`uλJ`替代机会率，可得`h_u=λJuJ/(λI+λJu)`。因此`h_u/h_1=u(λI+λJ)/(λI+λJu)`，到达率10和2时约0.0001199976，不是0.0001。均匀相位、固定延迟、无其他陈旧暴露及不变竞争都是额外假设，原批量标志没有检验。

10. **四家投资博弈。** 固定正奖池R、二元速度选择、正成本c；有快者时只有快者平分，均慢时各R/4。快对手数为0，投资增益`3R/4-c`；有1、2、3个快对手，增益依次`R/2-c`、`R/3-c`、`R/4-c`。所以`0<c<R/4`给严格占优；等号时最后一种无差异，不再严格。全投各得R/4-c，比全慢各少c，资源总成本4c。必须先给这些奖池规则，不能由“一点速度优势能赢”直接推出。

11. **资格题：可积随机幅度。** 设U非负、`0<EU<∞`、λI与λJ正、N≥2。定义`B(h)=λJ E[(U-h)+]`。等速单位订单角色模型中`πL=λIh-(N-1)B/N`、每个`πS=B/N`。连续压价及角色切换要求候选无差异`Φ(h)=λIh-B(h)=0`，N抵消；这里只刻画指定角色模型，不是所有市场博弈。

    正部对h是1-Lipschitz，故B有限、连续、非增；`Φ(0)=-λJEU<0`，且`B(h)≤λJEU`使Φ趋于正无穷。介值定理给根；h2>h1时`Φ(h2)-Φ(h1)≥λI(h2-h1)>0`，故唯一。常幅度时得到第8题公式。零幅度或零到达率的边界情况不在题设内。

    若`U1≤cx U2`且有限同均值，因为`(u-h)+`对u凸，每个h均有B1≤B2。在h1处Φ2≤0，Φ2严格增说明h2≥h1；均值相同且方差更大并不保证凸序。第8题展示可相等。根处B=λIh，各角色B/N，行业B，纯狙击者合计`(N-1)B/N`。投资者支付是行业转移收入，不自动等于相同数额的社会无谓损失；资源支出及参与效应另需分析。

12. **资格题：有限上限精确HJB与内点近似。** 参考价`dS=σdW`，整数库存q=-Q,...,Q、Q≥1，单位成交，买距δb=S-b、卖距δa=a-S，强度`Ae^-kδ`，A、k、γ正，成交噪声驱动与W独立，控制可预见且可容许。库存端点删去不允许的一侧，终值效用`-exp[-γ(x+qS)]`、无额外平仓惩罚。HJB为

    `0=u_t+(σ²/2)u_SS+sup_b Ae^-kδb[u(t,x-S+δb,q+1,S)-u]+sup_a Ae^-kδa[u(t,x+S+δa,q-1,S)-u]`。

    令`u=-exp[-γ(x+qS+θq(t))]`、θq(T)=0。内点一阶条件`exp[-γ(δb+θ(q+1)-θq)]=k/(k+γ)`，故`δb*=θq-θ(q+1)+log(1+γ/k)/γ`，卖方将q+1换q-1。若另加非负距离或价格网格，约束处须修正，不能直接套内点解。

    定义`a0=log(1+γ/k)/γ`、`C=A(1+γ/k)^(-k/γ)/(k+γ)`，代回得`θ'q=(γσ²/2)q²-CΣ邻居 exp[k(θ邻-θq)]`。令wq=exp(kθq)、α=kγσ²/2、η=A(1+γ/k)^(-(1+k/γ))，精确日历时间系统为`w'q=αq²wq-ηΣ邻居w邻`，wq(T)=1，端点只有一个邻居。

    用剩余时间τ=T-t则`w_τ=Bw`，B对角-αq²、邻项η。有限不可约对称Metzler矩阵的最大特征值具有严格正特征向量ψ；τ变大时w经标量归一化趋于ψ，未归一化不一定收敛。稳态买卖距分别为`log(ψq/ψ(q+1))/k+a0`与`log(ψq/ψ(q-1))/k+a0`，公因子抵消。

    在有限边界影响可忽略的内点，用`ψ(q-1)+ψ(q+1)≈2ψ+ψ''`，取高斯ψ=exp(-bq²/2)，配平q²项得b=√(α/η)，`c=b/k=√[σ²γ(1+γ/k)^(1+k/γ)/(2Ak)]`。由相邻比得`δb≈a0+(2q+1)c/2`、`δa≈a0-(2q-1)c/2`；零库存半价差a0+c/2。这才是本部分代码计算的高斯内点近似，不是有限Q精确公式。

    在该近似内γ趋零，a0→1/k、c→0。若固定有限Q，精确风险中性长时限矩阵对角零、邻项A/e，首特征向量`ψq=cos(qπ/(2Q+2))`。因此q=0精确半价差趋`1/k-log[cos(π/(2Q+2))]/k>1/k`。Q变大才消除边界修正；有限库存、长时限、小风险的极限次序不能混淆。

## 来源与复现

数学、ETF历史及监管采用上方英文区的原始论文、BIS与官方条款链接。价格跌幅没有替代重算。公开数据完整审计、拒绝键、一次执行日志及后续真实视觉观察保存在`renders/qa/quant38/`；渲染只使用已钉住的五个常规输出，不刷新或重跑失败ETF。纯库测试、指定数学算例不构成新市场试验。只有重新实际检查双语构建、最终节点表、动画表、原尺寸重点画面及标记区间后才能记录视觉完成；进程成功不等于批准，完整制作配音连续听审另列待办。

## Current visual review

Visual review is complete on source `3c0c71327f55d3eeec54b645c1616de04efe4a98`, fingerprint `e3fc43fd40dd1a8b65060adcf07aed5d93675dea0fe6a7e560347f582bef912b`. [Artifact-bound evidence](../../../docs/qa/quant38-polish-evidence.json) binds all 22 bilingual endpoint sheets, 11 English forty-frame motion sheets and 15 native frames actually inspected across eleven scenes. Exact flagged intervals and manually noticed concerns have individual observations and decisions. All 22 current bilingual construction sheets were actually reviewed; their 54 formatted fields and 16 plotted ranges agree with actual runtime values. Earlier construction rounds preserve independent exact source and mutable-output bytes at their real execution fingerprints and confer no final approval.

All 141 actual narration contexts agree across construction, bilingual endpoints and English motion: 95 manual Mandarin revisions and 46 exact unchanged English/Chinese pairs. English narration contains 8,909 words, about 53.0 minutes at 168 words per minute. Twelve complete bilingual solutions retain 6/4/2 grouping and three enlarged problem pages. The 187 additive captions preserve all 35,343 baseline values, yielding 35,530. One existing pure market-making test passes.

Six audited unchanged ordinary originals were invoked once each: five succeeded; ETF failed frozen validation of `yahoo/bars/HYG/2015-01-01_2020-12-31`. The failed output is omitted, without retry or substitute fit. The shared rejection barrier retains ten rejected keys and blocks unstarted dependents before original checking. Possible dependencies do not assert every key was read by every original. Three reused public derived grids are independently authenticated against prior provenance and current bytes. Five ordinary cache hashes are pinned, and sensitive prefixes plus ETF are rejected before cache/count access. All 98 protected files and financial algorithms remain unchanged. No original was rerun, no rejected key retried, and there was no refresh, new market trial or sealed strategy access. Existing registrations remain 23,552 through Part 38 and 23,562 globally.

The eleven-chapter silent timing preview is 65:57, with English subtitles. Eleven actual CPU speech reports cover 144 sampled lines, and the actual narrated opening lasts 220.400 seconds. Full continuous production listening and pronunciation review remain separately pending. The Fills chapter retains inspected sparse setup holds of approximately thirteen seconds for model-input headers and twenty-one seconds for experiment axes; these remain a pacing limitation.

## 当前视觉审阅

已实际审阅全部22张双语旁白节点画面表、11张英文四十帧动画表及15张原尺寸重点画面，覆盖十一个场景。每个标记区间与人工关注点均有绑定文件的观察与决定。先前诊断保留真实执行指纹、独立源文件与可变输出，不向最终画面转移批准。

全部141处实际旁白在各模式一致，含95处人工中文修订与46处双语均未改变的复用；实际核对54个格式字段和16处曲线范围。十二道题按六道基础、四道进阶、两道资格题提供完整双语解答。新增187条字幕保留原有全部35,343个值，总计35,530条。一个既有纯做市数学测试通过。

六个经审计的常规原始计算各调用一次，五个成功；ETF因HYG冻结校验失败而排除，无重试或替代拟合。三个公开派生网格经独立来源与字节哈希认证；98个受保护文件及原金融算法不变。没有新市场试验、刷新或封存策略访问。十一章静音预览为65:57，含英文字幕；十一份CPU报告检查144个句段，并实际检查配音开场。完整成片连续听审与发音审阅仍单独待办。
