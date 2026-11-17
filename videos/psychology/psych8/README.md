# Psychology, Built: Part 8, Reading the Brain

In 2009 a group of researchers put a dead Atlantic salmon in an MRI scanner, showed it photographs of people in
social situations, and asked it what each person was feeling. Analysed the way many published studies were at
the time, with a test in every voxel at one in a thousand and no correction for the number of tests, the salmon
had a small cluster of "active" voxels in its brain. With the standard corrections it had none. The fish was a
statistics lesson, and the lesson is larger than one threshold: a picture of a working brain is the last link of
a chain, from impulses to synaptic currents to blood flow to a magnetic signal to a statistical model to a
threshold to a map, and then comes a further step, from the map to a statement about a mind.

This part walks the chain. The route: a single neuron and its tuning curve; the EEG, why the scalp hears only
cells that are aligned and active together, and why the sources of a scalp pattern cannot be read off;
averaging, the square-root law, and the N400; magnetic resonance in three steps; the BOLD signal, its slow
response, the linear assumption and what the signal follows; the general linear model of an experiment, and
subtraction again; a hundred thousand tests, the corrections and their price, and the cluster failure of 2016;
circular analysis; the ceiling that reliability puts on a correlation, as an exercise for the viewer; reverse
inference by Bayes' rule; the difference between watching a region and intervening on it; and a plain list of
what scanning has and has not settled. The practice chapter sets the established clinical uses beside lie
detection and brain training; the frontier asks how many people a brain study needs.

## Where the numbers come from

| What | Source |
|---|---|
| The salmon: the task, the uncorrected threshold, the cluster, nothing after correction | Bennett et al. (2009), from the authors' commentary and summaries; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md), with what was read and what was not |
| Cortical cells that need a line at one orientation | Hubel and Wiesel (1959), from the abstract; the slide's edge is from their later recollections |
| First human EEG in 1924, published 1929; alpha at about ten a second; confirmed in 1934 | Berger (1929), from histories |
| "He spread the warm bread with socks"; a negative wave near 400 ms | Kutas and Hillyard (1980), from lecture notes and reviews; the film's curves are a model, tagged so |
| The BOLD signal (1990) and its first use in people (1992) | Ogawa et al. (1990), Kwong et al. (1992), from textbook histories |
| The fMRI response is close to linear in time | Boynton et al. (1996), from the abstract and a later review |
| BOLD follows local field potentials better than spikes | Logothetis et al. (2001), from the abstract |
| 499 people at rest, three million null analyses, up to 70% with a false cluster | Eklund, Nichols and Knutsson (2016), from the abstract and the debate that followed |
| More than half of surveyed studies selected voxels by the reported correlation; 57 of 134 papers | Vul et al. (2009); Kriegeskorte et al. (2009), from the abstracts and news reports |
| Reverse inference: a prior of 0.5 becomes 0.69 for Broca's area and language (a factor of 2.3) | Poldrack (2006), numbers from his own 2011 summary |
| The first transcranial magnetic stimulation | Barker, Jalinous and Freeston (1985), the PubMed record |
| 11,430 adults, six weeks of brain training, no transfer; the review of 132 articles; the 2016 settlement | Owen et al. (2010), Simons et al. (2016), the Federal Trade Commission's announcement as reported |
| fMRI lie detection: 100% without a countermeasure, 33% with; excluded by a court | Ganis et al. (2011), from the abstract; *United States v. Semrau* (2012), from case summaries |
| About 50,000 people; the typical study had 25; the typical association has r near 0.01 | Marek et al. (2022), from the abstract and a press summary |
| Test-retest reliability of task fMRI: mean ICC .397 over 90 experiments | Elliott et al. (2020), from the abstract |
| The gist of heard or imagined speech decoded from fMRI | Tang et al. (2023), from the abstract and summaries |
| Every curve, map, rate and sample size "computed by Psyche" or "simulated" | `explainer.psychology.psyche.imaging` |

The numbers that depend on choices made for the film. The model cell fires 40 impulses a second at its preferred
orientation and 2 at rest, with a tuning width of 20 degrees; its counts are Poisson, eight showings of half a
second at each of twelve orientations. The toy head has nine electrodes and twelve candidate sources in a
uniform conductor; the "quite different set" of sources is the single source plus a vector from the lead field's
null space. Single trials are a five-microvolt wave in smoothed noise of 20 microvolts; 200 trials a condition.
The relaxation curves use round values (grey matter 1,300 and 110 ms, white matter 800 and 80 ms). The
haemodynamic response is the usual difference of two gamma densities, peaking at 5 s. The synthetic brain is a
slice of 1,600 voxels with two active patches (78 voxels, weights 0.20 and 0.16 in units of the noise), noise
smoothed to 3 voxels, 120 scans at 2 s and a block design of 20 s on and off. Null brains are smooth noise with a
t distribution's tails; 1,000 of them give the rates. The null brain on screen is chosen by rule: the first, in
seed order, in which the uncorrected threshold declares a voxel. The cluster demonstration calibrates an extent
threshold (voxelwise p < 0.01) on noise with Gaussian smoothness and applies it to noise in which half the
variance comes from a field four times smoother: the mechanism of Eklund et al.'s result, in a toy, and its 16%
is not their 70%. The circular analysis uses 16 simulated people, 10,000 voxels and a threshold of r > 0.7
(p of about 0.001); averages are over 200 runs. The three scatter plots of chapter 9 are constructed to have
exactly the correlations shown. The lie detector's 90% is an assumed accuracy, and the base rate of one liar in
ten is an assumption. Sample sizes use Fisher's z approximation for 80% power at a two-sided 5% level.

## Built in this part

* `explainer/psychology/psyche/imaging.py`, the measurement chain as code: a tuning curve and Poisson counts;
  dipole sums, a toy lead field and a source no electrode can see; event-related potentials and the noise left by
  averaging; relaxation and the Fourier pair behind an MR image; the haemodynamic response, the convolution model
  and a least-squares fit with contrasts; a synthetic brain thresholded by four rules, null brains and their
  familywise rates, and a cluster threshold calibrated on the wrong kind of noise; circular selection of voxels;
  reverse inference, the ceiling on a correlation, and the samples small effects need. Tested in
  `tests/psychology/test_imaging.py` against closed forms, SciPy and the module's own known answers.
* The Ledger gains three rows and the Archive seventeen datasets.
* On the Homunculus map nothing lights yet: this part builds instruments, not faculties.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A word that does not fit the meaning of its sentence is followed, about 400 ms later, by a negative brain potential (the N400) | Kutas and Hillyard 1980 | replicated |
| Practising brain-training games improves abilities that were not practised | Jaeggi and colleagues 2008 | failed |
| A brain scan can tell whether a particular person is lying | Kozel and colleagues 2005 | not directly tested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the salmon (a demonstration of
a statistical error), Hubel and Wiesel's cells (history of a method; orientation selectivity is entered in Part
13), Berger and Barker (the history of two instruments), the BOLD signal, its linearity and what it follows
(properties of a measurement), the cluster failure, circular analysis and reverse inference (results about
methods), the fusiform face area (entered with its dispute in Part 14), and the frontier's three results:
brain-wide associations (due in Part 43), the reliability of task fMRI, and language decoding.

## Build it

```bash
python -m videos.psychology.psych8.compute            # every number (about ten seconds), into .cache/psych8/
python tools/qa_scene.py psych8 Tests                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych8 -q l   # the whole part, silent preview
python tools/build.py psych8                          # 1080p30 with narration
python tools/qa_scene.py psych8 Tests --lang zh       # the Chinese edition of one chapter
python tools/make.py psych8                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 8                    # the lab: averaging, the echo, a brain of noise, selection
python tools/check_ledger.py psych8                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # Psyche's imaging module, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A salmon in a scanner | The experiment; why it happened; the chain from a thought to a coloured map; objectives |
| 1 | Listening to one neuron | Hubel and Wiesel's line of light; a tuning curve from Poisson counts; what a single cell gives and costs |
| 2 | Voltages on the scalp | Berger's rhythm; aligned sources add as N and random ones as its square root; two sets of sources with one scalp pattern |
| 3 | Averaging out the noise | A wave hidden in single trials; averages of 10, 50 and 200; the square-root law; the N400 |
| 4 | MRI in five minutes | Protons lined up and tipped; relaxation and contrast; gradients, k-space and the Fourier transform |
| 5 | Blood, and a slow echo | The BOLD signal; a response that peaks at 5 s; responses add; what the signal follows |
| 6 | The linear model of an experiment | One voxel fitted; the same fit everywhere gives a map; a map is a subtraction, with Donders' assumption |
| 7 | A hundred thousand tests | A brain of noise; three corrections; what each finds and misses; the cluster rule against real noise |
| 8 | Choosing voxels by the answer | Correlations that were too good; the same analysis on noise; fresh data as test and cure |
| 9 | On you: which of these is impossible? | Three results and two reliabilities; the ceiling on a correlation |
| 10 | Reading a mind backwards | Forward and reverse inference; Bayes' rule with Poldrack's factor; decoding as the honest version |
| 11 | From watching to intervening | A scan is an observation; damage, a magnetic pulse, a current, light; what scanning has settled and what it has not |
| 12 | The Ledger | The N400, brain training, and lie detection by scan |
| 13 | In practice: what is sold, and what works | Epilepsy, sleep and surgery; a detector that is right nine times in ten; brain training tested; six questions |
| 14 | Frontier: how many people does a brain study need? | Small links and small studies; the samples needed; the gist of a story decoded; four open questions |
| | Recap, problems, and the road ahead | Ten lines; what today adds to the reply to Kant; payoffs; problems; references; Part 9 |

## Sources

**Books.** S. A. Huettel, A. W. Song and G. McCarthy, *Functional Magnetic Resonance Imaging* (3rd ed., 2014).
R. A. Poldrack, J. A. Mumford and T. E. Nichols, *Handbook of Functional MRI Data Analysis* (2011). S. J. Luck,
*An Introduction to the Event-Related Potential Technique* (2nd ed., 2014). R. A. Poldrack, *The New Mind
Readers* (2018).

**Papers.**
- C. M. Bennett, A. A. Baird, M. B. Miller and G. L. Wolford, "Neural correlates of interspecies perspective
  taking in the post-mortem Atlantic salmon: an argument for multiple comparisons correction", poster, Human
  Brain Mapping 2009; *Journal of Serendipitous and Unexpected Results* 1 (2010) 1–5.
- D. H. Hubel and T. N. Wiesel, "Receptive fields of single neurones in the cat's striate cortex", *Journal of
  Physiology* 148 (1959) 574–591.
- H. Berger, "Über das Elektrenkephalogramm des Menschen", *Archiv für Psychiatrie und Nervenkrankheiten* 87
  (1929) 527–570.
- M. Kutas and S. A. Hillyard, "Reading senseless sentences: brain potentials reflect semantic incongruity",
  *Science* 207 (1980) 203–205. M. Kutas and K. D. Federmeier, "Thirty years and counting: finding meaning in the
  N400 component of the event-related brain potential (ERP)", *Annual Review of Psychology* 62 (2011) 621–647.
- S. Ogawa, T. M. Lee, A. R. Kay and D. W. Tank, "Brain magnetic resonance imaging with contrast dependent on
  blood oxygenation", *PNAS* 87 (1990) 9868–9872. K. K. Kwong et al., "Dynamic magnetic resonance imaging of
  human brain activity during primary sensory stimulation", *PNAS* 89 (1992) 5675–5679.
- G. M. Boynton, S. A. Engel, G. H. Glover and D. J. Heeger, "Linear systems analysis of functional magnetic
  resonance imaging in human V1", *Journal of Neuroscience* 16 (1996) 4207–4221.
- N. K. Logothetis, J. Pauls, M. Augath, T. Trinath and A. Oeltermann, "Neurophysiological investigation of the
  basis of the fMRI signal", *Nature* 412 (2001) 150–157.
- A. Eklund, T. E. Nichols and H. Knutsson, "Cluster failure: why fMRI inferences for spatial extent have
  inflated false-positive rates", *PNAS* 113 (2016) 7900–7905.
- E. Vul, C. Harris, P. Winkielman and H. Pashler, "Puzzlingly high correlations in fMRI studies of emotion,
  personality, and social cognition", *Perspectives on Psychological Science* 4 (2009) 274–290. N. Kriegeskorte,
  W. K. Simmons, P. S. F. Bellgowan and C. I. Baker, "Circular analysis in systems neuroscience: the dangers of
  double dipping", *Nature Neuroscience* 12 (2009) 535–540.
- R. A. Poldrack, "Can cognitive processes be inferred from neuroimaging data?", *Trends in Cognitive Sciences* 10
  (2006) 59–63.
- A. T. Barker, R. Jalinous and I. L. Freeston, "Non-invasive magnetic stimulation of human motor cortex",
  *Lancet* 325 (1985) 1106–1107.
- A. M. Owen et al., "Putting brain training to the test", *Nature* 465 (2010) 775–778. D. J. Simons et al., "Do
  'brain-training' programs work?", *Psychological Science in the Public Interest* 17 (2016) 103–186. S. M.
  Jaeggi, M. Buschkuehl, J. Jonides and W. J. Perrig, "Improving fluid intelligence with training on working
  memory", *PNAS* 105 (2008) 6829–6833.
- G. Ganis, J. P. Rosenfeld, J. Meixner, R. A. Kievit and H. E. Schendan, "Lying in the scanner: covert
  countermeasures disrupt deception detection by functional magnetic resonance imaging", *NeuroImage* 55 (2011)
  312–319. F. A. Kozel et al., "Detecting deception using functional magnetic resonance imaging", *Biological
  Psychiatry* 58 (2005) 605–613. *United States v. Semrau*, 693 F.3d 510 (6th Cir. 2012).
- M. L. Elliott et al., "What is the test-retest reliability of common task-functional MRI measures? New
  empirical evidence and a meta-analysis", *Psychological Science* 31 (2020) 792–806.
- S. Marek et al., "Reproducible brain-wide association studies require thousands of individuals", *Nature* 603
  (2022) 654–660.
- J. Tang, A. LeBel, S. Jain and A. G. Huth, "Semantic reconstruction of continuous language from non-invasive
  brain recordings", *Nature Neuroscience* 26 (2023) 858–866.

## Problems and solutions

**1.** *A cell fires 40 impulses a second to its preferred orientation and 2 with no stimulus; its tuning is a
bell curve with standard deviation 20 degrees. What is its rate to a line 30 degrees off? If counts are Poisson,
how many half-second showings tell that rate from the peak rate with a z of 3?*

The rate is 2 + 38 exp(−(30/20)²/2) = 2 + 38 × 0.325 = 14.3 a second. In half a second the cell fires 20
impulses on average at the peak and 7.2 at 30 degrees off, and a Poisson count's variance equals its mean. Over n
showings the difference of the two mean counts is 12.8 with standard error √((20 + 7.2)/n), so z =
12.8 / √(27.2/n) ≥ 3 needs n ≥ 9 × 27.2 / 12.8² = 1.5. Two showings of each are enough. A well-tuned cell, heard
directly, is a very good instrument; the problem with it is how few you can hear.

**2.** *N unit dipoles point in random directions in a plane. Show that the mean square of their sum is N. A
patch of cortex has 10⁶ aligned cells, and a hundred times as many unaligned ones around it. Which contributes
more to the scalp?*

Write the sum as S = Σ vᵢ with |vᵢ| = 1. Then |S|² = Σ |vᵢ|² + Σ over i ≠ j of vᵢ·vⱼ. The first sum is N. Each
cross term averages to zero, because vⱼ is as likely to point one way as the opposite. So the mean of |S|² is N,
and the typical size of the sum is √N. The 10⁶ aligned cells sum to 10⁶. The 10⁸ unaligned ones sum to about
√(10⁸) = 10⁴. The aligned patch contributes a hundred times more, although it has a hundredth of the cells.

**3.** *A response of 5 microvolts sits in noise of 20. How many trials bring the noise in the average down to 1
microvolt? How many are needed to tell two conditions apart, if the test needs the difference to be 4 times its
standard error?*

The noise in an average of n trials is 20/√n, which is 1 when n = 400. For two conditions with n trials each, the
difference of the two averages has standard error 20 √(2/n). The true difference is 5, so 5 ≥ 4 × 20 √(2/n)
gives √(n/2) ≥ 16 and n ≥ 512 trials in each condition. Halving the noise by better recording would cut that to
128: the cost goes with the square of the noise.

**4.** *The response to one brief event is h(t). Write the predicted signal for events at times t₁, …, t_k, and
show that a block of events 2 s apart for 20 s gives a plateau. Why does the plateau start about 5 s late?*

Under the linear assumption the prediction is y(t) = Σ h(t − tᵢ), a convolution of a train of events with h. For
events every 2 s, once more than the duration of h has passed since the block began, the sum at any moment
contains one copy of h at every lag 0, 2, 4, … and is close to (1/2) ∫ h dt, a constant: the plateau. With the
film's h (peak 1, area 4.75) the constant is about 2.4 to 2.7, depending on where between events you look. The
plateau is late because each event's contribution is near zero for the first second or two and peaks at 5 s; the
sum reaches nine-tenths of its height about 7.5 s after the block begins. It also outlasts the block by the same
lag, which is why blocks are analysed with the convolved prediction and not with a square wave.

**5.** *A map has 100,000 voxels and nothing is there. How many pass at p < 0.001? What threshold does
Bonferroni give for a 5% chance of any? Why is that too strict when neighbouring voxels are alike?*

On average 100,000 × 0.001 = 100 voxels pass. Bonferroni sets each test at 0.05 / 100,000 = 5 × 10⁻⁷, a t of
about 5.2 with 118 degrees of freedom (4.9 for a normal deviate). The bound assumes the worst case, in which the
tests' false alarms never coincide. Neighbouring voxels are correlated, by the blood supply and by the smoothing
applied to the images, so the map holds far fewer independent pieces of evidence than voxels, and a threshold
tuned to 100,000 independent tests gives a familywise rate well under 5% and misses more than it needs to. Random
field theory and permutation tests set the threshold from the smoothness of the data instead.

**6.** *With `explainer.psychology.psyche.imaging`: run `voodoo` for 10, 16 and 40 subjects at the threshold that
gives p < 0.001 for each. How does the reported correlation depend on the sample? Then use `reverse_inference`
to find how selective a region must be to take a prior of 0.1 above 0.5.*

```python
import math
import numpy as np
from scipy import stats
from explainer.psychology.psyche import imaging as I

for n in (10, 16, 40):
    t = stats.t.ppf(0.999, n - 2)
    r_cut = t / math.sqrt(n - 2 + t * t)
    runs = [I.voodoo(subjects=n, voxels=10_000, threshold=r_cut, rng=np.random.default_rng(100 + k))
            for k in range(40)]
    print(n, round(r_cut, 2), round(np.nanmean([v["r_same"] for v in runs]), 2),
          round(np.nanmean([v["r_fresh"] for v in runs]), 2))

for factor in (5, 9, 10):
    print(factor, I.reverse_inference(0.1, factor * 0.05, 0.05)["posterior"])
```

The thresholds are r = 0.85, 0.71 and 0.47, and the circular analysis reports 0.88, 0.75 and 0.51, from noise,
with about ten voxels passing each time; in fresh data all three are zero. The reported number is set by the
sample size: the smaller the study, the more impressive the correlation. That is the opposite of what a reader
assumes, and it is why the largest published brain-behaviour correlations came from the smallest studies. For
the second part, the posterior odds are the prior odds times the factor: 1/9 times the factor must exceed 1, so
the region must be at least nine times as likely to be active when the process is engaged as when it is not.
Poldrack's estimate for one of the best cases was 2.3.

**7.** ★ *Design the study that could show a brain measure predicts something about one person that their
behaviour and their history do not, and say what would count as failure.*

There is no single right answer; a good one has five parts. (i) An outcome that matters and is measured later:
relapse within a year, a reading difficulty at age eight, response to one treatment against another. (ii) A
baseline model built without the scanner, from the things already known: age, history, questionnaires, a few
behavioural tests. This is the comparison that is usually missing, and the claim is about what the brain measure
adds to it. (iii) A sample large enough for the effect you can honestly expect (chapter 14: thousands, if the
added link is like the usual ones), with the brain measure's reliability measured in the same people, since it
caps the answer. (iv) The model, its features and its threshold fixed and registered before a held-out sample is
opened, ideally from another site and scanner, and the result reported as prediction on those unseen people:
how much does the brain measure improve on the baseline, with an interval? (v) A statement, in advance, of what
failure is: an improvement over the baseline that is zero within the interval, or too small to change any
decision. A brain measure can be real, replicable and still add nothing to what a ten-minute interview already
tells you; a study that cannot return that verdict has not tested the claim.

## Where it comes back

The EEG's rhythms in sleep: Part 10. Tuning curves and receptive fields, from the eye inward: Part 13. The
fusiform face area and what it is for: Part 14. Attention measured on the scalp: Part 18. The N400 and the
understanding of sentences: Part 23. Evidence accumulating in the brain before a choice: Part 25. What scans say
about awareness: Part 27. Why findings fail to repeat: Part 43. The statistics of brain data in full (mixed
models, permutation, decoding, representational similarity): Part 49. Brain training and the narrowness of
skills: Part 54. Psyche's `imaging` module is the forward model later parts use when they set a model's
prediction beside a recording.

## Open checks

Before the narrated master:

* Bennett et al.'s poster and paper were not read. The film says the report notes the salmon was "not alive at
  the time"; confirm the wording, and whether the uncorrected analysis used an extent threshold. The share of
  papers using uncorrected thresholds ("something like a quarter") is the survey figure the authors cite, as
  reported in their commentary. No voxel counts for the salmon are given. "A whole brain is about 100,000 voxels"
  is a round figure for 2 to 3 mm voxels.
* Hubel and Wiesel (1959) was not read. "Anaesthetized cats" and "spots worked in the eye" are standard; the
  slide's edge and "like a machine gun" are Hubel's later recollections and should be checked against his Nobel
  lecture. "A few thousand cells at once" refers to current high-density probes.
* Berger: the first recording in 1924 and publication in 1929 are from histories; "his own son" as a subject and
  the instrument he used should be checked. Adrian and Matthews confirmed the rhythm in 1934. That the
  non-uniqueness of the inverse problem was shown by Helmholtz "in the eighteen-fifties" (1853) is from textbooks.
  "A thousand times smaller than an impulse" compares tens of microvolts with about 100 millivolts.
* Kutas and Hillyard (1980) was not read. The sentence is as usually quoted; "a word printed in larger type
  produced a wave of that kind" (a late positivity) follows secondary accounts of their physical-deviance
  condition; that they had expected a P300 is from reviews. The film's curves are a model.
* MRI: 3 tesla as about 60,000 times the Earth's field, 128 MHz for protons at 3 tesla, and the relaxation times
  are textbook values, rounded. "A second or two" for a whole-brain functional image is typical, not universal.
* Ogawa et al. (1990) and the two 1992 papers were not read. "By something like one percent" is a typical
  figure at 1.5 to 3 tesla. The haemodynamic response's shape is the canonical model, not a measurement of one
  brain.
* Boynton et al. (1996) and Logothetis et al. (2001) are described from their abstracts.
* Eklund et al. (2016): "three million" analyses and "up to 70%" are from the abstract; the statement that the
  programs and their recommended settings were changed afterwards should be tied to the developers' notes. The
  film does not repeat the paper's withdrawn estimate of how many studies were affected.
* Vul et al. (2009): "more than half" of the surveyed studies is from the abstract; the traits named (jealousy,
  anxiety, empathy) and "a dozen or two people" describe the criticized studies as they are usually summarized.
  The working title "Voodoo correlations in social neuroscience" is from news reports.
* Poldrack (2006) was not read in full; the numbers are from his 2011 summary. "The regions that turn up in the
  most headlines are among the least selective" is a paraphrase of his argument, without a figure.
* Barker et al. (1985): "in Sheffield" and the twitch of the opposite hand are from the PubMed record and an
  encyclopedia entry.
* Owen et al. (2010): the comparison group's task is described only as "a comparison group that hadn't trained
  on such games"; check its description. The settlement's two million dollars and "without admitting fault" are
  from reports of the Federal Trade Commission's announcement of January 2016.
* The Ledger's row on lie detection cites Kozel et al. (2005) from memory: the mock theft and "most volunteers
  classified correctly" must be checked before the master. The row on brain training cites Jaeggi et al. (2008)
  from memory.
* Marek et al. (2022): about 50,000 people, a median study of 25, and a median association of 0.01 are from the
  abstract and a press summary; the reply by Spisak and colleagues (2023) is described from its abstract.
* Tang et al. (2023): three participants and about sixteen hours each are from a newspaper report; "a model
  trained on one person doesn't read another" and the failure when participants thought of something else
  follow the abstract's statement that decoding needs the subject's cooperation, and should be checked against
  the paper.
* The established clinical uses in chapter 13 are stated in general terms, without figures.
* The teaser for Part 9 (twins who met at thirty-nine) is checked with Part 9's own sources.
