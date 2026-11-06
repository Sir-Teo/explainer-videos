# Statistics, Built — Part 40: Time to Event

Part 40 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the twentieth part of Stage III, Master's. A leukaemia trial ends with twelve
of twenty-one patients still in remission: how long does remission last? This part builds survival analysis from the
risk set up:
- the survival function, the hazard and the cumulative hazard; censoring and truncation;
- Kaplan–Meier, Greenwood's variance and its intervals, Nelson–Aalen, the life table;
- counting processes and martingales;
- the log-rank test and Cox's partial likelihood, and how to check it;
- what hazard ratios mean, the restricted mean, and immortal time;
- parametric and AFT models, cure fractions, competing risks, frailty;
- prediction, with concordance, the IPCW Brier score, a survival forest and conformal lower bounds.

The part builds `statkit.survival` and an instrument, the Kaplan–Meier staircase (`KMStaircase`): the step function
drawn from the risk table, censoring ticks, a row of patients in time order, the drop at each event time labelled with
n and d, and shaded pointwise bands. Its real data, all from R's `survival` package (LGPL ≥ 2) except Gehan's table:
- Freireich et al.'s (1963) 6-MP trial, as tabulated by Gehan (1965);
- the Mayo Clinic PBC trial, 1974–84 (Fleming & Harrington 1991);
- the Stanford heart transplant programme, 1967–74 (Crowley & Hu 1977);
- the VA lung cancer trial (Kalbfleisch & Prentice 1980);
- the Mayo Clinic MGUS cohort (Kyle et al. 2002);
- McGilchrist & Aisbett's (1991) kidney catheter infections.

It opens with the 6-MP trial. On placebo all 21 relapsed; on 6-MP 9 did and 12 were censored. Averaging the 6-MP
times as if all had relapsed gives 17.1 weeks; averaging only the relapses gives 12.1.

From there the part covers:
- **Lifetimes.** S, h, H and S = e^{−H}; Graunt (1662) and Halley (1693); Gompertz (1825), with the World's hazards
  doubling about every 8 years; a 60-year-old man in the World has a median of 18.8 more years; Weibull and bathtub
  hazards.
- **Censoring and truncation.**
  - The four kinds; independent censoring and the likelihood.
  - The World's cohort: 4,000 adults aged 40–79 followed 15 years; 1,086 deaths, 1,702 alive at the end, 1,212 lost.
  - Ten-year survival: truth 0.786, KM 0.786; censored counted as deaths 0.590; censored dropped 0.320; censored as
    alive 0.815.
  - On the age scale, ignoring delayed entry moves the median age at death from 78 (the truth, and the
    delayed-entry KM) to 81.
- **Kaplan–Meier.** The product-limit estimator; the staircase for 6-MP (week 6: n = 21, d = 3; week 7: n = 17); the
  curve ends at 0.448. Efron's redistribute-to-the-right. Medians 23 weeks (95% CI from 13 to beyond the data) and 8
  (4–11).
- **Greenwood.** Greenwood (1926); plain, log and log-log bands; Hall–Wellner's simultaneous band.
- **Nelson–Aalen.** The cumulative hazard; placebo's slope is about 0.15 a week, 6-MP's a fifth of it. The life table
  (Cutler & Ederer 1958); log H against log t as a diagnostic.
- **Counting processes.** N, Y, Λ and M = N − Λ. Over 4,000 seeded paths M(1) has mean −0.01 and variance 26.0,
  against EΛ(1) = 26.3. Every estimator here is an integral against dM (Aalen 1978; Andersen & Gill 1982).
- **The log-rank test.** On Gehan's data the 6-MP arm had 9 relapses against 19.3 expected: χ² = 16.8,
  p = 4.2 × 10⁻⁵. Gehan's weighted version gives 13.5; Fleming–Harrington weights.
- **Cox.**
  - The partial likelihood, derived; Breslow and Efron ties.
  - Gehan's data: HR 4.82 (2.15–10.81) by Efron, 4.52 by Breslow.
  - The Mayo model on 312 patients with 125 deaths. HRs: age per decade 1.39, edema 2.19, log bilirubin 2.41, log
    albumin 0.05, log prothrombin time 20.4. Doubling bilirubin multiplies the hazard by 1.84.
  - D-penicillamine against placebo: HR 1.06 (0.75–1.50), log-rank p = 0.75.
- **Checking Cox.** Schoenfeld residuals and Grambsch–Therneau.
  - VA trial: Karnofsky HR 0.71 per 10 points, GT p = 0.001. Split at 90 days, the HR is 0.61 early and 1.01 late.
  - The Mayo model passes (p ≥ 0.055).
- **What hazard ratios mean.**
  - A seeded trial in which every patient's HR is 0.5, with a gamma frailty: the period HRs are 0.52, 0.67, 0.67 and
    0.76, and Cox's single HR is 0.58 (Hernán 2010).
  - RMST to 35 weeks on Gehan's data: 23.3 against 8.7, a gain of 14.6 weeks (8.5–20.8).
- **Immortal time.**
  - The Oscar winners (Redelmeier & Singh 2001; Sylvestre et al. 2006).
  - Stanford: 103 patients, 69 transplanted after a median 25 days, 30 died waiting. Ever-transplanted HR 0.27
    (0.17–0.43); transplant as time-varying 1.13 (0.63–2.04); adjusted for age 0.99.
  - The World's useless statin: ever-users 0.77 (0.67–0.90); time-varying 1.41 (confounding by indication); adjusted
    1.00 (0.86–1.17).
  - Suissa (2008); target trials.
- **Parametric models.**
  - AFT models; Weibull as PH and AFT.
  - VA trial: the time ratio per 10 Karnofsky points is 1.42–1.50 across four models. Weibull σ = 1.02 and implied HR
    0.71, as Cox. Log-logistic has the best AIC (1,448.3).
  - Cure models: the 6-MP plateau.
- **Competing risks.**
  - Cause-specific hazards; Aalen–Johansen.
  - MGUS, 1,384 patients, median age 72: 115 progressions, 860 deaths first. Progression by 20 years: 10.0% by
    Aalen–Johansen against 21.0% by 1 − KM; by 30 years 13.4% against 42.5%.
  - The World's cardiovascular deaths by 15 years: truth 14.9%, AJ 15.4%, 1 − KM 16.9%.
  - Per decade of age: death HR 1.91; progression cause-specific 1.14; Fine–Gray 0.84.
- **Frailty.**
  - Vaupel, Manton & Stallard; the World's population hazard bending below Gompertz.
  - Shared gamma frailty (Clayton). Kidney infections: θ̂ = 0.50. The female HR is 0.43 by Cox, 0.41 by Weibull and
    0.15 conditional on the frailty. LR for θ = 0 is 8.6 (boundary p = 0.002).
  - Recurrent events.
- **Prediction.** PBC, 416 patients, a third held out.
  - Concordance: bilirubin alone 0.773, Cox 0.828 (0.838 on its training data), a random survival forest 0.804.
  - Five-year IPCW Brier: no model 0.218, Cox 0.133, forest 0.148.
  - Conformal lower bounds under censoring (Candès, Lei & Ren 2023).

Data:
- Gehan, PBC, Stanford, VA, MGUS and kidney are the Museum's;
- the cohort is the World's;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.survival`** ([`explainer/stats/kit/survival.py`](../../../explainer/stats/kit/survival.py)), checked
  against statsmodels (`SurvfuncRight`, `survdiff`, `PHReg`) and closed forms in `tests/test_stats_kit_survival.py`:
  - **Survival and hazard:** risk tables with delayed entry and weights; Kaplan–Meier with Greenwood and plain, log
    and log-log intervals; medians and Brookmeyer–Crowley intervals; redistribute-to-the-right; Nelson–Aalen; RMST
    with its variance.
  - **Tests and Cox:** log-rank, Gehan–Breslow and Fleming–Harrington tests. Cox by Newton with Breslow or Efron ties,
    start-stop rows and weights, with Breslow's baseline. Schoenfeld residuals and the Grambsch–Therneau test.
  - **Parametric:** exponential, Weibull, log-normal and log-logistic AFT models.
  - **Competing risks and frailty:** Aalen–Johansen; Fine–Gray with IPCW weights; the shared gamma frailty Weibull.
  - **Prediction:** Harrell's C; the IPCW Brier score; a random survival forest with log-rank splits; conformal
    lower prediction bounds under censoring.
- **The World** gains its `cohort` block. Gompertz hazards for cardiovascular and other death; a gamma frailty on the
  first; loss to follow-up; 15 years of administrative censoring; a statin with no effect.
- **The Museum** gains `gehan()`, `pbc()`, `stanford_heart()`, `mgus2()`, `veteran()` and `kidney()`.
- **The Kaplan–Meier staircase** (`KMStaircase` in `explainer/stats/viz.py`).

The Coverage Board gains seven rows:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| S(t) from the known fates only (censored dropped) | exponential lifetimes, uniform censoring, n = 200 | 69.8% | broken |
| KM 90% CI, plain Greenwood | exponential lifetimes, n = 20, S(t) = 0.30 | 87.0% | broken |
| KM 90% CI, log-log | same | 90.8% | kept |
| Cox Wald 90% CI for β | exponential, n = 60, censoring 30% | 89.8% | kept |
| Cox CI, ever-treated (immortal time) | a null treatment started during follow-up, n = 400 | 0.0% | broken |
| Cox CI, treatment as time-varying | same | 91.2% | kept |
| conformal lower bound for T (90%) | Weibull lifetimes, exponential censoring, a wrong q(x) | 90.2% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats40.compute   # once (a few minutes)
python tools/build.py stats40 -q l                         # fast 480p preview
python tools/build.py stats40                              # 1080p30 -> renders/stats40.mp4
python tools/qa_scene.py stats40 KaplanMeier
python tools/lecture_length.py stats40 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | The 6-MP trial | 12 of 21 censored |
| 1 | Lifetimes | median 18.8 years from 60 |
| 2 | Censoring and truncation | 0.786 vs 0.590 / 0.320 / 0.815 |
| 3 | Kaplan–Meier | medians 23 vs 8 weeks |
| 4 | Greenwood's variance | plain 87.0% vs log-log 90.8% |
| 5 | Nelson–Aalen | slopes 0.15 vs 0.03 a week |
| 6 | Counting processes | Var M(1) = 26.0 ≈ EΛ = 26.3 |
| 7 | The log-rank test | χ² = 16.8 |
| 8 | Cox's partial likelihood | HR 4.82; the Mayo model |
| 9 | Checking Cox | Karnofsky 0.61 → 1.01 |
| 10 | What hazard ratios mean | 0.52 → 0.76; RMST +14.6 weeks |
| 11 | Immortal time | Stanford 0.27 → 1.13 |
| 12 | Parametric and AFT models | log-logistic AIC 1,448.3 |
| 13 | Competing risks | 10% vs 21% |
| 14 | Frailty | θ̂ = 0.50 |
| 15 | Prediction | C = 0.828; Brier 0.133 |
| 16 | Outro | — |

## Sources

- **Foundations.**
  - J. Graunt (1662); E. Halley, *Phil. Trans.* 17 (1693); B. Gompertz, *Phil. Trans.* 115 (1825); W. Weibull,
    *J. Appl. Mech.* 18 (1951).
  - M. Greenwood, *Reports on Public Health and Medical Subjects* 33 (1926); E. Kaplan & P. Meier, *JASA* 53 (1958);
    S. Cutler & F. Ederer, *J. Chronic Dis.* 8 (1958).
  - B. Efron, *Proc. 5th Berkeley Symp.* 4 (1967); W. Nelson, *J. Qual. Technol.* 1 (1969); O. Aalen, *Ann. Stat.* 6
    (1978).
  - W. J. Hall & J. Wellner, *Biometrika* 67 (1980); R. Brookmeyer & J. Crowley, *Biometrics* 38 (1982).
- **Trials and data.**
  - E. Freireich et al., *Blood* 21 (1963); E. Gehan, *Biometrika* 52 (1965).
  - E. R. Dickson et al., *Hepatology* 10 (1989); T. Fleming & D. Harrington (1991).
  - J. Crowley & M. Hu, *JASA* 72 (1977); J. Kalbfleisch & R. Prentice (1980, 2002).
  - R. Kyle et al., *NEJM* 346 (2002); C. McGilchrist & C. Aisbett, *Biometrics* 47 (1991).
- **Tests and Cox.**
  - N. Mantel, *Cancer Chemother. Rep.* 50 (1966); R. Peto & J. Peto, *JRSS A* 135 (1972).
  - D. Cox, *JRSS B* 34 (1972), *Biometrika* 62 (1975); N. Breslow, *Biometrics* 30 (1974); B. Efron, *JASA* 72 (1977).
  - P. Andersen & R. Gill, *Ann. Stat.* 10 (1982); R. Rebolledo, *Z. Wahrsch.* 51 (1980).
  - D. Schoenfeld, *Biometrika* 69 (1982); P. Grambsch & T. Therneau, *Biometrika* 81 (1994).
- **Interpretation.**
  - M. Hernán, *Epidemiology* 21 (2010); J. O. Irwin, *J. Hyg.* 47 (1949); P. Royston & M. Parmar, *BMC Med. Res.
    Methodol.* 13 (2013).
  - D. Redelmeier & S. Singh, *Ann. Intern. Med.* 134 (2001); M.-P. Sylvestre, E. Huszti & J. Hanley, *Ann. Intern.
    Med.* 145 (2006).
  - S. Suissa, *Am. J. Epidemiol.* 167 (2008); J. Anderson, K. Cain & R. Gelber, *J. Clin. Oncol.* 1 (1983);
    M. Hernán & J. Robins, *Am. J. Epidemiol.* 183 (2016).
- **Competing risks and frailty.**
  - O. Aalen & S. Johansen, *Scand. J. Stat.* 5 (1978); J. Fine & R. Gray, *JASA* 94 (1999).
  - J. Vaupel, K. Manton & E. Stallard, *Demography* 16 (1979); D. Clayton, *Biometrika* 65 (1978).
  - J. Boag, *JRSS B* 11 (1949); J. Berkson & R. Gage, *JASA* 47 (1952).
- **Prediction.**
  - F. Harrell et al., *JAMA* 247 (1982); E. Graf et al., *Stat. Med.* 18 (1999); H. Uno et al., *Stat. Med.* 30
    (2011).
  - H. Ishwaran et al., *Ann. Appl. Stat.* 2 (2008); E. Candès, L. Lei & Z. Ren, *JRSS B* 85 (2023).
- **Books.** Kalbfleisch & Prentice (2002); Fleming & Harrington (1991); Therneau & Grambsch (2000); Aalen, Borgan &
  Gjessing (2008).

## Problems and solutions

1. **KM without censoring.** With no censoring, n_{k+1} = n_k − d_k, so each factor is n_{k+1}/n_k and the product
   telescopes to (n − Σ_{t_k ≤ t} d_k)/n = #{T_i > t}/n.
2. **The censored exponential.** The log-likelihood is Σ δ_i log λ − λ Σ x_i = d log λ − λ Σ x_i. Setting the score to
   zero gives λ̂ = d/Σx_i. The information is d/λ², so Var(λ̂) ≈ λ²/d: precision comes from events, not people.
3. **Cox's score is log-rank.** For one binary covariate at β = 0, x̄(t_k) = n_{1k}/n_k. So
   U(0) = Σ_k (x_{(k)} − n_{1k}/n_k) = Σ_k (d_{1k} − E_{1k}) when each d_k = 1. The information at 0 is
   Σ (n_{1k}/n_k)(1 − n_{1k}/n_k), the log-rank variance without ties.
4. **Weibull is PH and AFT.** With W extreme-value, S(t | x) = exp(−e^{(log t − x'γ)/σ}) = exp(−t^{1/σ} e^{−x'γ/σ}).
   That is a Weibull with shape k = 1/σ, and the hazard k t^{k−1} e^{−x'γ/σ} is proportional in x with β = −γ/σ.
5. **The gamma frailty's population hazard.** S(t) = E e^{−Z H_0} = (1 + θ H_0)^{−1/θ}, the gamma Laplace transform.
   Then h_pop = −d log S/dt = h_0/(1 + θH_0). This equals E[Z | T > t] h_0, since the survivors' frailty is
   Gamma(1/θ, θ/(1 + θH_0)).
6. **RMST.** min(T, τ) = ∫_0^τ 1{T > t} dt. Take expectations and swap the order (Fubini): E min(T, τ) = ∫_0^τ S(t) dt.

## Glossary

- **Survival function; hazard; cumulative hazard**: P(T > t); the event rate among those at risk; its integral,
  −log S.
- **Right, left and interval censoring; truncation; delayed entry**: partial knowledge of T; not being seen at all
  unless T exceeds the entry time.
- **Risk set**: those still under observation and event-free just before t.
- **Kaplan–Meier; Greenwood; log-log interval**: the product-limit estimator; its variance; the interval on log(−log S).
- **Nelson–Aalen; life table**: the summed hazard; grouped-interval estimation.
- **Counting process; compensator; martingale**: N(t); the expected count ∫ Y h; their difference.
- **Log-rank test; weighted log-rank**: summed observed-minus-expected over risk sets; with weights.
- **Proportional hazards; partial likelihood; Breslow and Efron ties; Breslow's baseline**: Cox's model and its pieces.
- **Schoenfeld residuals; Grambsch–Therneau test; time-varying coefficient; stratification**: checking and relaxing PH.
- **RMST**: the area under S up to τ.
- **Immortal time; landmark analysis; target trial**: time in which the outcome could not occur; fixes.
- **AFT model; time ratio; cure fraction**: regression for log T; e^γ; the plateau.
- **Competing risks; cause-specific hazard; cumulative incidence; Aalen–Johansen; Fine–Gray**: other events that
  prevent the one of interest, and their tools.
- **Frailty; shared frailty; recurrent events**: unmeasured multiplicative risk; shared by a cluster; repeated events.
- **Concordance; IPCW Brier score; random survival forest; conformal lower bound**: prediction and its evaluation.

## Where it comes back

- **Part 41**: censoring as one kind of missing data; inverse probability weights.
- **Part 44**: martingales, counting processes and Rebolledo's central limit theorem.
- **Part 48**: the Kaplan–Meier curve as an empirical process.
- **Part 49**: Cox's estimator as a semiparametric efficient estimator.
- **Part 58**: monitoring survival trials as they accumulate.
