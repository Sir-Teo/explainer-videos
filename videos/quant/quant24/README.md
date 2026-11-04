# Quant, Built — Part 24: Factors

Part 24 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act IV, Return Premia (23–29). Part 23 built the theory of
expected returns; this part meets the handful of portfolios that, for half a century, have explained most of what
stocks earn, and opens the Track Record: the first strategies scored on the sealed years 2021–2025. It covers:

* how a factor model is tested: Gibbons–Ross–Shanken and its Sharpe-ratio geometry, Fama–MacBeth with Shanken's
  correction, on the 25 size and book-to-market portfolios (CAPM, three factors, Carhart, five factors);
* size and value: the anomalies (Basu, Banz, Rosenberg), Fama and French's 2 x 3 construction, their history since
  1926, their decay after publication, and the January effect;
* momentum: Jegadeesh–Titman deciles, the factor, the three horizons, time-series momentum across asset classes and its
  smile;
* momentum crashes: 1932 and 2009, Daniel and Moskowitz's bear-market betas, the short call on a rebound, and
  Barroso and Santa-Clara's volatility scaling;
* profitability and investment from the dividend discount model; five factors; value made redundant; the q-factors;
* low risk: betting against beta, volatility-sorted portfolios, and the critique of their construction;
* value and momentum everywhere; carry everywhere; quality minus junk;
* value's lost decade, measured: the drawdown, the value spread, revaluation, intangibles, and HML's details;
* green returns: expected against realised (Pástor, Stambaugh and Taylor), the carbon premium, rating disagreement;
* factor timing (the value spread; Haddad, Kozak and Santosh) and factor momentum (Ehsani and Linnainmaa);
* China's factors (Liu, Stambaugh and Yuan): shells, E/P value, turnover;
* the factor industry from the public record: Dimensional, AQR, factor ETFs, long-only tilts, costs;
* the Track Record opens: ten classic factors registered and scored once on 2021–2025.

Every number is computed by the series' own code ([`compute.py`](compute.py), the House's new
[`factors`](../../../explainer/quant/house/factors.py) library and [`track`](../../../explainer/quant/house/track.py)
ledger). Data: Kenneth French's data library (the five factors, momentum, short-term reversal, the 25 size–value
portfolios, momentum deciles, variance sorts, the book-to-market file's annual B/M), AQR's data sets (Betting Against
Beta, Quality Minus Junk, Time Series Momentum, Value and Momentum Everywhere, Century of Factor Premia, The Devil in
HML's Details), global-q.org's q5 factors, and Robert Stambaugh's CH-4 factors.

*An education in methods, not investment advice. Firms are described from the public record, as reported by the
sources named.*

## Chapters (about 59 minutes)

* **Six dollars** (3.1 min). A dollar in July 1963 in the market (less bills) → $25; in SMB, HML, RMW, CMA → $3.6–4.9;
  in momentum → $40 (to December 2020, no costs); the momentum crash of March–May 2009 (−49% while the market rose
  26%); a factor as a long–short portfolio, a factor model as an APT with named factors; the history strip
  (1972–2022); the plan; the research desk's library.
* **1. Testing a factor model** (4.6). The 25 size–value portfolios, 1963–2020 (small value 12.7% a year, small growth
  4.3%); the time-series test and GRS; its geometry (α'Σ⁻¹α = SR²(f, R) − SR²(f)); Fama–MacBeth and Shanken; results
  (GRS: CAPM 3.96, FF3 3.55, Carhart 3.09, FF5 2.96, all p < 10⁻⁵; average |α| 2.3% → 1.1% → 1.0% → 1.0%); alpha grids
  (small growth −5.5% under the CAPM and FF3, −3.3% under FF5); predicted against average returns; which assets,
  which test (Lewellen–Nagel–Shanken; Barillas–Shanken).
* **2. Size, value, and three factors** (3.6). Basu, Banz, Rosenberg–Reid–Lanstein, Fama–French; the 2 x 3
  construction on forty made-up stocks; SMB and HML since 1926 (2.4% a year, t = 2.1; 4.0%, t = 3.2); before and after
  1981 (SMB 3.4% → 1.0%, t = 0.6; HML 5.0% → 2.5%); January (SMB 2.0% a month against 0.03%); McLean–Pontiff (26%
  lower out of sample, 58% after publication); by decade; distress, extrapolation, size and junk.
* **3. Momentum** (4.0). Jegadeesh–Titman and the 2 x 3 UMD; deciles 1927–2020 (losers 0.9% a year, winners 15.0%);
  three horizons (reversal, momentum, long-run reversal); UMD (7.6% a year, Sharpe 0.47, t = 4.5, skew −3.1, worst
  month −52.6%, drawdown −78%); time-series momentum (Moskowitz–Ooi–Pedersen) by asset class (Sharpe 0.56–0.71; all
  1.06, 1985–2020); 2008 (+25% against the market's −38%); correlation with UMD 0.41; the smile; underreaction and the
  disposition effect.
* **4. Momentum crashes** (4.1). 2008–09 month by month (March −12%, April −34%, May −13%); July–August 1932 (−74%,
  the market +83%); the six worst months, all in rebounds; Daniel–Moskowitz's mechanism; conditional betas (normal
  0.01; bear market, market down −0.49; bear market, market up −0.97 and −48% a year); the short call; volatility
  scaling (Sharpe 0.46 → 0.75, skew −3.1 → −0.8, drawdown −78% → −46%, spring 2009 −49% → −24%); cautions
  (Cederburg et al.; crowding).
* **5. Profitability, investment, five factors and q** (4.0). The dividend discount model and B/M; worked (base 0.57,
  less profitable 1.33, investing more 0.41, riskier 0.86); Novy-Marx's gross profitability; RMW and CMA (3.0% a year
  each, Sharpe 0.39 and 0.44; corr(HML, CMA) 0.68); HML spanned (α 3.9% on the market and size, −1.0%, t = −0.8, with
  RMW and CMA); the investment CAPM and the q5 factors 1967–2020 (IA 4.1%, ROE 6.1%, EG 9.7% with t = 10.4; HML's α on
  q 0.0%); which model, which reason, and a caution on EG.
* **6. Low risk** (2.8). Frazzini–Pedersen's construction; BAB (US 1930–2020: 8.2% a year, Sharpe 0.73, t = 6.9,
  drawdown −55%; global 1987–2020: 9.2%, 0.90); variance-sorted quintiles 1963–2020 (Sharpe 0.57 → 0.16, beta 0.70 →
  1.59); leverage, lotteries, benchmarks; Novy-Marx–Velikov's critique; the raw spread (2.5%, t = 0.9).
* **7. Everywhere; carry; quality** (3.9). Value and momentum in eight markets (all positive, correlations −0.23 to
  −0.65, the mix better everywhere); all markets (value 0.41, momentum 0.57, correlation −0.59, mix 1.08, mix
  drawdown −10%); carry (Koijen–Moskowitz–Pedersen–Vrugt) in four asset classes (Sharpe 0.14–0.65, skew negative in
  three); quality minus junk (US 1957–2020: 4.0%, Sharpe 0.54, beta −0.25); liquidity, behaviour, diversification.
* **8. Value's lost decade** (3.6). HML 2007–2020 (−5.3% a year, t = −2.0, drawdown −57% to September 2020) against
  +5.6% in 1926–2006; how surprising (z ≈ −4.1; twenty years to t = 2); the value spread 1926–2020 (2.40 in 2020,
  above 96% of years; median 1.55); revaluation (Arnott et al.) and the Campbell–Shiller reading; intangibles, rates,
  flows, luck; HML with current prices (−2.6% a year against −5.3%); the verdict, and the sealed years.
* **9. Green returns** (2.8). Pástor–Stambaugh–Taylor's equilibrium; an illustrative decade (expected 5% and 7%;
  realised the other way round); the evidence (green outperformance 2012–2020 explained by concern shocks; Bolton–
  Kacperczyk's carbon premium); rating disagreement (Berg–Kölbel–Rigobon, correlations 0.4–0.7); expected is not
  realised.
* **10. Factor timing and factor momentum** (3.5). The siren song; the value spread against next year's HML,
  1927–2020 (slope 0.098, t = 1.8, R² 0.05; 12% fitted for 2021 against a 4% mean); Haddad–Kozak–Santosh; factor
  momentum on six factors 1964–2020 (Sharpe 0.58, t = 4.4, against 1.09 for holding all six); UMD's alpha on it
  (1.9%, t = 1.1).
* **11. China's factors** (2.8). Retail trading and rationed listing; the shell value; CH-4 (size, E/P value,
  turnover) 2000–2020 (market Sharpe 0.31; SMB 0.36; VMG 13.4% a year, Sharpe 1.05; PMO 9.3%, 0.75) against the US
  (HML 1.0%, 0.09); corr(SMB, VMG) −0.64; institutions shape factors.
* **12. The factor industry** (2.9). Dimensional (1981); AQR (1998; assets reported about $226 billion in 2018); factor
  indices and ETFs; a long-only tilt as the market plus a fraction of the factor (illustrative); turnover, measured
  costs (Frazzini–Israel–Moskowitz; Novy-Marx–Velikov 2016), capacity.
* **13. The Track Record opens** (3.4). The rules; the registration code; ten rows (research Sharpe → 2021–25 Sharpe:
  MKT 0.44 → 0.68, SMB 0.26 → −0.44, HML 0.31 → 0.55, UMD 0.46 → 0.18, RMW 0.39 → 0.62, CMA 0.44 → 0.12, BAB 0.73 →
  0.18, QMJ 0.54 → 0.25, TSMOM 1.06 → 0.28, value–momentum mix 1.08 → 1.06; standard errors about 0.45); year by year
  (2022: market −21%, HML +32%, UMD +20%, TSMOM +25%); the reading (decay as predicted, little significance, the mix
  held); the trial counter 315 → 325.
* **14. Rule 24: the factor library** (2.6). The first sheet; **lab**: `vol_scaled`, `factor_momentum`, `drawdown`;
  the `factors` module; Rule 24; the rule against 2009, value's decade, size after 1981, and green returns.
* **For the researcher: where momentum profits come from** (5.3). For the weighted relative-strength strategy
  w_i = (x_i − x̄)/N, the average profit is exactly (N − 1)/N²ΣCov(x_i, r_i) − (1/N²)Σ_{i≠j}Cov(x_j, r_i) + the
  covariance of the means (Lo and MacKinlay 1990): own persistence, lead–lag, dispersion of means. A simulated check
  (30 assets, AR(1) idiosyncratic φ = 0.1, a common factor) recovers each term. Ken French's 40 industries with full
  histories, monthly 1926–2020, in 10⁻⁴ a month (± block-bootstrap s.e.): one-month formation, profit 0.50 (± 0.26) =
  own 4.42 (± 2.42) + lead–lag −3.94 (± 2.28) + means 0.02; twelve-month (skip one), 3.43 (± 0.96) = own −1.07 (± 7.3)
  + lead–lag 4.32 (± 6.7) + means 0.18 (± 0.12): as $1/$1 strategies 3.8% and 6.8% a year (Sharpe 0.20, 0.32). The
  twelve-month profit comes from negative cross-serial covariance (Lewellen 2002), the dispersion of means about 5%
  (against Conrad and Kaul 1998; Jegadeesh and Titman 2002). Three open problems; pause: a positive lead from asset 1
  to asset 2 enters the lead–lag term with a minus sign, and the strategy loses.
* **Recap, desk questions, problems** (3.4). Fourteen lines; six desk questions; twelve problems (two at
  qualifying-exam level), solutions below.

## Hands-on

* **Lab** (the House's own code on screen): `vol_scaled`, `factor_momentum`, `drawdown` (ch. 14); the envelope's
  registration code (ch. 13).
* **Computed:** GRS and two-pass tests of four models; the factors' statistics, subperiods and decades; the momentum
  deciles; conditional betas and volatility-scaled momentum; spanning regressions; the q-factors; BAB and variance
  sorts; value and momentum in eight markets and their mix; carry and quality; the value spread and its forecast;
  factor momentum; CH-4; the Track Record's ten rows.
* **Live constructions:** the 25-portfolio grid and its alpha grids; a 2 x 3 sort with NYSE breakpoints; the decile
  staircase; the trend smile; the bear-market payoff of momentum; elastic bars of the Track Record.

## Textbook audit

| Textbook | Chapters | Where |
|---|---|---|
| Ang, *Asset Management* | 7 (factor theory), 14 (factor investing: size, value, momentum, low risk), 10 (alpha) | ch. 2–7, 12 |
| Ilmanen, *Expected Returns* | 12–14 (value, momentum, carry), 16 (illiquidity), 9 (equity premium) | ch. 3, 7 |
| Bali, Engle and Murray, *Empirical Asset Pricing* | 2–3 (portfolio sorts, Fama–MacBeth), 7–11 (size, value, momentum, low risk, liquidity) | ch. 1–6 |
| Pedersen, *Efficiently Inefficient* | 9 (value and momentum), 10 (low risk, quality), 11 (factors), 12 (trend) | ch. 3, 6, 7 |
| Cochrane, *Asset Pricing* | 12–15 (regression tests, GRS, Fama–MacBeth, Shanken) | ch. 1 |

## Papers, chapter by chapter

* Hook: Black, Jensen and Scholes (1972); Fama and French (1993).
* ch. 1: Fama and MacBeth (1973); Gibbons, Ross and Shanken (1989); Shanken (1992); Lewellen, Nagel and Shanken
  (2010); Barillas and Shanken (2018).
* ch. 2: Basu (1977); Banz (1981); Rosenberg, Reid and Lanstein (1985); Fama and French (1992, 1993, 1996);
  Lakonishok, Shleifer and Vishny (1994); McLean and Pontiff (2016); Asness, Frazzini, Israel, Moskowitz and Pedersen
  (2018).
* ch. 3: De Bondt and Thaler (1985); Jegadeesh (1990); Lehmann (1990); Jegadeesh and Titman (1993); Carhart (1997);
  Barberis, Shleifer and Vishny (1998); Hong and Stein (1999); Grinblatt and Han (2005); Moskowitz, Ooi and Pedersen
  (2012).
* ch. 4: Daniel and Moskowitz (2016); Barroso and Santa-Clara (2015); Cederburg, O'Doherty, Wang and Yan (2020).
* ch. 5: Fama and French (2006, 2015); Novy-Marx (2013); Hou, Xue and Zhang (2015, 2021); Stambaugh and Yuan (2017).
* ch. 6: Black (1972); Ang, Hodrick, Xing and Zhang (2006); Baker, Bradley and Wurgler (2011); Bali, Cakici and
  Whitelaw (2011); Frazzini and Pedersen (2014); Novy-Marx and Velikov (2022).
* ch. 7: Asness, Moskowitz and Pedersen (2013); Koijen, Moskowitz, Pedersen and Vrugt (2018); Asness, Frazzini and
  Pedersen (2019).
* ch. 8: Cohen, Polk and Vuolteenaho (2003); Asness and Frazzini (2013); Arnott, Harvey, Kalesnik and Linnainmaa
  (2021); Israel, Laursen and Richardson (2021); Eisfeldt, Kim and Papanikolaou (2022).
* ch. 9: Pástor, Stambaugh and Taylor (2021, 2022); Bolton and Kacperczyk (2021); Berg, Kölbel and Rigobon (2022).
* ch. 10: Asness (2016); Haddad, Kozak and Santosh (2020); Ehsani and Linnainmaa (2022).
* ch. 11: Liu, Stambaugh and Yuan (2019).
* ch. 12: Frazzini, Israel and Moskowitz (2018); Novy-Marx and Velikov (2016); press reports on AQR's assets.

## Build it

```bash
python -m videos.quant.quant24.compute                         # every item (fetches and caches the data)
EXPLAINER_TTS=silent python tools/qa_scene.py quant24 Crash     # one chapter, silent, with a contact sheet
python tools/make.py quant24 --cpu-voice -q m                  # English and Chinese, narrated by Kokoro on the CPU
```

The `envelope` item opens the hold-out for the ten registered factors; it is idempotent (a rerun with the same code
re-reads it) and refuses a second opening with different code.

## Desk questions, with solutions

1. **Momentum and value are negatively correlated. Why hold both?** Each has a positive premium, and with a
   correlation near −0.6 the 50/50 mix keeps the average return and loses most of the risk: across all markets a
   Sharpe ratio of 1.08 against 0.41 and 0.57 alone, with a worst drawdown of 10% against about 31%. It disappoints
   when both lose together, in a funding squeeze or when both premia decay (ch. 7).
2. **A model is rejected with p = 0.001 but its average pricing error is 0.3% a year. Use it?** Probably. Long samples
   reject every model. Check where the alphas are (one corner, like small growth, or everywhere), whether they line up
   with an omitted characteristic, whether they survive costs and a hold-out, and how rival models do on the same
   assets (ch. 1).
3. **The size premium: 3.4% before 1981, 1.0% after. Dead, never there, or hiding?** A t-statistic of 0.6 cannot
   decide. Decay after publication (McLean–Pontiff), the concentration in January, and the stronger premium once junk
   is controlled for each point a different way; international markets and earlier periods are the tie-breakers (ch.
   2).
4. **The market fell 40% in two years and just rose 10% in a month; momentum's beta is about −1. What do you do?**
   Cut or hedge it: scale it by volatility, or buy back market beta. If the bear market resumes you give up a strong
   month for momentum (its average in bear-market down months was +39% a year); if the rebound continues you avoid
   the crash (−48% a year in bear-market up months) (ch. 4).
5. **A pension fund that cannot borrow wants more return. High-beta stocks, or low-beta stocks plus futures?**
   Low-beta stocks with equity futures for the extra exposure: futures embed the leverage the fund cannot take
   directly. The low-risk anomaly says most constrained investors do the opposite, which is why high-beta stocks are
   overpriced (ch. 6).
6. **December 2020: the value spread is at its 96th percentile. What do you expect?** A tilt of the odds: the fitted
   line points to about 12% for value in 2021 against a 4% average, with an R² of 5%. Lean in modestly; whatever 2021
   brings is one draw (ch. 10; the hold-out's 2021 HML return was +22%, ch. 13).

## Problems, with solutions

1. **GRS as a Sharpe gain.** Stack the factors and test assets, z = (f, R). Write R = α + Bf + ε. The maximum squared
   Sharpe ratio of z is μ_z'V_z⁻¹μ_z; by the partitioned inverse (or by noting that the residuals ε are uncorrelated
   with f and have mean α), it splits as μ_f'Ω⁻¹μ_f + α'Σ⁻¹α. So α'Σ⁻¹α = SR²(f, R) − SR²(f).
2. **One asset.** With N = 1, J = (T − 1 − K) α̂²/σ̂² / (1 + SR_f²). The OLS variance of the intercept is
   σ²(1 + f̄'Ω⁻¹f̄)/T, so t² = Tα̂²/(σ̂²(1 + SR_f²)) and J = t²(T − K − 1)/T: the squared t-statistic of the alpha, up to
   the degrees of freedom.
3. **A 2 x 3 sort.** SMB = (1.2 + 1.0 + 1.5)/3 − (0.6 + 0.8 + 1.1)/3 = 1.233 − 0.833 = 0.40%. HML = (1.5 + 1.1)/2 −
   (1.2 + 0.6)/2 = 1.30 − 0.90 = 0.40%.
4. **Book-to-market.** M/B = Σ_{τ≥1} (ROE − g)(1 + g)^{τ−1}/(1 + r)^τ = (ROE − g)/(1 + r) × 1/(1 − (1 + g)/(1 + r)) =
   (ROE − g)/(r − g). With ROE 12% and g 5%: B/M = 0.8 means M/B = 1.25 = 0.07/(r − 0.05), so r = 10.6% (against 9% at
   B/M 0.57).
5. **The mix.** Mean 4.5%; variance ¼(0.01 + 0.01 − 2 × 0.6 × 0.01) = 0.002, volatility 4.47%; Sharpe ratio 1.01,
   against 0.4 and 0.5 alone.
6. **Momentum's beta in a rebound.** UMD's beta is 0.8 − 1.8 = −1.0, so a 15% market rise costs it about 15% before
   any stock-specific news: the crash mechanism of ch. 4.
7. **Scaling.** Weight 12%/40% = 0.3; the scaled loss is 0.3 × (−34%) = −10.2%.
8. **BAB by hand.** r = 0.6/0.7 − 0.8/1.5 = 0.857 − 0.533 = 0.32% a month (3.9% a year); its beta is 0.7/0.7 −
   1.5/1.5 = 0 if the betas are right.
9. **Years.** T = (2/0.45)² ≈ 19.8 years. In five years, t = SR√5 = 2 needs SR = 0.89.
10. **Green and brown.** Realised: green (1.05)(1.10) − 1 = 15.5%; brown (1.07)(0.95) − 1 = 1.65%. Expected next year:
    still 5% and 7%, unless concern keeps rising faster than prices assume.
11. **(qual) Lo and MacKinlay's identity.** π̄ = (1/T)Σ_tΣ_i(x_{it} − x̄_t)r_{it}/N = (1/N)Σ_i \overline{x_ir_i} − \overline{x̄ r̄}.
   Write \overline{x_ir_i} = Ĉov(x_i, r_i) + x̄_ir̄_i and \overline{x̄r̄} = Ĉov(x̄, r̄) + (mean x̄)(mean r̄), with
   Ĉov(x̄, r̄) = (1/N²)Σ_{i,j}Ĉov(x_j, r_i). Collect the diagonal: (1/N − 1/N²)ΣĈov(x_i, r_i) = ((N − 1)/N²)ΣĈov(x_i, r_i);
   the off-diagonal enters as −(1/N²)Σ_{i≠j}; the means give (1/N)Σx̄_ir̄_i − x̄r̄ = (1/N)Σ(x̄_i − x̄)(r̄_i − r̄).
12. **(qual) A known world.** r_it = μ_i + f_t + e_it with f iid and e_it = φe_{i,t−1} + z_it. For a one-period
   formation, Cov(x_i, r_i) = Cov(f, f′) + Cov(e_i, e_i′) = 0 + φσ_z²/(1 − φ²); Cov(x_j, r_i) = 0 for i ≠ j (f is iid,
   the e's independent); the means term is the cross-sectional variance of μ. The factor is common to all assets, so
   it cancels from x_i − x̄: it adds nothing.

## For the researcher

* **The theorems.** Lo and MacKinlay (1990), "When are contrarian profits due to stock market overreaction?" *RFS* 3;
  Jegadeesh and Titman (1993, 2002); Conrad and Kaul (1998), *RFS* 11; Moskowitz and Grinblatt (1999) on industry
  momentum; Lewellen (2002), "Momentum and autocorrelation in stock returns," *RFS* 15.
* **Simplifications.** The weighted (linear) strategy rather than deciles; 40 industries with complete histories;
  log formation returns; the bootstrap ignores the overlap of formation windows beyond the 24-month blocks.
* **Open problems.** Individual stocks and which links carry the profit; decomposing momentum's risk; whether lead–lag
  has been traded away.

## Data and reproducibility

* Kenneth French's data library, monthly, frozen through December 2025 and checksummed: the five factors (2 x 3),
  momentum, short-term reversal, the three factors since 1926, 25 portfolios on size and B/M, 10 on prior return,
  quintiles on variance and residual variance; the BE-ME file's annual "Sum of BE / Sum of ME" block (to 2020).
* AQR's data sets (Betting Against Beta, Quality Minus Junk, Time Series Momentum, Value and Momentum Everywhere,
  Century of Factor Premia, The Devil in HML's Details), parsed and frozen through December 2025 (AQR rebuilds each
  file's history at every update, so the parsed sheet is checksummed, not the file).
* global-q.org: q5 factors, monthly, 1967–2025. Robert Stambaugh: CH-4 factors, monthly, 2000–2021.
* The research window ends in December 2020. The hold-out, January 2021 to December 2025, is read only in the
  `envelope` item, after each of ten factors is registered (code hash, definition, cost model, one trial each); the
  trial counter rises from 315 to 325. Rows are written to `videos/quant/data/track_record.json`.
* Cost model, a placeholder until Part 26: 0.05% a year for the market, 1% for SMB, HML, RMW, CMA, QMJ and TSMOM, 1.5%
  for BAB and the value–momentum mix, 3% for UMD.
* Published figures quoted, not computed: Banz, Basu and the other papers' findings as cited; McLean and Pontiff's
  percentages; Berg, Kölbel and Rigobon's correlations; AQR's reported assets; Dimensional's founding.
* Illustrative inputs, labelled on screen: the 2 x 3 toy sort, the dividend discount model's firms, the green decade,
  the long-only loading, the bear-market payoff's slopes.

---

# 量化金融，从零搭建 — 第24部分：因子

本部分是第四幕“收益溢价”（第23–29部分）的第二部分。第23部分建立了预期收益的理论；本部分认识少数几个组合——半个世纪以来，它们解释了股票收益的大部分——并打开业绩记录：第一批在封存的2021–2025年数据上打分的策略。本部分讲：

* 如何检验因子模型：Gibbons–Ross–Shanken检验及其夏普比率几何、带Shanken修正的Fama–MacBeth，在25个规模–账面市值比组合上（CAPM、三因子、Carhart、五因子）；
* 规模与价值：异象（Basu、Banz、Rosenberg）、Fama与French的2 x 3构造、1926年以来的历史、发表后的衰减，以及一月效应；
* 动量：Jegadeesh–Titman十分位组合、因子、三个期限、跨资产类别的时间序列动量及其“微笑”；
* 动量崩盘：1932年与2009年、Daniel与Moskowitz的熊市贝塔、对反弹的空头看涨期权、Barroso与Santa-Clara的波动率缩放；
* 由股利贴现模型得出的盈利能力与投资；五因子；被取代的价值；q因子；
* 低风险：押注低贝塔、按波动率排序的组合，以及对其构造的批评；
* 处处可见的价值与动量；处处可见的套息；质量减垃圾；
* 价值失去的十年：回撤、价值价差、重估、无形资产，以及HML的细节；
* 绿色收益：预期与实现（Pástor、Stambaugh与Taylor）、碳溢价、评级分歧；
* 因子择时（价值价差；Haddad、Kozak与Santosh）与因子动量（Ehsani与Linnainmaa）；
* 中国的因子（Liu、Stambaugh与Yuan）：壳价值、E/P价值、换手率；
* 依据公开记录的因子行业：Dimensional、AQR、因子ETF、只做多的倾斜、成本；
* 业绩记录开启：十个经典因子登记，并在2021–2025年上打分一次。

*讲的是方法，不构成投资建议。涉及的公司均依据公开记录，并注明报道来源。*

## 章节（约59分钟）

* **六美元。** 1963年7月投入市场（减去国库券）的一美元 → 25美元；投入SMB、HML、RMW、CMA → 3.6–4.9美元；投入动量 → 40美元（到2020年12月，不计成本）；2009年3–5月的动量崩盘（−49%，而市场上涨26%）；因子是多空组合，因子模型是因子有名字的APT；历史条（1972–2022）；本部分安排；研究交易台的因子库。
* **1. 检验因子模型。** 25个规模–价值组合，1963–2020（小盘价值每年12.7%，小盘成长4.3%）；时间序列检验与GRS；其几何（α'Σ⁻¹α = SR²(f, R) − SR²(f)）；Fama–MacBeth与Shanken；结果（GRS：CAPM 3.96、FF3 3.55、Carhart 3.09、FF5 2.96，p都小于10⁻⁵；平均|α| 2.3% → 1.1% → 1.0% → 1.0%）；α网格（小盘成长在CAPM和FF3下为−5.5%，在FF5下为−3.3%）；预测收益对平均收益；用哪些资产、哪种检验（Lewellen–Nagel–Shanken；Barillas–Shanken）。
* **2. 规模、价值与三因子。** Basu、Banz、Rosenberg–Reid–Lanstein、Fama–French；用四十只虚构股票演示2 x 3构造；1926年以来的SMB和HML（每年2.4%，t = 2.1；4.0%，t = 3.2）；1981年前后（SMB 3.4% → 1.0%，t = 0.6；HML 5.0% → 2.5%）；一月（SMB每月2.0%，其他月份0.03%）；McLean–Pontiff（样本外低26%，发表后低58%）；按十年；困境、外推、规模与垃圾股。
* **3. 动量。** Jegadeesh–Titman与2 x 3的UMD；1927–2020年十分位组合（输家每年0.9%，赢家15.0%）；三个期限（反转、动量、长期反转）；UMD（每年7.6%，夏普比率0.47，t = 4.5，偏度−3.1，最差月份−52.6%，回撤−78%）；按资产类别的时间序列动量（Moskowitz–Ooi–Pedersen）（夏普比率0.56–0.71；合计1.06，1985–2020）；2008年（+25%，市场−38%）；与UMD的相关系数0.41；微笑；反应不足与处置效应。
* **4. 动量崩盘。** 2008–09年逐月（3月−12%、4月−34%、5月−13%）；1932年7–8月（−74%，市场+83%）；最差的六个月，全都在反弹中；Daniel–Moskowitz的机制；条件贝塔（正常时0.01；熊市中市场下跌−0.49；熊市中市场上涨−0.97，每年−48%）；空头看涨期权；波动率缩放（夏普比率0.46 → 0.75，偏度−3.1 → −0.8，回撤−78% → −46%，2009年春−49% → −24%）；注意事项（Cederburg等；拥挤）。
* **5. 盈利能力、投资、五因子与q。** 股利贴现模型与B/M；算例（基准0.57，盈利较低1.33，投资较多0.41，风险较高0.86）；Novy-Marx的毛利润率；RMW与CMA（各每年3.0%，夏普比率0.39和0.44；corr(HML, CMA) 0.68）；HML被张成（对市场和规模α为3.9%，加入RMW和CMA后为−1.0%，t = −0.8）；投资CAPM与1967–2020年的q5因子（IA 4.1%、ROE 6.1%、EG 9.7%，t = 10.4；HML对q的α为0.0%）；哪个模型、哪种理由，以及对EG的提醒。
* **6. 低风险。** Frazzini–Pedersen的构造；BAB（美国1930–2020：每年8.2%，夏普比率0.73，t = 6.9，回撤−55%；全球1987–2020：9.2%，0.90）；1963–2020年按方差排序的五分位组合（夏普比率0.57 → 0.16，贝塔0.70 → 1.59）；杠杆、彩票、基准；Novy-Marx–Velikov的批评；原始价差（2.5%，t = 0.9）。
* **7. 处处可见；套息；质量。** 八个市场中的价值与动量（全部为正，相关系数−0.23到−0.65，组合处处更好）；所有市场合计（价值0.41、动量0.57、相关系数−0.59、组合1.08、组合回撤−10%）；四个资产类别中的套息（Koijen–Moskowitz–Pedersen–Vrugt）（夏普比率0.14–0.65，三个为负偏）；质量减垃圾（美国1957–2020：4.0%，夏普比率0.54，贝塔−0.25）；流动性、行为、分散化。
* **8. 价值失去的十年。** 2007–2020年的HML（每年−5.3%，t = −2.0，到2020年9月回撤−57%），对比1926–2006年的+5.6%；有多意外（z ≈ −4.1；二十年才能到t = 2）；1926–2020年的价值价差（2020年为2.40，高于96%的年份；中位数1.55）；重估（Arnott等）与Campbell–Shiller的解读；无形资产、利率、资金流、运气；用当前价格的HML（每年−2.6%，对−5.3%）；结论，以及封存的年份。
* **9. 绿色收益。** Pástor–Stambaugh–Taylor的均衡；一个示意的十年（预期5%和7%；实现的结果相反）；证据（2012–2020年绿色跑赢可由关注度冲击解释；Bolton–Kacperczyk的碳溢价）；评级分歧（Berg–Kölbel–Rigobon，相关系数0.4–0.7）；预期不等于实现。
* **10. 因子择时与因子动量。** 塞壬之歌；价值价差对下一年HML，1927–2020（斜率0.098，t = 1.8，R² 0.05；对2021年的拟合值12%，均值4%）；Haddad–Kozak–Santosh；1964–2020年六个因子上的因子动量（夏普比率0.58，t = 4.4，而持有全部六个为1.09）；UMD对它的α（1.9%，t = 1.1）。
* **11. 中国的因子。** 散户交易与配给的上市；壳价值；CH-4（规模、E/P价值、换手率）2000–2020（市场夏普比率0.31；SMB 0.36；VMG每年13.4%，夏普比率1.05；PMO 9.3%，0.75），对比美国（HML 1.0%，0.09）；corr(SMB, VMG) −0.64；制度塑造因子。
* **12. 因子行业。** Dimensional（1981）；AQR（1998；2018年报道资产约2,260亿美元）；因子指数与ETF；只做多的倾斜相当于市场加上一部分因子（示意）；换手率、实测成本（Frazzini–Israel–Moskowitz；Novy-Marx–Velikov 2016）、容量。
* **13. 业绩记录开启。** 规则；登记代码；十行（研究期夏普比率 → 2021–25年夏普比率：MKT 0.44 → 0.68、SMB 0.26 → −0.44、HML 0.31 → 0.55、UMD 0.46 → 0.18、RMW 0.39 → 0.62、CMA 0.44 → 0.12、BAB 0.73 → 0.18、QMJ 0.54 → 0.25、TSMOM 1.06 → 0.28、价值–动量组合1.08 → 1.06；标准误约0.45）；逐年（2022年：市场−21%、HML +32%、UMD +20%、TSMOM +25%）；解读（如预期般衰减、显著性很低、组合守住了）；试验计数器315 → 325。
* **14. 第24条规则：因子库。** 第一张表；**实验**：`vol_scaled`、`factor_momentum`、`drawdown`；`factors`模块；第24条规则；用2009年、价值的十年、1981年后的规模和绿色收益检验这条规则。
* **写给研究者：动量收益从何而来。** 对加权相对强度策略w_i = (x_i − x̄)/N，平均利润恰为(N − 1)/N²ΣCov(x_i, r_i) − (1/N²)Σ_{i≠j}Cov(x_j, r_i) + 均值的协方差（罗与麦金莱1990）：自身持续性、领先–滞后、均值离散。模拟检验（30个资产、AR(1)特质部分φ = 0.1、一个公共因子）还原了每一项。肯尼斯·弗伦奇的40个完整历史行业，1926–2020月度，单位10⁻⁴每月（± 块自助法标准误）：一个月形成期，利润0.50（± 0.26）= 自身4.42（± 2.42）+ 领先–滞后−3.94（± 2.28）+ 均值0.02；十二个月（跳过一个月），3.43（± 0.96）= 自身−1.07（± 7.3）+ 领先–滞后4.32（± 6.7）+ 均值0.18（± 0.12）：作为1美元多/1美元空的策略每年3.8%和6.8%（夏普0.20、0.32）。十二个月的利润来自负的交叉序列协方差（卢埃林2002），均值离散约占5%（与康拉德和考尔1998相反；杰加迪什与蒂特曼2002）。三个开放问题；暂停题：资产1对资产2的正向领先以负号进入领先–滞后项，策略亏损。
* **回顾、交易台问题与习题。** 十四行回顾；六个交易台问题；十二道习题（两道为资格考试水平），解答见下文。

## 交易台问题与解答

1. **动量与价值负相关。为什么两个都持有？** 两者都有正溢价，而相关系数约为−0.6时，五五组合保留平均收益、去掉大部分风险：在所有市场合计，夏普比率为1.08，单独为0.41和0.57，最差回撤10%，而单独约31%。当两者一起亏损时——资金紧张，或两种溢价同时衰减——组合会令人失望（第7章）。
2. **一个模型以p = 0.001被拒绝，但平均定价误差只有每年0.3%。用不用？** 大概用。长样本会拒绝每一个模型。检查α在哪里（是像小盘成长那样的一个角落，还是到处都有），是否与某个遗漏的特征对齐，是否经得起成本和样本外检验，以及竞争模型在同样资产上的表现（第1章）。
3. **规模溢价：1981年前3.4%，之后1.0%。是死了、从未存在，还是藏起来了？** 0.6的t统计量无法判断。发表后的衰减（McLean–Pontiff）、集中在一月，以及控制垃圾股后溢价更强，分别指向不同方向；国际市场和更早的时期是决胜因素（第2章）。
4. **市场两年下跌40%，刚刚一个月上涨10%；动量的贝塔约为−1。怎么办？** 减仓或对冲：按波动率缩放，或买回市场贝塔。如果熊市继续，你会放弃动量的一个好月份（它在熊市下跌月份的平均为每年+39%）；如果反弹继续，你就避开了崩盘（熊市上涨月份每年−48%）（第4章）。
5. **一只不能借钱的养老基金想要更高收益。买高贝塔股票，还是低贝塔股票加期货？** 低贝塔股票，用股指期货获得额外暴露：期货内含基金无法直接承担的杠杆。低风险异象说明，大多数受约束的投资者做的正好相反，这就是高贝塔股票被高估的原因（第6章）。
6. **2020年12月：价值价差处于第96百分位。你预期什么？** 概率的一点倾斜：拟合线指向2021年价值约12%，而均值为4%，R²为5%。适度加仓；无论2021年结果如何，都只是一次抽样（第10章；样本外2021年HML收益为+22%，第13章）。

## 习题与解答

1. **GRS即夏普比率的增量。** 把因子和检验资产堆叠为z = (f, R)，写R = α + Bf + ε。z的最大平方夏普比率为μ_z'V_z⁻¹μ_z；由分块求逆（或注意残差ε与f不相关、均值为α），它分解为μ_f'Ω⁻¹μ_f + α'Σ⁻¹α。所以α'Σ⁻¹α = SR²(f, R) − SR²(f)。
2. **一个资产。** N = 1时，J = (T − 1 − K) α̂²/σ̂² / (1 + SR_f²)。截距的OLS方差为σ²(1 + f̄'Ω⁻¹f̄)/T，所以t² = Tα̂²/(σ̂²(1 + SR_f²))，J = t²(T − K − 1)/T：α的t统计量的平方，差一个自由度因子。
3. **2 x 3排序。** SMB = (1.2 + 1.0 + 1.5)/3 − (0.6 + 0.8 + 1.1)/3 = 1.233 − 0.833 = 0.40%。HML = (1.5 + 1.1)/2 − (1.2 + 0.6)/2 = 1.30 − 0.90 = 0.40%。
4. **账面市值比。** M/B = Σ_{τ≥1} (ROE − g)(1 + g)^{τ−1}/(1 + r)^τ = (ROE − g)/(1 + r) × 1/(1 − (1 + g)/(1 + r)) = (ROE − g)/(r − g)。ROE为12%、g为5%时：B/M = 0.8即M/B = 1.25 = 0.07/(r − 0.05)，所以r = 10.6%（B/M为0.57时为9%）。
5. **组合。** 均值4.5%；方差¼(0.01 + 0.01 − 2 × 0.6 × 0.01) = 0.002，波动率4.47%；夏普比率1.01，单独为0.4和0.5。
6. **反弹中动量的贝塔。** UMD的贝塔为0.8 − 1.8 = −1.0，所以市场上涨15%会让它在没有任何个股消息前就损失约15%：第4章的崩盘机制。
7. **缩放。** 权重12%/40% = 0.3；缩放后的损失为0.3 × (−34%) = −10.2%。
8. **手算BAB。** r = 0.6/0.7 − 0.8/1.5 = 0.857 − 0.533 = 每月0.32%（每年3.9%）；若贝塔准确，它的贝塔为0.7/0.7 − 1.5/1.5 = 0。
9. **年数。** T = (2/0.45)² ≈ 19.8年。五年内要t = SR√5 = 2，需要SR = 0.89。
10. **绿色与棕色。** 实现：绿色(1.05)(1.10) − 1 = 15.5%；棕色(1.07)(0.95) − 1 = 1.65%。下一年的预期：仍为5%和7%，除非关注度继续以超过价格预期的速度上升。
11. **（资格考试）罗与麦金莱的恒等式。** π̄ = (1/N)Σ_i \overline{x_ir_i} − \overline{x̄ r̄}。把\overline{x_ir_i}写成Ĉov(x_i, r_i) + x̄_ir̄_i，\overline{x̄r̄}写成Ĉov(x̄, r̄) + 均值之积，其中Ĉov(x̄, r̄) = (1/N²)Σ_{i,j}Ĉov(x_j, r_i)。对角项合并为((N − 1)/N²)ΣĈov(x_i, r_i)；非对角项以−(1/N²)Σ_{i≠j}进入；均值部分为(1/N)Σ(x̄_i − x̄)(r̄_i − r̄)。
12. **（资格考试）已知的世界。** r_it = μ_i + f_t + e_it，f独立同分布，e_it = φe_{i,t−1} + z_it。一期形成期时Cov(x_i, r_i) = φσ_z²/(1 − φ²)；i ≠ j时Cov(x_j, r_i) = 0；均值项是μ的横截面方差。因子对所有资产相同，在x_i − x̄中抵消：它不贡献任何利润。

## 数据与复现

* Kenneth French数据库，月度，冻结到2025年12月并校验哈希：五因子（2 x 3）、动量、短期反转、1926年以来的三因子、按规模和B/M的25个组合、按前期收益的10个组合、按方差和残差方差的五分位组合；BE-ME文件中年度“Sum of BE / Sum of ME”数据块（到2020年）。
* AQR的数据集（押注低贝塔、质量减垃圾、时间序列动量、处处可见的价值与动量、一个世纪的因子溢价、HML细节中的魔鬼），解析后冻结到2025年12月（AQR每次更新都会重建整个历史，所以校验的是解析后的表，而不是文件）。
* global-q.org：q5因子，月度，1967–2025。Robert Stambaugh：CH-4因子，月度，2000–2021。
* 研究窗口截止于2020年12月。样本外数据（2021年1月到2025年12月）只在`envelope`项中读取，且是在十个因子各自登记之后（代码哈希、定义、成本模型、各一次试验）；试验计数器从315升到325。各行写入`videos/quant/data/track_record.json`。
* 成本模型，在第26部分之前的占位：市场每年0.05%；SMB、HML、RMW、CMA、QMJ和TSMOM每年1%；BAB和价值–动量组合1.5%；UMD 3%。
* 引用而非计算的公开数字：所引论文中Banz、Basu等的发现；McLean与Pontiff的百分比；Berg、Kölbel与Rigobon的相关系数；AQR的报道资产；Dimensional的成立。
* 屏幕上标注为示意的输入：2 x 3的玩具排序、股利贴现模型中的公司、绿色的十年、只做多的载荷、熊市收益图的斜率。

## 写给研究者

* **定理。** 罗与麦金莱（1990），*RFS* 3；杰加迪什与蒂特曼（1993、2002）；康拉德与考尔（1998），*RFS* 11；Moskowitz与Grinblatt（1999）论行业动量；卢埃林（2002），*RFS* 15。
* **简化。** 用加权（线性）策略而非十分位；40个完整历史的行业；对数形成期收益；块自助法未考虑24个月块之外的形成期窗口重叠。
* **开放问题。** 个股以及哪些联系承载利润；分解动量的风险；领先–滞后是否已被交易掉。
