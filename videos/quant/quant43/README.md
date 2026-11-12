

# Quant, Built — Part 43: Can You Beat the Market?

The last part of the forty-three-part series asks what a claim of investment skill means, which evidence can support it, and where the assumptions enter. It combines Sharpe's holdings identity, stylised Gaussian fund populations, competitive Bayesian allocation, historical return statistics, careful pricing-summary comparisons and a return to Bachelier. The House is a teaching governance example. This part does not recommend or approve a portfolio.

The current visual pass is complete. Artifact-bound evidence in `docs/qa/quant43-polish-evidence.json` records current English and Mandarin construction, all 26 bilingual endpoint and 13 English motion sheets, native frames, exact concern intervals and sampled speech checks. Full continuous production-voice listening, pronunciation and mastering remain separately pending.

## Inputs and execution boundary

Eight unchanged ordinary originals were audited transitively and invoked exactly once each: `arith`, `luck`, `scale`, `adaptive`, `surface`, `bachelier`, `fdr`, `bg_theory`. All succeeded. The only public reader input is French daily factors through **2020-12-31**. The fund and allocation examples are fixed-seed simulations with known truth; they are not an empirical census of managers, a fitted fund database or a bootstrap of real fund returns.

The entire original `ensemble`, `record` and `research` functions are excluded. They would register/open/score strategy experiments or read their results. The apparently ordinary simulation prefix of the excluded research function is also excluded. No sealed outcome, final strategy, registry-derived performance statistic or substituted historical fit is used in the presentation.

The surface aggregation reads eight previously approved public derived JSON inputs: Part 13 `calibrate`, `levy_fits`; Part 12 `surface`; Part 14 `rbergomi`, `rheston`, `rb_replay`, `sigvol`; Part 10 `implied`. Each exact path was bound to a committed earlier approval before metadata or byte access, and every current hash matched. Their provenance does not imply identical statistical targets.

`common.load` accepts only the eight audited ordinary names and their exact hashes. Unknown/excluded names fail before path or counted-cache access. Missing or changed allowed outputs cannot compute implicitly. All eleven inherited rejected public keys remain barred before raw-cache/network access and the unchanged original checker. Financial algorithms, `compute.py` files and the protected manifest/envelope/track files remain unchanged. Existing counts are 23,561 through Part 42 and 23,562 through Part 43/globally; these are baseline counts, not new experiments.

Do not run the full `python -m videos.quant.quant43.compute` command: its default includes excluded originals. Do not rerun the completed once-only ordinary dispatcher. The existing pure check is `python -m pytest -q tests/test_quant_house.py -k test_skill_arithmetic_luck_berk_green_variance_ratio`; it passes without altering the financial library. Render inspection is a separate task.

## Chapters and scope

| Chapter | Question and evidence |
| --- | --- |
| Hook | Four scoped findings; selected success versus skill; data and method boundaries |
| Arithmetic | Same-universe value-weighted identity; costs; additive Gaussian active returns; noncentrality versus power; passive implementation |
| Luck | Explicit streak assumptions; simulated mixture and fresh null populations; tail-component estimates and realised false discovery proportion |
| Scale | Positive-part Bayesian allocation, finite sample associations, arbitrary asset units, gross value added versus fees and investor net returns |
| Adaptive | French total-market-return correlations and variance ratios through 2020; descriptive changes and identification limits |
| Record | Prospective evidence design; information, selection, costs, uncertainty, monitoring and complete reporting |
| Surface | Authenticated earlier public summaries with different metrics, quote filters and evaluation tasks |
| Open | Remaining empirical and methodological questions; bounded lessons rather than strategy outcome claims |
| Bachelier | Negative-forward support, nonpositive-strike extension, zero-rate pricing and explicit martingale conditions; dated clearing notices |
| Journey | Seven-act curriculum map, not a strategy outcome audit |
| House | Proposed cross-desk responsibilities and benchmark/evidence discipline; no capital or deployment approval |
| Research | Raw/capped Storey distinction, covariance variance, analytical expectations, BH/FDP/FDR and boundary-aware allocation proof |
| Outro | Scoped recap, six desk answers, twelve problems in 6/4/2 groups and complete solutions below |

The Journey now follows the canonical seven acts in `explainer/quant/__init__.py`: Markets and Money (1–3), Toolkit (4–8), Derivatives (9–22), Return Premia (23–29), Portfolios and the Firm (30–34), Microstructure (35–39), and System (40–42), followed by the separate finale (43).

## Scientific qualifications

### Holdings, costs and Gaussian luck

For one defined universe and period, value weights satisfy `w_P r_P + w_A r_A = r_M`, `w_P+w_A=1`. If passive holdings earn exactly the market return and `w_A>0`, then `r_A=r_M` before costs. After comparable costs, the active/passive difference is `-(c_A-c_P)`. This concerns a value-weighted aggregate, not the fraction of funds that win, every individual manager, different benchmarks or a general compounded wealth identity.

The Gaussian example instead assumes an **additive** cumulative active return `X_T ~ N(-cT, sigma_TE² T)` with fixed excess cost, stable volatility and independent increments. Hence `P(X_T>0)=Phi(-c sqrt(T)/sigma_TE)`. It is a model calculation, not a general probability of compounded portfolio wealth outperformance. The fee-growth illustration uses the chosen annual convention `1.07-f`; deducting a percentage of end-of-year assets would be a different convention.

The scaling `IR sqrt(T)` is a signal-to-noise noncentrality under stable iid assumptions. Setting it to two is not a guaranteed discovery date or a high-power test. A normal approximation at a critical value of two and noncentrality two has power about one half. Monitoring, multiplicity and time variation require separate treatment.

Pedersen's implementation discussion changes the market-portfolio and trading premises through issuance, repurchases and index changes; it does not refute a holdings identity conditional on its premises. SPIVA's **year-end 2024** report is cited as a dated, category-specific fund-count comparison: 65% of active large-cap U.S. equity funds underperformed the S&P 500 in 2024. That percentage is neither the holdings identity nor a forecast of current performance.

### Simulated funds and error criteria

The ordinary generator draws independent Gaussian monthly residuals for three chosen alpha groups. Calling the positive group “skilled” defines simulation truth; it does not identify skill in real funds. Its finite-sample zero-alpha t statistics have 239 degrees of freedom. Displayed standard-normal expected tail counts are labelled approximations. The separate zero-alpha reference population is not a resampling bootstrap.

The simplified BSW-style component is `max(0, S_right - pi0_hat gamma/2)` using a capped estimate of the **zero-alpha** share from two-sided p-values. Power, negative-alpha leakage into the right tail, clipping and the positive part affect interpretation. It is not a universal lower bound on the truly positive-alpha fraction, nor must the three estimated components sum to one.

For positive-alpha discovery, ordinary BH uses **one-sided** t p-values, with the true discovery null including zero and negative alpha. Let `V` be false selections and `R` all selections. `FDP=V/max(R,1)` is one realised proportion; `FDR=E[FDP]` is an expectation over repeated samples. Valid null p-values and independence, or an applicable positive-dependence condition, justify ordinary BH control. One run's observed FDP does not verify expected control.

The original adaptive calculation estimates zero-alpha mass from **two-sided** p-values, which is not the full nonpositive-alpha discovery null. Its q scores are reverse cumulative minima of `pi0_hat m p_(k)/k`; they are estimates associated with a tail procedure, not posterior probabilities that individual funds are null. The sorting formula and a cap alone do not prove adaptive FDR control.

### Raw and capped null-share estimators

At a fixed `0<=lambda<1`, define `W=sum_i 1{p_i>lambda}`, raw `pi0_tilde=W/[m(1-lambda)]`, and capped `pi0_hat=min(1,pi0_tilde)`. With uniform null marginals,

`E pi0_tilde = pi0 + sum_alt P(p_i>lambda)/[m(1-lambda)] >= pi0`.

This uses linearity, not independence. Suitable superuniform nulls give a lower-bound statement. It is an expectation statement, not a pointwise confidence bound, and choosing lambda from the same data needs an additional argument.

The cap does not inherit the bound. If all p-values equal one `U~Uniform(0,1)`, all nulls are valid and `pi0=1`. At `lambda=1/2`, the raw estimator is 0 or 2 with equal probability, so its mean is 1. The capped estimator is 0 or 1, so its mean is 1/2. In general `E[min(1,X)]` differs from `min(1,E[X])`.

Writing `I_i=1{p_i>lambda}`, `q_i=P(p_i>lambda)`, the exact variance is

`Var(pi0_tilde) = [sum_i q_i(1-q_i) + 2 sum_(i<j) Cov(I_i,I_j)]/[m²(1-lambda)²]`.

Under independence the covariance terms vanish. Uniform nulls contribute `m0 lambda(1-lambda)` to the numerator; alternatives contribute their Bernoulli variances. Dependence need not always increase variance. Under the all-null equicorrelated-indicator example with feasible correlation `kappa`, the variance is `lambda[1+(m-1)kappa]/[m(1-lambda)]`; fixed positive kappa can give a nonzero limit. Indicator correlation is not Gaussian z correlation.

The research curves are analytical raw-estimator expectations, not an execution of any prefix of `compute_research`. For an alternative `Z~N(mu,1)`, two-sided p-values and `c=Phi^-1(1-lambda/2)`,

`P(p>lambda)=Phi(c-mu)-Phi(-c-mu)`.

Substitution with null share .8 gives the displayed curves. Bias decreasing with lambda is not universal for arbitrary alternative distributions. Clipped empirical means are not represented by clipping this analytical expectation.

### Allocation, selection and units

Let `mu_t=E[a|F_t]` be a correctly specified Bayesian mean, `b>0`, fee `f>=0`, and conditionally mean-zero noise. Competitive positive-part allocation is `A_t=max(0,(mu_t-f)/b)`, with hypothetical net alpha `eta_(t+1)=a-bA_t-f+epsilon_(t+1)`.

`E_t eta_(t+1)=min(mu_t-f,0)`. Thus raw net alpha has zero conditional mean on **positive allocations**, but can be negative at zero allocation. Invested-dollar alpha satisfies `E_t[A_t eta_(t+1)]=0` including the boundary. For `F_t`-measurable `X_t` with integrable products, the tower property gives `E[X_t A_t eta_(t+1)]=0`.

The proof concerns the stated information set and conditional population. Pooling repeated fund observations and selecting funds with positive assets in both current and **future** years changes the statistical problem. Original naive pooled slope standard errors are not general confidence intervals; finite slopes and survivor-selected mean asset changes do not prove a martingale property. The separate fixed-size simulation is descriptive, with population reference `sigma_a²/(sigma_a²+sigma_epsilon²)` under its assumptions.

The simulation's asset units are arbitrary. Fee revenue is `f A`; true gross value added is `(a-bA)A`. Neither is manager profit after operating expenses. Finite realised investor alpha need not equal its conditional expectation. Changing `b` while endogenously scaling `A` does not automatically remove decreasing returns: `b A=max(0,mu-f)` can remain unchanged.

### Historical market and pricing evidence

Adaptive-market charts use daily total-market returns (`Mkt-RF + RF`), trailing 1,260-observation windows sampled every 21 observations, and decade-specific descriptive estimates. A correlation is not directional accuracy, a causal learning estimate, a significance test or an executable trading return. Nonsynchronous trading, bid-ask effects, risks and market structure can matter. Variance-ratio population identities require weak stationarity and finite nonzero variance; a sample deviation from one is not by itself a causal test of market efficiency.

The pricing aggregation's original unit label is too broad. The presentation preserves numbers but labels their actual meaning:

| Rows | Metric and target |
| --- | --- |
| One-volatility Black, Heston, SSVI | Direct vega-weighted IV RMSE on 193 eligible targets; SSVI k/T/IV target equality with Part 13 was verified |
| Merton, Kou, VG, NIG | Calibrator price-over-market-vega residual RMS, including its numerical handling; not the separately available direct IV RMSE |
| Rough Heston/Bergomi | Direct IV RMSE on a narrower 175-quote input set; finite-model-IV masks enter error routines |

Part 10's flat-per-expiry second score uses actual next-day marks on common expiries. Part 14's rough replay uses mean minimum training-trace scores versus final parameters on fresh paths against the **same dated quotes**; these first/second scores need not use the same parameters. Signature volatility compares final parameters on fitted/fresh paths against the same quotes. Fresh random numbers test numerical fit sensitivity, not next-day market or realised hedge P&L. The retrospective marks pool is not a simultaneous executable snapshot. These differences prevent a single common-design ranking; calibration error does not alone establish hedge quality, necessity of roughness or adoption suitability.

### Bachelier, support and measure

For a zero-rate risk-neutral normal forward `F_T~N(F,s_N²)`, `s_N=sigma_N sqrt(T)>0`, the call is `(F-K)Phi(d)+s_N phi(d)`, `d=(F-K)/s_N`. Nonzero deterministic rates require discounting. Normal volatility has absolute price units; setting `sigma_N=F sigma` matches a local diffusion coefficient, not exact ATM prices.

A positive unshifted Black forward cannot cross zero. A **negative underlying forward** is outside that model. But at a nonpositive strike on a **positive** terminal forward, a call's payoff is always `F_T-K`; its zero-rate price is `F-K` (or `DF(F-K)` in the forward formulation). The original computation skipped these entries; the presentation supplies this analytical extension without changing the financial algorithm.

The CFTC confirms the May WTI contract's -$37.63 settlement on 20 April 2020 and describes coinciding factors, not a complete root-cause decomposition. CME Clearing notice 20-171, dated 21 April, changed valuation for specified products from the end-of-day 22 April margin cycle. Notice 20-320 later returned products to Whaley or Black 76 from 31 August depending on product. These dated clearing notices do not describe every transaction's price or current universal policy.

A predictable stochastic integral against a martingale has zero expected gain only when it is a true integrable martingale; bounded predictable holdings and a square-integrable martingale on a finite horizon provide a sufficient example. A local martingale or mere predictability is insufficient. Risk-neutral pricing does not imply zero physical expected excess returns, and Sharpe's holdings identity is a separate accounting statement.

## Six desk questions, with answers

1. **A selected fund won five years running among 2,000. Skill?** Specify the null, the selection procedure, costs and dependence. Under independent symmetric annual wins the marginal streak probability is 1/32, giving an expected 62.5 streaks. If funds are independent too, at least one streak is overwhelmingly likely. These assumptions are not consequences of zero expected alpha. A pre-specified fund, a selected maximum and a population-level tail test are different inference problems.
2. **When does aggregate active money trail passive money?** In the same-universe holdings identity, passive earns the market, active weight is positive, and comparable active costs exceed passive costs. The net gap is the cost difference. Changing universes, flows or passive implementation changes the premises. A fund-count scorecard is a different object.
3. **Who benefits from skill?** It depends on scale, information, fees, competition and costs. Under the stated Bayesian competitive allocation, positive allocations have zero expected net alpha and skill can be associated with size and fee revenue. That model neither guarantees real investor returns nor equates fee revenue with manager profit.
4. **A strategy worked for fifty years. What now?** Examine information timing, mechanism stability, risks, costs, capacity and independent evaluation. A change in historical correlation does not identify learning or establish that the strategy will fail. No automatic capital decision follows from age alone.
5. **Research Sharpe is 2. What is future Sharpe?** No universal conversion follows. A justified model needs selection, sampling uncertainty, benchmark and distribution-shift assumptions, with independent evidence. A descriptive cross-sectional regression from unrelated rows would not itself be a causal decay estimate or universal forecast.
6. **Does the raw Storey bound survive clipping?** Not generally. Perfectly dependent uniform null p-values at lambda 1/2 give raw mean 1 and capped mean 1/2, although the true null share is 1. Valid marginals justify the raw identity; clipping changes the random variable.

## Problems with complete solutions — 6 foundational, 4 advanced, 2 qualifying

### Foundations: 1–6

1. **Holdings and costs.** Passive owns .4 of the same defined market and earns .08; the market earns .08. Derive active return and the net gap if active costs are one percentage point higher.

   **Solution.** With active weight .6, `.08=.4(.08)+.6 r_A`. Subtract .032 and divide by .6: `r_A=.08`. If costs are `c_A,c_P` with `c_A-c_P=.01`, then `(.08-c_A)-(.08-c_P)=-.01`. The result is an aggregate value-weighted one-period identity with positive active weight. It does not rank individual funds or determine how many outperform.

2. **Gaussian luck.** Zero skill, excess annual cost .0075, annual tracking error .04, horizon 10. Find positive cumulative active-return probability in the additive iid Gaussian model.

   **Solution.** `X_10~N(-.075,.04²·10)`. Standardising zero gives threshold `.075/(.04 sqrt(10))=.592927`. Thus `P(X_10>0)=1-Phi(.592927)=Phi(-.592927)≈.2766`. The result uses stable independent Gaussian increments and additive active returns; general compounded wealth requires a different model.

3. **Expected significant nulls.** Among 2,000 marginal standard-normal null statistics, find expected counts above 1.96 and 3. Is cross-test independence needed?

   **Solution.** Let `N_c=sum_j 1{Z_j>c}`. Linearity yields `E N_c=2000[1-Phi(c)]`, regardless of cross-test dependence. At 1.96 this is about 50.0; at 3 it is about 2.70. These are one-sided counts. Independence matters for distributions such as `P(max Z_j>c)` or count variance, not the expectation. The original fund t statistics have finite degrees of freedom, so these normal-tail counts are labelled approximations when used as references there.

4. **Raw and capped estimates.** Of 1,000 p-values, 300 exceed .5. Compute both estimates. Are they confidence bounds?

   **Solution.** `pi0_tilde=300/[1000(1-.5)]=.6`; `pi0_hat=min(1,.6)=.6`. Neither number is automatically a confidence bound. The raw expectation identity assumes valid null marginals and a fixed threshold and averages over repeated samples; it does not put this realised estimate above the true null fraction. Dependence and alternative tails affect uncertainty, and clipping changes expectation properties.

5. **Tail component.** Capped null estimate .8, two-sided level gamma .2, right-tail share .09. Compute the helper's positive-part estimate and interpret it.

   **Solution.** Estimated lucky zero-null share is `.8·.2/2=.08`. The helper returns `max(0,.09-.08)=.01`, or 1%. This is a tail-component estimate. It is not known true positive-alpha mass or an individual posterior probability. Positive alternatives can miss the tail, negative alternatives can enter it, the null estimate is capped, and the final positive part is nonlinear. Those facts prevent a universal lower-bound claim from the raw expectation proof alone.

6. **Competitive allocation.** Posterior mean .04, fee .01, b .001 per asset unit. Find allocation, conditional net alpha and fee revenue.

   **Solution.** `A=max(0,(.04-.01)/.001)=30` units. It is interior, so `E_t eta=.04-.001·30-.01=0`. Fee revenue is `.01·30=.3` asset units per period. It is revenue rather than profit after operating costs. The posterior mean is not realised true skill; a finite realised net return can differ from zero. At a posterior below the fee, allocation is zero and hypothetical net alpha can have negative conditional mean, but invested-dollar alpha is zero.

### Advanced: 7–10

7. **Variance ratios.** Weakly stationary returns have finite nonzero variance, rho1=.2 and all higher autocorrelations zero. Derive VR2 and VR5 and explain the scope.

   **Solution.** Expanding a q-period sum's variance gives `Var(sum r)=q gamma0 + 2 sum_(k=1)^(q-1)(q-k) gamma_k`. Divide by `q gamma0`: `VR(q)=1+2 sum_(k<q)(1-k/q)rho_k`. Hence `VR(2)=1+rho1=1.2`, and `VR(5)=1+2(4/5)(.2)=1.32`. This is a population stationarity identity. A sample estimator has uncertainty and can reflect nonsynchronous trading, changing moments and other mechanisms; it does not by itself identify a causal learning effect or executable alpha.

8. **Family-wise selection.** Twenty tests have valid marginal standard-normal null statistics. Find a one-sided threshold with family-wise error at most .05, without independence.

   **Solution.** By the union bound, `P(any false exceedance)<=sum_j P(Z_j>c)<=20[1-Phi(c)]` under the complete null; for a partial null, at most twenty null terms remain. Set each marginal tail to `.05/20=.0025`: `c=Phi^-1(.9975)≈2.8070`. Independence is unnecessary for this conservative bound, but valid marginal null tails are essential. This controls the probability of at least one false rejection; it is not an FDR threshold, an expected maximum, a posterior skill probability or a guarantee against every adaptive analysis.

9. **Correlated indicators.** All tests are null, lambda=.5, m=1,000, feasible pairwise indicator correlation kappa=.3. Find raw-estimator variance and its large-m limit.

   **Solution.** Each `I_i=1{p_i>.5}` has mean .5 and variance .25. Each pair has covariance `.3·.25=.075`. Therefore `Var(W)=1000(.25)+1000·999(.075)`. Divide by `[1000(.5)]²` to obtain `.3007`. Equivalently the formula is `[1+999(.3)]/1000`. The standard deviation is about .5484. With fixed kappa, the limit is `kappa lambda/(1-lambda)=.3`; under independence the variance would be .001. This is indicator correlation, not an assumed Gaussian z-score correlation, and is about the uncapped estimator. Feasible dependence can be constructed by mixing a shared uniform draw with independent uniform draws at the family level.

10. **Option domains.** Normal call: F=K=100, sN=10. Separately, positive zero-rate Black forward F=10 and strike -5. Price the calls.

    **Solution.** For the normal ATM call, `d=0`, so `C=sN phi(0)=10/sqrt(2 pi)≈3.98942`. In the separate Black model, `F_T>0` almost surely and `K=-5`, so payoff `(F_T+5)^+=F_T+5`. Risk-neutral forward expectation is 10, hence price is 15 at zero rates. No logarithm of F/K is needed for this extension. It does not make a negative underlying forward compatible with unshifted positive lognormal dynamics. Nonzero deterministic rates multiply the forward-payoff expectation by the discount factor.

### Qualifying examination: 11–12

11. **Null-share estimator in full.** Prove the raw expectation identity, derive general and independent variance formulas, and give a clipping counterexample.

    **Solution.** Fix `m>=1` and `0<=lambda<1`. For each i let `I_i=1{p_i>lambda}`, `q_i=P(p_i>lambda)`. Assume uniform null marginals; do not assume joint independence. Since indicators are integrable, `E W=sum_i q_i=m0(1-lambda)+sum_alt q_i`. Dividing by `m(1-lambda)` gives `E pi0_tilde=pi0+sum_alt q_i/[m(1-lambda)]>=pi0`. Equality holds exactly when the sum of alternative large-tail probabilities is zero. For superuniform nulls, null tail contributions are at least `1-lambda`, giving an inequality rather than the same equality. The threshold is fixed; a data-chosen threshold is a different random object.

    Expanding the variance of a sum gives `Var(W)=sum_i q_i(1-q_i)+2 sum_(i<j) Cov(I_i,I_j)`. Divide by `m²(1-lambda)²` for the raw-estimator variance. Under independence the covariance terms vanish; uniform nulls contribute `m0 lambda(1-lambda)` and alternatives contribute their Bernoulli variances. Under the full independent null this reduces to `lambda/[m(1-lambda)]`. For bounded independent indicators at fixed lambda, variance is O(1/m), but remaining alternative-tail bias need not vanish; variance shrinking alone does not prove consistency for pi0.

    If all-null indicators have feasible common pairwise correlation kappa, each covariance is `kappa lambda(1-lambda)`, yielding `lambda[1+(m-1)kappa]/[m(1-lambda)]`. Fixed positive kappa produces a nonzero limit; arbitrary dependence can also have different signs or rates. Gaussian factor correlation cannot simply be substituted for indicator correlation.

    For clipping, set every p-value equal to one `U~Uniform(0,1)`, so all nulls are individually valid and pi0=1. At lambda=.5, `W=m 1{U>.5}` and `pi0_tilde=2 1{U>.5}`. Thus `E pi0_tilde=1`, but `E min(1,pi0_tilde)=E1{U>.5}=.5`. This disproves a general capped upward-expectation bound. It also explains why clipping the analytical mean is not the same as averaging clipped samples, and why a raw expectation proof alone does not establish a nonlinear BSW component bound or adaptive FDR control.

12. **Competitive Bayesian allocation, including the boundary.** Prove the zero-dollar-alpha result and its predictable-information consequence.

    **Solution.** Let `mu_t=E[a|F_t]`, `b>0`, `f>=0`, `A_t=max(0,(mu_t-f)/b)`, and `eta_(t+1)=a-bA_t-f+epsilon_(t+1)`, where `E[epsilon_(t+1)|F_t]=0`. Allocation is F_t-measurable. First take conditional expectations: `E_t eta=mu_t-bA_t-f`. If `mu_t>f`, allocation is positive, `bA_t=mu_t-f`, and the conditional mean is zero. If `mu_t<=f`, allocation is zero and the hypothetical net-alpha conditional mean is `mu_t-f<=0`. Thus `E_t eta=min(mu_t-f,0)`, not universally zero.

    Assume `A_t eta` is integrable. Since A_t is measurable, `E_t[A_t eta]=A_t E_t eta`. In the interior the second factor is zero; at the boundary the first factor is zero. Hence the conditional expected invested-dollar alpha is zero everywhere. Equivalently, `1{A_t>0} eta` has conditional mean zero when integrable. Raw hypothetical net returns for inactive funds need not have that property.

    For F_t-measurable X_t with integrable `X_t A_t eta`, the tower property gives `E[X_t A_t eta]=E[X_t E_t(A_t eta)]=0`. To describe covariance, also require the relevant moments to exist; expected dollar alpha is zero, so the product identity implies orthogonality. A sample conditioned on positive future assets includes information not necessarily in F_t and need not satisfy this moment condition. Repeated observations sharing manager skill invalidate naive independent-row regression standard errors in general. Correctly specified Bayesian beliefs, mean-zero noise, competitive frictionless reallocation and the linear scale model are substantive assumptions; the proof is not an empirical guarantee for actual managers.

## Sources

- [Sharpe, The Arithmetic of Active Management (1991)](https://web.stanford.edu/~wfsharpe/art/active/active.htm).
- [Pedersen, Sharpening the Arithmetic of Active Management (2018)](https://rpc.cfainstitute.org/research/financial-analysts-journal/2018/faj-v74-n1-4).
- [SPIVA U.S. Year-End 2024](https://www.spglobal.com/spdji/en/spiva/article/spiva-us-year-end-2024/), used as a dated report.
- [Fama and French, Luck versus Skill (2010)](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2010.01598.x/full).
- [Barras, Scaillet and Wermers, False Discoveries in Mutual Fund Performance (2010)](https://terpconnect.umd.edu/~wermers/FDR_published.pdf).
- Storey (2002), *A Direct Approach to False Discovery Rates*; Benjamini and Hochberg (1995), *Controlling the False Discovery Rate*; Berk and Green (2004), *Mutual Fund Flows and Performance in Rational Markets*; Lo (2004), *The Adaptive Markets Hypothesis*; Berk and van Binsbergen (2015), *Measuring Skill in the Mutual Fund Industry*; Pástor, Stambaugh and Taylor (2015), *Scale and Skill in Active Management*; McLean and Pontiff (2016), *Does Academic Research Destroy Stock Return Predictability?*
- [CME Clearing 20-171](https://www.cmegroup.com/notices/clearing/2020/04/Chadv20-171.html), [CME Clearing 20-320](https://www.cmegroup.com/notices/clearing/2020/08/Chadv20-320.html), and [CFTC 8315-20](https://www.cftc.gov/PressRoom/PressReleases/8315-20).
- [Bachelier's 1900 thesis](https://www.numdam.org/item/ASENS_1900_3_17__21_0/). Earlier public pricing inputs retain their committed provenance; these notes do not instruct a new fit or sealed-data opening.

---

# 量化金融，从零搭建 — 第43部分：你能战胜市场吗？

四十三部分的最后一部分讨论“技能”主张需要什么证据，以及每个结论的假设。内容包括夏普持仓恒等式、简化高斯基金总体、竞争性贝叶斯资金配置、历史收益统计、定价汇总的可比性与巴舍利耶模型。公司是治理教学示例，不是投资建议或投资组合批准。

**当前视觉检查尚在进行。** 历史构建说明不等于本轮批准；必须检查当前英文、中文构建输出、最终端点图、运动图、精确问题区间及抽样语音，并绑定最终证据。

## 输入与执行边界

八个经完整传递源代码审计的普通原始计算各执行一次且全部成功：`arith`、`luck`、`scale`、`adaptive`、`surface`、`bachelier`、`fdr`、`bg_theory`。唯一公共读取器输入为截止二〇二〇年十二月三十一日的弗伦奇日因子。基金与配置例子使用固定种子模拟，真值按构造已知；不是实际基金普查、经验拟合或真实收益自助抽样。

整个`ensemble`、`record`、`research`原始函数均排除，因为它们会登记、打开、评分封存策略实验或读取结果。被排除研究函数中看似普通的模拟前缀也不执行或复用。演示不使用封存策略结果、最终策略、登记表推导的业绩数值或替代历史拟合。

曲面汇总仅复用上方列明的八个已批准公共派生文件。每个精确路径先与已提交的既有证据哈希绑定，再读取元数据和字节；当前哈希全部匹配。来源被认证不代表统计目标相同。

`common.load`只接受八个普通名称和精确哈希。未知或排除名称在路径和计数缓存访问前拒绝；允许项目缺失或变化时也不会隐式计算。十一条继承的拒绝公共键在原始缓存、网络与原检查器前继续拦截。金融算法、所有`compute.py`及受保护清单、信封、记录文件保持原样。既有累计次数为第42部分截止23,561，第43部分与全局23,562；没有新增实验。

**不要运行完整默认计算命令，也不要重跑已经完成的一次性调度器。** 默认原始脚本包含被排除函数。既有纯技能测试通过，但不代替图像和语音检查。

## 科学范围

同一确定市场和期间内，价值权重满足`w_P r_P+w_A r_A=r_M`。若被动组合确实赚市场收益、主动权重大于零，则主动总体扣费前也赚市场收益；可比成本的差额决定扣费后差距。这不是获胜基金数量比例、每个经理表现、跨市场比较或一般复利财富恒等式。发行、回购和指数调整会改变实际被动实施的持仓与交易前提。SPIVA二〇二四年年终报告中的65%是当年美国大盘主动股票基金相对标普500的基金数量比例，不是价值加权恒等式，也不是当前表现预测。

高斯例子假设**相加的**累计主动收益`X_T~N(-cT,sigma_TE² T)`、固定超额成本和独立稳定增量。因此正累计主动收益概率为`Phi(-c sqrt(T)/sigma_TE)`；不能直接解释为一般复利财富胜率。费用图采用选定的年度增长`1.07-f`，不是所有收费合同的统一约定。`IR sqrt(T)`是稳定独立模型中的非中心性信噪比。把它设为二不保证实际统计量超过二，也不构成高功效发现时间；正态近似中临界值与非中心性都为二时功效约一半。

基金总体有三个选定阿尔法组和独立高斯月残差。正组被称为“有技能”只是模拟真值的定义。零组t统计量有239自由度，正态尾部数量只作为近似参考。独立生成的零阿尔法总体并不是真实基金自助抽样。

简化尾部估计为`max(0,S_right-pi0_hat gamma/2)`。两侧p值估计的是**零阿尔法**份额；功效不足、负阿尔法备择进入右尾、上限截断与正部运算都影响解释，不能从原始期望证明推出普遍的正技能份额下界。

发现正阿尔法时，普通BH使用**单侧**t检验p值；真实发现零假设包括零与负阿尔法。`FDP=V/max(R,1)`为一次实现的错误发现比例，`FDR=E[FDP]`才是重复抽样平均。有效零假设p值与独立性或适用的正依赖条件支持BH控制。一次实现的FDP不能验证期望FDR。原始自适应计算用双侧p值的封顶估计，目标零阿尔法份额不同于完整非正阿尔法零假设；其q分数不是单只基金为假的后验概率，也不自动保证自适应错误控制。

### 原始与封顶空比例估计

固定`0<=lambda<1`，记`W=sum 1{p_i>lambda}`，原始`pi0_tilde=W/[m(1-lambda)]`，封顶`pi0_hat=min(1,pi0_tilde)`。若零假设边际p值均匀，则

`E pi0_tilde=pi0+sum_alt P(p_i>lambda)/[m(1-lambda)]>=pi0`。

这只需期望线性性，不需独立。适当超均匀零假设给出下界，但不一定同样的等式。结论是固定阈值的期望性质，不是每个样本的置信下界；数据选择阈值需要另证。

封顶不继承此性质。令所有p值等于同一个均匀随机变量U，所有零假设都有效，真份额为一。lambda为二分之一时，原始估计以相同概率取零或二，均值一；封顶估计取零或一，均值二分之一。`E min(1,X)`不等于`min(1,EX)`。

若`I_i=1{p_i>lambda}`、`q_i=P(p_i>lambda)`，精确方差为

`[sum q_i(1-q_i)+2 sum_(i<j) Cov(I_i,I_j)]/[m²(1-lambda)²]`。

独立时协方差消失；零假设部分贡献`m0 lambda(1-lambda)`，备择另贡献伯努利方差。依赖不一定总增加方差。全零假设、可行固定正指标相关kappa的例子给出方差`lambda[1+(m-1)kappa]/[m(1-lambda)]`，极限可不为零。指标相关不是高斯z统计量相关。

研究曲线为解析原始期望，不执行被排除函数的任何前缀。备择`Z~N(mu,1)`且用双侧p值时，令`c=Phi^-1(1-lambda/2)`，大p值概率为`Phi(c-mu)-Phi(-c-mu)`；代入真空比例.8得到曲线。任意备择分布下，提高lambda不保证偏差单调下降；封顶解析均值也不是封顶随机估计的平均。

### 配置证明与选择限制

正确贝叶斯均值`mu_t=E[a|F_t]`、正规模成本b、非负费用f与条件均值为零噪声下，配置`A_t=max(0,(mu_t-f)/b)`。假想净阿尔法`eta=a-bA_t-f+epsilon`的条件期望是`min(mu_t-f,0)`：正配置时为零，零配置时可以为负。但实际投入资金阿尔法`A_t eta`的条件期望在两种情况都为零。满足可积性、X为当前信息可测时，塔性质给出`E[X A_t eta]=0`。

原始模拟回归重复使用同一基金观测，并选取当年与**未来**都有资产的基金。这不是证明所用条件总体。朴素混合回归标准误不是一般置信区间，有限斜率或生存者选择的资产变化均值也不证明鞅性质。模拟资产是任意单位；费用收入`fA`不是扣除运营开支后的利润，真正毛阿尔法增加值为`(a-bA)A`。改变b而让A内生反向缩放，不等于移除规模递减。

历史图采用总市场日收益、1260观测滚动窗、每21观测抽取一次和分年代描述量。相关性不是方向预测正确率、因果学习效应或可执行利润。方差比总体恒等式需要弱平稳与有限非零方差；样本偏离一不直接识别市场效率的原因。

### 定价指标与巴舍利耶

单一波动率Black、Heston、SSVI的汇总为193个合格目标上的直接vega加权隐含波动率RMSE。SSVI目标k、T、IV与第13部分逐项一致已验证。跳跃模型四行则取价格除以市场vega的残差RMS，**不是**其另存的直接IV RMSE。粗糙模型输入集合较窄，为175条报价，误差还受有限IV掩码影响。名义同为波动率点不代表目标相同。

第10部分第二列为共同到期日的真实次日报价；第14部分粗糙重放为训练轨迹最小误差与最终参数新随机路径误差，仍比较同一天报价，参数还可能不同。签名波动率比较最终参数在训练/新路径上的误差，也不是次日行情或实际对冲盈亏。来源池是回顾性时间窗标记集合，不是同时可执行报价。混合表格不能给出统一公平排名、粗糙性必要性或部署批准。

零利率风险中性正态远期模型的看涨价格为`(F-K)Phi(d)+sN phi(d)`，`d=(F-K)/sN`。非零确定利率需贴现。`sigma_N=F sigma`只匹配局部扩散系数，不精确匹配平值价格。正的未平移Black远期不越零，负标的远期不在模型支持内。但正终值远期上的非正执行价看涨，其支付总是`F_T-K`，零利率价格为`F-K`；原始计算跳过该条目，演示给出解析延伸而不改算法。

CFTC确认二〇二〇年四月二十日五月WTI合约结算为-37.63美元，并列出同时出现的因素，不给出完整根因分解。CME清算20-171对指定产品在四月二十二日收盘保证金周期起改用Bachelier；20-320又规定八月三十一日起按产品回到Whaley或Black76。这些历史清算估值通知不代表全部成交定价或当下普遍规则。

可预测持仓对鞅的随机积分要成为真可积鞅，才能断言期望收益为零；有限期间内有界可预测持仓与平方可积鞅是充分例子。只有可预测性或局部鞅不够。风险中性测度结论不等于真实测度下零超额收益，夏普恒等式也是独立的会计结论。

## 六个交易台问题与答案

1. **两千只基金中选出的连续五年赢家有技能吗？** 要明确零假设、选择、成本与依赖。独立对称年度胜负时单只连胜概率1/32，期望数量62.5；再假设基金独立，至少一个连胜几乎必然，但不是严格确定。这不由零期望阿尔法自动推出。预先指定的基金、事后最大值与总体尾部检验是不同推断。
2. **主动总体何时落后被动？** 同一市场持仓恒等式、被动确实持有市场、主动权重为正，且可比主动成本更高时，净差额等于负的成本差。改变市场、资金流或被动实施会改变前提；基金数量记分卡不是同一对象。
3. **技能归谁？** 取决于规模、信息、费用、竞争与开支。指定竞争性贝叶斯模型中正配置期望净阿尔法为零，技能可与规模和费用收入相关；不保证实际投资者收益，也不把收入等同利润。
4. **策略成功五十年后做什么？** 检查信息时点、机制稳定性、风险、成本、容量及独立评估。历史相关变化不识别学习原因，也不证明策略必失败；年限本身不批准资本决策。
5. **研究夏普为二，未来是多少？** 没有普遍换算系数。需说明选择、抽样不确定性、基准与分布变化模型，并取得独立证据。异质行的描述回归不是因果衰减或普遍预测。
6. **封顶保留原始Storey下界吗？** 不一般保留。完全相依均匀零假设、lambda二分之一时原始均值一，封顶均值二分之一，真份额为一。边际有效与线性性证明原始恒等式，截断改变随机变量。

## 十二题完整解答：六基础、四进阶、二资格考试

### 基础1—6

1. **持仓与成本。** 被动权重.4，市场和被动收益均.08，主动成本高一个百分点。

   **解：** `.08=.4(.08)+.6r_A`，移项得到`.048=.6r_A`，故`r_A=.08`。设`c_A-c_P=.01`，净差`(.08-c_A)-(.08-c_P)=-.01`。这是同一确定市场中正主动权重的价值加权单期总体恒等式，不决定个别基金名次或获胜数量。

2. **高斯运气。** 零技能、年超额成本.0075、跟踪误差.04、十年相加收益胜率。

   **解：** `X_10~N(-.075,.04²·10)`。零点标准化阈值为`.075/(.04 sqrt(10))=.592927`，所以`P(X>0)=1-Phi(.592927)=Phi(-.592927)≈.2766`。必须假设稳定独立高斯增量，不能直接用于一般复利财富。

3. **显著零假设数量。** 两千个边际标准正态统计量超过1.96和3的期望数量，是否需要跨检验独立？

   **解：** `N_c=sum 1{Z_j>c}`，线性性给`EN_c=2000[1-Phi(c)]`，分别约50.0与2.70，均为单侧尾部。不需要跨检验独立；最大值概率与计数方差才依赖联合分布。原始基金t统计量自由度有限，因此正态数量在该处只是近似参考。

4. **原始与封顶估计。** 一千个p值中三百个超过.5。

   **解：** 原始为`300/[1000(1-.5)]=.6`，封顶`min(1,.6)=.6`。两者都不自动是置信界。固定阈值和有效边际支持重复抽样期望性质，不保证当前实现高于真份额。依赖与备择尾部影响不确定性，封顶又改变期望性质。

5. **尾部成分。** 空份额封顶估计.8、双侧水平.2、右尾份额.09。

   **解：** 估计幸运零组份额`.8·.2/2=.08`，正部结果`max(0,.09-.08)=.01`，即1%。它不是已知真实正阿尔法质量，也不是个体后验概率。正备择可漏检、负备择可入右尾，加上两次非线性，不能仅由原始期望证明推出普遍下界。

6. **竞争配置。** 后验均值.04、费率.01、每资产单位规模成本.001。

   **解：** `A=max(0,(.04-.01)/.001)=30`单位，为内点。条件净阿尔法`.04-.001·30-.01=0`，费用收入`.01·30=.3`资产单位/期，收入不是扣运营成本利润。后验均值不等于已实现真技能，有限实现不必为零。均值低于费用时资产为零，假想净收益条件均值可负，但实际投入资金阿尔法仍为零。

### 进阶7—10

7. **方差比。** 弱平稳、有限非零方差，rho1=.2，高阶相关为零。

   **解：** 展开q期和方差为`q gamma0+2 sum_(k=1)^(q-1)(q-k)gamma_k`，除以`q gamma0`，得`VR(q)=1+2 sum_(k<q)(1-k/q)rho_k`。因此`VR2=1.2`，`VR5=1+2(.8)(.2)=1.32`。这是总体恒等式；样本量有误差，也可能受不同步交易、时变矩和其他机制影响，不能单独识别学习原因或可执行收益。

8. **族错误。** 二十个有效标准正态单侧检验，将至少一个错误拒绝的概率控制在.05以内。

   **解：** 并集界给`P(any false)<=sum_j P(Z_j>c)<=20[1-Phi(c)]`。部分零假设时真实零组项不超过二十。令单项尾部`.05/20=.0025`，得`c=Phi^-1(.9975)≈2.8070`。不需独立，但需有效边际尾概率。控制的是族错误概率，不是FDR、期望最大值、技能后验概率或全部自适应搜索的统一保证。

9. **相依指标。** 全零假设、lambda=.5、m=1000、可行指标相关kappa=.3。

   **解：** 单项均值.5、方差.25，成对协方差`.3·.25=.075`。`Var W=1000(.25)+1000·999(.075)`，除以`[1000(.5)]²`得`.3007`，标准差约`.5484`。一般式为`[1+(m-1)kappa]/m`，固定kappa时极限`.3`；独立时方差`.001`。这是原始估计且相关是指标相关，不能替换为z相关。可在总体层面以一定概率采用共同均匀抽样、其余采用独立均匀抽样，构造所需可行依赖。

10. **期权支持域。** 正态平值F=K=100、sN=10；另一个正Black远期F=10、K=-5、零利率。

    **解：** 正态d=0，`C=10 phi(0)=10/sqrt(2pi)≈3.98942`。另例中Black终值远期严格正，故支付`(F_T+5)^+=F_T+5`，风险中性期望为15，零利率价格15，不需计算负比值对数。该解析延伸并不让负标的远期进入未平移正对数正态支持域。非零确定利率时贴现远期支付期望。

### 资格考试11—12

11. **完整空比例估计。** 证明原始期望、一般协方差方差、独立特例，并给出封顶反例。

    **解：** 固定`m>=1`、`0<=lambda<1`，令`I_i=1{p_i>lambda}`、`q_i=P(p_i>lambda)`。假设零组边际均匀，不假设联合独立。指标可积，故`EW=sum_iq_i=m0(1-lambda)+sum_altq_i`。除以`m(1-lambda)`得到原始期望为`pi0+sum_altq_i/[m(1-lambda)]>=pi0`。等号恰在备择尾概率和为零时成立。超均匀零组只支持相应不等式；阈值若由数据选择，已是另一随机对象。

    展开和的方差，`Var W=sum_iq_i(1-q_i)+2sum_(i<j)Cov(I_i,I_j)`；再除以平方分母。独立时交叉协方差消失，零组贡献`m0 lambda(1-lambda)`，备择贡献各自伯努利方差。全独立零组化为`lambda/[m(1-lambda)]`。固定lambda时独立有界指标方差为O(1/m)，但备择污染偏差可不消失，方差缩小本身不证明对pi0一致。

    全零组可行共同指标相关kappa时，成对协方差`kappa lambda(1-lambda)`，代入得到`lambda[1+(m-1)kappa]/[m(1-lambda)]`。固定正kappa产生非零极限；一般依赖可有不同符号和速度。高斯因子相关不能直接替代指标相关。

    反例令全部p值等于同一`U~Uniform(0,1)`，故每个零假设都有效、真份额一。lambda=.5时`W=m1{U>.5}`，原始估计`2·1{U>.5}`均值一，封顶估计`1{U>.5}`均值.5。故不存在一般的封顶向上期望保证，也说明截断解析均值不等于平均截断样本；原始证明不能直接证明非线性尾部成分下界或自适应FDR控制。

12. **含边界的竞争性贝叶斯配置。** 证明零条件期望投入资金阿尔法与塔性质结果。

    **解：** 设`mu_t=E[a|F_t]`，`b>0`、`f>=0`，`A_t=max(0,(mu_t-f)/b)`，`eta=a-bA_t-f+epsilon`，且`E_t epsilon=0`。A当前可测。条件期望`E_teta=mu_t-bA_t-f`。若mu大于费率，`bA=mu-f`，条件均值零；否则A为零，假想净阿尔法条件均值`mu-f<=0`。因此`E_teta=min(mu-f,0)`，不是无条件地处处为零。

    假设`A eta`可积，可提出可测A，得`E_t[A eta]=A E_teta`。内点第二因子零，边界第一因子零，所以投入资金阿尔法的条件均值处处零。可积时`1{A>0}eta`也有零条件均值，但不要求未投资基金的假想净收益具有此性质。

    对F_t可测的X，且`X A eta`可积，塔性质给`E[X A eta]=E[X E_t(A eta)]=0`。谈协方差还需相关矩存在；由于美元阿尔法均值零，乘积恒等式推出正交。若按未来正资产选择样本，条件包含当前信息外的未来量，不必满足此矩条件。重复基金观测共享技能，也一般不满足独立行朴素标准误条件。正确贝叶斯信念、条件均值零噪声、竞争性无摩擦重配与线性规模成本都是实质假设，不是实际经理的经验保证。

## 来源与检查

上方英文来源区提供原始论文、SPIVA历史报告、CME清算通知和CFTC报告链接。八个普通输出及八个复用公共输入均有精确哈希证据；不要重新拟合或打开被排除策略。最终视觉证据已完成，见 `docs/qa/quant43-polish-evidence.json`。语音抽样信号及时序检查已经完成；完整制作旁白的连续听审、发音检查及母带制作仍单独待做。

*Review log of the earlier QA passes on this part: [`docs/qa/quant/part43.md`](../../../docs/qa/quant/part43.md).*
