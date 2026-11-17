# Psychology, Built: Part 56, Psychology and Law

A witness picks a man from a line-up and is certain; years later DNA shows it was someone else. Mistaken
identification figures in about three quarters of the first 250 DNA exonerations in the United States. The
psychology of the courtroom is Parts 12 and 21 with a person's liberty attached, and for once the research changed
the practice. Then it changed its own mind about one of its reforms.

The viewer takes a line-up and predicts four numbers. Then the line-up as signal detection and the estimator
variables; simultaneous against sequential line-ups, and the ROC analysis that reversed a reform; confidence, its
calibration and its inflation; the system variables and the 2020 recommendations, with field data; false
confessions and interrogation; lie detection at 54% and the polygraph; context bias in forensic experts and the
reviews of forensic science; children's suggestibility and the memory wars; the story model, anchoring and the
hungry judges; risk tools and the impossibility result; and the standard error of an IQ score in *Hall v. Florida*.

## Where the numbers come from

| What | Source |
|---|---|
| Line-ups: six faces, the culprit's memory strength N(1.5, 1), others N(0, 1); simultaneous (max rule) and sequential (first face past the criterion) procedures, 100,000 simulated line-ups each, 33 criteria; at the criteria shown, simultaneous correct-ID 0.56 and innocent-suspect 0.11 (diagnosticity 5.3), sequential 0.43 and 0.06 (7.5); partial areas up to a false-ID rate of 0.16: 0.078 against 0.065 | Psyche (`work.lineup_roc`, `partial_auc`), item `roc` |
| The on-you line-up at a moderate criterion: culprit present 56% culprit, 31% filler, 13% no one; culprit absent 64% pick someone, 11% the innocent suspect | Psyche, item `onyou` |
| Confidence-accuracy: five confidence levels; initially 52%, 68%, 82%, 90% and 96% of suspect IDs correct; after feedback raising every suspect-picker one level, 93% at the top level, which holds twice as many IDs | Psyche (`work.confidence_feedback`), item `cac` |
| One calibrated risk score (d = 1.2) in groups with base rates 0.3 and 0.5, flagging above 50% risk: false-positive rates 10% and 28%, false-negative rates 54% and 27% | Psyche (`work.risk_groups`), item `risk` |
| IQ 71 with reliability 0.97: SEM 2.6, 95% interval 66 to 76 | Psyche (`work.score_interval`), item `iq` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/work.py` gains simultaneous and sequential line-ups by signal detection with ROC
  curves, diagnosticity ratios and partial areas, confidence and feedback inflation, a calibrated risk score's error
  rates across groups, and score intervals. Tested in `tests/psychology/test_work.py`.
* The Ledger gains six rows.
* The course's interactive: a staged event, a six-person line-up with confidence, and the reader's pick set beside
  the model's rates.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Sequential line-ups, one face at a time, are better than simultaneous ones at separating guilty from innocent suspects. | Lindsay and Wells 1985 | failed |
| Under fair, double-blind procedures, an eyewitness's initial high-confidence identification is usually accurate. | Juslin, Olsson and Winman 1996 | replicated |
| Innocent people accused of a minor laboratory offence often sign a confession, especially when presented with false evidence. | Kassin and Kiechel 1996 | replicated |
| People judging whether others are lying are only slightly better than chance. | Bond and DePaulo 2006 | replicated |
| Forensic examiners' conclusions can be changed by irrelevant contextual information. | Dror, Charlton and Peron 2006 | replicated |
| Judges grant parole far more often after a food break, and almost never just before one. | Danziger, Levav and Avnaim-Pesso 2011 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Garrett; Lindsay and Wells; Wells
and colleagues; Kassin and colleagues; Ceci and Bruck; Englich, Mussweiler and Strack; Dressel and Farid.

## Build it

```bash
python -m videos.psychology.psych56.compute            # every number (a minute)
python tools/qa_scene.py psych56 Sequential            # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych56 -q l   # the whole part, silent preview
python tools/build.py psych56                          # 1080p30 with narration
python tools/qa_scene.py psych56 Confidence --lang zh  # the Chinese edition of one chapter
python tools/make.py psych56                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 56                    # the lab: line-up ROCs, confidence, risk across groups
python tools/check_ledger.py psych56                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's work module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A certain witness | The exonerations; the question; objectives |
| 1 | On you: a line-up, and four numbers | The line-up; four predictions |
| 2 | The line-up as signal detection | Six faces, one criterion; estimator variables |
| 3 | Simultaneous against sequential | A reform adopted; the ROC reverses it |
| 4 | Confidence | Initial confidence under clean procedure; confidence grows after the fact |
| 5 | System variables and the reforms | What the system controls; real line-ups |
| 6 | False confessions | The ALT key; how interrogation produces them |
| 7 | Detecting lies | Fifty-four percent; the polygraph |
| 8 | Experts are people | The same fingerprints, again; forensic science reviewed |
| 9 | Children, suggestion and implanted memories | The day-care cases; the memory wars |
| 10 | Juries and judges | The story model, anchoring and deliberation; hungry judges |
| 11 | Risk assessment | Actuarial against clinical; calibrated and unequal |
| 12 | Numbers in court | *Hall v. Florida*; the Flynn effect in capital cases |
| 13 | The Ledger | Six rows; what they have in common |
| 14 | In practice: weighing an identification | Where this is a job; the likelihood ratio of a pick |
| 15 | Frontier: machines, interviews and tools | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 57 |

## Sources

* B. L. Garrett, *Convicting the Innocent* (Harvard University Press, 2011).
* S. E. Clark, A memory and decision model for eyewitness identification, *Applied Cognitive Psychology* 17 (2003)
  629-654; J. T. Wixted and L. Mickes, A signal-detection-based diagnostic-feature-detection model of eyewitness
  identification, *Psychological Review* 121 (2014) 262-276; G. L. Wells, Applied eyewitness-testimony research:
  system variables and estimator variables, *Journal of Personality and Social Psychology* 36 (1978) 1546-1557.
* R. C. L. Lindsay and G. L. Wells (1985); L. Mickes, H. D. Flowe and J. T. Wixted (2012); G. L. Wells et al.
  (2020).
* P. Juslin, N. Olsson and A. Winman (1996); G. L. Wells and A. L. Bradfield (1998); J. T. Wixted et al. (2016);
  J. T. Wixted and G. L. Wells (2017).
* S. M. Kassin and K. L. Kiechel (1996); M. B. Russano et al. (2005); S. M. Kassin et al. (2010).
* C. F. Bond and B. M. DePaulo (2006, 2008); M. Hartwig and C. F. Bond (2011); National Research Council, *The
  Polygraph and Lie Detection* (2003).
* I. E. Dror, D. Charlton and A. E. Peron (2006); I. E. Dror and D. Charlton (2006); J. Kukucka and S. M. Kassin
  (2014); National Research Council, *Strengthening Forensic Science in the United States* (2009); President's
  Council of Advisors on Science and Technology, *Forensic Science in Criminal Courts* (2016).
* S. J. Ceci and M. Bruck, *Jeopardy in the Courtroom* (American Psychological Association, 1995); E. F. Loftus and
  J. E. Pickrell, The formation of false memories, *Psychiatric Annals* 25 (1995) 720-725.
* N. Pennington and R. Hastie, Evidence evaluation in complex decision making, *Journal of Personality and Social
  Psychology* 51 (1986) 242-258; B. Englich, T. Mussweiler and F. Strack, Playing dice with criminal sentences,
  *Personality and Social Psychology Bulletin* 32 (2006) 188-200; S. Danziger et al. (2011); K. Weinshall-Margel and
  J. Shapard (2011); A. Glockner (2016).
* J. Dressel and H. Farid, The accuracy, fairness, and limits of predicting recidivism, *Science Advances* 4 (2018)
  eaao5580; A. Chouldechova, Fair prediction with disparate impact, *Big Data* 5 (2017) 153-163; J. Kleinberg, S.
  Mullainathan and M. Raghavan, Inherent trade-offs in the fair determination of risk scores (2016); J. Angwin, J.
  Larson, S. Mattu and L. Kirchner, Machine bias, *ProPublica* (2016).
* *Atkins v. Virginia*, 536 U.S. 304 (2002); *Hall v. Florida*, 572 U.S. 701 (2014).

## Problems and solutions

1. **Weighing a pick.** A line-up: correct-ID rate 0.60, innocent-suspect rate 0.05. The diagnosticity ratio, and the posterior odds from prior odds 1:4?

   *Solution.* The diagnosticity ratio is 0.60/0.05 = 12; posterior odds = 1/4 x 12 = 3, about 3 to 1 for
   guilt (75%), if the procedure was clean.
2. **A fair line-up.** Six faces, culprit absent, a fair line-up and a witness who picks someone 60% of the time: how often is the innocent suspect picked?

   *Solution.* In a fair culprit-absent line-up each face is equally likely to be picked: 0.60/6 = 0.10.
3. **Ratio against curve.** Why can a higher diagnosticity ratio come with a worse ROC? Draw two curves.

   *Solution.* The diagnosticity ratio rises as the criterion becomes stricter, along any one ROC;
   a procedure that only makes witnesses more cautious moves down its curve to a higher ratio, while its curve can
   lie below another procedure's everywhere.
4. **Lie judgements.** Lie judgements: 61% of truths and 47% of lies judged correctly. Overall accuracy with equal numbers?

   *Solution.* (0.61 + 0.47)/2 = 0.54.
5. **An interval.** IQ 69, reliability 0.95, SD 15: the SEM and the 95% interval.

   *Solution.* SEM = 15 sqrt(0.05) = 3.35; 69 +/- 1.96 x 3.35 = 62.4 to 75.6.
6. **Impossibility.** Base rates 0.2 and 0.4, one calibrated score: explain why the false-positive rates must differ.

   *Solution.* If the same score means the same risk in both groups, the higher base-rate group has more
   people at high scores, so more of its non-reoffenders are flagged too: its false-positive rate must be higher at
   any shared threshold, unless prediction is perfect.
7. ★ **A protocol.** Write the line-up protocol for a police force, with the reason for each rule.

   *Solution.* Double-blind administration (no cueing); unbiased instructions ("may or may not be present"); one
   suspect per line-up with fillers matching the description; an immediate confidence statement in the witness's
   words, recorded; video of the procedure; no repeated line-ups with the same suspect; no feedback.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Garrett's share of the first 250 exonerations; Clark (2003); Wells's system and estimator variables; Lindsay and
Wells (1985); Mickes, Flowe and Wixted (2012); the field comparison of procedures; the 2020 recommendations and
their list; Juslin et al. (1996); Wells and Bradfield (1998); the Houston field study; Kassin and Kiechel's 79
students and shares; Russano et al. (2005); Kassin et al. (2010); PEACE; Bond and DePaulo's 206 studies, 24,000
judges, 54%, 61% and 47%; the 2003 polygraph review; the Mayfield case; Dror, Charlton and Peron's five examiners
and four changes; Kukucka and Kassin (2014); the 2009 and 2016 reviews; Ceci and Bruck's experiments; the day-care
cases and convictions overturned; the NICHD protocol; Pennington and Hastie; Englich et al.'s dice; Danziger et
al.'s 1,112 rulings and 65%; the replies; Dressel and Farid's 65%; Chouldechova and Kleinberg et al.; ProPublica's
analysis; *Atkins* and *Hall*; the Flynn rate of about 0.3 points a year; machine face recognition and the
human-machine combination studies; the PEACE model's adoption in England and Wales and its stages;
Meissner et al. (2014); Dror et al. (2015) on linear sequential unmasking; the NICHD protocol's field studies
(Lamb and colleagues); Kassin and Sukel (1997) on the weight jurors give a coerced confession; Kukucka,
Kassin, Zapf and Dror (2017) on forensic examiners' bias blind spot; the age gradient in children's suggestibility
(Ceci and Bruck); and every page range in Sources. Chapter fourteen's posterior curves use Psyche's
simulated line-up rates at three criteria.
