

# Quant, Built — Part 34: Inside a Quant Firm

Part 34 of the [43-part series](../README.md), following the [syllabus](../SYLLABUS.md) and [reading map](../READING.md). This lesson studies business models, fees, risk, technology, surveillance, interviews and drawdown stops. Firm histories and legal cases are attributed historical accounts, not verification of current statistics or legal outcomes. The House chart and Rule 34 describe a proposed responsibility and review checklist; they do not implement a live trading or compliance system or approve a strategy.

The fourteen scenes cover the opening, six business models, disclosures, pods, research review, risk, technology, compliance, interviews, founding histories, factor-stop research, the proposed firm checklist, Brownian drawdown mathematics and the recap. English and Chinese share the same calculations. Eleven chapter questions have central working setups. The problem set has six basic, four advanced and two qualifying problems, with complete bilingual solutions below.

## Evidence and computation boundaries

Five unchanged ordinary calculations (`virtu`, `theory`, `power`, `platform`, `stops`) were each restored successfully once under an audited public-input barrier. The two French monthly source keys were verified without refresh; the factor calculation subsequently masks to December 2020. The `house` calculation is excluded: it would read sealed strategy outcomes and regress them against research results. Presentation loading rejects `house`, `envelope`, `track` and `holdout` prefixes before cache access, permits only the five ordinary names, and verifies their restored cache hashes. Missing or changed caches fail closed. Rendering cannot restore them automatically.

No financial algorithm, protected registry, sealed strategy payload or stored holdout result is changed or consulted. This review adds no market trials. Unchanged registration metadata contains **23,552 trials through Part 34**, and **23,562 globally**. Trial count is not an effective independent test count. Historical research comparisons are dependent and selected; their existence is not deployment approval.

Public source closures, actual original invocations and hash checks are recorded in the Part 34 QA evidence. Presentation approvals require fresh bilingual construction, actual image inspection, final motion review and audio checks against the final included source. A diagnostic pass or CPU speech sample does not certify pronunciation or full continuous production listening.

## Calculations, definitions and limits

* **Disclosed loss frequency:** a Gaussian daily model maps one loss in 1,238 to daily mean/standard deviation **3.1531**. Multiplication by √252 gives **50.0538** only under the time-independence and stable-variance assumptions. The original one-sided 95% binomial upper loss-probability bound is **0.0038261**, implying **2.6670 daily / 42.3380 annualized** under the same models. Specified finite-variance t(4) and t(3) location-scale alternatives give **5.3676** and **6.3420** daily. These three families do not establish a universal bound. Stipulate +1 with probability 1237/1238 and −2000 otherwise: the same loss probability has negative mean. A count alone identifies neither return magnitudes, ratio nor skill.
* **Independent trade aggregation:** for equal-risk independent trades, s=r√N. The cached 20,000-day Gaussian illustrations use per-trade ratio 0.01; their empirical loss frequencies have sampling error. An even-money coin with that ratio has win probability `(1+0.01/sqrt(1+0.01²))/2 ≈ 50.5%`. Positive net covariance increases variance at fixed marginal risk; negative covariance can reduce it. Counting trades does not measure independence or capacity.
* **Fees:** the stipulated positive-profit single-period rule is `(g−m)(1−p)`. At g=66%, m=5%, p=44%, it gives **34.16%**. It does not reconcile reported historical 66%/39% averages: annual data, fee history, bases, high-water marks and timing are required. With constant affine positive-profit fees, averaging commutes with the formula. Historical quotations remain attributed rather than newly validated.
* **Platform simulation:** 200 slots, 30 years, eight seeds, monthly arithmetic profit, chosen correlation 0.1, either latent skill N(0.5,0.5²) or constant 0.5. Stops act after the month's return, hiring is immediate and free, and new skill draws are independent. Firing resets running state **and the calendar-year payout accumulator**. Positive-year bonuses have no high-water mark or clawback; exposure restores at year end. The heterogeneous 5%-volatility investor ratios are **1.8951 with stops / 1.1872 without**; identical skill gives **1.3011 / 1.2334**, not a small cost from stopping. Selection, exposure, replacement and compensation all change. Displayed seed uncertainty is population-normalized across-seed SD/√8, not paired-difference uncertainty or a market confidence interval. Ratios of aggregate rows need not equal averages of run-level ratios.
* **Review and ramp:** information availability must precede positions and executable prices. Reconstruct every cash, funding, borrow, fee and impact leg. The chosen prior N(0,0.5²) and Gaussian likelihood variance 1/T give shrink weights 0.2, 0.5 and 0.7143 after 1, 4 and 10 years. The likelihood is an iid low-Sharpe approximation. A posterior mean is not a complete allocation policy; covariance, risk, financing, selection, objectives and constraints remain separate.
* **Liquidity:** a $50m position, $20m daily volume and 10% participation take **25 trading days**. The stipulated daily clip model `c=Y σ sqrt(q)`, with Y=1 and daily σ=2%, gives **63.2456 bp**. Interpreting it across many days needs impact-reset assumptions. It is not calibrated total block impact. Fixed participation and fixed child size imply different crisis comparisons.
* **Technology and surveillance:** the chosen 1,185 km route implies roughly **3.95 ms in vacuum / 5.81 ms in fibre** before route length, equipment and queuing. Speed value requires an opportunity and competition model. High cancellation alone does not establish spoofing: order placement, size, cancellation, opposite-side fills, communications and context require investigation. SEBI's July 2025 interim allegations and contemporary reports are a dated contested record, without a claimed current outcome. The Knight control discussion is a design rationale, not a proven counterfactual prevention guarantee.
* **Factor stops:** six factors × six rules reuse July 1966–December 2020 research observations. Thirty-six prior finite observations scale volatility; removing missing values can compress time, and leverage is uncapped. `apply_stop` uses arithmetic cumulative return drawdown, includes the full breach return, skips exactly the next wait observations with zero cash return and resets the peak. It differs from compounded-wealth drawdown. Costs, funding and execution are absent. At 15%/12 observations out, HML changes **0.1997→0.2752** and UMD **0.6034→0.5576**. Two hundred shuffles per rule give descriptive reference means and SDs. Stars beyond two shuffle SDs are not calibrated or selection-adjusted p-values, causal evidence or a universal stop rule.
* **Brownian stops:** Xₜ=μt+σWₜ is arithmetic cumulative profit, X₀=0, μ known real, σ>0 and d>0, with continuous monitoring and Mₜ=max₀≤s≤t Xₛ. S=μ/σ has units time⁻¹ᐟ² and δ=d/σ time¹ᐟ². The dimensionless shape a=2Sδ does not determine the absolute time scale alone. For μ≠0,

  `Eτ = σ²(eᵃ−1−a)/(2μ²) = (e²ˢᵟ−1−2Sδ)/(2S²)`,

  `Mτ ~ Exp(λ)`, `λ=(2μ/σ²)/(eᵃ−1)`, `E[Xτ]=E[Mτ]−d=μEτ`.

  At zero drift, Eτ=d²/σ² and λ=1/d. Strong negative Sδ gives leading time δ/|S|; large positive Sδ gives e²ˢᵟ/(2S²). Sign alone does not justify either approximation. At S=1, δ=0.5 the mean is **0.35914 years / 4.3097 months**; at δ=1 it is **2.19453 years**. The exponential law concerns the peak, not the stopping time.
* **Monitoring and simulation:** all 6,000 cached histogram stop times appear over 0–20 years without tail clipping; maximum 19.9464, mean 2.48273 and median 1.75942. Daily and eighth-day runs use independent seeds; square-root-step extrapolation is heuristic without error bars or a uniform accuracy bound. All six selected fine-grid rows stop by their horizon, but the general helper excludes nonstoppers from its reported means. Other parameters can have severe censoring. Deadline stop probabilities keep all original paths in their denominator. Labeling these as error and power requires a specified null, alternative, rejection rule and deadline; a deeper barrier reduces both rejection frequencies and is not automatically a sharper equal-significance test.

## Build and review

Run from the repository root with the environment activated. Use the existing verified ordinary caches; do not invoke `compute.py`, refresh data, open sealed experiments or rerun restoration to fill a missing cache.

```bash
python tools/build.py quant34 --lang en
python tools/build.py quant34 --lang zh
```

`manifest.py` defines the fourteen scenes. `common.py` enforces the presentation cache boundary; `narration_zh.json`, `zh_lines.py` and the additive series caption table support Chinese output. References include Narang; Isichenko; Paleologo; Zuckerman; Patterson; Derman; Thorp; Taylor (1975); Lehoczky (1977); Grossman–Zhou (1993); Magdon-Ismail et al. (2004); Budish–Cramton–Shim (2015); Minsky (2011); Virtu's 2014 S-1; the SEC's 2013 Knight order; the 2020 JPMorgan resolution; Sarao court records; SEBI's July 2025 interim order; attributed contemporary reporting; Kenneth French's data library. Consult the series reading map for full reading lists.

## Problems and complete solutions — English

### Basic 1 — Loss-frequency inversion

**Question.** Five losses in 1,250 days: find the Gaussian-implied daily ratio and iid annualization. What does the count fail to identify?

**Solution.** Set p̂=5/1250=0.004. If daily profit is N(μ,σ²), σ>0, then p=Φ(−μ/σ); the plug-in ratio is s=−Φ⁻¹(0.004)=**2.65207**. Under independent stable daily returns and 252 trading days, S=√252 s=**42.1003**. These are conditional plug-in values, without an estimation confidence interval here. The count omits magnitudes; the stipulated +1/−2000 counterexample above can have the same rare-loss probability and negative mean. Neither actual ratio, net investor return nor skill is identified without additional distributional and accounting information. Dependent loss indicators invalidate an ordinary iid binomial interpretation.

### Basic 2 — Two fee structures

**Question.** For 15% gross, compare 2% then 20% with 6% costs then 20%, assuming eligible profit remains positive.

**Solution.** On initial capital 100, the first pays capital fee 2 and profit fee 0.2(15−2)=2.6, leaving **10.4%**. The second charges costs 6 and profit fee 0.2(15−6)=1.8, leaving **7.2%**. The difference is **3.2 percentage points**. This chosen positive-profit one-period arithmetic excludes high-water marks, timing, financing and different gross returns. The chapter pause uses **10% gross**, giving 6.4% and 3.2%; it is a separate input, not a conflicting solution.

### Basic 3 — Netting and capital denominators

**Question.** Two pods have capital 100 each and profits +10 and −10. Each positive profit pays a 20% bonus. Find total bonus, investor profit, investor return and bonus/gross profit.

**Solution.** Gross profit is 10−10=0 currency units. Bonus B=0.2[max(10,0)+max(−10,0)]=**2**. Net investor profit is **−2**, and on total capital **200**, net return is **−1%**. The bonus divided by gross profit is 2/0 and is **undefined**, not an infinite percentage or a 2% return on combined capital. With positive aggregate gross profit, separate positive-pod bonuses can consume more than the headline share; that comparison needs a nonzero denominator. This specified one-period bonus has no clawback.

### Basic 4 — Chosen Gaussian posterior

**Question.** S∼N(0,τ²), τ=0.5, and Ŝₜ|S∼N(S,1/T). Find the posterior for Ŝₜ=2 at T=1 and T=4.

**Solution.** Multiplying prior and likelihood gives precision τ⁻²+T=4+T and posterior mean `T Ŝ/(4+T)`, variance `1/(4+T)`. Thus T=1 gives **mean 0.4, variance 0.2**; T=4 gives **mean 1, variance 0.125**. These follow by completing the square in `−[4S²+T(S−Ŝ)²]/2`. The observation model is a chosen low-Sharpe iid approximation, not exact inference from arbitrary dependent returns. A prior needs calibration; selection, covariance, financing and risk constraints prevent interpreting the posterior mean alone as a full capital decision.

### Basic 5 — Liquidity under a specified constraint

**Question.** Hold position Q, participation q and coefficient Y fixed. Daily volume halves and daily volatility doubles. Compare exit days and daily clip cost.

**Solution.** With constant volume, D=Q/(q ADV), hence D′=Q/(q ADV/2)=**2D**. The stipulated daily clip cost is c=Yσ√q, so c′=Y(2σ)√q=**2c**. For Q=5 ADV₀, initial days are 5/q and crisis days 10/q. The separate $50m/$20m/10% example is 25 days initially. If daily child size instead stays fixed, q doubles as ADV halves and the model cost becomes **2√2 c**, while days remain unchanged at Q/child size, provided the participation is feasible. Neither convention alone calibrates the full impact of a multi-day liquidation.

### Basic 6 — One reroll

**Question.** A fair independent die can be rerolled once, keeping the second roll. Derive the optimal risk-neutral policy and expectation, without fees.

**Solution.** The forced final roll has value E[D]=3.5. After seeing k on the first roll, keeping pays k and rerolling has conditional expectation 3.5, so reroll **1,2,3** and keep **4,5,6**. The initial expectation is `[3(3.5)+4+5+6]/6=25.5/6=**4.25**`. This also equals E[max(D,3.5)]. It lies above the one-roll value and below six. A fee or nonlinear utility changes the threshold.

### Advanced 7 — Maximum of two K-sided dice

**Question.** Derive the distribution and mean of the maximum M of two independent fair K-sided dice, and evaluate K=6.

**Solution.** For k=1,…,K, `P(M≤k)=(k/K)²`, so `P(M=k)=[k²−(k−1)²]/K²=(2k−1)/K²`; these probabilities sum to one. Then

`E[M]=(2Σk²−Σk)/K²=(K+1)(4K−1)/(6K)`.

Use Σk=K(K+1)/2 and Σk²=K(K+1)(2K+1)/6. At K=6 the mean is **161/36≈4.47222**, between 3.5 and six and **nearer 3.5**. The tail-sum check gives `Σ(k=1…K)[1−((k−1)/K)²]`, the same expression. Independence and equally likely faces are essential for the squared CDF; this is a payoff expectation, not a market quote with costs or inventory risk.

### Advanced 8 — A complete capped St. Petersburg tail

**Question.** For a fair independent coin, first head on toss N pays min(2ᴺ,2²⁰). Find the expectation and generalize to integer m≥1.

**Solution.** `P(N=n)=2⁻ⁿ`. For n≤m each term is one, contributing m. For n>m the payout is 2ᵐ and the total probability is 2⁻ᵐ, contributing one more. Therefore `E[min(2ᴺ,2ᵐ)]=**m+1**`, and the requested m=20 gives **$21**. Dropping the infinite capped tail incorrectly gives $20. The interview uses m=30, an exact cap $1,073,741,824 and expectation **$31**. The uncapped expectation diverges, but a risk-neutral expectation does not determine the price a risk-averse, capital-constrained person would pay, nor guarantee enforceability or counterparty resources.

### Advanced 9 — Kelly and long-run wealth

**Question.** Known iid even-money win probability p=0.55; derive Kelly, its growth, twice-Kelly growth and the asymptotic wealth conclusion.

**Solution.** For a fixed fraction f with |f|<1, `g(f)=p ln(1+f)+(1−p)ln(1−f)`. Its derivative is `p/(1+f)−(1−p)/(1−f)`; setting zero gives **f*=2p−1=0.1**. The second derivative is strictly negative, so this is the unique interior maximizer. Numerically `g(0.1)=**0.00500837**` per bet and `g(0.2)=**−0.000137742**`. With W₀>0, the iid strong law gives `(ln Wₙ−ln W₀)/n→g(f)`. Thus the twice-Kelly wealth tends to zero almost surely in this specified model. Every finite-time wealth multiplier 1±0.2 is positive: this is **not finite-time exact ruin**. At Kelly the almost-sure long-run log-growth rate is positive. Finite paths may still lose substantially, and uncertain p or correlated bets require separate analysis. The interview's p=0.60 instead gives f*=0.20 and different growth numbers.

### Advanced 10 — Exact marginal ratio of an on/off strategy

**Question.** Let R be iid with mean μ, variance σ²>0, and predictable Z∈{0,1} independent of the current R, with stationary P(Z=1)=p. Cash returns zero. Derive the marginal ratio for Y=ZR and the low-mean annual approximation at p=0.75, S=0.6.

**Solution.** `E[Y]=pμ` and `E[Y²]=p(σ²+μ²)`. Subtracting p²μ² gives `Var(Y)=pσ²+p(1−p)μ²`. For p>0 and per-period s=μ/σ,

`sY = √p s / √[1+(1−p)s²]`.

For small |s| this is approximately √p s. If ordinary square-root annualization with m periods applies, s=S/√m gives annual marginal ratio `√p S/√[1+(1−p)S²/m]`. The low-mean approximation is **0.6√0.75≈0.519615**; with m=12, the formula gives approximately **0.51768**. Positive S is reduced under these assumptions; negative S becomes less negative. At p=0, Y is identically zero and its ratio is undefined, not obtained by dividing zero variance. Predictable exposure can create serial dependence, particularly with nonzero mean, so annual long-run variance need not equal m times the marginal variance. Shuffling an already scaled factor is not proof that these idealized conditions hold.

### Qualifying 11 — Finite mean and the reflected ODE

**Question.** Prove the continuous Brownian drawdown-time formula with its assumptions and zero-drift limit, justifying finite expectation.

**Solution.** Let Xₜ=μt+σWₜ, X₀=0, known μ∈ℝ, σ>0, d>0; M includes zero and D=M−X. Stop at τ=inf{t:Dₜ≥d}. The reflected process satisfies `dD=−μdt−σdW+dM`; its regulator grows only at D=0. Seek a C² function on [0,d] satisfying

`(σ²/2)f″−μf′=−1`, `f(d)=0`, `f′(0)=0`.

For μ≠0 put κ=2μ/σ². The slope equation yields `f′(y)=(1−eᵏʸ)/μ≤0`. Integrating backwards from d gives

`f(y)=σ²[eᵏᵈ−eᵏʸ]/(2μ²)−(d−y)/μ`.

This is bounded and nonnegative on the compact interval. For μ=0 use `f(y)=(d²−y²)/σ²`, with the same properties. Apply Itô's formula up to t∧τ. The regulator term vanishes because f′(0)=0; the stochastic integral has mean zero since f′ is bounded and the time is bounded. Therefore

`E[f(Dₜ∧τ)]=f(y)−E[t∧τ]`, so `E[t∧τ]≤f(y)`.

Monotone convergence proves Eτ≤f(y)<∞, hence τ is finite almost surely. Now f(Dₜ∧τ)→f(d)=0 and bounded convergence gives **Eᵧτ=f(y)**. At y=0 this is

`Eτ=σ²(eᵃ−1−a)/(2μ²)`, `a=2μd/σ²`.

Expand eᵃ−1−a=a²/2+O(a³) to obtain the limit **d²/σ²** as μ→0. Equivalently, for S=μ/σ and δ=d/σ the nonzero-drift expression is `(e²ˢᵟ−1−2Sδ)/(2S²)`. S has units time⁻¹ᐟ² and δ time¹ᐟ², making the result a time. Grid monitoring, jumps, changing parameters or compounded wealth require different arguments; a simulation is not the finiteness proof.

### Qualifying 12 — Exponential peak, moving boundary and Wald

**Question.** Prove the exponential peak law, distinguish level-hit and terminal-profit probabilities, and justify expected terminal profit.

**Solution.** Start at a new maximum zero. Until X first reaches ε>0, the running maximum lies in [0,ε), so the moving stop boundary M−d lies between **−d and ε−d**. For ε<d, the probability q(ε) of stopping before reaching ε is bounded below by hitting fixed −d before ε and above by hitting fixed ε−d before ε. Use the increasing scale function

`s(x)=∫₀ˣ exp(−κu)du`, `κ=2μ/σ²`, with `s(x)=x` at μ=0.

The fixed-lower-boundary probability for ℓ<0 is `[s(ε)−s(0)]/[s(ε)−s(ℓ)]`. At ℓ=−d and ℓ=ε−d, numerator is ε+O(ε²), and both denominators tend to `(eᵏᵈ−1)/κ`. Thus the sandwich gives

`q(ε)=λε+o(ε)`, `λ=κ/(eᵏᵈ−1)>0`; at μ=0, λ=1/d.

This is a first-order argument; a finite moving boundary is not identical to a fixed one. Write H(x)=P(Mτ≥x). At the first hit of a new peak x, translation invariance and the strong Markov property give `H(x+y)=H(x)H(y)` for x,y≥0. The local expansion H(ε)=1−λε+o(ε) and H(0)=1 give **H(x)=e⁻λˣ**, so Mτ is exponential with mean 1/λ.

Consequently the chance of **reaching profit level x≥0 before the stop** is e⁻λˣ. By continuity `Xτ=Mτ−d`, so **terminal profit ≥z** has probability `e⁻λ⁽ᶻ⁺ᵈ⁾` for z≥−d, and one below −d. These are different events and neither says τ is exponential.

Part 11 proved Eτ<∞. The stopped Brownian family has `E[Wₜ∧τ²]=E[t∧τ]≤Eτ`; Itô isometry gives L² convergence to Wτ since `E[(Wτ−Wₜ∧τ)²]=E[τ−t∧τ]→0`. Hence E[Wτ]=0 and **E[Xτ]=μEτ**. Also E[Xτ]=1/λ−d. Substitution agrees with the time formula; at μ=0 both sides are zero. This justifies Wald rather than assuming optional stopping at an arbitrary unbounded time.

## 习题与完整解答 — 中文

### 基础 1 — 亏损频率反演

**题目。** 1,250 天有 5 天亏损。在日利润为正态分布的模型下，求隐含日均值与标准差之比及独立同分布条件下的年化值；说明计数无法识别什么。

**解答。** 样本频率 p̂=5/1250=0.004。若日利润为 N(μ,σ²)，σ>0，则 p=Φ(−μ/σ)，代入频率得到 s=−Φ⁻¹(0.004)=**2.65207**。若每日独立、方差稳定且一年有 252 个交易日，则 S=√252 s=**42.1003**。这是附带模型条件的代入估计，此处没有给出估计区间。计数不含损益幅度：以 1237/1238 的概率赚 1、其余情况亏 2000 的指定反例，亏损虽少，均值仍为负。因此仅凭计数不能识别真实比率、投资者净回报或技能。亏损指标若有依赖，普通独立伯努利二项解释也不成立。

### 基础 2 — 两种收费方式

**题目。** 指定毛收益 15%，比较先收资本的 2% 再收剩余正利润的 20%，与先扣 6% 成本再收 20%；假设收费利润为正。

**解答。** 以初始资本 100 计，第一种管理费为 2，业绩费为 0.2(15−2)=2.6，投资者留下 **10.4%**。第二种成本为 6，业绩费为 0.2(15−6)=1.8，留下 **7.2%**，相差 **3.2 个百分点**。这是单期指定算术，未计高水位、时点、融资及不同毛回报。章节暂停题另用 **10% 毛收益**，答案为 6.4% 和 3.2%；两题输入不同，不应混用。

### 基础 3 — 抵销风险与资本分母

**题目。** 两个团队各有资本 100，利润分别为 +10、−10；每个正利润支付 20% 奖金。求奖金总额、投资者利润、总资本回报及奖金占毛利润的比率。

**解答。** 毛利润为 10−10=0。奖金 B=0.2[max(10,0)+max(−10,0)]=**2 个货币单位**。投资者净利润为 **−2**；总资本为 **200**，所以回报为 **−1%**。奖金除以毛利润是 2/0，**没有定义**，不是无穷百分比，也不是总资本回报 −2%。若合计毛利润为正，单独支付赢家的奖金占比可能高于名义费率，但必须先检查分母非零。本题单期奖金没有追回条款。

### 基础 4 — 指定正态后验

**题目。** 先验 S∼N(0,τ²)，τ=0.5；似然 Ŝₜ|S∼N(S,1/T)。当观测比率为 2，分别求 T=1、4 的后验。

**解答。** 把指数项 `−[4S²+T(S−Ŝ)²]/2` 配方，得到后验精度 4+T，均值 `T Ŝ/(4+T)`，方差 `1/(4+T)`。因此一年后 **均值 0.4、方差 0.2**；四年后 **均值 1、方差 0.125**。似然是指定的低夏普、独立同分布近似，不是任意相关收益下的精确推断。先验校准、选择偏差、协方差、融资及风险约束仍需分析；后验均值本身不是完整资本分配规则。

### 基础 5 — 指定约束下的流动性

**题目。** 固定持仓 Q、成交参与率 q 和系数 Y。日成交量减半、日波动翻倍，退出天数和指定日子单成本如何变化？

**解答。** 在每日成交量恒定的假设下 D=Q/(q ADV)，故 D′=Q/(q ADV/2)=**2D**。日子单模型 c=Yσ√q 给出 c′=Y(2σ)√q=**2c**。若 Q=5 ADV₀，最初为 5/q 天，危机时为 10/q 天。另一个 5,000 万持仓、2,000 万日成交量、10% 参与率的例子最初需 **25 天**。若改为固定每日子单数量，成交量减半使参与率翻倍，成本变为 **2√2 c**，而退出天数仍为 Q/子单数量；还须检查参与率可行性。两种约束不同，均不能单独校准多日整笔清算的全部冲击。

### 基础 6 — 一次重掷

**题目。** 公平骰子允许重掷一次，第二次必须接受；无费用且风险中性。求最优策略与期望。

**解答。** 强制最后一次的期望为 3.5。看到第一次点数 k 后，保留得到 k，独立重掷期望为 3.5。因此 **1、2、3 重掷，4、5、6 保留**。总期望为 `[3×3.5+4+5+6]/6=**4.25**`，也等于 E[max(D,3.5)]。答案高于一次掷骰的 3.5，低于 6。加入费用或非线性效用会改变门槛。

### 进阶 7 — 两个 K 面骰子的最大值

**题目。** 两个独立公平 K 面骰子的最大值为 M，求分布与均值，并计算 K=6。

**解答。** 对 k=1,…,K，`P(M≤k)=(k/K)²`，差分得 `P(M=k)=(2k−1)/K²`；概率和为 1。利用整数求和公式，

`E[M]=(2Σk²−Σk)/K²=(K+1)(4K−1)/(6K)`。

其中 Σk=K(K+1)/2，Σk²=K(K+1)(2K+1)/6。K=6 时为 **161/36≈4.47222**，在 3.5 与 6 之间，而且**更接近 3.5**。也可用尾和 `Σ(k=1…K)[1−((k−1)/K)²]` 检查。平方分布函数依赖独立性与公平性。这只是支付期望，不含市场报价的费用或库存风险。

### 进阶 8 — 封顶圣彼得堡博弈的完整尾项

**题目。** 独立公平硬币首次正面在第 N 次，支付 min(2ᴺ,2²⁰)。求期望，并推广到整数 m≥1 的上限 2ᵐ。

**解答。** P(N=n)=2⁻ⁿ。当 n≤m，每项贡献 1，共 m。n>m 时支付固定 2ᵐ，而这一尾部总概率为 2⁻ᵐ，故另贡献 1。因此 `E[min(2ᴺ,2ᵐ)]=**m+1**`；题目 m=20 的答案为 **21 美元**，漏掉尾项会误得 20。面试例子 m=30，精确上限为 1,073,741,824 美元，期望为 **31 美元**。无上限期望发散，但风险中性期望不是风险厌恶、资金受限者愿付的票价，也不保证对手方有能力或有义务支付。

### 进阶 9 — 凯利与长期财富

**题目。** 已知独立同分布、等额赔率，胜率 p=0.55；求凯利比例、对数增长率、两倍凯利增长率及财富的渐近结论。

**解答。** 固定财富比例 f，|f|<1 时，`g(f)=p ln(1+f)+(1−p)ln(1−f)`。一阶导数为 `p/(1+f)−(1−p)/(1−f)`，令其为零得 **f*=2p−1=0.1**。二阶导数严格为负，所以是唯一内部最大值。数值为 `g(0.1)=**0.00500837**`，`g(0.2)=**−0.000137742**`，单位为每次下注。W₀>0 时，强大数定律给出 `(ln Wₙ−ln W₀)/n→g(f)`；因此指定模型中的两倍凯利财富几乎必然趋于零。每个有限期乘数 1±0.2 都为正，故这**不是有限时间恰好破产**。凯利比例的长期对数增长率为正，但有限样本仍可能大幅亏损。胜率未知或下注相关需要额外分析。面试另用 p=0.60，凯利为 0.20，增长数字不同。

### 进阶 10 — 开关仓位的精确边际比率

**题目。** R 独立同分布，均值 μ、方差 σ²>0；可预测指标 Z∈{0,1} 与当期 R 独立，平稳持仓概率为 p。现金收益为零。推导 Y=ZR 的边际比率，并在 p=0.75、年化 S=0.6 时给低均值近似。

**解答。** E[Y]=pμ，E[Y²]=p(σ²+μ²)，所以 `Var(Y)=pσ²+p(1−p)μ²`。令单期 s=μ/σ，p>0 时

`sY=√p s/√[1+(1−p)s²]`。

单期 |s| 很小时近似为 √p s。若另满足通常的平方根年化条件，一年 m 期、s=S/√m，则年化边际比率为 `√p S/√[1+(1−p)S²/m]`。低均值近似为 **0.6√0.75≈0.519615**；m=12 时精确边际公式约为 **0.51768**。在这些条件下，正比率降低，负比率变得较不负。p=0 时 Y 恒为零，其比率没有定义。可预测仓位可能产生序列依赖，特别是均值非零时，因此长期年化方差未必等于 m 倍单期方差。打乱已缩放因子不能证明所有理想化条件成立。

### 资格题 11 — 有限均值与反射微分方程

**题目。** 在明确假设下证明连续布朗回撤停止时间公式与零漂移极限，并先证明均值有限。

**解答。** Xₜ=μt+σWₜ，X₀=0，已知常数 μ∈ℝ、σ>0、d>0；峰值 M 包括初始零，D=M−X，τ=inf{t:Dₜ≥d}。反射过程满足 `dD=−μdt−σdW+dM`，调节项只在 D=0 增长。在 [0,d] 上寻找 C² 函数，满足

`(σ²/2)f″−μf′=−1`，`f(d)=0`，`f′(0)=0`。

μ≠0 时记 κ=2μ/σ²，一阶方程得 `f′(y)=(1−eᵏʸ)/μ≤0`；从 d 反向积分，

`f(y)=σ²[eᵏᵈ−eᵏʸ]/(2μ²)−(d−y)/μ`。

该函数在紧区间上有界且非负。μ=0 时取 `f(y)=(d²−y²)/σ²`，性质相同。对 t∧τ 应用伊藤公式；f′(0)=0 消去反射项，因 f′ 有界、停止时间有界，随机积分均值为零。因此

`E[f(Dₜ∧τ)]=f(y)−E[t∧τ]`，故 `E[t∧τ]≤f(y)`。

单调收敛先给出 Eτ≤f(y)<∞，所以 τ 几乎必然有限。随后 f(Dₜ∧τ)→f(d)=0，由有界收敛得到 **Eᵧτ=f(y)**。令 y=0，

`Eτ=σ²(eᵃ−1−a)/(2μ²)`，`a=2μd/σ²`。

用 eᵃ−1−a=a²/2+O(a³) 展开，μ→0 时极限为 **d²/σ²**。以 S=μ/σ、δ=d/σ 表示，则非零漂移公式为 `(e²ˢᵟ−1−2Sδ)/(2S²)`。S 单位为时间⁻¹ᐟ²，δ 为时间¹ᐟ²，结果具有时间单位。离散监控、跳跃、变参数或复利财富需要不同论证；模拟不能替代有限性证明。

### 资格题 12 — 指数峰值、移动边界与瓦尔德恒等式

**题目。** 证明停止时峰值的指数分布，区分触及利润水平与终止利润事件，并证明终止利润均值。

**解答。** 从新峰值零开始。在首次触及 ε>0 前，峰值位于 [0,ε)，所以移动停止边界 M−d 位于 **−d 与 ε−d** 之间。ε<d 时，停止先于触及 ε 的概率 q(ε)，下界为先触及固定 −d 的概率，上界为先触及固定 ε−d 的概率。取递增尺度函数

`s(x)=∫₀ˣ exp(−κu)du`，`κ=2μ/σ²`；μ=0 时 s(x)=x。

固定下界 ℓ<0 的先触及概率为 `[s(ε)−s(0)]/[s(ε)−s(ℓ)]`。对于 ℓ=−d 与 ℓ=ε−d，分子均为 ε+O(ε²)，分母都趋于 `(eᵏᵈ−1)/κ`。夹逼得到

`q(ε)=λε+o(ε)`，`λ=κ/(eᵏᵈ−1)>0`；μ=0 时 λ=1/d。

这是一阶极限论证，不能把有限移动边界直接等同固定边界。记 H(x)=P(Mτ≥x)。到达新峰值 x 时，用平移不变性与强马尔可夫性质得 `H(x+y)=H(x)H(y)`。结合 H(0)=1 与局部式 H(ε)=1−λε+o(ε)，得到 **H(x)=e⁻λˣ**，所以 Mτ 是均值 1/λ 的指数分布。

因此，**停止前曾达到利润水平 x≥0** 的概率为 e⁻λˣ。由连续性 Xτ=Mτ−d，所以 **终止利润至少为 z** 的概率在 z≥−d 时为 `e⁻λ⁽ᶻ⁺ᵈ⁾`，低于 −d 时为 1。两者事件不同，且都不说明 τ 服从指数分布。

上一题已证 Eτ<∞。停止布朗族满足 `E[Wₜ∧τ²]=E[t∧τ]≤Eτ`；伊藤等距又给 `E[(Wτ−Wₜ∧τ)²]=E[τ−t∧τ]→0`，所以 L² 收敛并有 E[Wτ]=0。因此 **E[Xτ]=μEτ**。另一方面 E[Xτ]=1/λ−d，代入与停止时间公式一致；μ=0 时均为零。这是瓦尔德恒等式的条件论证，不能对任意无界停止时间直接假定可选停止成立。

## Chapter question checks / 章节暂停题补充

The speed question needs captured notional and a first-arrival contest; 3 ms alone is not a dollar value. Cancellation at 98% is an investigation prompt, not a legal finding. For 1,000 firms with independent annual survival 1/2, the expected ten-year survivors are **1000/2¹⁰=0.9765625**. Cross-firm independence is unnecessary for that expectation, but necessary for a binomial count law; expectation does not guarantee one survivor or establish skill. Three independent fair dice have expectation 10.5 and SD √(105/12)≈2.958. Revealing one specified die is six gives conditional value 13, hence selling at 11 loses 2 in conditional expectation; a buy alone requires an order-flow information model.

For the research pause, S=1.5, annual σ=0.04, d=0.06 give δ=1.5, μ=0.06 and a=4.5. Thus **Eτ=(e⁴⋅⁵−5.5)/4.5=18.7816 years**, and **E[Xτ]=0.06Eτ=1.12690**, or 112.690% of initial capital in arithmetic profit before costs. This unbounded-time arithmetic model has no bankruptcy, financing or compounding constraint; it is not an attainable fixed-horizon investor return.

速度题需要被抢先捕获的名义金额及竞争模型，3 毫秒本身不是美元价值。98% 撤单率不能单独构成违法认定。1,000 家企业每年独立以 1/2 概率生存，十年幸存者的**期望为 0.9765625**；求期望无需企业间独立，但二项计数分布需要，且期望不保证恰有一家，也不证明技能。三个独立公平骰子之和均值 10.5、标准差约 2.958；透露指定一颗为 6 后条件均值为 13，在 11 卖出条件期望亏 2；仅观察买单则需订单信息模型。

研究暂停题给 S=1.5、年波动 0.04、回撤 0.06，得 δ=1.5、μ=0.06、a=4.5，故**平均停止时间 18.7816 年，平均算术利润 1.12690 倍初始资本**。这是不限制期限、无破产和融资约束的算术模型，不是可实现的固定期限复利投资回报。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part34.md`](../../../docs/qa/quant/part34.md).*
