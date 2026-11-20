# Economics, Built: Part 38, Work and Wages

Part 38 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first of Act VIII, *Work and the State*. It asks what sets a wage, and what
happens when the law sets it instead. Its answer: wages are set by the value of what people produce, by their skills,
which a year of school raises by roughly six to fifteen percent, and by their choices about how much and where to
work; but employers often have some power to set pay. When the law sets a moderate minimum, jobs barely fall; how high
it can go before they do is still being measured.

It opens on David Card and Alan Krueger's telephone survey of 410 fast-food restaurants either side of the Delaware in
1992, before and after New Jersey raised its minimum from $4.25 to $5.05, and recomputes their result from the public
data: full-time-equivalent employment per restaurant went from 20.44 to 21.03 in New Jersey and from 23.33 to 21.17 in
Pennsylvania, a difference in differences of +2.75. From there it covers:

- a game: predict what the higher minimum did; then the answer, with starting wages before and after in both states;
- labour supply with income effects, solved by Agora: hours rise with the wage and bend back above $14; the
  Marshallian elasticity (+0.16 at $6, −0.11 at $30), the income effect, the Hicksian elasticity by Slutsky's equation
  (+0.39 and +0.30) and the Frisch elasticity (0.5); participation; Chetty, Guren, Manoli and Weber's synthesis;
- cab drivers: daily income targets (Camerer, Babcock, Loewenstein and Thaler, 1997) against the standard model
  (Farber's every New York taxi trip, 2009-2013; Angrist, Caldwell and Hall's Uber experiment, a Frisch elasticity
  near 1.2);
- labour demand and a wage floor in a competitive market: a minimum 19% above the market wage costs 8.3% of the jobs
  when demand's elasticity is 0.5, and leaves more people wanting work than are hired;
- the border design and its critics: the own-wage elasticity recomputed (+0.97, 90% bootstrap interval −0.05 to
  2.09), entrée prices (+3.1% in New Jersey, −1.1% in Pennsylvania), Neumark and Wascher's payroll records and Card
  and Krueger's reply;
- the bunching estimator (Cengiz, Dube, Lindner and Zipperer: 138 state increases, 1979-2016, elasticity 0.41 with a
  standard error of 0.43) and Seattle's high minimum (Jardim et al.: hours at low wages fell, elasticities −2.0 to
  −0.2);
- monopsony, from Joan Robinson to Alan Manning: one employer hires 136 workers at $5.15 where a competitive market
  would hire 215 at $5.99, a 25% markdown; a minimum anywhere between the two raises employment, and only above $5.99
  does it cost jobs; Sokolova and Sorensen's 801 estimates of the supply elasticity facing a firm;
- the same design run on the Island, 200 times in each world: when restaurants hire on competitive demand curves the
  design finds −0.045 on average (negative in 83% of runs); when they set wages, +0.197 (never negative); New Jersey's
  +0.102 sits with the monopsony runs, but one run's standard error is about 0.045;
- an intermission without narration: the federal minimum wage in 2025 dollars, 1938-2025 (the Department of Labor's
  rate and the BLS's consumer prices, via FRED), as a tune: its real peak was $14.65 in 1968; it has been $7.25 since
  2009;
- human capital and Mincer's equation: Card's 3,010 young men in 1976, log wages by schooling (about 5% a year raw,
  with bumps at twelve and sixteen years); Mincer's equation fitted to 526 workers in the 1976 Current Population
  Survey (9.0% a year, standard error 0.8 points; experience peaks at 29 years; R² 0.30); the Fact;
- the return to schooling: ability bias with IQ (935 men in 1980: 0.075 falls to 0.056), Card's college-distance
  instrument recomputed (least squares 0.075; instrumental variables 0.131, standard error 0.054, first-stage F 13),
  Angrist and Krueger's quarter of birth, Bound, Jaeger and Baker's weak instruments, and Oreopoulos's British
  school-leaving age;
- selection: Roy's model on the Island (fishers and boatbuilders, each choosing the trade that pays them more), and
  Heckman's two steps: the fishers we see average 2.692 in logs, everyone 2.599, the correction gives 2.594;
- immigration and the Mariel boatlift, read three ways: Card (1990), Borjas (2017: −10 to −30% for a narrow group) and
  Peri and Yasenov (2019);
- three dials: the minimum wage's employment elasticity (new, contested), the return to schooling (three new rows) and
  labour supply (filled); *Called it?* on the 1979 survey of economists (90% of 211 agreed a minimum wage raises
  unemployment among the young and unskilled: partly right); a frontier chapter on employer concentration,
  non-competes, high minimums, the return to college and platform work.

## Build it

```bash
python -m videos.economics.econ38.compute              # every number (about a minute), into .cache/econ38/
python tools/qa_scene.py econ38 Monopsony              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ38 -q l   # the whole part, silent preview
python tools/build.py econ38                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 38                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Card and Krueger's public file of 410 restaurants (from
David Card's data archive at Berkeley); three datasets from the CRAN package `wooldridge` (GPL-3): Card's 1995 young
men from the National Longitudinal Survey, the 1976 Current Population Survey extract and the 1980 National
Longitudinal Survey extract with IQ scores; from FRED, the federal minimum wage and consumer prices; and tables
transcribed from Card and Krueger, Neumark and Wascher, Cengiz et al., Jardim et al., the cab-driver studies, Chetty
et al., Sokolova and Sorensen, Angrist and Krueger with Bound, Jaeger and Baker, Oreopoulos, the Mariel studies and
Kearl et al.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Four hundred and ten phone calls | Card and Krueger's restaurants either side of the Delaware; the question; objectives |
| 1 | Play it: a minimum wage a fifth higher | Predict; employment before and after; starting wages in both states |
| 2 | Labour supply | Hours with income effects; the backward bend; three elasticities and Slutsky; participation |
| 3 | Do people choose their hours? | Targets against the standard model; New York's cabs and Uber in Boston |
| 4 | Labour demand and a wage floor | The competitive prediction: fewer jobs, more people wanting them |
| 5 | The border design | The own-wage elasticity and prices recomputed; payroll records and the reply |
| 6 | Missing jobs, excess jobs | The bunching estimator; 138 state increases; Seattle |
| 7 | Monopsony | Robinson's one buyer; the markdown; a minimum wage that adds jobs; Manning |
| 8 | The same design on the Island | Card and Krueger's design run 200 times under each theory |
| — | Intermission | The real federal minimum wage since 1938, as a tune |
| 9 | Human capital and Mincer's equation | Becker; log wages by schooling; Mincer fitted; the Fact |
| 10 | The return to schooling | Ability bias; college distance as an instrument; quarter of birth; Britain in 1947 |
| 11 | Selection: Roy's model | Fishers and boatbuilders on the Island; Heckman's correction |
| 12 | Immigration: the Mariel boatlift | Miami in 1980, read three ways |
| 13 | The Dials | The minimum wage; the return to schooling; labour supply |
| 14 | In practice | Minimum-wage commissions, pay bands, people analytics; *Called it?* on the 1979 survey |
| 15 | Frontier | The real minimum and California's $20; concentration, non-competes, platforms |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 39, *The Wage Structure* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's labour module (`explainer.economics.agora.labour`) with the
Island's Part 38 truths, or from the Data Room; the narration states the cached numbers.

- **Card and Krueger.** Full-time equivalents are full-time workers plus managers plus half the part-time workers, as
  in the paper; the six restaurants that closed count as zero in the second wave. Means use every store that answered
  in each wave; the standard error of the difference in differences uses the balanced panel. The own-wage elasticity
  is New Jersey's proportional change in employment relative to Pennsylvania's, divided by the same for the starting
  wage, with a 90% interval from 2,000 bootstrap resamples of stores within each state. Entrée prices are the change
  in the mean log price of a meal's main item.
- **Labour supply.** A person maximizes c^(1−γ)/(1−γ) − ψ h^(1+1/φ)/(1+1/φ) with c = w h + y, with γ = 2, φ = 0.5,
  ψ = 1 and non-labour income y = 5 (dollars an hour's worth); hours are a share of the week. The elasticities are
  numerical derivatives; participation has lognormal reservation wages with median $12 and log standard deviation 0.5.
- **The competitive market.** Demand 100 w^(−0.5), supply 4 w: the market wage is $8.55; the floor is 18.8% above it.
- **Monopsony.** The value of the marginal worker 30 L^(−0.3); labour supply to the firm L = w³ (an elasticity of 3).
- **The Island's border.** The same 331 and 79 restaurants, with lognormal sizes (median 20 workers) and their own
  competitive wages around $4.60; the same rise from $4.25 to $5.05; a common trend of −6% and store-level noise of
  25% in employment. Under competition a store pays the larger of its competitive wage and the minimum and hires on a
  demand curve with elasticity 0.5; under monopsony it faces supply with elasticity 3. Each world is run 200 times.
- **Mincer.** Least squares of the log wage on schooling, experience and its square, with robust standard errors, on
  the 526 workers of Wooldridge's 1976 CPS extract.
- **College distance.** Card's specification: the log wage in 1976 on schooling, experience and its square, race,
  residence in a metropolitan area and in the South in 1976, residence in a metropolitan area in 1966 and eight
  regional dummies for 1966; the instrument is a four-year college in the county at age 14. Two-stage least squares
  with robust standard errors gives 0.1315 (0.054), Wooldridge's Example 15.4 (0.132, 0.055).
- **Ability.** The log wage on schooling, experience and tenure, with and without IQ, for 935 men in the 1980 survey.
- **Roy.** 20,000 islanders with jointly normal log wages in fishing (mean 2.6, standard deviation 0.4) and the
  boatyard (2.5, 0.6), correlation 0.3, and a cost of the boatyard drawn independently (standard deviation 0.3) and
  observed. Heckman's first step is a probit of choosing fishing on the cost; the second adds the inverse Mills ratio.
- **The intermission.** The annual average of the federal minimum wage, deflated by the annual average of the
  consumer price index for all urban consumers to 2025 dollars.

## Problems and solutions

**1.** *Difference in differences: New Jersey's restaurants went from 20.44 to 21.03 full-time-equivalent employees,
Pennsylvania's from 23.33 to 21.17. Find the effect, and say what it assumes.*

*Solution.* (21.03 − 20.44) − (21.17 − 23.33) = 0.59 + 2.16 = +2.75 employees per restaurant. It assumes that without
the rise New Jersey's employment would have changed by as much as Pennsylvania's (parallel trends), and that nothing
else hit one state and not the other between the two waves.

**2.** *Slutsky: at a high wage the Marshallian elasticity of hours is −0.11 and the income effect, w ∂h/∂y, is
−0.40. Find the Hicksian elasticity.*

*Solution.* ε^H = ε^M − w ∂h/∂y = −0.11 − (−0.40) = +0.29, about 0.3. The compensated response is positive, as it must
be; the raw response is negative only because the income effect of a higher wage outweighs it.

**3.** *The textbook floor: with a demand elasticity of 0.5, how much does employment fall when a minimum is set 19%
above the market wage?*

*Solution.* Employment is on the demand curve, L ∝ w^(−0.5), so it falls to 1.188^(−0.5) ≈ 0.917 of its old level:
−8.3%. Supply at the higher wage rises by 18.8% (elasticity one), so the gap between those wanting work and those
hired is about 27% of the old employment.

**4.** *Monopsony: with a supply elasticity of 3 facing the firm, how far below the value of the marginal worker is the
wage? With 10?*

*Solution.* The firm sets MRPL = w (1 + 1/η), so (MRPL − w)/MRPL = 1/(1 + η): 25% with η = 3, 9% with η = 10. The more
easily workers can leave, the less power the employer has.

**5.** *Mincer: with a return of 0.09, how much more does someone with four more years of school earn?*

*Solution.* 4 × 0.09 = 0.36 log points, so e^0.36 ≈ 1.43: about 43% more. (Not 36%: log points compound.)

**6.** *Ability bias: least squares gives 0.075; adding IQ gives 0.056, with 0.0055 per IQ point, and IQ is 3.5
points higher per year of school. Check the omitted-variable formula.*

*Solution.* The short regression's coefficient is the long one plus the omitted variable's coefficient times the
regression of the omitted variable on the included one: 0.056 + 0.0055 × 3.53 = 0.056 + 0.019 = 0.075. The formula
holds exactly when the auxiliary regression includes the same controls; here the gap is in the fifth decimal.

**7.** *The Wald estimator: men who grew up near a college average 13.53 years of school and a log wage of 6.311; those
who did not, 12.70 and 6.156. Estimate the return.*

*Solution.* (6.311 − 6.156)/(13.53 − 12.70) = 0.155/0.83 ≈ 0.19. Without controls, distance to a college also picks
up living in a city and in the North, where wages are higher; with Card's controls the estimate is 0.13.

**8.** ★ *Heckman: for jointly normal errors with unit-variance v, derive E[ε | v > −Zγ] = σ_εv φ(Zγ)/Φ(Zγ).*

*Solution.* Write ε = σ_εv v + u with u independent of v (the regression of ε on v). Then E[ε | v > −c] =
σ_εv E[v | v > −c]. For a standard normal, E[v | v > −c] = ∫_{−c}^{∞} v φ(v) dv / (1 − Φ(−c)) = φ(−c)/Φ(c) =
φ(c)/Φ(c), since φ′(v) = −v φ(v) and φ is symmetric. With c = Zγ, the selected sample's mean error is σ_εv times the
inverse Mills ratio, so adding the ratio as a regressor removes the bias, and its coefficient estimates σ_εv.

## Lab and interactive

- `python -m videos.economics.labs 38`: Card and Krueger's difference in differences from the restaurants; labour
  supply's elasticities with Slutsky checked; a competitive floor; monopsony and the minimum wage that maximizes
  hiring; the border design on the Island; Mincer on the 1976 CPS; Card's instrument; ability bias; Roy and Heckman.
- The interactive (course site): a minimum wage at a firm that sets wages. The reader sets the minimum and how elastic
  the supply of workers to the firm is, and watches hiring rise, peak at the competitive wage and fall.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[38]`; the minimum wage's employment
elasticity is a new dial, the return to schooling gains three rows and labour supply is filled
(`explainer/economics/dials.py`); the 1979 survey is a *Called it?* entry (`explainer/economics/calls.py`). Card and
Krueger's data are the public file from David Card's archive, checked by SHA-256; Wooldridge's data are from the CRAN
package, read without evaluating anything. FRED's series were retrieved on 2026-11-20. Card and Krueger's sample and
dates, Neumark and Wascher's payroll sample, Cengiz et al.'s events and elasticity, Jardim et al.'s elasticities,
Chetty et al.'s synthesis, Sokolova and Sorensen's count, Oreopoulos's leaving ages and the 1979 survey's share were
read from the published abstracts or articles; Angrist and Krueger's 25% from their paper's summary; the Mariel
arrivals and labour-force shares from Card (1990). The Federal Trade Commission's 2024 rule on non-compete agreements
is described only as adopted and set aside by a federal court; it never took effect.
