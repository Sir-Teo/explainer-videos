# Psychology, Built: Part 24, Reasoning and Problem Solving

Four cards, one rule, and nine people in ten turn the wrong ones. Change the cards to drinks and ages and nearly
everyone is right, although the logic has not changed. This part asks whether people are logical, and if not, what
they are instead: reasoners who use what content means, testers who look for information, searchers through spaces
of states, experts who see in chunks, and minds with too little time to optimize.

The selection task on you, abstract and as a drinking rule; syllogisms, their 64 forms, and validity decided by
brute force over set models; 139 people's answers to every syllogism from open data, and belief bias; mental models
and their search for counterexamples, three shortcuts (atmosphere, matching, probability heuristics) and all four
accounts scored on the data; pragmatic schemas and cheater detection; optimal data selection derived and computed
against Oaksford and Chater's meta-analysis; problems as spaces of states, the Tower of Hanoi drawn whole, a
hill-climber's wandering and a goal-stack production system's pauses; think-aloud protocols; Köhler's apes on Tenerife and the record that gave insight a
learning history (Birch, Epstein et al.); Duncker's candle; Luchins's water jars computed and mental set in chess
experts (Bilalić et al.); the
nine dots proved unsolvable inside the box, and warmth ratings; chess memory, chunks and deliberate practice;
the radiation problem and structure mapping computed; mental rotation fitted person by person to open data, and the
imagery debate; delta P and causal power derived, and seeing against doing; everyday predictions under three priors,
and bounded rationality. The practice chapter is interview puzzles and personnel selection, worked examples and
usability testing; the frontier is program induction, the Abstraction and Reasoning Corpus, and whether language
models reason by analogy.

## Where the numbers come from

| What | Source |
|---|---|
| About one person in ten turns E and 7 | Wason (1966, 1968), as summarized in the literature |
| About three in four solve the drinking-age version | Griggs and Cox (1982) |
| 64 syllogisms, 27 with a valid conclusion (each term assumed to name something); 22 without that assumption | Psyche (`reason.valid_conclusions`, all 256 models of three sets), item `syllogisms` |
| 139 people, 8,896 answers: 41% right overall, 48% where a conclusion follows, 37% where none does; "no valid conclusion" 28% of answers; hardest EA1 (4%), IA2, AE2; easiest AE1, EA2, EA3 | Ragni (2016), as packaged in the CCOBRA benchmark (MIT licence), fetched by `explainer.psychology.opendata` and checked by SHA-256; item `syllogisms` |
| Commonest answers predicted: logic 18 of 27 and 25 of 37; atmosphere 23 and 12; matching and probability heuristics 19 and 12 | Psyche (`reason.predict`, `score`), item `syllogisms` |
| Acceptance 89, 56, 71 and 10 percent | Evans, Barston and Pollard (1983), as tabulated by Evans, Handley and Harper (2001) |
| Twelve theories surveyed, seven tested on six studies, none fits well | Khemlani and Johnson-Laird (2012) |
| Expected information gain with P(p) = 0.1, P(q) = 0.2: p 0.61, q 0.15, not-q 0.05, not-p 0.01 bits | Psyche (`reason.selection_information`), item `selection` |
| Selections in 13 studies, 34 tasks, 845 people: p 89%, q 62%, not-q 25%, not-p 16% | Oaksford and Chater (1994), Table 2, read from the paper |
| 27 states and 39 moves for three discs; the hill-climber's median of 101 runs 14 moves (7% optimal); 62 for four discs against 15 | Psyche (`reason.hanoi_graph`, `hill_climb`), item `hanoi` |
| The goal stack's pauses for four discs, longest before moves 1, 9, then 5 and 13 | Psyche (`reason.goal_stack_solver`, one unit per move, 1.5 per subgoal), item `hanoi` |
| Nine dots: no drawing turning inside the square; 16 outside it (the same 16 with a wider grid) | Psyche (`reason.nine_dots`), item `ninedots` |
| Luchins's eleven water-jar problems (1942): B - A - 2C solves problems 2 to 8, 10 and 11; A - C solves 7 and 9, the shorter way on 7, the only one of the two on 9 | `compute.py`, item `jars` |
| About 10%, 30% and 75% solve the radiation problem unaided, after the story, and with a hint | Gick and Holyoak (1980), as summarized in textbooks |
| The fortress mapped onto the tumour: 4 objects, 9 relations matched | Psyche (`reason.structure_map`), item `analogy` |
| Practice explains 26% of differences in games, 21% in music, 18% in sports, 4% in education, under 1% in professions | Macnamara, Hambrick and Oswald (2014) |
| 54 people, 5,184 trials: mean times on correct same trials 1,563, 2,461, 3,053 and 3,341 ms at 0, 50, 100 and 150 degrees; mirror errors 3% to 22%; 53 of 54 slopes rising; median 10.8 ms per degree (93 degrees a second) | Ganis and Kievit (2015), figshare (CC BY 4.0), fetched by `explainer.psychology.opendata` and checked by SHA-256; Psyche (`reason.rotation_fit`, `rotation_model`), item `rotation` |
| Delta P and causal power for a cause of strength 0.5 on backgrounds from 0 to 0.9 | Psyche (`reason.delta_p`, `causal_power`), item `causes` |
| Predictions under power-law, Erlang and normal priors; a life-span prior with mean 75 and sd 16 (illustrative) gives 71, 72 and 96 at 18, 39 and 90 | Psyche (`reason.predict_total`), item `everyday` |
| 1,729 people solved about 64% of ARC's evaluation tasks | LeGris et al. (2024) |
| Five test users find about 84% of problems when L = 0.31 | Nielsen and Landauer (1993), computed, item `usability` |

## Built in this part

* `explainer/psychology/psyche/reason.py`: syllogisms (validity over all models of three sets, the figural effect,
  logic, atmosphere, matching and the probability heuristics' min-rule, CCOBRA parsing, response tables and
  scores); optimal data selection; the Tower of Hanoi's state graph, Sierpinski layout, shortest path, a
  goal-stack production system with latencies and a hill-climber; the nine dots by exhaustive search; structure
  mapping by brute force; rotation fits and a rotation model; delta P and causal power; posterior-median
  predictions. Tested in `tests/psychology/test_reason.py`.
* `explainer/psychology/opendata.py` gains Ganis and Kievit's mental rotation workbooks (read with the standard
  library, nothing executed) and Ragni's syllogism data at a fixed commit.
* The Ledger gains six rows; the Archive five datasets.
* The course's interactive is mental rotation on you: same or mirror, your time against the angle, your rotation
  speed beside the 54 people of the open data.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| The selection task is solved far more often when the rule is a familiar permission, such as a drinking age, than when it is abstract | Griggs and Cox 1982 | replicated |
| People accept believable conclusions more often than unbelievable ones with the same logical form, most of all when the conclusions do not follow | Evans, Barston and Pollard 1983 | replicated |
| The time to judge whether two figures are the same object grows linearly with the angle between them | Shepard and Metzler 1971 | replicated |
| Chess experts recall briefly seen positions from real games far better than novices, but not random ones | Chase and Simon 1973 | replicated |
| Expert performance is mainly the product of about 10,000 hours of deliberate practice | Ericsson, Krampe and Tesch-Romer 1993 | story and record |
| People's predictions about everyday quantities match the Bayesian predictions under each domain's real distribution | Griffiths and Tenenbaum 2006 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Wason (the task's history),
Johnson-Laird and Bara (a theory), Cheng and Holyoak and Cosmides (in the content row's record), Oaksford and Chater
(a model, computed), Newell, Shaw and Simon and Anderson (theories of search and production systems), Ericsson and
Simon (a method), Köhler, Thorndike, Birch and Epstein et al. (the history of insight in animals, drawn
schematically), Duncker and Adamson (demonstrations), Luchins and Bilalić et al. (mental set: the jars computed, the
eye-tracking study described), Metcalfe and Wiebe and MacGregor et al. (insight,
described), Gick and Holyoak (a transfer study given as rough shares), Kosslyn, Pylyshyn and Zeman et al. (the
imagery debate), Waldmann and Hagmayer (causal reasoning), Simon (bounded rationality), Evans et al. 2001 (the
belief-bias table as reprinted), Schmidt and Hunter, Sackett et al. and Sweller and Cooper (Parts 53 and 54), Ellis
et al., Chollet, LeGris et al. and Webb et al. (Part 60). Anderson and Douglass and Nielsen and Landauer appear only
beside Psyche's own computations.

## Build it

```bash
python -m videos.psychology.psych24.compute            # every number (under a minute; fetches the open data once)
python tools/qa_scene.py psych24 Imagery               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych24 -q l   # the whole part, silent preview
python tools/build.py psych24                          # 1080p30 with narration
python tools/qa_scene.py psych24 Search --lang zh      # the Chinese edition of one chapter
python tools/make.py psych24                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 24                    # the lab: syllogisms to mental rotation
python tools/check_ledger.py psych24                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's reasoning module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Four cards | The selection task on you, abstract and as a drinking rule; the questions; objectives |
| 1 | Deduction | Sixty-four syllogisms; validity by brute force; 139 people's answers; belief bias |
| 2 | Rules, models and shortcuts | Mental models and counterexamples; atmosphere, matching and probability heuristics; four accounts scored |
| 3 | Why content helps | Pragmatic schemas and cheater detection; optimal data selection derived; information against people's choices |
| 4 | Problem solving as search | States, operators and means-ends analysis; the Tower of Hanoi's whole space; the shortest path and a hill-climber |
| 5 | Production systems | Rules that fire; ACT-R; where a goal stack predicts pauses; thinking aloud as data |
| 6 | Insight | Köhler's apes; Duncker's candle; Luchins's jars; the nine dots by brute force; warmth ratings and progress monitoring |
| 7 | Expertise | De Groot, Chase and Simon; chunks; deliberate practice and how much it explains |
| 8 | Analogy | The radiation problem and the fortress; structure mapping computed |
| 9 | Mental imagery | Shepard and Metzler; 54 people's open data fitted; depictive or descriptive; aphantasia |
| 10 | Reasoning about causes | Delta P to causal power, derived; seeing against doing |
| 11 | Everyday predictions, and bounded rationality | The posterior median derived; three priors, three rules; Simon's satisficing |
| 12 | The Ledger | Content effects; belief bias; mental rotation; chess memory; 10,000 hours; everyday predictions |
| 13 | In practice: puzzles, protocols, training | Interview puzzles and selection; worked examples; usability testing computed |
| 14 | Frontier: machines that reason | ARC, program induction and large models; analogy in language models and its critics |
| | Recap, problems, and the road ahead | Ten lines; Kant's three objections; payoffs; problems; references; Part 25 |

## Sources

* P. C. Wason, Reasoning, in New Horizons in Psychology (1966); Reasoning about a rule, Quarterly Journal of
  Experimental Psychology 20 (1968) 273-281; R. A. Griggs and J. R. Cox, British Journal of Psychology 73 (1982)
  407-420; P. W. Cheng, K. J. Holyoak, R. E. Nisbett and L. M. Oliver, Pragmatic versus syntactic approaches to
  training deductive reasoning, Cognitive Psychology 18 (1986) 293-328.
* P. N. Johnson-Laird, Mental Models (1983); P. N. Johnson-Laird and B. G. Bara, Syllogistic inference, Cognition 16
  (1984) 1-61; R. S. Woodworth and S. B. Sells, An atmosphere effect in formal syllogistic reasoning, Journal of
  Experimental Psychology 18 (1935) 451-460; N. E. Wetherick and K. J. Gilhooly, 'Atmosphere', matching, and logic in
  syllogistic reasoning, Current Psychology 14 (1995) 169-178; N. Chater and M. Oaksford, The probability heuristics
  model of syllogistic reasoning, Cognitive Psychology 38 (1999) 191-258; S. Khemlani and P. N. Johnson-Laird,
  Theories of the syllogism: a meta-analysis, Psychological Bulletin 138 (2012) 427-457; CCOBRA,
  github.com/CognitiveComputationLab/ccobra.
* J. St B. T. Evans, J. L. Barston and P. Pollard, Memory & Cognition 11 (1983) 295-306; K. C. Klauer, J. Musch and B.
  Naumer, Psychological Review 107 (2000) 852-884; C. Dube, C. M. Rotello and E. Heit, Psychological Review 117 (2010)
  831-863.
* P. W. Cheng and K. J. Holyoak, Pragmatic reasoning schemas, Cognitive Psychology 17 (1985) 391-416; L. Cosmides,
  The logic of social exchange, Cognition 31 (1989) 187-276; M. Oaksford and N. Chater, A rational analysis of the
  selection task as optimal data selection, Psychological Review 101 (1994) 608-631.
* A. Newell, J. C. Shaw and H. A. Simon, Elements of a theory of human problem solving, Psychological Review 65
  (1958) 151-166; A. Newell and H. A. Simon, Human Problem Solving (1972); J. R. Anderson, Rules of the Mind (1993);
  J. R. Anderson and S. Douglass, Tower of Hanoi: evidence for the cost of goal retrieval, JEP: Learning, Memory, and
  Cognition 27 (2001) 1331-1346; K. A. Ericsson and H. A. Simon, Verbal reports as data, Psychological Review 87
  (1980) 215-251, and Protocol Analysis (1993).
* W. Köhler, *Intelligenzprüfungen an Menschenaffen* (1917; *The Mentality of Apes*, 1925); E. L. Thorndike,
  Animal intelligence, Psychological Review Monograph Supplements 2 (1898) no. 8; H. G. Birch, The relation of previous
  experience to insightful problem-solving, J. Comp. Psychol. 38 (1945) 367-383; R. Epstein, C. E. Kirshnit, R. P.
  Lanza and L. C. Rubin, "Insight" in the pigeon, Nature 308 (1984) 61-62; A. S. Luchins, Mechanization in problem
  solving, Psychological Monographs 54 (1942) no. 248; M. Bilalić, P. McLeod and F. Gobet, Why good thoughts block
  better ones, Cognition 108 (2008) 652-661.
* K. Duncker, On problem-solving, Psychological Monographs 58 (1945) no. 270; R. E. Adamson, JEP 44 (1952) 288-291;
  R. W. Weisberg and J. W. Alba, An examination of the alleged role of "fixation" in the solution of several
  "insight" problems, JEP: General 110 (1981) 169-192; J. Metcalfe and D. Wiebe, Intuition in insight and noninsight
  problem solving, Memory & Cognition 15 (1987) 238-246; J. N. MacGregor, T. C. Ormerod and E. P. Chronicle,
  Information processing and insight: a process model of performance on the nine-dot and related problems, JEP:
  LMC 27 (2001) 176-201.
* A. D. de Groot, Thought and Choice in Chess (1965); W. G. Chase and H. A. Simon, Perception in chess, Cognitive
  Psychology 4 (1973) 55-81; F. Gobet and H. A. Simon, Psychonomic Bulletin & Review 3 (1996) 159-163; G. Sala and
  F. Gobet, Memory & Cognition 45 (2017) 183-193; K. A.
  Ericsson, R. T. Krampe and C. Tesch-Romer, Psychological Review 100 (1993) 363-406; B. N. Macnamara, D. Z.
  Hambrick and F. L. Oswald, Psychological Science 25 (2014) 1608-1618; B. N. Macnamara and M. Maitra, Royal Society
  Open Science 6 (2019) 190327.
* M. L. Gick and K. J. Holyoak, Analogical problem solving, Cognitive Psychology 12 (1980) 306-355; D. Gentner,
  Structure-mapping: a theoretical framework for analogy, Cognitive Science 7 (1983) 155-170.
* R. N. Shepard and J. Metzler, Mental rotation of three-dimensional objects, Science 171 (1971) 701-703; G. Ganis
  and R. Kievit, Journal of Open Psychology Data 3 (2015) e3; S. M. Kosslyn, T. M. Ball and B. J. Reiser, JEP: Human
  Perception and Performance 4 (1978) 47-60; Z. W. Pylyshyn, The imagery debate, Psychological Review 88 (1981)
  16-45; A. Zeman, M. Dewar and S. Della Sala, Lives without imagery, Cortex 73 (2015) 378-380; M. Pounder et al.,
  Only minimal differences between individuals with congenital aphantasia and those with typical imagery on
  neuropsychological tasks that involve imagery, Cortex 148 (2022) 180-192.
* P. W. Cheng, From covariation to causation: a causal power theory, Psychological Review 104 (1997) 367-405; M. R.
  Waldmann and Y. Hagmayer, Seeing versus doing, JEP: LMC 31 (2005) 216-227; J. Pearl, Causality (2000).
* T. L. Griffiths and J. B. Tenenbaum, Psychological Science 17 (2006) 767-773; M. C. Mozer, H. Pashler and H.
  Homaei, Cognitive Science 32 (2008) 1133-1147; S. Lewandowsky, T. L. Griffiths and M. L. Kalish, Cognitive Science
  33 (2009) 969-998; H. A. Simon, A behavioral model of rational choice, Quarterly Journal of Economics 69 (1955)
  99-118.
* F. L. Schmidt and J. E. Hunter, Psychological Bulletin 124 (1998) 262-274; P. R. Sackett, C. Zhang, C. M. Berry
  and F. Lievens, Revisiting meta-analytic estimates of validity in personnel selection, Journal of Applied Psychology
  107 (2022) 2040-2068; J. Sweller and G. A. Cooper, Cognition and Instruction 2 (1985) 59-89; J. Nielsen and T. K.
  Landauer, A mathematical model of the finding of usability problems, Proceedings of INTERCHI (1993) 206-213.
* F. Chollet, On the measure of intelligence, arXiv 1911.01547 (2019); S. LeGris et al., H-ARC: a robust estimate of
  human performance on the Abstraction and Reasoning Corpus benchmark, arXiv 2409.01374 (2024); K. Ellis et al.,
  DreamCoder, Proceedings of PLDI (2021) 835-850; T. Webb, K. J. Holyoak and H. Lu, Emergent analogical reasoning in
  large language models, Nature Human Behaviour 7 (2023) 1526-1541; M. Lewis and M. Mitchell, Using counterfactual
  tasks to evaluate the generality of analogical reasoning in large language models, arXiv 2402.08955 (2024).
* Books: A. Newell and H. A. Simon, Human Problem Solving (1972); P. N. Johnson-Laird, How We Reason (2006); K. J.
  Holyoak and R. G. Morrison (eds.), The Oxford Handbook of Thinking and Reasoning (2012).

## Problems and solutions

**1. The hardest syllogism.** Use the eight kinds of thing to show that *No $A$ are $B$; all $B$ are $C$* has exactly one valid conclusion, and say which.

*Solution.* Take the eight kinds of thing over A, B, C. *No A are B* empties every kind that is
both A and B; *all B are C* empties every kind that is B but not C. B names something, so the kind B, C, not A is
inhabited: there are Cs that are not As, and *some C are not A* is true in every model. Every other answer fails
somewhere: *no A are C* fails if the kind A, C, not B is inhabited; *some A are C* and *some A are not C* fail
depending on whether A's members lie inside C; *all C are A* fails because of the Bs; and the a-to-c forms have the
same counterexamples. So the one valid conclusion is *some C are not A*, which 4% of Ragni's 139 people chose; the
commonest answer, *no A are C*, does not follow.

**2. Without existential presupposition.** Without existential presupposition, which of the 27 valid syllogisms lose their conclusion? Explain why *all $A$ are $B$; all $B$ are $C$* still implies *some $A$ are $C$* only if $A$ is nonempty.

*Solution.* Allow empty terms (the empty model and every model with an empty set).
Then 22 of the 64 syllogisms keep a conclusion and five lose theirs: AA4, AE2, AE4, EA1 and EA4. Each needs some
term to be inhabited to produce a particular conclusion: in AA4, *all B are A* and *all B are C* give *some A are
C* only if some B exists; in EA1, the Cs that are not As are the Bs. Likewise *all A are B; all B are C* gives *some
A are C* only if A is nonempty, though *all A are C* survives either way.

**3. When not-q is worth turning.** For optimal data selection with an even prior, show that the not-$q$ card's information gain does not depend on $P(q)$, and find where the $q$ card falls below it when $P(p) = 0.1$.

*Solution.* Under dependence (M_D) a not-q card never has p on the back; under independence
(M_I) it has p with probability P(p) = a. Neither depends on P(q), so the card's expected gain, the prior entropy
minus the expected posterior entropy, is a function of a alone (0.052 bits at a = 0.1). For the q card the hidden
side is p with probability a/b under M_D and a under M_I; as b grows the two predictions converge and the gain falls
toward zero. With a = 0.1 and an even prior, Psyche finds the q card falls below the not-q card at P(q) ≈ 0.32.

**4. The tower.** Show that the Tower of Hanoi with $n$ discs has $3^n$ states and needs $2^n - 1$ moves, and that the goal stack's longest pause comes before the first move.

*Solution.* Each disc is on one of three pegs, and the order on a peg is forced (largest at the bottom), so
there are 3^n states. To move n discs, the n − 1 above the largest must first go to the spare peg, the largest moves
once, and the n − 1 follow: T(n) = 2T(n − 1) + 1 with T(1) = 1, so T(n) = 2^n − 1, and no shorter path exists since
the largest disc must move and both transfers of the rest are themselves minimal. The goal stack pushes one subgoal
for each smaller disc in the way before its first move: n − 1 of them before move 1, more than anywhere else, so the
first pause is the longest (5.5 units for four discs).

**5. Causal power.** Derive causal power $q = \Delta P / (1 - P(e \mid \neg c))$ from the noisy-OR model, and find the corresponding power for a cause that prevents the effect.

*Solution.* Suppose the background produces the effect with probability b and the cause, independently,
with probability q (a noisy-OR). Then P(e | c) = 1 − (1 − b)(1 − q) = b + q(1 − b), and P(e | ¬c) = b. So q = (P(e |
c) − b)/(1 − b) = ΔP/(1 − P(e | ¬c)). For a preventive cause that stops the effect with probability p, P(e | c) =
b(1 − p), so p = −ΔP / P(e | ¬c): its power is measured against how often there is anything to prevent.

**6. Mirror pairs.** With `explainer.psychology.opendata': fit each person's rotation rate separately for same and mirror pairs. Are mirror pairs rotated at the same speed?

*Solution.* Fitting correct mirror trials person by person gives a median slope of 6.9 ms per degree (about
145 degrees a second), against 10.8 for same trials, but mirror pairs start slower: their mean at 0 degrees is 2,332
ms against 1,563. People seem to rotate until the shapes ought to match, find they do not, and then decide, which
adds a constant and flattens the slope; a mirror pair at 0 degrees still needs the check. The rate on mirror
trials is therefore not a clean measure of rotation speed.

**7. ★ Two priors, one person.** Design an experiment that separates a power-law prior from an Erlang prior in people's everyday predictions, person by person.

*Solution.* Teach each person a new quantity (say, the lifetimes of an invented machine) by
showing many examples drawn from either a power law or an Erlang distribution, then ask for predictions of the
total at several values of t. A power-law prior predicts totals proportional to t; an Erlang prior predicts roughly
t plus a constant. Fit both rules to each person's predictions and compare them by a cross-validated score, checking
with simulated people that the design can tell the rules apart at the number of trials planned. Iterated learning
(Lewandowsky, Griffiths and Kalish 2009), in which each person's predictions train the next, is another way to read
out an individual's prior.

## Open checks

Before the narrated master:

* Wason's "about one in ten" and Griggs and Cox's "about three in four" are the usually quoted shares; the film
  gives them as rough shares.
* Evans, Barston and Pollard's acceptance rates (89, 56, 71 and 10 percent) are from their table as reprinted by
  Evans et al. (2001); check them against the 1983 paper.
* Oaksford and Chater's card frequencies (.89, .62, .25, .16; 13 studies, 845 people) are from their 1994 table.
* Gick and Holyoak's shares (about 10, 30 and 75 percent) are summaries across their experiments, given as rough
  shares on screen and in the narration.
* Macnamara, Hambrick and Oswald's percentages are from the abstract; Schmidt and Hunter's and Sackett et al.'s
  validities (.51, .54, .51, .38; .31, .33, .42, .19) are from the papers' tables.
* LeGris et al.'s 1,729 people and 64% are from the paper's abstract; the 2013 "complete waste of time" is from an
  interview with Google's head of people operations, not a published study.
* The Ragni (CCOBRA) and Ganis and Kievit files are fetched on first use, checked by SHA-256 and never committed.
* The warmth curves, the chess recall bars, the flat block figures and the ARC-style task are schematics or
  inventions and say so on screen.
