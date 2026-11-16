# Psychology, Built: Part 55, Behaviour Change at Scale

In countries where people had to opt in to organ donation, few were donors; where they had to opt out, nearly
everyone was. A change of default, one sentence on a form, and the nudge became government policy around the world.
Then the accounting arrived: in published papers the average nudge moved behaviour by almost nine percentage
points; across every trial two government nudge units ran, by about one and a half. This part is that gap: what
changes behaviour at scale, by how much, and how we know.

The viewer ranks five ways to get people to the gym and predicts four numbers. Then automatic enrolment and the
algebra of a default; why defaults work and Save More Tomorrow; the toolbox and home energy reports; a megastudy with
its winner's curse and shrinkage; published nudges against nudge units, the meta-analysis and its correction;
heterogeneity and why effects shrink at scale; incentives for quitting and exercise; nudges that backfired;
campaigns and advertising; accuracy prompts and inoculation; a celebrated nudge that was fabricated, and choice
overload; and the ethics of steering.

## Where the numbers come from

| What | Source |
|---|---|
| The two-type reading of a default: opt-in (1 - q) p = 0.37 and opt-out q + (1 - q) p = 0.86 give q = 0.49 and p = 0.73 | Madrian and Shea's rates; Psyche (`work.default_inertia`), item `inertia` |
| A megastudy: 53 arms, true effects N(1 point, 1.2), base rate 30%, 1,200 people an arm and a control four times as large; the winner estimated at +7.0 points, truly +1.5, shrunk to +4.2 (weight 0.45 on its own estimate) | Psyche (`work.megastudy`), item `mega` |
| The winner's curse over 400 simulated megastudies: estimated +5.1, true +2.8, shrunk +2.3; shrinkage cuts the squared error by a factor of 4.0 | Psyche, item `curse` |
| A publication filter: 4,000 trials from one distribution of true effects (mean 1.4 points, SD 1.5); academic trials of 60 to 300 per arm, published if significant (and 10% of the rest), average 4.9 points as published (15% published); nudge-unit trials of 2,000 to 20,000 per arm, all reported, average 1.4 | Psyche (`work.publication_gap`), item `gap` |
| The power calculation in the worked trial: base 30%, two points, 80% power, 5% two-sided: about 8,400 per arm | the normal approximation |
| Every published number on screen | the studies listed under Sources, quoted as reported; the donation bars are approximate |

## Built in this part

* `explainer/psychology/psyche/work.py` gains the two-type default algebra, a megastudy simulator with the winner's
  curse and empirical-Bayes shrinkage, and a publication filter that reproduces the gap between published nudges and
  nudge-unit trials. Tested in `tests/psychology/test_work.py`.
* The Ledger gains six rows.
* The course's interactive: rank five gym interventions, then see the megastudy's pattern, its winner shrunk, and a
  comparison with forecasts.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Making enrolment in a retirement plan the default greatly increases participation. | Madrian and Shea 2001 | replicated |
| Mailing households a comparison of their energy use with their neighbours' reduces their consumption. | Schultz, Nolan, Cialdini, Goldstein and Griskevicius 2007 | replicated |
| Choice-architecture interventions change behaviour by about as much as the published studies report. | Mertens, Herberz, Hahnel and Brosch 2022 | replicated, smaller |
| Signing an honesty pledge at the top of a form, rather than the bottom, reduces dishonest reporting. | Shu, Mazar, Gino, Ariely and Bazerman 2012 | retracted |
| Offering more options reduces the likelihood of choosing and satisfaction with the choice. | Iyengar and Lepper 2000 | contested |
| Prompting people to think about accuracy improves the quality of the news they share. | Pennycook and colleagues 2021 | replicated, smaller |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Johnson and Goldstein;
DellaVigna and Linos; Thaler and Benartzi; Milkman and colleagues; Bryan, Tipton and Yeager; Volpp and colleagues;
Charness and Gneezy; Hall and Madsen; Kalla and Broockman; Lewis and Rao; Chater and Loewenstein.

## Build it

```bash
python -m videos.psychology.psych55.compute            # every number (seconds)
python tools/qa_scene.py psych55 Megastudy             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych55 -q l   # the whole part, silent preview
python tools/build.py psych55                          # 1080p30 with narration
python tools/qa_scene.py psych55 Reckoning --lang zh   # the Chinese edition of one chapter
python tools/make.py psych55                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 55                    # the lab: defaults, the megastudy, the publication filter
python tools/check_ledger.py psych55                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's work module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | One sentence on a form | Organ-donation defaults; the accounting; the question; objectives |
| 1 | On you: five ways to the gym, and four numbers | The ranking; four predictions |
| 2 | Why defaults work | Automatic enrolment and its algebra; three reasons; Save More Tomorrow |
| 3 | The toolbox | Choice architecture; home energy reports |
| 4 | The megastudy | Fifty-three ways to the gym; the winner's curse; shrinkage |
| 5 | The reckoning | Published against practice; the meta-analysis and its correction |
| 6 | Heterogeneity is the finding | Bryan, Tipton and Yeager; why effects shrink at scale |
| 7 | Incentives | Paying smokers to quit; paying for exercise |
| 8 | When nudges backfire | Fatality counts on highway signs; norms that license |
| 9 | Persuasion at scale | Campaign contact; advertising |
| 10 | Misinformation | Accuracy prompts; inoculation |
| 11 | A nudge that never was | Signing at the top; too many jams |
| 12 | Ethics and limits | Autonomy, transparency and sludge; the individual frame and the system |
| 13 | The Ledger | Six rows; what they have in common |
| 14 | In practice: a trial, designed | Where this is a job; a worked trial |
| 15 | Frontier: predicting what works where | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 56 |

## Sources

* E. J. Johnson and D. Goldstein, Do defaults save lives?, *Science* 302 (2003) 1338-1339; R. H. Thaler and C. R.
  Sunstein, *Nudge* (Yale University Press, 2008; final edition, Penguin, 2021).
* B. C. Madrian and D. F. Shea (2001); J. J. Choi et al. (2004); J. Beshears et al. (2009); R. H. Thaler and S.
  Benartzi, Save More Tomorrow, *Journal of Political Economy* 112 (2004) S164-S187.
* P. W. Schultz et al. (2007); H. Allcott (2011); H. Allcott and T. Rogers (2014); E. P. Bettinger, B. T. Long, P.
  Oreopoulos and L. Sanbonmatsu, The role of application assistance and information in college decisions, *Quarterly
  Journal of Economics* 127 (2012) 1205-1242.
* K. L. Milkman et al., Megastudies improve the impact of applied behavioural science, *Nature* 600 (2021) 478-483.
* S. DellaVigna and E. Linos (2022); S. Mertens et al. (2022); M. Maier et al. (2022); B. Szaszi et al., No reason to
  expect large and consistent effects of nudge interventions, *Proceedings of the National Academy of Sciences* 119
  (2022) e2200732119.
* C. J. Bryan, E. Tipton and D. S. Yeager, Behavioural science is unlikely to change the world without a
  heterogeneity revolution, *Nature Human Behaviour* 5 (2021) 980-989.
* K. G. Volpp et al., A randomized, controlled trial of financial incentives for smoking cessation, *New England
  Journal of Medicine* 360 (2009) 699-709; S. D. Halpern et al., Randomized trial of four financial-incentive programs
  for smoking cessation, *New England Journal of Medicine* 372 (2015) 2108-2117; G. Charness and U. Gneezy, Incentives
  to exercise, *Econometrica* 77 (2009) 909-931.
* J. D. Hall and J. M. Madsen, Can behavioral interventions be too salient? Evidence from traffic safety messages,
  *Science* 376 (2022) eabm3427.
* J. L. Kalla and D. E. Broockman, The minimal persuasive effects of campaign contact in general elections, *American
  Political Science Review* 112 (2018) 148-166; R. A. Lewis and J. M. Rao, The unfavorable economics of measuring the
  returns to advertising, *Quarterly Journal of Economics* 130 (2015) 1941-1973; T. Blake, C. Nosko and S. Tadelis,
  Consumer heterogeneity and paid search effectiveness, *Econometrica* 83 (2015) 155-174.
* G. Pennycook et al. (2021); J. Roozenbeek et al. (2021); G. Pennycook and D. G. Rand (2022); J. Roozenbeek, S. van
  der Linden, B. Goldberg, S. Rathje and S. Lewandowsky, Psychological inoculation improves resilience against
  misinformation on social media, *Science Advances* 8 (2022) eabo6254.
* L. L. Shu et al. (2012, retracted 2021); A. S. Kristal et al. (2020); S. S. Iyengar and M. R. Lepper (2000); B.
  Scheibehenne et al. (2010); A. Chernev et al. (2015).
* N. Chater and G. Loewenstein, The i-frame and the s-frame, *Behavioral and Brain Sciences* 46 (2023) e147.

## Problems and solutions

1. **The default algebra.** q = 0.9 - 0.4 = 0.5; p = 0.4/(1 - 0.5) = 0.8.
2. **Shrinkage.** The weight on the arm's own estimate is 1/(1 + 1.5^2) = 0.31; shrunk = 1 + 0.31 x (5 - 1) = +2.2
   points.
3. **A trial's size.** n = (1.96 + 0.84)^2 (0.3 x 0.7 + 0.32 x 0.68)/0.02^2 = about 8,400 per arm.
4. **A filtered average.** Published only if the estimate exceeds 1.96 x 4 = 7.8 points; the mean of N(1.5, 4)
   above 7.8 is 1.5 + 4 phi(1.57)/(1 - Phi(1.57)) = about 9.5 points, six times the truth.
5. **Cost per kWh.** Twelve letters cost $12 a year; 2% of 10,000 kWh is 200 kWh; $0.06 per kWh saved.
6. **Nudge or manipulation.** The disclosure test: would it still work if the person were told exactly what was done
   and why? A pre-ticked enrolment box with a plain statement ("we have enrolled you; untick to opt out") still
   works in studies that disclosed it, so it passes; a hidden subscription renewal does not.
7. **A trial design.** One primary outcome from administrative data, preregistered; arms for the current reminder,
   the new one and a variant; randomization by person with a power calculation from the base rate and the smallest
   effect worth having; the interval reported whatever it shows; planned subgroup checks only; a follow-up for
   persistence; and the cost per unit of change.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Johnson and Goldstein's country rates and online experiment; evidence on opt-out and actual donation rates; Madrian
and Shea's 37% and 86% and the default contribution rate; Choi et al. (2004) and Beshears et al. (2009); Save More
Tomorrow's rates (3.5% to 13.6% over four years); Bettinger et al.'s aid-form result; Allcott's 600,000 households
and 2%; Allcott and Rogers on persistence; Schultz et al.'s boomerang; Milkman et al.'s 61,000 members, 53 arms, the
best arm and the forecasts; DellaVigna and Linos's 126 trials, 8.7 and 1.4; Mertens et al.'s d = 0.43 and number of
studies; Maier et al.'s correction; Szaszi et al. (2022); Bryan, Tipton and Yeager (2021); Volpp et al.'s $750 and
the tripling; Halpern et al. (2015); Charness and Gneezy (2009); Hall and Madsen's Texas signs; Kalla and
Broockman's 49 experiments; Lewis and Rao's 25 experiments; Blake, Nosko and Tadelis (2015); Pennycook et al. (2021)
and the replications and meta-analysis; the inoculation studies; the signing study's 2020 replication, 2021
analysis and retraction; Iyengar and Lepper's jams and percentages; Scheibehenne et al.'s 50 experiments; Chernev et
al.'s moderators; Chater and Loewenstein (2023); and every page range in Sources.
