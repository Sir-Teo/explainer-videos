# Philosophy, Built — Part 27: Sense and Reference

Part 27 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), the first part of Act VI,
*Mind and Meaning*: the philosophy of language, from names to formal semantics, with a working semantic parser built.
Gongsun Long's white horse, with 'is' read as identity and as inclusion on a herd of six horses; the later Mohists'
three kinds of name, and Mill. Frege's puzzle (Hesperus and Phosphorus), his own example computed (the three
pairwise intersections of a triangle's medians, one point), sense and reference for names, predicates and
sentences, and indirect contexts. Russell's theory of descriptions in first-order logic, both scopes of negation
drawn as trees and evaluated in four models; Strawson's truth-value gaps against Russell's values; incomplete
descriptions and domain restriction; Donnellan's referential and attributive uses at a party, and Kripke's speaker's
reference. Kripke's three arguments against descriptivism: rigid designation across four worlds, Gödel and Schmidt,
the necessary a posteriori, and the causal-historical picture, with Evans's Madagascar. Putnam's Twin Earth, the
division of linguistic labour, Burge's arthritis, narrow content and self-knowledge. Kaplan's character and content,
'I am here now' in all eight proper contexts of a small model (a priori, contingent in four), the two-dimensional
matrix for 'water = H₂O' (necessary a posteriori) and 'water is the watery stuff' (contingent a priori), and
Schlenker's monsters. Tarski's Convention T, a T-sentence derived step by step, Davidson's programme and Foster's
problem (two truth theories agreeing on all 99 sentences in the actual world, and differing on 29 in another).
Montague's types and the λ-calculus, 'every student smokes' β-reduced step by step; a Heim–Kratzer parser (FA, PM,
PA, QR) that interprets every node of a tree, 'Ann likes every student' after quantifier raising, and both scopes of
'every student read a book'. Generalized quantifiers: conservativity checked on 256 pairs of sets (only 'only'
fails), the 512 conservative relations among 65 536 on a two-element universe, monotonicity profiles, and an
Ehrenfeucht–Fraïssé game proving that 'most' is not first-order. Intensions and logical omniscience (786 formulas,
15 propositions, 212 tautologies all one set of worlds). Belief reports: Lois Lane, Frege's puzzle as a **Price
List** (Frege; Salmon and Soames; Crimmins and Perry), Kripke's Pierre, and **the Wall's twenty-seventh brick**.
Donkey sentences and dynamic predicate logic, checked against first-order translations on 400 random models, and
discourse representation. Meaning in machines: the parser's logical forms compiled to SQL and run in sqlite, the
benchmarks (FraCaS, Spider, SCAN, COGS, MED), an inference suite whose gold labels are theorems, and the reversal
curse.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/semantics.py` (with
`fol` for Russell's formulas and `prop` for the Price List), tested in `tests/philosophy/test_semantics.py` and cached
by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy27.compute       # every computed item (seconds; .cache/philosophy27)
python tools/build.py philosophy27 -q l                # 480p preview
python tools/build.py philosophy27                     # 1080p30 -> renders/philosophy27.mp4
python tools/qa_scene.py philosophy27 Parser           # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Frege (1892); four questions; the plan. | — |
| 1 | `Names` | Gongsun Long (c. 300 BCE); the later Mohist canons; Mill (1843). | the white horse: inclusion and identity |
| 2 | `Frege` | Frege (1892): sense and reference; compositionality; indirect contexts. | the medians' intersections |
| 3 | `Russell` | Russell (1905); Ramsey; descriptivism. | three formulas in four models |
| 4 | `Strawson` | Strawson (1950); incomplete descriptions; Donnellan (1966); Kripke (1977). | gaps against values; domain restriction; the party |
| 5 | `Kripke` | Kripke (1970/1980); Searle (1958); Evans (1973). | rigid designation across four worlds |
| 6 | `Twin` | Putnam (1975); Burge (1979); Fodor (1987). | Oscar and his twin; the arthritis patient |
| 7 | `Kaplan` | Kaplan (1977/1989); Stalnaker; Chalmers; Schlenker (2003). | 8 contexts for 'I am here now'; three 2-D matrices |
| 8 | `Tarski` | Tarski (1933); Davidson (1967, 1973); Foster (1976). | a T-sentence derived; Foster's two theories on 99 sentences |
| 9 | `Montague` | Montague (1970); Church. | types in the model; β-reduction step by step |
| 10 | `Parser` | Heim and Kratzer (1998). | every node of three trees; both scopes |
| 11 | `Quantifiers` | Barwise and Cooper (1981); Keenan and Stavi (1986); Ehrenfeucht (1961); Fraïssé (1954). | conservativity on 256 pairs; 512 of 65 536; monotonicity; EF games for k = 1..4 |
| 12 | `Intensions` | Carnap (1947); Lewis; Stalnaker; Hintikka (1962); Berto and Jago (2019). | 786 formulas, 15 propositions |
| 13 | `Belief` | Salmon (1986); Soames; Crimmins and Perry (1989); Kripke (1979); **the Price List**; **the Wall's twenty-seventh brick**. | — |
| 14 | `Donkey` | Geach (1962); Kamp (1981); Heim (1982); Groenendijk and Stokhof (1991). | DPL against first-order on 400 models |
| 15 | `Machines` | FraCaS (1996); Yu et al. (2018); Lake and Baroni (2018); Kim and Linzen (2020); Yanaka et al. (2019); Berglund et al. (2023); Mandelkern and Linzen. | SQL in sqlite; an inference suite proved |
| 16 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Problems and solutions

1. Give Russell's analysis of 'the author of *Waverley* is not Scott' in both scopes; find a model separating them.

   *Solution.* With $W$ for "wrote Waverley" and $s$ for Scott: narrow scope (the description outside the negation), $\exists x\,(Wx \land \forall y\,(Wy \to y = x) \land x \ne s)$, "exactly one person wrote Waverley, and it was not Scott". Wide scope (the negation outside), $\lnot\exists x\,(Wx \land \forall y\,(Wy \to y = x) \land x = s)$, "it is not the case that Scott and Scott alone wrote Waverley". They come apart when there is no unique author. In a model with Scott and Tom where nobody wrote Waverley (or where both wrote it together), the narrow reading is false and the wide reading true.

2. Draw the two-dimensional matrix for 'I am here now', with contexts as rows.

   *Solution.* Take two proper contexts: $c_1$, Ann in Paris at noon in world $w_1$, and $c_2$, Ann in Rome at noon in $w_2$ (in $w_1$ she is in Paris, in $w_2$ in Rome). Rows are contexts, columns circumstances of evaluation. Row $c_1$: the content is "Ann is in Paris at noon", true at $w_1$, false at $w_2$. Row $c_2$: "Ann is in Rome at noon", false at $w_1$, true at $w_2$. The diagonal (each context evaluated at its own world) is true, as it is for every proper context: the sentence cannot be uttered falsely, a logical truth in Kaplan's logic. But no row is true throughout, so what it says is contingent: Ann might have been elsewhere.

3. Write a truth theory for 'and', 'or' and 'not' that Foster's trick cannot fool. What did you add?

   *Solution.* The clauses: "$\varphi$ and $\psi$" is true iff $\varphi$ is true and $\psi$ is true; "$\varphi$ or $\psi$" iff at least one is; "not $\varphi$" iff $\varphi$ is not true; plus one clause per atomic sentence. Foster's deviant theory changes a clause (say, "snow is white" is true iff grass is green, or "$\varphi$ and $\psi$" is true iff both are true and the earth moves) and still yields only true T-sentences in the actual world. To stop it, require more than truth: every axiom must hold as a law, true in every world of the model, as the film's comparison across worlds does. In a world where grass is not green the deviant atomic clause makes false predictions, so it is ruled out. What was added is modal strength (Davidson's lawlikeness), with T-sentences derived canonically from the axioms.

4. Interpret 'no student read every book' in both scopes; build a model where they differ.

   *Solution.* Surface scope: $\lnot\exists s\,(\text{Student}(s) \land \forall b\,(\text{Book}(b) \to \text{Read}(s, b)))$, "no student read all the books". Inverse scope: $\forall b\,(\text{Book}(b) \to \lnot\exists s\,(\text{Student}(s) \land \text{Read}(s, b)))$, "every book went unread by every student". Model: students $s_1, s_2$, books $b_1, b_2$, with $s_1$ having read only $b_1$ and $s_2$ only $b_2$. No student read both books, so the surface reading is true; but $b_1$ was read, so the inverse reading is false. (The inverse reading entails the surface one whenever there is at least one book.)

5. Prove that 'at least half' is conservative and right-upward but neither way on the left.

   *Solution.* "At least half the A are B" is $|A \cap B| \ge |A|/2$. Conservative: the condition mentions only $A$ and $A \cap B$, and $A \cap (A \cap B) = A \cap B$, so it holds of $(A, B)$ iff it holds of $(A, A \cap B)$. Right-upward monotone: if $B \subseteq B'$ then $|A \cap B'| \ge |A \cap B| \ge |A|/2$. Not left-upward: with $A = \{a\} \subseteq A' = \{a, b, c\}$ and $B = \{a\}$, it holds of $(A, B)$ ($1 \ge 1/2$) and fails of $(A', B)$ ($1 < 3/2$). Not left-downward: with $A' = \{a, b\}$, $A = \{b\}$, $B = \{a\}$, it holds of $(A', B)$ ($1 \ge 1$) and fails of $(A, B)$ ($0 < 1/2$).

6. Show by an Ehrenfeucht–Fraïssé game that 'there is an even number of $P$' is not first-order.

   *Solution.* Fix $k$ and compare two structures in which everything is P: one with $2k$ elements, one with $2k + 1$. In each of $k$ rounds, Spoiler picks an element in either structure; Duplicator answers with the element matched to it before if Spoiler repeats one, and otherwise with a fresh element of the other structure, which always exists since each has at least $k$ elements. After $k$ rounds the chosen elements match one-for-one, with equalities and the predicate P preserved, so Duplicator wins. By the Ehrenfeucht–Fraïssé theorem the two structures agree on every sentence of quantifier depth $k$. One has an even number of P's and the other an odd number, and every first-order sentence has some finite depth, so no first-order sentence says "there is an even number of P".

## Sources

Texts: Lycan, *Philosophy of Language* (3rd ed., 2019); Kripke, *Naming and Necessity* (1980); Heim and Kratzer,
*Semantics in Generative Grammar* (1998); Gamut, *Logic, Language, and Meaning* (1991); Peters and Westerståhl,
*Quantifiers in Language and Logic* (2006); Speaks, "Theories of Meaning" (*Stanford Encyclopedia of Philosophy*).

Papers and primary texts: Gongsun Long, *Bai Ma Lun*; the later Mohist canons; Mill (1843); Frege (1892); Russell
(1905); Tarski (1933); Carnap (1947); Strawson (1950); Searle (1958); Ehrenfeucht (1961); Geach (1962); Hintikka (1962);
Donnellan (1966); Davidson (1967, 1973); Montague (1970); Kripke (1970/1980, 1977, 1979); Evans (1973); Putnam (1975);
Foster (1976); Kaplan (1977/1989); Burge (1979); Barwise and Cooper (1981); Kamp (1981); Heim (1982); Keenan and Stavi
(1986); Salmon (1986); Fodor (1987); Crimmins and Perry (1989); Groenendijk and Stokhof (1991); FraCaS (1996); Soames
(2002); Schlenker (2003); Lake and Baroni (2018); Yu et al. (2018); Yanaka et al. (2019); Kim and Linzen (2020);
Berglund et al. (2023); Mandelkern and Linzen (2024).
