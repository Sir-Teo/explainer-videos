# Quant, Built — Part 21: Counterparty Risk, XVA and Clearing

Visual pass complete on `quantitative-finance`: 34 bilingual endpoint sheets,
17 English motion sheets and 27 focused native frames reviewed on the
frozen source. The chaptered silent preview runs 63:53. Full continuous
production-voice listening remains pending; signal checks do not certify pronunciation.
See [the evidence record](../../../docs/qa/quant21-polish-evidence.json).

Part 21 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), part of Act III, Derivatives (Q), and the fourth of its five parts on rates, credit and the basis (18–22). Part 20 priced the chance that a
borrower does not pay; this part prices the same chance for the other side of every derivative, and the collateral,
funding, capital and clearing that grew up around it. It covers:

* exposure: values on paths of a dated-curve Hull–White illustration with historical parameter proxies, expected and potential exposure, product shapes,
  netting and the law behind it, the regulators' effective EPE;
* collateral: thresholds, minimum transfers, the margin period of risk, Treasury collateral and haircuts, re-use and
  segregation;
* CVA and DVA derived and computed; CVA as a position (CS01 and its CDS hedge), incremental pricing, Monte Carlo and
  model error; wrong-way risk by copula and by Hull and White's hazard model, and Basel's alpha;
* FVA with symmetric and asymmetric funding, the FVA debate, KVA and MVA;
* sensitivities by adjoint differentiation, with the tape worked by hand; a network that learns a book's future
  values from cash flows, against per-date regression;
* initial margin: SIMM's derivation, the regulatory schedule, IM against the MVA it costs; procyclicality, EMIR's
  anti-procyclicality tools and a Kupiec backtest;
* clearing: novation, Duffie and Zhu's netting result, the default waterfall simulated, Lehman at LCH (2008) and Einar
  Aas at Nasdaq Clearing (2018);
* from the public record: the LME's nickel market (March 2022) and Archegos (March 2021); capital: SA-CCR, Basel's
  basic CVA charge, the leverage ratio.

Numerical examples use the series' own code ([`compute.py`](compute.py), and the House's new
[`xva`](../../../explainer/quant/house/xva.py) module), on the Fed's zero curve of 31 December 2025 and a Hull–White
model fitting that curve with historical volatility proxies, rather than option-price calibration. The floating leg is reset at each exposure date, ignoring past fixings. CVA uses deterministic-discount approximations under specified independence and closeout assumptions. Data: FRED (the 10-year Treasury yield, daily; the IMF's nickel price, monthly).

*An education in methods, not investment advice. Firms and episodes are described from the public record, as
reported by the sources named.*

## Chapters (about 55 minutes)

* **The other side of every trade** (2.5 min). Archegos's banks' reported losses (Credit Suisse 5.5, Nomura 2.9, Morgan
  Stanley 0.9, UBS 0.9, MUFG 0.3, $ billion); the history strip (1987–2023); the plan; the credit desk becomes an XVA
  desk.
* **1. Exposure** (3.8). EE, ENE and PFE defined; a fan of values for a 10-year payer swap (Hull–White, a = 0.0087,
  σ = 1.04%); the hump (EE peaks at 5.9m near year 4; PFE 19.2m); product shapes (swap, FX forward, cross-currency
  swap, bought option); netting a three-swap set (EE 21% lower); close-out netting and the ISDA master agreements;
  effective EPE (1.20m) and α = 1.4.
* **2. Collateral and the margin period of risk** (3.4). The CSA; EPE 2.98 → 1.08 (threshold $2m) → 0.81 (zero
  threshold, monthly grid); daily margin with a 10-day MPOR: 0.45 of the uncollateralised EPE; minimum transfer
  amounts (242 calls a year at zero, 8 at $2m, for 19% more EPE); Treasuries as collateral (+1.4% EPE unhaircut, −2.3%
  with Basel's 4%); re-use and segregation.
* **3. CVA and DVA** (4.5). The formula derived; CVA $404k (about 5 bp a year of notional), month by month; bilateral
  CVA 381k, DVA 154k, rising to 729k at six times the bank's own spread; CVA against the counterparty's spread (212k at
  half, 1,216k at four times), CS01 $1,957 a bp and a $4.6m CDS hedge; incremental CVA (a 5-year receiver: 60k alone,
  −12k added); Monte Carlo error (27k at 250 paths, 3.4k at 16,000) and model error (403–411k across mean reversions,
  re-fitted); the Basel Committee's two thirds.
* **4. Wrong-way risk** (2.8). The conditional formula; a Gaussian copula (CVA 366k at ρ = 0, 668k at 0.9, 195k at
  −0.6); Hull and White's hazard model λ = exp(a(t) + bV), refitted to the CDS curve (b = 0.1: 404k → 753k); α as
  partly its price (×1.25 at ρ = 0.3); general and specific wrong-way risk.
* **5. FVA, KVA and MVA** (3.4). Funding an uncollateralised client hedged with a collateralised dealer; Burgard–Kjaer,
  Hull–White's FVA debate, J.P. Morgan's $1.5 billion (January 2014); KVA derived (511k at a 10% hurdle); the stack
  (CVA, DVA, FCA, FBA, KVA, MVA); asymmetric funding (FVA 22k at 80/80 bp, 140k at 80/20, 297k at 150/20).
* **6. Sensitivities by AAD** (2.4). Bumping against one reverse sweep; the tape worked by hand for one default bucket;
  14 sensitivities agreeing with bumps (1.1 s against 1.1 s in this CPU run); **lab**: `cva_torch`.
* **7. A network that learns future values** (2.7). V(t, x) as a conditional expectation; training on realised
  discounted cash flows only; on fresh paths the CVA is 423k against the 414k reset-approximation reference (+2%), the coupon steps rounded off;
  against per-date regression (cubic: RMSE 0.19 against the network's 1.04; CVA +1.8%), and the 23,426 terms a cubic
  needs in 50 factors.
* **8. Initial margin** (3.5). The rules (2016–2022); a normal delta-only motivation for a SIMM-style quadratic form; key-rate DV01s and a SIMM-style IM of
  $3.4m; the regulatory schedule ($6.0m without netting credit); the IM profile; IM against CVA and MVA (at the 99th
  percentile CVA falls from 15k to 0.2k while MVA is 89k).
* **9. Margin procyclicality** (2.7). A 10-day 99% margin on 10-year notes from the daily yield: EWMA from $2.88 to $6.59
  per $100 in March 2020; the loop; EMIR's tools (jump ×2.3 alone, ×2.1 with a 25% buffer, ×1.6 with a 10-year floor,
  at 40% more margin in calm times); a overlapping-window, two-sided diagnostic (28 exceptions in 2,238 windows, 1.25%; iid-reference p = 0.25 does not certify coverage).
* **10. Central clearing** (3.4). Novation; Duffie and Zhu (clearing one of K classes helps only with more than 7, 15,
  31 dealers for K = 2, 4, 8); the waterfall; a simulated CCP (under the fixed toy law, survivors' fund is reached in about one in eight scenarios conditional on a default); Lehman at LCH (66,390 swaps, $9 trillion, about a third of its margin used) and Aas at Nasdaq Clearing
  (€114m beyond collateral; €7m of the CCP's capital; €107m of a €166m fund).
* **11. March 2022: the LME's nickel market** (2.5). Monthly prices (IMF); $28.9k, $48.1k, $101.4k a tonne on 4, 7 and 8
  March; variation margin on a hypothetical 100,000-tonne short ($1.9bn, then $5.3bn); the suspension and the
  cancelled trades; price limits; the High Court (2023) and the FCA's £9.2 million fine (2025).
* **12. Capital for counterparty risk** (2.7). SA-CCR derived for swaps; the netting set (8.1 alone, 4.8 netted, 1.4
  margined, $m of EAD); the PFE multiplier (0.61 one add-on out of the money, floor 5%); Basel's basic CVA charge
  (about $580k for this set; per-name capital falls only to half across many names); CVA capital and the leverage
  ratio.
* **13. March 2021: Archegos** (3.6). The total return swap; the fire sale; margin against the liquidation horizon (20%
  covers about 0.65 days' volume for a 4%-a-day stock; the Paul, Weiss report's 2.5–10 days at Credit Suisse alone);
  the race to sell (stylised: losses 20 against 40); the record.
* **14. Rule 21: the XVA desk** (2.7). One ticket (CVA, DVA reported, FVA, KVA, MVA: the client pays about $1.05
  million); the desk's night; the `xva` module; Rule 21; the rule against this part's three cases.
* **For the researcher: finite wrong-way bounds.** A transportation LP fixes an empirical law of 1,500 exposure paths and 120 monthly default buckets plus survival. Under deterministic discounting its independence value is 0.40m, maximum 1.81m and minimum 0.00. These are conditional finite bounds, allowing static couplings that need not be adapted or economically realizable. Sinkhorn points are plotted at their achieved KL values, with normalized costs; a penalty path does not solve every pre-set entropy budget. Chapter 4's flat-hazard copula and full-path hazard-link examples have different default or empirical path margins, so numerical inclusion does not establish a bound theorem. Matching margins and costs is a prerequisite. The worked two-path answer gives 1, 2 and 0.
* **Recap, desk questions, problems** (3.5). Sixteen lines; six desk questions; twelve problems (two at
  qualifying-exam level), solutions below.

## Hands-on

The learning diagram abbreviates parameter fitting: θ* minimizes the empirical squared loss, then the fitted value function is V at θ*. In problem 5, the constant margin-period exposure formula applies after the lag window, t ≥ m.

* **Labs** (the House's own code on screen, then run): `cva_torch` (ch. 6).
* **Computed:** exposure on 20,000 Hull–White paths; collateral on a daily grid; CVA, DVA, FVA, KVA and MVA; CS01 and
  incremental CVA; two wrong-way models; AAD against bumps; a network and per-date regressions; IM, its funding, and
  a margin backtest on fifteen years of the 10-year yield; a simulated clearing house.
* **Live constructions:** the exposure fan; the margin lag; the computation tape run forwards and backwards; the
  SIMM quadratic form; the default waterfall filling; the procyclicality loop; the fire-sale race.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Gregory, *The xVA Challenge* (4th ed.) | 3–4 (exposure, netting), 6–8 (collateral, margin, clearing), 11–12 (exposure models), 14–17 (CVA, DVA, wrong-way), 18–21 (FVA, MVA, KVA), 13 (capital) | ch. 1–5, 8–12 |
| Green, *XVA: Credit, Funding and Capital Valuation Adjustments* | 3–4 (CVA, DVA), 9–11 (FVA), 12–13 (KVA, MVA), 15–16 (Monte Carlo, AAD) | ch. 3–6 |
| Brigo, Morini and Pallavicini, *Counterparty Credit Risk, Collateral and Funding* | 4–5 (unilateral and bilateral CVA), 8 (wrong-way risk), 9–10 (collateral, funding) | ch. 3–5 |
| Hull, *Options, Futures, and Other Derivatives* | 24 (credit risk: CVA), 9 (OIS discounting and collateral) | ch. 2–3 |

## Papers, chapter by chapter

* Hook and ch. 1–2: Paul, Weiss, *Report on Archegos Capital Management* (to Credit Suisse's board, July 2021); ISDA
  master agreements (1987, 1992, 2002); Basel Committee, the IMM and α (2005); Canabarro, Picoult and Wilde (2003).
* ch. 3: Brigo and Masetti (2005); Gregory (2009); Basel Committee press release on Basel III (2011, the two thirds).
* ch. 4: Hull and White (2012), "CVA and wrong-way risk"; Pykhtin and Zhu (2007).
* ch. 5: Piterbarg (2010); Burgard and Kjaer (2011); Hull and White (2012), "The FVA debate"; Green, Kenyon and Dennis
  (2014); J.P. Morgan, fourth-quarter 2013 results.
* ch. 6–7: Giles and Glasserman (2006); Capriotti (2011); Longstaff and Schwartz (2001); Gnoatto, Picarelli and
  Reisinger (2023).
* ch. 8–9: BCBS–IOSCO, *Margin requirements for non-centrally cleared derivatives* (2015); ISDA SIMM methodology;
  Commission Delegated Regulation (EU) 153/2013, Article 28; Kupiec (1995); Christoffersen (1998).
* ch. 10: Duffie and Zhu (2011); CPMI–IOSCO, *Principles for Financial Market Infrastructures* (2012); Cont (2015); BIS
  Quarterly Review (December 2018), "Two defaults at CCPs, 10 years apart".
* ch. 11: LME notices (8 and 16 March 2022); the High Court's judgment (November 2023); FCA final notice (March 2025).
* ch. 12: Basel Committee, SA-CCR (2014) and the CVA framework (2020, MAR50); Andersen, Duffie and Song (2019).

## Build it

```bash
python -m videos.quant.quant21.compute                       # every item (fetches and caches the data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant21 CVA     # one chapter, silent, with a contact sheet
python tools/make.py quant21 --cpu-voice -q m                # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **Why does a bank's DVA increase as its credit gets worse, and is that profit real?** DVA reflects own non-performance risk under the specified closeout convention. A worse credit makes that likelier, so the liability is worth less
   and the bank books a gain. Accounting standards (IFRS 13, ASC 820) require it, but recognition is not freely spendable income; realization and prudential adjustments depend on the instrument and applicable rules (ch. 3).
2. **Two offsetting swaps with one counterparty: exposure with and without netting?** With netting, nothing: the
   values cancel on every path. Without it, the sum of each swap's positive part: the liquidator collects on the swap
   the defaulter is winning and leaves the bank an unsecured claim on the other (ch. 1).
3. **A counterparty posts daily cash margin with a zero threshold. How can you still lose?** Through the move between
   its last payment and the close-out (the margin period of risk, ch. 2), through the cost of replacing hedges in a
   market that has moved, through disputes and transfer thresholds, and through collateral that falls with the
   counterparty or the exposure (wrong-way, ch. 2 and 4).
4. **Why does margin rise exactly when cash is scarce?** Margin models scale with recent volatility, and volatility
   rises in a crisis; every margined position is called at once, the cash is raised by selling, and selling raises
   volatility again (ch. 9). Buffers, floors and longer look-backs damp the loop at the cost of more margin in calm
   times.
5. **What does a backward pass get wrong at max(V, 0), or at a jump in a payoff?** At a kink it returns the derivative
   on one side, which is correct almost everywhere and harmless on average. At a jump the pathwise derivative is zero
   almost everywhere and misses the jump's contribution entirely. Smooth the payoff (replace the step with a narrow
   sigmoid), or estimate those terms with likelihood-ratio or conditional-expectation methods (ch. 6).
6. **A client posts 20% margin on a single-stock swap. What do you most want to know?** The size of its position
   against the stock's daily volume, at every dealer combined: that sets how long a liquidation takes, and so the
   margin (ch. 13). It is hard to see because a swap leaves the shares in the dealers' names, and each dealer sees only
   its own.

## Problems, with solutions

In problem 11, M counts all transport columns, including survival. The research example has 120 default buckets plus one survival column. Pathwise sensitivity arguments at kinks require regularity and a justified exchange of differentiation and expectation; atoms and discontinuities need separate treatment.

1. **A forward's exposure.** V(t) = σW_t is normal with mean 0 and variance σ²t, so EE(t) = E[max(σW_t, 0)] = σ√t
   E[max(Z, 0)] = σ√t φ(0) = σ√(t/2π). Its 95th percentile is 1.645 σ√t, and PFE₉₅ = 1.645 σ√t since that is positive.
2. **The swap's hump.** f(t) = √t (T − t) has f′(t) = (T − t)/(2√t) − √t = 0 when T − t = 2t, so t = T/3: 3.3 years for
   a 10-year swap. Chapter 1's profile peaks near year 4 on a monthly grid, later than T/3 because the coupons are
   annual, so the remaining payments fall in steps rather than smoothly.
3. **CVA as a spread.** With a constant EE, flat hazard λ and rate r, the default density is λe^{−λt}, so CVA = (1 − R)
   EE ∫₀ᵀ e^{−rt} λ e^{−λt} dt = (1 − R) λ EE ∫₀ᵀ e^{−(r+λ)t} dt. Dividing by the risky annuity ∫₀ᵀ e^{−(r+λ)t} dt on
   notional N gives a running spread of (1 − R) λ EE/N: the credit triangle applied to the exposure.
4. **Bilateral CVA.** The bank loses on the counterparty's default at t only if it has not defaulted itself first. With
   independent defaults, P(τ_c ∈ dt, τ_b > t) = Q_b(t)(−dQ_c(t)), so CVA_bil = (1 − R) ∫ EE(t) P(0, t) Q_b(t)(−dQ_c(t)).
   Since Q_b(t) ≤ 1 everywhere, it is no larger than the unilateral CVA, and smaller whenever the bank can default.
5. **Collateralised exposure.** With zero threshold and margin period m, the collateral at t is V(t − m), so the
   exposure is max(σ(W_t − W_{t−m}), 0). The increment is normal with variance σ²m whatever t is, so EE = σ√(m/2π),
   constant in time: the square root of the margin period, not of the trade's age.
6. **An SA-CCR add-on by hand.** The supervisory duration is (e^{−0.05·0} − e^{−0.05·10})/0.05 = (1 − 0.607)/0.05 = 7.87,
   so the effective notional is 100 × 7.87 = 787 (one trade, in the over-five-years bucket, maturity factor 1). The
   add-on is 0.5% × 787 = $3.93 million and, with zero replacement cost and multiplier 1, EAD = 1.4 × 3.93 = $5.5
   million: chapter 12's "10y payer alone".
7. **Cover 2.** Under the exercise's imposed Cover Two requirement, resources cover the two largest stressed aggregate exposures beyond member margin in extreme but
   plausible markets: 30 + 25 = 55. If the third largest also defaults, its own margin and fund contribution are used
   first, then what remains of the mutualised fund after the CCP's own capital; beyond that, assessments on the
   surviving members, capped by the rulebook, and then recovery tools such as haircutting variation-margin gains. The
   survivors pay.
8. **The cost of AAD.** Reverse mode computes the gradient as a vector–Jacobian product, sweeping the recorded
   operations once backwards; each operation's adjoint costs a small constant multiple of the operation itself, so all
   n sensitivities cost a few valuations regardless of n, against n + 1 valuations for one-sided bumps. The price is
   memory: every intermediate value of the forward pass (each path, date and operation) must be stored for the
   backward one, or recomputed from checkpoints.
9. **When clearing one product helps.** Bilaterally, a dealer's exposure to each of N − 1 counterparties nets K
   independent classes of variance σ², so it is σ√K φ with φ = 1/√(2π), and the total is (N − 1)σ√K φ. Clearing one
   class leaves (N − 1)σ√(K − 1)φ bilaterally and adds σ√(N − 1)φ at the CCP, where that class nets across all N − 1
   counterparties. Clearing helps iff (N − 1)(√K − √(K − 1)) > √(N − 1), that is √(N − 1) > 1/(√K − √(K − 1)) = √K +
   √(K − 1), or N > 1 + (√K + √(K − 1))²: 7, 15 and 31 dealers for K = 2, 4 and 8.
10. **A KVA by hand.** KVA = h ∫₀ᵀ K₀(1 − t/T) dt = h K₀ [t − t²/(2T)]₀ᵀ = h K₀ T/2: the hurdle rate times the average
    capital times the life.
11. **(qual) The transport problem.** With c_ij = (1 − R)D(t_j)V_i(t_j)⁺ (and c = 0 for survival), CVA(p) = Σc_ij p_ij is
   linear in p, and the feasible set {p ≥ 0: Σ_j p_ij = 1/N, Σ_i p_ij = q_j} is a transportation polytope. A linear
   function attains its maximum and minimum at vertices, and a vertex of an N × M transportation polytope has at most
   N + M − 1 positive cells (its support is a forest in the bipartite graph). Two paths (0 and 10, weight ½ each), one
   date with q = 0.2: independence gives 0.2 × 5 = 1; the worst puts all 0.2 on the second path (feasible, since
   0.2 ≤ ½): 2; the best puts it on the first: 0.
12. **(qual) The entropic solution.** Assume θ > 0 and positive prescribed margins. The Lagrangian Σp c − (1/θ)Σp log(p/p⊥) + Σ_i α_i(Σ_j p_ij − 1/N) + Σ_j β_j(Σ_i p_ij −
   q_j) has first-order condition c_ij − (1/θ)(log(p_ij/p⊥_ij) + 1) + α_i + β_j = 0, so p_ij = a_i b_j p⊥_ij e^{θc_ij}
   with a_i = e^{θα_i − 1/2}, b_j = e^{θβ_j − 1/2}. Sinkhorn alternates a ← (1/N)/(Kb), b ← q/(Kᵀa) with K = p⊥e^{θc};
   each step is a Bregman projection onto one set of margins, and the iteration converges to the unique solution.

## For the researcher

* **The theorems.** Glasserman and Yang (2018), "Bounding wrong-way risk in measuring counterparty risk,"
  *Management Science* 64(12); Cuturi (2013) and Sinkhorn (1964) for entropic transport; Hull and White (2012);
  Brigo, Morini and Pallavicini (2013) for the modelling side.
* **Simplifications.** A 1,500-path subsample for the LPs; monthly buckets; the coupling allowed to look at the whole
  path (not only past exposure), which makes the worst case larger than a non-anticipative one.
* **Open problems.** Calibrating the entropy budget; time-respecting couplings; replacing the α multiplier.

## Data and reproducibility

The product-shape comparison includes a weighted rate/FX profile mixture and a flat positive option proxy; it does not value a jointly simulated cross-currency swap. The CVA running-spread conversion uses a $100 million reference notional against a $200 million gross swap book. CDS hazards are bootstrapped with a flat 4% discount assumption, separately from the dated exposure curve.

* FRED: DGS10 (daily, 2006–2025), PNICKUSDM (the IMF's nickel price, monthly); the Fed's fitted zero curve (Gürkaynak,
  Sack and Wright), as of 31 December 2025; frozen and checksummed.
* Published figures quoted, not computed: the banks' Archegos losses; LCH's and Nasdaq Clearing's defaults (BIS); the
  LME's daily prices, the cancelled trades and the FCA's fine; J.P. Morgan's FVA charge; the Paul, Weiss report's
  liquidation estimates.
* Illustrative inputs, labelled on screen: the counterparty's and the bank's CDS curves (80–170 and 40–85 bp), funding
  spreads, the SIMM-style risk weights, the capital proxy and hurdle rate, the clearing house's members and stresses,
  the hypothetical nickel position, the Archegos-style stock and the fire-sale model.
* No hold-out is opened in this part; the cumulative trial counter remains 317 through Part21 (23,562 globally).

---

# 量化金融，从零搭建 — 第21部分：交易对手风险、XVA与清算

本轮视觉复核完成：已实际检查34张双语旁白节点画面表、17张英文动画画面表及27张原尺寸重点画面。配音开场及分章静音预览已核验。完整成片连续听审与发音验证仍待完成，信号检查不能替代听审。

本例使用2025年末公开曲线与历史波动率代理，并未对交易期权价格校准。浮息腿在每个估值日重设，忽略既有定盘利率。CVA采用明确假设下的确定性贴现近似。资金、资本及保证金成本须统一政策，避免重复计入。

第20部分为借款人不还钱的可能性定价；本部分为每一笔衍生品另一方的同一种可能性定价，以及围绕它发展起来的抵押品、融资、资本和清算。本部分讲：

* 敞口：在拟合指定曲线、采用历史参数代理的Hull–White示例中的路径价值，预期敞口与潜在未来敞口，不同产品的形状，净额结算及其背后的法律，监管的有效EPE；
* 抵押品：门槛、最低转移金额、风险保证金期，国债作为抵押品与折扣率，再使用与隔离；
* 推导并计算CVA与DVA；作为头寸的CVA（CS01及其CDS对冲）、增量定价、蒙特卡罗误差与模型误差；用连接函数和Hull–White风险率模型刻画错向风险，以及巴塞尔的α；
* 对称与不对称融资下的FVA、FVA之争、KVA与MVA；
* 伴随微分求敏感度，并手算计算记录；从现金流学习账簿未来价值的神经网络，与逐日回归比较；
* 初始保证金：SIMM的推导、监管表格法、初始保证金与它带来的MVA；顺周期性、EMIR的逆周期工具与Kupiec回测；
* 清算：更替、Duffie和Zhu关于净额结算的结论、模拟违约瀑布、雷曼在LCH（2008）与Einar Aas在纳斯达克清算所（2018）；
* 依据公开记录：伦敦金属交易所的镍市场（2022年3月）与Archegos（2021年3月）；资本：SA-CCR、巴塞尔基本法CVA资本、杠杆率。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录，并注明报道来源。*

## 章节（约55分钟）

* **每笔交易的另一方。** Archegos相关银行报告的损失（瑞信55亿、野村29亿、摩根士丹利9亿、瑞银9亿、三菱日联3亿美元）；历史条（1987–2023）；本部分安排；信用交易台变成XVA交易台。
* **1. 敞口。** 定义EE、ENE与PFE；10年期付固定互换的价值扇形（Hull–White，a = 0.0087，σ = 1.04%）；驼峰（EE在第4年附近达到590万美元峰值；PFE 1,920万）；产品形状（互换、外汇远期、交叉货币互换、买入期权）；三笔互换的净额集（EE降低21%）；平仓净额与ISDA主协议；有效EPE（120万）与α = 1.4。
* **2. 抵押品与风险保证金期。** 信用支持附件；EPE 2.98 → 1.08（门槛200万美元）→ 0.81（零门槛，月度网格）；每日保证金、10天风险保证金期：未抵押EPE的0.45；最低转移金额（零时每年242次追加，200万时8次，EPE多19%）；国债作为抵押品（无折扣时EPE +1.4%，巴塞尔4%折扣时−2.3%）；再使用与隔离。
* **3. CVA与DVA。** 推导公式；CVA 40.4万美元（每年约为名义本金的5个基点），逐月分解；双边CVA 38.1万，DVA 15.4万，银行自身利差扩大到六倍时升到72.9万；CVA对交易对手利差（一半时21.2万，四倍时121.6万），CS01每基点1,957美元与460万美元的CDS对冲；增量CVA（一笔5年期收固定：单独6.0万，加入后−1.2万）；蒙特卡罗误差（250条路径2.7万，16,000条3,400）与模型误差（重新拟合后不同均值回归下40.3–41.1万）；巴塞尔委员会的三分之二。
* **4. 错向风险。** 条件公式；高斯连接函数（ρ = 0时CVA 36.6万，0.9时66.8万，−0.6时19.5万）；Hull和White的风险率模型λ = exp(a(t) + bV)，重新拟合到CDS曲线（b = 0.1：40.4万 → 75.3万）；α部分是它的价格（ρ = 0.3时×1.25）；一般与特定错向风险。
* **5. FVA、KVA与MVA。** 为一个无抵押客户融资，并与有抵押的交易商对冲；Burgard–Kjaer、Hull–White的FVA之争、摩根大通的15亿美元（2014年1月）；推导KVA（10%门槛收益率下51.1万）；全部调整（CVA、DVA、FCA、FBA、KVA、MVA）；不对称融资（80/80个基点时FVA 2.2万，80/20时14.0万，150/20时29.7万）。
* **6. 用AAD求敏感度。** 扰动对一次反向扫描；对一个违约区间手算计算记录；14个敏感度与扰动一致（本次CPU运行中为1.1秒对1.1秒）；**实验**：`cva_torch`。
* **7. 学习未来价值的网络。** 把V(t, x)看作条件期望；只用实现的贴现现金流训练；在新路径上CVA为42.3万对重设近似参考值41.4万（+2%），付息处的台阶被磨平；与逐日回归比较（三次多项式：RMSE 0.19对网络的1.04；CVA +1.8%），以及50个因子下三次多项式需要的23,426项。
* **8. 初始保证金。** 规则（2016–2022）；把SIMM推导为正态VaR；关键利率DV01与类SIMM初始保证金340万美元；监管表格法（不计净额600万美元）；初始保证金曲线；初始保证金对CVA与MVA（第99百分位时CVA从1.5万降到0.02万，而MVA为8.9万）。
* **9. 保证金的顺周期性。** 由每日收益率得到的10年期国债10天99%保证金：EWMA在2020年3月从每100美元2.88升到6.59；循环；EMIR的工具（单独跳升×2.3，25%缓冲时×2.1，10年下限时×1.6，代价是平静时期多40%保证金）；Kupiec回测（2,238天中28次例外，1.25%，p = 0.25；集中在2019和2020年）。
* **10. 中央清算。** 更替；Duffie和Zhu（K = 2、4、8时，清算K类中的一类只有在交易商多于7、15、31家时才有帮助）；瀑布；模拟清算所（大约每八个有违约的年份中有一个动用存活会员的基金）；雷曼在LCH（66,390笔互换，9万亿美元，约用掉三分之一保证金）与Aas在纳斯达克清算所（超出抵押品1.14亿欧元；清算所自有资本700万欧元；1.66亿欧元基金中的1.07亿）。
* **11. 2022年3月：伦敦金属交易所的镍市场。** 月度价格（IMF）；3月4、7、8日每吨2.89万、4.81万、10.14万美元；一个假设的10万吨空头的变动保证金（19亿美元，然后53亿）；暂停交易与取消交易；涨跌幅限制；高等法院（2023）与英国金融行为监管局920万英镑罚款（2025）。
* **12. 交易对手风险的资本。** 为互换推导SA-CCR；净额集（单独8.1、净额4.8、有保证金1.4，单位为百万美元EAD）；PFE乘数（价外一个附加值时0.61，下限5%）；巴塞尔基本法CVA资本（这个净额集约58万美元；名称很多时每个名称的资本只降到一半）；CVA资本与杠杆率。
* **13. 2021年3月：Archegos。** 总收益互换；抛售；按清算期限计的保证金（对日波动4%的股票，20%只覆盖约0.65天成交量；Paul, Weiss报告所说仅在瑞信就有2.5–10天）；抢先抛售（示意：损失20对40）；公开记录。
* **14. 第21条规则：XVA交易台。** 一张交易单（CVA、报告的DVA、FVA、KVA、MVA：客户约付105万美元）；交易台的夜间流程；`xva`模块；第21条规则；用本部分三个案例检验这条规则。
* **写给研究者：有限错向风险边界。** 运输LP固定1500条敞口路径及120个月度违约桶加存活桶的边际。在确定性贴现下，独立值0.40百万、最大值1.81百万、最小值0。边界仅针对这个有限问题，静态耦合不一定适应或可由经济模型实现。Sinkhorn点按实际KL绘制；规范化成本后的惩罚路径并不求解所有指定熵预算。第四章平坦强度Copula及全路径强度联系示例的违约或路径边际不同，数值落在区间内不能证明边界包含关系；比较前必须匹配边际及成本。两路径题的实际演算答案为1、2、0。
* **回顾、交易台问题与习题。** 十六行回顾；六个交易台问题；十二道习题（两道为资格考试水平），解答见下文。

## 交易台问题与解答

学习图将参数拟合简写：先由θ*最小化经验平方损失，再使用参数θ*对应的价值函数。习题5中恒定保证金风险期敞口公式适用于时滞窗口之后，即t ≥ m。

1. **为什么银行信用变差时DVA上升，这种利润是真的吗？** DVA是银行若先违约就不必偿还所欠款项的价值。信用变差使这种情况更可能，负债的价值下降，银行记录收益。会计准则（IFRS 13、ASC 820）要求这样做，但会计确认并不产生可自由支用的收入，实现、对冲及审慎资本处理取决于具体工具与适用规则（第3章）。
2. **与同一交易对手的两笔相互抵消的互换：有无净额结算时的敞口？** 有净额结算时为零：每条路径上价值都相互抵消。没有净额结算时是每笔互换正部之和：清算人会收取违约方赢的那笔，而把另一笔留给银行作为无担保债权（第1章）。
3. **交易对手每天以现金缴纳保证金、门槛为零。你怎么还会亏损？** 通过它最后一次付款与平仓之间的变动（风险保证金期，第2章），通过在已经变动的市场中重建对冲的成本，通过争议与转移门槛，以及通过与交易对手或敞口一起下跌的抵押品（错向，第2章与第4章）。
4. **为什么保证金恰恰在现金稀缺时上升？** 保证金模型随近期波动率缩放，而危机中波动率上升；所有有保证金的头寸同时被追加，现金靠卖出资产筹集，卖出又推高波动率（第9章）。缓冲、下限和更长的回看期能抑制这个循环，代价是平静时期更多的保证金。
5. **在max(V, 0)处或在支付的跳跃处，反向扫描会出什么错？** 在折点处它返回一侧的导数，几乎处处正确，平均而言无害。在跳跃处，逐路径导数几乎处处为零，完全遗漏了跳跃的贡献。可以平滑支付（用一个很窄的sigmoid代替阶跃），或用似然比或条件期望方法估计这些项（第6章）。
6. **客户在单一股票互换上缴纳20%保证金。你最想知道什么？** 它的头寸相对该股日成交量的大小，而且要合计所有交易商：这决定清算需要多久，从而决定保证金（第13章）。这很难看到，因为互换让股票留在交易商名下，每个交易商只看到自己那一份。

## 习题与解答

习题11中的M计全部运输列，包括存活状态。正文示例有120个违约桶，另有1个存活列。折点处逐路径求导须满足正则条件并能交换求导与期望，原子概率及不连续支付须另行处理。

1. **远期的敞口。** V(t) = σW_t服从均值0、方差σ²t的正态分布，所以EE(t) = E[max(σW_t, 0)] = σ√t E[max(Z, 0)] = σ√t φ(0) = σ√(t/2π)。其第95百分位为1.645 σ√t，由于为正，PFE₉₅ = 1.645 σ√t。
2. **互换的驼峰。** f(t) = √t (T − t)，f′(t) = (T − t)/(2√t) − √t = 0时T − t = 2t，所以t = T/3：10年期互换为3.3年。第1章的曲线在月度网格上于第4年附近达到峰值，比T/3晚，因为票息按年支付，剩余付款是分级下降而不是平滑下降。
3. **作为利差的CVA。** EE恒定、风险率λ和利率r为常数时，违约密度为λe^{−λt}，所以CVA = (1 − R) EE ∫₀ᵀ e^{−rt} λ e^{−λt} dt = (1 − R) λ EE ∫₀ᵀ e^{−(r+λ)t} dt。除以名义本金N上的风险年金∫₀ᵀ e^{−(r+λ)t} dt，得到持续利差(1 − R) λ EE/N：把信用三角用在敞口上。
4. **双边CVA。** 只有当银行自己尚未先违约时，交易对手在t时刻的违约才会让银行亏损。违约相互独立时，P(τ_c ∈ dt, τ_b > t) = Q_b(t)(−dQ_c(t))，所以CVA_bil = (1 − R) ∫ EE(t) P(0, t) Q_b(t)(−dQ_c(t))。由于处处Q_b(t) ≤ 1，它不大于单边CVA，只要银行可能违约就更小。
5. **有抵押的敞口。** 零门槛、风险保证金期为m时，t时刻的抵押品为V(t − m)，敞口为max(σ(W_t − W_{t−m}), 0)。无论t为何，增量都服从方差为σ²m的正态分布，所以EE = σ√(m/2π)，不随时间变化：取决于风险保证金期的平方根，而不是交易存续时间。
6. **手算SA-CCR附加值。** 监管久期为(e^{−0.05·0} − e^{−0.05·10})/0.05 = (1 − 0.607)/0.05 = 7.87，有效名义本金为100 × 7.87 = 787（一笔交易，在五年以上区间，期限因子为1）。附加值为0.5% × 787 = 393万美元；重置成本为零、乘数为1时，EAD = 1.4 × 3.93 = 550万美元：即第12章的"单独的10年期付固定"。
7. **Cover 2。** 在本题指定覆盖二要求下，资源覆盖两个最大合计压力敞口超出成员保证金的损失：30 + 25 = 55。若第三大会员也违约，先用它自己的保证金和基金份额，然后是清算所自有资本之后剩余的共同基金；再往后是按规则设上限的对存活会员的追加摊款，然后是诸如削减变动保证金收益之类的恢复工具。由存活会员承担。
8. **AAD的成本。** 反向模式把梯度作为向量–雅可比积来计算，对记录下的运算向后扫描一次；每个运算的伴随量只花费该运算本身的一个小常数倍，所以全部n个敏感度只花费几次估值，与n无关，而单侧扰动需要n + 1次估值。代价是内存：前向过程的每个中间值（每条路径、每个日期、每个运算）都要为反向过程保存，或从检查点重新计算。
9. **何时清算一种产品有帮助。** 在双边情形下，交易商对N − 1个交易对手中每一个的敞口对K个方差为σ²的独立类别做净额，等于σ√K φ，φ = 1/√(2π)，总量为(N − 1)σ√K φ。清算一类后，双边部分剩下(N − 1)σ√(K − 1)φ，并在清算所增加σ√(N − 1)φ，那一类在那里对全部N − 1个交易对手做净额。清算有帮助当且仅当(N − 1)(√K − √(K − 1)) > √(N − 1)，即√(N − 1) > 1/(√K − √(K − 1)) = √K + √(K − 1)，或N > 1 + (√K + √(K − 1))²：K = 2、4、8时分别为7、15、31家交易商。
10. **手算KVA。** KVA = h ∫₀ᵀ K₀(1 − t/T) dt = h K₀ [t − t²/(2T)]₀ᵀ = h K₀ T/2：门槛收益率乘以平均资本再乘以存续期。
11. **（资格考试）运输问题。** c_ij = (1 − R)D(t_j)V_i(t_j)⁺（生存时c = 0），CVA(p) = Σc_ij p_ij对p是线性的，可行集{p ≥ 0: Σ_j p_ij = 1/N, Σ_i p_ij = q_j}是运输多面体。线性函数在顶点处取最大和最小值，而N × M运输多面体的顶点至多有N + M − 1个正格子（其支撑是二部图中的森林）。两条路径（0和10，各½）、一个日期q = 0.2：独立给出0.2 × 5 = 1；最坏把全部0.2放在第二条路径上（因0.2 ≤ ½可行）：2；最好放在第一条上：0。
12. **（资格考试）熵解。** 设θ > 0且给定边际严格为正。 拉格朗日函数的一阶条件为c_ij − (1/θ)(log(p_ij/p⊥_ij) + 1) + α_i + β_j = 0，所以p_ij = a_i b_j p⊥_ij e^{θc_ij}。Sinkhorn交替进行a ← (1/N)/(Kb)、b ← q/(Kᵀa)，K = p⊥e^{θc}；每一步都是向一组边际的Bregman投影，迭代收敛到唯一解。

## 数据与复现

产品形状比较包含利率与外汇敞口的加权混合及平坦正期权价值代理，并非联合模拟的跨币种互换估值。CVA年化利差以一亿美元参考本金换算，而组合总名义本金为两亿美元。CDS强度自举使用平坦4%贴现假设，与指定日期的敞口曲线另行处理。

* FRED：DGS10（日度，2006–2025）、PNICKUSDM（IMF镍价，月度）；美联储拟合的零息曲线（Gürkaynak、Sack和Wright），截至2025年12月31日；冻结并校验哈希。
* 引用而非计算的公开数字：各银行在Archegos上的损失；LCH与纳斯达克清算所的违约（国际清算银行）；伦敦金属交易所的日价格、被取消的交易与金融行为监管局的罚款；摩根大通的FVA费用；Paul, Weiss报告的清算估计。
* 屏幕上标注为示意的输入：交易对手与银行的CDS曲线（80–170与40–85个基点）、融资利差、类SIMM风险权重、资本替代指标与门槛收益率、清算所的会员与压力情景、假设的镍头寸、类Archegos股票与抛售模型。
* 本部分不打开任何样本外数据；累计试验计数器保持317，全局23562。

## 写给研究者

* **定理。** 格拉斯曼与Linan Yang（2018），*Management Science* 64(12)；Cuturi（2013）与Sinkhorn（1964）论熵运输；Hull与White（2012）；Brigo、Morini与Pallavicini（2013）的建模视角。
* **简化。** 线性规划用1,500条路径的子样本；月度区间；耦合可以看整条路径（不只是过去的敞口），所以最坏情形比非预期的版本更大。
* **开放问题。** 校准熵预算；尊重时间的耦合；取代α乘数。
