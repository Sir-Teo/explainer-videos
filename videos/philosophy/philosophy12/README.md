# Philosophy, Built — Part 12: Knowledge Among Many

Part 12 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): epistemic logic, common
knowledge and social epistemology. Hintikka's knowledge as a box, the axioms of S5 and their frames, belief as KD45
with Moore's paradox and Stalnaker's combination, negative introspection and logical omniscience; three agents with
three cards, public announcements, and Cheryl's birthday; the muddy children, solved to n = 8; common knowledge as a
tower and as reachability, Aumann's partitions, Lewis's conventions and Chwe's rituals; the coordinated attack and
Halpern and Moses's theorem (the Wall's twelfth brick); Byzantine generals, FLP, Paxos and Raft, and Bitcoin's
probabilistic finality; Rubinstein's email game and Monderer and Samet's common p-belief; Aumann's agreement theorem,
the Geanakoplos–Polemarchakis dialogue and the no-trade theorem; public announcement logic, product updates and lies;
the Russian cards problem; Moore sentences and Fitch's paradox, with a Price List; testimony (Hume, Reid, Coady),
miracles by Bayes, and epistemic injustice (Fricker); peer disagreement and higher-order evidence; Galton's ox, the
diversity prediction theorem, Hayek and prediction markets; and Zollman's networks of scientists, with Nguyen's
bubbles and echo chambers.

Every model, count and verdict on screen is computed by the Reasoner's module for knowledge among many
(`explainer/philosophy/reasoner/epistemic.py`): multi-agent S5 models with K, E and C; public announcements and a
product update; the muddy children for any n; Cheryl's birthday; the coordinated attack's tower of mutual knowledge;
the email game's best-response iteration and its p-beliefs; the agreement dialogue; the Russian cards check over all
consistent deals; Fitch's conjunction by tableau; Nakamoto's catch-up probabilities; the diversity identity; and the
Zollman simulator with recorded belief trajectories. It is tested in `tests/philosophy/test_epistemic.py` and cached
by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy12.compute       # every computed item (about ten seconds; .cache/philosophy12)
python tools/build.py philosophy12 -q l                # 480p preview
python tools/build.py philosophy12                     # 1080p30 -> renders/philosophy12.mp4
python tools/qa_scene.py philosophy12 Muddy            # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | the tower of "knows that"; the muddy children as the running puzzle; the plan. | — |
| 1 | `Hintikka` | knowledge as a box (1962); K, T, 4, 5 and their frames; belief as KD45, Moore's paradox, Stalnaker (2006); the critics. | — |
| 2 | `Cards` | three cards, six worlds, one colour per agent; a public announcement (Plaza 1989); Cheryl's birthday. | six nested knowledge claims; who knows what after "I hold 0"; July 16 after three announcements |
| 3 | `Muddy` | the cube of worlds; the children's reasoning; eight children. | 8 → 7 → 4 worlds; round 2 for the muddy two; 256 → 255 → 247 → 219 → 163 → 93; nothing without the father |
| 4 | `Common` | E, E², …, C; common knowledge as reachability; Aumann's meet; Lewis (1969); Chwe (2001). | the height of the tower before the father spoke: none, E, E² |
| 5 | `Attack` | the coordinated attack (Gray 1978; Halpern and Moses 1990); the proof; **the Wall's twelfth brick**. | after n delivered messages, Eⁿ⁻¹ and never C |
| 6 | `Systems` | Byzantine generals (1982), FLP (1985), Paxos and Raft; Nakamoto (2008). | all 45 pairs of the 10 majorities of five overlap; Nakamoto's catch-up probabilities |
| 7 | `Email` | Rubinstein's email game (1989); Monderer and Samet's common p-belief (1989). | best responses unravel, type by type, to "never attack"; every informed general's belief 0.526 that his last email was lost |
| 8 | `Agree` | Aumann (1976); Geanakoplos and Polemarchakis (1982); Milgrom and Stokey (1982). | 1/3, 1/2, 1/3, then agreement at 1/3 |
| 9 | `Actions` | public announcement logic and its reduction axioms; Baltag, Moss and Solecki (1998); lies. | the product update of a private reading |
| 10 | `Russian` | the Russian cards problem (2000; van Ditmarsch 2003). | the Fano-plane announcement: Bob learns in all 28 consistent deals; Cath learns nothing |
| 11 | `Fitch` | Moore sentences; Fitch (1963; Church 1945); **Price List**: Fitch's triad. | an announcement that falsifies itself; K(q ∧ ¬Kq) unsatisfiable with T, satisfiable without |
| 12 | `Testimony` | Hume, Reid, Coady (1992); miracles by Bayes; Fricker's epistemic injustice (2007). | the posterior of a one-in-a-million miracle for witnesses of three reliabilities |
| 13 | `Peers` | Christensen's restaurant (2007); equal weight, steadfast, total evidence; higher-order evidence. | 9/19 = 0.47 after disagreement |
| 14 | `Crowds` | Galton's ox (1907); the diversity prediction theorem; a shared bias; Hayek (1945) and prediction markets. | the identity on a toy fair of 800 guesses, with and without a shared bias |
| 15 | `Networks` | Zollman (2007); belief trajectories; Nguyen (2020). | 500 runs per network: cycle 89% right in ~123 rounds, complete 53% in ~11 |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Hintikka, *Knowledge and Belief* (1962); Lewis, *Convention* (1969); Hume, *Enquiry* §10 (1748); Reid,
*Inquiry* (1764); Hayek, "The Use of Knowledge in Society" (1945); Galton, "Vox Populi", *Nature* (1907); Fagin,
Halpern, Moses and Vardi, *Reasoning About Knowledge* (1995); van Ditmarsch, van der Hoek and Kooi, *Dynamic
Epistemic Logic* (2007); Coady, *Testimony* (1992); Fricker, *Epistemic Injustice* (2007); Page, *The Difference*
(2007); Chwe, *Rational Ritual* (2001); Lackey and Christensen (eds.), *The Epistemology of Disagreement* (2013).

Papers: Fitch (1963); Aumann (1976); Gray (1978); Lamport, Shostak and Pease (1982); Geanakoplos and Polemarchakis
(1982); Milgrom and Stokey (1982); Fischer, Lynch and Paterson (1985); Plaza (1989); Rubinstein (1989); Monderer and
Samet (1989); Halpern and Moses (1990); Lamport (1998); Baltag, Moss and Solecki (1998); van Ditmarsch (2003, 2014);
Stalnaker (2006); van Benthem, van Eijck and Kooi (2006); Christensen (2007, 2010); Elga (2007); Zollman (2007);
Nakamoto (2008); Kelly (2010); Ongaro and Ousterhout (2014); Lasonen-Aarnio (2014); Nguyen (2020).

## Problems and solutions

1. **The cards.** After Ann announces "I hold 0", two worlds remain, 012 and 021, and Ann cannot tell them apart: she
   still does not know whether Bob holds 1 or 2. Her announcement told the others about her card; it told her nothing
   new.
2. **Four children, two muddy.** Start: 16 worlds. The father's announcement removes 0000: 15. The first "nobody
   knows" removes the four worlds with exactly one muddy child: 11 (0011, 0101, 0110, 0111, 1001, 1010, 1011, 1100,
   1101, 1110, 1111). In the actual world 1100, the two muddy children now know (round 2); when they say so, the two
   clean ones learn that the world is 1100 (round 3).
3. **One agent.** With one agent, Eφ is Kφ, so E²φ is KKφ, which in S5 is equivalent to Kφ, and every Eᵏφ (k ≥ 1)
   is Kφ. So Cφ, the conjunction of all of them, is just Kφ = E²φ: for a single S5 agent, common knowledge is
   knowledge.
4. **A new dialogue.** With the event {1, 5} and actual state 1: A says 1/3; B says 1/4; this tells A the state is
   in {1, 2, 3, 4}, which leaves A's cell {1, 2, 3} and A says 1/3 again; that tells B the state is not 4 (where A
   would now say 0), and B's cell becomes {1, 2, 3}: both say 1/3.
5. **Hume's witness.** With reliability r = 0.999, the posterior P·r / (P·r + (1 − P)(1 − r)) is below a half exactly
   when P < (1 − r) = 0.001: any event rarer than one in a thousand stays more likely false than true after her
   report.
6. **(Essay) Disagreement.** A strong answer applies Chapter 13's computation to a real case, says who counts as a
   peer and why, and meets the strongest objection to its policy: spinelessness for equal weight, arrogance for
   steadfastness, and indeterminacy for total evidence.

## 习题与解答

1. **纸牌。** 安宣布“我拿着0”之后，剩下两个世界012和021，而安分不清它们：她仍然不知道鲍勃拿的是1还是2。她的宣告告诉了别人她的牌，却没有
   告诉她自己任何新东西。
2. **四个孩子，两个脸上有泥。** 开始：16个世界。父亲的宣告去掉0000：剩15个。第一次“没人知道”去掉恰有一个孩子有泥的四个世界：剩11个（0011、
   0101、0110、0111、1001、1010、1011、1100、1101、1110、1111）。在实际世界1100中，两个有泥的孩子此时知道了（第2轮）；他们说出来以后，两个
   干净的孩子得知世界是1100（第3轮）。
3. **一个主体。** 只有一个主体时，$E\varphi$就是$K\varphi$，所以$E^2\varphi$是$KK\varphi$，在S5中它等价于$K\varphi$，每个$E^k\varphi$（$k \geq 1$）
   都是$K\varphi$。所以$C\varphi$，即它们全体的合取，就是$K\varphi = E^2\varphi$：对单个S5主体而言，共同知识就是知识。
4. **一段新的对话。** 事件为$\{1, 5\}$、实际状态为1时：A说1/3；B说1/4；这告诉A状态在$\{1, 2, 3, 4\}$中，A的格子仍是$\{1, 2, 3\}$，A再说1/3；
   这又告诉B状态不是4（在那里A此时会说0），于是B的格子变成$\{1, 2, 3\}$：两人都说1/3。
5. **休谟的证人。** 可靠度$r = 0.999$时，后验$P r / (P r + (1 - P)(1 - r))$小于一半，恰当$P < 1 - r = 0.001$：任何比千分之一更罕见的事件，
   在她报告之后仍然更可能为假。
6. **（论述题）分歧。** 好的回答把第13章的计算用于一个真实案例，说明谁算同行以及为什么，并回应其策略所面对的最强反驳：对平等权重，是没有主见；
   对坚持己见，是傲慢；对全部证据，是不确定。
