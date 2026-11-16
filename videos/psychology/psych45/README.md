# Psychology, Built: Part 45, Item Response Theory

Two pupils of the same ability take different forms of a reading test and score eight and three out of ten. In the
1950s the Danish mathematician Georg Rasch was asked to compare reading across tests that share no items, and
modelled the single encounter of one person with one item: the odds of success depend only on ability minus
difficulty. Person and item separate, and from that idea come adaptive tests, a statistical definition of an unfair
item, national surveys that report populations, and software that tracks what a learner knows.

The viewer watches an adaptive test narrow on Psyche and predicts four numbers. Then the blind spots of classical
scores (computed); the Rasch model, specific objectivity and the sufficient sum score, derived and checked on the
LSAT; discrimination and guessing, and the LSAT's Rasch and two-parameter fits (matching the published fits);
information and the standard error by ability; joint, conditional and marginal estimation, Bock and Aitkin's EM and
ability estimates; an adaptive test against fixed forms, and item exposure (computed); the graded response model on
attitude items; differential item functioning by Mantel and Haenszel, separating bias from impact (computed);
mean-sigma linking (computed); matrix sampling and plausible values with a conditioning model (computed); and
knowledge tracing and Elo (computed).

## Where the numbers come from

| What | Source |
|---|---|
| The hook: two forms of 10 Rasch items (difficulties -2.5 to 0 and 0 to 2.5); a person of ability 0.5 expects 8.3 and 3.4 | Psyche (`irt.prob`), item `classical` |
| Classical blind spots: 10 items (difficulties -2 to 2) answered by 2,000 simulated people of mean -0.7 and 2,000 of mean 0.7; item 5 right for 39% and 69%; the classical SEM (alpha 0.62) against the IRT standard error, 0.74 at the middle and 1.2 at ±3 | Psyche (`irt.simulate`, `irt.fixed_form_se`), item `classical` |
| The LSAT's five items, 1,000 people: proportions correct 0.92, 0.71, 0.55, 0.76, 0.87; Rasch (common slope 0.755) difficulties -3.615, -1.322, -0.318, -1.730, -2.780, log-likelihood -2466.94; two-parameter slopes 0.66 to 0.89, log-likelihood -2466.65; likelihood ratio 0.57 on 4 df (p = 0.97); conditional ML difficulties (centred) -1.256, 0.475, 1.236, 0.168, -0.623 from the 699 people with scores 1 to 4; P(1 1 0 0 0 given a score of 2) = 0.129 at every ability | `opendata.lsat_1000` (ltm 1.2-0, fetched from CRAN and SHA-256 checked); Psyche (`irt.fit_mml`, `irt.fit_cml`), item `lsat`; the fits match ltm's |
| EM on the LSAT: log-likelihood -2475.5 after one cycle, -2466.65 after forty; EAP abilities by score -1.91 to 0.63 with posterior SD near 0.8 | Psyche (`irt.fit_mml`, `irt.eap`, `irt.mle_theta`), item `em` |
| LSAT test information: largest (0.58) at ability -1.75; smallest standard error 1.31 | Psyche (`irt.info`), item `info` |
| Adaptive testing: a bank of 300 simulated two-parameter items, 1,000 simulated people: stopping at SE 0.3 takes 17 items on average (RMSE 0.28); the best fixed form needs about 35 items for the same error, a random form about 60; the first item reaches every test-taker | Psyche (`irt.cat`, `irt.eap`), item `cat` |
| Rating scales: four items on science and technology (Comfort, Work, Future, Benefit), 392 people, four categories: discriminations 1.04, 1.23, 2.30, 1.09; thresholds as fitted | `opendata.science_attitudes` (ltm 1.2-0); Psyche (`irt.fit_grm`), item `grm`; the fit matches ltm's |
| DIF: 15 Rasch items, two groups of 3,000 whose means differ by 0.8: on a fair item the proportions correct differ by 0.15 but the Mantel-Haenszel delta is 0.05 (category A); with the item made 0.8 harder for one group, delta -1.85 (category C) | Psyche (`irt.mantel_haenszel`), item `dif` |
| Linking: two 30-item forms sharing 10 anchors; this year's group has mean 0.5 and SD 1.2; mean-sigma A = 1.21, B = 0.43; the new items' difficulties off by 0.40 before linking and 0.07 after; true-score equating: 6, 10, 15, 20 and 24 on this year's form equal 6.6, 11.0, 16.1, 20.9 and 24.5 on last year's | Psyche (`irt.fit_mml`, `irt.mean_sigma`), item `linking` |
| Plausible values: 4,000 students, 24 items in 4 booklets of 6, two groups 0.41 apart: SD 1.03 (truth), 0.73 (EAP), 1.02 (plausible values), 1.06 (conditioned); gap 0.22 (EAP), 0.22 (unconditioned plausible values), 0.44 (conditioned) | Psyche (`irt.eap`, `irt.plausible_values`, `irt.latent_em`), item `pv` |
| Knowledge tracing: 500 simulated students, 10 practices, truth (0.2, 0.15, 0.2, 0.1); fitted (0.18, 0.15, 0.20, 0.09); one student's P(known) passing 0.95 by the fifth practice; Elo difficulties falling with practice | Psyche (`irt.bkt_fit`, `irt.bkt_filter`, `irt.elo_learn`), item `bkt` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

The diagram of knowledge tracing's two states is schematic; the
adaptive test on screen is Psyche's, on a simulated bank.

## Built in this part

* `explainer/psychology/psyche/irt.py`: the 3PL model and its information, marginal ML by EM on a quadrature grid
  (checked by direct maximization and against ltm's published fits), conditional ML through the elementary
  symmetric functions, EAP and ML abilities, an adaptive test, Samejima's graded response model, Mantel-Haenszel
  DIF, mean-sigma linking, a conditioning model and plausible values, Bayesian knowledge tracing and Elo. Tested in
  `tests/psychology/test_irt.py`.
* `explainer/psychology/opendata.py` reads the LSAT and Eurobarometer items from ltm 1.2-0 (CRAN), checked by
  SHA-256 and never committed.
* The Ledger gains two rows.
* The course's interactive: an adaptive test of ten "which is larger?" pairs, chosen one at a time, with the band
  narrowing; its difficulties are illustrative and nothing is stored.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| An adaptive test reaches the precision of a fixed test with far fewer items, often about half. | Weiss 1982 | replicated |
| A recurrent neural network predicts students' answers far better than Bayesian knowledge tracing. | Piech and colleagues 2015 | replicated, smaller |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Rasch; Lord and Novick, and Lord;
Holland and Thayer; van der Linden.

## Build it

```bash
python -m videos.psychology.psych45.compute            # every number (about a minute; fetches the data once)
python tools/qa_scene.py psych45 Cat                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych45 -q l   # the whole part, silent preview
python tools/build.py psych45                          # 1080p30 with narration
python tools/qa_scene.py psych45 Dif --lang zh         # the Chinese edition of one chapter
python tools/make.py psych45                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 45                    # the lab: LSAT fits, information, CAT, DIF, tracing
python tools/check_ledger.py psych45                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's irt module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Different questions, one scale | Two forms, one ability; one person, one item; the question; objectives |
| 1 | On you: an adaptive test, and four numbers | An adaptive test narrowing; four predictions |
| 2 | What classical theory cannot do | Difficulty depends on who answers; one error for everyone? |
| 3 | The Rasch model | One encounter; specific objectivity; the sum score is enough |
| 4 | Two and three parameters | Discrimination and guessing; five law-school items |
| 5 | Information | Fisher information, item by item; what five easy items can measure |
| 6 | Estimation | Three ways to estimate items; Bock and Aitkin's EM; each person's ability |
| 7 | Adaptive testing | Four steps, repeated; the same precision with half the items; the costs |
| 8 | Rating scales | Samejima's graded responses; four items, four discriminations |
| 9 | Fairness as a statistic | A gap is not a bias; Mantel and Haenszel, score by score |
| 10 | Linking and equating | Two years, two forms; mean and sigma; from score to score |
| 11 | Large-scale assessment | Many items, few per student; plausible values |
| 12 | Tracking learning | Bayesian knowledge tracing; one student; Elo and deeper models |
| 13 | The Ledger | Two rows; what they have in common |
| 14 | In practice: exams, clinics and machines | Where it runs; measuring machines |
| 15 | Frontier: time, generated items and learning systems | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; Kant's three objections; payoffs; problems; references; Part 46 |

## Sources

* G. Rasch, *Probabilistic Models for Some Intelligence and Attainment Tests* (Danish Institute for Educational
  Research, 1960); F. M. Lord and M. R. Novick, *Statistical Theories of Mental Test Scores* (Addison-Wesley,
  1968), with A. Birnbaum's chapters; F. M. Lord, *Applications of Item Response Theory to Practical Testing
  Problems* (Erlbaum, 1980); S. E. Embretson and S. P. Reise, *Item Response Theory for Psychologists* (Erlbaum,
  2000); W. J. van der Linden (ed.), *Handbook of Item Response Theory* (CRC Press).
* R. D. Bock and R. Lieberman, Fitting a response model for n dichotomously scored items, *Psychometrika* 35 (1970)
  179-197; R. D. Bock and M. Aitkin, Marginal maximum likelihood estimation of item parameters: application of an
  EM algorithm, *Psychometrika* 46 (1981) 443-459; D. Rizopoulos, ltm: an R package for latent variable modeling
  and item response theory analyses, *Journal of Statistical Software* 17 (2006).
* F. Samejima, *Estimation of Latent Ability Using a Response Pattern of Graded Scores*, Psychometrika Monograph 17
  (1969); G. N. Masters, A Rasch model for partial credit scoring, *Psychometrika* 47 (1982) 149-174.
* D. J. Weiss (1982); H. Wainer (ed.), *Computerized Adaptive Testing: A Primer* (2nd edition, 2000); J. B. Sympson
  and R. D. Hetter (1985) on exposure control; D. Cella et al. (2010) on PROMIS.
* P. W. Holland and D. T. Thayer, Differential item performance and the Mantel-Haenszel procedure, in H. Wainer and
  H. I. Braun (eds.), *Test Validity* (Erlbaum, 1988) 129-145; P. W. Holland and H. Wainer (eds.), *Differential
  Item Functioning* (1993).
* M. J. Kolen and R. L. Brennan, *Test Equating, Scaling, and Linking* (3rd edition, Springer, 2014).
* R. J. Mislevy, Randomization-based inference about latent variables from complex samples, *Psychometrika* 56
  (1991) 177-196.
* A. T. Corbett and J. R. Anderson, Knowledge tracing: modeling the acquisition of procedural knowledge, *User
  Modeling and User-Adapted Interaction* 4 (1995) 253-278; C. Piech et al. (2015); M. Khajah, R. V. Lindsey and
  M. C. Mozer (2016); X. Xiong et al. (2016); R. Pelánek, Applications of the Elo rating system in adaptive
  educational systems, *Computers and Education* 98 (2016) 169-179.
* W. J. van der Linden, A hierarchical framework for modeling speed and accuracy on test items, *Psychometrika* 72
  (2007) 287-308.

## Problems and solutions

1. **A Rasch probability.** e^0.5/(1 + e^0.5) = 1.649/2.649 = 0.622.
2. **Information.** At θ = 0, P = 0.5 and I = 4 × 0.25 = 1. At θ = 1, P = 1/(1 + e^-2) = 0.881 and
   I = 4 × 0.881 × 0.119 = 0.42.
3. **A test's standard error.** Each item gives 1.5² × 0.25 = 0.5625; ten give 5.625, so SE = 1/√5.625 = 0.42.
4. **Sufficiency by hand.** P(1 0 | r = 1) = e^0/(e^0 + e^-1) = 1/(1 + 0.368) = 0.731, whatever θ: the factor
   e^θ/((1 + e^(θ-0))(1 + e^(θ-1))) is common to both patterns and cancels.
5. **Linking.** A = 1.0/0.8 = 1.25, B = 0.4 - 1.25 × 0 = 0.4; the new item's difficulty on last year's scale is
   1.25 × 1 + 0.4 = 1.65.
6. **A step of knowledge tracing.** After a right answer, P(known) = 0.2 × 0.9/(0.2 × 0.9 + 0.8 × 0.2) = 0.18/0.34 =
   0.529; after the learning step, 0.529 + 0.471 × 0.15 = 0.600.
7. **An adaptive anxiety questionnaire.** A bank of 60 or more graded items calibrated in a large sample spanning
   the range of severity; EAP scoring from a normal prior; the most informative item at each step, chosen at random
   among the best three for exposure, with at least one item from each content area (physical, cognitive,
   avoidance); stop at SE 0.3 or 12 items; before use, test each item for DIF between the two language versions by
   ordinal logistic regression or a graded-response likelihood-ratio test matched on the latent score, revise or
   drop flagged items, and link the two versions through items that function the same.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Rasch's 1950s commission (reading tests for Danish schools and the military's intelligence tests) and his 1960
book; the LSAT data's origin as Section 6 of the Law School Admission Test, analysed by Bock and Lieberman (1970);
the Eurobarometer items' wording, year (1992) and British sample (as documented in ltm); Birnbaum's chapters in Lord
and Novick (1968); Bock and Aitkin (1981); Samejima (1969) and Masters (1982); Weiss (1982) and the "about half"
saving; Sympson and Hetter's exposure control; the PROMIS item banks and adaptive forms (Cella et al. 2010); Holland
and Thayer (1988) and the ETS A/B/C categories (|Δ| below 1; 1.5 or more and significant); Kolen and Brennan's
methods; Mislevy (1991) and plausible values in NAEP and PISA; Corbett and Anderson (1995) and the 0.95 mastery
rule; Piech et al.'s AUCs (about 0.86 against 0.67), Khajah, Lindsey and Mozer (2016) and Xiong et al. (2016);
van der Linden (2007); the use of item response models for AI benchmarks; and every page range in Sources.
