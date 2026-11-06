# Philosophy, Built — Part 13: Degrees of Belief

Part 13 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): Bayesian epistemology.
Ramsey and de Finetti's betting measure of belief, Kolmogorov's axioms, and credences as points on the simplex; the
Dutch book, found by a linear program and proved by a separating hyperplane, with Kemeny and Lehman's converse and
the objections to betting arguments; Joyce's accuracy argument, drawn in two and three dimensions; proper scoring
rules (Brier, log, spherical) and the improper linear rule, four synthetic forecasters, calibration and Murphy's
decomposition, and their uses from meteorology to superforecasting and cross-entropy; conditionalization, the base
rate, Lewis's diachronic book, old evidence, and Jeffrey's rule; the problem of the priors, washing out and
Cromwell's rule, subjective and objective Bayesianism, Jaynes's maximum entropy; Bertrand's chords (the Wall's
thirteenth brick), van Fraassen's cube factory and Jaynes's invariance reply; the interpretations of probability,
the Principal Principle, de Finetti's representation theorem and the big bad bug; Ellsberg's urns, credal sets,
dilation and Elga's objection; the lottery and the preface, the lottery triad as a Price List, Leitgeb's stable
belief, and naked statistical evidence; Sleeping Beauty, simulated, with its bets and the double halfer; observation
selection, SSA and SIA on toy universes, the Doomsday argument, the presumptuous philosopher and fine-tuning; and
Bayesian networks, the cost of exact inference, logical omniscience and Bayesian brains.

Every number on screen is computed by the Reasoner's credence laboratory (`explainer/philosophy/reasoner/credence.py`):
the Dutch-book LP over any finite set of worlds; Euclidean projection onto the simplex and the dominance check; four
scoring rules, best reports and synthetic forecasters with calibration bins; Lewis's diachronic book and Jeffrey's
rule; the maximum-entropy die; three chord ensembles simulated 100,000 times each and the cube factory; dilation over a
credal set; the lottery, the preface and Leitgeb's stable sets; Sleeping Beauty simulated 100,000 times; and the
Doomsday argument under SSA and SIA. It is tested in `tests/philosophy/test_credence.py` and cached by
[`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy13.compute       # every computed item (a few seconds; .cache/philosophy13)
python tools/build.py philosophy13 -q l                # 480p preview
python tools/build.py philosophy13                     # 1080p30 -> renders/philosophy13.mp4
python tools/qa_scene.py philosophy13 Bertrand         # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | belief comes in degrees; Ramsey (1926); the plan. | — |
| 1 | `Ramsey` | betting quotients (Ramsey 1926, de Finetti 1937); Kolmogorov's axioms (1933); credences as points; the simplex. | — |
| 2 | `Dutch` | the bookie; the LP; the Dutch book theorem and its converse (Kemeny, Lehman 1955), by a separating hyperplane; five objections. | a 20-cent book against (0.6, 0.6); a 10-cent book against four credences, and none after repair |
| 3 | `Accuracy` | the Brier score; Joyce (1998); dominance in 2D and 3D; the theorem (Predd et al. 2009) and its fine print. | projections and their Brier scores in every world |
| 4 | `Scoring` | proper and strictly proper rules; absolute error is improper; forecasters; calibration; Murphy (1973); uses. | expected-penalty curves at p = 0.7; (0,0,0) beats (⅓,⅓,⅓) under absolute error; Brier and log scores of four forecasters; calibration bins |
| 5 | `Update` | conditionalization; base-rate neglect; Lewis's diachronic book (Teller 1973); old evidence; Jeffrey's rule (1965). | 0.4 → 0.64; 9.2% after a positive test; −0.1 in every world; 0.56 → 0.42 |
| 6 | `Priors` | the problem of the priors; washing out and Cromwell's rule; subjective and objective Bayesians; Jaynes (1957). | three priors updated on 1,000 flips; the maximum-entropy die with mean 4.5 |
| 7 | `Bertrand` | indifference; Bertrand's chords (1889); why each answer holds; the cube factory; Jaynes (1973); **the Wall's thirteenth brick**. | 100,000 chords per method: 0.333, 0.502, 0.248; ½, ¼, ⅛ |
| 8 | `Chance` | five interpretations; the Principal Principle (Lewis 1980); learning a chance; de Finetti's representation theorem; the big bad bug. | credence in a bent coin and in heads over twelve flips |
| 9 | `Imprecise` | Ellsberg (1961); credal sets; dilation (Seidenfeld and Wasserman 1993); Elga (2010); uses. | P(H \| M) = P(G) across the credal set: ½ dilates to [0, 1] |
| 10 | `Lottery` | the Lockean thesis; Kyburg (1961); Makinson (1965); **Price List**: the lottery triad; Leitgeb (2017); statistical evidence. | 0.999 per ticket, 0 for all; 0.99³⁰⁰ ≈ 0.049; the nested stable sets |
| 11 | `Beauty` | the week; halfers and thirders (Elga 2000, Lewis 2001); bets; "today is Monday"; centred worlds. | 100,000 runs: 0.500 heads per experiment, 0.333 per waking; break-even prices ⅓ and ½ |
| 12 | `Anthropic` | observation selection; SSA and SIA on toy universes; Doomsday (Carter, Leslie); the presumptuous philosopher; fine-tuning. | 0.990 on the toys; 0.999 under SSA, 0.001 then 0.5 under SIA |
| 13 | `Machines` | Bayesian networks (Pearl 1988); exact inference by enumeration and its cost (Cooper 1990; Dagum and Luby 1993); logical omniscience; Bayesian brains. | P(rain \| wet) = 0.358; joint tables of 2ⁿ entries |
| 14 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Ramsey, "Truth and Probability" (1926); de Finetti, "La prévision" (1937); Kolmogorov, *Grundbegriffe* (1933);
Keynes, *A Treatise on Probability* (1921); Jeffrey, *The Logic of Decision* (1965); Jaynes, *Probability Theory: The
Logic of Science* (2003); van Fraassen, *Laws and Symmetry* (1989); Walley, *Statistical Reasoning with Imprecise
Probabilities* (1991); Pearl, *Probabilistic Reasoning in Intelligent Systems* (1988); Bostrom, *Anthropic Bias*
(2002); Pettigrew, *Accuracy and the Laws of Credence* (2016); Leitgeb, *The Stability of Belief* (2017); Titelbaum,
*Fundamentals of Bayesian Epistemology* (2022); Hájek, "Interpretations of Probability" (SEP).

Papers: Bertrand (1889); Brier (1950); Good (1952); Kemeny (1955); Lehman (1955); Jaynes (1957, 1973); Ellsberg
(1961); Kyburg (1961); Blackwell and Dubins (1962); Makinson (1965); Savage (1971); Murphy (1973); Teller (1973);
Casscells, Schoenberger and Graboys (1978); Glymour (1980); Lewis (1980, 1994, 2001); Diaconis and Zabell (1982);
Garber (1983); Cooper (1990); Dagum and Luby (1993); Seidenfeld and Wasserman (1993); Hall (1994); Thau (1994); Joyce
(1998, 2010); Elga (2000, 2010); White (2000, 2005); Ernst and Banks (2002); Hanson (2003); Greaves and Wallace (2006);
Meacham (2008); Predd et al. (2009); Jones and Love (2011); Caie (2013); Garrabrant et al. (2016); Guo et al. (2017);
Lieder and Griffiths (2020).

## Problems and solutions

1. **A Dutch book.** c(A) + c(B) = 0.7 but c(A ∨ B) = 0.8. Sell the agent a ticket on A ∨ B for 0.8 and buy tickets
   on A and on B from her for 0.3 and 0.4. If A: she gains 1 − 0.8 on the first ticket and pays out 1 on the A ticket
   she sold, having received 0.7: net −0.1. If B: the same, −0.1. If neither: −0.8 + 0.7 = −0.1. A sure loss of ten
   cents.
2. **The log score.** f(q) = −p ln q − (1 − p) ln(1 − q). f′(q) = −p/q + (1 − p)/(1 − q) = 0 exactly when q = p, and
   f″(q) = p/q² + (1 − p)/(1 − q)² > 0, so q = p is the unique minimizer: the rule is strictly proper.
3. **A rarer disease.** P(ill | +) = 0.001 × 0.99 / (0.001 × 0.99 + 0.999 × 0.01) = 0.00099 / 0.01098 ≈ 9.0%. In
   natural frequencies: of 100,000 people, 100 are ill and 99 test positive; of the 99,900 who are well, 999 test
   positive.
4. **Jeffrey's cloth in reverse.** With P(blue) = 0.2 and P(green) = 0.8 − v, P(sold) = 0.4(0.8 − v) + 0.4(0.2) +
   0.8v = 0.4 + 0.4v. Setting this to 0.5 gives v = P(violet) = 0.25, and P(green) = 0.55.
5. **One more chord.** A random-radius chord at distance d from the centre has length 2√(1 − d²), with d uniform on
   [0, 1]. It is longer than 1 exactly when d < √3/2, so the chance is √3/2 ≈ 0.866.
6. **(Essay) Halfer or thirder?** A strong answer states which principle it keeps (no change without new evidence;
   indifference among centred possibilities; conditionalization on self-locating evidence), shows what the other
   answers give up, and faces its own cost from Chapter 11: the thirder's change of credence without news about the
   coin, the halfer's two thirds for a fair future toss, or the double halfer's abandonment of conditionalization.

## 习题与解答

1. **一个荷兰赌。** $c(A) + c(B) = 0.7$，但$c(A \lor B) = 0.8$。以0.8卖给她一张$A \lor B$的票，再分别以0.3和0.4从她那里买下$A$票和$B$票。若$A$：
   她在第一张票上得$1 - 0.8$，在卖出的$A$票上赔1，又已收到0.7：净得$-0.1$。若$B$：同样是$-0.1$。若两者都不发生：$-0.8 + 0.7 = -0.1$。
   稳输一角。
2. **对数评分。** $f(q) = -p \ln q - (1 - p)\ln(1 - q)$。$f'(q) = -p/q + (1 - p)/(1 - q) = 0$恰当$q = p$，且$f''(q) = p/q^2 + (1 - p)/(1 - q)^2 > 0$，
   所以$q = p$是唯一的最小点：这条规则是严格恰当的。
3. **更罕见的病。** $P(\text{患病} \mid +) = 0.001 \times 0.99 / (0.001 \times 0.99 + 0.999 \times 0.01) = 0.00099 / 0.01098 \approx 9.0\%$。
   用自然频数说：十万人中，100人患病，其中99人呈阳性；99,900名健康者中，999人呈阳性。
4. **反过来用杰弗里的布。** 设$P(\text{蓝}) = 0.2$、$P(\text{绿}) = 0.8 - v$，则$P(\text{售出}) = 0.4(0.8 - v) + 0.4(0.2) + 0.8v = 0.4 + 0.4v$。
   令它等于0.5，得$v = P(\text{紫}) = 0.25$，$P(\text{绿}) = 0.55$。
5. **再来一条弦。** 随机半径法得到的、离圆心距离为$d$的弦长为$2\sqrt{1 - d^2}$，$d$在$[0, 1]$上均匀分布。它长于1恰当$d < \sqrt{3}/2$，
   所以概率是$\sqrt{3}/2 \approx 0.866$。
6. **（论述题）二分之一派还是三分之一派？** 好的回答要说明自己保留哪条原则（没有新证据就不改变；在中心化的可能性之间无差别；对自我定位证据作条件化），
   指出其他答案放弃了什么，并直面第11章里自己的代价：三分之一派在没有关于硬币的新消息时改变信念度，二分之一派对一次公平的未来抛掷给出三分之二，
   或者双重二分之一派放弃条件化。
