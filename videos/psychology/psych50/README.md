# Psychology, Built: Part 50, The Weight of Evidence

In 2008 Erick Turner and colleagues put two piles side by side: the 74 antidepressant trials registered with the US
regulator, and what the journals printed. About half the trials were positive; in the journals almost all were, and
the average effect looked about a third larger. Part 4 told the replication crisis as a story; this part is the
mathematics of reading a literature that has been filtered, the forensic tools that caught impossible numbers, and
the argument that the deepest problem was never statistics but theory. The series' own Ledger is audited with its
own tools.

The viewer tests a mean that cannot be (5.19 from 28 whole-number answers) and predicts four numbers. Then the filter
simulated; fixed and random effects, a forest plot by hand and the prediction interval; meta-regression and its low
power; funnels, Egger's test, PET and PEESE, and what else makes a funnel lopsided; five correction methods run on
literatures with a known truth; meta-analyses against preregistered replications; registered reports and the other
designs that remove the filter; GRIM, SPRITE and statcheck; fabricated mileage detected; many analysts, one dataset,
and a specification curve; Meehl's paradox computed; and the Ledger's 263 findings audited by status, act and
decade.

## Where the numbers come from

| What | Source |
|---|---|
| The filter simulated: 74 trials of a drug with true effect 0.3 (between-trial SD 0.1), 40 to 160 per arm; every significant trial published and 35% of the others; 39 of 74 positive; 51 published, 39 of them positive; pooled effect 0.31 from all trials and 0.37 from the published | Psyche (`meta.literature`, `random_effects`), item `piles` |
| A forest plot: 15 studies, true mean 0.4, tau 0.15; random-effects mean 0.41 (95% interval 0.29 to 0.53; Hartung-Knapp 0.28 to 0.54), tau 0.17, I-squared 49%, prediction interval 0.03 to 0.79 | Psyche (`meta.random_effects`), item `forest` |
| Moderator power: half the studies 0.2 larger (0.5 against 0.3), tau 0.2, 20 to 80 per arm; power 25%, 30%, 59%, 87%, 99% with 10, 20, 40, 80, 160 studies (300 meta-analyses each) | Psyche (`meta.moderator_power`), item `moderator` |
| A funnel: 300 studies of a true 0.2 (tau 0.1), significant ones published and 15% of the rest, 30% of non-significant studies p-hacked; 118 published; Egger's intercept 1.43 (p = 0.002); PET 0.13, PEESE 0.30, naive 0.41 | Psyche (`meta.literature`, `egger`, `pet`, `peese`), item `funnel` |
| Every correction on every literature: six scenarios x 50 literatures of 150 studies; average estimates (naive, trim-and-fill, PET-PEESE, selection model, p-curve) 0.08, 0.07, -0.03, 0.00, 0.03 at no effect; 0.39, 0.36, 0.25, 0.20, 0.28 at 0.2; 0.59, 0.54, 0.45, 0.49, 0.53 at 0.5; 0.50, 0.40, 0.21, 0.19, 0.50 at 0.2 with tau 0.3; 0.22, 0.20, -0.01, 0.08, -0.01 at no effect with p-hacking; 0.20, 0.18, 0.17, 0.19, 0.24 at 0.2 with no filter | Psyche (`meta.grade`), item `grade` |
| Meta-analyses against replications: ten small true effects (0.03 to 0.23), each with a filtered literature of 60 studies and one replication of 1,500 per group; meta-analyses average 2.5 times the replications | Psyche (`meta.literature`, `random_effects`), item `kvarven` |
| GRIM on five means (5.19, n = 28; 3.45, 20; 4.68, 15; 2.17, 12; 6.33, 21): the first and third impossible; SPRITE samples of 20 on a 1-to-7 scale for mean 3.50 with SD 1.50 and 1.00 | Psyche (`meta.grim`, `sprite`), item `grim` |
| statcheck on six reported tests: one inconsistent at the 0.05 line (t(30) = 1.80 reported p = .04, recomputed .082) | Psyche (`meta.statcheck`), item `statcheck` |
| Mileage: 6,000 gamma-distributed differences (shape 2, scale 6,500) against 6,000 uniform on 0 to 50,000 | simulated, item `mileage` |
| A specification curve: 300 simulated people, a small true effect, four covariates; 96 specifications (covariate subsets, three outlier rules, raw or log outcome); estimates 0.05 to 0.21, 52% significant | Psyche (`meta.spec_curve`), item `specs` |
| Meehl's paradox: pairwise correlations N(0, 0.15^2), random directional predictions; confirmed 6%, 14%, 25%, 36%, 41%, 44% at n = 30, 100, 300, 1,000, 3,000, 10,000 | simulated, item `crud` |
| The Ledger audited: 263 rows through Part 49; 142 replicated, 19 smaller, 12 story and record, 49 contested, 35 failed, 2 retracted, 4 not directly tested; by act and by decade of the original | `explainer/psychology/ledger.py` via `meta.ledger_audit`, item `audit` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

The mileage histograms illustrate the shape of the published argument; they are not the study's data.

## Built in this part

* `explainer/psychology/psyche/meta.py`: simulated literatures with publication filters and p-hacking;
  DerSimonian-Laird pooling with Hartung-Knapp and prediction intervals; meta-regression and moderator power; Egger,
  PET, PEESE and PET-PEESE; trim-and-fill (L0); the three-parameter selection model; p-curve's skew test and estimate;
  a grading harness; GRIM, a SPRITE search and statcheck; a specification-curve engine; the Ledger audit. Tested in
  `tests/psychology/test_meta.py`.
* The Ledger gains five rows; Part 4's two declarations about meta-science are resolved.
* The course's interactive: the reader judges reported means as possible or impossible, then sees GRIM's verdict and
  the arithmetic.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| The journal literature on antidepressants overstated their efficacy relative to all the trials registered with the regulator, through unpublished negative trials and positively reported ones. | Turner and colleagues 2008 | replicated |
| Meta-analyses of published studies in psychology estimate effects about as large as large preregistered replications of the same effects find. | Hagger, Wood, Stiff and Chatzisarantis 2010 | failed |
| A substantial share of psychology articles report at least one p-value that does not match its test statistic and degrees of freedom. | Bakker and Wicherts 2011 | replicated |
| Researchers' beliefs, pooled in prediction markets or surveys, predict which published findings will replicate better than chance. | Dreber and colleagues 2015 | replicated |
| Discoveries made with preregistration, large samples and independent replication replicate at near the rate their statistical power predicts. | Protzko and colleagues 2023 | retracted |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Borenstein and colleagues; Brown
and Heathers; Heathers and colleagues; Steegen and colleagues with Simonsohn, Simmons and Nelson; Carter and
colleagues; Meehl; Oberauer and Lewandowsky; Smaldino and McElreath.

## Build it

```bash
python -m videos.psychology.psych50.compute            # every number (several minutes)
python tools/qa_scene.py psych50 Correct               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych50 -q l   # the whole part, silent preview
python tools/build.py psych50                          # 1080p30 with narration
python tools/qa_scene.py psych50 Forensics --lang zh   # the Chinese edition of one chapter
python tools/make.py psych50                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 50                    # the lab: filters, corrections, GRIM, specification curves
python tools/check_ledger.py psych50                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's meta module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Two piles of trials | Turner's two piles; the filter simulated; the question; objectives |
| 1 | On you: a mean that cannot be, and four numbers | GRIM in your head; four predictions |
| 2 | Combining studies | Fixed and random effects; a forest plot by hand; which interval answers your question |
| 3 | Moderators | Meta-regression; moderators hide |
| 4 | Seeing the filter | A funnel with a bite; Egger, PET and PEESE; other causes of asymmetry |
| 5 | Correcting for it | Five corrections; every method on every literature; no method works everywhere |
| 6 | Meta-analyses against replications | Ten effects measured twice; precise and wrong |
| 7 | Designs that remove the filter | Registered reports; registries, multi-site protocols and sequential designs |
| 8 | Forensic statistics | GRIM; SPRITE; statcheck |
| 9 | Fabrication, detected | Miles no one drives; what gives fabrication away |
| 10 | Many analysts, one dataset | Twenty-nine teams and the red cards; a specification curve |
| 11 | The theory crisis | Meehl's paradox; confirmed by crud; stronger theories |
| 12 | The Ledger, audited | 263 findings; where they held; reading the audit with the part's tools |
| 13 | The Ledger | Five rows; what they have in common |
| 14 | In practice: reviews, vendors and file drawers | Where a literature is weighed; your own file drawer |
| 15 | Frontier: rates, robots and incentives | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; Kant's three objections; payoffs; problems; references; Part 51 |

## Sources

* E. H. Turner et al. (2008); I. Kirsch et al. (2008); A. Cipriani et al. (2018).
* M. Borenstein, L. V. Hedges, J. P. T. Higgins and H. R. Rothstein, *Introduction to Meta-Analysis* (Wiley, 2009);
  J. P. T. Higgins, S. G. Thompson and D. J. Spiegelhalter, A re-evaluation of random-effects meta-analysis, *Journal
  of the Royal Statistical Society A* 172 (2009) 137-159.
* M. Egger, G. Davey Smith, M. Schneider and C. Minder, Bias in meta-analysis detected by a simple, graphical test,
  *BMJ* 315 (1997) 629-634; T. D. Stanley and H. Doucouliagos, Meta-regression approximations to reduce publication
  selection bias, *Research Synthesis Methods* 5 (2014) 60-78; S. Duval and R. Tweedie, Trim and fill, *Biometrics* 56
  (2000) 455-463; J. L. Vevea and L. V. Hedges, A general linear model for estimating effect size in the presence of
  publication bias, *Psychometrika* 60 (1995) 419-435; U. Simonsohn, L. D. Nelson and J. P. Simmons, p-curve and
  effect size, *Perspectives on Psychological Science* 9 (2014) 666-681; F. Bartos and U. Schimmack, Z-curve 2.0,
  *Meta-Psychology* 6 (2022); E. C. Carter, F. D. Schonbrodt, W. M. Gervais and J. Hilgard, Correcting for bias in
  psychology, *Advances in Methods and Practices in Psychological Science* 2 (2019) 115-144.
* M. S. Hagger et al. (2010, 2016); A. Kvarven, E. Stromland and M. Johannesson (2020); A. M. Scheel, M. R. M. J.
  Schijen and D. Lakens (2021).
* N. J. L. Brown and J. A. J. Heathers, The GRIM test, *Social Psychological and Personality Science* 8 (2017) 363-369;
  J. A. Heathers, J. Anaya, T. van der Zee and N. J. L. Brown, Recovering data from summary statistics: Sample
  Parameter Reconstruction via Iterative TEchniques (SPRITE), *PeerJ Preprints* (2018); M. Bakker and J. M. Wicherts
  (2011); M. B. Nuijten et al. (2016).
* L. L. Shu, N. Mazar, F. Gino, D. Ariely and M. H. Bazerman, Signing at the beginning makes ethics salient,
  *Proceedings of the National Academy of Sciences* 109 (2012) 15197-15200, retracted 2021; A. S. Kristal et al.,
  Signing at the beginning versus at the end does not decrease dishonesty, *Proceedings of the National Academy of
  Sciences* 117 (2020) 7103-7107.
* R. Silberzahn et al. (2018); S. Steegen, F. Tuerlinckx, A. Gelman and W. Vanpaemel, Increasing transparency
  through a multiverse analysis, *Perspectives on Psychological Science* 11 (2016) 702-712; U. Simonsohn,
  J. P. Simmons and L. D. Nelson, Specification curve analysis, *Nature Human Behaviour* 4 (2020) 1208-1214.
* P. E. Meehl, Theoretical risks and tabular asterisks, *Journal of Consulting and Clinical Psychology* 46 (1978)
  806-834; P. E. Meehl, Why summaries of research on psychological theories are often uninterpretable,
  *Psychological Reports* 66 (1990) 195-244; K. Oberauer and S. Lewandowsky, Addressing the theory crisis in
  psychology, *Psychonomic Bulletin and Review* 26 (2019) 1596-1618; T. Yarkoni (2022).
* A. Dreber et al. (2015); C. F. Camerer et al. (2018); E. Forsell et al. (2019); J. Protzko et al. (2023, retracted
  2024); P. E. Smaldino and R. McElreath, The natural selection of bad science, *Royal Society Open Science* 3 (2016)
  160384.

## Problems and solutions

1. **Fixed effect.** Three studies: $d$ = 0.2, 0.5, 0.3 with variances 0.01, 0.04, 0.02. Find the fixed-effect estimate.

   *Solution.* Weights 100, 25, 50; (100 x 0.2 + 25 x 0.5 + 50 x 0.3)/175 = (20 + 12.5 + 15)/175 = 0.27.
2. **I-squared.** $Q$ = 30 on 14 degrees of freedom. Find $I^2$.

   *Solution.* (30 - 14)/30 = 0.53.
3. **A prediction interval.** A random-effects mean of 0.4 with SE 0.05 and $\tau$ = 0.2: give a rough 95% prediction interval.

   *Solution.* Roughly 0.4 +/- 1.96 x sqrt(0.2^2 + 0.05^2) = 0.4 +/- 0.40, so about 0.0 to 0.8.
4. **GRIM.** $n$ = 17 answers on a 1-to-5 scale, reported mean 3.48. Apply GRIM.

   *Solution.* 3.48 x 17 = 59.16; 59/17 = 3.471 (3.47) and 60/17 = 3.529 (3.53): 3.48 is impossible.
5. **statcheck.** Reported: $t(24) = 1.90$, $p = .03$ (two-sided). Recompute $p$; is the error gross?

   *Solution.* p = 2 x P(t_24 > 1.90) = 0.070; the reported .03 is inconsistent, and gross: it crosses 0.05.
6. **PET against naive.** PET's intercept is 0.05 (SE 0.06) and the naive estimate 0.38. What do you report?

   *Solution.* Report both, and the selection model; PET's intercept near zero with a wide interval
   says the published estimate of 0.38 may be mostly filter. The honest summary is the range, and a call for a
   registered replication.
7. ★ **A plan.** Plan a meta-analysis of a literature you suspect is filtered: search, registries, models, corrections and how you will present their disagreement.

   *Solution.* Register the protocol; search databases, trial registries, preprints and authors for unpublished
   studies; pool by random effects with Hartung-Knapp and a prediction interval; draw the funnel and run Egger; run
   trim-and-fill, PET-PEESE, a selection model and p-curve; present all of them together as a sensitivity range;
   weight registered studies separately; and say what a decisive registered study would need.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Turner et al.'s 74 trials, the share positive, published and spun, and the size of the inflation; Kirsch et al.
(2008); Cipriani et al.'s 522 trials; Kvarven et al.'s fifteen comparisons and the factor of about three; Hagger et
al. (2010) and its estimate; Scheel et al.'s 96% and 44%; Brown and Heathers' findings; Heathers et al. (2018);
Bakker and Wicherts (2011); Nuijten et al.'s numbers of p-values and journals and their shares; Dreber et al.
(2015), Camerer et al. (2018) and Forsell et al. (2019); the Protzko et al. retraction and its reasons; the 2012
signing study, the 2021 analysis of its mileage data, its retraction and Kristal et al. (2020); Silberzahn et al.'s
29 teams and range of odds ratios; Steegen et al. (2016); Simonsohn et al. (2020); Meehl's papers and dates;
Oberauer and Lewandowsky (2019); Smaldino and McElreath (2016); Carter et al. (2019); the predictors of replication
named in the audit chapter; and every page range in Sources.
