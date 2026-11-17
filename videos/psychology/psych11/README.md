# Psychology, Built: Part 11, The Threshold

On the morning of 22 October 1850 Gustav Theodor Fechner, a Leipzig professor of forty-nine whose career as a
physicist had been ended by years of illness, lay in bed thinking about how the body and the mind are related. By
his own account he saw that morning how the relation could be measured: if a stimulus grows by equal ratios, the
sensation grows by equal steps. He spent ten years on experiments, with lifted weights, lights and distances on the
skin, and published them in 1860 in the two volumes of the *Elements of Psychophysics*. It is the first serious
reply to Kant's first objection, that the mind admits no mathematics, and the subject's practitioners still keep
22 October as Fechner Day.

This part opens Act III, *The Senses*, and asks whether Fechner's reply works. The route: Weber's fraction, the
observation it rests on, run on Psyche to show where it holds and where it fails; Fechner's step from a fraction to
a logarithm, and the one assumption it needs; the three classical methods, and the reason a yes-or-no threshold
mixes what an observer can see with what they are willing to say; the threshold as a curve with four numbers;
a threshold of the viewer's own; fitting the curve by maximum likelihood with a bootstrap interval, and what one
slip does to a fit with no room for slips; staircases and QUEST, which spend trials where they teach most; Stevens,
who asked people for numbers and got power laws; the quarrel between Fechner and Stevens, and why thresholds cannot
settle it; two machines that give the same Weber's law for different reasons, and the slope that says which noise
is in charge; and Weber's law for number, for time and, a century before Fechner, for money. The practice chapter is
the hearing test, the eye chart, the codec and the tasting panel; the frontier asks whether a sensation
is the kind of thing that has a size at all.

## Where the numbers come from

| What | Source |
|---|---|
| Fechner's morning (22 October 1850), his age, the ten years of experiments, the two volumes of 1860 | Fechner (1860), as told by Boring (1961) and later histories; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md) |
| Weber's observation that the just noticeable difference grows in proportion to the standard (touch and lifted weights) | Weber (1834; German, 1846), from histories and textbooks; no single historical fraction is given |
| Fechner's three methods: just noticeable differences (limits), right and wrong cases (constant stimuli), average error (adjustment) | Fechner (1860), from encyclopedia and glossary entries |
| Stevens's exponents: brightness 0.33, loudness 0.67, vibration 0.95, visual length 1.0, heaviness 1.45, electric shock 3.5 | Stevens (1957, 1975), from the table as reproduced in textbooks |
| Range, first-stimulus and sequence effects in magnitude estimation | Poulton (1968), from the abstract and summaries; Teghtsoonian (1971) for the opposing view |
| A k-down 1-up staircase settles where p^k = 1/2: 70.7% (2-down), 79.4% (3-down), 84.1% (4-down) | Levitt (1971), derived on screen |
| QUEST: a Bayesian rule that places each trial at the current best estimate | Watson and Pelli (1983) |
| The lapse rate and the parametric bootstrap for psychometric functions | Wichmann and Hill (2001) |
| The near miss to Weber's law for pure tones: the fraction falls slowly with level (slope about 0.9 instead of 1) | McGill and Goldberg (1968), from summaries |
| The adult Weber fraction for number, about 0.11; children need 3:4 at three and 5:6 at six | Halberda, Mazzocco and Feigenson (2008); Halberda and Feigenson (2008), from the abstracts |
| Scalar timing: the spread of timed responses grows in proportion to the interval | Gibbon (1977), from summaries |
| The quick CSF: a contrast sensitivity curve's four parameters in under 50 trials | Lesmes et al. (2010), from the abstract |
| Plateau's painters (1872): a grey midway between black and white; Plateau argued for a power law; Delboeuf found the midpoints moved with the lighting | Plateau (1872), from later papers' accounts; the number of painters and their greys are not given |
| CIE lightness: a cube root with an offset; lightness 50 is 18.4% of white's luminance | the CIE 1976 formula, L* = 116 (Y/Yn)^(1/3) − 16 |
| Thurstone's law of comparative judgment; nineteen offences scaled by paired comparison | Thurstone (1927, two papers), from citations and a replication's account |
| The square-root law: in dim light the threshold grows as the square root of the background (photon noise); a floor below it, Weber's law above | de Vries (1943); Rose (1948), from encyclopedia entries and later papers |
| The value of a small gain is inversely proportional to the wealth already held, so value is a logarithm | Bernoulli (1738), from the 1954 translation as quoted |
| The triangle test: three samples, two the same; guessing is right a third of the time | the standard method of sensory testing (ISO 4120, ASTM E1885), from descriptions; the counts and powers are exact binomial computations |
| The hearing test's rule (10 dB down after a response, 5 dB up after a miss; threshold the lowest level heard on 2 of 3 rising presentations) | Hughson and Westlake (1944) as described in audiometer manufacturers' guides |

Everything else is computed by `compute.py` with Psyche's `psychophysics` module and is a model's behaviour,
tagged as such on screen. Psyche's observer has an impression of each stimulus with noise σ(I)² = σ₀² + (kI)²,
k = 0.08 and σ₀ = 0.5, a lapse rate of 2%, and answers a two-interval question exactly by the normal difference
rule; its just noticeable difference (75% correct) at a standard of 100 is 7.65. The sizes of all simulated
studies are set in advance; where a single study is shown it is the middle one of 101 by its estimate, picked by
rule and not by its result. The contrast sensitivity curve, the eye chart and the time-estimation spreads are
illustrations and say so.

| Number on screen | Value | How |
|---|---|---|
| Psyche's Weber fraction over the middle of the range | 0.076 | JND / standard at 100 |
| ... at an intensity of 1, near the floor | 0.48 | the floor σ₀ dominates below about 6 |
| Just noticeable steps from 1 to 1,000 (k = 0.08) | 90, 30 per decade | ln 1000 / ln 1.08 |
| Method of limits: threshold, descending, ascending | 14.1, 23.8, 4.4 | four series, steps of 2.5 |
| Method of limits for three willingnesses to say yes | 10.4, 14.9, 19.8 | medians of 200 runs each |
| Method of adjustment: point of subjective equality, SD, JND | 102.2, 11.2, 7.6 | 20 settings; JND = SD × z₀.₇₅ |
| Constant stimuli fit: α, β, λ; 75% threshold [95% interval]; truth | 7.6, 5.8, 0.06; 8.6 [6.3, 11.4]; 8.2 | 8 levels × 40 trials, ML, 1,000 bootstrap refits |
| Goodness of fit: share of repeats that fit worse than the data | 81% | the 1,000 refits' deviances |
| A threshold that drifts between blocks (factor e^(0.6z)): share that fit worse; studies flagged; median thresholds, drifting against steady | 49%; 5% of 41; 8.9 against 8.7 | 300 refits each; 101 fits each |
| One slip at the top level: threshold with λ fixed at 0, with λ free | 10.1, 8.1 | the same study with one more error at 24 |
| 2-down 1-up staircase, 80 trials, ×1.25 steps: estimate; 70.7% level | 7.4; 6.5 | one run, mean of the last 8 reversals |
| 3-down 1-up, 200 trials: median of 101 runs; 79.4% level | 9.75; 10.01 | |
| Coarse (×1.25) against fine (×1.12) steps: medians | 5.9, 6.4 | Levitt's target is a small-step result |
| QUEST, 40 trials: estimate; 82% level | 10.4; 11.3 | |
| Error after 32 trials (RMSE in log units, each against its own target) | constant stimuli 0.92, staircase 0.75, QUEST 0.36 | 101 runs each |
| Magnitude estimation on Psyche: fitted exponents (planted 0.33, 1.45, 3.5) | 0.33, 1.50, 3.70 | geometric means of 40 people |
| Cross-modality match of brightness to loudness | 0.49 | 0.33 / 0.67 |
| A grey midway between 4% and 85% reflectance: half the light, a power law (exponent 1/3), Fechner's logarithm | 44%, 27%, 18% | arithmetic mean, mean of cube roots, geometric mean |
| Range effect: fitted exponent over ranges of 10, 100, 1,000 | 1.34, 0.84, 0.67 | a judge who spreads any range over the same numbers |
| Noise that grows against a compressed code: ratio of thresholds | 0.96 to 0.99 | 41 standards |
| Threshold against background for an eye with a floor, photon noise and Weber noise: slopes | 0, 0.50, 1.00 | σ² = 0.05² + I + (0.02 I)² |
| Number: Weber fraction at three and at six, from 3:4 and 5:6 | 0.30, 0.19 | the ratio at 75% correct |
| Thurstone's Case V on 200 simulated judges, six offences: largest error against the planted scale | 0.03 (units of the noise of a difference) | normal deviates of the proportions, averaged |
| Bernoulli: ten ducats at a wealth of 10 against at 1,000 | about 70 times the value | ln 2 / ln 1.01 |
| Triangle test, 30 tasters: right answers needed at 5%; power if 30% can tell; tasters for 80% power at 30% and at 10% | 15; 71%; 40 and 325 | exact binomial, guess rate 1/3 |
| Hearing test: Psyche's listener (50% point 25 dB) gets a threshold of | 30 dB | the Hughson-Westlake rule on a scripted track |

## Built in this part

* `explainer/psychology/psyche/psychophysics.py`: an observer whose noise grows with intensity, with a floor, a
  lapse rate and an optional near miss; exact two-interval probabilities; Weber fractions and JNDs; psychometric
  functions (cumulative Gaussian, logistic, Weibull) with guess and lapse rates; maximum-likelihood fits with a
  bounded lapse rate, thresholds at any level and the parametric bootstrap; the method of limits (with a criterion),
  of adjustment and of constant stimuli; k-down 1-up staircases and their targets; a QUEST-style Bayesian placement;
  Fechner's count and law; Stevens's power law, magnitude estimation, power fits and cross-modality matching; a
  photon-noise term (the square-root regime), the bootstrap's goodness of fit, the triangle test's critical
  counts and power, and paired comparisons with Thurstone's Case V.
  Tested in `tests/psychology/test_psychophysics.py`.
* The Battery's second task, `threshold`: a two-interval brightness discrimination at eight increments over a
  standard of 100, run on Pool members.
* The Ledger gains two rows and the Archive fifteen datasets.
* The course's interactive is a real threshold measurement: two grey patches, a 2-down 1-up staircase over 50
  trials, and the reader's own psychometric curve fitted at the end.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| The smallest noticeable change in a stimulus is a constant fraction of its size | Weber 1834 | replicated |
| Judged magnitude grows as a power of stimulus intensity | Stevens 1957 | replicated |

Both rows carry their limits. Weber's law holds over the middle of most ranges and fails at the edges: near the
absolute threshold the fraction grows, and for loud tones it shrinks a little (McGill and Goldberg's near miss);
the fraction differs from sense to sense. The power form is among the most repeated results in psychophysics, but
the exponents are not constants of the senses: they move with the range presented, the first stimulus and the
numbers people like to use (Poulton 1968).

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Levitt's staircase, QUEST and
Wichmann and Hill's fitting (methods, derived or run on Psyche), the number sense (a preview; entered in Part 30),
scalar timing (shown as a pattern; the series does not study interval timing), and the quick CSF (a method at the
frontier; vision is entered in Part 13), the square-root law (a theory of the threshold; the eye's thresholds are
entered in Part 13), Bernoulli's logarithm (a preview; choices under risk are entered in Part 26), Plateau's painters (a historical
proposal; the power law's row is Stevens's), and Thurstone's scaling (a method, run on simulated judges; scaling
judgments is entered in Part 46).

## Build it

```bash
python -m videos.psychology.psych11.compute            # every number (a few minutes), into .cache/psych11/
python tools/qa_scene.py psych11 Fit                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych11 -q l   # the whole part, silent preview
python tools/build.py psych11                          # 1080p30 with narration
python tools/qa_scene.py psych11 Fit --lang zh         # the Chinese edition of one chapter
python tools/make.py psych11                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 11                    # the lab: Weber, three methods, a fit, a staircase, Stevens
python tools/check_ledger.py psych11                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's psychophysics module, the Battery, the Ledger
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Leipzig, 22 October 1850 | Fechner's morning; Kant's first objection, still unanswered after ten parts; which patch is brighter; objectives |
| 1 | Weber's fraction | ΔI = kI; on Psyche, a law in the middle and two edges: the floor and the near miss |
| 2 | Fechner's step | Counting just noticeable steps; the logarithm in four lines; the one assumption it rests on |
| 3 | Three classical methods | Limits, adjustment, constant stimuli, each run on Psyche; why a yes-no threshold moves with the observer's caution |
| 4 | The threshold is a curve | A step or a slope; four numbers (guess, threshold, spread, lapse); three shapes, nearly the same |
| 5 | On you: a threshold of your own | Eight pairs of patches; the answers and the chance of each for a model observer |
| 6 | Fitting the curve | The binomial likelihood; the likelihood over every curve; the bootstrap interval; does the curve fit, and the drift a fit cannot see; one slip and the lapse rate |
| 7 | Asking efficiently | The staircase and where it settles (p^k = 1/2); QUEST; three methods on the same budget of trials |
| 8 | Stevens asks for numbers | Magnitude estimation; straight lines on log-log axes; the table of exponents; cross-modality matching |
| 9 | Fechner against Stevens | Same Weber, two assumptions; hard to tell apart over the range people use; Plateau's painters and the middle grey; exponents that bend to the experiment |
| 10 | Where Weber's law comes from | Growing noise or a compressed code; the same thresholds, to within a few percent; the slope tells you the noise (dark light, the square-root law, Weber) |
| 11 | Weber's law elsewhere | Which cloud has more dots, through childhood; timed intervals whose spread grows with their length; Bernoulli's logarithm of wealth |
| 12 | The Ledger | Weber's law; Stevens's power law |
| 13 | In practice: hearing tests, eye charts and codecs | The audiometer's staircase; the eye chart as a descending method of limits; compression measured in JNDs; the triangle test and its power |
| 14 | Frontier: what the numbers measure | What is solid and what is argued; Thurstone's scale with no ruler; the quick CSF; open questions |
| | Recap, problems, and the road ahead | Ten lines; what today adds to the reply to Kant; payoffs; problems; references; Part 12 |

## Sources

**Books.** G. T. Fechner, *Elemente der Psychophysik* (1860). G. A. Gescheider, *Psychophysics: The Fundamentals*
(3rd ed., 1997). F. A. A. Kingdom and N. Prins, *Psychophysics: A Practical Introduction* (2nd ed., 2016).
S. S. Stevens, *Psychophysics* (1975).

**Papers.**
- E. H. Weber, *De Pulsu, Resorptione, Auditu et Tactu: Annotationes Anatomicae et Physiologicae* (1834); *Der
  Tastsinn und das Gemeingefühl* (1846).
- E. G. Boring, "Fechner: inadvertent founder of psychophysics", *Psychometrika* 26 (1961) 3–8.
- S. S. Stevens, "On the psychophysical law", *Psychological Review* 64 (1957) 153–181.
- E. C. Poulton, "The new psychophysics: six models for magnitude estimation", *Psychological Bulletin* 69 (1968)
  1–19.
- R. Teghtsoonian, "On the exponents in Stevens's law and the constant in Ekman's law", *Psychological Review* 78
  (1971) 71–80.
- H. Levitt, "Transformed up-down methods in psychoacoustics", *Journal of the Acoustical Society of America* 49
  (1971) 467–477.
- A. B. Watson and D. G. Pelli, "QUEST: a Bayesian adaptive psychometric method", *Perception & Psychophysics* 33
  (1983) 113–120.
- F. A. Wichmann and N. J. Hill, "The psychometric function: I. Fitting, sampling, and goodness of fit; II.
  Bootstrap-based confidence intervals and sampling", *Perception & Psychophysics* 63 (2001) 1293–1313, 1314–1329.
- W. J. McGill and J. P. Goldberg, "A study of the near-miss involving Weber's law and pure-tone intensity
  discrimination", *Perception & Psychophysics* 4 (1968) 105–109.
- J. Halberda, M. M. M. Mazzocco and L. Feigenson, "Individual differences in non-verbal number acuity correlate
  with maths achievement", *Nature* 455 (2008) 665–668; J. Halberda and L. Feigenson, "Developmental change in the
  acuity of the number sense", *Developmental Psychology* 44 (2008) 1457–1465.
- J. Gibbon, "Scalar expectancy theory and Weber's law in animal timing", *Psychological Review* 84 (1977)
  279–325.
- J. Plateau, "Sur la mesure des sensations physiques, et sur la loi qui lie l'intensité de ces sensations à
  l'intensité de la cause excitante", *Bulletins de l'Académie Royale de Belgique* 33 (1872) 376–388.
- L. L. Thurstone, "A law of comparative judgment", *Psychological Review* 34 (1927) 273–286; "The method of
  paired comparisons for social values", *Journal of Abnormal and Social Psychology* 21 (1927) 384–400.
- Hl. de Vries, "The quantum character of light and its bearing upon threshold of vision, the differential
  sensitivity and visual acuity of the eye", *Physica* 10 (1943) 553–564; A. Rose, "The sensitivity performance of
  the human eye on an absolute scale", *Journal of the Optical Society of America* 38 (1948) 196–208.
- D. Bernoulli, "Specimen theoriae novae de mensura sortis" (1738); translated by L. Sommer as "Exposition of a
  new theory on the measurement of risk", *Econometrica* 22 (1954) 23–36.
- L. A. Lesmes, Z.-L. Lu, J. Baek and T. D. Albright, "Bayesian adaptive estimation of the contrast sensitivity
  function: the quick CSF method", *Journal of Vision* 10(3):17 (2010) 1–21.

## Problems and solutions

**1.** *Weber's fraction for a task is 0.05. Starting at an absolute threshold of 1, how many just noticeable steps
lie between 1 and 1,000? Between 1,000 and 2,000? What does Fechner's law say about the sensation at 2,000 compared
with 1,000?*

Each step multiplies the intensity by 1.05, so the number of steps from a to b is ln(b/a) / ln 1.05, and ln 1.05 =
0.0488. From 1 to 1,000: 6.908 / 0.0488 ≈ 142 steps. From 1,000 to 2,000: 0.693 / 0.0488 ≈ 14 steps. Fechner's law
counts steps from the absolute threshold, so the sensation at 1,000 is about 142 units and at 2,000 about 156:
doubling the stimulus adds a tenth to the sensation. Every doubling, wherever it starts, adds the same 14 units.
That is the logarithm, and the claim that a doubled stimulus is not a doubled sensation is exactly what Stevens
later disputed.

**2.** *A two-interval observer's impression of each stimulus has a standard deviation of σ. Show that it is right
75% of the time when the increment is √2 z₀.₇₅ σ ≈ 0.95σ. If σ = 0.08 I, what is Weber's fraction?*

Call the two impressions X₁ ~ N(I, σ²) and X₂ ~ N(I + Δ, σ²), independent. The observer is right when X₂ > X₁. The
difference X₂ − X₁ is normal with mean Δ and standard deviation √2 σ, so P(right) = Φ(Δ / (√2 σ)). Setting this to
0.75 gives Δ / (√2 σ) = z₀.₇₅ = 0.674, so Δ = √2 × 0.674 σ = 0.954σ. With σ = 0.08 I the JND is 0.954 × 0.08 I =
0.076 I: Weber's fraction is 0.076, the value Psyche shows over the middle of its range. (Psyche's noise at I + Δ
is slightly larger than at I, and its floor adds a little near the bottom; neither changes the second decimal at
100.) The lesson: Weber's law follows from noise that grows in proportion to the stimulus, and the fraction is the
noise's coefficient times a constant set by the definition of "just noticeable".

**3.** *Derive where a 3-down 1-up staircase settles. Which rule would you use to measure the 84% point? Why does a
large step size bias the estimate?*

The level goes down after three right answers in a row and up after any wrong one. At a level where the chance of
a right answer is p, the chance of going down is p³ and of going up 1 − p³ (ignoring the runs that are cut short,
which affect only when the step happens, not its direction). The staircase hovers where up and down are equally
likely: p³ = 1/2, p = 0.5^(1/3) = 0.794. For 84%: p^k = 1/2 gives k = ln 0.5 / ln 0.84 = 3.98, so a 4-down 1-up
rule (0.841). Large steps: the derivation treats p as the same at the levels just above and just below the point
the staircase oscillates around. With large steps the two levels sit on different parts of the curve, where it
bends, and the balance point between them is no longer the level where p^k = 1/2. On Psyche, with steps of ×1.25
the 2-down 1-up median was 5.9 against a 70.7% level of 6.5; with ×1.12 it was 6.4. Levitt's targets are what a
staircase approaches as the steps shrink.

**4.** *At one level, 30 of 40 trials are right. Write the binomial log-likelihood of a proportion p and find its
maximum. Use √(p(1−p)/n) to give an approximate 95% interval.*

ln L(p) = 30 ln p + 10 ln(1 − p) + ln C(40, 30). Its derivative is 30/p − 10/(1 − p), which is zero at p = 30/40 =
0.75. The standard error is √(0.75 × 0.25 / 40) = 0.068, so the interval is 0.75 ± 1.96 × 0.068, about 0.62 to
0.88. A single level of forty trials pins a proportion to about ±0.13; this is why the film's fit, with eight
levels, still has an interval for the threshold of 6.3 to 11.4, roughly ±30%. Fitting the whole curve borrows
strength across levels, but forty trials a level is not a precise measurement.

**5.** *Brightness has exponent 0.33 and loudness 0.67. By what factor must light increase to double brightness? In
a cross-modality match, by what factor must sound pressure rise when light rises tenfold?*

Brightness ∝ L^0.33, so doubling it needs L to rise by 2^(1/0.33) = 2^3.03 ≈ 8.2. A tenfold rise in light raises
brightness by 10^0.33 = 2.14. For the matched loudness, which grows as P^0.67, to rise by the same factor, sound
pressure must rise by 2.14^(1/0.67) = 10^(0.33/0.67) = 10^0.49 ≈ 3.1. On log-log axes the match is a straight line
of slope 0.33 / 0.67 = 0.49, predicted from two separate experiments that both asked for numbers, and checked by a
third that asks for none. This was Stevens's strongest argument that the numbers measured something.

**6.** *With `explainer.psychology.psyche.psychophysics`: run `staircase` 200 times with step factors 1.1 and 1.5,
and `quest` with 20 and 60 trials; compare each with the level it aims at.*

```python
import numpy as np
from scipy import optimize
from explainer.psychology.psyche import psychophysics as P

o = P.Observer()
level = lambda p: optimize.brentq(lambda d: float(o.p_correct(100.0, d)) - p, 0.01, 60)
for f in (1.1, 1.5):
    e = [P.staircase(o, 100.0, 24.0, factor=f, rng=np.random.default_rng(i), n_trials=200)["estimate"]
         for i in range(200)]
    print(f, np.median(e), level(P.updown_target(2)))
for n in (20, 60):
    e = [P.quest(o, 100.0, n, rng=np.random.default_rng(1000 + i))["estimate"] for i in range(200)]
    print(n, np.median(e), level(0.82))
```

The 70.7% level is 6.53. With 200 trials, steps of ×1.1 give a median of 6.4 and steps of ×1.5 give 5.8: the
coarse staircase sits low, as in problem 3. With the default 80 trials the fine staircase gives 7.6, too high,
because from a start of 24 it spends its first reversals still coming down: small steps need more trials. QUEST's
82% level is 11.3; its median is 10.1 after 20 trials and 10.7 after 60, and its error (RMSE in log units) falls
from 0.48 to 0.27. Every method trades bias against trials, and the honest report gives both.

**7.** *★ Psyche's two observers of chapter 10 have the same thresholds. Design a measurement other than a threshold
that would tell them apart, and say what each predicts.*

One observer's internal signal grows in proportion to the stimulus, with noise that grows too; the other's signal
is the logarithm of the stimulus, with constant noise. Thresholds depend only on the ratio of signal difference to
noise, which is the same for both, so no discrimination experiment at one level separates them. A measurement of
the signal's *shape* can. Bisection: show 10 and 1,000 and ask for the stimulus halfway between them in sensation.
The compressed code puts the midpoint at the geometric mean, 100; the proportional code at the arithmetic mean,
505. Or compare differences: is the difference between 10 and 20 larger, smaller or the same as between 100 and
200? The compressed code says the same; the proportional code says the second, by a factor of ten in signal, though
not in discriminability. A third route measures the noise directly: with confidence ratings or response times,
the proportional observer's variability at high levels is larger in absolute terms, the compressed one's the same.
Real data from bisection and difference judgments do not cleanly choose either, which is the subject of the
frontier chapter: such judgments carry their own biases, as Poulton showed for magnitude estimates.

## Where it comes back

Seeing against saying, and the method of limits' moving threshold: Part 12, *Signal and Noise*. The eye's
thresholds and contrast: Part 13. Prices and whether anyone notices a change: Part 26. The number sense in
children: Part 30. Scaling people's judgments, from magnitude estimates to survey scales: Part 46. Displays built
for human thresholds: Part 51. Why perception compresses, and efficient coding: Part 58. Psyche's `psychophysics`
module and the Battery's `threshold` task supply the observer, the fits and the staircases those parts use.

## Open checks

Before the narrated master:

* Fechner: "forty-nine", "a physicist worn out by years of illness" (his breakdown of about 1839 to 1843; by 1850
  he had recovered his sight and health in part), "ten years of experiments" and the date are from Boring (1961)
  and histories, not from the *Elemente* itself. Fechner Day as kept by the International Society for
  Psychophysics is from memory.
* Weber: no historical value of his fraction for lifted weights is given, because sources disagree (1/30, 1/40,
  8 to 10%). The Latin title of 1834 differs between sources; the archive gives the form found most often.
  "An anatomist and physiologist in Leipzig" is from histories.
* Stevens's table of exponents is from textbooks reproducing it, not from the 1957 paper; which publication first
  gave each value is not settled here. Loudness 0.67 is for a 3,000 Hz tone, with respect to sound pressure.
  The cross-modality results Stevens reported (that matches follow the ratio of exponents) are from summaries.
* Poulton (1968) and Teghtsoonian (1971) were read only in abstract and summary. "Ekman's law" is named only in a
  reference title.
* Watson and Pelli (1983): the page numbers are from memory. Psyche's QUEST is a grid posterior with the trial
  placed at the posterior mean; the original places it at the posterior mode or mean with a Weibull, and the
  details differ.
* The hearing test: the Hughson-Westlake rule is from audiometer manufacturers' guides; ASHA's own wording was not
  read. Clinical practice varies in the starting level and whether the threshold needs 2 of 3 or 2 of 4 rising
  presentations.
* The eye chart as a descending method of limits with a small guess rate, and codecs that "measure what they keep
  in units of just noticeable difference", are general descriptions from memory, not from a particular standard.
* The staircase biases on Psyche (coarse steps sitting low, fine steps needing more trials) are this model's; the
  direction of the coarse-step bias in real data depends on the curve's shape and the step rule.
* Halberda: "adults about 0.11" is the mean in the 2008 *Nature* study; the children's ratios (3:4 at three, 5:6
  at six) are from the developmental paper's abstract. The film's fractions at three and six (0.30 and 0.19) are
  computed from those ratios by the film's own definition and are not the paper's numbers.
* The time-estimation spreads on screen are an illustration with a coefficient of variation of 0.15, not a
  dataset.
* de Vries (1943) and Rose (1948): the page numbers are from memory; the claim that measured threshold-versus-
  background curves "bend this way, though the middle is only roughly a square root" rests on encyclopedia entries
  and later papers' discussions (rod vision fits it best; gratings and higher spatial frequencies depart). Psyche's
  eye has its constants chosen to show three clean regimes.
* Bernoulli (1738): the volume and pages of the original are from memory; the rule (section 10) and its use for
  insurance and the St Petersburg game are from the translation as quoted in later accounts.
* The triangle test: the standards (ISO 4120, ASTM E1885) were not read; the method's description and the guess rate
  are from descriptions of them. The "proportion of distinguishers" model (those who can tell answer right, the rest
  guess) is the one these standards use for power, from memory.
* The drifting observer: its drift (a factor e^(0.6z) per block of ten trials) is this film's choice. That the
  deviance test has little power against such drift with 40 trials a level is a result for this design, not a
  general law; larger drifts, more trials or slower drifts would be caught more often.
* Plateau (1872): only later papers' accounts were read. That he "argued for a power law" from the painters' greys
  is how they describe it; the number of painters, the greys they painted and his exponent are not given. Delboeuf's
  finding that the midpoints moved with the lighting is from the same accounts. The patches on screen are encoded for
  an sRGB display and are approximate. "The grey card photographers meter against" (18%) is the usual description;
  the card's history is not checked.
* Thurstone (1927): the crime scale's nineteen offences are from a replication's account; the six offences and
  their planted seriousness on screen are invented for the simulation. Elo's system and preference leaderboards as
  "descendants" is a summary from memory (Elo's original rating assumed normally distributed performances; current
  leaderboards fit Bradley-Terry models).

