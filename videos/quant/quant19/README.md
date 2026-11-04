# Quant, Built — Part 19: Term-Structure Models

Part 19 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), part of Act III, Derivatives (Q), and the second of its five parts on rates, credit and the basis (18–22). Part 18 built the curve; this part
makes it random, and prices the options on it. It covers:

* short-rate models: Vasicek (1977) and Cox–Ingersoll–Ross (1985) fitted to the bill rate, how badly the speed of mean
  reversion is estimated, and the same model fitted to prices instead (ℙ against ℚ);
* affine term structures (Duffie and Kan 1996): the Riccati system, solved and checked; a second factor against the
  data's correlations;
* Hull–White (1990), fitted to today's curve and to the volatility of yields; Black–Derman–Toy, Black–Karasinski and
  the trinomial tree; HJM (1992), its drift condition derived and tested, and Ho–Lee as the simplest case;
* caps, floors and swaptions: Black (1976), Bachelier (1900), Jamshidian's decomposition, parity, cap stripping; negative
  rates, zero floors and the 2020 switch to Bachelier; SABR (2002), the data's beta, the backbone and the density's
  failure at long expiries;
* market models (1997) and the forward market model for SOFR (Lyashenko and Mercurio 2019); correlation and swaptions;
* Bermudan swaptions by regression on independent paths (Longstaff and Schwartz 2001), checked by an exact lattice;
  callable bonds; the desk's risk report and the model reserve;
* two curves after 2008, and collateral discounting (Piterbarg 2010);
* bond risk premia: Fama–Bliss, Cochrane–Piazzesi (2005) and a neural network, registered before a sealed 2021–2025
  hold-out; macro-finance models (Ang and Piazzesi 2003);
* mortgages: prepayment, negative convexity, OAS, convexity hedging, the TBA market and the Fed's holdings;
* the 1994 bond massacre and Orange County, from the public record.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's new
[`termstructure`](../../../explainer/quant/house/termstructure.py) module). Data: the Fed's fitted Treasury curve (GSW),
FRED, Freddie Mac's mortgage survey, the NY Fed's ACM term premium, and the SEC's record of Orange County.

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 55 minutes)

* **The bond massacre** (2.9 min). 4 February 1994: the first hike in five years, seven by February 1995, 3% to 6%; in
  1994 the 2-year yield rose 3.3 points and the 10-year 1.6; Orange County's pools ($19.8 bn of securities on $7.2 bn of
  deposits, $12.6 bn of reverse repo: leverage 2.75), a $1.5–1.7 bn loss implying a duration of 3.2–3.7 years;
  bankruptcy, 6 December 1994; the history strip (1976–2020); the plan.
* **1. Short-rate models: Vasicek and CIR** (2.7). Both SDEs and the Feller condition; fitted to the 3-month bill,
  1990–2025 (Vasicek a = 0.124, b = 1.76%, σ = 0.71%; CIR Feller ratio 1.02; half-lives 5.6 and 6.3 years); 2,000
  simulated histories re-estimated: median â = 0.163 against a true 0.124, 19% more than double, a 95% interval for
  the half-life of 3 to 39 years; fans from today's 3.57% (11% of Vasicek paths below zero within ten years).
* **2. Affine term structures** (3.6). Feynman–Kac, the exponential-affine guess and the Riccati equations derived;
  curve shapes from three starting rates; the yield surface in 3D; **lab**: `affine_zcb` matches both closed forms to six
  decimals; ℙ against ℚ: fitted to 432 month-end curves with the same σ, Vasicek's long-run level is 8.2% instead of
  1.8% (87 bp RMSE); two factors (a = 0.02 and 0.9) reproduce the data's correlations (2y–10y 0.78 against 0.77, 1y–30y
  0.40 against 0.42), where one factor says 1.
* **3. Hull–White: fitting today's curve** (3.7). The shift φ(t) and the bond formula derived; a and σ fitted to the
  volatility of yields, 2023–2025 (a = 0.0087, σ = 1.04%); the same fit in four windows, failing at the boundary when
  the short end was pinned at zero (2010–12, 2019–21); the drift; 20,000 exact paths reprice the curve to 0.06%;
  Black–Derman–Toy, Black–Karasinski and Hull and White's trinomial tree.
* **4. Heath–Jarrow–Morton: the drift condition** (2.6). The drift condition derived; Ho–Lee (σ² (T − t); a 30-year
  forward expected 2.5 points higher in ten years at 1% vol); three PCA volatilities (83.9%, 10.6%, 3.4%); the forward
  curve's evolution in 3D; the martingale test (0.998 to 0.990).
* **5. Caps, floors and swaptions** (3.7). Black (1976) and Bachelier (1900) derived; Jamshidian's decomposition;
  put–call parity for swaptions (exact at three strikes); Hull–White caplets quoted both ways (flat 104 bp normal, 44% to
  23% Black); cap stripping (Rebonato's hump recovered from flat vols); the swaption grid (100–106 bp); a 5-year cap at
  3.06%.
* **6. Negative rates and Bachelier** (2.9). The ECB deposit rate below zero from 11 June 2014 to 26 July 2022 (min
  −0.50%); the German 10-year yield (38 months below zero, −0.65% in August 2019); Black's wall at zero, shifted Black,
  Bachelier; a zero floor worth 89 bp at a 0.5% forward under Bachelier and nothing under Black; WTI at −$37.63 and CME's
  switch to Bachelier (April 2020).
* **7. SABR for rates** (3.7). The model and the normal-SABR formula; sixty years of the 10-year yield's realised
  volatility, normal (285 bp in 1980) and lognormal (108% in 2020); the data's β = 0.30 (spread of normal vols 52%
  against 79%); α, ρ and ν as dials; the backbone and the hedge; Hagan's expansion at 10 years: a negative density
  below 0.75%, and arbitrage-free SABR (2014).
* **8. Market models: LIBOR and SOFR** (2.6). BGM, Jamshidian, Miltersen–Sandmann–Sondermann (1997); drifts under the
  terminal measure; ten caplets by Monte Carlo within 1.3% of Black and Bachelier; correlation and the 5y×5y swaption
  (90 bp falls to 52 as β goes from 0 to 1; formula 77.4 against simulation 77.4 at β = 0.2); the FMM for SOFR.
* **9. Bermudan swaptions** (3.9). A 10-non-call-1 receiver at 4.37%; LSM fitted on one set of paths and priced on
  another: 440 ± 4 bp against 321 for the best European; an exact lattice under the terminal measure: Europeans to
  0.002%, the Bermudan 441.0; the exercise boundary; a callable bond (96.36 against a 100.77 bullet: +56 bp of yield);
  mean reversion and the switch option (premium 37% to 52%).
* **10. Multi-curve and collateral** (2.8). The TED spread (0.39% before 2007; 4.58% on 10 October 2008; 1.42% in
  March 2020); projection against discounting; one curve against two (par rates 0.15 bp apart; an off-market swap 0.06
  per 100 apart); Piterbarg (2010); CSA discounting, valuation adjustments, and SOFR's single curve (October 2020).
* **11. Bond risk premia** (4.3). The expectations hypothesis; Fama–Bliss on the Fed's curve (slopes 0.72–1.20, about
  three standard errors from zero); Cochrane–Piazzesi's regression (R² 24% to 2003, 15% to 2025; coefficients
  unstable); CP and a 5–16–1 network registered before a sealed 2021–2025 hold-out: out-of-sample R² −2.17 and −1.01
  in 2004–2020, +0.26 and +0.44 in the hold-out, by the level and not the timing (correlations −0.31 and 0.06); the
  forecast against ACM's term premium (ρ = 0.83); Ang and Piazzesi (2003); the trial counter 313.
* **12. Mortgages and negative convexity** (4.7). Freddie Mac's 30-year rate (18.63% in 1981, 2.65% in 2021, 6.15% at
  the end of 2025); the prepayment S-curve; a 6.5% pool by simulation (duration 2.1, convexity −240); OAS 92 bp against
  a zero-vol spread of 150 bp (option cost 58 bp); convexity hedging and summer 2003 (10-year 3.13% to 4.61%); the TBA
  market and dollar rolls; the Fed's MBS ($2.74 tn in April 2022, $2.04 tn at the end of 2025).
* **13. Rule 19: the options desk for rates** (2.7). Five model tests; the morning report for $1 bn of the Bermudan
  (delta −$351 thousand a bp, vega +$470 thousand a bp of vol) and its hedge (1.36 Europeans and a small swap); the
  model reserve (441–487 bp across mean reversion, against ±4 of noise); the termstructure module; Rule 19.
* **For the researcher: the zero lower bound and the shadow rate** (5.6). Black (1995): r = max(s, r_min) with a
  Gaussian (Vasicek) shadow rate; prices from a one-dimensional PDE. Wu and Xia (2016): f(n) ≈ r_min + σ_n g((a_n −
  r_min)/σ_n), g(z) = zΦ(z) + φ(z), the floor plus a Bachelier call on the shadow forward a_n under the forward
  measure, so ∂f/∂s ≈ Φ(z_n)e^{−κn}. With κ 0.15, θ 4%, σ 1.5%: exact (implicit finite differences) against Wu–Xia
  forwards agree within 8 bp at ten years and a few basis points elsewhere, for shadow rates −3% to +3%; the floor's
  premium over the shadow forward at a −3% shadow rate is 208/152/77/40 bp at 1/2/5/10 years. The model's 1-year/10-year
  sensitivity ratio falls to a tenth of normal at s ≈ −2.5%. Treasury (GSW daily, yearly regressions of Δy(1) on
  Δy(10)): slope 0.62 on average in 1990–2007, 0.10 in 2010–2014 (1-year yield 0.22%), back to 0.51 in 2019; Swanson
  and Williams (2014) found the same in responses to news. Three open problems; pause: z = −1 gives f = 1% × g(−1) =
  0.083%, and a further 50 bp fall in the shadow rate lowers it by 0.5% × Φ(−1) × 0.8 = 6 bp.
* **Recap, desk questions, ten problems (two at qualifying-exam level)** (3.1). Thirteen lines; four desk questions;
  solutions below.

## Hands-on

* **Lab** (the House's own code on screen, then run): `affine_zcb` (ch. 2).
* **Computed checks:** a model re-estimated on its own simulations; the Riccati solver against two closed forms; Monte
  Carlo repricing of the curve; the HJM martingale test; Monte Carlo caplets against Black and Bachelier; swaption
  parity; the lattice against Jamshidian and against LSM.
* **Live constructions:** the trinomial tree; the Ho–Lee drift; cap stripping as a staircase; SABR's three dials and
  its backbone; the Bermudan boundary; the convexity-hedging loop; the TBA trade.
* **3D:** the affine yield surface over (short rate, maturity); the forward curve's evolution under HJM.

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

## Build it

```bash
python -m videos.quant.quant19.compute                     # every item, seconds each (fetches and caches the data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant19 SABR  # one chapter, silent, with a contact sheet
python tools/make.py quant19 --cpu-voice -q m              # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Why is a Bermudan worth more than its most expensive European?** The Bermudan's holder can follow the European's
   plan (exercise on its date if in the money, otherwise let it lapse), so the Bermudan is worth at least as much. It is
   worth more because the date is chosen after seeing the path: if rates fall early, exercise early; if late, late. How
   much more depends on how loosely rates on different dates are tied together, which no single European reveals
   (ch. 9: 37% to 52% across mean reversion).
2. **A caplet is quoted at 25% Black volatility with rates at 4%. Roughly what normal vol is that?** σ_N ≈ σ_Black × F =
   0.25 × 4% = 1%: about 100 bp a year. The rule is exact at the money for small σ√T.
3. **An MBS investor hedges duration every day and rates end the year unchanged. Why can they have lost?** Negative
   convexity is short gamma. After rates fall the pool's duration shortens and the hedger must buy duration; after
   they rise, sell it. Each rebalance buys high and sells low, losing about ½|C|σ² a year per unit, whatever the
   direction. The MBS's extra yield is the premium for selling that option (its OAS is what remains).
4. **Hull–White reprices today's curve exactly. Why can its option prices be wrong tomorrow?** The curve is fitted by
   construction (φ); the dynamics (a, σ) are assumed and calibrated to a few options. Tomorrow φ must be refitted, the
   parameters may jump (ch. 3), and products that depend on what was not calibrated (the correlation between dates,
   the smile) carry model risk: the reserve of Rule 19.

## Problems, with solutions

1. **Vasicek's distribution.** r_T = b + (r₀ − b)e^{−aT} + σ∫₀ᵀ e^{−a(T−s)} dW_s, so r_T is normal with that mean and
   variance σ²∫₀ᵀ e^{−2a(T−s)} ds = σ²(1 − e^{−2aT})/(2a). From the bond formula, −ln P(T)/T = −A(T)/T + B(T)r₀/T with
   B → 1/a and A(T)/T → −(b − σ²/(2a²)), so long yields tend to b − σ²/(2a²): the convexity term pulls them below b.
2. **The Riccati equation.** P(t, r) solves P_t + a(b − r)P_r + ½σ²P_rr − rP = 0. Try P = e^{A(τ) − B(τ)r} with τ = T − t:
   matching the terms in r gives B′ = 1 − aB, B(0) = 0, so B = (1 − e^{−aτ})/a; the rest gives A′ = −abB + ½σ²B².
3. **Ho–Lee.** α(t, T) = σ(t, T)∫ₜᵀ σ(t, u) du = σ²(T − t). So f(t, T) = f(0, T) + σ²t(T − t/2) + σW_t: every forward
   moves by the same random shock, and the curve drifts upward and steepens over time, more at longer maturities.
4. **The Hull–White shift.** P(0, T) = E[e^{−∫₀ᵀ(x + φ)}] = e^{−∫₀ᵀφ} e^{½V(0,T)}. Matching P^M(0, T) gives ∫₀ᵀ φ =
   −ln P^M(0, T) + ½V(0, T); differentiate: φ(T) = f^M(0, T) + ½∂V/∂T = f^M(0, T) + σ²(1 − e^{−aT})²/(2a²).
5. **An ATM caplet.** At the money d = 0, so the Bachelier price is σ_N√T φ(0) = σ_N√(T/(2π)) per unit of annuity. The
   caplet: 0.25 × 0.96 × 0.01 × √(1/(2π)) = 0.25 × 0.96 × 0.01 × 0.399 = 0.00096 of notional, about 9.6 bp.
6. **Jamshidian.** Each P(T, tᵢ; x) falls as x rises, so Σcᵢ P(T, tᵢ; x) > 1 exactly when x < x*, and then every P(T, tᵢ;
   x) > Kᵢ = P(T, tᵢ; x*). For x < x*, (Σcᵢ Pᵢ − 1)⁺ = Σcᵢ(Pᵢ − Kᵢ) = Σcᵢ(Pᵢ − Kᵢ)⁺; for x ≥ x* both sides are zero. The
   payoffs agree state by state, so the prices agree.
7. **The bias of a fitted exercise rule.** Fitted and judged on the same paths, the regression has seen those paths'
   futures: it exercises where these particular paths happen to do well, which no real holder could, so the in-sample
   price is biased upward. On independent paths the fitted rule is just a stopping rule someone could follow, and no
   stopping rule beats the optimal one, so its value is a lower bound (plus Monte Carlo noise). Ch. 9: 442 in sample,
   440 out, 441 by the lattice.
8. **A prepaying pool.** Each year a fraction c of the balance prepays, so the balance is (1 − c)ᵗ = e^{t ln(1−c)}. Its
   average life is ∫₀^∞ (1 − c)ᵗ dt = −1/ln(1 − c): 16.2 years at 6% (in practice capped by the 30-year term and
   shortened by amortization), 1.7 years at 45%. That swing in life is the pool's negative convexity.
9. **(qual) Wu and Xia's call.** With s ~ N(a, σ²) and z = (a − r)/σ, E[max(s, r)] = r + E[(s − r)⁺] =
   r + ∫_{r}^{∞}(x − r)φ((x − a)/σ)dx/σ = r + σ∫_{−z}^{∞}(u + z)φ(u)du = r + σ[φ(z) + zΦ(z)] = r + σg(z), using
   ∫_{−z}^∞uφ = φ(z) and ∫_{−z}^∞φ = Φ(z). Then g′(z) = Φ(z) + zφ(z) + φ′(z) = Φ(z), since φ′(z) = −zφ(z).
10. **(qual) The dead short end.** In the one-factor model a_n = θ + (s_t − θ)e^{−κn} − (convexity), so ∂a_n/∂s_t =
   e^{−κn} and ∂f(n)/∂s_t = g′(z_n)e^{−κn} = Φ(z_n)e^{−κn}. With s_t well below the floor, z_n ≪ 0 at short n (the
   shadow forward is far below zero and its variance σ_n² is small), so Φ(z_n) ≈ 0; at long n, a_n has reverted
   towards θ > 0 and σ_n has grown, so z_n > 0 and Φ ≈ 1. News moves s_t; long forwards respond, short ones do not.

## For the researcher

* **The theorems.** Black (1995), "Interest rates as options," *J. Finance* 50(5); Wu and Xia (2016), "Measuring the
  macroeconomic impact of monetary policy at the zero lower bound," *JMCB* 48(2–3); Krippner (2013, 2020) on shadow
  rates and their sensitivity; Swanson and Williams (2014), *AER* 104(10).
* **Simplifications.** One factor and a fixed floor at zero; the risk-neutral dynamics used directly (no term premium);
  the data regression is reduced-form and mixes several factors.
* **Open problems.** Whether shadow rates measure policy; uncertain and negative floors; options near the bound.

## Data and reproducibility

* The Fed's fitted Treasury curve (GSW; `feds200628.csv`), frozen through 31 December 2025 and checksummed; the curve
  of 31 December 2025 is the Svensson fit of that day.
* FRED: DTB3, DFEDTAR, DGS10, ECBDFR, IRLTLT01DEM156N, TEDRATE (discontinued January 2022), MORTGAGE30US, WSHOMCB.
* The NY Fed's ACM term premium (monthly), for comparison.
* Published figures quoted, not computed: Orange County's pools and losses (SEC); WTI's −$37.63 settlement and CME's
  notices; Bloomberg's $18 trillion of negative-yielding debt (December 2020); the SOFR discounting switch.
* Illustrative inputs, labelled on screen: SABR parameters, the caplet vol hump, the prepayment S-curve, the MBS
  pricing model and its assumed market price.
* Two forecasts registered before their hold-out: `cp_tent_oos` and `mlp_bond_premia_oos` (one configuration each);
  the trial counter rises from 311 to 313.

---

# 量化金融，从零搭建 — 第19部分：期限结构模型

第18部分搭建了收益率曲线；本部分让它随机运动，并为它上面的期权定价。本部分讲：

* 短期利率模型：用国库券利率拟合Vasicek（1977）与Cox–Ingersoll–Ross（1985），均值回归速度估计得有多差，以及改用价格拟合同一个模型（ℙ对ℚ）；
* 仿射期限结构（Duffie与Kan，1996）：求解并核对Riccati方程组；用第二个因子对照数据中的相关性；
* Hull–White（1990）拟合当天的曲线和收益率的波动率；Black–Derman–Toy、Black–Karasinski与三叉树；HJM（1992），推导并检验其漂移条件，Ho–Lee作为最简单的情形；
* 利率上限、下限与互换期权：Black（1976）、Bachelier（1900）、Jamshidian分解、平价关系、上限剥离；负利率、零下限与2020年改用Bachelier；SABR（2002）、数据给出的beta、骨架，以及长期限下密度的失效；
* 市场模型（1997）与SOFR的远期市场模型（Lyashenko与Mercurio，2019）；相关性与互换期权；
* 用独立路径上的回归为百慕大互换期权定价（Longstaff与Schwartz，2001），并用精确格点核对；可赎回债券；交易台的风险报告与模型准备金；
* 2008年后的两条曲线，以及抵押品贴现（Piterbarg，2010）；
* 债券风险溢价：Fama–Bliss、Cochrane–Piazzesi（2005）与一个神经网络，在封存的2021–2025年样本外之前登记；宏观金融模型（Ang与Piazzesi，2003）；
* 住房抵押贷款：提前还款、负凸性、期权调整利差、凸性对冲、TBA市场与美联储的持仓；
* 1994年的债市大屠杀与橙县，依据公开记录。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约55分钟）

* **债市大屠杀。** 1994年2月4日：五年来首次加息，到1995年2月共七次，从3%到6%；1994年2年期收益率上升3.3个百分点，10年期上升1.6个；橙县的投资池（198亿美元证券对72亿美元存款，126亿美元逆回购：杠杆2.75倍），15–17亿美元的亏损意味着3.2–3.7年的久期；1994年12月6日破产；历史条（1976–2020）；本部分安排。
* **1. 短期利率模型：Vasicek与CIR。** 两个随机微分方程与Feller条件；用1990–2025年的3个月期国库券拟合（Vasicek：a = 0.124，b = 1.76%，σ = 0.71%；CIR的Feller比值1.02；半衰期5.6年和6.3年）；对2,000条模拟历史重新估计：â的中位数0.163，而真值为0.124，19%的历史估计值超过真值两倍，半衰期的95%区间为3到39年；从当前3.57%出发的扇形图（Vasicek有11%的路径在十年内跌破零）。
* **2. 仿射期限结构。** 推导Feynman–Kac、指数仿射猜测与Riccati方程；三个起始利率下的曲线形状；三维收益率曲面；**实验**：`affine_zcb`与两个闭式解在小数点后六位一致；ℙ对ℚ：用同样的σ拟合432条月末曲线，Vasicek的长期水平为8.2%而不是1.8%（均方根误差87个基点）；两个因子（a = 0.02和0.9）重现了数据中的相关性（2年对10年0.78对0.77，1年对30年0.40对0.42），而单因子模型说是1。
* **3. Hull–White：拟合当天的曲线。** 推导平移φ(t)与债券公式；用2023–2025年收益率的波动率拟合a和σ（a = 0.0087，σ = 1.04%）；在四个时间窗口中做同样的拟合，短端被钉在零附近时（2010–12、2019–21）拟合落在边界上；漂移；20,000条精确路径把曲线重新定价到0.06%以内；Black–Derman–Toy、Black–Karasinski与Hull和White的三叉树。
* **4. Heath–Jarrow–Morton：漂移条件。** 推导漂移条件；Ho–Lee（σ²(T − t)；在1%的波动率下，30年期远期利率十年后的期望值高2.5个百分点）；三个主成分波动率（83.9%、10.6%、3.4%）；三维中远期曲线的演化；鞅检验（0.998到0.990）。
* **5. 利率上限、下限与互换期权。** 推导Black（1976）与Bachelier（1900）；Jamshidian分解；互换期权的看涨看跌平价（在三个行权价上精确成立）；用两种方式报价的Hull–White利率上限单元（正态波动率平坦在104个基点，Black波动率从44%到23%）；上限剥离（从平坦波动率中恢复Rebonato的驼峰）；互换期权网格（100–106个基点）；5年期上限价格为3.06%。
* **6. 负利率与Bachelier。** 欧洲央行存款便利利率从2014年6月11日到2022年7月26日低于零（最低−0.50%）；德国10年期国债收益率（38个月低于零，2019年8月为−0.65%）；Black模型在零处的墙、平移Black、Bachelier；远期利率为0.5%时，零下限在Bachelier下值89个基点，在Black下一文不值；WTI −37.63美元与芝商所改用Bachelier（2020年4月）。
* **7. 利率的SABR模型。** 模型与正态SABR公式；六十年来10年期收益率的已实现波动率，正态（1980年285个基点）与对数正态（2020年108%）；数据给出β = 0.30（正态波动率的离散程度52%，对数正态79%）；α、ρ、ν三个旋钮；骨架与对冲；10年期限下的Hagan展开：0.75%以下密度为负，以及无套利SABR（2014）。
* **8. 市场模型：LIBOR与SOFR。** BGM、Jamshidian、Miltersen–Sandmann–Sondermann（1997）；终端测度下的漂移；十个上限单元的蒙特卡洛价格与Black和Bachelier相差在1.3%以内；相关性与5年×5年互换期权（β从0到1时，90个基点降到52；β = 0.2时公式77.4对模拟77.4）；SOFR的远期市场模型。
* **9. 百慕大互换期权。** 10年期、1年后可行权、行权利率4.37%的收取方期权；在一组路径上拟合LSM、在另一组上定价：440 ± 4个基点，而最贵的欧式为321；终端测度下的精确格点：欧式误差0.002%，百慕大441.0；行权边界；可赎回债券（96.36对子弹式债券100.77：收益率高56个基点）；均值回归与切换期权（溢价从37%到52%）。
* **10. 多曲线与抵押品。** TED利差（2007年前0.39%；2008年10月10日4.58%；2020年3月1.42%）；预测与贴现；一条曲线对两条曲线（平价利率相差0.15个基点；偏离市场的互换每100相差0.06）；Piterbarg（2010）；按CSA贴现、估值调整，以及SOFR的单一曲线（2020年10月）。
* **11. 债券风险溢价。** 预期假说；在美联储曲线上的Fama–Bliss回归（斜率0.72–1.20，离零约三个标准误）；Cochrane–Piazzesi回归（到2003年R² 24%，到2025年15%；系数不稳定）；CP与一个5–16–1网络在封存的2021–2025年样本外之前登记：样本外R²在2004–2020年为−2.17和−1.01，在封存期为+0.26和+0.44，靠的是水平而非时机（相关系数−0.31和0.06）；预测值对ACM期限溢价（相关系数0.83）；Ang与Piazzesi（2003）；试验计数器313。
* **12. 住房抵押贷款与负凸性。** 房地美的30年期利率（1981年18.63%，2021年2.65%，2025年底6.15%）；提前还款S形曲线；用模拟为6.5%的资产池定价（久期2.1，凸性−240）；期权调整利差92个基点，零波动率利差150个基点（期权成本58个基点）；凸性对冲与2003年夏天（10年期从3.13%升到4.61%）；TBA市场与美元滚动；美联储持有的MBS（2022年4月2.74万亿美元，2025年底2.04万亿）。
* **13. 第19条规则：利率期权交易台。** 五项模型检验；10亿美元百慕大期权的晨报（每基点delta −35.1万美元，每基点波动率vega +47.0万美元）及其对冲（1.36份欧式期权加一笔小额互换）；模型准备金（不同均值回归下441–487个基点，而噪声只有±4）；期限结构模块；第19条规则。
* **写给研究者：零下限与影子利率。** 布莱克（1995）：r = max(s, r_min)，影子利率为高斯（Vasicek）过程；价格由一维PDE给出。吴菁与夏凡（2016）：f(n) ≈ r_min + σ_n g((a_n − r_min)/σ_n)，g(z) = zΦ(z) + φ(z)，即远期测度下下限加上对影子远期a_n的Bachelier看涨期权，所以∂f/∂s ≈ Φ(z_n)e^{−κn}。取κ 0.15、θ 4%、σ 1.5%：精确解（隐式有限差分）与吴–夏远期在十年期相差8个基点以内，其他期限几个基点，影子利率从−3%到+3%都如此；影子利率为−3%时，下限相对影子远期的溢价在1/2/5/10年为208/152/77/40个基点。模型中1年对10年的敏感度之比在s ≈ −2.5%时降到正常的十分之一。美国国债（GSW日度数据，Δy(1)对Δy(10)的逐年回归）：1990–2007年斜率平均0.62，2010–2014年0.10（1年期收益率0.22%），2019年回到0.51；斯旺森与威廉斯（2014）在对消息的反应中发现了同样的现象。三个开放问题；暂停题：z = −1时f = 1% × g(−1) = 0.083%，影子利率再降50个基点使它下降0.5% × Φ(−1) × 0.8 = 6个基点。
* **回顾、交易台问题、十道习题（两道为资格考试水平）。** 十三行回顾；四个交易台问题；解答见下文。

## 交易台问题与解答

1. **为什么百慕大期权比它最贵的欧式期权更值钱？** 百慕大期权的持有人可以照搬欧式期权的做法（在其日期若为价内就行权，否则放弃），所以至少同样值钱。它更值钱，是因为日期可以在看到路径之后再选：利率早跌就早行权，晚跌就晚行权。多出多少，取决于不同日期的利率之间联系有多松，而任何单个欧式期权都看不出这一点（第9章：随均值回归不同，溢价从37%到52%）。
2. **一个利率上限单元报价为25%的Black波动率，利率为4%。大约相当于多少正态波动率？** σ_N ≈ σ_Black × F = 0.25 × 4% = 1%：约每年100个基点。在平值且σ√T较小时这一规则是精确的。
3. **一位MBS投资者每天对冲久期，而利率年底回到年初水平。为什么仍可能亏钱？** 负凸性就是空头gamma。利率下跌后资产池的久期缩短，对冲者必须买入久期；利率上升后则要卖出。每次再平衡都是高买低卖，无论方向，每单位每年约亏½|C|σ²。MBS多出的收益率是卖出这个期权的权利金（剩下的才是期权调整利差）。
4. **Hull–White精确地重新定价了今天的曲线。为什么它的期权价格明天可能是错的？** 曲线是按构造拟合的（φ）；动态（a、σ）是假设的，并且只校准到少数几个期权。明天φ必须重新拟合，参数可能跳变（第3章），而依赖于未校准部分（不同日期之间的相关性、微笑）的产品带有模型风险：这就是第19条规则中的准备金。

## 习题与解答

1. **Vasicek的分布。** r_T = b + (r₀ − b)e^{−aT} + σ∫₀ᵀ e^{−a(T−s)} dW_s，所以r_T服从正态分布，均值如上，方差为σ²∫₀ᵀ e^{−2a(T−s)} ds = σ²(1 − e^{−2aT})/(2a)。由债券公式，−ln P(T)/T = −A(T)/T + B(T)r₀/T，其中B → 1/a、A(T)/T → −(b − σ²/(2a²))，所以长期收益率趋于b − σ²/(2a²)：凸性项把它拉到b以下。
2. **Riccati方程。** P(t, r)满足P_t + a(b − r)P_r + ½σ²P_rr − rP = 0。令τ = T − t，试P = e^{A(τ) − B(τ)r}：比较含r的项得B′ = 1 − aB、B(0) = 0，所以B = (1 − e^{−aτ})/a；其余部分给出A′ = −abB + ½σ²B²。
3. **Ho–Lee。** α(t, T) = σ(t, T)∫ₜᵀ σ(t, u) du = σ²(T − t)。所以f(t, T) = f(0, T) + σ²t(T − t/2) + σW_t：每个远期利率受到同一个随机冲击，曲线随时间向上漂移并变陡，期限越长越明显。
4. **Hull–White的平移。** P(0, T) = E[e^{−∫₀ᵀ(x + φ)}] = e^{−∫₀ᵀφ} e^{½V(0,T)}。令其等于P^M(0, T)得∫₀ᵀ φ = −ln P^M(0, T) + ½V(0, T)；求导：φ(T) = f^M(0, T) + ½∂V/∂T = f^M(0, T) + σ²(1 − e^{−aT})²/(2a²)。
5. **平值利率上限单元。** 平值时d = 0，所以Bachelier价格为每单位年金σ_N√T φ(0) = σ_N√(T/(2π))。该单元：0.25 × 0.96 × 0.01 × √(1/(2π)) = 0.25 × 0.96 × 0.01 × 0.399 = 名义本金的0.00096，约9.6个基点。
6. **Jamshidian。** 每个P(T, tᵢ; x)都随x上升而下降，所以恰好当x < x*时Σcᵢ P(T, tᵢ; x) > 1，此时每个P(T, tᵢ; x) > Kᵢ = P(T, tᵢ; x*)。当x < x*时，(Σcᵢ Pᵢ − 1)⁺ = Σcᵢ(Pᵢ − Kᵢ) = Σcᵢ(Pᵢ − Kᵢ)⁺；当x ≥ x*时两边都为零。支付在每个状态下都相同，所以价格相同。
7. **拟合出的行权规则的偏差。** 在同一组路径上拟合并评判时，回归已经"看见"了这些路径的未来：它在这些特定路径恰好表现好的地方行权，这是任何真实持有人都做不到的，所以样本内价格偏高。在独立路径上，拟合出的规则只是一个任何人都能执行的停止规则，而没有停止规则能胜过最优规则，所以它的价值是一个下界（加上蒙特卡洛噪声）。第9章：样本内442，样本外440，格点441。
8. **提前还款的资产池。** 每年余额的c比例提前还款，所以余额为(1 − c)ᵗ = e^{t ln(1−c)}。平均寿命为∫₀^∞ (1 − c)ᵗ dt = −1/ln(1 − c)：在6%时为16.2年（实际上受30年期限限制并因摊还而缩短），在45%时为1.7年。寿命的这种摆动正是资产池的负凸性。
9. **（资格考试）吴–夏的看涨期权。** s ~ N(a, σ²)、z = (a − r)/σ时，E[max(s, r)] = r + E[(s − r)⁺] = r + σ∫_{−z}^{∞}(u + z)φ(u)du = r + σ[φ(z) + zΦ(z)] = r + σg(z)。又g′(z) = Φ(z) + zφ(z) + φ′(z) = Φ(z)，因为φ′(z) = −zφ(z)。
10. **（资格考试）失去反应的短端。** 单因子模型中a_n = θ + (s_t − θ)e^{−κn} − （凸性），所以∂f(n)/∂s_t = Φ(z_n)e^{−κn}。s_t远低于下限时，短期n处z_n ≪ 0（影子远期远低于零且方差σ_n²小），Φ(z_n) ≈ 0；长期n处a_n已回复到θ > 0且σ_n变大，z_n > 0、Φ ≈ 1。消息移动s_t；长期远期有反应，短期远期没有。

## 数据与复现

* 美联储拟合的美国国债曲线（GSW；`feds200628.csv`），冻结到2025年12月31日并校验哈希；2025年12月31日的曲线是当天的Svensson拟合。
* FRED：DTB3、DFEDTAR、DGS10、ECBDFR、IRLTLT01DEM156N、TEDRATE（2022年1月停止更新）、MORTGAGE30US、WSHOMCB。
* 纽约联储的ACM期限溢价（月度），用于比较。
* 引用而非计算的公开数字：橙县投资池及其亏损（美国证监会）；WTI −37.63美元的结算价与芝商所的通知；彭博统计的18万亿美元负收益率债务（2020年12月）；SOFR贴现切换。
* 屏幕上标注为示意的输入：SABR参数、上限单元波动率驼峰、提前还款S形曲线、MBS定价模型及其假设的市场价格。
* 在样本外之前登记的两个预测：`cp_tent_oos`与`mlp_bond_premia_oos`（各一种配置）；试验计数器从311升到313。

## 写给研究者

* **定理。** 布莱克（1995），*J. Finance* 50(5)；吴菁与夏凡（2016），*JMCB* 48(2–3)；Krippner（2013、2020）论影子利率及其敏感性；斯旺森与威廉斯（2014），*AER* 104(10)。
* **简化。** 单因子、下限固定为零；直接使用风险中性动态（无期限溢价）；数据回归是简约式的，混合了多个因子。
* **开放问题。** 影子利率是否度量政策立场；不确定的与负的下限；下限附近的期权。
