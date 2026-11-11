# Quant, Built — Part 20: Credit

Visual pass complete on `quantitative-finance`: 40 English/Chinese endpoint
sheets and 20 English motion sheets reviewed on the frozen source, plus
20 focused native frames. The chaptered silent preview runs 80:28.
Full continuous production-voice listening remains pending; signal checks do not
certify pronunciation. See [the evidence record](../../../docs/qa/quant20-polish-evidence.json).

Part 20 of [43 parts](../README.md), following term structure and preceding
counterparty risk. This lecture distinguishes physical event probabilities,
risk-neutral pricing inputs and descriptive historical illustrations.
The current source has 137 bilingual narration entries, approximately 69.2 minutes
at the series' narration-rate convention. Actual playback includes animations
and pauses and is measured separately.

## Chapters and scope

1. **Opening.** The Lehman CDS auction's final price was 8.625% of par. The
   corresponding gross protection payment on covered auction-settled contracts
   was 91.375%, before premiums, netting, hedges and counterparty performance.
2. **Spreads.** FRED Moody's Aaa and Baa yields relative to a ten-year Treasury
   illustrate broad yield differences. They are not duration-matched OAS. Baa
   minus Aaa still contains duration, composition, liquidity and premium effects;
   neither series isolates physical expected default loss.
3. **Merton.** A single zero-coupon obligation, continuously diffusing replicable
   assets, constant parameters and no earlier default give equity as a call and
   debt as assets minus equity. Pricing drift is risk-neutral; physical default
   probability uses a physical drift and a specified distribution. The 3D spread
   display explicitly caps its vertical view at 1,500 bp. Term curves instead use
   an invertible log1p scale with raw bp tick labels and no top-coding; numerical
   cancellation residuals below 1e-7 bp are treated as zero.
4. **Distance to default.** Three original price/filing reconstructions illustrate
   fitted asset cushions. Their monthly parameters are fitted at month-end and
   assigned to earlier days in that month. These are **retrospective fits**, not
   certified live forecasts. The original drift floor and filing-order/version
   assumptions remain disclosed. A distance is not a probability, and its normal
   tail is not Moody's calibrated EDF. Plots retain the saved finite ranges.
5. **First passage and Leland.** Continuous-monitoring first-passage probabilities
   differ from terminal-event probabilities. Discrete path drawings can miss
   barrier crossings. Leland's perpetual debt, tax benefit and bankruptcy costs
   illustrate an endogenous boundary under a specific model.
6. **Intensity and recovery.** Deterministic intensity gives exponential survival;
   a stochastic Cox intensity gives marginal survival as an expectation.
   Zero recovery, fractional recovery of market value and face recovery at
   maturity are different contracts. The separately named CIR example evaluates
   recovery-of-market-value pricing exactly within the deterministic-rate model.
7. **CDS.** Premium and protection legs, accrued-premium approximation,
   illustrative quote bootstrapping, annuity sensitivity, gross settlement
   versus net jump, auction eligibility, upfront conventions and residual basis
   risk. The quotes are invented teaching inputs, not a market calibration.
8. **Bankruptcy labels.** An 8-K Item 1.03 reporting event is not every definition
   of credit default. Coverage, entity resolution, repeated reports, legal event
   dates, outcome windows, censoring and the at-risk denominator require audits.
   Current-vintage XBRL frames and an assumed three-month lag do not establish
   historical availability; public float is not total equity capitalization.
9. **Altman.** Historical discriminant weights and zones are illustrated on
   declared synthetic observations. They are not calibrated probabilities.
   Five-ratio logit weights differ in sign convention, scaling and objective.
10. **Logit and trees.** Independent fit, selection and evaluation samples from a
    fixed invented law demonstrate preprocessing, early stopping, ROC, Brier
    scores and calibration. The 3D display is a median slice, not partial
    dependence or a causal leverage experiment.
11. **Vasicek and capital.** Homogeneous conditional independence and vanishing
    equal exposures yield a limiting default-fraction distribution. Finite
    simulations have lattice and sampling effects. The corporate IRB formula
    is a stylized regulatory illustration, not all current capital requirements.
12. **Copulas.** Marginal curves leave joint dependence unidentified. Latent
    Gaussian correlation differs from binary-default correlation. The two-name
    cloud uses correlation 0.5 and t degrees of freedom 3; the 125-name pool uses
    correlation 0.2 and t degrees of freedom 4. Both 1,500-point clouds are shown
    in full. The loss histogram spans the entire 0–60% support in 0.5%-loss bins
    without folding tail observations into an overflow bin. Monte Carlo tails need uncertainty.
13. **Tranches.** Waterfalls, fixed-marginal dependence stresses,
    default-weighted recovery and illustrative loss sensitivities. Expected-loss
    curves and ticks are consistently in percent of tranche notional. A bounded
    senior tranche need not be monotone in correlation for all parameters.
    Base correlations match expected losses from an **85%/15% mixture of two
    Gaussian regimes**, not a t-copula market calibration. Interpolation alone
    does not guarantee a consistent loss distribution or arbitrage-free pricing.
14. **Crisis.** A stylized aggregate-state loss model explains a possible risk
    premium mechanism; it does not reconstruct a mortgage deal. The FCIC's 83%
    downgrade statistic concerns **Moody's 2006 Aaa MBS tranches**, not every AAA
    asset. Downgrade, default and realized full loss are different outcomes. The
    re-tranching page displays the expected tranche-loss payoff, without a universal
    ordering of correlation sensitivities.
15. **London Whale.** $6.2 billion trading losses and the approximately $920 million
    September 2013 multi-agency penalties are different amounts. The VaR formulas
    are general teaching approximations, not a reconstruction of a proprietary
    model. Model changes require independent validation and fixed-position comparisons.
16. **March 2020.** Unadjusted ETF closing-price changes exclude distributions.
    The March 23 and April 9 facilities had eligibility restrictions. Descriptive
    co-movement does not identify causal policy effects or isolate expected defaults.
    The displayed spread change is not identified as a causal policy effect.
17. **Private credit.** The IMF's 2023 estimate of about $2.1 trillion includes
    assets and undeployed commitments. Listed BDC NAV is a levered net-asset
    measure, not simply loan value. Quarter-end NAV is published later; changes
    in NAV and raw price exclude distributions and are not total returns.
18. **House rule.** Align the event, horizon, information date and probability
    measure before comparing probabilities. Accounts and prices share information.
    Evaluate calibration, concentration and dependence scenarios; state each
    hedge's exposure, sensitivity and residual basis risk.
19. **Research.** Exact model CDF, numerical quadrature, discrete versus interpolated
    quantiles, formal granularity expansion and concentrated-book failure. A
    separate answer explains why 400 legal names can have effective count 3.99.
20. **Recap and problems.** Four desk questions, ten worked problems, references
    and the connection to counterparty risk.

## Data boundaries and reproduction

The five original items `dataset`, `models`, `sorts`, `altfit` and `envelope`
access or depend on the sealed firm-year experiment. The presentation loader
rejects them before invoking the original loader. Do not run the original
all-items compute command during this review.

Twenty permitted original descriptive items restored normally. `defaults` failed
with an unexpected SEC response; one justified normal retry also failed. Both
logs remain in `renders/qa/quant20/`. No annual filing count or count/spread
correlation is reported, and no substitute count is fabricated. Public filing
records are distinct from the joined sealed predictive experiment, which remains
closed.

Original compute drivers, House algorithms and the three global quant registries
are preserved. The Part 20 cumulative historical trial count remains 317 and the
global count 23,562. This review adds no market trial and opens no sealed market
experiment. These are counter observations, not new registrations or evidence
that all historical experiments were valid.

Two separately named examples are implemented in
[`synthetic_credit_example.py`](synthetic_credit_example.py):

```bash
python -m videos.quant.quant20.synthetic_credit_example synthetic_credit_example rmv_credit_example
python -m pytest -q tests/test_quant20_teaching_examples.py
python tools/zh_lines.py quant20 --todo
python tools/lecture_length.py quant20 --floor 50
python tools/qa_series.py quant20 --cached-only --resume --timeout 1800
python tools/qa_series.py quant20 --lang zh --cached-only --resume --timeout 1800
python tools/qa_series.py quant20 --motion --cached-only --resume --timeout 1800
```

Run commands in the configured Manim/TeX environment. A successful render alone
is not visual approval; inspect the current images and movie contact sheets,
then record review receipts tied to the source fingerprint and input signatures.

The synthetic law, sizes and seeds were fixed before execution: fit 8,000/202001,
selection 4,000/202002, evaluation 6,000/202003. Clipping and scaling use fit
observations only. A fixed ridge logit is compared with at most 240 depth-3 trees,
learning rate .05, minimum leaf 30, subsampling .8, seed 0 and selection-based
30-round early stopping. Evaluation observations are generated after selection.
There is no tuning to make one model win.

Actual synthetic evaluation outputs: 563 events among 6,000 observations; AUC
0.7123 for fixed Z, 0.9276 for logit and 0.9246 for trees. Brier scores are 0.04910,
0.04960 and 0.08510 for logit, trees and the **fit-sample** base-rate benchmark.
There are 107 selected trees. These numbers provide no market generalization.
Calibration uses ten groups of 600 and discloses tie splitting; ROC moves tied
scores together. The median slice updates log equity for the leverage/cushion identity.

For the CIR example, let a = 1−R. The required expectation is
E[exp(−a∫λ dt)], not E[exp(−∫λ dt)] raised to a. Scaling initial intensity and
long-run mean by a and volatility by √a gives the exact CIR Laplace functional.
An independent Riccati ODE test verifies the result. Jensen's inequality implies
that its yield spread is at least the legacy scaled-zero-recovery approximation
for 0<a<1. Original `compute_cox` remains unchanged.

## Four desk answers

1. **100 bp CDS, recovery 40%.** The continuous flat-intensity approximation gives
   λᴽ = .01/.6 = .016667. The one-year probability is 1−exp(−λ)=1.65%, and the
   five-year probability is 1−exp(−5λ)=8.00%. Intensity and probability differ;
   these are pricing-measure results under fixed conventions.
2. **Volatility transfer.** With asset value and other Merton inputs fixed, equity
   call value rises with asset volatility and debt value falls by the same amount.
   This is a model asset-substitution mechanism, not every firm's causal response.
3. **Tiny senior expected loss.** If losses coincide with high marginal value of
   wealth, a pricing kernel can assign a substantial premium. Expected loss or
   a rating alone does not specify that kernel or a traded spread.
4. **Fit AUC .98 versus independent .90.** Report an honestly described independent
   assessment with counts, uncertainty and population limits, while disclosing
   development results. The gap includes sampling variation and fitting effects;
   check calibration separately. Both ranking and calibration can shift.

## Ten worked problems

1. **Merton debt and spread.** Put–call parity gives
   B=V−E=D exp(−rT)Φ(d₂)+VΦ(−d₁). Its yield is −ln(B/D)/T, so
   s=−ln[Φ(d₂)+(V exp(rT)/D)Φ(−d₁)]/T. This assumes a single terminal obligation,
   replicable lognormal assets, constant parameters and no intervening default.
2. **Equity volatility.** Itô's diffusion term is E_V σ_V V dW. Because E_V=Φ(d₁),
   σ_E=Φ(d₁)σ_V V/E. Leverage magnifies equity volatility as the residual claim
   becomes small; a statement about a varying firm requires holding the other
   model inputs and financing conventions explicit.
3. **Continuous CDS triangle.** With constant λ, recovery R, deterministic r and
   continuous premiums, premium PV is s∫₀ᵀexp[−(r+λ)t]dt. Protection PV is
   (1−R)λ times the same integral, hence s=(1−R)λ. Scheduled premiums and accrual
   conventions change the exact relation.
4. **Three-year annual CDS, 120 bp.** Declare the convention: annual premiums at
   1,2,3, no accrued premium, continuous protection payment, r=.04 and R=.4.
   Solve .012∑ᵢ₌₁³exp[−(.04+λ)i]
   =.6λ[1−exp(−3(.04+λ))]/(.04+λ).
   The triangle starts at λ=.02. Solving this equation gives λ=.0194118 and a
   one-year probability 1−exp(−λ)=1.92246%. Adding accrued premium requires a
   changed equation. One three-year quote cannot identify three unrestricted
   annual hazards without further assumptions.
5. **Vasicek limit.** Given M, defaults have probability
   p(M)=Φ[(Φ⁻¹(p)−√ρ M)/√(1−ρ)]. Conditional independence and vanishing equal
   weights give default fraction L∞=p(M). For 0<x<1 and 0<ρ<1,
   F(x)=Φ[(√(1−ρ)Φ⁻¹(x)−Φ⁻¹(p))/√ρ]. Consequently
   qα=Φ[(Φ⁻¹(p)+√ρ Φ⁻¹(α))/√(1−ρ)]. A fixed LGD multiplies the fraction.
6. **Corporate IRB illustration.** For p=.02, LGD=.45 and maturity M=2.5, use
   R(p)=.12(1−exp(−50p))/(1−exp(−50))
   +.24[1−(1−exp(−50p))/(1−exp(−50))],
   b(p)=[.11852−.05478 ln p]² and
   K=LGD{Φ[(Φ⁻¹(p)+√R Φ⁻¹(.999))/√(1−R)]−p}
   ×[1+(M−2.5)b]/(1−1.5b). The unchanged House function gives K=.0918834,
   versus expected loss .009; risk weight 12.5K=1.14854. This omits other current
   regulatory requirements and is not a bank-specific capital recommendation.
7. **Tranche dependence.** Normalized tranche loss is
   [(L−A)⁺−(L−D)⁺]/(D−A). First-loss equity and uncapped senior stop-loss payoffs
   have different convexity. Under the homogeneous fixed-marginal Gaussian pool,
   increasing dependence shifts mass toward joint survival and severe joint loss.
   Equity expected loss falls and super-senior stop loss rises under this ordering.
   A capped senior tranche is a difference of stop losses, so its sensitivity
   need not have one sign for all PDs, attachments and correlations. A protection
   buyer and seller have opposite positions; spread repricing also needs premium legs.
8. **Logit odds.** Odds are exp(β₀+βᵀx). A two-standard-deviation increase with
   coefficient .5 per standard deviation multiplies odds by exp(1)=2.71828,
   not probability. From probability p, new probability is ep/(1−p+ep).
9. **Qualifying problem: finite pool.** Given the bad-state factor y, K|y is
   Binomial(N,p(y)); therefore
   Pr(L≤k/N)=∫[∑ⱼ₌₀ᵏ C(N,j)p(y)ʲ(1−p(y))ᴺ⁻ʲ]φ(y)dy.
   This identity is exact under the model; numerical evaluation is not exact
   arithmetic. Conditional variance p(1−p)/N tends to zero, yielding the limiting
   distribution. For a continuous strictly increasing limit CDF at qα, quantiles
   converge too. The saved grid is y∈[−8,8] with 8,001 points. Its `exact` output
   is the discrete numerical quantile; `smooth` linearly interpolates the CDF
   between k/N support points. They must not be given the same name or error claim.
10. **Qualifying problem: smooth granularity expansion.** Let Lε=μ(Y)+εU,
    E[U|Y]=0, h the density of Y, v(y)=Var(U|y), with μ locally increasing,
    μ′≠0, h>0 and adequate smoothness, integrability and remainder control.
    Write fμ(x)=h(y)/μ′(y), y=μ⁻¹(x). Expanding a smooth CDF gives
    Fε(x)=Fμ(x)+(ε²/2)d[fμ(x)v(μ⁻¹(x))]/dx+o(ε²).
    Substituting qε=q₀+δ and solving Fε(qε)=α yields
    δ=−ε²/(2h(yα)) d[h(y)v(y)/μ′(y)]/dy+o(ε²).
    In the homogeneous finite-pool approximation ε²=1/N and v=p(1−p), producing
    the displayed GA. Its finite-grid coefficient is approximately 2.03958 for
    p=.01, ρ=.12 and α=.999. **Raw discrete loss quantiles have O(1/N) lattice
    effects**, so the smooth remainder cannot be asserted for them automatically.
    Unequal-name substitution by 1/HHI requires homogeneous risk and small maximum
    exposures. A 500-name Zipf book has maximum weight .1472 and effective count
    28.09; simulated q.999≈.1959 versus .1629 from that heuristic, demonstrating
    its limitation rather than validating it. With one 50% exposure and 399 sharing
    the rest, HHI=.25+.25/399 and effective count≈3.99. At PD 1% and full LGD,
    q.999 is at least .5 regardless of the smaller names' dependence.

## Sources and audit trail

Primary public records, accessed for this review on 8 November 2026:

- [FRED BAA10Y](https://fred.stlouisfed.org/series/BAA10Y),
  [BAA](https://fred.stlouisfed.org/series/BAA), [AAA](https://fred.stlouisfed.org/series/AAA),
  [GS10](https://fred.stlouisfed.org/series/GS10), [USREC](https://fred.stlouisfed.org/series/USREC).
- [FCIC report, p. 221](https://fraser.stlouisfed.org/files/docs/historical/fct/fcic_report_final_20110127.pdf):
  rating-agency/vintage denominator and downgrade history.
- [Senate London Whale findings](https://www.hsgac.senate.gov/subcommittees/investigations/rep/senate-investigations-subcommittee-holds-hearing-and-releases-report-on-jpmorgan-chase-whale-trades/),
  [FCA final notice](https://www.fca.org.uk/publication/final-notices/jpmorgan-chase-bank.pdf),
  [SEC September 2013 settlement](https://www.sec.gov/newsroom/press-releases/2013-187).
- [Federal Reserve SMCCF](https://www.federalreserve.gov/monetarypolicy/smccf.htm),
  [April 9 term sheet](https://www.federalreserve.gov/newsevents/pressreleases/files/monetary20200409a2.pdf).
- [IMF April 2024 GFSR, chapter 2](https://www.imf.org/en/-/media/files/publications/gfsr/2024/april/english/ch2.pdf):
  the assets-plus-undeployed-commitments definition of the $2.1 trillion estimate.
- [Basel explanatory note on IRB risk weights](https://www.bis.org/bcbs/irbriskweight.pdf),
  [SEC Form 8-K](https://www.sec.gov/files/form8-k.pdf), and the original source
  citations embedded in the descriptive data loader.

Texts: O'Kane, *Modelling Single-name and Multi-name Credit Derivatives*;
Schönbucher, *Credit Derivatives Pricing Models*; Duffie–Singleton, *Credit Risk*;
Lando, *Credit Risk Modeling*; Hull, *Options, Futures, and Other Derivatives*.
Edition-dependent chapter numbering is not treated as a universal locator.

Research: Altman (1968), Merton (1974), Black–Cox (1976), Leland (1994),
Jarrow–Turnbull (1995), Lando (1998), Duffie–Singleton (1999), Li (2000),
Shumway (2001), Friedman (2001), Vasicek (2002), Gordy (2003),
Crosbie–Bohn (2003), Andersen–Sidenius (2004), Getmansky–Lo–Makarov (2004),
Bharath–Shumway (2008), Campbell–Hilscher–Szilagyi (2008),
Coval–Jurek–Stafford (2009), Gourieroux–Laurent–Scaillet (2000),
Martin–Wilde (2002), Gordy–Lütkebohmert (2013), and the market-history papers
named in the scenes. Findings are conditional on each paper's population,
identification and model assumptions.

## 中文讲义

本轮视觉复核完成：已实际检查40张英中文旁白节点画面表、20张英文动画画面表
及20张原尺寸重点画面。配音开场与分章静音预览已核验；
完整成片连续听审及发音验证仍待完成，信号检查不能替代听审。
现有137项双语旁白，按课程语速估计约69.2分钟，实际播放还包括动画与停顿。

**内容与关键限定。** 雷曼拍卖8.625%终价对应适用合约91.375%总保护支付，
不是所有合约净现金量。穆迪收益率减十年国债并非久期匹配OAS，Baa减Aaa
也非纯违约风险。Merton只在单笔终点债务、可复制连续扩散资产等假设下给出
期权表示；定价测度与实际事件测度须区分。三个公司的违约距离是事后月末
拟合，原漂移下限和申报版本、排序限制保留，不是已认证实时预测；距离本身
不是概率，正态尾也非穆迪经验校准EDF。首次通过的连续公式与离散路径图
不同，Leland的内生边界依赖永续债、税与破产成本假设。

Merton期限曲线采用可逆的对数加一坐标，基点刻度标注原值，不截顶；低于
$10^{-7}$基点的浮点残差视为零。两幅copula点云各完整显示1500点；
池损失直方图覆盖完整0–60%区间，不将尾部观测折叠入末格。分层预期损失
曲线与刻度均按分层本金百分比计量。

确定性强度给指数生存率，随机Cox强度的边际生存率须取期望。市场价值比例
回收、到期面值回收和违约立即回收是不同现金流。独立命名CIR例子精确计算
市场价值比例回收泛函，不能简单将零回收收益率乘一减回收率。CDS示例报价
是虚构教学输入；区分保费腿、保护腿、应计近似、风险年金敏感度、违约总支付
和相对当前市值的净跳跃。标准票息、拍卖与清算都有适用条件，现券加保护
仍有融资、可交割性与对手方等剩余风险。

8-K第1.03项只报告破产或接管，不覆盖所有信用违约。标签须核查覆盖、实体、
重复报告、法律事件日、窗口、删失与风险总体分母。当前XBRL框架及固定三个月
滞后不证明时点可得；公众持股市值不等于总权益市值。原公开检索及一次有理由
正常重试都失败，计数与相关系数保持不可用，不能从旧讲义补造。五项原实验
路径`dataset/models/sorts/altfit/envelope`在展示入口被阻止。二十项允许原描述计算
正常恢复；98份受保护源码与登记文件保持不变，Part 20累计317、全局23562，
没有新增市场试验，没有开启封存公司年度实验。

Altman历史判别分数和区间不是校准概率。固定合成总体使用十二个财务输入，
维持权益、资产、杠杆与缓冲恒等关系；拟合8000、选择4000、评估6000，种子
分别202001、202002、202003。截尾与尺度只用拟合集，提升树按选择集早停，
评估样本在选择结束后生成，事前固定参数与种子，不挑有利结果。实际评估
563个事件，Z、Logit与树AUC依次0.7123、0.9276、0.9246；Brier依次比较Logit
0.04910、树0.04960、拟合集基础率基准0.08510，选中107棵树。这些数值不证明
市场预测能力。ROC相同分数一同移动；校准十组各600，披露拆分平局。
三维曲面是合成中位数切片，不是部分依赖，更不是杠杆因果效应。

Vasicek需要同质条件独立及小暴露极限；有限池保留格点与模拟误差，简化IRB
不等于完整当前资本规则。潜在相关性不同于二元违约相关性。散点云用相关性
0.5与t自由度3，125名字池用0.2与自由度4；尾部计数须考虑不确定度。封顶
优先层损失对相关性不一定普遍单调，买卖保护方向相反。随机回收例子固定的是
按违约加权平均回收。基础相关性来自85%/15%双高斯状态混合，并非t连接函数
市场校准；插值不保证一致联合损失分布或无套利。

FCIC的83%针对穆迪2006年Aaa抵押贷款支持证券分层，降级不等于违约或全损。
伦敦鲸62亿美元交易损失不同于2013年9月约9.2亿美元多机构罚款，VaR教学公式
不重建专有模型。2020年ETF图是未调整价格，不含分配；美联储工具有评级和
其他资格条件，前后图不能识别因果政策效果。IMF的2.1万亿美元包含资产与未
投放承诺资本。BDC净值是含负债的净资产，不是单纯贷款值；期末值发布更晚，
净值和价格变化非总回报，波动差不能唯一识别贷款风险或评估平滑。

**四道交易台题。** 100基点、回收40%的连续平保费近似给风险中性强度1.6667%，
一年概率1.65%、五年8.00%，强度不是概率。Merton其他输入固定时，资产波动
增加把债务价值转给权益。优先层坏状态集中损失可能获得定价核溢价，预期损失
或评级本身不决定利差。样本内0.98和独立0.90须透明同时披露，强调独立评估、
事件数、不确定度和总体限制；差距不全是记忆，排序与校准都可能随周期变化。

**十题解答。**

1. 平价关系给B=V−E=D exp(−rT)Φ(d₂)+VΦ(−d₁)，故
   s=−ln[Φ(d₂)+(V exp(rT)/D)Φ(−d₁)]/T，依赖单笔终点债等假设。
2. Itô扩散项为E_Vσ_VV，且E_V=Φ(d₁)，故σ_E=Φ(d₁)σ_VV/E。
   剩余权益变小会放大杠杆波动，须明确保持其余输入的比较方式。
3. 连续保费现值s∫exp[−(r+λ)t]dt，保护腿为(1−R)λ乘同一积分，
   得s=(1−R)λ；离散日期、应计和结算改变精确关系。
4. 明确年付、不计应计、违约连续支付、r=.04、R=.4：
   .012∑ᵢ₌₁³exp[−(.04+λ)i]=.6λ[1−exp(−3(.04+λ))]/(.04+λ)。
   三角初值λ=.02，解为.0194118，一年概率1.92246%。加入应计须改方程，
   一条三年报价不足以识别三条自由年度风险率。
5. 给定M，p(M)=Φ[(Φ⁻¹(p)−√ρM)/√(1−ρ)]。条件独立及小等额暴露使
   L趋于p(M)，得到F(x)=Φ[(√(1−ρ)Φ⁻¹(x)−Φ⁻¹(p))/√ρ]及
   qα=Φ[(Φ⁻¹(p)+√ρΦ⁻¹(α))/√(1−ρ)]，固定LGD按比例缩放。
6. p=.02、LGD=.45、M=2.5，将上文规定R(p)、b(p)代入IRB式，
   K=.0918834，预期损失.009，风险权重12.5K=1.14854，其他资本规则未含。
7. 分层损失为[(L−A)⁺−(L−D)⁺]/(D−A)。同质固定边际高斯池的依赖变化
   使首损权益与超优先止损有不同凸性响应；封顶层是两止损之差，不保证
   全参数单调。买卖保护方向相反，完整利差还需保费腿。
8. Logit系数每标准差.5，增加两个标准差使几率乘exp(1)=2.71828，
   不是概率直接乘该数。原概率p的新概率为ep/(1−p+ep)。
9. 资格题：给定y，K服从Binomial(N,p(y))，对二项累积概率乘φ(y)积分，
   即得Pr(L≤k/N)精确模型恒等式。条件方差p(1−p)/N趋零，配合连续且唯一
   极限分位点得到分位数收敛。数值求积不是精确算术；保存例子用[-8,8]
   8001点。`exact`是离散数值分位数，`smooth`在线性插值CDF上反解，不能
   混称或声称同一误差阶。
10. 资格题：设Lε=μ(Y)+εU、E[U|Y]=0、v(y)=Var(U|y)，均值局部递增、
    导数非零、密度h为正，并满足光滑、可积及余项条件。
    fμ(x)=h(y)/μ′(y)，平滑展开Fε=Fμ+(ε²/2)d(fμv)/dx+o(ε²)，在
    qε=q₀+δ代入Fε(qε)=α，得δ=−ε²/(2h)d(hv/μ′)/dy+o(ε²)。
    同质池取ε²=1/N、v=p(1−p)，本例系数约2.03958。原离散分位数有
    O(1/N)格点误差，不能自动继承平滑余项。逆HHI替换要求同质风险和最
    大暴露较小。500笔Zipf最大14.72%、有效28.09，模拟分位数约19.59%，
    启发式约16.29%，说明限制。一个50%暴露加399笔分摊余额，HHI=.25+
    .25/399，有效约3.99；PD 1%、全损时99.9%分位数至少50%，与其余依赖无关。

上方英文来源表的原始文献、官方记录和数据链接同样适用于中文内容。完整连续
成片听审仍待完成，数值、信号与时间检查不等于听审认证。

## Additional pause-question answers / 其他暂停题答案

- **Share risk rises at fixed asset value.** In the Merton comparison, ΔB=−ΔE.
  A 10% equity gain is a debt loss of .1E dollars, not necessarily 10% of debt.
  资产固定时债务价值变化等于权益变化的负数，不是债务也必然变化百分之十。
- **Equal leverage, different equity volatility.** Distance also needs consistent
  asset volatility, drift, horizon and boundary. Bank funding and regulatory
  mechanisms require a different audit. 相同杠杆不能独立确定距离，银行还有存款、
  融资与监管机制。
- **Leland barrier and volatility.** At fixed coupon, tax and rate,
  V_B=(1−tax)C/(r+σ²/2) falls with σ; shareholders value waiting. The optimal
  coupon can change separately. 固定票息等条件下，波动增加使边界下降，整体最优
  票息与杠杆是另一个比较。
- **Hazard doubles before default.** In flat deterministic RMV pricing the
  bond value multiplies by exp[−(1−R)λ_old T]. Other recovery conventions need
  their own repricing. 违约前风险重估也会使债价下跌，须使用实际回收与曲线惯例。
- **Every hotel in one city.** Sector, location and local-demand concentrations
  remain beyond a generic corporate factor; finite-name sizes matter too.
  同城酒店共享行业、地域与需求冲击，贷款多不代表充分分散。
- **Correlation and no defaults.** In the stated homogeneous Gaussian pool with
  fixed marginals, greater common correlation increases joint survival and
  clusters bad outcomes. 均值不变可以同时出现更多零违约和更重联合损失。
- **Which tranche gained?** State funded versus protection position; a capped
  senior tranche needs its own dependence sensitivity and premium legs.
  必须说明买卖保护方向，不能把封顶优先层与超优先止损混同。
- **Reported VaR halves on unchanged positions.** Reconcile old/new inputs,
  units and conventions, independently validate implementation and test liquidity,
  concentration and nonlinear stresses. 更低报告值不证明经济暴露下降。
- **ETF 5% below NAV.** Check timestamps, stale quotes, executable bond prices,
  bid-ask costs and creation/redemption constraints before naming a wrong price.
  净值与交易价格使用的信息和可执行条件不同，折价本身不能判错。
- **Private-fund volatility and Sharpe.** Audit cash flows, distributions, fees,
  leverage, marks, serial dependence, defaults and stressed exits. 波动差距不能
  唯一识别底层风险或估值平滑。

For the spread pause question's supplied physical rate .3% and LGD 60%, the
first-order annual expected loss is .003×.6=.0018, or 18 bp. The arithmetic
remainder of a 200 bp yield gap is 182 bp; it cannot be uniquely assigned to a
risk premium because liquidity, duration, instrument differences and the
approximation remain. 利差暂停题给定实际事件率0.3%、违约损失率60%，一阶
预期年损失18基点，200基点差额中算术剩余182基点，不能唯一归为风险溢价。

The final explanatory pass distinguishes physical expected loss from the CDS
pricing intensity, and corrects the spread-literature interpretation. Merton
maturity curves compare alternative terminal debts rather than sequential
survival observations. In the fixed Leland grid, total firm value peaks near
coupon 6.5 while debt value peaks near 8.5; those are different objectives.
最终讲解明确实际预期损失与CDS定价强度的区别。Merton期限曲线比较不同
终点债务，不是依次存续的观测。固定Leland网格中，企业总值在票息约6.5
处最高，债务价值在约8.5处最高，两者是不同目标。
