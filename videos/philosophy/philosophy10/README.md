# Philosophy, Built — Part 10: The Mind's Own Laws

Part 10 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): Descartes to Kant, and the
start of Act III, on knowledge. The skeptical crisis (Sextus Empiricus and Agrippa's trilemma, Montaigne, Galileo's
telescope); Descartes's three waves of doubt, the cogito, the clear-and-distinct rule and the Cartesian circle, and
Elisabeth of Bohemia's question about mind and body; coordinates, Descartes's method of normals and the four rules;
Spinoza's *Ethics* Part I read by the Reasoner as a graph of proofs; Leibniz's two principles, finite and infinite
analysis, least time and Snell's law, the monads, and the argument with Clarke about space; Locke's white paper,
primary and secondary qualities, three degrees of knowledge, and Molyneux's question with its answer of 2011;
Berkeley's *esse est percipi*, the master argument, abstract ideas and *The Analyst*; Hume's impressions and ideas,
the missing shade of blue, the fork, causation and its two definitions, the problem of induction, the bundle self, and
Reid's reply; Kant's question and the analytic/synthetic, a priori/a posteriori grid, the Copernican revolution, space
and time as forms of intuition, incongruent counterparts, the categories, the deduction and the second analogy, the
antinomies, transcendental idealism and its readings; non-Euclidean geometry and Eddington's eclipse, the relativized a
priori (Reichenbach, Carnap, Friedman); Hegel, briefly and honestly; and the empiricist trilemma. Its brick in **the
Wall** is "Hume; Kant": experience cannot show necessity, and reason beyond experience contradicts itself.

Every graph, count and check on screen is computed by the Reasoner's module for the early moderns
(`explainer/philosophy/reasoner/modern.py`: the citations of *Ethics* I read from R. H. M. Elwes's translation
(Project Gutenberg #3800) by `parse_ethics`, with depths, the longest chain, idle axioms, the most cited items and the
ancestors of any proposition; Descartes's method of normals by computer algebra; continued fractions finite and
infinite; the path of least time; Hume's rival rules; the missing shade; Kant's grid; chirality of a plane shape;
Gauss's spherical excess; and the deflection of starlight), tested in `tests/philosophy/test_modern.py` and cached by
[`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy10.compute       # every computed item (a few seconds; .cache/philosophy10)
python tools/build.py philosophy10 -q l                # 480p preview
python tools/build.py philosophy10                     # 1080p30 -> renders/philosophy10.mp4
python tools/qa_scene.py philosophy10 Spinoza          # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Kant's B1 sentence; Sextus and Agrippa's trilemma, Montaigne (1580), Galileo (1610); reason and experience; the plan. | — |
| 1 | `Doubt` | the *Meditations* (1641): three waves of doubt; the cogito; the clear-and-distinct rule; Arnauld's circle; Elisabeth (1643). | — |
| 2 | `Geometry` | *La Géométrie* (1637); the method of normals; the four rules of the *Discourse*. | y = x² at (1, 1): the double-root condition gives k = 3/2, and the normal is perpendicular to the tangent |
| 3 | `Spinoza` | *Ethics* I (1677) in geometrical order; what the proof of God rests on; *Deus sive Natura*. | 51 items, 102 citations, no circles, a ten-step chain, Axioms 2 and 7 never cited (7 is cited in the Latin), the nine ancestors of P11 |
| 4 | `Leibniz` | contradiction and sufficient reason; truths of reason and of fact; Fermat (1662) and Leibniz (1682) on least time; the *Monadology* (1714); Leibniz–Clarke (1715–16). | 355/113 = [3; 7, 16]; √2 = [1; 2, 2, …]; the least-time crossing point obeys Snell's law |
| 5 | `Locke` | the *Essay* (1689): white paper; primary and secondary qualities and the three basins; three degrees of knowledge; Molyneux (1688) and Held et al. (2011). | — |
| 6 | `Berkeley` | the *Principles* (1710); *esse est percipi*; the master argument; abstract ideas; *The Analyst* (1734); Johnson's stone. | the difference quotient of x² at 3 for o = 0.1 … 0.0001 |
| 7 | `Hume` | the *Treatise* (1739) and *Enquiry* (1748): impressions and ideas; the missing shade of blue; the fork. | eleven shades, one left out |
| 8 | `Cause` | constant conjunction and habit; the two definitions; the problem of induction; the bundle self; Reid (1764). | four rules that fit eight sunrises and disagree about the ninth |
| 9 | `Kant` | the *Prolegomena* (1783); the grid; the Copernican revolution (B xvi). | — |
| 10 | `Aesthetic` | space and time as forms of intuition; 7 + 5 = 12 and the triangle; incongruent counterparts (1768); Gauss's survey. | no rotation matches a flat hand to its mirror image; the octant triangle's 270°; Gauss's triangle's excess, 14.9″ |
| 11 | `Categories` | the table of judgments and the categories; the deduction (B131); the second analogy (the house and the ship). | — |
| 12 | `Antinomies` | the first antinomy as two proofs; the four antinomies and Kant's diagnosis; **the Wall's tenth brick**. | — |
| 13 | `Idealism` | appearances and things in themselves; B xxx; two worlds or two aspects (Strawson 1966, Allison 1983, Langton 1998). | — |
| 14 | `After` | Lobachevsky, Bolyai, Riemann; general relativity and the 1919 eclipse; Reichenbach (1920), Carnap, Friedman (2001). | starlight at the sun's edge: 1.75″ (Einstein), 0.88″ (Newtonian); Eddington's 1.98″ and 1.61″ |
| 15 | `Hegel` | being, nothing, becoming; determinate negation; Fichte's triad; attempted formalizations and their limits. | — |
| 16 | `Price` | **Price List**: the empiricist trilemma; four answers side by side. | the MUS {E, N, S} and its three corrections |
| 17 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Sextus Empiricus, *Outlines of Pyrrhonism*; Montaigne, *Essays* (1580); Galileo, *Sidereus Nuncius* (1610);
Descartes, *Discourse on the Method* and *La Géométrie* (1637), *Meditations* with Objections and Replies (1641), the
correspondence with Elisabeth (1643); Spinoza, *Ethics* (1677; Curley and Elwes trans.); Leibniz, *Monadology* (1714),
the Leibniz–Clarke correspondence (1715–16); Locke, *Essay Concerning Human Understanding* (1689); Berkeley,
*Principles* (1710), *Three Dialogues* (1713), *The Analyst* (1734); Hume, *Treatise* (1739), *Enquiry* (1748); Reid,
*Inquiry* (1764); Kant, "On the first ground of the distinction of regions in space" (1768), *Critique of Pure Reason*
(1781, 1787; Guyer and Wood trans.; 李秋零 译), *Prolegomena* (1783); Hegel, *Phenomenology of Spirit* (1807),
*Science of Logic* (1812–16).

Studies and papers: Cottingham, *Descartes*; Curley, *Behind the Geometrical Method*; Garber, *Leibniz: Body,
Substance, Monad*; Gardner, *Kant and the Critique of Pure Reason* (1999); Allison, *Kant's Transcendental Idealism*
(1983); Strawson, *The Bounds of Sense* (1966); Langton, *Kantian Humility* (1998); Friedman, *Dynamics of Reason*
(2001); Reichenbach, *The Theory of Relativity and A Priori Knowledge* (1920); Dyson, Eddington and Davidson (1920);
Held et al., "The newly sighted fail to match seen with felt", *Nature Neuroscience* (2011).

## Problems and solutions

1. **What Proposition 14 rests on.** Following the citations back, Proposition 14 ("besides God, no substance") rests
   on fourteen items: Definitions 3, 5 and 6; Axioms 1, 4 and 5; and Propositions 1–7 and 11.
2. **Two analyses.** Euclid's algorithm on 1071/462 gives [2; 3, 7] and stops: the ratio is commensurable (the
   greatest common divisor is 21). On √3 it gives [1; 1, 2, 1, 2, …], repeating forever. For Leibniz the first is like a
   truth of reason, whose analysis ends in an identity; the second like a truth of fact, whose analysis never ends,
   though it has a reason that God sees whole.
3. **Descartes's method.** A circle centred at (0, k) through (2, 4) meets y = x² where y² + (1 − 2k)y + k² − r² = 0.
   For a double root at y = 4 the roots sum to 8 = 2k − 1, so k = 9/2 (and r² = 17/4). The normal from (0, 9/2) to
   (2, 4) has slope −1/4, the tangent 4: their product is −1.
4. **Hume's rival rules.** "The sun rises every day" and "the sun rises until today and never again" agree on every
   past sunrise. To prefer the first we must assume the future resembles the past. That assumption is not a relation
   of ideas (its denial is conceivable) and cannot be established from experience without assuming it, so no argument
   chooses; custom does.
5. **Kant's grid.** "Every effect has a cause" is analytic (an effect is by definition something caused). "Every event
   has a cause" is synthetic a priori for Kant (the second analogy). "A straight line is the shortest between two
   points" is Kant's own example of the synthetic a priori (B16); after general relativity, as a claim about physical
   space, it is a posteriori.
6. **(Essay) The empiricist trilemma.** A strong answer uses Chapter 16's Price List and comparison table, and meets
   the objection its exit faces: for rationalism, why reason should fit the world; for Kant, non-Euclidean space and
   the unknowable things in themselves; for radical empiricism, the apparent necessity of logic and mathematics; for the
   Aristotelian, how a few cases could show what must be.

## 习题与解答

1. **命题14依赖什么。** 沿引用回溯，命题14（“除神之外没有实体”）依赖十四项：定义3、5、6；公理1、4、5；以及命题1–7和11。
2. **两种分析。** 对1071/462运行欧几里得算法得到[2; 3, 7]并停止：这个比可公度（最大公约数是21）。对√3则得到[1; 1, 2, 1, 2, …]，永远重复。
   对莱布尼茨来说，前者像理性真理，其分析终止于一个同一式；后者像事实真理，其分析永无尽头，尽管它有一个神能完整看见的理由。
3. **笛卡尔的方法。** 以(0, k)为圆心、过(2, 4)的圆与y = x²相交于y² + (1 − 2k)y + k² − r² = 0的根处。要在y = 4处有二重根，两根之和
   8 = 2k − 1，所以k = 9/2（r² = 17/4）。从(0, 9/2)到(2, 4)的法线斜率为−1/4，切线斜率为4：乘积为−1。
4. **休谟的对立规则。** “太阳每天升起”与“太阳升到今天为止，此后再也不升”在过去的每次日出上都一致。要偏爱前者，我们必须假定未来与过去相似。
   这个假定不是观念的关系（它的否定可以设想），也不能不预设它而从经验中确立，所以没有论证能作出选择；作选择的是习惯。
5. **康德的方格。** “每个结果都有原因”是分析的（结果按定义就是被引起的东西）。“每个事件都有原因”对康德来说是先天综合的（第二类比）。
   “直线是两点之间最短的线”是康德自己举的先天综合的例子（B16）；在广义相对论之后，作为关于物理空间的断言，它是后天的。
6. **（论述题）经验论三难。** 好的回答利用第16章的代价清单和比较表，并回应其出路所面对的反驳：对理性主义，是理性为何与世界相合；对康德，是
   非欧空间与不可知的物自体；对激进经验论，是逻辑和数学看似具有的必然性；对亚里士多德主义者，是少数几个例子如何能显示必然如此。
