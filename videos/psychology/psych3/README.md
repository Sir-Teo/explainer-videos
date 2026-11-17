# Psychology, Built: Part 3, The Measure

In 1932 the British Association for the Advancement of Science appointed nineteen physicists and psychologists to
decide whether a sensation can be measured. In 1940 the committee reported that it could not agree. The physicists'
objection was that measuring means adding, as rods are laid end to end, and nothing can be done with two loudnesses
that corresponds to that. Kant had said that mathematics cannot be applied to the mind; the committee said
something sharper, that a number attached to a mind is not yet a measurement.

This part asks three questions of any such number. What does it mean: which statements about it still say
something after a change of scale that is allowed (Stevens's four scales, and a computed answer to the old quarrel
over averaging ratings)? How much of it is error (true score and error, reliability, Spearman's correction for
attenuation, the Spearman-Brown formula, Cronbach's alpha, and the fact that error has more than one source)? And
does it measure what its name says (validity, the nomological network, the multitrait-multimethod matrix, jingle
and jangle, and what kind of thing a construct is)? It closes with two warnings: what people can and cannot report
about themselves, and why the experimental tasks that never fail make poor tests of a person. The viewer takes
part once, by rating a personality sketch that turns out to have been written for everyone.

## Where the numbers come from

| What | Source |
|---|---|
| The committee of 1932 to 1940, its nineteen members, the member's objection quoted, the four scales | Stevens (1946), read from the article; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md). The committee's own reports were not read, so the member is not named |
| Forer's sketch: 39 students, mean rating 4.26 of 5, 34 of them at 4 or 5 | Forer (1949), as reported by Dickson and Kelly (1985); see Open checks |
| Choice blindness: 120 people, 15 choices, 3 exchanged, at most 26% noticed, 84% sure they would have noticed | Johansson, Hall, Sikström and Olsson (2005), from the first author's summary in his thesis (2006); the jam and tea study is Hall et al. (2010) |
| Grit and conscientiousness, 0.84 | Credé, Tynan and Harms (2017) |
| Retest reliabilities of classic tasks | Hedge, Powell and Sumner (2018) |
| How measures are reported in journals | Flake and Fried (2020), and the surveys it reports |
| Every questionnaire score, every reliability and correlation "on the Pool" | `explainer.psychology.pool` and `explainer.psychology.measure`. Simulated: each person's true values are stored, so every estimate is shown beside the truth |
| The chances in chapter 2 | illustrative: computed from a model in which only person minus question matters, and from one in which the questions also differ in sharpness |
| The two correlation tables of chapter 9 | computed in `compute.py` (`latent`): a one-factor model and a network of six variables that push one another |

The numbers that depend on choices made for the film: each item is answered as 0.6 times the trait plus
independent error, cut into five categories; the conflict task gives everyone an effect of about 60 ms with a
standard deviation between people of 17 ms and trial noise of 100 ms, which puts the retest reliability of the
cost at 120 trials a condition near the published Stroop figure. The Pool is never evidence about people.

## Built in this part

* `explainer/psychology/measure.py`, the measurement library: Stevens's scale types with their permissible
  transformations, the test for whether a comparison of mean ratings can be reversed by respacing the scale,
  reliability, Spearman-Brown, Cronbach's alpha, split halves, the correction for attenuation, the standard error
  of measurement, the intraclass correlation, Cohen's kappa, the multitrait-multimethod matrix, a one-factor fit,
  a mutualism network, and the cancellation conditions of conjoint measurement.
* The Pool gains three traits with planted correlations, grit (0.84 with conscientiousness), a response style for
  each of three methods, answers to items on a rating scale (`Pool.items`, `Pool.scale`), and a conflict task
  (`Pool.conflict_task`). The people of Parts 1 and 2 are unchanged.
* No new gear on the Homunculus map. Parts 2 to 4 build the laboratory, the ruler and the rules of evidence.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A general personality sketch is accepted as a description of oneself | Forer 1949 | replicated |
| Reports of why one acted are often inferences, not observations | Nisbett and Wilson 1977 | replicated (for reports of causes; its reach is still argued) |
| People fail to notice a swapped choice, and explain it | Johansson, Hall, Sikström and Olsson 2005 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the grit meta-analysis (its row,
whether grit adds to conscientiousness, is due in Part 28), the reliability paradox (Part 59), Stevens's scales
(an argument, not a finding), and Flake and Fried's counts (a description of practice).

## Build it

```bash
python -m videos.psychology.psych3.compute            # every number (a few seconds), into .cache/psych3/
python tools/qa_scene.py psych3 TrueScore             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych3 -q l   # the whole part, silent preview
python tools/build.py psych3                          # 1080p30 with narration
python tools/qa_scene.py psych3 TrueScore --lang zh   # the Chinese edition of one chapter
python tools/make.py psych3                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 3                    # the lab: a questionnaire taken apart
python tools/check_ledger.py psych3                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # the measurement library, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The committee that could not agree | The British Association's committee, 1932 to 1940; no addition, no measurement; Kant's scoreboard; three questions; objectives |
| 1 | What a number survives | Stevens's definition and four scales; the test of a meaningful statement; averaging ratings, in a case where it is safe and a case where the order of two means reverses; sums of items |
| 2 | From an order to a scale | Conjoint measurement in one picture: three people, three questions, and the conditions under which an order implies an additive scale; a table that fails |
| 3 | On you: a reading of your character | Six statements to rate; Forer's class of 39; why a sketch fits everyone; a measure must tell people apart |
| 4 | True score and error | One person tested 300 times; X = T + E; variance split into true and error; reliability from a parallel form |
| 5 | Spearman's correction | Error shrinks correlations; the correction for attenuation; test length; what the correction costs in small studies |
| 6 | Longer tests are better tests | Spearman-Brown, derived and checked; Cronbach's alpha and three things about it; error from the day and from the judge; the library |
| 7 | Does it measure what its name says? | Reliable is not valid; content, criterion and construct; the nomological network; the multitrait-multimethod matrix with method variance planted |
| 8 | Jingle and jangle | One name for two things, two names for one; grit and conscientiousness |
| 9 | What is a construct? | A hidden cause, or symptoms that cause one another; the two imply the same correlations; what can tell them apart |
| 10 | Asking people | Nisbett and Wilson's thesis; choice blindness; what a self-report is worth |
| 11 | The reliability paradox | A conflict task that every small study replicates and that ranks people poorly; published retest figures; why |
| 12 | The Ledger | One row in full (telling more than we can know); today's three rows |
| 13 | In practice: every score is a measurement | A hiring test, a survey, a clinical questionnaire, a product metric; five questions for any score |
| 14 | Frontier: is it a quantity at all? | Stevens against Michell; how measures are reported; three open questions and a research problem |
| | Recap, problems, and the road ahead | Ten lines; Kant's scoreboard; payoffs; problems; references; Part 4 |

## Sources

**Books.** F. M. Lord and M. R. Novick, *Statistical Theories of Mental Test Scores* (1968). L. J. Cronbach,
G. C. Gleser, H. Nanda and N. Rajaratnam, *The Dependability of Behavioral Measurements* (1972). J. Michell,
*Measurement in Psychology* (1999). D. Borsboom, *Measuring the Mind* (2005).

**Papers.**
- S. S. Stevens, "On the theory of scales of measurement", *Science* 103 (1946) 677–680.
- C. Spearman, "The proof and measurement of association between two things", *American Journal of Psychology* 15
  (1904) 72–101; "Correlation calculated from faulty data", *British Journal of Psychology* 3 (1910) 271–295.
  W. Brown, "Some experimental results in the correlation of mental abilities", *British Journal of Psychology* 3
  (1910) 296–322.
- L. J. Cronbach, "Coefficient alpha and the internal structure of tests", *Psychometrika* 16 (1951) 297–334.
- J. Cohen, "A coefficient of agreement for nominal scales", *Educational and Psychological Measurement* 20 (1960)
  37–46.
- L. J. Cronbach and P. E. Meehl, "Construct validity in psychological tests", *Psychological Bulletin* 52 (1955)
  281–302.
- D. T. Campbell and D. W. Fiske, "Convergent and discriminant validation by the multitrait-multimethod matrix",
  *Psychological Bulletin* 56 (1959) 81–105.
- R. D. Luce and J. W. Tukey, "Simultaneous conjoint measurement", *Journal of Mathematical Psychology* 1 (1964)
  1–27.
- B. R. Forer, "The fallacy of personal validation: a classroom demonstration of gullibility", *Journal of Abnormal
  and Social Psychology* 44 (1949) 118–123. D. H. Dickson and I. W. Kelly, "The 'Barnum effect' in personality
  assessment: a review of the literature", *Psychological Reports* 57 (1985) 367–382.
- R. E. Nisbett and T. D. Wilson, "Telling more than we can know: verbal reports on mental processes",
  *Psychological Review* 84 (1977) 231–259.
- P. Johansson, L. Hall, S. Sikström and A. Olsson, "Failure to detect mismatches between intention and outcome in
  a simple decision task", *Science* 310 (2005) 116–119. L. Hall, P. Johansson, B. Tärning, S. Sikström and
  T. Deutgen, "Magic at the marketplace", *Cognition* 117 (2010) 54–61.
- M. Credé, M. C. Tynan and P. D. Harms, "Much ado about grit: a meta-analytic synthesis of the grit literature",
  *Journal of Personality and Social Psychology* 113 (2017) 492–511.
- C. Hedge, G. Powell and P. Sumner, "The reliability paradox: why robust cognitive tasks do not produce reliable
  individual differences", *Behavior Research Methods* 50 (2018) 1166–1186.
- J. Michell, "Quantitative science and the definition of measurement in psychology", *British Journal of
  Psychology* 88 (1997) 355–383.
- J. K. Flake and E. I. Fried, "Measurement schmeasurement: questionable measurement practices and how to avoid
  them", *Advances in Methods and Practices in Psychological Science* 3 (2020) 456–465.

## Problems and solutions

**1.** *Which of these sentences still say something after a permitted change of scale, and why? (a) "It is twice
as hot today, 20 °C against 10 °C." (b) "Her reaction time is twice his." (c) "The median rating was 4." (d) "The
mean rating rose from 3.0 to 3.5, half as much again as last year's rise."*

(a) No. Celsius is an interval scale: the zero is a convention, so x' = ax + b is allowed, and in Fahrenheit the
same two days are 68 and 50, a ratio of 1.36. (b) Yes. Time has a real zero; only the unit can change, and a ratio
of two times does not depend on the unit. (c) Yes, even if ratings are only ordinal: under any increasing recoding
the answer that half the people are at or below is the same answer. (d) Only if ratings form an interval scale.
The sentence compares two differences, and a ratio of differences survives x' = ax + b but not a respacing of the
five answers. Whether ratings are an interval scale is what chapter 1 leaves open.

**2.** *Two classes rate a course from 1 to 5. Class A's answers are in the shares 0, 0.2, 0.6, 0.2, 0; class B's
are 0.3, 0.1, 0.1, 0.1, 0.4. Compare the means. Then show from the cumulative shares that an increasing recoding of
the five answers can reverse the comparison, and find one.*

The means are 3.0 and 3.2, so B is ahead. Write the recoded values as v₁ < v₂ < ... < v₅ with gaps
gⱼ = vⱼ₊₁ − vⱼ > 0. A mean is v₅ minus the sum of gⱼ times the cumulative share at or below answer j, so

mean(A) − mean(B) = Σⱼ gⱼ (F_B(j) − F_A(j)).

The cumulative shares are 0, 0.2, 0.8, 1.0 for A and 0.3, 0.4, 0.5, 0.6 for B, so F_B − F_A = 0.3, 0.2, −0.3,
−0.4: both signs occur. Putting weight on the first gaps makes A the larger, weight on the last gaps makes B the
larger. For example, count answer 1 as −3 and leave the rest: A's mean is still 3.0 and B's is 3.2 − 4 × 0.3 = 2.0.
When F_B − F_A has one sign throughout, every choice of positive gaps gives the same order: that is the rule of the
chapter, and `measure.order_can_flip` checks it.

**3.** *Two forms of a test give X = T + E and X' = T + E', with errors of equal variance that are unrelated to T
and to each other. Show that corr(X, X') = Var(T)/Var(X).*

Cov(X, X') = Cov(T, T) + Cov(T, E') + Cov(E, T) + Cov(E, E') = Var(T), since the last three terms are zero.
Var(X) = Var(T) + Var(E) = Var(X'), because the error variances are equal. So corr(X, X') = Var(T)/Var(X), the
reliability. The assumption that does the work is that the two forms share the true score and nothing else.

**4.** *A 10-item test has reliability 0.70. How many items of the same kind are needed for 0.90? State the
assumption the formula makes, and one way in which lengthening a real test can break it.*

Solve r_k = kr/(1 + (k − 1)r) for k: k = r_k(1 − r)/(r(1 − r_k)) = 0.9 × 0.3/(0.7 × 0.1) = 3.86 times as long, so
39 items. The formula assumes the added items are parallel to the old ones: the same true score, the same error
variance, errors unrelated to one another. A real test breaks it when the new items measure something a little
different, when they repeat the wording of old ones (their errors are then related, and reliability is
overstated), or when a test so long tires the people taking it.

**5.** *Two measures with reliabilities 0.60 and 0.70 correlate 0.30. Estimate the correlation between the true
scores. Why can this estimate exceed 1 in a small sample although no correlation can?*

0.30/√(0.60 × 0.70) = 0.30/0.648 = 0.46. The bound r_xy ≤ √(r_xx r_yy) holds for the population values. In a sample
all three numbers are estimates with their own errors, and the observed correlation can land above the square root
of the estimated reliabilities. In the film, with 60 people and six-item scales measuring traits that correlate
0.84, that happens in about 4 studies in 100.

**6.** *With `explainer.psychology.measure` and the Pool: build a 20-item test from 10 items of `conscientious`
and 10 of `extravert`. Compute alpha and the correlation of the two halves. What does each number tell you, and
what does alpha not?*

```python
import numpy as np
from explainer.psychology import measure
from explainer.psychology.pool import Pool
P = Pool()
ids = P.sample(20_000, seed=1)
c, e = P.items("conscientious", ids, 10, seed=1), P.items("extravert", ids, 10, seed=2)
measure.cronbach_alpha(np.hstack([c, e]))                    # about 0.81
np.corrcoef(c.sum(axis=1), e.sum(axis=1))[0, 1]              # about 0.07
```

Alpha says that the items covary on average and that there are many of them. The two halves, which correlate
0.07, say that the test measures two nearly unrelated things. Alpha is not evidence that a test measures one
thing; the pattern of the correlations between items is (and factor analysis, Part 32, is the tool).

**7.** *★ You have each person's answers to each item, with error. Devise a test of whether an additive scale lies
behind them that fails when there is none and passes when there is one.*

Open. The cancellation conditions are statements about an exact order, and a table of observed proportions breaks
them by chance even when a scale exists. The directions that have been tried: treat the true chances as unknown
and ask how probable it is that they satisfy the conditions (order-restricted and Bayesian tests); fit a model
that implies additivity, such as Rasch's (Part 46), and judge its fit; or count violations against the number
expected from sampling error alone. Each needs a decision about how much violation is too much, and none is
agreed. A good answer says what the test's error rates are in both directions, and shows them by simulation, for
which `measure.double_cancellation` and the Pool are a start.

## Where it comes back

Flexible analysis, and what counts as evidence: Part 4. What an observer can report, as the threshold: Part 11.
Grit, and what it adds to conscientiousness: Part 28. The hidden-cause picture, as factor analysis: Part 32.
Symptoms as a network: Part 39. Which picture of a construct is right: Part 44. Scales that can be tested, as the
modern theory of test items: Part 46. Hierarchical models of tasks: Part 47. The reliability paradox, put to work:
Part 59. The measurement library (`measure.py`) and the Pool's traits are used by every later part that shows a
score.

## Open checks

Before the narrated master:

* Forer (1949) was not reachable. The design, the 39 students and the pattern of ratings are from Dickson and
  Kelly's review, which gives the mean as 4.3; the value 4.26 and the wording of the six statements are from
  secondary reproductions (one encyclopedia entry gives 4.30). Read the article and correct if needed.
* The committee's final report (*Advancement of Science* 1, 1940, 331–349) was not read. The quotation is as
  Stevens gives it; the member's name, and Campbell's own words, should be checked there.
* Nisbett and Wilson (1977) was not reachable; the film states its thesis and no figures from its studies.
* Johansson et al. (2005) is cited from the first author's own summary in his thesis; check the paper for the
  wording about the similarity of reports on swapped and unswapped trials.
* Michell (1997, 1999), Luce and Tukey (1964), Cronbach and Meehl (1955) and Campbell and Fiske (1959) are stated
  from standard accounts.
* The jingle fallacy is usually credited to Thorndike (1904); the film names only Kelley (1927), which Credé,
  Tynan and Harms confirm.
