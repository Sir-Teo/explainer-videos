# Quant, Built — Part 26: Backtesting Without Fooling Yourself

Part 26 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act IV, Return Premia (23–29). Part 25 counted the factor zoo's
tries; this part builds the machine that simulates a strategy's history, and every check that keeps the simulation
honest. It covers:

* the biases, each planted on purpose and measured: look-ahead (a same-bar signal; GDP as published against GDP as
  revised), survivorship (today's ticker file; Brown–Goetzmann–Ibbotson–Ross; Shumway's delisting returns), and
  selection (the best of N, from extreme-value theory);
* an event-driven backtester (fills, latency, spread, impact, commissions, borrow, splits and dividends) against the
  vectorised one-liner, on a real strategy;
* the Sharpe ratio's standard error (Lo; Mertens), its annualisation under autocorrelation, and the minimum backtest
  length;
* the trial counter so far, the hurdle it implies, the deflated Sharpe ratio and an effective number of trials;
* the probability of backtest overfitting by CSCV; purged and embargoed cross-validation; walk-forward;
* White's reality check, Hansen's SPA and Romano–Wolf's step-down, on 10,000 technical rules re-run after Sullivan,
  Timmermann and White, in two eras;
* e-value monitoring of 207 published predictors after publication, with e-BH;
* planted alpha in a simulated market; how a strategy gets capital, and a capital ramp gated by a monitor;
* the best of the 10,000 rules registered (10,000 trials) and opened on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's new
[`backtest`](../../../explainer/quant/house/backtest.py) module). Data: Kenneth French's daily and monthly factors,
the Federal Reserve Bank of Philadelphia's Real-Time Data Set, EDGAR (frames, full-text search, the SEC's ticker
file), Yahoo Finance daily bars with splits and dividends, Cboe's PutWrite index, and Open Source Asset Pricing
2024.10.

*An education in methods, not investment advice.*

## Chapters (about 67 minutes)

* **Ten thousand rules** (3.3 min). The best of 10,000 rules on 1926–1986 (long above the 5-day average, short
  below): Sharpe 1.67 against the market's 0.42; 0.02 on 1987–2020, rank 3,281. "Your backtest has a Sharpe ratio of 3:
  list what could be wrong" as the part's map; the history strip (Cowles 1933 to Arnott–Harvey–Markowitz 2019); the
  plan; the House.
* **1. Look-ahead and point in time** (3.8). A planted one-day look-ahead in a 200-day moving-average rule
  (1990–2020): Sharpe 0.22 honest, 1.31 planted, 0.50 buy and hold; 8.8 with a 5-day average. Four ways look-ahead
  enters. 2008 Q4 GDP by vintage: −3.8% first (January 2009), −6.2%, −8.9% (July 2011), −8.4% (December 2020).
  216 quarters since 1966: mean revision 1.5 points, 7% changed sign, correlation 0.79. FRED's quarter-start date
  stamp merged "as of": a GDP timing rule's Sharpe 0.38 in real time, 0.43 naive.
* **2. Survivorship** (3.4). Today's ticker file holds 39% of 2012's public filers and 6% of the 977 that reported a
  bankruptcy in 2009–2020. Delisting returns (Shumway 1997; Shumway–Warther 1999). 5,000 no-skill managers, a −30%
  exit: survivors average +3.6% a year, all of them 0.0%; the volatile survivors look best (8.7%). Index membership,
  backfill, the strategy graveyard.
* **3. Selection: the best of many** (3.5). The best of N noise strategies, five years daily: 0.69, 1.12, 1.46, 1.73
  for N = 10 to 10,000. Φ(c)^N; Gumbel; the expected maximum; the formula against simulation; 10⁶ tries give above 2.
  Leinweber's butter in Bangladesh (R² 75%, then 99%). Where N comes from.
* **4. The event-driven backtester** (5.9). The loop: bars, corporate actions, fills, mark and borrow, the strategy's
  point-in-time view, orders after a latency. The vectorised line and its assumptions. EEM's one-day reversal,
  2010–2020: vectorised 0.43; engine at that close 0.45; next open −0.18; with a 1 bp half-spread −0.30; with impact,
  commission and borrow −0.49 (−11.7% a year). The edge is overnight (0.77) and the day loses (−0.28). Costs on
  \$1 million: \$131k spread, \$36k impact, \$159k commission, \$8k borrow; turnover 257 a year. AAPL's 4:1 split
  (−74% in prices as traded; momentum wrong for 10 days). SPY price 11.5% a year against 13.7% with dividends. Borrow,
  fills, capacity. The lab.
* **5. The Sharpe ratio's error** (3.6). A true Sharpe of 0.5 over five years: estimates ±0.46, 13% negative. The
  delta method; Lo (2002); Mertens (2002). Years to two standard errors ≈ 4/SR². The market 1926–2020: 0.44 ± 0.10;
  Cboe PutWrite 2007–2020: 0.45 ± 0.27 → 0.30 (skew −1.6, kurtosis 9.6). Smoothed returns: √12 gives 1.63 for a true
  1.0, Lo's η gives 1.05 (56% overstated).
* **6. The trial counter and the hurdle** (3.1). Registration (code hash, parameters, trials); 346 configurations
  before this part, by part; the hurdle for ten years of daily data (0.93 at 346, 1.22 at 10,346); the minimum backtest
  length (45 tries in five years at Sharpe 1); why the count is both an upper and a lower bound.
* **7. Technical rules that weren't** (3.6). The four families; 10,000 rules from a grid of 32,730; in sample 757 beat
  buy and hold, out of sample 16; the eras' Sharpe ratios correlate 0.16; each family's best rule (all short-horizon);
  the index's first-order autocorrelation by decade (0.29 in the 1970s, negative after 2000): stale prices (Fisher
  1966; Lo–MacKinlay 1990).
* **8. The deflated Sharpe ratio** (3.5). PSR and DSR derived; N_eff from the participation ratio (176 and 155 of
  10,000); √V = 0.19 a year. 1926–86 winner: DSR 1.00. 1987–2020 winner (a 200/250-day crossover, Sharpe 0.56,
  PSR(0) 0.9994): DSR 0.35 for N = 10,000, 0.76 for N_eff; it would pass only if chosen from about a dozen.
* **9. The probability of backtest overfitting** (3.1). CSCV with 16 blocks (12,870 splits); the logit; PBO 0.00 in
  1926–86 and 0.43 in 1987–2020; the in-sample winner's Sharpe 0.78 → 0.04 out of sample, losses in 42% of splits;
  what it can and cannot see.
* **10. Purged cross-validation and walk-forward** (3.4). Overlapping labels; a 25-nearest-neighbour forecaster of the
  next 20 days (1963–2020): shuffled 5-fold R² +2.9% (hit 55%), blocked −5.6%, purged and embargoed −5.5%,
  walk-forward −5.3%. Purging, embargo, walk-forward; when purging matters.
* **11. Reality checks** (3.5). The null of no edge anywhere; the stationary bootstrap; White's statistic; 1926–86:
  p = 0, SPA p = 0, Romano–Wolf 153 rules (107 channel breakouts); 1987–2020: best t 3.3 (nominal p 0.0005), 214 rules
  with t > 1.96, RC p = 0.056, SPA p = 0.47, Romano–Wolf none.
* **12. Monitoring live strategies with e-values** (3.1). Peeking; the betting monitor (shortfall scaled at four
  standard deviations, a mixture of six constant bets, threshold 20). Dividend seasonality (2013, t = 14.6) flagged in
  August 2018; the predicted dividend yield (1979) never doubted. 207 predictors: 68 flagged as not as good as their
  backtests, 40 by e-BH at 10%; only 7 as not even half; median flag eight years after publication.
* **13. Planted alpha** (2.5). 1,000 strategies, five years, ten planted. Planted Sharpe 1: t > 1.96 finds 5.9 real
  and 19.8 false; Bonferroni 0.4 and 0.0; Romano–Wolf 0.5 and 0.1; DSR of the best passes in 7.5%. Planted Sharpe 2:
  the strict tests find about 7 with no false ones; DSR passes in 95%.
* **14. How a strategy gets capital** (3.1). Idea, research review, incubation, ramp, full allocation, monitoring and
  retirement (Lopez de Prado's meta-strategy paradigm; Arnott–Harvey–Markowitz). A ramp gated by a monitor: the
  overfitted strategy is stopped in 62% of five-year careers (median month 43), the real one in 4%; tested against
  only half the backtest, 10%.
* **15. The best rule, registered and opened** (1.9). Registered with 10,000 trials: the counter goes from 346 to
  10,346. 2021–2025: Sharpe −0.27 ± 0.45 against the market's 0.61. Three eras: 1.67, 0.02, −0.27.
* **16. Rule 26: the backtest protocol** (3.0). The first sheet; a protocol after Arnott, Harvey and Markowitz, with
  execution added; the lab (`expected_max_sr`, `deflated_sharpe`, `psr`); the module; the rule; four cases.
* **For the researcher: inference on the winner** (5.9). X ~ N(μ, Σ), winner ĵ = argmax X; the winner's curse and
  the naive interval's undercoverage (0.975⁵⁰ − 0.025⁵⁰ ≈ 28% for 50 independent noise rules). Conditioning: Z =
  X − Σ_{·j}X_j/Σ_jj is independent of X_j, {ĵ = j} = {L(Z) ≤ X_j ≤ U(Z)}, so X_j given winning is a truncated normal;
  inverting it gives a median-unbiased estimate and an interval with exact conditional coverage (Andrews, Kitagawa
  and McCloskey 2024); the hybrid adds a β = 0.5% projection interval. Simulated (50 estimates, correlation 0.5,
  4,000 draws a world): with all means zero, naive covers 69% with median bias +1.58 s.e., conditional 95.6% and
  hybrid 95.8% (median lengths 10.7 and 5.5 against naive 3.9 and projection 6.3); one clear winner: naive 94%;
  means spread 0 to 2: naive 77%, conditional and hybrid 95.5–95.6%. The 10,000 rules: chosen on 1926–86, MA 1/5
  (band 0%) at 1.67 led by 6.9 s.e., so conditioning changes nothing ([1.43, 1.92]), and it earned 0.02 on
  1987–2020: the market changed (index autocorrelation faded), not selection. Chosen on 1987–2003, filter 0.5% at
  1.07 beat its closest rival by 0.06 s.e. with 42 rules within two s.e.: conditional estimate −1.73 with interval
  [−13.5, 1.23], hybrid −0.08 with [−0.10, 1.25]; on 2004–20 it earned −0.40 ± 0.48. Three open problems; pause:
  0.98 against 1.0 is a near tie, so the conditional interval is very wide; 0.2 against 1.0 is a clear win, so it is
  close to the naive one.
* **Recap, desk questions, problems** (3.9). Twelve problems (two at qualifying-exam level), solutions below.

## Hands-on

* **Lab** (the House's own code on screen): `Backtester.run` (ch. 4), `pit.register` (ch. 6),
  `expected_max_sr`, `deflated_sharpe`, `psr` (ch. 16).
* **Computed:** a planted look-ahead; GDP vintages; survivorship in EDGAR; the best of N; four backtests of one
  strategy; Sharpe standard errors; 10,000 rules in two eras with DSR, PBO, RC, SPA and Romano–Wolf; four validation
  schemes; 207 e-value monitors; planted alpha; capital ramps; the best rule opened.
* **Live constructions:** the best-of-N distribution sliding right; the event loop; the race of five equity curves;
  the CSCV blocks; the stationary bootstrap's blocks; purge and embargo; walk-forward; a monitor crossing 20; the
  trial counter jumping.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Lopez de Prado, *Advances in Financial Machine Learning* | 7 (purged CV), 8–9 (feature importance and tuning, as context), 11–14 (the dangers of backtesting, backtesting through CV, synthetic data, backtest statistics) | ch. 4, 8–10, 13 |
| Isichenko, *Quantitative Portfolio Management* | 7 (simulation: the backtest, costs, look-ahead, survivorship) | ch. 1, 2, 4 |
| Bailey and Lopez de Prado, *Machine Learning for Asset Managers* | 8 (testing set overfitting) | ch. 6, 8 |

## Papers, chapter by chapter

* Hook: Cowles (1933); Brock, Lakonishok and LeBaron (1992); Sullivan, Timmermann and White (1999).
* ch. 1: Croushore and Stark (2001) on the real-time data set.
* ch. 2: Brown, Goetzmann, Ibbotson and Ross (1992); Shumway (1997); Shumway and Warther (1999).
* ch. 3: Bailey and Lopez de Prado (2014); Leinweber (2007).
* ch. 5: Lo (2002); Mertens (2002); Getmansky, Lo and Makarov (2004); Ledoit and Wolf (2008).
* ch. 6: Bailey, Borwein, Lopez de Prado and Zhu (2014); Harvey and Liu (2015).
* ch. 7: Alexander (1961); Fama and Blume (1966); Fisher (1966); Lo and MacKinlay (1990); Brock, Lakonishok and LeBaron
  (1992); Sullivan, Timmermann and White (1999); Lo, Mamaysky and Wang (2000).
* ch. 8: Bailey and Lopez de Prado (2012, 2014).
* ch. 9: Bailey, Borwein, Lopez de Prado and Zhu (2017).
* ch. 10: Lopez de Prado (2018).
* ch. 11: Politis and Romano (1994); White (2000); Hansen (2005); Romano and Wolf (2005).
* ch. 12: Ville (1939); Wang and Ramdas (2022); Grünwald, de Heide and Koolen (2024).
* ch. 14: Lopez de Prado (2018), ch. 1; Arnott, Harvey and Markowitz (2019).

## Build it

```bash
python -m videos.quant.quant26.compute                          # every item; rules/dsr/pbo/rc share a 10,000-rule matrix
EXPLAINER_TTS=silent python tools/qa_scene.py quant26 Engine     # one chapter, silent, with a contact sheet
python tools/make.py quant26 --cpu-voice -q m                   # English and Chinese, narrated by Kokoro on the CPU
```

## Desk questions, with solutions

1. **A backtest has a Sharpe ratio of 3. What could be wrong?** Look-ahead: a same-bar signal, data stamped by period
   rather than release, revised data, full-sample normalisation. Survivorship: a universe from today's list, missing
   delisting returns. Selection: the best of many configurations. Execution: fills at the close it was computed from,
   no latency, no spread, impact or borrow. Corporate actions mishandled. A sample too short or too calm (a Sharpe
   estimate over three years is uncertain by about ±0.6). Leaky validation. A regime that ended. First rerun it in the
   event-driven engine at the next open with costs; then ask for the trial count and compute the deflated Sharpe ratio
   (ch. 1–8).
2. **400 settings of one idea, ten years daily, best Sharpe 1.2. Better than noise?** For 400 independent zero-skill
   settings with V = 1/2520 per day the expected best is about 0.94 a year, so 1.2 is above it, but not by much.
   Settings of one idea are correlated (N_eff smaller, hurdle lower) and differ in exposure (V larger, hurdle higher);
   compute both from the settings' own returns, then the DSR with the best's skewness and kurtosis (ch. 3, 8).
3. **Three years of monthly returns, Sharpe 2.0, first-order autocorrelation 0.4. A fair range?** If only ρ₁ is
   non-zero, η(12) = 12/√(12 + 2·11·0.4) = 2.63 against √12 = 3.46, so the corrected annual figure is about
   2.0 × 2.63/3.46 ≈ 1.5. Its standard error over 36 months is about 0.6, so roughly 0.3 to 2.7. Positive
   autocorrelation in a fund's returns also suggests smoothed marks: ask how the book is valued (ch. 5).
4. **200 trades a year, 4 bp gross a trade, costs estimated at 3 bp. How sure must you be?** The net edge is 1 bp a
   trade, about 2% a year on the traded notional. A cost estimate a third too low (4 bp) leaves nothing; trade it small,
   measure realised costs and impact live, and size up only when the measured cost is clearly below 4 bp (ch. 4, 14).
5. **A default model with a three-year label, validated by five random folds of firm-years. The leak?** A firm's
   consecutive years share most of their label and nearly all their features, and random folds put them on both sides.
   Split by firm and by time; purge any training firm-year whose three-year label window overlaps the test period, and
   embargo after it (ch. 10).
6. **A monitor at 12, threshold 20. Lower the threshold to 10 and stop now?** No. Ville's guarantee holds for a
   threshold fixed in advance; choosing it after seeing the path is optional stopping on the threshold itself. Decide
   thresholds in advance (several may be pre-registered, with their error rates), or start a new monitor for a new claim
   from today's data (ch. 12).

## Problems, with solutions

1. **The Sharpe ratio's error.** SR = μ/σ, with ∂SR/∂μ = 1/σ and ∂SR/∂σ = −μ/σ². For normal returns Var μ̂ = σ²/T,
   Var σ̂ ≈ σ²/(2T) and the two estimates are independent, so Var SR̂ ≈ (1/σ²)(σ²/T) + (μ²/σ⁴)(σ²/(2T)) =
   (1 + SR²/2)/T.
2. **The best of N.** max Zᵢ ≤ c exactly when every Zᵢ ≤ c, so the CDF is Φ(c)^N. The median solves Φ(c) = 2^{−1/100}
   = 0.99309: c ≈ 2.46.
3. **The hurdle for 100 tries.** V = 1/1260 per day: E[max] ≈ √V[(1 − γ)Φ⁻¹(0.99) + γΦ⁻¹(1 − 1/(100e))] =
   (0.4228 × 2.326 + 0.5772 × 2.676)/√1260 = 0.0713 a day, × √252 = 1.13 a year.
4. **Minimum backtest length.** For N = 1,000: (0.4228 × 3.090 + 0.5772 × 3.377)² ≈ 10.6, divided by SR² = 1:
   about 10.6 years.
5. **A PSR with skew.** Denominator √(1 − (−1)(0.1) + (6 − 1)/4 × 0.01) = √1.1125 = 1.055; z = 0.1 × √59/1.055 =
   0.728; PSR(0) = Φ(0.728) ≈ 0.77.
6. **Lo's η.** η(12) = 12/√(12 + 2 × 11 × 0.3) = 12/√18.6 = 2.78, against √12 = 3.46: the usual rule overstates the
   annual Sharpe ratio by about 24%.
7. **CSCV's splits.** C(16, 8) = 12,870; a given block is in sample in C(15, 7) = 6,435 of them, exactly half.
8. **What purging costs.** An interior fold's label span runs from its first day to 20 days past its last. Purged: the
   20 training observations before it (their labels reach into it) and the 20 after it (they start inside its label
   span); embargoed: the next 20. About 60 observations, of 4,000 training ones.
9. **The stationary bootstrap's blocks.** Block lengths are geometric: mean 1/p = 10 days; P(L ≥ 20) = 0.9¹⁹ ≈ 0.135.
10. **Peeking.** By Ville's inequality the e-process monitor passes 20 with probability at most 5% over any horizon,
    however often it is read. Ten years of monthly one-sided 5% tests on the cumulative mean raise at least one false
    alarm in about 32% of simulated careers (24% if the first year is skipped), and the share tends to one as the
    horizon grows (the law of the iterated logarithm).
11. **(qual) The truncated normal.** Cov(Z, X_j) = Σ_{·j} − Σ_{·j}Σ_jj/Σ_jj = 0, and (Z, X_j) is jointly normal, so Z
    is independent of X_j. Write X_k = Z_k + (Σ_jk/Σ_jj)X_j; then X_j ≥ X_k ⇔ X_j(Σ_jj − Σ_jk)/Σ_jj ≥ Z_k. Hence
    L(Z) = max over k with Σ_jk < Σ_jj of Σ_jjZ_k/(Σ_jj − Σ_jk), U(Z) = min over k with Σ_jk > Σ_jj of the same
    expression, and rivals with Σ_jk = Σ_jj require Z_k ≤ 0, which does not involve X_j. Given Z the event {ĵ = j}
    is {L ≤ X_j ≤ U} (ties have probability zero), and X_j is independent of Z, so X_j | ĵ = j, Z is N(μ_j, Σ_jj)
    truncated to [L, U].
12. **(qual) The naive interval for a winner.** With all means 0 the interval X_ĵ ± 1.96 covers 0 iff
    −1.96 ≤ max_j X_j ≤ 1.96, whose probability is Pr(all ≤ 1.96) − Pr(all < −1.96) = Φ(1.96)^J − Φ(−1.96)^J:
    0.950 for J = 2 (the curse is mild), 0.282 for J = 50. The conditional interval has coverage 0.95 given every
    winner j and every Z, so averaging over them it is 0.95 for any J.

## For the researcher

* **The theorems.** Andrews, Kitagawa and McCloskey (2024), "Inference on winners," *QJE* 139(1): conditional,
  unconditional and hybrid inference after selection by argmax; Lee, Sun, Sun and Taylor (2016), *Annals of
  Statistics* 44, on exact post-selection inference by the same truncated-normal device; Bailey and López de Prado (2014) for the deflated Sharpe ratio.
* **Simplifications.** Sharpe ratios treated as normal with covariance ρ_jk/T (exact for small Sharpe ratios and iid
  returns; daily returns are neither exactly); the projection critical value by a Gaussian multiplier bootstrap that
  ignores serial dependence; the rivals' correlations estimated, not known.
* **Open problems.** Finite-sample accuracy under fat tails and changing volatility; conditioning on a sequential
  research path; selection and structural change together.

## Data and reproducibility

* Kenneth French: daily factors 1926-07 to 2025-12 (the sealed 2021–2025 market and T-bill returns read only in
  `envelope`), monthly three factors to 2020-12.
* Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists: ROUTPUT, monthly vintages 1965M11 to
  2020M12 (the parsed matrix is checksummed; the file's document properties are skipped because they do not parse).
* EDGAR: frames (dei:EntityPublicFloat, 2011–2020), full-text search for 8-K item 1.03 (from Part 20), and the SEC's
  `company_tickers.json` as first downloaded (November 2026), checksummed; matched by CIK.
* Yahoo Finance: daily bars with split and dividend events for EEM, SPY (2010–2020) and AAPL (2019-12 to 2020-12),
  frozen and checksummed. AAPL is un-adjusted before 31 August 2020 by the split ratio to give prices as traded.
* Cboe PUT index (2007–2020); Open Source Asset Pricing 2024.10 (from Part 3) for the monitors, research years only.
* Registered here: `stw_best_rule_part26` (10,000 trials); the counter rises from 346 to 10,346. The hold-out
  `kenfrench/rf_daily` is sealed here for the first time.
* Published figures quoted, not computed: Shumway's −30%; Leinweber's R²s; Lo's 65%; Bailey et al.'s 45 tries.
* Simulated or illustrative: the best-of-N distributions, the survivorship managers, the 5-year Sharpe sampling
  distribution, the smoothed returns, the planted market, the capital ramps, the rule families' price path.

---

# 量化金融，从零搭建 — 第26部分：不自欺的回测

本部分是第四幕“收益溢价”（第23–29部分）的第四部分。第25部分数清了因子动物园的尝试次数；本部分搭建模拟一个策略历史的机器，以及让模拟保持诚实的每一项检验。本部分讲：

* 各种偏差，每一种都故意植入并加以测量：前视偏差（同一根K线的信号；公布时的GDP与修订后的GDP）、幸存者偏差（今天的代码清单；Brown–Goetzmann–Ibbotson–Ross；Shumway的退市收益）与选择偏差（极值理论给出的N个中的最佳）；
* 一个事件驱动的回测器（成交、延迟、价差、冲击、佣金、借券、拆股与分红）对比向量化的一行代码，用在一个真实策略上；
* 夏普比率的标准误（Lo；Mertens）、自相关下的年化，以及最短回测长度；
* 目前为止的试验计数器、它所隐含的门槛、紧缩夏普比率与有效试验次数；
* 用CSCV计算的回测过拟合概率；清洗与禁运的交叉验证；滚动前推；
* White的现实检验、Hansen的SPA与Romano–Wolf的逐步下降，用于按Sullivan、Timmermann与White重新运行的10,000条技术规则，分两个时代；
* 对207个已发表预测变量在发表后的e值监控，以及e-BH；
* 在模拟市场中植入的alpha；一个策略如何获得资金，以及由监控把关的资金爬坡；
* 10,000条规则中最好的一条登记（10,000次试验）并在2021–2025年上打开。

*讲的是方法，不构成投资建议。*

## 章节（约67分钟）

* **一万条规则**（3.3分钟）。1926–1986年10,000条规则中最好的一条（收盘高于5日均线做多，低于做空）：夏普比率1.67，市场0.42；1987–2020年为0.02，排第3,281名。以“你的回测夏普比率为3：列出可能出错的地方”作为本部分的地图；历史条（1933年Cowles到2019年Arnott–Harvey–Markowitz）；计划；本系列公司。
* **1. 前视偏差与时点数据**（3.8）。在200日均线规则中植入一天的前视（1990–2020）：诚实0.22，植入1.31，买入持有0.50；5日均线为8.8。前视偏差进入的四种方式。2008年第四季度GDP的各个版本：首次−3.8%（2009年1月），−6.2%，−8.9%（2011年7月），−8.4%（2020年12月）。1966年以来216个季度：平均修订1.5个百分点，7%改变符号，相关系数0.79。FRED以季度首日为时间戳“截至”合并：GDP择时规则的夏普比率实时为0.38，朴素为0.43。
* **2. 幸存者偏差**（3.4）。今天的代码文件保留了2012年公开申报者的39%，以及2009–2020年报告破产的977家公司的6%。退市收益（Shumway 1997；Shumway–Warther 1999）。5,000名无技能的经理、−30%出局：幸存者平均每年+3.6%，全体为0.0%；高波动的幸存者看起来最好（8.7%）。指数成分、回填、策略墓地。
* **3. 选择：众多中的最佳**（3.5）。N个噪声策略中最好的一个（五年日度）：N从10到10,000为0.69、1.12、1.46、1.73。Φ(c)^N；Gumbel；期望最大值；公式对比模拟；10⁶次尝试给出2以上。Leinweber的孟加拉国黄油（R² 75%，然后99%）。N从何而来。
* **4. 事件驱动的回测器**（5.9）。循环：K线、公司行为、成交、估值与借券、策略的时点视图、延迟后的订单。向量化的一行及其假设。EEM一日反转，2010–2020：向量化0.43；引擎在该收盘成交0.45；次日开盘−0.18；加1个基点半价差−0.30；加冲击、佣金与借券−0.49（每年−11.7%）。优势在隔夜（0.77），日内亏损（−0.28）。100万美元的成本：价差13.1万、冲击3.6万、佣金15.9万、借券0.8万美元；换手每年257倍。AAPL的1拆4（按成交价格−74%；动量信号错10天）。SPY价格每年11.5%，含分红13.7%。借券、成交、容量。实验。
* **5. 夏普比率的误差**（3.6）。真实夏普0.5、五年数据：估计值±0.46，13%为负。delta方法；Lo（2002）；Mertens（2002）。达到两个标准误所需年数≈4/SR²。1926–2020年市场：0.44 ± 0.10；Cboe PutWrite 2007–2020：0.45 ± 0.27 → 0.30（偏度−1.6，峰度9.6）。平滑收益：真实1.0时√12给出1.63，Lo的η给出1.05（高估56%）。
* **6. 试验计数器与门槛**（3.1）。登记（代码哈希、参数、试验次数）；本部分之前按部分统计的346个配置；十年日度数据的门槛（346时0.93，10,346时1.22）；最短回测长度（五年、夏普1时45次尝试）；为什么计数既是上界又是下界。
* **7. 不灵的技术规则**（3.6）。四个家族；从32,730条的网格中抽取10,000条；样本内757条胜过买入持有，样本外16条；两个时代的夏普比率相关0.16；每个家族最好的规则（都是短周期）；指数日收益一阶自相关按十年（1970年代0.29，2000年后为负）：陈旧价格（Fisher 1966；Lo–MacKinlay 1990）。
* **8. 紧缩夏普比率**（3.5）。推导PSR与DSR；由参与比得到N_eff（10,000中的176与155）；√V = 每年0.19。1926–86年赢家：DSR 1.00。1987–2020年赢家（200/250日交叉，夏普0.56，PSR(0) 0.9994）：N = 10,000时DSR 0.35，N_eff时0.76；只有从大约十几次尝试中选出才能通过。
* **9. 回测过拟合概率**（3.1）。16块的CSCV（12,870种划分）；logit；1926–86年PBO为0.00，1987–2020年为0.43；样本内赢家的夏普0.78 → 样本外0.04，42%的划分中亏损；它能看到什么、看不到什么。
* **10. 清洗交叉验证与滚动前推**（3.4）。重叠标签；预测未来20天的25近邻预测器（1963–2020）：打乱的5折R² +2.9%（命中55%），分块−5.6%，清洗与禁运−5.5%，滚动前推−5.3%。清洗、禁运、滚动前推；何时清洗重要。
* **11. 现实检验**（3.5）。处处无优势的原假设；平稳自助法；White的统计量；1926–86：p = 0，SPA p = 0，Romano–Wolf 153条规则（107条通道突破）；1987–2020：最佳t 3.3（名义p 0.0005），214条规则t > 1.96，RC p = 0.056，SPA p = 0.47，Romano–Wolf 0条。
* **12. 用e值监控实盘策略**（3.1）。偷看；下注式监控（缺口按四个标准差缩放，六个固定下注的混合，门槛20）。股息季节性（2013年，t = 14.6）于2018年8月被标记；预测股息率（1979年）从未被怀疑。207个预测变量：68个被标记为不如其回测，按e-BH在10%下为40个；不到一半的只有7个；中位数在发表后八年标记。
* **13. 植入的alpha**（2.5）。1,000个策略、五年、植入十个。植入夏普1：t > 1.96找到5.9个真实与19.8个虚假；Bonferroni 0.4与0.0；Romano–Wolf 0.5与0.1；最佳者的DSR在7.5%的市场中通过。植入夏普2：严格检验找到约7个且没有虚假；DSR在95%中通过。
* **14. 一个策略如何获得资金**（3.1）。想法、研究评审、孵化、爬坡、满额配置、监控与退役（Lopez de Prado的元策略范式；Arnott–Harvey–Markowitz）。由监控把关的爬坡：过拟合的策略在62%的五年生涯中被停止（中位数第43个月），真实的为4%；若只检验回测的一半，为10%。
* **15. 最佳规则，登记并打开**（1.9）。以10,000次试验登记：计数器从346升到10,346。2021–2025：夏普−0.27 ± 0.45，市场0.61。三个时代：1.67、0.02、−0.27。
* **16. 第26条规则：回测规程**（3.0）。第一张表；仿Arnott、Harvey与Markowitz并加上执行的规程；实验（`expected_max_sr`、`deflated_sharpe`、`psr`）；模块；规则；四个案例。
* **写给研究者：对赢家的推断**（5.9）。X ~ N(μ, Σ)，赢家ĵ = argmax X；赢家的诅咒与朴素区间的覆盖不足（50条独立噪声规则时为0.975⁵⁰ − 0.025⁵⁰ ≈ 28%）。条件化：Z = X − Σ_{·j}X_j/Σ_jj与X_j独立，{ĵ = j} = {L(Z) ≤ X_j ≤ U(Z)}，所以给定胜出时X_j服从截断正态分布；反解它得到中位数无偏估计和条件覆盖率精确的区间（Andrews、Kitagawa与McCloskey 2024）；混合方法再加上β = 0.5%的投影区间。模拟（50个估计，相关0.5，每个世界4,000次抽样）：所有均值为零时，朴素区间覆盖69%、中位数偏差+1.58个标准误，条件区间95.6%，混合区间95.8%（中位长度10.7和5.5，朴素3.9，投影6.3）；一个明显赢家：朴素94%；均值分布在0到2：朴素77%，条件与混合95.5–95.6%。一万条规则：在1926–86年选出的MA 1/5（带宽0%）为1.67，领先6.9个标准误，条件化什么也不改变（[1.43, 1.92]），它在1987–2020年赚到0.02：是市场变了（指数自相关消退），而不是选择。在1987–2003年选出的0.5%过滤规则为1.07，只以0.06个标准误胜过最接近的对手，两个标准误内有42条规则：条件估计−1.73、区间[−13.5, 1.23]，混合估计−0.08、区间[−0.10, 1.25]；它在2004–20年赚到−0.40 ± 0.48。三个开放问题；暂停题：0.98对1.0几乎是平局，所以条件区间很宽；0.2对1.0是明显胜出，所以它接近朴素区间。
* **回顾、交易台问题与习题**（3.9）。十二道习题（两道为资格考试难度），解答见下文。

## 交易台问题与解答

1. **回测夏普比率为3，可能哪里错了？** 前视：同一根K线的信号、按期间而不是发布时间标记的数据、修订后的数据、用全样本做标准化。幸存者：用今天的清单构成的样本、缺失的退市收益。选择：众多配置中的最佳。执行：在计算信号的那个收盘价成交、没有延迟、没有价差、冲击或借券。公司行为处理错误。样本太短或太平静（三年的夏普估计不确定性约为±0.6）。泄漏的验证。已经结束的市场状态。先在事件驱动引擎中以次日开盘加成本重跑；再询问试验次数并计算紧缩夏普比率（第1–8章）。
2. **一个想法的400组参数、十年日度、最佳夏普1.2，比噪声好吗？** 对400个独立的零技能参数、每日V = 1/2520，期望最佳约为每年0.94，所以1.2高于它，但不多。同一想法的参数彼此相关（N_eff更小，门槛更低），敞口不同（V更大，门槛更高）；用这些参数自己的收益算出两者，再用最佳者的偏度和峰度计算DSR（第3、8章）。
3. **三年月度收益、夏普2.0、一阶自相关0.4，合理区间？** 若只有ρ₁非零，η(12) = 12/√(12 + 2·11·0.4) = 2.63，而√12 = 3.46，所以修正后的年化值约为2.0 × 2.63/3.46 ≈ 1.5。36个月的标准误约0.6，所以大约0.3到2.7。基金收益的正自相关也提示估值被平滑：问清账簿如何估值（第5章）。
4. **每年200笔交易、每笔毛利4个基点、成本估计3个基点，需要多有把握？** 每笔净优势1个基点，约为交易名义的每年2%。成本估计低估三分之一（4个基点）就什么也不剩；小规模交易，实时测量成本与冲击，只有当测得成本明显低于4个基点时才加大规模（第4、14章）。
5. **三年标签的违约模型，用公司年的五个随机折验证，泄漏在哪？** 同一公司的相邻年份共享大部分标签和几乎全部特征，随机折把它们放在两边。按公司和时间划分；清洗那些三年标签窗口与测试期重叠的训练公司年，并在其后禁运（第10章）。
6. **监控值12、门槛20，把门槛降到10现在就停？** 不行。Ville的保证只对事先固定的门槛成立；看到路径后再选门槛，就是对门槛本身的可选停止。事先决定门槛（可以事先登记几个门槛及其错误率），或从今天的数据开始为一个新主张启动新的监控（第12章）。

## 习题与解答

1. **夏普比率的误差。** SR = μ/σ，∂SR/∂μ = 1/σ，∂SR/∂σ = −μ/σ²。正态收益下Var μ̂ = σ²/T，Var σ̂ ≈ σ²/(2T)，且两个估计独立，所以Var SR̂ ≈ (1/σ²)(σ²/T) + (μ²/σ⁴)(σ²/(2T)) = (1 + SR²/2)/T。
2. **N个中的最大。** 当且仅当每个Zᵢ ≤ c时max Zᵢ ≤ c，所以分布函数为Φ(c)^N。中位数满足Φ(c) = 2^{−1/100} = 0.99309：c ≈ 2.46。
3. **100次尝试的门槛。** 每日V = 1/1260：E[max] ≈ √V[(1 − γ)Φ⁻¹(0.99) + γΦ⁻¹(1 − 1/(100e))] = (0.4228 × 2.326 + 0.5772 × 2.676)/√1260 = 每日0.0713，× √252 = 每年1.13。
4. **最短回测长度。** N = 1,000：(0.4228 × 3.090 + 0.5772 × 3.377)² ≈ 10.6，除以SR² = 1：约10.6年。
5. **含偏度的PSR。** 分母√(1 − (−1)(0.1) + (6 − 1)/4 × 0.01) = √1.1125 = 1.055；z = 0.1 × √59/1.055 = 0.728；PSR(0) = Φ(0.728) ≈ 0.77。
6. **Lo的η。** η(12) = 12/√(12 + 2 × 11 × 0.3) = 12/√18.6 = 2.78，而√12 = 3.46：通常的规则把年化夏普比率高估约24%。
7. **CSCV的划分。** C(16, 8) = 12,870；某一块在其中C(15, 7) = 6,435种中为样本内，恰好一半。
8. **清洗的代价。** 一个内部折的标签区间从其第一天到最后一天之后20天。被清洗的：它之前的20个训练观测（其标签伸入测试折）和之后的20个（它们开始于测试折的标签区间内）；被禁运的：再之后的20个。约60个观测，占4,000个训练观测中的一小部分。
9. **平稳自助法的块。** 块长服从几何分布：均值1/p = 10天；P(L ≥ 20) = 0.9¹⁹ ≈ 0.135。
10. **偷看。** 由Ville不等式，e过程监控在任何期限内越过20的概率至多5%，无论读取多频繁。十年里每月做一次单侧5%检验，在约32%的模拟生涯中至少出现一次误报（若跳过第一年为24%），并且随期限增长趋于一（重对数律）。
11. **（资格考试）截断正态分布。** Cov(Z, X_j) = Σ_{·j} − Σ_{·j}Σ_jj/Σ_jj = 0，且(Z, X_j)联合正态，所以Z与X_j独立。写X_k = Z_k + (Σ_jk/Σ_jj)X_j；则X_j ≥ X_k ⇔ X_j(Σ_jj − Σ_jk)/Σ_jj ≥ Z_k。因此L(Z) = 对Σ_jk < Σ_jj的k取Σ_jjZ_k/(Σ_jj − Σ_jk)的最大值，U(Z) = 对Σ_jk > Σ_jj的k取同一表达式的最小值；Σ_jk = Σ_jj的对手要求Z_k ≤ 0，与X_j无关。给定Z，事件{ĵ = j}就是{L ≤ X_j ≤ U}（平局概率为零），而X_j与Z独立，所以X_j | ĵ = j, Z服从截断到[L, U]的N(μ_j, Σ_jj)。
12. **（资格考试）赢家的朴素区间。** 所有均值为0时，区间X_ĵ ± 1.96覆盖0当且仅当−1.96 ≤ max_j X_j ≤ 1.96，其概率为Pr(全部 ≤ 1.96) − Pr(全部 < −1.96) = Φ(1.96)^J − Φ(−1.96)^J：J = 2时为0.950（诅咒很轻），J = 50时为0.282。条件区间在每个赢家j和每个Z下的覆盖率都是0.95，所以对它们取平均后，任何J下都是0.95。

## 数据与复现

* Kenneth French：1926-07到2025-12的日度因子（封存的2021–2025年市场与国库券收益只在`envelope`中读取），到2020-12的月度三因子。
* 费城联储宏观经济学家实时数据集：ROUTPUT，1965M11到2020M12的月度版本（解析后的矩阵经校验；文件的文档属性无法解析，故跳过）。
* EDGAR：frames（dei:EntityPublicFloat，2011–2020）、8-K第1.03项的全文检索（来自第20部分），以及首次下载（2026年11月）的SEC `company_tickers.json`，经校验；按CIK匹配。
* 雅虎财经：EEM、SPY（2010–2020）与AAPL（2019-12到2020-12）带拆股与分红事件的日K线，冻结并校验。AAPL在2020年8月31日之前按拆股比例还原为成交价格。
* Cboe PUT指数（2007–2020）；开源资产定价2024.10（来自第3部分），监控只用研究年份。
* 本部分登记：`stw_best_rule_part26`（10,000次试验）；计数器从346升到10,346。封存数据`kenfrench/rf_daily`在此首次封存。
* 引用而非计算的已发表数字：Shumway的−30%；Leinweber的R²；Lo的65%；Bailey等人的45次尝试。
* 模拟或示意：N个中最佳的分布、幸存者经理、五年夏普的抽样分布、平滑收益、植入市场、资金爬坡、规则家族的价格路径。

## 写给研究者

* **定理。** Andrews、Kitagawa与McCloskey（2024），《Inference on winners》，*QJE* 139(1)：按argmax选择之后的条件、无条件与混合推断；Lee、Sun、Sun与Taylor（2016），*Annals of Statistics* 44，用同样的截断正态方法做精确的选择后推断；Bailey与López de Prado（2014）的紧缩夏普比率。
* **简化。** 把夏普比率当作协方差为ρ_jk/T的正态估计（对小夏普比率和独立同分布收益是准确的；日收益两者都不完全满足）；投影临界值用忽略序列相关的高斯乘子自助法得到；对手之间的相关是估计的，而非已知。
* **开放问题。** 厚尾和波动率变化下的有限样本精度；以序贯的研究路径为条件；同时处理选择与结构变化。
