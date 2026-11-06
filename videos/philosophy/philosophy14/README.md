# Philosophy, Built — Part 14: Changing Your Mind

Part 14 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): belief revision,
conditionals and defeasible reasoning. Expansion, revision and contraction on a detective's spheres; revision versus
update (Katsuno and Mendelzon); the recovery debate (Hansson's Cleopatra); the eight AGM revision postulates and six
contraction postulates, checked exhaustively for four operators, with Satoh's failure of subexpansion; Grove's
spheres, partial meet contraction, the Levi and Harper identities and entrenchment; Spohn's ranking functions as
orders of magnitude, four iterated operators against the Darwiche–Pearl postulates, and the forgotten red bird; the
material, strict and relevant conditionals, Oswald and Kennedy, and the Ramsey test; Gärdenfors's impossibility
theorem, proved on three worlds; Stalnaker and Lewis on counterfactuals, five classic countermodels, the limit
assumption, Fine's Nixon and Lewis's priorities, and counterfactual explanations in machine learning; Adams's thesis,
Lewis's triviality theorem (proved on three worlds and checked by exhaustive search), imaging, and the triviality
cluster as a Price List (the Wall's fourteenth brick, with Gärdenfors); McGee's counterexample to modus ponens and the
miners; Reiter's default logic, the Nixon diamond, circumscription, negation as failure and the Yale shooting
problem; KLM's System P, rational monotonicity, Adams's ε-semantics and System Z with its drowning problem; Dung's
argumentation frameworks; and truth maintenance, database repairs and knowledge editing in language models.

Every verdict on screen is computed by three new Reasoner modules. `explainer/philosophy/reasoner/revision.py`: AGM
operations on rankings and spheres, the postulates checked over every pair of propositions, Dalal, Satoh and Winslett
operators, partial meet contraction, the Levi and Harper identities, entrenchment, four iterated operators and the
Darwiche–Pearl check, and Gärdenfors's theorem. `cond.py`: counterfactual models with Lewis's truth condition, the
five countermodels, Lewis's triviality proof and the exhaustive search, imaging, and McGee's numbers. `argue.py`:
Reiter extensions, System Z, the KLM rules on ranked and preferential models, and Dung's semantics with labellings.
They are tested in `tests/philosophy/test_revision.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy14.compute       # every computed item (a few seconds; .cache/philosophy14)
python tools/build.py philosophy14 -q l                # 480p preview
python tools/build.py philosophy14                     # 1080p30 -> renders/philosophy14.mp4
python tools/qa_scene.py philosophy14 Trivial          # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Quine (1951); the black swan; the plan. | — |
| 1 | `Moves` | expansion, revision, contraction; revision vs update (Katsuno and Mendelzon 1991); recovery (Hansson 1991). | the detective's three moves; the book and the magazine |
| 2 | `AGM` | Alchourrón, Gärdenfors and Makinson (1985); eight revision and six contraction postulates. | the postulates for spheres, Dalal, Satoh and Winslett over 255² pairs; Satoh's counterexample |
| 3 | `Spheres` | Grove (1988); remainders and partial meet contraction; Levi and Harper; entrenchment (1988). | four revisions; four remainders, maxichoice and full meet; both identities; entrenchment 1, 1, 2, 3 |
| 4 | `Iterated` | Spohn's ranks (1988), as orders of magnitude; natural, lexicographic, Spohn and amnesic revision; Darwiche and Pearl (1997). | DP1–DP4 for four operators; the red bird remembered and forgotten |
| 5 | `Ramsey` | the material conditional; strict and relevant conditionals; Oswald and Kennedy (Adams 1970); the Ramsey test (1929). | the detective's conditional, read off the spheres |
| 6 | `Gardenfors` | monotonicity and preservation; **Gärdenfors's impossibility** (1986); Levi, Grahne. | every candidate for H * (B ∨ C) fails |
| 7 | `Counter` | Stalnaker (1968), Lewis (1973); five failures; the limit assumption; Fine (1975) and Lewis (1979); counterfactual explanations (Wachter et al. 2017). | five countermodels; CEM once the tie is broken; a loan's L1 and L2 explanations |
| 8 | `Trivial` | Adams's and Stalnaker's theses; **Lewis's triviality** (1976); imaging; **Price List**: the triviality cluster; **the Wall's fourteenth brick**. | the three-world proof; no proposition fits on four or three worlds; imaging 0.6 vs conditioning 0.5 |
| 9 | `McGee` | McGee (1985); import–export; Kratzer's restrictors; the miners (Kolodny and MacFarlane 2010). | the 1980 probabilities |
| 10 | `Defaults` | Tweety; Reiter (1980); the Nixon diamond; circumscription; negation as failure; the Yale shooting problem (1986); Gottlob (1992). | Tweety's extensions; two Nixon extensions; two minimal Yale models |
| 11 | `KLM` | preferential models (KLM 1990); System P; rational monotonicity; Adams's ε-semantics; System Z (Pearl 1990); Makinson and Gärdenfors (1991). | the rules on a ranked and a preferential model; Z-layers and six queries |
| 12 | `Argue` | Dung (1995); grounded, preferred, stable; a trial; uses in law, negotiation, argument mining and LLM debate. | three small frameworks and two trials, labelled |
| 13 | `Machines` | truth maintenance (Doyle 1979); database repairs (Arenas et al. 1999); knowledge editing (ROME, MEMIT; Cohen et al. 2024). | certain answers; AGM revision vs a local edit |
| 14 | `Outro` | recap; the Reasoner's modules; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Gärdenfors, *Knowledge in Flux* (1988); Hansson, *A Textbook of Belief Dynamics* (1999); Lewis,
*Counterfactuals* (1973); Adams, *The Logic of Conditionals* (1975); Bennett, *A Philosophical Guide to Conditionals*
(2003); Edgington, "Indicative Conditionals" (SEP); Makinson, *Bridges from Classical to Nonmonotonic Logic* (2005);
Spohn, *The Laws of Belief* (2012); Baroni et al. (eds.), *Handbook of Formal Argumentation* (2018).

Papers: Ramsey (1929); Quine (1951); Stalnaker (1968); Adams (1970); Lewis (1976, 1979); Fine (1975); Reiter (1978,
1980); McCarthy (1980); Doyle (1979); Alchourrón, Gärdenfors and Makinson (1985); McGee (1985); Gärdenfors (1986);
Hanks and McDermott (1986); Kratzer (1986); de Kleer (1986); Grove (1988); Spohn (1988); Dalal (1988); Satoh (1988);
Gärdenfors and Makinson (1988); Kraus, Lehmann and Magidor (1990); Pearl (1990); Katsuno and Mendelzon (1991);
Makinson and Gärdenfors (1991); Hansson (1991); Gottlob (1992); Lehmann and Magidor (1992); Boutilier (1993); Nayak
(1994); Dung (1995); Darwiche and Pearl (1997); Grahne (1998); Arenas, Bertossi and Chomicki (1999); Prakken (2010);
Kolodny and MacFarlane (2010); Wachter, Mittelstadt and Russell (2017); Khoo and Mandelkern (2019); Meng et al.
(2022, 2023); Cohen et al. (2024).

## Problems and solutions

1. **Revise and contract.** K = {pq}. The most plausible ¬p world is p̄q, at rank 2, so K * ¬p = {p̄q}. Contracting p
   adds the most plausible ¬p world to K: K ÷ p = {pq, p̄q}, which still believes q but no longer p.
2. **Full meet revision.** Full meet revision is sphere revision with two spheres, K and everything. If K ∩ A ∩ B is
   nonempty, then K * A = K ∩ A and K * (A ∧ B) = K ∩ A ∩ B = (K * A) ∩ B; if K ∩ A is nonempty but K ∩ A ∩ B is
   empty, (K * A) ∩ B is empty, so K*7 holds and K*8's antecedent fails; if K ∩ A is empty, both sides are A ∩ B.
3. **Remembering.** Naturally, revising by ¬q puts pq̄ at 0 and keeps pq, p̄q, p̄q̄ in order; revising then by q
   returns to pq: p and q are believed. Amnesically, after ¬q everything but pq̄ is at rank 1, so revising by q leaves
   pq and p̄q tied: the belief in p, which neither piece of news concerned, is lost.
4. **A tie.** Take an actual world where A is false and two A-worlds equally close to it, one with B and one without.
   The closest A-worlds include both, so neither "if A, B" nor "if A, ¬B" holds: conditional excluded middle fails,
   as in Bizet and Verdi.
5. **Lewis with new numbers.** P(C | A) = 0.5 / 0.75 = 2/3. Conditioning on C forces X to contain AC; on ¬C, to miss
   AC̄ and ĀC̄. So X = {AC} and P(X) = 0.5 ≠ 2/3.
6. **A framework.** a is unattacked, so in; b is out. c and d attack each other, so the grounded extension is {a},
   with c and d undecided. The preferred, and stable, extensions are {a, c} and {a, d}; the complete ones are {a},
   {a, c} and {a, d}.

## 习题与解答

1. **修正与收缩。** $K = \{pq\}$。最可信的$\lnot p$世界是秩为2的$\bar p q$，所以$K * \lnot p = \{\bar p q\}$。收缩$p$时把最可信的$\lnot p$世界加入$K$：
   $K \div p = \{pq, \bar p q\}$，它仍相信$q$，但不再相信$p$。
2. **全交修正。** 全交修正就是只有两个球面（$K$与全体）的球面修正。若$K \cap A \cap B$非空，则$K * A = K \cap A$，
   $K * (A \land B) = K \cap A \cap B = (K * A) \cap B$；若$K \cap A$非空而$K \cap A \cap B$为空，则$(K * A) \cap B$为空，K*7成立，K*8的前件不成立；
   若$K \cap A$为空，两边都是$A \cap B$。
3. **记住。** 用自然修正，按$\lnot q$修正把$p\bar q$放到0，$pq$、$\bar p q$、$\bar p \bar q$保持原序；再按$q$修正回到$pq$：$p$和$q$都被相信。
   用失忆修正，按$\lnot q$修正后除$p\bar q$外一切都在秩1，于是按$q$修正后$pq$与$\bar p q$并列：对$p$的信念——两条消息都与它无关——丢失了。
4. **并列。** 取一个$A$为假的实际世界，以及两个与它同样接近的$A$世界，一个有$B$、一个没有。最近的$A$世界包括两者，所以“如果$A$，$B$”与
   “如果$A$，$\lnot B$”都不成立：条件排中律失效，正如比才与威尔第的例子。
5. **换个数字的刘易斯证明。** $P(C \mid A) = 0.5 / 0.75 = 2/3$。以$C$为条件迫使$X$包含$AC$；以$\lnot C$为条件，迫使它不含$A\bar C$与
   $\bar A \bar C$。所以$X = \{AC\}$，$P(X) = 0.5 \neq 2/3$。
6. **一个论辩框架。** $a$不受攻击，所以在内；$b$在外。$c$与$d$相互攻击，所以根基外延是$\{a\}$，$c$和$d$未定。偏好外延（也是稳定外延）是
   $\{a, c\}$和$\{a, d\}$；完全外延是$\{a\}$、$\{a, c\}$和$\{a, d\}$。
