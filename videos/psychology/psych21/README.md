# Psychology, Built: Part 21, Memory II: Forgetting and Inventing

In 1974 Elizabeth Loftus and John Palmer changed one word in a question about a film of a car crash, and a week later
the people who had heard "smashed" remembered broken glass that was never there. This part follows memory's two
failures, losing what it had and gaining what it never had, and finds that both come from the same design: a memory
that keeps the gist, rewrites itself when used, and has to infer where its contents came from.

Ebbinghaus's curve and three replications (Heller, Mack and Seitz's two subjects in 1991, Dros's seventy hours in
2015) with four laws fitted and compared by AIC; Jost's law from the hazard of a power law; the averaging artefact,
derived; Jenkins and Dallenbach's sleepers, Underwood's proactive interference, retroactive interference in a linear
associator, and retrieval-induced forgetting; consolidation from Müller and Pilzecker and Ribot to a two-store model
solved in closed form, replay in sleep, targeted memory reactivation, and reconsolidation with its record in people;
catastrophic interference and complementary learning systems, with Rumelhart's semantic network taught the penguin,
focused or interleaved; spacing from Ebbinghaus to Cepeda's ridgeline, with Pavlik and Anderson's model; the testing
effect and its metacognitive illusion, with the bifurcation model fitted to Roediger and Karpicke; Bartlett's War of
the Ghosts and the category adjustment model derived; the DRM illusion on you and by global matching;
misinformation, source monitoring, implanted memories and the verbal-overshadowing Registered Replication Report
pooled from its open data; flashbulb memories, eyewitness confidence and the confidence-accuracy characteristic by
signal detection; S., superior autobiographical memory, and why a good memory forgets. The practice chapter is study
techniques, spaced-repetition software with half-life regression fitted and checked on held-out practice, and
line-ups, interviews and therapy; the frontier is weakening a memory by reconsolidation, silent engrams, and
forgetting in machines.

## Where the numbers come from

| What | Source |
|---|---|
| Speed estimates of 40.8, 39.3, 38.1, 34.0 and 31.8 mph for smashed, collided, bumped, hit and contacted; broken glass reported by 16, 7 and 6 of 50 | Loftus and Palmer (1974), from summaries of the paper's two experiments |
| Savings after 20 minutes to 31 days for Ebbinghaus, Mack, Seitz and Dros | Murre and Dros (2015), Table 3 (CC BY) |
| AIC of the four laws for each person: the power law best for Ebbinghaus, Mack and Seitz, the logarithm for Dros | Psyche (`memory.fit_law`), item `laws` |
| Underwood's estimate that forgetting in a day falls from about 75% to about 25% without prior lists | Underwood (1957), from the abstract; the curve drawn is a schematic of its shape |
| Retroactive interference against the overlap of the second list's cues | Psyche (`memory.associator_interference`), item `interference` |
| Ribot's gradient in a two-store model | Psyche (`memory.two_store`), schematic rates, item `consolidate` |
| The penguin, focused or interleaved | Psyche (`memory.penguin_experiment`), item `penguin` |
| 1,354 people, 32 facts, gaps up to 105 days, retention intervals of 7, 35, 70 and 350 days, 26 combinations; optimal gaps about 20 to 40% of a week and 5 to 10% of a year | Cepeda, Vul, Rohrer, Wixted and Pashler (2008), the paper |
| The model's best gaps for the four retention intervals | Psyche (`memory.spacing_ridge`), item `spacing` |
| Restudy 81, 54, 42% and test 75, 68, 56% at 5 minutes, 2 days and a week; SSSS, SSST, STTT 83, 78, 71% at 5 minutes and 40, 56, 61% at a week; predictions 4.8, 4.2, 4.0; about 70% recalled on the initial tests | Roediger and Karpicke (2006), the paper |
| The bifurcation model's five parameters and its predicted initial-test recall | Psyche (`memory.fit_bifurcation`), item `testing` |
| Bias and error of the category adjustment model for three trace noises | Psyche (`memory.category_adjustment`), item `adjust` |
| Recall of studied words .65 and of the lure .40; recognition .86 and .84 (Experiment 1); lure recall .55 and 72% of lures called old judged remembered (Experiment 2) | Roediger and McDermott (1995), the paper |
| The DRM illusion by global matching | Psyche (`memory.drm_global_matching`), item `drm` |
| 24 people, about a quarter; 423 people in eight studies, 30.4%; a preregistered replication of 123, 35% | Loftus and Pickrell (1995), Scoboria et al. (2017), Murphy et al. (2023), from abstracts and summaries |
| Every lab's correct identifications in the two verbal-overshadowing replications; the originals' 17 of 44 against 28 of 44 (Study 1) and 18 of 37 against 27 of 38 (Study 4) | Alogna et al. (2014), the two data workbooks (osf.io/ybeur), fetched by `explainer.psychology.opendata` and checked by SHA-256, item `overshadow` |
| 54 students on 12 September 2001, retested after 1, 6 or 32 weeks | Talarico and Rubin (2003), from the abstract |
| The confidence-accuracy characteristic for three memory strengths | Psyche (`memory.lineup_cac`), item `lineup` |
| 20 people with superior autobiographical memory and 38 controls | Patihis et al. (2013), from the abstract |
| Ten study techniques in three bands | Dunlosky et al. (2013), from the abstract and summary table |
| 13 million practice traces; error 45% or more below the baselines; 12% more daily engagement | Settles and Meeder (2016), from the abstract |
| Half-life regression fitted to simulated learners, held out, and compared with a single average and Leitner's boxes | Psyche (`memory.hlr_simulate`, `memory.fit_hlr`), item `hlr` |

## Built in this part

* `explainer/psychology/psyche/memory.py` gains Part 21: four forgetting laws with AIC, Jost's law, the gamma mixture
  of exponentials; A-B, A-C interference in a linear associator; a two-store model of consolidation; Rumelhart's
  semantic network with the penguin learnt focused or interleaved; Pavlik and Anderson's activation with
  activation-dependent decay, and the spacing ridge; the bifurcation model and its fit; the category adjustment
  model; the DRM illusion by global matching; line-ups by signal detection with the confidence-accuracy
  characteristic; half-life regression, simulated and fitted. Tested in `tests/psychology/test_forget.py`.
* `explainer/psychology/opendata.py` gains the verbal-overshadowing Registered Replication Report's two workbooks,
  read with the standard library.
* The Ledger gains eight rows, including the forgetting curve deferred from Part 20; the Archive twelve datasets.
* The course's interactive is a DRM experiment: four lists, each built around a word it leaves out, and a
  remember/know/new test.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Memory falls fast and then ever more slowly | Ebbinghaus 1885 | replicated |
| Spaced study beats massed study, with a best gap that grows with the retention interval | Ebbinghaus 1885 | replicated |
| Retrieval improves long-term retention more than restudy | Roediger and Karpicke 2006 | replicated |
| People recall and recognise an unpresented associate | Roediger and McDermott 1995 | replicated |
| Misleading post-event information enters reports of the event | Loftus and Palmer 1974 | replicated |
| Suggested childhood events come to be remembered by a minority | Loftus and Pickrell 1995 | replicated |
| Reactivated human memories can be updated by new learning | Walker et al. 2003 | contested |
| Describing a face impairs identifying it | Schooler and Engstler-Schooler 1990 | replicated, smaller |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Jenkins and Dallenbach and
Underwood (history of a debate whose conclusion is the interference rows' background), Anderson, Bjork and Bjork with
Murayama et al. (a meta-analysed effect whose mechanism is argued; described), Müller and Pilzecker, Ribot, Wilson and
McNaughton, Rasch et al. and Nader et al. (consolidation's history and neuroscience; the human claim is the
reconsolidation row), McCloskey and Cohen and McClelland, McNaughton and O'Reilly (models), Pavlik and Anderson,
Kornell, Bjork and Garcia, and Huttenlocher, Hedges and Duncan (models), Bartlett and Bergman and Roediger (a
classic method, described with its caution), Johnson, Hashtroudi and Lindsay (a framework), Talarico and Rubin and
Wixted and Wells (Part 56's rows), Wixted and Mickes (a model), Luria and Parker, Cahill and McGaugh (single cases),
Patihis et al. (in the DRM row's record), Richards and Frankland (a theoretical argument), Dunlosky et al. (a review;
Part 54), Wells et al. and Garry et al. (Part 56), Kindt et al., Brunet et al., Ryan et al. and Kirkpatrick et al.
(frontier).

## Build it

```bash
python -m videos.psychology.psych21.compute            # every number (about a minute; fetches the open data once)
python tools/qa_scene.py psych21 Testing               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych21 -q l   # the whole part, silent preview
python tools/build.py psych21                          # 1080p30 with narration
python tools/qa_scene.py psych21 Drm --lang zh         # the Chinese edition of one chapter
python tools/make.py psych21                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 21                    # the lab: forgetting laws to half-life regression
python tools/check_ledger.py psych21                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's memory module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Smashed or hit? | Loftus and Palmer's two experiments; the DRM list and test on you; the questions; objectives |
| 1 | The shape of forgetting | Four people's savings; four laws and AIC; Jost's law from the hazard; the averaging artefact derived |
| 2 | Why we forget | Decay or interference; the sleepers; proactive interference; an associator's retroactive interference; retrieval-induced forgetting |
| 3 | Consolidation | Müller and Pilzecker, Ribot and H.M.; two stores derived; replay and targeted reactivation; reconsolidation |
| 4 | Two ways to learn | Catastrophic interference; Rumelhart's network; the penguin, focused or interleaved; complementary learning systems |
| 5 | Spacing | The effect; Cepeda's ridgeline; Pavlik and Anderson's model and its ridge; three accounts |
| 6 | Testing | Roediger and Karpicke's crossover and the illusion; the bifurcation model derived and fitted |
| 7 | Remembering as rebuilding | Bartlett and its replication; Huttenlocher's dots; the category adjustment model derived and computed |
| 8 | Words that were never there | Your test scored; Roediger and McDermott; global matching derived; three accounts |
| 9 | Suggestion | Misinformation; source monitoring; lost in the mall and its replications; verbal overshadowing, lab by lab |
| 10 | Confidence and accuracy | Flashbulb memories; the witness in court; a line-up by signal detection; the confidence-accuracy characteristic |
| 11 | Remembering too much | S.; superior autobiographical memory and false memory; why a good memory forgets |
| 12 | The Ledger | The forgetting curve; spacing; testing; DRM; misinformation; implantation; reconsolidation in people; verbal overshadowing |
| 13 | In practice: study, apps, line-ups | Ten techniques rated; Leitner, SuperMemo and half-life regression fitted and checked; line-ups, interviews, therapy |
| 14 | Frontier: editing memory | Weakening fear by reconsolidation; silent engrams; elastic weight consolidation, replay and unlearning |
| | Recap, problems, and the road ahead | Ten lines; the first two objections; payoffs; problems; references; Part 22 |

## Sources

* E. F. Loftus and J. C. Palmer, Reconstruction of automobile destruction, Journal of Verbal Learning and Verbal
  Behavior 13 (1974) 585-589.
* H. Ebbinghaus, Über das Gedächtnis (1885); J. M. J. Murre and J. Dros, Replication and analysis of Ebbinghaus'
  forgetting curve, PLoS ONE 10 (2015) e0120644; O. Heller, W. Mack and J. Seitz, Zeitschrift für Psychologie 199
  (1991) 3-18.
* J. T. Wixted and E. B. Ebbesen, On the form of forgetting, Psychological Science 2 (1991) 409-415; R. B. Anderson
  and R. D. Tweney, Artifactual power curves in forgetting, Memory & Cognition 25 (1997) 724-730.
* J. G. Jenkins and K. M. Dallenbach, Obliviscence during sleep and waking, American Journal of Psychology 35 (1924)
  605-612; B. J. Underwood, Interference and forgetting, Psychological Review 64 (1957) 49-60.
* M. C. Anderson, R. A. Bjork and E. L. Bjork, Remembering can cause forgetting, Journal of Experimental Psychology:
  Learning, Memory, and Cognition 20 (1994) 1063-1087; K. Murayama, T. Miyatsu, D. Buchli and B. C. Storm, Forgetting
  as a consequence of retrieval: a meta-analytic review of retrieval-induced forgetting, Psychological Bulletin 140
  (2014) 1383-1409.
* G. E. Müller and A. Pilzecker, Experimentelle Beiträge zur Lehre vom Gedächtniss (1900); P. Alvarez and L. R.
  Squire, Memory consolidation and the medial temporal lobe: a simple network model, PNAS 91 (1994) 7041-7045.
* M. A. Wilson and B. L. McNaughton, Reactivation of hippocampal ensemble memories during sleep, Science 265 (1994)
  676-679; B. Rasch, C. Büchel, S. Gais and J. Born, Odor cues during slow-wave sleep prompt declarative memory
  consolidation, Science 315 (2007) 1426-1429.
* K. Nader, G. E. Schafe and J. E. LeDoux, Nature 406 (2000) 722-726; M. P. Walker et al., Nature 425 (2003) 616-620;
  T. E. Hardwicke, M. Taqi and D. R. Shanks, PNAS 113 (2016) 5206-5211.
* M. McCloskey and N. J. Cohen, Catastrophic interference in connectionist networks: the sequential learning
  problem, Psychology of Learning and Motivation 24 (1989) 109-165; J. L. McClelland, B. L. McNaughton and R. C.
  O'Reilly, Why there are complementary learning systems in the hippocampus and neocortex, Psychological Review 102
  (1995) 419-457; T. T. Rogers and J. L. McClelland, Semantic Cognition (2004).
* N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted and D. Rohrer, Psychological Bulletin 132 (2006) 354-380; N. J.
  Cepeda, E. Vul, D. Rohrer, J. T. Wixted and H. Pashler, Psychological Science 19 (2008) 1095-1102; P. I. Pavlik and
  J. R. Anderson, Cognitive Science 29 (2005) 559-586.
* H. L. Roediger III and J. D. Karpicke, Psychological Science 17 (2006) 249-255; N. Kornell, R. A. Bjork and M. A.
  Garcia, Journal of Memory and Language 65 (2011) 85-97; C. A. Rowland, Psychological Bulletin 140 (2014) 1432-1463.
* F. C. Bartlett, Remembering (1932); E. T. Bergman and H. L. Roediger III, Memory & Cognition 27 (1999) 937-947;
  J. Huttenlocher, L. V. Hedges and S. Duncan, Categories and particulars, Psychological Review 98 (1991) 352-376.
* H. L. Roediger III and K. B. McDermott, JEP: LMC 21 (1995) 803-814; J. Arndt and E. Hirshman, Journal of Memory and
  Language 39 (1998) 371-391; D. A. Gallo, Memory & Cognition 38 (2010) 833-848.
* E. F. Loftus, D. G. Miller and H. J. Burns, JEP: HLM 4 (1978) 19-31; M. K. Johnson, S. Hashtroudi and D. S.
  Lindsay, Source monitoring, Psychological Bulletin 114 (1993) 3-28; E. F. Loftus and J. E. Pickrell, Psychiatric
  Annals 25 (1995) 720-725; A. Scoboria et al., Memory 25 (2017) 146-163; G. Murphy et al., Memory 31 (2023) 711-724.
* J. W. Schooler and T. Y. Engstler-Schooler, Cognitive Psychology 22 (1990) 36-71; C. A. Meissner and J. C. Brigham,
  Applied Cognitive Psychology 15 (2001) 603-616; V. K. Alogna et al., Perspectives on Psychological Science 9 (2014)
  556-578.
* R. Brown and J. Kulik, Flashbulb memories, Cognition 5 (1977) 73-99; J. M. Talarico and D. C. Rubin, Psychological
  Science 14 (2003) 455-461; J. T. Wixted and G. L. Wells, Psychological Science in the Public Interest 18 (2017)
  10-65; J. T. Wixted and L. Mickes, Psychological Review 121 (2014) 262-276; G. L. Wells et al., Law and Human
  Behavior 44 (2020) 3-36.
* A. R. Luria, The Mind of a Mnemonist (1968); E. S. Parker, L. Cahill and J. L. McGaugh, Neurocase 12 (2006) 35-49;
  L. Patihis et al., PNAS 110 (2013) 20947-20952; B. A. Richards and P. W. Frankland, The persistence and
  transience of memory, Neuron 94 (2017) 1071-1084.
* J. Dunlosky et al., Psychological Science in the Public Interest 14 (2013) 4-58; B. Settles and B. Meeder, A
  trainable spaced repetition model for language learning, ACL (2016) 1848-1858; M. Garry, C. G. Manning, E. F.
  Loftus and S. J. Sherman, Imagination inflation, Psychonomic Bulletin & Review 3 (1996) 208-214.
* M. Kindt, M. Soeter and B. Vervliet, Nature Neuroscience 12 (2009) 256-258; A. Brunet et al., American Journal of
  Psychiatry 175 (2018) 427-433; T. J. Ryan, D. S. Roy, M. Pignatelli, A. Arons and S. Tonegawa, Science 348 (2015)
  1007-1013; J. Kirkpatrick et al., Overcoming catastrophic forgetting in neural networks, PNAS 114 (2017) 3521-3526.

## Problems and solutions

**1. The power law and its hazard.** Fit $S = a t^{-b}$ to Ebbinghaus's savings by least squares on $\log S$ against $\log t$, and show that its hazard $-d \ln S / dt$ is $b/t$.

*Solution.* log S = log a − b log t is linear in log t, so least squares on the logs gives
b as minus the slope; on Ebbinghaus's seven savings it is about 0.13 (the curve-space fit of chapter 1 weights the
points differently and gives a similar value). −d ln S/dt = −d/dt(ln a − b ln t) = b/t, which falls with age: Jost's
second law. An exponential's hazard is 1/τ, the same at every age.

**2. Averaged exponentials.** Prove that if $\lambda \sim \mathrm{Gamma}(k, \theta)$, then $E\,e^{-\lambda t} = (1 + \theta t)^{-k}$, and say why this warns against reading a single trace's law off an average.

*Solution.* With λ ~ Gamma(k, θ), E e^{−λt} = ∫ e^{−λt} λ^{k−1} e^{−λ/θ}/(Γ(k)θ^k) dλ =
(1/θ^k) / (1/θ + t)^k = (1 + θt)^{−k}, the Laplace transform of the gamma density. A power-law average is therefore
consistent with every trace being exponential; the law of a single trace cannot be read off an average over traces
(or items, or people) that differ in rate.

**3. Two stores.** Solve $\dot h = -a h$, $\dot c = k h - b c$ from $h(0) = 1$, $c(0) = 0$, and find the age at which $c$ peaks.

*Solution.* h = e^{−at}. Then ċ + bc = k e^{−at}; multiplying by e^{bt}, d(c e^{bt})/dt = k e^{(b−a)t}, so
c e^{bt} = k (e^{(b−a)t} − 1)/(b − a) and c = k (e^{−bt} − e^{−at})/(a − b). Setting ċ = 0: b e^{−bt} = a e^{−at},
so t* = ln(a/b)/(a − b). With a = 0.3 and b = 0.004, t* = ln 75/0.296 ≈ 14.6 time units: after a lesion, memories of
about that age are the best kept.

**4. Feedback in the bifurcation model.** In the bifurcation model, give feedback after the initial test so that failed items gain $g_f$. How does the crossover delay move as $g_f$ grows?

*Solution.* With feedback, items that fail the initial test gain g_f instead of
nothing. At g_f = 0 the crossover is the one fitted. As g_f grows, the tested group's distribution no longer leaves
a block of weak items behind, so testing's advantage appears at shorter delays; once the average gain of the tested
group exceeds the restudy gain, testing wins at every delay, and the crossover disappears. Run `memory.bifurcation`
with the failed items' gain added to see the delay move toward zero.

**5. The category adjustment model.** Show that $\hat{x} = \lambda y + (1 - \lambda) \rho$ with $\lambda = \sigma_c^2 / (\sigma_c^2 + \sigma_y^2)$ minimises $E(\hat{x} - x)^2$, and that the minimum is $\lambda \sigma_y^2$.

*Solution.* E(x̂ − x)² with x̂ = λy + (1 − λ)ρ, y = x + ε, x = ρ + δ (independent, with
variances σ_y² and σ_c²): x̂ − x = λε − (1 − λ)δ, so E(x̂ − x)² = λ²σ_y² + (1 − λ)²σ_c². Differentiating,
2λσ_y² − 2(1 − λ)σ_c² = 0 gives λ = σ_c²/(σ_c² + σ_y²), and substituting gives σ_y²σ_c²/(σ_c² + σ_y²) = λσ_y².

**6. Pooling the replication.** With `explainer.psychology.opendata`: pool the second overshadowing replication yourself, fixed and random effects, and test whether the original's effect lies in the pooled interval.

*Solution.* For each lab, d_i = p_verbal − p_control with variance p(1−p)/n summed over the two
groups. The fixed-effect estimate is Σ w_i d_i / Σ w_i with w_i = 1/v_i; DerSimonian and Laird's τ² is
max(0, (Q − (k − 1))/(Σw − Σw²/Σw)) with Q = Σ w_i (d_i − d̄)². For the second replication τ² is zero, so the two
estimates agree; the original's −25 points lies well outside the pooled interval, which is the sense in which the
effect replicated smaller. `compute_overshadow` in this part's `compute.py` does exactly this.

**7. ★ Feedback and the memory.** Design a line-up study that could tell whether confidence inflation after feedback changes the memory itself, or only the report.

*Solution.* Show witnesses a line-up, record confidence at once, and then give confirming,
disconfirming or no feedback. Later, test the same witnesses with a new line-up in which the earlier choice and the
culprit are both present (or with a forced choice between them), with confidence. If feedback changes only the
report, later choices among the faces are unchanged and only confidence moves; if it changes the memory, later
choices shift toward the confirmed face, even when confidence is measured by a method blind to the feedback. Fit
the signal-detection model of chapter 10 to both sessions and ask whether feedback moves the criteria or the
distributions.

## Where it comes back

Concepts, categories and the penguin again: Part 22. Memory across the lifespan: Part 31. Fear, trauma and their
treatment: Part 40. Fitting and comparing models: Part 48. Spacing, testing and the classroom: Part 54. Witnesses,
line-ups and the courtroom: Part 56. Forgetting in machines: Part 60. Psyche's `memory` module supplies the forgetting
laws, the spacing and testing models, the line-up model and half-life regression those parts extend.

## Open checks

Before the narrated master:

* Loftus and Palmer's speed estimates and broken-glass counts are from summaries; read the 1974 paper.
* Jenkins and Dallenbach's design (two subjects, ten-syllable lists, 1 to 8 hours) is from reviews; none of their
  numbers is shown.
* Underwood's 75% and 25% are from his abstract; the curve drawn is a schematic.
* Talarico and Rubin's sample and schedule are from the abstract; the curves are schematic.
* Neisser and Harsch's numbers are not shown; the account is from secondary summaries.
* The Settles and Meeder figures (13 million traces, 45%, 12%) are from the abstract.
* Rowland's meta-analytic effect of about half a standard deviation is from secondary summaries.
