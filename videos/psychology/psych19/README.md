# Psychology, Built: Part 19, Working Memory

George Miller was persecuted by an integer, seven. This part follows the limit on what can be held in mind from
Miller's chunks to a contest between four likelihoods fitted to seven thousand open trials, and from a box in a
diagram to a ring of neurons whose memory diffuses, and it asks what an industry promising to enlarge the limit
actually delivered.

Digit span on you; absolute judgment as a channel of about 2.6 bits, computed; span counts chunks, not bits, and
recoding performed; Sperling's partial report and a fading icon; the Brown-Peterson task, Keppel and Underwood's
first trial, and SIMPLE's temporal distinctiveness derived; the modal model and patient K.F.; Baddeley and Hitch's
multicomponent model, the phonological loop run on Psyche with the word-length effect and articulatory suppression,
and span against speech rate; Sternberg's memory scanning, self-terminating against exhaustive search, and Townsend's
proof that limited-capacity parallel search mimics serial search; change detection, Cowan's and Pashler's K derived,
and Cowan's four; continuous report on Bays, Catalao and Husain's open data with mixture and swap fits, four process
models fitted to every observer, and a variable-precision observer who never guesses but looks as if it does;
delay activity, a ring attractor computed and its diffusion; complex span and fluid intelligence; dual n-back,
active controls, the meta-analyses and the FTC. The practice chapter is chunked codes, forms, interruptions,
read-backs and span as a clinical measure; the frontier is why the limit is small, with a shared information budget
fitted to the data.

## Where the numbers come from

| What | Source |
|---|---|
| Spans of about 9 binary digits, 7 decimal digits and 5 words; absolute judgment of about 2.6 bits; Smith's recoding to about 40 binary digits; "persecuted by an integer" | Miller (1956), from secondary summaries and quotations |
| The judgment channel: transmitted information against categories, levelling off at 2.70 bits (noise 4% of the range) | Psyche (`wm.absolute_judgment`), item `judgment` |
| About 4.5 letters by whole report; about 9 of 12 available by partial report at once | Sperling (1960), from secondary summaries; the monograph's tables not read |
| Partial report against cue delay: 9.2 letters at 0 ms, 5.9 at 300, 4.6 at 1,000 | Psyche (`wm.partial_report`, i = 0.62, τ = 250 ms), item `sperling` |
| About 80% recalled after 3 s of counting and about 10% after 18 s | Peterson and Peterson (1959), from secondary summaries |
| SIMPLE: late trials 78, 62, 44, 27, 16 and 10% at 3 to 18 s; at 18 s, 100% on trial 1, 75% on trial 2, 64% on trial 3 | Psyche (`wm.brown_peterson`, c = 1, a soft threshold at D = 0.5), item `forgetting`; Keppel and Underwood (1962) for the pattern |
| K.F.'s digit span of about 2 with normal long-term learning | Warrington and Shallice (1969), Shallice and Warrington (1970), from secondary summaries |
| The loop: spans of 6.2 (0.3 s words) and 3.0 (0.8 s words), 2.4 and 2.3 under suppression; span against reading rate | Psyche (`wm.loop_span`), item `loop`; Baddeley, Thomson and Buchanan (1975) for the pattern and the two seconds |
| Sternberg's 37.9 ms per item from 397.2 ms, r² = 0.994 | Sternberg (1966), from a hosted copy of the paper |
| Scanning models: serial 38.3 ms per item; self-terminating half the slope on yes trials; unlimited parallel curved; limited-capacity parallel identical to serial | Psyche (`wm.sternberg_rts`), item `sternberg` |
| Capacity of about 4 objects; objects with four features held as well as single features | Luck and Vogel (1997), from the abstract |
| Change detection with K = 3.5 slots, and Cowan's K recovering it | Psyche (`wm.change_detection`, `wm.k_cowan`), item `change` |
| 4 ± 1 | Cowan (2001), from memory and reviews |
| 7,271 trials from 12 observers; set sizes 1, 2, 4 and 6; sample durations 100, 500 and 2,000 ms | Bays, Catalao and Husain (2009), the data file itself (osf.io/c2yx5), fetched by `explainer.psychology.opendata` and checked by SHA-256 |
| Error spreads (circular s.d.) of about 16, 29, 49 and 63 degrees | computed from the open data, item `bays` |
| Mixture fits: g = 0.01, 0.09, 0.28, 0.44; s.d. 14, 18, 22, 22 degrees; swaps at six squares 27%, uniform 18% | fitted to the open data (`wm.fit_mixture`, `wm.fit_swap`), item `bays` |
| Four process models fitted to each observer: variable precision best for 11 of 12; summed AIC worse by 827 (slots + averaging), 948 (slots), 1,526 (equal precision) | fitted to the open data (`wm.fit_model`), item `bays`; van den Berg et al. (2012, 2014) for the models and their result |
| The mimic: the median observer's variable-precision fit (J1 = 27.4, α = 1.20, τ = 15.8) simulated and refitted by the mixture: g = 0.34 and 0.49 at four and six, N(1 − g) = 3.05 at six | Psyche (`wm.simulate_report`, `wm.fit_mixture`), item `mimic` |
| Delay activity and memory fields | Funahashi, Bruce and Goldman-Rakic (1989), described; the firing curves are a schematic |
| The ring attractor: memory s.d. 5.1, 7.3, 10.3 and 13.9 degrees at 0.5, 1, 2 and 4 s; variance linear in delay | Psyche (`wm.ring_attractor`, J0 = −1, J1 = 6, noise 0.06), item `ring`; Wimmer et al. (2014) for the evidence |
| Activity-silent memory; TMS reactivation | Mongillo, Barak and Tsodyks (2008); Rose et al. (2016), from memory and reviews |
| Reading span and comprehension, r about 0.41 | Daneman and Carpenter (1980); Daneman and Merikle (1996), from secondary summaries |
| Working memory and fluid intelligence: about 0.72 latent, about 0.45 between single tasks | Kane, Hambrick and Conway (2005); Ackerman, Beier and Boyle (2005), as quoted in a later review |
| Dual n-back for 8, 12, 17 or 19 days | Jaeggi et al. (2008), the paper's design |
| 20 sessions against adaptive visual search and no contact; no transfer | Redick et al. (2013), from the abstract |
| 87 publications, 145 comparisons; near transfer only | Melby-Lervåg, Redick and Hulme (2016), from the abstract |
| Simulated training trials: far-transfer d averaging 0.37 against no-contact controls (37% of trials above 0.45) and 0.00 against active controls | Psyche (`wm.training_trial`), item `training` |
| About 70 signatories to the 2014 consensus; a reply with more than 100 | the Stanford Center on Longevity's statement and press coverage |
| $2 million in refunds, a $50 million judgment suspended | the FTC's press release of 5 January 2016 |
| A shared budget of 2.3 bits, one item held to 15 degrees; predicted 15, 33, 50 and 57 against observed 16, 29, 49 and 63 | fitted to the open data's spreads (`wm.budget_sd`), item `budget`; Sims, Jacobs and Knill (2012) and van den Berg and Ma (2018) for the idea |

## Built in this part

* `explainer/psychology/psyche/wm.py`: absolute judgment as a channel; recoding; the phonological loop with
  suppression; partial report; SIMPLE and the Brown-Peterson task; Sternberg scanning under serial, self-terminating,
  unlimited-parallel and limited-capacity-parallel models; change detection and the K formulas; von Mises
  precision; the mixture and swap models; slots, slots plus averaging, equal and variable precision fitted by maximum
  likelihood and compared by AIC; a ring attractor; brain-training trials; a shared information budget. Tested in
  `tests/psychology/test_wm.py` against closed forms (Fisher information, harmonic numbers, the exponential minimum),
  recovery of known parameters, and the signatures each model is built to show.
* `explainer/psychology/opendata.py`: open trial-level data fetched on first use into `.cache/psychology_data/` and
  checked by SHA-256; Bays, Catalao and Husain (2009) is the first.
* The Battery's task 5 (change detection) now runs on Psyche.
* The Ledger gains six rows; the Archive twenty-three datasets.
* The course's interactive is change detection: forty-eight trials at four set sizes, and the reader's own K.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A cued part of a brief display is available far beyond whole report, for under a second | Sperling 1960 | replicated |
| Three consonants are forgotten in 18 s because the trace decays | Peterson and Peterson 1959 | story and record |
| Span is shorter for longer words; suppression removes the difference | Baddeley, Thomson and Buchanan 1975 | replicated |
| Memory scanning is linear, with equal slopes for yes and no | Sternberg 1966 | replicated |
| About three to four items can be held without rehearsal | Luck and Vogel 1997 | replicated |
| Working-memory training raises fluid intelligence | Jaeggi et al. 2008 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Miller (history and arithmetic),
Shallice and Warrington (a single case), Baddeley and Hitch (a model), Zhang and Luck and van den Berg et al. (models
fitted here), Bays et al. (open data, fitted), Funahashi et al. (described), Wimmer et al. and Mongillo et al.
(models), Daneman and Carpenter and Kane et al. (correlations; Part 32), Simons et al. and the FTC (a review and a
settlement).

## Build it

```bash
python -m videos.psychology.psych19.compute            # every number (two minutes; fetches the open data once)
python tools/qa_scene.py psych19 Precision             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych19 -q l   # the whole part, silent preview
python tools/build.py psych19                          # 1080p30 with narration
python tools/qa_scene.py psych19 Neurons --lang zh     # the Chinese edition of one chapter
python tools/make.py psych19                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 19                    # the lab: span, forgetting, scanning, capacity, precision
python tools/check_ledger.py psych19                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's working-memory module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Persecuted by an integer | Digit span on you; Miller's seven; the questions; objectives |
| 1 | The magical number seven | Absolute judgment as a channel, computed; span counts chunks; recoding performed |
| 2 | More than you can report | Whole report; partial report; the icon fading, on Psyche |
| 3 | Forgetting in eighteen seconds | The Brown-Peterson task; the first trial; SIMPLE derived |
| 4 | A system, not a store | The modal model and K.F.; Baddeley and Hitch; the word-length effect and suppression; span and speech rate |
| 5 | Searching what you hold | Sternberg's task; exhaustive against self-terminating; Townsend's mimicry derived |
| 6 | Four, not seven | Change detection; Cowan's K derived; the magical number four |
| 7 | Slots or resources | Continuous report on open data; mixture and swaps; four process models; the verdict; the mimic |
| 8 | How neurons hold a thought | Delay activity; a ring attractor computed; diffusion; silent synapses |
| 9 | Working memory and reasoning | Complex span; working memory and fluid intelligence |
| 10 | Can you train it? | Dual n-back; active controls; the meta-analysis; Psyche's trials; the consensus and the FTC |
| 11 | The Ledger | Partial report; Brown-Peterson; word length; scanning; four; training |
| 12 | In practice: forms, read-backs, tests | Chunked codes and forms; read-backs and checklists; span as a measure |
| 13 | Frontier: what is the limit for? | Settled and open; a shared information budget fitted; attention, memory and machines |
| | Recap, problems, and the road ahead | Ten lines; the first two objections; payoffs; problems; references; Part 20 |

## Sources

**Books.** A. Baddeley, *Working Memory, Thought, and Action* (Oxford, 2007). N. Cowan, *Working Memory Capacity*
(Psychology Press, 2005). M. J. Kahana, *Foundations of Human Memory* (Oxford, 2012).

**Papers.** G. A. Miller, The magical number seven, plus or minus two, *Psychol. Rev.* 63 (1956) 81–97. G. Sperling,
The information available in brief visual presentations, *Psychol. Monogr.* 74 (1960) no. 11. M. Coltheart, Iconic
memory and visible persistence, *Percept. Psychophys.* 27 (1980) 183–228. J. Brown, Some tests of the decay theory of
immediate memory, *Q. J. Exp. Psychol.* 10 (1958) 12–21. L. R. Peterson and M. J. Peterson, Short-term retention of
individual verbal items, *J. Exp. Psychol.* 58 (1959) 193–198. G. Keppel and B. J. Underwood, Proactive inhibition in
short-term retention of single items, *J. Verbal Learn. Verbal Behav.* 1 (1962) 153–161. D. D. Wickens, Encoding
categories of words, *Psychol. Rev.* 77 (1970) 1–15. G. D. A. Brown, I. Neath and N. Chater, A temporal ratio model of
memory, *Psychol. Rev.* 114 (2007) 539–576. R. C. Atkinson and R. M. Shiffrin, Human memory: a proposed system and its
control processes, *Psychology of Learning and Motivation* 2 (1968) 89–195. E. K. Warrington and T. Shallice, The
selective impairment of auditory verbal short-term memory, *Brain* 92 (1969) 885–896. T. Shallice and E. K.
Warrington, Independent functioning of verbal memory stores, *Q. J. Exp. Psychol.* 22 (1970) 261–273. A. D. Baddeley
and G. Hitch, Working memory, *Psychology of Learning and Motivation* 8 (1974) 47–89. A. D. Baddeley, The episodic
buffer, *Trends Cogn. Sci.* 4 (2000) 417–423. A. D. Baddeley, N. Thomson and M. Buchanan, Word length and the
structure of short-term memory, *J. Verbal Learn. Verbal Behav.* 14 (1975) 575–589. P. Lovatt, S. E. Avons and J.
Masterson, The word-length effect and disyllabic words, *Q. J. Exp. Psychol.* 53A (2000) 1–22. S. Sternberg,
High-speed scanning in human memory, *Science* 153 (1966) 652–654. S. Sternberg, Memory scanning: new findings and
current controversies, *Q. J. Exp. Psychol.* 27 (1975) 1–32. J. T. Townsend, Some results concerning the
identifiability of parallel and serial processes, *Br. J. Math. Stat. Psychol.* 25 (1972) 168–199. S. J. Luck and E.
K. Vogel, The capacity of visual working memory for features and conjunctions, *Nature* 390 (1997) 279–281. N. Cowan,
The magical number 4 in short-term memory, *Behav. Brain Sci.* 24 (2001) 87–185. H. Pashler, Familiarity and visual
change detection, *Percept. Psychophys.* 44 (1988) 369–378. P. Wilken and W. J. Ma, A detection theory account of
change detection, *J. Vis.* 4 (2004) 1120–1135. W. Zhang and S. J. Luck, Discrete fixed-resolution representations in
visual working memory, *Nature* 453 (2008) 233–235. P. M. Bays and M. Husain, Dynamic shifts of limited working
memory resources in human vision, *Science* 321 (2008) 851–854. P. M. Bays, R. F. G. Catalao and M. Husain, The
precision of visual working memory is set by allocation of a shared resource, *J. Vis.* 9(10):7 (2009). R. van den
Berg et al., Variability in encoding precision accounts for visual short-term memory limitations, *PNAS* 109 (2012)
8780–8785. R. van den Berg, E. Awh and W. J. Ma, Factorial comparison of working memory models, *Psychol. Rev.* 121
(2014) 124–149. W. J. Ma, M. Husain and P. M. Bays, Changing concepts of working memory, *Nat. Neurosci.* 17 (2014)
347–356. S. Funahashi, C. J. Bruce and P. S. Goldman-Rakic, Mnemonic coding of visual space in the monkey's
dorsolateral prefrontal cortex, *J. Neurophysiol.* 61 (1989) 331–349. K. Wimmer, D. Q. Nykamp, C. Constantinidis and
A. Compte, Bump attractor dynamics in prefrontal cortex explains behavioral precision in spatial working memory, *Nat.
Neurosci.* 17 (2014) 431–439. G. Mongillo, O. Barak and M. Tsodyks, Synaptic theory of working memory, *Science* 319
(2008) 1543–1546. N. S. Rose et al., Reactivation of latent working memories with transcranial magnetic stimulation,
*Science* 354 (2016) 1136–1139. M. Daneman and P. A. Carpenter, Individual differences in working memory and reading,
*J. Verbal Learn. Verbal Behav.* 19 (1980) 450–466. M. Daneman and P. M. Merikle, Working memory and language
comprehension: a meta-analysis, *Psychon. Bull. Rev.* 3 (1996) 422–433. M. J. Kane, D. Z. Hambrick and A. R. A.
Conway, Working memory capacity and fluid intelligence are strongly related constructs, *Psychol. Bull.* 131 (2005)
66–71. P. L. Ackerman, M. E. Beier and M. O. Boyle, Working memory and intelligence: the same or different
constructs?, *Psychol. Bull.* 131 (2005) 30–60. S. M. Jaeggi et al., Improving fluid intelligence with training on
working memory, *PNAS* 105 (2008) 6829–6833. T. S. Redick et al., No evidence of intelligence improvement after
working memory training, *J. Exp. Psychol. Gen.* 142 (2013) 359–379. M. Melby-Lervåg, T. S. Redick and C. Hulme,
Working memory training does not improve performance on measures of intelligence or other measures of far transfer,
*Perspect. Psychol. Sci.* 11 (2016) 512–534. D. J. Simons et al., Do "brain-training" programs work?, *Psychol. Sci.
Public Interest* 17 (2016) 103–186. C. R. Sims, R. A. Jacobs and D. C. Knill, An ideal observer analysis of visual
working memory, *Psychol. Rev.* 119 (2012) 807–830. R. van den Berg and W. J. Ma, A resource-rational theory of set
size effects in human visual working memory, *eLife* 7 (2018) e34963. K. Oberauer et al., Benchmarks for models of
short-term and working memory, *Psychol. Bull.* 144 (2018) 885–958.

## Problems and solutions

**1. Smith's arithmetic.** With groups of five binary digits recoded into one chunk and a span of 8 chunks, Smith
could hold 8 × 5 = 40 binary digits: 5 bits a chunk, 40 bits in all, against 9 bits without recoding. The span in
chunks barely changed; the information per chunk did.

**2. The two K formulas.** A single probe: on a change trial the changed item is stored with probability K/N and
detected; otherwise "different" is guessed with probability g, so H = K/N + (1 − K/N) g. On a no-change trial, a stored
probe is called "same" and an unstored one "different" with probability g, so F = (1 − K/N) g. Then H − F = K/N, K =
N(H − F). With the whole display back and one item changed, a stored changed item is detected; a "same" display is
called different only by guessing on unstored items, F = g (Pashler's assumption that guessing happens when the
change is not seen), and H = K/N + (1 − K/N) g, so H − F = (K/N)(1 − g) and K = N(H − F)/(1 − F).

**3. Townsend's mimicry.** If j comparisons each finish after an exponential time with rate 1/(jc), the first of them
finishes after an exponential time with rate j · 1/(jc) = 1/c (the minimum of independent exponentials has the sum of
their rates), whose mean is c. By the memoryless property the remaining j − 1 comparisons start afresh, now each at
rate 1/((j − 1)c). Summing the stages, the total is a sum of k exponentials of mean c: exactly the serial exhaustive
model with exponential comparisons, in mean, variance and distribution.

**4. SIMPLE by hand.** With c = 1, the similarity of ages a and b is exp(−|log a − log b|) = min(a, b)/max(a, b). At 3
s among items 30 and 60 s old: D = 1/(1 + 0.1 + 0.05) = 0.87. At 18 s: D = 1/(1 + 0.6 + 0.3) = 0.53. Waiting fifteen
seconds moved the item two-thirds of the way toward its neighbours on the log scale, and its distinctiveness fell by
almost half, without any decay.

**5. A von Mises's precision.** J = κ I1(κ)/I0(κ). At κ = 5, I1(5)/I0(5) = 0.8934, so J = 4.47. The circular s.d. is
√(−2 log 0.8934) = 0.475 radians, 27 degrees; for large κ, J ≈ κ − 1/2 and the s.d. ≈ 1/√κ.

**6. When can AIC be trusted?** Simulating a slots observer with K = 3 and J = 15 at set sizes 1, 2, 4 and 6 and
fitting both models, AIC picked slots in 20 of 20 runs at 50, 200 and 800 trials per set size: a flat floor of true
guesses beside sharply remembered items is hard for variable precision to fake, because it would need many items
with almost no precision and the rest with a lot. The reverse is the hard direction: chapter seven's mimic shows a
variable-precision observer producing a mixture fit that looks like slots, and recovering variable precision needs
more trials. Parameter and model recovery, in both directions, are Part 48's subject.

**7. ★ A convincing training study.** Randomize enough people to detect d = 0.2 on a pre-registered composite of
several reasoning tests (about 400 a group for 80% power); give the control group an adaptive, engaging placebo they
believe is training, and measure expectations in both groups; blind the testers; test at follow-up as well as
immediately; and require that individual gains on the trained task predict gains on reasoning. A control group that
does not believe it was trained cannot rule out expectation.

## Where it comes back

Long-term memory, and working memory as its active part: Parts 20 and 21. The lifespan and ADHD: Parts 31 and 41.
Intelligence: Part 32. Model and parameter recovery: Part 48. Read-backs and checklists: Part 51; cognitive load:
Part 54. The limit as an efficient code: Part 58. Small workspaces and large contexts: Part 60. Psyche's `wm` module
supplies the K formulas, the precision models and the ring attractor those parts extend.

## Open checks

Before the narrated master:

* Miller's numbers and Smith's 40 digits are from summaries and quotations of the 1956 paper.
* Sperling's "about 9 of 12" and "about 4.5" are the commonly quoted figures; read the monograph's tables.
* Peterson and Peterson's 80% and 10% are from secondary summaries (one says under 10% at 18 s).
* K.F.'s span of about two, and Baddeley and Hitch's reasoning-with-digits result, are from summaries.
* Sternberg's 1.2 s per digit and 2 s delay, and Luck and Vogel's 100 ms and 900 ms timings, are from memory.
* The Chinese, English and Welsh digit spans are from memory of Ellis and Hennelly (1980) and Stigler et al. (1986).
* Jaeggi et al.'s sample sizes, the consensus signatory counts (about 70; 127 or 133 in the reply) and Wimmer et al.'s
  findings are from abstracts and press coverage.
