# Psychology, Built: Part 49, Modelling the Brain's Data

In 2020 seventy research teams were given the same brain-imaging dataset and the same nine yes-or-no hypotheses. No
two teams chose the same analysis pipeline, and for several hypotheses their answers split. Part 8 built the
measurement chain; this part builds the analysis chain on a synthetic brain where the truth is known, and then asks
the question that reorganized the field: how many people does a brain-behaviour correlation need?

The viewer counts the forks in an ordinary pipeline (6,912 paths from ten choices) and predicts four numbers. Then
the multiverse on Psyche's brain (72 pipelines, five regional hypotheses, 44 different maps); preprocessing, head
motion as a distance-dependent confound in connectivity, and the matched-filter rule for smoothing; the linear model
at two levels and why fixed effects mislead; thresholds at depth, permutation inference and cluster failure,
simulated; decoding, and the leak that reads noise at 94%; representational similarity against a noise ceiling;
encoding models judged by prediction; the default mode network and the anticorrelations global-signal regression
makes; EEG and MEG, and ERP windows chosen from the answer; the population vector and a neural manifold;
brain-computer interfaces and their bit rates; and the sample-size reckoning, attenuation by unreliable measures,
and the microprocessor studied with neuroscience's methods.

## Where the numbers come from

| What | Source |
|---|---|
| The multiverse: 30 simulated people, five disc regions with planted group effects 0, 0.25, 0.45, 0.7, 1.1 (in within-person noise SDs), person-specific smooth departures (SD 0.6), long-tailed spatial noise and a head-motion artefact at the rim; 72 pipelines (smoothing 0, 4, 8 voxels; six thresholds; with or without the most-moving fifth excluded; with or without an age covariate): share saying yes 0%, 0%, 22%, 60%, 76%; 44 distinct thresholded maps; by smoothing, the 1.1 effect found by 100%, 100% and 29% of pipelines | Psyche (`neurodata.multiverse`), item `multiverse` |
| Fixed against random effects: 20 people, no group effect, person effects SD 1, measurement SE 0.5: 13.9% of null voxels below p < 0.001 with fixed effects, 0.11% with random effects (200 simulated studies of 500 voxels) | Psyche (`neurodata.fixed_vs_random`), item `fixed` |
| Four rules on one group map (4-voxel smoothing): 40, 44, 46 and 27 voxels declared by p < 0.001, FDR 5%, clusters formed at p < 0.01, and permutation max-t, of 196 planted voxels | Psyche (`neurodata.run_pipeline`), item `thresholds` |
| Cluster failure: 200 null group studies (20 people) with long-tailed spatial autocorrelation; extents calibrated on Gaussian noise give a familywise rate of 12.5% at a p < 0.01 cluster-forming threshold and 6.5% at p < 0.001; sign-flipping permutation (200 per study) 4.5% and 6.0% | Psyche (`neurodata.cluster_fwe`), item `clusterfwe` |
| Motion and connectivity: 80 identical brains, half moving more; movers minus still is +0.048 for the nearest region pairs and -0.004 for the farthest (slope -0.06 per unit distance); after censoring moving scans, about +0.002 everywhere | Psyche (`neurodata.motion_connectivity`), item `motion` |
| Global-signal regression: two networks plus a shared global signal; within-network correlation 0.47, between 0.14; after regression 0.23 and -0.27 | Psyche (`neurodata.global_signal`), item `gsr` |
| Decoding: 2 categories x 40 trials, 1,000 voxels, nearest-centroid, 5-fold cross-validation, 100 datasets: on noise 48% (all voxels), 49% (50 voxels selected inside folds), 94% (selected on all data first); with a 0.3-SD signal in a tenth of voxels 68%, 64%, 96% | Psyche (`neurodata.decoding`), item `decoding` |
| Representational similarity: 24 stimuli in four categories, a size gradient within each; 12 simulated people; Spearman with the category model 0.64, with the size model 0.45; noise ceiling 0.88 to 0.90 | Psyche (`neurodata.rsa`), item `rsa` |
| Encoding: 300 voxels, 40 features, ridge (penalty 10 by cross-validation), 300 training and 60 test stimuli shown twice: responsive voxels' median prediction r 0.78, median ceiling 0.83, median 94% of ceiling | Psyche (`neurodata.encoding`), item `encoding` |
| ERP windows: 24 people, no difference, 2,000 studies: 5.6% significant with a window fixed in advance, 45.2% with the window at the difference's peak, 5.2% with the window at the average's peak | Psyche (`neurodata.erp_windows`), item `erp` |
| The population vector: cosine-tuned Poisson neurons, 0.2 s windows: mean error 44, 26, 22, 14, 8, 6 and 6 degrees with 4, 8, 16, 32, 64, 128 and 256 neurons | Psyche (`neurodata.population_vector_error`), item `popvec` |
| A neural manifold: 100 neurons during slow random reaching; the first two principal components hold over 90% of the variance | Psyche (`neurodata.manifold`), item `manifold` |
| Bit rates by Wolpaw's formula: 8 bits a minute (2 targets, 90%, 4 s), 19 (4 targets, 80%, 3 s), 167 (26 letters, 95%, 1.5 s) | Psyche (`neurodata.wolpaw_itr`), item `itr` |
| Brain-behaviour correlations, true r = 0.1, 4,000 studies per size: middle 95% -0.30 to 0.49 at n = 25 and 0.07 to 0.13 at n = 4,000; power 8%, 17%, 61%, 99.5%, 100% at 25, 100, 500, 2,000, 4,000; average reported \|r\| among significant results 0.47 at n = 25; a significant result replicates 6% of the time at n = 25; 783 people for 80% power; a true 0.2 with reliabilities 0.4 and 0.8 is observed at about 0.11 | Psyche (`neurodata.bwas`, `attenuated`; `imaging.n_for_correlation`), items `bwas`, `thresholds` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

The ten forks of chapter one and their option counts are illustrative of a standard fMRI pipeline; their product is
the number Carp reported, chosen so. The descriptions of brain-computer interfaces and of Huth's maps are summaries
without figures.

## Built in this part

* `explainer/psychology/psyche/neurodata.py`: group contrast maps with people as a sample, fixed and random effects,
  sign-flipping permutation for maximum t and cluster size, Gaussian-calibrated cluster extents, a 72-path multiverse,
  head motion's distance-dependent artefact and censoring, global-signal regression, cross-validated decoding with
  and without leakage, representational similarity with a noise ceiling, a ridge encoding model against repeat
  reliability, ERP windows chosen three ways, cosine-tuned populations with the population vector and principal
  components, Wolpaw's information rate, and brain-behaviour correlations by sample size with attenuation. Built on
  Part 8's synthetic brain (`imaging`). Tested in `tests/psychology/test_neurodata.py`.
* The Ledger gains five rows; Part 8's small-sample declaration and Part 23's two declarations about Part 49 are
  resolved as notes.
* The course's interactive: the reader chooses a pipeline (smoothing, threshold, exclusions) for Psyche's brain,
  predicts whether a region will light up, and sees the map and how many of the other pipelines agree.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Different defensible analysis pipelines applied to the same brain-imaging data can reach different conclusions about the same hypotheses. | Carp 2012 | replicated |
| A set of brain regions, including medial prefrontal and posterior cingulate cortex, is more active at rest than during many externally directed tasks, and its activity is correlated at rest. | Raichle and colleagues 2001 | replicated |
| Correlations between individual differences in brain structure or function and complex behaviour, found in samples of a few dozen people, are large and reproducible. | Kanai and Rees 2011 | failed |
| Cluster-extent inference with a lenient cluster-forming threshold (p < 0.01), using the standard parametric approximations, controls the familywise error at the stated 5%. | Friston and colleagues 1994 | failed |
| The category of a seen object can be decoded from distributed patterns of activity in ventral temporal cortex, even with the most selective regions left out. | Haxby and colleagues 2001 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Poldrack, Mumford and Nichols;
Power and colleagues; Murphy and colleagues; Naselaris and colleagues; Huth and colleagues; Georgopoulos and
colleagues; Willett and colleagues; Jonas and Kording; Elliott and colleagues; Luck.

## Build it

```bash
python -m videos.psychology.psych49.compute            # every number (about a minute)
python tools/qa_scene.py psych49 Thresholds            # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych49 -q l   # the whole part, silent preview
python tools/build.py psych49                          # 1080p30 with narration
python tools/qa_scene.py psych49 Decoding --lang zh    # the Chinese edition of one chapter
python tools/make.py psych49                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 49                    # the lab: fixed effects, leaks, windows, sample sizes
python tools/check_ledger.py psych49                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's neurodata module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Seventy teams, one dataset | The seventy teams; the multiverse on Psyche's brain; the question; objectives |
| 1 | On you: count the forks, and four numbers | Ten choices, 6,912 pipelines; four predictions |
| 2 | Preprocessing | Four steps; head motion makes connections; how wide a blur? |
| 3 | The linear model, at two levels | Two levels; one person and thirty; scans are not people |
| 4 | Thresholds at depth | Four rules on one map; permutation; cluster failure, simulated; the threshold is a fork |
| 5 | Patterns | From blobs to patterns; decoding noise at 94%; what decoding shows |
| 6 | Geometry | Distances, not voxels; three tables; the noise ceiling |
| 7 | Encoding models | Predicting the brain from the stimulus; the noise ceiling; maps of meaning |
| 8 | Connectivity | The brain at rest; anticorrelations made to order; what a correlation can mean |
| 9 | EEG and MEG | Three analyses beyond the average; choosing the window from the answer |
| 10 | Populations of neurons | The population vector; a neural manifold |
| 11 | Reading out | From a cursor to sentences; bits per minute; what is decoded and what is not |
| 12 | The sample-size reckoning | One correlation, five sample sizes; what gets reported; a noisy ruler; the microprocessor |
| 13 | The Ledger | Five rows; what they have in common |
| 14 | In practice: clinics, devices and claims | Where the analyses run; auditing a claim about the brain |
| 15 | Frontier: foundation models and precision mapping | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; Kant's three objections; payoffs; problems; references; Part 50 |

## Sources

* R. Botvinik-Nezer et al., Variability in the analysis of a single neuroimaging dataset by many teams, *Nature* 582
  (2020) 84-88; J. Carp (2012); R. Silberzahn et al. (2018).
* R. A. Poldrack, J. A. Mumford and T. E. Nichols, *Handbook of Functional MRI Data Analysis* (Cambridge, 2011);
  T. E. Nichols and A. P. Holmes, Nonparametric permutation tests for functional neuroimaging, *Human Brain Mapping*
  15 (2002) 1-25; K. J. Friston et al. (1994); C.-W. Woo, A. Krishnan and T. D. Wager (2014); A. Eklund,
  T. E. Nichols and H. Knutsson (2016).
* J. D. Power et al., Spurious but systematic correlations in functional connectivity MRI networks arise from subject
  motion, *NeuroImage* 59 (2012) 2142-2154; K. Murphy et al., The impact of global signal regression on resting state
  correlations, *NeuroImage* 44 (2009) 893-905; M. E. Raichle et al. (2001); M. D. Greicius et al. (2003);
  B. T. T. Yeo et al. (2011).
* J. V. Haxby et al. (2001, 2011); N. Kriegeskorte, M. Mur and P. Bandettini, Representational similarity analysis,
  *Frontiers in Systems Neuroscience* 2 (2008) 4; N. Kriegeskorte et al. (2008); T. Naselaris, K. N. Kay,
  S. Nishimoto and J. L. Gallant, Encoding and decoding in fMRI, *NeuroImage* 56 (2011) 400-410; A. G. Huth et al.,
  Natural speech reveals the semantic maps that tile human cerebral cortex, *Nature* 532 (2016) 453-458.
* S. J. Luck, *An Introduction to the Event-Related Potential Technique* (2nd edition, MIT Press, 2014).
* A. P. Georgopoulos, J. F. Kalaska, R. Caminiti and J. T. Massey, On the relations between the direction of
  two-dimensional arm movements and cell discharge in primate motor cortex, *Journal of Neuroscience* 2 (1982)
  1527-1537; J. R. Wolpaw et al., Brain-computer interfaces for communication and control, *Clinical
  Neurophysiology* 113 (2002) 767-791; F. R. Willett et al., A high-performance speech neuroprosthesis, *Nature* 620
  (2023) 1031-1036.
* R. Kanai and G. Rees (2011); W. Boekel et al. (2015); S. Marek et al. (2022); M. L. Elliott et al., What is the
  test-retest reliability of common task-functional MRI measures?, *Psychological Science* 31 (2020) 792-806;
  E. Jonas and K. P. Kording, Could a neuroscientist understand a microprocessor?, *PLOS Computational Biology* 13
  (2017) e1005268.

## Problems and solutions

1. **Paths.** 2⁵ × 3 = 96; if independent, 1 - 0.95⁹⁶ = 0.99. (Real paths are correlated, so the true chance is
   lower, but still far above 5%.)
2. **A group t.** t = 0.3/(1.0/√20) = 0.3 × 4.47 = 1.34, on 19 degrees of freedom: not significant.
3. **Bonferroni.** 0.05/50,000 = 10⁻⁶ per voxel (z about 4.9).
4. **Bits.** B = 1 + 0.8 log₂ 0.8 + 0.2 log₂ 0.2 = 1 - 0.258 - 0.464 = 0.278 bits per choice; 30 choices a minute
   give 8.3 bits per minute.
5. **Attenuation.** 0.25 × √(0.5 × 0.9) = 0.25 × 0.671 = 0.17.
6. **A leak.** The test trials helped pick the voxels that happen to differ between the labels, so the test is no
   longer independent of the training; do every selection, scaling and tuning step inside each training fold.
7. **A plan.** Choose the smallest correlation worth finding (say 0.15) and the measures' reliabilities; attenuate
   (with reliabilities 0.6 and 0.8, 0.15 becomes about 0.10), then size the sample for that (about 780 for 80% power,
   so use a shared dataset of thousands); register one pipeline, including motion censoring; fit in a discovery
   half and test once in a held-out half.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
the seventy teams, nine hypotheses and the size and task of the NARPS sample (Botvinik-Nezer et al. 2020); Carp's
count of 6,912 pipelines; Silberzahn et al.'s twenty-nine teams; Raichle et al. (2001) and Greicius et al. (2003);
Yeo et al.'s 1,000 people; Kanai and Rees (2011); Boekel et al.'s seventeen correlations and their outcome; Marek et
al.'s sample sizes and conclusions; Friston et al. (1994); Woo, Krishnan and Wager (2014); Eklund, Nichols and
Knutsson's familywise rates; Haxby et al.'s eight categories (2001) and hyperalignment (2011); Kriegeskorte et al.
(2008); Naselaris et al. (2011); Huth et al. (2016) and their number of participants; Power et al. (2012); Murphy et
al. (2009); Georgopoulos et al. (1982); Wolpaw's formula; Willett et al. (2023) and other speech neuroprostheses;
Elliott et al.'s mean reliability of about 0.4; Jonas and Kording (2017) and its three games; Nichols and Holmes
(2002); and every page range in Sources.
