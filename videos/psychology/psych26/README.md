# Psychology, Built: Part 26, Judgment and Choice

A disease threatens six hundred people. Described as lives saved, most people choose the sure programme; described
as deaths, most choose the gamble, though the outcomes are identical. This part asks why the same people buy
insurance and lottery tickets, and follows the answer from Bernoulli's utility through Allais's paradox to prospect
theory, then tests that theory on 1,928 open choice problems and takes the critics seriously: frequencies, simple
rules, a hot-hand fallacy that was in the statistic, and values that come from the world we sample.

The disease problem on you, in both frames, with Tversky and Kahneman's splits; expected value, the St Petersburg
game (a hundred thousand plays) and Bernoulli's logarithm, and the four axioms of expected utility; Allais's
problems as Kahneman and Tversky asked them, drawn in the probability triangle, and preference reversals; prospect
theory's reflection effect, value function, weighting function and the cumulative form of 1992; the fourfold
pattern computed from the 1992 parameters, and the common-ratio effect; four models fitted to choices13k's
described problems and cross-validated; availability, anchoring, Linda and the cab problem; natural frequencies and
take-the-best against regression out of sample in two simulated worlds; overconfidence and the calibration curve,
with the selection reply (Gigerenzer et al., Juslin) made exact on a calibrated judge, and interval overconfidence; the hot-hand bias by exact enumeration;
exponential, hyperbolic and beta–delta discounting with a computed reversal; decisions from experience, in Psyche
and in choices13k's feedback blocks; the bat and the ball, two systems, and one accumulator that mimics them; and
decision by sampling. The practice chapter is defaults, pensions and risk communication; the frontier is theories
found by machines, resource-rational anchoring, and whether risk preference is a trait.

## Where the numbers come from

| What | Source |
|---|---|
| The disease problem: 72% of 152 chose the sure programme framed as lives saved; 78% of 155 chose the gamble framed as deaths | Tversky and Kahneman (1981) |
| Prospect theory with the 1992 values: saved frame, sure 105.9 against risky 93.6; death frame, sure −438.5 against risky −353.1 | Psyche (`choice.framing`), item `framing` |
| St Petersburg: each toss adds one ducat of expected value; the median of 101 runs of 100,000 plays averages 19.4 ducats; a log-utility player pays 5.0 with wealth 10 and 20.9 with wealth 1,000,000 | Psyche (`choice.st_petersburg_ev`, `st_petersburg_ce`), item `stpete` |
| Allais: 82% chose B and 83% chose C, N = 72; in the triangle A = (0.01, 0.33), B = (0, 0), C = (0.67, 0.33), D = (0.66, 0); the 1992 values choose B and C | Kahneman and Tversky (1979), Problems 1 and 2; Psyche (`choice.triangle`, `cpt`), item `allais` |
| 80% took a sure 3,000 over 4,000 at 0.8; 92% took −4,000 at 0.8 over a sure −3,000; 65% took 4,000 at 0.2 over 3,000 at 0.25 (N = 95 each); the 1992 values make all three popular choices | Kahneman and Tversky (1979), Problems 3, 3′ and 4; Psyche, item `fourfold` |
| Value of ±100: 57.5 and −129.5 (2.25 times); a 50–50 bet against losing 100 needs a win of 274 | Psyche (`choice.value`, `cpt`), item `curves` |
| Certainty equivalents of 100 at 5% and 95%: 10.0 and 76.9; of −100: −8.3 and −83.1 | Psyche (`choice.fourfold`), item `fourfold` |
| choices13k: 13,006 problems; 1,928 described, unambiguous and without feedback; variance of the B rate 0.0431 | Peterson, Bourgin, Agrawal, Reichman and Griffiths (2021), github.com/jcpeterson/choices13k at commit 821ae7e8, fetched by `explainer.psychology.opendata` and checked by SHA-256 (no licence stated; not redistributed) |
| Mean squared error, fitted (10-fold cross-validated): expected value 0.0269 (0.0269), power utility 0.0215 (0.0215), value curve without weighting 0.0213 (0.0213), cumulative prospect theory 0.0161 (0.0162); predicting the mean 0.0431; R² 0.38, 0.50, 0.51, 0.63 | Psyche (`choice.fit_model`, `cv_models`), item `c13k` |
| Fitted to the described problems: α 0.75, λ 1.13, γ 0.78, δ 0.57; to the 9,831 feedback problems: α 0.79, λ 0.83, γ 0.84, δ 0.97 | the same, item `c13k` |
| 1,266 problems seen without and with feedback; risky option against a sure one with an outcome of probability ≤ 0.1: when that outcome is the worst (42 problems), 41% to 46%; when it is the best (105), 56% to 57% | choices13k; item `c13k` |
| Anchoring: medians 25 and 45 after anchors 10 and 65 | Tversky and Kahneman (1974) |
| Linda: 85% of 142 chose the conjunction | Tversky and Kahneman (1983) |
| The cab problem: 12 of the 29 cabs called Blue are Blue, 0.41; median answer 0.80 | Psyche (`choice.bayes`, `natural_frequencies`), item `bayes`; Tversky and Kahneman (1982) |
| Mammography: 8 of 103 positives have cancer, 7.8%; Bayesian answers about 16% with probabilities and 46% with frequencies | Psyche, item `bayes`; Gigerenzer and Hoffrage (1995) |
| Take-the-best against regression and tallying, 6 binary cues, 120 objects, 300 worlds a point: in the non-compensatory world (weights 8, 4, …, noise 3) take-the-best leads by 5.4 points with 8 objects and up to 15 objects | Psyche (`choice.heuristics_cv`), item `ttb` |
| Calibration: a judge that answers with a cue of validity 0.55 to 0.95 and states that validity; 200,000 questions. Drawn at random: sure 75%, right 75%. Keeping every misleading question and three in five of the rest: sure 74%, right 64% | `compute.py`, item `calibration` |
| The hot hand: four flips, expected share of heads after a head 17/42 = 0.405; 100 shots after three hits, 0.460 (200,000 simulated sequences) | Psyche (`choice.streak_exact`, `streak_sim`), item `hothand` |
| Hyperbolic k = 0.05 a week: 100 sooner against 110 four weeks later reverses at 20 weeks; exponential 0.97 a week never reverses | Psyche (`choice.discount`, `reversal_delay`), item `time` |
| A 10% outcome is missed by seven draws 48% of the time; P(risky) described against seven draws: 0.36/0.58, 0.79/0.52, 0.10/0.48, 0.69/0.42 | Psyche (`choice.p_never_seen`, `sample_choices`, `cpt`), item `experience` |
| One accumulator started near the intuitive answer: fastest fifth 97% intuitive, slowest fifth 79% checked | Psyche (Part 25's `decide.simulate`), item `systems` |
| Decision by sampling in an illustrative account (credits median 150, debits median 60, lognormal): losing 100 ranks 0.68, gaining it 0.35, 1.9 times as large | Psyche (`choice.dbs_value`), item `sampling` |
| Resource-rational anchoring: anchor 40 points away, each step removes 12%; best stop after 21 steps (cheap time) or 12 (dear), leaving 2.7 or 8.6 points of bias | Psyche, item `rational` |
| Organ donation consent: Germany (opt in) 12%, Austria (opt out) 99.98% | Johnson and Goldstein (2003) |
| Save More Tomorrow: 3.5% to 13.6% over four pay rises | Thaler and Benartzi (2004) |

## Built in this part

* `explainer/psychology/psyche/choice.py`: lotteries, expected value and utility, the St Petersburg game and
  Bernoulli's price, the probability triangle and expected utility's slope; the value function, the Tversky–
  Kahneman and Prelec weighting functions, cumulative prospect theory for one lottery or many at once, certainty
  equivalents and the fourfold pattern, the disease problem; four choice models fitted by least squares and
  cross-validated; Bayes's rule and natural frequencies; simulated environments, take-the-best, tallying and
  regression out of sample; the streak statistic exactly and by simulation; exponential, hyperbolic and beta–delta
  discounting and the reversal point; choices from small samples; decision by sampling. Tested in
  `tests/psychology/test_choice.py`.
* `explainer/psychology/opendata.py` gains choices13k (CSV and JSON, nothing evaluated).
* The Battery gains task 9, risky and delayed choices (`battery.run("gambles", ...)`).
* The Ledger gains six rows; the Archive one dataset.
* The course's interactive puts the disease problem and a ladder of sure amounts against gambles to you, and draws
  your own fourfold pattern.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Described as lives saved, most people choose a sure programme; described as deaths, the gamble | Tversky and Kahneman 1981 | replicated |
| An arbitrary number considered before an estimate pulls the estimate toward it | Tversky and Kahneman 1974 | replicated |
| The Allais pattern: a sure gain preferred, then the preference reversed when a common chance is removed | Kahneman and Tversky 1979 | replicated |
| A conjunction judged more probable than one of its parts | Tversky and Kahneman 1983 | replicated |
| Losses weigh about twice as much as equal gains | Kahneman and Tversky 1979 | contested |
| The hot hand is a cognitive illusion | Gilovich, Vallone and Tversky 1985 | story and record |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the history (Pascal and Fermat,
Bernoulli, von Neumann and Morgenstern, Savage, Friedman and Savage), theories described (Quiggin, Parducci, two
systems), preference reversals with Grether and Plott's replication, take-the-best as a rule tested in simulation,
the description–experience gap with its meta-analysis, and the practice and frontier chapters' studies (defaults and
Save More Tomorrow are due rows in Part 55, risk preference as a trait in Part 33).

## Build it

```bash
python -m videos.psychology.psych26.compute            # every number (about a minute; fetches choices13k once)
python tools/qa_scene.py psych26 Thirteen              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych26 -q l   # the whole part, silent preview
python tools/build.py psych26                          # 1080p30 with narration
python tools/qa_scene.py psych26 Prospect --lang zh    # the Chinese edition of one chapter
python tools/make.py psych26                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 26                    # the lab: prospect theory on open choice data
python tools/check_ledger.py psych26                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's choice module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Six hundred lives | The disease problem on you in both frames; the splits; Bernoulli to the Nobel; the questions; objectives |
| 1 | The standard: expected value and utility | Expected value; St Petersburg; Bernoulli's concave utility; the four axioms |
| 2 | The violations | Allais's problems; the probability triangle; preference reversals |
| 3 | Prospect theory | Reflection; the value function; the weighting function; the cumulative form |
| 4 | The fourfold pattern | Certainty equivalents computed; the four cells; the common-ratio effect |
| 5 | Thirteen thousand gambles | choices13k; four models cross-validated; predicted against observed; the fitted curves |
| 6 | Heuristics and biases | Availability, representativeness, anchoring; Linda; the cab problem |
| 7 | The reply: frequencies and fast, frugal rules | Natural frequencies; take-the-best; out of sample in two worlds |
| 8 | The hot hand | The 1985 study; all sixteen sequences of four flips; the bias and the hot hand restored |
| 9 | Choice over time | Exponential and hyperbolic discounting; a reversal computed; beta and delta |
| 10 | Decisions from experience | Sampling paradigm; rare events never seen; the gap in Psyche; feedback in choices13k |
| 11 | Two systems? | The bat and the ball; System 1 and System 2; one accumulator with a biased start |
| 12 | Where values come from | Decision by sampling; range and frequency; efficient coding |
| 13 | The Ledger | Framing; anchoring; Allais; Linda; loss aversion; the hot hand |
| 14 | In practice: defaults, pensions and risk | Organ donation defaults; Save More Tomorrow; relative and absolute risk |
| 15 | Frontier: theories found by machines | Machine-learned theories; resource-rational anchoring; risk preference as a trait |
| | Recap, problems, and the road ahead | Ten lines; Kant's three objections; payoffs; problems; references; Part 27 |

## Sources

* D. Bernoulli, Specimen theoriae novae de mensura sortis (1738), translated as Exposition of a new theory on the
  measurement of risk, Econometrica 22 (1954) 23-36.
* J. von Neumann and O. Morgenstern, Theory of Games and Economic Behavior (1944; 2nd ed. 1947); L. J. Savage, The
  Foundations of Statistics (1954).
* M. Friedman and L. J. Savage, The utility analysis of choices involving risk, Journal of Political Economy 56
  (1948) 279-304.
* M. Allais, Le comportement de l'homme rationnel devant le risque, Econometrica 21 (1953) 503-546; M. J. Machina,
  "Expected utility" analysis without the independence axiom, Econometrica 50 (1982) 277-323.
* S. Lichtenstein and P. Slovic, Reversals of preference between bids and choices in gambling decisions, Journal
  of Experimental Psychology 89 (1971) 46-55; D. M. Grether and C. R. Plott, Economic theory of choice and the
  preference reversal phenomenon, American Economic Review 69 (1979) 623-638; A. Tversky, P. Slovic and D. Kahneman,
  The causes of preference reversal, American Economic Review 80 (1990) 204-217.
* D. Kahneman and A. Tversky, Prospect theory: an analysis of decision under risk, Econometrica 47 (1979) 263-291;
  A. Tversky and D. Kahneman, Advances in prospect theory: cumulative representation of uncertainty, Journal of Risk
  and Uncertainty 5 (1992) 297-323; J. Quiggin, A theory of anticipated utility, Journal of Economic Behavior and
  Organization 3 (1982) 323-343; D. Prelec, The probability weighting function, Econometrica 66 (1998) 497-527.
* A. Tversky and D. Kahneman, The framing of decisions and the psychology of choice, Science 211 (1981) 453-458;
  A. Kuhberger, The influence of framing on risky decisions: a meta-analysis, Organizational Behavior and Human
  Decision Processes 75 (1998) 23-55.
* A. Tversky and D. Kahneman, Availability: a heuristic for judging frequency and probability, Cognitive Psychology
  5 (1973) 207-232; Judgment under uncertainty: heuristics and biases, Science 185 (1974) 1124-1131; Extensional
  versus intuitive reasoning: the conjunction fallacy in probability judgment, Psychological Review 90 (1983)
  293-315; Evidential impact of base rates, in D. Kahneman, P. Slovic and A. Tversky (eds), Judgment Under
  Uncertainty (1982).
* G. Gigerenzer and U. Hoffrage, How to improve Bayesian reasoning without instruction: frequency formats,
  Psychological Review 102 (1995) 684-704; G. Gigerenzer and D. G. Goldstein, Reasoning the fast and frugal way:
  models of bounded rationality, Psychological Review 103 (1996) 650-669; G. Gigerenzer, P. M. Todd and the ABC
  Research Group, Simple Heuristics That Make Us Smart (1999), with J. Czerlinski, G. Gigerenzer and D. G.
  Goldstein's chapter on how good simple heuristics are.
* T. Gilovich, R. Vallone and A. Tversky, The hot hand in basketball, Cognitive Psychology 17 (1985) 295-314; J. B.
  Miller and A. Sanjurjo, Surprised by the hot hand fallacy? A truth in the law of small numbers, Econometrica 86
  (2018) 2019-2047.
* G. Ainslie, Specious reward, Psychological Bulletin 82 (1975) 463-496; J. E. Mazur, An adjusting procedure for
  studying delayed reinforcement (1987); K. N. Kirby and R. J. Herrnstein, Preference reversals due to myopic
  discounting of delayed reward, Psychological Science 6 (1995) 83-89; E. S. Phelps and R. A. Pollak, On second-best
  national saving and game-equilibrium growth, Review of Economic Studies 35 (1968) 185-199; D. Laibson, Golden eggs
  and hyperbolic discounting, Quarterly Journal of Economics 112 (1997) 443-477.
* R. Hertwig, G. Barron, E. U. Weber and I. Erev, Decisions from experience and the effect of rare events in risky
  choice, Psychological Science 15 (2004) 534-539; D. U. Wulff, M. Mergenthaler-Canseco and R. Hertwig, A
  meta-analytic review of two modes of learning and the description-experience gap, Psychological Bulletin 144
  (2018) 140-176.
* S. Frederick, Cognitive reflection and decision making, Journal of Economic Perspectives 19(4) (2005) 25-42;
  K. E. Stanovich and R. F. West, Individual differences in reasoning, Behavioral and Brain Sciences 23 (2000)
  645-665; J. St B. T. Evans and K. E. Stanovich, Dual-process theories of higher cognition, Perspectives on
  Psychological Science 8 (2013) 223-241; G. Keren and Y. Schul, Two is not always better than one, Perspectives on
  Psychological Science 4 (2009) 533-550; A. W. Kruglanski and G. Gigerenzer, Intuitive and deliberate judgments
  are based on common principles, Psychological Review 118 (2011) 97-109.
* N. Stewart, N. Chater and G. D. A. Brown, Decision by sampling, Cognitive Psychology 53 (2006) 1-26; A. Parducci,
  Category judgment: a range-frequency model, Psychological Review 72 (1965) 407-418; L. Walasek and N. Stewart, How
  to make loss aversion disappear and reverse, Journal of Experimental Psychology: General 144 (2015) 7-11.
* E. J. Johnson and D. Goldstein, Do defaults save lives?, Science 302 (2003) 1338-1339; I. P. Levin and G. J.
  Gaeth, How consumers are affected by the framing of attribute information before and after consuming the
  product, Journal of Consumer Research 15 (1988) 374-378; R. H. Thaler and S. Benartzi, Save More Tomorrow, Journal
  of Political Economy 112 (2004) S164-S187; G. Gigerenzer et al., Helping doctors and patients make sense of health
  statistics, Psychological Science in the Public Interest 8 (2007) 53-96; A. Furedi, The public health implications
  of the 1995 'pill scare', Human Reproduction Update 5 (1999) 621-626.
* J. C. Peterson, D. D. Bourgin, M. Agrawal, D. Reichman and T. L. Griffiths, Using large-scale experiments and
  machine learning to discover theories of human decision-making, Science 372 (2021) 1209-1214; I. Erev, E. Ert,
  O. Plonsky, D. Cohen and O. Cohen, From anomalies to forecasts, Psychological Review 124 (2017) 369-409;
  F. Lieder and T. L. Griffiths, Resource-rational analysis, Behavioral and Brain Sciences 43 (2020) e1; F. Lieder,
  T. L. Griffiths, Q. J. M. Huys and N. D. Goodman, The anchoring bias reflects rational use of cognitive
  resources, Psychonomic Bulletin & Review 25 (2018) 322-349; R. Frey, A. Pedroni, R. Mata, J. Rieskamp and
  R. Hertwig, Risk preference shares the psychometric structure of major psychological traits, Science Advances 3
  (2017) e1701381.
* The Ledger's further sources (Jacowitz and Kahneman; Klein et al.; Maniadis, Tufano and List; Huck and Müller;
  Ruggeri et al.; Fiedler; Hertwig and Gigerenzer; Mellers, Hertwig and Kahneman; Gal and Rucker; Mrkva et al.) are
  listed in its rows.

## Problems and solutions

1. **Parallel lines.** Show that every expected-utility indifference line in the probability triangle has slope $(u_2 - u_1)/(u_3 - u_2)$, and so that B over A forces D over C in Allais's problems.

   *Solution.* With outcomes x1 < x2 < x3, EU = p1 u1 + p3 u3 + (1 − p1 − p3) u2, so along an indifference
   line (u1 − u2) dp1 + (u3 − u2) dp3 = 0, and dp3/dp1 = (u2 − u1)/(u3 − u2): a constant. The step from B to A is
   (+0.01, +0.33), the same as from D to C, and EU(A) − EU(B) = 0.01 (u1 − u2) + 0.33 (u3 − u2) = EU(C) − EU(D). So
   the two differences have the same sign: B over A forces D over C.
2. **The value curve alone.** With $v(x) = x^{0.88}$ and no probability weighting, which programme does the disease problem's gain frame choose? What does the weighting function add?

   *Solution.* Saved frame: 200^0.88 = 105.9 against (1/3) 600^0.88 = 92.8, so the sure programme.
   Death frame: −λ 400^0.88 = −194.9 λ against (2/3)(−λ 600^0.88) = −185.6 λ, so the gamble, for any λ. Curvature
   alone produces the framing effect. The weighting function widens the gaps (105.9 against 93.6; −438.5 against
   −353.1 with λ = 2.25), because w(1/3) and w(2/3) are below 1/3 and 2/3.
3. **Why the cumulative form.** Show that the 1979 form $\sum w(p_i)\,v(x_i)$ can prefer a lottery to one that dominates it, and that the cumulative weights cannot.

   *Solution.* Take 100 with probability 0.05. Split it into 100 with 0.025 and 99.9 with 0.025: a
   lottery dominated by the first. The 1979 form gives it weight 2 w(0.025) = 0.183 instead of w(0.05) = 0.132
   (with γ = 0.61), so it can be valued higher. Cumulative weights for the split are w(0.025) and
   w(0.05) − w(0.025), summing to w(0.05), and moving probability to a better outcome can only raise
   P(X ≥ x) and so the value: no violation of dominance.
4. **Seventeen forty-seconds.** For four fair flips, list the fourteen sequences with a flip after a head and verify that the average share of heads after a head is $17/42$.

   *Solution.* The shares after a head in the fourteen defined sequences are: HHHH 1, HHHT 2/3,
   HHTH 1/2, HHTT 1/2, HTHH 1/2, HTHT 0, HTTH 0, HTTT 0, THHH 1, THHT 1/2, THTH 0, THTT 0, TTHH 1, TTHT 0. They sum
   to 17/3, and 17/3 ÷ 14 = 17/42 = 0.405.
5. **The reversal point.** A hyperbolic discounter with $k = 0.05$ a week prefers 110 at week $t + 4$ to 100 at week $t$ for which $t$? Derive the reversal point.

   *Solution.* 110/(1 + k(t + 4)) > 100/(1 + kt) when 10 kt > 400k − 10, that is t > 40 − 1/k. With
   k = 0.05, t > 20 weeks: nearer than 20 weeks the sooner 100 is preferred, further away the 110.
6. **Prelec's function on choices13k.** With `explainer.psychology.opendata.choices13k`: fit prospect theory with Prelec's weighting function instead. Does it predict held-out problems better?

   *Solution.* With w(p) = exp(−(−ln p)^a), separately for gains and losses, fitted the
   same way: α 0.75, λ 0.98, a 0.72 for gains and 0.53 for losses; mean squared error 0.0156 (R² 0.64), 10-fold
   cross-validated 0.0156 against 0.0162 for the Tversky–Kahneman form. Slightly better, and still a
   loss-aversion coefficient near one.
7. ★ **Gap or small samples?** Design an experiment that would tell the description–experience gap from the effect of small samples alone, and say what each account predicts.

   *Solution.* One design (after Rakow and colleagues' yoked studies): give each person in a
   description group the exact outcome frequencies that a matched person in the experience group saw. If the gap
   is only sampling error, the yoked descriptions reproduce the experience group's choices; if experience itself
   changes how rare events are weighted, a gap remains. A second design forces large samples (say 100 draws), so
   rare events are seen as often as they occur: sampling error then vanishes, and any gap left is about the mode
   of learning.

## Open checks

* The 1979 and 1992 splits and parameters are quoted from the papers; the Gigerenzer and Hoffrage percentages
  (16% and 46%) and the Johnson and Goldstein consent rates are from the papers as widely reported and should be
  rechecked against the originals before the final cut.
* choices13k's payoffs are in the units of the choice prediction competitions; the film calls the stakes small
  rather than naming a currency.
* The decision-by-sampling numbers come from an illustrative simulated account, tagged as Psyche's; Stewart,
  Chater and Brown used real bank records.
