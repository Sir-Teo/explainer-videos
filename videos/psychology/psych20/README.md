# Psychology, Built: Part 20, Memory I: Storing and Finding

In 1885 Hermann Ebbinghaus, his own and only subject, published the first experiments on memory. This part follows
the search for what is remembered and how it is found, from his invented syllables to a model of a slowly drifting
state of mind, fitted by maximum likelihood to 3,528 lists recalled by real people, and tested on the experiments
that broke the older story.

Ebbinghaus's savings with his own formula, a power law and an exponential fitted; ACT-R's activation, and Anderson
and Schooler's argument that forgetting tracks the odds of need; free recall on you; the serial-position curve and
first recall on the PEERS open data, Glanzer and Cunitz's dissociation and Rundus's rehearsal; the lag-conditional
response probability derived with its denominators, contiguity and its forward lean on the open data, person by
person, and long-term recency; levels of processing, transfer-appropriate processing, the generation effect and the
method of loci; encoding specificity; Godden and Baddeley's divers and Murre's replication from his open data, with an
exact sign-flip test; state dependence; SAM's buffer and search, simulated; the drift of context derived, context
similarity at lag k, recency and the ratio argument, and contiguity from reinstated context; the context model's
exact likelihood, a maximum-likelihood fit to half the lists, a held-out comparison against serial position alone in
bits per recall, and two tests on other designs (it passes Glanzer and Cunitz and fails Bjork and Whitten); a Hopfield
network settling and its capacity derived and computed; H.M., the memory-systems map, priming in amnesia; familiarity
and recollection, dual-process and unequal-variance ROCs; the hippocampus as an index, pattern separation computed,
time cells, context reinstatement in the brain and engrams. The practice chapter is the cognitive interview, survey
recall and word-list tests in the clinic; the frontier is one system or many, context from lists to lives, and a
context model inside language models.

## Where the numbers come from

| What | Source |
|---|---|
| Savings of 58.2, 44.2, 35.8, 33.7, 27.8, 25.4 and 21.1% after 20 minutes to 31 days; his formula with k = 1.84, c = 1.25; about 2,300 syllables | Ebbinghaus (1885), ch. VII, from the 1913 translation (Archive, Part 1) |
| Refitted: Ebbinghaus's law k = 1.82, c = 1.21 (residual SS 18.8); power law 82.5 t^−0.131 (25.5); exponential, τ = 33.5 days (580) | Psyche (`memory.fit_forgetting`), item `forgetting` |
| ACT-R's activation with d = 0.5, a retrieval threshold of −0.5 and noise 0.4; one, three and ten uses | Psyche (`memory.actr_activation`, `memory.actr_recall`), item `forgetting`; the equation from Anderson's ACT-R |
| Need probability falling as a power of time since last use, in headlines, child-directed speech and email | Anderson and Schooler (1991), from the abstract and secondary summaries |
| 126 people, 3,528 lists of 16 words, immediate free recall | PEERS (Kahana lab), as packaged with psifr 0.10.1; the CSV inside the wheel, fetched by `explainer.psychology.opendata` and checked by SHA-256 |
| Serial position 82% (position 1), about 57% (the middle), 92% (position 16); 45% of recalls start at position 16; lag-CRP 0.45 at +1 and 0.26 at −1 | computed from the open data, item `peers` |
| Person by person: 98% show recency and 97% primacy against their own middle; 89% lean forward | computed from the open data, item `persons`; Healey and Kahana (2014) for the test, from the abstract |
| Murdock's design (lists of 10 to 40 words at 1 or 2 s); Glanzer and Cunitz's 30 s of counting; Rundus's rehearsal; Bjork and Whitten; Baddeley and Hitch's rugby players; Howard and Kahana's continual distractor | the papers' designs and findings as reviewed; none of their numbers is shown |
| Recognition of about 15, 48 and 81% after case, rhyme and meaning questions (incidental), 23, 59 and 81% (intentional) | Craik and Tulving (1975), Experiments 2 and 9, as quoted in a review |
| The generation effect: 86 studies, 445 effect sizes, mean 0.40 | Bertsch, Pesta, Wiscott and McDaniel (2007), from the PubMed abstract |
| Memory athletes 70.8 and controls 39.9 of 72 words after 20 minutes; 40 sessions of 30 minutes | Dresler et al. (2017), from the paper at PubMed Central |
| Godden and Baddeley's means: 13.5 (land, land), 8.4 (land, water), 8.6 (water, land), 11.4 (water, water) of 36 words | as transcribed by Murre in the workbook of his 2021 replication; the 1975 paper was not read |
| Murre's sixteen divers: 9.25, 9.81, 6.94 and 5.00 words; the per-diver context effect −1.25 words (s.e. 0.58); exact sign-flip p = 0.055; a heated pool 1.8 m deep, one session | the workbook itself (osf.io/q2vjk), fetched and checked by SHA-256, item `divers`; the paper at PubMed Central |
| Environmental context effects of about d = 0.25 | Smith and Vela (2001), as Murre summarises them |
| SAM with a buffer of 4, a = b = 0.1, eight failures to stop: serial position 0.75 to 1.00, lag-CRP 0.24 at +1 and 0.20 at −1 | Psyche (`memory.sam_simulate`), item `sam`, 4,000 lists, parameters set by hand |
| The fitted context model: β_enc 0.95, β_rec 0.92, β_start 0.04, γ 0.10, φ_s 8.9, φ_d 1.66, τ 1.19, s_0 0.007, s_r 0.30; ρ = 0.31; log-likelihood −39,697 on 1,764 lists | Psyche (`memory.fit_cmr_ml`), item `cmr`, fitted to every other list of PEERS |
| Held out (the other 1,764 lists, 18,632 recalls): 3.30 bits per recall by chance among the words left, 3.23 by serial position alone, 2.67 by the context model | Psyche (`memory.cmr_loglik`, `memory.position_choice_loglik`), item `cmr` |
| A delay (drift 0.99 to new context): recency 86% to 70%, first recalls from position 1 rising from 8% to 24%; distraction after every word: no long-term recency | Psyche (`memory.cmr_simulate`), item `cmr`; Sederberg, Howard and Kahana (2008) for the model that passes |
| Context similarity of 0.31 at lag 1; support from retrieved context, forward 1.00 against backward 0.37 | Psyche, items `drift` and `reinstate` |
| A ring stored with seven random patterns in 100 units, cued with 30% flipped, back within one sweep | Psyche, item `hopfield` |
| Recall collapsing between 0.14 and 0.18 patterns per unit in 200 units; 0.138 N in the limit | Psyche (`memory.hopfield_capacity`), item `hopfield`; Amit, Gutfreund and Sompolinsky (1985) |
| H.M.'s operation in 1953 and mirror tracing | Scoville and Milner (1957); Milner (1962) (Archive, Part 7) |
| Dual-process ROC with recollection 0.3 and familiarity d′ = 1; unequal-variance ROC with d = 1.2 and s.d. 1.25 | Psyche (`memory.dual_process_roc`, `memory.uvsd_roc`), item `recognition` |
| Inputs overlapping 80% give codes overlapping 38% (200 inputs to 2,000 cells, 2% active) | Psyche (`memory.pattern_separation`), item `separation` |
| The cognitive interview: 42 studies, 55 comparisons, nearly 2,500 people; d = 0.87 for correct details, about 0.24 for errors; 85% against 82% accurate | Köhnken, Milne, Memon and Bull (1999), from the abstract and summaries |
| Induction heads that behave like CMR | Ji-An, Zhou, Benna and Mattar (2024), from the abstract |

## Built in this part

* `explainer/psychology/psyche/memory.py`: forgetting laws fitted by least squares; the serial-position curve,
  first recall and the lag-CRP with available-transition denominators; SAM's rehearsal buffer, sampling, recovery and
  stopping; the context maintenance and retrieval model without semantic or source features, with distractor drift,
  its exact likelihood along observed sequences and a maximum-likelihood fit; a baseline that predicts each recall
  from serial position alone; a Hopfield network and its capacity; ACT-R's base-level activation; dual-process and
  unequal-variance ROCs; pattern separation by a sparse expansion. Tested in `tests/psychology/test_memory.py`,
  including the likelihood against the model's own simulation and the worked lag-CRP.
* `explainer/psychology/opendata.py` gains PEERS free recall (from the psifr wheel, both files checked by SHA-256)
  and Murre's divers (from his OSF workbook, read with the standard library).
* The Ledger gains six rows; the Archive seven datasets.
* The course's interactive is free recall: three lists of ten words, and the reader's own serial-position and lag-CRP
  curves.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| The first and last few items are recalled best, and recall starts at the end | Murdock 1962 | replicated |
| Recalling one item brings back its neighbours in time, forward more than backward | Kahana 1996 | replicated |
| Words processed for meaning are remembered better than for sound or appearance | Craik and Tulving 1975 | replicated |
| Generated words are remembered better than read ones | Slamecka and Graf 1978 | replicated |
| A cue helps when it was part of what was encoded | Tulving and Thomson 1973 | replicated |
| Divers recall best in the environment where they learnt | Godden and Baddeley 1975 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Ebbinghaus (Part 21's row),
Anderson and Schooler (an analysis of the environment), Raaijmakers and Shiffrin and Hopfield (models), H.M. and
Milner (a single case, Part 7), the memory-systems taxonomy and the priming dissociations (a framework and its
evidence, Part 7's lesson), Mandler and Tulving's remember-know and the recognition debate (Part 12's ROC row and an
open argument), Marr and Teyler and DiScenna (theories), time cells, Manning et al. and the engram (neuroscience
findings reported, Part 5), Dresler et al. (a single training study), Köhnken et al. (Part 56), Loftus and Marburger
(a survey method), Berry et al. and Ji-An et al. (frontier models).

## Build it

```bash
python -m videos.psychology.psych20.compute            # every number (four minutes; fetches the open data once)
python tools/qa_scene.py psych20 Fit                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych20 -q l   # the whole part, silent preview
python tools/build.py psych20                          # 1080p30 with narration
python tools/qa_scene.py psych20 Context --lang zh     # the Chinese edition of one chapter
python tools/make.py psych20                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 20                    # the lab: forgetting, free recall, context, attractors
python tools/check_ledger.py psych20                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's memory module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | One subject, 2,300 syllables | Ebbinghaus's method and savings; free recall on you; the questions; objectives |
| 1 | Savings and the first curve | Three laws fitted; ACT-R's activation; Anderson and Schooler's environment |
| 2 | First and last | Scoring your sheet; serial position and first recall on open data; two stores |
| 3 | One word leads to the next | The lag-CRP derived; contiguity and its lean; 126 people one at a time; long-term recency |
| 4 | What you do with it | Levels of processing; transfer-appropriate processing; generation; the method of loci |
| 5 | The cue and the trace | Encoding specificity; the divers; Murre's replication from open data; state dependence |
| 6 | Searching associative memory | SAM's buffer, search and stopping; simulated against the data |
| 7 | A context that drifts | The drift derived; context similarity; recency and the ratio argument; contiguity's forward lean |
| 8 | Fitting the context model | The likelihood; the fitted parameters; the held-out test in bits; tested on two other designs |
| 9 | Memories as valleys | A Hopfield network; recall by settling; capacity derived and computed |
| 10 | One memory or many? | H.M.; a map of memory systems; priming in amnesia |
| 11 | Knowing and remembering | Familiarity and recollection; two ROC models; where the two processes are |
| 12 | The hippocampus as an index | Indexing theory; pattern separation computed; time cells, reinstatement and engrams |
| 13 | The Ledger | Serial position; contiguity; levels; generation; encoding specificity; the divers |
| 14 | In practice: interviews, surveys, the clinic | The cognitive interview; telescoping and landmarks; word-list tests |
| 15 | Frontier: from lists to lives | One system or many; context from lists to lives; a context model inside language models |
| | Recap, problems, and the road ahead | Ten lines; the first two objections; payoffs; problems; references; Part 21 |

## Sources

**Books.** M. J. Kahana, *Foundations of Human Memory* (Oxford, 2012). A. Baddeley, M. W. Eysenck and M. C. Anderson,
*Memory* (3rd ed., Routledge, 2020). H. Ebbinghaus, *Memory: A Contribution to Experimental Psychology* (transl. H. A.
Ruger and C. E. Bussenius, 1913).

**Forgetting and its environment.** H. Ebbinghaus, *Über das Gedächtnis* (1885). J. R. Anderson and L. J. Schooler,
Reflections of the environment in memory, *Psychol. Sci.* 2 (1991) 396–408. J. R. Anderson and C. Lebiere, *The
Atomic Components of Thought* (1998). J. M. J. Murre and J. Dros, Replication and analysis of Ebbinghaus' forgetting
curve, *PLoS ONE* 10 (2015) e0120644.

**Free recall.** B. B. Murdock, The serial position effect of free recall, *J. Exp. Psychol.* 64 (1962) 482–488. M.
Glanzer and A. R. Cunitz, Two storage mechanisms in free recall, *J. Verbal Learn. Verbal Behav.* 5 (1966) 351–360. D.
Rundus, Analysis of rehearsal processes in free recall, *J. Exp. Psychol.* 89 (1971) 63–77. R. A. Bjork and W. B.
Whitten, Recency-sensitive retrieval processes in long-term free recall, *Cogn. Psychol.* 6 (1974) 173–189. A. D.
Baddeley and G. Hitch, Recency reexamined, in *Attention and Performance VI* (1977). M. J. Kahana, Associative
retrieval processes in free recall, *Mem. Cognit.* 24 (1996) 103–109. M. W. Howard and M. J. Kahana, Contextual
variability and serial position effects in free recall, *J. Exp. Psychol. Learn. Mem. Cogn.* 25 (1999) 923–941. M. K.
Healey and M. J. Kahana, Is memory search governed by universal principles or idiosyncratic strategies?, *J. Exp.
Psychol. Gen.* 143 (2014) 575–596. M. K. Healey, N. M. Long and M. J. Kahana, Contiguity in episodic memory,
*Psychon. Bull. Rev.* 26 (2019) 699–720. N. W. Morton, Psifr: analysis and visualization of free recall data, *J. Open
Source Softw.* (2020).

**Encoding and cues.** F. I. M. Craik and R. S. Lockhart, Levels of processing, *J. Verbal Learn. Verbal Behav.* 11
(1972) 671–684. F. I. M. Craik and E. Tulving, Depth of processing and the retention of words in episodic memory, *J.
Exp. Psychol. Gen.* 104 (1975) 268–294. C. D. Morris, J. D. Bransford and J. J. Franks, Levels of processing versus
transfer appropriate processing, *J. Verbal Learn. Verbal Behav.* 16 (1977) 519–533. N. J. Slamecka and P. Graf, The
generation effect, *J. Exp. Psychol. Hum. Learn. Mem.* 4 (1978) 592–604. S. Bertsch et al., The generation effect: a
meta-analytic review, *Mem. Cognit.* 35 (2007) 201–210. M. Dresler et al., Mnemonic training reshapes brain networks
to support superior memory, *Neuron* 93 (2017) 1227–1235. E. Tulving and D. M. Thomson, Encoding specificity and
retrieval processes in episodic memory, *Psychol. Rev.* 80 (1973) 352–373. D. R. Godden and A. D. Baddeley,
Context-dependent memory in two natural environments, *Br. J. Psychol.* 66 (1975) 325–331. S. M. Smith and E. Vela,
Environmental context-dependent memory, *Psychon. Bull. Rev.* 8 (2001) 203–220. J. M. J. Murre, The Godden and
Baddeley (1975) experiment on context-dependent memory on land and underwater: a replication, *R. Soc. Open Sci.* 8
(2021) 200724. D. W. Goodwin et al., Alcohol and recall: state-dependent effects in man, *Science* 163 (1969). J. E.
Eich, The cue-dependent nature of state-dependent retrieval, *Mem. Cognit.* 8 (1980) 157–173.

**Models.** J. G. W. Raaijmakers and R. M. Shiffrin, Search of associative memory, *Psychol. Rev.* 88 (1981) 93–134.
M. W. Howard and M. J. Kahana, A distributed representation of temporal context, *J. Math. Psychol.* 46 (2002)
269–299. S. M. Polyn, K. A. Norman and M. J. Kahana, A context maintenance and retrieval model of organizational
processes in free recall, *Psychol. Rev.* 116 (2009) 129–156. P. B. Sederberg, M. W. Howard and M. J. Kahana, A
context-based theory of recency and contiguity in free recall, *Psychol. Rev.* 115 (2008) 893–912. J. J. Hopfield,
Neural networks and physical systems with emergent collective computational abilities, *PNAS* 79 (1982) 2554–2558. D.
J. Amit, H. Gutfreund and H. Sompolinsky, Storing infinite numbers of patterns in a spin-glass model of neural
networks, *Phys. Rev. Lett.* 55 (1985) 1530–1533. H. Ramsauer et al., Hopfield networks is all you need (2020).

**Systems, recognition and the hippocampus.** W. B. Scoville and B. Milner (1957). E. Tulving, Episodic and semantic
memory (1972). L. R. Squire, Memory systems of the brain, *Neurobiol. Learn. Mem.* 82 (2004) 171–177. E. K.
Warrington and L. Weiskrantz, Amnesic syndrome: consolidation or retrieval?, *Nature* 228 (1970) 628–630. P. Graf, L.
R. Squire and G. Mandler, The information that amnesic patients do not forget, *J. Exp. Psychol. Learn. Mem. Cogn.* 10
(1984) 164–178. G. Mandler, Recognizing: the judgment of previous occurrence, *Psychol. Rev.* 87 (1980) 252–271. E.
Tulving, Memory and consciousness, *Can. Psychol.* 26 (1985) 1–12. A. P. Yonelinas (1994). J. T. Wixted, Dual-process
theory and signal-detection theory of recognition memory, *Psychol. Rev.* 114 (2007) 152–176. T. J. Teyler and P.
DiScenna, The hippocampal memory indexing theory, *Behav. Neurosci.* 100 (1986) 147–154. J. K. Leutgeb et al.,
Pattern separation in the dentate gyrus and CA3 of the hippocampus, *Science* 315 (2007) 961–966. C. J. MacDonald, K.
Q. Lepage, U. T. Eden and H. Eichenbaum, Hippocampal "time cells" bridge the gap in memory for discontiguous events,
*Neuron* 71 (2011) 737–749. J. R. Manning et al., Oscillatory patterns in temporal lobe reveal context reinstatement
during memory search, *PNAS* 108 (2011). X. Liu et al. (2012).

**Practice and frontier.** R. P. Fisher and R. E. Geiselman, *Memory-Enhancing Techniques for Investigative
Interviewing* (1992). G. Köhnken, R. Milne, A. Memon and R. Bull, The cognitive interview: a meta-analysis, *Psychol.
Crime Law* 5 (1999) 3–27. E. F. Loftus and W. Marburger, Since the eruption of Mt. St. Helens, has anyone beaten you
up?, *Mem. Cognit.* 11 (1983) 114–120. C. J. Berry, D. R. Shanks and R. N. A. Henson, A single-system account of the
relationship between priming, recognition, and fluency, *J. Exp. Psychol. Learn. Mem. Cogn.* 34 (2008) 97–111. M. G.
Uitvlugt and M. K. Healey, Temporal proximity links unrelated news events in memory, *Psychol. Sci.* 30 (2019). L.
Ji-An, C. Zhou, M. Benna and M. G. Mattar, Linking in-context learning in transformers to human episodic memory,
*NeurIPS* (2024).

## Problems and solutions

**1. A saving.** Ebbinghaus took 1,156 s to learn a list and 780 s to relearn it a day later. What is the saving, and what does his formula predict for 24 hours?

*Solution.* (1,156 − 780)/1,156 = 32.5%. His formula at t = 1,440 minutes: log10 1,440 = 3.158, raised to 1.25 is
4.21, and 100 × 1.84/(4.21 + 1.84) = 30.4%, which is his own calculated value for a day; the observed saving in his
table was 33.7%.

**2. A lag-CRP by hand.** For the recall sequence 16, 15, 14, 1, 2, 9 of a 16-word list, count the actual and possible transitions at lags $+1$ and $-1$, and give both CRPs.

*Solution.* The transitions are 16→15 (−1), 15→14 (−1), 14→1 (−13), 1→2 (+1), 2→9 (+7). Lag −1 was
possible after 16, 15 and 14 (to 15, 14 and 13, none yet recalled) and taken twice: CRP(−1) = 2/3. Lag +1 was possible
after 1 (to 2) and after 2 (to 3), but not after 16 (no 17), 15 or 14 (16 and 15 already recalled), and taken once:
CRP(+1) = 1/2. `memory.lag_crp` agrees (`tests/psychology/test_memory.py`).

**3. The drift of context.** Show that for orthogonal inputs the drift keeps $\|\mathbf{c}\| = 1$ with $\rho = \sqrt{1 - \beta^2}$, and that $\mathbf{c}_i \cdot \mathbf{c}_j \to \rho^{|i-j|}$ for a long list.

*Solution.* With ‖c_{i−1}‖ = 1, ‖c^IN‖ = 1 and c_{i−1}·c^IN = 0, ‖ρc_{i−1} + βc^IN‖² = ρ² + β², which
is 1 when ρ = √(1 − β²); the general formula reduces to this when the dot product is zero. Unrolling, c_i = ρ^i c_0 +
β Σ_{k≤i} ρ^{i−k} c^IN_k, and for orthogonal inputs c_i·c_j (j > i) = ρ^{i+j} + β² Σ_{k≤i} ρ^{i−k} ρ^{j−k} =
ρ^{j−i}[ρ^{2i} + β²(1 − ρ^{2i})/(1 − ρ²)] = ρ^{j−i}, exactly, since β² = 1 − ρ².

**4. A choice rule ignores a common factor.** Show that a choice rule $a_i^{1/\tau} / \sum_k a_k^{1/\tau}$ is unchanged when every $a_i$ is multiplied by the same constant, and use it to explain long-term recency.

*Solution.* (ka_i)^{1/τ}/Σ_k (ka_k)^{1/τ} = k^{1/τ}a_i^{1/τ}/(k^{1/τ} Σ_k a_k^{1/τ}),
and k^{1/τ} cancels. A delay that moves the test context away from all the words multiplies their matches by about
the same factor, so among the words the competition is unchanged; recency fades only against cues that do not shrink
with the rest (the pull to the start of the list, a baseline, noise). Distraction after every word also makes the
neighbours of the last word much less similar to it, so it stands out among them again: the ratio rule. Chapter 8
shows that our fitted version, whose start-of-list cue does not shrink, still fails this test.

**5. A Hopfield network must settle.** Prove that an asynchronous update of a Hopfield network with symmetric weights and zero diagonal never raises $E = -\tfrac{1}{2}\mathbf{s}^\top W \mathbf{s}$.

*Solution.* Updating unit i changes s_i by Δs_i and E by ΔE = −Δs_i Σ_j W_ij s_j (the
symmetric W counts the pair twice, cancelling the ½, and W_ii = 0 leaves no self-term). The update sets s_i to the sign
of h_i = Σ_j W_ij s_j, so Δs_i is zero or has the sign of h_i, and ΔE = −Δs_i h_i ≤ 0. E is bounded below on a finite
set of states, so the network reaches a state that no update changes.

**6. The divers' test and its power.** With `explainer.psychology.opendata': redo Murre's sign-flip test, then find the power to detect a context effect of 4 words with 16 divers and his spread.

*Solution.* Murre's per-diver effects have mean −1.25 words and s.d. 2.32; the exact
sign-flip test over all 65,536 patterns gives p = 0.055, two-sided. An effect of four words, the size of 1975's, is
d = 4/2.32 = 1.73 at that spread; a paired t test at α = 0.05 has 80% power with five divers and essentially 100%
with sixteen. The replication was not too small; the question is whether a warm, shallow pool in one session is the
same experiment.

**7. ★ One system or two.** Design an experiment that could tell a single-system account of priming and recognition from a two-system account, and say what each predicts.

*Solution.* Measure priming (identification speed or stem completion) and recognition for the same
items in the same people, with recognition confidence. A single-system model, one strength read by two noisy tests,
predicts that priming is larger for items recognised with higher confidence, and that a patient's or a condition's
dissociation shrinks when the two tests are matched for reliability. A two-system model allows priming for items
judged new to equal priming for items judged old. Fit both models to every trial and compare them on held-out
people, as chapter 8 did for recall; Berry, Shanks and Henson's papers do this.

## Where it comes back

Forgetting, consolidation and false memories: Part 21. Semantic memory and concepts: Part 22. Memory across the
lifespan: Part 31. Fitting and comparing models of behaviour: Part 48. Spacing, testing and the classroom: Part 54.
Witnesses and the cognitive interview: Part 56. Memory in machines: Part 60. Psyche's `memory` module supplies the
forgetting laws, the context model and its likelihood, and the Hopfield network those parts extend.

## Open checks

Before the narrated master:

* Craik and Tulving's proportions are as quoted in a review of the paper (Experiments 2 and 9).
* Godden and Baddeley's means are Murre's transcription in his workbook; read the 1975 paper.
* Smith and Vela's d of about 0.25 is Murre's summary of their meta-analysis.
* The designs of Murdock, Glanzer and Cunitz, Rundus, Bjork and Whitten, Baddeley and Hitch and Howard and Kahana are
  from reviews; none of their numbers is shown.
* Köhnken et al.'s error effect is 0.24 in the abstract and 0.28 in one summary.
* The PEERS subset is the one psifr ships (lists without an encoding task); its exact selection should be confirmed
  against the PEERS documentation.
