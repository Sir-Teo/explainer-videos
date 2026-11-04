# Quant, Built — Part 30: Portfolio Construction

Part 30 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act V, Portfolios, Strategies and the Firm (30–38), built to the
series' PhD layer. Part 29 ended on a theorem about estimated means; this part is about estimated covariances, and about
the rules that try to need neither. Its universe is Kenneth French's 49 value-weighted US industry portfolios: research
on 1970–2020 (monthly; daily for the spectrum), 2021–2025 sealed. It covers:

* error maximisation (Michaud): a known-truth experiment, the sensitivity of the optimum to one mean, 5 against 20
  years of data, resampled efficiency;
* the contest against 1/N (DeMiguel, Garlappi and Uppal), with costs, windows and the risk each rule predicted for
  itself; the three-fund and 1/N-combination rules (Kan and Zhou; Tu and Zhou);
* covariance in high dimension: the Marchenko–Pastur law against the industries' daily spectrum, the market and
  sector modes, crises, and eigenvalue clipping (Laloux et al.);
* shrinkage: Ledoit and Wolf's linear estimators, analytical nonlinear shrinkage against the oracle, factor-model
  covariances, the window;
* constraints as shrinkage (Jagannathan and Ma), proved and checked; norm constraints;
* Black–Litterman: reverse optimisation, views relative to equilibrium, He and Litterman's view portfolios, confidence;
  Bayes–Stein means (Jorion);
* risk parity (Spinu's convex ERC) and hierarchical risk parity (López de Prado);
* robust optimisation, why VaR is a bad objective, and CVaR as a linear program (Rockafellar and Uryasev);
* growth: Kelly and fractional Kelly under estimation error, Cover's universal portfolio, Fernholz's diversity weights
  and the excess growth rate;
* entropy pooling (Meucci): a stress view on returns and one on volatility;
* end-to-end portfolios trained on the Sharpe ratio, and decision-focused learning (Elmachtoub and Grigas);
* **for the researcher**: why the optimizer underestimates its own risk: the exact in- and out-of-sample laws of the
  sample minimum-variance portfolio's variance (a Wishart χ² lemma, proved; an F law), the limits (1 − γ) and
  1/(1 − γ), simulations, the industries, and what shrinkage does to it; open problems;
* shrunk minimum variance, HRP and 1/N registered and opened on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py) and the House's
[`portfolio`](../../../explainer/quant/house/portfolio.py) module). Data: Kenneth French's data library (49 industry
portfolios, monthly and daily; firm counts and sizes; the Fama–French factors for the risk-free rate).

*An education in methods, not investment advice.*

## Chapters (about 55 minutes)

* **Hook: the optimizer's promise** (2.1). Five years of data: promised 1.4% a month volatility for 1% a month,
  delivered 0.55% at 6.9%; where Act V begins; seventy years of optimizing with estimates; the plan.
* **1. Error maximisation** (3.9). Markowitz and Merton's closed form; one standard error of a five-year mean in one
  industry (15.8 points a year) moves 4.8 of weight in a portfolio of gross exposure 9.8; twelve estimated frontiers
  against the true one; 300 optimizers' promises and deliveries; 20 years instead of 5 (true volatility 6.9% → 3.6%);
  resampling no better (7.1% against 6.9%); Chopra–Ziemba, the inverse's smallest eigenvalues.
* **2. The humble 1/N** (3.3). DeMiguel, Garlappi and Uppal (2009); the rolling contest 1980–2020 on 10-year
  windows: 1/N 0.55, sample tangency ≈ 0 (gross 141), shrunk minimum variance 0.62–0.64 at 12% volatility against 16.6%;
  predicted against realised risk (sample GMV 7.3% → 14.0%); costs at 10 and 50 bp; 5- against 10-year windows (sample
  23.8% → 14.0%, shrunk 12.0% and 12.1%); Kan–Zhou and Tu–Zhou.
* **3. Covariance in high dimension** (3.3). Marchenko–Pastur; 2019's daily spectrum: 2 of 49 eigenvalues above
  the edge 2.08, the top one 25.8 (53%); the shuffled control; the market and defensive-against-cyclical modes; the
  top share peaking at 82% in 2011; 2008 against 2019; clipping.
* **4. Shrinkage: Ledoit and Wolf** (4.6). Linear shrinkage and its optimal intensity; targets; nonlinear
  shrinkage against the oracle (sample's smallest eigenvalue 2.4 times too small); the horse race (sample GMV 5.6× the
  minimum at 5 years, nonlinear 1.49×; clipping worse than the sample at 20 years); factor-model covariances (one PCA
  factor: Sharpe 0.71, predicted 12.1% against realised 12.7%); intensities through time (0.14–0.51 toward constant
  correlation); the window.
* **5. Constraints as shrinkage** (2.3). Long only keeps 9 industries (2.18 of shorts unconstrained);
  Jagannathan–Ma, checked to 1e-15; out of sample (5-year windows: 23.8% → 12.1%); norm constraints (DeMiguel,
  Garlappi, Nogales and Uppal).
* **6. Black–Litterman** (3.7). Reverse optimisation (δ = 7.5); the posterior; a view that software beats
  utilities by 3% against equilibrium's 9.4%: the posterior spread falls to 6.2%, 15.6% of weight moves from software to
  utilities; sample means give gross 45; He and Litterman; confidence from 3.1% to 9.4%; Bayes–Stein (intensity 0.43;
  tangency −0.19 → −0.06).
* **7. Risk parity and HRP** (3.4). Risk contributions of 1/N; Spinu's convex problem; the single-linkage tree;
  the reordered correlation matrix; recursive bisection from the House's source; in sample and out of sample (HRP 0.62
  at 14.6%, turnover 7% a month).
* **8. Robust optimisation and CVaR** (3.4). Ellipsoidal uncertainty sets; with Ω ∝ Σ, more risk aversion; VaR's
  non-subadditivity; Rockafellar–Uryasev; the tails; in sample min CVaR wins (7.89% against 8.08%), rolled forward it
  loses (8.47% against 8.01%).
* **9. Kelly, Cover and Fernholz** (4.6). Kelly on the market (2.82); the growth curve; fractional Kelly c* =
  SR²/(SR² + 1/T): 0.91 with 51 years, about one half with 5; Cover's universal portfolio on gold and utilities (best
  mix 16% gold, ×158; universal ×98; ratio 1.61 against a bound of 613); the per-period bound; diversity weighting
  (+0.2% a year) and the excess growth rate.
* **10. Entropy pooling** (2.7). Meucci's problem and its dual; a view that banks lose 3% a month: crisis months
  reweighted (2009-01, 1998-08, 2020-03), 525 effective scenarios of 612; a volatility view: average correlation 0.57 →
  0.82; partial confidence, inequalities, the limits.
* **11. End-to-end portfolios** (2.7). The network and the Sharpe loss; Zhang, Zohren and Roberts (2020);
  training 1.44, validation 0.26, against a two-step rule's 0.74 and 1/N's 0.58; concentration (largest weight 65%);
  smart predict-then-optimize.
* **12. Minimum variance and HRP, registered and opened** (3.5). 22 trials each; the counter 23,478 → 23,523;
  research 0.62, 0.62, 0.55; 2021–25: 1/N 0.58 ± 0.45, HRP 0.50, shrunk GMV 0.35 (volatility 13.5% against 16.2%); the
  Jobson–Korkie–Memmel differences (+0.23 ± 0.49, +0.08 ± 0.09); 2021–25 rewarded the formerly volatile industries
  (correlation 0.61); next steps.
* **13. Rule 30: the optimizer** (2.5). The sheet; `lw_identity` and the active-set long-only solver from the House's
  source; the module; Rule 30; three cases.
* **For the researcher: why the optimizer underestimates its own risk** (6.3). Setup; the in-sample law
  χ²_{n−K+1}/n via Muirhead's lemma, proved with a Schur complement; the out-of-sample F law (Kempf and Memmel); the
  limits; simulations at T = 60–600 (T = 120: 0.593 and 1.685 against exact 0.597 and 1.686); the distributions; what
  shrinkage does; the industries (true/reported variance 50 at 5 years against normal theory's 31; 3.9 against 2.8 at
  10; shrunk: 2.4 and 1.9); the correction; three open problems.
* **Recap, desk questions, problems** (3.1). Fourteen lines; six desk questions; twelve problems (two at
  qualifying-exam level), solutions below.

## Hands-on

* Built and run here: every estimator and allocation in the House's `portfolio` module, rolled monthly over 1980–2020;
  a long-only minimum-variance active-set solver; a min-CVaR linear program; Cover's universal portfolio; entropy
  pooling; an end-to-end network trained on the Sharpe ratio.
* Labs: from the House's source: `lw_identity`, `hrp`'s bisection, the long-only active-set solver.
* Simulations against theory: the sample GMV's in- and out-of-sample variance against the exact laws.

## Textbook audit

| Textbook | Sections | Chapters |
|---|---|---|
| Meucci, *Risk and Asset Allocation* (2005) | estimation, Bayesian allocation, entropy pooling (2008 paper) | 1, 6, 10 |
| Grinold and Kahn, *Active Portfolio Management* | ch. 14–15 (portfolio construction, transaction costs) | 2, 5 |
| Paleologo, *Advanced Portfolio Management* (2021) | factor models, covariance estimation, the risk illusion | 3, 4, research |
| Chincarini and Kim, *Quantitative Equity Portfolio Management* | optimization, constraints | 5, 7 |
| Muirhead, *Aspects of Multivariate Statistical Theory* (1982) | 3.2 (Wishart, Theorem 3.2.12) | research |

## Papers, chapter by chapter

* ch. 1: Markowitz (1952); Merton (1972); Michaud (1989); Best and Grauer (1991); Chopra and Ziemba (1993); Scherer (2002).
* ch. 2: DeMiguel, Garlappi and Uppal (2009), *RFS* 22; Kan and Zhou (2007), *JFQA* 42; Tu and Zhou (2011), *JFE* 99.
* ch. 3: Marchenko and Pastur (1967); Laloux, Cizeau, Bouchaud and Potters (1999); Bun, Bouchaud and Potters (2017).
* ch. 4: Ledoit and Wolf (2003, 2004a, 2004b, 2020).
* ch. 5: Jagannathan and Ma (2003), *JF* 58; DeMiguel, Garlappi, Nogales and Uppal (2009), *Management Science* 55.
* ch. 6: Black and Litterman (1992), *FAJ*; He and Litterman (1999); Jorion (1986), *JFQA* 21.
* ch. 7: Maillard, Roncalli and Teïletche (2010); Spinu (2013); López de Prado (2016), *JPM*.
* ch. 8: Goldfarb and Iyengar (2003); Ceria and Stubbs (2006); Artzner, Delbaen, Eber and Heath (1999); Rockafellar and
  Uryasev (2000).
* ch. 9: Kelly (1956); Breiman (1961); Cover (1991); Fernholz (2002).
* ch. 10: Meucci (2008), "Fully flexible views".
* ch. 11: Zhang, Zohren and Roberts (2020), *JFDS*; Elmachtoub and Grigas (2022), *Management Science*.
* ch. 12: Jobson and Korkie (1981); Memmel (2003).
* Research: Muirhead (1982); Kempf and Memmel (2006); Bai, Liu and Wong (2009); El Karoui (2010); Ledoit and Wolf (2017);
  Bodnar, Parolya and Schmid (2018).

## For the researcher

* **The theorem.** For T i.i.d. N(μ, Σ) returns of K assets with sample covariance Σ̂ (n = T − 1), the sample GMV
  portfolio's reported variance satisfies σ̂²_in/σ²_min = χ²_{n−K+1}/n exactly, and its true variance
  σ²_out/σ²_min = 1 + (K − 1)/(n − K + 2)·F_{K−1, n−K+2}, with mean (n − 1)/(n − K). As K/T → γ < 1 they tend to 1 − γ
  and 1/(1 − γ), so the true variance exceeds the reported one by 1/(1 − γ)².
* **Simplifications.** Normal i.i.d. returns for the theory; the industries' 1970–2020 moments as the "truth" in every
  simulation; monthly rebalancing on trailing windows with no constraints beyond those stated; costs a flat 10 bp per
  dollar traded; the end-to-end network is small (one hidden layer of 16) and trained on 31 years.
* **Open problems.** Exact finite-sample laws for heavy-tailed, dependent returns; the shrinkage optimal for the
  portfolio rather than the covariance; minimum variance when K > T.

## Build it

```bash
python -m videos.quant.quant30.compute                            # every item; a few minutes on 2 cores
python -m pytest -q tests/test_quant_house.py -k "portfolio or gmv_theory"
EXPLAINER_TTS=silent python tools/qa_scene.py quant30 Research     # one chapter, silent, with a contact sheet
python tools/build.py quant30                                      # the narrated part
```

## Desk questions, with solutions

1. **Why does the optimizer love the asset with the most estimation error?** It maximises estimated return per unit of
   estimated risk, so it overweights the assets whose means are overestimated and whose variances or correlations are
   underestimated: it selects for flattering errors (Michaud). Shrink the inputs, constrain, or use rules that need
   fewer of them.
2. **A 49-asset GMV backtest on 5-year windows reports 3% volatility.** With γ = 49/60 ≈ 0.82, under normality the true
   variance is about (n − 1)/(n − K)/((n − K + 1)/n) ≈ 31 times the reported one, about 5.6 times in volatility; the
   industries were worse (50). Shrink, lengthen the window, use a factor model, and report risk out of sample.
3. **A long-only constraint improves the portfolio. Luck?** No: by Jagannathan and Ma it is the unconstrained GMV of a
   covariance whose largest covariances, the ones the optimizer would exploit, are reduced by the constraint's
   multipliers.
4. **Black–Litterman with no views?** The posterior mean is the equilibrium Π = δΣw_mkt, so the optimal portfolio is
   the market (scaled by 1/(1 + τ) if the posterior covariance is inflated).
5. **Should a long-horizon investor hold full Kelly?** Only with known means; with a mean estimated from T years the
   optimal fraction is SR²/(SR² + 1/T) < 1, and fat left tails argue for less still.
6. **HRP lost to 1/N on 2021–25. Drop it?** The difference was +0.08 with a standard error of 0.09; judge a risk-based
   rule on its stated goal (risk) and on long samples, and count the change as a new trial.

## Problems, with solutions

1. **Two assets.** w₁ = σ₂²/(σ₁² + σ₂²) = 0.04/0.05 = 0.8, w₂ = 0.2; volatility √(0.64·0.01 + 0.04·0.04) = √0.008 ≈ 8.9%.
2. **ERC.** Uncorrelated: equal contributions w_i²σ_i² mean w_i ∝ 1/σ_i: 2/3 and 1/3.
3. **Marchenko–Pastur edges.** q = 49/60 = 0.817, √q = 0.904: λ₊ = 1.904² ≈ 3.62, λ₋ = 0.096² ≈ 0.009.
4. **Optimal intensity.** With E S = Σ, E‖δF + (1 − δ)S − Σ‖² = δ²‖F − Σ‖² + (1 − δ)²E‖S − Σ‖², minimised at
   δ* = E‖S − Σ‖²/(‖F − Σ‖² + E‖S − Σ‖²) = E‖S − Σ‖²/E‖S − F‖².
5. **BL with P = 0.** The posterior is the prior: μ = Π; the portfolio is the market.
6. **Kelly.** f* = 0.06/0.16² = 2.34; at 2f*, g = r + 2f*μ − 2f*²σ² = r + 2μ²/σ² − 2μ²/σ² = r.
7. **Cover's bound.** (1/n)log(max_b S_n(b)/Ŝ_n) ≤ log(n + 1)/n → 0: the growth rates coincide asymptotically.
8. **CVaR.** β = 80%: the worst 20% is {10}, CVaR = 10; β = 60%: the worst 40% is {5, 10}, CVaR = 7.5.
9. **Entropy pooling on two scenarios.** −0.1q₁ + 0.1q₂ = 0.05 and q₁ + q₂ = 1 give q = (0.25, 0.75): with two
   scenarios the view alone fixes the posterior.
10. **The risk illusion.** γ = 0.4: true over reported variance → 1/(1 − 0.4)² ≈ 2.8.
11. **(qual) The laws.** For a fixed a, a'Σ⁻¹a/a'W⁻¹a ~ χ²_{n−K+1} (rotate a to e₁; (W⁻¹)₁₁ = 1/W₁₁·₂ with the Schur
    complement W₁₁·₂ ~ σ₁₁·₂χ²_{n−K+1}, and (Σ⁻¹)₁₁ = 1/σ₁₁·₂). With W = nΣ̂ and a = 1, Σ̂⁻¹ = nW⁻¹, so σ̂²_in = 1/(1'Σ̂⁻¹1) =
    1/(n·1'W⁻¹1) and σ̂²_in/σ²_min = (1'Σ⁻¹1)/(n·1'W⁻¹1) = χ²_{n−K+1}/n, mean (n − K + 1)/n. Given
    σ²_out/σ²_min = 1 + (K − 1)/(n − K + 2)·F, E F_{d₁,d₂} = d₂/(d₂ − 2) gives E = 1 + (K − 1)/(n − K) = (n − 1)/(n − K).
    As K/T → γ: in → 1 − γ, out → 1/(1 − γ), and their ratio → 1/(1 − γ)² (the ratio of limits, since both concentrate).
12. **(qual) Jagannathan–Ma.** KKT for min w'Sw, 1'w = 1, w ≥ 0: 2Sw − γ1 − λ = 0, λ ≥ 0, λ'w = 0. Let
    S̃ = S − ½(λ1' + 1λ'). Then S̃w = Sw − ½λ(1'w) − ½1(λ'w) = Sw − ½λ = ½γ1, so S̃w ∝ 1 and w is the GMV portfolio of
    S̃ (when S̃ is positive definite). The multipliers are positive only for assets the unconstrained problem wanted to
    short, so the constraint lowers exactly their covariances.

## Data and reproducibility

* Kenneth French's data library: 49 industry portfolios, value-weighted, monthly (complete from July 1969) and daily;
  the number of firms and average firm size (for market weights); the Fama–French monthly factors (risk-free rate);
  frozen and checked by SHA-256 in `videos/quant/data/manifest.json`.
* Registered: `lw_gmv_part30` and `hrp_part30` (22 trials each), `equal_weight_part30` (1); the counter goes from
  23,478 to 23,523; the hold-outs (`kenfrench/industries49`, `kenfrench/ff3_monthly`) sealed and opened once. Track
  Record rows: 2021–25 Sharpe 0.35 ± 0.44 (0.33 net), 0.50 ± 0.46 (0.49), 0.58 ± 0.45 (0.58).
* Studied after the registration and not part of its count: factor-model covariances and Bayes–Stein means
  (Chapters 4 and 6).
* Quoted, not computed: DeMiguel–Garlappi–Uppal's, Chopra–Ziemba's, Scherer's and Zhang–Zohren–Roberts's results.
* Simulated or illustrative: every "known truth" experiment uses the industries' 1970–2020 moments as the truth.

---

# 量化金融，从零搭建 — 第30部分：组合构建

本系列共四十三部分，这是第五幕"组合、策略与公司"（第30–38部分）的第一部分，按本系列的博士层次标准构建。第29部分以一条关于估计均值的定理结束；本部分讲的是估计的协方差，以及那些试图两者都不需要的规则。资产范围是Kenneth French的49个市值加权美国行业组合：1970–2020年用于研究（月度；谱分析用日度），2021–2025年密封。

*这是方法的教育，不是投资建议。*

## 章节（约55分钟）

* **开篇：优化器的承诺。** 五年的数据：承诺以每月1.4%的波动率赚每月1%，交付的是6.9%波动率下的0.55%；第五幕从这里开始；七十年用估计做优化的历史；本部分的计划。
* **1. 误差最大化。** Markowitz与Merton的闭式解；一个行业的均值误差为五年均值的一个标准误（每年15.8个百分点）时，在总敞口9.8的组合里移动4.8的权重；十二条估计前沿对比真实前沿；300个优化器的承诺与交付；20年而不是5年（真实波动率6.9% → 3.6%）；重抽样没有更好（7.1%对6.9%）；Chopra–Ziemba，逆矩阵的最小特征值。
* **2. 朴素的1/N。** DeMiguel、Garlappi与Uppal（2009）；1980–2020年十年窗口的滚动较量：1/N为0.55，样本切点组合约为0（总敞口141），收缩的最小方差为0.62–0.64，波动率12%对16.6%；预测与实现风险（样本GMV 7.3% → 14.0%）；10与50个基点的成本；5年与10年窗口（样本23.8% → 14.0%，收缩12.0%与12.1%）；Kan–周与Tu–周。
* **3. 高维中的协方差。** 马尔琴科–帕斯图尔定律；2019年的日度谱：49个特征值中2个高于边界2.08，最大的为25.8（53%）；打乱对照；市场模态与防御对周期模态；最大份额在2011年达到82%的峰值；2008对2019；裁剪。
* **4. 收缩：Ledoit与Wolf。** 线性收缩及其最优强度；目标；非线性收缩对比先知值（样本最小特征值小了2.4倍）；赛马（五年时样本GMV为最小值的5.6倍，非线性1.49倍；二十年时裁剪比样本还差）；因子模型协方差（单个主成分因子：夏普比率0.71，预测12.1%对实现12.7%）；强度随时间的变化（朝常相关0.14–0.51）；窗口。
* **5. 约束即收缩。** 只做多保留9个行业（无约束时有2.18的空头）；Jagannathan–Ma，验证到1e-15；样本外（五年窗口：23.8% → 12.1%）；范数约束（DeMiguel、Garlappi、Nogales与Uppal）。
* **6. Black–Litterman。** 反向优化（δ = 7.5）；后验；软件业比公用事业每年多赚3%的观点，对比均衡的9.4%：后验价差降到6.2%，15.6%的权重从软件业移到公用事业；样本均值给出总敞口45；He与Litterman；置信度从3.1%到9.4%；贝叶斯–斯坦（强度0.43；切点组合−0.19 → −0.06）。
* **7. 风险平价与HRP。** 1/N的风险贡献；Spinu的凸问题；单链接树；重排后的相关矩阵；本系列公司源码中的递归二分；样本内与样本外（HRP 0.62，波动率14.6%，每月换手7%）。
* **8. 鲁棒优化与CVaR。** 椭球不确定集；Ω ∝ Σ时等于更大的风险厌恶；VaR不满足次可加性；Rockafellar–Uryasev；尾部；样本内最小CVaR胜出（7.89%对8.08%），滚动向前则落败（8.47%对8.01%）。
* **9. Kelly、Cover与Fernholz。** 市场上的凯利杠杆（2.82）；增长曲线；分数凯利c* = SR²/(SR² + 1/T)：51年时0.91，5年时约一半；黄金与公用事业上的Cover通用组合（最佳组合16%黄金，×158；通用组合×98；比值1.61，界为613）；每期的界；多样性加权（每年+0.2%）与超额增长率。
* **10. 熵池化。** Meucci的问题及其对偶；银行业每月亏损3%的观点：危机月份被调高权重（2009年1月、1998年8月、2020年3月），612个情景中有效525个；一个波动率观点：平均相关性0.57 → 0.82；部分置信度、不等式、局限。
* **11. 端到端组合。** 网络与夏普比率损失；Zhang、Zohren与Roberts（2020）；训练期1.44，验证期0.26，对比两步规则的0.74和1/N的0.58；集中（最大权重65%）；先预测后优化的改进（SPO）。
* **12. 最小方差与HRP，登记并打开。** 每个22次试验；计数器23,478 → 23,523；研究期0.62、0.62、0.55；2021–25年：1/N 0.58 ± 0.45，HRP 0.50，收缩GMV 0.35（波动率13.5%对16.2%）；Jobson–Korkie–Memmel差异检验（+0.23 ± 0.49，+0.08 ± 0.09）；2021–25年奖励此前波动大的行业（相关性0.61）；下一步。
* **13. 第30条规则：优化器。** 第一张表；本系列公司源码中的`lw_identity`与只做多有效集求解器；模块；第30条规则；三个案例。
* **写给研究者：优化器为什么低估自己的风险。** 设定；样本内分布律χ²_{n−K+1}/n，经由Muirhead的引理，用舒尔补证明；样本外F分布律（Kempf与Memmel）；极限；T = 60–600的模拟（T = 120时0.593和1.685，精确值0.597和1.686）；分布；收缩的作用；行业上（五年时真实/报告方差为50，正态理论31；十年时3.9对2.8；收缩后2.4与1.9）；修正；三个开放问题。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十二道习题（两道为资格考试难度），解答见下文。

## 写给研究者

* **定理。** 对K个资产T期独立同分布的N(μ, Σ)收益，样本协方差为Σ̂（n = T − 1），样本GMV组合报告的方差精确满足σ̂²_in/σ²_min = χ²_{n−K+1}/n，真实方差σ²_out/σ²_min = 1 + (K − 1)/(n − K + 2)·F_{K−1, n−K+2}，均值为(n − 1)/(n − K)。当K/T → γ < 1时，它们分别趋于1 − γ和1/(1 − γ)，所以真实方差超过报告方差的倍数为1/(1 − γ)²。
* **简化。** 理论中假设正态独立同分布收益；每个模拟都以行业1970–2020年的矩为"真相"；在滞后窗口上按月再平衡，除所述约束外没有其他约束；成本统一为每交易一美元10个基点；端到端网络很小（一个16单元的隐藏层），在31年上训练。
* **开放问题。** 厚尾、相依收益下精确的有限样本分布律；对组合而非对协方差最优的收缩；K > T时的最小方差。

## 交易台问题与解答

1. **为什么优化器偏爱估计误差最大的资产？** 它最大化每单位估计风险的估计收益，所以会超配均值被高估、方差或相关性被低估的资产：它在挑选讨喜的误差（Michaud）。收缩输入、加约束，或使用需要更少输入的规则。
2. **一个49资产、五年窗口的GMV回测报告3%的波动率。** γ = 49/60 ≈ 0.82时，在正态假设下真实方差约为报告值的(n − 1)/(n − K)/((n − K + 1)/n) ≈ 31倍，波动率约5.6倍；行业数据更糟（50）。收缩、延长窗口、用因子模型，并在样本外报告风险。
3. **只做多约束让组合变好了。是运气吗？** 不是：根据Jagannathan与Ma，它是一个协方差矩阵的无约束GMV，而这个矩阵中优化器原本会利用的那些最大的协方差，被约束的乘数降低了。
4. **没有观点的Black–Litterman？** 后验均值就是均衡Π = δΣw_mkt，所以最优组合就是市场组合（若后验协方差被放大，则缩放1/(1 + τ)）。
5. **长期投资者应该持有全凯利吗？** 只有在均值已知时才应如此；均值用T年估计时，最优比例为SR²/(SR² + 1/T) < 1，而厚左尾意味着还要更少。
6. **HRP在2021–25年输给了1/N。要放弃它吗？** 差异为+0.08，标准误为0.09；应按一条基于风险的规则自己声明的目标（风险）并在长样本上评判它，而把更换计为一次新的试验。

## 习题与解答

1. **两个资产。** w₁ = σ₂²/(σ₁² + σ₂²) = 0.04/0.05 = 0.8，w₂ = 0.2；波动率√(0.64·0.01 + 0.04·0.04) = √0.008 ≈ 8.9%。
2. **ERC。** 不相关时，风险贡献w_i²σ_i²相等意味着w_i ∝ 1/σ_i：2/3与1/3。
3. **马尔琴科–帕斯图尔边界。** q = 49/60 = 0.817，√q = 0.904：λ₊ = 1.904² ≈ 3.62，λ₋ = 0.096² ≈ 0.009。
4. **最优强度。** 当E S = Σ时，E‖δF + (1 − δ)S − Σ‖² = δ²‖F − Σ‖² + (1 − δ)²E‖S − Σ‖²，在δ* = E‖S − Σ‖²/(‖F − Σ‖² + E‖S − Σ‖²) = E‖S − Σ‖²/E‖S − F‖²处取最小。
5. **P = 0的BL。** 后验就是先验：μ = Π；组合就是市场组合。
6. **凯利。** f* = 0.06/0.16² = 2.34；在2f*处，g = r + 2f*μ − 2f*²σ² = r + 2μ²/σ² − 2μ²/σ² = r。
7. **Cover的界。** (1/n)log(max_b S_n(b)/Ŝ_n) ≤ log(n + 1)/n → 0：增长率渐近相同。
8. **CVaR。** β = 80%时，最坏的20%是{10}，CVaR = 10；β = 60%时，最坏的40%是{5, 10}，CVaR = 7.5。
9. **两个情景上的熵池化。** −0.1q₁ + 0.1q₂ = 0.05与q₁ + q₂ = 1给出q = (0.25, 0.75)：只有两个情景时，观点本身就确定了后验。
10. **风险错觉。** γ = 0.4：真实方差与报告方差之比 → 1/(1 − 0.4)² ≈ 2.8。
11. **（资格考试）分布律。** 对固定的a，a'Σ⁻¹a/a'W⁻¹a ~ χ²_{n−K+1}（把a旋转到e₁；(W⁻¹)₁₁ = 1/W₁₁·₂，舒尔补W₁₁·₂ ~ σ₁₁·₂χ²_{n−K+1}，且(Σ⁻¹)₁₁ = 1/σ₁₁·₂）。取W = nΣ̂、a = 1：σ̂²_in/σ²_min = (1'Σ⁻¹1)/(n·1'W⁻¹1) = χ²_{n−K+1}/n，均值为(n − K + 1)/n。已知σ²_out/σ²_min = 1 + (K − 1)/(n − K + 2)·F，由E F_{d₁,d₂} = d₂/(d₂ − 2)得E = 1 + (K − 1)/(n − K) = (n − 1)/(n − K)。当K/T → γ时：样本内 → 1 − γ，样本外 → 1/(1 − γ)，二者之比 → 1/(1 − γ)²（因两者都集中，比值的极限即极限之比）。
12. **（资格考试）Jagannathan–Ma。** min w'Sw、1'w = 1、w ≥ 0的KKT条件：2Sw − γ1 − λ = 0，λ ≥ 0，λ'w = 0。令S̃ = S − ½(λ1' + 1λ')。则S̃w = Sw − ½λ(1'w) − ½1(λ'w) = Sw − ½λ = ½γ1，所以S̃w ∝ 1，w是S̃的GMV组合（当S̃正定时）。乘数只对无约束问题想要做空的资产为正，所以约束恰好降低了它们的协方差。

## 数据与复现

* Kenneth French数据库：49个行业组合，市值加权，月度（自1969年7月起完整）与日度；公司数目与平均公司规模（用于市场权重）；Fama–French月度因子（无风险利率）；已冻结，并在`videos/quant/data/manifest.json`中用SHA-256校验。
* 本部分登记：`lw_gmv_part30`与`hrp_part30`（各22次试验），`equal_weight_part30`（1次）；计数器从23,478升到23,523；样本外数据（`kenfrench/industries49`、`kenfrench/ff3_monthly`）已封存并只打开一次。业绩记录：2021–25年夏普比率0.35 ± 0.44（扣成本后0.33）、0.50 ± 0.46（0.49）、0.58 ± 0.45（0.58）。
* 在登记之后研究、不计入其试验数的内容：因子模型协方差与贝叶斯–斯坦均值（第4章与第6章）。
* 引用而非计算的结果：DeMiguel–Garlappi–Uppal、Chopra–Ziemba、Scherer以及Zhang–Zohren–Roberts的结果。
* 模拟或示意：每个"已知真相"的实验都以行业1970–2020年的矩为真相。
