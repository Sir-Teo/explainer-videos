# Psychology, Built: Part 27, Consciousness

A man with a damaged visual cortex insists he sees nothing in half his visual field, and when forced to guess,
points to objects there almost perfectly. Blindsight makes the question experimental: hold the stimulus constant,
vary awareness, and look for what changes. This part follows that method from masking and rivalry to the rival
theories, computes what they claim, and ends with the first test their authors agreed on in advance, Libet's clock
read as accumulated noise, and consciousness lost and found in unresponsive patients.

A digit flashed for one frame and then for ten, on you; D.B. and the history of blindsight; the contrastive method,
inattentional blindness and masked priming; the criterion problem computed with a signal-detection model of masking,
and three ways to measure awareness; blindsight's tests, routes and doubts; the easy and hard problems and the
Koch–Chalmers wager; binocular rivalry on you, Psyche's rivalry oscillator, rivalry neurons and no-report designs;
the global workspace with ignition computed (graded early, all-or-none late); integrated information in Tononi's
2004 form computed for six small networks, its predictions and critics; recurrent processing and higher-order
theories; the Cogitate adversarial collaboration; Libet's experiment and Schurger's accumulator; losing
consciousness: the wakefulness–awareness plane, covert awareness and the perturbational complexity index;
attention, metacognition and what would count as progress. The practice chapter is anaesthesia, diagnosis after
brain injury and machines; the frontier is a scorecard of the theories.

## Where the numbers come from

| What | Source |
|---|---|
| Masking: evidence x ~ N(±d/2, 1) with d = 3 (1 − e^(−SOA/40 ms)); at 33 ms, d = 1.69, "seen" (|x| > 1.5) on 27% of trials, 74% correct on the trials called unseen; 68% with a lax criterion (1.0), 77% with a strict one (2.0) | Psyche (`workspace.masking`, `visibility_curve`), item `masking` |
| Rivalry: 600 s simulated, 174 dominance periods, mean 3.4 s, gamma shape 3.5; raising one eye's input from 0.60 to 0.65 lengthens its periods from 3.4 to 4.5 s and shortens the other eye's from 3.3 to 2.6 s | Psyche (`workspace.rivalry`, `dominance_durations`), item `rivalry` |
| Ignition: 400 trials at each of 31 strengths; sensory activity at 60 ms graded; workspace activity at 600 ms off or on, with ignition near strength 0.85 (42% of trials there) | Psyche (`workspace.ignition`), item `ignition` |
| Φ (Tononi 2004): unconnected two-node loops 0; a feed-forward chain of six 1 bit; copy rings of four and six 2 bits; five nodes each the OR of the rest 0.64; a ring of six XOR gates 0; 31 bipartitions for six nodes | Psyche (`workspace.ei`, `phi`, `network`), item `phi` |
| Schurger's accumulator over 1,200 s: 151 movements with a clean 3-s window, median wait 5.1 s, back-averaged ramp from about 2 s before | Psyche (`workspace.schurger`, `back_average`), item `libet` |
| Illustrative responses: PCI 0.85 (wake-like), 0.11 (sleep-like), 0.08 (local), 1.02 (noise, not a response); the clinical threshold 0.31 | Psyche (`workspace.lz76`, `pci`, `responses`), item `pci`; Casarotto et al. (2016) |
| D.B.: surgery in 1973, forced-choice localization and discrimination far above chance | Weiskrantz, Warrington, Sanders and Marshall (1974) |
| About half of observers missed the gorilla | Simons and Chabris (1999) (Part 18's row: 46% of 192) |
| Masked primes of 43 ms speed congruent responses and prepare a motor response | Dehaene et al. (1998) |
| The urge reported about 200 ms before movement; the readiness potential from about 550 ms (spontaneous acts) | Libet, Gleason, Wright and Pearl (1983) |
| Choice decoded seconds early at about 60% accuracy | Soon, Brass, Heinze and Haynes (2008) |
| 5 of 54 patients modulated activity; about a quarter of 353 patients without bedside command following did so by fMRI or EEG | Monti et al. (2010); Bodien et al. (2024) |
| About four in ten patients diagnosed vegetative were minimally conscious | Schnakers et al. (2009) |
| An open letter signed by 124 researchers | Fleming et al. (2023) |

## Built in this part

* `explainer/psychology/psyche/workspace.py`: masking as one signal read twice (forced choice and a criterion for
  "seen"), with visibility curves; a rivalry oscillator with mutual inhibition, adaptation and slow noise, and
  dominance durations with a gamma fit; a two-stage ignition network (a linear sensory stage, a bistable workspace);
  Boolean networks, effective information and Φ over all bipartitions (Tononi 2004); Schurger, Sitt and Dehaene's
  leaky stochastic accumulator with back-averaging; Lempel–Ziv complexity (LZ76) and the perturbational complexity
  index, with illustrative response patterns. Tested in `tests/psychology/test_workspace.py`.
* The Ledger gains four rows (inattentional blindness keeps its row from Part 18).
* The course's interactive is masking on you: an arrow for a few frames, a mask, a guess and a visibility report,
  and your accuracy on the trials you called unseen.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| After damage to primary visual cortex, people locate and discriminate stimuli they say they do not see | Weiskrantz, Warrington, Sanders and Marshall 1974 | replicated |
| A masked word or number that cannot be reported speeds responses to a related target | Dehaene et al. 1998 | replicated, smaller |
| The readiness potential begins several hundred milliseconds before the reported urge to move | Libet, Gleason, Wright and Pearl 1983 | replicated |
| Some patients without bedside signs of awareness follow commands with their brain activity | Owen et al. 2006 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the founding programmes (Baars,
Crick and Koch), the theories and their reviews (the workspace, integrated information, recurrent processing,
higher-order theories, Seth and Bayne), methods (Eriksen, the awareness scale, no-report designs), philosophical
distinctions (Nagel, Chalmers, Block), the Cogitate study (a single preregistered study, too recent for a record),
rivalry's neural correlates, and the practice chapter's clinical studies; machines are due a row in Part 60.

## Build it

```bash
python -m videos.psychology.psych27.compute            # every number (about a minute)
python tools/qa_scene.py psych27 Workspace             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych27 -q l   # the whole part, silent preview
python tools/build.py psych27                          # 1080p30 with narration
python tools/qa_scene.py psych27 Integration --lang zh # the Chinese edition of one chapter
python tools/make.py psych27                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 27                    # the lab: masking, rivalry, ignition and phi
python tools/check_ledger.py psych27                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's workspace module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Seeing without knowing it | A masked digit on you; D.B.; the questions; objectives |
| 1 | The contrastive method | Masking, rivalry, inattention, neglect; the gorilla; masked priming |
| 2 | Masking and the criterion problem | One signal read twice; unseen accuracy under three criteria; objective, subjective and metacognitive measures |
| 3 | Blindsight | The tests; the routes around V1; scattered light, graded awareness and wagers |
| 4 | The easy problems and the hard one | Chalmers, Nagel and Block; the Koch–Chalmers wager |
| 5 | Correlates: rivalry, report and no-report | Rivalry on you; the rivalry oscillator; neurons that follow the percept; no-report designs |
| 6 | The global workspace | The broadcast; ignition computed; bimodal late activity; four signatures |
| 7 | Integrated information | The axioms; Φ derived and computed; six networks; predictions and the open letter |
| 8 | Recurrence and higher order | Lamme's recurrence; higher-order theories; front or back |
| 9 | An adversarial collaboration | The agreed design; what each theory got wrong |
| 10 | Volition: Libet's clock | Libet's experiment; Schurger's accumulator; the ramp from averaging; where the debate stands |
| 11 | Losing consciousness | Wakefulness and awareness; covert awareness; the complexity index |
| 12 | Attention, metacognition and progress | Two dissociations; metacognition; what would count as progress |
| 13 | The Ledger | Blindsight; masked priming; Libet's timing; covert awareness |
| 14 | In practice: anaesthesia, injury and machines | Awareness under anaesthesia; diagnosis after injury; indicator properties for machines |
| 15 | Frontier: the scorecard | The theories scored; what comes next |
| | Recap, problems, and the road ahead | Ten lines; Kant's three objections; payoffs; problems; references; Part 28 |

## Sources

* L. Weiskrantz, E. K. Warrington, M. D. Sanders and J. Marshall, Visual capacity in the hemianopic field following
  a restricted occipital ablation, Brain 97 (1974) 709-728; L. Weiskrantz, Blindsight: A Case Study and Implications
  (1986).
* J. Campion, R. Latto and Y. M. Smith, Behavioral and Brain Sciences 6 (1983) 423-448; A. Cowey and P. Stoerig,
  Blindsight in monkeys, Nature 373 (1995) 247-249; N. Persaud, P. McLeod and A. Cowey, Nature Neuroscience 10
  (2007) 257-261; M. Overgaard et al., PLoS ONE 3 (2008) e3028; M. C. Schmid et al., Nature 466 (2010) 373-377.
* B. J. Baars, A Cognitive Theory of Consciousness (1988); F. Crick and C. Koch, Towards a neurobiological theory of
  consciousness, Seminars in the Neurosciences 2 (1990) 263-275.
* D. J. Simons and C. F. Chabris, Perception 28 (1999) 1059-1074; S. Dehaene et al., Imaging unconscious semantic
  priming, Nature 395 (1998) 597-600; E. Van den Bussche et al., Psychological Bulletin 135 (2009) 452-477;
  M. A. Vadillo et al., Psychonomic Bulletin & Review 23 (2016) 87-102.
* C. W. Eriksen, Discrimination and learning without awareness, Psychological Review 67 (1960) 279-300; T. Z.
  Ramsøy and M. Overgaard, Introspection and subliminal perception, Phenomenology and the Cognitive Sciences 3 (2004)
  1-23; A. Del Cul, S. Baillet and S. Dehaene, Brain dynamics underlying the nonlinear threshold for access to
  consciousness, PLoS Biology 5 (2007) e260.
* T. Nagel, What is it like to be a bat?, Philosophical Review 83 (1974) 435-450; D. J. Chalmers, Facing up to the
  problem of consciousness, Journal of Consciousness Studies 2 (1995) 200-219; N. Block, On a confusion about a
  function of consciousness, Behavioral and Brain Sciences 18 (1995) 227-247.
* W. J. M. Levelt, On Binocular Rivalry (1965); D. A. Leopold and N. K. Logothetis, Nature 379 (1996) 549-553; D. L.
  Sheinberg and N. K. Logothetis, PNAS 94 (1997) 3408-3413; F. Tong et al., Neuron 21 (1998) 753-759; S. Frässle et
  al., Journal of Neuroscience 34 (2014) 1738-1747; N. Tsuchiya et al., Trends in Cognitive Sciences 19 (2015)
  757-770.
* S. Dehaene, M. Kerszberg and J.-P. Changeux, PNAS 95 (1998) 14529-14534; C. Sergent, S. Baillet and S. Dehaene,
  Nature Neuroscience 8 (2005) 1391-1400; S. Dehaene and J.-P. Changeux, Neuron 70 (2011) 200-227.
* G. Tononi, An information integration theory of consciousness, BMC Neuroscience 5 (2004) 42; M. Oizumi, L.
  Albantakis and G. Tononi, PLoS Computational Biology 10 (2014) e1003588; G. Tononi, M. Boly, M. Massimini and
  C. Koch, Nature Reviews Neuroscience 17 (2016) 450-461; S. Fleming et al., The integrated information theory of
  consciousness as pseudoscience, PsyArXiv (2023).
* V. A. F. Lamme, Towards a true neural stance on consciousness, Trends in Cognitive Sciences 10 (2006) 494-501;
  H. Lau and R. E. Passingham, PNAS 103 (2006) 18763-18768; H. Lau and D. Rosenthal, Trends in Cognitive Sciences
  15 (2011) 365-373; A. K. Seth and T. Bayne, Theories of consciousness, Nature Reviews Neuroscience 23 (2022)
  439-452.
* L. Melloni et al., Making the hard problem of consciousness easier, Science 372 (2021) 911-912; Cogitate
  Consortium, Adversarial testing of global neuronal workspace and integrated information theories of
  consciousness, Nature (2025).
* H. H. Kornhuber and L. Deecke (1965); B. Libet, C. A. Gleason, E. W. Wright and D. K. Pearl, Brain 106 (1983)
  623-642; C. S. Soon et al., Nature Neuroscience 11 (2008) 543-545; J. Trevena and J. Miller, Consciousness and
  Cognition 19 (2010) 447-456; A. Schurger, J. D. Sitt and S. Dehaene, PNAS 109 (2012) E2904-E2913.
* S. Laureys, Trends in Cognitive Sciences 9 (2005) 556-559; A. M. Owen et al., Science 313 (2006) 1402; M. M.
  Monti et al., New England Journal of Medicine 362 (2010) 579-589; Y. G. Bodien et al., New England Journal of
  Medicine 391 (2024); A. G. Casali et al., Science Translational Medicine 5 (2013) 198ra105; S. Casarotto et al.,
  Annals of Neurology 80 (2016) 718-729.
* C. Koch and N. Tsuchiya, Trends in Cognitive Sciences 11 (2007) 16-22; S. M. Fleming et al., Science 329 (2010)
  1541-1543.
* P. S. Myles et al., Lancet 363 (2004) 1757-1763; M. S. Avidan et al., New England Journal of Medicine 358 (2008)
  1097-1108; J. J. Pandit et al., the 5th National Audit Project (2014); C. Schnakers et al., BMC Neurology 9 (2009)
  35; J. T. Giacino et al., Neurology 91 (2018) 450-460; D. Kondziella et al., European Journal of Neurology 27
  (2020) 741-756; P. Butlin, R. Long et al., Consciousness in artificial intelligence (2023).

## Problems and solutions

1. **Unseen accuracy.** With μ = d/2, unseen trials are those with |x| < c. Accuracy among them is
   [Φ(c − μ) − Φ(−μ)] / [Φ(c − μ) − Φ(−c − μ)]. The numerator is the mass of N(μ, 1) on (0, c), the rest of the
   denominator its mass on (−c, 0); for μ > 0 the density is larger at every point of (0, c) than at its mirror
   image in (−c, 0), so the ratio exceeds one half.
2. **Strict criteria.** As c grows, nearly every trial is called unseen, so accuracy on unseen trials tends to the
   overall accuracy Φ(μ). A strict criterion therefore turns all of performance into "unconscious perception";
   showing a second system needs more than above-chance guessing, for instance zero objective sensitivity on the
   same trials, or metacognition that fails while discrimination succeeds.
3. **The copy ring.** Cut the ring into two arcs. Only two links cross the cut, one each way; across each, the node
   on the far side copies the near node's (uniformly random) state, carrying exactly 1 bit, and every other node of
   the receiving arc depends only on its own arc. So EI(A→B) = EI(B→A) = 1 and Φ = 2. A cut that interleaves the
   nodes crosses more links and carries more, so the minimum is at two arcs.
4. **Two loops.** Separate the loops. Each loop's next state depends only on itself, so neither part's state tells
   anything about the other's next state: EI = 0 both ways, this cut is the minimum, and Φ = 0, however much each loop
   carries. Integration, not information, is what Φ measures.
5. **The ramp.** Activity is reset at each crossing, so it is always below the threshold and its long-run average is
   lower still; just before a crossing it is, by definition, at the threshold. Averaging backward from crossings
   must therefore climb toward the threshold, whatever the drift.
6. **Rivalry's shape.** With noise 0.15 and adaptation 0.15 the simulated durations become more irregular (gamma
   shape near 2), because switches are driven more by noise than by fatigue; with little noise and strong adaptation
   they become regular (shape well above 10).
7. ★ **A no-report test.** Present faces and houses in rivalry, read the percept from eye movements or pupil size
   rather than a key press, and silence or stimulate dorsolateral prefrontal cortex (or test patients with
   prefrontal lesions). The workspace and higher-order theories predict that experience, read from the reflexes and
   from later memory, is disrupted; integrated information and recurrent processing predict it is not, if
   posterior cortex is intact.

## Open checks

* The Cogitate results (no prefrontal ignition at offset; orientation not decodable in prefrontal cortex; no
  sustained posterior synchrony) are summarized from the published paper and should be rechecked against it, with
  its volume and pages.
* Del Cul et al.'s visibility threshold near 50 ms, the Simons and Chabris rate (Part 18's row: 46%), the NAP5 rate
  of about one in twenty thousand, Schnakers et al.'s four in ten, and Bodien et al.'s quarter are quoted from the
  papers as widely reported; recheck before the final cut.
* The rivalry neurons' shares are drawn schematically (few in V1, more in V4, most in inferotemporal cortex), not to
  the papers' exact percentages.
* Φ here is Tononi's 2004 measure; IIT 3.0 and 4.0 compute it differently, and the film says so.
