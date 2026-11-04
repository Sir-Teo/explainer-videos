# Quant, Built — Part 25: The Factor Zoo

Part 25 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act IV, Return Premia (23–29). Part 24 met the classic factors;
this part meets the hundreds published since, and the statistics needed to tell the few that are real from the many
that were found by looking. It covers:

* the best of many noisy strategies and the hurdle the count implies; Harvey, Liu and Zhu's t > 3; a field's
  false-positive arithmetic;
* multiple testing: the familywise error rate (Bonferroni, Holm), the false discovery rate (Benjamini–Hochberg), the
  bootstrap (White, Romano–Wolf), on 212 published predictors in sample and after publication;
* replication: Hou–Xue–Zhang against Jensen–Kelly–Pedersen, and Chen and Zimmermann's open-source asset pricing;
* decay: empirical-Bayes shrinkage against the post-publication record, McLean and Pontiff's timeline, publication
  bias, and the data categories;
* data-mined signals against peer-reviewed ones (Chen, Lopez-Lira and Zimmermann; Yan and Zheng);
* Kozak, Nagel and Santosh's shrinkage SDF on 154 predictors, cross-validated;
* Feng, Giglio and Xiu's double-selection test of new factors against the zoo;
* weak factors (Kan–Zhang, Kleibergen, Giglio–Xiu) and the three-pass estimator;
* PCA, risk-premium PCA (Lettau–Pelger) and instrumented PCA (Kelly–Pruitt–Su);
* comparing models by the squared Sharpe ratio (Barillas–Shanken; Fama–French 2018; Bryzgalova–Huang–Julliard);
* the shrinkage SDF and the zoo's equal weight, registered and opened on 2021–2023.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's new
[`zoo`](../../../explainer/quant/house/zoo.py) module). Data: Open Source Asset Pricing, release 2024.10 (212
predictors as their original papers built them, with their documentation), Kenneth French's data library and
global-q.org's q5 factors.

*An education in methods, not investment advice. The predictors' returns are paper returns of their original
portfolios, before realistic trading costs.*

## Chapters (about 56 minutes)

* **Two hundred coins** (2.8 min). 200 noise strategies, 20 years each: five clear t = 1.96, the best t = 2.89; the
  file drawer and forking paths; the zoo's count by publication year (51 by 2000, 212 by 2016); the history strip
  (1979–2023); the plan; the SDF model.
* **1. Hundreds of factors, and a rising hurdle** (3.9). The law of the maximum; the honest p-value of the best of 200
  (t = 2.9: 0.0019 alone, 0.31 as the best of 200); a field's arithmetic (Ioannidis: with π = 0.1 and power 0.5, 53% of
  significant results are true); the simulated best t against n (1.5 for 10, 2.8 for 200, 3.3 for 1,000); Bonferroni's
  hurdle as the zoo grew (2.58 in 1980, 3.30 in 2000, 3.68 in 2016); Harvey–Liu–Zhu (316 factors, t > 3); the zoo's
  reproduced t's (87% above 1.96, 58% above 3).
* **2. Multiple testing: FWER and FDR** (5.3). FWER and Bonferroni (|t| ≥ 3.68 for 212 tests); Holm's step-down;
  FDR and Benjamini–Hochberg; the V/R table; five p-values by hand (Bonferroni 2, Holm 3, BH 4); the BH line on the
  zoo's post-publication p-values; counts (in sample: 185 raw, 86 Bonferroni, 91 Holm, 184 BH of 212; after
  publication, one-sided: 59, 7, 8, 24 of 208); the bootstrap (White; Romano–Wolf); choosing q; which error to control.
* **3. Replication and open-source asset pricing** (3.6). Hou–Xue–Zhang (65% of 452 fail |t| ≥ 1.96; 82% at 2.78);
  Chen and Zimmermann's release; what it contains; published against reproduced t (188 predictors: 88% reproduce
  t > 1.96, median ratio 0.90, correlation 0.75); construction; microcaps (about 60% of stocks, 3% of value);
  Jensen–Kelly–Pedersen (153 factors, 93 countries, 13 themes).
* **4. Decay, shrinkage and publication bias** (3.5). Empirical Bayes on the t's (variance 5.9, shrink 0.83); worked
  (7 → 6.5; 2.5 → 2.7); in-sample against post-publication means (208 predictors: 0.69% → 0.26% a month, kept 38%,
  slope 0.43); noise alone against the record (83% against 38%); McLean–Pontiff's timeline (−26% out of sample,
  −58% after publication); by data category (price 0.29, analyst 0.34, accounting 0.38, trading 0.45, event 0.64);
  Chen–Zimmermann's publication bias (small); plan a third to a half.
* **5. Data-mined against peer-reviewed** (3.0). Chen–Lopez-Lira–Zimmermann's 29,000 accounting ratios; what chance
  gives (about 1,320 clear |t| > 2, 78 clear 3); about half survives in both groups; risk explanations no better;
  Yan–Zheng's bootstrap; the count separates them.
* **6. Shrinking the cross-section** (4.4). The SDF linear in 154 factors and its plug-in; KNS's prior and ridge
  posterior; the principal-component reading; two directions worked; the cross-validated path (out-of-block R² peaks
  at 0.30 at κ ≈ 1.0 a year, −1.0 unshrunk); blocks, metric, grid; the largest loadings (short-term reversal first);
  1973–2000 fit, 2001–2020 held (Sharpe: tangency 15.5 → 2.6, KNS 6.1 → 1.9, equal weights 2.8 → 1.2); sparsity in PCs;
  paper returns.
* **7. Taming the zoo** (3.3). The SDF-loading question; the lasso and its bias; a toy; double selection; 25 factors
  published since 2011 against 53 published by 2003 (own t > 1.96: 21; naive SDF t: 14; double selection: 5).
* **8. Weak factors** (3.0). The second pass with near-zero betas; a simulation (strong: median 0.48% against a true
  0.5%; weak: median 0.07%, 10–90% range −0.58% to 0.75%); attenuation (var(β)/(var(β) + var(u)) = 0.2 worked);
  omitted factors (Giglio–Xiu); the three-pass estimator.
* **9. PCA, RP-PCA and IPCA** (3.5). The scree (first component 34%, five 67%, ten 76%); RP-PCA; the first
  components (PCA's out-of-sample Sharpe −0.03, RP-PCA's 0.88); out-of-sample Sharpe by K (K = 5: PCA 0.39, RP-PCA
  1.99); γ; RMS alphas (5.1% with none; about 4% with ten components, either method); IPCA; what each optimises.
* **10. Comparing models** (3.6). Barillas–Shanken's insight; how test assets mislead; the named models (SR² in
  1967–1993: CAPM 0.10, FF3 0.73, Carhart 1.80, FF5 2.77, FF6 3.53, q4 4.37, q5 7.13; out-of-sample Sharpe 0.57 to
  1.47); 382 models (rank correlation 0.77); the top five (mixed families); Fama–French's 'Choosing factors'; Bayesian
  model averaging (Bryzgalova–Huang–Julliard).
* **11. The shrinkage SDF, registered and opened** (3.6). What is registered (20 trials and 1); the results (research
  Sharpe 4.6 and 2.1; 2021–23: +34.7% a year with Sharpe 3.06 ± 0.60, and +7.2% with 2.14 ± 0.63); the paths; the
  cost break-even (about 35% a year); caveats (paper returns, leverage); why the hold-out needs no correction; what
  comes next; the counter 325 → 346.
* **12. Rule 25: the SDF model** (2.8). The trial count by part; the first sheet; **lab**: `kns_b`, `rp_pca`,
  `double_selection`; the `zoo` module; Rule 25; the rule against this part's cases.
* **For the researcher: how many anomalies are real?** (6.0). Benjamini and Hochberg's theorem, FDR = π₀q for
  independent tests, with the proof's key step (replace p_i by 0; the rejection count R⁽ⁱ⁾ is then independent of
  p_i, and Σ_k (1/k)(qk/m)Pr(R⁽ⁱ⁾ = k) = q/m). Storey's π̂₀(λ) = #{p > λ}/(m(1 − λ)), conservative. Simulated zoos
  of 208 tests (400 replications, real effects with gamma-distributed mean t, mean 2): realized FDR 0.030, 0.047,
  0.083 against π₀q = 0.03, 0.05, 0.08; π̂₀ = 0.44, 0.60, 0.84 (± 0.06–0.07) for π₀ = 0.3, 0.5, 0.8. The zoo: the
  in-sample p-values are selected (π̂₀ = 0.03, meaningless); the 208 post-publication t-statistics give π̂₀(½) = 0.375,
  and π̂₀(λ) falls from 0.75 (λ = 0.05) to 0.14 (λ = 0.9), so the far right is thinner than uniform. Efron's two-group
  model with a kernel mixture density: 70 anomalies with lfdr < 0.2, Σ(1 − lfdr) ≈ 135 real effects; BH at 10% finds
  41, Storey-adjusted BH 76. Strongest after publication: DivYieldST (t 9.7), AnnouncementReturn (7.3),
  AnalystRevision (6.6). Three open problems; pause: π̂₀ = 0.76, so about 0.076 × 120 ≈ 9 false discoveries.
* **Recap, desk questions, problems** (3.8). Fourteen lines; six desk questions; twelve problems (two at
  qualifying-exam level), solutions below.

## Hands-on

* **Lab** (the House's own code on screen): `kns_b`, `rp_pca`, `double_selection` (ch. 12).
* **Computed:** the best of n noise strategies; Bonferroni's hurdle by year; three multiple-testing procedures on 212
  predictors; empirical-Bayes shrinkage and the decay; a cross-validated shrinkage SDF; PCA and RP-PCA out of sample;
  double selection for 25 new factors; a weak-factor simulation; 382 models ranked; two registered strategies scored
  on the hold-out.
* **Live constructions:** sorted t's of 200 coins; the BH line over sorted p-values; the shrinkage path; the funnel of
  new factors; weak and strong premium histograms; PCA against RP-PCA by K; the cost break-even line.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Kelly and Xiu, *Financial Machine Learning* | 3 (regularisation, the lasso), 4 (PCA, RP-PCA, IPCA), 5 (SDF estimation, KNS) | ch. 6–9 |
| Bali, Engle and Murray, *Empirical Asset Pricing* | 5 (the cross-section, multiple tests), 6 (factor models) | ch. 1–4, 10 |
| Efron, *Large-Scale Inference* | 1–4 (empirical Bayes, false discovery rates) | ch. 2, 4 |
| Cochrane, *Asset Pricing* | 12–13 (regression tests, the SDF with many factors) | ch. 6, 10 |

## Papers, chapter by chapter

* Hook: Cochrane (2011); Chen and Zimmermann (2022).
* ch. 1: Ioannidis (2005); Harvey, Liu and Zhu (2016); Harvey (2017).
* ch. 2: Holm (1979); Benjamini and Hochberg (1995); White (2000); Romano and Wolf (2005); Harvey and Liu (2020).
* ch. 3: Fama and French (2008); Hou, Xue and Zhang (2020); Chen and Zimmermann (2022); Jensen, Kelly and Pedersen
  (2023).
* ch. 4: McLean and Pontiff (2016); Chen and Zimmermann (2020); Chordia, Goyal and Saretto (2020).
* ch. 5: Yan and Zheng (2017); Chen, Lopez-Lira and Zimmermann (working paper, arXiv 2212.10317).
* ch. 6: Kozak, Nagel and Santosh (2018, 2020).
* ch. 7: Tibshirani (1996); Belloni, Chernozhukov and Hansen (2014); Feng, Giglio and Xiu (2020).
* ch. 8: Kan and Zhang (1999); Kleibergen (2009); Giglio and Xiu (2021); Giglio, Xiu and Zhang (test assets and weak
  factors).
* ch. 9: Connor and Korajczyk (1986); Kelly, Pruitt and Su (2019); Lettau and Pelger (2020).
* ch. 10: Lewellen, Nagel and Shanken (2010); Barillas and Shanken (2017, 2018); Fama and French (2018); Bryzgalova,
  Huang and Julliard (2023).
* ch. 11: Novy-Marx and Velikov (2016) on costs.

## Build it

```bash
python -m videos.quant.quant25.compute                        # every item (OSAP data cached by Part 3)
EXPLAINER_TTS=silent python tools/qa_scene.py quant25 KNS      # one chapter, silent, with a contact sheet
python tools/make.py quant25 --cpu-voice -q m                 # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **200 strategies, all noise. Expected best t?** About 2.8, or about 3.0 if losing strategies may be flipped into
   shorts, with a 5–95% range of roughly 2.2 to 3.5. The maximum of n near-normal draws grows like √(2 ln n) (ch. 1).
2. **You report the best of 200 with t = 2.9. Its honest p-value?** With independent tests, 1 − Φ(2.9)²⁰⁰ ≈ 0.31: no
   evidence at all. Computing it needs the number of tries and their dependence, which only the researcher knows
   (ch. 1).
3. **100 candidate signals, the ten best traded equally. Which error rate?** The false discovery rate, perhaps at
   10%: a dud among ten dilutes the book; the familywise rate is for single claims (ch. 2).
4. **An anomaly with t = 4 equal-weighted and t = 1.2 value-weighted with NYSE breakpoints. Real? Trade it?** It is
   probably real in microcaps, which are about 60% of stocks and 3% of value, and probably not tradable at scale. Size
   it to the capacity of the stocks that carry it, after costs, or leave it (ch. 3).
5. **A new paper reports t = 3.5 and 0.8% a month. What do you plan for?** A third to a half, 0.3–0.4% a month before
   costs: the zoo kept 38% after publication (ch. 4).
6. **A factor with t = 5 alone but an insignificant SDF loading after double selection. Hold it?** Only as a cheaper or
   better-implemented way to hold the factors that span it; it brings no new premium (ch. 7).

## Problems, with solutions

1. **The best of n.** For independent standard normals, max Zᵢ ≤ c exactly when every Zᵢ ≤ c, so the probability is
   Φ(c)ⁿ. The median maximum solves Φ(c)ⁿ = ½, Φ(c) = 2^{−1/n}; for n = 200, Φ(c) = 0.99654 and c ≈ 2.70.
2. **Bonferroni for the zoo.** p ≤ 0.05/212 = 0.000236 two-sided, so |t| ≥ Φ⁻¹(1 − 0.000118) ≈ 3.68.
3. **Three procedures.** Bonferroni (0.01): 0.001 and 0.008 pass, two rejections. Holm: 0.001 ≤ 0.01, 0.008 ≤ 0.0125,
   0.012 ≤ 0.0167, but 0.03 > 0.025: three. BH (thresholds 0.01, 0.02, 0.03, 0.04, 0.05): the largest k with
   p₍ₖ₎ ≤ 0.01k is k = 4 (0.03 ≤ 0.04): four.
4. **Empirical Bayes.** v = 6 − 1 = 5, shrink 5/6; E[θ | t = 7] = 4 + (5/6)(3) = 6.5.
5. **Ridge in components.** With Σ = Σₖ λₖ qₖqₖ', Σ + γI = Σₖ (λₖ + γ) qₖqₖ', so (Σ + γI)⁻¹μ = Σₖ (qₖ'μ)/(λₖ + γ) qₖ =
   Σₖ λₖ/(λₖ + γ) · (qₖ'μ/λₖ) qₖ, the unshrunk loading qₖ'μ/λₖ times λₖ/(λₖ + γ).
6. **Two directions.** Unshrunk: 0.002/0.01 = 0.2 and 0.002/0.0001 = 20. With γ = 0.001: 0.2 × 0.01/0.011 = 0.18 and
   20 × 0.0001/0.0011 = 1.82. The small-variance direction, with a Sharpe ratio ten times higher on the same mean, is
   distrusted: its loading falls elevenfold.
7. **RP-PCA at γ = −1.** (1/T)F'F − μ̄μ̄' = (1/T)Σₜ (Fₜ − μ̄)(Fₜ − μ̄)', the sample covariance with divisor T; its
   eigenvectors are PCA's.
8. **Attenuation.** plim λ̂ = λ · 0.01/(0.01 + 0.04) = 0.2λ: the premium is estimated at a fifth of its true size.
9. **Model comparison.** B, since 0.8 > 0.5. For traded factors, any test assets R give GRS(f; R) ∝ SR²(f, R) −
   SR²(f), and SR²(f, R) is the same for both models once R contains both sets of factors, so the model with the
   higher SR²(f) leaves less to explain for every R.
10. **Mining by chance.** Two-sided: 29,000 × 0.0455 ≈ 1,320 clear |t| > 2, and 29,000 × 0.0027 ≈ 78 clear |t| > 3,
    with no true premium anywhere (if independent).
11. **(qual) Benjamini and Hochberg's theorem.** BH rejects p_i iff p_i ≤ qR/m, so V/max(R, 1) = Σ_{i∈H₀}Σ_k
    (1/k)1{p_i ≤ qk/m, R = k}. Let R⁽ⁱ⁾ be the number of rejections with p_i set to 0, a function of p₋ᵢ only. On
    {p_i ≤ qk/m}, R = k iff R⁽ⁱ⁾ = k (p_i rejected with k rejections ⇒ lowering it changes nothing; conversely, if
    R⁽ⁱ⁾ = k and p_i ≤ qk/m, raising p_i from 0 leaves every count #{p ≤ qj/m}, j ≥ k, unchanged). By independence and uniformity,
    Pr(p_i ≤ qk/m, R⁽ⁱ⁾ = k) = (qk/m)Pr(R⁽ⁱ⁾ = k), so each null contributes (q/m)Σ_k Pr(R⁽ⁱ⁾ = k) = q/m, and
    FDR = m₀q/m = π₀q.
12. **(qual) Storey and the tail-area rate.** E#{p > λ} = m₀(1 − λ) + Σ_{i∈H₁}Pr(p_i > λ) ≥ m₀(1 − λ), so
    E π̂₀(λ) ≥ π₀ (before capping at 1). In the two-group model f = π₀φ + (1 − π₀)f₁, the tail-area false discovery
    rate is Fdr(z) = Pr(H₀ | Z ≥ z) = π₀Φ̄(z)/F̄(z) = ∫_z^∞ [π₀φ(u)/f(u)] f(u)du / F̄(z) = E[lfdr(Z) | Z ≥ z]: the tail
    rate averages the local rate over the tail, so it is smaller than lfdr at the threshold when lfdr decreases in z.

## For the researcher

* **The theorems.** Benjamini and Hochberg (1995), "Controlling the false discovery rate," *JRSS B* 57; Benjamini and
  Yekutieli (2001), *Annals of Statistics* 29, on dependence; Storey (2002), "A direct approach to false discovery
  rates," *JRSS B* 64; Storey and Tibshirani (2003), *PNAS* 100; Storey, Taylor and Siegmund (2004), *JRSS B* 66;
  Efron, Tibshirani, Storey and Tusher (2001), *JASA* 96, and Efron, *Large-Scale Inference* (2010), on the two-group
  model and the local false discovery rate. In finance: Harvey, Liu and Zhu (2016); McLean and Pontiff (2016);
  Jensen, Kelly and Pedersen (2023).
* **Simplifications.** One-sided p-values from the post-publication t-statistics in the published direction; a
  standard normal null (Efron's empirical null, fitted to the centre, would differ); a Gaussian kernel for the
  mixture density; λ = ½ for π̂₀; anomalies treated as independent.
* **Open problems.** Standard errors of π̂₀ and lfdr under realistic dependence; separating anomalies that were never
  real from those traded away; testing against an economically meaningful null rather than zero.

## Data and reproducibility

* Open Source Asset Pricing, release 2024.10 (Hugging Face: OpenSourceAP/CrossSection): `PredictorLSretWide.parquet`
  (original-paper long–short portfolios, monthly, percent) and `SignalDoc.csv`; cached and checksummed by Part 3. The
  release's hold-out months (2021-01 to 2023-12) were sealed in Part 3 and are read only in `envelope`.
* Kenneth French's five factors and momentum; global-q.org's q5 factors (for the model comparison, 1967–2020).
* Registered here: `kns_sdf_part25` (20 trials: the κ grid) and `zoo_equal_weight_part25` (1); the counter rises from
  325 to 346. Placeholder costs: 2% a year for the SDF, 1% for equal weights, until Part 26.
* Published figures quoted, not computed: Hou–Xue–Zhang's failure rates; Jensen–Kelly–Pedersen's sample;
  McLean–Pontiff's percentages; Chen–Lopez-Lira–Zimmermann's retention; Harvey–Liu–Zhu's count; Fama–French's
  microcap shares.
* Simulated or illustrative: the 200 coins, the best-of-n curve, the weak-factor histograms, the five p-values, the two
  directions, the lasso toy, the Ioannidis arithmetic.

---

# 量化金融，从零搭建 — 第25部分：因子动物园

本部分是第四幕“收益溢价”（第23–29部分）的第三部分。第24部分认识了经典因子；本部分面对此后发表的数以百计的因子，以及区分少数真实因子与大量“找出来”的因子所需的统计方法。本部分讲：

* 多个噪声策略中最好的一个，以及试验次数所要求的门槛；Harvey、Liu与Zhu的t > 3；一个领域的假阳性算术；
* 多重检验：族错误率（Bonferroni、Holm）、错误发现率（Benjamini–Hochberg）、自助法（White、Romano–Wolf），用于212个已发表预测变量的样本内与发表后；
* 复现：Hou–Xue–Zhang对Jensen–Kelly–Pedersen，以及Chen与Zimmermann的开源资产定价；
* 衰减：经验贝叶斯收缩对发表后的记录、McLean与Pontiff的时间线、发表偏差与数据类别；
* 数据挖掘的信号对同行评审的信号（Chen、Lopez-Lira与Zimmermann；Yan与Zheng）；
* Kozak、Nagel与Santosh在154个预测变量上经交叉验证的收缩SDF；
* Feng、Giglio与Xiu对新因子相对于动物园的双重选择检验；
* 弱因子（Kan–Zhang、Kleibergen、Giglio–Xiu）与三步估计；
* PCA、风险溢价PCA（Lettau–Pelger）与工具化PCA（Kelly–Pruitt–Su）；
* 用平方夏普比率比较模型（Barillas–Shanken；Fama–French 2018；Bryzgalova–Huang–Julliard）；
* 收缩SDF与动物园的等权组合，登记并在2021–2023年上打开。

*讲的是方法，不构成投资建议。预测变量的收益是其原始组合的纸面收益，未扣除现实的交易成本。*

## 章节（约56分钟）

* **两百枚硬币。** 200个噪声策略，各20年：五个超过t = 1.96，最好的t = 2.89；抽屉问题与分岔路径；动物园按发表年份的数量（2000年51个，2016年212个）；历史条（1979–2023）；本部分安排；SDF模型。
* **1. 数以百计的因子与上升的门槛。** 最大值的规律；200个中最好者的诚实p值（t = 2.9：单独0.0019，作为200个中最好者0.31）；一个领域的算术（Ioannidis：π = 0.1、检验力0.5时，显著结果中53%为真）；模拟的最佳t对n（10个1.5，200个2.8，1000个3.3）；随动物园增长的Bonferroni门槛（1980年2.58，2000年3.30，2016年3.68）；Harvey–Liu–Zhu（316个因子，t > 3）；动物园复现的t（87%高于1.96，58%高于3）。
* **2. 多重检验：FWER与FDR。** FWER与Bonferroni（212个检验需|t| ≥ 3.68）；Holm的逐步下降；FDR与Benjamini–Hochberg；V/R表；手算五个p值（Bonferroni 2个、Holm 3个、BH 4个）；动物园发表后p值上的BH线；计数（样本内：212个中原始185、Bonferroni 86、Holm 91、BH 184；发表后，单侧：208个中59、7、8、24）；自助法（White；Romano–Wolf）；q的选择；该控制哪种错误。
* **3. 复现与开源资产定价。** Hou–Xue–Zhang（452个中65%达不到|t| ≥ 1.96；门槛2.78时82%）；Chen与Zimmermann的数据发布；其内容；发表的t对复现的t（188个预测变量：88%复现t > 1.96，中位数比率0.90，相关系数0.75）；构造方法；微盘股（约60%的股票、3%的市值）；Jensen–Kelly–Pedersen（153个因子、93个国家、13个主题）。
* **4. 衰减、收缩与发表偏差。** t的经验贝叶斯（方差5.9，收缩0.83）；算例（7 → 6.5；2.5 → 2.7）；样本内对发表后的均值（208个预测变量：每月0.69% → 0.26%，保留38%，斜率0.43）；仅噪声对实际记录（83%对38%）；McLean–Pontiff的时间线（样本外−26%，发表后−58%）；按数据类别（价格0.29、分析师0.34、会计0.38、交易0.45、事件0.64）；Chen–Zimmermann的发表偏差（很小）；按三分之一到一半来计划。
* **5. 数据挖掘对同行评审。** Chen–Lopez-Lira–Zimmermann的29,000个会计比率；偶然性给出的结果（约1,320个超过|t| > 2，78个超过3）；两组都约有一半存活；风险解释并不更好；Yan–Zheng的自助法；区分二者的是计数。
* **6. 收缩横截面。** 对154个因子线性的SDF及其直接估计；KNS的先验与岭回归后验；主成分解读；两个方向的算例；交叉验证路径（样本外R²在κ约为每年1.0时达峰值0.30，不收缩时为−1.0）；分块、度量、网格；最大载荷（短期反转居首）；1973–2000拟合、2001–2020持有（夏普比率：切点组合15.5 → 2.6，KNS 6.1 → 1.9，等权2.8 → 1.2）；主成分上的稀疏性；纸面收益。
* **7. 驯服动物园。** SDF载荷问题；lasso及其偏差；一个玩具例子；双重选择；2011年以来发表的25个因子对2003年前发表的53个（自身t > 1.96：21个；朴素SDF t：14个；双重选择：5个）。
* **8. 弱因子。** 贝塔接近零时的第二步；一个模拟（强因子：中位数0.48%，真值0.5%；弱因子：中位数0.07%，10–90%区间−0.58%到0.75%）；衰减（var(β)/(var(β) + var(u)) = 0.2的算例）；遗漏因子（Giglio–Xiu）；三步估计。
* **9. PCA、RP-PCA与IPCA。** 碎石图（第一个成分34%，五个67%，十个76%）；RP-PCA；第一个成分（PCA样本外夏普比率−0.03，RP-PCA 0.88）；按K的样本外夏普比率（K = 5：PCA 0.39，RP-PCA 1.99）；γ；RMS阿尔法（没有因子时5.1%；十个成分时两种方法都约为4%）；IPCA；各自优化的是什么。
* **10. 比较模型。** Barillas–Shanken的洞见；检验资产如何误导；有名字的模型（1967–1993年的SR²：CAPM 0.10、FF3 0.73、Carhart 1.80、FF5 2.77、FF6 3.53、q4 4.37、q5 7.13；样本外夏普比率0.57到1.47）；382个模型（秩相关0.77）；前五名（混合各族）；Fama–French的“选择因子”；贝叶斯模型平均（Bryzgalova–Huang–Julliard）。
* **11. 收缩SDF，登记并打开。** 登记了什么（20次试验和1次）；结果（研究期夏普比率4.6和2.1；2021–23年：每年+34.7%、夏普比率3.06 ± 0.60，以及+7.2%、2.14 ± 0.63）；路径；成本盈亏平衡（约每年35%）；注意事项（纸面收益、杠杆）；为什么样本外不需要修正；接下来会怎样；计数器325 → 346。
* **12. 第25条规则：SDF模型。** 按部分的试验次数；第一张表；**实验**：`kns_b`、`rp_pca`、`double_selection`；`zoo`模块；第25条规则；用本部分的案例检验这条规则。
* **写给研究者：有多少异象是真的？** Benjamini–Hochberg定理：独立检验下FDR = π₀q，并给出证明的关键一步（把p_i换成0；此时拒绝个数R⁽ⁱ⁾与p_i独立，且Σ_k (1/k)(qk/m)Pr(R⁽ⁱ⁾ = k) = q/m）。Storey的π̂₀(λ) = #{p > λ}/(m(1 − λ))，是保守的。208个检验的模拟动物园（400次重复，真实效应的t均值服从均值为2的伽马分布）：实际FDR为0.030、0.047、0.083，对应π₀q = 0.03、0.05、0.08；π₀ = 0.3、0.5、0.8时π̂₀ = 0.44、0.60、0.84（± 0.06–0.07）。动物园：样本内p值经过挑选（π̂₀ = 0.03，没有意义）；208个发表后的t统计量给出π̂₀(½) = 0.375，π̂₀(λ)从0.75（λ = 0.05）降到0.14（λ = 0.9），说明最右端比均匀分布更稀。Efron的两组模型，混合密度用核估计：70个异象的lfdr < 0.2，Σ(1 − lfdr) ≈ 135个真实效应；10%水平的BH找到41个，经Storey调整的BH找到76个。发表后最强的：DivYieldST（t 9.7）、AnnouncementReturn（7.3）、AnalystRevision（6.6）。三个开放问题；暂停题：π̂₀ = 0.76，所以约0.076 × 120 ≈ 9个错误发现。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十二道习题（两道为资格考试难度），解答见下文。

## 交易台问题与解答

1. **200个策略，全是噪声。预期最好的t是多少？** 约2.8；如果允许把亏损策略翻转为做空，约3.0；5–95%区间大约为2.2到3.5。n个近似正态抽样的最大值按√(2 ln n)增长（第1章）。
2. **你报告了200个中最好的一个，t = 2.9。它诚实的p值是多少？** 检验独立时，1 − Φ(2.9)²⁰⁰ ≈ 0.31：毫无证据。计算它需要知道尝试的次数及其相依性，而这只有研究者知道（第1章）。
3. **100个候选信号，等权交易最好的十个。控制哪种错误率？** 错误发现率，也许取10%：十个中有一个无效信号只会稀释组合；族错误率适用于单一的主张（第2章）。
4. **一个异象等权t = 4，按NYSE断点市值加权t = 1.2。是真的吗？要交易吗？** 它在微盘股中大概是真的——微盘股约占股票数量的60%、市值的3%——但大概无法大规模交易。按承载它的那些股票的容量、扣除成本后确定规模，或者放弃（第3章）。
5. **一篇新论文报告t = 3.5、每月0.8%。你按多少来计划？** 三分之一到一半，即扣除成本前每月0.3–0.4%：动物园在发表后保留了38%（第4章）。
6. **一个因子单独t = 5，但双重选择后其SDF载荷不显著。要持有吗？** 只有当它是持有张成它的那些因子的更便宜或实现得更好的方式时才持有；它没有带来新的溢价（第7章）。

## 习题与解答

1. **n个中的最大值。** 对独立标准正态变量，max Zᵢ ≤ c当且仅当每个Zᵢ ≤ c，所以概率为Φ(c)ⁿ。最大值的中位数满足Φ(c)ⁿ = ½，即Φ(c) = 2^{−1/n}；n = 200时，Φ(c) = 0.99654，c ≈ 2.70。
2. **动物园的Bonferroni。** 双侧p ≤ 0.05/212 = 0.000236，所以|t| ≥ Φ⁻¹(1 − 0.000118) ≈ 3.68。
3. **三种程序。** Bonferroni（0.01）：0.001和0.008通过，拒绝两个。Holm：0.001 ≤ 0.01，0.008 ≤ 0.0125，0.012 ≤ 0.0167，但0.03 > 0.025：三个。BH（阈值0.01、0.02、0.03、0.04、0.05）：满足p₍ₖ₎ ≤ 0.01k的最大k为k = 4（0.03 ≤ 0.04）：四个。
4. **经验贝叶斯。** v = 6 − 1 = 5，收缩5/6；E[θ | t = 7] = 4 + (5/6)(3) = 6.5。
5. **主成分中的岭回归。** 由Σ = Σₖ λₖ qₖqₖ'，Σ + γI = Σₖ (λₖ + γ) qₖqₖ'，所以(Σ + γI)⁻¹μ = Σₖ (qₖ'μ)/(λₖ + γ) qₖ = Σₖ λₖ/(λₖ + γ) · (qₖ'μ/λₖ) qₖ，即未收缩的载荷qₖ'μ/λₖ乘以λₖ/(λₖ + γ)。
6. **两个方向。** 未收缩：0.002/0.01 = 0.2，0.002/0.0001 = 20。γ = 0.001时：0.2 × 0.01/0.011 = 0.18，20 × 0.0001/0.0011 = 1.82。方差小的方向，同样的均值下夏普比率高十倍，最不被信任：它的载荷下降到十一分之一。
7. **γ = −1时的RP-PCA。** (1/T)F'F − μ̄μ̄' = (1/T)Σₜ (Fₜ − μ̄)(Fₜ − μ̄)'，即除数为T的样本协方差；它的特征向量就是PCA的。
8. **衰减。** plim λ̂ = λ · 0.01/(0.01 + 0.04) = 0.2λ：溢价被估计为真实大小的五分之一。
9. **模型比较。** B，因为0.8 > 0.5。对可交易因子，任何检验资产R都给出GRS(f; R) ∝ SR²(f, R) − SR²(f)，而当R包含两组因子时，SR²(f, R)对两个模型相同，所以SR²(f)更高的模型对每个R留下的待解释部分都更少。
10. **偶然挖掘。** 双侧：29,000 × 0.0455 ≈ 1,320个超过|t| > 2，29,000 × 0.0027 ≈ 78个超过|t| > 3，而且哪里都没有真实溢价（若相互独立）。
11. **（资格考试）Benjamini–Hochberg定理。** BH拒绝p_i当且仅当p_i ≤ qR/m，所以V/max(R, 1) = Σ_{i∈H₀}Σ_k (1/k)1{p_i ≤ qk/m, R = k}。令R⁽ⁱ⁾为把p_i设为0后的拒绝个数，它只是p₋ᵢ的函数。在{p_i ≤ qk/m}上，R = k当且仅当R⁽ⁱ⁾ = k（p_i在共k个拒绝中被拒绝 ⇒ 把它调低什么也不改变；反之，若R⁽ⁱ⁾ = k且p_i ≤ qk/m，把p_i从0调回原值不改变任何j ≥ k的计数#{p ≤ qj/m}）。由独立性和均匀性，Pr(p_i ≤ qk/m, R⁽ⁱ⁾ = k) = (qk/m)Pr(R⁽ⁱ⁾ = k)，所以每个零假设贡献(q/m)Σ_k Pr(R⁽ⁱ⁾ = k) = q/m，FDR = m₀q/m = π₀q。
12. **（资格考试）Storey与尾部错误发现率。** E#{p > λ} = m₀(1 − λ) + Σ_{i∈H₁}Pr(p_i > λ) ≥ m₀(1 − λ)，所以E π̂₀(λ) ≥ π₀（截断到1之前）。在两组模型f = π₀φ + (1 − π₀)f₁中，尾部错误发现率Fdr(z) = Pr(H₀ | Z ≥ z) = π₀Φ̄(z)/F̄(z) = ∫_z^∞ [π₀φ(u)/f(u)] f(u)du / F̄(z) = E[lfdr(Z) | Z ≥ z]：尾部率是局部率在尾部上的平均，所以当lfdr随z递减时，它小于阈值处的lfdr。

## 数据与复现

* 开源资产定价，2024.10版（Hugging Face：OpenSourceAP/CrossSection）：`PredictorLSretWide.parquet`（原论文的多空组合，月度，百分比）和`SignalDoc.csv`；由第3部分缓存并校验哈希。该版本的样本外月份（2021-01到2023-12）在第3部分封存，只在`envelope`中读取。
* Kenneth French的五因子与动量；global-q.org的q5因子（用于模型比较，1967–2020）。
* 本部分登记：`kns_sdf_part25`（20次试验：κ网格）和`zoo_equal_weight_part25`（1次）；计数器从325升到346。第26部分之前的占位成本：SDF每年2%，等权每年1%。
* 引用而非计算的公开数字：Hou–Xue–Zhang的失败率；Jensen–Kelly–Pedersen的样本；McLean–Pontiff的百分比；Chen–Lopez-Lira–Zimmermann的保留率；Harvey–Liu–Zhu的计数；Fama–French的微盘股份额。
* 模拟或示意：200枚硬币、最佳n曲线、弱因子直方图、五个p值、两个方向、lasso玩具例子、Ioannidis算术。

## 写给研究者

* **定理。** Benjamini与Hochberg（1995），*JRSS B* 57；Benjamini与Yekutieli（2001），*Annals of Statistics* 29，论相关情形；Storey（2002），*JRSS B* 64；Storey与Tibshirani（2003），*PNAS* 100；Storey、Taylor与Siegmund（2004），*JRSS B* 66；Efron、Tibshirani、Storey与Tusher（2001），*JASA* 96，以及Efron的*Large-Scale Inference*（2010），论两组模型与局部错误发现率。金融中：Harvey、Liu与Zhu（2016）；McLean与Pontiff（2016）；Jensen、Kelly与Pedersen（2023）。
* **简化。** 用发表后t统计量在发表方向上的单侧p值；标准正态零分布（Efron按中心拟合的经验零分布会不同）；混合密度用高斯核；π̂₀取λ = ½；把异象视为相互独立。
* **开放问题。** 现实相关结构下π̂₀和lfdr的标准误；区分从来不真的异象与被交易掉的异象；针对有经济意义的零假设而非零做检验。
