# Psychology, Built: Part 18, Attention

Half of the observers counting basketball passes never see a person in a gorilla suit walk through the game. Far more
reaches the senses than reaches report, and attention is what decides. This part follows the idea from the first
box-and-arrow diagram of a mind, Broadbent's filter of 1958, to a model in which attention is one multiplication placed
before one division, and asks what it costs radiologists, drivers and anyone watching an alarm.

The gorilla and the flicker paradigm; Cherry's shadowing, the split span and Broadbent's filter; the own-name effect,
Treisman's attenuation (run on Psyche as signal and noise against word thresholds), late selection and Lavie's load;
Posner's cueing with benefits and costs, endogenous and exogenous cues and inhibition of return; feature and
conjunction search with set-size functions, feature integration theory and illusory conjunctions, guided search run
on Psyche, a computed saliency map with a scan path, and an unguided T-among-Ls search with its two-to-one slopes;
change blindness fitted on Psyche to Rensink's means, attentional set and inattentional blindness, radiologists and
the gorilla; the attentional blink as a two-stage model and the psychological refractory period as a central
bottleneck; the Stroop effect as a two-pathway diffusion with its asymmetry and delta plot, flankers, conflict
monitoring and the sequence effect, task switching; Moran and Desimone's V4 neurons, biased competition, and Reynolds
and Heeger's normalization model of attention derived, with contrast gain and response gain from stimulus and
attention-field sizes; Bundesen's theory of visual attention as a race; the vigilance decrement and the prevalence
effect refitted; phones while driving and media multitasking. The practice chapter is professional search, alarm
fatigue, driving law and attention metrics in advertising; the frontier is whether attention is one thing,
rhythmic sampling, and attention in transformers.

## Where the numbers come from

| What | Source |
|---|---|
| The gorilla: 192 observers, 46% missed the unexpected visitor (gorilla or umbrella woman); noticing doubled when counting the black team | Simons and Chabris (1999), from secondary summaries |
| The flicker paradigm: 240 ms images, 80 ms blanks, 48 scenes, ten observers; 17.1 alternations (10.9 s) for marginal and 7.3 (4.7 s) for central changes; 1.4 (0.9 s) without blanks | Rensink, O'Regan and Clark (1997), the paper read in full |
| Cherry's shadowing; Broadbent's split span and filter | Cherry (1953), Broadbent (1958), from memory and reviews |
| About a third hear their own name in the ignored ear; a word list repeated 35 times goes unrecognized | Moray (1959); Wood and Cowan (1995), from secondary summaries |
| Treisman's ear-switching story; Deutsch and Deutsch | from memory and reviews |
| The attenuator: P(heard) for the own name (threshold 0.55), a predicted word (0.7) and an ordinary word (1.1) at attenuation 0.4, noise 0.25 | Psyche (`attention.dichotic`), item `dichotic` |
| Flanker interference against load: capacity 4, 60 ms when all is spare | Psyche (`attention.flanker_interference`), item `load`; Lavie (1995) for the pattern |
| Posner cueing: valid, neutral and invalid RTs at a 400 ms cue; endogenous and exogenous cue effects with inhibition of return | Psyche (`attention.cue_effect`, `attention.posner_rts`), item `cueing`; Posner (1980) and Posner and Cohen (1984) for the pattern, no numbers quoted |
| Set-size functions for feature, conjunction and T-among-L searches (4 to 32 items, 400 trials a point): slopes 0/3, 12/35 and 23/47 ms an item | Psyche (`attention.search_slopes`), item `search` |
| Conjunction slopes of about 29 ms an item (present) and 67 (absent) | Treisman and Gelade (1980), Experiment 1, as reproduced in a lecture; the exact values are to be checked against the paper |
| A saliency map of a field of bars and its first fixations | Psyche (`attention.saliency_map`, `attention.scan_path`), item `saliency`; Itti, Koch and Niebur (1998) for the method |
| Change blindness fitted: 1.2 items sampled a cycle, interesting items 4 times as likely; 8.1 and 18.5 alternations against 7.3 and 17.1 | Psyche (`attention.flicker`), item `flicker`, fitted on a grid to Rensink's means |
| Noticing against similarity and load | Psyche (`attention.notice_probability`), item `notice`; Most et al. (2001) for the pattern |
| 24 radiologists, a gorilla 48 times a nodule, 20 did not report it; most looked at it | Drew, Võ and Wolfe (2013), from the abstract and press coverage |
| The attentional blink from 180 to 450 ms after T1 | Raymond, Shapiro and Arnell (1992), from the abstract; the curve is Psyche's (`attention.attentional_blink`), item `blink` |
| The PRP: RT2 against SOA with gamma stages of 100, 150 and 80 ms | Psyche (`attention.prp`), item `prp`; Pashler (1994) for the theory |
| Stroop 1935: about 47 s longer per 100-item card, 74% more | Stroop (1935), via MacLeod (1991) and secondary summaries |
| Psyche's Stroop: congruent 465 ms, neutral 545, incongruent 754; reading 487, 503, 524; the delta plot; the sequence effect (270 ms after congruent, 79 after incongruent) | Psyche (`attention.stroop`, `attention.stroop_sequence`), item `stroop` |
| Task switching against preparation | Psyche (`attention.switch_cost`), item `switch`; Rogers and Monsell (1995) for the pattern, no numbers quoted |
| Moran and Desimone's two stimuli in a V4 field | described; the bars are a schematic |
| Contrast gain (c50 × 0.71, Rmax × 1.00) and response gain (Rmax × 1.47, c50 × 0.86) | Psyche (`attention.normalization_crf`, `attention.gain_type`), item `normalize`; Reynolds and Heeger (2009) for the model, Herrmann et al. (2010) for the test |
| Whole report against exposure: C = 30 items a second, t0 = 20 ms, K = 4 | Psyche (`attention.tva_whole_report`), item `tva`; Bundesen (1990) for the theory |
| A two-hour watch: d′ from 2.6 to 1.7, a rising criterion | Psyche (`attention.vigilance`), item `vigilance`; Mackworth (1948) for the pattern |
| Misses of 11%, 25% and 52% at prevalences of 50%, 10% and 1%; refitted with d′ = 2.48 and a criterion moved 69% of the ideal way (10.7%, 26.3%, 51.2%) | Wolfe, Horowitz and Kenner (2005), as registered for Part 12; the fit is Psyche's, item `prevalence` |
| 48 undergraduates; red-light misses more than doubled during a phone call; handheld equal to hands-free; radio and a book on tape no reliable effect | Strayer and Johnston (2001), the paper read in full |
| Media multitasking: 14 replication tests, 5 in the predicted direction; a meta-analysis of 39 tests from 12 studies, d = 0.17, near zero after bias correction | Wiradhany and Nieuwenstein (2017), from the abstract and later citations |
| Rhythmic sampling at about 4 Hz | Landau and Fries (2012), from memory; the curves are a schematic |
| Tolman's shortcut, Moran and Desimone's bars, the rhythm curves | schematics, labelled on screen as not data |

## Built in this part

* `explainer/psychology/psyche/attention.py`: the dichotic attenuator and Broadbent's filter; load as spare capacity;
  cue effects for endogenous and exogenous cues with inhibition of return; search displays, item saliency, guided
  search with a quitting threshold and set-size functions; a centre-surround saliency map with a winner-take-all scan
  path; the prevalence effect as a criterion shift; the flicker paradigm; the attentional blink as a two-stage model;
  the PRP under a central bottleneck; a diffusion simulator, the Stroop task as two pathways, conflict monitoring and
  delta plots; task-switching cost; the normalization model of attention with a gain-type fit; Bundesen's whole
  report; a vigilance watch; noticing as a function of similarity. Tested in `tests/psychology/test_attention.py`
  against closed forms (the binomial for whole report, the diffusion's accuracy and mean time) and the patterns each
  model is built to show.
* The Battery's tasks 3 (Stroop) and 4 (visual search) now run on Psyche.
* The Ledger gains six rows, one of them deferred from Part 16; the Archive twenty-five datasets.
* The course's interactive is a visual search the reader does: feature and conjunction searches at four set sizes,
  with the reader's own set-size functions and slopes.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A stimulus seen often without consequence is later learned slowly (deferred from Part 16) | Lubow and Moore 1959 | replicated |
| Naming the ink of a conflicting colour word is slower | Stroop 1935 | replicated |
| People busy with a task often miss an unexpected, visible object | Simons and Chabris 1999 | replicated |
| A cue speeds responses at its location and slows them elsewhere | Posner 1980 | replicated |
| A second target 200 to 500 ms after a first is often missed | Raymond, Shapiro and Arnell 1992 | replicated |
| Heavy media multitaskers are worse at filtering distraction | Ophir, Nass and Wagner 2009 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Anderson, Laurent and Yantis (value-driven capture), Awh et al. (a review), Rensink et al. (change blindness,
fitted by Psyche), Cherry, Broadbent, Moray, Treisman, Deutsch and Deutsch (history), Lavie (with its
critics), Treisman and Gelade (with its slopes), Wolfe's guided search and Itti and Koch (models run on Psyche), Wolfe
et al. (2005; its row is in Part 12), Pashler (a model), Eriksen and Eriksen, Botvinick et al. (a model), Rogers and
Monsell (a pattern with Psyche's numbers), Moran and Desimone (schematic), Reynolds and Heeger (a model),
Bundesen (a model), Mackworth (vigilance's row is due in Part 51), and Strayer and Johnston (driving returns in Part
51, without a promised row).

## Build it

```bash
python -m videos.psychology.psych18.compute            # every number (a minute or two), into .cache/psych18/
python tools/qa_scene.py psych18 Guidance              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych18 -q l   # the whole part, silent preview
python tools/build.py psych18                          # 1080p30 with narration
python tools/qa_scene.py psych18 Neurons --lang zh     # the Chinese edition of one chapter
python tools/make.py psych18                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 18                    # the lab: filters, cueing, search, time, Stroop, gain
python tools/check_ledger.py psych18                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's attention module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The gorilla nobody saw | The gorilla; the flicker paradigm with Rensink's times; the questions; objectives |
| 1 | The cocktail party and the filter | Cherry's shadowing; the split span; Broadbent's filter diagram |
| 2 | Early or late? | The own name; Treisman's attenuator on Psyche; late selection; Lavie's load |
| 3 | A spotlight that moves without the eyes | Posner's task; benefits and costs; two kinds of cue and inhibition of return |
| 4 | Searching | On you: feature and conjunction displays; set-size functions |
| 5 | Features, binding and guidance | Feature integration; guided search on Psyche; a saliency map; selection history; a T among Ls |
| 6 | Seeing without attention | Change blindness fitted; attentional set; radiologists and the gorilla |
| 7 | Attention in time | The attentional blink; the psychological refractory period |
| 8 | Control and conflict | Stroop on you and as a diffusion; flankers and conflict monitoring; task switching |
| 9 | What attention does to a neuron | V4 and biased competition; the normalization model derived; contrast and response gain |
| 10 | Capacity as a race | Bundesen's equation; whole report |
| 11 | Vigilance, and rare targets | Mackworth's clock revisited; the prevalence effect refitted |
| 12 | Doing two things at once | Phones and driving; media multitasking and its replications |
| 13 | The Ledger | Latent inhibition; Stroop; inattentional blindness; cueing; the blink; media multitasking |
| 14 | In practice: alarms, radiology, roads, screens | Professional search; alarm fatigue; driving law; viewability |
| 15 | Frontier: is attention one thing? | What is solid and argued; rhythmic sampling; attention in transformers |
| | Recap, problems, and the road ahead | Ten lines; the first two objections; payoffs; problems; references; Part 19 |

## Sources

**Books.** H. Pashler, *The Psychology of Attention* (MIT Press, 1998). D. J. Simons and C. F. Chabris, *The Invisible
Gorilla* (Crown, 2010). D. E. Broadbent, *Perception and Communication* (Pergamon, 1958).

**Papers.** D. J. Simons and C. F. Chabris, Gorillas in our midst, *Perception* 28 (1999) 1059–1074. R. A. Rensink, J.
K. O'Regan and J. J. Clark, To see or not to see, *Psychol. Sci.* 8 (1997) 368–373. E. C. Cherry, Some experiments on
the recognition of speech, with one and with two ears, *J. Acoust. Soc. Am.* 25 (1953) 975–979. N. Moray, Attention in
dichotic listening, *Q. J. Exp. Psychol.* 11 (1959) 56–60. N. L. Wood and N. Cowan, The cocktail party phenomenon
revisited, *J. Exp. Psychol. Learn. Mem. Cogn.* 21 (1995) 255–260. A. M. Treisman, Contextual cues in selective
listening, *Q. J. Exp. Psychol.* 12 (1960) 242–248. J. A. Deutsch and D. Deutsch, Attention: some theoretical
considerations, *Psychol. Rev.* 70 (1963) 80–90. N. Lavie, Perceptual load as a necessary condition for selective
attention, *J. Exp. Psychol. Hum. Percept. Perform.* 21 (1995) 451–468. M. I. Posner, Orienting of attention, *Q. J.
Exp. Psychol.* 32 (1980) 3–25. M. I. Posner and Y. Cohen, Components of visual orienting, *Attention and Performance
X* (1984) 531–556. A. M. Treisman and G. Gelade, A feature-integration theory of attention, *Cogn. Psychol.* 12 (1980)
97–136. A. Treisman and H. Schmidt, Illusory conjunctions in the perception of objects, *Cogn. Psychol.* 14 (1982)
107–141. J. M. Wolfe, K. R. Cave and S. L. Franzel, Guided search, *J. Exp. Psychol. Hum. Percept. Perform.* 15 (1989)
419–433. J. M. Wolfe, Guided Search 6.0, *Psychon. Bull. Rev.* 28 (2021) 1060–1092. L. Itti, C. Koch and E. Niebur, A
model of saliency-based visual attention, *IEEE Trans. Pattern Anal. Mach. Intell.* 20 (1998) 1254–1259. S. B. Most et
al., How not to be seen, *Psychol. Sci.* 12 (2001) 9–17. T. Drew, M. L.-H. Võ and J. M. Wolfe, The invisible gorilla
strikes again, *Psychol. Sci.* 24 (2013) 1848–1853. J. E. Raymond, K. L. Shapiro and K. M. Arnell, Temporary
suppression of visual processing in an RSVP task, *J. Exp. Psychol. Hum. Percept. Perform.* 18 (1992) 849–860. M. M.
Chun and M. C. Potter, A two-stage model for multiple target detection in RSVP, *J. Exp. Psychol. Hum. Percept.
Perform.* 21 (1995) 109–127. H. Pashler, Dual-task interference in simple tasks, *Psychol. Bull.* 116 (1994) 220–244.
J. R. Stroop, Studies of interference in serial verbal reactions, *J. Exp. Psychol.* 18 (1935) 643–662. C. M.
MacLeod, Half a century of research on the Stroop effect, *Psychol. Bull.* 109 (1991) 163–203. J. D. Cohen, K. Dunbar
and J. L. McClelland, On the control of automatic processes, *Psychol. Rev.* 97 (1990) 332–361. B. A. Eriksen and C.
W. Eriksen, Effects of noise letters upon the identification of a target letter, *Percept. Psychophys.* 16 (1974)
143–149. M. M. Botvinick et al., Conflict monitoring and cognitive control, *Psychol. Rev.* 108 (2001) 624–652. G.
Gratton, M. G. H. Coles and E. Donchin, Optimizing the use of information, *J. Exp. Psychol. Gen.* 121 (1992)
480–506. R. D. Rogers and S. Monsell, Costs of a predictable switch between simple cognitive tasks, *J. Exp. Psychol.
Gen.* 124 (1995) 207–231. J. Moran and R. Desimone, Selective attention gates visual processing in the extrastriate
cortex, *Science* 229 (1985) 782–784. R. Desimone and J. Duncan, Neural mechanisms of selective visual attention,
*Annu. Rev. Neurosci.* 18 (1995) 193–222. D. J. Heeger, Normalization of cell responses in cat striate cortex, *Vis.
Neurosci.* 9 (1992) 181–197. J. H. Reynolds and D. J. Heeger, The normalization model of attention, *Neuron* 61 (2009)
168–185. K. Herrmann et al., When size matters: attention affects performance by contrast or response gain, *Nat.
Neurosci.* 13 (2010) 1554–1559. C. Bundesen, A theory of visual attention, *Psychol. Rev.* 97 (1990) 523–547. G.
Sperling, The information available in brief visual presentations, *Psychol. Monogr.* 74 (1960) 1–29. N. H. Mackworth,
The breakdown of vigilance during prolonged visual search, *Q. J. Exp. Psychol.* 1 (1948) 6–21. J. M. Wolfe, T. S.
Horowitz and N. M. Kenner, Rare items often missed in visual searches, *Nature* 435 (2005) 439–440. M. S. Fleck and S.
R. Mitroff, Rare targets are rarely missed in correctable search, *Psychol. Sci.* 18 (2007) 943–947. D. L. Strayer and
W. A. Johnston, Driven to distraction, *Psychol. Sci.* 12 (2001) 462–466. D. L. Strayer, F. A. Drews and D. J. Crouch,
A comparison of the cell phone driver and the drunk driver, *Hum. Factors* 48 (2006) 381–391. E. Ophir, C. Nass and A.
D. Wagner, Cognitive control in media multitaskers, *PNAS* 106 (2009) 15583–15587. R. Wiradhany and M. R.
Nieuwenstein, Cognitive control in media multitaskers: two replication studies and a meta-analysis, *Atten. Percept.
Psychophys.* 79 (2017) 2620–2641. P. E. Dux and R. Marois, The attentional blink: a review of data and theory, *Atten.
Percept. Psychophys.* 71 (2009) 1683–1700. A. N. Landau and P. Fries, Attention samples stimuli rhythmically, *Curr.
Biol.* 22 (2012) 1000–1004. A. Vaswani et al., Attention is all you need, *NeurIPS* (2017).

## Problems and solutions

**1. Setting the attenuator.** Under Treisman's attenuator with noise s.d. 0.25, find the attenuation at which your name, threshold 0.55, is heard on a third of trials.

*Solution.* P(heard) = Φ((a − 0.55)/0.25) = 1/3 gives (a − 0.55)/0.25 = Φ⁻¹(1/3) = −0.431, so
a = 0.44: the ignored ear passes a little under half its signal. An ordinary word, threshold 1.1, is then heard with
probability Φ((0.44 − 1.1)/0.25) = Φ(−2.6) ≈ 0.4%.

**2. Serial, self-terminating search.** A serial, self-terminating search checks items at 50 ms each. Derive the target-present and target-absent slopes, and their ratio.

*Solution.* With n items checked in random order at t ms each, a present target is found
after (n + 1)/2 checks on average, so RT = base + t(n + 1)/2 and the slope is t/2 = 25 ms an item; an absent response
needs all n checks, slope t = 50 ms. The ratio is exactly 2 for the means; a guided search lowers both slopes, and
its absent slope depends on the quitting threshold, so the ratio need not be 2.

**3. The bottleneck's slope.** Show that a central bottleneck makes the second response time fall with slope $-1$ at short SOAs, and find the SOA at which the slope becomes 0.

*Solution.* RT2 = max(SOA + A2, A1 + B1) + B2 + C2 − SOA. While SOA + A2 < A1 + B1 the maximum is
A1 + B1, so RT2 = A1 + B1 + B2 + C2 − SOA and dRT2/dSOA = −1. Once SOA > A1 + B1 − A2 = 100 + 150 − 100 = 150 ms (with
Psyche's means), RT2 = A2 + B2 + C2, a constant: slope 0. With variable stages the corner is rounded.

**4. Why interference outweighs facilitation.** In a diffusion with bound $a$ and drift $v$, the mean decision time is $\frac{a}{v}\tanh(av)$. Show why subtracting drift costs more time than adding it saves.

*Solution.* T(v) = (a/v) tanh(av) is decreasing and convex in v, so for a change
Δ, T(v − Δ) − T(v) > T(v) − T(v + Δ). With a = 1.5, v = 2.5 and Δ = 1.2 (Psyche's word pathway after control), T(1.3) −
T(2.5) = 0.51 and T(2.5) − T(3.7) = 0.19 units, or about 205 and 75 ms at 400 ms a unit: Psyche's 209 and 80.

**5. Contrast gain from a uniform field.** Write the normalization model with an attention field, and show that a uniform attention gain cancels at high contrast.

*Solution.* With A constant over the pool, R = A E/(A pool(E) + σ). At high contrast σ
is negligible and R → E/pool(E): A cancels and the maximum is unchanged. At low contrast R ≈ A E/σ: multiplying the
drive by A is the same as multiplying c^n by A, that is, multiplying contrast by A^(1/n). With A = 2 and n = 2 the
curve shifts left by √2, so c50 falls by a factor 0.71, Psyche's value for a small stimulus.

**6. Misses against search time.** With `explainer.psychology.psyche.attention`: vary the quitting threshold in guided search, and plot misses against the absent slope.

*Solution.* Raising the quitting margin z from 0.5 to 2.5 standard deviations (conjunction
search, 150 trials a point) lowers misses from 32% to 0.7% and raises the absent slope from 15 to 46 ms an item, while
the present slope rises only from 4 to 11: thoroughness is paid for mostly on absent trials.

**7. ★ A limit or a choice?** Design an experiment that tells a capacity limit from a strategic choice in the attentional blink.

*Solution.* Keep the stimuli identical and change only what the observer is encouraged to do with
T1: for example, add a concurrent irrelevant task, or tell people to attend more diffusely. If the blink shrinks while
T1 accuracy holds, part of it is a strategy of over-investing in T1 rather than a fixed capacity limit; Olivers and
Nieuwenhuis (2005) found that music or a free-association task reduced the blink in just this way.

## Where it comes back

Working memory, what attention selects and holds: Part 19. The central executive: Part 19's multicomponent model. Self-control: Part 28. Perceptual decisions as evidence accumulation: Part 25. Attention across the
lifespan and in ADHD: Parts 31 and 41. Vigilance, driving and cockpits: Part 51. Designing for attention, and against
it: Part 52. Attention in brains and in machines: Part 60. Psyche's `attention` module supplies the search, cueing and
conflict models those parts extend.

## Open checks

Before the narrated master:

* Anderson et al.'s design and Awh et al.'s argument are from the abstract and memory; Lubow's review from its
  chapter abstracts.
* The 46% and the black-team doubling in Simons and Chabris (1999) are from secondary summaries.
* Treisman and Gelade's slopes are from a lecture reproduction of Experiment 1.
* Moray's third, the 35 repetitions, and the details of Treisman's ear-switching study are from memory and summaries.
* Posner's, Rogers and Monsell's and Mackworth's numbers are not quoted; the curves are Psyche's.
* Drew et al.'s eye-tracking claim, Landau and Fries's 4 Hz and the transformer history are from abstracts and memory.
* The alarm-fatigue and ad-viewability statements (half the pixels for one second) are from industry and
  patient-safety summaries.
