# Psychology, Built: Part 28, Motivation

In 1954 a rat with a misplaced electrode keeps returning to the corner of its box where a current came on, and given
a lever it presses until it is exhausted. This part asks why anything does anything, from the body's control loops
to goals and self-control, where several of psychology's most famous findings did not survive, and recomputes the
largest test of one of them from its open data.

Olds and Milner's rat, and Psyche's learner abandoning food for a current; homeostasis from Bernard and Cannon to
Hull, a thermostat derived with its steady error and an integral term that removes it; hunger's signals (the
hypothalamus, leptin, ghrelin) and a diet as an energy-balance loop, with a settling point and a defended set point;
curiosity and puzzles, what Yerkes and Dodson's mice showed and the later inverted U, sketched; wanting against
liking, hedonic hotspots, the salt cue and incentive value recomputed from the body's state; overjustification with
self-perception as Bayes, the meta-analyses and self-determination theory; Atkinson's expectancy-times-value model,
goal-setting and implementation intentions; a discount curve on you by titration; ego depletion, a simulated
literature of a null effect and the precision-effect test, then the Registered Replication Report's 23 laboratories
as a forest plot; the marshmallow test with confounding derived and rational giving up; grit's increment over
conscientiousness computed from a meta-analysis's correlations, and growth mindset; effort as a cost with the
expected value of control. The practice chapter is incentives, weight-loss programmes and habits; the frontier is
what is spent when effort is spent, and motivation in artificial agents.

## Where the numbers come from

| What | Source |
|---|---|
| The self-stimulation learner: two levers, food worth the hunger and the current worth a fixed amount; past a current worth about 1.4 (food at its hungriest = 1) it presses the current 98% of the time and its energy store runs out | Psyche (`drive.self_stimulation`), item `stim` (five seeds per value) |
| The thermostat: k = 0.2 a minute, a window (D = −1) at minute 20; at rest 15 C with proportional control, 20 C with k_i = 0.05; half-time ln 2 / k = 3.5 minutes | Psyche (`drive.thermostat`), item `thermostat` |
| A 500-kcal cut for 300 days: the static rule promises 19.5 kg; a settling point (24 kcal a day per kg, 7,700 kcal per kg) loses 12.7 kg toward a steady 20.8 kg with a time constant of 321 days; a defended set point (hunger 60, thrift 25 kcal a day per kg below it, illustrative) loses 4.5 kg | Psyche (`drive.body_weight`, `static_rule`), item `weight`; the per-kilogram slope follows Hall et al. (2011) |
| Arousal sketch: best arousal 0.61 for an easy task and 0.31 for a hard one | Psyche (`drive.arousal_performance`), item `arousal`; illustrative |
| The salt cue: cached value −1.0 after training, decaying toward 0 in extinction; incentive value +0.9 on the first test after the state flips | Psyche (`drive.salt_cue`), item `salt` |
| Self-perception: inferred interest 0.73 after drawing unrewarded, 0.57 after drawing for a reward (prior 0.5) | Psyche (`drive.self_perception`), item `perception` |
| Titration: three hyperbolic choosers (k = 0.002, 0.02, 0.1 a day), six delays, six questions each; fitted k 0.0020, 0.0200, 0.0987; areas 0.76, 0.30, 0.11; at 30 days the procedure lands on 63.3 against a true 62.5 | Psyche (`drive.discount_titration`), item `titration` |
| A simulated literature: 1,500 studies of a null effect (10 to 40 per group), 550 published (90% significant); random-effects g = 0.49 [0.46, 0.51]; precision-effect intercept 0.04 (SE 0.05) | Psyche (`evidence.literature`, `drive.random_effects`, `drive.pet`), item `literature` |
| The Registered Replication Report: 23 laboratories, 2,141 people; Hedges's g recomputed per laboratory; random-effects d = 0.04 [−0.07, 0.14] (published: 0.04 [−0.07, 0.15]); 11 estimates above zero, 2 significant; I² = 35%; the protocol's source study g = 0.68 (47 people) | the report's open table (`opendata.ego_depletion_rrr`), item `rrr` |
| Waiting: return times with a median of 5 minutes; expected further wait at 5 minutes 1.2 (normal) or 54 (heavy-tailed); best give-up time 3.6 minutes for the heavy tail, wait it out otherwise | Psyche (`drive.remaining_wait`, `give_up_time`), item `waiting` |
| Confounding: 20,000 simulated children; waiting and later scores correlate 0.33; the slope falls from 0.33 to 0.10 (70%) with background and ability controlled, recovering the true 0.10 | Psyche (`drive.confounded_delay`), item `confound` |
| Grit: 88 samples, 66,807 people; grit and academic performance ρ = .18; grit and conscientiousness ρ = .84; grit alone explains 3.2% of variance and adds 0.3% beyond conscientiousness if conscientiousness also correlates .18 with performance (3.1% if it correlates only .10; least, 0%, at .18/.84 = .21; beyond that grit's weight turns negative and the increment grows again) | Credé, Tynan and Harms (2017) (`archive.CREDE_2017`), item `grit` |
| Effort: below a reward of about 2.25 the expected value of control says not to try; effort collapses at difficulty 1.55 (reward 4) or 2.30 (reward 8) | Psyche (`drive.evc_curve`, `intensity`), item `effort` |
| Hagger et al.'s 2010 meta-analysis: 198 tests, average d about 0.6 | Hagger, Wood, Stiff and Chatzisarantis (2010) |
| Deci, Koestner and Ryan: 128 experiments | Deci, Koestner and Ryan (1999) |

## Built in this part

* `explainer/psychology/psyche/drive.py`: a thermostat with proportional and integral control; energy balance with a
  settling point and a defended set point, and the static rule; Part 17's learner with a food lever and a current;
  an arousal sketch; the salt cue's cached and incentive values; self-perception as Bayes; Atkinson's tendency; the
  expected value of control and effort across difficulty; expected remaining waits and give-up times; a confounded
  delay-of-gratification study; Hedges's g, DerSimonian–Laird random effects and the precision-effect test; the
  adjusting-amount titration. Tested in `tests/psychology/test_drive.py`.
* `explainer/psychology/opendata.py` fetches the ego-depletion Registered Replication Report's per-laboratory table
  from OSF and checks it by SHA-256 (`ego_depletion_rrr`); the Archive registers it (`EGO_DEPLETION_RRR`).
* The Ledger gains six rows.
* The course's interactive is a delay-discounting titration on you: six delays from a day to a year, six questions
  each, one delay measured twice, with your hyperbolic k and the area under your points.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Animals work for electrical stimulation of certain brain sites, often in preference to food | Olds and Milner 1954 | replicated |
| An expected, tangible reward for an enjoyed activity reduces later free choice of it | Lepper, Greene and Nisbett 1973 | replicated (scope contested) |
| Specific, difficult goals lead to better performance than "do your best" | Locke 1968 | replicated |
| Self-control on one task impairs it on the next, as if a resource were used up | Baumeister, Bratslavsky, Muraven and Tice 1998 | failed |
| How long a preschooler waits predicts achievement years later | Shoda, Mischel and Peake 1990 | replicated, smaller |
| Grit predicts achievement beyond conscientiousness | Duckworth, Peterson, Matthews and Kelly 2007 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the history of homeostasis and
drive theory (Bernard, Cannon, Hull, saccharin), the physiology of hunger (hypothalamic lesions, leptin, ghrelin,
weight-loss physiology), Harlow's and Butler's monkeys, Yerkes and Dodson and Teigen's history, theories of
curiosity, wanting and liking's neuroscience (due a row with addiction in Part 41), self-determination theory,
Atkinson's model, the effort studies and theories, growth mindset (due a row in Part 54), the practice chapter's
applications, and the frontier's models and machine-learning papers.

## Build it

```bash
python -m videos.psychology.psych28.compute            # every number (under a minute; fetches the RRR table once)
python tools/qa_scene.py psych28 Replication           # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych28 -q l   # the whole part, silent preview
python tools/build.py psych28                          # 1080p30 with narration
python tools/qa_scene.py psych28 Wanting --lang zh     # the Chinese edition of one chapter
python tools/make.py psych28                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 28                    # the lab: loops, weight, the current, the RRR, waiting
python tools/check_ledger.py psych28                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's drive module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The rat that would not stop pressing | Olds and Milner; the lever; Psyche's learner and the current; the questions; objectives |
| 1 | Drives and homeostasis | Bernard, Cannon and Hull; the thermostat derived; integral control and allostasis; what drive reduction cannot explain |
| 2 | Hunger as control | The hypothalamus, leptin and ghrelin; a diet as a loop; a defended set point; set point or settling point |
| 3 | Beyond drives: curiosity and arousal | Harlow's puzzles and Butler's window; what Yerkes and Dodson's mice showed; the inverted U as a sketch; curiosity as an information gap |
| 4 | Wanting is not liking | Liking faces and dopamine; hedonic hotspots; the salt cue; cached against incentive value |
| 5 | Intrinsic and extrinsic | The magic markers; self-perception as Bayes; the meta-analyses; self-determination theory |
| 6 | Goals | Atkinson's model derived; specific, difficult goals and their costs; implementation intentions |
| 7 | On you: sooner or later | The titration on you and on Psyche; three discount curves and the area under them; what a discount rate measures |
| 8 | Self-control as a resource | Cookies and radishes; the strength model and glucose; a literature built on nothing; the precision-effect test |
| 9 | Twenty-three laboratories | The registered protocol; the forest plot from the open data; after the report |
| 10 | The marshmallow test | Mischel's studies; confounding derived and simulated; reliable adults; when to stop waiting |
| 11 | Grit and mindset | Grit and the meta-analysis; grit's increment computed; growth mindset |
| 12 | Effort as a cost | Avoiding demand; the expected value of control over reward and difficulty; why effort costs anything |
| 13 | The Ledger | Brain-stimulation reward; overjustification; goals; ego depletion; delay of gratification; grit |
| 14 | In practice: incentives, diets and habits | Fines that backfire; weight-loss programmes as control; habits |
| 15 | Frontier: what is spent, and machines that want | Opportunity cost; motivation in artificial agents; open problems |
| | Recap, problems, and the road ahead | Ten lines; Kant's three objections; payoffs; problems; references; Part 29 |

## Sources

Homeostasis and drives: C. Bernard, *Introduction à l'étude de la médecine expérimentale* (1865); W. B. Cannon,
*The Wisdom of the Body* (1932); C. L. Hull, *Principles of Behavior* (1943); F. D. Sheffield and T. B. Roby,
Reward value of a non-nutritive sweet taste, Journal of Comparative and Physiological Psychology 43 (1950) 471-481.

Brain-stimulation reward: J. Olds and P. Milner (1954); J. Olds (1958); A. Routtenberg and J. Lindy (1965);
W. A. Carlezon and E. H. Chartoff (2007) (full references in the Ledger).

Hunger: A. W. Hetherington and S. W. Ranson, Hypothalamic lesions and adiposity in the rat, Anatomical Record 78
(1940) 149-172; Y. Zhang et al., Positional cloning of the mouse obese gene and its human homologue, Nature 372
(1994) 425-432; M. Kojima et al., Ghrelin is a growth-hormone-releasing acylated peptide from stomach, Nature 402
(1999) 656-660; R. L. Leibel, M. Rosenbaum and J. Hirsch, Changes in energy expenditure resulting from altered body
weight, New England Journal of Medicine 332 (1995) 621-628; K. D. Hall et al., Quantification of the effect of
energy imbalance on bodyweight, Lancet 378 (2011) 826-837; E. Fothergill et al., Persistent metabolic adaptation 6
years after "The Biggest Loser" competition, Obesity 24 (2016) 1612-1619.

Curiosity and arousal: H. F. Harlow, M. K. Harlow and D. R. Meyer, Learning motivated by a manipulation drive,
Journal of Experimental Psychology 40 (1950) 228-234; R. A. Butler, Discrimination learning by rhesus monkeys to
visual-exploration motivation, Journal of Comparative and Physiological Psychology 46 (1953) 95-98; R. M. Yerkes and
J. D. Dodson (1908) and K. H. Teigen (1994) (`archive.TEIGEN_1994`); J. A. Easterbrook, The effect of emotion on cue
utilization and the organization of behavior, Psychological Review 66 (1959) 183-201; D. E. Berlyne, *Conflict,
Arousal, and Curiosity* (1960); G. Loewenstein, The psychology of curiosity: a review and reinterpretation,
Psychological Bulletin 116 (1994) 75-98; M. J. Kang et al., The wick in the candle of learning: epistemic curiosity
activates reward circuitry and enhances memory, Psychological Science 20 (2009) 963-973.

Wanting and liking: K. C. Berridge and T. E. Robinson, What is the role of dopamine in reward: hedonic impact, reward
learning, or incentive salience?, Brain Research Reviews 28 (1998) 309-369; S. Peciña, B. Cagniard, K. C. Berridge,
J. W. Aldridge and X. Zhuang, Hyperdopaminergic mutant mice have higher "wanting" but not "liking" for sweet rewards,
Journal of Neuroscience 23 (2003) 9395-9402; S. Peciña and K. C. Berridge, Hedonic hot spot in nucleus accumbens
shell, Journal of Neuroscience 25 (2005) 11777-11786; J. Zhang, K. C. Berridge, A. J. Tindell, K. S. Smith and
J. W. Aldridge, A neural computational model of incentive salience, PLoS Computational Biology 5 (2009) e1000437;
M. J. F. Robinson and K. C. Berridge, Instant transformation of learned repulsion into motivational "wanting",
Current Biology 23 (2013) 282-289; K. C. Berridge and M. L. Kringelbach, Pleasure systems in the brain, Neuron 86
(2015) 646-664.

Rewards and goals: the overjustification and goal-setting rows' references in the Ledger; D. J. Bem,
Self-perception theory, Advances in Experimental Social Psychology 6 (1972) 1-62; J. W. Atkinson, Motivational
determinants of risk-taking behavior, Psychological Review 64 (1957) 359-372.

Discounting: J. E. Mazur (1987), in *Quantitative Analyses of Behavior* V; K. N. Kirby, N. M. Petry and W. K. Bickel,
Heroin addicts have higher discount rates for delayed rewards than non-drug-using controls, Journal of Experimental
Psychology: General 128 (1999) 78-87; J. Myerson, L. Green and M. Warusawitharana, Area under the curve as a measure
of discounting, Journal of the Experimental Analysis of Behavior 76 (2001) 235-243.

Self-control: the ego-depletion, delay-of-gratification and grit rows' references in the Ledger; C. S. Dweck,
*Mindset* (2006); V. F. Sisk et al., To what extent and under which circumstances are growth mind-sets important to
academic achievement? Two meta-analyses, Psychological Science 29 (2018) 549-571; D. S. Yeager et al., A national
experiment reveals where a growth mindset improves achievement, Nature 573 (2019) 364-369.

Effort: J. W. Brehm and E. A. Self, The intensity of motivation, Annual Review of Psychology 40 (1989) 109-131;
W. Kool, J. T. McGuire, Z. B. Rosen and M. M. Botvinick, Decision making and the avoidance of cognitive demand,
Journal of Experimental Psychology: General 139 (2010) 665-682; A. Westbrook, D. Kester and T. S. Braver, What is the
subjective cost of cognitive effort?, PLoS ONE 8 (2013) e68210; A. Shenhav, M. M. Botvinick and J. D. Cohen, The
expected value of control, Neuron 79 (2013) 217-240; R. Kurzban, A. Duckworth, J. W. Kable and J. Myers, An
opportunity cost model of subjective effort and task performance, Behavioral and Brain Sciences 36 (2013) 661-679;
M. Inzlicht, A. Shenhav and C. Y. Olivola, The effort paradox, Trends in Cognitive Sciences 22 (2018) 337-349.

Practice and frontier: U. Gneezy and A. Rustichini, A fine is a price, Journal of Legal Studies 29 (2000) 1-17;
P. Lally, C. H. M. van Jaarsveld, H. W. W. Potts and J. Wardle, How are habits formed, European Journal of Social
Psychology 40 (2010) 998-1009; M. Agrawal, M. G. Mattar, J. D. Cohen and N. D. Daw, The temporal dynamics of
opportunity costs, Psychological Review 129 (2022) 564-585; J. Schmidhuber, Curious model-building control systems,
Proceedings of the International Joint Conference on Neural Networks (1991) 1458-1463; D. Pathak, P. Agrawal,
A. A. Efros and T. Darrell, Curiosity-driven exploration by self-supervised prediction, ICML (2017).

Data: the ego-depletion Registered Replication Report's per-laboratory table, osf.io/jymhe (component kh85v), no
licence stated, fetched and never redistributed.

## Problems and solutions

1. **The thermostat.** With e = x − s, de/dt = −ke + D, so e(t) = D/k + (e₀ − D/k)e^(−kt) and e → D/k. A
   proportional controller only pushes when there is an error, and to cancel a constant D it must push with force D,
   which needs an error D/k. With the integral term, any steady state needs d/dt of ∫e = e = 0, so the error at rest
   is zero; the integral holds the push the disturbance needs.
2. **The settling point.** ρ dW/dt = −c − a(W − W₀), so W − W₀ → −c/a, approached as e^(−at/ρ). Half of the loss
   takes ρ ln 2 / a: with ρ = 7,700 and a = 24, about 222 days. A defended set point adds h + g to a, shrinking both
   the loss and the time constant.
3. **Atkinson.** dT/dP = (M_s − M_af)(1 − 2P) = 0 at P = 1/2, a maximum when M_s > M_af and a minimum when
   M_s < M_af; the failure-anxious then prefer P near 0 or 1.
4. **Self-perception.** With R = 1, the posterior odds of interest are the prior odds times
   σ(β₀ + β_I + β_R)/σ(β₀ + β_R). As β_R grows, both terms tend to 1 and the ratio to 1, so the posterior falls to
   the prior: an act fully explained by its reward says nothing about the actor. (With β_R = 0 the ratio is largest.)
5. **The RRR, again.** The fixed-effect estimate is 0.036 against the random-effects 0.037: τ² is small (I² = 35%)
   and the laboratories' sample sizes are similar, so the two weightings nearly agree.
6. **Remaining waits.** E[T − t | T > t] = ∫ₜ^∞ S(u) du / S(t). Its derivative has the sign of
   h(t)·m(t) − 1, with h the hazard and m the mean residual life. For a normal T the hazard rises without bound, so m
   falls; for a Pareto T the hazard falls like 1/t and m(t) grows linearly with t.
7. ★ **A test between accounts of effort.** The resource account predicts that depletion depends on what was spent
   and carries over regardless of what comes next; the opportunity-cost account predicts that the cost of effort
   rises with the value of the alternatives available, and can be lowered by making the current task more valuable or
   the alternatives worse, with no rest. For example: hold the first task fixed, and vary whether an attractive
   alternative activity is visible during the second; or pay more for the second task without a break. Persistence
   that recovers with payment and falls with tempting alternatives favours opportunity cost.

## Open checks

This part was written in a session whose web-search allowance was used up, so the following are quoted from the
literature as widely reported and should be rechecked against the articles before the final cut:

* Baumeister et al. (1998): the radish eaters' persistence ("less than half the time" of the other groups).
* Lepper, Greene and Nisbett (1973): the expected-award group drew "about half as much"; the follow-up interval of one
  to two weeks.
* Hagger et al. (2010): 198 tests and d about 0.6; Deci, Koestner and Ryan (1999): 128 experiments.
* Vohs et al. (2021): the number of laboratories and the estimate ("close to zero"), and that Baumeister was among
  the designers.
* Watts, Duncan and Quan (2018): about 900 children, the association about half the original and two-thirds smaller
  again with controls; Kidd, Palmeri and Aslin (2013): "about four times as long".
* Gneezy and Rustichini (2000): ten centres, six with fines, and late arrivals staying high after removal.
* Lally et al. (2010): automaticity levelling off "after a couple of months" on average.
* Sisk et al. (2018): correlations "around a tenth"; Yeager et al. (2019): the effect concentrated in lower-achieving
  students.
* Routtenberg and Lindy (1965), Olds (1958) rates of "thousands an hour", the hedonic hotspots' size, and the
  1940s–50s hypothalamic lesion results are described qualitatively.
* The defended-set-point coefficients (hunger 60, thrift 25 kcal a day per kg) are illustrative; the settling-point
  slope of 24 kcal a day per kg follows Hall et al.'s rule of thumb and should be checked against the paper.
