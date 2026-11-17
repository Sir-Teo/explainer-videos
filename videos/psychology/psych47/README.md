# Psychology, Built: Part 47, People over Time

In 1973 Herbert Clark pointed out that a generation of studies of language had tested whether their effects would
generalize to new people but never to new words. Treating both as samples took thirty years to become routine. The
deeper version of his point is the hardest in the series: a relation that holds across people need not hold within
any one of them, and psychology's theories are mostly about the second.

The viewer guesses one person's slope inside a cloud of points and predicts four numbers. Then the
language-as-fixed-effect fallacy, simulated (about half of null studies significant when words are ignored);
repeated measures and the multilevel model; partial pooling of person-level slopes; participants and items crossed,
min F′ and the maximal-model debate; power that depends on the number of stimuli, and the generalizability crisis;
growth with time-varying predictors, and what happens when the predictor is not split; Simpson's paradox inside a person and person-mean centring; ergodicity, and a
population whose group correlation describes almost no one; experience sampling and the small-sample bias of
inertia; cause over time and its repairs; and critical slowing down before a tipping point, with its false alarms
in diary data.

## Where the numbers come from

| What | Source |
|---|---|
| The fallacy: 200 simulated priming studies with no effect (30 participants, 20 words, 10 per condition; participant SD 0.5, word SD 0.5, trial SD 1): significant at 5% in 52.5% by participants only, 2.5% by items, 2.0% by min F′ | Psyche (`within.false_positive_rates`), item `fpr` |
| One such study: p = 0.69 (participants), 0.85 (items), 0.86 (min F′); each word's mean shown by condition; a crossed mixed model (statkit's `vc_lmm`) matched the by-item test exactly on a check study | Psyche (`within.priming_study`, `min_f_test`, `crossed_test`), item `example` |
| Stimuli and power: a real effect of 0.4 with 30 participants: power 16%, 23%, 30%, 60%, 65% with 8, 12, 20, 32 and 48 words (80 studies each) | Psyche (`within.stimulus_power`), item `stimpower` |
| Effective sample size: 100 people with intraclass correlation 0.3; m observations each are worth N m/(1 + (m - 1) 0.3) independent ones for the grand mean (100, 154, 227, 270, 299, 318 for m = 1, 2, 5, 10, 20, 50; 4,000 simulated studies agree), with a ceiling of 333 | the formula and a simulation, item `neff` |
| Partial pooling: 40 people, 15 observations each, slopes with mean 0.5 and SD 0.3: each person's own slope misses by 0.29 on average (RMSE), the multilevel model's by 0.19 | Psyche (`within.person_slopes`, statkit's `lmm`), item `slopes` |
| How much to trust one person: the weight on a person's own slope, G/(G + σ²/(n s²)) with G = 0.09 and σ² = s² = 1, from 2 to 60 observations; 0.57 at 15 | the formula, item `shrinkw` |
| Participants differ in the effect: 200 simulated studies with no average effect, participant slope SD 0.5 and word SD 0.2: false positives 10.5% by participants, 12.5% by items, 3.0% by min F′ | Psyche (`within.false_positive_rates`), item `slopefpr` |
| People or items: power for a real effect of 0.4 with 15, 30, 60, 120 participants and 10, 20, 40 words (40 studies a cell): 10% to 22.5% with 10 words, 27.5% to 40% with 20, 50% to 55% with 40 | Psyche (`within.stimulus_power`), item `powergrid` |
| Splitting the predictor: 200 children, 5 weeks, a planted within-child practice effect of +0.5 and between-child -0.4; entered once 0.17; split, +0.41 and -0.38 | Psyche (`within.growth_split`, statkit's `lmm`), item `growth` |
| Simpson inside a person: 12 people, 15 occasions each; slope -0.65 pooled, -0.96 between people and +0.59 within (planted -1.0 and +0.6) | Psyche (`within.simpson_cloud`), item `simpson` |
| Ignoring the person: 30 people, 20 occasions, person slopes with mean 0 and SD 0.3; one pooled regression is significant in 15.2% of 2,000 studies, a t-test on the 30 person slopes in 4.7% | simulation, item `naive` |
| Ergodicity: 200 people, 100 occasions, stable differences correlated 0.8 and person-specific relations centred on zero: the cross-sectional correlation averages 0.63; 8% of people are within 0.1 of it, 47% are negative | Psyche (`within.nonergodic`), item `ergodic` |
| Each person's own slope in the Simpson cloud: all twelve between 0.43 and 0.75; pooled -0.65 | Psyche (`within.simpson_cloud`), item `ownslopes` |
| Own data or the group's: predicting a person's later within-person correlation from their own first 5, 10, 20, 40 occasions (mean absolute error 0.40, 0.24, 0.17, 0.13) or from the group's correlation (0.65) | Psyche (`within.own_vs_group`), item `owngroup` |
| Inertia: a true autoregression of 0.4 estimated around each person's mean: 0.16, 0.29, 0.33, 0.36, 0.38, 0.39 from 10, 20, 30, 50, 100, 200 occasions (2,000 series each), matching Kendall's approximation | Psyche (`within.inertia_bias`), item `inertia` |
| How many waves: 500 people with stable traits and a within-person cross-lag of 0.2, estimated from departures from each person's observed mean: 0.12, 0.17, 0.20, 0.20, 0.20 with 3, 5, 10, 20, 50 waves | Psyche (`within.crosslag_waves`), item `waves` |
| How many prompts: the reliability of a person's mean of k prompts when one prompt's intraclass correlation is 0.4 (Spearman-Brown): 0.40, 0.67, 0.82, 0.90, 0.95, 0.97 for k = 1, 3, 7, 14, 28, 56 (500 simulated people agree within 0.05) | the formula and a simulation, item `relmean` |
| Critical slowing down: a double-well system whose lower well flattens; before the tip, Kendall's τ of autocorrelation 0.47 and of variance 0.34; over 100 simulated lives, a continuous record warns before 58% of tips with 1% false alarms; a noisy daily diary of the same lives before 25%, with 16% false alarms | Psyche (`within.double_well`, `rolling_indicators`, `warning_rates`), item `tipping` |
| The analyst's window: a fresh set of 60 lives that tip and 60 that never do, continuous records; warnings before a tip 5%, 42%, 58%, 70% and false alarms 2%, 3%, 5%, 12% with rolling windows of 100, 200, 300, 500 steps | Psyche (`within.warning_rates`), item `windows` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

The typing example is an illustration of the planted pattern; the mood series on the experience-sampling chapter is
illustrative and labelled so.

## Built in this part

* `explainer/psychology/psyche/within.py`: a priming-study simulator with participant and item variance, the
  by-participant, by-item, min F′ and crossed mixed-model tests, false-positive rates and power by number of
  stimuli, person-level slopes against multilevel BLUPs, a within/between cloud, a non-ergodic population, the
  small-sample bias of person-level autoregression, a growth model with a split predictor, a person's own data against the group's, cross-lag estimates by number of waves, and a double-well system with early-warning indicators and their
  hit and false-alarm rates. Mixed models from *Statistics, Built*'s `explainer/stats/kit/mixed.py`. Tested in
  `tests/psychology/test_within.py`.
* The Ledger gains three rows.
* The course's interactive: clouds of people over time, where the reader guesses the slope within one person
  before the colours show it.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Analyses that treat a study's stimuli as fixed, rather than as a sample, find effects that do not generalize to new stimuli far more often than their nominal error rate. | Clark 1973 | replicated |
| People whose moment-to-moment emotions carry over more from one moment to the next (higher autocorrelation, 'inertia') are more prone to depression, and inertia adds information beyond how much their emotions vary. | Kuppens, Allen and Sheeber 2010 | contested |
| Rising autocorrelation and variance in a person's daily emotions signal an approaching transition into or out of depression (critical slowing down). | van de Leemput and colleagues 2014 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Laird and Ware; Baayen, Davidson
and Bates, Barr and colleagues, and Matuschek and colleagues; Yarkoni; Robinson; Molenaar; Hamaker, Kuiper and
Grasman.

## Build it

```bash
python -m videos.psychology.psych47.compute            # every number (a few minutes)
python tools/qa_scene.py psych47 Simpson               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych47 -q l   # the whole part, silent preview
python tools/build.py psych47                          # 1080p30 with narration
python tools/qa_scene.py psych47 Ergodic --lang zh     # the Chinese edition of one chapter
python tools/make.py psych47                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 47                    # the lab: items as a sample, pooling, Simpson, inertia
python tools/check_ledger.py psych47                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's within module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Twenty words, one conclusion | Clark's fallacy, simulated; the deeper point; the question; objectives |
| 1 | On you: one cloud, and four numbers | Guess one person's slope; four predictions |
| 2 | Repeated measures | Averaging throws away the structure; regressions within regressions; how much is one more observation worth? |
| 3 | Random intercepts and slopes | Partial pooling; how much to trust one person |
| 4 | Participants and items, crossed | Why the by-participant test fails; when people differ in the effect; how much structure? |
| 5 | Stimuli are a sample too | Power comes from stimuli too; people or items?; the generalizability crisis |
| 6 | Growth | Trajectories, and what changes with them; splitting the predictor |
| 7 | Simpson inside a person | The same cloud, by person; every person, one by one |
| 8 | Within against between | Person-mean centring; the ecological fallacy, inside one mind; ignoring the person |
| 9 | Ergodicity | Molenaar's manifesto; a population that describes no one; your own few days or everyone's? |
| 10 | Intensive longitudinal data | Experience sampling; inertia and its estimate; how many prompts? |
| 11 | Cause over time | The panel, repaired; how many waves? |
| 12 | Tipping points | Critical slowing down; warnings and false alarms; the analyst's window |
| 13 | The Ledger | Three rows; what they have in common |
| 14 | In practice: users, patients and dashboards | The same question, everywhere |
| 15 | Frontier: the science of one | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; Kant's three objections; payoffs; problems; references; Part 48 |

## Sources

* H. H. Clark (1973); R. H. Baayen, D. J. Davidson and D. M. Bates, Mixed-effects modeling with crossed random
  effects for subjects and items, *Journal of Memory and Language* 59 (2008) 390-412; D. J. Barr et al. (2013);
  H. Matuschek, R. Kliegl, S. Vasishth, H. Baayen and D. Bates, Balancing type I error and power in linear mixed
  models, *Journal of Memory and Language* 94 (2017) 305-315.
* N. M. Laird and J. H. Ware, Random-effects models for longitudinal data, *Biometrics* 38 (1982) 963-974;
  A. Gelman and J. Hill, *Data Analysis Using Regression and Multilevel/Hierarchical Models* (Cambridge, 2007);
  T. A. B. Snijders and R. J. Bosker, *Multilevel Analysis* (2nd edition, Sage, 2012).
* C. M. Judd, J. Westfall and D. A. Kenny (2012); T. Yarkoni, The generalizability crisis, *Behavioral and Brain
  Sciences* 45 (2022) e1.
* W. S. Robinson, Ecological correlations and the behavior of individuals, *American Sociological Review* 15 (1950)
  351-357; E. H. Simpson, The interpretation of interaction in contingency tables, *Journal of the Royal Statistical
  Society B* 13 (1951) 238-241.
* P. C. M. Molenaar, A manifesto on psychology as idiographic science, *Measurement* 2 (2004) 201-218; A. J. Fisher,
  J. D. Medaglia and B. F. Jeronimus, Lack of group-to-individual generalizability is a threat to human subjects
  research, *Proceedings of the National Academy of Sciences* 115 (2018) E6106-E6115.
* M. Csikszentmihalyi and R. Larson, Validity and reliability of the experience-sampling method, *Journal of Nervous
  and Mental Disease* 175 (1987) 526-536; N. Bolger and J.-P. Laurenceau, *Intensive Longitudinal Methods*
  (Guilford, 2013); P. Kuppens, N. B. Allen and L. B. Sheeber (2010); E. Dejonckheere et al. (2019).
* E. L. Hamaker, R. M. Kuiper and R. P. P. P. Grasman (2015).
* M. Scheffer et al., Early-warning signals for critical transitions, *Nature* 461 (2009) 53-59; I. A. van de
  Leemput et al. (2014); M. Wichers et al. (2016); M. A. Helmich et al. (2024).

## Problems and solutions

1. **min F′.** A by-participant test gives $F_1 = 6.0$ on (1, 29) df and a by-item test $F_2 = 2.0$ on (1, 18). Find min $F'$ and its denominator degrees of freedom.

   *Solution.* 6 × 2/(6 + 2) = 1.5; denominator df = (6 + 2)²/(6²/18 + 2²/29) = 64/(2 + 0.138) = 29.9. Not
   significant (p ≈ 0.23), though F₁ alone gave p ≈ 0.02.
2. **Shrinkage.** A person's own slope is 1.0 with sampling variance 0.09; people's slopes have mean 0.5 and variance 0.09. Find the multilevel estimate.

   *Solution.* The weight on the person's own estimate is 0.09/(0.09 + 0.09) = 0.5, so the estimate is
   0.5 + 0.5 × (1.0 - 0.5) = 0.75.
3. **Within and between.** A person averages $\bar x_p = 4$; today $x = 6$. With $\beta_W = 0.6$ and $\beta_B = -1$, split today's predicted value into its within and between parts.

   *Solution.* The within part is 0.6 × (6 - 4) = 1.2; the between part is -1 × 4 = -4.
4. **Inertia's bias.** True inertia 0.5, 25 occasions per person. Roughly what will the average estimate be?

   *Solution.* About 0.5 - (1 + 1.5)/25 = 0.5 - 0.1 = 0.4.
5. **Items limit precision.** Ten items per condition, items vary with SD 0.5, effect 0.4. With unlimited participants, what is the standard error of the effect?

   *Solution.* The difference of two means of ten item effects has SE √(2 × 0.5²/10) = 0.22, whatever
   the number of participants; an effect of 0.4 is then only 1.8 standard errors from zero.
6. **An AR(1) variance.** An AR(1) mood with $\phi = 0.4$ and shocks of SD 1. What is its variance?

   *Solution.* 1/(1 - 0.4²) = 1/0.84 = 1.19.
7. ★ **A diary study.** Design a diary study of whether poor sleep raises next-day anxiety within persons: occasions, lag, centring, model, and power at both levels.

   *Solution.* Prompt five times a day for four weeks, with sleep reported each morning and anxiety at each
   prompt; centre sleep on each person's mean and enter the departure and the mean separately; model next-day
   anxiety with random intercepts and random slopes for the within-person sleep effect, and an autoregressive term
   for anxiety; plan power by simulation at both levels (about 100 people for the between-person effect, enough
   days per person for the within-person slopes), and decide exclusions and the lag before the data.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Clark (1973) and min F′; Baayen, Davidson and Bates (2008); Barr et al. (2013); Matuschek et al. (2017); Judd,
Westfall and Kenny (2012); Yarkoni (2022); Laird and Ware (1982); Robinson (1950) and his state and individual
correlations; Simpson (1951); Molenaar (2004); Fisher, Medaglia and Jeronimus (2018) and the size of their
individual-to-group variance ratios; Csikszentmihalyi and Larson's experience sampling; Kuppens, Allen and Sheeber
(2010); Dejonckheere et al. (2019); Hamaker, Kuiper and Grasman (2015); Scheffer et al. (2009); van de Leemput et al.
(2014); Wichers et al. (2016); the prospective test cited as Helmich et al. (2024); Kendall's small-sample bias of
the autoregression; micro-randomized trials; and every page range in Sources.
