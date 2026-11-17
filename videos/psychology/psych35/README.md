# Psychology, Built: Part 35, Social Cognition

In 1959 Festinger and Carlsmith had 71 men turn pegs for an hour, then paid some of them one dollar and others twenty
to tell a waiting student that the task had been interesting. The men paid one dollar later rated the task more
enjoyable. Festinger called it dissonance: a lie told for too little money has to be justified from the inside.
Eight years later Bem gave a different explanation, that people read their own attitudes from their behaviour the
way they read anyone else's. This part is about that reading: how people explain each other, judge each other in a
tenth of a second, flatter themselves, and work out what someone wants from where they walk; and about the famous
findings of the field that did not survive being checked.

The hook is the peg board, the dollar and the prophecy that failed; the viewer watches three shapes move, as in
Heider and Simmel's film, and predicts four numbers. Then Kelley's cube as an analysis of variance (computed),
Jones and Harris's Castro essays and a rational observer of them; dissonance against self-perception, Bem's
simulation, Fazio, Zanna and Cooper's reconciliation and the 2024 test in 39 laboratories; LaPiere's road trip and
letter, the theory of planned behaviour and when attitudes predict; Svenson's drivers, self-serving attributions,
false consensus, and the Dunning-Kruger graph rebuilt from regression to the mean (computed); faces judged in a tenth
of a second, competence and Senate races, and thin slices of teaching; the elderly walk and its failure, Kahneman's
letter, and which priming is solid; power posing, its replication, and the winner's curse that explains both
(computed); the false-belief localizer and its overlap with attention; inverse planning in a gridworld (computed)
and against people; and Nisbett and Wilson's stockings and choice blindness. The practice chapter is judging people
at work, user research and machines that infer what users want; the frontier is theory of mind in language models.

## Where the numbers come from

| What | Source |
|---|---|
| Kelley's cube, 2 people x 2 entities x 2 occasions: a person pattern puts all the variance in the person main effect (consensus 0, distinctiveness 0, consistency 1); an entity pattern in the entity effect; a circumstance pattern leaves 89% in the interaction | Psyche (`social.kelley`), item `kelley` |
| A rational observer of the essays: the inferred attitude is ±0.71 when the writer chose, ±0.21 when the observer thinks the assignment held with probability 0.7, and 0 when sure it held | Psyche (Bayes' rule), item `essays` |
| The Dunning-Kruger plot from 4,000 simulated people: with a correlation of 0.3 and a 15-point flattering shift, the quarters estimate 54, 61, 68 and 72; with a perfect correlation and no shift, they estimate their true places; with none, about 50 | Psyche (`social.dunning_kruger`), item `dk` |
| Inverse planning on a 7 x 9 grid with a wall and three goals, softmax planner with beta 0.7: one walk gives goal A 67% after one step; the other holds A at 56% and C at 43% for three steps, then C takes over | Psyche (`social.goal_posterior`), item `goals` |
| The winner's curse: 20,000 two-group studies of d = 0.2; with 21 per group, 9.5% reach significance and report d = 0.78 on average; with 100 per group, 28% reach it and report 0.37 | Psyche (simulated), item `curse` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/social.py` (committed with Part 34): the inverse planner (`grid_distances`,
  `action_probs`, `goal_posterior`), Kelley's cube (`kelley`) and the Dunning-Kruger plot from noise
  (`dunning_kruger`); and, written ahead for Part 36, Tajfel's allocation matrices (`tajfel_matrix`, `allocate`), an
  IAT as two blocks of diffusion decisions (`iat_d`, `iat_study`), the list experiment (`list_experiment`), a
  promotion ladder (`pipeline`) and an illusory-correlation model (`illusory_correlation`). Tested in
  `tests/psychology/test_social.py`.
* The Ledger gains eight rows.
* The course's interactive is goal inference: watch an agent walk part of the way through a maze, say which of three
  goals it is heading for, and compare your answers with the inverse planner's posterior.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Observers infer a person's attitude from what they say or do even when the situation forced it | Jones and Harris 1967 | replicated |
| Freely choosing to argue against your own view moves your attitude toward what you argued, more than being told to | Festinger and Carlsmith 1959 | failed |
| People overestimate how many others share their own choices and opinions | Ross, Greene and House 1977 | replicated |
| The least skilled overestimate their standing the most, because they lack the skill to see their errors | Kruger and Dunning 1999 | contested |
| Most people rate themselves above the median on desirable traits and skills | Svenson 1981 | replicated |
| Reading words about old age makes people walk more slowly afterwards | Bargh, Chen and Burrows 1996 | failed |
| Holding an expansive pose for two minutes raises testosterone, lowers cortisol and increases risk-taking | Carney, Cuddy and Yap 2010 | failed |
| People infer an agent's goal from its movement as a Bayesian observer of a roughly rational planner would | Baker, Saxe and Tenenbaum 2009 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Festinger, Riecken and
Schachter, Heider and Simmel, Bem and Fazio, Zanna and Cooper, LaPiere, Ajzen and Glasman and Albarracín, Mezulis et
al., Willis and Todorov, Todorov et al., Ambady and Rosenthal, Saxe and Kanwisher, Mitchell, Ng and Russell,
Kosinski and Ullman.

## Build it

```bash
python -m videos.psychology.psych35.compute            # every number (a few seconds)
python tools/qa_scene.py psych35 Inverse               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych35 -q l   # the whole part, silent preview
python tools/build.py psych35                          # 1080p30 with narration
python tools/qa_scene.py psych35 Attribution --lang zh # the Chinese edition of one chapter
python tools/make.py psych35                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 35                    # the lab: Kelley's cube, Dunning-Kruger, inverse planning
python tools/check_ledger.py psych35                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's social module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1959: one dollar or twenty | The pegs; the result; the prophecy that failed; the question; objectives |
| 1 | On you: shapes and numbers | Three moving shapes; four predictions |
| 2 | Explaining behaviour | Kelley's cube as an analysis of variance; the Castro essays; a rational observer |
| 3 | Dissonance or self-perception | Two theories; Bem's simulation; where each holds; the 39-lab test |
| 4 | Attitudes and behaviour | LaPiere's road trip and letter; when attitudes predict |
| 5 | The self's illusions | Better than average; false consensus; Dunning-Kruger and the same picture from noise |
| 6 | First impressions | A tenth of a second; faces and votes; thin slices of behaviour |
| 7 | Priming and its collapse | The walk to the elevator; infrared beams and expectations; what kind of priming is solid |
| 8 | Power posing | A pose, a talk and a reversal; why small significant studies look big |
| 9 | Thinking about thinking | Two kinds of false story; the temporoparietal junction; specific or shared |
| 10 | Mind reading as inverse planning | Run the planner backwards; two walks; the model against people |
| 11 | Knowing ourselves | Four identical pairs; choice blindness; the observer inside |
| 12 | The Ledger | Eight rows and the tally |
| 13 | In practice: judging people, asking people | Judging people at work; what users say and do; machines that infer what you want |
| 14 | Frontier: minds in machines | False-belief tasks for language models; small changes; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 36 |

## Sources

* L. Festinger and J. M. Carlsmith, Cognitive consequences of forced compliance, *Journal of Abnormal and Social
  Psychology* 58(2) (1959) 203-210.
* L. Festinger, H. W. Riecken and S. Schachter, *When Prophecy Fails* (1956).
* F. Heider and M. Simmel, An experimental study of apparent behavior, *American Journal of Psychology* (1944).
* H. H. Kelley, The processes of causal attribution, *American Psychologist* (1973).
* E. E. Jones and V. A. Harris, The attribution of attitudes, *Journal of Experimental Social Psychology* 3 (1967).
* D. T. Gilbert and P. S. Malone, The correspondence bias, *Psychological Bulletin* 117(1) (1995) 21-38.
* D. E. Walker, K. A. Smith and E. Vul, The "fundamental attribution error" is rational in an uncertain world,
  *Decision* (2022).
* D. J. Bem, Self-perception: an alternative interpretation of cognitive dissonance phenomena, *Psychological
  Review* 74(3) (1967) 183-200.
* R. H. Fazio, M. P. Zanna and J. Cooper, Dissonance and self-perception: an integrative view of each theory's
  proper domain of application, *Journal of Experimental Social Psychology* (1977).
* D. C. Vaidis et al., A multilab replication of the induced-compliance paradigm of cognitive dissonance, *Advances
  in Methods and Practices in Psychological Science* 7(1) (2024).
* R. T. LaPiere, Attitudes vs. actions, *Social Forces* 13 (1934).
* I. Ajzen, The theory of planned behavior, *Organizational Behavior and Human Decision Processes* 50 (1991) 179-211.
* L. R. Glasman and D. Albarracín, Forming attitudes that predict future behavior, *Psychological Bulletin* (2006).
* O. Svenson, Are we all less risky and more skillful than our fellow drivers?, *Acta Psychologica* 47(2) (1981)
  143-148; L. Koppel et al., a preregistered replication, *Meta-Psychology* (2023).
* A. H. Mezulis, L. Y. Abramson, J. S. Hyde and B. L. Hankin, Is there a universal positivity bias in attributions?,
  *Psychological Bulletin* 130(5) (2004) 711-747.
* L. Ross, D. Greene and P. House, The false consensus effect, *Journal of Experimental Social Psychology* 13 (1977);
  B. Mullen et al., a meta-analysis of 115 hypothesis tests, *Journal of Experimental Social Psychology* 21 (1985).
* J. Kruger and D. Dunning, Unskilled and unaware of it, *Journal of Personality and Social Psychology* 77(6) (1999);
  E. Nuhfer et al., *Numeracy* (2016, 2017); R. D. McIntosh et al., *Journal of Experimental Psychology: General*
  (2019).
* J. Willis and A. Todorov, First impressions: making up your mind after a 100-ms exposure to a face,
  *Psychological Science* (2006).
* A. Todorov, A. N. Mandisodza, A. Goren and C. C. Hall, Inferences of competence from faces predict election
  outcomes, *Science* (2005).
* N. Ambady and R. Rosenthal, Half a minute, *Journal of Personality and Social Psychology* (1993).
* J. A. Bargh, M. Chen and L. Burrows, Automaticity of social behavior, *Journal of Personality and Social
  Psychology* 71(2) (1996); S. Doyen, O. Klein, C.-L. Pichon and A. Cleeremans, Behavioral priming: it's all in the
  mind, but whose mind?, *PLOS ONE* (2012).
* D. R. Carney, A. J. C. Cuddy and A. J. Yap, Power posing, *Psychological Science* 21(10) (2010); E. Ranehill et
  al., Assessing the robustness of power posing, *Psychological Science* 26(5) (2015).
* R. Saxe and N. Kanwisher, People thinking about thinking people, *NeuroImage* (2003); J. P. Mitchell, Activity in
  right temporo-parietal junction is not selective for theory-of-mind, *Cerebral Cortex* 18(2) (2008) 262-271.
* C. L. Baker, R. Saxe and J. B. Tenenbaum, Action understanding as inverse planning, *Cognition* 113(3) (2009)
  329-349; C. L. Baker, J. Jara-Ettinger, R. Saxe and J. B. Tenenbaum, *Nature Human Behaviour* 1 (2017) 0064.
* R. E. Nisbett and T. D. Wilson, Telling more than we can know, *Psychological Review* 84(3) (1977) 231-259.
* P. Johansson, L. Hall, S. Sikström and A. Olsson, Failure to detect mismatches between intention and outcome in a
  simple decision task, *Science* (2005).
* A. Y. Ng and S. Russell, Algorithms for inverse reinforcement learning, *ICML* (2000).
* M. Kosinski, Evaluating large language models in theory of mind tasks, *PNAS* (2024); T. Ullman, Large language
  models fail on trivial alterations to theory-of-mind tasks, arXiv 2302.08399 (2023).

## Problems and solutions

1. **Kelley's cube.** If only person 1 reacts, the response is 1 on every cell of person 1's slab and 0 elsewhere,
   so every cell equals the grand mean plus the person effect: the entity, occasion and interaction terms are zero
   and the person effect carries all the variance. Consensus is low (nobody else reacts), distinctiveness is low
   (person 1 reacts to every entity) and consistency is high (on every occasion): Kelley's pattern for blaming the
   person.
2. **The rational observer.** P(pro essay | pro) = 1 and P(pro essay | anti) = π, so by Bayes' rule
   P(pro | pro essay) = (1/2)/(1/2 + π/2) = 1/(1 + π). It exceeds 1/2 whenever π < 1: unless the observer is
   certain the assignment fully constrained the essay, the essay is some evidence about the writer, and inferring
   an attitude is reasonable.
3. **Dunning-Kruger from regression.** Averaging E[Y | X] over the bottom quarter gives
   50 + s + ρ(E[X | bottom] − 50). For a uniform skill percentile E[X | bottom] = 12.5, so the bottom quarter
   estimates 50 + s − 37.5ρ. With ρ = 0 every quarter estimates 50 + s: a flat line above the diagonal for the
   bottom and below it for the top, the famous picture with no insight in it at all.
4. **Dawes's two thirds.** With a uniform prior on p and one observation (you agree), the posterior is Beta(2, 1),
   with mean 2/3. Ross, Greene and House's agreers estimated about 62% and refusers about 67% for their own choice:
   close to what an observer with one data point, themselves, should say.
5. **The winner's curse.** Reported only when d̂ > 1.96σ, d̂ is a normal truncated below at 1.96σ, with mean
   d + σφ(a)/(1 − Φ(a)), where a = 1.96 − d/σ = 1.31. Then φ(a) = 0.169, 1 − Φ(a) = 0.095, and the mean is
   0.2 + 0.31 x 1.78 = 0.75: about 3.8 times the truth. The simulation's 0.78 differs because each study also
   estimates its own standard deviation.
6. **One step of inverse planning.** The posterior is prior x likelihood, normalized. Equal likelihoods for A and C
   multiply both by the same number, so their ratio is unchanged; a zero likelihood sends B to zero, and A and C
   split B's share in their old ratio.
7. **★ Dissonance against self-perception.** Self-perception needs no arousal and works only where the attitude
   was weak or ambiguous; dissonance predicts arousal, and change mainly for acts well outside the person's view.
   One design: have people write essays near or far from their own position, with high or low choice, and offer
   half a pill said to cause tension (a misattribution cue). Dissonance predicts that the pill removes the attitude
   change for far essays under high choice; self-perception predicts no effect of the pill. This is the logic of
   Zanna and Cooper's misattribution studies and of Fazio, Zanna and Cooper's division of the territory.

## Open checks

Checked against the articles, their abstracts or official pages, or named secondary summaries of them
(2026-11-16): Festinger and Carlsmith's 71 men and the one and twenty dollars; *When Prophecy Fails*, the flood
predicted for 21 December 1954 and the follow-ups; Jones and Harris's means (59.6, 17.4, 44.1 and 22.9); Gilbert and
Malone's four mechanisms; the 2017 Philippine replication; Walker, Smith and Vul; Bem's simulation; Fazio, Zanna and
Cooper; Vaidis et al.'s 39 labs, 19 countries and 4,898 people; LaPiere's 251 places, one refusal, 128 replies and
92%; Ajzen; Glasman and Albarracín's moderators; Svenson's 93% and 69%; Koppel et al.'s 1,203; Mezulis et al.'s 266
studies and d = 0.96; Ross, Greene and House; Mullen et al.'s 115 tests; Kruger and Dunning's 12th and 62nd
percentiles; Nuhfer et al. and McIntosh et al.; Willis and Todorov's exposures and traits; Todorov et al.'s 68.8%;
Ambady and Rosenthal's clips and the principals; Bargh, Chen and Burrows; Doyen et al.'s infrared sensors and
expectations; Kahneman's 2012 letter; Carney, Cuddy and Yap's 42; Ranehill et al.'s 200; Carney's 2016 statement;
Saxe and Kanwisher; Mitchell's overlap with attentional reorienting; Baker, Saxe and Tenenbaum's three experiments
and r = .96 in the 2007 version; the food trucks; Nisbett and Wilson's stockings; Johansson et al.'s 15 pairs and
under one detection in ten; Kosinski's 40 tasks, 640 prompts, 75% and 20%; Ullman's alterations.

Still to recheck against the full texts before the final cut:

* Ross, Greene and House's 62% and 67%, from secondary summaries (used only in problem 4's solution).
* Nisbett and Wilson's reported reasons (knit, sheerness) and the size of the position effect ("far more often";
  about four times, in secondary sources).
* That the power-posing talk was "one of the most watched of its kind", and that Kahneman had featured priming in
  *Thinking, Fast and Slow*, both widely reported but not checked against a primary source here.
* Choice blindness's total detection rate, which sources report differently; the film quotes only "fewer than one
  in ten noticed at once".
* Bargh, Chen and Burrows's sample sizes and timing procedure; the film says only that an experimenter timed the
  walk with a stopwatch.
* Ng and Russell (2000), cited from the standard reference; Ullman's popcorn example, as summarized.
