# Psychology, Built: Part 62, The Dissertation

The series ends as a doctorate does. One question, left open where two earlier parts collide, is taken through a
registered report: the plan written as code and its SHA-256 recorded before the analysis ran, a design check on
simulated people, reviews, Stage 2 on open data, and the result reported whatever it showed. Part 24 found
mental-rotation slopes rising for 53 of 54 people in Ganis and Kievit's open data, a robust effect; Part 59's
reliability paradox says a robust effect is often a poor measure of individuals. Is a person's rotation slope a
reliable measure of that person? Then the accounts are closed: Psyche sits the Battery, the Ledger is read from top
to bottom, the Homunculus is drawn one last time, and Kant's three objections are answered one at a time.

The viewer takes a last experiment (a rotated letter, same or mirror) and predicts four numbers. Then how research is
done; ethics as practice; Stage 1 (theory, hypotheses, the plan as code); the design check and three reviews written
for the film; Stage 2, with one deviation reported; the exploratory analyses, labelled; writing the paper; Psyche's
scorecard; the Ledger complete; the Homunculus; the verdict on Kant and a fourth objection; where to go; the last
Ledger row; the roles; and eight open problems gathered from every part's frontier.

## The registered report

* **Plan.** `explainer/psychology/psyche/thesis.py`, `PLAN`; SHA-256
  `1ee2fa7b1189547d57863b673b825ff6d434d63461032bd0d718fd6919aee462`, recorded at 14:57 UTC on 16 November 2026,
  before the data were read for this analysis.
* **H1** (the paradox's risky prediction): the Spearman-Brown corrected odd/even split-half reliability of a
  person's rotation slope is below 0.70. **H2**: the person's mean time on the same trials is more reliable than
  the slope. Decision: H1 supported if the 95% bootstrap interval (4,000 resamples over people, seed 62) lies below
  0.70, refuted if it lies above, otherwise inconclusive; H2 supported if the paired difference's interval lies
  above 0.
* **Design check.** 54 simulated people, 200 studies per true reliability: at 0.40 the rule says supported 67% of
  the time; at 0.55, 30%; at 0.70 it is inconclusive 94% of the time; at 0.85 it says refuted 75%.
* **Deviation.** The registered minimum of 4 usable trials per angle in each half kept none of the 54 people (the
  data have as few as three 'same' trials per angle in a half, before errors). It was lowered to 2, a decision made on
  those counts alone, before any reliability was computed (`thesis.DEVIATION`).
* **Result.** 40 people kept (14 excluded); median slope 11.9 ms per degree; halves correlate 0.58; slope
  reliability 0.74 (95% interval 0.51 to 0.87): **H1 inconclusive**. Mean time 0.94 (0.88 to 0.97); the paired
  difference's interval 0.07 to 0.44: **H2 supported**.
* **Exploratory.** All 54 people with mirror trials included: 0.73 (0.57 to 0.83). Between-person SD of the slope
  about 4.3 ms per degree around a mean of 12.5 (a third of the mean), against a quarter in Part 59's simulated
  Stroop effect: robustness alone does not doom reliability; the ratio of real differences to trial noise does.

## Where the numbers come from

| What | Source |
|---|---|
| Ganis and Kievit's mental rotation study: 54 people, 96 trials each, at 0, 50, 100 and 150 degrees | Ganis and Kievit (2015), Journal of Open Psychology Data (CC BY 4.0), fetched by `explainer.psychology.opendata` and checked by SHA-256, as in Part 24; items `stage2` and `explore` |
| The design check | Psyche (`thesis.power`), item `power` |
| Psyche's scorecard: reaction time, threshold, Stroop, change detection and risky choice match their signatures with one set of default parameters; visual search (absent slope 3.5 times the present one) and free recall (with default parameters recency runs back over most of the list: first item 0.44, the eighth 0.44, the last 0.84) do not; six tasks were modelled only inside their own parts | Psyche (`thesis.scorecard`, through `battery.run`), item `scorecard` |
| The complete Ledger: 322 rows; held 203 (replicated 167, smaller 23, story and record 13), contested 64, failed 42, retracted 4, not directly tested 9; by act | the Ledger (`explainer/psychology/ledger.py`), item `board` |
| The two failures, drawn: search times at set sizes 4, 8, 16 and 32 (feature about 507 ms throughout; conjunction present 547 to 832 ms, absent 669 to 1,659 ms) and the serial-position curve of 16-item free recall (0.44, falling to 0.26 at positions 3 and 4, rising to 0.84) | Psyche (`battery.run`, default parameters), item `failures` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/thesis.py`: the registered plan and its hash, the reported deviation, split-half
  reliability of slopes with bootstrap intervals, the decision rule, a design check on simulated people, Psyche's
  Battery scorecard and the Ledger by act. Tested in `tests/psychology/test_thesis.py`.
* The Ledger gains its last row, the dissertation's own result.
* The course's interactive: the last experiment, mental rotation on you, with your slope and its split-half
  reliability.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A person's mental-rotation slope (response time per degree), though the effect is nearly universal, is an unreliable measure of that person (split-half reliability below 0.70), as the reliability paradox predicts. | Psychology, Built (Part 62, a registered report) 2026 | not directly tested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the Belmont Report; Hoffman and
colleagues; Ganis and Kievit (whose data the row analyses); Kant's objections.

## Build it

```bash
python -m videos.psychology.psych62.compute            # every number (a few minutes)
python tools/qa_scene.py psych62 StageTwo              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych62 -q l   # the whole part, silent preview
python tools/build.py psych62                          # 1080p30 with narration
python tools/qa_scene.py psych62 Kant --lang zh        # the Chinese edition of one chapter
python tools/make.py psych62                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 62                    # the lab: the registered report, rerun
python tools/check_ledger.py psych62                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's thesis module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Kant's three objections, again | The objections; the question; objectives |
| 1 | On you: the last experiment, and four numbers | Rotated letters; four predictions |
| 2 | How research is done | Finding a question; the craft |
| 3 | Ethics as practice | The Belmont principles applied; the profession's failures and codes |
| 4 | The registered report, Stage 1 | Theory and hypotheses; the plan as code |
| 5 | Peer review, shown | The design check; three reviews written for the film |
| 6 | Stage 2: the data | The deviation; each person's slope; the verdict |
| 7 | Writing it | Exploratory, and labelled; the paper |
| 8 | Psyche's scorecard | The Battery, task by task |
| 9 | The Ledger, complete | 322 rows by act; the pattern |
| 10 | The Homunculus, last drawing | What is mechanism, and what is still a person |
| 11 | The verdict on Kant | Three objections answered; the fourth |
| 12 | Where to go | Reading by direction |
| 13 | The Ledger: the last row | The dissertation's row; why the series ends on an open row |
| 14 | In practice: the roles | Roles, and the parts that prepare for them |
| 15 | Frontier: the open problems of sixty-two parts | Eight open problems |
| | The end | Your numbers; twelve lines; problems; references; the end |

## Sources

* I. Kant, *Metaphysische Anfangsgruende der Naturwissenschaft* (1786), Preface; translated by E. B. Bax (1883).
* G. Ganis and R. Kievit (2015); C. Hedge, G. Powell and P. Sumner (2018); J. N. Rouder and J. M. Haaf (2019).
* National Commission for the Protection of Human Subjects of Biomedical and Behavioral Research, *The Belmont
  Report: Ethical Principles and Guidelines for the Protection of Human Subjects of Research* (1979); D. H. Hoffman
  et al., *Report to the Special Committee of the Board of Directors of the American Psychological Association:
  Independent Review Relating to APA Ethics Guidelines, National Security Interrogations, and Torture* (2015).
* C. D. Chambers, *The Seven Deadly Sins of Psychology* (Princeton University Press, 2017); C. D. Chambers and L.
  Tzavella, The past, present and future of Registered Reports, *Nature Human Behaviour* 6 (2022) 29-42; A. M.
  Scheel, M. R. M. J. Schijen and D. Lakens (2021); C. K. Soderberg et al. (2021).
* E. R. Kandel et al., *Principles of Neural Science*; P. Dayan and L. F. Abbott, *Theoretical Neuroscience* (MIT
  Press, 2001); J. R. Busemeyer and A. Diederich, *Cognitive Modeling* (Sage, 2010); S. Farrell and S. Lewandowsky,
  *Computational Modeling of Cognition and Behavior* (Cambridge University Press, 2018); D. Borsboom, *Measuring the
  Mind* (Cambridge University Press, 2005); R. McElreath, *Statistical Rethinking* (CRC Press, 2020); J. Henrich,
  *The WEIRDest People in the World* (Farrar, Straus and Giroux, 2020); D. Kahneman, *Thinking, Fast and Slow*
  (Farrar, Straus and Giroux, 2011); D. H. Barlow (ed.), *Clinical Handbook of Psychological Disorders* (Guilford).

## Problems and solutions

1. **Spearman-Brown.** Halves correlate 0.58. The Spearman-Brown reliability of the full test?

   *Solution.* 2 x 0.58 / 1.58 = 0.73 (0.74 with the unrounded correlation).
2. **A narrower interval.** A reliability of 0.74 from 40 people. Roughly how many people to make the 95% interval half as wide?

   *Solution.* Interval width shrinks roughly as one over the square root of the sample: four times as
   many people, about 160.
3. **What a reviewer could have asked.** The registered minimum excluded everyone. List two things a Stage 1 reviewer could have asked to catch it.

   *Solution.* For the number of 'same' trials per angle in the published data (it is in
   the data descriptor), and for a pilot of the exclusion rule on simulated data with the real trial counts; or a
   pre-registered fallback rule if too many people were excluded.
4. **Not a replication rate.** Of 322 Ledger rows, 203 held. Why is that number not "the replication rate of psychology"?

   *Solution.* The rows are not a random sample of psychology's findings: they were chosen because
   they were taught, famous or disputed, and their statuses mix direct replications with meta-analyses and
   judgment. The share describes this series' Ledger, not the field.
5. **Serial self-terminating search.** Psyche's search slopes: 10 ms per item present, 35 absent. What would a serial self-terminating search predict?

   *Solution.* On target-present trials the searcher stops halfway through on average, so the
   absent slope should be about twice the present slope; 35 against 10 is steeper, and points to a model that
   rechecks items or terminates conservatively.
6. **The fourth objection.** Write Kant's fourth objection in one sentence, and the evidence that it is being answered.

   *Solution.* "The people who study the mind are rewarded for striking results, and that distorts
   what is published." It is being answered by registered reports (far more null results), open data and code, big
   team replications, and ledgers with dates.
7. ★ **A Stage 1 report.** Choose an open problem from any part's Frontier and write its Stage 1 registered report.

   *Solution.* A question from a frontier chapter; the theory as a model that makes a prediction the
   alternative forbids; data and exclusion rules (piloted on the real trial counts); the analysis as code; a design
   check on simulated people; a decision rule with an inconclusive region; the plan's hash.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Ganis and Kievit's journal and design (as in Part 24); the Belmont Report's date and principles; the 2015 Hoffman
review's findings and the APA's policy change; Chambers and Tzavella (2022); Scheel et al. (2021); Soderberg et al.
(2021); the editions of the books in Sources; and every page range in Sources. Chapter six's cost of a
reliability of 0.74 uses an illustrative true correlation (0.4) and criterion reliability (0.8); chapter nine's
tally by decade is computed from the Ledger's own rows.
