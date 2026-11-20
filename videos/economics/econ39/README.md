# Economics, Built: Part 39, The Wage Structure

Part 39 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second of Act VIII, *Work and the State*. It asks why some people are paid so
much more than others, and how much of the gap is unfair. Its answer: pay differs because skills differ, and skills
are rewarded more when technology outruns education; because machines took over the routine tasks of the middle;
because some firms pay more than others; and because some jobs are worse. But part of the gap is discrimination,
which experiments can measure, and much of the gender gap opens with the first child.

It opens on Marianne Bertrand and Sendhil Mullainathan's correspondence experiment, recomputed from the data: 4,870
invented résumés sent to 1,323 advertisements in Boston and Chicago in 2001-02, identical but for a randomly assigned
name. Résumés with White-sounding names were called back 9.65% of the time (one in ten), those with
African-American-sounding names 6.45% (one in fifteen): 50% more call-backs, with a 95% interval from 23% to 82%.
From there it covers:

- the wage distribution since 1979 (BLS, via FRED): the college premium for full-time workers rose from 1.38 in 1979
  to 1.73 in 1992 and 1.80 in 2025; the real median weekly wage rose 13% while output per hour grew 2.4 times; since
  2000 the 90/10 ratio widened at the top while the median moved closer to the tenth percentile; Autor and Dorn's
  wage growth by occupational percentile, 1980-2005, is U-shaped;
- the race between education and technology: the canonical model, Katz and Murphy's elasticity of 1.41; the same
  regression on 1992-2025 fails (trend and supply correlate 0.997, the implied elasticity is negative); with sigma
  fixed, relative demand for college workers grew 2.4% a year in the 1990s, 2.2% in the 2000s and 1.7% since 2010,
  against supply's pull of 1.9%;
- a game: twelve kinds of work, 1980-2005 (Autor and Dorn's data): machine operators fell 54%, precision crafts 38%,
  clerical work 11%; child care, health aides, financial sales and professionals grew;
- tasks, not skills (Autor, Levy and Murnane): employment polarization by percentile, 1980-2005; Agora's task model,
  in which automating a fifth of the tasks lowers the middle's wage relative to the bottom (1.26 to 1.20) and raises
  the top's relative to the middle (1.68 to 1.82);
- robots (Acemoglu and Restrepo): the Island's 300 commuting zones, where the naive slope (-0.68) triples the planted
  -0.2 until the manufacturing share is held fixed (-0.27, s.e. 0.045); America: -0.2 points of employment and -0.42%
  of wages per robot per thousand workers;
- firms: the two-way fixed-effects model on the Island's 20,000 workers and 400 firms (firm effects 11% of the
  variance, sorting 16%), the limited-mobility bias as movers become scarce, and West Germany (Card, Heining and
  Kline: firm effects 18.5% to 21.2%, sorting 2.3% to 16.4%);
- superstars (Rosen 1981) computed, and the labour share of the nonfarm business sector, down 14% since 1980, with
  Autor et al.'s superstar firms;
- an intermission without narration: the college premium, 1979-2025, as a tune;
- unions: membership 20.1% in 1983 and 9.9% in 2024; the union premium among 545 young men, 1980-87, is 0.182 by
  least squares but 0.080 within men; union pay is more compressed (CPS 1985);
- compensating differentials: Smith's passage; Rosen's hedonic wage locus on the Island; Mas and Pallais's call-centre
  experiment (20% of wages to avoid short-notice schedules, 8% to work from home);
- discrimination in theory: Becker's marginal employer, computed; Phelps's statistical discrimination and Arrow's
  self-fulfilling beliefs;
- discrimination measured: the résumés by city, sex and quality (a better résumé adds 2.3 points for White names, 0.5
  for African-American names); audits and correspondence studies; Quillian et al.'s meta-analysis (36% more
  call-backs, no change since 1989); Goldin and Rouse's blind auditions; an Oaxaca-Blinder decomposition of the CPS
  gender gap (1985: a gap of 0.23, almost none of it "explained") and its limits;
- the gender gap: women's median weekly earnings rose from 62% of men's in 1979 to 82% in 2025; Goldin's last
  chapter (long and particular hours); the child penalty, by an event study on the Island and in Denmark (about 20%);
  the Fact;
- three dials, all new (the elasticity of substitution between college and high-school workers, the firm share of
  wage variance, the call-back gap); pay audits; *Called it?* on Leontief's horses (1983: too early to say); a frontier
  chapter on pay transparency (Cullen and Pakzad-Hurson: wages about 2% lower) and hiring algorithms.

## Build it

```bash
python -m videos.economics.econ39.compute              # every number (about half a minute), into .cache/econ39/
python tools/qa_scene.py econ39 Firms                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ39 -q l   # the whole part, silent preview
python tools/build.py econ39                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 39                     # the lab
```

The data are in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): Bertrand and Mullainathan's résumés from the CRAN
package `openintro` (GPL-3); Autor and Dorn's replication files from David Dorn's data page, read by the Data Room's
own reader for old Stata files (`data/stata.py`, which parses bytes and evaluates nothing); Vella and Verbeek's union
panel and the 1978/1985 CPS from the CRAN package `wooldridge`; from FRED, the BLS's median weekly earnings by
education and sex, the deciles, employment by education, the labour share and prime-age employment; and tables from
Katz and Murphy, Card and Lemieux, Ciccone and Peri, Autor, Goldin and Katz, Autor, Levy and Murnane, Acemoglu and
Restrepo, Card, Heining and Kline, Autor et al., the BLS's union release, Mas and Pallais, Goldin and Rouse, Quillian et
al., Goldin, Kleven et al., Cullen and Pakzad-Hurson, Reuters and Leontief.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Emily, Greg, Lakisha and Jamal | The résumés and their call-backs, square by square; the question; objectives |
| 1 | The wage distribution since 1979 | The college premium; the real median; the deciles; wage growth by occupation |
| 2 | The race between education and technology | The canonical model; Katz and Murphy; the failed refit; demand's slowdown |
| 3 | Play it: what happened to twelve kinds of work | Guess; the shares 1980-2005; against 1980 pay and routineness |
| 4 | Tasks, not skills | Routine and non-routine; polarization; the task model with automation |
| 5 | Robots | The exposure design; the Island's zones; Acemoglu and Restrepo |
| 6 | Firms: the same worker, a different wage | AKM; the variance decomposition; Germany; limited-mobility bias |
| 7 | Superstars and the labour share | Rosen's reach; the labour share; superstar firms |
| — | Intermission | The college premium since 1979, as a tune |
| 8 | Unions | Membership; the premium within men; compression |
| 9 | Compensating differentials | Smith; the hedonic wage locus; the price of flexibility |
| 10 | Discrimination in theory | Becker's marginal employer; Phelps and Arrow |
| 11 | Discrimination measured | The résumés in detail; field experiments; Oaxaca-Blinder and its limits |
| 12 | The gender gap | Convergence; hours; the child penalty; the Fact |
| 13 | The Dials | Skill substitution; the firm share; the call-back gap |
| 14 | In practice | Who does this; a pay audit; *Called it?* on Leontief (1983) |
| 15 | Frontier | Pay transparency; hiring algorithms; open questions |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 40, *Inequality and Mobility* |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's labour module, part II
(`explainer.economics.agora.labour`), with the Island's Part 39 truths, or from the Data Room; the narration states
the cached numbers.

- **The résumés.** Call-back rates by the race the name signals; the ratio's interval by the delta method on the log
  rates; rates by city, by the sex of the name and by the study's own résumé-quality flag.
- **The premium.** Annual medians of usual weekly earnings for full-time wage and salary workers aged 25 and over with
  a bachelor's degree or more, over those of high-school graduates with no college; relative supply is the annual
  average of the employment levels of the same two groups (1992 on; 2025 averages the eleven months published).
- **The race.** The naive regression is least squares of the log premium on a trend and log relative supply,
  1992-2025; the demand index is the log premium plus log relative supply over sigma.
- **Polarization.** Autor and Dorn's employment shares by percentile of the 1980 occupational wage distribution
  (each percentile 1% of 1980 employment) and their wage changes, smoothed here by local linear regression with a
  Gaussian kernel of nine percentiles; the twelve groups aggregate their 330 occupations by Dorn's code ranges, with
  1980-weighted mean wages and routine task intensity.
- **The task model.** Tasks on [0, 1], Cobb-Douglas across tasks; low, middle and high skills with productivity
  exp(beta i), beta = 0, 1, 2, and equal supplies; machines take the band (0.40, 0.60).
- **Robots.** 300 zones with Dirichlet industry mixes over six industries adopting 8, 3, 3, 2, 0.5 and 0 robots per
  thousand workers; the employment rate changes by -0.2 per unit of exposure and by -3 points per unit of
  manufacturing share, with noise of 0.4 points.
- **Firms.** 20,000 workers and 400 firms over six years; worker effects with standard deviation 0.40, firm effects
  0.15, residuals 0.12; workers draw firms with a tilt towards high-premium firms (0.3) and a tenth move each year;
  AKM by sparse least squares (LSQR); the sweep reruns the economy with 0.5% to 20% moving.
- **Superstars.** 100,000 performers with lognormal talent (log standard deviation 0.10); earnings proportional to
  talent to the power 1, 3 or 8.
- **Unions.** Vella and Verbeek's 545 men, 1980-87: least squares with schooling, experience and its square,
  marriage, race and year effects; the within estimator with clustered standard errors. The 1985 CPS densities use
  Gaussian kernels with Silverman's bandwidth.
- **The hedonic locus.** 60 workers with lognormal distaste for risk (median 1) and 60 firms with lognormal costs of
  safety (median 2), matched assortatively.
- **Becker.** 10,000 employers; a share with no prejudice, the rest exponential with mean 0.15; minority workers an
  eighth of the labour force.
- **Oaxaca-Blinder.** Men's and women's log wages in the 1978 and 1985 CPS samples on schooling, experience and its
  square, union membership, race, marriage and region, with women's coefficients as the reference.
- **The child penalty.** 4,000 mothers and 4,000 fathers observed from five years before to ten after the first
  child (born at 20 to 40, in 1985 to 2015); a planted penalty for mothers of 0.30 in the first year, 0.25, 0.22 and
  0.20 at years 2, 5 and 10; event-time, age and year effects by least squares.

## Problems and solutions

**1.** *Call-backs: 235 of 2,435 résumés with White names, 157 of 2,435 with African-American names. Find each rate,
their ratio, and the number of résumés per call-back.*

*Solution.* 235/2,435 = 9.65% and 157/2,435 = 6.45%; the ratio is 1.50, so White names received 50% more call-backs.
A White-named applicant needed about 10.4 résumés per call-back, an African-American-named applicant about 15.5.

**2.** *The canonical model: with sigma = 1.4, by how much does the college premium fall if relative supply rises 10%
and demand does not move?*

*Solution.* The log premium falls by ln(1.1)/1.4 = 0.0953/1.4 = 0.068 log points: about 6.6%.

**3.** *The race: relative supply grows 2.7% a year and the premium is flat. With sigma = 1.41, how fast must relative
demand be growing?*

*Solution.* A flat premium needs the demand index to grow as fast as supply's pull, 2.7/1.41 = 1.9% a year. Any
faster and the premium rises.

**4.** *Unions: least squares gives a premium of 0.182; comparing the same men gives 0.080. What share of the
cross-sectional gap is selection, and what does the within estimate assume?*

*Solution.* (0.182 - 0.080)/0.182 = 56% of it reflects who joins rather than what unions pay. The within estimate
assumes that changes in union status are unrelated to changes in a man's other prospects, and that the premium is
the same for joiners and leavers; misclassified union status, which differencing amplifies, biases it towards zero.

**5.** *Becker: a fifth of workers are in the minority and 30% of employers have no prejudice. What is the market gap?
And if the minority were 40%?*

*Solution.* The unprejudiced employers can hire every minority worker, so the marginal employer has no prejudice and
the gap is zero. With a 40% minority some prejudiced employers must hire minority workers; the gap equals the taste
of the employer at the 40th percentile of prejudice, which is positive.

**6.** *Phelps: productivity has variance 1 and mean 0 in both groups; test noise has variance 0.25 for A and 1 for B.
What is each group's pay at a score of 2?*

*Solution.* lambda_A = 1/(1 + 0.25) = 0.8 and lambda_B = 1/(1 + 1) = 0.5, so pay is 0.8 × 2 = 1.6 for A and
0.5 × 2 = 1.0 for B: the same score, different pay, with no difference in average ability.

**7.** *Oaxaca-Blinder: men average 13.0 years of school, women 12.6; the return for women is 0.08; the gap is 0.23. How
much is "explained" by schooling?*

*Solution.* (13.0 - 12.6) × 0.08 = 0.032, about 14% of the gap; the remaining 0.198 is "unexplained" by schooling,
which is not the same as discrimination.

**8.** ★ *AKM: show that with n_j movers per firm, the plug-in variance of firm effects exceeds the true variance by
roughly the average sampling variance, sigma²_e × mean(2/n_j).*

*Solution.* A firm's premium is identified by its movers' wage changes: each change is the difference of the two
firms' premiums plus the difference of two residuals, with variance 2 sigma²_e. Averaging over n_j movers gives
psi_hat_j = psi_j + e_j with Var(e_j) ≈ 2 sigma²_e / n_j and e_j uncorrelated with psi_j. So E[Var(psi_hat)] ≈ Var(psi)
+ mean(2 sigma²_e / n_j): noise inflates the estimated dispersion of firm effects. The worker effects absorb -e_j
for the firm's stayers, so the estimated covariance of worker and firm effects is pushed down, which is why few
movers make sorting look weak or even negative (chapter 6).

## Lab and interactive

- `python -m videos.economics.labs 39`: the résumés; the premium and the naive Katz-Murphy regression; the demand
  index; polarization; the task model; robots with and without the control; AKM against the truth; the union premium
  within men; Becker's gap; an Oaxaca-Blinder split; the child penalty.
- The interactive (course site): the race between education and technology. The reader sets the elasticity of
  substitution and the growth of demand and supply, and compares the premium they imply with the one the BLS
  measured since 1979.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[39]`; the three dials are in
`explainer/economics/dials.py`; Leontief's 1983 remark is a *Called it?* entry (`explainer/economics/calls.py`); the
child penalty is a Fact (`explainer/economics/facts.py`). FRED's series were retrieved on 2026-11-20; the October 2025
household survey was not collected, so 2025's employment averages eleven months. Bertrand and Mullainathan's, Goldin
and Rouse's, Goldin's, Kleven et al.'s, Autor and Dorn's and Mas and Pallais's results were read from the AEA's
abstracts (Kleven et al.'s 40% and 80% from NBER Working Paper 24219); Katz and Murphy's coefficient from Blanchard's
account; Card and Lemieux's, Ciccone and Peri's and Autor, Goldin and Katz's from their abstracts; Card, Heining and
Kline's shares from Table 3 of NBER Working Paper 18522; Acemoglu and Restrepo's from the JPE abstract; the union
figures from the BLS's January 2025 release; Quillian et al.'s from the PNAS paper's summary; Cullen and
Pakzad-Hurson's from the Econometrica abstract; the Amazon report from syndicated copies of Reuters's story; Leontief's
remark from secondary listings of the 1983 symposium. Goldin and Rouse's often-quoted "50 percent" is not in their
abstract, which stresses that some estimates are imprecise; the film states only what the abstract does.
