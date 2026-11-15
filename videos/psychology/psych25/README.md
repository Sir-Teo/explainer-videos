# Psychology, Built: Part 25, Deciding in Time

A cloud of moving dots: which way? You can wait and be right, or answer now and risk being wrong, and you choose the
rate of exchange. This part asks why a decision takes the time it takes, and answers with one idea in many forms:
evidence added up, noisily, until it crosses a line. Wald found it was the fastest reliable way to decide, Ratcliff
found it fits people's choices and times together, and Shadlen found it, or something like it, in neurons.

Moving dots on you, slow and then fast; Hick's law, with a race of accumulators that recovers the logarithm, and
Fitts's law derived from iterative corrections; the speed–accuracy trade-off in 17 people's open data and as a
curve traced by one model; the shape of a response-time distribution, an ex-Gaussian fit and why the mean misleads;
Wald's sequential probability ratio test run on a shell's hits and misses, its bounds and average sample number
against a fixed test, and its optimality; the diffusion model's four numbers, P(upper) and the mean decision time
derived, and the first-passage densities computed by Navarro and Fuss's series and checked by simulation; selective
influence, tested on the 17 people (fitted per person under four models) and on Ratcliff and Rouder's three
observers at 33 brightnesses; fast and slow errors, in the data and from variability in start and in drift;
accumulators in LIP, averaged as Roitman and Shadlen averaged them, and the ramping–stepping dispute; the linear
ballistic accumulator, leaky competing accumulators and urgency; the stop-signal race and the integration method;
and confidence as the balance of evidence, with its folded X. The practice chapter is interfaces, braking and
clinics; the frontier is attention in value-based choice and whether decision parameters are traits.

## Where the numbers come from

| What | Source |
|---|---|
| Wald's bounds ±2.94 (19 to 1) for p = 0.5 against 0.7 with α = β = 0.05; a hit adds 0.34, a miss subtracts 0.51; the median run of 101 stopped at shot 32 | Psyche (`decide.sprt_bernoulli`, `wald_bounds`), item `sprt` |
| Average shots about 30 under p = 0.5 and 32 under p = 0.7 (Wald's approximation), simulated 33 and 34; a fixed exact binomial test needs 67 | Psyche (`decide.sprt_oc_asn`, `sprt_simulate`, `fixed_n`), item `sprt` |
| A race of 2, 4, 8 and 16 accumulators held to 90% accuracy: mean decision time 0.61, 1.12, 1.52, 1.88 (model units), about 0.42 per bit | Psyche (`decide.race_hick`), item `hick` |
| Corrections leaving a share 0.25 of the distance: 3 for a 5-bit movement | Psyche, item `fitts` (Crossman and Goodeve's model) |
| 17 people, 31,351 kept trials: told to be accurate, all 17 slower and all 17 more accurate; the median person paid 223 ms for 8 points of accuracy | Wagenmakers, Ratcliff, Gomez and McKoon (2008), with Heathcote and Love's two extra participants, as packaged in the R package rtdists (GPL ≥ 3), fetched by `explainer.psychology.opendata` and checked by SHA-256; item `selective` |
| The median person by mean time (person 3): 928 correct times in accuracy blocks, mean 0.76 s, median 0.69 s; ex-Gaussian μ 0.54 s, σ 0.07 s, τ 0.23 s | the same data; Part 1's `chronometry.fit_exgauss`, item `shape` |
| v = 1.5, a = 1.2, z = a/2: P(upper) 0.858 (simulated 0.861), mean decision time 0.287 s (simulated 0.297 s, Euler steps of 0.5 ms); the same conditional mean for both bounds | Psyche (`decide.p_upper`, `mean_dt`, `fpt_density`, `simulate`), item `ddm` |
| Per-person fits with w fixed at 0.5: bound lower under speed for 16 of 17, to a median 70% of its careful width; bound-only beats drift-only by AIC for all 17; best model bound and t0 for 7, bound, t0 and drift for 10 | Psyche (`decide.fit_conditions`), item `selective` |
| Errors faster than correct answers (medians) for 13 of 17 under speed; slower for 14 of 17 under accuracy | the same data, item `selective` |
| Three observers, 23,848 kept trials, 33 brightnesses in 8 bins: careful bounds 1.89, 1.92, 1.66 against fast bounds 0.83, 0.79, 1.07 | Ratcliff and Rouder (1998), as packaged in rtdists; Psyche's stimulus-coded fit (`compute._fit_rr98`), item `rr98` |
| Mean decision time correct/error: no variability 0.334/0.340 s; drift varies (sd 1.2) 0.297/0.341; start varies (width 0.6 a) 0.308/0.280 | Psyche (`decide.simulate`, 60,000 trials each), item `variability` |
| Accumulators averaged by drift, aligned to the stimulus and to the response | Psyche (`decide.aligned_means`), item `brain` |
| About three quarters of LIP neurons better fitted by steps | Latimer, Yates, Meister, Huk and Pillow (2015) |
| Up to 203 LIP neurons recorded at once | Steinemann et al. (2024) |
| LBA with rates 1.2 and 0.8: the faster accumulator wins 78% | Psyche (`decide.lba_defective`, `lba_simulate`), item `lba` |
| A collapsing bound: skew 1.9 to 1.2, accuracy 83% to 74%, mean time 1.15 s to 0.73 s | Psyche (`decide.simulate_bound`), item `urgency` |
| The integration method recovers a 220 ms stop time to within 4 ms at every delay where 10–90% escape | Psyche (`decide.stop_race`, `ssrt_integration`), item `stop` |
| Confidence (share of the bound) on correct trials 0.67 to 0.74, on errors 0.63 to 0.35, as drift rises from 0.2 to 3.2 | Psyche (`decide.race_confidence`), item `confidence` |
| Two equally good snacks: P(choose left) from 0.26 to 0.70 with gaze advantage; the last item looked at chosen 71% | Psyche (`decide.addm`), item `addm` |
| Test–retest correlation of EZ drift: 0.35 with 20 trials a session, 0.90 with 500 | Psyche (`decide.retest`), item `traits` |
| Perception–brake times about 0.75, 1.25 and 1.5 s; road design 2.5 s | Green (2000); AASHTO stopping sight distance |

## Built in this part

* `explainer/psychology/psyche/decide.py`: Wald's test on Bernoulli data with its bounds, operating characteristic,
  average sample number, a simulator and the exact fixed-sample comparison; the diffusion model's closed forms,
  Navarro and Fuss's first-passage densities with drift variability integrated out, response-time densities with
  t0 variability, conditional mean times, vectorized simulators with every variability and with any time-varying
  bound; maximum-likelihood fits for one condition or several sharing parameters, and EZ diffusion; the linear
  ballistic accumulator; a race of n accumulators held to a fixed accuracy (Hick's law); stimulus- and
  response-aligned averages and a stepping model; the stop-signal race with the integration and mean methods; the
  balance of evidence; the attentional drift-diffusion model; test–retest reliability of fitted drifts. Tested in
  `tests/psychology/test_decide.py`.
* `explainer/psychology/opendata.py` gains the two rtdists datasets (read by `rdata.py`, nothing evaluated).
* The Ledger gains five rows; the Archive two datasets. Hick's law keeps its row from Part 1.
* The course's interactive is the moving dots on you, in fast and careful blocks: your accuracy, your times, and
  your two bounds by EZ diffusion.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| The time of an aimed movement grows linearly with the logarithm of twice the distance over the width of the target | Fitts 1954 | replicated |
| Instructions to be fast or accurate act on the diffusion model's boundary separation | Ratcliff and Rouder 1998 | replicated |
| Errors are faster than correct responses when speed is stressed, and slower when accuracy is stressed | Ratcliff and Rouder 1998 | replicated |
| Single neurons in the lateral intraparietal area accumulate evidence for a choice, ramping to a bound | Roitman and Shadlen 2002 | contested |
| Stopping is a race between independent go and stop processes, from which the stop-signal reaction time can be estimated | Logan and Cowan 1984 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the history the part tells
(Wallis, Wald, Ratcliff), the sequential-sampling tradition (Stone, Laming), the selective-influence studies
described beside the row (Ratcliff, Voss et al.), Shadlen and Newsome's recordings (in the LIP row's original),
Usher and McClelland and Bogacz et al. (models), Vickers, Kiani and Shadlen and Pleskac and Busemeyer (confidence,
described), and the practice and frontier chapters' studies.

## Build it

```bash
python -m videos.psychology.psych25.compute            # every number (a few minutes; fetches the open data once)
python tools/qa_scene.py psych25 Selective             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych25 -q l   # the whole part, silent preview
python tools/build.py psych25                          # 1080p30 with narration
python tools/qa_scene.py psych25 Diffusion --lang zh   # the Chinese edition of one chapter
python tools/make.py psych25                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 25                    # the lab: Wald's test to the diffusion model on open data
python tools/check_ledger.py psych25                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's decision module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Moving dots | The dots on you, slow and fast; Wald, Ratcliff and LIP; the questions; objectives |
| 1 | Two old laws | Hick's law and a race that recovers it; Fitts's law derived from corrections |
| 2 | The speed-accuracy trade-off | 17 people's two operating points; one model's whole curve; why mean times mislead comparisons |
| 3 | The shape of a response time | One person's distribution and an ex-Gaussian fit; same mean, different shapes; quantiles |
| 4 | Wald's test | The SPRT derived and run; half the shots of a fixed test; from shells to seeing |
| 5 | The diffusion model | Four numbers; P(upper) and the mean time derived; the densities computed |
| 6 | Each parameter, a claim | Selective influence; 17 people fitted under four models; three observers at 33 brightnesses; exceptions |
| 7 | Fast errors and slow errors | The data's flip with the instruction; variability in drift and in start |
| 8 | Accumulators in the brain | LIP and the moving dots; averages aligned two ways; ramp or step |
| 9 | Relatives: races, leaks and urgency | The linear ballistic accumulator; leaky competing accumulators; collapsing bounds |
| 10 | Stopping | The stop-signal race derived; the inhibition function; the stop time recovered; independence |
| 11 | Confidence | The balance of evidence; Kiani and Shadlen; the folded X |
| 12 | The Ledger | Fitts's law; speed and the bound; fast and slow errors; LIP ramping; the stop-signal race |
| 13 | In practice: menus, brakes and clinics | Fitts and Hick at the interface; braking distances; slower or more careful |
| 14 | Frontier: values, attention and traits | Gaze and value in the attentional diffusion model; reliability of decision parameters |
| | Recap, problems, and the road ahead | Ten lines; Kant's three objections; payoffs; problems; references; Part 26 |

## Sources

* W. E. Hick, On the rate of gain of information, Quarterly Journal of Experimental Psychology 4 (1952) 11-26; R.
  Hyman, Journal of Experimental Psychology 45 (1953) 188-196; R. W. Proctor and D. W. Schneider, Quarterly Journal
  of Experimental Psychology 71 (2018) 1281-1299.
* P. M. Fitts, Journal of Experimental Psychology 47 (1954) 381-391; P. M. Fitts and J. R. Peterson, Journal of
  Experimental Psychology 67 (1964) 103-112; E. R. F. W. Crossman and P. J. Goodeve, Feedback control of
  hand-movement and Fitts' law (1963; Quarterly Journal of Experimental Psychology 35A (1983) 251-278); I. S.
  MacKenzie, Human-Computer Interaction 7 (1992) 91-139.
* R. G. Pachella, The interpretation of reaction time in information-processing research, in Human Information
  Processing (1974); W. A. Wickelgren, Speed-accuracy tradeoff and information processing dynamics, Acta
  Psychologica 41 (1977) 67-85.
* R. Ratcliff, Group reaction time distributions and an analysis of distribution statistics, Psychological Bulletin
  86 (1979) 446-461; R. D. Luce, Response Times (1986).
* A. Wald, Sequential tests of statistical hypotheses, Annals of Mathematical Statistics 16 (1945) 117-186;
  Sequential Analysis (1947); A. Wald and J. Wolfowitz, Optimum character of the sequential probability ratio test,
  Annals of Mathematical Statistics 19 (1948) 326-339; W. A. Wallis, The Statistical Research Group, 1942-1945,
  Journal of the American Statistical Association 75 (1980) 320-330.
* M. Stone, Models for choice-reaction time, Psychometrika 25 (1960) 251-260; D. R. J. Laming, Information Theory
  of Choice-Reaction Times (1968).
* R. Ratcliff, A theory of memory retrieval, Psychological Review 85 (1978) 59-108; R. Ratcliff and J. N. Rouder,
  Psychological Science 9 (1998) 347-356; R. Ratcliff and G. McKoon, Neural Computation 20 (2008) 873-922; D. J.
  Navarro and I. G. Fuss, Fast and accurate calculations for first-passage times in Wiener diffusion models,
  Journal of Mathematical Psychology 53 (2009) 222-230; S. Blurton, M. Kesselmeier and M. Gondan, Journal of
  Mathematical Psychology 56 (2012) 470-475.
* E.-J. Wagenmakers, R. Ratcliff, P. Gomez and G. McKoon, Journal of Memory and Language 58 (2008) 140-159; A.
  Heathcote and J. Love, Frontiers in Psychology 3 (2012) 292; E.-J. Wagenmakers, H. L. J. van der Maas and R. P. P.
  P. Grasman, An EZ-diffusion model for response time and accuracy, Psychonomic Bulletin & Review 14 (2007) 3-22.
* A. Voss, K. Rothermund and J. Voss, Memory & Cognition 32 (2004) 1206-1220; B. Rae, A. Heathcote, C. Donkin, L.
  Averell and S. Brown, Journal of Experimental Psychology: Learning, Memory, and Cognition 40 (2014) 1226-1243; G.
  Dutilh and colleagues, Psychonomic Bulletin & Review 26 (2019) 1051-1069.
* M. N. Shadlen and W. T. Newsome, Motion perception: seeing and deciding, PNAS 93 (1996) 628-633; Neural basis of
  a perceptual decision in the parietal cortex (area LIP) of the rhesus monkey, Journal of Neurophysiology 86
  (2001) 1916-1936; J. D. Roitman and M. N. Shadlen, Journal of Neuroscience 22 (2002) 9475-9489; K. W. Latimer
  and colleagues, Science 349 (2015) 184-187; M. N. Shadlen and colleagues, Science 351 (2016) 1406; N. A.
  Steinemann and colleagues, eLife 12 (2024) RP90859.
* S. D. Brown and A. Heathcote, The simplest complete model of choice response time: linear ballistic
  accumulation, Cognitive Psychology 57 (2008) 153-178; M. Usher and J. L. McClelland, Psychological Review 108
  (2001) 550-592; R. Bogacz, E. Brown, J. Moehlis, P. Holmes and J. D. Cohen, The physics of optimal decision
  making, Psychological Review 113 (2006) 700-765; P. Cisek, G. A. Puskas and S. El-Murr, Journal of Neuroscience
  29 (2009) 11560-11571; J. Drugowitsch and colleagues, Journal of Neuroscience 32 (2012) 3612-3628; G. E. Hawkins,
  B. U. Forstmann, E.-J. Wagenmakers, R. Ratcliff and S. D. Brown, Journal of Neuroscience 35 (2015) 2476-2484.
* G. D. Logan and W. B. Cowan, Psychological Review 91 (1984) 295-327; F. Verbruggen and colleagues, eLife 8 (2019)
  e46323; P. G. Bissett, H. M. Jones, R. A. Poldrack and G. D. Logan, Science Advances 7 (2021) eabf4355.
* D. Vickers, Decision Processes in Visual Perception (1979); R. Kiani and M. N. Shadlen, Science 324 (2009)
  759-764; T. J. Pleskac and J. R. Busemeyer, Psychological Review 117 (2010) 864-901; J. I. Sanders, B. Hangya and
  A. Kepecs, Neuron 90 (2016) 499-506; B. Maniscalco and H. Lau, Consciousness and Cognition 21 (2012) 422-430.
* M. Green, How long does it take to stop?, Transportation Human Factors 2 (2000) 195-216; R. Ratcliff, A. Thapar
  and G. McKoon, Psychology and Aging 16 (2001) 323-341.
* I. Krajbich, C. Armel and A. Rangel, Nature Neuroscience 13 (2010) 1292-1298; C. Hedge, G. Powell and P. Sumner,
  The reliability paradox, Behavior Research Methods 50 (2018) 1166-1186; V. Lerche and A. Voss, Psychological
  Research 81 (2017) 629-652.
* B. U. Forstmann, R. Ratcliff and E.-J. Wagenmakers, Sequential sampling models in cognitive neuroscience, Annual
  Review of Psychology 67 (2016) 641-666.

## Problems and solutions

**1. No drift.** With v = 0 the equation is P'' = 0 with P(0) = 0 and P(a) = 1, so P(z) = z/a. In the general
formula, write k = 2v/s²: (1 − e^{−kz})/(1 − e^{−ka}) ≈ (kz)/(ka) = z/a to first order in k.

**2. The mean time with an unbiased start.** With z = a/2 and unit noise, P(upper) = (1 − e^{−va})/(1 − e^{−2va})
= 1/(1 + e^{−va}). Then a P − a/2 = (a/2)(1 − e^{−va})/(1 + e^{−va}) = (a/2) tanh(va/2), and dividing by v gives
E[T] = (a/2v) tanh(va/2). As v → 0, tanh(va/2) ≈ va/2 and E[T] → a²/4, which is z(a − z) at z = a/2.

**3. The shortest run of Wald's test.** A hit adds log(0.7/0.5) = 0.336 and a miss adds log(0.3/0.5) = −0.511; the
bounds are ±2.944. Accepting p = 0.7 needs the sum to reach 2.944, which takes at least nine hits in a row
(8 × 0.336 = 2.69 is short). Accepting p = 0.5 takes at least six misses (5 × 0.511 = 2.55 is short; 6 × 0.511 =
3.07).

**4. Corrections.** After k corrections the remaining distance is D r^k, and the movement ends when it is below W/2:
r^k < W/(2D) = 2^{−5}, so k > 5/log₂(1/r). With r = 0.25, k > 2.5: three corrections. With r = 0.5, k > 5: six.
Coarser corrections (smaller r) need fewer of them, and each bit costs 1/log₂(1/r) corrections.

**5. Two estimates of the stop time.** The integration method sets SSRT = F⁻¹(p) − SSD, with p the share of stop
trials that escape. When p = 0.5 the quantile is the go distribution's median, and for a symmetric distribution the
median is the mean, so SSRT = mean go time − SSD; averaged over the delays a staircase visits, mean go time minus
mean delay. With a skewed go distribution, or p far from a half, the two differ, which is why the integration method
is preferred.

**6. EZ on the open data.** For each person and block, take the proportion correct, and the mean and variance of
correct times, and apply `decide.ez` (with s = 1). EZ assumes an unbiased start and no variability between trials;
it puts the bound lower under speed for all 17 people, at a median 59% of the careful bound (the full fits: 16 of
17, at 70%). Three summary statistics recover the main finding; the ratios differ because EZ assumes no variability
between trials and uses correct responses only.

**7. ⋆ A collapsing bound or variable drift?** Both can make errors slow and both shorten tails relative to some
alternatives, so use the joint shape of correct and error distributions across difficulty. A collapsing bound
predicts that the slowest responses are the least accurate at every difficulty and that the right tail's shape is
nearly the same across difficulties (it is cut by the bound); variability in drift predicts slow errors that grow
with difficulty and tails that lengthen for hard conditions. A design: many difficulty levels, randomly mixed, with
enough trials per level for conditional accuracy functions (accuracy by RT quantile); fit both models and compare
them on held-out quantiles, as Hawkins et al. (2015) did.

## Open checks

Before the narrated master:

* Hick's lamps and Fitts's tapping are described from the papers' abstracts and standard summaries; Fitts's "16
  men" is from the 1954 paper's method and should be rechecked against it.
* Green's braking times (0.75, 1.25, 1.5 s) are as usually quoted from his 2000 review; the 2.5 s design value is
  the AASHTO stopping-sight-distance assumption.
* The story of 1943 (the Navy's question, Friedman and Wallis, Wald) follows Wallis (1980).
* The LIP averages, the stepping trials, the urgency bounds, the confidence race, the attentional model and the
  reliability simulation are Psyche's, and say so on screen; no neuron's data are shown.
* The rtdists files (GPL ≥ 3) are fetched on first use, checked by SHA-256 and never committed.
