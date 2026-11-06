# Philosophy, Built — Part 8: The Liar

Part 8 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): truth and paradox. Eubulides,
the Later Mohists, Bhartṛhari and the medieval *insolubilia*; Tarski's three ingredients, his satisfaction definition
and his hierarchy, and Kripke's Nixon–Jones objection; Grelling, Richard, Berry and Priest's inclosure schema;
Kripke's fixed points, built and run, with grounded, ungrounded and paradoxical sentences, the intrinsic fixed point
and the transfinite construction over arithmetic; the liar as a non-terminating program and least-fixed-point
semantics; revenge, Field's determinacy hierarchy and contextualism; revision theory; Curry's paradox, its kinship
with Löb's theorem, strict-tolerant logic and the validity Curry; Yablo's staircase; dialetheism, LP and naive set
theory; the Price List; the axiomatic theories TB, CT, KF and FS and the conservativeness debate; correspondence,
coherence, pragmatism, identity and deflation, Davidson's truth-conditional semantics and the slingshot; the surprise
exam in dynamic epistemic logic and the knower; and Moore's paradox. Its brick in **the Wall** is "The liar": a
language cannot hold its own truth predicate without a gap, a glut or a hierarchy. Its **Price List** is the liar:
classical logic, the T-schema, self-reference, and no true contradictions.

Every value, fixed point, revision sequence, staircase, run and check on screen is computed by the Reasoner's truth
module (`explainer/philosophy/reasoner/truth.py`: strong Kleene evaluation of a language with its own truth
predicate, Kripke's jump and its stages, every fixed point and Kripke's classification, the exclusion-negation
revenge, revision sequences over every starting hypothesis, finite Yablo staircases, Grelling's adjectives, Tarski's
satisfaction clauses on a small model, strict-tolerant consequence, the T-biconditionals in K3 and LP, the surprise
exam as public announcement, the sentences run as recursive programs, and Moore's paradox in KD4), tested in
`tests/philosophy/test_truth.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy8.compute        # every computed item (a few seconds; cached in .cache/philosophy8)
python tools/build.py philosophy8 -q l                 # 480p preview
python tools/build.py philosophy8                      # 1080p30 -> renders/philosophy8.mp4
python tools/qa_scene.py philosophy8 Kripke            # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | the liar, both ways round; four ways out; the plan. | — |
| 1 | `Ancient` | Eubulides, Chrysippus and Epimenides; the Later Mohists (Canon B 71); Bhartṛhari's "unnameable"; Bradwardine and Buridan. | — |
| 2 | `Tarski` | the T-schema, self-reference and classical logic (1933); satisfaction and Convention T; the hierarchy; Kripke's Nixon and Jones (1975). | l ↔ ¬l unsatisfiable; Tarski's clauses on a three-object model, all 66 sentences to depth 2 |
| 3 | `Family` | Grelling–Nelson (1908); Richard (1905); Berry; Priest's inclosure schema (1994). | eight adjectives sorted, and "heterological" with no consistent value |
| 4 | `Kripke` | one language with its own truth predicate; strong Kleene; the construction as learning. | a world of 13 sentences, and the jump stage by stage to the least fixed point |
| 5 | `Fixed` | every fixed point; grounded, ungrounded and paradoxical; the intrinsic fixed point; ω₁^CK and Burgess (1986). | all three fixed points; Kripke's classification of the 13 |
| 6 | `Programs` | sentences as recursive programs; ungrounded = non-terminating; Tarski (1955), Scott (1969); parallel and sequential "or". | the 13 run as programs, matching the least fixed point |
| 7 | `Revenge` | the strengthened liar; the exclusion liar has no fixed point; Field (2008); contextualism (Parsons, Burge 1979, Glanzberg 2004); **the Wall's eighth brick**. | the exclusion liar's jump oscillating, and no fixed point among its three values |
| 8 | `Revision` | Gupta and Herzberger (1982), Gupta–Belnap (1993); limit rules. | two revision sequences; verdicts over all 8,192 starting hypotheses |
| 9 | `Curry` | Curry (1942); contraction; Curry and Löb; strict-tolerant logic (Cobreros, Égré, Ripley, van Rooij 2012); the validity Curry (Beall–Murzi 2013). | c ↔ (c → q) ⊨ q; ST: ⊢ T⌜L⌝ and T⌜L⌝ ⊢ q valid, ⊢ q not |
| 10 | `Yablo` | Yablo's staircase (1993); finite truncations; Ketland's ω-inconsistency; Priest (1997), Sorensen, Cook (2014). | every truncation to 1–8 sentences has exactly one consistent assignment |
| 11 | `Glut` | dialetheism and LP (Priest 1979); the same construction read as gluts; the T-schema in K3 and LP; prices; naive set theory (Brady 1989, Weber 2010). | the least fixed point read as gaps and as gluts; each T-biconditional's value |
| 12 | `Price` | **Price List**: the liar; four answers side by side. | the MUS {C, T, S, N} and its four corrections |
| 13 | `Axioms` | TB, CT, KF, FS (Halbach); KF's axioms; conservativeness and deflationism (Shapiro 1998, Ketland 1999, Field 1999). | — |
| 14 | `Theories` | Aristotle and the Mohists; correspondence, coherence, pragmatism, identity, deflation; Davidson (1967); the slingshot (Church, Gödel, Davidson); Horwich's minimalism. | — |
| 15 | `Exam` | the surprise exam (O'Connor 1948); Gerbrandy's announcement analysis (2007); the knower (Kaplan–Montague 1960), in five lines. | the backward elimination; the announcement iterated: {1..5}, {1..4}, …, ∅ |
| 16 | `Moore` | Moore's paradox (1942); Hintikka's analysis (1962); unsuccessful updates. | p ∧ ¬Bp satisfiable, B(p ∧ ¬Bp) unsatisfiable on every KD4 frame up to three worlds |
| 17 | `Outro` | recap; the Reasoner's truth module; the Wall; problems; payoffs; references. | — |

## Sources

Books: Kripke, "Outline of a theory of truth" (1975); Gupta and Belnap, *The Revision Theory of Truth* (1993); Field,
*Saving Truth from Paradox* (2008); Priest, *In Contradiction* (1987, 2nd ed. 2006) and *Beyond the Limits of Thought*
(1995); Halbach, *Axiomatic Theories of Truth* (2011); Beall, Glanzberg and Ripley, *Formal Theories of Truth* (2018);
Maudlin, *Truth and Paradox* (2004); Sorensen, *A Brief History of the Paradox* (2003); Cook, *The Yablo Paradox*
(2014); Chow, "The surprise examination or unexpected hanging paradox" (1998).

Papers and texts: *Mojing*, Canon B 71; Aristotle, *Metaphysics* Γ 7; Bhartṛhari, *Vākyapadīya*; Bradwardine,
*Insolubilia* (c. 1324); Buridan, *Sophismata*; Richard (1905); Russell (1908); Grelling and Nelson (1908); Ramsey
(1927); Tarski (1933, 1944, 1955); Curry (1942); Moore (1942); O'Connor (1948); Quine (1953); Kaplan and Montague
(1960); Hintikka (1962); Davidson, "Truth and meaning" (1967) and "True to the facts" (1969); Scott (1969); Parsons
(1974); Burge (1979); Priest (1979, 1994, 1997); Gupta (1982); Herzberger (1982); McGee (1985); Burgess (1986);
Friedman and Sheard (1987); Brady (1989); Horwich (1990); Feferman (1991); Yablo (1993); Houben (1995); Shapiro
(1998); Ketland (1999, 2005); Field (1999); Glanzberg (2004); Gerbrandy (2007); Weber (2010); Cobreros, Égré, Ripley
and van Rooij (2012); Beall and Murzi (2013).

## Problems and solutions

1. **Two truth-tellers.** A says "B is true", B says "A is true". The jump gives A the value of B and B the value of A,
   so the fixed points are exactly the assignments with A = B: both t, both f, or both n. Two are classical. The least
   fixed point leaves both n, so both are ungrounded but not paradoxical, like the single truth-teller.
2. **Kripke versus revision.** Let S be "the liar is true or the liar is not true", T⌜L⌝ ∨ ¬T⌜L⌝. In every fixed
   point the liar is n (Chapter 5), so S has value n ∨ ¬n = n in every fixed point: it is paradoxical, and excluded
   middle fails for it. In revision theory every hypothesis gives the liar a classical value, so S is a classical
   instance of excluded middle at every stage after the first: stably true. (The Reasoner's verdicts agree: s8 is
   paradoxical in Chapter 5 and stably true in Chapter 8.)
3. **Grelling on the Price List.** (i) Every adjective is autological or heterological (classical logic); (ii) an
   adjective is heterological iff it does not apply to itself (the defining biconditional, a T-schema for
   "applies to"); (iii) "heterological" is an adjective of the language (self-reference); (iv) it cannot be both
   (consistency). Steps (i)–(iv) yield: heterological iff not heterological. Each Price List exit removes one step.
4. **Finite Yablo.** With Y₁…Yₙ, Yₙ says nothing, so it is true. Then Yₙ₋₁ ("Yₙ is untrue") is false, and every
   earlier Yₖ is false because Yₙ is a true later sentence. That assignment satisfies every biconditional, and it is
   forced: by backward induction from Yₙ, each value is determined. So there is exactly one.
5. **The knower.** Let K ↔ ¬Kn⌜K⌝. From Kn⌜K⌝ → K (factivity) and K → ¬Kn⌜K⌝ we get ¬Kn⌜K⌝, hence K. That derivation
   used only known principles, so its conclusion K is known: Kn⌜K⌝. Contradiction.
6. **(Essay) Gap, glut, hierarchy or restriction?** A strong answer uses Chapter 12's Price List and the comparison
   table, and meets its own revenge: for a gap, "not determinately true"; for a glut, "just true" and Curry; for a
   hierarchy, the single word "true" and Nixon and Jones; for a restriction, asserting sentences one calls untrue.

## 习题与解答

1. **两个真话者。** A说“B是真的”，B说“A是真的”。跳跃给A以B的值、给B以A的值，所以不动点恰好是A = B的那些指派：都为t、都为f或都为n。
   其中两个是经典的。最小不动点让两者都为n，所以两者都是无根的但不是悖论的，就像单个的真话者。
2. **克里普克与修正论。** 设S为“说谎者为真或说谎者不为真”，即T⌜L⌝ ∨ ¬T⌜L⌝。在每个不动点中说谎者都是n（第5章），所以S在每个不动点中
   的值都是n ∨ ¬n = n：它是悖论的，排中律对它不成立。在修正论中，每个假设都给说谎者一个经典值，所以S在第一阶段之后的每个阶段都是排中律的
   一个经典实例：稳定地真。（推理机的裁决与此一致：s8在第5章是悖论的，在第8章是稳定地真的。）
3. **代价清单上的格雷林悖论。** (i) 每个形容词要么自谓要么他谓（经典逻辑）；(ii) 一个形容词是他谓的当且仅当它不适用于自身（定义性的双条件句，
   即“适用于”的T模式）；(iii) “他谓的”是这门语言中的一个形容词（自指）；(iv) 它不能两者都是（一致性）。由(i)–(iv)得出：他谓的当且仅当
   不是他谓的。代价清单上的每条出路各去掉其中一步。
4. **有限的亚布罗序列。** 对Y₁…Yₙ，Yₙ什么都没说，所以为真。于是Yₙ₋₁（“Yₙ不真”）为假，而每个更早的Yₖ都为假，因为Yₙ是一个为真的后续句子。
   这个指派满足每个双条件句，而且是被迫的：从Yₙ逆向归纳，每个值都被确定。所以恰有一个。
5. **知者悖论。** 设K ↔ ¬Kn⌜K⌝。由Kn⌜K⌝ → K（事实性）和K → ¬Kn⌜K⌝得¬Kn⌜K⌝，从而K。这个推导只用到已知的原则，所以它的结论K是被知道的：
   Kn⌜K⌝。矛盾。
6. **（论述题）空隙、过剩、层级还是限制？** 好的回答利用第12章的代价清单和比较表，并回应它自己的复仇：对空隙，是“不确定地为真”；对过剩，是
   “仅仅为真”和柯里；对层级，是单一的“真”字以及尼克松与琼斯；对限制，是断言自己称为不真的句子。
