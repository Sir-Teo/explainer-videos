# Quant, Built — Part 18: Money, Bonds and the Curve

Part 18 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act IV, Fixed Income and Credit. It covers:

* money and the central bank: the floor system (interest on reserves, the overnight reverse repo), the balance sheet
  through QE and QT, and Taylor's rule against the funds rate;
* bonds, yields, zero and forward rates, and conventions; a curve bootstrapped from Treasury's par yields and fitted by
  Nelson–Siegel–Svensson, checked against the Fed's own curve (Gürkaynak, Sack and Wright 2007);
* duration (Macaulay 1938), convexity and DV01; key-rate risk and Redington's immunization (1952), under twists;
* fifty years of the curve, and the three factors that move it (Litterman and Scheinkman 1991);
* swaps and the negative swap spread (Jermann 2020); Treasury futures and the cheapest to deliver; repo, SOFR and the
  end of LIBOR;
* expectations against the term premium: Campbell–Shiller and Fama–Bliss, and Adrian–Crump–Moench re-estimated;
  FOMC days and how far the news travels;
* relative value: Salomon's arbitrage group, and a PCA-neutral butterfly, pre-registered and tested on a sealed hold-out;
* two crises from the public record: the gilt and LDI spiral of September 2022, and Silicon Valley Bank in March 2023.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's new
[`rates`](../../../explainer/quant/house/rates.py) module). Data: the Fed's fitted Treasury curve (GSW), Treasury's daily
par yields and auction records, FRED, the NY Fed's ACM term premium, and SVB's 10-K from EDGAR.

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 53 minutes)

* **The safest asset** (2.9 min). Silicon Valley Bank's $91.3 bn held-to-maturity book marked through 2022 off the
  Fed's 6-year zero yield (+2.55 points): a $15.16 bn reported loss against $16.0 bn of equity (10-K, EDGAR); 8–10
  March 2023 (Fed review); the history strip (1938–2025); the plan; the rates desk opens.
* **1. Money, reserves and the floor** (2.5). The Fed's T-account; Poole's demand for reserves (1968), scarce against
  ample; every week since 2009 of fed funds minus interest on reserves against reserves; the administered rates and the
  market rates between them, 2007–2025.
* **2. QE and QT: the balance sheet** (2.1). Total assets $0.9 tn (Aug 2008) to $8.97 tn (Apr 2022); the balance-sheet
  identity; QT to November 2025: assets −$2.41 tn, reverse repos −$1.81 tn, reserves −$0.93 tn; the facility's peak
  ($2.55 tn, 30 Dec 2022); runoff ended 1 December 2025 (FOMC, 29 October 2025).
* **3. The Taylor rule** (2.2). Taylor (1993) derived and the Taylor principle; against the funds rate 1987–2025
  (ρ = 0.65 to 2007; 2.9 points below in 2003–05; 9.3 below in 2021–22, 13% called for in 2022); in 3D, the rule as a
  plane with each quarter's rate above or below it.
* **4. Bonds, yields and forwards** (3.1). A 4% 10-year note as a bundle of zeros, discounted live (98.52 off the curve
  of 31 December 2025, yield 4.18%); zero, forward and instantaneous-forward rates derived; the three curves; day
  counts and compounding.
* **5. Bootstrapping a curve** (2.4). The bootstrap derived; Treasury's fourteen quotes solved node by node (every par
  bond repriced to 10⁻¹¹ bp); **lab**: `bootstrap_par`; 8 March 2023 (2s10s −107 bp, deeper than any day since 1981
  but one), against the Fed's curve.
* **6. Duration and convexity** (2.8). Macaulay's balance point; duration, convexity and DV01 derived; a 30-year bond
  at ±100 bp (exact −15.45 / +19.69 against duration's ∓17.38); the desk question; SVB's loss by one line of
  arithmetic (6.2 × 2.55% × $91.3 bn = $14.5 bn against $15.16 bn reported).
* **7. Key rates and immunization** (2.0). Key-rate DV01s of a 10-year note and of a DV01-neutral steepener; Redington's
  three conditions; a 15-year liability funded with 5- and 30-year zeros: a surplus under every parallel move, and an
  11% loss under a one-point twist; the surplus surface over (shift, twist) in 3D.
* **8. Fitting the curve: Nelson–Siegel and Svensson** (2.2). The loadings; four dials sculpting a curve; Svensson fits
  to two days (3.3 and 6.9 bp RMSE) against the Fed's; **lab**: `fit_nss`, betas by regression for each pair of taus.
* **9. Five decades of the curve** (1.8). The zero curve at every month end since 1972, animated (10-year peak 14.9%,
  September 1981; low 0.55%, 2020); nine eras side by side (inverted on 16% of days); the 10-year minus 1-year spread
  with NBER recessions: an inversion 7 to 34 months before each of seven, and the longest inversion (27 months,
  2022–24) without one so far; the whole history as a 3D surface.
* **10. Level, slope and curvature** (2.6). PCA derived; 10,005 daily changes since 1985: 83.9%, 10.6% and 3.4% of
  variance; 20 October 1987 rebuilt from three scores; the same shapes in every decade; forty years as a walk in factor
  space (3D).
* **11. Swaps and the negative swap spread** (2.9). The par swap rate derived; swap spreads 2000–2016 (about 58 bp at 10
  years before 2008; 30-year negative from 24 October 2008, 10-year from 15 September 2015); why the arbitrage stays
  open (Jermann 2020).
* **12. Treasury futures and the cheapest to deliver** (2.5). The 10-year note contract; conversion factor, invoice and
  basis derived; the 19 notes deliverable into December 2025, priced off the Fed's curve; the cheapest switches from the
  shortest to the longest note as the 10-year passes about 5.3%.
* **13. Repo, SOFR and the end of LIBOR** (2.8). Repo, general collateral and specials; why fed funds trades below
  interest on reserves (the Federal Home Loan Banks); LIBOR's crisis file (Barclays, 27 June 2012: $200 m, $160 m,
  £59.5 m); SOFR chosen in 2017, LIBOR's last panel 30 June 2023; compounding in arrears (46 bp above the first day's
  rate while the Fed hiked).
* **14. Expectations and the term premium** (3.2). The expectations hypothesis; Campbell–Shiller slopes from 0.02 (1
  year) to −1.66 (10 years) where it predicts 1, Fama–Bliss slopes near 1 where it predicts 0; ACM's three regressions,
  re-estimated: ρ = 0.9999 with the NY Fed's series, 10 bp apart; the 10-year split since 1961 (premium 4.6% in 1981,
  −1.5% in 2020); since August 2024: yield +0.35, expectations −0.54, premium +0.89.
* **15. FOMC days** (2.2). The 2-year yield on 215 scheduled meeting days, 1994–2020 (s.d. 6.2 bp against 5.1); the six
  biggest days; Kuttner (2001), Gürkaynak, Sack and Swanson (2005); the 10-year-ahead forward moves 0.33 of the 2-year
  (Hanson and Stein 2015).
* **16. Relative value: the butterfly** (2.8). Salomon Brothers' arbitrage group and the 1991 auction scandal ($290 m);
  LTCM founded (1994); a PCA-neutral 2s5s10s fly derived (weights −0.60, 1, −0.53); the rule registered before its
  hold-out: Sharpe −0.25 in sample, −0.52 in 2021–2025 (gross −0.44); a half-life of 815 trading days; the trial counter
  311.
* **17. September 2022: gilts and LDI** (3.1). Pension funds and leveraged LDI pools; the buffer 1/(LD); 130 bp in three
  days; the spiral simulated (a 50 bp shock becomes 64, 88, 139 or 335 bp as price impact rises); the surface over
  (shock, impact) in 3D; the Bank of England's £19.3 bn (28 September – 14 October); the 250 bp standard.
* **18. March 2023: Silicon Valley Bank** (3.0). The balance sheet from the 10-K ($211.8 bn of assets, $91.3 bn held to
  maturity, 94% of deposits uninsured); the estimated mark through 2022 against equity; three days in March; the Bank
  Term Funding Program at par; Jiang, Matvos, Piskorski and Seru (about $2 tn across US banks).
* **19. Rule 18: the rates desk** (1.5). Four positions reported three ways (DV01, and level, slope and curvature risk):
  a steepener and an immunized fund with zero DV01 and real factor risk; the rates module; Rule 18.
* **Recap, desk questions, problems** (2.7). Thirteen lines; four desk questions; eight problems with solutions below.

## Hands-on

* **Labs** (the House's own code on screen, then run): `bootstrap_par` (ch. 5), `fit_nss` (ch. 8), `acm_decompose`
  (ch. 14).
* **Live constructions:** cash flows shrinking to present values; zero nodes solved one by one; Macaulay's beam; four
  Nelson–Siegel–Svensson dials; the curve morphing month by month since 1972; a day rebuilt from three factor scores;
  the cheapest-to-deliver envelope as yields shift.
* **3D:** the Taylor plane and fifty years of policy around it; the immunized fund's surplus over (shift, twist); the
  curve's history as a landscape; the factor walk; the LDI spiral over (shock, impact).

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Tuckman and Serrat, *Fixed Income Securities* (4th ed.) | 1–4 (prices, discount factors, spot and forward rates, yields), 5–6 (DV01, duration, convexity), 7 (key rates), 8 (regression and factor hedging), 10 (repo), 14 (futures), 16 (swaps) | ch. 4–7, 10–13 |
| Veronesi, *Fixed Income Securities* | 1–4 (the Fed, basics), 6 (duration), 7 (interest rate risk management) | ch. 1–7 |
| Hull, *Options, Futures, and Other Derivatives* | 4 (interest rates), 6 (interest rate futures), 7 (swaps), 9 (OIS, funding) | ch. 4, 11–13 |
| Fabozzi, *The Handbook of Fixed Income Securities* | yield curve, Treasury futures, repo | ch. 8–13 |

## Papers, chapter by chapter

* ch. 1–3: Poole (1968); Taylor (1993); FOMC statements (2008–2025); Federal Reserve H.4.1 and FRED series.
* ch. 4–7: Macaulay (1938); Redington (1952); Fisher and Weil (1971).
* ch. 8–10: Nelson and Siegel (1987); Svensson (1994); Gürkaynak, Sack and Wright (2007); Litterman and Scheinkman
  (1991).
* ch. 11–13: Jermann (2020); Duffie and Stein (2015); CFTC, DOJ and FSA releases on Barclays (27 June 2012); ARRC
  (2017); FCA (3 July 2023); Avalos, Ehlers and Eren (2019) for the repo spike (Part 2).
* ch. 14–15: Fama and Bliss (1987); Campbell and Shiller (1991); Adrian, Crump and Moench (2013); Kim and Wright (2005);
  Kuttner (2001); Gürkaynak, Sack and Swanson (2005); Hanson and Stein (2015); Nakamura and Steinsson (2018).
* ch. 16: SEC and DOJ settlements with Salomon Brothers (1992); Federal Reserve Bank of Cleveland, *Economic
  Commentary* (15 June 1992).
* ch. 17: Bank of England, *Quarterly Bulletin* (2023) "Financial stability buy/sell tools: a gilt market case study";
  Pinter (2023); FPC record (March 2023) on LDI resilience.
* ch. 18: Federal Reserve, *Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank* (April
  2023); SVB Financial Group 2022 10-K; Federal Reserve press release on the BTFP (12 March 2023); Jiang, Matvos,
  Piskorski and Seru (2024).

## Build it

```bash
python -m videos.quant.quant18.compute                     # every item, seconds each (fetches and caches the data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant18 Fit  # one chapter, silent, with a contact sheet
python tools/make.py quant18 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **A 10-year zero yields 4% (annual). Duration? Price change for +1 bp?** Price 100/1.04¹⁰ = 67.56. A zero pays once,
   so its Macaulay duration is 10; modified duration 10/1.04 = 9.62; DV01 = 9.62 × 67.56 × 0.0001 = 0.065. One basis
   point up costs about 6.5 cents per 100 of face.
2. **Why does convexity cost money?** Take two bonds with the same yield and duration, one more convex. In any large
   move, up or down, the more convex one does better; if they also yielded the same, buying it against the other would
   profit from volatility alone. So the convex bond trades at a lower yield, by about ½Cσ² a year (problem 3).
3. **How can a swap rate be below the Treasury yield?** The arbitrage (buy the bond financed in repo, pay fixed on the
   swap) ties up a dealer's balance sheet for the bond's whole life, and since 2008 leverage ratios charge capital for
   it; the swap barely uses any. Pension funds and insurers receive fixed at the long end. Jermann (2020): a cost of
   holding bonds makes the no-arbitrage spread negative, most at long maturities.
4. **SVB's assets could not default. What should its risk report have shown?** The economic value of equity under a
   rate shock, key rate by key rate: about −6.2 × Δy × $91 bn for the held-to-maturity book, against the duration of
   its deposits. With 94% of them uninsured, that duration was near zero in a panic, so the book was an unhedged bet on
   rates. Held to maturity, the loss was invisible in earnings and capital, not in value.

## Problems, with solutions

1. **Forward rates.** From Z(t₂) = Z(t₁)e^{−f(t₂−t₁)} and Z(t) = e^{−z(t)t}: f = (z₂t₂ − z₁t₁)/(t₂ − t₁). Letting t₂ → t₁,
   f(t) = d(z t)/dt = z(t) + t z′(t). The forward lies above the zero curve exactly where the zero curve rises (z′ > 0).
2. **Two durations.** A zero has one cash flow, at T, so the value-weighted average time is T. A perpetuity paying c at
   annual yield y is worth P = c/y; −(dP/dy)/P = 1/y is the modified duration, and Macaulay's is (1 + y) times that:
   (1 + y)/y. At 5%, 21 years.
3. **The value of convexity.** dP/P ≈ −D dy + ½C(dy)² plus the yield earned, y dt. With E[dy] = 0 and E[(dy)²] = σ²dt,
   E[dP/P] ≈ y dt + ½Cσ² dt: convexity earns ½Cσ² a year, which is what a convex bond gives up in yield.
4. **A bootstrap by hand.** 100 = 5/1.04 + 105/(1 + z₂)², so (1 + z₂)² = 105/95.192 = 1.1030 and z₂ = 5.025%, a little
   above the 5% par yield, because the early coupon was discounted at the lower 4%.
5. **The par swap rate.** A floating-rate note resets to the market rate, so it is worth par: the floating payments are
   worth 1 − Z(T). The fixed payments are worth K·A with A = Σ τᵢZ(tᵢ). Setting them equal gives K* = (1 − Z(T))/A. After
   inception the receiver's value is (K − K*)A, so a 1 bp change in the swap rate is worth about A × 0.0001.
6. **Redington.** With continuous rates a zero's duration is its maturity. Value weights w₅ + w₃₀ = 1 and 5w₅ + 30w₃₀ = 15
   give w₃₀ = 0.4, w₅ = 0.6, on a liability worth 100e^{−0.6} = 54.88. A zero's convexity is T²: assets 0.6 × 25 + 0.4 ×
   900 = 375 against the liability's 225, so every parallel move leaves a surplus; a twist can still cost money (ch. 7).
7. **Taylor's rule.** i = 2 + 4 + ½(4 − 2) + ½(−1) = 6.5%.
8. **An LDI buffer.** NAV falls by L × D × Δy of itself, so the pool is wiped out at Δy = 1/(4 × 25) = 1 point. After 50
   bp, NAV = 1 − 100 × 0.005 = 0.5 and gilt holdings fall to 4 × (1 − 25 × 0.005) = 3.5. Restoring a 1-point buffer
   needs holdings of 0.5/(25 × 0.01) = 2: sell 1.5, or 43% of the gilts, into a falling market.

## Data and reproducibility

* The Fed's fitted Treasury curve (Gürkaynak, Sack and Wright; `feds200628.csv`), 1961–2025, frozen through 31 December
  2025 and checksummed; Svensson parameters from 1980, Nelson–Siegel before.
* Treasury's daily par yield curve (2023, 2025) and TreasuryDirect's note auction records (through 2025).
* FRED: DFEDTAR, DFEDTARL/U, DFF, IOER, IORB, RRPONTSYAWARD, RRPONTSYD, SOFR, WALCL, WRESBAL, FEDFUNDS, GDPC1, GDPPOT,
  GDPDEF, PCEPILFE, DGS2–30, DSWP2–30 (ICE swap rates, to October 2016), DTB3.
* The NY Fed's ACM term premium (monthly), for comparison only; the House re-estimates it.
* SVB Financial Group's XBRL facts from EDGAR (10-K for 2022, filed 24 February 2023); the Federal Reserve's SVB review.
* Published figures quoted, not computed: the Bank of England's gilt purchases and the 130 bp move; SOFR volumes (NY
  Fed); the Barclays penalties; the Salomon settlement.
* One strategy registered and tested: `pca_fly_2s5s10s` (one configuration); the trial counter rises from 310 to 311.

---

# 量化金融，从零搭建 — 第18部分：货币、债券与收益率曲线

本部分讲：

* 货币与中央银行：地板体系（准备金利息、隔夜逆回购）、量化宽松与量化紧缩中的资产负债表，以及泰勒规则对联邦基金利率；
* 债券、收益率、零息利率与远期利率，以及各种惯例；用美国财政部的平价收益率自举出曲线，用Nelson–Siegel–Svensson拟合，并与美联储自己的曲线（Gürkaynak、Sack与Wright，2007）核对；
* 久期（Macaulay，1938）、凸性与DV01；关键利率风险与Redington的免疫（1952），以及扭转下的表现；
* 五十年的收益率曲线，以及推动它的三个因子（Litterman与Scheinkman，1991）；
* 互换与负的互换利差（Jermann，2020）；国债期货与最便宜可交割券；回购、SOFR与LIBOR的终结；
* 预期与期限溢价：Campbell–Shiller与Fama–Bliss回归，并重新估计Adrian–Crump–Moench模型；FOMC会议日，以及消息沿曲线传多远；
* 相对价值：所罗门兄弟的套利小组，以及一个预先登记、在封存的样本外检验的主成分中性蝶式交易；
* 两次危机，依据公开记录：2022年9月英国国债与LDI的螺旋，以及2023年3月的硅谷银行。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约53分钟）

* **最安全的资产。** 用美联储6年期零息收益率（+2.55个百分点）给硅谷银行913亿美元的持有至到期账簿逐日估值：10-K报告的亏损为151.6亿美元，而权益为160亿美元（EDGAR）；2023年3月8–10日（美联储审查报告）；历史条（1938–2025）；本部分安排；利率交易台开张。
* **1. 货币、准备金与地板体系。** 美联储的T型账户；Poole（1968）的准备金需求，稀缺对充裕；2009年以来每周的联邦基金利率减准备金利率对准备金；2007–2025年的管理利率，以及夹在中间的市场利率。
* **2. 量化宽松与量化紧缩。** 总资产从0.9万亿美元（2008年8月）到8.97万亿（2022年4月）；资产负债表恒等式；到2025年11月的量化紧缩：资产−2.41万亿，逆回购−1.81万亿，准备金−0.93万亿；逆回购工具的峰值（2022年12月30日，2.55万亿）；缩表于2025年12月1日结束（FOMC，2025年10月29日）。
* **3. 泰勒规则。** 推导泰勒（1993）与泰勒原则；1987–2025年对联邦基金利率（到2007年相关系数0.65；2003–05年低2.9个点；2021–22年低9.3个点，2022年规则要求13%）；三维中，规则是一个平面，每个季度的利率位于其上或其下。
* **4. 债券、收益率与远期利率。** 把一只4%的10年期票据看成一捆零息债券，实时贴现（按2025年12月31日的曲线为98.52，收益率4.18%）；推导零息利率、远期利率与瞬时远期利率；三条曲线；计息天数与复利惯例。
* **5. 自举一条曲线。** 推导自举；逐个节点求解财政部的十四个报价（每个平价债券都重新定价到10⁻¹¹个基点）；**实验**：`bootstrap_par`；2023年3月8日（2年对10年利差−107个基点，比1981年以来除一天外的任何一天都深），与美联储的曲线比较。
* **6. 久期与凸性。** Macaulay的平衡点；推导久期、凸性与DV01；30年期债券在±100个基点下（精确值−15.45 / +19.69，久期给出∓17.38）；交易台问题；用一行算术算出硅谷银行的亏损（6.2 × 2.55% × 913亿 = 145亿，对报告的151.6亿）。
* **7. 关键利率与免疫。** 10年期票据和DV01中性陡峭化交易的关键利率DV01；Redington的三个条件；用5年和30年零息债券为15年期负债融资：任何平行移动都留下盈余，而一个百分点的扭转造成11%的亏损；三维中盈余在（平移，扭转）上的曲面。
* **8. 拟合曲线：Nelson–Siegel与Svensson。** 载荷；用四个旋钮塑造一条曲线；在两天上的Svensson拟合（均方根误差3.3和6.9个基点）对美联储的曲线；**实验**：`fit_nss`，对每对tau用回归求beta。
* **9. 收益率曲线的五十年。** 1972年以来每个月末的零息曲线，动画呈现（10年期峰值14.9%，1981年9月；低点0.55%，2020年）；九个时代并排（16%的交易日倒挂）；10年期减1年期利差与美国国家经济研究局的衰退：七次衰退之前7到34个月都出现过倒挂，而最长的一次倒挂（27个月，2022–24）至今没有带来衰退；整段历史作为一张三维曲面。
* **10. 水平、斜率与曲率。** 推导主成分分析；1985年以来10,005个日变化：方差的83.9%、10.6%和3.4%；用三个得分重建1987年10月20日；每个十年都是同样的形状；四十年在因子空间中的游走（三维）。
* **11. 互换与负的互换利差。** 推导平价互换利率；2000–2016年的互换利差（2008年前10年期约58个基点；30年期自2008年10月24日起为负，10年期自2015年9月15日起为负）；为什么套利没有消失（Jermann，2020）。
* **12. 国债期货与最便宜可交割券。** 10年期国债期货合约；推导转换因子、发票价格与基差；可交割到2025年12月合约的19只票据，用美联储曲线定价；当10年期收益率越过约5.3%时，最便宜可交割券从最短的票据换成最长的。
* **13. 回购、SOFR与LIBOR的终结。** 回购、一般担保品与特殊券；为什么联邦基金利率低于准备金利率（联邦住房贷款银行）；LIBOR的危机档案（巴克莱，2012年6月27日：2亿美元、1.6亿美元、5,950万英镑）；2017年选定SOFR，LIBOR最后一个报价小组于2023年6月30日结束；滞后复利（美联储加息期间比首日利率高46个基点）。
* **14. 预期与期限溢价。** 预期假说；Campbell–Shiller斜率从0.02（1年）降到−1.66（10年），而假说预测为1；Fama–Bliss斜率接近1，而假说预测为0；ACM的三步回归，重新估计：与纽约联储的序列相关系数0.9999，平均相差10个基点；1961年以来的10年期分解（1981年溢价4.6%，2020年−1.5%）；2024年8月以来：收益率+0.35，预期−0.54，溢价+0.89。
* **15. FOMC会议日。** 1994–2020年215个例会日的2年期收益率（标准差6.2个基点，对5.1）；变动最大的六天；Kuttner（2001），Gürkaynak、Sack与Swanson（2005）；10年后的远期利率变动为2年期的0.33（Hanson与Stein，2015）。
* **16. 相对价值：蝶式交易。** 所罗门兄弟的套利小组与1991年的拍卖丑闻（2.9亿美元）；LTCM成立（1994）；推导主成分中性的2s5s10s蝶式（权重−0.60、1、−0.53）；在打开样本外之前登记的规则：样本内夏普−0.25，2021–2025年−0.52（未扣成本−0.44）；半衰期815个交易日；试验计数器311。
* **17. 2022年9月：英国国债与LDI。** 养老基金与加杠杆的LDI基金池；缓冲为1/(LD)；三天上升130个基点；模拟螺旋（随着价格冲击加大，50个基点的冲击变成64、88、139或335个基点）；三维中在（冲击，价格冲击）上的曲面；英格兰银行的193亿英镑（9月28日至10月14日）；250个基点的标准。
* **18. 2023年3月：硅谷银行。** 来自10-K的资产负债表（资产2,118亿美元，持有至到期913亿，94%的存款未受保险）；2022年逐日估算的亏损对权益；三月的三天；按面值估价抵押品的银行定期融资计划；Jiang、Matvos、Piskorski与Seru（美国银行合计约2万亿美元）。
* **19. 第18条规则：利率交易台。** 四个头寸，三种报告方式（DV01，以及水平、斜率和曲率风险）：DV01为零却有真实因子风险的陡峭化交易和免疫基金；利率模块；第18条规则。
* **回顾、交易台问题与习题。** 十三行回顾；四个交易台问题；八道习题，解答见下文。

## 交易台问题与解答

1. **10年期零息债券收益率4%（年复利）。久期是多少？上升1个基点价格变动多少？** 价格100/1.04¹⁰ = 67.56。零息债券只支付一次，所以Macaulay久期为10；修正久期10/1.04 = 9.62；DV01 = 9.62 × 67.56 × 0.0001 = 0.065。上升一个基点，每100面值损失约6.5美分。
2. **为什么凸性要花钱？** 两只收益率和久期相同的债券，一只凸性更大。在任何大幅变动中，无论涨跌，凸性大的都表现更好；如果它们收益率也相同，买一只卖一只就能只靠波动率获利。所以凸性大的债券收益率更低，每年约低½Cσ²（习题3）。
3. **互换利率怎么会低于国债收益率？** 套利（用回购融资买入国债，在互换中支付固定）会在债券的整个存续期内占用交易商的资产负债表，而2008年后杠杆率要求为此计提资本；互换几乎不占用。养老基金和保险公司在长端收取固定。Jermann（2020）：持有债券的成本使无套利互换利差为负，期限越长越负。
4. **硅谷银行的资产不会违约。它的风险报告应该显示什么？** 利率冲击下的权益经济价值，按关键利率分解：持有至到期账簿约为−6.2 × Δy × 910亿美元，对比存款自身的久期。94%的存款未受保险，恐慌中它们的久期接近零，所以这个账簿是对利率的未对冲押注。持有至到期使亏损在利润和资本中看不见，但在价值中看得见。

## 习题与解答

1. **远期利率。** 由Z(t₂) = Z(t₁)e^{−f(t₂−t₁)}和Z(t) = e^{−z(t)t}得f = (z₂t₂ − z₁t₁)/(t₂ − t₁)。令t₂ → t₁，f(t) = d(z t)/dt = z(t) + t z′(t)。远期曲线恰好在零息曲线上升（z′ > 0）的地方位于其上方。
2. **两个久期。** 零息债券只有T时的一笔现金流，所以按价值加权的平均时间就是T。年收益率为y、每年支付c的永续债价值P = c/y；−(dP/dy)/P = 1/y为修正久期，Macaulay久期是它的(1 + y)倍：(1 + y)/y。在5%时为21年。
3. **凸性的价值。** dP/P ≈ −D dy + ½C(dy)²，再加上赚到的收益率y dt。由E[dy] = 0和E[(dy)²] = σ²dt，E[dP/P] ≈ y dt + ½Cσ² dt：凸性每年赚½Cσ²，这正是凸性大的债券在收益率上让出的部分。
4. **手算自举。** 100 = 5/1.04 + 105/(1 + z₂)²，所以(1 + z₂)² = 105/95.192 = 1.1030，z₂ = 5.025%，略高于5%的平价收益率，因为较早的票息是按较低的4%贴现的。
5. **平价互换利率。** 浮动利率票据按市场利率重置，所以价值为面值：浮动支付价值1 − Z(T)。固定支付价值K·A，其中A = Σ τᵢZ(tᵢ)。令二者相等得K* = (1 − Z(T))/A。成交后收取方的价值为(K − K*)A，所以互换利率变动1个基点价值约为A × 0.0001。
6. **Redington。** 连续复利下零息债券的久期就是其期限。由价值权重w₅ + w₃₀ = 1和5w₅ + 30w₃₀ = 15得w₃₀ = 0.4、w₅ = 0.6，负债价值为100e^{−0.6} = 54.88。零息债券的凸性为T²：资产0.6 × 25 + 0.4 × 900 = 375，对负债的225，所以任何平行移动都留下盈余；扭转仍可能亏钱（第7章）。
7. **泰勒规则。** i = 2 + 4 + ½(4 − 2) + ½(−1) = 6.5%。
8. **LDI缓冲。** 净资产值按自身的L × D × Δy下降，所以在Δy = 1/(4 × 25) = 1个百分点时被耗尽。上升50个基点后，净资产值 = 1 − 100 × 0.005 = 0.5，国债持仓降为4 × (1 − 25 × 0.005) = 3.5。要恢复1个百分点的缓冲，持仓需为0.5/(25 × 0.01) = 2：在下跌的市场中卖出1.5，即43%的国债。

## 数据与复现

* 美联储拟合的美国国债曲线（Gürkaynak、Sack与Wright；`feds200628.csv`），1961–2025年，冻结到2025年12月31日并校验哈希；1980年起为Svensson参数，之前为Nelson–Siegel。
* 美国财政部每日平价收益率曲线（2023、2025年）与TreasuryDirect的票据拍卖记录（到2025年）。
* FRED：DFEDTAR、DFEDTARL/U、DFF、IOER、IORB、RRPONTSYAWARD、RRPONTSYD、SOFR、WALCL、WRESBAL、FEDFUNDS、GDPC1、GDPPOT、GDPDEF、PCEPILFE、DGS2–30、DSWP2–30（ICE互换利率，到2016年10月）、DTB3。
* 纽约联储的ACM期限溢价（月度），仅用于比较；本系列公司自行重新估计。
* 硅谷银行金融集团在EDGAR上的XBRL数据（2022年10-K，2023年2月24日提交）；美联储的硅谷银行审查报告。
* 引用而非计算的公开数字：英格兰银行的国债购买与130个基点的变动；SOFR成交量（纽约联储）；巴克莱的罚款；所罗门兄弟的和解金额。
* 登记并检验了一个策略：`pca_fly_2s5s10s`（一种配置）；试验计数器从310升到311。
