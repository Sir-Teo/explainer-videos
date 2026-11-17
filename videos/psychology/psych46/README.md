# Psychology, Built: Part 46, Scaling, Surveys and Choice

In 1927 Louis Thurstone asked students which of two offences was more serious, for every pair, and derived a scale
of seriousness from their inconsistencies. Duncan Luce later replaced Thurstone's normal curves with a single axiom,
and Daniel McFadden turned the result into the logit model that forecasts how people travel and what they buy. Then a
decoy that no one chose was shown to change what people did choose. This part turns preferences and answers into
numbers, and shows where the numbers bend.

The viewer makes paired comparisons and predicts four numbers. Then Thurstone's Case V, derived as signal detection
between two stimuli and fitted to Guilford's vegetables; Luce's axiom and Bradley-Terry by the MM algorithm; random
utility, with Gumbel noise giving the logit (simulated) and McFadden's forecast; the red bus and the blue bus
(computed); the decoy, compromise and similarity effects, and a comparing chooser that produces the first two and
predicts their growth with deliberation (computed); a choice-based conjoint study recovering part-worths and
willingness to pay, and a market simulation (computed); Tourangeau's four steps and Krosnick's satisficing; wording,
order and acquiescence (computed); the number of scale points (computed); careless respondents who inflate alpha and
manufacture correlations (computed); and the net promoter score and its error (computed).

## Where the numbers come from

| What | Source |
|---|---|
| Guilford's vegetables: nine vegetables, every pair; corn preferred to turnips by 92.6%; the Case V scale from turnips (-0.99) to corn (0.64); the nine values reproduce the 72 proportions within 3.5 points on average; Bradley-Terry by MM in 93 updates, correlation 0.9997 with Case V and slope 1.72 | `opendata.vegetables_guilford` (psychTools 2.6.4, fetched from CRAN and SHA-256 checked); Psyche (`scaling.thurstone_scale`, `scaling.btl_fit`), item `veg` |
| Gumbel random utility: utilities 0, 0.5 and 1; 400,000 simulated choices give 0.186, 0.307, 0.506 against the logit's 0.186, 0.307, 0.506 | Psyche (`scaling.gumbel_choice_shares`), item `gumbel` |
| Red bus, blue bus: the logit's thirds against 0.49, 0.25, 0.25 with nearly identical buses (correlated normal noise) | Psyche (`scaling.normal_choice_shares`), item `redbus` |
| The comparing chooser: A (6, 4) and B (4, 6) split 50:50; a decoy below A raises A to 50% after 5 comparisons and 76% after 40; a decoy below B lowers A to 22%; an extreme option beyond A puts A in the middle, 38% against 31% (40 comparisons; no effect after 5) | Psyche (`scaling.pairwise_sampler`, 60,000 simulated choices per menu), item `decoy` |
| Conjoint: phones with price ($400, $600, $800), battery, camera and brand; 600 simulated people with varying part-worths, 12 tasks each (7,200 choices); estimates -0.53 per $100, 0.84, 0.48, 0.28, -0.19 against averages -0.6, 0.9, 0.5, 0.3, -0.2; willingness to pay about $160 for a two-day battery and $92 for a great camera (planted: $150 and $83); market shares 36%, 27%, 37%, and 49% for the first phone at $500 | Psyche (`scaling.conjoint_design`, `scaling.fit_clogit`), item `conjoint` |
| Scale points: the correlation of a rating with a continuous attitude, 0.80 for 2 points, 0.89 for 3, 0.94 for 5, 0.96 for 7, 0.97 for 11 | 200,000 simulated answers, item `points` |
| Acquiescence: two unrelated traits, six items each; with an agreeing style (loading 0.4) and one-way keys the scales correlate 0.25; balanced keys 0.01 | Psyche (`scaling.styled_answers`, 20,000 simulated people), item `acq` |
| Careless respondents: two six-item scales with traits correlated 0.3; as straightliners rise from 0 to 30%, alpha rises from 0.75 to 0.92 and the scales' correlation from 0.24 to 0.75 | Psyche (`scaling.straightline`, 5,000 simulated people), item `careless` |
| The net promoter score: a simulated population with 23% promoters and 42% detractors (NPS -20); standard error 11.3 points from 50 customers, 5.5 from 200, 2.5 from 1,000; with 200 customers each, the better of two products ranked first 90% of the time by NPS and 91% by the mean | Psyche (`scaling.nps`, `scaling.nps_se`), item `nps` |
| How many judges: nine stimuli spread evenly over 2.4 SDs, panels of 5 to 400 judges under Case V (100 panels each); the scale values miss by 0.35, 0.22, 0.14, 0.09, 0.06, 0.03 SD with 5, 10, 25, 50, 100, 400 judges | Psyche (`scaling.simulate_pairs`, `scaling.thurstone_scale`), item `judges` |
| A leaderboard from random votes: 20 entrants with Bradley-Terry log-strengths from -1.5 to 1.5, 50 to 3,200 votes on random pairs, fitted by MM with a pseudo-vote of 0.05 each way on every pair (100 boards each); rank correlation 0.66 after 50 votes, 0.94 after 400, 0.99 after 3,200; the true best ranked first 17%, 42% and 81% of the time | Psyche (`scaling.btl_fit`), item `arena` |
| How many respondents: the conjoint study rerun 40 times at 50 to 800 people; the middle 80% of the battery's willingness to pay spans $119 to $194 with 50 people and $144 to $159 with 800 (planted $150) | Psyche (`scaling.simulate_conjoint`, `scaling.fit_clogit`), item `wtp_n` |
| Attention checks: with k checks a random responder (passing each with probability 1/5) is caught with probability 1 - 0.2^k, and an attentive person (slipping one time in fifty, an assumption) is excluded with probability 1 - 0.98^k: 80% and 2% for one check, 99.2% and 5.9% for three, 99.97% and 9.6% for five | arithmetic, item `checks` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

The phones, the holiday comparisons on screen and the offences in the hook are illustrations; Thurstone's offence
list is named only by example.

## Built in this part

* `explainer/psychology/psyche/scaling.py`: Thurstone's Case V (probabilities, simulation, scaling), Bradley-Terry
  by Hunter's MM algorithm, Luce's axiom checked, the logit and Gumbel random utility, correlated-noise choice
  shares, McFadden's conditional logit by Newton, a pairwise-comparison sampler that produces the attraction and
  compromise effects, a conjoint designer and simulator, acquiescent answers, straightlining and the net promoter
  score with its standard error. Tested in `tests/psychology/test_scaling.py`.
* `explainer/psychology/opendata.py` reads Guilford's vegetable comparisons from psychTools 2.6.4.
* The Ledger gains four rows.
* The course's interactive: twelve paired comparisons of the reader's own, turned into a Bradley-Terry scale, then
  a menu with a decoy; nothing is stored.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Adding an option that is clearly worse than one alternative, but not the other, raises the share of the alternative that dominates it. | Huber, Payne and Puto 1982 | contested |
| Asking whether something should be forbidden or whether it should be allowed gives different answers, though the questions are logically the same. | Rugg 1941 | replicated |
| Some respondents tend to agree with statements regardless of their content, and the tendency is stable enough to distort scales keyed in one direction. | Cronbach 1946 | replicated |
| One question, how likely a customer is to recommend a company, predicts its growth better than other measures of customer satisfaction. | Reichheld 2003 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Thurstone; McFadden; Simonson and
Tversky; Tourangeau, Rips and Rasinski; Krosnick; Likert; Hainmueller, Hopkins and Yamamoto.

## Build it

```bash
python -m videos.psychology.psych46.compute            # every number (a minute; fetches the data once)
python tools/qa_scene.py psych46 Models                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych46 -q l   # the whole part, silent preview
python tools/build.py psych46                          # 1080p30 with narration
python tools/qa_scene.py psych46 Effects --lang zh     # the Chinese edition of one chapter
python tools/make.py psych46                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 46                    # the lab: Case V, Bradley-Terry, the logit, decoys, conjoint
python tools/check_ledger.py psych46                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's scaling module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Which crime is worse? | Thurstone's comparisons; from a choice to a number; the question; objectives |
| 1 | On you: twelve comparisons, and four numbers | Six pairs on you; four predictions |
| 2 | The law of comparative judgment | Two fluctuating impressions; nine vegetables; how many judges? |
| 3 | Luce's choice axiom | One axiom; fitting it by an algorithm that always climbs; a leaderboard from random votes |
| 4 | Random utility | Gumbel noise gives the logit; McFadden's forecast |
| 5 | Where the axiom fails | The red bus and the blue bus; decoys and compromises |
| 6 | Models of context effects | A chooser who compares; more thought, more context |
| 7 | Conjoint analysis | A choice task; part-worths recovered; a market simulated; how many respondents? |
| 8 | Between the question and the answer | Four steps; optimizing or satisficing |
| 9 | Question effects | Wording and order; agreeing with everything |
| 10 | Rating scales | Likert's shortcut; how many points? |
| 11 | Data quality online | Careless answers make scales look better; finding the careless; how many checks? |
| 12 | One number to rule them all? | The net promoter score; a noisy number |
| 13 | The Ledger | Four rows; what they have in common |
| 14 | In practice: pricing, polls and leaderboards | Where the models run; leaderboards are paired comparisons |
| 15 | Frontier: causes, preferences and simulated respondents | Three frontiers; open questions |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; Kant's three objections; payoffs; problems; references; Part 47 |

## Sources

* L. L. Thurstone, A law of comparative judgment, *Psychological Review* 34 (1927) 273-286; L. L. Thurstone, The
  method of paired comparisons for social values, *Journal of Abnormal and Social Psychology* 21 (1927) 384-400;
  J. P. Guilford, *Psychometric Methods* (2nd edition, McGraw-Hill, 1954).
* R. A. Bradley and M. E. Terry, Rank analysis of incomplete block designs I, *Biometrika* 39 (1952) 324-345;
  R. D. Luce, *Individual Choice Behavior* (Wiley, 1959); D. R. Hunter, MM algorithms for generalized Bradley-Terry
  models, *Annals of Statistics* 32 (2004) 384-406.
* D. McFadden, Conditional logit analysis of qualitative choice behavior, in P. Zarembka (ed.), *Frontiers in
  Econometrics* (Academic Press, 1974) 105-142; D. McFadden, The measurement of urban travel demand, *Journal of
  Public Economics* 3 (1974) 303-328; K. E. Train, *Discrete Choice Methods with Simulation* (2nd edition, Cambridge,
  2009).
* A. Tversky, Elimination by aspects: a theory of choice, *Psychological Review* 79 (1972) 281-299; J. Huber, J. W.
  Payne and C. Puto (1982); I. Simonson, Choice based on reasons: the case of attraction and compromise effects,
  *Journal of Consumer Research* 16 (1989) 158-174; R. M. Roe, J. R. Busemeyer and J. T. Townsend, Multialternative
  decision field theory, *Psychological Review* 108 (2001) 370-392; S. Frederick, L. Lee and E. Baskin (2014); S. Yang
  and M. Lynn (2014).
* R. D. Luce and J. W. Tukey, Simultaneous conjoint measurement, *Journal of Mathematical Psychology* 1 (1964) 1-27;
  P. E. Green and V. Srinivasan, Conjoint analysis in marketing, *Journal of Marketing* 54 (1990) 3-19; J.
  Hainmueller, D. J. Hopkins and T. Yamamoto, Causal inference in conjoint analysis, *Political Analysis* 22 (2014)
  1-30.
* R. Tourangeau, L. J. Rips and K. Rasinski, *The Psychology of Survey Response* (Cambridge, 2000); J. A. Krosnick,
  Response strategies for coping with the cognitive demands of attitude measures in surveys, *Applied Cognitive
  Psychology* 5 (1991) 213-236; D. Rugg (1941); H. Schuman and S. Presser (1981); H.-J. Hippler and N. Schwarz (1986).
* R. Likert, A technique for the measurement of attitudes, *Archives of Psychology* 140 (1932); L. J. Cronbach
  (1946); J. B. Billiet and M. J. McClendon (2000); B. Weijters, M. Geuens and N. Schillewaert (2010); A. W. Meade and
  S. B. Craig, Identifying careless responses in survey data, *Psychological Methods* 17 (2012) 437-455.
* F. F. Reichheld (2003); T. L. Keiningham, B. Cooil, T. W. Andreassen and L. Aksoy (2007).

## Problems and solutions

1. **Case V.** Under Thurstone's Case V, 84% prefer $j$ to $i$. How far apart are they, in units of $\sigma$?

   *Solution.* Φ⁻¹(0.84) ≈ 1, so s_j - s_i = σ√2 × 1 ≈ 1.41σ.
2. **Luce.** Luce strengths $v = (1, 2, 4)$. Find $P(2 \succ 1)$, the shares from the menu $\{1, 2, 3\}$, and check that the odds of 2 over 1 are the same in both.

   *Solution.* P(2 ≻ 1) = 2/3. From {1, 2, 3}: 1/7, 2/7 and 4/7. The odds of 2 over 1 are 2 in both, as the axiom
   requires.
3. **Logit shares.** A logit with utilities $0$, $\ln 2$ and $\ln 3$. Find the choice shares.

   *Solution.* e^0, e^(ln 2), e^(ln 3) are 1, 2, 3: shares 1/6, 1/3 and 1/2.
4. **Red bus.** Car and red bus are equally liked. Add an identical blue bus. Give the logit's car share and the true one.

   *Solution.* The logit gives the car 1/3; with identical buses the car keeps 1/2 and each bus takes 1/4.
5. **Willingness to pay.** A conjoint gives $-0.6$ per \$100 of price and $0.5$ for a great camera. What is the camera worth?

   *Solution.* 0.5/0.6 × $100 = $83.
6. **NPS.** 400 customers: 30% promoters, 25% detractors. Find the NPS and its standard error.

   *Solution.* 30 - 25 = 5. SE = 100 × √((0.30 + 0.25 - 0.05²)/400) = 100 × √(0.5475/400) = 3.7 points.
7. ★ **A split-ballot survey.** Design a split-ballot survey that measures support for a policy and estimates the effect of its wording and of question order, with balanced keys.

   *Solution.* Randomize respondents to four versions: "allow" or "forbid" wording crossed with the
   policy question before or after a related question; within each, the attitude scale has half its items reversed.
   Estimate the policy support in each cell; the wording effect is the difference between wordings averaged over
   order, the order effect the difference between orders, and their interaction tests whether one changes the other;
   preregister the contrasts and the sample size for the smallest effect of interest (Part 43).

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Thurstone's 1927 papers, his offence list and the students; Guilford's vegetable data (the judges and their number,
as documented in psychTools); Luce (1959) and Bradley and Terry (1952); Hunter (2004); McFadden's BART forecast (a
predicted share near 6.3% against an observed 6.2%, and the official forecast of about 15%) and his 2000 Nobel
Prize; Tversky (1972); Huber, Payne and Puto (1982); Simonson (1989) and the evidence that time pressure weakens the
compromise effect; Frederick, Lee and Baskin (2014) and Yang and Lynn (2014); Luce and Tukey (1964); Green and
Srinivasan (1990); Tourangeau, Rips and Rasinski (2000); Krosnick (1991); Rugg's 1941 percentages; Schuman and
Presser (1981) and Hippler and Schwarz (1986); the television-hours anchor study (Schwarz and colleagues, 1985);
Likert (1932); Cronbach (1946); Billiet and McClendon (2000); Weijters, Geuens and Schillewaert (2010); Meade and
Craig (2012); Reichheld (2003) and Keiningham et al. (2007); Hainmueller, Hopkins and Yamamoto (2014); the use of
Bradley-Terry models in chatbot arenas and preference tuning; and every page range in Sources.
