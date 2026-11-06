# Philosophy, Built — Part 22: Possible Worlds

Part 22 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the metaphysics of modality,
from the semantics of Part 4 to the engineering that runs on it today. Modal talk everywhere (could, must, would,
fragile), and five questions. De re and de dicto: the number of planets on three worlds, Quine's three grades of modal
involvement, his mathematical cyclist evaluated on a model (both de dicto claims true, both de re claims false), and
the replies of Marcus and Kripke. Names: the description theory (Frege, Russell, Searle), Kripke's modal argument drawn
across four worlds (the name tracks Aristotle; the description tracks whoever taught Alexander), the epistemic and
semantic arguments (Gödel and Schmidt, Feynman), and the causal picture with Evans's Madagascar. The necessary
*a posteriori*: Hesperus and Phosphorus, the four boxes of necessity and a priority, Putnam's Twin Earth, and the
contingent a priori (the standard metre; Evans's Julius). Lewis's modal realism: concrete isolated worlds,
recombination, actuality as an indexical, propositions as sets of worlds (eight worlds drawn), and the incredulous
stare with the other objections. Counterpart theory: Lewis's 1968 postulates, the translation scheme, Humphrey and
Nixon on four islands with counterpart bridges (both the direct semantics and the first-order translation give: might
have won, true; necessity of identity and of distinctness, false), a census of every small model (16 896 counterpart
models, 64 Kripke models) showing which principles fail where, and Kripke's Humphrey objection with Lewis's reply and
its payoff for Part 21's statue. Ersatz worlds: linguistic, Plantinga's, Stalnaker's and Armstrong's; Carnap's sixteen
state descriptions; Lewis's two objections (primitive modality; alien properties, counted: 256 genuine worlds, only 160
descriptions in the actual vocabulary); actualism. Necessitism: the Barcan formula (1946), Wittgenstein's possible
child on a contingentist and a necessitist model, Williamson (2013), and Prior's proof that quantified S5 forces the
formula. Conceivability: Descartes's argument, where the bridge seems to fail, Yablo's and Chalmers's distinctions, and
Kripke's diagnosis. Two-dimensional semantics: the matrix of `water = H₂O` filled cell by cell over Earth, Twin Earth
and a third world, then six sentences classified into all four boxes by their diagonals and actual rows; the bridge to
Part 31's zombies; and **the Wall's twenty-second brick**. Kripke's puzzle about belief (Pierre and Londres) as a
**Price List**, and Paderewski. Fine's counterexamples to the modal account of essence, tabulated, and essence as real
definition. Impossible worlds: why intensions are too coarse, Nolan's counterpossibles computed (vacuous on possible
worlds; discriminating with impossible ones), and what impossible worlds are for. Dispositions: the conditional
analysis against finks, reverse finks and masks, with Lewis's reformed analysis checked on all four cases; powers.
Possible worlds at work: verification, epistemic protocols, counterfactual fairness; a counterfactual explanation of a
credit decision found by searching 462 worlds (four tie for closest: Lewis against Stalnaker, and actionable recourse);
and Sato's distribution semantics on a ProbLog program (eight worlds; P(calls) = 0.196).

Every number on screen is computed by the Reasoner's new module `explainer/philosophy/reasoner/worlds.py`, tested in
`tests/philosophy/test_worlds.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy22.compute       # every computed item (seconds; .cache/philosophy22)
python tools/build.py philosophy22 -q l                # 480p preview
python tools/build.py philosophy22                     # 1080p30 -> renders/philosophy22.mp4
python tools/qa_scene.py philosophy22 TwoD             # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Lewis (1973); modal talk; worlds as semantics and as metaphysics; five questions; the plan. | — |
| 1 | `DeRe` | Quine (1953, 1960); Marcus (1961); Kripke (1980). | the planets on three worlds; the cyclist on a model |
| 2 | `Rigid` | Frege; Russell; Searle (1958); Kripke (1970); Evans (1973). | a name and a description across four worlds |
| 3 | `Aposteriori` | Hesperus and Phosphorus; Kant (1781); Putnam (1975); Wittgenstein; Kripke; Evans (1979). | — |
| 4 | `Realism` | Lewis (1973, 1986); Forrest and Armstrong (1984). | propositions as sets of eight worlds |
| 5 | `Counterparts` | Lewis (1968, 1971); Kripke (1980); Gibbard (1975). | Lewis's translation; Humphrey's islands; the census of small models |
| 6 | `Ersatz` | Carnap (1947); Plantinga (1974); Stalnaker (1976); Armstrong (1989); Lewis (1986). | sixteen state descriptions; alien properties counted |
| 7 | `Necessitism` | Barcan (1946); Kripke (1963); Prior (1956); Williamson (2013). | the Barcan formula on two models |
| 8 | `Conceive` | Descartes (1641); Hume (1739); Yablo (1993); Chalmers (2002); Kripke (1970). | — |
| 9 | `TwoD` | Stalnaker (1978); Davies and Humberstone (1980); Chalmers and Jackson (2001); Chalmers (2006); **the Wall's twenty-second brick**. | six two-dimensional matrices and their classes |
| 10 | `Pierre` | Kripke (1979); Salmon (1986); Soames (2002); Kripke's puzzle as a **Price List**. | the conflict and its exits |
| 11 | `Essence` | Kripke on origins; Fine (1994); Lowe; Hale (2013). | the modal account against real essence |
| 12 | `Impossible` | Nolan (1997); Hintikka; Williamson (2007); Berto and Jago (2019). | counterpossibles on six worlds |
| 13 | `Dispositions` | Ryle (1949); Carnap (1936); Martin (1994); Johnston (1992); Bird (1998, 2007); Lewis (1997); Mumford. | two analyses on four struck objects |
| 14 | `Industry` | Kusner et al. (2017); Wachter, Mittelstadt and Russell (2017); Stalnaker (1968); Lewis (1973); Ustun et al. (2019); Sato (1995); De Raedt et al. (2007). | the closest worlds that flip a decision; a ProbLog query over eight worlds |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Kripke, *Naming and Necessity* (1980); Lewis, *Counterfactuals* (1973) and *On the Plurality of Worlds* (1986);
Plantinga, *The Nature of Necessity* (1974); Armstrong, *A Combinatorial Theory of Possibility* (1989); Williamson,
*Modal Logic as Metaphysics* (2013); Gendler and Hawthorne (eds.), *Conceivability and Possibility* (2002);
García-Carpintero and Macià (eds.), *Two-Dimensional Semantics* (2006); Hale, *Necessary Beings* (2013); Berto and
Jago, *Impossible Worlds* (2019); Bird, *Nature's Metaphysics* (2007); Menzel, "Possible Worlds" (*Stanford
Encyclopedia of Philosophy*, 2021).

Papers: Barcan (1946); Quine (1953, 1956); Prior (1956); Searle (1958); Marcus (1961); Kripke (1963, 1979); Lewis
(1968, 1971, 1997); Stalnaker (1968, 1976, 1978); Evans (1973, 1979); Adams (1974); Putnam (1975); Davies and
Humberstone (1980); Forrest and Armstrong (1984); Salmon (1986); Johnston (1992); Yablo (1993); Fine (1994); Martin
(1994); Sato (1995); Nolan (1997); Bird (1998); Chalmers and Jackson (2001); Chalmers (2002, 2006); De Raedt, Kimmig and
Toivonen (2007); Wachter, Mittelstadt and Russell (2017); Kusner, Loftus, Russell and Silva (2017); Ustun, Spangher and
Liu (2019).
