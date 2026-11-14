# Psychology, Built: Part 12, Signal and Noise

In the Second World War, British aircraft hunted submarines by radar, and an observer watched a dim screen for
hours for a faint blip among specks of noise. The Royal Air Force found that its observers missed real contacts, and
missed more as a patrol wore on; sometimes they reported a contact that was nothing. It asked Norman Mackworth why,
and in 1948 he published a laboratory version, a clock pointer that now and then jumped twice as far, watched for
two hours. The double jumps reported fell as the watch went on. But a miss can mean two things: the jump was not
seen, or it was seen and the observer was not sure enough to say so. A hit rate alone cannot tell them apart.

This part is the theory that can, worked out for radar receivers by engineers at Michigan in 1954 and brought into
psychology the same year by Wilson Tanner and John Swets. It is the third objection's day in Kant's wager: the
observer's report is coloured by the reporting, and detection theory measures the colouring. The route: four
outcomes and why a hit rate means nothing alone; two distributions and a line, giving d′ for seeing and c for
saying; the ROC, and the viewer's own d′ from a memory test; the ideal observer, the likelihood ratio and the trap
in maximizing accuracy when signals are rare; fitting rating ROCs and recognition's slope of 0.8; forced choice and
the root two; the high-threshold and dual-process rivals; base rates and the mammogram; the prevalence effect; and
the radar watch revisited, where the false alarms tell caution from fatigue. The practice chapter is screening,
alarms and the classifier ROC of machine learning; the frontier is confidence about one's own decisions.

## Where the numbers come from

| What | Source |
|---|---|
| Airborne radar observers missing contacts; the RAF's request; the Clock Test, two hours, the vigilance decrement | Mackworth (1948), from encyclopedia entries and reviews; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md); the detection rates are not given |
| The theory of signal detectability, noise against signal plus noise, and the ROC for receivers | Peterson, Birdsall and Fox (1954), from the library record and later accounts |
| A decision-making theory of visual detection; the yes-no threshold as a decision | Tanner and Swets (1954) |
| Payoffs, probabilities and ratings on one ROC; the theory's spread in psychology | Swets, Tanner and Birdsall (1961), from later reviews; Green and Swets (1966) |
| The likelihood-ratio rule is most powerful | Neyman and Pearson (1933), as in *Statistics, Built*, Part 10 |
| Recognition zROC slopes near 0.8 | Ratcliff, Sheu and Gronlund (1992), from reviews |
| The dual-process (recollection plus familiarity) account of recognition ROCs | Yonelinas (1994), from the author's posted copy |
| The mammogram problem: 1%, 80%, 9.6%; correct answers 16% with probabilities, 46% with natural frequencies | Gigerenzer and Hoffrage (1995), from later papers quoting it; Eddy (1982) for the problem |
| Misses of 11%, 25% and 52% at prevalences of 50%, 10% and 1%; false alarms very rare | Wolfe, Horowitz and Kenner (2005), from a public copy of the text |
| Letting observers correct a hasty answer removes much of the prevalence effect | Fleck and Mitroff (2007), from later summaries |
| 42 vigilance studies: a real sensitivity decrement that depends on the task and the event rate | See, Howe, Warm and Dember (1995), from the abstract |
| The same decision process across diagnostic fields | Swets, Dawes and Monahan (2000), from the abstract |
| Meta-d′: how much of the evidence confidence can use | Maniscalco and Lau (2012), from the abstract |
| Line-ups: sequential procedures had the higher diagnosticity ratio (0.44/0.15 against 0.52/0.28) but simultaneous ones discriminated better by ROC | Mickes, Flowe and Wixted (2012), from the posted copy's summary as quoted |

Everything else is computed by `compute.py` with Psyche's `sdt` module and is a model's behaviour, tagged as such on
screen. Psyche's observer has normal evidence on blank trials and normal evidence shifted by d′ (and in chapters 6
and 8 widened by 1.25) on signal trials, and says yes past a criterion. Every simulated study shown alone is the
middle one of many by a statistic fixed in advance. The radar screen, the clock, and the distributions of
recognition's familiarity are drawings and say so.

| Number on screen | Value | How |
|---|---|---|
| One observer (d′ = 1.5) under five payoff schemes: hit rates; false-alarm rates; d′; c | 97% to 37%; 63% to 3%; 1.50 in every scheme; −1.07 to +1.07 | the best criterion for each scheme |
| The correction for guessing, (H − F)/(1 − F), for one observer at five criteria; d′ | 0.87 down to 0.29; 1.50 throughout | closed form |
| A criterion at 1.0 with d′ = 1.5: hit and false-alarm rates; z scores; d′; c | 69%, 16%; 0.50, −1.00; 1.50; 0.25 | closed form |
| Area under the ROC for d′ = 1.5 | 0.856, the same as Φ(d′/√2) | closed form |
| Two tests with equal area (0.856): hits at 2% false alarms; at 30% | B (signal twice as wide) 56%, A 29%; 82% and 84% | binormal ROCs crossing near 27% |
| A rating study (150 + 150 trials): five ROC points | on the d′ = 1.5 curve | the middle of 101 by area |
| On you: 9 hits and 3 false alarms of 12 | d′ ≈ 1.2, c ≈ 0 | log-linear correction |
| Ideal criteria for signals 50%, 20%, 5% of the time: β; hit rates | 1, 4, 19; 77%, 43%, 11% | d′ = 1.5, equal payoffs |
| At 5%: correct with the best line; saying no to everything; the midpoint line | 95.2%; 95%; 77% | the same |
| Rating study from σ = 1.25: fitted slope and d′; equal-variance test | 0.81 and 1.19 (planted 0.80, 1.25); χ² = 5.5, p = 0.019 | 300 + 300 trials, the middle of 41 by slope |
| Two-interval forced choice at d′ = 1: correct; an unbiased yes-no observer | 76%; 69% | Φ(d′/√2), Φ(d′/2) |
| 75% correct in two-interval choice means d′ = | 0.95 | √2 z₀.₇₅ |
| High-threshold line against the rating data: squared error; detection curve; dual process (recollection 15%) | 0.051; 0.001; 0.002 | least squares in ROC space |
| Mammogram in natural frequencies: of 103 positives, real | 8 (7.8%) | 1,000 women |
| The same test where 10% are ill | 48% | the same rates |
| Bayes's rule in odds: likelihood ratio of a positive; after a second positive; after a negative | 8.3; 41%; 0.22% | odds before × H/F |
| Misses for a criterion moved half way, and all the way, to the ideal at 50%, 10%, 1% (d′ = 2.5) | 11%, 21%, 37%; 11%, 36%, 72% | the published 11%, 25%, 52% lie between |
| Two watchers over two hours: hit rates; false alarms (A, growing cautious; B, seeing less) | 76% to 44% for both; 10% to 2% (A), 10% to 32% (B) | 25 signals and 225 blanks a block |
| Two readers, each d′ = 1.5: averaged, independent; correlated 0.5; 'either says yes' hits and false alarms; 'both' | 2.12; 1.73; 95% and 40%; 60% and 5% | closed form |
| One witness at two criteria: diagnosticity ratio (d′ = 1.2) | 2.5 lax, 4.7 strict | the same ROC |
| A spam filter with d′ = 2: area under the ROC; precision at 80% recall, half spam and 1% spam | 0.92; 87% and 6% | closed form |
| Confidence's own ROC: area for an exact, a noisy and a noisier confidence (accuracy 77% for all) | 0.73, 0.65, 0.57 | 200,000 simulated trials each |

## Built in this part

* `explainer/psychology/psyche/sdt.py`: the equal- and unequal-variance observer; hit and false-alarm rates; d′, c
  and β from rates, with the log-linear correction; ROCs, zROCs and their area; rating counts simulated and fitted
  by maximum likelihood with equal or unequal variances; the likelihood ratio, the optimal β and criterion from
  base rates and payoffs, and expected value; two- and m-alternative forced choice; the high-threshold and
  dual-process ROCs; natural frequencies and positive predictive value; criteria that follow prevalence. Tested in
  `tests/psychology/test_sdt.py`.
* The Ledger gains three rows and the Archive thirteen datasets.
* The course's interactive is an old/new recognition test with confidence ratings that draws the reader's ROC.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Changing the payoffs or the base rate moves where an observer says yes, while sensitivity stays the same | Tanner and Swets 1954 | replicated |
| When targets are rare, searchers miss more of them | Wolfe, Horowitz and Kenner 2005 | replicated |
| Recognition memory's zROC slope is below one, about 0.8 | Ratcliff, Sheu and Gronlund 1992 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Mackworth's watch and the 1995
meta-analysis (vigilance is entered in Part 51), the mammogram problem (judgment is entered in Part 26), meta-d′ (a
method; confidence is entered in Part 25), Swets, Dawes and Monahan (a review of applications) and the line-up study
(a live dispute; eyewitness memory is entered in Part 21).

## Build it

```bash
python -m videos.psychology.psych12.compute            # every number (under a minute), into .cache/psych12/
python tools/qa_scene.py psych12 Roc                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych12 -q l   # the whole part, silent preview
python tools/build.py psych12                          # 1080p30 with narration
python tools/qa_scene.py psych12 Roc --lang zh         # the Chinese edition of one chapter
python tools/make.py psych12                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 12                    # the lab: d′ and c, ROCs, fitting, the ideal observer
python tools/check_ledger.py psych12                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's sdt module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Radar observers, 1940s | The radar screen; Mackworth's Clock Test; Kant's third objection; objectives |
| 1 | Four outcomes | Hits, misses, false alarms, correct rejections; one observer under five reward schemes; the correction for guessing |
| 2 | Two distributions and a line | The picture; d′ and c from two rates; two knobs; chapter 1 in the two numbers |
| 3 | The ROC | Slide the line and trace the curve; the family by d′ and the area; two tests with the same area; a whole curve from confidence ratings |
| 4 | On you: old or new? | Twelve words; twenty-four tested; the answers; your d′ from a table |
| 5 | The ideal observer | The likelihood ratio and Neyman-Pearson; base rates and payoffs move the line; accuracy rewards silence |
| 6 | Fitting an ROC | zROCs and their slope; a maximum-likelihood fit, equal against unequal variance; recognition's lopsided evidence |
| 7 | Forced choice | The difference of two looks and the root two; more alternatives, a lower floor |
| 8 | Threshold or signal detection? | The high-threshold line against curved data; recollection plus familiarity, and why it fits as well |
| 9 | Base rates | The mammogram problem; natural frequencies; Bayes's rule in odds; the same test in different populations |
| 10 | When targets are rare | The prevalence effect; a criterion that follows the base rate; quitting too soon |
| 11 | The watch, revisited | Two watchers with one hit rate and opposite false alarms; what does fall on a long watch |
| 12 | The Ledger | The criterion moves; the prevalence effect; recognition's zROC slope |
| 13 | In practice: screening, alarms and classifiers | Signal, noise and criterion across fields; double reading; police line-ups; ROC against precision and recall |
| 14 | Frontier: knowing what you saw | What is solid and what is argued; confidence's own ROC and meta-d′; open questions |
| | Recap, problems, and the road ahead | Ten lines; the third objection; payoffs; problems; references; Part 13 |

## Sources

**Books.** D. M. Green and J. A. Swets, *Signal Detection Theory and Psychophysics* (1966). N. A. Macmillan and
C. D. Creelman, *Detection Theory: A User's Guide* (2nd ed., 2005). T. D. Wickens, *Elementary Signal Detection
Theory* (2002).

**Papers.**
- N. H. Mackworth, "The breakdown of vigilance during prolonged visual search", *Quarterly Journal of Experimental
  Psychology* 1 (1948) 6–21.
- W. W. Peterson, T. G. Birdsall and W. C. Fox, "The theory of signal detectability", *Transactions of the IRE
  Professional Group on Information Theory* 4 (1954) 171–212.
- W. P. Tanner Jr. and J. A. Swets, "A decision-making theory of visual detection", *Psychological Review* 61 (1954)
  401–409.
- J. A. Swets, W. P. Tanner Jr. and T. G. Birdsall, "Decision processes in perception", *Psychological Review* 68
  (1961) 301–340.
- R. Ratcliff, C.-F. Sheu and S. D. Gronlund, "Testing global memory models using ROC curves", *Psychological
  Review* 99 (1992) 518–535.
- A. P. Yonelinas, "Receiver-operating characteristics in recognition memory: evidence for a dual-process model",
  *Journal of Experimental Psychology: Learning, Memory, and Cognition* 20 (1994) 1341–1354.
- G. Gigerenzer and U. Hoffrage, "How to improve Bayesian reasoning without instruction: frequency formats",
  *Psychological Review* 102 (1995) 684–704.
- J. E. See, S. R. Howe, J. S. Warm and W. N. Dember, "A meta-analysis of the sensitivity decrement in vigilance",
  *Psychological Bulletin* 117 (1995) 230–249.
- J. A. Swets, R. M. Dawes and J. Monahan, "Psychological science can improve diagnostic decisions", *Psychological
  Science in the Public Interest* 1 (2000) 1–26.
- J. M. Wolfe, T. S. Horowitz and N. M. Kenner, "Rare items often missed in visual searches", *Nature* 435 (2005)
  439–440.
- M. S. Fleck and S. R. Mitroff, "Rare targets are rarely missed in correctable search", *Psychological Science* 18
  (2007) 943–947.
- L. Mickes, H. D. Flowe and J. T. Wixted, "Receiver operating characteristic analysis of eyewitness memory:
  comparing the diagnostic accuracy of simultaneous versus sequential lineups", *Journal of Experimental
  Psychology: Applied* 18 (2012) 361–376.
- B. Maniscalco and H. Lau, "A signal detection theoretic approach for estimating metacognitive sensitivity from
  confidence ratings", *Consciousness and Cognition* 21 (2012) 422–430.

## Problems and solutions

**1.** *One observer has a hit rate of 0.84 and a false-alarm rate of 0.16; another, 0.69 and 0.07. Find d′ and c
for each. Do they see differently, or decide differently?*

First: z(0.84) = 0.99 and z(0.16) = −0.99, so d′ = 1.99 and c = −½(0.99 − 0.99) = 0. Second: z(0.69) = 0.50 and
z(0.07) = −1.48, so d′ = 1.97 and c = −½(0.50 − 1.48) = 0.49. Their sensitivities are the same to two decimals; the
second observer is more cautious, by about half a standard deviation. Compared by hit rate alone, the second looks
worse at seeing; compared by false-alarm rate alone, better. Neither is true.

**2.** *For the equal-variance model, show that the likelihood ratio is exp(d′x − d′²/2), and that the ideal
criterion is x\* = d′/2 + ln β / d′. Find it for d′ = 2, signals on a quarter of trials, all outcomes worth the
same.*

ℓ(x) = φ(x − d′)/φ(x) = exp(−(x − d′)²/2 + x²/2) = exp(d′x − d′²/2). Setting ℓ(x) = β and taking logs gives
d′x − d′²/2 = ln β, so x\* = d′/2 + ln β / d′. With equal payoffs β = P(noise)/P(signal) = 0.75/0.25 = 3, and
x\* = 1 + ln 3 / 2 = 1.55. The hit rate is 1 − Φ(1.55 − 2) = Φ(0.45) = 0.67 and the false-alarm rate 1 − Φ(1.55) =
0.06. Because the ratio rises monotonically with x, a line on x is the likelihood-ratio rule, and by the
Neyman-Pearson lemma no other rule with this false-alarm rate gets more hits.

**3.** *Show that the area under an equal-variance ROC is Φ(d′/√2), and under an unequal-variance one
Φ(d′/√(1 + σ_s²)).*

The ROC plots H(k) = P(X_s > k) against F(k) = P(X_n > k) as k runs over the line. The area is ∫ H dF over the
false-alarm axis; substituting F = P(X_n > k), dF is minus the noise density at k, so the area is
∫ P(X_s > k) f_n(k) dk = P(X_s > X_n) for independent draws. The difference X_s − X_n is normal with mean d′ and
variance 1 + σ_s², so P(X_s − X_n > 0) = Φ(d′/√(1 + σ_s²)), which for σ_s = 1 is Φ(d′/√2), the two-interval score.

**4.** *With the mammogram's hit and false-alarm rates (0.8 and 0.096), at what prevalence is a positive test right
half the time?*

The share of positives that are real is 0.8p / (0.8p + 0.096(1 − p)). Setting it to ½: 0.8p = 0.096(1 − p), so
p = 0.096 / 0.896 = 0.107. Only where about one woman in nine is ill does a positive test become a coin flip; in a
screening population of 1% it is right about one time in thirteen.

**5.** *A high-threshold observer detects with p = 0.5 and otherwise guesses yes at rate g. Compute d′ from its rates
for g = 0.1 and g = 0.4. What does the difference say about using d′ when that model is true?*

H = p + (1 − p)g and F = g. For g = 0.1: H = 0.55, F = 0.10, d′ = z(0.55) − z(0.10) = 0.13 + 1.28 = 1.41. For
g = 0.4: H = 0.70, F = 0.40, d′ = 0.52 + 0.25 = 0.78. The observer's sensitivity, p, has not changed, but d′ has
halved, because the high-threshold ROC is a straight line and d′ assumes a curved one. If that model were true,
comparing d′ across conditions with different criteria would mislead. That observers' d′ stays roughly constant
across criteria in real detection data is one of the arguments against the model (chapter 8).

**6.** *With `explainer.psychology.psyche.sdt`: simulate rating studies from an observer with σ_s = 1.25 at 50 and at
500 trials of each kind, and find how often `fit_rating` rejects equal variances.*

```python
import numpy as np
from scipy import stats
from explainer.psychology.psyche import sdt as D

obs, crit = D.Observer(d=1.25, sigma_s=1.25), [-0.4, 0.2, 0.7, 1.2, 1.8]
for n in (50, 500):
    rejected = 0
    for i in range(200):
        cs, cn = D.simulate_ratings(obs, crit, n, n, np.random.default_rng(5000 + i))
        lr = 2 * (D.fit_rating(cs, cn)["loglik"] - D.fit_rating(cs, cn, equal_variance=True)["loglik"])
        rejected += stats.chi2.sf(lr, 1) < 0.05
    print(n, rejected / 200)
```

With 50 trials of each kind the test rejects equal variances 17% of the time; with 500, 91%. A typical recognition
experiment has tens of trials per person, which is why zROC slopes are usually estimated from many people pooled,
and why a single person's slope means little.

**7.** *★ Chapter 11's two watchers have the same hit rates. Design a single session that tells them apart, and say
what each predicts.*

Include blank trials and count false alarms: the cautious watcher's false alarms fall over the session and the
tiring one's rise, while both lose hits; computed block by block, the first keeps d′ and raises c, the second keeps c
and loses d′. Two further checks need no new trial types. Ask for a confidence rating on every response and fit a
rating ROC per block: the cautious watcher's points slide along one curve, the tiring watcher's curve sinks toward
the diagonal. Or change the payoff in the last block, rewarding hits: a watcher who had only grown cautious recovers
its early hit rate at an unchanged false-alarm cost, which a watcher who sees less cannot do.

## Where it comes back

The eye's single photons and its own noise: Part 13. Recognition memory, line-ups and false memories: Part 21.
Confidence and evidence over time: Part 25. Base rates and judgment: Part 26. Awareness measured with d′: Part 27.
Alarms, long watches and rare targets: Part 51. Hiring as a detection problem: Part 53. Psyche's `sdt` module
supplies the observer, the ROCs and the fits those parts use.

## Open checks

Before the narrated master:

* The radar story: "the Royal Air Force found that its observers missed real contacts, and missed more as a patrol
  wore on", "sometimes reported a contact that was nothing", and "asked Mackworth why" are from encyclopedia
  entries and reviews, not from Mackworth (1948). "A pointer that jumps one step every second" is the usual
  description of the clock; the number of double jumps and the detection rates are not given.
* "Engineers at Michigan for radar receivers": Peterson, Birdsall and Fox's paper concerns detecting signals in
  noise for receivers; that it was built for radar specifically is the usual account, from memory.
* "The ROC" as the radar engineers' name: from the theory's histories, not checked against the 1954 paper's
  wording.
* That people move their criterion in the right direction but less than an ideal observer (the Ledger row's note)
  is the usual summary in detection texts, from memory.
* Neyman-Pearson (1933) and *Statistics, Built* Part 10: the cross-reference follows the syllabus.
* Recognition's slope of 0.8 and its readings (wider old-item distributions, encoding variability, the
  dual-process mixture) are from reviews; Ratcliff et al.'s title and pages are from memory.
* The mammogram: "most people, doctors included, guess far higher" is the standard summary of Eddy (1982) and
  later studies, from memory; the 16% and 46% are one source's figures, which others round to "about 20%" and
  "about 50%".
* Wolfe et al. (2005): the stimuli as "a tool among overlapping objects, like a baggage X-ray" and the three miss
  rates are from a public copy of the text; the number of observers is not given. Fleck and Mitroff (2007): that
  "most of the extra misses disappeared" is a summary; the volume and pages are from memory. Threat-image
  projection at airports is described from general knowledge.
* See et al. (1995): "a real loss of sensitivity whose size depended on the kind of discrimination and on event
  rate" is from the abstract as quoted; the later criterion-shift argument is from a 2015 paper found by search.
* Swets, Dawes and Monahan (2000): only the abstract was read; the table of fields on screen is this film's.
* The prevalence model (a criterion moved a share of the way to the accuracy-maximizing one) and the confidence
  model (confidence reading the evidence with extra noise) are illustrations whose constants were chosen; the
  watchers' rates were constructed so that their hit rates match exactly.
* The correction for guessing as "still found in multiple-choice scoring and some clinical tests" is a general
  statement from memory.
* Double reading: "many screening programmes have each image read twice" and the 'either says yes' rule are general
  descriptions; the readers' correlation of 0.5 is an illustration.
* Line-ups: the ratios 0.44/0.15 and 0.52/0.28 are from one experiment as quoted in a summary; that sequential
  line-ups were "widely recommended" is from the paper's framing and later commentary; the authors' first names
  (Laura Mickes, Heather Flowe, John Wixted) are from memory. Defences of the ratio exist (for example Clark 2012)
  and are not presented in detail.

