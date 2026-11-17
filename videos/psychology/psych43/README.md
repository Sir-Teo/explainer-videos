# Psychology, Built: Part 43, The Replication

The degree ends as a degree does, with a project. Forty-two parts built a model subject, a laboratory, a measurement
library, a false-positive lab and a Ledger of findings; this part uses them to replicate two classic effects
properly, on screen, from the choice of target to the report. The plan is written as code and run on simulated data
before the real data are read, and the narration of the results is computed from them.

A row of the Ledger marked "not directly tested" (the fear bridge, Part 29) shows what makes a target feasible. Two
targets are chosen: verbal overshadowing (Part 21), expected to hold, and ego depletion (Part 28), in doubt; the
viewer takes part in a third, the Stroop task, on the course site. Then what counts as the same study and the two
registered protocols; the smallest effect of interest, power and the small-telescopes benchmark d33 (computed); the
preregistration as code and a dry run on simulated labs; the trial strip, counterbalancing, checks and timing;
consent and debriefing; the open lab-level data of the two registered multi-lab replications; the confirmatory
analyses exactly as planned; the three registered criteria and the replication Bayes factor; a labelled small
multiverse; the report in registered-report form; and the degree looked back on: the Ledger so far, the map, and the
three acts still to come.

### A note on the targets

The syllabus planned a Stroop variant as the effect expected to hold. The film needs real, fixed, open lab-level
data for both targets, and the Archive holds them for two registered multi-lab replications whose original authors
helped write the protocols: verbal overshadowing (Alogna et al. 2014, its second study, which followed the original's
order) and ego depletion (Hagger et al. 2016). The Stroop task is kept as the viewer's own study on the course site.
Both target effects were met earlier in the series (Parts 21 and 28); this part re-analyses them from the lab-level
data with its own frozen pipeline, and its results agree with the statuses those parts entered.

## Where the numbers come from

| What | Source |
|---|---|
| The original estimates: verbal overshadowing 25 fewer correct identifications per 100 (17 of 44 against 28 of 44; SE 10.3 per 100); ego depletion, the study the protocol followed, g = 0.68 (SE 0.30; 23 and 24 people) | the original rows of the two open datasets, via `explainer.psychology.opendata` |
| d33: 16 per 100 for verbal overshadowing (control rate 64%, 44 per group, normal approximation); 0.46 for ego depletion (23 and 24 people, noncentral t) | `capstone.d33_rd`, `capstone.d33`, item `plans` |
| The smallest effect of interest for ego depletion, d = 0.1: 2,600 per group for 95% power in one study; the original's power for d = 0.2: 10% | `capstone.n_per_group`, `capstone.power2`, item `plans` |
| The dry run: 23 simulated labs of 46 per group, 200 runs per true effect: significant in 4.5% with no effect, 69% at d = 0.1, 100% at the original's 0.68 | `capstone.dry_run`, item `dryrun` |
| Verbal overshadowing, 22 labs, 2,055 people: 16 fewer correct picks per 100 (95% interval 12 to 20), one-sided p below 10⁻¹⁴, τ² = 0 | `capstone.analyse` on the open data, item `confirm` |
| Ego depletion, 23 labs, 2,141 people: g = 0.04 (95% interval -0.07 to 0.14), one-sided p = 0.25, τ² = 0.023 | `capstone.analyse` on the open data, item `confirm` |
| The verdicts: verbal overshadowing meets 2 of 3 criteria (significant, reaches d33; the original's 25 lies outside the interval), replication Bayes factor about 10¹²; ego depletion meets 0 of 3, Bayes factor 0.025 (about 40 to 1 for no effect) | `capstone.verdict`, item `verdict` |
| The multiverse: 8 analyses each; ego depletion from 0.03 to 0.04 in all labs and 0.13 to 0.15 in the English-speaking labs; verbal overshadowing 16 per 100 in the second study and 4 per 100 in the first (no filler) | `capstone.multiverse`, item `multiverse` |
| Power curves: the original study (23 and 24) 10% at d = 0.2 and 52% at 0.6; the pooled labs (about 1,070 per group as one study) 64% at d = 0.1 and above 99% at 0.2; 2,600 per group 95% at 0.1 | `capstone.power2`, item `powercurve` |
| Lab sizes: verbal overshadowing 60 to 150 people (22 labs, 2,055), ego depletion 50 to 181 (23 labs, 2,141) | the open data, item `labs` |
| Heterogeneity: verbal overshadowing τ = 0, I² = 0; ego depletion τ = 0.15, I² = 35%, 95% prediction interval for a new lab -0.28 to 0.36 | item `confirm` |
| The garden: 300 simulated replications with no effect (23 labs of 23 per group): the planned analysis significant in 4%; the best of 14 analyses (two estimators; all labs or either half of three splits) in 12% | `capstone.simulate_labs`, `capstone.multiverse`, item `garden` |
| A product test: 5% conversion, a lift of 0.5 points, two-sided 5%, 80% power: 31,231 per arm; 122,121 for half the lift, 8,155 for double | item `abtest` |
| The Ledger so far: counts by status of every row in Parts 1 to 43 | `ledger.counts` |

## Built in this part

* `explainer/psychology/capstone.py`: the preregistration as a frozen `Plan`, two-group power by the noncentral t,
  d33 for a standardized and for a binary outcome, sample size for a power target, the replication Bayes factor,
  per-lab effects, fixed and random-effects pooling, simulated labs, the dry run, the confirmatory analysis, the
  verdict and the multiverse. Tested in `tests/psychology/test_capstone.py`.
* The Ledger gains two rows about replication itself.
* The course's interactive is the Stroop task: congruent and incongruent colour words, timed, with the viewer's own
  effect shown against the planned smallest effect of interest (no score is kept or sent).

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Studies accepted for publication before their results are known report positive results far less often than standard articles do | Allen and Mehler 2019 | replicated |
| Replications often fail because of hidden moderators: effects depend strongly on the setting and the sample | Van Bavel and colleagues 2016 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Brandt and colleagues, Zwaan and
colleagues; Nosek and Errington; Simonsohn; Verhagen and Wagenmakers. The two targets' rows are Part 21's and Part
28's; Alogna and colleagues and Hagger and colleagues are in their records.

## Build it

```bash
python -m videos.psychology.psych43.compute            # the plans, the dry run, then the real data (a minute)
python tools/qa_scene.py psych43 Confirm               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych43 -q l   # the whole part, silent preview
python tools/build.py psych43                          # 1080p30 with narration
python tools/qa_scene.py psych43 Verdict --lang zh     # the Chinese edition of one chapter
python tools/make.py psych43                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 43                    # the lab: the whole pipeline
python tools/check_ledger.py psych43                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # the capstone pipeline, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line, with the result sentences as templates over the
computed values) and the series table `videos/psychology/psychology_text_zh.json` (the text on screen); the terms
are in [`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The project | The degree ends with a project; a row never tested; two targets; the question; objectives |
| 1 | On you: colour words, and four predictions | The Stroop effect; four predictions |
| 2 | What counts as the same study | Direct and conceptual replication; the two protocols |
| 3 | How big, and how many? | The smallest effect of interest and power; small telescopes; power as a curve |
| 4 | The plan, written as code | Preregistration; a dry run before any real data; every fork closed in advance |
| 5 | Building the experiment | The trial strip; checks built in |
| 6 | Consent, and what participants are told | Before anyone takes part; the site's consent screen |
| 7 | The data | Two registered multi-lab replications; forty-five laboratories, lab by lab |
| 8 | The confirmatory analysis | Verbal overshadowing; ego depletion; how much the labs differ |
| 9 | Was it a replication? | Three questions and a fourth; the verdict; what each result would have meant |
| 10 | Exploratory, and labelled | A small multiverse; the garden, simulated |
| 11 | The report | A registered report; before it is sent |
| 12 | The degree | The Ledger so far; the map |
| 13 | The Ledger | Two rows, and the two targets |
| 14 | In practice: decide before the data | The same workflow, everywhere; a product test, planned |
| 15 | Frontier: what a failure licenses | What a failure licenses; open questions |
| | Recap, problems, and the road ahead | Your predictions; eleven lines; Kant's three objections; payoffs; problems; references; Part 44 |

## Sources

* V. K. Alogna et al., Registered replication report: Schooler and Engstler-Schooler (1990), *Perspectives on
  Psychological Science* 9 (2014) 556-578, data at osf.io/ybeur; J. W. Schooler and T. Y. Engstler-Schooler, Verbal
  overshadowing of visual memories, *Cognitive Psychology* 22 (1990) 36-71.
* M. S. Hagger, N. L. D. Chatzisarantis et al., A multilab preregistered replication of the ego-depletion effect,
  *Perspectives on Psychological Science* 11 (2016) 546-573, data at osf.io/jymhe; C. Sripada, D. Kessler and J.
  Jonides, Methylphenidate blocks effort-induced depletion of regulatory control in healthy volunteers,
  *Psychological Science* 25 (2014) 1227-1234.
* M. J. Brandt et al., The replication recipe: what makes for a convincing replication? *Journal of Experimental
  Social Psychology* 50 (2014) 217-224; R. A. Zwaan, A. Etz, R. E. Lucas and M. B. Donnellan, Making replication
  mainstream, *Behavioral and Brain Sciences* 41 (2018) e120.
* U. Simonsohn, Small telescopes: detectability and the evaluation of replication results, *Psychological Science*
  26 (2015) 559-569; D. Lakens, Sample size justification, *Collabra: Psychology* 8 (2022) 33267.
* J. Verhagen and E.-J. Wagenmakers, Bayesian tests to quantify the result of a replication attempt, *Journal of
  Experimental Psychology: General* 143 (2014) 1457-1475.
* B. A. Nosek and T. M. Errington, What is replication? *PLoS Biology* 18 (2020) e3000691; C. D. Chambers and L.
  Tzavella (2022); C. Allen and D. M. A. Mehler (2019); A. M. Scheel, M. R. M. J. Schijen and D. Lakens (2021).
* J. J. Van Bavel et al. (2016); R. A. Klein et al. (2018); A. Olsson-Collentine, J. M. Wicherts and M. A. L. M. van
  Assen (2020).
* J. R. Stroop, Studies of interference in serial verbal reactions, *Journal of Experimental Psychology* 18 (1935)
  643-662.

## Problems and solutions

1. **d33 for 20 per group.** Power 1/3 needs d/SE = z(0.975) - z(2/3) = 1.96 - 0.43 = 1.53, with SE = √(2/20) =
   0.316: d33 ≈ 0.48 (the noncentral t gives 0.50).
2. **The original's power.** SE = √(1/23 + 1/24) = 0.292, so d/SE = 0.685 and power ≈ P(Z > 1.96 - 0.685) =
   P(Z > 1.275) ≈ 0.10.
3. **One study at d = 0.1.** n = 2 (1.96 + 1.645)² / 0.1² = 2 × 12.99 / 0.01 ≈ 2,600 per group.
4. **The replication Bayes factor.** Under the original: N(0.04; 0.68, 0.30² + 0.055²), sd 0.305, z = -2.10,
   density 0.0442/0.305 = 0.145. Under no effect: N(0.04; 0, 0.055²), z = 0.73, density 0.306/0.055 = 5.57. BF =
   0.145/5.57 ≈ 0.026: about 38 to 1 for no effect.
5. **Pooling two labs.** A: RD = 0.500 - 0.667 = -0.167, v = 0.25/60 + 0.222/60 = 0.00787 (w = 127); B: RD = 0.50 -
   0.62 = -0.12, v = 0.25/100 + 0.2356/100 = 0.00486 (w = 206). Pooled: (-0.167 × 127 - 0.12 × 206)/333 = -0.138,
   SE 1/√333 = 0.055: about 14 fewer correct per 100.
6. **A multiverse.** 3 × 4 × 5 = 60 analyses; with independent 5% false-positive rates, 1 - 0.95⁶⁰ = 0.95. The
   analyses share data, so the true rate is lower, but well above 5%: one more reason to register one of them.
7. **A Stroop preregistration.** Hypothesis: incongruent trials are slower than congruent ones (one-sided). Smallest
   effect of interest: 20 ms, the smallest interference reported in standard versions. With trial-level SD around
   100 ms and 48 trials per condition, one person's SE is about 20 ms; a group of 30 gives a within-person dz far
   above what is needed for 95% power. Exclusions, fixed in advance: trials faster than 200 ms or slower than 2,000
   ms, errors, and people below 80% accuracy or failing two attention checks. Analysis: each person's mean
   incongruent minus congruent time, a one-sided t test against zero, and the effect size with its interval; the
   script is run on simulated participants before any real data.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts below come from the standard
literature and the open data's own documentation, and were not re-checked online today: the order of the original
verbal-overshadowing procedure and of the two replication studies; the letter-crossing and conflict-task procedure
and the reasons the protocol followed Sripada et al.; the review and approval of both protocols by the original
authors; Brandt et al.'s recipe; Zwaan et al.'s arguments; Simonsohn's definition of d33 and his one-sided test (this
part uses the 95% interval's upper end); Lakens's sample-size justification; Verhagen and Wagenmakers's replication
Bayes factor (this part uses its normal approximation, not their t-based version); Allen and Mehler's and Scheel et
al.'s figures (44% against 96%); Van Bavel et al.'s analysis; Many Labs 2's findings on heterogeneity;
Olsson-Collentine et al.'s; Nosek and Errington's definition; Chambers and Tzavella's review; the history of the fear
bridge row; and every page range in Sources.
