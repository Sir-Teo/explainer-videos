# Economics, Built: Part 67, The Next Economics

Part 67 of a sixty-eight-part course in economics (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth of Act XII, *The Frontier*. It asks how much of what economics says is
true, and how the field is changing the way it finds out. Its answer: more than its critics say, less than its
journals print. Published results are selected, so they are exaggerated, and in the laboratories they replicate about
three times in five; the selection can be seen and partly corrected. The field is changing how it finds out: plans
before data, code checked before publication, many analysts and whole specification curves instead of one estimate,
and records that accumulate. Machines will speed every step, the errors included.

It opens with Brodeur, Lé, Sangnier and Zylberberg's 50,000 test statistics from the AER, the JPE and the QJE,
2005-2011: a valley for p-values between 0.25 and 0.10, a bump just below 0.05, and 10-20% of marginally significant
results that should have fallen short. A simulated field of 160,000 studies with known true effects (three in ten
exactly zero), specification search after an insignificant first try, and journals that publish every significant
result and about a third of the rest reproduces the camel: just above 1.96 against just below, the published results
run 3.2 to 1, the same studies' first tries 0.9 to 1. From there it covers:

- Play it: six published results picked by rule (the significant results at six evenly spaced ranks of z), each
  replicated with 90% power against its published effect: four of six replicate; the weakest published results
  replicate about half the time, the strongest about seven in ten;
- replication in the lab: Camerer et al.'s 18 experiments from the AER and QJE (2011-2014), 11 replicated (61%),
  effects 66% of the originals; the simulated field gives 60% and 71%; the winner's curse (true effects 62% of the
  published ones just past 1.96, 80% above 6); *Called it?*: the prediction markets, which priced replication at 75%
  on average and ranked the studies only weakly (partly right);
- reproducing papers: the ladder (reproduce, robustness, replicate, generalize); Chang and Li (22 of 67 papers from
  the files alone, 29 of 59 with the authors' help); the AEA Data Editor since 2018; the Institute for Replication's
  110 papers (over 85% reproducible, coding errors in about a quarter, about 70% robust); Reinhart and Rogoff's
  question asked 48 ways on the Herndon-Ash-Pollin data: 47 of 48 find slower growth above the threshold, by
  0.1 to 5.8 points, and none can say which way the causation runs;
- specification searching by design (Brodeur, Cook and Heyes): instruments worst, trials and discontinuities least;
  in the simulated field the caliper ratio runs 2.9 (trials, discontinuities), 3.2 (difference in differences) and
  3.6 (instruments), and the share of insignificant results missing from the record from 64-67% (trials, discontinuities) to 73%
  (instruments); Kranz and
  Pütz's correction for rounding;
- publication bias corrected (Andrews and Kasy): the step model of selection; a simulated minimum-wage meta-study
  whose published average elasticity is -0.017 against a truth of -0.010, and whose correction recovers -0.011;
  thirty-fold selection in the laboratory experiments, threefold in the minimum-wage literature; Ioannidis, Stanley
  and Doucouliagos's 159 literatures (median power 18% or less, typical exaggeration twofold);
- an intermission: Britain's public debt as a share of GDP, 1870-2020 (peak 270% in 1946; growth averaged 1.1% a
  year in the 51 years above 90%, 1.4% in the 40 peacetime ones, 1.6% below 90%);
- remedies: forking paths (five specifications, moderately alike, give a 17% false-positive rate; twenty, 36%);
  pre-analysis plans and their limits (Olken); registered reports (the JDE from 2018); ten outcomes, three real:
  testing each at 5% finds 2.4 real effects and a false one 31% of the time, Bonferroni 1.5 and 3%,
  Benjamini-Hochberg 1.8 and 10%;
- the empirical turn (Hamermesh): theory 58% of articles in the AER, JPE and QJE in 1983 and 19% in 2011, empirical
  work with the authors' own data from 2% to 34%; Leamer's con and Angrist and Pischke's credibility revolution;
  administrative data and who can get it;
- structure, design, and the Dials audited: 93 Dials holding 410 estimates (101 computed in these films), 112 from
  designs, 90 from structural or calibrated models, 104 from plain regressions; 20 settled within a range, 35
  depending on the setting, 36 contested, 2 not identified; the widest spreads (the return to capital in poor
  countries, risk aversion, the neutral rate, AI's productivity, what schools add);
- many analysts, one dataset (Huntington-Klein et al.): seven analysts on a simulated programme evaluation, seven
  sample sizes, estimates from 0.05 to 0.18 and a spread 2.0 times the mean standard error; all 288 specifications,
  97% significant, from 0.03 to 0.20; DellaVigna and Pope's experts;
- what the models leave out: complexity economics; Brock and Hommes's cobweb with switching forecasters, from a
  steady state through a two-cycle (beyond beta = 1.90) to chaos; the identification problem;
- the profession: Hamermesh's authors (single-authored articles from 84% to 20%, women from 4.7% to 12.6% of
  authorship); Heckman and Moktan's top five; Akerlof's sins of omission;
- economics with AI in the loop: Korinek's uses; Ludwig and Mullainathan's hypothesis generation; a thousand
  specifications searched by machine give a false positive 98% of the time, and the defences;
- the Dials (how often results replicate, new); practice (reading a paper, the field's prior, a forecast, an op-ed);
  and the frontier: living meta-analyses, routine replication, machine-readable results, forecasts on file, and the
  Dials as a public good.

## Build it

```bash
python -m videos.economics.econ67.compute              # every number (about a minute), into .cache/econ67/
python tools/qa_scene.py econ67 Designs                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py econ67 -q l   # the whole part, silent preview
python tools/build.py econ67                           # 1080p30 with narration and the series' computed score
python -m videos.economics.labs 67                     # the lab
```

The data are Reinhart and Rogoff's panel as processed by Herndon, Ash and Pollin and the Jordà-Schularick-Taylor
Macrohistory Database (both in the Data Room, registered in
[`SOURCES.md`](../../../explainer/economics/data/SOURCES.md)), and the published numbers transcribed in
`explainer/economics/data/tables.py` (`hamermesh_2013`, `camerer_2016`, `replication_67`, `selection_67`,
`forecasts_67`, `remedies_67`). The research field, the meta-study and the many-analysts dataset are simulated, with
the truth known. Everything else is stated from the papers listed in `dials.SHOWN[67]`.

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A two-humped camel | Brodeur et al.'s 50,000 tests; the simulated field's published results against its first tries; objectives |
| 1 | Play it: which results replicate? | Six published results; four replicate; the field's odds by the strength of evidence |
| 2 | Replication in the lab | Camerer et al.'s 18 experiments; the winner's curse; *Called it?*: the prediction markets |
| 3 | Reproducing papers | The ladder; Chang and Li; the Data Editor; the Institute for Replication; Reinhart and Rogoff 48 ways |
| 4 | Specification searching by design | Brodeur, Cook and Heyes; four designs in the simulated field; rounding |
| 5 | Publication bias, corrected | The selection model; a simulated funnel; corrected literatures |
| — | Intermission | Britain's public debt, 1870-2020, as a line and a tune |
| 6 | Remedies | Forking paths; pre-analysis plans and registered reports; ten outcomes and three rules |
| 7 | The empirical turn | Hamermesh's methods, 1963-2011; the credibility revolution; administrative data |
| 8 | Structure, design, and the Dials audited | Two camps; the Dials by kind of evidence and by status |
| 9 | Many analysts, one dataset | Huntington-Klein et al.; seven teams; 288 specifications; experts' forecasts |
| 10 | What the models leave out | Complexity economics; Brock and Hommes's route to chaos; the identification problem |
| 11 | The profession | Who writes economics; the top five; sins of omission |
| 12 | Economics with AI in the loop | The research chain; machine-made hypotheses; search at machine speed |
| 13 | The Dials | How often results replicate (new); the Dials most often reopened |
| 14 | In practice | Reading a paper; the field's prior for a new result; forecasts, models and op-eds |
| 15 | Frontier | A cumulative record; the Dials as a public good |
| — | Outro | The answer; twelve lines; problems; reading; next, Part 68, *The Dissertation* |

## What is computed, and from what

Everything plotted is computed by `compute.py` with Agora's `field` module (`explainer.economics.agora.field`); the
narration states the cached numbers.

- **The simulated field.** 160,000 studies in four designs of 40,000. True z: zero with probability 0.3, otherwise
  N(0, 4). First estimate: true z plus N(0, 1). After an insignificant first try the researcher searches with
  probability 0.10 (trials), 0.15 (discontinuities), 0.30 (difference in differences) or 0.45 (instruments): up to five
  further specifications, each correlated 0.6 with the first, reporting the first significant one or the largest.
  Journals publish every significant result and 35% of the rest.
- **Replication.** Each published significant result repeated with precision chosen for 90% power against its
  published z (the replication's z has mean z_true x 3.24/z_published); success is z >= 1.96 in the same direction.
- **The selection model.** Published |z| folded from a mixture of nulls, N(0, 1), and N(mu, 1 + s^2), with
  relative publication probability beta below 1.96; maximum likelihood by Nelder-Mead from three starting points. The caliper ratio counts |z| in [1.96, 2.16) over [1.76, 1.96).
- **The meta-study.** True elasticities N(-0.01, 0.005^2), standard errors log-uniform on [0.008, 0.12], negative
  significant estimates always published, the rest with probability 0.3, 600 published; Andrews and Kasy's model with
  study-specific standard errors fitted by maximum likelihood.
- **Reinhart and Rogoff 48 ways.** Thresholds of 60, 70, 80, 90, 100 and 120% of GDP; country-by-country or pooled
  means; from 1946 or 1950; with or without their exclusions of New Zealand before 1950 and Australia and Canada
  before 1951 (Italy before 1951 always out, as in Part 32).
- **Many analysts.** 4,000 people; the programme's effect 0.25 under 30, 0.10 from 30 to 49, -0.02 from 50; take-up
  rising for the young, the poor and three regions; t(3) noise and 0.6% miscoded records; 30% of enrollees quit. Each
  specification is OLS with HC0 standard errors; the 288 are every combination of nine age ranges and five binary
  choices.
- **Brock and Hommes.** x_t = -b(1 - n_t) x_(t-1)/(B + b n_t), n_t a logit in beta[(b/2)(x_(t-1) - x_(t-2))^2 - C],
  with b/B = 1.35 and C = 1; 240 values of beta from 0.05 to 10, 1,500 periods each, the last 60 kept.
- **Forking paths.** Equicorrelated N(0, 1) statistics; 20,000 simulated studies per point. Ten outcomes with three
  real effects at z = 2.8 (80% power), 20,000 studies, three rules.
- **The intermission.** JST's `debtgdp` for the United Kingdom and growth of `rgdpmad`, 1870-2020; the melody is the
  debt ratio, year by year.

## Problems and solutions

**1.** *The caliper: with no selection, the density of |z| is smooth near 1.96; explain why the counts just above and
just below should be nearly equal, and what a ratio of 3 implies.*

*Solution.* In a narrow window of width w on each side of 1.96, a smooth density f gives counts of about N f(1.96) w
on each side, differing only by the slope: the ratio is about 1 + f'(1.96) w / f(1.96), slightly below one where the
density falls (the simulated first tries give 0.89 with w = 0.2). A ratio of 3 cannot come from a smooth density: about
two thirds of the results just above the line, or their missing counterparts just below, are the work of selection,
either insignificant results left unpublished or results moved across the line by search.

**2.** *The winner's curse: with true z = 1 and noise N(0, 1), compute the mean of the estimate given that it is
significant, and the power of a replication sized for that mean.*

*Solution.* Given Z > 1.96 with Z ~ N(1, 1), E[Z | Z > 1.96] = 1 + phi(0.96)/(1 - Phi(0.96)) = 1 + 0.2516/0.1685 =
2.49. A replication with 90% power against z = 2.49 must scale the expected z by k = (1.282 + 1.96)/2.49 = 1.30. Its
true expected z is 1 x 1.30 = 1.30, so its power is P(N(1.30, 1) > 1.96) = 1 - Phi(0.66) = 0.25, not 0.9.

**3.** *Forking paths: for k independent tests at 5%, show that the chance of at least one false positive is
1 - 0.95^k; why is it lower when the tests are correlated?*

*Solution.* Under the null each test is insignificant with probability 0.95, independently, so all k are with
probability 0.95^k and at least one is significant with probability 1 - 0.95^k (40% for k = 10). Correlated tests
fail together: when one is insignificant the others tend to be too, so the k chances overlap; with perfect correlation
the k tests are one test and the chance stays 5%.

**4.** *Selection: with latent z ~ N(mu, sigma^2) and publication probability beta below 1.96, write the density of
published z and its normalizing constant.*

*Solution.* With p(z) = 1 for |z| >= 1.96 and beta otherwise, the published density is p(z) phi((z - mu)/sigma)/sigma
divided by the probability of publication, P = beta [Phi((1.96 - mu)/sigma) - Phi((-1.96 - mu)/sigma)] + 1 -
[Phi((1.96 - mu)/sigma) - Phi((-1.96 - mu)/sigma)]. Maximizing the log of this over (mu, sigma, beta) is Andrews and
Kasy's estimator in its simplest form. The latent distribution must be right: the film's field mixes exact nulls with
real effects, and a single normal fitted to it confuses the spike of nulls near zero with selection (it reports beta
= 0.56 for a filter of 0.30); a mixture of the two recovers 0.29.

**5.** *Many analysts: take the seven teams' estimates and standard errors; compute their spread over the mean
standard error, and say what a ratio of 2 means for a reader.*

*Solution.* The estimates are 0.052, 0.115, 0.131, 0.130, 0.049, 0.131 and 0.176, with standard errors from 0.020 to
0.029. Their standard deviation is 0.046 and the mean standard error 0.023, a ratio of 2.0. A reader who sees one
team's estimate and its standard error understates the uncertainty: the analyst's choices add variance about three
times the sampling variance (2.0^2 - 1), so an honest interval is more than twice as wide.

**6.** *Brock and Hommes: show that the steady state of the switching cobweb loses stability when
(1 - n\*) b = B + n\* b, and find the beta at which this happens for b/B = 1.35, C = 1.*

*Solution.* At the steady state x = 0 the rational rule's advantage is -C, so n\* = 1/(1 + e^(beta C)). Because the
advantage depends on squared price changes, n does not respond to small deviations to first order, and the linearized
map is x_t = -b(1 - n\*) x_(t-1)/(B + b n\*). Its eigenvalue is negative, and the steady state loses stability when it
reaches -1, that is when (1 - n\*) b = B + n\* b, or n\* = (b - B)/(2b) = 0.35/2.70 = 0.130. Then e^(beta C) = 1/n\* - 1
= 6.71 and beta = ln 6.71 = 1.90: the period-doubling of the bifurcation diagram.

## Lab and interactive

- `python -m videos.economics.labs 67`: a simulated field with search and selection; the caliper ratio and the
  selection model; replication and the winner's curse; forking paths; the meta-study correction; many analysts and
  the specification curve; Brock and Hommes's steady state and its loss of stability.
- The interactive (course site): field. The reader sets how often researchers search, how many specifications they
  try and how often journals publish insignificant results, and watches the published z-curve, the caliper ratio and
  the replication rate respond.

## Sources

The studies the film states are listed with what each shows in `dials.SHOWN[67]`; the new Dial (how often results
replicate) is in `explainer/economics/dials.py`, and the *Called it?* record of the 2016 replication markets in
`explainer/economics/calls.py`. The methods are stated from the works cited in the chapters (Leamer 1983, Brock and
Hommes 1997, Doucouliagos and Stanley 2009, Farmer and Foley 2009, Angrist and Pischke 2010, Reinhart and Rogoff 2010,
Hamermesh 2013, Herndon, Ash and Pollin 2014, Olken 2015, Open Science Collaboration 2015, Chang and Li 2015,
Brodeur et al. 2016, Camerer et al. 2016, Ioannidis, Stanley and Doucouliagos 2017, Camerer et al. 2018, DellaVigna
and Pope 2018, Christensen and Miguel 2018, Andrews and Kasy 2019, Akerlof 2020, Brodeur, Cook and Heyes 2020,
Heckman and Moktan 2020, Arthur 2021, Huntington-Klein et al. 2021, Kranz and Pütz 2022, Korinek 2023, Brodeur et al.
2024, Ludwig and Mullainathan 2024) and computed here.
