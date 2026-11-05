# Philosophy, Built — Part 1: Calculemus

The opening part of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)). It follows
Leibniz's dream, *let us calculate*, from its beginnings. It covers:
- the first philosophers and what an argument is;
- Zeno, Socrates and Plato;
- Aristotle's syllogistic, with all 256 moods checked by machine;
- Mohist, Nyāya and Stoic logic;
- Llull's combinatorial wheels;
- Leibniz's characteristic numbers and his reading of the Yijing as binary.

It introduces the series' devices: the Reasoner, the Wall (first brick: Zeno) and the Price List.

Every count and verdict on screen is computed by [`compute.py`](compute.py) with the Reasoner
(`explainer/philosophy/reasoner/syllogism.py` and `prop.py`, tested in `tests/philosophy/`). In particular:
- the 256 moods are checked against all 256 arrangements of the eight Venn regions (15 valid, or 24 when every term
  is inhabited);
- Leibniz's two-number semantics is checked against all 19,683 assignments built from the primes 2, 3, 5, and the
  survivors are exactly the 24 traditional moods.

Quotations name their translations.

## Build it

```bash
python -m videos.philosophy.philosophy1.compute      # seconds; cached in .cache/philosophy1
python tools/build.py philosophy1 -q l               # 480p preview
python tools/build.py philosophy1                    # 1080p30
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Leibniz's *calculemus* (1685); the unicorn syllogism, valid for the tradition and invalid for modern logic; the series map; the three devices; objectives. | — |
| 1 | `Axial` | Greece, India and China, 800–200 BCE (Jaspers's disputed "Axial Age"); Thales; reasons instead of authorities; the Milesian tradition of criticism (Popper). | — |
| 2 | `Argument` | premises and conclusion; validity and soundness; form; refutation by counterexample. | three arguments checked by the syllogism engine |
| 3 | `Zeno` | Parmenides and Zeno; Achilles in exact fractions; the geometric series and the limit; Thomson's lamp (1954) and Benacerraf (1962); **the first brick of the Wall**. | the chase's stages and the meeting time 100/9 s |
| 4 | `Euthyphro` | the dilemma (10a); Socrates' argument; **a Price List** of five claims; exits: Socrates, divine command, substitution failure. | the MUS (all five) and five MCSes |
| 5 | `Meno` | Meno's paradox (80d); the slave boy doubles the square (82b–85b); recollection; innateness to inductive bias. | the squares of side 4, 3 and the diagonal (areas 16, 9, 8) |
| 6 | `Line` | the divided line (509d); the cave (514a). | the two middle segments are equal for every ratio (exact fractions) |
| 7 | `Categorical` | the *Prior Analytics*; variables for terms; A, E, I, O; Venn diagrams; the square of opposition. | — |
| 8 | `Moods` | figures and moods; Venn regions as possible worlds; all 256 moods checked; the mnemonic names. | 15 Boolean-valid moods, by figure; a countermodel for the undistributed middle |
| 9 | `Import` | the empty world refutes Darapti; existential import gives the 24 traditional moods; **a Price List** for the unicorns (modern logic, the tradition, Strawson's presupposition). | the empty countermodel; 24 = 15 + 9 |
| 10 | `Mohists` | Mozi and the Later Mohists; *bian*; parallelizing inference and its failure (*Xiaoqu*: loving her brother is not loving a handsome man); Gongsun Long's white horse (identity vs inclusion). | — |
| 11 | `Nyaya` | the five members; *vyāpti*; the kitchen and the lake; Dignāga's three marks (Part 15). | — |
| 12 | `Llull` | the nine principles; the first figure's 36 chords; the fourth figure's three wheels (729 settings) and 84-column Table; Leibniz's *De arte combinatoria* (1666). | C(9,2) = 36, C(9,3) = 84, 9³ = 729 |
| 13 | `Leibniz` | characteristic numbers (1679); divisibility for "all"; the two-number repair; Leibniz's arithmetic models the syllogism exactly (Łukasiewicz 1951; Sotirov 1999). | five sentences in illustrative numbers; all 256 moods against 19,683 assignments: exactly the 24 traditional moods survive |
| 14 | `Yijing` | binary arithmetic (1679); Bouvet's diagram (1701); Shao Yong's order read as 0–63; what the correspondence does and does not show; *omnibus ex nihilo ducendis sufficit unum*. | the 64 hexagrams generated from their binary numerals |
| 15 | `Limits` | De Morgan's relations; nested quantifiers; the split into Parts 2 and 3. | — |
| 16 | `Outro` | recap; the Reasoner; the Wall; problems; payoffs; references. | — |

## Sources

Books:
- Kenny, *A New History of Western Philosophy*, vol. 1;
- Kneale and Kneale, *The Development of Logic*;
- Łukasiewicz, *Aristotle's Syllogistic from the Standpoint of Modern Formal Logic* (2nd ed., 1957);
- Graham, *Later Mohist Logic, Ethics and Science* (1978) and *Disputers of the Tao* (1989);
- Ganeri (ed.), *Indian Logic: A Reader* (2001);
- Matilal, *The Character of Logic in India* (1998);
- Eco, *The Search for the Perfect Language* (1995);
- Bonner, *The Art and Logic of Ramon Llull* (2007).

Texts and papers:
- Plato, *Euthyphro* 10a–11b (trans. Grube), *Meno* 80d–86c (trans. Grube) and *Republic* VI 509d–511e and VII 514a
  (trans. Grube and Reeve);
- Aristotle, *Prior Analytics* I.2 (trans. Jenkinson) and *Physics* VI.9;
- Herodotus I.74;
- Popper, "Back to the Presocratics" (1958);
- Jaspers, *Vom Ursprung und Ziel der Geschichte* (1949);
- Thomson, "Tasks and Super-Tasks" (Analysis 1954);
- Benacerraf, "Tasks, Super-Tasks, and the Modern Eleatics" (J. Phil. 1962);
- Strawson, *Introduction to Logical Theory* (1952);
- Venn, "On the Diagrammatic and Mechanical Representation of Propositions and Reasonings" (1880);
- the *Xiaoqu* (trans. after Graham);
- Gongsun Long, *Baima lun*;
- the *Nyāya Sūtra* I.1.32–39;
- Llull, *Ars brevis* (1308);
- Leibniz:
  - *Dissertatio de arte combinatoria* (1666);
  - "Elementa calculi" and "De progressione dyadica" (1679);
  - "On the General Characteristic" (trans. Loemker);
  - *The Art of Discovery* (1685, trans. Wiener);
  - "Explication de l'arithmétique binaire" (1703);
- Adams, "A Modified Divine Command Theory of Ethical Wrongness" (1973);
- Sotirov, "Arithmetizations of Syllogistic à la Leibniz" (J. Applied Non-Classical Logics 1999).

## Problems and solutions

1. **The divided line.** Cut the unit line in the ratio k : 1: the parts are k/(1+k) and 1/(1+k). Cutting each again
   in the ratio k : 1, the lower piece of the first part is (k/(1+k))·(1/(1+k)), and the upper piece of the second is
   (1/(1+k))·(k/(1+k)). These are the same product, k/(1+k)², whatever k is.
2. **Which term must be inhabited?**
   - Darapti (figure 3, AAI): all M are P, all M are S, so some S are P. It needs **M** inhabited: any M is then both
     S and P.
   - Bramantip (figure 4, AAI): all P are M, all M are S, so some S are P. It needs **P** inhabited: any P is then M,
     hence S.
   - The Reasoner confirms both: each mood's countermodel empties that term, and adding "that term is inhabited" to
     the premises makes the mood valid.
3. **Barbara in Leibniz's numbers.**
   - "All M are P" means P⁺ | M⁺ and P⁻ | M⁻. "All S are M" means M⁺ | S⁺ and M⁻ | S⁻.
   - Divisibility is transitive, so P⁺ | S⁺ and P⁻ | S⁻: all S are P.
   - This holds for every assignment, not only those our search tried.
4. **Llull's combinatorics.**
   - Sixteen principles need C(16, 2) = 120 chords.
   - Four wheels of nine letters have 9⁴ = 6,561 settings.
5. **Thomson's lamp.**
   - The story fixes the lamp's state only at times before t = 1, and in every interval before 1 the lamp is
     switched again. So no state before 1 is "the last".
   - The sequence of states on, off, on, … has no limit, just as 1 − 1 + 1 − … has no sum.
   - Any final state is consistent with everything the story says (Benacerraf 1962). The question "on or off?" has
     no answer the description determines.
6. **(Essay) Is the *Euthyphro* dilemma a false dilemma?** Strong answers:
   - defend substitution failure, since "because" is hyperintensional and grounding claims track which name is used;
   - or a modified divine command theory: Adams (1973) grounds the good in God's loving nature rather than in
     arbitrary will, which answers the arbitrariness horn;
   - or Socrates' own exit.

   Say what each costs.

## 习题与解答

1. **线段的分割。** 把单位长线段按k∶1分割，两段为k/(1+k)和1/(1+k)。再把每段按k∶1分割，第一段的下半部分是(k/(1+k))·(1/(1+k))，第二段的上半
   部分是(1/(1+k))·(k/(1+k))。两者是同一个乘积k/(1+k)²，与k无关。
2. **哪个词项必须非空？**
   - Darapti（第三格AAI）：所有M是P，所有M是S，所以有些S是P。它需要**M**非空：任一M既是S又是P。
   - Bramantip（第四格AAI）：所有P是M，所有M是S，所以有些S是P。它需要**P**非空：任一P是M，从而是S。
   - 推理机证实了这两点：每个式的反模型都恰好把那个词项清空，而把“该词项非空”加入前提后，这个式就有效了。
3. **莱布尼茨数字中的Barbara。**
   - “所有M是P”即P⁺ | M⁺且P⁻ | M⁻；“所有S是M”即M⁺ | S⁺且M⁻ | S⁻。
   - 整除具有传递性，所以P⁺ | S⁺且P⁻ | S⁻：所有S是P。
   - 这对每一种赋数都成立，而不只是我们搜索过的那些。
4. **柳利的组合数。**
   - 十六个原则需要C(16, 2) = 120条弦。
   - 四个各有九个字母的转盘有9⁴ = 6561种设置。
5. **汤姆森的灯。**
   - 故事只规定了t = 1之前各时刻灯的状态，而在1之前的每一段时间里灯都会再被切换一次，所以1之前没有“最后一个”状态。
   - 状态序列“开、关、开……”没有极限，正如1 − 1 + 1 − ……没有和。
   - 任何最终状态都与故事所说的一切相容（贝纳塞拉夫1962）。“开还是关？”这个问题，在描述所决定的范围内没有答案。
6. **（论述题）游叙弗伦两难是假两难吗？** 好的回答可以：
   - 为“替换失效”辩护：“因为”是超内涵的，根据关系会追踪所用的是哪个名称；
   - 或者采用修正的神命论：亚当斯（1973）把善建立在上帝慈爱的本性上，而不是任意的意志上，从而回应“任意性”那一角；
   - 或者采纳苏格拉底自己的出路。

   并说明每条出路的代价。
