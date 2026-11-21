# Economics, Built: Part 54, Estimating Models

Part 54 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth of Act X, *The Graduate Core*. It asks how a model's hidden machinery is
measured from the choices it predicts. Its answer: by writing down how the choices would follow from the hidden
parameters, and finding the values under which the model reproduces what people did, by likelihood when the model
gives probabilities, by moments when it gives only averages, and by simulation when it gives neither; then by asking
what in the data pins each value down, how far the answer leans on assumptions the data cannot check, and whether the
model predicts what it was never shown.

It opens on the Bay Area's new railway: the official forecast said about 15% of work trips would use BART; Daniel
McFadden's model, estimated from a survey of commuters' choices before a train ran, said 6.3%; in 1975 it was 6.2%.
Everything after that is done on the Island, where the truth was planted, so every estimate can be graded:

- what structural means (Marschak, Lucas): twelve years of fuel prices and the share who drive; a straight line fits
  the history (each dollar, about ten points fewer drivers) and, asked about an $8 congestion charge, says -33% would
  drive; the logit says 2.1%, the truth 2.7%;
- random utility and maximum likelihood: the logit from extreme-value errors, its S-curve through 3,000 commuters'
  choices, the likelihood surface climbed by Newton's method in five steps, the estimates (-0.062 a minute, -0.536 a
  dollar, against -0.06 and -0.5) and the value of time, $6.96 an hour (standard error 0.41; planted $7.20); a railway
  forecast whose total is close (44% against 43%) but which draws riders from the car too often (the logit leaves 25%
  driving, the nested truth 30%), the independence of irrelevant alternatives and the nested logit;
- Play it: patience and caution both make the Island's households save; which of four facts (consumption growth while
  young, wealth before retirement, wealth in the last years, consumption's change at retirement) tells them apart?
  None: on every fact one more unit of caution does what about 0.011 more patience does, so the four lines of values
  that leave each fact unchanged lie almost on top of each other;
- the generalized method of moments (Hansen 1982) and Hansen and Singleton's Euler equation, estimated without solving
  the model on 2,000 periods of the Island's consumption growth and two assets' returns: beta 0.969 (0.002) and risk
  aversion 2.90 (0.11) against 0.97 and 3; J = 11.3 on 6 degrees of freedom, not rejected; an asset paying one point a
  period more than the model can price gives J = 67 on 13, rejected;
- simulation (McFadden 1989, Pakes and Pollard 1989): simulated moments with fixed draws and the (1 + 1/S) price;
  indirect inference (Gouriéroux, Monfort and Renault 1993) for a moving average through an autoregression, with half
  the error of the first-autocorrelation estimator in 300 samples (0.071 against 0.131);
- the Island's life-cycle households estimated by simulated moments after Gourinchas and Parker: sixteen moments of
  3,000 households, 138 solved and simulated economies from a start of (0.93, 3), patience 0.9505 (0.0004) and caution
  1.95 (0.04) against 0.95 and 2, J = 6.4 on 14, and a correlation between the two estimates of -0.9999;
- an intermission film of America's vehicle miles travelled over the past twelve months, 1971-2026 (1.1 trillion to
  3.3), with its 2007 plateau and the pandemic's dip, as a line and a tune;
- dynamic choice (Rust, Hotz and Miller, Keane and Wolpin) and hidden types: 800 commuters for 8 weeks, two planted
  types and no habit; one logit for everybody finds a response of 0.63 (truth 0.8) and a habit of 1.16 (standard error
  0.05) that does not exist, Heckman's spurious state dependence; a two-type mixture by EM finds 0.85, a share of 0.40
  and a habit of 0.10;
- identification (Koopmans) and Andrews, Gentzkow and Shapiro's sensitivity matrix: how far caution's estimate moves
  if each of the sixteen facts were 1% higher (up to 5.7, against a standard error of 0.04); a survey that overstates
  wealth by 1% moves it by -1.45 as predicted and -1.50 when estimated again, 38 standard errors;
- calibration against estimation (Kydland and Prescott; Hansen and Heckman): fix caution from the Dial and estimate
  patience; caution 1 gives patience 0.961, caution 4 gives 0.927, and only near 2 does the fit pass the J-test
  (J = 529 at 1, 2,417 at 4, 7.7 at 2);
- sufficient statistics (Baily, Chetty): on Part 42's unemployment-insurance model, the formula built from the
  consumption drop and one elasticity crosses zero exactly where welfare peaks (33% of the wage); an analyst with one
  experiment at 20% who assumes the elasticity never changes puts the optimum at 50%;
- validation (Todd and Wolpin on PROGRESA): a schooling model estimated on control villages predicts a subsidy's
  effect of 18.2 points and the experiment finds 18.1; in a world where parents respond to what the money is for, the
  same model still predicts 18.2 and the experiment finds 30.3;
- bounds (Manski): with about a fifth of attendance records missing, the effect lies between -6% and 35% with no
  assumption, between 5% and 28% if the missing attend no more often than the rest; the truth, 18.1%, is inside both;
- the Dials: relative risk aversion, contested because each method leans on different facts, and the discount factor
  of Part 44's buses, not identified;
- in practice (transport appraisal, merger simulation, central banks' Bayesian models, pricing teams, UberX's consumer
  surplus) and *Called it?* on Google Flu Trends (partly right); a frontier of learned estimators (an MA(1) estimated
  from summaries with a typical error of 0.058 after 3,000 simulated samples) and open questions.

## Build it

```bash
python -m videos.economics.econ54.compute              # every number (about three minutes), into .cache/econ54/
python tools/qa_scene.py econ54 LifeCycle              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ54 -q l   # the whole part, silent preview
python tools/build.py econ54                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 54                     # the lab
```

The only data are the Federal Highway Administration's vehicle miles travelled, via FRED, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md); every other number is computed.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The railway forecast | BART: the official forecast, McFadden's, and what happened; the question; objectives |
| 1 | What "structural" means | Reduced form and structure; a line through history asked about a congestion charge |
| 2 | Random utility and maximum likelihood | The logit; its curve; the likelihood surface; the value of time; a railway |
| 3 | Play it: which fact pins down which parameter? | Four facts, two parameters; the lines that coincide |
| 4 | The generalized method of moments | Moment conditions; Euler equations; the J-test |
| 5 | When the likelihood has no formula | Simulated moments; indirect inference; 300 samples |
| 6 | The Island's households, estimated | Sixteen moments; the fit; the truth recovered on a ridge |
| — | Intermission | America's vehicle miles, 1971-2026, as a line and a tune; the story so far |
| 7 | Dynamic choices and hidden types | Nested fixed points; spurious habit; a mixture by EM |
| 8 | Identification | The sensitivity matrix; a 1% error in wealth |
| 9 | Calibration against estimation | The debate; borrowed caution and estimated patience |
| 10 | Sufficient statistics | The formula against the model; one elasticity extrapolated |
| 11 | Validation: predict the experiment | PROGRESA; the Island's subsidy, twice |
| 12 | Bounds instead of points | Manski's intervals with and without an assumption |
| 13 | The Dials: how averse to risk? | Risk aversion by method; the discount factor, not identified |
| 14 | In practice: estimation as a job | Where models are estimated; *Called it?* (partly right) |
| 15 | Frontier: learned estimators | Simulation-based inference; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 55, *Identifying Macro* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's estimation harness (`explainer.economics.agora.estimate`),
the Island's Part 54 truths and, for sufficient statistics, Part 42's model (`agora.insurance`); the narration states
the cached numbers.

- **Commuters.** 3,000 commuters; car 15-45 minutes and $2-8, bus 25-70 minutes and $0.5-2.5; utility -0.06 a minute,
  -0.5 a dollar, a bus constant of -0.4, Gumbel errors. The logit by Newton's method from zero; its log likelihood on a
  49 x 45 grid of the two weights with the constant at its estimate; the value of time by the delta method.
- **History.** Twelve years in which fuel moved a car trip's cost by -$1 to +$1.50; shares from the true logit with
  binomial sampling; a least-squares line; an $8 charge.
- **Rail.** 35 minutes and $2.50; the truth a nested logit with bus and rail in one nest (lambda 0.5) and a rail
  constant of -0.2; the forecast the estimated logit with that constant.
- **Play it.** The life-cycle model below at the truth; four summary moments from the households' bins; their
  derivatives by central differences with common random numbers; the 95% region from their efficient combination.
- **GMM.** Consumption growth an AR(1) (mean 2%, persistence 0.3, s.d. 2%); returns that satisfy the Euler equation
  exactly with beta 0.97 and gamma 3 plus noise (s.d. 3% and 12%); instruments a constant and the lagged growth and
  returns; two-step GMM with Nelder-Mead; a third asset with a premium of 1% a period.
- **Indirect inference.** MA(1) with theta 0.5; an AR(3) lens; 10 simulated paths; 300 samples of 200.
- **Life cycle.** 50 years (40 working with a hump-shaped income profile and a Rouwenhorst shock with persistence 0.95
  and s.d. 0.15; 10 on a pension of 40% of last earnings), R = 1.03, no borrowing, solved by the endogenous grid method;
  3,000 households; consumption in ten five-year bins and wealth in the last six; 5 simulated populations; efficient
  weights; the profile over 13 values of caution; the 1% wealth test estimated again.
- **Types.** 800 people, 9 weeks (the first used only as a lag), 40% with constant -1.5 and 60% with 1.0, response 0.8,
  no state dependence; pooled logits and two-type mixtures by EM.
- **Sufficient statistics.** Part 42's static model (gamma 2, A 3, theta 0.3856, kappa 11.81) on 59 benefits from 0.02
  to 0.6.
- **Validation and bounds.** 200 villages of 60 children; wages $5-30; attendance a logit in a trait and the wage net of
  a $10 subsidy in a random half; a second world adding 0.6 for the subsidy's label; records missing with probability
  0.12 for attenders and 0.3 for the rest.
- **Learned estimator.** 3,000 simulated MA(1) samples of 400 with theta uniform on (-0.9, 0.9); a cubic regression from
  the first three autocorrelations; 300 test samples.

## Problems and solutions

**1.** *The logit: if the unseen parts of the utility of car and bus are independent extreme-value draws, show that
the chance of the bus is e^V_bus / (e^V_car + e^V_bus).*

*Solution.* With standard Gumbel errors, the difference of two independent draws has the logistic distribution,
Pr(e_car - e_bus <= x) = 1/(1 + e^-x). The bus is chosen when V_bus + e_bus > V_car + e_car, that is when
e_car - e_bus < V_bus - V_car, which has probability 1/(1 + e^-(V_bus - V_car)) = e^V_bus / (e^V_car + e^V_bus).

**2.** *The value of time: with weights of -0.06 a minute and -0.5 a dollar, what is an hour worth? Give its standard
error by the delta method.*

*Solution.* A minute is worth 0.06/0.5 = $0.12, an hour 60 x 0.12 = $7.20. The value is v = 60 b_t / b_c, with
gradient (60/b_c, -60 b_t / b_c^2); its variance is that gradient times the covariance of the two estimates times the
gradient again. With the film's estimates and covariance it gives $6.96 with a standard error of 0.41.

**3.** *The red bus and the blue bus: car and a red bus are chosen equally often; a blue bus identical to the red one is
added. What does the logit predict, and what would you expect?*

*Solution.* With equal utilities the logit gives each of the three options a third, so the car's share falls from 1/2
to 1/3. One would expect the blue bus to take only red-bus riders: car 1/2, each bus 1/4. The logit's independent
errors treat the blue bus as a genuinely new option; a nested logit with the two buses in one nest and lambda near 0
gives the expected answer.

**4.** *GMM: for y = x beta + u with instruments z, show that GMM with W = (Z'Z)^-1 is two-stage least squares.*

*Solution.* The conditions are E[z(y - x beta)] = 0, with sample average g = Z'(y - X b)/n. Minimizing g'Wg gives the
first-order condition X'Z W Z'(y - X b) = 0, so b = (X'Z W Z'X)^-1 X'Z W Z'y. With W = (Z'Z)^-1 this is
(X'P X)^-1 X'P y with P = Z(Z'Z)^-1 Z', which is two-stage least squares.

**5.** *Hansen's J: with eight conditions and two parameters, J = 11.3. Is the model rejected at 5%? At 10%?*

*Solution.* There are 8 - 2 = 6 degrees of freedom. The chi-squared critical values are 12.59 at 5% and 10.64 at 10%,
so the model is not rejected at 5% but is at 10% (p = 0.08), as in the film.

**6.** *Simulated moments: why must the random draws be the same at every guess? By how much does S = 5 inflate the
variance?*

*Solution.* With fresh draws the simulated moments change between two guesses even when the parameters barely do, so
the objective is not a smooth function of the parameters and an optimizer cannot climb it; fixing the draws makes it
smooth. The simulated moments average S samples, so their noise adds 1/S of the data's sampling variance: the
estimate's variance is (1 + 1/S) times that of the infeasible estimator with exact moments, 1.2 for S = 5.

**7.** *Spurious habit: with two types and no habit, show that Pr(y_t = 1 | y_t-1 = 1) > Pr(y_t = 1 | y_t-1 = 0).*

*Solution.* Let the types have chances p_H > p_L of choosing 1 each period, independently over time, and shares s and
1 - s. Then Pr(y_t = 1 | y_t-1 = 1) = (s p_H^2 + (1 - s) p_L^2)/(s p_H + (1 - s) p_L), the average of p weighted by
p, which exceeds the average of p weighted by 1 - p, Pr(y_t = 1 | y_t-1 = 0). Last period's choice says which type
someone probably is; it changes nothing about them.

**8.** *Manski: outcomes lie in [0, 1] and shares p_1 and p_0 of the two arms are missing. Show that the no-assumption
bound on the effect has width p_1 + p_0.*

*Solution.* In arm a the mean lies between (1 - p_a) m_a and (1 - p_a) m_a + p_a, where m_a is the observed mean: an
interval of width p_a. The effect's lower bound is the treated arm's lowest mean minus the control arm's highest, the
upper bound the reverse, so its width is p_1 + p_0: about 0.41 in the film, with a fifth of records missing in each
arm.

## Lab and interactive

- `python -m videos.economics.labs 54`: the commuters' logit and value of time; the railway forecast against the nested
  truth; GMM on the Euler equation with the J-test; indirect inference against the naive estimator; the hidden-types
  panel; the subsidy validation; Manski's bounds.
- The interactive (course site): estimate. The reader is handed the Island's commuters with the truth hidden, adjusts the
  weights on minutes and dollars by hand to raise the likelihood, sees the value of time implied, and then reveals the
  truth and the maximum.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[54]`; the risk-aversion and discount-factor
dials are in `explainer/economics/dials.py`; Google Flu Trends is a *Called it?* entry (`explainer/economics/calls.py`),
and BART is Part 5's; the vehicle miles are in the Data Room. Checked on 2026-11-21: Todd and Wolpin's design and
finding (estimation on the control villages, predictions that track the experimental impacts, and a better subsidy
schedule at similar cost), stated without numbers; Lazer and colleagues' account of Google Flu Trends (about twice the
CDC's figure in the 2012-13 season, three-week-old CDC data doing better); Cohen and coauthors' estimate of UberX's
consumer surplus in four cities in 2015. Gourinchas and Parker's own estimates are not shown, since their published
point estimates could not be checked here; the film uses their method only. The models are stated from the papers cited
in the chapters (Koopmans 1949, Marschak 1953, McFadden 1974 and 1989, Lucas 1976, Baily 1978, Heckman 1981, Hansen
1982, Hansen and Singleton 1982, Kydland and Prescott 1982 and 1996, Heckman and Singer 1984, Rust 1987, Pakes and
Pollard 1989, Manski 1990, Gouriéroux, Monfort and Renault 1993, Hotz and Miller 1993, Smith 1993, Hansen and Heckman
1996, Keane and Wolpin 1997, Gourinchas and Parker 2002, Todd and Wolpin 2006, Smets and Wouters 2007, Chetty 2009,
Andrews, Gentzkow and Shapiro 2017, Cranmer, Brehmer and Louppe 2020, Horton 2023) and computed here.
