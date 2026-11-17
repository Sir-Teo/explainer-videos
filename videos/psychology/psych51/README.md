# Psychology, Built: Part 51, Human Factors

In the 1940s pilots of some bomber types kept retracting the landing gear after landing when they meant to raise the
flaps. In 1947 Paul Fitts and Richard Jones collected 460 reports of "pilot error" and found the same few again and
again: the two levers sat side by side and felt the same. Alphonse Chapanis gave one a wheel-shaped knob and the
other a flap-shaped one, and the errors went away. Human factors begins with the idea that error is designed in and
can be designed out; this part follows it into control rooms, screening halls, automated cockpits, operating
theatres and night shifts. Act XII, psychology at work, begins here.

The viewer watches Mackworth's clock and predicts four numbers. Then compatibility and coding, Fitts's and Hick's
laws fitted; slips, lapses, mistakes and violations, and Rasmussen's ladder; Three Mile Island; multiple resources
and NASA-TLX; a two-hour watch analysed by signal detection half hour by half hour; the prevalence effect and a
gorilla in a lung scan; situation awareness and how it is measured; levels of automation, Bainbridge's ironies as a
model, mode confusion and Air France 447; calibrated trust, an alarm as a criterion and alarm fatigue; the Swiss
cheese model with correlated holes, the surgical checklist, Tenerife and crew resource management; and fatigue
against blood alcohol.

## Where the numbers come from

| What | Source |
|---|---|
| Fitts's law: 400 simulated movements (distances 64 to 512, widths 8 to 64), MT = 0.05 + 0.15 log2(D/W + 1) s with lognormal noise; fitted a = 0.05, b = 0.15 s per bit, r = 0.95 | Psyche (`work.fitts_trials`), item `fitts` |
| Hick-Hyman: RT = 0.2 + 0.15 log2(N + 1) s, plus 0.12 log2(N + 1) s for an incompatible mapping (illustrative parameters) | Psyche (`work.hick_rt`), item `hick` |
| NASA-TLX: ratings 70, 20, 60, 40, 65, 50 with weights 4, 0, 3, 2, 4, 2; weighted score 60, raw mean 51 | Psyche (`work.nasa_tlx`), item `tlx` |
| A two-hour watch, 60 simulated watchers: 20 events a minute, 1.2% signals; d' falls linearly from 2.6 by 0.5 over the watch and c rises from 0.6 by 0.6; hits by half hour 0.73, 0.67, 0.57, 0.49; estimated d' 2.56 to 2.15, c 0.65 to 1.11 | Psyche (`work.vigilance`), item `vigilance` |
| One watcher, the same watch: hits 0.81, 0.50, 0.56, 0.50 | Psyche (`work.vigilance`), item `onewatch` |
| The prevalence effect, d' = 2: misses at prevalence 50%, 10%, 2%, 1% are 0.16, 0.54, 0.83, 0.90 for the accuracy-maximizing criterion and 0.16, 0.27, 0.37, 0.42 for an observer who shifts 35% of the way on the log-beta scale | Psyche (`work.prevalence`, `prevalence_partial`), item `prevalence` |
| The ironies of automation as a model: median takeover 2.5(1 + 0.35 log10 MTBF) s, lognormal (log-SD 0.45); at reliability 0.9, 0.99, 0.999, 0.9999 the median is 3.4, 4.3, 5.1, 6.0 s, the share within 7 s 0.95, 0.86, 0.76, 0.62, and failures per demand 5.3e-3, 1.4e-3, 2.4e-4, 3.8e-5 (the growth of takeover time is an assumption chosen to show the shape) | Psyche (`work.takeover`), item `takeover` |
| An alarm on a noisy sensor: events 1% of readings, d' = 2.5; at a threshold of 1 SD, 93% of events alarmed and 5.6% of alarms real; with responses matched to the alarm's reliability, the best threshold is 2.7 SD and 23% of events are answered | Psyche (`work.alarm`), item `alarm` |
| The Swiss cheese model: four layers, each open 10% of the time, a Gaussian copula with correlation 0, 0.2, 0.4, 0.6; 400,000 simulated days; accident rates 0.9e-4, 1.3e-3, 5.2e-3, 1.4e-2 | Psyche (`work.swiss_cheese`), item `cheese` |
| Hours awake against blood alcohol: the line through Dawson and Reid's two reported points (17 h like 0.05%, 24 h like 0.10%) | Dawson and Reid (1997) as reported, item `fatigue` |
| The shares of awareness errors by level (about 76%, 20% and 3%) | Jones and Endsley (1996) as usually quoted; see Open checks |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/work.py`: Fitts's and the Hick-Hyman laws with a compatibility cost; a vigilance
  watch analysed by signal detection block by block; the prevalence effect, optimal and partial; NASA-TLX; takeover
  after automation; alarm thresholds with positive predictive value and probability-matching operators; the Swiss
  cheese model with correlated holes; hours awake against blood-alcohol equivalents. Tested in
  `tests/psychology/test_work.py`.
* The Ledger gains four rows; the deferred rows for the vigilance decrement (Parts 12 and 18) are resolved.
* The course's interactive: Mackworth's clock for ninety seconds, with common and rare double jumps; the reader's
  hits, false alarms, d' and c.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| In a long watch for rare signals, detection falls within the first half hour and keeps falling. | Mackworth 1948 | replicated |
| Introducing a short surgical safety checklist reduces deaths and complications after surgery. | Haynes and colleagues 2009 | contested |
| People who monitor reliable automation detect its rare failures less well than people who do the task themselves, and less well the more reliable it has been. | Parasuraman, Molloy and Singh 1993 | replicated |
| Staying awake for 17 to 24 hours impairs performance about as much as a blood-alcohol concentration of 0.05% to 0.10%. | Dawson and Reid 1997 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Fitts and Jones; Fitts; Bainbridge;
Endsley; Jones and Endsley; Hart and Staveland; Reason.

## Build it

```bash
python -m videos.psychology.psych51.compute            # every number (seconds)
python tools/qa_scene.py psych51 Vigilance             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych51 -q l   # the whole part, silent preview
python tools/build.py psych51                          # 1080p30 with narration
python tools/qa_scene.py psych51 Automation --lang zh  # the Chinese edition of one chapter
python tools/make.py psych51                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 51                    # the lab: Fitts, the watch, the alarm, the cheese
python tools/check_ledger.py psych51                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's work module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Two levers that felt the same | Fitts and Jones's pilot errors; Chapanis's knobs; the question; objectives |
| 1 | On you: watch the clock, and four numbers | Mackworth's clock; four predictions |
| 2 | Error designed in | Compatibility and stereotypes; coding; Fitts's law fitted; Hick's law |
| 3 | Slips, lapses and mistakes | Four kinds of error; skills, rules and knowledge; the old view and the new |
| 4 | A light that told the wrong story | Three Mile Island; what changed |
| 5 | Attention at work | Multiple resources; measuring workload |
| 6 | The watch | Two hours at the clock; sensitivity or criterion; one watcher's record |
| 7 | Rare targets | The prevalence effect; a gorilla in the lungs; what helps |
| 8 | Situation awareness | Three levels; where awareness fails; measuring it |
| 9 | The ironies of automation | Levels and stages; Bainbridge; the irony as a model; mode confusion; Air France 447 |
| 10 | Trust and alarms | Calibrated trust; an alarm is a criterion; better alarms; alarm fatigue on the ward |
| 11 | Systems, checklists and crews | The Swiss cheese model; the checklist; Tenerife; crew resource management |
| 12 | Fatigue as a measured risk | Hours awake against blood alcohol; the clock; managing fatigue |
| 13 | The Ledger | Four rows; what they have in common |
| 14 | In practice: a takeover request, designed | Where human factors works; the brief; four steps; the safety case |
| 15 | Frontier: supervising learning machines | What is new; decision aids in high-stakes work; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 52 |

## Sources

* P. M. Fitts and R. E. Jones, *Analysis of factors contributing to 460 "pilot-error" experiences in operating
  aircraft controls*, Memorandum Report TSEAA-694-12, Aero Medical Laboratory, Wright-Patterson Air Force Base (1947);
  A. Chapanis, W. R. Garner and C. T. Morgan, *Applied Experimental Psychology* (Wiley, 1949).
* P. M. Fitts, The information capacity of the human motor system in controlling the amplitude of movement, *Journal
  of Experimental Psychology* 47 (1954) 381-391; W. E. Hick, On the rate of gain of information, *Quarterly Journal of
  Experimental Psychology* 4 (1952) 11-26; R. Hyman, Stimulus information as a determinant of reaction time, *Journal
  of Experimental Psychology* 45 (1953) 188-196.
* D. A. Norman, Categorization of action slips, *Psychological Review* 88 (1981) 1-15; J. Reason, *Human Error*
  (Cambridge University Press, 1990); J. Rasmussen, Skills, rules, and knowledge, *IEEE Transactions on Systems, Man,
  and Cybernetics* 13 (1983) 257-266; S. Dekker, *The Field Guide to Understanding Human Error* (Ashgate, 2006).
* J. G. Kemeny et al., *Report of the President's Commission on the Accident at Three Mile Island* (1979).
* C. D. Wickens, Multiple resources and performance prediction, *Theoretical Issues in Ergonomics Science* 3 (2002)
  159-177; S. G. Hart and L. E. Staveland, Development of NASA-TLX, in P. A. Hancock and N. Meshkati (eds), *Human
  Mental Workload* (North-Holland, 1988) 139-183.
* N. H. Mackworth (1948); J. E. See et al. (1995); J. S. Warm, R. Parasuraman and G. Matthews (2008).
* J. M. Wolfe, T. S. Horowitz and N. M. Kenner, Rare items often missed in visual searches, *Nature* 435 (2005)
  439-440; T. Drew, M. L.-H. Vo and J. M. Wolfe, The invisible gorilla strikes again, *Psychological Science* 24
  (2013) 1848-1853.
* M. R. Endsley, Toward a theory of situation awareness in dynamic systems, *Human Factors* 37 (1995) 32-64; D. G. Jones
  and M. R. Endsley, Sources of situation awareness errors in aviation, *Aviation, Space, and Environmental Medicine*
  67 (1996) 507-512.
* T. B. Sheridan and W. L. Verplank, *Human and Computer Control of Undersea Teleoperators* (MIT, 1978); R.
  Parasuraman, T. B. Sheridan and C. D. Wickens, A model for types and levels of human interaction with automation,
  *IEEE Transactions on Systems, Man, and Cybernetics A* 30 (2000) 286-297; SAE J3016, *Taxonomy and Definitions for
  Terms Related to Driving Automation Systems*; L. Bainbridge, Ironies of automation, *Automatica* 19 (1983) 775-779;
  E. L. Wiener, *Human Factors of Advanced Technology ("Glass Cockpit") Transport Aircraft*, NASA Contractor Report
  177528 (1989); BEA, *Final Report on the accident on 1st June 2009 to the Airbus A330-203 registered F-GZCP* (2012).
* R. Parasuraman, R. Molloy and I. L. Singh (1993); R. Parasuraman and V. Riley, Humans and automation: use, misuse,
  disuse, abuse, *Human Factors* 39 (1997) 230-253; J. D. Lee and K. A. See, Trust in automation: designing for
  appropriate reliance, *Human Factors* 46 (2004) 50-80; R. Parasuraman and D. H. Manzey (2010); J. P. Bliss, R. D.
  Gilson and J. E. Deaton, Human probability matching behaviour in response to alarms of varying reliability,
  *Ergonomics* 38 (1995) 2300-2312; R. D. Sorkin, B. H. Kantowitz and S. C. Kantowitz, Likelihood alarm displays,
  *Human Factors* 30 (1988) 445-459; The Joint Commission, Sentinel Event Alert 50: Medical device alarm safety in
  hospitals (2013).
* J. Reason, *Managing the Risks of Organizational Accidents* (Ashgate, 1997); A. B. Haynes et al. (2009); D. R.
  Urbach et al. (2014); A. S. Haugen et al. (2015); A. Gawande, *The Checklist Manifesto* (2009).
* Spanish civil aviation authority and Netherlands Aviation Safety Board reports on the Tenerife collision (1978);
  J. K. Lauber, Resource management on the flight deck, NASA Conference Publication 2120 (1980); R. L. Helmreich,
  A. C. Merritt and J. A. Wilhelm, The evolution of crew resource management training in commercial aviation,
  *International Journal of Aviation Psychology* 9 (1999) 19-32.
* D. Dawson and K. Reid (1997); A. M. Williamson and A.-M. Feyer (2000); C. P. Landrigan et al., Effect of reducing
  interns' work hours on serious medical errors in intensive care units, *New England Journal of Medicine* 351 (2004)
  1838-1848.

## Problems and solutions

1. **Fitts's law.** Fitts's law with $a$ = 0.1 s and $b$ = 0.15 s per bit: predict the time to reach a 2 cm target 16 cm away ($ID = \log_2(2D/W)$).

   *Solution.* ID = log2(2 x 16 / 2) = 4 bits; MT = 0.1 + 0.15 x 4 = 0.70 s.
2. **A watch.** A watch: 40 signals, 28 hits; 2,000 non-signals, 30 false alarms. Find $d'$ and $c$.

   *Solution.* H = 28/40 = 0.70, F = 30/2,000 = 0.015; z(H) = 0.524, z(F) = -2.170; d' = 2.69, c = -(0.524 -
   2.170)/2 = 0.82: a conservative watcher.
3. **Real alarms.** Targets in 1 bag in 200; hit rate 0.9, false-alarm rate 0.05. What share of alarms are real?

   *Solution.* PPV = 0.005 x 0.9 / (0.005 x 0.9 + 0.995 x 0.05) = 0.0045/0.0543 = 0.083: about one alarm in
   twelve is real.
4. **Independent layers.** Four independent layers, each failing one time in 20: the chance of an accident?

   *Solution.* 0.05^4 = 6.25 x 10^-6, about one in 160,000; if the layers share causes, much more.
5. **NASA-TLX.** NASA-TLX ratings 70, 40, 60, 50, 30, 80 with weights 5, 1, 3, 2, 0, 4: the weighted score?

   *Solution.* (70 x 5 + 40 x 1 + 60 x 3 + 50 x 2 + 30 x 0 + 80 x 4)/15 = 990/15 = 66.
6. **Takeovers in time.** A level-3 car hands over with a 7 s budget; takeover times are lognormal with median 5 s and log-SD 0.45. What share finish in time?

   *Solution.* P(T < 7) = Phi(ln(7/5)/0.45) = Phi(0.75) = 0.77.
7. ★ **A safety case for dose entry.** Write the human-factors section of a safety case for a medication pump's dose entry: tasks, likely slips, lapses and mistakes, the tests, and the residual risk.

   *Solution.* Tasks: select the drug, enter the dose and rate, confirm, start. Likely errors:
   slips (a decimal point or an extra zero, the wrong drug in a look-alike list), lapses (a step skipped after an
   interruption), mistakes (units confused, mg against micrograms, or a wrong rule for a weight-based dose). Controls:
   a drug library with hard and soft limits, units always shown, no trailing zeros, a confirmation that restates the
   dose in words and against the usual range, and a second check for high-risk drugs. Evidence: a usability test with
   nurses on the critical tasks, with error rates and their causes, under realistic interruption. Residual risk: what
   errors remain and at what rate, why that is acceptable, and how field reports will be read for design.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
the B-17 gear and flap confusion and which aircraft types it involved; Fitts and Jones's 460 reports and the report's
number; Chapanis's knobs and the date; Three Mile Island's sequence (the relief valve, the indicator, the
pressurizer level, the number of alarms in the first minutes) and the changes after it; Wickens's model as described;
NASA-TLX's 15 pairwise comparisons; Mackworth's clock (one step a second, double jumps, two-hour watches, RAF
observers); See et al.'s conclusions; Warm, Parasuraman and Matthews (2008); Wolfe, Horowitz and Kenner (2005); Drew,
Vo and Wolfe's gorilla (its size, the share of radiologists who missed it, the eye tracking); Endsley's three levels;
Jones and Endsley's shares by level; SAGAT, SPAM and SART as described; Sheridan and Verplank's ten levels and
Parasuraman, Sheridan and Wickens's four stages; SAE J3016's levels; Bainbridge (1983); the Strasbourg accident of
1992 (the crew's intent and the two modes); Wiener's surveys and the "what is it doing now" question; the Air France
447 sequence, the stall warning's behaviour and the death toll; Lee and See (2004); Bliss's probability matching;
Sorkin's likelihood alarms; the alarm counts and false-alarm shares on intensive-care monitors; the Joint
Commission's 2013 alert; the 1935 bomber crash and the origin of aviation checklists; Haynes et al.'s 19 items,
eight hospitals and the death and complication rates; Urbach et al.'s Ontario result; Haugen et al. (2015); the
Tenerife sequence and toll; NASA's late-1970s findings on crew failures and the 1979 workshop; Dawson and Reid's
task, the 28 hours and the equivalences; Williamson and Feyer (2000); the timing of sleep-related crashes; Landrigan
et al. (2004) and the later duty-hour trials; and every page range in Sources.
