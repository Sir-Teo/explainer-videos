

# Quant, Built — Part 39: Crypto and DeFi

This part connects market microstructure with automated market makers, transaction ordering, perpetual funding, collateral and stablecoin redemption. Thirteen scenes distinguish exact accounting identities, continuous-price limits, chosen simulations and descriptive market samples. The digital-assets desk is a proposed research design, without deployment or capital approval.

Current artifact-bound visual evidence is linked below; historical build claims do not establish current approval.

## Chapters and measurement scope

| Scene | Subject and evidence |
| --- | --- |
| Hook | Equal-value constant-product holding comparison; the distinct rebalancing benchmark |
| Chains | Public settlement, different venue designs, consensus, custody and liquidation |
| AMM | Fee-adjusted swaps, reserves, marginal price, arbitrage, oracles and impermanent loss |
| LVR | Common-initial-wealth benchmarks, local loss fractions and sampling sensitivity |
| Concentrated | Multiplicative ranges, local efficiency, sampled exits and a contextual bandit |
| MEV | Transaction order and bounded largest-feasible sandwich candidates |
| Perps | Settlement transfers, a premium proxy and a separate continuous-funding price model |
| Carry | Chosen funding/basis ledger, committed capital, margin liquidity and venue stresses |
| Stable | Reserve haircut accounting, USDC/USDT observations, Terra and historical legal context |
| Market | Venue segmentation, a normalized GBTC/BTC market-price ratio and turnover proxies |
| House | Proposed exposure controls and source excerpts from the unchanged library |
| Research | Continuous/discrete LVR proof, one-step moments and a stationary log-band reset model |
| Outro | Six desk questions, twelve fully solved problems in 6/4/2 grouping, forward links |

## Data access and reproducibility

Ten audited unchanged ordinary originals were each invoked once: `amm`, `lvr`, `fees`, `v3`, `rl`, `mev`, `funding`, `stable`, `etf`, `research`. All succeeded. Their exact output hashes are pinned in `common.py`; missing or changed caches fail before implicit computation. The original algorithms, every `compute.py`, and all 98 protected files remain unchanged.

`compute_carry` is excluded: its source registers a strategy, opens an envelope and records outcomes. Its cache/payload is not read, opened or scored. Hook, Carry, House and Outro use no historical carry-strategy values. The carry chapter instead states chosen accounting assumptions. Existing registrations remain 23,561 through Part 39 and 23,562 globally; they are not new work authorized by this review.

The pre-dispatch audit enumerated 494 possible immutable public keys. This closure is a list of possible dependencies, not a claim that each original read every key. Public archive checks use the unchanged checker under a persistent pre-check barrier. Ten inherited rejected keys remain barred; no refresh, failed-key retry, substitute fit, registry mutation or new market trial occurred.

Public samples include ETHUSDT minute candles in 2023; BTC/ETH spot and perpetual hourly candles with funding settlements through December 2025; USDCUSDT, USTUSDT, LUNAUSDT and FTTUSDT event samples; GBTC/IBIT Yahoo bars and BTC daily closes. These public observations are distinct from a sealed strategy experiment.

For current exact caches, run final QA from the repository root only after the relevant construction/language checks:

```bash
EXPLAINER_TTS=silent python tools/qa_series.py quant39 --cached-only --resume
EXPLAINER_TTS=silent python tools/qa_series.py quant39 --lang zh --cached-only --resume
EXPLAINER_TTS=silent python tools/qa_series.py quant39 --motion --cached-only --resume
python tools/lecture_length.py quant39 --floor 50
```

Do not run the default all-item computation: it includes the excluded carry original. The exact caches must match their approved hashes. A fresh machine needs an independently audited ordinary-only restoration under immutable-manifest checks; changing historical data is not a repair for a rejected key.

## Mathematical and empirical conventions

**Holding is a different benchmark from rebalancing.** A fee-free equal-value constant-product position has terminal value `2 sqrt(r)/(1+r)` times the value of holding its starting assets. Standard relative impermanent loss divides the terminal gap by terminal holding value. The chart's pool-minus-hold gap in initial-value units uses a different denominator.

Let `V(P)=inf_{(x,y) in C}(Px+y)` for a price-independent feasible set. It is concave. If the minimizing risky holding is unique and `V` differentiable, `V'(P)=x*(P)`. Start a self-financing benchmark at `R_0=V(P_0)` with `dR=x*(P)dP`. For a positive continuous semimartingale, sufficient local smoothness and predictable locally integrable holdings give

\[
R_t-V(P_t)=-\frac12\int_0^t V''(P_s)\,d[P]_s\ge0.
\]

For `dP=mu_t P dt+sigma_t P dW`, the entire `x*dP` term cancels, including drift. The loss is finite variation but can remain random through price/volatility. Expectation claims require true-martingale and integrability conditions. With `V=2 sqrt(kP)`, the local rate is `sigma² V/8`. Concentrated holdings give `sigma² L sqrt(P)/4` in range and zero outside. Their first derivative is continuous at range boundaries, so piecewise smooth Itô does not add a local-time term from a derivative jump. Jumps instead contribute nonnegative concavity gaps, as Problem 11 derives.

**A sum of local fractions is not an investment return.** The ETH measurement sums `loss_i/V_{i-1}`. Its comparison sums squared log increments divided by eight. Both use changing values or local increments; neither equals a compounded LP return on initial capital. Sampling omits within-step paths. Similar rounded monthly totals do not prove a continuous-price model, frequency invariance or executable profit.

**The simulator's fee ledger is specific.** `arb_pool` keeps k or L fixed, puts input fees outside the invariant and immediately values token fees in numeraire. It omits retained-fee compounding, gas, competing arbitrageurs, execution uncertainty and native protocol details. Its own fee-inclusive rebalancing shortfall can be reconciled with arbitrage profit; fee-free discrete LVR is a different denominator. Fees change trades and holdings, so general finite-sample loss invariance is not implied.

**The fee-band theorem has a different drift convention.** Write input fee `f`, exact log half-band `gamma=-log(1-f)`, and `a=sqrt(2 lambda)/sigma`. Under driftless Brownian log mispricing and independent Poisson edge resets, the stationary pre-block trade probability is `1/(1+a gamma)`. Replacing gamma by f is a small-fee approximation. The cited paper's symmetric analysis assumes zero log drift (price drift `mu=sigma²/2`), whereas the simulator uses martingale-level GBM (`mu=0`, log drift `-sigma²/2`). Fixed and Poisson clocks also differ. Its ARB comparison with continuous fee-free LVR is an asymptotic result requiring regularity, fast blocks and, when curvature at displaced edges is replaced by current curvature, a small-band approximation. Trade frequency alone does not prove the profit identity. Empirical discrepancies do not isolate fat tails as their cause.

**The refinement output is one-step moment evidence.** The unchanged original resets its RNG, rescales the same four million normal draws and keeps their number fixed for each m. It estimates the mean normalized step loss relative to `s²/8`, compared with `(1-exp(-s²/8))/(s²/8)`. It does not construct nested fixed-horizon Brownian paths or establish pathwise convergence. The original's misleading comment remains unchanged; the lecture corrects its interpretation.

**Concentration and learning.** Ranges are `[P/w,Pw]`, not symmetric plus/minus percentages. Centre efficiency is `1/(1-w^-1/2)`; local fee scaling additionally needs comparable volume and liquidity allocation. Daily sampled exits miss intraminute crossings and do not measure continuous first passage. The learner uses lagged noisy volatility buckets in a two-regime contextual bandit, an external chosen fee yield, centre efficiency, sampled in-range share, benchmark-relative LVR and reset costs. Actions do not control tomorrow's state. One seeded training run and common evaluation seeds do not quantify training uncertainty. The oracle receives regime information and extra Monte Carlo action selection. Reward is not a total executable LP return; simple 365-times reward annualization is not compounding.

**Oracle observations.** Arithmetic TWAP averages price levels; averaging log prices and exponentiating yields a geometric time average. For a fee-free fixed-product move with price ratio r>=1, reserves obey x1=x0/sqrt(r), y1=y0*sqrt(r); gross numeraire input y0*(sqrt(r)-1) is not net manipulation profit. Flash loans require atomic repayment and do not remove fees, gas, price impact, competition or oracle safeguards.

**Ordering.** Sandwich bisection finds the largest feasible front-run size inside a bound, not a separately verified profit maximum. A negative raw candidate does not prove every attack unprofitable; no-attack is an available action. Victim token shortfall valued at the initial reference differs from attack profit; their difference is not automatically fee income. Private routes and batches address some ordering incentives, without eliminating all MEV.

**Funding and carry.** The empirical premium is based on selected prior hourly closes, with candle-open timestamps, missing-observation allowances and a display filter. It is not the official impact-price premium index. A simple eight-hour rate annualization is not a financed capital return. The continuous proportional solution `F/S=kappa/(kappa-(r-q))` assumes constant coefficients, matching time units, a linear zero-value contract, `kappa>r-q` and transversality. It is separate from a discrete clamped venue rule. Matched spot/perpetual units leave basis, future funding, financing, collateral liquidity, venue and legal risks.

**Stablecoin and fund measurements.** The USDC/USDT sample begins at its observed low: the earlier fall is left-censored. The count below 0.98 is an aggregate minute count, not necessarily one spell; recovery is the first later sampled close above 0.995. The quote is in tether, not direct dollars. An 8% reserve-exposure stress does not prove a 0.92 market-price floor or a liquidity-only explanation. The haircut table repeats aggregate liquidation coverage; it does not solve the last redeemer's payoff or a run equilibrium. GBTC close divided by a BTC daily close, normalized at one base date, is not NAV discount without share entitlement, fee erosion and synchronized clocks. IBIT close times volume is a turnover proxy, not exact dollar volume or inflow.

## Primary sources and historical scope

- [Milionis, Moallemi, Roughgarden and Zhang, Automated Market Making and Loss-Versus-Rebalancing](https://arxiv.org/abs/2208.06046): concave value, rebalancing benchmark and curvature loss.
- [Milionis, Moallemi and Roughgarden, Automated Market Making and Arbitrage Profits in the Presence of Fees](https://arxiv.org/abs/2305.14604): symmetry assumptions, stationary mispricing and asymptotic profit/fee rates.
- [Flash Boys 2.0](https://arxiv.org/abs/1904.05234): 2019 preprint, 2020 conference; transaction ordering.
- [Uniswap v3 Core, March 2021](https://uniswap.org/whitepaper-v3.pdf): ranges and concentrated reserves.
- [Federal Reserve/Treasury/FDIC, 12 March 2023](https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312b.htm): SVB depositor protection, access beginning 13 March. Chronology is not causal identification of token recovery.
- [SEC order 34-99306, 10 January 2024](https://www.sec.gov/files/rules/sro/nysearca/2024/34-99306.pdf): spot Bitcoin product listing approvals; approval, conversion and first trading are distinct events.
- [SEC, Tai Mo Shan settlement, 20 December 2024](https://www.sec.gov/newsroom/press-releases/2024-212): incentivized May 2021 UST purchases and agreement to pay about $123 million, without admitting or denying findings; also records the April 2024 Terraform civil verdict.
- [MiCA Regulation 2023/1114](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng): asset-referenced/e-money provisions generally applied from 30 June 2024, with distinct provisions and transitions.
- [GENIUS Act, Public Law 119-27](https://www.congress.gov/bill/119th-congress/senate-bill/1582/text): enacted 18 July 2025. Effective date is the earlier of 18 months after enactment and 120 days after specified final implementation rules. This historical description does not certify current applicability, product eligibility or compliance.

Two guessed DOJ URLs returned 404 and are not evidence. The initial SEC press-release URL returned an unrelated Morgan Stanley release, the Circle URL redirected to a generic blog and the v2-whitepaper URL returned 404. These are retained as lookup failures, not used as evidence for the claims above. Source receipts retain response bytes and titles. Further bibliographic and frontier claims below are reading context unless specifically supported; this pass does not claim an exhaustive 2026 literature or legal update.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Harvey, Ramachandran and Santoro, *DeFi and the Future of Finance* (2021) | DEXs, lending, stablecoins, risks | 2, 5, 8 |
| Narayanan, Bonneau, Felten, Miller and Goldfeder, *Bitcoin and Cryptocurrency Technologies* (2016) | ledgers, consensus, custody | 1 |

## Papers, chapter by chapter

* ch. 1: Nakamoto (2008); Buterin (2014).
* ch. 2: Adams et al., Uniswap v2/v3 whitepapers (2020, 2021); Angeris and Chitra (2020), *ACM AFT*; Egorov (2019),
  stableswap whitepaper.
* ch. 3: Milionis, Moallemi, Roughgarden and Zhang (2022).
* ch. 4: Adams et al. (2021); Lehar and Parlour (2025), *JF* (further reading; the lecture does not rely on an unverified theorem attribution).
* ch. 5: Daian et al. (2020), *IEEE S&P*; Qin, Zhou and Gervais (2022), *IEEE S&P*.
* ch. 6: He, Manela, Ross and von Wachter (2022); Ackerer, Hugonnier and Jermann (2024) (further reading; the lecture does not rely on an unverified theorem attribution).
* ch. 7: matched-unit accounting and chosen collateral/venue stresses; no historical strategy outcome is used.
* ch. 8: Diamond and Dybvig (1983), *JPE*; Lyons and Viswanath-Natraj (2023), *J. International Money and Finance*;
  Liu, Makarov and Schoar (2023), NBER WP.
* ch. 9: Makarov and Schoar (2020), *JFE*; Liu and Tsyvinski (2021), *RFS*; Liu, Tsyvinski and Wu (2022), *JF*.
* Research: Milionis, Moallemi, Roughgarden and Zhang (2022); Milionis, Moallemi and Roughgarden (2023); Capponi and
  Jia (2021).

## Desk questions with answers

1. A fee-free constant-product doubling gives `2 sqrt(2)/3-1=-5.719%` relative to terminal holding. It does not measure the same gap as common-initial-wealth rebalancing.
2. Under the continuous assumptions above, LVR is `-1/2 integral V'' d[P]`; for constant product the local rate is `sigma²V/8`. With jumps, add concavity gaps.
3. A narrower range increases centre liquidity and curvature per dollar. Net performance also depends on price location, exits, volume, competition and costs; high volatility alone does not supply a universal trading rule.
4. Funding incentives help link perpetual and spot prices subject to constraints. The proportional continuous solution needs the separate constant-coefficient and transversality assumptions, not merely a funding payment.
5. A matched-unit carry ledger retains funding, basis, margin, custody, venue, collateral-currency, execution and legal risks. The lecture uses chosen stresses, without historical strategy outcomes.
6. A stablecoin quote alone does not identify illiquidity or insolvency. Inspect reserve valuation, other claims, redemption rights, access timing and quote currency.

## Twelve problems with complete solutions

### Basic 1–6

1. **Relative impermanent loss at ratios 4 and 1/4.** Equal-value initial holdings have terminal hold value proportional to `(1+r)/2` and pool value proportional to `sqrt(r)`. Their ratio is `2 sqrt(r)/(1+r)`. At 4, it is `4/5`; at 1/4 it is `1/1.25=4/5`. Both relative losses are `-20%`. This assumes fee-free constant product and external arbitrage, with no deposits or withdrawals.

2. **Buy 50 ETH from 1,000 ETH / $2m, no fee.** Initial `k=2e9`. Remaining token reserve is 950, so final numeraire reserve is `2e9/950=2,105,263.1579`. Gross payment is `$105,263.1579`; average price is `$2,105.2632/ETH`, or `5.2632%` above the initial marginal price. It is payment for exact output, with no fee or gas.

3. **Local LVR dollar rate.** At current value $10m and annual sigma 0.8, `sigma²V/8=$800,000/year`; dividing by 365 gives `$2,191.7808/calendar day`. The local normalized annual rate is 8%. These are instantaneous-rate conversions at the specified current value and constant sigma. Future V changes, so this is not a realized annual dollar loss or investment return.

4. **One discrete doubling and quadratic variation.** With price ratio `u=2`, the exact gap is `Delta LVR/V0=(sqrt(2)-1)²/2=(3-2sqrt(2))/2=0.08578644`. A smooth deterministic path can double with zero quadratic variation, while a volatile path can have the same endpoint and positive quadratic variation. Thus a doubling alone does not specify a continuous-rate estimate. The plug-in `(log 2)²/8=0.06005663` is a one-increment statistic, not identified quadratic variation of the unobserved path.

5. **Multiplicative range w=1.21.** At the geometric centre, concentrated value is `2L sqrt(P)(1-1/sqrt(w))`, compared with `2L sqrt(P)` for equal full-range liquidity. Efficiency is `1/(1-1/1.1)=11`. At that centre and equal capital, the local in-range LVR rate is 11 times the full-range rate. Real fee income and whole-path performance require additional assumptions; below/above the range the curvature vanishes in this model.

6. **Exact log band and probability.** There are `lambda=86400/12=7200` mean blocks/day. Sigma is `0.05/sqrt(day)`. Input fee `f=.003` gives `gamma=-log(.997)=.00300450902`. Then `a=sqrt(14400)/.05=2400`, `eta=a gamma=7.21082165` and `P_trade=1/(1+eta)=0.12179049`. Replacing gamma by f gives eta 7.2 and probability 0.12195122. The exact expression here refers to stationary driftless log Brownian mispricing with independent Poisson resets, not actual Ethereum or the martingale-level simulator.

### Advanced 7–10

7. **Simple carry return under chosen constants.** Let spot and perpetual start at 100, one unit held throughout, funding notional fixed at 100, funding `.0001` per settlement, three settlements/day, no basis movement, financing, fees or default. Annual funding is `100*.0001*3*365=10.95`. Committed capital is `100+100/3=133.3333`; simple annual return is `10.95/133.3333=8.2125%`. It is not compounded. A buffer raises capital; changing notionals, rates and costs change the answer.

8. **Continuous perpetual premium.** Match units: kappa `3/day=1095/year`, `a=r-q=.05/year`. With constant coefficients, pricing-measure spot drift a, zero-value linear gains and the no-bubble/transversality condition, drift balance for `F=cS` gives `c a=kappa(c-1)`, so `c=1095/1094.95`. Premium is `.05/1094.95=.00004566419`, or `.4566419 bp`. The positivity condition `kappa>a` holds. Without the transversality condition this algebra does not establish uniqueness among arbitrary bubble solutions.

9. **Fully specified venue-failure payoffs.** If the one-year simple return is +.10 when no failure occurs and -.25 if failure occurs, then `E R=(1-p).10-p.25=.10-.35p`; zero mean gives `p=2/7=28.5714%`. Under an alternative model that earns +.10 even in a failure year and then loses .25, the expression is `.10-.25p` and the answer is 40%. These are different payoffs. If failure instead gives -1 under the original survival-only specification, the break-even p is `.10/1.10=9.0909%`, not 10%. No probability of any actual venue is inferred.

10. **Chosen liquidation coverage and service.** With .70 liquid and .30 liquidated at .70 of par, aggregate proceeds are `.70+.30*.70=.91` per token. Add the explicit mechanism that all assets are liquidated up front, no other claims/costs exist, and unit tokens are paid par in a fixed sequence until proceeds run out. The first 91% of token claims are paid fully and the last 9% receive zero (with a fractional marginal claim if indivisibility matters). This allocation is not the unchanged original's `last_get` field, which repeats aggregate coverage. Accounting does not prove a run equilibrium: preferences, beliefs, timing and actions are still missing.

### Qualifying 11–12

11. **Continuous LVR, boundaries, a discrete step and jumps.** Take a price-independent feasible set C. Its infimum of affine functions is concave. Under attainment, a unique minimizing risky holding and differentiability, the envelope theorem gives `V'=x*`; under local C² regularity `V''=x*'<=0`. Let P be a positive continuous semimartingale and x*(P) predictable and locally P-integrable. Define `R0=V(P0)` and `R=R0+integral x*(P)dP`. Local Itô gives `dV=x*dP+.5 V'' d[P]`, hence `R-V=-.5 integral V'' d[P]>=0`. A drift in P cancels with the entire x*dP term. This is a pathwise identity; turning local stochastic integrals into zero-mean true martingales requires additional integrability.

    For constant product, `V=2 sqrt(kP)`, `x*=sqrt(k/P)` and `V''=-sqrt(k)/(2P^(3/2))`; under `d[P]=sigma²P²dt`, the rate is `sigma² sqrt(kP)/4=sigma²V/8`. In a concentrated range, `x*=L(P^-1/2-pb^-1/2)`, so its derivative is `-L/(2P^(3/2))` in range, zero outside; the rate is `sigma²L sqrt(P)/4` inside. V' is continuous at both boundaries and locally absolutely continuous, allowing the piecewise smooth Itô extension without derivative-jump local time.

    For one fee-free step, write u=P1/P0. The benchmark gain is `x0(P1-P0)=V0(u-1)/2`; pool change is `V0(sqrt(u)-1)`. Their difference is `V0(u+1-2sqrt(u))/2=V0(sqrt(u)-1)²/2`. If conditionally `log u ~ N(-v/2,v)` with v=sigma²dt, then `E u=1` and `E sqrt(u)=exp(-v/8)`, giving `E[gap|F0]=V0(1-exp(-v/8))`. Dividing by dt and letting dt shrink recovers the local rate. The expectation condition is not supplied by a single observed endpoint.

    For a positive càdlàg semimartingale, under sufficient Itô-with-jumps regularity and left-limit predictable holdings, add
    `sum_s [V(Ps-)+V'(Ps-)*Delta Ps - V(Ps)]` to `-.5 integral V'' d[P]^c`. Concavity makes each bracket nonnegative. The purely continuous variance integral alone therefore misses jump losses. Feasible trading, fees and delayed arbitrage would require a different model.

12. **Stationary edge-reset model and limits.** Let z follow `dz=sigma dW` between independent Poisson times of rate lambda, and reset to `sgn(z) gamma` when a block sees `|z|>gamma`; otherwise do nothing. Assume sigma,lambda,gamma>0 and stationarity/ergodicity. Write density rho. Inside the band, the stationary adjoint equation is `.5 sigma²rho''=0`; symmetry and zero interior probability current imply constant c. Outside, `.5 sigma²rho''-lambda rho=0`; integrable tails are `c exp[-a(|z|-gamma)]`, where `a=sqrt(2lambda)/sigma`, continuous at both edges.

    At +gamma, reset inflow is `lambda integral_gamma^infinity rho dz=lambda c/a`. The derivative jump is `rho'(gamma+)-rho'(gamma-)=-ac`; integrating the adjoint equation across the edge gives `.5 sigma²(-ac)+lambda c/a=0`, because `a²=2lambda/sigma²`. The negative edge is symmetric. Finite Brownian diffusion spends zero calendar time at an individual edge, so no stationary atom is needed. Normalization gives `2gamma c+2c/a=1`. Independent Poisson arrivals see the stationary pre-arrival distribution, hence `P_trade=2c/a=1/(1+a gamma)`.

    For proportional input fee f, exact symmetric log half-band is `gamma=-log(1-f)`, with `gamma=f+O(f²)`. The simple probability is exact for the stated driftless-log reset model, not for arbitrary price drift or fixed blocks. At fixed positive lambda, `gamma down to 0` gives probability 1. At fixed positive gamma, `lambda to infinity` gives probability asymptotic to `sigma/(gamma sqrt(2lambda))`, tending to 0. These are probability limits. Claims that arbitrage profit vanishes or fees recover a fee-free reference require the separate profit formulas, demand-curve growth bounds and asymptotic regime; they do not follow from P_trade alone. Taking gamma to zero and lambda to infinity jointly can yield different limits according to gamma*sqrt(lambda).

# 第39部分：加密货币与去中心化金融

本部分区分精确记账恒等式、连续价格极限、指定模拟和市场描述。十三个场景覆盖链与交易场所、自动做市、再平衡基准损失、集中流动性、交易排序、永续资金费、基差与保证金、稳定币、基金及研究证明。数字资产交易台是研究提案，不代表部署或资本批准。当前科学修订尚需新的双语构建与最终视觉审阅，历史构建记录不构成当前批准。

## 数据与复现边界

十个获准的常规原始计算各调用一次且均成功：amm、lvr、fees、v3、rl、mev、funding、stable、etf、research。common.py 固定成功输出的字节哈希；缺失或变化的缓存不能触发隐式重算。所有 compute.py、金融算法及98个受保护文件保持原样。carry 原始计算会登记策略、打开封存样本并记录结果，因此被排除；不读取其缓存或载荷，不打开或评分。开场、交易台、结尾不使用历史套利策略收益。

本次没有刷新数据、重试已拒绝的不可变键、替代历史拟合、登记试验或改变注册表。第39部分累计计数仍为23,561，全局为23,562。494个可能公开数据键是依赖闭包，不表示每个原始计算都读过全部键。十个继承的拒绝键继续禁止。上述英文命令只检查精确已批准缓存；默认全项目计算包含被排除的 carry，不应运行。

## 定义与研究假设

持有初始资产与自融资再平衡是不同基准。标准无常损失以期末持有组合价值作分母；以初始价值为单位画出的“池减持有”差额不是同一个百分比。令 `V(P)=inf_C(Px+y)`，可行集不依赖价格，则 V 凹。若最小点唯一且 V 可微，包络定理给出 `V'=x*`。从共同初值 `R0=V(P0)` 出发，定义 `dR=x*dP`。对正连续半鞅、局部光滑价值函数及可预测、局部可积持仓，

`R_t-V(P_t)=-1/2 integral V''(P_s)d[P]_s >=0`。

价格漂移随整个 `x*dP` 项消去；剩余过程有限变差，但不必确定。取期望还需真鞅及可积条件。常数乘积池的局部速率是 `sigma²V/8`；集中仓位区间内为 `sigma²L sqrt(P)/4`，区间外为零。边界一阶导数连续，没有导数跳跃产生的额外局部时项。价格跳跃要另加凹性差额。

ETH结果累加每一步损失除以当步初始池价值，是分母变化的局部损失比率之和，不是初始资本总收益。平方对数增量除以八是小步长比较；相近的四舍五入结果不证明连续价格模型、频率不变性或可执行利润。

费用模拟保持 k 或 L 不变，费用放在曲线外，输入代币费用即时按计价货币估值。原生池内费用复投、gas、竞争、执行不确定性均未建模。含费模拟自己的再平衡缺口与套利利润可作记账核对；无费离散损失是另一个分母，不能推出有限样本损失不变。

费用带证明假设对数价格无漂移、独立泊松出块和边缘重置。输入费率 f 的精确对数半带宽为 `gamma=-log(1-f)`；用 f 代替 gamma 是小费用近似。对称论文模型的价格漂移为 `sigma²/2`，使对数漂移为零；模拟却用价格水平为鞅的GBM，对数漂移为 `-sigma²/2`。固定时钟也不同于泊松时钟。利润与无费连续损失的比较是另需正则性、快速出块及相应小带宽近似的渐近关系；交易概率本身不能证明利润恒等式。真实样本残差不单独识别厚尾成因。

所谓细化输出实际上每次重置随机数发生器，重新缩放相同四百万个标准正态数，每组数量不变；它比较单步矩，不是固定期限嵌套布朗路径。区间是 `[P/w,Pw]`，不是对称正负百分比。局部中心效率不保证全程收益。分钟观测的出界天数漏掉分钟内穿越。学习器是滞后波动桶状态的上下文赌博机，奖励依赖指定费用收入、活跃比例、基准相对损失与重置成本，不是完整LP投资回报。单个训练种子不能量化训练不确定性，预知状态的比较对象还使用额外模拟预算。

夹子攻击的二分法寻找有上界的最大可行抢跑规模，未单独验证利润最优。负候选值不证明所有攻击都亏损；不攻击始终是可选行动。受害者按初始参考价估值的代币缺口与攻击利润口径不同，其差不是自动等于手续费。

永续合约的小时收盘价溢价代理不是官方冲击价格指数；简单年化资金费不是投入资本收益。连续比例价格公式要求常系数、时间单位一致、线性零价值合约、`kappa>r-q`及排除泡沫的横截条件，与离散限幅规则分开。匹配单位仍有基差、未来资金费、融资、抵押品流动性、交易场所与法律风险。

USDC/USDT样本起点就是样本低点，早期下跌被左截断；低于0.98的分钟数是累计量，不一定连续；恢复是之后第一次收盘价超过0.995。USDT报价不是直接美元赎回价值。8%储备暴露的算术不证明0.92价格下界或纯流动性解释。清算表不是末位赎回者收益或挤兑均衡。GBTC/BTC归一化市价比缺少每份币权、费用侵蚀和同步时钟，不能称净值折价；IBIT收盘价乘成交量是成交金额代理，不是精确金额或净流入。

预言机还须区分算术时间均价与对数平均后的几何均价。无费固定乘积价格乘r时，储备为x0/根号r及y0根号r；总输入不是操纵净利润。闪电贷需原子偿还，不消除费用、gas、冲击、竞争或预言机保护。

## 交易台六问

1. 无费常数乘积池价格翻倍，相对期末持有价值落后5.719%；再平衡损失回答另一问题。
2. 连续再平衡损失是 `-1/2 integral V'' d[P]`；常数乘积局部速率为 `sigma²V/8`，跳跃另加凹性缺口。
3. 缩窄区间放大局部曲率；成交量、竞争、出界、重置及对冲成本会改变净表现。
4. 资金费激励联系永续与现货，但比例连续价格解需要单独假设与横截条件。
5. 匹配单位不能消除基差、资金费、保证金、托管、稳定币、执行与场所风险。
6. 单个稳定币报价不能识别偿付能力或流动性，应审查储备、其他请求权、赎回权、时间及计价币。

## 十二道题及完整解答

### 基础题1–6

1. **价格比4与1/4的相对无常损失。** 初始等价值资产的持有终值正比于 `(1+r)/2`，池终值正比于 `sqrt(r)`，比例为 `2sqrt(r)/(1+r)`。r=4时为4/5；r=1/4时也为4/5，因此均为-20%。假设无费用、外部套利、没有新增或撤回流动性。

2. **买出50 ETH的精确付款。** 初始储备1000 ETH与200万美元，k=20亿。剩950 ETH，计价币储备变为 `20亿/950=2,105,263.1579`。付款105,263.1579美元，平均2105.2632美元/ETH，比初始边际价格高5.2632%。没有手续费或gas。

3. **局部美元损失速率。** 当前价值1000万美元、年波动率0.8，局部速率为 `.64*1000万/8=80万美元/年`，除以365得2191.7808美元/日；局部归一化速率为8%/年。未来池价值变化，因此不是全年实际美元损失或投资回报。

4. **单步翻倍与二次变差。** 精确比率为 `(sqrt(2)-1)²/2=(3-2sqrt(2))/2=.08578644`。光滑确定路径可以翻倍但二次变差为零；另一波动路径可同终点而二次变差为正。单一翻倍不能确定连续公式中的方差。代入 `(log2)²/8=.06005663`只是单增量统计量，不是未观测路径二次变差。

5. **w=1.21的中心效率。** 集中价值为 `2Lsqrt(P)(1-1/sqrt(w))`；同L全区间为 `2Lsqrt(P)`。资本效率 `1/(1-1/1.1)=11`。中心、等资本、区间内的局部损失速率放大11倍；全程费用与收益仍需额外条件，区间外曲率为零。

6. **费用带与交易概率。** 平均12秒一块，对应每天lambda=7200。sigma=.05/平方根日；f=.003，精确gamma=`-log(.997)=.00300450902`。a=`sqrt14400/.05=2400`，eta=7.21082165，概率=.12179049。以f近似gamma时eta=7.2、概率=.12195122。精确性限于平稳、对数无漂移、泊松边缘重置模型，不适用于任意真实链或水平鞅模拟。

### 进阶题7–10

7. **指定常资金费与资本口径。** 现货与永续各100、保持一单位，结算名义额固定100，费率每8小时.0001，每天三次，无基差、融资、费用或违约。年收入 `100*.0001*3*365=10.95`。资本 `100+100/3=133.3333`，简单年收益8.2125%，不复利。额外缓冲、名义额或费率变化会改变结果。

8. **连续永续溢价。** kappa=3/日=1095/年，a=r-q=.05/年。在定系数、定价测度漂移a、零价值线性收益与无泡沫横截条件下，设F=cS，漂移平衡 `ca=kappa(c-1)`，故c=1095/1094.95。溢价 `.05/1094.95=.00004566419`，即.4566419基点。kappa>a成立；单凭代数并不能排除任意泡沫解。

9. **明确场所失败支付后再求概率。** 若一年不失败收益+.10，失败收益-.25，则期望 `.10(1-p)-.25p=.10-.35p`，零期望给p=2/7=28.5714%。若失败年也先赚+.10再损失.25，则变为 `.10-.25p`，答案40%；它是另一个支付模型。若原模型失败收益改为-1，则p=.10/1.10=9.0909%，不是10%。不推断任何实际场所失败概率。

10. **指定清算与顺序偿付。** .70流动资产按面值、.30资产折价30%，总回收 `.70+.30*.70=.91`。再明确：全部资产预先清算、无其他索取或成本，按固定顺序每份足额支付直到款项用完。前91%份额全额、后9%为零；不可分份额可有一个边际部分支付。该结果不是原始计算中重复总覆盖率的last_get字段。缺少偏好、信念、时间和行动，不能据此证明挤兑均衡。

### 资格题11–12

11. **连续LVR、边界、单步与跳跃。** 价格独立可行集上的仿射函数下确界V是凹函数；若最小点存在唯一且可微，包络定理给 `V'=x*`；局部C²时 `V''=x*'<=0`。P为正连续半鞅，持仓可预测且局部可积。令共同初值 `R0=V(P0)`，`R=R0+integral x*dP`。局部Itô给 `dV=x*dP+.5V''d[P]`，相减得到非负 `R-V=-.5integral V''d[P]`。整个x*dP包含的漂移也消去；这是逐路径恒等式，期望为零的随机积分还需真鞅及可积条件。

    常数乘积：V=2sqrt(kP)，x*=sqrt(k/P)，`V''=-sqrt(k)/(2P^(3/2))`，代入 `d[P]=sigma²P²dt` 得速率 `sigma²sqrt(kP)/4=sigma²V/8`。集中仓位区间内 `x*=L(P^-1/2-pb^-1/2)`，导数 `-L/(2P^(3/2))`，区间外为零，故区间内速率 `sigma²Lsqrt(P)/4`。一阶导数边界连续且局部绝对连续，分段光滑Itô无需导数跳跃局部时项。

    单步令u=P1/P0，再平衡收益为 `V0(u-1)/2`，池价值变化 `V0(sqrt(u)-1)`，差为 `V0(sqrt(u)-1)²/2`。若条件 `log u~N(-v/2,v)`，v=sigma²dt，则Eu=1、Esqrt(u)=exp(-v/8)，所以条件期望 `V0(1-exp(-v/8))`；除以dt并缩小时段得到局部连续速率，单个终点不提供该分布假设。

    若P为正的右连续有左极限半鞅，在足够的含跳Itô正则性和左极限可预测持仓下，除连续部分 `-.5integral V''d[P]^c` 外加 `sum[V(Ps-)+V'(Ps-)*DeltaPs-V(Ps)]`。每项由凹性非负。仅连续方差积分遗漏跳跃损失；费用、延迟套利和交易可行性需改模型。

12. **平稳边缘重置密度。** 在独立泊松率lambda的块之间，z满足 `dz=sigma dW`，遇块且|z|>gamma则重置到对应±gamma，否则不动。sigma、lambda、gamma均正，假设平稳遍历。带内平稳伴随方程 `.5sigma²rho''=0`，对称性与零内概率流给常数c；带外 `.5sigma²rho''-lambda rho=0`，可积尾为 `c exp[-a(|z|-gamma)]`，a=sqrt(2lambda)/sigma，边界密度连续。

    正边界重置流入 `lambda integral_gamma^infty rho=lambda c/a`，导数跳跃为-ac。跨边界积分方程给 `.5sigma²(-ac)+lambda c/a=0`，因为a²=2lambda/sigma²；负边界对称。布朗扩散在单一点的日历占用时间为零，无需平稳原子。归一化 `2gamma c+2c/a=1`。独立泊松到达看到到达前平稳时间分布，因此概率 `2c/a=1/(1+a gamma)`。

    输入费用f对应精确对数带宽gamma=-log(1-f)=f+O(f²)。公式精确性属于此无对数漂移模型，不属于任意漂移或固定块。固定lambda、gamma趋零时概率趋1；固定gamma、lambda趋无穷时概率渐近sigma/(gamma sqrt(2lambda))趋零。这只是概率极限，利润趋零或费用回收参考损失还需单独利润公式、需求曲线增长界及渐近条件。若共同取极限，结果取决于gamma*sqrt(lambda)的路径。

## 原始资料与法律日期

英文资料表链接到已核对的LVR与费用论文、Flash Boys 2.0、Uniswap v3白皮书、美联储2023年3月12日声明、SEC2024年1月10日批准令、MiCA和GENIUS法案正文。GENIUS于2025年7月18日成法；生效日是成法18个月后与指定最终规则公布120天后的较早者，不能把成法与全面适用混为一谈。MiCA稳定币条款一般自2024年6月30日适用，其他条款及过渡另有安排。本段不认证当前合规、保险、产品资格或穷尽2026年前沿。失败或误指向的资料查找不作为论据。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part39.md`](../../../docs/qa/quant/part39.md).*
