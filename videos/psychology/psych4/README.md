# Psychology, Built: Part 4, The Evidence

In 2011 a leading journal of social psychology published nine experiments, on more than a thousand people, that
appeared to show responses being influenced by events that had not yet happened. The experiments used the field's
ordinary designs and its ordinary statistics. Either the future reaches back into the present, or those methods
could produce a finding out of nothing. Within four years the field had shown which, by running a hundred of its
own published studies again, and had begun to change its rules.

This part asks when a finding should be believed. It builds the tools first: what an effect size looks like, what a
p-value is and the six things it is not, and what power is and how little of it published studies have had since
anyone first counted. Then it shows three ways in which honest work produces false results. The viewer makes a
study of nothing significant with four defensible choices. A thousand simulated laboratories publish only their
successes, and a literature about nothing reports a medium effect. A researcher looks at the data ten times and
stops when it works. Meehl's older warning follows (rejecting "no effect" is a weak test of a theory), then what
separated fabrication from flexibility, the Reproducibility Project and the argument over what its 36% means, and
the repairs: preregistration, registered reports, many laboratories on one protocol, and how to claim that nothing
is there. The part closes Act I, and from here every part ends with its rows in the Replication Ledger.

## Where the numbers come from

| What | Source |
|---|---|
| Bem's nine experiments, more than 1,000 participants, mean effect 0.22, eight significant; the two sets of replications | Bem (2011), Ritchie, Wiseman and French (2012), Galak et al. (2012), from the abstracts; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md) |
| Power of published studies, 0.48 for a medium effect in 1962 and 0.37 in 1984 | Cohen (1962); Sedlmeier and Gigerenzer (1989); see Open checks |
| The 60.7% that four flexible choices can reach | Simmons, Nelson and Simonsohn (2011), and the same simulation recomputed here with `statkit.multiple.phack` (62%) |
| 100 studies; 97% of originals and 36% of replications significant; effects half the size; 47% and 39% | Open Science Collaboration (2015), from the abstract; the comment and the response in *Science* 351 (2016) |
| Many Labs: 10 of 13 and 15 of 28 findings; median effect 0.60 against 0.15 | Klein et al. (2014, 2018), from the abstracts |
| 13 of 21 experiments from *Nature* and *Science* | Camerer et al. (2018) |
| 96% of 152 ordinary reports against 44% of 71 registered reports | Scheel, Schijen and Lakens (2021) |
| 55 publications with fraud; the committees' sentence about the field's culture | The Levelt, Noort and Drenth committees (2012); see Open checks |
| Prediction markets on 44 replications; median prior 9% | Dreber et al. (2015) |
| A 2023 report of high replicability under the reformed practices, retracted in 2024 | Protzko et al. and the journal's retraction note; see Open checks |
| Every curve, funnel, p-curve, rate and literature "in the lab" | `explainer.psychology.evidence`. Simulated or computed, with the truth set by us, and tagged so on screen |

The numbers that depend on choices made for the film. The forking-paths study has two outcomes that correlate about
0.55 (a reaction time and an error rate), an outlier rule at 2.5 standard deviations, one covariate and one chance
to add ten people a group; with other choices the 18% would be another number, and the published 61% comes from
stronger ones. The example dataset is number 16, the first in which the planned analysis fails and another
succeeds; it was picked by that rule and not by how striking it looks. The thousand laboratories have 10 to 100
people a group. The literature that resembles the Reproducibility Project (a quarter of hypotheses true, an effect
of 0.4, 30 people a group) is the nearest cell of a three-by-three grid, and the grid is shown so that nobody takes
the cell for an estimate. The two studies that "find nothing" are illustrative, with the same estimate and
different sizes; the bound of 0.1 and the comparison with Bem's 0.22 are choices. The dashboard's twenty metrics
are dataset 1, the first with exactly one of them below .05.

## Built in this part

* `explainer/psychology/evidence.py`, the false-positive lab: effect sizes and their pictures (overlap,
  probability of superiority), p-values and power for two groups, optional stopping (`peeking`), the four forks
  (`forks`, `any_significant`), the published simulation of flexibility (`flexibility`, on `statkit.multiple`),
  a literature with a publication filter (`literature`), p-curves, replications planned from the printed effect
  (`replicate`), the share of significant findings that are true (`ppv`), equivalence tests (`tost`) and a Bayes
  factor for no effect against a stated alternative (`bf01`).
* The Ledger gains six rows, and the Archive nine datasets.
* No new gear on the Homunculus map. Act I built the laboratory, the ruler and the rules of evidence; the machine
  starts in Part 5.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Responses are influenced by events that have not yet happened | Bem 2011 | failed |
| Published studies are underpowered | Cohen 1962 | replicated |
| Published effects shrink when repeated | Open Science Collaboration 2015 | replicated |
| A glimpse of a flag shifts political views | Carter, Ferguson and Hassin 2011 | failed |
| An image of money increases support for the existing system | Caruso, Vohs, Baxter and Waytz 2013 | failed |
| Imagined contact reduces prejudice | Husnu and Crisp 2010 | contested (present in the pooled data, much smaller than reported) |

The syllabus planned the Ledger's "first twenty rows from the Reproducibility Project and Many Labs" for this
part. Six are entered, because each row needs its sources read and a date, and six could be done to that standard.
The other findings from those projects get their rows in the parts that present them.

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Simmons, Nelson and Simonsohn's
simulation (a demonstration, recomputed here), the fraud inquiry (one case, not a finding about minds), and three
pieces of meta-science whose rows are due in Part 50 (registered reports against ordinary reports, the prediction
markets, and the retracted report on the reformed practices).

## Build it

```bash
python -m videos.psychology.psych4.compute            # every number (under a minute), into .cache/psych4/
python tools/qa_scene.py psych4 Drawer                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych4 -q l   # the whole part, silent preview
python tools/build.py psych4                          # 1080p30 with narration
python tools/qa_scene.py psych4 Drawer --lang zh      # the Chinese edition of one chapter
python tools/make.py psych4                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 4                    # the lab: a literature built, filtered and replicated
python tools/check_ledger.py psych4                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # the lab, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Feeling the future | Bem's experiment on recalling words practised afterwards; nine experiments; the dilemma; objectives |
| 1 | How big is big? | Cohen's d as overlap and as the chance one person beats another; 0.2, 0.5 and 0.8 drawn; the same effect as a correlation and as variation explained; a tiny effect made "significant" by sample size |
| 2 | What a p-value is | One study against 20,000 shuffles; the definition; six things a p-value is not |
| 3 | Power | Power against sample size; Cohen's survey; 2,000 small studies of a real effect and the winner's curse; how many significant findings are true |
| 4 | On you: the garden of forking paths | A study of nothing and four choices; all sixteen analyses; how often nothing becomes something; the published 61% |
| 5 | The file drawer | Twenty studies and one journal; two funnels of 1,000 laboratories; printed effect against study size; three p-curves |
| 6 | Honest people, wrong results | Optional stopping, with the p-value's path; HARKing; choices that depend on the data though only one analysis is run |
| 7 | Meehl's warning | Everything correlates a little with everything; a correlation of 0.05 against sample size; physics and psychology; weak predictions |
| 8 | Fraud is the smaller problem | Stapel; fabrication against flexibility; the committees on the field's culture |
| 9 | One hundred replications | The Reproducibility Project; the exchange of 2016; a literature that is mostly true and mostly fails to replicate |
| 10 | The repairs | Preregistration and registered reports; Many Labs; equivalence tests and Bayes factors for claiming an absence |
| 11 | What survives | Six findings to bet on; what the survivors have in common; what predicted success |
| 12 | The Ledger | One row in full (feeling the future); today's six rows |
| 13 | In practice: twenty metrics on a dashboard | A product test of nothing with one green metric; the four repairs in a product team |
| 14 | Frontier: have the reforms worked? | Three things known and one retraction; four open questions and a research problem |
| | Recap, problems, and the road ahead | Ten lines; Kant's scoreboard at the end of Act I; payoffs; problems; references; Part 5 |

## Sources

**Books.** C. Chambers, *The Seven Deadly Sins of Psychology* (2017). S. Ritchie, *Science Fictions* (2020).
J. Cohen, *Statistical Power Analysis for the Behavioral Sciences* (2nd ed., 1988).

**Papers.**
- D. J. Bem, "Feeling the future: experimental evidence for anomalous retroactive influences on cognition and
  affect", *Journal of Personality and Social Psychology* 100 (2011) 407–425. S. J. Ritchie, R. Wiseman and
  C. C. French, "Failing the future", *PLoS ONE* 7 (2012) e33423. J. Galak, R. A. LeBoeuf, L. D. Nelson and
  J. P. Simmons, "Correcting the past: failures to replicate psi", *JPSP* 103 (2012) 933–948.
- J. Cohen, "The statistical power of abnormal-social psychological research: a review", *Journal of Abnormal and
  Social Psychology* 65 (1962) 145–153. P. Sedlmeier and G. Gigerenzer, "Do studies of statistical power have an
  effect on the power of studies?", *Psychological Bulletin* 105 (1989) 309–316.
- J. P. Simmons, L. D. Nelson and U. Simonsohn, "False-positive psychology: undisclosed flexibility in data
  collection and analysis allows presenting anything as significant", *Psychological Science* 22 (2011) 1359–1366.
- R. Rosenthal, "The file drawer problem and tolerance for null results", *Psychological Bulletin* 86 (1979)
  638–641. N. L. Kerr, "HARKing: hypothesizing after the results are known", *Personality and Social Psychology
  Review* 2 (1998) 196–217. A. Gelman and E. Loken, "The garden of forking paths" (2013, unpublished manuscript).
- P. E. Meehl, "Theory-testing in psychology and physics: a methodological paradox", *Philosophy of Science* 34
  (1967) 103–115; "Theoretical risks and tabular asterisks", *Journal of Consulting and Clinical Psychology* 46
  (1978) 806–834.
- Levelt Committee, Noort Committee and Drenth Committee, *Flawed Science: The Fraudulent Research Practices of
  Social Psychologist Diederik Stapel* (2012).
- Open Science Collaboration, "Estimating the reproducibility of psychological science", *Science* 349 (2015)
  aac4716. D. T. Gilbert, G. King, S. Pettigrew and T. D. Wilson, comment, *Science* 351 (2016) 1037;
  C. J. Anderson et al., response, same issue.
- R. A. Klein et al., "Investigating variation in replicability: a 'Many Labs' replication project", *Social
  Psychology* 45 (2014) 142–152; "Many Labs 2", *Advances in Methods and Practices in Psychological Science* 1
  (2018) 443–490.
- C. F. Camerer et al., "Evaluating the replicability of social science experiments in *Nature* and *Science*
  between 2010 and 2015", *Nature Human Behaviour* 2 (2018) 637–644. A. Dreber et al., "Using prediction markets
  to estimate the reproducibility of scientific research", *PNAS* 112 (2015) 15343–15347.
- A. M. Scheel, M. R. M. J. Schijen and D. Lakens, "An excess of positive results: comparing the standard
  psychology literature with Registered Reports", *AMPPS* 4 (2021).
- J. Protzko et al., "High replicability of newly discovered social-behavioural findings is achievable", *Nature
  Human Behaviour* 8 (2024) 311–319, and its Retraction Note (24 September 2024).

## Problems and solutions

**1.** *Two groups differ by d = 0.3. What share of the two distributions overlaps, and how often does a randomly
chosen member of the higher group beat one of the lower? About how many people per group give an 80% chance of
detecting it?*

With two normal curves of equal spread, the overlap is 2Φ(−d/2) = 2Φ(−0.15) = 0.88, and the chance that a member
of the higher group beats one of the lower is Φ(d/√2) = Φ(0.212) = 0.58. For 80% power at α = .05, two-sided, the
number per group is about 2(1.96 + 0.84)²/d² = 15.7/0.09 = 175. So an effect that 58 pairs in 100 would show
needs 350 people to be found four times in five. (`evidence.overlap`, `evidence.superiority`, `evidence.n_for`.)

**2.** *For each sentence say whether it follows from p = .03, and why. (a) "There is a 3% chance the result is a
fluke." (b) "If nothing were going on, data this extreme would turn up 3% of the time." (c) "A repeat has a 97%
chance of succeeding."*

(a) No. That is a probability about the hypothesis given the data; p is a probability about the data given the
hypothesis of no effect, and turning one into the other needs the share of tested hypotheses that are true (see
problem 3). (b) Yes; it is the definition. (c) No. The chance that a repeat is significant is its power, which
depends on the true effect and the sample. If the true effect equalled the one observed, a repeat of the same size
would succeed only a little more than half the time, since the estimate would fall below the observed one about
half the time.

**3.** *Of 1,000 hypotheses, a share π are true; studies have power 1 − β and use α = .05. Show that the share of
significant findings that are true is π(1 − β) / [π(1 − β) + (1 − π)α]. Evaluate it for π = 0.1 with power 0.35,
and with power 0.8.*

Of the 1,000π true hypotheses, 1,000π(1 − β) reach significance. Of the 1,000(1 − π) false ones, 1,000(1 − π)α
do. The share of significant findings that are true is the first count over the sum, and the 1,000 cancels. For
π = 0.1 and power 0.35: 0.035/(0.035 + 0.045) = 0.44. For power 0.8: 0.08/(0.08 + 0.045) = 0.64. Raising power
helps, and with only one hypothesis in ten true, a third of the significant findings are still false. Lowering α
or testing better hypotheses helps more. (`evidence.ppv`.)

**4.** *An analyst has four independent yes-or-no choices, and each of the 16 analyses has a 5% false-positive
rate. Give an upper bound for the chance that at least one is significant. Why was the figure in chapter 4 far
below it?*

The chance that at least one of 16 events of probability 0.05 occurs is at most 16 × 0.05 = 0.80 (the union
bound), and if the 16 tests were independent it would be 1 − 0.95¹⁶ = 0.56. Chapter 4's figure was 18%, because
the 16 analyses are run on the same people and are strongly correlated: dropping two outliers or adding a
covariate changes the test statistic only a little, so the analyses mostly succeed or fail together. Flexibility
is costly in proportion to how different the alternatives are, which is why switching the outcome did more than
any other single choice (9% against 5 to 8%).

**5.** *A study with 20 people a group reports d = 0.70, p = .03, and only significant studies are printed. What
is the smallest effect such a study could have printed? What does that say about the true effect?*

The standard error of d with 20 a group is about √(2/20) = 0.32, so significance needs d of at least 1.96 × 0.32
= 0.62. A printed study of this size therefore reports at least 0.62 whatever the truth is: the report says more
about the sample size than about the effect. The true effect could be 0.7; it could as easily be 0.2 (such
studies print an average of 0.76 when the truth is 0.2, chapter 5) or zero. Read the 0.70 as an upper bound.

**6.** *With `explainer.psychology.evidence`: build a literature of 1,000 laboratories on a true effect of 0.2
with 30 people a group, publish the significant ones, and replicate each with 90% power for the effect it printed.
Report the replication rate. Then explain it to someone who concludes that most of the findings were false.*

```python
import numpy as np
from explainer.psychology import evidence as E
rng = np.random.default_rng(4)
lit = E.literature(1000, 0.2, 30, rng)     # power is 0.12, so about 120 are published
rep = E.replicate(lit, rng)                # each planned from its own printed effect
print(rep["originals"], rep["rate"], rep["ratio"])   # 123 0.25 0.37
```

A quarter replicate in this run of 123 printed studies (18% with the 4,000 laboratories of the lab, where the
figure is steadier), at about a third of the printed size, and every one of the findings is true. The printed
effects average about 0.6, three times the truth, because only overshoots were significant. A replication planned
to have 90% power for 0.6 has little power for 0.2. So a failed replication of this kind is evidence that the
printed effect was too large, which it was. It is weak evidence that the effect is zero.

**7.** ★ *Design a study that could show whether registered reports produce truer findings, and not merely fewer
positive ones. State what "truer" means and what would be compared.*

Open. A sketch of what an answer needs. "Truer" has to be defined by something outside the original study, and the
natural choice is the outcome of a later, larger replication: the share of positive findings that replicate, and
the ratio of replication to original effect. Comparing registered reports with ordinary papers on that measure is
confounded, because authors choose the format and may choose it for different hypotheses. The clean design assigns
the format at random, to studies or to laboratories, before the hypotheses are tested, and then replicates
everything, positive and null, since a format that only prints more nulls would also raise the share of positives
that replicate if it merely made positives rarer and more extreme. The retraction of 2024 is a warning that such a
study must itself be registered in a form that can be checked.

## Where it comes back

Every later part ends with its Ledger rows. The classic social experiments, re-examined: Part 34. Social priming
and what is left of it: Part 35. A replication run on screen, preregistered: Part 43. Bayes factors and the
comparison of models: Part 48. Meta-science, with p-curves, corrections for bias and the evidence on registered
reports: Part 50. Nudges at scale and the winner's curse again: Part 55. The false-positive lab (`evidence.py`) is
used wherever a later part asks how much to believe a result.

## Open checks

Before the narrated master:

* Simmons, Nelson and Simonsohn (2011) was read in summary only. The 60.7% is their Table 1's figure for four
  flexibilities combined as reported in secondary sources; the film recomputes the simulation and shows both
  numbers. Check the table, and the wording about their demonstration study.
* Cohen (1962) and Sedlmeier and Gigerenzer (1989) were not read. The mean power for a medium effect (0.48, then
  0.37) is from secondary summaries; the film says "a year of one journal" and "the same journal, 24 years later".
* The Levelt report was not read. The count of 55 publications and the quoted sentence are from university
  summaries of the final report.
* The original references of the three Many Labs 1 findings in the Ledger (Carter, Ferguson and Hassin 2011;
  Caruso et al. 2013; Husnu and Crisp 2010) are cited from memory of the Many Labs paper's list; check them there.
* The comment and response of 2016 are characterized from their abstracts. The comment's authors are not named on
  screen.
* Meehl (1967, 1978), Rosenthal (1979), Kerr (1998), Gelman and Loken (2013) and John, Loewenstein and Prelec
  (2012) are stated from standard accounts; no figure is quoted from any of them. The Texas sharpshooter is told
  as the old joke it is.
* Protzko et al. and the retraction note are stated from a summary of the note; the film says only that analyses
  were not preregistered as the paper said, and that the authors agreed to the retraction. Read the note.
* The description of Bem's recall experiment in chapter 0 should be checked against the article's Experiment 8/9
  before the master.
