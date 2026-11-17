# Psychology, Built: Part 53, People at Work

From 1924 to 1927 engineers at Western Electric's Hawthorne Works varied the lighting where workers assembled
telephone parts, and, as the story goes, output rose whatever they did. The Hawthorne effect entered every textbook;
when Steven Levitt and John List found the original records in 2011, the evidence for it was slight. The real
history of work psychology is less romantic and more useful: the correlation between a hiring method and later
performance, estimated across a century and revised sharply in 2022.

The viewer chooses between two candidates and predicts four numbers. Then the first tests and the Army's in 1917;
validity, the criterion problem and rater noise; range restriction and unreliability simulated on 200,000 applicants,
corrected in order, and a correction that overshoots; Schmidt and Hunter's 1998 summary against Sackett and
colleagues' 2022 revision; interviews, noise and structure; Taylor-Russell tables and the Brogden-Cronbach-Gleser
utility; adverse impact, *Griggs* and the validity-diversity frontier; algorithms that learned past hiring; Herzberg's two factors and Vroom's expectancy
theory with their records; goals;
pay by the windshield and a fine that became a price; satisfaction, psychological safety, leadership (Lewin's clubs, traits, the Ohio
dimensions, transformational leadership and the critique of its measures) and a randomized trial of
working from home.

## Where the numbers come from

| What | Source |
|---|---|
| 200,000 simulated applicants: predictor and true performance correlated 0.50; a rating with reliability 0.6 among applicants; the top 20% hired. Observed validity among the hired 0.19; incumbents' rating reliability 0.54; u = 2.12; corrected for unreliability 0.25, then for range restriction (Case II) 0.49; truth 0.50 | Psyche (`work.selection`, `case2`), item `selection` |
| The overcorrection: an unrestricted study observes 0.39; corrected with the borrowed u, 0.78; truth 0.50 | Psyche, item `overcorrect` |
| Taylor-Russell success rates at a base rate of 0.5, validities 0 to 0.5, selection ratios 0.05 to 0.9 (for example 0.67 at r = 0.3 and 20% hired) | Psyche (`work.taylor_russell`, bivariate normal), item `tr` |
| Brogden-Cronbach-Gleser utility: 100 hires, 5 years, SD_y 20,000 a year, top 20%, 100 per applicant tested; net 4.3 million (r = 0.31), 5.8 million (0.42), 2.6 million (0.19), 7.1 million (0.51) | Psyche (`work.bcg_utility`), item `utility` |
| Adverse impact at an overall selection ratio of 20% with 30% of applicants in the lower-scoring group: impact ratios 1.0, 0.75, 0.55, 0.40, 0.28, 0.20 for group differences 0 to 1.0 SD | Psyche (`work.adverse_impact`), item `impact` |
| The frontier: an ability test (validity 0.31, d = 0.8) and a structured interview (0.42, d = 0.3), correlated 0.3 (illustrative inputs); the most valid mix 0.46 with impact ratio 0.42; interview alone 0.42 and 0.65; test alone 0.31 and 0.28 | Psyche (`work.frontier`), item `frontier` |
| Interviews: 20,000 simulated candidates; validities of the test 0.29, unstructured interview 0.18, structured 0.39, a holistic combination weighting the unstructured impression 0.7: 0.28, the test and structured interview combined by regression 0.49 | Psyche (`work.interviews`), item `interviews` |
| The hiring choice: among 1,000 simulated pairs where A has the much better test and B the much better unstructured impression, A performs better 57% of the time | Psyche, item `hire` |
| The validities of 1998 and 2022 | Schmidt and Hunter (1998); Sackett et al. (2022), as reported |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/work.py` gains a selection simulator (observed validity under unreliability and range
  restriction with Thorndike's Case II correction), Taylor-Russell success rates, the Brogden-Cronbach-Gleser
  utility, adverse impact with the four-fifths rule, the validity-diversity frontier, and an interview-noise model
  with holistic and mechanical combination. Tested in `tests/psychology/test_work.py`.
* The Ledger gains four rows; goal setting is Part 28's row.
* The course's interactive: hire from pairs of candidates described by a test score and an interview impression,
  then see how often your choices beat the test alone.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| In the Hawthorne illumination studies, output rose whenever the lighting was changed, because the workers knew they were being studied. | Roethlisberger and Dickson 1939 | story and record |
| Structured employment interviews predict job performance better than unstructured ones. | McDaniel, Whetzel, Schmidt and Maurer 1994 | replicated |
| General mental ability tests predict job performance with a corrected validity of about 0.5, the best single predictor. | Schmidt and Hunter 1998 | contested |
| Introducing a small fine for late pick-up at daycare centres increased late pick-ups, which stayed high after the fine was removed. | Gneezy and Rustichini 2000 | not directly tested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Lazear; Judge and colleagues;
Edmondson; Bloom and colleagues; the combined tag for Schmidt and Hunter with Sackett and colleagues.

## Build it

```bash
python -m videos.psychology.psych53.compute            # every number (seconds)
python tools/qa_scene.py psych53 Corrections           # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych53 -q l   # the whole part, silent preview
python tools/build.py psych53                          # 1080p30 with narration
python tools/qa_scene.py psych53 Fairness --lang zh    # the Chinese edition of one chapter
python tools/make.py psych53                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 53                    # the lab: restriction, utility, impact, the frontier
python tools/check_ledger.py psych53                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's work module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The lights at Hawthorne | The story; the data, found again; the question; objectives |
| 1 | On you: two candidates, and four numbers | The hiring choice; four predictions |
| 2 | Testing a nation | Taylor, Münsterberg and the Gilbreths; the Army tests of 1917 |
| 3 | Validity and the criterion | A predictor and a criterion; the criterion problem |
| 4 | Why observed validities mislead | Range restriction; two corrections, in order |
| 5 | A century of evidence, revised | 1998 and 2022; how a correction overshoots |
| 6 | The interview | Noise that feels like signal; structure as the fix |
| 7 | From a correlation to money | Taylor and Russell; the Brogden-Cronbach-Gleser formula |
| 8 | Fairness | Adverse impact; *Griggs* and after; the validity-diversity frontier |
| 9 | Algorithms in hiring | A screen that learned the past; auditing an algorithm |
| 10 | Goals | Goal-setting theory; when goals go wrong |
| 11 | Pay, and what money crowds out | Paying by the windshield; a fine is a price |
| 12 | Satisfaction, teams and where people work | Satisfaction and performance; psychological safety; working from home, randomized |
| 13 | The Ledger | Four rows; what they have in common |
| 14 | In practice: a selection system, designed | Where this is a job; a worked design |
| 15 | Frontier: new assessments, old questions | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 54 |

## Sources

* F. J. Roethlisberger and W. J. Dickson (1939); S. D. Levitt and J. A. List (2011).
* H. Münsterberg, *Psychology and Industrial Efficiency* (Houghton Mifflin, 1913); F. W. Taylor, *The Principles of
  Scientific Management* (1911); R. M. Yerkes (ed.), *Psychological Examining in the United States Army* (1921).
* S. E. Scullen, M. K. Mount and M. Goff, Understanding the latent structure of job performance ratings, *Journal of
  Applied Psychology* 85 (2000) 956-970; C. Viswesvaran, D. S. Ones and F. L. Schmidt, Comparative analysis of the
  reliability of job performance ratings, *Journal of Applied Psychology* 81 (1996) 557-574.
* R. L. Thorndike, *Personnel Selection* (Wiley, 1949); F. L. Schmidt and J. E. Hunter (1998); P. R. Sackett, C.
  Zhang, C. M. Berry and F. Lievens (2022); I.-S. Oh, H. Le and P. L. Roth (2023).
* M. A. McDaniel et al. (1994); J. Dana, R. Dawes and N. Peterson, Belief in the unstructured interview: the
  persistence of an illusion, *Judgment and Decision Making* 8 (2013) 512-520; S. Highhouse, Stubborn reliance on
  intuition and subjectivity in employee selection, *Industrial and Organizational Psychology* 1 (2008) 333-342.
* H. C. Taylor and J. T. Russell, The relationship of validity coefficients to the practical effectiveness of tests
  in selection, *Journal of Applied Psychology* 23 (1939) 565-578; H. E. Brogden, When testing pays off, *Personnel
  Psychology* 2 (1949) 171-183; L. J. Cronbach and G. C. Gleser, *Psychological Tests and Personnel Decisions*
  (2nd edition, University of Illinois Press, 1965).
* *Griggs v. Duke Power Co.*, 401 U.S. 424 (1971); Uniform Guidelines on Employee Selection Procedures (1978); W. De
  Corte, F. Lievens and P. R. Sackett, Combining predictors to achieve optimal trade-offs between selection quality
  and adverse impact, *Journal of Applied Psychology* 92 (2007) 1380-1393.
* New York City Local Law 144 of 2021 on automated employment decision tools (enforced from 2023).
* E. A. Locke (1968); E. A. Locke and G. P. Latham (2002); M. E. Schweitzer, L. Ordóñez and B. Douma, Goal setting as
  a motivator of unethical behavior, *Academy of Management Journal* 47 (2004) 422-432.
* E. P. Lazear, Performance pay and productivity, *American Economic Review* 90 (2000) 1346-1361; U. Gneezy and A.
  Rustichini (2000); U. Gneezy, S. Meier and P. Rey-Biel (2011).
* T. A. Judge, C. J. Thoresen, J. E. Bono and G. K. Patton, The job satisfaction-job performance relationship,
  *Psychological Bulletin* 127 (2001) 376-407; A. Edmondson, Psychological safety and learning behavior in work
  teams, *Administrative Science Quarterly* 44 (1999) 350-383; N. Bloom, J. Liang, J. Roberts and Z. J. Ying, Does
  working from home work? Evidence from a Chinese experiment, *Quarterly Journal of Economics* 130 (2015) 165-218.

## Problems and solutions

1. **Two corrections.** An observed validity of 0.25 among hires, criterion reliability 0.5 among them, $u$ = 1.5. Correct for both, in order.

   *Solution.* 0.25/sqrt(0.5) = 0.354; Case II with u = 1.5: 0.354 x 1.5 / sqrt(1 + 0.125 x 1.25) = 0.49.
2. **Utility.** Validity 0.3, top 10% hired: $\bar z_x = \phi(1.28)/0.1$. With $SD_y$ = 15,000, 50 hires, 4 years, find the gain before costs.

   *Solution.* z = 1.28, phi(1.28) = 0.175, so the mean score of those hired is 1.75; 50 x 4 x 0.3 x 15,000 x 1.75 =
   about 1.58 million before costs.
3. **Four-fifths.** Selection rates 30% and 20%. Compute the impact ratio. Does it pass the four-fifths rule?

   *Solution.* 0.20/0.30 = 0.67 < 0.8: flagged for adverse impact.
4. **A composite.** Two predictors, validities 0.3 and 0.4, correlated 0.3, equal weights. Find the composite's validity.

   *Solution.* (0.3 + 0.4)/sqrt(1 + 1 + 2 x 0.3) = 0.7/1.61 = 0.43.
5. **Spearman-Brown.** A structured interview's three raters each rate with reliability 0.5. Find the reliability of their mean (Spearman-Brown).

   *Solution.* 3 x 0.5/(1 + 2 x 0.5) = 0.75.
6. **Concurrent studies.** Why does a concurrent study need little or no range-restriction correction? Give one case where it needs some.

   *Solution.* The incumbents were not selected on the new test, so its range among them is nearly the
   applicants' range. It needs a correction if the incumbents were selected on something correlated with the test
   (indirect restriction), or if poor performers have left (attrition on the criterion).
7. ★ **A design.** Design a selection system for a role you know: job analysis, predictors, combination, adverse impact, validation and a decision log.

   *Solution.* Job analysis; two or three predictors with evidence for the role (a structured interview, a job
   knowledge test or work sample), scored by anchored rules and combined by fixed weights; an adverse-impact check
   on a pilot with a search for alternatives along the frontier; a predictive validation with a multi-rater
   criterion a year on, corrected only for the restriction that happened; and a decision log written before the
   data.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
the Hawthorne studies' dates, rooms and parts assembled; Levitt and List's findings and the Monday changes;
Münsterberg's 1913 tests; the Army Alpha and Beta numbers (about 1.75 million); Scullen, Mount and Goff's share of
rater variance; the inter-rater reliability of about 0.5 for supervisor ratings; Schmidt and Hunter's validities
(0.51, 0.54, 0.51, 0.38, 0.48); Sackett et al.'s (0.42, 0.40, 0.33, 0.31, 0.19); Oh, Le and Roth's reply; McDaniel
et al. (1994); Dana, Dawes and Peterson's random-answer interviews; Highhouse (2008); Taylor and Russell (1939);
Brogden (1949); *Griggs* and the four-fifths rule; findings on differential prediction; De Corte et al. (2007); the
2018 reports of a company's résumé screen; New York City's Local Law 144; Locke (1968) and Locke and Latham (2002);
Schweitzer et al. (2004); Lazear's 44% and its split; Gneezy and Rustichini's ten centres, six with the fine, and
the doubling; Gneezy, Meier and Rey-Biel (2011); Judge et al.'s 0.30 and 312 samples; Edmondson's teams and her
hospital-error finding; Bloom et al.'s 13%, attrition and promotion results; later hybrid-work trials; and every
page range in Sources.
