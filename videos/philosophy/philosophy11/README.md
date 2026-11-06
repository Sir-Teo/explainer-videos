# Philosophy, Built — Part 11: What Is Knowledge?

Part 11 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the second part of Act III.
Plato's three answers in the *Theaetetus* and the tether of the *Meno*; justified true belief; Gettier's two cases
(1963), built as first-order models; the older cases (Dharmottara's mirage, Russell's clock, Chisholm's sheep) and
the lucky arrow; the repairs (no false lemmas and Barn County, defeasibility and Tom Grabit) and Zagzebski's recipe;
Goldman's reliabilism and the generality problem, Norman and Truetemp; Nozick's tracking and Kripke's red barn;
safety, the garbage chute and the lottery; Sosa's archer, credit and Pritchard's anti-luck virtue epistemology;
Williamson's knowledge first, anti-luminosity and the failure of KK on the unmarked clock; the brain in a vat and
the closure argument as a Price List; Moore and Wittgenstein's hinges, Dretske's zebra, Lewis's contextualism and
DeRose's bank, Putnam's semantic argument; Zhuangzi's butterfly and the Pyrrhonists; foundations, coherence and
infinite chains, with Bayesian coherence and the Bovens–Hartmann impossibility; internalism, externalism and the new
evil demon; Quine's two dogmas and the web of belief; and experimental philosophy's Gettier studies and their
replications. Its brick in **the Wall** is "Gettier": no fallibilist analysis escapes Gettier cases, and no
condition that can change gradually is luminous.

Every case and verdict on screen is computed by the Reasoner's module for knowledge
(`explainer/philosophy/reasoner/knowledge.py`): Gettier's cases as first-order structures, with the inference
checked by the tableau prover and the belief evaluated in the actual and a nearby world; scenarios of worlds ordered
by similarity, with sensitivity (Nozick), adherence and safety (Sosa, Williamson) computed for each belief;
Zagzebski's recipe; reliability of process types over a toy population, and the generality problem; margins for
error on a cold morning and an unmarked clock (K without KK); Lewis's rule of relevant alternatives; Shogenji's and
Olsson's coherence measures and the posterior given independent reports; and every minimal revision of a Quinean web,
by SAT. It is tested in `tests/philosophy/test_knowledge.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy11.compute       # every computed item (a second; .cache/philosophy11)
python tools/build.py philosophy11 -q l                # 480p preview
python tools/build.py philosophy11                     # 1080p30 -> renders/philosophy11.mp4
python tools/qa_scene.py philosophy11 Tracking         # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Socrates's question; Ann's working clock and Ben's stopped one; the plan. | — |
| 1 | `Plato` | *Theaetetus*: perception, true judgment (the jury), true judgment with an account; *Meno*'s statues; JTB. | — |
| 2 | `Gettier` | Gettier's two assumptions and two cases. | each inference valid (a closed tableau); each belief true in the actual model and false in a nearby one; the false lemma |
| 3 | `Older` | Dharmottara's mirage (c. 770); Russell (1948); Chisholm (1966); the lucky arrow. | — |
| 4 | `Repairs` | Clark's no false lemmas and Barn County; Lehrer–Paxson defeasibility and Tom Grabit; Zagzebski (1994). | the recipe run on the doctor: every condition short of truth survives; safety fails |
| 5 | `Reliable` | Goldman (1979); the generality problem (Conee and Feldman 1998); Norman (BonJour 1980), Truetemp (Lehrer 1990). | one look, five process types: 94%, 96%, 10%, 10%, 100% |
| 6 | `Tracking` | Nozick's four conditions; Kripke's red barn; sensitivity and closure. | the closest not-p worlds in the coins, barns and vat models |
| 7 | `Safety` | Sosa (1999), Williamson (2000), Pritchard (2005); the chute; the lottery. | a scorecard: true, sensitive, safe for seven beliefs |
| 8 | `Virtue` | Sosa's AAA; Greco's credit; Lackey's Chicago visitor; Pritchard's anti-luck virtue epistemology. | — |
| 9 | `First` | Williamson: knowledge first, E = K; anti-luminosity; **the Wall's eleventh brick**. | 25 moments of a cold morning: the two that are cold but not knowably cold |
| 10 | `KK` | Hintikka (1962) and axiom 4; margins break transitivity; the unmarked clock. | p, Kp, KKp, KKKp end at 20, 19, 18, 17 |
| 11 | `Skeptic` | the brain in a vat; closure; **Price List**: the skeptic's triad. | the MUS {S1, S2, S3} and its three corrections |
| 12 | `Answers` | Moore (1939) and Wittgenstein's hinges; Dretske's zebra (1970); Lewis (1996) and DeRose's bank; Putnam (1981). | Lewis's rule in the careless and careful contexts |
| 13 | `Butterfly` | Zhuangzi's dream; Sextus: equipollence, *epochē*, *ataraxia*; Apelles's sponge. | — |
| 14 | `Structure` | **Price List**: Agrippa's regress; foundations, Neurath's boat, Klein's infinitism; Bayesian coherence. | the more coherent of two report sets is less likely true when witnesses are good; the curves cross at x = 1/2 |
| 15 | `Internal` | internalism and externalism; the chicken sexer; the new evil demon (Lehrer and Cohen 1983). | — |
| 16 | `Quine` | "Two Dogmas" (1951): the analyticity circle; the web; Putnam's quantum logic (1968). | the five minimal revisions of the Uranus–Mercury web; Neptune (1846), Vulcan, general relativity (1915) |
| 17 | `XPhi` | Weinberg, Nichols and Stich (2001); Nagel et al. (2013), Kim and Yuan (2015), Seyedsayamdost (2015), Machery et al. (2017), Cova et al. (2021); Williamson and Cappelen on the method of cases. | — |
| 18 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Plato, *Theaetetus* (Fowler and Levett trans.), *Meno*; Sextus Empiricus, *Outlines of Pyrrhonism*;
*Zhuangzi*, ch. 2 (Watson trans.); Descartes, *Meditations* (1641); Moore, "Proof of an External World" (1939);
Wittgenstein, *On Certainty* (1969); Quine, "Two Dogmas of Empiricism" (1951); Gettier, "Is Justified True Belief
Knowledge?" (1963); Hintikka, *Knowledge and Belief* (1962); Nozick, *Philosophical Explanations* (1981), ch. 3;
Putnam, *Reason, Truth and History* (1981), ch. 1; Lewis, "Elusive Knowledge" (1996); Williamson, *Knowledge and
Its Limits* (2000) and *The Philosophy of Philosophy* (2007); Sosa, *A Virtue Epistemology* (2007).

Papers: Clark (1963); Lehrer and Paxson (1969); Dretske, "Epistemic Operators" (1970); Klein (1971); Goldman,
"Discrimination and Perceptual Knowledge" (1976) and "What Is Justified Belief?" (1979); BonJour (1980); Lehrer and
Cohen (1983); Cohen (1984); Lehrer, *Theory of Knowledge* (1990); DeRose (1992); Zagzebski, "The Inescapability of
Gettier Problems" (1994); Conee and Feldman, "The Generality Problem for Reliabilism" (1998); Sosa, "How to Defeat
Opposition to Moore" (1999); Shogenji (1999); Weinberg, Nichols and Stich (2001); Bovens and Hartmann, *Bayesian
Epistemology* (2003); Hawthorne, *Knowledge and Lotteries* (2004); Olsson, *Against Coherence* (2005); Stanley,
*Knowledge and Practical Interests* (2005); Lackey (2007); Greco, *Achieving Knowledge* (2010); Kripke, "Nozick on
Knowledge" (2011); Pritchard, "Anti-Luck Virtue Epistemology" (2012); Cappelen, *Philosophy without Intuitions*
(2012); Nagel, San Juan and Mar (2013); Kim and Yuan (2015); Seyedsayamdost (2015); Machery et al., "Gettier
Across Cultures" (2017); Cova et al. (2021). Textbooks: Pritchard, *What Is This Thing Called Knowledge?*; Nagel,
*Knowledge: A Very Short Introduction* (2014).

## Problems and solutions

1. **Gettier's lemma.** In Case II the false lemma is "Jones owns a Ford". A case with no false lemma: Barn County,
   where Henry's perceptual belief is not inferred from anything. A case with inference but no false lemma (after
   Feldman 1974): Smith reasons from true premises only, "Nogot, who works in my office, has shown me papers saying
   he owns a Ford", to "someone in my office owns a Ford"; Nogot was lying, but Havit, also in the office, owns one.
2. **The recipe for 99% reliability.** Step one: a 99%-reliable thermometer, on one of its rare bad days, reads 20°
   when the room is 17°; the belief "it is 20°" is reliably formed and false. Step two: the heating has just pushed
   the room to exactly 20°, independently of the fault. The belief is true, believed, and from a 99%-reliable
   process, but a nearby world (the heating a minute later) has the same belief false: not safe, not knowledge.
3. **Kripke's barns under safety.** "There is a red barn" is safe: in every nearby world where Henry believes it, it
   is true (the only world that would fool him, a red facade, is far away). "There is a barn" formed by looking is
   unsafe (a green facade is nearby). Formed by deduction from "there is a red barn", it is safe: in the nearby
   worlds where Henry believes it on that basis, there is a red barn. Safety is relative to the basis of the belief,
   and closure under competent deduction survives.
4. **A wider margin.** With a margin of two marks, Kp holds where the hand is at 18 or below and KKp at 16 or below:
   each K strips two marks.
5. **KK and margins.** In a margin model, Kp at w requires p at w + 1, KKp requires Kp at w + 1 and so p at w + 2,
   and in general Kⁿp requires p at w + n. If KK held, Kp would give Kⁿp for every n, so p would hold at every
   position from w on; but p ("at most 20") is false at 21. So Kp could hold nowhere: margins and KK together make
   knowledge of p impossible.
6. **(Essay) The skeptic.** A strong answer uses Chapter 11's Price List and states the price of each exit: for
   Moore, an argument that seems to beg the question; for Dretske and Nozick, abominable conjunctions; for the
   contextualist, that "knows" shifts as conversations do, and that the skeptic wins whenever she is listened to.

## 习题与解答

1. **盖蒂尔的引理。** 在案例二中，假的引理是“琼斯有一辆福特”。没有假引理的案例：谷仓县，亨利的知觉信念不是从任何东西推出来的。有推理但
   没有假引理的案例（仿费尔德曼1974）：史密斯只从真前提推理，“我办公室的诺格特给我看过他有一辆福特的文件”，推出“我办公室里有人有一辆福特”；
   诺格特在撒谎，但同在办公室的哈维特确实有一辆。
2. **对99%可靠性运用配方。** 第一步：一支99%可靠的温度计，在它少有的坏日子里，房间是17°时显示20°；“现在是20°”这一信念由可靠过程形成，
   却是假的。第二步：暖气恰好把房间加热到正好20°，与故障无关。这个信念为真、被相信、来自99%可靠的过程，但在一个邻近世界里（暖气晚开一分钟）
   同样的信念是假的：不安全，不是知识。
3. **安全性下的克里普克谷仓。** “那里有一座红谷仓”是安全的：在亨利相信它的每个邻近世界里它都为真（唯一能骗过他的红色假门面离得很远）。
   靠观看形成的“那里有一座谷仓”不安全（附近有绿色的假门面）。如果它是从“那里有一座红谷仓”演绎出来的，它就是安全的：在亨利基于这一根据相信它的
   邻近世界里，都有一座红谷仓。安全性相对于信念的根据，在有能力的演绎下封闭性得以保留。
4. **更宽的误差余量。** 误差余量为两格时，指针在18或以下时$Kp$成立，在16或以下时$KKp$成立：每个$K$剥掉两格。
5. **KK与误差余量。** 在误差余量模型中，$w$处的$Kp$要求$w+1$处有$p$，$KKp$要求$w+1$处有$Kp$，从而$w+2$处有$p$；一般地，$K^np$要求
   $w+n$处有$p$。如果KK成立，$Kp$就会给出对每个$n$的$K^np$，于是从$w$起每个位置都有$p$；但$p$（“至多20”）在21处为假。所以$Kp$在哪里都
   不能成立：误差余量与KK合在一起，使对$p$的知识成为不可能。
6. **（论述题）怀疑论者。** 好的回答利用第11章的代价清单，并说明每个出路的代价：对摩尔，是一个看似窃取论题的论证；对德雷斯克和诺齐克，是
   “可憎的合取”；对语境主义者，是“知道”随对话而移动，而且怀疑论者只要有人听她讲就会获胜。
