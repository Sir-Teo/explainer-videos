# Psychology, Built: Part 16, Conditioning

Pair a signal with food and a dog comes to salivate at the signal; present the signal alone and the response fades;
wait a day and part of it is back. Something was learned in extinction, but it was not the erasure of the first
lesson. And two dogs with the same forty pairings can learn entirely different things, if food also comes, for one of
them, when there is no signal. This part follows those two puzzles to their answers: learning tracks contingency, it
is driven by surprise, and extinction is new learning bound to its context.

It opens Act IV. Pavlov's method and vocabulary, generalization and discrimination, and why the conditioned response
prepares rather than substitutes. Thorndike's cats and the law of effect; Watson's behaviourism and Little Albert, from
the paper's own notes and as retold. Skinner's chamber, shaping, and the four schedules of reinforcement with their
cumulative records. A contingency game for the viewer, ΔP, and Rescorla's 1968 random control. Kamin's blocking. The
Rescorla–Wagner rule, derived as gradient descent on a squared prediction error (Widrow and Hoff's delta rule), drawn
on its error surface, and run on overshadowing, conditioned inhibition and overexpectation; its asymptote proved to be
ΔP, and Rescorla's ten groups reproduced. What it gets wrong: latent inhibition, spontaneous recovery and renewal, with
a two-memory model of extinction; Mackintosh's and Pearce and Hall's learned attention; scalar timing and the I/T law
of rate-estimation theory; Herrnstein's matching law derived from melioration, and melioration as a trap. Biology's
limits: Garcia's taste aversions, the Brelands' misbehaving animals, preparedness, and Bandura's Bobo doll. The
practice chapter is exposure therapy, animal training and token economies, contingency management for addiction, and
loot boxes; the frontier is propositional learning, latent causes, and reconsolidation.

## Where the numbers come from

| What | Source |
|---|---|
| Pavlov's Nobel Prize (1904, digestion); signals were metronomes, buzzers, harmoniums, lights and touches, a bell only rarely | the Nobel record; Todes's biography (2014), as summarized by its publisher and reviewers |
| Acquisition, extinction and next-day recovery of a salivary response (drops) | Psyche (`conditioning.extinction_in_context`, α = 0.18, a 48-hour context drift; 12 drops at full strength), item `pavlov` |
| A generalization gradient over tone frequency | Psyche: a Gaussian in octaves, width 0.35; the shape, not a fit |
| Experimental neurosis (a circle and an ellipse made rounder) | Pavlov (1927), described without figures |
| Escape times in the puzzle box | Psyche (`puzzle_box`, 12 acts, Δw = 0.1): one cat (seed 12) and the median and quartiles of 200 |
| Watson and Rayner: no fear at about nine months; the bar at 8 months 26 days; two pairings at 11 months 3 days, five more at 11 months 10 days (seven in all); transfer at 11 months 15 days; last tests at 1 year 21 days; Albert taken from the hospital that day | the paper (Classics in the History of Psychology), read 2026-11-14 |
| Albert's identity disputed (Merritte, who died at six; Barger, who lived to 87) | Beck et al. (2009); Powell et al. (2014), from abstracts and summaries |
| Shaping: the criterion is the 60th percentile of the last 20 responses; 79% rewarded against 0.3% when waiting for the target | Psyche (`shaping`), item `shaping` |
| Cumulative records under FR 20, VR 20, FI 60 s and VI 60 s, with their rates | Psyche (`schedule`): the signatures as Ferster and Skinner (1957) describe them; the numbers are the model's |
| The fertilizer game: 24 plants, 12 fertilized, nine of each twelve bloom (ΔP = 0) | constructed (item `contingency`, a fixed seed for the order) |
| People's ratings follow ΔP; 150 people in three experiments | Wasserman, Elek, Chatlosh and Baker (1993), from the abstract |
| Rescorla (1968): 24 rats in Experiment 1; 80 rats in ten groups in Experiment 2; twelve 2-min tones a session for five sessions, an 8-min mean gap; 0.5 s, 0.9 mA shocks; the ten pairs of probabilities; the three statements of the discussion | the paper, read 2026-11-14 |
| Kamin's design and result (little fear of the light after noise training); unblocking with a stronger shock | Kamin (1969), from later accounts |
| The rule's curves, the error surface and the blocking path | Psyche (`rescorla_wagner`, αβ = 0.15), item `rw` |
| Overshadowing (α = 0.45 and 0.1), conditioned inhibition, overexpectation | Psyche, item `rw`; Kremer (1978) for overexpectation in rats |
| The asymptote V_X = ΔP with a context cue | derived here and in `rw_asymptote`; Chapman and Robbins (1990) |
| Rescorla's ten groups on Psyche: eight simulated rats a group, α = 0.12, β = 1 and 0.4, the median; suppression ratio e^(−8V)/(1 + e^(−8V)) | Psyche (`rescorla_1968`, `suppression_ratio`), item `rescorla68` |
| Latent inhibition in sheep and goats | Lubow and Moore (1959), from a review's account |
| Renewal after extinction in another context | Bouton and Bolles (1979); Psyche's two-memory model (similarity 0.15), item `extinction` |
| Mackintosh's and Pearce and Hall's attention on one history (A always rewarded, B half the time) | Psyche (`mackintosh`, `pearce_hall`), item `attention` |
| Scalar timing: a peak at the trained interval with a coefficient of variation of 0.2 | Psyche (`peak_curve`); the property as reviewed by Gallistel and Gibbon (2000) |
| Reinforcements to acquisition ≈ 300 (I/T)⁻¹ | Gallistel and Gibbon (2000), as summarized by Kakade and Dayan and later papers |
| Rescorla–Wagner's trials to V = 0.5 against I/T | Psyche (`rw_trials_to_criterion`), item `timing` |
| The matching law on seven pairs of variable-interval schedules; the generalized fit | Psyche (`concurrent`, melioration), item `choice` |
| Baum (1979): 103 data sets from 23 studies; undermatching common | the abstract and later reanalyses |
| The melioration trap (A pays 1 + 3f, B pays 3f) | constructed after Herrnstein and Prelec (1991); Psyche, 50 runs |
| Bright-noisy-tasty water; illness by X-rays or lithium chloride; long delays | Garcia and Koelling (1966); Garcia, Ervin and Koelling (1966), from records and later accounts |
| The raccoon and the pigs | Breland and Breland (1961), from excerpts and later accounts |
| 72 children (36 boys, 36 girls), Stanford nursery school | Bandura, Ross and Ross (1961) |
| Monkeys learn fear of snakes, not flowers, by watching | Cook and Mineka (1989), from memory |
| Contingency management: 47 comparisons, d = 0.42, 0.66 for cocaine, 0.65 for opiates; prize-based 0.46 at the end of treatment, 0.33 at three months, none at six | Prendergast et al. (2006); Benishek et al. (2014), from the abstracts |
| 7,422 gamers; η² = 0.054 for loot-box spending and problem gambling, 0.004 for other spending | Zendle and Cairns (2018) |
| Instructed fear; blocking that depends on beliefs about additivity | as reviewed by Mitchell, De Houwer and Lovibond (2009) |
| Gradual extinction in rats | Gershman, Jones, Norman, Monfils and Niv (2013), from memory |
| Reconsolidation update, and a year's follow-up | Schiller et al. (2010); replications mixed |

## Built in this part

* `explainer/psychology/psyche/conditioning.py`: Rescorla–Wagner for any design written as phases of trial types, its
  gradient, and its exact asymptote (so ΔP falls out); a contingency learner with a context cue; Rescorla's 1968
  schedule; a suppression read-out; Mackintosh's and Pearce and Hall's attention rules; a two-memory model of extinction
  bound to context, with renewal and spontaneous recovery; a generalization gradient; a law-of-effect learner in
  Thorndike's box; shaping by successive approximation; an operant chamber with the four schedules and cumulative
  records; concurrent schedules chosen by melioration, the generalized matching fit and a melioration trap; scalar
  timing, the I/T law, and Rescorla–Wagner's trials to criterion. Tested in `tests/psychology/test_conditioning.py`.
* The Ledger gains six rows, one of them (conditioned tolerance) deferred from Part 10; the Archive twenty-three datasets.
* The course's interactive is the contingency game: four blocks of plants, a rating after each, and the reader's
  ratings against ΔP and against the outcome's density.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A cue paired with an already-predicted outcome acquires little association | Kamin 1969 | replicated, smaller |
| Rats avoid a taste after illness and a light or sound after shock, not the reverse | Garcia and Koelling 1966 | replicated |
| Tolerance is partly conditioned to drug cues; a dose kills more often in a new place | Siegel, Hinson, Krank and McCully 1982 | replicated |
| An infant conditioned to fear a white rat shows how phobias are learned | Watson and Rayner 1920 | story and record |
| Animals divide responses between two sources in proportion to their rewards | Herrnstein 1961 | replicated |
| An extinguished fear returns in the context where it was learned | Bouton and Bolles 1979 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Pavlov (the method, told as
history), Ferster and Skinner (schedules whose signatures are drawn on Psyche), Wasserman et al. (human contingency
judgment, entered with judgment in Part 26), Rescorla (1968; a design reproduced on Psyche, the paper's figures not
drawn), Rescorla and Wagner (a model), Lubow and Moore (latent inhibition, described and modelled; its row is in Part 18), Mackintosh and
Pearce and Hall (models), Gallistel and Gibbon (a theory and a summary of data, with its exceptions), the Brelands
(trainers' observations), Bandura, Ross and Ross (described without figures), Prendergast et al. (treatment
evidence, entered in Part 42), Zendle and Cairns (a survey, with its limits), Mitchell et al. and Gershman et al.
(theory at the frontier), and Schiller et al. (reconsolidation, whose row is due in Part 21).

## Build it

```bash
python -m videos.psychology.psych16.compute            # every number (seconds), into .cache/psych16/
python tools/qa_scene.py psych16 RescorlaWagner        # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych16 -q l   # the whole part, silent preview
python tools/build.py psych16                          # 1080p30 with narration
python tools/qa_scene.py psych16 Choice --lang zh      # the Chinese edition of one chapter
python tools/make.py psych16                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 16                    # the lab: the rule, its asymptote, renewal, matching
python tools/check_ledger.py psych16                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's conditioning module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A response that comes back | Pavlov's laboratory; acquisition, extinction and recovery on Psyche; two dogs with the same pairings; objectives |
| 1 | Pavlov's method | US, UR, CS, CR; generalization and discrimination; substitution against preparation |
| 2 | The law of effect | Thorndike's cats; behaviourism; Little Albert as recorded, and as retold |
| 3 | Skinner's box | The chamber and the recorder; shaping; four schedules; partial reinforcement |
| 4 | Contingency, not pairing | The fertilizer game; ΔP and the outcome-density effect; Rescorla's ten groups |
| 5 | Blocking | Kamin's design; surprise and unblocking |
| 6 | The Rescorla-Wagner rule | The rule; its derivation as gradient descent; acquisition and extinction; blocking on the error surface |
| 7 | What the rule predicts | Overshadowing, inhibition, overexpectation; why the asymptote is ΔP; Rescorla's groups on Psyche |
| 8 | What the rule gets wrong | Latent inhibition; renewal and a two-memory model; spontaneous recovery |
| 9 | Attention to cues | Mackintosh against Pearce and Hall; one history, opposite attention; both, it seems |
| 10 | Time | Scalar timing; the I/T law and rate estimation |
| 11 | Choice | The matching law; melioration derives it; when melioration is a trap |
| 12 | Biology's limits | Garcia and Koelling; instinctive drift and preparedness; learning by watching |
| 13 | The Ledger | Blocking; taste aversion; conditioned tolerance; Little Albert; matching; renewal |
| 14 | In practice: therapy, training and games | Exposure; clickers and token economies; contingency management; loot boxes |
| 15 | Frontier: links, beliefs and hidden causes | What is solid and argued; propositions; latent causes; reconsolidation |
| | Recap, problems, and the road ahead | Ten lines; the first and second objections; payoffs; problems; references; Part 17 |

## Sources

**Books.** I. P. Pavlov, *Conditioned Reflexes*, trans. G. V. Anrep (Oxford University Press, 1927). D. P. Todes, *Ivan
Pavlov: A Russian Life in Science* (Oxford University Press, 2014). B. F. Skinner, *The Behavior of Organisms*
(Appleton-Century, 1938). C. B. Ferster and B. F. Skinner, *Schedules of Reinforcement* (Appleton-Century-Crofts, 1957).
M. E. Bouton, *Learning and Behavior: A Contemporary Synthesis*, 2nd ed. (Sinauer, 2016).

**Papers.** E. L. Thorndike, Animal intelligence, *Psychol. Rev. Monogr. Suppl.* 2(4) (1898). J. B. Watson and R.
Rayner, Conditioned emotional reactions, *J. Exp. Psychol.* 3 (1920) 1–14. B. Harris, Whatever happened to Little
Albert?, *Am. Psychol.* 34 (1979) 151–160. R. A. Powell, N. Digdon, B. Harris and C. Smithson, Correcting the record on
Watson, Rayner, and Little Albert, *Am. Psychol.* 69 (2014) 600–611. R. A. Rescorla, Probability of shock in the
presence and absence of CS in fear conditioning, *J. Comp. Physiol. Psychol.* 66 (1968) 1–5. L. J. Kamin,
Predictability, surprise, attention, and conditioning, in B. A. Campbell and R. M. Church (eds), *Punishment and
Aversive Behavior* (1969) 279–296. R. A. Rescorla and A. R. Wagner, A theory of Pavlovian conditioning, in A. H. Black
and W. F. Prokasy (eds), *Classical Conditioning II* (1972) 64–99. B. Widrow and M. E. Hoff, Adaptive switching
circuits, *IRE WESCON Convention Record* (1960) 96–104. E. F. Kremer, The Rescorla–Wagner model: losses in associative
strength in compound conditioned stimuli, *J. Exp. Psychol. Anim. Behav. Process.* 4 (1978) 22–36. G. B. Chapman and
S. J. Robbins, Cue interaction in human contingency judgment, *Mem. Cognit.* 18 (1990) 537–545. E. A. Wasserman, S. M.
Elek, D. L. Chatlosh and A. G. Baker, Rating causal relations, *J. Exp. Psychol. Learn. Mem. Cogn.* 19 (1993) 174–188.
R. E. Lubow and A. U. Moore, Latent inhibition, *J. Comp. Physiol. Psychol.* 52 (1959) 415–419. M. E. Bouton and R. C.
Bolles, Contextual control of the extinction of conditioned fear, *Learn. Motiv.* 10 (1979) 445–466. B. Vervliet, M. G.
Craske and D. Hermans, Fear extinction and relapse, *Annu. Rev. Clin. Psychol.* 9 (2013) 215–248. N. J. Mackintosh, A
theory of attention, *Psychol. Rev.* 82 (1975) 276–298. J. M. Pearce and G. Hall, A model for Pavlovian learning,
*Psychol. Rev.* 87 (1980) 532–552. M. E. Le Pelley, The role of associative history in models of associative learning,
*Q. J. Exp. Psychol.* 57B (2004) 193–243. C. R. Gallistel and J. Gibbon, Time, rate, and conditioning, *Psychol. Rev.*
107 (2000) 289–344. R. J. Herrnstein, Relative and absolute strength of response as a function of frequency of
reinforcement, *J. Exp. Anal. Behav.* 4 (1961) 267–272. W. M. Baum, Matching, undermatching, and overmatching in
studies of choice, *J. Exp. Anal. Behav.* 32 (1979) 269–281. R. J. Herrnstein and D. Prelec, Melioration: a theory of
distributed choice, *J. Econ. Perspect.* 5 (1991) 137–156. J. Garcia and R. A. Koelling, Relation of cue to
consequence in avoidance learning, *Psychon. Sci.* 4 (1966) 123–124. J. Garcia, F. R. Ervin and R. A. Koelling,
Learning with prolonged delay of reinforcement, *Psychon. Sci.* 5 (1966) 121–122. M. Domjan and N. E. Wilson,
Specificity of cue to consequence in aversion learning in the rat, *Psychon. Sci.* 26 (1972) 143–145. S. Siegel, R. E. Hinson, M. D. Krank and J. McCully, Heroin "overdose" death, *Science* 216 (1982) 436–437. S. Siegel and B. M. C. Ramos, Applying laboratory research: drug anticipation and the treatment of drug addiction, *Exp. Clin. Psychopharmacol.* 10 (2002) 162–183. K. Breland and
M. Breland, The misbehavior of organisms, *Am. Psychol.* 16 (1961) 681–684. A. Bandura, D. Ross and S. A. Ross,
Transmission of aggression through imitation of aggressive models, *J. Abnorm. Soc. Psychol.* 63 (1961) 575–582. M.
Cook and S. Mineka, Observational conditioning of fear to fear-relevant versus fear-irrelevant stimuli in rhesus
monkeys, *J. Abnorm. Psychol.* 98 (1989) 448–459. T. Maes et al., The elusive nature of the blocking effect: 15
failures to replicate, *J. Exp. Psychol. Gen.* 145 (2016) e49–e71. M. Prendergast et al., Contingency management for
treatment of substance use disorders: a meta-analysis, *Addiction* 101 (2006) 1546–1560. L. A. Benishek et al.,
Prize-based contingency management for the treatment of substance abusers: a meta-analysis, *Addiction* 109 (2014)
1426–1436. D. Zendle and P. Cairns, Video game loot boxes are linked to problem gambling, *PLoS ONE* 13 (2018) e0206767.
C. J. Mitchell, J. De Houwer and P. F. Lovibond, The propositional nature of human associative learning, *Behav. Brain
Sci.* 32 (2009) 183–198. S. J. Gershman, D. M. Blei and Y. Niv, Context, learning, and extinction, *Psychol. Rev.* 117
(2010) 197–209. D. Schiller et al., Preventing the return of fear in humans using reconsolidation update mechanisms,
*Nature* 463 (2010) 49–53.

## Problems and solutions

**1. The rule by hand.** With one cue and λ = 1, V_{n+1} = V_n + 0.2(1 − V_n), so 1 − V_{n+1} = 0.8(1 − V_n) and
V_n = 1 − 0.8ⁿ. V reaches 0.9 when 0.8ⁿ ≤ 0.1, n ≥ ln 0.1 / ln 0.8 = 10.3: on the eleventh trial.

**2. Gradient descent.** E = ½(λ − Σᵢ xᵢVᵢ)², so ∂E/∂V_X = −(λ − Σᵢ xᵢVᵢ)x_X. A step of size η against the gradient is
ΔV_X = η(λ − ΣV)x_X, the Rescorla–Wagner rule for every cue present (x_X = 1) and no change for absent ones, with
η = α_Xβ. A larger αβ is a longer step: faster learning, and, above 1/(number of cues present), overshoot.

**3. The asymptote is ΔP.** Trials with the cue (probability q) carry C and X, with the outcome at p₁; trials without
it (1 − q) carry C alone, with the outcome at p₀. With equal β the expected changes are
E[ΔV_X] ∝ q(p₁ − V_C − V_X) and E[ΔV_C] ∝ q(p₁ − V_C − V_X) + (1 − q)(p₀ − V_C). Setting both to zero gives V_C + V_X = p₁
and then V_C = p₀, so V_X = p₁ − p₀ = ΔP for every q in (0, 1). With β for outcomes larger than for their absence the
asymptote is no longer ΔP, and before the asymptote a frequent outcome inflates V_X (the outcome-density effect).

**4. Overexpectation.** On an AB trial the error is 1 − (V_A + V_B) = 1 − 2 = −1, so both lose strength although the
food arrives. With equal α both fall by the same amount each trial (their difference never changes) until
V_A + V_B = 1: each ends at 0.5. With unequal α the more salient cue loses more, and the difference between them is
kept.

**5. Matching from melioration.** The chooser shifts toward the key with the higher local rate, R/B, and stops only
when R_L/B_L = R_R/B_R. Then B_L/B_R = R_L/R_R, and adding 1 to each side, B_L/(B_L + B_R) = R_L/(R_L + R_R). On
variable-interval keys this equality is reachable, because spending less time on a key raises its local rate (its
rewards wait to be collected); on ratio keys the local rates are fixed, so the chooser cannot equalize them and goes to
the richer key.

**6. Fixing renewal.** In `extinction_in_context` all excitation is context-free, so AAB = ABC. Split it: a share ω of
what acquisition writes is stored with the context of acquisition, expressed elsewhere with similarity s. With ω = 0.4,
s = 0.15 and acquisition complete, extinction in A must cancel 0.6 + 0.4 = 1, so I_A = 1, and a test in B gives
0.6 + 0.15 × 0.4 − 0.15 × 1 = 0.51. In ABC, extinction in B cancels 0.6 + 0.06 = 0.66, and a test in C gives
0.6 + 0.06 − 0.15 × 0.66 = 0.56; in ABA, 0.6 + 0.4 − 0.15 × 0.66 = 0.90. The order ABA > ABC > AAB is the one in the
data.

**7. ★ Two theories of attention.** Learned predictiveness (after Le Pelley and McLaren): in phase 1, cue A is always
followed by outcome 1 and cue B is followed by it on a random half of trials; in phase 2, A and B are both paired with
a new outcome, each in compound with a novel cue, and learning about each is measured at test (and attention by eye
tracking). Mackintosh predicts faster new learning about A, the cue that predicted well; Pearce and Hall predict faster
learning about B, the cue whose consequences were uncertain. Counterbalance which physical stimuli play A and B, and
include a phase-2 condition where all cues are new, to measure learning with no history.

## Where it comes back

Prediction errors in dopamine neurons: Part 17. Attention: Part 18. Memory rewritten when it is used: Part 21. Choices
over time: Part 26. Fear, exposure and relapse: Part 40. Addiction: Part 41. Does therapy work?: Part 42. Products
designed around habits: Part 52. Psyche's `conditioning` module supplies the learning rules those parts extend.

## Open checks

Before the narrated master:

* The rarity of the bell in Pavlov's laboratory is Todes's finding as summarized by others; his book was not read.
* Pavlov's experimental neurosis and the mistranslation of "conditional" are the usual history.
* Thorndike's puzzle-box details (the loop, the timing) are from historical accounts; his own curves are not drawn.
* Watson's 1913 manifesto and the forty years of influence are the usual history.
* Barger's age at death (87) and that he never knew are from accounts of Powell et al. (2014).
* Kamin's unblocking with a stronger shock is from later accounts.
* Chapman and Robbins (1990) are credited for the ΔP asymptote from later citations; the derivation here stands on its own.
* The 300 (I/T)⁻¹ summary is quoted from accounts of Gallistel and Gibbon (2000), not from the paper.
* The Brelands' raccoon and pigs are from excerpts; Cook and Mineka (1989) and the gradual-extinction study (Gershman et
  al. 2013) are from memory.
* Schiller et al.'s one-year follow-up is from memory; "replications mixed" summarizes later reviews.
* The token-economy history (wards in the 1960s; consent) is described without figures.
