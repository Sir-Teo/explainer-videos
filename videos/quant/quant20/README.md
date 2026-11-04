# Quant, Built — Part 20: Credit

Part 20 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), part of Act III, Derivatives (Q), and the third of its five parts on rates, credit and the basis (18–22). Parts 18 and 19 priced bonds that
always pay; this part prices the chance that they do not. It covers:

* what a credit spread measures, from seventy years of Moody's yields, and the credit spread puzzle;
* structural models: Merton (1974), the distance to default run every day on three real companies from their prices
  and filings, Black–Cox first passage, Leland's chosen barrier and optimal leverage;
* reduced form: default as a random clock (Jarrow–Turnbull, Duffie–Singleton, Lando's CIR intensity); the credit
  default swap's legs, a bootstrapped hazard curve, CS01 and jump to default, the 2009 Big Bang, auctions;
* default prediction on a dataset built entirely from EDGAR: bankruptcy filings (8-K Item 1.03) as labels, XBRL
  frames as features; Altman's Z (1968) and a re-weighted version, a logit and gradient-boosted trees, registered
  before the sealed 2021–2023 firm-years were opened;
* portfolios: Vasicek's large pool and the Basel IRB formula, finite pools, Gaussian and t copulas, default
  correlation, first-to-default baskets, CDO tranches, random recovery, base correlation;
* from the public record: 2007–08's senior tranches (Coval–Jurek–Stafford; the FCIC), the London Whale (2012), March
  2020 in corporate bonds; private credit and its marks.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's new
[`credit`](../../../explainer/quant/house/credit.py) module). Data: FRED (Moody's Baa and Aaa, Treasury yields,
recessions), EDGAR (XBRL frames and company facts, full-text search of 8-K filings), and daily prices.

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 54 minutes)

* **What a promise is worth** (2.1 min). Lehman, 15 September 2008; the CDS auction of 10 October (8.625); the Baa
  spread to 6.16% (4 December 2008); the history strip (1968–2024); the plan; the credit desk opens.
* **1. What a credit spread measures** (2.5). Baa and Aaa over the 10-year Treasury since 1953 with recessions
  (averages 1.91% and 0.95%; 4.31% on 23 March 2020); Baa minus Aaa (0.97% on average, 3.38% at the end of 2008);
  expected loss, risk premium, liquidity; the credit triangle; Huang–Huang, Longstaff–Mithal–Neis,
  Collin-Dufresne–Goldstein–Martin.
* **2. Merton: debt as an option** (3.0). Payoffs; the model derived; the 5-year spread over (leverage, volatility) in
  3D; term structures and the short-spread failure; the puzzle in numbers (a Baa-like firm: 37 bp against 191);
  **lab**: `merton_solve`.
* **3. Distance to default, from prices** (2.9). KMV's recipe on Boeing, American Airlines and Norwegian Cruise Line,
  2018–2025 (worst: 0.96, 0.41, 0.12; Norwegian's Merton PD 45% on 13 May 2020); equity against the default point;
  Merton's one-year spreads (peaks 331, 536 and 1,630 bp; about zero in 2019); EDF and Bharath–Shumway.
* **4. First passage and the choice to default** (2.5). Black–Cox paths and formula (10-year PD 24% terminal, 54%
  first passage); CreditGrades; Leland (1994) derived and computed (optimal leverage 75%, spread 75 bp).
* **5. Default as a random clock** (2.9). Hazards and survival as discounting; 200 simulated clocks; risky zeros under
  three recovery conventions; risk-neutral against real-world PDs; Lando's Cox process; CIR intensity curves (35 to
  101 bp for a calm name, 458 to 189 for a stressed one).
* **6. The credit default swap** (3.8). The contract (J.P. Morgan, 1994); the legs derived; a hazard curve bootstrapped
  from illustrative quotes; CS01 ($4,249 on $10 m) and jump to default ($6 m); the Big Bang (8 April 2009: upfronts of
  −1.8%, −10.2%, +20.3%); the two-stage auction; the CDS–bond basis; **lab**: `bootstrap_hazard`.
* **7. Seventeen years of bankruptcies** (2.0). 1,265 Item 1.03 filings by 1,225 companies, 2009–2025 (232 in 2009, 19
  in 2021, 88 in 2023); correlation 0.73 with the Baa spread, 0.38 a year ahead; decile sorts (top leverage decile
  3.9% a year against 0.8%); the dataset's construction.
* **8. Altman's Z** (2.1). The 1968 formula and zones; on the sealed years, AUC 0.815 (distress zone 1.9% a year, 55%
  of filers); re-weighted by a logit on 2010–16, validation AUC 0.827 against 0.794; four ratios, survivors against
  bankrupt firms.
* **9. Logit and boosted trees, sealed** (3.8). Shumway's hazard logit and the House's gradient boosting; a tree;
  sealed 2021–23 AUC 0.815 / 0.867 / 0.905 (Altman / logit / trees), the trees' top decile holding 68% of the
  bankruptcies; by period, the trees from 0.976 in sample to 0.905; Brier scores against the base rate; calibration by
  decile; the learned surface over leverage and the market cushion in 3D; importance and coefficients; **lab**: the
  histogram split; the trial counter 313 → 315.
* **10. The large pool and bank capital** (2.8). Vasicek derived; loss densities (99.9th percentiles 8.1%, 17.6%, 33.3%
  for ρ = 0.05, 0.15, 0.30 at PD 2%); finite pools (22.0%, 18.5%, 17.6% for 50, 200, 1,000 loans); the Basel IRB
  formula (risk weight 92.32% at PD 1%; capital about 16 times the expected loss).
* **11. Copulas: defaults together** (2.9). Sklar and Li; joint default (ρ = 0.3: default correlation 0.065, joint
  probability 17 bp against 4); Gaussian and t clouds; a five-name first-to-default basket (507 bp independent, 125 at
  ρ = 0.99); a 125-name pool's tail (P(loss > 15%) 0.08% against 1.3%).
* **12. CDOs and tranches** (2.6). The waterfall; tranche expected loss against correlation; May 2005; random recovery
  (senior expected loss 1.1 → 5.4 bp) and deltas (0.67, 0.26, 0.005); the base-correlation skew (0.16 to 0.55).
* **13. 2007–08: the senior tranches** (2.6). The economic catastrophe bond (losses only below the 0.16th percentile;
  expected loss 3.7 bp against 120 for the pool); repricing (expected loss ×710 when PD doubles and ρ goes from 0.15 to
  0.4); the FCIC's findings on 2006's AAA mortgage securities (83% downgraded); CDO-squared.
* **14. 2012: the London Whale** (1.9). The CIO's synthetic credit portfolio ($6.2 bn of losses; $920 m of penalties);
  the VaR model change and the spreadsheet error; three lessons.
* **15. Corporate bonds and March 2020** (2.3). LQD −20% and HYG −22% by mid-March; the Baa spread 2.05% → 4.31% → 2.93%;
  the Fed's corporate credit facilities and Haddad–Moreira–Muir; credit factors and the distress puzzle.
* **16. Private credit and its marks** (2.0). The asset class (about $2.1 tn, IMF); Ares Capital's price ($8.08 on 23
  March 2020) against its reported NAV ($17.32 → $16.97); quarterly volatility 4.5% (NAV) against 19.8% (shares);
  smoothed returns (Getmansky–Lo–Makarov).
* **17. Rule 20: the credit desk** (1.7). Two default probabilities for the same firms, from accounts and from prices;
  AMR's 13% from its 2010 accounts; the credit module; Rule 20.
* **For the researcher: the granularity adjustment** (6.1). For N equal loans in Vasicek's model, NL | y ~
  Binomial(N, p(y)) and P(L ≤ k/N) = ∫Bin(k; N, p(y))φ(y)dy exactly; as N → ∞ the α-quantile tends to the ASRF value
  p(Φ⁻¹(α)). Gordy's (2003) adjustment (Gouriéroux–Laurent–Scaillet 2000; Martin and Wilde 2002) adds
  GA = −(1/(2φ))d/dy[φσ²/μ′], here (1/(2N))[yp(1 − p)/(bφ(z)) − (1 − 2p) − zp(1 − p)/φ(z)], 2.04/N at PD 1%, ρ 0.12,
  α 99.9%. Exact against ASRF: 10.5% against 9.0% at N = 100 (a sixth more capital), 9.6% at 250, 9.2% at 1,000;
  ASRF + GA 11.1/9.9/9.2%, accurate from about 250 loans, overcorrecting at 25–50; Monte Carlo agrees. Relative
  adjustment largest at low correlation (ρ 0.24: c = 1.48; PD 3%: c = 2.32). A Zipf book of 500 loans (largest 14.7%):
  effective N = 1/HHI = 28, MC 99.9% loss 19.6% against ASRF 9.0% and ASRF + GA(28) 16.3%. Portfolio invariance holds
  only in the ASRF limit (Gordy 2003), which is why Pillar 1 omits the term. Three open problems; pause: the
  one-plus-399 book has HHI ≈ 0.25 + 0.25/399, effective N ≈ 4.
* **Recap, desk questions, ten problems (two at qualifying-exam level)** (2.9). Thirteen lines; four desk questions;
  solutions below.

## Hands-on

* **Labs** (the House's own code on screen, then run): `merton_solve` (ch. 2), `bootstrap_hazard` (ch. 6), the
  boosted trees' histogram split (ch. 9).
* **Computed from filings:** distances to default for three companies, every day for eight years; a 47,762 firm-year
  dataset with 433 bankruptcies; two registered models scored once on sealed years.
* **Live constructions:** Merton's payoffs; barrier paths; default clocks; the CDS legs and auction; a decision tree;
  the tranche waterfall filling; copula clouds.
* **3D:** Merton's spread over leverage and volatility; the trees' bankruptcy probability over leverage and the market
  cushion.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| O'Kane, *Modelling Single-name and Multi-name Credit Derivatives* | 3 (credit risk modelling), 5–7 (the CDS: pricing, curve building, risk), 12–13 (copulas, the LHP model), 14–17 (CDOs, base correlation) | ch. 5–6, 10–13 |
| Schönbucher, *Credit Derivatives Pricing Models* | 2 (structural), 5–7 (intensities), 10 (copulas) | ch. 2–5, 11 |
| Duffie and Singleton, *Credit Risk* | 3 (structural), 5–6 (reduced form, recovery), 10 (correlated defaults) | ch. 2–5, 11 |
| Lando, *Credit Risk Modeling* | 2–3 (Merton, first passage), 4 (statistical default prediction), 5 (intensities), 9 (dependence) | ch. 2–5, 8–11 |
| Hull, *Options, Futures, and Other Derivatives* | 24 (credit risk), 25 (credit derivatives) | ch. 1, 6, 12 |

## Papers, chapter by chapter

* Hook and ch. 1: Moody's seasoned yields (FRED); Creditex and Markit (2008), Lehman auction results; Huang and Huang
  (2012); Longstaff, Mithal and Neis (2005); Collin-Dufresne, Goldstein and Martin (2001).
* ch. 2–4: Merton (1974); Black and Scholes (1973); Jensen and Meckling (1976); Black and Cox (1976); Leland (1994);
  Duffie and Lando (2001); Finger et al., *CreditGrades Technical Document* (2002); Crosbie and Bohn (2003); Vassalou
  and Xing (2004); Bharath and Shumway (2008).
* ch. 5–6: Jarrow and Turnbull (1995); Lando (1998); Duffie and Singleton (1999); Hull, Predescu and White (2005);
  ISDA, the Big Bang protocol (2009).
* ch. 7–9: Altman (1968); Shumway (2001); Campbell, Hilscher and Szilagyi (2008); Friedman (2001); Chen and Guestrin
  (2016).
* ch. 10–13: Vasicek (1987, 2002); Gordy (2003); Basel Committee (2004, 2005, an explanatory note on the IRB risk
  weights); Sklar (1959); Li (2000); Andersen and Sidenius (2004); Altman, Brady, Resti and Sironi (2005); Coval, Jurek
  and Stafford (2009); FCIC, *The Financial Crisis Inquiry Report* (2011).
* ch. 14: JPMorgan Chase, *Report of the Management Task Force Regarding 2012 CIO Losses* (2013); U.S. Senate PSI,
  *JPMorgan Chase Whale Trades* (2013).
* ch. 15–16: Federal Reserve press releases (23 March and 9 April 2020); Haddad, Moreira and Muir (2021); Bai, Bali and
  Wen (2019); Dickerson, Mueller and Robotti (2023); Getmansky, Lo and Makarov (2004); IMF, *Global Financial Stability
  Report* (April 2024).

## Build it

```bash
python -m videos.quant.quant20.compute                       # every item (fetches and caches the data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant20 Models  # one chapter, silent, with a contact sheet
python tools/make.py quant20 --cpu-voice -q m                # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **A 5-year CDS trades at 100 bp, recovery 40%. Annual default probability?** The credit triangle: λ ≈ s/(1 − R) =
   0.01/0.6 = 1.67% a year, so about 1 − e^{−5λ} = 8% over five years. It is a risk-neutral probability: it includes
   the premium for bearing default risk, and historical default rates for such names are lower (ch. 5).
2. **Why are equity holders long volatility and bondholders short it?** In Merton's model equity is a call on the
   firm's assets struck at the debt; bondholders hold a safe bond minus a put. More asset volatility raises both
   options' values, so it transfers value from bondholders to shareholders: asset substitution. Covenants and
   collateral exist to limit it.
3. **Why can a senior tranche with a tiny expected loss deserve a wide spread?** Its losses arrive only in the worst
   states of the economy (ch. 13: below the 0.16th percentile), when every other asset is also losing and money is
   worth most. A price that weights losses by when they arrive charges far more than the expected loss; a rating on
   expected loss alone calls it as safe as a government bond.
4. **A default model scores 0.98 in sample and 0.90 out of sample. Which do you report?** The out-of-sample one, on data
   sealed before the model was fitted; the gap is what the model memorized (ch. 9). And calibration must be checked
   separately: rankings survive the credit cycle better than probabilities do.

## Problems, with solutions

1. **Merton's debt.** B = V − E = V − [V N(d₁) − D e^{−rT} N(d₂)] = D e^{−rT} N(d₂) + V N(−d₁). The yield is
   −ln(B/D)/T, so the spread is s = −(1/T) ln[N(d₂) + (V e^{rT}/D) N(−d₁)].
2. **Equity volatility.** By Itô, dE = (∂E/∂V) dV + …, and ∂E/∂V = N(d₁), so σ_E E = N(d₁) σ_V V. As the firm nears
   default, E falls faster than N(d₁)V: equity becomes a leveraged claim on the assets and its volatility rises.
3. **The par spread with a flat hazard.** With continuous premiums, premium leg = s ∫₀ᵀ e^{−(r+λ)t} dt and protection
   leg = (1 − R) ∫₀ᵀ λ e^{−(r+λ)t} dt. The integrals are equal, so s = (1 − R)λ exactly.
4. **A bootstrap by hand.** λ ≈ 0.012/0.6 = 2.0%. With annual premiums the risky annuity is Σ e^{−(0.04+0.02)t} ≈ 0.942
   + 0.887 + 0.835 = 2.664, and the protection leg is about 0.6 × Σ e^{−0.04t}(e^{−0.02(t−1)} − e^{−0.02t}) ≈ 0.0323;
   the spread they imply, 0.0323/2.664 = 121 bp, is close enough that one more step (λ ≈ 1.96%) reprices 120 bp.
5. **Vasicek's distribution.** Given M, defaults are independent with probability p(M) = N((N⁻¹(p) − √ρ M)/√(1 − ρ)); in
   a large pool L = p(M). Then P(L ≤ x) = P(M ≥ (N⁻¹(p) − √(1 − ρ) N⁻¹(x))/√ρ) = N((√(1 − ρ) N⁻¹(x) − N⁻¹(p))/√ρ), and
   the q-quantile is N((N⁻¹(p) + √ρ N⁻¹(q))/√(1 − ρ)).
6. **Basel capital at PD 2%.** ρ = 0.12w + 0.24(1 − w) with w = (1 − e^{−1})/(1 − e^{−50}) = 0.632: ρ = 0.164. The
   conditional PD at the 99.9th percentile is N((N⁻¹(0.02) + √0.164 × 3.09)/√0.836) = N((−2.054 + 1.252)/0.914) =
   N(−0.877) = 19.0%. With b = (0.11852 − 0.05478 ln 0.02)² = 0.111, K = 0.45 × (0.190 − 0.02) × 1/(1 − 0.166) = 9.2%
   of exposure, about ten times the expected loss of 0.9%.
7. **Tranches and correlation.** The pool's expected loss does not depend on ρ. As ρ rises the distribution of L spreads
   out: more mass near zero and more in the tail. The equity tranche's loss min(L, d)/d is concave in L, so spreading L
   lowers its expectation; a senior tranche's loss is convex near its attachment, so spreading raises it.
8. **Odds in a logit.** log-odds rise by 0.5 × 2 = 1.0, so the odds are multiplied by e¹ = 2.72; for a rare event the
   probability is multiplied by about the same.
9. **(qual) The finite pool.** Given Y = y, the N defaults are independent Bernoulli(p(y)), so NL | y ~ Bin(N, p(y));
   integrate over the factor. As N → ∞, L − p(Y) → 0 in probability given Y (law of large numbers), so L → p(Y) and,
   p being increasing and continuous, q_α(L) → p(q_α(Y)) = p(Φ⁻¹(α)).
10. **(qual) The granularity expansion.** Let x_ε be the α-quantile of μ(Y) + εU, with g the density of μ(Y).
   Conditioning on Y and expanding to second order in ε (the first-order term vanishes since E[U | Y] = 0),
   in the form of Gouriéroux, Laurent and Scaillet,
   x_ε = x₀ − (ε²/(2g(x₀)))∂/∂x{E[U² | μ = x]g(x)}|_{x₀} + o(ε²). Changing variables to y, with
   g(x) = h(y)/μ′(y) and ∂/∂x = (1/μ′)∂/∂y, gives −(ε²/(2h(y)))d/dy[h(y)Var(U | y)/μ′(y)] at y = q_α(Y).

## For the researcher

* **The theorems.** Vasicek (2002), "The distribution of loan portfolio value," *Risk*; Gordy (2003), "A risk-factor
  model foundation for ratings-based bank capital rules," *J. Financial Intermediation* 12; Gouriéroux, Laurent and
  Scaillet (2000), "Sensitivity analysis of values at risk," *J. Empirical Finance* 7; Martin and Wilde (2002),
  "Unsystematic credit risk," *Risk*; Pykhtin (2004), "Multi-factor adjustment," *Risk*; Gordy and Lütkebohmert
  (2013), *Int. J. Central Banking*.
* **Simplifications.** One factor; full loss given default; equal loans for the exact formula; the lumpy book by
  Monte Carlo.
* **Open problems.** Many factors; small, lumpy books; estimation risk in PD and ρ.

## Data and reproducibility

* FRED: BAA, AAA, GS10 (monthly), BAA10Y (daily), USREC; frozen through 31 December 2025 and checksummed.
* EDGAR full-text search: every 8-K reporting Item 1.03, 2009–2025 (a company's first filing per episode); XBRL frames
  for 14 concepts, 2010–2023, and the public float (dei); company facts for Boeing, American Airlines, Norwegian Cruise
  Line and Ares Capital. All public, keyless, fetched politely and cached.
* Daily closes (Yahoo Finance) for BA, AAL, NCLH, LQD, HYG and ARCC.
* Published figures quoted, not computed: Lehman's auction price; the FCIC's findings; the JPMorgan task force's and
  the Senate's figures; the Federal Reserve's facilities; the IMF's estimate of private credit.
* Illustrative inputs, labelled on screen: the CDS quotes, the copula and tranche parameters, the recovery model.
* Two models registered before the hold-out was opened: `logit_default_holdout` and `gbm_default_holdout` (one
  configuration each); the trial counter rises from 313 to 315.

---

# 量化金融，从零搭建 — 第20部分：信用

第18和第19部分为总会兑付的债券定价；本部分为它们可能不兑付的那种可能性定价。本部分讲：

* 信用利差衡量什么：七十年的穆迪收益率，以及信用利差之谜；
* 结构模型：Merton（1974），用三家真实公司的价格和申报文件每天计算违约距离，Black–Cox首次通过，Leland的自选边界与最优杠杆；
* 简约形式：违约作为随机时钟（Jarrow–Turnbull、Duffie–Singleton、Lando的CIR强度）；信用违约互换的两条腿、自举出的风险率曲线、CS01与违约跳跃、2009年的"大爆炸"、拍卖；
* 完全基于EDGAR构建的数据集上的违约预测：破产申报（8-K第1.03项）作为标签，XBRL frames作为特征；Altman的Z（1968）及其重新加权的版本、一个logit和梯度提升树，在打开封存的2021–2023年公司年度之前登记；
* 组合：Vasicek大样本池与巴塞尔内部评级法公式、有限样本池、高斯与t连接函数、违约相关性、首次违约篮子、CDO分层、随机回收率、基础相关性；
* 依据公开记录：2007–08年的优先级分层（Coval–Jurek–Stafford；金融危机调查委员会）、伦敦鲸（2012）、2020年3月的公司债市场；私募信贷及其估值。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约54分钟）

* **一个承诺值多少。** 雷曼，2008年9月15日；10月10日的CDS拍卖（8.625）；Baa利差升到6.16%（2008年12月4日）；历史条（1968–2024）；本部分安排；信用交易台开张。
* **1. 信用利差衡量什么。** 1953年以来Baa和Aaa相对10年期国债的利差与衰退（平均1.91%和0.95%；2020年3月23日4.31%）；Baa减Aaa（平均0.97%，2008年底3.38%）；预期损失、风险溢价与流动性；信用三角；Huang–Huang、Longstaff–Mithal–Neis、Collin-Dufresne–Goldstein–Martin。
* **2. Merton：债务作为期权。** 支付；推导模型；三维中5年期利差对（杠杆，波动率）；期限结构与短期利差的失效；用数字说明利差之谜（一家类Baa公司：37个基点对191）；**实验**：`merton_solve`。
* **3. 从价格得到违约距离。** 在波音、美国航空和挪威邮轮上运用KMV的方法，2018–2025年（最低：0.96、0.41、0.12；挪威邮轮2020年5月13日的Merton违约概率为45%）；权益对违约点；Merton的一年期利差（峰值331、536和1,630个基点；2019年约为零）；EDF与Bharath–Shumway。
* **4. 首次通过与选择违约。** Black–Cox路径与公式（10年违约概率：到期判定24%，首次通过54%）；CreditGrades；推导并计算Leland（1994）（最优杠杆75%，利差75个基点）。
* **5. 违约作为随机时钟。** 风险率，生存即贴现；200个模拟时钟；三种回收惯例下的风险零息债券；风险中性与现实违约概率；Lando的Cox过程；CIR强度曲线（平静名称从35到101个基点，承压名称从458到189）。
* **6. 信用违约互换。** 合约（摩根大通，1994）；推导两条腿；从示意报价自举出风险率曲线；CS01（1,000万美元对应4,249美元）与违约跳跃（600万美元）；大爆炸（2009年4月8日：预付款−1.8%、−10.2%、+20.3%）；两阶段拍卖；CDS–债券基差；**实验**：`bootstrap_hazard`。
* **7. 十七年的破产。** 2009–2025年1,225家公司提交的1,265份第1.03项申报（2009年232家，2021年19家，2023年88家）；与Baa利差的相关系数0.73，提前一年为0.38；十分位分组（杠杆最高的十分之一每年3.9%，平均0.8%）；数据集的构建。
* **8. Altman的Z。** 1968年的公式与区间；在封存年份中AUC为0.815（困境区每年1.9%，占申报公司的55%）；用2010–16年的logit重新加权，验证期AUC 0.827对0.794；四个比率，存活公司对破产公司。
* **9. Logit与提升树，封存检验。** Shumway的风险率logit与公司自己的梯度提升；一棵树；封存的2021–23年AUC为0.815 / 0.867 / 0.905（Altman / logit / 树），树的风险最高十分之一包含68%的破产；按期间，树从样本内0.976降到0.905；Brier分数对基准率；按十分位校准；三维中在杠杆与市场缓冲上学到的曲面；重要性与系数；**实验**：直方图分裂；试验计数器313 → 315。
* **10. 大样本池与银行资本。** 推导Vasicek；损失密度（违约概率2%时，ρ = 0.05、0.15、0.30的99.9%分位数为8.1%、17.6%、33.3%）；有限样本池（50、200、1,000笔贷款为22.0%、18.5%、17.6%）；巴塞尔内部评级法公式（违约概率1%时风险权重92.32%；资本约为预期损失的16倍）。
* **11. 连接函数：一起违约。** Sklar与Li；联合违约（ρ = 0.3：违约相关系数0.065，联合概率17个基点对4）；高斯与t散点云；五个名称的首次违约篮子（独立时507个基点，ρ = 0.99时125）；125个名称样本池的尾部（损失超过15%的概率0.08%对1.3%）。
* **12. CDO与分层。** 瀑布；分层预期损失对相关性；2005年5月；随机回收率（优先级预期损失1.1 → 5.4个基点）与delta（0.67、0.26、0.005）；基础相关性偏斜（0.16到0.55）。
* **13. 2007–08年：优先级分层。** 经济巨灾债券（只在第0.16个百分位以下才亏损；预期损失3.7个基点，样本池为120）；重新定价（违约概率翻倍、ρ从0.15升到0.4时预期损失×710）；金融危机调查委员会关于2006年AAA抵押贷款证券的调查结果（83%被下调评级）；CDO平方。
* **14. 2012年：伦敦鲸。** 首席投资办公室的合成信用组合（亏损62亿美元；罚款9.2亿美元）；VaR模型的更换与电子表格错误；三条教训。
* **15. 公司债与2020年3月。** 到3月中旬LQD下跌20%，HYG下跌22%；Baa利差2.05% → 4.31% → 2.93%；美联储的公司信贷工具与Haddad–Moreira–Muir；信用因子与困境之谜。
* **16. 私募信贷及其估值。** 这一资产类别（约2.1万亿美元，国际货币基金组织）；Ares Capital的股价（2020年3月23日8.08美元）对其报告的每股净资产值（17.32 → 16.97美元）；季度波动率4.5%（净资产值）对19.8%（股价）；平滑的收益（Getmansky–Lo–Makarov）。
* **17. 第20条规则：信用交易台。** 同一批公司的两个违约概率，分别来自账目和价格；AMR从其2010年账目得到的13%；信用模块；第20条规则。
* **写给研究者：颗粒度调整。** Vasicek模型中N笔相同贷款的NL | y ~ Binomial(N, p(y))，精确地P(L ≤ k/N) = ∫Bin(k; N, p(y))φ(y)dy；N → ∞时α分位数趋于ASRF值p(Φ⁻¹(α))。戈迪（2003）的调整（古里耶鲁–洛朗–斯凯莱2000；Martin与Wilde 2002）加上GA = −(1/(2φ))d/dy[φσ²/μ′]，这里为(1/(2N))[yp(1 − p)/(bφ(z)) − (1 − 2p) − zp(1 − p)/φ(z)]，PD 1%、ρ 0.12、α 99.9%时为2.04/N。精确值对ASRF：N = 100时10.5%对9.0%（多六分之一资本），250时9.6%，1,000时9.2%；ASRF + GA为11.1/9.9/9.2%，从约250笔起准确，25–50笔时过度修正；蒙特卡洛一致。低相关时相对调整最大（ρ 0.24：c = 1.48；PD 3%：c = 2.32）。500笔齐普夫账簿（最大一笔14.7%）：有效N = 1/HHI = 28，蒙特卡洛99.9%损失19.6%，ASRF 9.0%，ASRF + GA(28) 16.3%。组合不变性只在ASRF极限下成立（戈迪2003），所以第一支柱省略了这一项。三个开放问题；暂停题：一笔加399笔的账簿HHI ≈ 0.25 + 0.25/399，有效N ≈ 4。
* **回顾、交易台问题、十道习题（两道为资格考试水平）。**

## 交易台问题与解答

1. **5年期CDS报价100个基点，回收率40%。年违约概率是多少？** 信用三角：λ ≈ s/(1 − R) = 0.01/0.6 = 每年1.67%，所以五年约为1 − e^{−5λ} = 8%。这是风险中性概率：它包含承担违约风险的溢价，这类名称的历史违约率更低（第5章）。
2. **为什么股东做多波动率，债权人做空波动率？** 在Merton模型中，权益是以债务为行权价的公司资产看涨期权；债权人持有安全债券减去一个看跌期权。资产波动率上升会提高两个期权的价值，于是价值从债权人转移到股东：资产替代。限制性条款和抵押品就是为了限制它。
3. **为什么预期损失很小的优先级分层也该有很宽的利差？** 它的损失只出现在经济最糟糕的状态（第13章：第0.16个百分位以下），那时其他资产也都在亏损，钱最值钱。按损失到来的时间加权的价格，收取的远多于预期损失；只看预期损失的评级会把它当作和政府债券一样安全。
4. **一个违约模型样本内得分0.98，样本外0.90。报告哪一个？** 样本外的那个，在模型拟合之前封存的数据上；差距就是模型记住的东西（第9章）。还必须单独检查校准：排序比概率更能经受信用周期。

## 习题与解答

1. **Merton的债务。** B = V − E = V − [V N(d₁) − D e^{−rT} N(d₂)] = D e^{−rT} N(d₂) + V N(−d₁)。收益率为−ln(B/D)/T，所以利差为s = −(1/T) ln[N(d₂) + (V e^{rT}/D) N(−d₁)]。
2. **权益波动率。** 由伊藤公式，dE = (∂E/∂V) dV + …，且∂E/∂V = N(d₁)，所以σ_E E = N(d₁) σ_V V。公司接近违约时，E比N(d₁)V下降得更快：权益成为对资产的杠杆化索取权，其波动率上升。
3. **常数风险率下的平价利差。** 连续支付保费时，保费腿 = s ∫₀ᵀ e^{−(r+λ)t} dt，保护腿 = (1 − R) ∫₀ᵀ λ e^{−(r+λ)t} dt。两个积分相等，所以s = (1 − R)λ精确成立。
4. **手算自举。** λ ≈ 0.012/0.6 = 2.0%。按年支付时，风险年金为Σ e^{−(0.04+0.02)t} ≈ 0.942 + 0.887 + 0.835 = 2.664，保护腿约为0.6 × Σ e^{−0.04t}(e^{−0.02(t−1)} − e^{−0.02t}) ≈ 0.0323；它们隐含的利差0.0323/2.664 = 121个基点已经很接近，再迭代一步（λ ≈ 1.96%）即可重新定价120个基点。
5. **Vasicek的分布。** 给定M，违约相互独立，概率为p(M) = N((N⁻¹(p) − √ρ M)/√(1 − ρ))；在大样本池中L = p(M)。于是P(L ≤ x) = P(M ≥ (N⁻¹(p) − √(1 − ρ) N⁻¹(x))/√ρ) = N((√(1 − ρ) N⁻¹(x) − N⁻¹(p))/√ρ)，q分位数为N((N⁻¹(p) + √ρ N⁻¹(q))/√(1 − ρ))。
6. **违约概率2%时的巴塞尔资本。** ρ = 0.12w + 0.24(1 − w)，w = (1 − e^{−1})/(1 − e^{−50}) = 0.632：ρ = 0.164。第99.9个百分位处的条件违约概率为N((N⁻¹(0.02) + √0.164 × 3.09)/√0.836) = N((−2.054 + 1.252)/0.914) = N(−0.877) = 19.0%。b = (0.11852 − 0.05478 ln 0.02)² = 0.111，K = 0.45 × (0.190 − 0.02) × 1/(1 − 0.166) = 敞口的9.2%，约为0.9%预期损失的十倍。
7. **分层与相关性。** 样本池的预期损失不依赖于ρ。ρ上升时L的分布更分散：更多质量集中在零附近，也有更多在尾部。权益分层的损失min(L, d)/d是L的凹函数，所以分散会降低其期望；优先级分层的损失在其起点附近是凸的，所以分散会提高其期望。
8. **logit中的胜算。** 对数胜算上升0.5 × 2 = 1.0，所以胜算乘以e¹ = 2.72；对于罕见事件，概率也大约乘以同样的倍数。
9. **（资格考试）有限资产池。** 给定Y = y，N个违约是独立的伯努利(p(y))，所以NL | y ~ Bin(N, p(y))；对因子积分。N → ∞时给定Y有L − p(Y) → 0（大数定律），所以L → p(Y)，p递增连续，q_α(L) → p(Φ⁻¹(α))。
10. **（资格考试）颗粒度展开。** 令x_ε为μ(Y) + εU的α分位数。对Y条件化，P(μ + εU ≤ x) = G(x) + (ε²/2)∂/∂x{E[U² | μ = x]g(x)} + o(ε²)（一阶项因E[U | Y] = 0而消失），g是μ(Y)的密度。令其等于α并取x_ε = x₀ + ε²x₂，得x₂ = −(1/(2g))∂/∂x{E[U² | μ = x]g(x)}；换元到y（g = h/μ′，∂/∂x = (1/μ′)∂/∂y）得−(1/(2h(y)))d/dy[h(y)Var(U | y)/μ′(y)]，在y = q_α(Y)处取值。

## 数据与复现

* FRED：BAA、AAA、GS10（月度）、BAA10Y（日度）、USREC；冻结到2025年12月31日并校验哈希。
* EDGAR全文搜索：2009–2025年所有报告第1.03项的8-K（每家公司每次事件的第一份申报）；2010–2023年14个概念的XBRL frames，以及公众持股市值（dei）；波音、美国航空、挪威邮轮和Ares Capital的公司事实数据。全部公开、无需密钥，礼貌地抓取并缓存。
* BA、AAL、NCLH、LQD、HYG和ARCC的日收盘价（雅虎财经）。
* 引用而非计算的公开数字：雷曼的拍卖价格；金融危机调查委员会的调查结果；摩根大通工作组和美国参议院的数字；美联储的信贷工具；国际货币基金组织对私募信贷的估计。
* 屏幕上标注为示意的输入：CDS报价、连接函数与分层参数、回收率模型。
* 在样本外打开之前登记的两个模型：`logit_default_holdout`与`gbm_default_holdout`（各一种配置）；试验计数器从313升到315。

## 写给研究者

* **定理。** Vasicek（2002），*Risk*；戈迪（2003），*J. Financial Intermediation* 12；古里耶鲁、洛朗与斯凯莱（2000），*J. Empirical Finance* 7；Martin与Wilde（2002），*Risk*；Pykhtin（2004），*Risk*；戈迪与Lütkebohmert（2013），*Int. J. Central Banking*。
* **简化。** 单因子；违约损失率为100%；精确公式用相同贷款；成块账簿用蒙特卡洛。
* **开放问题。** 多因子；小而成块的账簿；PD与ρ的估计风险。
