# Economics, Built: Part 4, The Evidence

Part 4 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last of Act I, *The Question*. It asks when data can answer an economic
question, and answers: when something moved one thing and nothing else (a storm, a lottery, a birthday, a border),
found in the world or made on purpose; when you can say what it moved and for whom; and when the answer will survive
the policy it informs.

It opens in 1914, when Henry Moore fitted lines through the prices and quantities of pig iron, found that his
"law of demand" sloped up, and called it a new kind of demand curve; Philip Wright's review the next year explained
what had happened, and Elmer Working's question of 1927 (what do statistical demand curves show?) frames the part.
From there it covers:

- a game: the Island's fish market, 240 days of prices and quantities, four candidate lines, and the planted truth;
- simultaneity: each day where two shifting lines cross; the four kinds of day; the probability limit of least
  squares as a weighted mixture of the two slopes;
- the instrument: storms move supply and trace demand, feasts move demand and trace supply; the Wald ratio and two-
  stage least squares; Wright's Appendix B (1928), its arrows, and Stock and Trebbi's stylometry (2003);
- Haavelmo (1944) and the Cowles Commission: systems of equations, identification, exclusions as assumptions;
- omitted variables and selection: the Island's school records, the omitted-variable bias by formula, a new school
  as an instrument, and Ashenfelter's dip;
- Leamer's "con" (1983) and LaLonde's test (1986): the National Supported Work experiment against the methods of the
  day, and Dehejia and Wahba's sequel; *Called it?*: wrong, and wrong in sign;
- an intermission without narration: the draft lottery of 1 December 1969, capsule by capsule, under each birthday's
  month as a pitch;
- the credibility revolution: Angrist's draft lottery (1990), quarter of birth (1991), Card and Krueger's border
  (1994), the designs, and the 2021 Nobel prize;
- experiments: the Island's apprenticeship by choice and by lottery, the negative income tax trials, PROGRESA, and
  the laboratory, the field, policy trials and A/B tests;
- the Lucas critique: the American Phillips curve of the 1960s and 1970s, the Island's council and its menu, Lucas
  (1976) and Haavelmo's autonomy;
- structure and design: the local average treatment effect, the 2010 debate in the *Journal of Economic
  Literature*, and the bridges between them;
- a new dial (the return to a year of school, from eleven natural experiments), weak instruments on the Island, the
  people who evaluate for a living, how to plan a trial and how many people it needs, and a frontier chapter on
  spillovers and general equilibrium.

## Build it

```bash
python -m videos.economics.econ4.compute              # every number (a few seconds), into .cache/econ4/
python tools/qa_scene.py econ4 PlayIt                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ4 -q l   # the whole part, silent preview
python tools/build.py econ4                           # 1080p30 with narration and the series' computed score
python -m explainer.economics.data --refresh draft1970 fred   # the data again, with a report of changes
python -m videos.economics.labs 4                     # the lab
```

The data are frozen extracts in `explainer/economics/data/`, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md): the Selective Service System's lottery of 1 December
1969 (from the *Journal of Statistics Education*'s data archive) and FRED's unemployment rate and consumer price
index, retrieved on 19 November 2026. LaLonde's National Supported Work data, in Dehejia and Wahba's subsample with
429 PSID comparison men, and Card and Krueger's table 3 come from the Museum of *Statistics, Built*
(`explainer/stats/museum.py`). Passages and tables transcribed from publications (Moore 1914, Leamer 1983, LaLonde
1986, Card 2001, Lucas 1976) are in `explainer/economics/data/tables.py`, each with where it was read and the date it
was checked.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | When can data answer an economic question? | Moore (1914): crops slope down, pig iron slopes up, "as the supply increases the price rises"; Wright's review (1915): rain moves the supply of crops, business conditions the demand for pig iron; the Island's 240 days and a line through them, +8.3 fish per dollar; Working (1927); the question; the title; objectives |
| 1 | Play it: find the demand curve | Four lines through the cloud (A the best fit, B steep, C in between, D flat); a countdown; the truth: demand −66.7 fish per dollar (C), supply +88.9, the best fit +8.3, neither |
| 2 | Two curves, one cloud | An ordinary day, a feast, a storm, both; 164 ordinary days, 45 feasts, 23 storms, 8 with both; the average day of each kind; plim of least squares = (d σ²ᵤ − b σ²ᵥ)/(σ²ᵤ + σ²ᵥ) = (88.9 × 1063 − 66.7 × 960)/(1063 + 960) = +15.1; which curve each kind of shift reveals |
| 3 | The instrument | 31 stormy days, 209 calm; the Wald ratio (182.3 − 218.6)/(3.50 − 2.95) = −65.2 against the planted −66.7; two-stage least squares −65.2 (s.e. 9.5), first stage +56 cents; Wright's Appendix B (1928), the arrows, no arrow from the weather to demand; Stock and Trebbi (2003): Philip, not Sewall; feasts trace supply, +90.2 against +88.9 |
| 4 | Haavelmo: identification | *The Probability Approach in Econometrics* (1944); a system with random shocks, the data, what the data could reveal; the Cowles Commission; Nobel 1989; the two equations with feast and storm; exclusions; the order condition |
| 5 | Omitted variables and selection | 1,200 islanders' schooling and earnings: least squares 10.1%; ability planted; plim = ρ + γ cov(S, A)/var(S) = 0.080 + 0.10 × 1.48/5.44 = 0.107; holding ability fixed 0.074; the new school: 11.00 against 8.99 years, log earnings 1.890 against 1.729, Wald 0.161/2.01 = 0.080 (2SLS 0.080, s.e. 0.011); who signs up for training; Ashenfelter's dip (schematic) |
| 6 | The con, and LaLonde's test | Leamer (1983), p. 37: "hardly anyone takes anyone else's data analyses seriously", the plumed birds; the National Supported Work Demonstration; the lottery's +$886 for men; LaLonde's table 5: PSID −$15,578 raw, −$8,067 adjusted, CPS −$8,870 and −$4,416, differences in differences +$425 and +$1,714, narrower groups −$509 and +$224; Dehejia and Wahba's subsample: 185 trainees, 260 controls, 429 PSID men; experiment +$1,794, raw −$635, adjusted +$1,548; *Called it?*: wrong |
| | Intermission: the lottery of 1969 | No narration: the 366 capsules in the order drawn, by birthday; each month's average place against the draws so far; correlation −0.23 between birthday and draw order, 1 of 20,000 fair shuffles as far; under it, each capsule's month as a pitch; the story so far |
| 7 | The credibility revolution | Angrist (1990): the lottery number, service, earnings; white veterans about 15% lower in the early 1980s; quarter of birth (Angrist and Krueger 1991): OLS 0.070, 0.063, 0.052 against IV 0.101, 0.060, 0.078 for men born in the 1920s, 30s and 40s; Card and Krueger (1994): New Jersey 20.44 → 21.03, Pennsylvania 23.33 → 21.17, difference in differences +2.76 (s.e. 1.36); instruments, differences in differences, discontinuities, experiments; Angrist and Pischke (2010); Nobel 2021 |
| 8 | Experiments | The apprenticeship (planted +0.10): by choice −0.146 (s.e. 0.018), the choosers' ability 0.94 SD lower; by lottery +0.107 (s.e. 0.019), the groups alike; the negative income tax (Friedman 1962): the guarantee, the break-even, 50 cents of each dollar; New Jersey and Pennsylvania 1968–72, about 1,350 families, eight plans; Seattle–Denver; what they found; PROGRESA (1997): 506 villages, 320 first and 186 about two years later; Levy; enrolment; Oportunidades; the lab, the field, policy trials (Nobel 2019), A/B tests |
| 9 | The Lucas critique | US unemployment and CPI inflation 1961–79; Samuelson and Solow's menu (1960); Friedman and Phelps; the 1970s; the Island's thirty calm years, slope 0.86; the council's 8%: the menu says 105.2, the first year 105.6, the last ten years 99.9; expected inflation catches up; Lucas (1976), p. 41; deep parameters; Haavelmo's autonomy |
| 10 | Structure and design | Volunteers, never-serves and compliers; no defiers; the local average treatment effect (Imbens and Angrist 1994); Deaton, Imbens and Heckman in the *JEL* (2010); would PROGRESA travel?; design against structure; sufficient statistics (Chetty 2009); identified moments (Nakamura and Steinsson 2018) |
| 11 | The Dials: what is a year of school worth? | The new dial from Card (2001), table 2: eleven natural experiments, each beside least squares on the same data (least squares 0.052–0.085, instruments 0.060–0.164; the instrument higher in 9 of 11); weak instruments: 60 instruments of pure noise, 400 times, median first-stage F 1.0, median estimate 0.100 where least squares was 0.101; the real instrument 0.080 (F = 272); Staiger and Stock's F of 10; four explanations; status: settled within a range |
| 12 | In practice: who evaluates for a living | Evaluation firms (MDRC, 1974), development labs, government units, experimentation teams, expert witnesses, central bank researchers; planning a trial in six steps; the minimum detectable effect, σ = 0.39: about 480 islanders for +0.10, power 71% with 400 (simulated), 100% with 1,600 |
| 13 | Frontier: when treatments spill over | 100 villages, the share offered a place drawn from 0 to 100%: within villages +0.106 (s.e. 0.018, planted +0.10), the not-offered lose −0.097 per unit share (planted −0.08), everyone against no one +0.031 (planted +0.02); Crépon et al. (2013), Egger et al. (2022), Muralidharan, Niehaus and Sukhtankar (2023); what is not known; the research problem |
| | Recap, problems, and the road ahead | The answer; eleven lines; problems; reading; the end of Act I; Samuelson (1938) and Part 5 |

## What is computed, and from what

Everything plotted is computed by `compute.py` from Agora's econometrician (`explainer.economics.agora.econometrician`,
over statkit's `quasi.tsls`), with the Island's Part 4 truths in `explainer.economics.island`, or from the Data Room,
the Museum or a transcribed table; the narration states the cached numbers.

- **The fish market** (`fish_season`, planted): 240 days; demand q = a − b p + 70·feast + u with b = 66.7, supply
  q = c + d p − 80·storm + v with d = 88.9; feasts on 25% of days, storms on 15%; shocks N(0, 12²); seed 1927. The
  probability limit uses the variances of the total shifts, (d σ²ᵤ − b σ²ᵥ)/(σ²ᵤ + σ²ᵥ).
- **The instrument**: the Wald ratio is the difference in mean quantity over the difference in mean price between
  stormy and calm days (or feast and ordinary days); two-stage least squares and the first-stage F from statkit.
- **The school records** (`schooling_records`, planted): 1,200 islanders; ability N(0, 1); schooling 9 + 1.5·ability
  + 2·(grew up near the new school) + N(0, 1.5²); log earnings with a return of 0.08 and 0.10 per unit of ability
  (noise 0.35); seed 1991. The scatter shows 300 of them.
- **LaLonde**: table 5 of LaLonde (1986) for men, from `tables.LALONDE_1986`; the subsample comparisons are
  differences in mean 1978 earnings and least squares on age, schooling, race, ethnicity, marriage, no degree and
  1974–75 earnings.
- **The draft lottery**: each day's draw order from the Selective Service's 1969 lottery; the correlation between day
  of the year and draw order; a permutation test with 20,000 shuffles (seed 1969). The film places capsule k at
  1.5 + 36·k/366 seconds; each month's bar is 1 − (mean place − 1)/(k − 1) among the k drawn so far, so a fair draw
  keeps every bar near the middle; the data melody maps each capsule's month to a pitch.
- **The apprenticeship** (`apprenticeship`, planted): 1,600 young islanders; effect 0.10; by choice, each signs up
  with probability logistic(−1.4·ability); by lottery, half at random; ability moves log earnings by 0.25 per SD;
  seed 2019. Power: MDE = (z.975 + z.80)·σ/√(p(1 − p)N), and 400 fresh trials at each size.
- **The negative income tax**: income = max(earnings, G + (1 − t)·earnings), in units of the poverty line, with
  New Jersey's guarantees (0.5 to 1.25) and tax rates (0.3, 0.5, 0.7).
- **Lucas's islands** (`lucas_islands`, planted): output = 100 + 0.8·(π − Eπ) + N(0, 0.4²); thirty calm years with
  π ~ N(2, 2²), then twenty at 8% (± 0.5); expected inflation adapts halfway each year; seed 1976.
- **The Phillips curve**: annual means of the unemployment rate (UNRATE) and year-on-year changes in the annual mean
  of the CPI-U (CPIAUCSL), 1961–79.
- **The Dial**: Card (2001), table 2, from `tables.CARD_2001`, intervals ±1.96 standard errors; the weak-instrument
  experiment uses the school records with 60 columns of fair coin flips as instruments, 400 times (seed 1995).
- **The villages** (`village_trial`, planted): 100 villages of 40; shares 0, 25, 50, 75 or 100% in equal numbers,
  randomly assigned; direct effect 0.10, spillover −0.08 times the village's share for everyone, village shocks
  N(0, 0.04²); the within-village estimate averages each mixed village's difference; seed 2013.
- **The score** (`explainer/economics/score.py`): the scissors theme, chapter stings, beds under the pauses, and the
  close; the intermission's melody. Synthesized from sines; nothing recorded.

## Problems and solutions

**1.** *Demand is q = 100 − 2p + u and supply q = 20 + 3p + v, with var(u) = 4 and var(v) = 1, independent. To what
does the least-squares slope of q on p converge? Which curve would it find if u never moved?*

*Solution.* With b = 2 and d = 3, the slope converges to (d σ²ᵤ − b σ²ᵥ)/(σ²ᵤ + σ²ᵥ) = (3·4 − 2·1)/(4 + 1) = 2: a
positive slope, closer to supply's 3 than to demand's −2, because demand moves more. If u never moved, only supply
would shift, every point would lie on the demand curve, and the slope would converge to −b = −2.

**2.** *Storms cut the Island's supply by 80 fish at every price, and also keep 10 fish' worth of buyers at home.
With demand dq/dp = −66.7 and supply dq/dp = 88.9, what does the storm's Wald ratio estimate? Which assumption
failed?*

*Solution.* The price rises by (80 − 10)/(66.7 + 88.9) = 70/155.6 = 0.45 dollars, and the quantity falls by
66.7 × 0.45 + 10 = 40.0 fish (check on supply: 88.9 × 0.45 − 80 = −40.0). The Wald ratio is −40.0/0.45 = −88.9,
a third more elastic than the true −66.7. The exclusion restriction failed: the instrument moved demand too, so part
of the fall in quantity is the storm's direct effect on buyers, credited to the price.

**3.** *log w = α + 0.08 S + 0.10 A + e, cov(S, A) = 1.5, var(S) = 5.5. Find the probability limit of least squares.
Now years of school are reported with an error of variance 1. What does least squares find now?*

*Solution.* 0.08 + 0.10 × 1.5/5.5 = 0.08 + 0.027 = 0.107. With reported schooling S + m, the covariance with
log w is unchanged, 0.08 × 5.5 + 0.10 × 1.5 = 0.59, but the variance rises to 6.5, so least squares finds
0.59/6.5 = 0.091. The two biases pull in opposite directions; here ability wins, but by less. This is one of Card's
reasons why instruments, which fix measurement error too, can come out above least squares.

**4.** *NSW trainees earned $2,096 in 1974, $1,532 in 1975 and $6,349 in 1978; the survey men $5,619, $2,466 and
$6,984. Compute the raw comparison, and two differences in differences, from 1974 and from 1975. The experiment
said $1,794. What went wrong?*

*Solution.* Raw: 6,349 − 6,984 = −$635. From 1974: (6,349 − 2,096) − (6,984 − 5,619) = 4,253 − 1,365 = +$2,888.
From 1975: (6,349 − 1,532) − (6,984 − 2,466) = 4,817 − 4,518 = +$299. The answers straddle the experiment's
$1,794, and the choice of base year moves the estimate by $2,600. Difference in differences assumes the two groups'
earnings would have moved in parallel; their paths before the programme already differ (1974 to 1975: trainees
−$564, survey men −$3,153), so the assumption fails, and nothing in the 1978 data can say by how much.

**5.** *A low lottery number raises the chance of serving from 0.20 to 0.36, and lowers average earnings by $400.
Estimate the effect of service. For whom is it the effect?*

*Solution.* The Wald estimate is −400/(0.36 − 0.20) = −$2,500. Under the assumptions that the number affects
earnings only through service and that nobody serves only because his number was not called, it is the average
effect for the compliers, the 16% of men who served because of a low number; not for volunteers, nor for men who
would never have served.

**6.** *y = 100 + 0.8(π − Eπ), E_t = E_{t−1} + 0.5(π_{t−1} − E_{t−1}), E = 2 in the calm years. The council holds
π = 8 from now on. Find output in each of the first four years, and compare the menu's promise.*

*Solution.* In the calm years y = 100 + 0.8(π − 2) = 98.4 + 0.8π, which promises 104.8 at π = 8, every year. Year
1: E = 2, y = 104.8. Year 2: E = 2 + 0.5 × 6 = 5, y = 102.4. Year 3: E = 6.5, y = 101.2. Year 4: E = 7.25, y = 100.6.
The gap halves each year and output returns to 100; the menu held only while inflation surprised.

**7.** *Earnings have σ = 0.4; half the sample is offered a place. How many people do you need to detect an effect
of 0.05 with 80% power at the 5% level? And if only 30% of those offered take it up?*

*Solution.* N = ((1.96 + 0.84) σ/MDE)²/(p(1 − p)) = (2.80 × 0.4/0.05)²/0.25 = 22.4² × 4 ≈ 2,007. If only 30% take
it up (and the offer does nothing to the rest), the effect of the offer is 0.3 × 0.05 = 0.015, and N grows by
1/0.3² ≈ 11, to about 22,300. Take-up is the most expensive number in a trial's plan.

**8.** ★ *Design the Island's next village trial: how many villages, at what shares, to detect a spillover of −0.04
per unit share with 80% power?* (Research problem.)

*Solution sketch.* The spillover is identified only by variation in the share across villages, so precision is set
by the number of villages and the spread of their shares, not by the number of people. The mean earnings of a
village's untreated members have variance σ²_village + σ²/n_untreated (here 0.04² + 0.39²/n); the slope's
standard error is roughly that standard deviation over √G·sd(share). With 40 people per village and shares spread
over 0 to 75% for the untreated (sd about 0.28), a spillover of −0.04 needs a standard error near 0.014, which takes
several hundred villages; larger villages help only until the village shock dominates. Extreme shares (0 and 100%)
maximize the spread but leave no untreated people at 100% and no within-village comparison, so the direct effect and
the spillover compete for the design. Baird, Bohren, McIntosh and Özler (*Review of Economics and Statistics*, 2018)
derive the power of these randomized-saturation designs; start from `econometrician.village_trial` and simulate the
power of each candidate design, as chapter 12 did for the apprenticeship. Open questions: designs when the spillover
travels between villages, and when the shares that matter are not the ones assigned.

## Where it comes back

| Idea | Where |
|---|---|
| choice, observed: what demand curves are made of | Part 5, *What People Want* |
| the Phillips curve and expectations | Part 28, *Inflation and Expectations* |
| the minimum wage, at the border and since | Part 38, *Work and Wages* |
| demand estimation with instruments (BLP) | Part 43, *Measuring Market Power* |
| field experiments and behaviour | Part 45, *Behavioural Economics* |
| trials in development | Part 46, *Development* |
| identifying a monetary shock | Part 55, *Identifying Macro* |
| a regression in court | Part 59, *The Expert Witness* |
| experiments in markets | Part 61, *Economics at the Platforms* |

## Sources

**Primary texts.**
- H. L. Moore, *Economic Cycles: Their Law and Cause* (1914), p. 126, as quoted in the editorial of *The
  Econometrics Journal* 28(1) (2025), arXiv 2501.16395.
- P. G. Wright, "Moore's Economic Cycles", *Quarterly Journal of Economics* 29(2) (1915) 631–641; *The Tariff on
  Animal and Vegetable Oils* (1928), Appendix B.
- E. J. Working, "What Do Statistical 'Demand Curves' Show?", *Quarterly Journal of Economics* 41(2) (1927) 212–235.
- T. Haavelmo, "The Probability Approach in Econometrics", *Econometrica* 12, supplement (1944).
- R. E. Lucas, Jr., "Econometric Policy Evaluation: A Critique", *Carnegie-Rochester Conference Series on Public
  Policy* 1 (1976) 19–46, p. 41 (the sentence as quoted with its page in the secondary literature).
- Selective Service System, the lottery of 1 December 1969, in the *Journal of Statistics Education* data archive
  (draft70yr), after S. E. Fienberg, "Randomization and Social Affairs: The 1970 Draft Lottery", *Science* 171
  (1971) 255–261.

**Papers.**
- J. H. Stock and F. Trebbi, "Who Invented Instrumental Variable Regression?", *Journal of Economic Perspectives*
  17(3) (2003) 177–194.
- E. E. Leamer, "Let's Take the Con out of Econometrics", *American Economic Review* 73(1) (1983) 31–43.
- R. J. LaLonde, "Evaluating the Econometric Evaluations of Training Programs with Experimental Data", *American
  Economic Review* 76(4) (1986) 604–620, table 5; R. H. Dehejia and S. Wahba, *JASA* 94 (1999) 1053–1062.
- O. Ashenfelter, "Estimating the Effect of Training Programs on Earnings", *Review of Economics and Statistics*
  60(1) (1978) 47–57.
- J. D. Angrist, "Lifetime Earnings and the Vietnam Era Draft Lottery", *American Economic Review* 80(3) (1990)
  313–336; J. D. Angrist and A. B. Krueger, "Does Compulsory School Attendance Affect Schooling and Earnings?",
  *Quarterly Journal of Economics* 106(4) (1991) 979–1014.
- D. Card and A. B. Krueger, "Minimum Wages and Employment", *American Economic Review* 84(4) (1994) 772–793, table 3.
- G. W. Imbens and J. D. Angrist, "Identification and Estimation of Local Average Treatment Effects", *Econometrica*
  62(2) (1994) 467–475.
- J. Bound, D. A. Jaeger and R. M. Baker, *JASA* 90 (1995) 443–450; D. Staiger and J. H. Stock, *Econometrica* 65(3)
  (1997) 557–586.
- D. Card, "Estimating the Return to Schooling: Progress on Some Persistent Econometric Problems", *Econometrica*
  69(5) (2001) 1127–1160, table 2; O. Ashenfelter, C. Harmon and H. Oosterbeek, *Labour Economics* 6 (1999) 453–470.
- J. D. Angrist and J.-S. Pischke, "The Credibility Revolution in Empirical Economics", *Journal of Economic
  Perspectives* 24(2) (2010) 3–30.
- A. Deaton, "Instruments, Randomization, and Learning about Development"; G. W. Imbens, "Better LATE Than Nothing";
  J. J. Heckman, "Building Bridges between Structural and Program Evaluation Approaches to Evaluating Policy":
  *Journal of Economic Literature* 48(2) (2010).
- R. Chetty, "Sufficient Statistics for Welfare Analysis", *Annual Review of Economics* 1 (2009) 451–488;
  E. Nakamura and J. Steinsson, "Identification in Macroeconomics", *Journal of Economic Perspectives* 32(3) (2018)
  59–86.
- M. Friedman, *Capitalism and Freedom* (1962), ch. 12; A. H. Munnell, ed., *Lessons from the Income Maintenance
  Experiments* (Federal Reserve Bank of Boston, 1986).
- T. P. Schultz, "School Subsidies for the Poor: Evaluating the Mexican Progresa Poverty Program", *Journal of
  Development Economics* 74 (2004) 199–250; E. Skoufias, *PROGRESA and Its Impacts* (IFPRI, 2005); S. Levy,
  *Progress against Poverty* (Brookings, 2006).
- B. Crépon, E. Duflo, M. Gurgand, R. Rathelot and P. Zamora, "Do Labor Market Policies Have Displacement Effects?",
  *Quarterly Journal of Economics* 128(2) (2013) 531–580.
- D. Egger, J. Haushofer, E. Miguel, P. Niehaus and M. Walker, "General Equilibrium Effects of Cash Transfers",
  *Econometrica* 90(6) (2022) 2603–2643.
- K. Muralidharan, P. Niehaus and S. Sukhtankar, "General Equilibrium Effects of (Improving) Public Employment
  Programs", *Econometrica* 91(4) (2023) 1261–1295.
- M. G. Hudgens and M. E. Halloran, *JASA* 103 (2008) 832–842; P. M. Aronow and C. Samii, *Annals of Applied
  Statistics* 11(4) (2017) 1912–1947; S. Baird, J. A. Bohren, C. McIntosh and B. Özler, *Review of Economics and
  Statistics* 100(5) (2018) 844–860.
- B. A. Olken, "Promises and Perils of Pre-Analysis Plans", *Journal of Economic Perspectives* 29(3) (2015) 61–80.

**Textbooks.** Angrist and Pischke, *Mostly Harmless Econometrics* (2009) and *Mastering 'Metrics* (2014); Stock and
Watson, *Introduction to Econometrics*, chs. 1–3, 12–13; Cunningham, *Causal Inference: The Mixtape* (2021);
Acemoglu, Laibson and List, *Economics*, ch. 2.
