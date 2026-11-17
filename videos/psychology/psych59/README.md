# Psychology, Built: Part 59, Computational Psychiatry

The plan of computational psychiatry is simple to state: give a patient a task from Acts IV and V, fit the model,
read off the parameter that has gone wrong, and choose a treatment by it. The first obstacle is the reliability
paradox: Psyche's 400 people do a Stroop-like task twice, the group effect has a t statistic near 50, and each
person's effect correlates about 0.3 with itself three weeks later. This part is the field's promise and the
measurement discipline of Part 3 and Part 4 it is having to relearn. The part opens with the care card (education,
not diagnosis or treatment, and where help is found).

The viewer designs a task on a slider (uniform effects against variable ones) and predicts four numbers. Then the
two routes (theory-driven and data-driven); compulsivity and model-based control; anxiety and volatility, with the
hierarchical Gaussian filter in outline; mood as an integral of prediction errors; buying reliability with trials,
attenuation and the fixes; biotypes from a circular pipeline on data with no types, and the split-half stability
check that exposes them; a prediction model scored three ways (in sample, cross-validated, in a new trial); the
personalized advantage index and the sample a choice rule needs; brain stimulation and psychedelics by Part 2's
standards; digital phenotyping and the small samples behind its first strong results; and five tests a parameter
must pass to be a clinical target, with four candidates scored.

## Where the numbers come from

| What | Source |
|---|---|
| The reliability paradox: 400 people, 60 trials per condition, a true effect of 60 ms with a between-person SD of 15 and a trial SD of 120; t = 48, retest r = 0.30 (expected 0.32) | Psyche (`precision.paradox`), item `paradox` |
| The designer's slider: reliability against the share of the effect that varies between people, for 20 to 800 trials per condition | Psyche (`precision.design_tradeoff`), item `tradeoff` |
| Reliability against trials (0.32 at 60 trials; about 1,150 trials for 0.9) | Psyche (`precision.difference_reliability`), in the scene |
| Attenuation: a true r of 0.5, symptom reliability 0.8, task reliability 0.2 to 1.0; observed 0.20 to 0.45 | Psyche (`precision.attenuated_r`), item `attenuate` |
| Biotypes: 220 patients, 20 features, no subgroups; six features chosen by their correlation with symptoms, k-means with four clusters; symptom differences at p < 0.05 in 9 of 10 studies; split-half agreement (adjusted Rand index) about 0.16, against about 0.74 with planted subgroups | Psyche (`precision.biotypes`), item `biotypes` |
| Prediction: 300 patients per trial, 40 features, three weakly predictive; ten selected, ridge logistic regression; AUC 0.72 in sample, 0.59 cross-validated with selection inside the folds, 0.57 in a new trial with shifted features and drifted coefficients (60 pairs of trials) | Psyche (`precision.cross_trial`), item `travel` |
| A choice rule's sample: about 350 patients for a main effect of 0.3 (two-sided 5%, 80% power), about 1,400 for an interaction of the same size | Psyche (`precision.pai_sample`), item `pai` |
| Phones: 400 simulated studies of a true correlation of 0.2, with 30 or 300 people | computed in the scene (seed 5904) |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/precision.py`: difference-score reliability, the paradox, the design trade-off,
  attenuation, k-means and the adjusted Rand index, the biotype pipeline with its stability check, a trial
  simulator, ridge logistic regression, AUC, cross-trial prediction and the choice rule's sample. Tested in
  `tests/psychology/test_precision.py`.
* The Ledger gains four rows.
* The course's interactive: design a task on a slider and watch group effect and reliability trade off, then buy
  reliability with trials.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Cognitive tasks with robust group effects (Stroop, flanker, stop-signal) measure individual differences poorly: their difference scores have low test-retest reliability. | Hedge, Powell and Sumner 2018 | replicated |
| Weaker model-based (goal-directed) control on the two-step task goes with a transdiagnostic dimension of compulsive behaviour and intrusive thought. | Gillan and colleagues 2016 | replicated |
| Resting-state connectivity divides depression into four biotypes that differ in symptoms and in response to brain stimulation. | Drysdale and colleagues 2017 | contested |
| A machine-learning model trained on one clinical trial predicts which patients will respond to treatment in other trials. | Chekroud and colleagues 2016 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Huys, Maia and Frank; Browning
and colleagues; Mathys and colleagues; Rutledge and colleagues; DeRubeis and colleagues; Cole and colleagues;
Goodwin and colleagues; Insel.

## Build it

```bash
python -m videos.psychology.psych59.compute            # every number (a minute)
python tools/qa_scene.py psych59 Biotypes              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych59 -q l   # the whole part, silent preview
python tools/build.py psych59                          # 1080p30 with narration
python tools/qa_scene.py psych59 Travel --lang zh      # the Chinese edition of one chapter
python tools/make.py psych59                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 59                    # the lab: reliability, biotypes, prediction that travels
python tools/check_ledger.py psych59                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's precision module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Robust effects, unreliable people | The care card; the paradox; the question; objectives |
| 1 | On you: design a task, and four numbers | The designer's slider; four predictions |
| 2 | The programme | Two routes; what has been delivered |
| 3 | Compulsivity and model-based control | Fourteen hundred people online; what limits it |
| 4 | Learning under uncertainty | Volatility and anxiety; the hierarchical Gaussian filter |
| 5 | Mood as computation | Happiness moment to moment; how to test it |
| 6 | Fixing measurement | Reliability bought with trials; attenuation; the fixes |
| 7 | Biotypes | Four biotypes; the pipeline on data with no types; split-half stability |
| 8 | Prediction that does not travel | Predicting response; three accuracies; why |
| 9 | Choosing a treatment | The personalized advantage index; its sample; what works meanwhile |
| 10 | New interventions | Stimulation; fast-acting drugs; Part 2's standards |
| 11 | Digital phenotyping | The phone as an instrument; small samples; limits |
| 12 | What would count as a computational target | Five tests; four candidates scored |
| 13 | The Ledger | Four rows; what they have in common |
| 14 | In practice: evaluating a biomarker claim | Where this is a job; a made-up claim; six questions |
| 15 | Frontier: a clinical-grade battery | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 60 |

## Sources

* Q. J. M. Huys, T. V. Maia and M. J. Frank, Computational psychiatry as a bridge from neuroscience to clinical
  applications, *Nature Neuroscience* 19 (2016) 404-413; P. Series (ed.), *Computational Psychiatry: A Primer* (MIT
  Press, 2020); A. D. Redish and J. A. Gordon (eds.), *Computational Psychiatry: New Perspectives on Mental Illness*
  (MIT Press, 2016).
* C. Hedge, G. Powell and P. Sumner (2018); A. Z. Enkavi et al. (2019); J. N. Rouder and J. M. Haaf (2019).
* C. M. Gillan et al. (2016); E. H. Patzelt et al. (2019); C. M. Gillan et al. (2020); N. D. Daw, S. J. Gershman,
  B. Seymour, P. Dayan and R. J. Dolan, Model-based influences on humans' choices and striatal prediction errors,
  *Neuron* 69 (2011) 1204-1215.
* T. E. J. Behrens, M. W. Woolrich, M. E. Walton and M. F. S. Rushworth, Learning the value of information in an
  uncertain world, *Nature Neuroscience* 10 (2007) 1214-1221; M. Browning, T. E. Behrens, G. Jocham, J. X. O'Reilly
  and S. J. Bishop, Anxious individuals have difficulty learning the causal statistics of aversive environments,
  *Nature Neuroscience* 18 (2015) 590-596; C. Mathys, J. Daunizeau, K. J. Friston and K. E. Stephan, A Bayesian
  foundation for individual learning under uncertainty, *Frontiers in Human Neuroscience* 5 (2011) 39.
* R. B. Rutledge, N. Skandali, P. Dayan and R. J. Dolan, A computational and neural model of momentary subjective
  well-being, *PNAS* 111 (2014) 12252-12257; E. Eldar, R. B. Rutledge, R. J. Dolan and Y. Niv, Mood as
  representation of momentum, *Trends in Cognitive Sciences* 20 (2016) 15-24.
* A. T. Drysdale et al. (2017); R. Dinga et al. (2019).
* A. M. Chekroud et al. (2016, 2024); G. S. Collins, J. B. Reitsma, D. G. Altman and K. G. M. Moons, Transparent
  reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD), *Annals of Internal
  Medicine* 162 (2015) 55-63.
* R. J. DeRubeis et al., The Personalized Advantage Index: translating research on prediction into individualized
  treatment recommendations, *PLoS ONE* 9 (2014) e83875.
* E. J. Cole et al., Stanford neuromodulation therapy (SNT): a double-blind randomized controlled trial, *American
  Journal of Psychiatry* 179 (2022) 132-141; H. S. Mayberg et al., Deep brain stimulation for treatment-resistant
  depression, *Neuron* 45 (2005) 651-660; P. E. Holtzheimer et al., Subcallosal cingulate deep brain stimulation for
  treatment-resistant depression: a multisite, randomised, sham-controlled trial, *Lancet Psychiatry* 4 (2017)
  839-849.
* R. M. Berman et al., Antidepressant effects of ketamine in depressed patients, *Biological Psychiatry* 47 (2000)
  351-354; G. M. Goodwin et al., Single-dose psilocybin for a treatment-resistant episode of major depression, *New
  England Journal of Medicine* 387 (2022) 1637-1648.
* T. R. Insel, Digital phenotyping: technology for a new science of behavior, *JAMA* 318 (2017) 1215-1216; S. Saeb
  et al., Mobile phone sensor correlates of depressive symptom severity in daily-life behavior, *Journal of Medical
  Internet Research* 17 (2015) e175.

## Problems and solutions

1. **Trials for 0.8.** A task's retest reliability is 0.3 with 60 trials per condition. How many trials for 0.8?

   *Solution.* Spearman-Brown: the factor is (0.8/0.2)/(0.3/0.7) = 9.3, so about 560 trials per condition.
2. **Attenuation.** A true correlation of 0.4; reliabilities 0.5 and 0.8. The expected observed correlation?

   *Solution.* 0.4 x sqrt(0.5 x 0.8) = 0.4 x 0.63 = 0.25.
3. **A leaky pipeline.** Features were chosen on all patients, then the model was cross-validated. Why is the estimate too high, and how do you fix the pipeline?

   *Solution.* The features were chosen because they correlated with the outcome in every patient,
   including the ones later held out, so each held-out fold has already been looked at. Put the selection (and any
   tuning) inside each training fold, and test the final model on an independent sample.
4. **A stability check.** Two halves of a sample give clusters that agree with an adjusted Rand index of 0.15. What do you conclude, and what null would you compare against?

   *Solution.* An adjusted Rand index of 0.15 means the two halves cut the sample in nearly unrelated
   ways: the clusters are not reproducible. Compare against the same pipeline run on data with the covariance kept
   and the clusters removed (for example, draws from a single Gaussian with the sample's covariance); if real data
   are no more stable than that null, there is no evidence of types.
5. **An interaction of 0.2.** A choice rule's benefit is an interaction of size 0.2. About how many patients to detect it?

   *Solution.* A main effect of 0.2 needs about 4 x (1.96 + 0.84)^2 / 0.2^2 = 785 patients; an
   interaction of the same size about four times that, roughly 3,100.
6. **A small study's correlation.** A phone feature correlates 0.6 with mood in 25 people. Give a 95% interval for the correlation.

   *Solution.* Fisher's z: atanh(0.6) = 0.69, standard error 1/sqrt(22) = 0.21, so 0.69 +/-
   0.42, and back-transformed 0.27 to 0.80. The interval is compatible with a modest correlation.
7. ★ **A target, tested.** Design a study to test whether model-based control is a treatment target: reliability, intervention, mediation.

   *Solution.* Measure model-based control with a reliability-tuned task and a hierarchical model, at
   several sessions (aim for retest reliability of 0.8); randomize patients with compulsive symptoms to a training
   or treatment expected to change it, against an active control; measure the parameter and symptoms weekly;
   pre-register the mediation analysis (does the parameter change before symptoms, and does it carry the effect?);
   and replicate in a second site.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Hedge, Powell and Sumner's samples and reliabilities; Enkavi et al.'s retest sample and results; Rouder and Haaf
(2019); Gillan et al.'s sample of about 1,400 and three factors; Patzelt et al. (2019); Gillan et al. (2020) and its
journal; Behrens et al. (2007); Browning et al. (2015) and the later inconsistent replications; Mathys et al.
(2011); Rutledge et al.'s 18,000 app users; Eldar et al. (2016); Drysdale et al.'s 1,200 scans and four clusters;
Dinga et al.'s 187 people and findings; Chekroud et al.'s 25 items, about 1,900 patients and external accuracies;
Chekroud et al. (2024)'s five antipsychotic trials; DeRubeis et al.'s trial and findings; TMS's 2008 clearance;
Cole et al.'s 29 people; Mayberg et al. (2005) and the stopped BROADEN trial; ketamine and the 2019 esketamine
approval; Goodwin et al.'s 233 patients, doses and results; Insel (2017); Saeb et al. (2015) and the later larger
studies; and every page range in Sources.
