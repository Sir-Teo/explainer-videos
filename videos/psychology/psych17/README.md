# Psychology, Built: Part 17, Reward and Prediction

A monkey gets an unannounced drop of juice and a dopamine neuron fires. After training, the neuron fires at the light
that predicts the juice and not at the juice; when the juice is withheld it falls silent at the moment it was due. In
1997 those recordings were laid beside the temporal-difference error of reinforcement learning, δ = r + γV′ − V, and
they matched. This part derives that error, runs it, and follows it from prediction to action, exploration, maps,
habits and plans, and on to what dopamine does besides.

Credit over time and second-order conditioning; value as discounted future reward; the Bellman equation and the TD
error derived (Sutton 1988), with Samuel's checkers and backgammon as history; a tapped delay line for time inside a
trial; the error's migration from reward to cue, computed, and Steinberg et al.'s optogenetic unblocking; actor and
critic, Q-learning and the softmax, the basal ganglia's Go and NoGo pathways and Frank et al.'s patients with
Parkinson's disease; a reversal bandit played by Psyche, its learning rate read back by maximum likelihood and checked
by parameter recovery; five exploration policies and their regret, and directed and random exploration in people;
Tolman and Honzik's latent learning on a planner and a learner without a map, cognitive maps, place and grid cells;
devaluation and habits, Daw et al.'s two-step task with its stay-probability signatures and the argument over what they
mean; the successor representation, reward and transition revaluation, and replay; dopamine ramps, movement and
salience signals, and a distributional code; Redish's model of a drug that cannot be predicted away. The practice
chapter is recommender systems and bandit tests, impulse-control disorders on dopamine agonists, and habits; the
frontier is learning to learn in prefrontal cortex.

## Where the numbers come from

| What | Source |
|---|---|
| Schultz's three recordings (unpredicted juice, a predicting cue, an omitted reward) | Schultz, Dayan and Montague (1997); drawn from Psyche's TD learner, not from his figures (item `schultz`: rates 5 + 30δ spikes/s, ten Poisson trials) |
| The TD error's migration over 120 trials; second-order conditioning | Psyche (`rl.td_conditioning`, `rl.second_order`; α = 0.2, γ = 0.98, 30 steps of 0.1 s, cue at step 5, juice at step 20), items `schultz` and `migration` |
| The TD error within one trial: the first, a trained one, a trained one with the juice omitted | Psyche (`rl.td_conditioning`, 150 trials), item `cases` |
| Bursts that scale with a cue's reward probability and size | later work from Schultz's laboratory, described without figures |
| Samuel's checkers (1959), Watkins's Q-learning (1989), TD-Gammon, DQN (2015), Bellman (1957), Sutton (1988), Barto, Sutton and Anderson (1983) | the usual history |
| Steinberg et al. (2013): optogenetic dopamine stimulation at reward unblocks learning; stimulation at other times does not | the abstract and commentaries; the four bars are Rescorla-Wagner on the design (α = 0.2, 100 pretraining trials, 40 compound trials, the light adding 0.5 to the error), item `steinberg` |
| Frank, Seeberger and O'Reilly (2004): off medication, better learning to avoid; on, better learning to choose | the abstract and later reviews; the bars are Psyche's opponent Go/NoGo learner after Collins and Frank (2014), 300 simulated people per dopamine level (ρ = −0.5, 0, 0.5), item `frank`: avoiding B falls from 0.74 to 0.66 as dopamine rises, while choosing A stays near 0.81. The learner gets the direction, not the whole pattern, and says so on screen |
| The reversal bandit: 80/20 then 20/80 at trial 100; α = 0.3, β = 5; win-stay 96%, lose-shift 40%; the fit (α 0.50, β 5.5) | Psyche (`rl.q_learning_bandit`, `rl.fit_bandit`), item `bandit` |
| Parameter recovery over 40 simulated players (α from 0.1 to 0.8, β from 2 to 10): r = 0.90 for α, 0.70 for β | Psyche, item `bandit` |
| Regret over 5,000 plays on machines paying 40, 45, 50 and 60% (100 runs): greedy 308, softmax 329, UCB1 162, ε-greedy 83, Thompson 40. Over 1,000 plays and 30 runs ε-greedy and Thompson were tied, so the longer run is shown | Psyche (`rl.explore_regret`), item `explore` |
| Wilson et al. (2014): directed and random exploration grow with the horizon | from memory and later reviews; the two curves are a logistic choice model with the bonus and noise set by hand (horizon 1: no bonus, σ = 4; horizon 6: a 6-point bonus, σ = 7) to show the direction, not fitted |
| Tolman's shortcut, the dopamine signals beyond the error, place-cell replay | schematics, labelled on screen as not data |
| Tolman and Honzik (1930): three groups; food from day 11; the late group's jump | textbook accounts and a review of the design |
| The maze on Psyche: a planner and a learner without a map, medians of 40 runs | Psyche (`rl.latent_learning`), item `maze` |
| Place cells (1971), grid cells (2005), the Nobel Prize (2014), grid-like signals in people (2010) | O'Keefe and Dostrovsky; Hafting et al.; Doeller, Barry and Burgess |
| Devaluation after moderate and extensive training | Adams and Dickinson (1981); Adams (1982), from reviews |
| The two-step task: 70/30 transitions, drifting payoffs; 17 participants | Daw et al. (2011); stay probabilities from Psyche (`rl.two_step`, 30 runs of 400 trials), item `twostep` |
| The mixture weight lower with compulsive symptoms, stress and load; model-free mimicry; careful instructions | Gillan et al. (2016), Otto et al. (2013), Akam et al. (2015), Feher da Silva and Hare (2020), from memory |
| Reward and transition revaluation for three learners | Psyche (`rl.revaluation`), item `successor`; Momennejad et al. (2017) for people |
| Replay during sleep (1994), forward and backward replay, prioritized replay | Wilson and McNaughton (1994); Foster and Wilson (2006); Pfeiffer and Foster (2013); Mattar and Daw (2018), from memory |
| Dopamine ramps; movement and salience signals | Howe et al. (2013); Howe and Dombeck (2016); Bromberg-Martin et al. (2010), from memory |
| A distributional code in mouse dopamine neurons | Dabney et al. (2020); Psyche's thirteen expectile learners, item `distrib` |
| Redish's model, with a drug surge of 0.5 | Redish (2004); Psyche (`rl.redish`), item `redish` |
| Yahoo!'s front-page contextual bandit | Li et al. (2010) |
| A bandit test: versions clicked 5% and 6%, 20,000 visitors, Thompson sampling against an even split (1,172 clicks against 1,100), 50 runs | Psyche, item `abtest` |
| 3,090 patients; 13.6% with an impulse-control disorder; 17.1% on agonists against 6.9% on levodopa (drawn as bars) | Weintraub et al. (2010), from the record and secondary summaries |
| Harlow's learning sets (1949); meta-reinforcement learning in prefrontal cortex | Harlow (1949); Wang et al. (2018) |

## Built in this part

* `explainer/psychology/psyche/rl.py`: TD(0) on a complete serial compound, with the error's migration and omission
  dip; second-order conditioning; Q-learning bandits with a softmax, their likelihood, a multi-start maximum-likelihood
  fit and win-stay/lose-shift; greedy, ε-greedy, softmax, UCB1 and Thompson sampling with regret; a maze in which a
  planner shows latent learning and a Q-learner does not; Daw's two-step task with model-free, model-based and hybrid
  agents and their stay probabilities; the successor matrix and reward and transition revaluation; a distributional
  population of expectile learners; Redish's drug model. Tested in `tests/psychology/test_rl.py`.
* The Ledger gains four rows; the Archive seventeen datasets.
* The course's interactive is a reversal bandit: eighty pulls on two machines paying 80% and 20%, which swap after
  pull 40, then the reader's learning rate and inverse temperature fitted by maximum likelihood on the page.
* The part's own simulations, in `compute.py`: Steinberg's design under Rescorla-Wagner, Frank's selection task on
  an opponent Go/NoGo learner (after Collins and Frank 2014), and a bandit test against an even split.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Dopamine neurons signal reward prediction errors | Schultz, Dayan and Montague 1997 | replicated |
| The two-step task shows model-free and model-based signatures | Daw, Gershman, Seymour, Dayan and Dolan 2011 | replicated |
| Rats learn a maze without reward and show it when food appears | Tolman and Honzik 1930 | replicated |
| Entorhinal grid cells fire on a triangular lattice | Hafting, Fyhn, Molden, Moser and Moser 2005 | replicated |

The first row's note records that the error's scope is argued; the second's that the reading of the mixture weight is
contested. Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Frank et al. (one study,
described, with Psyche's learner beside it), Wilson et al. (described), Tolman (1948, history), Adams and Dickinson (devaluation; its row is due in Part
28), Momennejad et al. (described with its partial result), Howe et al. and Dabney et al. (frontier), Redish (a model;
addiction's row is due in Part 41), Li et al. (an application), Weintraub et al. (a survey's rates) and Wang et al. (a
model).

## Build it

```bash
python -m videos.psychology.psych17.compute            # every number (about a minute), into .cache/psych17/
python tools/qa_scene.py psych17 Dopamine              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych17 -q l   # the whole part, silent preview
python tools/build.py psych17                          # 1080p30 with narration
python tools/qa_scene.py psych17 Controllers --lang zh # the Chinese edition of one chapter
python tools/make.py psych17                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 17                    # the lab: TD, bandits, exploration, two steps, maps
python tools/check_ledger.py psych17                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's rl module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A neuron that fires at surprise | Schultz's three recordings, drawn on Psyche; the 1997 equation; the questions; objectives |
| 1 | Credit over time | The credit-assignment problem; Samuel's checkers; second-order conditioning |
| 2 | Temporal-difference learning | Value as discounted future reward; the Bellman equation; the TD error derived; a delay line |
| 3 | The error moves to the cue | The migration, computed; every feature from one line; optogenetic unblocking |
| 4 | From prediction to action | Actor and critic; Q-learning and the softmax; Go and NoGo; Parkinson's on and off medication |
| 5 | A bandit, and your learning rate | A reversal bandit; reading α and β back by likelihood; parameter recovery |
| 6 | Explore or exploit | The dilemma; five policies and their regret; directed and random exploration in people |
| 7 | Tolman's maps | Latent learning on Psyche; cognitive maps; place and grid cells |
| 8 | Habits and plans | Devaluation; the two-step task; three signatures; what the weight means |
| 9 | Between habit and plan | The successor representation; reward and transition revaluation; replay |
| 10 | Is dopamine only an error? | Ramps, movement and salience; a distributional code |
| 11 | When the signal is hijacked | Redish's model of a drug that cannot be predicted away |
| 12 | The Ledger | Dopamine errors; the two-step task; latent learning; grid cells |
| 13 | In practice: recommenders, medicine, habits | Bandits online; impulse-control disorders on agonists; habits |
| 14 | Frontier: learning to learn | What is solid and argued; Harlow's learning sets and meta-learning; open questions |
| | Recap, problems, and the road ahead | Ten lines; the first two objections; payoffs; problems; references; Part 18 |

## Sources

**Books.** R. S. Sutton and A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed. (MIT Press, 2018),
chapters 14 and 15. P. Dayan and L. F. Abbott, *Theoretical Neuroscience* (MIT Press, 2001), chapter 9.

**Papers.** W. Schultz, P. Dayan and P. R. Montague, A neural substrate of prediction and reward, *Science* 275 (1997)
1593–1599. R. S. Sutton, Learning to predict by the methods of temporal differences, *Mach. Learn.* 3 (1988) 9–44.
A. L. Samuel, Some studies in machine learning using the game of checkers, *IBM J. Res. Dev.* 3 (1959) 210–229. A. G.
Barto, R. S. Sutton and C. W. Anderson, Neuronlike adaptive elements that can solve difficult learning control
problems, *IEEE Trans. Syst. Man Cybern.* 13 (1983) 834–846. C. J. C. H. Watkins, *Learning from Delayed Rewards*
(PhD thesis, Cambridge, 1989). E. E. Steinberg et al., A causal link between prediction errors, dopamine neurons and
learning, *Nat. Neurosci.* 16 (2013) 966–973. M. J. Frank, L. C. Seeberger and R. C. O'Reilly, By carrot or by stick,
*Science* 306 (2004) 1940–1943. H. Robbins, Some aspects of the sequential design of experiments, *Bull. Am. Math.
Soc.* 58 (1952) 527–535. W. R. Thompson, On the likelihood that one unknown probability exceeds another, *Biometrika*
25 (1933) 285–294. P. Auer, N. Cesa-Bianchi and P. Fischer, Finite-time analysis of the multiarmed bandit problem,
*Mach. Learn.* 47 (2002) 235–256. R. C. Wilson et al., Humans use directed and random exploration to solve the
explore-exploit dilemma, *J. Exp. Psychol. Gen.* 143 (2014) 2074–2081. E. C. Tolman and C. H. Honzik, Introduction and
removal of reward, and maze performance in rats, *Univ. Calif. Publ. Psychol.* 4 (1930) 257–275. E. C. Tolman,
Cognitive maps in rats and men, *Psychol. Rev.* 55 (1948) 189–208. D. Thistlethwaite, A critical review of latent
learning and related experiments, *Psychol. Bull.* 48 (1951) 97–129. J. O'Keefe and J. Dostrovsky, The hippocampus as
a spatial map, *Brain Res.* 34 (1971) 171–175. T. Hafting et al., Microstructure of a spatial map in the entorhinal
cortex, *Nature* 436 (2005) 801–806. C. F. Doeller, C. Barry and N. Burgess, Evidence for grid cells in a human memory
network, *Nature* 463 (2010) 657–661. C. D. Adams and A. Dickinson, Instrumental responding following reinforcer
devaluation, *Q. J. Exp. Psychol.* 33B (1981) 109–121. N. D. Daw et al., Model-based influences on humans' choices
and striatal prediction errors, *Neuron* 69 (2011) 1204–1215. T. Akam, R. Costa and P. Dayan, Simple plans or
sophisticated habits?, *PLoS Comput. Biol.* 11 (2015) e1004648. C. Feher da Silva and T. A. Hare, Humans primarily use
model-based inference in the two-stage task, *Nat. Hum. Behav.* 4 (2020) 1053–1066. P. Dayan, Improving
generalization for temporal difference learning: the successor representation, *Neural Comput.* 5 (1993) 613–624. I.
Momennejad et al., The successor representation in human reinforcement learning, *Nat. Hum. Behav.* 1 (2017)
680–692. M. A. Wilson and B. L. McNaughton, Reactivation of hippocampal ensemble memories during sleep, *Science* 265
(1994) 676–679. M. G. Mattar and N. D. Daw, Prioritized memory access explains planning and hippocampal replay, *Nat.
Neurosci.* 21 (2018) 1609–1617. M. W. Howe et al., Prolonged dopamine signalling in striatum signals proximity and
value of distant rewards, *Nature* 500 (2013) 575–579. W. Dabney et al., A distributional code for value in
dopamine-based reinforcement learning, *Nature* 577 (2020) 671–675. A. D. Redish, Addiction as a computational process
gone awry, *Science* 306 (2004) 1944–1947. L. Li, W. Chu, J. Langford and R. E. Schapire, A contextual-bandit approach
to personalized news article recommendation, *WWW* (2010) 661–670. D. Weintraub et al., Impulse control disorders in
Parkinson disease: a cross-sectional study of 3090 patients, *Arch. Neurol.* 67 (2010) 589–595. H. F. Harlow, The
formation of learning sets, *Psychol. Rev.* 56 (1949) 51–65. J. X. Wang et al., Prefrontal cortex as a
meta-reinforcement learning system, *Nat. Neurosci.* 21 (2018) 860–868.

## Problems and solutions

**1. Values on a short chain.** With the reward at the third step after the cue (steps 0, 1, 2, 3 and the juice at
step 3), V(3) = 1, V(2) = 0.9, V(1) = 0.81, V(0) = 0.729. The moment before the cue has value 0, because nothing
predicts the cue, so at the cue's onset δ = 0 + γV(0) − 0 = 0.656; at the juice, δ = 1 + 0 − 1 = 0.

**2. The TD error from Bellman.** If V is correct, V(s) = E[r + γV(s′) | s], so E[δ | s] = E[r + γV(s′) | s] − V(s) = 0.
A nonzero average error means the prediction is off, and moving V(s) by αδ is a stochastic step toward the fixed point
(for a fixed policy, the Bellman operator is a contraction with factor γ, so the fixed point is unique).

**3. The error's journey.** With α = 1, the first trial sets the value of the juice's own moment; on the next trial the
moment before it is a surprise and takes the value γ, and so on: each trial moves the first nonzero value one step
earlier. Fifteen steps take fifteen trials, and from the sixteenth trial on the error sits at the cue's onset, where
it stays because the cue is unpredicted. With smaller α the front still moves a step per trial but takes many trials
to grow.

**4. The bandit's likelihood.** log L(α, β) = Σₜ [β Q_t(a_t) − log Σ_b e^{β Q_t(b)}], with Q updated by α after each
outcome. When β is large, nearly every choice goes to the higher-valued option, so P(a_t) ≈ 1 for almost all trials
whether β is 15 or 30: the likelihood is flat in β beyond a point, and β is poorly recovered (chapter five's plot).
The learning rate is pinned down by the few trials around a change, which is why reversals help.

**5. A successor matrix.** For the chain 1 → 2 → 3 (3 ends the episode), T has ones at (1, 2) and (2, 3), and
M = I + γT + γ²T² has rows (1, γ, γ²), (0, 1, γ), (0, 0, 1). With a reward r at state 3, V = Mr gives V(1) = γ²r,
V(2) = γr: a new r updates every value at once. If state 2 now leads to a state 4 instead, the true M changes row 1
(and row 2); a learner that revisits only state 2 updates row 2, but row 1 still predicts a visit to 3: transition
revaluation fails for the successor representation and succeeds for a planner that recomputes M from T.

**6. The two-step signature against w.** Running `rl.two_step` with w from 0 to 1 and computing the interaction
(P(stay | rewarded, common) − P(stay | rewarded, rare)) − (P(stay | unrewarded, common) − P(stay | unrewarded, rare))
gives about 0 at w = 0, rising roughly linearly to about 0.4 at w = 1 for the default α = 0.5, β = 5; the main effect
of reward shrinks as w grows.

**7. ★ What a ramp means.** If a ramp is a TD error under uncertainty about position or time, a sudden jump forward
(teleporting the animal closer in virtual reality, or a cue that tells it more time has passed) should produce a
phasic burst proportional to the jump in value, and the ramp's slope should change with running speed; if the ramp
encodes value itself, a jump should shift its level without a transient burst. Kim et al. (2020) ran this logic in
mice in virtual reality and found the bursts.

## Where it comes back

Attention, and what is worth learning about: Part 18. Memory, replay and consolidation: Part 21. Decisions, value and
risk: Part 26. Motivation, wanting and liking: Part 28. Addiction: Part 41. Products designed around habits: Part 52.
The predictive brain, and learning to learn: Part 58. Psyche's `rl` module supplies the learners those parts extend.

## Open checks

Before the narrated master:

* Schultz's recordings are drawn from Psyche, not reproduced; the probability and magnitude scaling are described
  without figures.
* TD-Gammon's level and DQN's dozens of games are the usual history.
* Frank et al. (2004) and the later debate are from abstracts and reviews.
* Wilson et al.'s horizons and the claim about children are from memory.
* Tolman and Honzik's group sizes and error counts are not given; the comparison is as textbooks report it.
* Adams and Dickinson's procedures (devaluation by sickness or satiety) and Adams (1982) on overtraining are from reviews.
* Gillan et al. (2016), Otto et al. (2013) and Akam et al. (2015) are cited from memory.
* Replay results (1994, 2006, 2013, 2018) and the dopamine movement and salience results are from memory.
* Weintraub et al.'s percentages are from secondary summaries of the paper.
* Kim et al. (2020), cited in problem 7, is from memory.
