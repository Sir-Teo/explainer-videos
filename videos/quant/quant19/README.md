# Quant, Built — Part 19: Term-Structure Models

Part 19 of the [43-part series](../README.md). Part 18 built a discount curve; this part gives curves stochastic dynamics and prices rate options. The [syllabus](../SYLLABUS.md) and [reading map](../READING.md) describe the wider course.

> Scientific and bilingual review and current-source visual QA are complete. Full production-voice listening remains pending. Narration is approximately 60 minutes before animation and pauses.

## Data boundary and examples

The original `compute.py`, House algorithms and global data/experiment registries are unchanged. Only 22 permitted original descriptive examples were normally restored. Active scenes refuse `premia`, `premia_acm` and `envelope`: those legacy paths register or load forecast experiments involving sealed returns. This pass adds no market trial and opens no sealed strategy-return payload. Historical trial counts stay 315 through Part 19 and 23,562 globally.

Two separately named, fixed-seed numerical examples correct presentation problems without changing the original algorithms or their caches:

* [market_model_example.py](market_model_example.py) uses caplet resets at 0.5–5 years and payments at 1–5.5 years, with matching initial forward ratios. It samples each reset payoff with the payment/terminal bond ratio at that reset. The original demonstration mixed initial accrual and option-expiry time origins. The new example records individual Monte Carlo standard errors. Maximum deviations are 1.275% for Black and 0.719% for Bachelier, respectively 1.333 and 0.950 standard errors; finite Euler bias remains possible. Unbounded normal simple forwards are a local numerical approximation: positive bond ratios require `L > -1/delta`, and the example rejects paths that violate this domain. A finite successful sample does not certify global admissibility. Zero-volatility ATM values are zero.
* [reserve_example.py](reserve_example.py) solves a new volatility for each mean-reversion scenario to match the **same** European: 2-year expiry into an 8-year receiver swap at the same strike and target price. Maximum hedge-pricing error is below `1e-9` of notional. Numerical Bermudan grid prices range from 439.7 to 518.1 bp. This replaces post-hoc ratio rescaling. Matching one synthetic hedge is not fitting a market option surface; the range is a sensitivity scenario, not a fair-value bound, confidence interval or automatic accounting reserve.

Sources are the pinned Federal Reserve fitted Treasury curve (GSW), FRED and cited public records. Full-sample descriptive yield and return regressions are distinct from sealed forecast-return experiments. Current-vintage smoothed curves are not directly investable prices and do not establish point-in-time forecast performance. No data-manifest refresh is used. The legacy NY Fed ACM comparison is excluded because it depends on the blocked forecast payload.

## Chapters

1. **Opening: the bond massacre.** The Fed's 1994 tightening and Orange County illustrate leverage and nonlinear rate exposure. The SEC's June-1994 balance sheet has $19.8bn securities, $7.2bn participant deposits and $12.6bn reverse repos. Dividing a reported $1.5–1.7bn loss fraction by a five-year yield change is a rough duration-equivalent, not a measured portfolio duration: dates, funding and nonlinear exposures differ.
2. **Short-rate models.** Vasicek's Gaussian transition and CIR's nonnegative diffusion. Feller makes zero inaccessible when the initial state is positive; its failure does not permit negative CIR rates. The original monthly bill proxy is clipped at one basis point before both fits. Bill discount yields differ from instantaneous continuously compounded rates. Historical fits, parameter uncertainty, re-estimation bias and sampled fans are descriptive.
3. **Affine term structures.** Pricing-measure Feynman–Kac and Riccati equations, admissible state spaces, Vasicek/CIR limits and a two-factor Gaussian model. Using historical parameters in pricing formulas is explicitly illustrative. A drift gap equals diffusion loading times the market price of risk under a stated sign convention. Perfect positive instantaneous correlation applies to the positive loadings of this one-factor affine model, not every nonlinear one-factor model. The two factors resemble, but are not literally, empirical principal components.
4. **Hull–White.** With `x_0=0`, a deterministic shift fits the initial curve analytically. The drift intercept is not itself the mean-reversion target. This example fits historical yield-volatility proxies, not option-market quotes. Boundary fits in low-rate windows expose model misspecification. Gaussian state and integral simulation can be exact at sampled dates, while sample repricing still has uncertainty.
5. **HJM.** The money-market pricing-measure drift is fixed by forward volatility; in rolling-maturity coordinates a curve-slope term also enters. Ho–Lee's displayed expectation refers to a fixed calendar maturity, not a rolling 30-year forward. Empirical yield loadings are differentiated into illustrative forward volatilities. Saved bond-pricing ratios around 0.998–0.990 are diagnostics: no standard errors or convergence study justify declaring a numerical pass. Shaded percentile bands are pointwise, not simultaneous path coverage.
6. **Caps, floors and swaptions.** Fixing/payment dates, payment-date and annuity numeraires, Black and Bachelier quote assumptions, parity and cap stripping. Volatility has square-root-time units. Hull–White simple forwards are not exactly normal merely because short rates are Gaussian. Jamshidian assumes positive coupon weights, monotone component prices and an existing unique root; negative fixed coupons need separate treatment.
7. **Negative rates.** ECB deposit rates were negative from 11 June 2014 through 26 July 2022; German monthly government yields also went negative. Unshifted Black requires positive forward and strike. Normal or suitably shifted models can accommodate negatives. CME's April-2020 Bachelier switch concerns specified energy options, not a universal rates-market transition.
8. **SABR.** Stochastic volatility, level/skew/curvature and backbone hedges. Each backbone example solves alpha to match one identical ATM normal-vol target; it does not fit an entire smile. The implied-volatility formula is asymptotic. A historical Treasury realized-volatility slope near 0.3 does not identify pricing-measure SABR beta for a swap forward. Fractional unshifted powers need a suitable domain; shifts and boundary conventions matter. A nonnegative central density plot does not establish global normalization; negative strike curvature at sampled strikes reveals butterfly arbitrage in the approximation.
9. **Market models.** Forward-measure caplet marginals and a common terminal measure. The displayed drift is a one-factor formula; multiple factors require correlations. The corrected dated example is separate from the original House implementation. A frozen-weight swaption-volatility calculation is an approximation. A generalized forward market model handles remaining uncertainty during compounded overnight accrual; linear decay is a model specification, and SOFR caplets are not unconditionally more valuable than IBOR caplets.
10. **Bermudan swaptions.** An optimal Bermudan is at least its best scheduled European; strict inequality is conditional. Independent-path evaluation estimates a feasible policy's expected lower-bound value, with sampling error. A small in/out-sample difference does not isolate look-ahead bias. The plotted exercise line is a sample maximum among exercised paths, not an exact boundary. A finite Gaussian grid has quadrature, interpolation and boundary error despite exact transition distributions. Callable bonds use the issuer's embedded exercise right.
11. **Multi-curve and collateral.** TED reflects more than pure bank default risk. Separate projection and discount curves encode index, tenor and collateral conventions; projection pseudo-discount factors need not be traded bond prices. Collateral-rate discounting assumes a consistent measure and idealized collateral mechanics. A standard SOFR OIS with SOFR cash collateral can use one curve; tenor, funding and cross-currency bases persist.
12. **Bond premia.** Public-curve Fama–Bliss regressions use overlapping annual log returns and 12-lag Newey–West standard errors. Their full-sample association is not a causal result or live trading score. Cochrane–Piazzesi motivates the research question; the active lesson gives a validation protocol covering publication lags, purging overlapping targets, training-only fitting, feasible benchmarks, every specification tried, costs and uncertainty. No sealed forecast is evaluated. Macro-finance models connect states and risk prices.
13. **Mortgages.** A stylized prepayment S-curve and pass-through can produce negative effective convexity. A duration-matched bond's shaded price gap is not a pure option value. The zero-volatility/OAS difference is a model-dependent spread adjustment, not a dollar option price; zero volatility does not remove prepayment. Hedging flows can amplify moves, but the 2003 chart does not identify a causal contribution. Servicing exposures differ from pool exposures. TBA is a standardized forward-delivery market; delivery incentives do not make its quote equal to a worst pool's price. Dollar rolls transfer interim cash-flow entitlements and are not simply repos.
14. **The House.** Separate theoretical restrictions, numerical diagnostics and market calibration. The risk table uses symmetric curve bumps and a bump to the Hull–White diffusion parameter sigma; this parameter sensitivity differs from market quote vega. One fixed European is actually recalibrated before comparing model sensitivities. A reserve policy needs evidence and governance beyond a chosen price range.
15. **Research: the floor and shadow rate.** A one-factor floored Gaussian model, a finite-difference benchmark and a Wu–Xia-style Gaussian forward approximation. The floored model changes the forward-measure tilt, so the substitution is approximate. Higher-dimensional pricing equations remain possible but more costly. Daily yield co-movement is not an event-study replication. Local sensitivity and a finite shock are worked separately.
16. **Recap, desk questions and problems.** The closing material consolidates assumptions, numerical error, measure changes and model risk. The manifest has 16 scenes: the opening, 13 numbered chapters, Research and Outro; Research precedes Outro.

## Desk answers

1. A Bermudan permits each scheduled European's exercise policy, giving an inequality for optimal model values. A finite learned-policy estimate is noisy and may not obey that inequality exactly. Strict extra value requires useful flexibility.
2. Near ATM with small total volatility, `sigma_N ≈ F sigma_B = 0.04 × 0.25 = 0.01`: **100 bp per square root year**. This is approximate. Exact ATM conversion satisfies `sigma_N sqrt(T/(2 pi)) = F[2 Phi(sigma_B sqrt(T)/2)-1]` for common annuity and conventions.
3. Negative convexity can cause losses even if rates return to their starting level. Under local constant convexity and ideal linear hedging, relative convexity PnL is approximately `0.5 C sum((delta y)^2)`. Total PnL also includes carry, spreads, changing prepayments, hedge basis and transaction costs; it is not a guaranteed annual loss formula.
4. An exact initial-curve fit fixes a deterministic shift, not all future dynamics, smile or cross-date dependence. This example uses historical volatility proxies; a desk needs relevant option calibration. Daily re-fitting is an operational choice, not a condition for internal consistency of the original model.

## Ten worked problems

1. **Vasicek.** For `a>0`, `r_T=b+(r_0-b)e^(-aT)+sigma integral_0^T e^(-a(T-s))dW_s`, giving mean `b+(r_0-b)e^(-aT)` and variance `sigma²(1-e^(-2aT))/(2a)`. When these are pricing-measure parameters, the long zero yield is `b-sigma²/(2a²)`.
2. **Riccati.** With pricing drift `a(b-r)` and terminal bond value one, substitute `P=exp(A(tau)-B(tau)r)` into the pricing PDE. `A(0)=B(0)=0`, `B'=1-aB` and `A'=-abB+sigma²B²/2`. Thus `B=(1-e^(-a tau))/a`; `A` is the log prefactor, not its exponential.
3. **Ho–Lee.** For `t<=T`, `f(t,T)=f(0,T)+sigma² t(T-t/2)+sigma W_t` under the money-market pricing measure. The drift correction steepens the expected fixed-calendar-maturity curve; individual realized curves need not rise, and rolling tenors require the maturity-shift term.
4. **Hull–White shift.** Assume `x_0=0`, `dx=-a x dt+sigma dW`. Gaussian integration gives `P(0,T)=exp(-integral phi+V(0,T)/2)`. Matching the initial curve and differentiating yields `phi(T)=f^M(0,T)+sigma²(1-e^(-aT))²/(2a²)`.
5. **ATM caplet.** Bachelier's price per annuity is `sigma_N sqrt(T/(2 pi))`. For notional one, `delta=.25`, discount factor `.96`, expiry one and normal volatility `.01`, price is `.25 × .96 × .01 / sqrt(2 pi) = .00095746`, or **9.575 bp of notional**. Fixing and payment dates differ.
6. **Jamshidian.** For nonnegative weights and monotone zero prices with a unique root, choose `x*` so `sum c_i P_i(x*)=1`, and `K_i=P_i(x*)`. All components change moneyness at the same state, so `(sum c_i P_i-1)+ = sum c_i(P_i-K_i)+`. This is a receiver's bond call; payer orientation gives puts. Without the weight/root assumptions this argument need not apply.
7. **Exercise-rule bias.** Same-path fitting permits look-ahead, which can bias an evaluation upward relative to a feasible rule. Policy approximation can bias value downward relative to the optimum; the combined estimator has no general upper-bound guarantee. Independent evaluation of a fixed feasible policy has expected payoff at most optimal value. Its finite Monte Carlo estimate has sampling error; conditional standard errors do not capture all training-policy uncertainty.
8. **Prepayment life.** With continuous interpolation `S(t)=(1-c)^t=exp(-h t)`, `h=-ln(1-c)`, and no amortization or maturity, `E[tau]=integral S dt=1/h`: 16.16 years for 6%, 1.673 for 45%. Annual end-of-year geometric repayment instead has mean `1/c`. With maturity `T`, the continuous expected life is `(1-e^(-hT))/h`. Different constant speeds alone do not prove negative convexity; rate-dependent prepayments create that mechanism.
9. **Normal floor payoff.** If `s~N(a,sigma_n²)` under the relevant measure, `E[max(s,r_min)]=r_min+sigma_n[phi(z)+z Phi(z)]`, `z=(a-r_min)/sigma_n`. Integration of the normal tail proves the formula, and `g'(z)=Phi(z)`. Using unfloored-model moments for the floored model's forward measure is an additional approximation.
10. **Sensitivity.** Holding parameters and horizon variance fixed, `partial f(n)/partial s≈Phi(z_n)e^(-kappa n)`. Yield sensitivity averages this over maturity. With zero floor, `a=-1%` and `sigma_n=1%`, `f=8.332 bp`. A `-50 bp` move in today's state with loading `.8` gives local change **−6.346 bp**. Recompute at `a=-1.4%`: `f_new=3.667 bp`, an actual approximate-formula change **−4.665 bp**. A finite move is not its first-order derivative.

## Reproduce this review

Run from the repository root after activating the Manim/TeX environment. Do not run `compute` without the explicit whitelist and do not use `--force` or refresh data.

```bash
python -m videos.quant.quant19.compute shadow_theory shortrate hw hjm lmm bermudan negative sabr multicurve mbs y1994 meanrev ratevol sabrpdf lmmcorr capstrip lattice pq twofactor greeks famabliss hwwin
python -m videos.quant.quant19.market_model_example market_model_example
python -m videos.quant.quant19.reserve_example reserve_example
EXPLAINER_TTS=silent python tools/qa_series.py quant19 --cached-only --resume
EXPLAINER_TTS=silent python tools/qa_series.py quant19 --lang zh --cached-only --resume
EXPLAINER_TTS=silent python tools/qa_series.py quant19 --motion --cached-only --resume
python tools/zh_lines.py quant19 --todo
python tools/lecture_length.py quant19 --floor 50
```

All 32 bilingual endpoint sheets and 16 English motion sheets were actually inspected after the final repairs. The [artifact-bound evidence](../../../docs/qa/quant19-polish-evidence.json) records native-frame reviews, speech checks, a narrated opening and a chaptered silent preview. Signal and timing checks do not certify pronunciation or full continuous production listening, which remains pending.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Brigo and Mercurio, *Interest Rate Models: Theory and Practice* (2nd ed.) | 1–2 (definitions, numeraires), 3 (one-factor short-rate models: Vasicek, CIR, Hull–White, BK), 4 (two-factor G2++), 5 (HJM), 6 (LIBOR and swap market models), 8 (cap and swaption calibration), 13 (callables, Bermudans) | ch. 1–5, 8–9 |
| Andersen and Piterbarg, *Interest Rate Modeling*, vols. II–III | 10–12 (one-factor and Gaussian models), 14–15 (market models), 16 (SABR, smile), 18–19 (callable LIBOR exotics, Bermudans) | ch. 3–9 |
| Rebonato, *Volatility and Correlation* | caplet vol shapes (abcd), correlation and swaption vols | ch. 5, 8 |
| James and Webber, *Interest Rate Modelling* | affine models, empirical term structure, MBS | ch. 2, 11–12 |

## Papers, chapter by chapter

* Hook: SEC administrative proceedings on the Orange County investment pools (1996); FOMC statements (1994).
* ch. 1–2: Vasicek (1977); Cox, Ingersoll and Ross (1985); Feller (1951); Phillips and Yu (2005); Duffie and Kan
  (1996); Dai and Singleton (2000).
* ch. 3–4: Ho and Lee (1986); Hull and White (1990, 1994); Black, Derman and Toy (1990); Black and Karasinski (1991);
  Heath, Jarrow and Morton (1992).
* ch. 5–7: Bachelier (1900); Black (1976); Jamshidian (1989); Rebonato (2004); Hagan, Kumar, Lesniewski and Woodward
  (2002, 2014); Bartlett (2006); CME Group notices (April 2020).
* ch. 8–9: Brace, Gatarek and Musiela (1997); Jamshidian (1997); Miltersen, Sandmann and Sondermann (1997); Lyashenko
  and Mercurio (2019); Longstaff and Schwartz (2001).
* ch. 10: Piterbarg (2010); LCH and CME notices on the SOFR discounting switch (October 2020).
* ch. 11: Fama and Bliss (1987); Campbell and Shiller (1991); Cochrane and Piazzesi (2005); Ang and Piazzesi (2003);
  Adrian, Crump and Moench (2013); Bianchi, Büchner and Tamoni (2021).
* ch. 12: SIFMA good-delivery guidelines; Federal Reserve H.4.1.

## Primary public records

* [SEC: Orange County pool securities and financing](https://www.sec.gov/municipal/uwriter).
* [ECB: negative deposit rate effective 11 June 2014](https://www.ecb.europa.eu/press/pr/date/2014/html/pr140605.en.html) and [official rate history](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html).
* [CME: Bachelier switch effective 22 April 2020](https://www.cmegroup.com/notices/clearing/2020/04/Chadv20-171.html).
* [SIFMA: TBA pool notification process](https://www.sifma.org/wp-content/uploads/2024/04/TBA_Market_Governance-Uniform_Practices_Manual-Chapter_7_Pool_Notification_Process.pdf).
* [Hagan et al. (2014), Arbitrage-Free SABR](https://doi.org/10.1002/wilm.10290).
* [Lyashenko and Mercurio (2019), forward/backward-looking rates](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3330240).

---

# 量化金融，从零搭建 — 第19部分：期限结构模型

本部分承接第18部分的贴现曲线，为利率曲线建立随机动态并定价期权。全系列43部分；章节与文献见[系列计划](../README.md)、[教学大纲](../SYLLABUS.md)及[阅读地图](../READING.md)。

> 科学与双语复核、当前源码的端点帧和动画视觉验收已完成。完整成片配音的连续听审仍待完成。旁白约60分钟，动画和停顿另计。

## 数据边界与独立示例

原`compute.py`、House算法及全局数据与试验登记均保持不变，只正常恢复22项允许的描述性示例。当前场景拒绝载入`premia`、`premia_acm`、`envelope`，因为旧路径会登记或载入涉及封存收益的预测试验。本轮不新增市场试验，不打开封存策略收益，不刷新数据清单。第19部分累计315次、全局23,562次保持原值。公开曲线上的全样本描述性回归，不等于封存预测表现；当前版本的平滑曲线也不是可直接交易的价格。

另行命名的`market_model_example.py`使用一致日期：半年至五年定息，再过半年付款，初始远期由匹配日期贴现比计算；各自定息时按付款债券与终端债券比值加权。Black与Bachelier最大偏差分别为1.275%和0.719%，约1.333与0.950个标准误，有限Euler离散误差仍可能存在。无界正态单利远期只是局部数值近似，正债券比值要求`L > -1/delta`；示例拒绝越界路径，有限样本未越界不代表全局可行性。零波动平值价格为零。旧算法与缓存没有改写。

`reserve_example.py`对每个均值回归情景重新求波动率，匹配同一执行价、两年到期、其后八年期限的接收方欧式及同一目标价格。对冲工具误差小于名义本金的`1e-9`；百慕大网格价格为439.7至518.1基点。这是真正重新校准，不是按价格比缩放。匹配一个合成对冲并非校准完整市场期权曲面；范围只是敏感度情景，不是公允价值界限、置信区间或自动会计准备金。

## 章节与解释边界

* **开场与1994年。** 美联储紧缩和橙县说明杠杆及非线性暴露。证交会1994年六月数据为198亿美元证券、72亿美元参与者存款及126亿美元逆回购。损失比例除以五年期收益率变化，只给出粗略久期等价量；日期、融资与非线性均不同，不能当作测得组合久期。
* **短率。** Vasicek高斯转移；CIR非负扩散。正初值下Feller使零不可达，不满足时也不会允许负利率。原月末国库券贴现收益率先截在一基点，再拟合两个模型；它只是瞬时连续复利短率的代理。历史拟合、均值回归估计不确定度、重估偏差及路径扇均为描述性。
* **仿射模型。** 定价测度下Feynman–Kac和Riccati、可行状态空间及不同模型的长期极限。历史参数代入定价公式只作示意。漂移差等于扩散载荷乘风险价格，须说明符号约定。一因子完全正瞬时相关仅适用于这里的正仿射载荷，不是所有非线性模型定理。双因子类似水平与斜率，并非经验主成分本身。
* **Hull–White。** 在`x_0=0`条件下，确定性平移解析拟合初始曲线。漂移截距不同于回归目标。示例拟合历史收益率波动代理，并非市场期权报价；低利率时期边界拟合暴露模型限制。采样日期的高斯状态与积分可精确模拟，均值重定价仍有抽样误差。
* **HJM。** 货币市场定价测度漂移由远期波动决定；滚动期限坐标还含曲线斜率项。Ho–Lee期望针对固定日历到期日，不是滚动三十年远期。历史收益率载荷经求导构成示意远期波动。已存0.998至0.990价格比缺少标准误和收敛检验，不能宣布数值通过。分位阴影为逐点范围，不是完整路径覆盖。
* **上限、下限与互换期权。** 区分定息与付款日、付款日与年金计价物、Black/Bachelier分布假设、平价和波动率剥离。波动率使用根号时间单位。高斯短率不使单利远期严格正态。Jamshidian需要非负息票权重、单调零息价格及唯一存在的根；负息票须另行检查。
* **负利率。** 欧洲央行存款利率从2014年六月十一日至2022年七月二十六日为负，德国月度国债收益率也曾为负。未平移Black要求正远期和执行价；正态或适当平移模型可容纳负数。CME在2020年的切换针对指定能源期权，并非所有利率市场统一转型。
* **SABR。** 随机波动、水平、偏斜、曲率及骨架对冲。每个骨架示例求alpha匹配同一平值正态波动目标，并非拟合整个微笑。隐含波动公式为渐近近似。历史国债实现波动斜率约0.3不能识别互换远期定价测度beta。分数幂需适当定义域，平移和边界重要。中央密度非负不证明全局归一化；采样执行价负曲率揭示近似的蝶式套利。
* **市场模型。** 各远期测度下边际与共同终端测度。一因子漂移推广至多因子时须包括相关系数。日期一致的示例与旧House实现分开。固定权重互换波动公式仍为近似。广义远期市场模型描述隔夜复利期间剩余风险，线性衰减只是设定，SOFR上限单元并非无条件更贵。
* **百慕大。** 最优价值至少等于表内最贵欧式，严格更贵有条件。独立路径估值给出可行策略期望下界的带噪声估计；样本内外差很小不能单独识别前瞻偏差。已行权路径的最高利率只是边界摘要。高斯网格即便使用精确转移分布，也有求积、插值及边界误差。可赎回债含发行人行权权利。
* **多曲线与抵押。** TED不只反映违约风险。投影与贴现曲线体现指数、期限和抵押安排，伪贴现因子不必是可交易债券价格。抵押利率贴现需要一致测度和理想化抵押假设。SOFR现金抵押的普通SOFR隔夜指数互换可共用一条曲线，但期限、融资及跨币种基差仍存在。
* **债券溢价。** 公开曲线Fama–Bliss回归使用重叠年度对数收益和十二阶Newey–West标准误。全样本相关并非因果或实时交易成绩。Cochrane–Piazzesi引出预测问题，验证方案涵盖发布滞后、重叠目标剔除、训练拟合、可行基准、全部尝试、成本与不确定度。不评估封存预测。宏观金融模型连接状态与风险价格。
* **抵押贷款。** 示意提前还款规则可产生负有效凸性。与久期匹配债券的阴影差不是纯期权价值。零波动利差减OAS是依赖模型的收益率调整，不是美元期权价；关掉波动并未取消提前还款。对冲流可能放大行情，但2003年图不能识别因果贡献。服务权暴露不同。TBA是标准化远期交割，报价不等于最差单池价格；美元滚动改变期间本息归属，不是简单回购。
* **House与研究。** 区分理论限制、数值诊断和市场校准；风险表采用对称曲线冲击和Hull–White扩散参数sigma冲击，参数敏感度不同于市场报价vega；同一固定欧式须实际重新校准后再比模型敏感度。影子利率采用一因子有限差分基准及Wu–Xia式高斯近似，下限改变远期测度倾斜，近似误差依赖模型。多因子方程仍可建立，但成本更高。日度收益率共变并非新闻事件研究。研究场景先于回顾，清单共16个场景。

## 交易台解答

1. 百慕大可采用表内任何欧式行权规则，因此精确最优价值至少等于每个欧式。有限策略估计有噪声，严格多出的价值需要灵活性有用。
2. 近平值、小总波动时，正态波动约为远期乘Black波动，即`.04 × .25 = .01`，**每根号年100基点**。这是近似。同一年金与惯例下，精确平值转换满足`sigma_N sqrt(T/(2 pi))=F[2 Phi(sigma_B sqrt(T)/2)-1]`。
3. 负凸性仓位即便利率返回起点，仍可能因实现变动亏损。局部常凸性、理想线性对冲下，相对凸性损益约`0.5 C sum((delta y)^2)`；总损益还含持有收益、利差、提前还款、对冲基差和成本，并非保证年度亏损公式。
4. 当前曲线的精确拟合只确定平移项，不能确定全部未来动态、微笑和跨期依赖。本例用历史波动代理，交易台须按相关期权校准；次日重拟合是操作选择，而非原模型内部一致的必要条件。

## 十道习题解答

1. `a>0`时，`r_T=b+(r_0-b)e^(-aT)+sigma integral_0^T e^(-a(T-s))dW_s`，均值为前两项，方差`sigma²(1-e^(-2aT))/(2a)`。若为定价测度参数，长期零息收益率为`b-sigma²/(2a²)`。
2. 定价漂移为`a(b-r)`、债券终值一。代入`P=exp(A-B r)`，有`A(0)=B(0)=0`、`B'=1-aB`、`A'=-abB+sigma²B²/2`，故`B=(1-e^(-a tau))/a`。这里A是对数前因子。
3. `t<=T`下，`f(t,T)=f(0,T)+sigma² t(T-t/2)+sigma W_t`。这是货币市场定价测度的固定日历到期日表达式；期望修正随T变陡，不表示每条实际路径上升，滚动期限还须加期限移动项。
4. `x_0=0`、`dx=-a x dt+sigma dW`时，高斯积分给出`P(0,T)=exp(-integral phi+V/2)`。匹配曲线并求导，得到`phi(T)=f^M(0,T)+sigma²(1-e^(-aT))²/(2a²)`。
5. 平值Bachelier每单位年金价格为`sigma_N sqrt(T/(2 pi))`。单位本金、`.25`计息、`.96`贴现、到期一年、波动`.01`，价格`.00095746`，即本金的**9.575基点**；定息与付款日期不同。
6. 非负息票、单调零息价及唯一存在的根下，取`sum c_i P_i(x*)=1`和`K_i=P_i(x*)`。所有分量在同一状态改变价内性，故`(sum c_i P_i-1)+=sum c_i(P_i-K_i)+`。接收方为债券看涨，支付方为看跌；缺少这些条件则推导未必成立。
7. 同路径拟合可使用未来信息，使评估相对可行策略向上偏；策略近似又可使价值相对最优向下偏，综合估计一般不构成上界。独立评估固定可行策略时，期望支付不超过最优值；有限蒙特卡洛估计仍有抽样误差，条件标准误不包含所有训练策略不确定性。
8. 连续插值生存率`S(t)=(1-c)^t=exp(-h t)`，`h=-ln(1-c)`。无摊还及终止期限时，平均寿命`1/h`，6%为16.16年，45%为1.673年。若每年末离散偿付，几何分布均值为`1/c`。期限T截断后，连续均值为`(1-e^(-hT))/h`。不同常数速度本身不证明负凸性，关键是提前还款随利率变化。
9. 对适当测度下`s~N(a,sigma_n²)`，正态尾积分给出`E[max(s,r_min)]=r_min+sigma_n[phi(z)+z Phi(z)]`，`z=(a-r_min)/sigma_n`；求导得`g'=Phi`。用无下限模型矩代替受限模型远期测度矩，是额外近似。
10. 固定参数及期限方差，`partial f(n)/partial s≈Phi(z_n)e^(-kappa n)`，收益率导数须沿期限平均。零下限、均值−1%、期限标准差1%时，远期为8.332基点。当前状态下降50基点、载荷`.8`，局部变化为**−6.346基点**；在新均值−1.4%重算，远期3.667基点，有限变化**−4.665基点**。有限移动不能等同一阶导数。

## 复现及验收

在仓库根目录激活Manim/TeX环境，使用上方英文区的显式白名单及两个独立示例命令。不要无参数运行整个计算入口，不使用强制重算或刷新。来源为固定版本GSW、FRED、证交会、欧洲央行、CME与SIFMA等上方链接。最终修复后的32张双语叙述节点图与16张英文动画抽帧图均已实际审查；[绑定产物的证据](../../../docs/qa/quant19-polish-evidence.json)记录原尺寸画面、抽样语音、实际旁白开场及分章静音预览。信号与时间检查不代表发音或完整同步验收；完整连续成片听审仍待完成。
